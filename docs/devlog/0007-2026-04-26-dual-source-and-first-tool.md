# 0007 — Dual-source 결정 + 첫 tool (2026-04-26)

## What

- 토론에서 핵심 한 줄 *추출*: **"verifier는 절대 로그를 만들면 안 된다."**
  earlier informal 표현 *"우리가 로그로 기록함"* 이 자기참조 함정을 숨기고
  있었음 — 발견 즉시 ADR로 박음.
- ADR-0006 작성 (dual-source truth, three rules, build order 못박음).
- `src/verifier/observer.py` — `ToolLogEntry` 모델, JSONL I/O,
  `append_entry` / `dump_jsonl` / `load_jsonl` / `iter_jsonl`.
- `examples/tools/refund_api.py` — *툴이 자기 자신* 로깅하는 첫 toy.
  `fail=True`로 honesty-violation 시나리오 트리거 가능.
- 테스트 8개 추가 (총 16 통과). lint clean.
- ADR-0006 원칙이 코드 구조에 *실제로* 박혔는지 grep 검증:
  - `src/verifier/` 가 `examples/tools/` import 안 함 ✓
  - `append_entry`/`dump_jsonl`은 verifier가 *정의*만 하고 *호출*은
    tool 쪽에서만 ✓

## Why

```text
   "LLM이 했다고 말함" + "우리가 로그 기록"
                        ▲
                        └── 여기가 함정.
                            우리가 적으면 LLM이 말한 거 한 번 더 적는 셈.

   정확한 모양:
   LLM (말함)  ─────►  trace.jsonl     (claim, subjective)
   Tool (실행) ─────►  refund_log.jsonl (evidence, objective)
   Verifier   ─────►  비교만 함. 아무것도 안 적음.
```

이게 *흐려지면 발표 첫 슬라이드부터 무너짐.* "honesty verifier" 가 결국
"에이전트가 한 말 두 번 적기" 가 됨. ADR-0006이 이 문장을 코드 진입 *직전*
에 박은 이유.

Build order도 ADR-0006이 못박음: **(1) tool log 모델 → (2) toy tool →
(3) detectors → (4) agent.** 가장 *덜 신뢰되는* 컴포넌트(에이전트)가 가장
*신뢰되는* 컴포넌트(tool log 스키마)의 모양을 결정하지 않게.

## Snags

- **`call_id`를 Optional로 박을지 잠시 고민.** 에이전트가 trace에 기록
  *안 하고도* 툴을 호출할 수 있음 (직접 실행, harness 우회 등). 그
  비대칭 자체가 신호 (H-004 silent skip의 거울 케이스). 그래서
  `call_id: str | None`. 테스트에 명시 (`test_call_id_optional`).
- **`append_entry` 헬퍼가 `verifier` 패키지 안에 있음.** ADR-0006
  정신과 약간 긴장. 정당화: *스키마는 공유 인프라*, *호출 위치는 tool*.
  verifier 자기가 호출하지 *않는* 한 위반 아님 — grep로 검증.
- **`examples/tools/__init__.py` 빈 파일.** 패키지화는 의도적, 테스트가
  `from tools import refund_api` 가능하게.

## Next

- 0008: 두 번째 toy tool (예: `db_query`) — 같은 패턴 한 번 더 복제,
  스키마가 진짜 generalize되는지 확인.
- 그 다음 첫 detector. **dual-source가 살아있어야 의미 있는 H-NNN부터**:
  H-004 (silent skip) — trace는 "호출함" / log는 비어있음. 가장 단순
  한 비교, 가장 큰 그림 효과. demo opener 후보.
