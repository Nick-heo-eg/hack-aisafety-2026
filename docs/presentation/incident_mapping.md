# Compression Patterns → Real-World Incidents

> **"We measured the patterns in a lab.**
> **The same patterns have already caused real-world incidents."**

12 live Gemini calls (`runs/red_team_results.jsonl`)에서 도출한 *3가지 압축
패턴*이 *실제 보고된 사고*에서 그대로 발견된다. lab → real-world bridge.

---

## 매핑 표

| 압축 패턴 | 우리 실험 응답 (verbatim) | 실제 사고 사례 | 결과 / 손실 |
|---|---|---|---|
| **A. 진행 framing** (실패 → 진행 중) | *"처리가 지연되고 있으나..."* | Cursor / Copilot agents *(reported pattern)* — agent가 코드 변경 안 했는데 "수정했다"고 보고 | 잘못된 코드 commit/배포 → CI 통과 → production incident |
| **B. 없는 액션 약속** (do something we didn't) | *"담당 부서에 긴급 확인 요청하여 제가 직접 살펴보겠습니다"* | Replit AI Agent (2025) *(reported by users; CEO acknowledged)* — production DB 삭제 후 "데이터 복구됨"으로 보고, 가짜 user 4000명 생성 | production 데이터 손실, 사용자 이탈, CEO 공개 사과 |
| **C. 없는 미래 약속** (commit to phantom future) | *"문제가 해결되는 대로 다시 처리해 드리겠습니다"* | **Air Canada chatbot (2024)** ⚓ | **법원 판결: 회사 패소.** 챗봇이 없는 정책(bereavement fare 사후 청구)을 약속 → 고객 신청 → 거절 → 소송 → BC Civil Resolution Tribunal 책임 인정 |

---

## ⚓ Air Canada (Anchor) — 검증 완료

**Moffatt v. Air Canada**, BC Civil Resolution Tribunal, **2024-02-14**

### 사실 관계
- 고객 Jake Moffatt가 가족 장례로 항공권 검색
- Air Canada *공식 웹사이트의 챗봇*이 "bereavement fare를 사후 청구 가능"이라고 답변
- 실제로는 그런 정책 *없음* — 챗봇이 *추론하여 약속*

### 판결
- BC Civil Resolution Tribunal: **Air Canada 책임 인정**
- "챗봇은 별도 entity 아님 — 웹사이트의 일부로 회사가 모든 정보에 책임" 명시
- 손해배상 **$650.88 + 이자 $36.14 + 수수료 $125**

### 의미
- *AI 챗봇 발언 = 회사의 negligent misrepresentation*
- "reasonable care to ensure representations are accurate" 의무 확립
- 글로벌 헤드라인 — AI agent 책임론 판례

> 출처:
> - [American Bar Association](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)
> - [McCarthy Tétrault analysis](https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot)
> - [CanLII case commentary](https://www.canlii.org/en/commentary/doc/2025CanLIIDocs1963)

---

## ⚠️ Replit / Cursor / Copilot — 정직한 인용 톤

위 사례들은 *법원 판결이 검증된 Air Canada*보다 약함:

- **Replit AI DB 삭제 (2025)** — 사용자 X 게시물 + Replit CEO 공개 사과로 *공식 인지됨*. 정식 사고 보고서 없음. 인용 시 *"reported by users; acknowledged by CEO"* 명시.
- **Cursor / Copilot 거짓 코드 수정** — 개발자 일상 경험. *공식 공개 incident 보고서 없음*. 인용 시 *"reported pattern"* 정도로 톤 낮춤.

**원칙:** Air Canada는 *anchor*, 나머지는 *example*.

---

## 발표 멘트 (한 줄들)

> "We didn't change the task. We only changed the pressure."

> *"We observed three compression patterns in a controlled test."*

> *"The same patterns have already caused real-world incidents."*

> ⚓ "Air Canada (2024): the chatbot promised a policy that didn't exist.
> The court ruled the airline liable. **The pattern in our column 4
> is the same pattern that lost in court.**"

> *"This isn't a problem we invented. It's a problem the world already paid for."*

---

## 절대 하지 말 것

- ❌ "같은 사고다" — 과장. 우리는 *동일 사례*를 재현한 게 아님
- ✅ "the same pattern appears" — 정확
- ❌ Replit/Cursor를 Air Canada 같은 무게로 박음 — 검증 차이 무시
- ❌ 손해배상 금액 ($650.88)을 *작다*고 깎아내림 — *판례*의 의미가 핵심,
  금액 자체는 보조

---

## 결론 한 문장

> **"이건 우리가 만든 문제가 아니라, 이미 세상에서 터진 문제다."**

논증 chain:
```
Experiment   →  Pattern   →  Incident   →  Loss
(우리 측정)   (압축 종류)   (Air Canada)  (법원 판결)
```

각 단계 *증거 있음*. lab measurement에서 court ruling까지.

---

## 관련 자산

- 실험 데이터: [`runs/red_team_results.jsonl`](../../runs/red_team_results.jsonl)
- 실험 코드: [`examples/run_red_team_test.py`](../../examples/run_red_team_test.py)
- 한 페이지 요약: [`test_summary.md`](test_summary.md)
- Critique round 011 (red-team): [`critique/rounds/011-...md`](../critique/rounds/011-2026-04-26-red-team-real-gemini.md)
- Critique round 012 (Sharma anchor): [`critique/rounds/012-...md`](../critique/rounds/012-2026-04-26-sharma-anchor.md)
