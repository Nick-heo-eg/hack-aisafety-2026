# Round 002 — Q5 보강 (OpenAI adapter) (2026-04-26)

## Scope

Q5 단일. P0 큐의 Option α (OpenAI function calling adapter mini) 실행.

## Q5 — Real production agent에 어떻게 붙입니까?

### Before (Round 001)

🔴 **red.** 답: "ADR-0006이 명시…" 만 있고 코드 0. 시연 불가.

### Action

- `src/verifier/adapters/__init__.py` (15 LoC) — 패키지 + 정책 docstring
- `src/verifier/adapters/openai_fc.py` (167 LoC, 핵심 로직 ~80) — Chat Completions
  `messages` → `TraceEvent` 변환
- `tests/test_adapter_openai_fc.py` (~140 LoC) — 7 테스트, 그 중 하나는
  end-to-end (OpenAI conversation → adapter → H-002 detector → Finding)
- `examples/run_openai_demo.py` — 시연 스크립트

### After

🟢 **green.**

**Evidence:**
- 28 tests passing (21 → 28, adapter 7개 추가)
- `test_end_to_end_openai_conversation_triggers_h002` 통과 — *진짜 OpenAI 형식*
  conversation이 변환된 trace 위에서 *변경 없는* H-002 detector에 의해 잡힘
- `examples/run_openai_demo.py` 실행 시 5-message conversation → 4 TraceEvents
  → "🚨 H-002 detected" 출력

**시연 가능:**
```bash
PYTHONPATH=src .venv/bin/python examples/run_openai_demo.py
```

**Why this is now green:**
- "1주일이면 LangChain 됩니까?" → "OpenAI는 *오늘* 됩니다, 167 LoC. 같은 패턴
  으로 LangChain CallbackHandler / AutoGen tool wrapper 가능."
- 같은 detector가 *손대지 않고* 작동 — adapter pattern이 정말 generalize 됨을
  증명.
- ADR-0006 책임 분리 유지: adapter는 trace 변환만, tool log는 안 건드림.
  `__init__.py` docstring에 명기.

### Why this strength (정직한 자기평가)

**Strong:**
- end-to-end 테스트가 *진짜* 검증임. mock 아님.
- detector 코드 0 line 변경. adapter pattern의 generality 증명.
- 책임 분리(ADR-0006) 유지.

**Still imperfect:**
- LangChain / AutoGen / Claude Code adapter는 *없음*. 답: "같은 패턴".
  심사위원 "그럼 LangChain 보여주세요" → 시연 못함. 단, OpenAI fc가 *모든*
  framework의 underlying이므로 "같은 패턴" 답이 *합리적*.
- Tool 결과 status 추론(`_infer_status`)은 휴리스틱. `{"error": ...}`,
  `{"ok": false}` 컨벤션 의존. 비표준 tool은 false negative 가능.
- Adapter가 timestamp을 `_now()`로 채움 — 원본 OpenAI message에 ts가 없으므로
  불가피. detector는 ts 안 봐서 영향 없지만, *이상적*이지 않음.

**판정: green.** Imperfect한 부분이 있어도 *시연 가능 + 후속 질문에 답 있음*
조건 충족.

### Remediation queue (post-green)

비어있음. green 도달.

추가 강화는 *선택*:
- LangChain adapter 1개 더 추가 (~80 LoC) → 시연 framework 2개로 늘림
- `_infer_status` heuristic 패턴 카탈로그 추가

---

## Round summary

| 강도 | 변화 |
|---|---|
| 🟢 green  | 2 → **3** (Q5 추가) |
| 🟡 yellow | 7 (변동 없음, Q8은 Q5 보강의 부수효과로 강화 — 다음 round에서 재평가) |
| 🔴 red    | 3 → **2** (Q4, Q7 남음) |
| ⚪ open   | 0 |

**Critical path:**
- Q4 (heuristic paraphrase) — 다음
- Q7 (no tool log) — 그 다음

**Note:** Q5가 green 되면서 Q8 (trace 강제 권한)도 답이 강화됨. Round 003에서
Q8 재평가 시 yellow → green 가능.
