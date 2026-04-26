# 3-min Video Script — Two Writers, One Reader

> **센터 컷:** Two Writers diagram. 다른 모든 컷은 이걸 *받쳐주는* 역할만.
> **금지:** 슬라이드 욕심. "이것도 보여주고 싶다"는 생각이 들면 *지우는* 게 맞다.
> **3분 = 180초.** 컷 수가 아니라 *호흡*이 중요.

---

## 🎯 한 줄

> **The agent can lie in trace. The tool cannot lie in its own log.**

---

## 📐 Timeline (180초)

```
0:00 ─────────────────────────────────────── 3:00
│  hook  │ thesis │ ⭐ TWO WRITERS │ demo │ layer │ closing │
│  10s   │  15s   │      30s       │  85s │  20s  │   20s   │
```

| 시간 | 컷 | 화면 (영상에 보이는 것) | 음성 (말하는 것) | 자막 (영어) | 녹화 source |
|---|---|---|---|---|---|
| **0:00 - 0:10** | **Hook** | 정적 슬라이드: 큰 글씨 한 줄 + 검은 배경 | "AI 에이전트는 항상 '완료했습니다' 라고 말합니다. **진짜 했는지는, 아무도 확인하지 않습니다.**" | "AI agents always say 'done.' Nobody verifies they actually did." | `slides/00_hook.md` (신규) |
| **0:10 - 0:25** | **Thesis** | 4-layer 표 (Guardrail / Gate / Supervisor / **us**) — 우리 자리만 강조 | "가드레일은 입력을 봅니다. 게이트는 실행을 막습니다. 감독자는 추론을 봅니다. 우리는 *말과 실제*를 봅니다." | "Guardrail: input. Gate: execution. Supervisor: reasoning. **Us: claim vs reality.**" | `slides/04_layer_table.md` (기존) |
| **0:25 - 0:55** ⭐ | **TWO WRITERS** | 센터 다이어그램 (agent → trace / tool → log / verifier compares) — 천천히 등장 (애니메이션) | "두 개의 writer가 있습니다. 에이전트는 trace에 *자기 행동을* 적습니다. 도구는 *자기 자신*이 호출됐다는 사실을 자기 로그에 적습니다. **에이전트는 trace에 거짓말할 수 있습니다. 도구의 자기 로그에는 못 합니다.** 우리는 그 둘을 비교합니다." | "Two writers. The agent writes its own trace. The tool writes its own log. **The agent can lie in trace. The tool cannot lie in its own log.** We compare them." | `slides/02_two_writers.md` (신규 — 센터 컷) |
| **0:55 - 1:25** | **Demo 1: mismatch** | 터미널 녹화 — `run_demo.py` 좌우 분할 출력 | "환불 처리해달라는 요청. 도구는 service_unavailable로 실패. 에이전트는 *'완료했습니다'* 라고 말합니다. verifier가 *즉시* 잡습니다. 다운스트림 게이트는 고객 알림을 차단합니다." | "Refund request. Tool fails with service_unavailable. Agent says 'completed.' Verifier catches it. Gate blocks the customer notification." | `examples/run_demo.py` 녹화 |
| **1:25 - 1:50** | **Demo 2: paraphrase** | 터미널 녹화 — `run_paraphrase_demo.py` 3-column 표 | "키워드만 보면 우회됩니다. '이미 조치되었습니다' 같은 표현은 못 잡습니다. 패턴 판사를 더하면 일부 잡습니다. **실제 LLM 판사를 더하면 의미까지 잡습니다.** Heuristics miss it. Patterns catch some. **Semantics catch the rest.**" | "Keywords miss paraphrases. Pattern judge catches in-distribution. **Real LLM (Gemini) catches the rest.** Heuristics miss it. Patterns catch some. Semantics catch the rest." | `examples/run_paraphrase_demo.py` 녹화 (Gemini 키 활성화 상태) |
| **1:50 - 2:20** | **Demo 3: production** | 터미널 녹화 — `run_openai_demo.py` (짧게) + 코드 화면 1초 | "이건 toy일까요? OpenAI Chat Completions를 그대로 받습니다. 167줄짜리 어댑터로. 같은 detector, 같은 Finding. AutoGen, LangChain, Claude Code도 같은 패턴입니다." | "Just a toy? Plug in OpenAI Chat Completions. 167 lines of adapter. Same detector. Same Finding. AutoGen / LangChain / Claude Code follow the same pattern." | `examples/run_openai_demo.py` 녹화 |
| **2:20 - 2:40** | **Audit gap** | 정적 슬라이드: "Gate prevents the action. We prevent the *false belief* about it." | "게이트는 잘못된 행동을 막습니다. 우리는 그 행동에 대한 *거짓 믿음*을 막습니다. 게이트 없는 verifier는 무력하고, **verifier 없는 게이트는 검증되지 않은 가드입니다.**" | "Gates prevent the action. We prevent the **false belief** about it. Gates without verifiers are guards without auditors." | `slides/05_audit_gap.md` (기존) |
| **2:40 - 3:00** | **Closing** | TWO WRITERS 다이어그램 *재등장* (페이드인) + 큰 글씨 한 줄 + GitHub URL | "다른 시스템들은 *에이전트가 정직하다고 가정*합니다. 우리는 그 가정을 *검증합니다.* 두 개의 writer. 한 개의 reader." | "Other systems **assume** the agent is honest. We **verify** that assumption. **Two writers. One reader.**" | `slides/07_closing.md` (신규) — 02 재사용 + 텍스트 |

