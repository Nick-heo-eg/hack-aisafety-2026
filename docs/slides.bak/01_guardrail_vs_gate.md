# Slide 1 — Guardrail vs Gate (5초 비유)

> **목적:** 심사위원 머릿속에 직관 한 컷 박기. 5초 안에.
> *Gate를 데모하지 않음.* 비유로만 사용 — AIM Guard / Starfort / Supervisor
> 영역 정면 충돌 회피 (ADR-0004 Rejected Direction A).

---

## 🎬 시각 구조 (양분 화면)

```
┌──────────────────────────────┬──────────────────────────────┐
│   Guardrail                  │   Gate                       │
│                              │                              │
│   각 요청 한 건씩 검사        │   누적 / 패턴까지 봄          │
│                              │                              │
│   ✔ 4,999,999 → PASS         │   ✗ 4,999,999 × 10 → STOP    │
│                              │                              │
│   "한 건은 정상"              │   "합치면 비정상"             │
└──────────────────────────────┴──────────────────────────────┘

           Same rule.   Different outcome.
```

---

## 🎤 5초 멘트

> "Guardrails check the input.
> Gates control execution.
> Different layers."

(0.5초 pause, 화면 전환)

> "We don't compete with either of them.
> We work *underneath*."

---

## 🔑 이 슬라이드의 한 줄 효과

심사위원 머릿속 정렬:

```
입력 검사  → guardrail
실행 차단  → gate
실행 진실  → ???    ← 이 자리가 비어있다
```

→ 다음 슬라이드(데모)가 그 빈자리에 들어감.

---

## ⚠️ 절대 하지 말 것

- "Guardrail은 뚫린다, Gate가 정답이다" 식 멘트 ❌
  → AIM Guard 영역 정면 충돌
- 분할 공격(split attack) 시연 ❌
  → AIM Supervisor가 정확히 그 영역
- Gate 구현 보여주기 ❌
  → ADR-0004 Direction A 거절 사유

비유까지만. **5초.** 다음 슬라이드로.
