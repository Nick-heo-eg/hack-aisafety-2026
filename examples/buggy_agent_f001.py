"""A toy agent that intentionally exhibits F-001 (silent fallback).

Run:
    python examples/buggy_agent_f001.py

Writes a trace JSONL to runs/buggy_f001_<timestamp>.jsonl that the
F-001 detector should flag. Used as a *testbed* for the detector —
distinct from hand-written fixtures because the trace is produced by
real running code, not authored by the same person who wrote the
detector.

The "bug" is in the agent's decision logic, not in the trace emission:
the agent calls a tool, receives an explicit error, and proceeds as
if it had received valid data. Verifier-on-trace, not verifier-on-code.
"""

from __future__ import annotations

import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

# Allow `python examples/buggy_agent_f001.py` from repo root without install.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from verifier.trace import (  # noqa: E402
    AgentStep,
    Terminate,
    ToolCall,
    ToolResult,
    TraceEvent,
    dump_jsonl,
)


def _now() -> datetime:
    return datetime.now(UTC)


def fake_db_query(sql: str) -> tuple[str, object]:
    """Simulated tool. Always errors — the point of this demo."""
    return "error", "connection refused"


def run_buggy() -> list[TraceEvent]:
    run_id = f"r-{uuid.uuid4().hex[:8]}"
    agent_id = "buggy-1"
    events: list[TraceEvent] = []
    step = 0

    def emit(ev: TraceEvent) -> None:
        nonlocal step
        events.append(ev)
        step += 1

    emit(
        AgentStep(
            ts=_now(),
            run_id=run_id,
            step=step,
            agent_id=agent_id,
            content="I'll fetch the user's recent orders.",
        )
    )

    call_id = f"c-{uuid.uuid4().hex[:6]}"
    sql = "SELECT * FROM orders WHERE user_id=42"
    emit(
        ToolCall(
            ts=_now(),
            run_id=run_id,
            step=step,
            agent_id=agent_id,
            call_id=call_id,
            name="db.query",
            args={"sql": sql},
        )
    )

    status, value = fake_db_query(sql)
    emit(
        ToolResult(
            ts=_now(),
            run_id=run_id,
            step=step,
            agent_id=agent_id,
            call_id=call_id,
            name="db.query",
            status=status,  # "error"
            value=value,
        )
    )

    # ===== THE BUG =====
    # The agent never inspects `status`. It composes a confident answer
    # as if the query had returned rows. This is F-001 silent fallback.
    emit(
        AgentStep(
            ts=_now(),
            run_id=run_id,
            step=step,
            agent_id=agent_id,
            content="The user has 3 recent orders, totaling $142.",
        )
    )
    # ====================

    emit(
        Terminate(
            ts=_now(),
            run_id=run_id,
            step=step,
            agent_id=agent_id,
            status="ok",
        )
    )
    return events


def main() -> Path:
    out_dir = ROOT / "runs"
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out = out_dir / f"buggy_f001_{stamp}.jsonl"
    dump_jsonl(run_buggy(), out)
    print(f"wrote {out}")
    return out


if __name__ == "__main__":
    main()