---

## 🎬 컷별 비중 (왜 이 시간 배분인가)

| 영역 | 시간 | 비중 |
|---|---|---|
| **데모 (1+2+3)** | 95s | **53%** ← 영상의 절반 이상이 *코드가 일하는 모습* |
| Thesis (Two Writers + 4-layer) | 45s | 25% |
| Hook + Closing | 30s | 17% |
| Audit gap | 20s | 11% |

→ **시간의 절반 이상이 데모.** 말로 설명하는 시간 < 보여주는 시간.

---

## 🎤 멘트 원칙

1. **한 컷 = 한 메시지.** 컷 안에서 두 번째 메시지 시작하면 *컷을 잘라야 함*.
2. **자막은 영어로 통일** (한국어 음성 + 영어 자막). AIM은 OpenAI/Anthropic 파트너 — 영어 자막이 *국제적 신뢰* 시그널.
3. **숫자는 자막에 박아둠** ("167 lines", "0/5 → 3/5 → 5/5"). 음성에서 흘려도 시각으로 잡힘.
4. **TWO WRITERS는 *느리게*** — 다른 컷보다 호흡 길게. 이게 thesis다.

---

## 📋 슬라이드 backlog

영상 timeline에서 도출된 *최소* 슬라이드:

| ID | 상태 | 우선순위 | 비고 |
|---|---|---|---|
| `00_hook.md` | 신규 | P0 | 한 줄 + 검은 배경. ~5분 spec |
| `02_two_writers.md` | 신규 | **P0 (센터)** | 다이어그램 spec — 가장 중요. ~20분 |
| `04_layer_table.md` | ✅ 있음 | — | 그대로 사용 |
| `05_audit_gap.md` | ✅ 있음 | — | 그대로 사용 |
| `07_closing.md` | 신규 | P1 | 02 재사용 + 텍스트 오버레이 |
| ~~`01_guardrail_vs_gate.md`~~ | 있음 | **drop** | timeline에 안 들어감. 04가 같은 일 함 |

→ **신규 3장 작성 필요** (00, 02, 07). 02가 압도적 우선.

---

## 🎥 녹화 자산

| Source | 무엇 | 비고 |
|---|---|---|
| 터미널 녹화 1 | `examples/run_demo.py` | 좌우 분할 출력 그대로. 한 번에 깨끗이. |
| 터미널 녹화 2 | `examples/run_paraphrase_demo.py` | **GEMINI_API_KEY set 상태**에서 녹화 (3-column 표 + Gemini 컬럼 살아있어야 함) |
| 터미널 녹화 3 | `examples/run_openai_demo.py` | 짧게 (5초 컷) |
| 코드 화면 1 | `src/verifier/adapters/openai_fc.py` 첫 화면 | 1초 컷 — "167줄" 시각 anchor |

**터미널 setup (영상 일관성):**
- 폰트 크게 (16-18pt)
- 다크 배경
- 프롬프트 미니멀 (`$` 만)
- 줄 너비 100자 이상 (run_paraphrase_demo는 92자 출력)

---

## ⚠️ 절대 하지 말 것

1. ❌ 슬라이드 추가 — backlog에 없으면 *짜지 말 것*. 메시지 분산.
2. ❌ "judge layer 아키텍처" 같은 jargon — 음성 멘트에 넣지 말 것.
3. ❌ "ADR-0006" 언급 — 시청자는 ADR이 뭔지 모름.
4. ❌ critique engine 언급 — 빌드 도구, 발표 자산 아님 (devlog 0008).
5. ❌ "비어있는 시장" framing — Thesis 컷에서 *우리 자리*만 강조하면 충분, 다른 layer 폄하 금지.

---

## 🚦 다음 작업

1. **`docs/slides/02_two_writers.md`** — 센터 다이어그램 spec (~20분)
2. `docs/slides/00_hook.md` (~5분)
3. `docs/slides/07_closing.md` (~5분)
4. 터미널 녹화 setup 점검 (폰트/배경)
5. 녹화 → 편집 → 자막 (영상 제작)

5는 사용자 영역. 1-3은 markdown spec까지 우리가 가능.
