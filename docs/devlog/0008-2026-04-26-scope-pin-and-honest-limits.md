# 0008 — Scope pin + 우리의 한계 명기 (2026-04-26)

## What

- 발표 framing **B (하이브리드)** 확정. C(풀 Guardrail vs Gate 데모) 거절 재확인.
- 첫 detector `H-002` (Hallucinated tool result) 출하. 5 테스트 추가, 총 21 통과.
- `examples/buggy_agent.py` + `examples/run_demo.py` — 좌우 분할 라이브 데모 작동.
- `docs/slides/01_guardrail_vs_gate.md` (5초 비유) + `docs/demo_script.md` (30초 멘트 + Q&A 4개).
- `docs/SESSION_STATUS.md` 신설 — 세션 단락 시 즉시 회복용 SSOT.
- 알려진 LLM agent 사고 4건(Air Canada 챗봇 / Replit DB 삭제 / Copilot 환각 수정 /
  Cursor 테스트 거짓)을 우리 4-layer 모델에 매핑 — sweet spot과 한계 둘 다 식별.

## Why — 무엇을 *고정*했나

### 우리 자리 (4-layer)

```
┌─────────────────────────────────────────────┐
│  Guardrail   (input/output)        ─ AIM Guard       │
│  Gate        (execution control)    ─ AIM Starfort    │
│  Supervisor  (decision logic)       ─ AIM Supervisor  │
├═════════════════════════════════════════════┤
│  Honesty Verifier  (말한 것 vs 실제)  ─ 우리           │
└─────────────────────────────────────────────┘
              ▲
        모두가 의존하는 가정:
        "agent는 자기 행동을 정직하게 보고한다"
        ── 우리가 검증하는 것은 *이 가정 자체*
```

차별 한 줄: **"Other systems assume the agent is honest. We verify that
assumption."**

### 왜 다시 한 번 박았나

오늘 하루에만 framing 흔들림 3회:
1. 오전: "execution failure verifier" → ADR-0004 피벗 (honesty)
2. 오후: "guardrail은 뚫리고 gate가 막는다" 데모 제안 → C 옵션
3. **B 합의** → 그래도 "결국 가드레일 보완 컨셉이지?" 재질문 → 재정렬

3번이 결정적. C는 ADR-0004 Direction A 정확히 그것 — AIM Guard / Starfort /
Supervisor 영역 정면. **"보완"이라는 단어가 들어가는 순간 우리는 그들 위에 얹힌
부속이 됨.** 우리 자리는 *보완*이 아니라 *그들이 안 보는 dimension*.

## 사고 사례 4건과 우리 적합도

```
사례                          Guardrail  Gate    Supervisor  우리 적합도
──────────────────────────    ────────   ────    ──────────  ──────────
1. Air Canada 챗봇 (2024)     ✅통과     ✅통과   ✅통과       ⭐⭐⭐ sweet
2. Replit prod DB 삭제 (2025) ✅통과     ❌Gate*  ✅통과       ⭐ 부분
3. Copilot 환각 수정 (2024)   ✅통과     ✅통과   ✅통과       ⭐⭐ 보통
4. Cursor 테스트 거짓 보고    ✅통과     ✅통과   △            ⭐⭐⭐ sweet

  * 사례 2: Gate가 *있었으면* 잡았을 수도. 사후 보고 거짓말은 우리가
    잡지만, 진짜 원하는 건 사전 차단 → Gate territory.
```

### Sweet spot (우리가 깔끔히 잡는 것)

- **사례 1 (Air Canada):** 환각 정책 인용 — 정책 DB 조회 log가 *없는데* 정책을
  인용함. H-002 변종.
- **사례 4 (Cursor):** "tests passed" 보고 — shell tool log엔 `exit_code=1`.
  H-002 정확히.

공통점: **행동 자체는 무해한데 보고가 거짓.** 다운스트림이 그 보고를 *근거로*
의사결정.

### 데모 시나리오 (refund) 위치

현재 데모는 *가상* 사례. 직관적이지만 인지도 낮음. 발표에서 "Air Canada 같은
케이스" 한 줄로 인지 부스트 가능. 또는 데모를 Cursor 시나리오로 교체 가능
(~30 LoC) — 결정 보류, 데모 안정성 우선.

## 우리의 한계 (의도적, 명기)

### 1. 사후 검출, 사전 차단 아님

우리는 *agent가 거짓말한 후* 잡음. Replit이 DB 지운 후 "복구했다"고 거짓말한
*뒤에* "복구 log 없음"을 보고함. **이미 일어난 행동은 못 되돌림.** 사전 차단은
Gate (Starfort) territory.

