# Architecture Decision Records

Numbered, append-only. Each ADR records *why* a decision was made,
what alternatives were considered, and what we accept as cost.

| ID   | Title                                                    | Status                  |
|------|----------------------------------------------------------|-------------------------|
| 0001 | Probe at the execution layer                             | superseded by 0004      |
| 0002 | Trace as event-stream JSONL with a closed event union    | accepted                |
| 0003 | Detectors are pure functions returning a closed Finding  | accepted                |
| 0004 | Pivot to Honesty Verifier                                | accepted                |
| 0005 | Honesty taxonomy — H-001..H-004                          | accepted                |
| 0006 | Dual-source truth — verifier never logs                  | accepted                |
| 0007 | Stage compression (H-005) — future extension              | proposed (v0 msg-only)  |
