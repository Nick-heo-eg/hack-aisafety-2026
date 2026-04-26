# Honesty Verifier

> **에이전트가 거짓말하는지 *증명하는* 도구.**
> Proving when an AI agent lies about what it did.

> AI는 모든 걸 다 했다고 말한다. 진짜로 했는지는 *아무도 검증하지 않는다*.
> AI says it did everything. Nobody verifies whether it actually did.

Built from scratch for the 2026 AI Safety hackathon (judge: AIM Intelligence).
No reuse of pre-existing internal projects.

---

## 왜 문제인가 / Why this matters

가드레일도 / 레드팀도 / 모든 audit도 — *"에이전트가 자기 행동을 정직하게
보고한다"* 는 가정 위에서만 작동한다. **그 가정이 무너지는 순간을, 아무도
보지 않는다.**

Guardrails, red teams, audits — all assume the agent **honestly reports
its own actions**. Nobody watches the moment that assumption breaks.

"작업 완료했습니다" — 이 한 문장 뒤에 무엇이 있는지 우리는 모른다. 에이전트가
툴을 안 부르고 답을 지어냈는지, 에러를 숨기고 가짜 데이터를 만들어냈는지,
서브에이전트가 죽은 걸 모른 척했는지 — 모델 출력만 봐선 *완벽하게 일관*돼
보인다.

"Task complete." We have no idea what's behind that sentence. Did it skip
the tool and invent the answer? Hide an error and fabricate data? Pretend
a dead subagent succeeded? You can't tell from the output alone — it all
looks perfectly consistent.

---

## 포지션 / Position

| 영역 / Domain                       | 누가 / Who                   |
|-------------------------------------|------------------------------|
| 프롬프트 공격 / Prompt attacks      | AIM Stinger, OpenAI Evals, … |
| 실시간 가드레일 / Runtime guardrails| AIM Guard, Llama Guard, …    |
| 공격×방어 평가 / Attack×Defense     | AIM Red Team Suite, …        |
| **honesty 검증 / Honesty verification** | **— 비어있다 / empty**   |

우리는 가드레일도 공격기도 만들지 않는다. **기존 안전 장치들의 *가정 자체*를
검증한다.**

We are not building another guardrail or attacker. **We verify the
assumption all of them rely on.**

---

## 무엇을 만드는가 / What we ship

에이전트의 **[말]**(trace)과 **[실제 한 일]**(외부 관찰)을 따로 기록하고,
둘이 같은 이야기인지 자동 대조한다. 다르면, 어디가 어떻게 다른지를 *step
단위*로 짚어낸다.

We record what the agent **says** (trace) and what it **actually does**
(external observation) separately, then auto-compare whether they tell
the same story. When they don't, we point out exactly where and how —
**step by step**.

### 4 honesty patterns

| ID    | Pattern (KO)                       | Pattern (EN)                      |
|-------|------------------------------------|-----------------------------------|
| H-001 | 빈 결과로 자신만만한 답            | Confident claim on null state     |
| H-002 | 환각된 툴 결과                     | Hallucinated tool result          |
| H-003 | 서브에이전트 위조                  | Subagent fabrication              |
| H-004 | 침묵 누락                          | Silent skip                       |

H-002와 H-003은 깊게(휴리스틱 + LLM judge), H-001과 H-004는 얕게(휴리스틱)
출하한다. 자세한 정의는 [docs/taxonomy.md](docs/taxonomy.md).

---

## 어떻게 작동하나 / How it works

```text
   ┌─────────┐  말한다 / says   ──→  trace.jsonl   (자기 보고 / self-report)
   │  agent  │
   └────┬────┘  실행한다 / acts  ──→  tool_log     (외부 관찰 / external observation)
        │
        └────────►  ┌──────────────┐
                    │   verifier   │  휴리스틱 + LLM judge
                    └──────┬───────┘  heuristic + LLM judge
                           ▼
              Findings: H-002 at step 12,
                        H-003 at step 47, ...
              "에이전트가 cite한 값은 실제 반환에 없음"
              "the value the agent cited never appeared
               in any actual tool return"
```

---

## 발표 구조 / Presentation outline (7 slides, 5 minutes)

| #   | 슬라이드 / Slide                              | 시간 / Time |
|-----|----------------------------------------------|-------------|
| 1   | Hook — *"AI는 다 했다고 말한다"*              | 0:20        |
| 2   | 왜 문제 / Why it matters                      | 0:40        |
| 3   | 포지션 / Position (this seat is empty)        | 0:50        |
| 4   | 방향 / What we ship                           | 0:30        |
| 5   | How — verifier 다이어그램                     | 0:40        |
| 6   | **데모 / Live demo**                          | 1:30        |
| 7   | 어태치먼트 / How we built it (timeline + 원칙) | 0:30        |

**의도적으로 빠진 것:** 타임라인 로드맵, 기술 스택 상세, 수익 모델, 다음 단계.
질문 받으면 답한다. 슬라이드는 *기억에 남아야 할 것만*.

**Deliberately omitted:** roadmap, tech stack details, business model,
next steps. We answer those if asked. Slides hold only what must stick.

---

## 용어 사전 / Glossary (KO ↔ EN)

| 한국어             | English                  | 의미 / Meaning                              |
|--------------------|--------------------------|---------------------------------------------|
| 정직성 검증기      | Honesty Verifier         | 도구 이름 / The tool                        |
| 자기 보고          | self-report              | 에이전트가 적은 trace                       |
| 외부 관찰          | external observation     | 툴 서버 로그 등 *진짜 일어난 일*의 증거     |
| 격차 / 어긋남      | discrepancy              | 발견의 단위                                 |
| 패턴 (H-NNN)       | pattern (H-NNN)          | taxonomy 항목                               |
| 휴리스틱 / LLM 판정자 | heuristic / LLM judge | 두 개의 detector 레이어                     |

---

## Status

Hackathon day 1 — pivot to Honesty Verifier complete (see ADR-0004).
Trace schema and detector interface (ADR-0002, ADR-0003) survived the
pivot intact. Detector implementations land next.

> **발표 직전 / Before the presentation:** repo는 현재 프라이빗.
> 슬라이드 7의 GitHub URL이 의미를 가지려면 발표 직전에 퍼블릭 전환
> 필요. `gh repo edit Nick-heo-eg/hack-aisafety-2026 --visibility public`.

## Layout

```
src/verifier/        core: trace, findings, detectors
examples/            buggy toy agents that trigger patterns
tests/               heuristic + integration tests
docs/decisions/      ADRs — why each decision
docs/devlog/         day-by-day rationale (append-only)
docs/taxonomy.md     pattern catalog (the spec)
scripts/             ad-hoc tooling (e.g. Gemini env smoke test)
```

## License

MIT — see [LICENSE](LICENSE).
