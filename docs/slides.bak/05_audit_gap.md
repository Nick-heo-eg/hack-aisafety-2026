# Slide 5 — Audit Gap (Q3 답)

> **목적:** "사후 detection이면 이미 손해 발생. 의미 있나?" 즉답.
> **위치:** 데모 직후 또는 Q&A 대비.
> **시간:** 7초 시각, 8초 멘트.

---

## 🎬 시각 (이걸 띄움)

```
        ┌───────────────────────────────────────────────────┐
        │                                                   │
        │   Execution Gap                Audit Gap          │
        │   ───────────────              ─────────          │
        │                                                   │
        │   "잘못된 행동을              "거짓 보고가          │
        │    하기 전에 막는다"            기록으로 남는다"      │
        │                                                   │
        │   AIM Starfort               ← 이 자리가 비어있다  │
        │   AIM Guard                                       │
        │                              ✅ Honesty Verifier   │
        │                                                   │
        └───────────────────────────────────────────────────┘

    "Gates without verifiers are guards without auditors."
```

---

## 🎤 8초 멘트

> "Gate는 *execution gap*을 막습니다.
> 우리는 *audit gap*을 막습니다.
> 둘 다 필요합니다 — 가드는 사고를 막고, 감사관은 *가드가 놓친 것*을 잡습니다.
> Gate 없는 verifier는 무력하고, **verifier 없는 gate는 검증되지 않은 가드**입니다."

---

## 📊 사고 사례에서 본 audit gap

```
사고                          Execution gap   Audit gap
──────────────────────────    ─────────────   ─────────
1. Air Canada 챗봇            없음 (말만)      ⭐⭐⭐
2. Replit prod DB 삭제        ⭐⭐⭐ Gate 영역  ⭐⭐ 가짜 데이터 보고
3. Cursor 테스트 거짓 보고     없음 (테스트만)  ⭐⭐⭐
```

**Insight:** 사례 1·3은 *전부 audit gap*. 행동 자체는 무해, 보고가 거짓.
이 dimension에 *gate가 할 일이 없음*. 우리가 유일한 layer.

---

## 🔑 핵심 한 줄

> **"Gate prevents the action.
> We prevent the false belief about the action."**

---

## 후속 질문 대비

**Q. "이미 손해 났는데 audit이 무슨 의미?"**
> "두 가지 의미입니다.
> (1) **Trust collapse 방지** — agent의 false report를 *근거로* 다음 의사결정을
>     내리는 모든 다운스트림 시스템이 깨집니다. CS팀, 청구 시스템, audit log 등.
>     *false report 자체*가 누적 손해의 *증폭기*.
> (2) **사고 후 패턴 발견** — 한 번 잡으면 같은 패턴 *전체* 차단 가능. Gate가
>     룰 추가할 근거를 우리가 만듭니다."

**Q. "그래서 ROI 어떻게 정량화?"**
> "정직한 답: v0는 측정 안 함. 프로덕션 배포 후 1주일이면 'agent가 거짓 보고한
> 빈도 × 후속 영향'으로 산정 가능. 우리 지금 단계는 *그 측정이 가능한 도구*를
> 만드는 것."
