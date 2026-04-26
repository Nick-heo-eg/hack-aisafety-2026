# ADR-0002: Trace as event-stream JSONL with a closed event union

- **Status:** accepted
- **Date:** 2026-04-26
- **Deciders:** Nick-heo-eg
- **Context:** First detector requires a defined input format.

## Context

ADR-0001 committed us to operating on **traces**, not prompts. That
turns the trace format into the verifier's only input contract — every
detector reads it, every adapter writes it, every test fixture is one.
Get it wrong now and every later piece pays the cost.

Concrete decisions to make:

1. **File format.** One file vs many; structured vs free-form.
2. **Event model.** A single flexible event vs a closed union of typed events.
3. **Identity.** What ties events in the same run together; how parent/child agents are linked.
4. **Extensibility.** What happens when someone needs to add a field.

## Decision

**Format: JSONL — one JSON object per line, one file per run.**

**Event model: closed discriminated union, keyed by `type`.** The v0
event types are:

- `agent_step` — the agent emits content / a decision
- `tool_call` — the agent invokes a tool with args
- `tool_result` — a tool returns (status: ok | error | empty)
- `state_read` — agent reads from a named state slot
- `state_write` — agent writes to a named state slot
- `spawn` — parent agent starts a subagent
- `terminate` — agent run ends (status: ok | error | timeout)

Every event carries: `type`, `ts` (ISO-8601), `run_id`, `step` (monotonic
int within run), `agent_id`. Parent/child runs are linked by `parent_run_id`
on the child's `terminate` (and on the parent's `spawn`).

**Extensibility: additive only.** New fields are optional with defaults.
New event types are added to the union. Existing fields never change
meaning — if semantics shift, the field is renamed and the old one
deprecated, never silently overloaded.

## Why these choices

**JSONL over a single JSON document.**
Traces are append-only event streams. JSONL lets a running agent flush
one line per event without ever rewriting the file, lets a detector
stream-process a 10MB trace without loading it whole, and survives
a crash mid-run with a valid prefix. A single JSON array doesn't.

**Closed union over an open `metadata` bag.**
Detectors are pattern matchers over event shapes. If `tool_result` can
hide its status inside an arbitrary `metadata` dict, every detector has
to defensively probe for it and the taxonomy patterns become unwriteable
in concrete terms. A closed union forces adapter authors to map their
agent's events into our model — that's the cost — but it makes detectors
*declarative* rather than defensive.

**`step` as a monotonic int.**
Timestamps alone are not enough — events within the same millisecond
need a deterministic order, and ordering is the only thing some patterns
(F-003 retry loop, F-004 ignored decision) depend on.

**`run_id` + `parent_run_id`, not nested traces.**
F-006 (subagent fabrication) needs cross-trace correlation. Flat files
linked by ID stay greppable, diffable, and parallelizable. Nested traces
force a tree parser into every tool that touches them.

## Consequences

**Positive**
- Detectors can be written as pure functions over typed events.
- Adapters from existing agent frameworks have a clear, narrow target.
- Test fixtures are just `.jsonl` files — readable in any editor.

**Negative**
- Adapters carry the impedance-matching cost. An agent framework whose
  native events don't map cleanly will need lossy translation.
- The closed union means adding a new event type is a schema change,
  not a config change — intentional friction.
- JSONL has no native cross-event referential integrity; we enforce
  it at parse time (e.g., `tool_result.call_id` must reference a prior
  `tool_call.call_id` in the same run).

## Rejected alternatives

- **OpenTelemetry spans.** Would inherit a mature ecosystem, but spans
  model duration and parent/child *intervals*, not the
  decision/state/result vocabulary patterns reference. Forcing our
  events into spans loses the very fields detectors need.
- **A free-form `event: dict` with no schema.** Faster to start, but
  pushes the schema into every detector's defensive code. We'd be
  re-discovering the schema implicitly across the codebase.
- **Protobuf / msgpack.** Faster I/O, hostile to humans. At hackathon
  scale traces are small and inspection matters more than throughput.
- **One trace per agent step (many small files).** Filesystem pressure,
  no obvious ordering primitive across files.
