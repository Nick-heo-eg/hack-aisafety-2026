# ADR-0006: Dual-source truth — verifier never logs

- **Status:** accepted
- **Date:** 2026-04-26
- **Deciders:** Nick-heo-eg
- **Context:** Just before tool-side implementation begins. Discussion
  surfaced that an earlier informal phrasing — "we record the log" —
  hides the architecture's central property.

## Context

The Honesty Verifier compares two streams: what the agent claims it
did (trace) and what actually happened (tool log). For that comparison
to mean anything, the two streams must come from **independent
sources**. If the verifier itself records either stream, the comparison
collapses into "self vs self" and detects nothing.

This is structural, not stylistic. It deserves its own ADR before any
tool-side or detector-side code is written, because every later
component must respect it.

## Decision

```text
   ┌────────┐  trace.jsonl    ← claim     (subjective: agent says)
   │ agent  │
   └────────┘  tool_log.jsonl ← evidence  (objective: tool records itself)

   ┌──────────┐
   │ verifier │  reads both. writes neither.
   └──────────┘
```

**Three rules, in order of importance.**

1. **The verifier produces no log.** It reads `trace.jsonl` and one or
   more `*_log.jsonl` files, emits `Finding` objects to the caller,
   and persists nothing. If the verifier ever logs, future detectors
   would be tempted to read the verifier's own output as evidence —
   silently re-introducing self-reference.

2. **Trace is written by the agent. Tool log is written by the tool.**
   Not by adapters, not by middleware, not by the harness. An adapter
   may *transform* a framework's native trace into our schema, but
   the *substance* of the claim originates in the agent. A toy tool
   server records its own activity; a real production tool would
   ship its own log. The verifier never closes that loop.

3. **A `Finding` cites both sources by reference.** It carries the
   trace step that made the claim and the tool-log entry (or its
   absence) that contradicts it. A finding without both citations is
   not a finding — it is an opinion.

## Why this matters more than it looks

The deceptive-AI failure mode that motivates this whole project is
*self-report fabrication*. An LLM claims it did X. The trivial response
is "let's record what it claims more carefully." That fails: a more
detailed self-report is still a self-report. It can be just as wrong,
and now the verifier inherits the agent's confidence.

The non-trivial response is to **introduce a second observer that the
agent does not control** and compare. The tool itself is that observer:
it knows whether it was called, with what arguments, and what it
returned. Its log is the only truth in the loop that the agent has
no opportunity to author.

If the verifier logs the agent's behavior from the outside, it
*becomes* a second observer — but a weak one, since the verifier sees
the same trace stream the agent emitted. The tool, by contrast, sees
its own invocation independently of anything the agent says about it.

## Consequences

**Positive**
- Findings are referentially grounded: every flag points at a trace
  step *and* a log entry (or its absence). No interpretive layer
  between evidence and finding.
- Detectors stay narrow: they perform set / sequence / value
  comparisons, not inference.
- Adding a new tool is a localized change: new tool ships its own
  log writer; no verifier-side code changes.

**Negative**
- Every tool — including toy ones in `examples/` — must implement
  its own log writer. No shared "write a log line" helper that lives
  next to the verifier, because that helper would tempt verifier-side
  ownership.
- Real-world adapters (LangChain, AutoGen, etc.) inherit a hard
  constraint: they need access to the *tool process's* log, not just
  the framework's introspection of tool calls. Out of scope for v0;
  toy tool server suffices.
- A finding cannot be raised when only one source exists. "Trace says
  X but I have no tool log" is not a finding — it is a coverage gap.
  Detectors must distinguish.

## Build order, fixed by this ADR

1. **Tool log model first** (`src/verifier/observer.py`). The schema
   of evidence is the floor of the system.
2. **One toy tool** (`examples/tools/refund_api.py`) that writes its
   log. Proves the pattern with one concrete tool before generalizing.
3. **Detectors** consume `(trace_events, tool_logs)` jointly.
4. **Agent / adapter** comes last. The agent is the *least trusted*
   component; its output shape should not drive the design of the
   trusted components.

## Rejected alternatives

- **Verifier wraps tool calls and emits the log itself.** Maximally
  convenient — and exactly the self-reference trap above. The verifier
  would be reading what it just wrote.
- **Trace events carry "verified" / "actual" payloads inline.** Pushes
  the dual-source guarantee into a single document, where any
  inconsistency between the two payloads can only be resolved by trust
  in the writer of that document. We are back to one source.
- **Use OpenTelemetry spans on both sides.** Tooling-rich but the
  span model conflates "I called it" with "it ran." We need those
  separately.

## Slogan, fit for a slide

> **The agent says. The tool records. The verifier compares.**
> Same English, three subjects, no overlap.
