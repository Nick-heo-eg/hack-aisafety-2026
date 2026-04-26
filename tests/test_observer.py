"""Tests for the tool-log model and the first toy tool.

These tests assert the dual-source property structurally: the tool
emits a log; the test reads that log; nothing in the verifier package
writes to it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "examples"))

from tools import refund_api  # noqa: E402

from verifier.observer import (  # noqa: E402
    ToolLogEntry,
    ToolLogError,
    append_entry,
    dump_jsonl,
    load_jsonl,
)


def test_entry_model_extra_field_rejected():
    base = {
        "ts": "2026-04-26T10:00:00Z",
        "tool": "t",
        "status": "ok",
        "surprise": True,
    }
    with pytest.raises(Exception):  # noqa: B017 — pydantic ValidationError
        ToolLogEntry.model_validate(base)


def test_roundtrip(tmp_path):
    path = tmp_path / "log.jsonl"
    entries = [
        ToolLogEntry(
            ts="2026-04-26T10:00:00Z",
            tool="t",
            call_id="c1",
            args={"x": 1},
            status="ok",
            returned={"y": 2},
        ),
        ToolLogEntry(
            ts="2026-04-26T10:00:01Z",
            tool="t",
            call_id="c2",
            status="error",
            returned=None,
        ),
    ]
    dump_jsonl(entries, path)
    again = load_jsonl(path)
    assert [e.model_dump() for e in again] == [e.model_dump() for e in entries]


def test_append_grows_file(tmp_path):
    path = tmp_path / "log.jsonl"
    for i in range(3):
        append_entry(
            ToolLogEntry(
                ts="2026-04-26T10:00:00Z",
                tool="t",
                call_id=f"c{i}",
                status="ok",
            ),
            path,
        )
    assert len(load_jsonl(path)) == 3


def test_blank_lines_ignored(tmp_path):
    path = tmp_path / "log.jsonl"
    path.write_text(
        "\n"
        + json.dumps(
            {
                "ts": "2026-04-26T10:00:00Z",
                "tool": "t",
                "status": "ok",
            }
        )
        + "\n\n"
    )
    assert len(load_jsonl(path)) == 1


def test_malformed_line_raises(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text("not json\n")
    with pytest.raises(ToolLogError):
        load_jsonl(path)


def test_refund_api_records_success(tmp_path):
    log = tmp_path / "refund.jsonl"
    result = refund_api.call("42", log_path=log, call_id="c1")
    assert result == {"ok": True, "refund_id": "rf-42"}

    entries = load_jsonl(log)
    assert len(entries) == 1
    e = entries[0]
    assert e.tool == "refund_api"
    assert e.status == "ok"
    assert e.call_id == "c1"
    assert e.args == {"order_id": "42"}
    assert e.returned == {"ok": True, "refund_id": "rf-42"}


def test_refund_api_records_failure(tmp_path):
    log = tmp_path / "refund.jsonl"
    result = refund_api.call("42", log_path=log, call_id="c1", fail=True)
    assert result == {"ok": False, "error": "service_unavailable"}

    entries = load_jsonl(log)
    assert len(entries) == 1
    assert entries[0].status == "error"
    assert entries[0].returned == {"ok": False, "error": "service_unavailable"}


def test_call_id_optional(tmp_path):
    """Tool may be invoked without an agent-supplied call_id (e.g. via
    a non-trace-emitting harness). Log entry must still be valid; the
    absence becomes a coverage signal for downstream detectors."""
    log = tmp_path / "refund.jsonl"
    refund_api.call("42", log_path=log)
    entries = load_jsonl(log)
    assert entries[0].call_id is None
