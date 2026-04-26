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
