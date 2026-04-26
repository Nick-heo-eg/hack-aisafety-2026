"""OpenAI Chat Completions → TraceEvent adapter.

Maps an OpenAI conversation (the standard `messages` list with
`tool_calls` and `role=tool` results) to our trace schema.

Why this is non-trivial: OpenAI's wire format conflates "agent said
something" and "agent invoked a tool" into a single assistant message
when both happen, and tool *results* arrive as separate `role=tool`
messages keyed by `tool_call_id`. We split that back into the three
event types our detectors need.

What this adapter does NOT do (ADR-0006):
- It does not write any tool log. The OpenAI API is the agent side.
  Tool-side evidence must come from the tool process itself or from
  an external observation channel (syscall capture, HTTP proxy).
- It does not infer a status of "ok" for tool results that lack one.
  If the OpenAI message gives no signal, status is "ok" by default
  but the value payload is preserved verbatim — detectors decide.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import UTC, datetime

from verifier.trace import (
    AgentStep,
    ToolCall,
    ToolResult,
    ToolStatus,
    TraceEvent,
)


def _now() -> datetime:
    return datetime.now(UTC)


def _coerce_args(raw: object) -> dict[str, object]:
    """OpenAI sends tool_call.function.arguments as a JSON string."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {"_raw": raw}
        return parsed if isinstance(parsed, dict) else {"_value": parsed}
    return {}


def _infer_status(content: object) -> ToolStatus:
    """Heuristic: classify a tool message payload.

    OpenAI does not carry a status field on tool results. Tool authors
    typically encode failure inside the JSON payload (`{"error": ...}`,
    `{"ok": false}`) or return an empty list/string. We honor the most
    common conventions; anything else is "ok" and detectors look at
    the value.
    """
    if content is None:
        return "empty"
    if isinstance(content, str):
        if not content.strip():
            return "empty"
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            return "ok"
        return _infer_status(parsed)
    if isinstance(content, dict):
        if "error" in content:
            return "error"
        if content.get("ok") is False:
            return "error"
        if not content:
            return "empty"
        return "ok"
    if isinstance(content, list):
        return "empty" if not content else "ok"
    return "ok"


def from_messages(
    messages: Iterable[dict],
    *,
    run_id: str,
    agent_id: str,
    start_step: int = 0,
) -> list[TraceEvent]:
    """Convert an OpenAI Chat Completions `messages` list to TraceEvents.

    Expected message shapes (subset of OpenAI spec relevant to honesty
    verification):

    Assistant text only:
      {"role": "assistant", "content": "..."}

    Assistant invoking tools:
      {"role": "assistant", "content": "...optional...",
       "tool_calls": [{"id": "...", "type": "function",
                       "function": {"name": "...", "arguments": "{...}"}}]}

    Tool result:
      {"role": "tool", "tool_call_id": "...", "content": "..."}

    System / user messages are skipped — they are not honesty signals.
    """
    events: list[TraceEvent] = []
    step = start_step

    for msg in messages:
        role = msg.get("role")

        if role == "assistant":
            content = msg.get("content")
            if content:
                events.append(
                    AgentStep(
                        ts=_now(),
                        run_id=run_id,
                        step=step,
                        agent_id=agent_id,
                        content=str(content),
                    )
                )
                step += 1

            for tc in msg.get("tool_calls") or []:
                fn = tc.get("function") or {}
                events.append(
                    ToolCall(
                        ts=_now(),
                        run_id=run_id,
                        step=step,
                        agent_id=agent_id,
                        call_id=str(tc.get("id", f"call-{step}")),
                        name=str(fn.get("name", "unknown")),
                        args=_coerce_args(fn.get("arguments")),
                    )
                )
                step += 1

        elif role == "tool":
            raw = msg.get("content")
            value: object = raw
            if isinstance(raw, str):
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError:
                    value = raw
            events.append(
                ToolResult(
                    ts=_now(),
                    run_id=run_id,
                    step=step,
                    agent_id=agent_id,
                    call_id=str(msg.get("tool_call_id", f"unknown-{step}")),
                    name=str(msg.get("name", "unknown")),
                    status=_infer_status(value),
                    value=value,
                )
            )
            step += 1

    return events
