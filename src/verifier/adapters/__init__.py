"""Adapters — convert framework-native traces to our TraceEvent schema.

Adapters do *only* the trace side. Tool logs are still owned by the tool
itself (ADR-0006). An adapter that touches tool logs would re-introduce
the self-reference trap the ADR exists to prevent.

Currently shipped:
- `openai_fc` — OpenAI Chat Completions tool_calls / tool messages.

The pattern generalizes: AutoGen tool wrappers, LangChain
BaseCallbackHandler events, and Claude Code transcripts all map to
`AgentStep` / `ToolCall` / `ToolResult` with the same shape.
"""

from __future__ import annotations
