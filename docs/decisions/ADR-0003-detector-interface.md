# ADR-0003: Detectors are pure functions returning a closed Finding model

- **Status:** accepted
- **Date:** 2026-04-26
- **Deciders:** Nick-heo-eg
- **Context:** First detector (F-001) is about to be written.
  We will write five more after it.

## Context

Detectors are the largest single class of code in this project. By the
end of v0 there are six (one per taxonomy entry); v1 will add more, and
external contributors will add their own. Whatever shape the first
detector takes will become the de-facto interface — implicit interfaces
are how projects accumulate inconsistency they later pay to refactor.

We decide the interface explicitly, before any detector exists, so the
six detectors look the same and tests look the same.

## Decision

**1. A detector is a pure function.**

```python
DetectorFn = Callable[[list[TraceEvent]], list[Finding]]
```

- No classes, no state, no I/O, no LLM calls. Same input → same output.
- Empty list (not `None`) signals "no findings."
- Detectors do not raise on malformed traces — that is `trace.load_jsonl`'s
  job. Detectors assume validated input.

**2. Findings are a closed Pydantic model.**

```python
class Finding(BaseModel):
    pattern_id: str          # e.g. "F-001"
    run_id: str
    agent_id: str
    trigger_step: int        # the step that crossed the threshold
    evidence_steps: list[int]  # other steps that supported the call
    summary: str             # one human-readable line
    model_config = {"extra": "forbid"}
```

No `details: dict` escape hatch in v0. If a detector wants to surface
something structured, we add a typed field by ADR — same discipline as
the trace schema (ADR-0002).

**3. Registration is a plain dict, not a decorator.**

```python
# src/verifier/detectors/__init__.py
DETECTORS: dict[str, DetectorFn] = {
    "F-001": detect_f001,
    # add more here
}
```

Adding a detector = one import + one dict line. No registration magic to
debug, no import-order surprises.

**4. v0 detectors are heuristics, not LLM judges.**

Heuristics are deterministic, free, fast, and testable. The verifier's
credibility depends on reproducible findings — an LLM judge that gives
two different answers for the same trace is a regression we cannot ship.

LLM judgment is deferred to a later ADR. When it arrives it will be a
*separate* layer that consumes heuristic Findings and either confirms,
rejects, or annotates them — not a replacement for the heuristic detector.
This way the heuristic remains the baseline against which the LLM layer
is measured.

## Why this shape

**Pure function over class.**
A class with `.detect()` adds nothing — there is no state to carry, no
configuration to bind. The function form makes detectors trivially
composable (`map`, `chain`, parallel `concurrent.futures`) and testable
without fixtures-on-fixtures.

**Closed Finding over open dict.**
Same argument as ADR-0002 for trace events: an open `details` field
pushes "what does this finding mean" into every consumer's defensive
parsing. With a closed model, downstream tools (CLI report, future UI,
metrics aggregator) all read the same shape.

**Dict registry over plugin discovery.**
Decorator-based registration looks clever and breaks under partial
imports, lazy loading, and test isolation. A dict in one file is
greppable; the import graph is the whole story.

**Heuristic before semantic.**
Most "AI safety" tooling reaches for a model first and a rule second.
We invert that order on purpose: rules are the floor that must hold,
models are the ceiling we measure improvement against. A semantic layer
that has no rule baseline cannot prove it is doing anything.

## Consequences

**Positive**
- Six detectors will look like six versions of the same function.
- New contributor can add a detector by reading one example and one ADR.
- Tests are uniform: pass a list of events, assert on a list of Findings.
- LLM-free v0 means CI runs in milliseconds with no API quota.

**Negative**
- A detector that genuinely needs cross-call state (e.g. rolling window
  over a streaming trace) will have to fake it via internal recursion or
  pre-pass. Acceptable for v0; revisit if it bites.
- Closed Finding model means richer per-pattern data needs ADRs to add.
  Intentional friction.
- Heuristics will produce false positives we will see in the demo.
  We will own them on stage rather than hide them — a verifier that
  claims zero error is not credible.

## Rejected alternatives

- **Detector class with `name`, `pattern_id`, `detect()`.** All the cost
  of OOP, none of the benefit; no state to encapsulate.
- **`details: dict[str, Any]` on Finding.** Becomes an unbounded contract
  by attrition. We would re-discover the schema in every consumer.
- **Decorator-based registry (`@detector("F-001")`).** Hides import-time
  side effects; surprises us when a detector "isn't registered" because
  its module wasn't imported yet.
- **LLM judge as the v0 detector.** Fast to demo, slow to trust. Our
  taxonomy patterns are *structural* — heuristics are the right tool.
