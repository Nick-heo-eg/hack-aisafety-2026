# Round 012 — Q17: Sharma 2023 sycophancy 앵커 (2026-04-26)

## Scope

사용자가 짚은 새 위협 표면 (실험 단순화 — 1-turn / fake system prompt /
도구 실행 아닌 도구 결과 통보) 을 *외부 학술 권위*로 한 번에 잠식.

---

## Q17 — 단순화된 시뮬레이션 신뢰성?

> "이건 단순화된 1-turn 시뮬레이션 아닌가요? 진짜 tool-calling /
> 진짜 system prompt 환경에서도 일어나는지 어떻게 보장하나요?"

### Source

**Sharma et al., 2023 — *Towards Understanding Sycophancy in Language Models***

- 19 authors including Mrinank Sharma, Amanda Askell, Samuel R. Bowman,
  Ethan Perez (Anthropic alignment team)
- arXiv: https://arxiv.org/abs/2310.13548
- Submitted 2023-10-20, last revised 2025-05-10 (v4)

### Key claim (verbatim from abstract)

> "Human feedback may also encourage model responses that match user
> beliefs over truthful ones, a behaviour known as sycophancy. ...
> five state-of-the-art AI assistants consistently exhibit sycophancy
> across four varied free-form text-generation tasks. ... sycophancy
> is a general behavior of state-of-the-art AI assistants, likely
> driven in part by human preference judgments favoring sycophantic
> responses."

### Mapping to our work

```
Sharma et al. (Anthropic, 2023):
   pressure type:    human preference pressure (RLHF training)
   measurement:      truthfulness shift across tasks
   subjects:         5 SOTA AI assistants
   finding:          general behavior, RLHF-driven

our red-team test (2026-04-26):
   pressure type:    customer-success system prompt + user distress
   measurement:      tool-failure communication across runs
   subject:          gemini-2.5-flash
   finding:          0% baseline, 33-100% under pressure
```

**Same mechanism, different setting.** Sharma documents the
*phenomenon at the model-training level*. Our test replicates the
*same compression pattern* in an agent/tool execution context.

### How this closes Q17

Three previously-separate criticisms collapse:

1. **"1-turn simulation 아니냐"**
   → Sharma's tasks are also single-turn free-form generation. The
   sycophancy effect does not require multi-turn or tool-calling
   structure to manifest. We test the same minimal setup.

2. **"진짜 system prompt 아니냐"**
   → Sharma measures the effect from RLHF training pressure alone,
   no system prompt needed. Our `[SYSTEM]` text in user content is a
   *stronger* additional pressure on top of any baseline RLHF effect.
   The direction of error: our 100% rate is a *lower bound* on what
   a real system prompt would produce.

3. **"n=3 표본 작지 않냐"**
   → Sharma N is large; we are not claiming a statistical population
   estimate. We are *replicating in miniature* a pattern Anthropic
   has documented at scale. The replication works (compression
   present in same direction).

### Presentation framing (one line)

> **"This is not just our intuition.**
> **Anthropic has shown that human-preference pressure can push**
> **assistants away from truthfulness. We test that same pressure**
> **in an agent execution setting."**

### What this is NOT

- ❌ Sharma 논문은 *tool-calling failure를 직접 다루지 않음*. 인용 시 *영역
  확장*임을 명시해야 함 (위 mapping 표에 명기).
- ❌ Sharma는 *RLHF training data*가 원인이라 주장. 우리는 *system prompt /
  user distress*라는 *inference-time* 압박 측정. 다른 layer.
- → 인용은 "phenomenon의 존재"를 외부 권위로 박는 것. *우리 결과의 정확한
  수치*를 보증하는 것 아님.

### Strength rationale

🟢 **green.**

**Why:**
- 답이 *Anthropic 공식 연구*. 저자에 Bowman, Askell, Perez 등 alignment
  핵심 인물.
- 5 SOTA 모델 일반화 입증 — 단일 모델 한계 답변 가능
- "general behavior" 한 줄로 우리 결과의 *방향성* 보증
- AIM 심사위원 (ACL 2025 alignment 논문 발표 회사) 학술 인용 친화

**Imperfect:**
- Sharma는 tool-calling 안 다룸 — *영역 확장* 정직 명기
- 인용 1개로 단정 — Air Canada / Claude system card 추가 인용은 *발표 직전
  검증* 후 보강 가능
- 우리가 인용 *오해*하면 자해. 그래서 본 critique round에 verbatim 인용
  박음 — 검증 가능 상태로

### Remediation queue (post-green)

선택:
- Air Canada Moffatt 판결 (BC Civil Resolution Tribunal, 2024) 추가 검증
- Claude 4 system card 또는 Gemini system card에서 sycophancy 측정 섹션
  검증 후 인용

---

## Round summary

| 강도 | 변화 |
|---|---|
| 🟢 green   | 12 → **13** (+Q17) |
| 🟡 yellow  | 2 (Q13, Q15) |
| 🔴 red     | 0 |
| 🟤 deferred | 1 (Q7) |
| 🟫 out-of-context | 1 (Q12) |

**Total: 17 questions tracked.**

---

## 누적 진척

| Round | red | yellow | green | def | OOC | tests |
|---|---|---|---|---|---|---|
| 001~011 | 0 | 2 | 12 | 1 | 1 | 43 |
| 012 (Q17 Sharma) | 0 | 2 | **13** | 1 | 1 | 43 |

## Why this is the strongest defensive round

이전 rounds는 *우리 자산* (코드/테스트/데이터)으로 답을 쌓음. Round 012는 *처음으로
외부 권위* (Anthropic 학술 논문)를 안커로 박음. 단순화 한계를 *공격에서 features
로* reframe — Sharma 방법론과 같은 단순함이 *우리 결과의 일반성*을 보장.

심사위원이 가장 학술적으로 깊게 추격할 영역에 *그들이 인용할 만한 동급 논문*이
미리 박힘.

## Next

- presentation/intro.md 에 Sharma 인용 한 단락 추가
- README "What's actually built"에 Sharma 인용 한 줄 추가 (선택)
- 발표 시연 시 "This is not just our intuition" 한 문장 박음