→ 발표 답변: "We close the *audit* gap, not the *execution* gap. Both are
needed. Gates without verifiers are guards without auditors."

### 2. Tool log 자체 위조엔 무력

ADR-0006의 dual-source 가정은 *agent가 tool log를 못 건드린다*는 것. tool 자체가
거짓 log를 쓰면 우리도 속음.

→ 완화: 프로덕션은 syscall capture(strace) 또는 HTTP proxy(mitmproxy)로 한 단계
더 외부화. ADR-0004 명시. v0 toy tool은 신뢰 전제.

### 3. *행동* 없는 거짓말 (순수 환각)

Air Canada 케이스 *자체*는 우리 sweet spot이지만, 미묘함: 챗봇이 정책 DB를
*아예 안 호출*하고 답변했다면 — *호출 시도 자체가 없음*을 어떻게 위반으로 박나?

→ 답: "정책 인용 시 정책 DB 조회 *필수*"라는 *정책 prerequisite*를 verifier가
알아야 함. v0 휴리스틱은 거기까지 못 감 — LLM judge layer가 필요 (H-002 깊은
버전, ADR-0005). v0는 *명시적 tool_call 후 거짓말* 케이스에 한정.

### 4. Heuristic의 paraphrase 취약

현재 H-002 detector는 한국어/영어 success keyword 매칭. 의역되면 못 잡음
("문제 없이 마무리되었습니다"는 키워드 없음).

→ LLM judge layer가 답이지만 v0는 heuristic floor만 출하. *측정 가능한 약점*
으로 둠 — "heuristic 잡힘 vs LLM judge 잡힘" 비교가 자체로 발표 자료.

### 5. Single-turn, single-agent

H-003 (subagent fabrication)은 taxonomy엔 있지만 v0 detector 없음. 멀티에이전트
시스템(Claude Code subagent, AutoGen, CrewAI)에서 가장 무서운 honesty 위반 케이스
인데 — 시간 부족.

→ 발표 답변: "v0는 floor. H-003은 다음 마일스톤. multi-agent 환경에서 가장
임팩트 큰 패턴이라는 인식은 ADR-0005에 박혀있음."

### 6. 우리 도구 *자체*는 production-grade 아님

데모용 toy tool, 자체 venv, fixture 기반 trace. 진짜 프로덕션 LangChain /
AutoGen / Claude Code adapter 없음.

→ 의도. ADR-0004: "원리가 깨끗히 보이는 것이 현실적이지만 어수선한 것보다 강함
(해커톤 시간엔)."

## Snags

- **Detector signature 변경.** `DetectorFn = Callable[[list[TraceEvent]],
  list[Finding]]` 였는데 H-002가 tool_log도 필요해서 `Callable[[list[TraceEvent],
  list[ToolLogEntry]], list[Finding]]`로 변경. **ADR-0003이 detector interface를
  trace-only로 가정**하고 있었음 — 코드는 바꾸고 ADR은 못 바꿈. 다음 작업으로
  ADR-0003 amendment 필요 (ADR-0001처럼 superseded 표시 + amendment 머리에).
- **Korean character width.** `run_demo.py` 좌우 분할 출력에서 한글이 width 2,
  ASCII width 1 — naive 계산으로 정렬 *대체로* 맞지만 이모지에서 1px씩 어긋남.
  데모 충분, 픽셀 perfect 아님.
- **B framing이 두 번째 흔들림.** "결국 가드레일 보완 아니냐"는 재질문이 왔다는
  것 자체가 위험 신호 — 발표 시 심사위원이 *동일한 오해*를 할 수 있음.
  데모 첫 멘트가 "We work *underneath*"인 이유 = 그 오해 *선제 차단*.
- **사고 사례 인용 검증 안 함.** Air Canada Moffatt 판결, Replit DB 삭제 사건은
  일반 지식. 발표에 인용하려면 정확한 출처 확인 필요. 현재는 framing 검증용
  사고 실험.

## Next

- **ADR-0007** — verifier ↔ gate consumer 분리 정당화 (코드 박은 후 작성).
- **ADR-0003 amendment** — DetectorFn signature 변경 명기.
- **커밋 끊기** — (a) detector + 테스트, (b) demo agent + runner, (c) docs (이
  devlog 포함).
- **선택지 A** — 데모 시나리오를 Cursor 테스트 거짓으로 교체 (~30 LoC, 인지도↑).
- **선택지 B** — 현재 refund 유지 + 발표 멘트에 "Air Canada/Cursor 같은 케이스"
  한 줄 끼움 (0 LoC).
- **선택지 C** — 사고 사례 매핑 슬라이드 추가 (위 4-사례 표).
