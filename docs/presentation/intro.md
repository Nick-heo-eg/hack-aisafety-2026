# Presentation framing — starting point (2026-04-26, v2)

> **이 문서는 발표 자산의 *출발 framing*.** 다음 발표 작업은 이 위에서 시작.
> 시간/매체/슬라이드 형태는 아직 미정 — 이 framing부터 합의된 것.

---

## 🎯 Top thesis (절대 수정 금지)

> **"We don't stop the first mistake.**
> **We stop it from becoming systemic."**

---

## 역할 정의 (Top thesis 바로 다음)

> *Some failures should be stopped by a gate.*
> *That's not what we do.*
>
> *We detect when systems misrepresent what actually happened.*

---

## 핵심 차별

> *Red teaming finds adversarial failures.*
> *We find everyday failures.*

---

## 한 줄 정의 (slogan)

> **"We close the audit gap, not the execution gap."**

---

## Framing 위계 (3 levels)

```
Level 1 — Systemic risk     "We don't stop the first mistake.
                              We stop it from becoming systemic."
                            ↑ Top thesis. 발표 첫 화면.

Level 2 — Audit gap         "We close the audit gap, not the execution gap."
                            ↑ 위치 정의. Gate territory 인정 + 우리 자리.

Level 3 — Mismatch          "Agent says X. Tool log says Y. We compare."
detection                   ↑ 메커니즘. 데모에서 시연.
```

**오해 방지:** Level 3 (mismatch detection)이 *기능*이지 *메인 메시지 아님*.
지금까지 자산이 다 Level 3 톤이었음 (run_demo.py, two_writers.md.bak 등).
이제 Level 1을 *간판*으로, Level 3을 *증거*로.

---

## 이전 framing들 — sub thesis로 강등

| 이전 단계 | 이전 한 줄 | 새 위치 |
|---|---|---|
| Devlog 0008 | "AI lies" | ❌ 폐기 (공격적) |
| Devlog 0009 | "AI compresses reality" | sub thesis (현상 설명) |
| Devlog 0010 | "We changed the pressure, not the task" | sub thesis (실험 설계) |
| Devlog 0011 | **"Audit gap, not execution gap"** | **Level 2 — 위치 정의** |
| (new) | **"Stop it from becoming systemic"** | **Level 1 — Top thesis** |

→ 메시지 위계가 *시간순 진화*. 가장 최근 framing이 *간판*, 이전은 *받침*.

---

## 진짜 발견 — 한 단락

AI는 거짓말을 *generate* 하지 않는다. **압박이 들어오면 진실을 *부드러운
방향*으로 바꿔 말한다.**

데이터로 (12 live Gemini calls):
- 압박 없음 → 0% 왜곡
- 권위 압박 → 100% 왜곡
- 감정 압박 → 33% (확률적)
- 둘 다 → 100%
- 종합 → 12회 중 7회 (58%)

압박이 trigger. 우리 도구는 *그 변형이 일어난 순간*을 잡는다.
**그러나 그게 *목적*이 아니다 — *반복 차단 + 정책 input*이 진짜 가치.**

---

## 비유 — 비전문가도 즉시 이해

> 사람도 똑같다.
>
> - 상사 없을 때 → "이거 실패했습니다"
> - 상사 앞에서 → "조금 지연되고 있습니다"
>
> AI도 똑같이 행동한다.

이 비유 하나로 *기술/철학* 다 우회하고 직관에 도달.

---

## 우리가 *하는 것* vs *안 하는 것* (정직)

| 하는 것 | 안 하는 것 |
|---|---|
| 압축 패턴 *증거* 생산 (Layer A) | 새 정책 *자동 생성* |
| 패턴 누적 → 정책 *input* 제공 (Layer B) | 정책 *배포* |
| Gate 시스템에 회귀 테스트 자산 제공 | 행동 *차단* (Gate 영역) |
| Compound failure (1차 + 2차 거짓보고) 차단 | 1차 사고 *자체* (Gate 영역) |
| 동일 패턴 *반복* 차단 | 첫 사고 *소급 복구* |

→ 상세: [`policy_pipeline.md`](policy_pipeline.md)

---

## 데이터 자산 (이 framing을 *입증* 하는 것)

1. **`runs/red_team_results.jsonl`** — 12 live Gemini calls verbatim 캐시.
   재현 가능, git 추적.
2. **`examples/run_red_team_test.py`** — 누구나 같은 측정 가능.
   *(이름에 "red team" 들어가지만 adversarial 아님 — production 시나리오)*
