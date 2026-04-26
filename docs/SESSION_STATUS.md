# SESSION_STATUS

> **목적:** 새 세션 시작 시 *즉시* 복구할 수 있게 현재 좌표만 박아두는 파일.
> 영구 기록은 `docs/devlog/` 와 `docs/decisions/` 가 담당. 이 파일은 *지금
> 여기*만. 한 화면에 들어와야 함.

---

## 🔥 발표 framing (확정 — Option B 하이브리드)

> **"Other systems assume the agent is honest. We verify that assumption."**

3단 데모:

1. **슬라이드 1장 (5초):** Guardrail vs Gate — 직관적 비유 *only*. AIM Guard/Starfort/Supervisor 영역 *건드리지 않음*.
2. **데모 (핵심):** Mismatch — `agent says "Refund completed"` vs `tool_log: error` → dual-source verifier가 즉시 감지
3. **마지막 한 줄:** `HOLD signal triggered → 고객 전달 차단` — Gate는 verifier의 *consumer*로만 등장

**왜 풀 Gate 데모(C)는 거절했나:** AIM Guard / Starfort / **AIM Supervisor** (2026 라인업)와 정면 충돌. ADR-0004가 이미 명시 거절. 웹검색(2026-04-26)으로 재확인 — AIM Supervisor가 "agent decision logic 모니터링, 환각/편향/PII flag" 광고 중. Gate 영역은 그들 territory.

**우리 차별점 (한 표):**

| 영역 | AIM | 우리 |
|---|---|---|
| Guardrail (input/output) | ✓ | ✗ |
| Supervisor (decision logic) | ✓ | ✗ |
| **Execution truth verification** | ✗ | ✓ |

---

## 📍 좌표

- **브랜치:** `main` (origin sync)
- **마지막 커밋:** `a24418b — ADR-0006: dual-source truth + first toy tool`
- **테스트:** **43 통과** (trace 9 + observer 8 + h002 6 + h003 5 + adapter 7 + judges 9 — Q9 FP 케이스 + H-003 detector 추가)
- **데모:** ✅ 셋 다 작동
  - `PYTHONPATH=src .venv/bin/python examples/run_demo.py` (메인 mismatch 데모)
  - `PYTHONPATH=src .venv/bin/python examples/run_openai_demo.py` (OpenAI 통합 — Q5 답)
  - `PYTHONPATH=src .venv/bin/python examples/run_paraphrase_demo.py` (judge layer — Q4 답, 0/4 → 4/4)
- **Working tree (uncommitted):**
  - `experiments/probe_honesty.py` (이전 세션)
  - `docs/SESSION_STATUS.md` (회복용)
  - `docs/slides/01_guardrail_vs_gate.md` (5초 비유 슬라이드)
  - `docs/demo_script.md` (30초 발표 스크립트 + Q&A)
  - `src/verifier/detectors/h002.py` (첫 detector)
  - `src/verifier/detectors/__init__.py` (레지스트리에 H-002 등록, signature 변경)
  - `tests/test_h002.py` (5개 테스트)
  - `examples/buggy_agent.py` (refund 거짓말 에이전트)
  - `examples/run_demo.py` (좌우 분할 + GATE HOOK 출력)

---

## 🎯 다음 할 것

**남은 것 (필수):**
1. **ADR-0007** — verifier ↔ gate consumer 책임 분리 정당화 (코드 본 다음 작성)
2. **DetectorFn signature 변경 영향**: detector가 `(trace, tool_logs)` 받도록 바뀜 — `docs/decisions/ADR-0003-detector-interface.md` 갱신 필요할 수 있음, 검토
3. **커밋** — 단위로 끊어서 (detector / agent+demo / docs)

**남은 것 (선택):**
- H-001 / H-003 / H-004 추가 detector
- LLM judge layer (H-002 깊이 강화) — Gemini 키 받으면

**차단 없음.** Gemini 키 leaked지만 데모는 hardcoded fixture로 100% 동작.

---

