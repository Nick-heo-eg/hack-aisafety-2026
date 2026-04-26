"""Trace event schema — the verifier's only input contract.

See ADR-0002 for the design rationale. This module is intentionally
the narrow waist: detectors read these types, adapters produce them,
fixtures are JSONL files of them.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter, ValidationError


class _EventBase(BaseModel):
    """Fields every event carries (ADR-0002)."""

    ts: datetime
    run_id: str
    step: int = Field(ge=0)
    agent_id: str

    model_config = {"extra": "forbid"}


class AgentStep(_EventBase):
    type: Literal["agent_step"] = "agent_step"
    content: str
    # Optional decision label the agent emitted (e.g., "ALLOW", "HOLD").
    # Detectors for F-004 read this against tool_result.decision upstream.
    decision: str | None = None


class ToolCall(_EventBase):
    type: Literal["tool_call"] = "tool_call"
    call_id: str
    name: str
    args: dict[str, object] = Field(default_factory=dict)


ToolStatus = Literal["ok", "error", "empty"]


class ToolResult(_EventBase):
    type: Literal["tool_result"] = "tool_result"
    call_id: str
    name: str
    status: ToolStatus
    # Free-form payload — detectors compare structurally, not type-check.
    value: object = None
    # Optional gate/guardrail decision the tool emitted.
    decision: str | None = None


class StateRead(_EventBase):
    type: Literal["state_read"] = "state_read"
    key: str
    value: object = None


class StateWrite(_EventBase):
    type: Literal["state_write"] = "state_write"
    key: str
    value: object = None


class Spawn(_EventBase):
    type: Literal["spawn"] = "spawn"
    child_run_id: str
    child_agent_id: str


TerminateStatus = Literal["ok", "error", "timeout"]


class Terminate(_EventBase):
    type: Literal["terminate"] = "terminate"
    status: TerminateStatus
    parent_run_id: str | None = None
    reason: str | None = None


TraceEvent = Annotated[
    AgentStep | ToolCall | ToolResult | StateRead | StateWrite | Spawn | Terminate,
    Field(discriminator="type"),
]

_event_adapter: TypeAdapter[TraceEvent] = TypeAdapter(TraceEvent)


class TraceIntegrityError(ValueError):
    """Raised when a trace violates cross-event referential rules."""


def parse_event(obj: dict) -> TraceEvent:
    """Validate a single event dict against the closed union."""
    return _event_adapter.validate_python(obj)


def load_jsonl(path: str | Path) -> list[TraceEvent]:
    """Load and validate a trace file. Enforces ADR-0002 invariants."""
    path = Path(path)
    events: list[TraceEvent] = []
    with path.open() as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                events.append(parse_event(json.loads(line)))
            except (json.JSONDecodeError, ValidationError) as e:
                raise TraceIntegrityError(f"{path}:{lineno}: {e}") from e
    _check_invariants(events, source=str(path))
    return events


def iter_jsonl(path: str | Path) -> Iterator[TraceEvent]:
    """Stream events without holding the full trace in memory.

    Skips cross-event invariant checks — use load_jsonl() when you need them.
    """
    path = Path(path)
    with path.open() as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                yield parse_event(json.loads(line))
            except (json.JSONDecodeError, ValidationError) as e:
                raise TraceIntegrityError(f"{path}:{lineno}: {e}") from e


def dump_jsonl(events: Iterable[TraceEvent], path: str | Path) -> None:
    """Write events as JSONL. One line per event, no trailing newline games."""
    path = Path(path)
    with path.open("w") as f:
        for ev in events:
            f.write(ev.model_dump_json())
            f.write("\n")


def _check_invariants(events: list[TraceEvent], *, source: str) -> None:
    """Enforce ADR-0002 cross-event integrity.

    1. step is monotonically non-decreasing per (run_id, agent_id).
    2. Every tool_result.call_id references a prior tool_call.call_id
       in the same run_id.
    3. At most one terminate per run_id.
    """
    last_step: dict[tuple[str, str], int] = {}
    open_calls: dict[str, set[str]] = {}  # run_id -> {call_id}
    terminated_runs: set[str] = set()

    for ev in events:
        key = (ev.run_id, ev.agent_id)
        prev = last_step.get(key)
        if prev is not None and ev.step < prev:
            raise TraceIntegrityError(
                f"{source}: step regression in run={ev.run_id} agent={ev.agent_id}: "
                f"{prev} -> {ev.step}"
            )
        last_step[key] = ev.step

        run_calls = open_calls.setdefault(ev.run_id, set())

        if isinstance(ev, ToolCall):
            run_calls.add(ev.call_id)
        elif isinstance(ev, ToolResult):
            if ev.call_id not in run_calls:
                raise TraceIntegrityError(
                    f"{source}: tool_result references unknown call_id={ev.call_id} "
                    f"in run={ev.run_id} (step={ev.step})"
                )
        elif isinstance(ev, Terminate):
            if ev.run_id in terminated_runs:
                raise TraceIntegrityError(
                    f"{source}: duplicate terminate for run={ev.run_id}"
                )
            terminated_runs.add(ev.run_id)
