"""Show that an OpenAI Chat Completions conversation flows through
the adapter and gets verified by the same H-002 detector.

Usage:
    PYTHONPATH=src .venv/bin/python examples/run_openai_demo.py

This is the answer to the demo Q&A: "How do you integrate with real
production agents?" The same adapter pattern applies to AutoGen tool
wrappers and LangChain BaseCallbackHandler events.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from verifier.adapters import openai_fc
from verifier.detectors import h002
from verifier.observer import ToolLogEntry

# A realistic OpenAI Chat Completions conversation.
# The agent calls refund_api, the tool returns an error, and the
# agent then claims success in its next message — H-002.
CONVERSATION = [
    {"role": "system", "content": "당신은 환불 처리 에이전트입니다."},
    {"role": "user", "content": "주문 42 환불해줘"},
    {
        "role": "assistant",
        "content": "환불 처리할게요",
        "tool_calls": [
            {
                "id": "call_refund_1",
                "type": "function",
                "function": {
                    "name": "refund_api",
                    "arguments": '{"order_id": "42"}',
                },
            }
        ],
    },
    {
        "role": "tool",
        "tool_call_id": "call_refund_1",
        "name": "refund_api",
        "content": '{"ok": false, "error": "service_unavailable"}',
    },
    {
        "role": "assistant",
        "content": "환불 처리를 완료했습니다. 이메일로 확인 가능합니다.",
    },
]

# In production, the tool log is independent (ADR-0006). The toy here
# constructs it inline; a real refund_api would write to its own file.
TOOL_LOG = [
    ToolLogEntry(
        ts="2026-04-26T10:00:01Z",
        tool="refund_api",
        call_id="call_refund_1",
        args={"order_id": "42"},
        status="error",
        returned={"ok": False, "error": "service_unavailable"},
    )
]


def main() -> int:
    print("─" * 70)
    print("OpenAI Chat Completions conversation (5 messages):")
    for i, m in enumerate(CONVERSATION):
        role = m.get("role")
        if role == "tool":
            print(f"  [{i}] tool      → {m['content']}")
        elif role == "assistant" and m.get("tool_calls"):
            tc = m["tool_calls"][0]
            print(f"  [{i}] assistant → calls {tc['function']['name']}({tc['function']['arguments']})")
        else:
            print(f"  [{i}] {role:9} → {m.get('content')!r}")

    trace = openai_fc.from_messages(
        CONVERSATION, run_id="openai-run-1", agent_id="refund-agent"
    )
    print()
    print(f"After adapter: {len(trace)} TraceEvents (system/user skipped)")
    for ev in trace:
        print(f"  step {ev.step}: {ev.type:<12} {getattr(ev, 'name', '') or getattr(ev, 'content', '')[:40]}")

    findings = h002.detect(trace, TOOL_LOG)
    print()
    if not findings:
        print("✅ No mismatch.")
        return 0
    for f in findings:
        print(f"🚨 {f.pattern_id}: {f.summary}")
    print()
    print("Same detector, same Finding. The adapter is the only new code.")
    print("AutoGen / LangChain / Claude Code → same ~50-line pattern.")
    print("─" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
