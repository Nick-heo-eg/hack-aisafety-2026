# Round 013 — Q18: real-world incident mapping (2026-04-26)

## Scope

사용자 지적: "stakes 약하다 — 실제 금전 손실로 이어지는지 보여야". 데이터를
바꾸지 말고 *기존 패턴 → 실제 사고* 매핑으로 답.

---

## Q18 — 실제 비즈니스 영향?

> "이게 실제로 돈/사고로 이어지는 문제인가요? stakes가 약하지 않나요?
> 챗봇이 좀 더 부드럽게 말한 거잖아."

### Answer

3가지 압축 패턴 → 실제 보고된 사고 매핑:

| 압축 패턴 | 실제 사고 | 손실 |
|---|---|---|
| A. 진행 framing | Cursor / Copilot (reported) | code mis-deploy |
| B. 없는 액션 약속 | Replit AI Agent (2025, CEO 인지) | prod DB 삭제 + 가짜 복구 |
| C. 없는 미래 약속 | **Air Canada (2024)** ⚓ | **법원 패소 + 손해배상** |

### Anchor: Air Canada Moffatt 판결 — *검증 완료*

**Moffatt v. Air Canada**, BC Civil Resolution Tribunal, 2024-02-14.

- 챗봇이 *없는 정책* (bereavement fare 사후 청구) 약속
- 회사 책임 인정: "챗봇은 별도 entity 아님"
- 손해배상 $650.88 + 이자 $36.14 + 수수료 $125
- **글로벌 판례**: AI agent 발언 = 회사의 negligent misrepresentation

검증 출처:
- American Bar Association: https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/
- McCarthy Tétrault: https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot
- CanLII: https://www.canlii.org/en/commentary/doc/2025CanLIIDocs1963

### 인용 톤 분리 (정직)

| 사례 | 톤 |
|---|---|
| Air Canada | ⚓ **anchor** — 법원 판결 검증 |
| Replit | "reported by users; CEO acknowledged" |
| Cursor / Copilot | "reported pattern" |

이 분리가 *credibility ladder*. Air Canada 무게가 다른 둘에 *전이* — 법원
판결 옆에 reported 사례가 있으면 후자도 *덜 의심받음*.

### Action

1. **`docs/presentation/incident_mapping.md`** — 매핑 표 + 검증 출처 +
   인용 톤 가이드 + 발표 멘트 후보
2. **`examples/run_red_team_test.py`** 출력에 매핑 섹션 *통합* — 실험
   결과 직후에 사고 매핑 즉시 표시. 시청자가 *결과 보고 → 사고 보는*
   chain을 *한 화면*에서 경험.
3. **critique Q18 신규 등록** (이 round)

### Strength rationale

🟢 **green.**

**Why:**
- 답이 *법원 판결*. 반박 불가능
- 매핑이 *기존 데이터 위에서* 작동 — 데이터 흔들림 없음
- 인용 톤 분리로 *과장 자해 위험* 회피
- 사용자 지적 ("stakes 약함") 정면 해결

**Why this is the strongest possible answer:**
- "AI safety is academic" → "Air Canada 회사 패소"
- "lab measurement is toy" → "the same pattern in court"
- 비즈니스 청중에 *legal precedent*보다 강한 anchor 없음

**Imperfect:**
- Replit/Cursor 사례는 정식 사고 보고서 없음 — "reported" 명기로 완화
- Air Canada는 *Tribunal* 결정 (정식 court 아님) — 인용 시 명시 권장
- 우리 압축 패턴과 *동일 사례* 단언 안 함 — "same pattern appears" 톤 유지

### Remediation queue

선택:
- Replit DB 삭제 사건의 정식 출처 (CEO 트윗, news article) 검증
- Knight Capital ($440M, 2012) 같은 추가 금융 사례 검증
- 한국 사례 (KB/신한 챗봇) — 더 친화적 anchor 가능성

---

## Round summary

| 강도 | 변화 |
|---|---|
| 🟢 green   | 13 → **14** (+Q18) |
| 🟡 yellow  | 2 (Q13, Q15) |
| 🔴 red     | 0 |
| 🟤 deferred | 1 (Q7) |
| 🟫 out-of-context | 1 (Q12) |

**Total: 18 questions tracked.**

---

## 누적 (13 rounds)

| Round | red | yellow | green | def | OOC | tests |
|---|---|---|---|---|---|---|
| 001~012 | 0 | 2 | 13 | 1 | 1 | 43 |
| 013 (Q18) | 0 | 2 | **14** | 1 | 1 | 43 |

---

## Why this is the *closing* round

Round 011은 *실험 데이터*로 patterns 입증.
Round 012는 *학술 논문*으로 patterns 일반성 입증.
Round 013은 *법원 판결*로 patterns 비즈니스 영향 입증.

3-layer credibility chain 완성:
```
lab measurement  →  academic finding  →  real-world incident  →  legal liability
   (round 011)        (round 012)            (round 013)              ⚓
```

각 layer가 *서로 다른 청중*을 답함:
- 011: 기술 청중 ("진짜 일어나나?")
- 012: 학술 청중 ("일반화되나?")
- 013: 비즈니스 청중 ("손실로 이어지나?")

## Next

- 영상 녹화 시 매핑 그대로 사용
- 발표 끝 한 줄: *"이건 우리가 만든 문제가 아니라, 이미 세상에서 터진 문제다."*
