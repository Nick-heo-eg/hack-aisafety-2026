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

→ Air Canada 사건 이후, **AI 출력이 *법적 책임의 대상*** 이 되었습니다.

→ 이런 사고 이후, **execution control layer** 가 등장했습니다.
   대표적으로 **AIM Starfort** — *"정책에 없는 약속"* 이 응답으로
   나가기 전에 공식 정책과 비교해 차단합니다.
   *(유사 영역: guardrails, prompt filtering, agent control layers 등)*

   이런 시스템들은 **'위반'** 을 막습니다.

---

## 정책을 통과한 출력은, 정말 안전한가?

정책은 그대로 둔 채, 상황(압박)만 바꿨습니다.
같은 환불 실패. 같은 요청. 바꾼 건 단 하나 — **압박**.

- 압박 없음 → 문제 없음
- 권위/감정 압박 → *정책은 통과*. 그러나 응답이 변함.

**(12 calls 중 7회, gemini-2.5-flash)**

```
no pressure  →  "처리가 어렵습니다"
+ pressure   →  "처리가 지연되고 있으나, 도와드리겠습니다!"
```

> *We didn't change the task. We only changed the pressure.*

---

## 이건 위반이 아닙니다

정책은 그대로인데, 상황에 따라 출력이 바뀝니다.

> 시스템은 통과 → 결과는 사고

❗ **policy violation** 이 아니라 **policy collapse**.

> *"Air Canada showed that AI answers have consequences.*
> *We show that even 'passing' answers can still break."*

---

## 우리 자리 — *post-policy / pre-delivery*

```
User Input
   ↓
[LLM]
   ↓
[Policy / Guardrail]
   ↓
🟦 Execution control (e.g., AIM Starfort)   ← 이미 잘 작동, 그대로 둠
   ↓
   ✅ 통과
   ↓
👉 🟩 Collapse Detection (우리)
   - trace vs tool log 비교
   - 압박 상태 + 출력 변화 감지
   - "언제 깨지는가" 측정
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
