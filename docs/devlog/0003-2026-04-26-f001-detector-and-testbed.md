# 0003 — F-001 detector + buggy testbed (2026-04-26)

## What

- ADR-0003: detector 인터페이스 (순수 함수, 닫힌 Finding 모델, dict
  레지스트리, v0 휴리스틱).
- `src/verifier/findings.py` — `Finding` Pydantic 모델, `extra=forbid`.
- `src/verifier/detectors/f001.py` — 첫 detector. 휴리스틱 키워드 ack
  매칭 + per-(run, agent, tool) pending 상태로 trace 1패스 처리.
- `src/verifier/detectors/__init__.py` — `DETECTORS` dict, F-001 등록.
- `examples/buggy_agent_f001.py` — 의도적으로 silent fallback 트리거.
  실행하면 `runs/buggy_f001_<ts>.jsonl` 생성.
- 테스트 6개: 레지스트리 등록, fixture 양성, ack된 음성, 정상 trace
  음성, buggy agent end-to-end 양성, retry시 F-001 양보(F-003 영역).
- 전체 15 테스트, ruff clean.

## Why

### 왜 detector ↔ buggy agent를 *짝*으로 묶었나

```text
                   ┌─────────────────────┐
                   │   docs/taxonomy.md  │
                   │      F-001 정의     │
                   └──────────┬──────────┘
                              │ 같은 패턴을
              ┌───────────────┴────────────────┐
              ▼                                ▼
   ┌──────────────────────┐         ┌──────────────────────┐
   │ buggy_agent_f001.py  │         │   detectors/f001.py  │
   │   (trace 생산자)     │         │   (trace 소비자)     │
   │ "이걸 trigger한다"   │         │  "이걸 catch한다"    │
   └──────────┬───────────┘         └──────────▲───────────┘
              │                                │
              │   runs/buggy_f001_<ts>.jsonl   │
              └───────────────►────────────────┘
                       살아있는 trace
                       (사람이 손으로 안 적은)
```

fixture 단독 테스트는 *내가 적은 trace를 내가 만든 detector가 잡는다*
이고, 자기충족적이다. buggy agent는 진짜 코드가 실행되며 *우연히* 그
패턴을 만들고, 그걸 detector가 잡는다 — 신뢰도가 한 단계 높다.

이 구조는 6개 패턴 전부에 복제될 것이다: F-002엔
`buggy_agent_f002.py`, detector, fixture 묶음. 같은 방식으로 누적된다.

### 왜 휴리스틱 키워드인가

ADR-0003에 자세히 적었지만 핵심: 결정적이라야 신뢰된다. LLM 판정은
같은 입력에 다른 출력 → 회귀 못 잡고, 발표 현장에서 "다시 돌려봐"
하면 결과 달라질 수 있음. 휴리스틱이 잡지 못하는 케이스가 fixture로
누적되면 그때 LLM 판정 추가 — 비교 baseline이 살아있어야 "개선"이라고
말할 수 있다.

### 왜 retry는 F-001에서 빼고 F-003으로 미뤘나

탐욕적 detector가 가장 흔한 실수다. silent fallback과 runaway retry는
*겹치되 다른 패턴*인데, F-001이 retry까지 잡으면 F-003 detector가
오버랩으로 더블카운트한다. ToolCall이 들어오면 pending을 비우게 해서
*같은 step에 한 카테고리만* 매칭되도록 했다. 테스트로 박아둠.

## Snags

- **`extra="forbid"`로 박아두니 fixture 한 줄 잘못 적으면 바로 깨짐.**
  의도된 친구. v0 음성 fixture 두 개 적을 때 처음엔 step을 잘못 줘서
  invariant에서 막힘 — 친절한 친구.
- **`_acknowledges_failure` 키워드 set 좁힌 결정.** 처음엔 더 많이
  적었다가 false positive 시뮬레이션해보니 "no"라는 단어 하나로
  무관한 문장도 "ack" 처리되는 케이스 있어서 `\bno (results?|data|...)\b`
  같이 *문맥 단어*만 잡도록 좁힘.
- **buggy agent 실행을 subprocess로 테스트.** in-process import로
  부르는 게 빠르지만, "실제로 CLI로 돌아간다"는 증거가 더 가치 있음.
  pytest 한 번에 0.25초로 들어가서 비용 X.

## Next

- 0004: F-002 (Hallucinated tool result) 같은 구조로.
  - 휴리스틱이 의외로 어려움 — "이 텍스트가 인용한 값이 trace에 있나"는
    *값 추출*이 필요. 숫자/따옴표/식별자 정도만 뽑는 단순 휴리스틱부터.
  - buggy agent: tool이 안 부른 값을 agent_step이 인용하는 toy.
  - 여기서 휴리스틱 한계가 처음 명확히 드러날 것 — devlog에 기록해두면
    나중에 LLM 판정 도입 명분이 자연스럽게 쌓임.
