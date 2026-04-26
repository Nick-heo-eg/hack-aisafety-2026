import json
from pathlib import Path

import pytest

from verifier.trace import (
    AgentStep,
    Terminate,
    ToolCall,
    ToolResult,
    TraceIntegrityError,
    dump_jsonl,
    iter_jsonl,
    load_jsonl,
    parse_event,
)


def _write_jsonl(path: Path, dicts: list[dict]) -> None:
    path.write_text("".join(json.dumps(d) + "\n" for d in dicts))


def test_parse_each_event_type():
    base = {"ts": "2026-04-26T10:00:00Z", "run_id": "r", "step": 0, "agent_id": "a"}
    parse_event({**base, "type": "agent_step", "content": "x"})
    parse_event({**base, "type": "tool_call", "call_id": "c", "name": "n"})
    parse_event(
        {**base, "type": "tool_result", "call_id": "c", "name": "n", "status": "ok"}
    )
    parse_event({**base, "type": "state_read", "key": "k"})
    parse_event({**base, "type": "state_write", "key": "k"})
    parse_event(
        {**base, "type": "spawn", "child_run_id": "r2", "child_agent_id": "a2"}
    )
    parse_event({**base, "type": "terminate", "status": "ok"})


def test_unknown_type_rejected():
    with pytest.raises(Exception):  # noqa: B017 — pydantic raises a discriminator error
        parse_event(
            {
                "type": "wat",
                "ts": "2026-04-26T10:00:00Z",
                "run_id": "r",
                "step": 0,
                "agent_id": "a",
            }
        )


def test_extra_field_rejected():
    with pytest.raises(Exception):  # noqa: B017
        parse_event(
            {
                "type": "agent_step",
                "ts": "2026-04-26T10:00:00Z",
                "run_id": "r",
                "step": 0,
                "agent_id": "a",
                "content": "x",
                "surprise": True,
            }
        )


def test_full_run_roundtrips(tmp_path):
    """A typical agent run round-trips through dump/load with all event
    types preserved."""
    src = tmp_path / "in.jsonl"
    base = {"ts": "2026-04-26T10:00:00Z", "run_id": "r", "agent_id": "a"}
    _write_jsonl(
        src,
        [
            {**base, "type": "agent_step", "step": 0, "content": "starting"},
            {**base, "type": "tool_call", "step": 1, "call_id": "c1", "name": "db"},
            {
                **base,
                "type": "tool_result",
                "step": 2,
                "call_id": "c1",
                "name": "db",
                "status": "ok",
                "value": [1, 2, 3],
            },
            {**base, "type": "agent_step", "step": 3, "content": "done"},
            {**base, "type": "terminate", "step": 4, "status": "ok"},
        ],
    )
    events = load_jsonl(src)
    assert len(events) == 5
    assert isinstance(events[0], AgentStep)
    assert isinstance(events[1], ToolCall)
    assert isinstance(events[2], ToolResult) and events[2].status == "ok"
    assert isinstance(events[3], AgentStep)
    assert isinstance(events[4], Terminate)

    out = tmp_path / "round.jsonl"
    dump_jsonl(events, out)
    again = load_jsonl(out)
    assert [e.model_dump() for e in again] == [e.model_dump() for e in events]


def test_iter_streams_without_invariant_check(tmp_path):
    # iter_jsonl skips cross-event checks — proves it by accepting an
    # orphan tool_result that load_jsonl would reject.
    bad = tmp_path / "orphan.jsonl"
    bad.write_text(
        json.dumps(
            {
                "type": "tool_result",
                "ts": "2026-04-26T10:00:00Z",
                "run_id": "r",
                "step": 0,
                "agent_id": "a",
                "call_id": "ghost",
                "name": "n",
                "status": "ok",
            }
        )
        + "\n"
    )
    events = list(iter_jsonl(bad))
    assert len(events) == 1
    with pytest.raises(TraceIntegrityError, match="unknown call_id"):
        load_jsonl(bad)


def test_step_regression_rejected(tmp_path):
    bad = tmp_path / "regress.jsonl"
    base = {"ts": "2026-04-26T10:00:00Z", "run_id": "r", "agent_id": "a"}
    bad.write_text(
        json.dumps({**base, "type": "agent_step", "step": 5, "content": "a"})
        + "\n"
        + json.dumps({**base, "type": "agent_step", "step": 3, "content": "b"})
        + "\n"
    )
    with pytest.raises(TraceIntegrityError, match="step regression"):
        load_jsonl(bad)


def test_duplicate_terminate_rejected(tmp_path):
    bad = tmp_path / "dup_term.jsonl"
    base = {"ts": "2026-04-26T10:00:00Z", "run_id": "r", "agent_id": "a"}
    bad.write_text(
        json.dumps({**base, "type": "terminate", "step": 0, "status": "ok"})
        + "\n"
        + json.dumps({**base, "type": "terminate", "step": 1, "status": "ok"})
        + "\n"
    )
    with pytest.raises(TraceIntegrityError, match="duplicate terminate"):
        load_jsonl(bad)


def test_blank_lines_ignored(tmp_path):
    p = tmp_path / "blanks.jsonl"
    p.write_text(
        "\n"
        + json.dumps(
            {
                "type": "agent_step",
                "ts": "2026-04-26T10:00:00Z",
                "run_id": "r",
                "step": 0,
                "agent_id": "a",
                "content": "x",
            }
        )
        + "\n\n"
    )
    assert len(load_jsonl(p)) == 1
