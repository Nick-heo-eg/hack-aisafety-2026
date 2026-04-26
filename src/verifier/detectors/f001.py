"""F-001 — Silent fallback on tool failure.

Heuristic (v0): a tool_result with status in {error, empty} that is
followed (within the same run+agent, before any other tool_call to the
same name) by an agent_step whose content does NOT contain any
acknowledgement keyword is reported as F-001.

Acknowledgement keywords are a deliberately small, anglocentric set
for v0. False positives on multilingual traces are a known limit
captured in docs/taxonomy.md and ADR-0003.
"""

from __future__ import annotations

import re

from verifier.findings import Finding
from verifier.trace import AgentStep, ToolCall, ToolResult, TraceEvent

PATTERN_ID = "F-001"

# Word-boundary matched, case-insensitive. Kept narrow on purpose:
# a wider list overfits to phrasing and inflates false negatives.
_ACK_TERMS = (
    r"error",
    r"errors",
    r"fail",
    r"failed",
    r"failing",
    r"failure",
    r"retry",
    r"retrying",
    r"abort",
    r"aborted",
    r"sorry",
    r"unable",
    r"could ?n[o']t",
    r"can ?n[o']t",
    r"try again",
    r"no (results?|data|rows?|records?)",
    r"empty",
    r"timed? ?out",
)
_ACK_RE = re.compile(r"\b(?:" + "|".join(_ACK_TERMS) + r")\b", re.IGNORECASE)


def _acknowledges_failure(text: str) -> bool:
    return bool(_ACK_RE.search(text))


def detect(events: list[TraceEvent]) -> list[Finding]:
    findings: list[Finding] = []

    # Index a "pending failed result" per (run_id, agent_id, tool_name).
    # Cleared when (a) a confirming agent_step arrives, (b) a fresh
    # tool_call to the same name supersedes it, or (c) detection fires.
    pending: dict[tuple[str, str, str], ToolResult] = {}

    for ev in events:
        if isinstance(ev, ToolResult):
            if ev.status in ("error", "empty"):
                pending[(ev.run_id, ev.agent_id, ev.name)] = ev
            else:
                pending.pop((ev.run_id, ev.agent_id, ev.name), None)
            continue

        if isinstance(ev, ToolCall):
            # A retry / re-call replaces the prior pending result for this tool;
            # whether that retry handles the failure is F-003's concern, not ours.
            pending.pop((ev.run_id, ev.agent_id, ev.name), None)
            continue

        if isinstance(ev, AgentStep):
            # Any pending failed result in this run+agent that is *not*
            # acknowledged by this step is F-001 evidence.
            stale_keys = [
                k for k in pending if k[0] == ev.run_id and k[1] == ev.agent_id
            ]
            if not stale_keys:
                continue
            if _acknowledges_failure(ev.content):
                # Step explicitly acknowledges; clear all pending for this agent.
                for k in stale_keys:
                    pending.pop(k, None)
                continue
            for k in stale_keys:
                bad = pending.pop(k)
                findings.append(
                    Finding(
                        pattern_id=PATTERN_ID,
                        run_id=ev.run_id,
                        agent_id=ev.agent_id,
                        trigger_step=ev.step,
                        evidence_steps=[bad.step, ev.step],
                        summary=(
                            f"agent_step at step {ev.step} proceeds without "
                            f"acknowledging {bad.status} result of tool "
                            f"{bad.name!r} at step {bad.step}"
                        ),
                    )
                )
            continue

        # state_read / state_write / spawn / terminate do not affect F-001.

    return findings
