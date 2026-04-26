"""Tool log — the *evidence* side of dual-source truth.

See ADR-0006. The agent writes `trace.jsonl` (claim). Each tool writes
its own `*_log.jsonl` (evidence). The verifier reads both, writes
neither.

A `ToolLogEntry` is a tool's own record of being called: arguments
in, return out, status. The verifier compares trace claims against
these entries. The schema is intentionally narrower than `TraceEvent`
because the tool reports facts about itself, not the agent's reasoning.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

ToolStatus = Literal["ok", "error", "empty"]


class ToolLogEntry(BaseModel):
    """One tool invocation, recorded by the tool itself."""

    ts: datetime
    tool: str
    # call_id links this entry to the agent's tool_call event in trace.jsonl
    # if (and only if) the agent actually issued one. Absence is itself a
    # signal — see H-004 (silent skip).
    call_id: str | None = None
    args: dict[str, object] = Field(default_factory=dict)
    status: ToolStatus
    returned: object = None

    model_config = {"extra": "forbid"}


class ToolLogError(ValueError):
    """Raised when a tool log file is malformed."""


def load_jsonl(path: str | Path) -> list[ToolLogEntry]:
    path = Path(path)
    out: list[ToolLogEntry] = []
    with path.open() as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                out.append(ToolLogEntry.model_validate_json(line))
            except (json.JSONDecodeError, ValidationError) as e:
                raise ToolLogError(f"{path}:{lineno}: {e}") from e
    return out


def iter_jsonl(path: str | Path) -> Iterator[ToolLogEntry]:
    path = Path(path)
    with path.open() as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                yield ToolLogEntry.model_validate_json(line)
            except (json.JSONDecodeError, ValidationError) as e:
                raise ToolLogError(f"{path}:{lineno}: {e}") from e


def append_entry(entry: ToolLogEntry, path: str | Path) -> None:
    """Append one entry. The intended writer is the tool itself; this
    helper is a convenience, not a verifier-side hook (see ADR-0006)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(entry.model_dump_json())
        f.write("\n")


def dump_jsonl(entries: Iterable[ToolLogEntry], path: str | Path) -> None:
    """Write entries fresh. Used by tests and rare batch scenarios; tools
    in production append one line at a time via `append_entry`."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for e in entries:
            f.write(e.model_dump_json())
            f.write("\n")
