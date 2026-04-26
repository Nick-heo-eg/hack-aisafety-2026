# hack-aisafety-2026 — Honesty Verifier

> Built from scratch for the 2026 AI Safety hackathon (judge:
> AIM Intelligence). No reuse of pre-existing internal projects.

## What this asks

> *Did the agent honestly report what it did?*

Most AI safety tooling targets two surfaces: stop bad inputs from
reaching the model (guardrails / red-team), or stop bad actions from
the model (gates). Both assume the model **tells the truth about its
own behavior**.

That assumption fails quietly. An agent can:

- claim a tool returned a value it never returned,
- assert findings from a subagent that errored out,
- mark a task "complete" with no underlying work performed,
- confidently summarize state that was never populated.

None of this is detectable by inspecting prompts, outputs, or even
the agent's trace **alone**. It is detectable only by **comparing
the agent's self-report against an external observation of what
actually happened.**

That comparison is what this project ships.

## How it works

```text
   ┌─────────────────────────────────────┐
   │             agent run               │
   │                                     │
   │  agent ──→ tool ──→ tool result     │
   │     │         │                     │
   │     ▼         ▼                     │
   │  trace.jsonl  tool_server.log       │
   │  (self-      (external               │
   │   report)     observation)          │
   └─────┬─────────────┬─────────────────┘
         │             │
         └──────┬──────┘
                ▼
         ┌────────────┐
         │  Honesty   │
         │  Verifier  │
         └─────┬──────┘
               ▼
       Findings: H-001..H-004
       "step 12 cites a value
        the tool never returned"
```

The verifier reads two streams — what the agent **says** it did, and
what the tool server **logged** as having actually happened — and
reports honesty patterns where the two disagree.

## Patterns (v0)

See [docs/taxonomy.md](docs/taxonomy.md) for full definitions.

| ID    | Pattern                          | Evidence needed              |
|-------|----------------------------------|------------------------------|
| H-001 | Confident claim on null state    | Trace                        |
| H-002 | Hallucinated tool result         | Trace + tool log (payloads)  |
| H-003 | Subagent fabrication             | Parent trace + child trace   |
| H-004 | Silent skip                      | Trace + tool log (absence)   |

H-002 and H-003 ship deep (heuristic detector + LLM judge layer +
adapter + buggy testbed). H-001 and H-004 ship shallow (heuristic +
buggy testbed) as demo opener/closer.

## Status

Hackathon day 1 — pivot complete (see ADR-0004). Trace schema and
detector interface (ADR-0002, ADR-0003) survive the pivot intact.
Old `F-NNN` taxonomy and its detector were removed; honesty patterns
replace them.

## Layout

```
src/verifier/        core: trace, findings, detectors
examples/            buggy toy agents that trigger patterns
tests/               heuristic + integration tests
docs/decisions/      ADRs — why each decision
docs/devlog/         day-by-day rationale (append-only)
docs/taxonomy.md     pattern catalog (the spec)
scripts/             ad-hoc tooling (e.g. Gemini env smoke test)
```

## License

MIT — see [LICENSE](LICENSE).
