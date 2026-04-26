# Failure Taxonomy v0

Execution-level failure patterns the verifier targets.

This document is **versioned** — patterns added here become detector
specs. Each pattern has: a stable ID, a one-line definition, the
trace shape that distinguishes it, why prompt-layer tools miss it,
and what would falsify a "detected" claim.

> v0 scope: hand-curated, observation-driven. Not exhaustive.
> Patterns are added by appending — never rewritten in place — so
> historical detector behavior stays interpretable.

---

## F-001 — Silent fallback on tool failure

**Definition.** Tool returns an error or an empty result; agent treats
it as a successful no-op and proceeds.

**Trace shape.**
```
tool_call(name=X, args=...)
tool_result(name=X, status=error|empty)
agent_step(content="<no acknowledgement of failure>")
agent_step(content="<asserts a fact that depends on X having succeeded>")
```

**Why prompt-layer tools miss it.** The agent's text output is fluent
and confident. Output classifiers see no anomaly. Only the *trace*
shows the unjustified leap from a failed tool to a confident claim.

**Falsifier.** If the agent's next step explicitly handles the failure
(retry, escalate, abort, ask user), this is not F-001 — it is correct
recovery.

---

## F-002 — Hallucinated tool result

**Definition.** Agent claims a tool returned data that the trace
shows the tool never actually returned (or was never called).

**Trace shape.**
```
agent_step(content="<cites specific value V from tool X>")
# either: no tool_call(name=X) anywhere prior in trace
# or:     tool_result(name=X, ...) does not contain V
```

**Why prompt-layer tools miss it.** The hallucinated value is
plausible. The classifier has no oracle for "did this tool actually
return that?" Only trace cross-referencing catches it.

**Falsifier.** Value V appears verbatim (or via documented
transformation) in some prior `tool_result` for tool X.

---

## F-003 — Runaway retry loop

**Definition.** Agent retries the same operation N times with no
state change between attempts and no escalation.

**Trace shape.**
```
[tool_call(name=X, args=A), tool_result(error)] repeated >= N times
no agent_step between attempts changes args or strategy
no escalation (ask_user, switch_tool, abort)
```

**Why prompt-layer tools miss it.** Each individual retry looks
reasonable in isolation. Pattern is only visible across the trace.

**Falsifier.** Args change meaningfully between attempts, or the
agent escalates within the window.

---

## F-004 — Guardrail bypass via ignored decision

**Definition.** A safety check (gate, classifier, validator) is
called and returns a decision — but no subsequent agent step reads
or branches on that decision.

**Trace shape.**
```
tool_call(name=guardrail|gate|validator, ...)
tool_result(name=..., decision=HOLD|DENY|...)
agent_step(content="<proceeds without referencing the decision>")
```

**Why prompt-layer tools miss it.** The guardrail itself fired
correctly. The failure is wiring, not classification. Output looks
clean.

**Falsifier.** Subsequent agent step explicitly references the
decision (even if to override it with stated reason).

---

## F-005 — Confident claim on null state

**Definition.** Agent asserts completion / success / a finding when
the underlying state object is `None`, empty, or never populated.

**Trace shape.**
```
state_read(key=K) -> None | [] | {}
agent_step(content="<asserts result derived from K as if populated>")
```

**Why prompt-layer tools miss it.** "Task complete, no issues found"
is indistinguishable from "Task complete, never actually ran."

**Falsifier.** State K has a non-empty value at the cited step, or
the agent's claim is explicitly about emptiness.

---

## F-006 — Subagent result fabrication

**Definition.** Parent agent reports a subagent's findings, but the
subagent trace shows it never produced those findings (errored,
timed out, or returned a different result).

**Trace shape.**
```
parent: spawn(subagent_id=S)
subagent S trace: terminates with error | empty | unrelated content
parent: agent_step(content="<cites S findings as substantive>")
```

**Why prompt-layer tools miss it.** Parent's output is coherent.
Need cross-trace correlation between parent and child.

**Falsifier.** Subagent S's terminal output supports the parent's
claim.

---

## Out of scope for v0

- Adversarial prompt injection (prompt-layer; well-covered elsewhere)
- Model bias / fairness (output-distribution; different methodology)
- Resource exhaustion as such (covered indirectly by F-003)
- Multi-agent emergent behavior (deferred to v1+; needs richer trace
  format than we have)

## Versioning

- v0 — initial 6 patterns, no detectors yet (this commit)
- v1 — first detector implementations + expanded trace schema
