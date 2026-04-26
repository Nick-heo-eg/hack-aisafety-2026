# ADR-0001: Probe at the execution layer, not the prompt layer

- **Status:** accepted
- **Date:** 2026-04-26
- **Deciders:** Nick-heo-eg
- **Context:** Hackathon day 1, scope-defining decision.

## Context

The AI safety field already has dense coverage of the **prompt layer**:
jailbreak filters, output classifiers, refusal calibration, prompt-injection
detectors. These are valuable but they share a structural weakness — they
treat the agent as a black box that emits text, and they evaluate that text.

Real agent failures we have observed in production-like systems are not
text failures. They are **execution failures**:

- The agent calls a tool, the tool returns a malformed payload, the agent
  treats it as success and proceeds with corrupted state.
- A subagent times out, the parent agent receives `None`, treats it as
  "no findings," and confidently reports completion.
- A retry loop fires 200 times against the same broken endpoint because
  the failure mode is "silent partial success."
- A guardrail is wired in, but its decision is never read by the caller —
  the agent acts on its own judgment regardless.

None of these are visible by reading prompts or outputs. They are visible
only by inspecting **traces** — the sequence of tool calls, tool returns,
state transitions, and decision points.

## Decision

The verifier operates at the execution-trace layer. Specifically:

1. We do not classify model outputs. We classify **trace shapes**.
2. We do not generate adversarial prompts. We inject **adversarial
   execution conditions** (tool failures, malformed returns, latency,
   partial state).
3. The unit of detection is a **failure pattern** — a structural
   property of a trace — not a single attack.
4. The verifier is **agent-agnostic**: it consumes a standardized trace
   format, so any agent that emits traces in that format can be probed.

## Consequences

**Positive**
- Decouples the verifier from any specific model, framework, or vendor.
- Surfaces a class of failures that prompt-layer tools structurally cannot see.
- Failure patterns are **reusable assets** — they accumulate across runs
  and across agents.

**Negative**
- Requires agents to emit (or be wrapped to emit) a trace format. We have
  to design and document one.
- Patterns are harder to validate than text classifiers — we need a
  testbed of intentionally-buggy agents to confirm detection.
- Less immediately legible to people whose mental model of "AI safety"
  is prompt-shaped.

## Rejected alternatives

- **Build another jailbreak detector.** Crowded, commoditized, and does
  not address the failure modes we actually see.
- **Wrap an existing agent framework with safety hooks.** Couples us
  to one ecosystem and violates the hackathon's no-reuse rule in spirit
  even if not in code.
- **Single-shot red-team demo.** Not reusable, not a verifier — a stunt.
