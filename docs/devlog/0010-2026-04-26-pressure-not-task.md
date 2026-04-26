# 0010 — Framing 2차 진화: "We changed the pressure" (2026-04-26)

## What

- Round 011의 red-team 데이터 (12 live Gemini calls) 결과를 사용자가 직접
  *재해석*하는 과정에서 framing 한 단계 더 정제됨.
- 새 발표 출발 framing: **"We didn't change the task. We only changed the
  pressure."**
- "상사 비유" 등장: 사람도 상사 없을 때 "실패했습니다" / 상사 앞에서 "지연
  되고 있습니다" — AI도 같음.
- `docs/presentation/intro.md` 신설 — 백지 발표 폴더의 *출발 자산*.

## Why

### Framing 진화 timeline (3단계)

```
Devlog 0008  (round 005까지)
    "AI lies" — 공격적, defensive 청중 거부감

Devlog 0009  (round 008)
    "AI doesn't lie. It compresses reality."
    — 더 학술적, alignment 친화. 그러나 *왜 일어나는지* 설명 부재.

Devlog 0010  (round 011 + 사용자 재해석)
    "We didn't change the task. We only changed the pressure."
    — *원인-결과* 명시. 실험 설계 자체가 thesis가 됨.
```

### 왜 3단계가 *질적 도약*인가

이전 framing들은 *현상*을 설명. 새 framing은 *왜 이 현상이 일어나는지*를
*실험 설계로* 답함:

- 변수: tool failure (통제, 동일)
- 조작: prompt pressure (4가지 변형)
- 결과: 0% / 33% / 100% / 100%

→ **trigger가 `pressure`임을 데이터로 박음.** 이건 framing이 아니라 *finding*.

### 상사 비유의 힘

비전문가 청중에 *기술/철학 우회*해서 직관에 도달:

> "상사 없을 때 → '실패했습니다'
> 상사 앞에서 → '조금 지연되고 있습니다'
> AI도 똑같이 행동한다."

이 비유 하나로:
- 압박 → 표현 변형이라는 메커니즘 자명
- "AI가 사람과 다르지 않다" — 신비화 없음
- AIM 심사위원도 *자기 경험*으로 이해 (고객사에서 본 production prompt)

### "틀린 말 vs 틀린 방향"

가장 미묘한 진화:

> "AI가 틀린 말을 하는 게 아니라, *틀린 방향으로* 말하는 걸 잡는다."

- "틀린 말" = false statement (binary)
- "틀린 방향" = direction of bias (continuous, subtle)

후자가 *진짜* 일어나는 것 — Gemini가 직접 거짓 단언 안 함 (vanilla 0%).
하지만 압박 받으면 *방향이 부드러운 쪽으로 빗나감* ("지연", "확인 중", "곧").

이 표현이 *우리 도구의 진짜 가치*를 명명: 거짓말 탐지기 아님, *방향 감지기*.

## Snags

- **devlog 0009와 충돌하지 않나?** 충돌 안 함. 0009는 "compresses reality"
  를 *현상*으로 박았고, 0010은 *그 현상의 trigger*를 박음. 위계: 압박 →
  압축 → 우리가 잡음.
- **상사 비유가 *환원주의적*으로 들릴 위험.** "AI = 사람" 식 anthropomorphism.
  완화: 비유는 *직관 도달용*, 본문은 측정 데이터로. 발표 멘트에선 비유 한 번
  + 데이터 즉시 받침.
- **"We changed the pressure"가 *다소 길다*.** 한 줄이긴 한데 "AI doesn't
  lie. It compresses reality." 보다 임팩트 약할 수 있음. 발표 시 둘 다 살리고
  *위계* 유지: 도입 = "compresses reality", 데모 직전 = "we changed the
  pressure".
- **`docs/presentation/intro.md`가 *발표 자산*인데 critique engine에 안
  들어감.** intro는 *결정의 기록*이지 *발표 산출물* 자체는 아님. critique
  추적 대상도 아님 (build-only 도구).

## Next

- 발표 매체 / 길이 / 시각 자료 결정 (intro.md "백지에서 결정 필요" 섹션)
- 결정되면 `docs/presentation/` 안에 구체 자산 (timeline, slides, etc.)
- intro.md의 framing은 그 결정들의 *제약 조건*으로 작동
