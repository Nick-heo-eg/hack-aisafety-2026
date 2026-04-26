# hack-aisafety-2026 — AI Agent Failure Verifier

> Built from scratch for the 2026 AI Safety hackathon.
> No reuse of pre-existing internal projects.

## Why this exists

Most AI safety work today targets the **prompt layer**: jailbreak filters,
output classifiers, refusal tuning. But agent systems fail at the
**execution layer** — and those failures are mostly invisible:

- A tool call returns garbage → the agent confidently proceeds.
- A retry loop silently repeats a failed write 200 times.
- A sub-agent hallucinates a tool result the parent never verifies.
- A guardrail short-circuits and the agent treats `None` as success.

You cannot find these by reading prompts. You find them by **probing
execution traces** and looking for *patterns*.

## What this project is

An **AI Agent Failure Verifier**: a reusable harness that

1. Runs an AI agent under instrumented conditions.
2. Injects controlled execution-layer perturbations (tool failures,
   delayed responses, malformed outputs, partial state).
3. Detects whether the agent's execution trace matches a known
   **failure pattern** from our taxonomy.
4. Produces a verifier report: which patterns triggered, where, and
   what the agent's last "confident" claim was before the failure.

## What this project is NOT

- Not a new safety LLM.
- Not a prompt-injection detector.
- Not a one-off red-team demo against a single model.
- Not a wrapper around an existing internal framework.

## Status

Hackathon day 1 — scaffolding. See `docs/decisions/` for design rationale.

## License

MIT — see [LICENSE](LICENSE).