## 🎬 데모 출력 목표

```
╔═══════════════════════════════════╤═══════════════════════════════════╗
║  🟦 AGENT SAYS                     │  🟥 REALITY                       ║
╠═══════════════════════════════════╪═══════════════════════════════════╣
║  "환불 처리를 완료했습니다"         │  refund_api → status: error       ║
║  ✔ 정상 처리                       │  ❌ 실제 환불 안 됨                ║
╚═══════════════════════════════════╧═══════════════════════════════════╝

🚨 VERIFIER:  H-MISMATCH detected
              trace step 3 claims success / tool_log step 2 says error

🛑 GATE HOOK: HOLD signal sent
              → customer notification blocked
              → "We caught it before the customer ever heard it."
```

---

## 🗺 핵심 ADR

- **ADR-0004** — pivot to honesty verifier. *"Pivot to inline gate (Direction A): Direct collision with AIM Guard / Starfort. Worst possible position."* → C 옵션 거절 근거.
- **ADR-0005** — taxonomy H-001~H-004
- **ADR-0006** — dual-source truth. verifier는 비교만. (gate는 *consumer*, 위반 아님)
- **슬로건:** "The agent says. The tool records. The verifier compares."
- **차별 한 줄:** "Other systems assume the agent is honest. We verify that assumption."

---

## 🧰 빠른 명령어

```bash
cd ~/hack/hack-aisafety-2026
.venv/bin/pytest                         # 테스트
git log --oneline -5                     # 진행 확인
.venv/bin/python examples/run_demo.py    # ← 데모 실행 (만들 예정)
```

---

## 📂 핵심 파일

- `src/verifier/trace.py` — TraceEvent 7종 (입력 스키마)
- `src/verifier/observer.py` — ToolLogEntry (증거 스키마)
- `src/verifier/findings.py` — Finding (출력 모델)
- `src/verifier/detectors/__init__.py` — 레지스트리 (H-002 등록됨)
- `src/verifier/detectors/h002.py` — 첫 detector
- `examples/tools/refund_api.py` — toy tool, `fail=True` 지원
- `examples/buggy_agent.py`, `examples/run_demo.py` — 라이브 데모
- `docs/taxonomy.md` — 패턴 정의
- `docs/demo_script.md` — 30초 발표 스크립트 + Q&A
- `docs/slides/01_guardrail_vs_gate.md` — 5초 비유 슬라이드
- `README.md` — 7슬라이드 발표 구조

## 🛠 빌드 도구 (발표 외)

- `docs/critique/` — **내부 critique engine**. 발표에 언급 안 함.
  - `score.md` — 16 질문 한 화면 (현재: 🔴 0 / 🟡 2 / 🟢 **12** / 🟤 1 / 🟫 1 — round 011에서 Q16 (real Gemini red-team) green: 12 live calls)

## 🎬 발표 트랙 (백지 재시작 — 2026-04-26)

이전 video_script + slides 6장 **전부 폐기**. 시간/음성/컷 가정 다 기존 자산은 `.bak` 으로:

- `docs/video_script.md.bak` — 3분 timeline (참고용)
- `docs/demo_script.md.bak` — 30초 멘트 (참고용)
- `docs/slides.bak/` — 6장 전부 (02 Two Writers 다이어그램만 *후보로* 재활용 검토)

새 트랙: `docs/presentation/` — **`intro.md` 박힘** (round 011 데이터 + 사용자
재해석으로 도출된 *발표 출발 framing*). 한 줄: **"We didn't change the task.
We only changed the pressure."** 매체/길이/시각자료는 여전히 미정.

framing 진화 기록: [`devlog/0010`](devlog/0010-2026-04-26-pressure-not-task.md)

**살아있는 자산:** `examples/run_*.py` 3개 (변경 없음, 43 tests passing).
  - `questions.jsonl` — 질문 카탈로그
  - `rounds/001-...md` — Round 1 baseline 진단
  - 다음 세션 회복 시 `score.md` 먼저 읽기
