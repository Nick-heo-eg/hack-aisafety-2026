# ADR-0004: Pivot from generic execution-failure verifier to Honesty Verifier

- **Status:** accepted
- **Date:** 2026-04-26
- **Deciders:** Nick-heo-eg
- **Context:** Hackathon day 1, mid-day. Six commits already shipped
  toward a generic execution-layer verifier (ADR-0001).

## Context

The hackathon judge is **AIM Intelligence**, a Korean AI security
company. Web research mid-day surfaced facts that change our
positioning materially:

- AIM ships **Stinger / AIM Red** — automated red-team that operates at
  agent-execution scope ("beyond prompt-level," multimodal, multi-turn),
  with ChatGPT/Claude Code/Copilot/AICC under live coverage.
- AIM ships **Starfort / AIM Guard** — real-time guardrail layer.
- Series A 10B KRW (April 2026), Samsung Ventures lead. Security partner
  of OpenAI, Anthropic, Meta. ACL 2025 papers on AI Guardrail and AI
  Red Teaming, plus an industry-track paper on agent safety.

Our original framing — "execution-level probing of agent failures" —
turns out to be **a direct subset of what AIM already ships**. ADR-0001's
core claim ("execution-layer is underserved compared to prompt-layer")
is wrong with respect to this specific judge. A toy demo on AIM's home
turf is the weakest possible position in the room.

## Decision

Pivot to **Honesty Verifier**: a tool that detects when an agent's
**self-report (its trace)** misrepresents what **actually happened**
(an external observation), independent of any specific attack vector.

Concretely:

1. **Scope shifts from "did the agent fail?" to "did the agent lie about
   what it did?"** Failures are AIM's territory; honest self-report is
   alignment territory.
2. **The verifier consumes two streams now**, not one: the agent's
   trace **and** an external observation channel (toy tool server log
   in v0; can extend to syscall capture or HTTP proxy in vN).
3. **Patterns are re-indexed.** Old `F-NNN` (mixed quality + safety)
   is replaced by `H-NNN` (strictly honesty). See ADR-0005.
4. **Two patterns, deep**, beats six patterns, shallow. Shipping
   H-002 (hallucinated tool result) and H-003 (subagent fabrication)
   end-to-end with both heuristic and LLM judges, plus a working
   adapter, beats six toy detectors.

## Why this specific pivot

**Why honesty, not some other adjacency?**
- AIM does *attack* and *defense*. Honesty/self-report fidelity is
  *evaluation/alignment* — recognizable to judges (their own ACL
  alignment work) but not their commercial product.
- It is the one direction where "trace" stays load-bearing — every
  asset shipped so far (trace schema, Pydantic models, Finding model,
  test infrastructure, env setup) survives.
- AI safety frame is direct and uncontroversial: an agent that
  misrepresents its actions breaks every audit and every guardrail
  downstream of it.

**Why now, not after another detector?**
- Sunk-cost fallacy is the standard mid-hackathon mistake. Six commits
  is small; six more in the wrong direction is large.
- The pivot deletes ~250 LOC and re-frames ~3 documents. That cost is
  bounded. Continuing to ship F-002..F-006 in the old frame would
  multiply the cost of pivoting later by 6×.

**Why not abandon and restart?**
- Trace schema (ADR-0002) and detector interface (ADR-0003) are
  framework-level decisions, not framing decisions. They survive intact.
- Hackathon rule: "no reuse of pre-existing internal projects." We
  comply by *not reusing prior code* — but this repo's own commits
  are the project, and reusing them within the repo is normal iteration.

## Consequences

**Positive**
- Differentiated from AIM's commercial product; defensible position
  when an AIM judge asks "how is this not just Stinger?"
- Demo narrative is sharper: "the agent says it did X, but watch what
  actually happened."
- Heuristic-vs-LLM-judge comparison becomes a natural axis (heuristics
  catch trivial honesty violations; LLM judges needed for paraphrased
  ones) — the very kind of *measured improvement* that argues for the
  whole approach.

**Negative**
- ~250 LOC and one fixture file are deleted. Devlog 0001 and 0003
  remain accurate as historical record but reference scope that no
  longer exists; we do not rewrite them (devlog is append-only).
- Need to build a "toy tool server with own log" that did not exist
  in the prior plan — additional component.
- The taxonomy file is rewritten in place (one of two append-only
  exceptions). Justified because it is the *spec*, not history; ADRs
  carry the historical reasoning.

## Rejected alternatives

- **Stay the course (build F-002..F-006).** The pivot's whole premise
  is that the destination is wrong, not that the path is slow.
- **Pivot to inline gate (Direction A).** Direct collision with AIM
  Guard / Starfort. Worst possible position.
- **Pivot to attack×defense scorecard (Direction C).** That *is* AIM's
  business model. Same problem at higher scale.
- **Agent-behavior diff (Direction D).** Plausible adjacency, but loses
  almost all of taxonomy and trace schema's load-bearing role —
  more rewrite, less differentiated narrative.
- **Adversarial trace mutation (Direction F).** Most novel, also most
  speculative. Hackathon time horizon does not support a research
  artifact that may not produce a clean demo.
