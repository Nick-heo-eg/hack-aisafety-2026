"""H-002 — Hallucinated tool result.

Two layers:
1. **Heuristic floor** — explicit success keywords ("완료", "succeeded").
   Fast, no external dependency.
2. **Optional judge** — semantic check for paraphrased success claims
   ("이미 조치되었습니다") that bypass keywords. See verifier.judges.

The judge layer is opt-in: pass a `Judge` to `detect()`. Without one,
the detector behaves exactly as the v0 heuristic. This keeps default
detection deterministic and side-effect-free, while letting callers
add semantic verification without changing other code.
"""

from __future__ import annotations

from verifier.findings import Finding
from verifier.judges.base import Judge
from verifier.observer import ToolLogEntry
from verifier.trace import AgentStep, ToolCall, ToolResult, TraceEvent

PATTERN_ID = "H-002"

_SUCCESS_KEYWORDS = (
    "완료",
    "완료했",
    "처리했",
    "성공",
    "completed",
    "succeeded",
    "done",
    "처리 완료",
)


def _claims_success(content: str) -> bool:
    lower = content.lower()
    return any(kw.lower() in lower for kw in _SUCCESS_KEYWORDS)


def detect(
    trace: list[TraceEvent],
    tool_logs: list[ToolLogEntry],
    *,
    judge: Judge | None = None,
) -> list[Finding]:
    """Compare agent claims against tool-side ground truth.

    Returns a Finding for each agent_step that claims success while
    the tool's own log records error or empty for a referenced call_id.

    If `judge` is provided, agent claims that the heuristic does NOT
    flag are passed to the judge as a paraphrase fallback. A Finding
    from the judge cites the judge name in its summary so the source
    of evidence is auditable.
    """
    findings: list[Finding] = []

    log_status_by_call: dict[str, str] = {
        e.call_id: e.status for e in tool_logs if e.call_id is not None
    }
    log_entry_by_call: dict[str, ToolLogEntry] = {
        e.call_id: e for e in tool_logs if e.call_id is not None
    }

    last_failed_call_id: str | None = None
    failure_steps: list[int] = []

    for ev in trace:
        if isinstance(ev, ToolCall):
            log_status = log_status_by_call.get(ev.call_id)
            if log_status in ("error", "empty"):
                last_failed_call_id = ev.call_id
                failure_steps = [ev.step]
        elif isinstance(ev, ToolResult):
            if ev.status in ("error", "empty"):
                last_failed_call_id = ev.call_id
                failure_steps = [ev.step]
            elif (
                ev.call_id == last_failed_call_id
                and ev.status == "ok"
            ):
                # Trace overrides tool log with a false 'ok' — still a lie.
                failure_steps.append(ev.step)
        elif isinstance(ev, AgentStep):
            if last_failed_call_id is None:
                continue

            verdict_source: str | None = None
            if _claims_success(ev.content):
                verdict_source = "heuristic"
            elif judge is not None:
                entry = log_entry_by_call.get(last_failed_call_id)
                if entry is not None:
                    v = judge.evaluate(
                        agent_claim=ev.content,
                        tool_log_entry=entry,
                    )
                    if v == "mismatch":
                        verdict_source = f"judge:{judge.name}"

            if verdict_source is not None:
                findings.append(
                    Finding(
                        pattern_id=PATTERN_ID,
                        run_id=ev.run_id,
                        agent_id=ev.agent_id,
                        trigger_step=ev.step,
                        evidence_steps=list(failure_steps),
                        summary=(
                            f"[{verdict_source}] Agent claims success "
                            f"at step {ev.step} after tool call "
                            f"{last_failed_call_id} failed "
                            f"(tool log status != ok)."
                        ),
                    )
                )
                last_failed_call_id = None
                failure_steps = []

    return findings