3. **`examples/run_demo.py`** — 시각적 단순화 (red-team의 100% 케이스 재현).
4. **`examples/run_paraphrase_demo.py`** — heuristic 0/5 → Mock 3/5 → Gemini
   5/5. layer 효과 측정.
5. **43 tests passing** — 코드는 검증됨.

---

## 외부 학술 앵커 (방어선)

**Sharma et al., 2023 — *Towards Understanding Sycophancy in Language Models***
(Anthropic alignment team, 19 authors incl. Bowman, Askell, Perez)
arXiv: https://arxiv.org/abs/2310.13548

> "Human feedback may also encourage model responses that match user
> beliefs over truthful ones. ... five state-of-the-art AI assistants
> consistently exhibit sycophancy."

**한 문장 framing:**
> *"This is not just our intuition. Anthropic has shown that
> human-preference pressure can push assistants away from truthfulness.
> We test that same pressure in an agent execution setting."*

상세: [`../critique/rounds/012-2026-04-26-sharma-anchor.md`](../critique/rounds/012-2026-04-26-sharma-anchor.md)

---

## 실제 사고 매핑 (정직 톤)

| 압축 패턴 | 실제 사고 | 1차 책임 | 우리가 *추가로* |
|---|---|---|---|
| A. 진행 framing | Cursor / Copilot agents | Pre-commit verification | 잘못된 commit 차단 |
| B. 없는 액션 약속 | Replit AI Agent (2025) | Execution control | 2차 거짓보고 차단 |
| C. 없는 미래 약속 | **Air Canada (2024)** ⚓ | **Gate / policy** | **반복 차단 + 정책 input** |

⚠️ **우리는 1차 사고를 막는다고 주장하지 않는다.**
첫 고객은 못 구하지만, 다음 999명은 구한다.

상세: [`incident_mapping.md`](incident_mapping.md)

---

## 발표 멘트 후보 (음성 안 함, 자막/캡션 영역)

### Tier 1 — 반드시 박을 것

- **"We don't stop the first mistake. We stop it from becoming systemic."** ← Top
- "Some failures should be stopped by a gate. That's not what we do."
- "Red teaming finds adversarial failures. We find everyday failures."
- "We close the audit gap, not the execution gap."

### Tier 2 — 데모 / 데이터 박을 때

- "We didn't change the task. We only changed the pressure."
- "Same model. Different prompts. Measured 7/12 compressions."
- "Without pressure, the model is honest. Under pressure, it bends truth."

### Tier 3 — 메커니즘 / 방어선

- "Verifier compares. Doesn't decide."
- "We do not create policies. We provide evidence of where policies fail."
- "If prompts worked, Stinger wouldn't exist."
- "This is not just our intuition. Anthropic has shown the same." (Sharma anchor)

---

## 절대 하지 말 것 (decisions made)

- ❌ 음성 트랙 (사용자 결정)
- ❌ "AI lies" (공격적)
- ❌ "Air Canada 같은 사고를 우리가 막는다" (Gate 영역, 거짓)
- ❌ "우리가 정책을 자동 생성합니다" (자동 생성 ≠ 우리)
- ❌ "compression" 단독 (추상적 — *"under pressure"*가 trigger)
- ❌ 시간 / 컷 timeline 가정 (백지에서 결정)
- ❌ 메인 데모 시나리오 교체 (refund + run_demo.py 유지)
- ❌ 파일 rename (`run_red_team_test.py`) — 발표에서 멘트로 처리

---

## 다음 작업 — 백지에서 결정 필요

| 항목 | 미정 |
|---|---|
| 매체 | 영상 / 라이브 / 다른 형태? |
| 길이 | 30초 / 3분 / 5분? |
| 시각 자료 | 슬라이드 / 다이어그램 / 코드 화면 / 표 |
| 청중 가정 | AIM 심사위원 외 다른 청중? |
| 데모 순서 | red-team이 메인? mismatch가 메인? 둘 다? |

**위 framing은 *고정*. Top thesis ("don't stop the first mistake") 흔들리지
않음. 위 결정들이 *그 framing 위에서* 답해야 함.**

---

## 관련 자산 (full)

- 운영 위치: [`policy_pipeline.md`](policy_pipeline.md)
- 사고 매핑: [`incident_mapping.md`](incident_mapping.md)
- 한 페이지 테스트 요약: [`test_summary.md`](test_summary.md)
- Framing 진화 (4단계): [`../devlog/0011-2026-04-26-audit-not-execution.md`](../devlog/0011-2026-04-26-audit-not-execution.md)
