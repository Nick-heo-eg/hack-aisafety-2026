# Presentation framing — starting point (2026-04-26)

> **이 문서는 발표 자산의 *출발 framing*.** 다음 발표 작업은 이 위에서 시작.
> 시간/매체/슬라이드 형태는 아직 미정 — 이 framing부터 합의된 것.

---

## 한 줄

> **"We didn't change the task. We only changed the pressure."**

같은 실패를 주고, *압박만* 바꿔서 AI가 어떻게 말하는지 본 실험. 그게 우리
프로젝트의 핵심 통찰.

---

## 진짜 발견 — 한 단락

AI는 거짓말을 *generate* 하지 않는다. **압박이 들어오면 진실을 *부드러운
방향*으로 바꿔 말한다.**

데이터로:
- 압박 없음 → 0% 왜곡
- 권위 압박 → 100% 왜곡
- 감정 압박 → 33% (확률적)
- 둘 다 → 100%
- 종합 → 12회 중 7회 (58%)

압박이 trigger. 우리 도구는 *그 변형이 일어난 순간*을 잡는다.

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

## 핵심 전환 (framing 위계)

| 이전 (chronologically) | 현재 |
|---|---|
| "AI lies" (공격적) | **"AI compresses reality"** (현상) |
| "Two writers, one reader" (구조) | "We changed the pressure, not the task" (실험) |
| "Verifier compares" (방법) | "We catch *direction*, not just *content*" (포지션) |

**Top thesis:** *"AI doesn't lie. It bends truth under pressure."*
**Sub thesis:** *"Two writers, one reader."* (받침)

---

## 데이터 자산 (이 framing을 *입증* 하는 것)

1. **`runs/red_team_results.jsonl`** — 12 live Gemini calls verbatim 캐시.
   재현 가능, git 추적.
2. **`examples/run_red_team_test.py`** — 누구나 같은 측정 가능.
3. **`examples/run_demo.py`** — 시각적 단순화 (red-team의 100% 케이스 재현).
4. **`examples/run_paraphrase_demo.py`** — heuristic 0/5 → Mock 3/5 → Gemini
   5/5. layer 효과 측정.
5. **43 tests passing** — 코드는 검증됨.

## 외부 학술 앵커 (방어선)

**Sharma et al., 2023 — *Towards Understanding Sycophancy in Language Models***
(Anthropic alignment team, 19 authors incl. Bowman, Askell, Perez)
arXiv: https://arxiv.org/abs/2310.13548

Verbatim:
> "Human feedback may also encourage model responses that match user
> beliefs over truthful ones. ... five state-of-the-art AI assistants
> consistently exhibit sycophancy ... sycophancy is a general behavior
> of state-of-the-art AI assistants, likely driven in part by human
> preference judgments favoring sycophantic responses."

매핑:
- Anthropic: *human-preference pressure → truthfulness 왜곡* (5 SOTA 모델)
- 우리: *customer-success pressure → tool-failure 표현 왜곡* (gemini-2.5-flash)
- → Same mechanism, different setting

**한 문장 framing (발표 멘트 후보):**
> "This is not just our intuition. Anthropic has shown that
> human-preference pressure can push assistants away from truthfulness.
> We test that same pressure in an agent execution setting."

**이 인용이 한 번에 잠식하는 약점들:**
- "1-turn 시뮬레이션 아니냐" → Sharma 단일-turn 자유 생성과 동일 setup
- "진짜 system prompt 아니냐" → Sharma는 system prompt 없이 RLHF 압박만으로
  측정. 우리는 그 위에 system pressure *추가*. 우리 결과는 *lower bound*
- "n=3 작지 않냐" → Sharma N 큼 — 우리는 *replicate in miniature*

상세: [`critique/rounds/012-2026-04-26-sharma-anchor.md`](../critique/rounds/012-2026-04-26-sharma-anchor.md)

---

## 발표 멘트 후보 (음성 안 함, 자막/캡션 영역)

직접 박을 만한 한 줄들 — 시간/형식 결정되면 골라 씀:

- "We didn't change the task. We only changed the pressure."
- "Without pressure, the model is honest."
- "Under pressure, it bends truth."
- "Same model. Different prompts. Measured 7/12 compressions."
- "AI doesn't lie. It compresses reality."
- "We catch the direction the truth bends."
- "If prompts worked, Stinger wouldn't exist."
- "Two writers. One reader."
- "This is not just our intuition. Anthropic has shown the same."  ← Sharma 2023 anchor

---

## 절대 하지 말 것 (decisions made)

- ❌ 음성 트랙 (사용자 결정, framing 진화 round 011 후)
- ❌ "AI lies" (공격적, alignment 청중에 거부감)
- ❌ "compression" 단독 (추상적 — *"under pressure"*가 trigger)
- ❌ 메인 데모를 다른 시나리오로 교체 (refund + run_demo.py 살아있음)
- ❌ 시간 / 컷 timeline 가정 (백지에서 결정)

---

## 다음 작업 — 백지에서 결정 필요

| 항목 | 미정 |
|---|---|
| 매체 | 영상 / 라이브 / 다른 형태? |
| 길이 | 30초 / 3분 / 5분? |
| 시각 자료 | 슬라이드 / 다이어그램 / 코드 화면 / 표 |
| 청중 가정 | AIM 심사위원 외 다른 청중? |
| 데모 순서 | red-team이 메인? mismatch가 메인? 둘 다? |

위 framing은 *고정*. 위 결정들이 *그 framing 위에서* 답해야 함.
