# 0001 — Kickoff and scaffolding (2026-04-26)

## What

- 프라이빗 레포 `Nick-heo-eg/hack-aisafety-2026` 생성, MIT.
- 로컬 클론 `~/hack/hack-aisafety-2026/`, Python src-layout 부트스트랩,
  pytest 스모크 통과.
- ADR-0001: execution-layer 프로빙으로 방향 못박음.
- Failure taxonomy v0: F-001~F-006 6개 패턴 초안.
- 커밋: `d48e31d`, `9129ebf`, `28057a0`, `784087a`.

## Why

- **AI safety 주제 후보 4개 중 (e) "Agent Failure Verifier" 선택.**
  Jailbreak/output guardrail/refusal calibration은 다 *프롬프트 레이어*다.
  레드오션이고, 진짜 운영에서 본 실패들은 거기서 안 잡힌다 — 툴이 빈
  결과를 줬는데 에이전트가 자신만만하게 다음 단계로 가는 류.
- **Verifier로 프레이밍 (모델 X, 데모 X).** 패턴이 누적 자산이 되도록.
  단발 데모는 해커톤 끝나면 죽는다.
- **Taxonomy 먼저, detector 나중.** detector가 *무엇을* 찾는지 정의가
  먼저 없으면 코드가 정의가 되어버린다 — 나중에 못 바꾼다.
- **ADR 분리.** taxonomy는 *목록*, ADR은 *왜 이 목록인가*. 둘을 한
  파일에 섞으면 둘 다 읽기 어려워진다.

## Snags

- `gh repo create --confirm` deprecation 경고. 무해, 다음에 빼면 됨.
- 첫 `git commit`을 `cd` 없이 쳤는데 됐길래 잠깐 의심 — 이전 Bash 호출의
  `cd hack-aisafety-2026`가 같은 셸 인보케이션 안에 살아있어서였음. 셸
  상태는 호출 사이에 안 남는다고 알고 있었지만, *같은* `&&` 체인 안에서는
  당연히 남는다. 다음부턴 절대경로로 가는 게 안전.
- GH_TOKEN scope에 `read:org` 빠져있음. 지금은 무관, 조직 작업 들어가면
  그때 refresh.

## Next

- Trace 스키마 정의 (ADR-0002 + Pydantic 모델).
- 첫 detector: F-001 silent-fallback. fixture trace + pytest로.
- 의도적으로 F-001 트리거하는 toy buggy agent — detector 정답지 검증용.
