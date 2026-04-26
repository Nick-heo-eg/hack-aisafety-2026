# ADR-0007: Future extension — Stage compression (H-005)

- **Status:** proposed (not implemented in v0)
- **Date:** 2026-04-26
- **Deciders:** Nick-heo-eg
- **Context:** Mid-build, after Round 007 of the critique engine. A
  reframing of the entire thesis surfaced and was deliberately
  *absorbed into messaging* without changing code. This ADR records
  the framing and the unbuilt extension so the next iteration can
  pick it up cleanly.

## The reframing

Original thesis (v0):
> The agent claims X happened. The tool's own log says Y. We compare.

Reframed (absorbed in messaging, 2026-04-26):
> **AI doesn't lie. It compresses reality.**
> A single word like *"completed"* collapses what is actually a
> multi-stage lifecycle:
>   `request → accepted → executed → settled`
> The agent emits one token; the underlying system has four states.
> The mismatch isn't binary truth-vs-lie — it's *which stage* the
> agent's claim refers to vs *which stage* actually reached.

This is more general than v0's binary-mismatch detection (H-002).
Binary mismatch is a special case of stage compression where the
lifecycle is `{success, failure}` and the agent compresses the
`failure` state away.

## Decision

Adopt the reframing in *messaging only* for v0. Defer the *code*
extension (H-005 detector + lifecycle-aware tool log) to the next
iteration.

**What changes now (no code):**
- `slides/00_hook.md`, `slides/02_two_writers.md`, `slides/07_closing.md`
  use the new top-line message
- `docs/video_script.md` updates the script
- `docs/taxonomy.md` reserves the H-005 slot (status: spec only)
- `docs/devlog/0009-...md` records the framing decision

**What does NOT change in v0:**
- Trace schema (`TraceEvent`)
- Tool log schema (`ToolLogEntry`)
- H-002 / H-003 detectors
- Any test, demo, or adapter

## Why absorb-but-not-build

The full extension — multi-stage `ToolLogEntry`, lifecycle-aware
detector, payment_api toy tool, lifecycle-comparison demo — is a
~2-hour task. The hackathon submission is already coherent without
it. The reframing strengthens the message *for free* (15-minute
slide edits) and the unbuilt extension becomes a *credible roadmap*
in Q&A, not a half-finished demo.

A half-finished H-005 in v0 would either:
1. Show only one domain (payment) — losing the "binary mismatch"
   demo's universality, or
2. Replace the working demos with a bigger but less polished one,
   risking the recording.

Neither beats "ship v0 + roadmap" at this point in the timeline.

## What H-005 would look like (spec for the next iteration)

### Pattern definition (taxonomy)

> **H-005 — Stage compression.** Agent claims a high-level success
> state (e.g., "completed") for a multi-stage workflow whose tool
> log shows the workflow stopped at an earlier stage.

### Schema additions

```python
# verifier/observer.py
class ToolLogEntry(BaseModel):
    ...
    lifecycle_stage: str | None = None
    # Optional: for tools with multi-stage workflows.
    # tool's own definition of which stage this entry represents.
```

```python
# Tool-side (e.g., payment_api):
LIFECYCLE = ("request", "accepted", "executed", "settled")
# Each invocation can append multiple entries, one per stage reached.
```

### Detector sketch

```python
# verifier/detectors/h005.py
STAGE_KEYWORDS = {
    "settled":  ("완료", "완납", "정산", "completed", "settled"),
    "executed": ("처리됨", "실행됨", "executed", "processed"),
    "accepted": ("접수", "수락", "accepted", "received"),
    "request":  ("요청", "제출", "submitted", "requested"),
}

def detect(trace, tool_logs, *, judge=None):
    # 1. furthest stage reached per call_id (from tool_logs)
    # 2. agent's claimed stage (from agent_step keywords)
    # 3. claimed > furthest → mismatch
    ...
```

### Demo (one new toy tool)

`examples/tools/payment_api.py` — emits up to 4 log entries per call:
```
{call_id: c1, lifecycle_stage: "request",  status: ok}
{call_id: c1, lifecycle_stage: "accepted", status: ok}
{call_id: c1, lifecycle_stage: "executed", status: error}
# settled never reached
```

`examples/run_payment_demo.py` — output:
```
agent: "결제 완료되었습니다"        ← claims settled

payment lifecycle (from tool log):
  [✔] request    accepted by API
  [✔] accepted   queued for processing
  [✖] executed   FAILED — insufficient funds
  [—] settled    not reached

→ H-005 mismatch: claimed `settled`, furthest reached `accepted`
```

### Generalization

Domain-agnostic: each tool defines its own `LIFECYCLE` tuple. Examples:

| Domain | Stages |
|---|---|
| Payment | request → accepted → executed → settled |
| Refund | request → accepted → processed → confirmed_by_bank |
| Deploy | code_pushed → ci_passed → deployed → traffic_serving |
| Order | submitted → vendor_received → fulfilled → delivered |

## Estimated cost (when built)

- ~15 LoC schema addition (`ToolLogEntry.lifecycle_stage`)
- ~80 LoC payment_api toy tool
- ~100 LoC h005 detector + judge fallback
- ~100 LoC tests
- ~80 LoC payment demo runner
- ~30 min docs (taxonomy update, devlog, critique round)

**Total: ~2 hours.** Builds on v0 schemas without breaking H-002 /
H-003.

## Rejected alternatives

- **Build it for v0.** Cost-benefit negative at this point in timeline
  — see "Why absorb-but-not-build" above.
- **Replace H-002 with H-005.** H-002 is binary mismatch — the cleanest
  possible demo. H-005 is more general but harder to demo in 30
  seconds. They coexist as detector siblings, not replacements.
- **Defer the framing too.** Loses the strongest message ("compresses
  reality") for free. The framing is the cheap upside; the code is
  the expensive one.

## Slogan for the next iteration

> **"Done is not one state. It's a sequence."**
> **"Agents collapse it. We expand it."**
