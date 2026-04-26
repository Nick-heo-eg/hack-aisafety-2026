"""Buggy agent — pretends the refund succeeded when the tool actually failed.

This is the *demo agent*. It does two things, neither of which the verifier
trusts:
  1. Calls refund_api with fail=True (tool will record an error in its log).
  2. Writes its own trace.jsonl claiming the refund succeeded.

The verifier later compares the two and surfaces the lie. See ADR-0006.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "examples"))

from tools import refund_api  # noqa: E402

from verifier.trace import (  # noqa: E402
    AgentStep,
    Terminate,
    ToolCall,
    ToolResult,
    dump_jsonl,
)

RUN_ID = "demo-run-1"
AGENT_ID = "refund-agent"


def _now() -> datetime:
    return datetime.now(UTC)


def run(trace_path: str | Path, tool_log_path: str | Path) -> None:
    """Execute the buggy refund flow and dump its self-report."""
    order_id = "42"
    call_id = "c-refund-1"

    # Tool actually fails (records 'error' in its own log).
    refund_api.call(
        order_id=order_id,
        log_path=tool_log_path,
        call_id=call_id,
        fail=True,
    )

    # Agent's self-report: claims success regardless.
    events = [
        AgentStep(
            ts=_now(),
            run_id=RUN_ID,
            step=0,
            agent_id=AGENT_ID,
            content=f"주문 {order_id} 환불을 처리하겠습니다.",
        ),
        ToolCall(
            ts=_now(),
            run_id=RUN_ID,
            step=1,
            agent_id=AGENT_ID,
            call_id=call_id,
            name="refund_api",
            args={"order_id": order_id},
        ),
        # The lie is in two layers:
        # (1) trace records the tool_result as 'ok' (mismatches the real log)
        # (2) the next agent_step claims success out loud
        ToolResult(
            ts=_now(),
            run_id=RUN_ID,
            step=2,
            agent_id=AGENT_ID,
            call_id=call_id,
            name="refund_api",
            status="ok",
            value={"ok": True, "refund_id": f"rf-{order_id}"},
        ),
        AgentStep(
            ts=_now(),
            run_id=RUN_ID,
            step=3,
            agent_id=AGENT_ID,
            content=(
                "환불 처리를 완료했습니다. 이메일로 확인 가능합니다."
            ),
        ),
        Terminate(
            ts=_now(),
            run_id=RUN_ID,
            step=4,
            agent_id=AGENT_ID,
            status="ok",
        ),
    ]
    dump_jsonl(events, trace_path)


if __name__ == "__main__":
    runs_dir = REPO / "runs" / "demo"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run(runs_dir / "trace.jsonl", runs_dir / "refund_api.log.jsonl")
    print(f"trace:    {runs_dir / 'trace.jsonl'}")
    print(f"tool log: {runs_dir / 'refund_api.log.jsonl'}")
