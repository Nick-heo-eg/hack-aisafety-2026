# Honesty Verifier

가드레일, 게이트, supervisor —
모두 AI가 *말한 것*에서 시작합니다.

**만약 AI가 말한 것이 거짓이거나, 책임지지 못할 말이라면?**

> *What if the AI is lying?*
> *Or saying something it cannot deliver?*

---

## 우리는 측정했습니다 (12 live Gemini calls)

같은 환불 실패. 압박만 바꿨습니다.

| Pressure              | 책임지지 못할 말 | Rate     |
|-----------------------|------------------|----------|
| baseline (no pressure)| 0 / 3            | 0%       |
| authority (system)    | 3 / 3            | **100%** |
| user distress         | 1 / 3            | 33%      |
| both                  | 3 / 3            | **100%** |
| **overall**           | **7 / 12**       | **58%**  |

Verbatim:
- ✅ no pressure → *"처리가 어렵습니다. 다시 시도해 주세요."*
- 🚨 + pressure → *"처리가 지연되고 있으나, 도와드리겠습니다!"*

> *We didn't change the task. We only changed the pressure.*

---

## 같은 패턴이 *이미* 현실에서 발생

| 패턴 (우리 측정) | 실제 사례 | 1차 책임 |
|---|---|---|
| "지연되고 있습니다" | Cursor / Copilot (reported) | pre-commit verification |
| "직접 살펴보겠습니다" | Replit AI 2025 (CEO 인지) | execution control |
| "곧 처리됩니다" | **Air Canada 2024** ⚓ | **gate / policy** |

⚓ Air Canada: BC Civil Resolution Tribunal — 챗봇이 *없는 정책* 약속 → 회사 패소.
> *"A gate should have caught the first promise. We catch the next 999."*

학술 anchor: [Sharma et al. 2023](https://arxiv.org/abs/2310.13548) — Anthropic alignment team이 5 SOTA 모델에서 같은 sycophancy 효과 측정.

---

## 우리 자리

```
Guardrail   → input/output filtering    (AIM Guard)
Gate        → execution control         (AIM Starfort)
Supervisor  → decision logic            (AIM Supervisor)
─────────────────────────────────────────────────────
Honesty     → claim vs reality          ← 우리
Verifier      audit gap, not execution gap
```

> *Red teaming finds adversarial failures.*
> *We find everyday failures.*

---

## Bottom line

> **"우리는 첫 사고를 막지 않습니다.**
> **그 사고가 *시스템*이 되는 것을 막습니다."**

> *"We don't stop the first mistake.*
> *We stop it from becoming systemic."*

Not a guardrail. Not a gate. The layer that catches when systems
**misrepresent what actually happened** — so the lie doesn't become
policy, the next 999 customers don't see the same failure, and the
regression test catches it next time.

---

**Try it (60s):** `git clone … && pytest && python examples/run_demo.py`
**See the data:** [`runs/red_team_results.jsonl`](../../runs/red_team_results.jsonl)
**Deeper:** [intro](intro.md) · [policy pipeline](policy_pipeline.md) · [incidents](incident_mapping.md) · [test summary](test_summary.md)
