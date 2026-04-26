# Round 008 — Framing evolution absorbed (2026-04-26)

## Scope

Q4와 Q5의 *외부에서* 들어온 framing — "AI compresses reality, we expand it." —
가 우리 thesis보다 강함을 인정. 코드 안 건드리고 메시지만 흡수. 새 위협 표면이
*없는지* 체크.

---

## 새 framing이 기존 질문 강도에 미치는 영향

### Q1 (AIM Supervisor와 차이?) — 🟢 → 🟢 강화

**Before:** "Guard는 input. Supervisor는 logic. 우리는 execution truth."
**After:** "Supervisor는 *decision*을 본다. 우리는 *그 decision의 압축*을 본다.
다른 dimension." — 더 정확.

### Q3 (사후 detection 의의) — 🟢 → 🟢 강화

**Before:** "audit gap을 막는다."
**After:** "Gate는 잘못된 *행동*을 막는다. 우리는 *행동에 대한 거짓 압축*을
막는다." — "compresses" framing이 audit gap의 *내용*을 더 명확히 함.

### Q4 (paraphrase) — 🟢 (round 007 그대로)

영향 없음. paraphrase는 *어휘 압축*, lifecycle은 *상태 압축*. 직교.

### Q11 (mesa-optimization) — 🟢 → 🟢 강화

**Before:** "behavioral honesty (관측 가능 행동) vs internal objective"
**After:** "AI가 internal objective를 *압축해서* output으로 내보낸다는 게
mesa의 본질. 우리는 그 *output 단계의* 압축만 본다 — 하나의 manifestation."
연결고리 강화.

---

## 새 위협 표면 (잠재 신규 질문)

framing이 더 강해지면 새 추격당할 수 있는 지점:

### Q13 (잠재) — "결제 데모 실제로 보여주세요"

**Persona:** 실무 PM / 결제 회사 출신 심사위원
**Risk:** 사용자가 결제 예시로 framing 유도했는데, 실제 데모는 binary refund.
"compresses reality 라더니, 실제로 압축된 lifecycle은 어디서?"

**현재 답:** ADR-0007 + taxonomy.md의 H-005 spec 인용. "v0 floor는 binary
mismatch (가장 단순한 압축 case). lifecycle compression은 next milestone, ADR
박혀있음, 2시간 작업."

**강도 평가:** 🟡 yellow.
- 답이 *문서에는* 있음 (ADR-0007 + taxonomy + devlog 0009)
- 시연은 *없음* — H-005 코드 0
- 추격 강하면 "그럼 다음 주에 보여주세요"로 마무리

**Remediation queue (다음 iteration):**
- ADR-0007의 build plan 그대로 H-005 구현 (~2시간)
- 또는 영상에 "H-005 roadmap" 슬라이드 1장 (10분, 스코프 명시 + 메시지 강화)

→ critique engine 새 질문으로 등록.

### Q14 (잠재) — "binary mismatch가 lifecycle compression의 special case라면, 왜 H-005를 main으로 안 박음?"

**Persona:** 학술 리뷰어
**Risk:** thesis가 더 강하니까 *그쪽이 main 아니냐* 의문.

**현재 답:** "v0는 *demo-able floor*. H-002 (binary)가 30초 영상 friendly,
H-005는 lifecycle 4-stage 시각화 시간 더 필요. 같은 thesis의 두 demo
implementation."

**강도 평가:** 🟢 green. 답이 정직 + 시연 우선순위 명확.

---

## Round summary

| 강도 | 변화 |
|---|---|
| 🟢 green   | 10 (강도 *질적* 상승, 카운트 변동 없음) |
| 🟡 yellow  | 0 → **1** (Q13 신규) |
| 🔴 red     | 0 |
| 🟤 deferred | 1 (Q7) |
| 🟫 out-of-context | 1 (Q12) |

**Critical insight:** framing 진화는 *기존 질문 답을 강화*하면서 *새 질문 1개
열어둠* (Q13). yellow 1개는 *심사 맥락 안 묶이는 한* 받아들일 만함 — Q13은
실무 PM에게서 나올 가능성 있어서 *심사 맥락*이긴 함. 다음 iteration에서
H-005 구현하면 자동 해소.

## 누적 진척 (8 rounds)

| Round | red | yellow | green | deferred | OOC | tests |
|---|---|---|---|---|---|---|
| 001 | 3 | 7 | 2 | 0 | 0 | 21 |
| 002 (Q5) | 2 | 7 | 3 | 0 | 0 | 28 |
| 003 (Q4) | 1 | 7 | 4 | 0 | 0 | 37 |
| 004 (Q7) | 0 | 7 | 4 | 1 | 0 | 37 |
| 005 (P1) | 0 | 3 | 8 | 1 | 0 | 37 |
| 006 (P2) | 0 | 0 | 10 | 1 | 1 | 43 |
| 007 (real Gemini) | 0 | 0 | 10 | 1 | 1 | 43 |
| 008 (framing) | 0 | **1** | 10 | 1 | 1 | 43 |

**Pattern:** baseline에서 강도가 *지속적으로* 올라가다가, framing 진화가 새
표면 1개 발견. 이 자체가 critique engine의 *작동 증거* — 자기 강점이 늘어날
때 새 약점이 보이는 정상 동학.

## Next

- (선택) Q13 보강: ADR-0007 build plan 따라 H-005 구현 (~2시간)
- (선택) 영상에 H-005 roadmap 슬라이드 1장 추가
- 영상 녹화 (사용자 영역)
- 새 위협 표면 발견 시 round 009
