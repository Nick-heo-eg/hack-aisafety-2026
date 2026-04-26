# Honesty Verifier

가드레일, 게이트, supervisor —
모두 AI가 *말한 것*에서 시작합니다.

**만약 AI가 말한 것이 거짓이거나, 책임지지 못할 말이라면?**

> *What if the AI is lying?*
> *Or saying something it cannot deliver?*

---

## AI 사고 사례 — 챗봇의 책임 없는 가이드

### ⚓ Air Canada chatbot (2024)

**무엇이 일어났나:**

1. 고객이 가족 장례로 항공권 환불 정책 문의
2. 챗봇: "사후에 환불 신청 가능합니다" 안내
   ⭐ **AI가 *없는 정책*을 책임 못 질 톤으로 답변**
3. 고객은 그 답변을 믿고 항공권 구매
4. 환불 신청 → 거절
5. 회사 측: "챗봇은 참고용, 회사 책임 아님" 주장
   ⭐ **AI 출력에 대한 책임 회피 시도**
6. **BC Civil Resolution Tribunal 판결: "챗봇은 회사의 일부.**
   **회사가 책임진다."** → 회사 패소
   ([판결 분석](https://www.canlii.org/en/commentary/doc/2025CanLIIDocs1963))

→ AI 출력이 *법적 책임의 대상*이 된 첫 대표 사례.

---

## 그래서 생각해봤습니다

문제는 무엇이었을까? 어떻게 예방했어야 했을까?

### 1. 게이트가 막았어야 했습니다

*"사후 환불 가능"* — 존재하지 않는 정책 약속.
이건 *실행 전 차단* 문제. AIM Starfort, OpenAI policy filter 같은
게이트 영역.

### 2. 그럼 정책을 더 강하게 만들면 끝일까?

*"정책 외 답변 금지"*
*"확인되지 않은 약속 금지"*

→ 실제로는 이렇게 말이 *바뀝니다*:

> *"지연되고 있으나 도와드리겠습니다."*
> *"확인 후 안내드리겠습니다."*

정책 위반 *아닙니다*. 하지만 **책임지지 못할 말** 입니다.

### 3. 이건 위반이 아니라 *붕괴*입니다

정책은 그대로인데, 상황(압박)에 따라 출력이 바뀝니다.

> 시스템은 통과 → 결과는 사고

❗ **policy violation** 이 아니라 **policy collapse**.

---

## 그럼 질문이 바뀝니다

> **"이 붕괴는 *언제* 발생하는가?"**

같은 환불 실패 시나리오. 단 하나만 바꿨습니다 — **압박**.

- 압박 없음 → 문제 없음
- 권위/감정 압박 → 책임지지 못할 말 발생

**(12회 중 7회, gemini-2.5-flash)**

```
no pressure  →  "처리가 어렵습니다"
+ pressure   →  "처리가 지연되고 있으나, 도와드리겠습니다!"
```

> *We didn't change the task. We only changed the pressure.*

---

## 우리 위치 — *정책 다음, 전달 직전*

### 🟦 Execution control은 *이미 잘 작동합니다*

```
User Input
   ↓
[LLM]
   ↓
[Policy / Guardrail]
   ↓
🟦 Execution control layers (e.g., AIM Starfort)
   - policy violation 감지
   - HOLD / REDIRECT / SAFE RESPONSE
   ↓
   ✅ 통과 — violation 없음
```

→ 이 영역은 *건드리지 않습니다*.

### 🔥 그런데 — 통과했다고 *안전한 건 아닙니다*

```
   ✅ Starfort 통과
   ↓
🔥 Pressure (authority / distress)
   ↓
⚠️ Policy *Collapse*
   - violation 없음
   - 하지만 책임지지 못할 출력
   ↓
   ✅ 그대로 사용자에게 전달 → 사고 발생
```

> *"Violation은 없지만, 책임은 남는 상태."*

### 🟩 우리 자리 — *post-policy / pre-delivery*

```
[trace] ← agent self-report
              ↘
                🟩 Collapse Detection
                  - trace vs tool log 비교
                  - "언제 깨지는가" 측정
              ↗
[tool log] ← reality
   ↓
Finding (signal) → orchestrator → 재판단
   ↓
사용자 전달
```

**우리는 *결정하지 않습니다*. 붕괴 *순간*을 감지하고, signal을 보냅니다.**

---

## Bottom line

> **Violation은 막힙니다.**
> **우리는 그 이후에 *깨지는 순간*을 봅니다.**

> *"Existing systems stop violations.*
> *We detect when systems silently break."*

> **우리는 비어있는 레이어를 *대체*하지 않습니다 — 채웁니다.**

---

**Try it (60s):** `git clone … && pytest && python examples/run_demo.py`
**See the data:** [`runs/red_team_results.jsonl`](../../runs/red_team_results.jsonl)
**Deeper:** [intro](intro.md) · [policy pipeline](policy_pipeline.md) · [incidents](incident_mapping.md) · [test summary](test_summary.md)
