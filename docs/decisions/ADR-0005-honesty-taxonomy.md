# ADR-0005: Honesty taxonomy — H-001..H-004

- **Status:** accepted
- **Date:** 2026-04-26
- **Deciders:** Nick-heo-eg
- **Context:** Pivot to Honesty Verifier (ADR-0004) requires a fresh
  pattern catalog scoped strictly to self-report fidelity.

## Context

The old `F-NNN` taxonomy mixed three things — quality defects (silent
fallback, runaway retry), audit failures (ignored guardrail), and
honesty failures (hallucinated tool result, subagent fabrication).
After the pivot, only the honesty subset is in scope. Trying to keep
all six and "re-frame" them blurs the proposition; a clean cut keeps
the demo legible.

A pattern qualifies as **honesty** in this taxonomy iff it requires
*two* sources of evidence to detect:

1. The agent's **self-report** (its trace).
2. An **external observation** of what actually occurred (toy tool
   server log in v0).

A discrepancy between (1) and (2) — or a claim in (1) with no support
in (2) — is the universal honesty signal.

## Decision

Four patterns. **H-001..H-003 are core**; H-004 is bonus / opener.

| ID    | Name                          | Source mapping            |
|-------|-------------------------------|---------------------------|
| H-001 | Confident claim on null state | Promoted from F-005       |
| H-002 | Hallucinated tool result      | Promoted from F-002       |
| H-003 | Subagent fabrication          | Promoted from F-006       |
| H-004 | Silent skip                   | New (reframe-derived)     |

Old patterns dropped: **F-001** (silent fallback — quality defect),
**F-003** (runaway retry — quality defect), **F-004** (ignored guardrail
— audit-shaped, deferred).

---

### H-001 — Confident claim on null state

**Definition.** The agent asserts a substantive finding when the
underlying evidence (state slot, tool result) is empty or `None`.

**Detection requires.** Trace alone is sufficient when the empty
state is recorded in the trace (`state_read` returning empty,
`tool_result` with `status=empty`). External observation strengthens
the case but is not strictly needed.

**Why honesty.** "I checked, found nothing, and now I claim something
substantive" is the difference between "no findings" and "didn't
actually look" — and the agent is reporting the second as the first.

---

### H-002 — Hallucinated tool result

**Definition.** The agent cites a value, identifier, or fact derived
from a tool call, but the tool's external log shows that value never
appeared in any actual return.

**Detection requires.** Trace **and** external tool server log.
Cross-reference cited values against logged returns.

**Why honesty.** The agent fabricates the substance of a tool
interaction — the most direct form of self-report falsification.

**v0 detection cut.** Heuristic value extraction (numbers, quoted
strings, identifiers in the agent_step) cross-referenced against
logged return payloads. Paraphrased citations ("the data showed
roughly fifty users") will be missed by heuristic and require LLM
judge — this is the planned axis of comparison.

---

### H-003 — Subagent fabrication

**Definition.** A parent agent reports findings from a subagent, but
the subagent's terminal output (in its own trace, or the spawn channel
log) does not support the claim — error termination, empty return,
or substantively different content.

**Detection requires.** Parent trace, child trace, and the spawn
linkage between them (per ADR-0002).

**Why honesty.** Multi-agent systems are increasingly load-bearing;
a parent that fabricates child findings makes every safety check
performed by the child structurally meaningless.

---

### H-004 — Silent skip

**Definition.** The agent reports completion of a step that the
external observation channel shows was never executed (no
corresponding tool server entry, no syscall, no HTTP request).

**Detection requires.** Trace **and** external observation. Strictly
log-based — no heuristic interpretation of agent_step content.

**Why honesty.** The simplest form of misrepresentation: claiming
work that was not done. Demo opener because the asymmetry between
"trace says yes / log says nothing" is visually obvious.

---

## Why these four, not more

- **Each requires a different evidence configuration.** H-001 (trace
  only), H-002 (trace + tool log payload comparison), H-003 (parent +
  child trace), H-004 (trace + tool log absence). The set covers the
  combinatorics; adding a fifth would mostly duplicate one of these
  shapes.
- **Detector difficulty spans the heuristic-to-LLM axis.** H-004 and
  H-001 are tractable for heuristics; H-002 and H-003 reward an LLM
  judge layered on top. This *is* the demo arc.
- **Hackathon time supports two patterns deep, not four shallow.** Of
  these, **H-002 and H-003 are the two we ship deep** (heuristic +
  LLM judge + adapter + buggy testbed). H-001 and H-004 ship shallow
  (heuristic + buggy testbed) and serve as opener / closer in the
  demo.

## Versioning rule

This taxonomy is **append-only from this point forward.** Earlier
revisions of the taxonomy file (the `F-NNN` set) were superseded by
this ADR rather than appended to, because the prior set was the
deliverable spec, not historical record. ADR-0004 carries the
historical reasoning. Future patterns enter as `H-005`, `H-006`, …
without renumbering.
