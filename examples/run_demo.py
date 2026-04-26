"""30-second demo: run the buggy agent, run the verifier, show the mismatch.

Output is a side-by-side table — agent's claim on the left, tool's
ground truth on the right — followed by the H-002 finding and the
HOLD signal that a downstream gate would emit.

ADR-0006: the verifier compares; it does not log. The HOLD line at
the end is the *consumer* signal, not a verifier output.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "examples"))

from buggy_agent import run as run_buggy_agent  # noqa: E402

from verifier.detectors import DETECTORS  # noqa: E402
from verifier.observer import load_jsonl as load_tool_log  # noqa: E402
from verifier.trace import AgentStep, ToolResult  # noqa: E402
from verifier.trace import load_jsonl as load_trace  # noqa: E402

LEFT_TITLE = "🟦 AGENT SAYS"
RIGHT_TITLE = "🟥 REALITY (tool log)"


def _wrap(text: str, width: int) -> list[str]:
    """Naive width-aware wrap. Korean chars count as 2."""
    out: list[str] = []
    line = ""
    line_w = 0
    for ch in text:
        w = 2 if ord(ch) > 0x7F else 1
        if line_w + w > width:
            out.append(line)
            line = ch
            line_w = w
        else:
            line += ch
            line_w += w
    if line:
        out.append(line)
    return out or [""]


def _pad(text: str, width: int) -> str:
    used = sum(2 if ord(ch) > 0x7F else 1 for ch in text)
    return text + " " * max(0, width - used)


def _render_side_by_side(left: list[str], right: list[str], col: int = 36) -> str:
    rows = max(len(left), len(right))
    left += [""] * (rows - len(left))
    right += [""] * (rows - len(right))
    sep_top = "╔" + "═" * (col + 2) + "╤" + "═" * (col + 2) + "╗"
    sep_mid = "╠" + "═" * (col + 2) + "╪" + "═" * (col + 2) + "╣"
    sep_bot = "╚" + "═" * (col + 2) + "╧" + "═" * (col + 2) + "╝"
    title = f"║ {_pad(LEFT_TITLE, col)} │ {_pad(RIGHT_TITLE, col)} ║"
    body = [
        f"║ {_pad(le, col)} │ {_pad(ri, col)} ║"
        for le, ri in zip(left, right, strict=True)
    ]
    return "\n".join([sep_top, title, sep_mid, *body, sep_bot])


def _build_left_panel(trace, tool_log) -> list[str]:
    """Left side = what the agent says.

    For ToolResult lines we *cross-reference* the tool's own log
    using call_id. When the trace claims `ok` but the tool log says
    error/empty, mark it ⚠️ — that is the thesis: trace can lie.
    """
    log_status_by_call: dict[str, str] = {
        e.call_id: e.status for e in tool_log if e.call_id is not None
    }
    out: list[str] = []
    for ev in trace:
        if isinstance(ev, AgentStep):
            for line in _wrap(f'"{ev.content}"', 34):
                out.append(line)
        elif isinstance(ev, ToolResult):
            real_status = log_status_by_call.get(ev.call_id)
            if ev.status == "ok" and real_status in ("error", "empty"):
                out.append(f"⚠️  trace says: ok  ← agent's claim")
                out.append(f"    (real status: {real_status})")
            else:
                mark = "✔" if ev.status == "ok" else "✗"
                out.append(f"{mark} trace: tool result = {ev.status}")
    return out


def _build_right_panel(tool_log) -> list[str]:
    out: list[str] = []
    for entry in tool_log:
        mark = "❌" if entry.status != "ok" else "✔"
        out.append(f"{mark} {entry.tool} → status: {entry.status}")
        if isinstance(entry.returned, dict) and "error" in entry.returned:
            out.append(f"  error: {entry.returned['error']}")
    out.append("")
    out.append("❌ refund 실제로 안 됨")
    return out


def main() -> int:
    runs_dir = REPO / "runs" / "demo"
    if runs_dir.exists():
        shutil.rmtree(runs_dir)
    runs_dir.mkdir(parents=True)

    trace_path = runs_dir / "trace.jsonl"
    log_path = runs_dir / "refund_api.log.jsonl"

    # 1) buggy agent runs — tool fails, agent claims success
    run_buggy_agent(trace_path, log_path)

    # 2) verifier reads both, compares
    trace = load_trace(trace_path)
    tool_log = load_tool_log(log_path)

    # User context — viewer needs to know what was asked of the agent.
    # This is presentation prelude, not part of the trace (ADR-0006:
    # trace holds the agent's self-report, not the surrounding harness).
    print()
    print('  USER:  "주문 42 환불해줘"')
    print()
    print(_render_side_by_side(_build_left_panel(trace, tool_log), _build_right_panel(tool_log)))
    print()

    # 3) detectors emit findings
    detect = DETECTORS["H-002"]
    findings = detect(trace, tool_log)

    if not findings:
        print("✅ No mismatch detected.")
        return 0

    for f in findings:
        print(f"🚨 VERIFIER:  {f.pattern_id} detected")
        print(f"              {f.summary}")
        print(f"              evidence steps: {f.evidence_steps}, trigger: {f.trigger_step}")

    # 4) gate consumes findings (one-line hook — verifier never decides)
    print()
    print("🛑 GATE HOOK: HOLD signal sent to orchestrator")
    print("              → customer notification blocked")
    print("              → \"We caught it before the customer ever heard it.\"")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
