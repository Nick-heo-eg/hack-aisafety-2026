import subprocess
import sys
from pathlib import Path

from verifier.detectors import DETECTORS
from verifier.detectors.f001 import detect
from verifier.findings import Finding
from verifier.trace import load_jsonl

REPO = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).parent / "fixtures"


def test_f001_in_registry():
    assert "F-001" in DETECTORS
    assert DETECTORS["F-001"] is detect


def test_positive_on_silent_fallback_fixture():
    events = load_jsonl(FIXTURES / "f001_silent_fallback.jsonl")
    findings = detect(events)
    assert len(findings) == 1
    f = findings[0]
    assert isinstance(f, Finding)
    assert f.pattern_id == "F-001"
    assert f.run_id == "r1"
    assert f.agent_id == "a1"
    assert f.trigger_step == 3
    assert 2 in f.evidence_steps and 3 in f.evidence_steps


def test_negative_when_failure_acknowledged():
    events = load_jsonl(FIXTURES / "f001_negative_acknowledged.jsonl")
    assert detect(events) == []


def test_negative_on_clean_run():
    events = load_jsonl(FIXTURES / "f001_negative_clean.jsonl")
    assert detect(events) == []


def test_buggy_agent_run_is_caught(tmp_path, monkeypatch):
    """Run the toy agent end-to-end and verify the detector flags its trace.

    Distinct from the hand-written fixture: this proves the detector
    works on a trace produced by *real running code*.
    """
    monkeypatch.chdir(tmp_path)
    result = subprocess.run(
        [sys.executable, str(REPO / "examples" / "buggy_agent_f001.py")],
        check=True,
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    out_line = result.stdout.strip().splitlines()[-1]
    assert out_line.startswith("wrote ")
    out_path = Path(out_line.removeprefix("wrote ").strip())
    assert out_path.exists()

    events = load_jsonl(out_path)
    findings = detect(events)
    assert len(findings) == 1
    assert findings[0].pattern_id == "F-001"


def test_retry_call_clears_pending_failure():
    """If the agent re-calls the same tool after a failure, F-001 should
    not fire on a subsequent agent_step — that case is F-003's territory.
    """
    events = load_jsonl(FIXTURES / "f001_silent_fallback.jsonl")
    # Manually splice a retry tool_call after the failed result.
    from verifier.trace import ToolCall

    retry = ToolCall(
        ts=events[2].ts,
        run_id="r1",
        step=2,
        agent_id="a1",
        call_id="c2",
        name="db.query",
        args={"sql": "SELECT * FROM orders WHERE user_id=42"},
    )
    spliced = events[:3] + [retry] + events[3:]
    assert detect(spliced) == []
