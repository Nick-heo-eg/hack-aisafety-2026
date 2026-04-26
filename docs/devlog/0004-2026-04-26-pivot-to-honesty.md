# 0004 — Pivot to Honesty Verifier (2026-04-26)

## What

- 방향 통째 피벗: "execution-failure verifier" → "**Honesty Verifier**".
- 계기: 심사 회사 = AIM Intelligence. 웹 리서치로 그들이
  Stinger/AIM Red(공격) + Starfort/AIM Guard(방어) 둘 다 운영 중,
  시리즈 A 100억, OpenAI/Anthropic/Meta 보안 파트너, ACL 2025 논문
  3편 — 우리 원래 영역 *전부 그들 영역*.
- ADR-0004 (피벗 결정), ADR-0005 (H-001~H-004 honesty taxonomy) 작성.
- ADR-0001 superseded 표시 + 머리에 amendment 박음 (append-only 정신
  유지: 본문 안 건드리고 사후 수정 명시).
- README, taxonomy.md 통째 재작성.
- 옛 F-001 자산 삭제: detector(`f001.py`), buggy agent
  (`buggy_agent_f001.py`), fixture 3개, test_f001.py.
- `test_trace.py`의 fixture 의존 테스트는 inline JSONL 작성으로 변환
  (테스트 인프라는 살고, 옛 시나리오만 사라짐).
- Detector 레지스트리는 빈 dict로 — H-NNN detector 자리만 잡음.
- 9개 테스트 통과, ruff clean.

## Why

### 왜 갑자기 피벗했나

원래 ADR-0001은 "execution-layer는 prompt-layer보다 덜 다뤄진 영역"
이라 가정. 웹 리서치 5분에 무너짐:

```text
   원래 영역 ────────────────────────►  AIM 영역
   ─────────                            ────────
   prompt 공격                          Stinger / AIM Red
   execution 공격                       Stinger ("beyond prompt-level")
   런타임 게이트                        Starfort / AIM Guard
   다중모달                             Stinger (text/image/audio/video)
   에이전틱 시스템                      Stinger (multi-turn)

   → 우리 verifier가 들어가려던 자리, 다 그들이 이미 차지함.
```

이 상태에서 우리가 만드는 건 *그들의 미니어처*. 발표장에서 가장 약한
포지션. 매몰비용 무시하고 자리 옮기는 게 6커밋 추가 다음에 옮기는
것보다 *6배 싸다*.

### 왜 honesty인가 — 6개 후보 중 이걸 고른 이유

```text
   방향                          AIM과 충돌    살아남는 자산   새로움
   ───────────────────────────   ──────────    ─────────────   ─────
   A. Inline gate                정면 (Guard)  적음            낮음
   B. External verifier (원래)   영역 (Red)    거의 다         낮음
   C. Attack × Defense scorecard 정확히 사업   거의 다         0
   D. Agent diff                 약            절반            중
 ▶ E. Honesty Verifier           약            절반 (재해석)   높음
   F. Adversarial mutation       약            trace만         높음(학술)
```

E를 고른 이유:
- AIM의 *상업 영역 밖* — 그들 ACL 논문이 alignment 영역을 *알아보지만*
  *상업 제품으로는 안 만들고 있음*. 인정과 차별화 동시.
- 자산 절반 살아남음 (trace 스키마 ADR-0002, detector 인터페이스
  ADR-0003, Pydantic 모델, 테스트 인프라). 옛 F-002/F-005/F-006이
  사실은 honesty 패턴이었던 것 — taxonomy 재배치만 하면 됨.
- 데모 내러티브가 *영화처럼* 명확: "에이전트가 보고한 것 vs 실제
  일어난 것" — 시각적으로 양분됨.
- AI safety 연결 직설: deceptive self-report는 모든 audit과 모든
  guardrail의 *근거를 무너뜨림*.

### 왜 "외부 관찰"을 toy tool server로 가나

진짜 syscall capture(strace/ptrace)나 HTTP proxy(mitmproxy)는 더
*현실적*이지만 — 해커톤 시간엔 *원리가 깨끗히 보이는 것*이 *현실적
이지만 어수선한 것*보다 강함. ADR-0004에 "프로덕션은 syscall/proxy로
확장 가능" 명시. v0는 toy 충분.

## Snags

- **ADR-0001을 어떻게 처리할지가 결정 한 번 더 필요했음.** 옵션:
  (a) 통째 삭제, (b) 본문 다시 쓰기, (c) "superseded" 표시 + 머리
  amendment + 본문 보존. (c) 선택. *왜* 잘못 출발했는지가 ADR의
  가장 큰 가치 중 하나 — 그걸 지우면 같은 잘못 또 함.
- **taxonomy.md는 통째 재작성 (append-only 위반).** Devlog 0001/0003에
  앞으로의 규칙으로 "append-only" 박아둔 직후라 약간 아팠음. ADR-0005
  마지막 단락에 *왜 예외인지* 적음: taxonomy는 *deliverable spec*이지
  *historical record*가 아님. 역사는 ADR이 짊어짐. 같은 룰을 두 종류
  문서에 똑같이 적용하면 둘 중 하나가 망가짐.
- **fixture 의존 테스트 한 개**(`test_load_f001_fixture_roundtrips`)
  를 inline JSONL로 변환. 새 honesty fixture가 들어오기 전 단계라
  fixture 디렉토리는 비워둠 — 다음 detector 작업 시 채워질 자리.
- **devlog 0001과 0003이 이제 "사라진 코드"를 인용함.** 그대로 둠.
  append-only 정신: 과거가 틀렸다는 사실이 *기록*이지 *제거 사유*가
  아님.

## Next

- 0005: H-001 / H-004 (얕은 두 개 — heuristic 만으로 가능).
  toy tool server 골격까지 같이.
- 0006: H-002 / H-003 (깊은 두 개 — heuristic + LLM judge).
  - LLM judge 도입은 여기서 첫 등장.
  - Gemini 키 3개 라이브 (`scripts/check_gemini_keys.py`) — 환경 준비됨.
- 0007: 데모 시나리오 + 발표 자료.
