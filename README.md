# Honesty Verifier

> **에이전트가 거짓말하는지 *증명하는* 도구.**
> Proving when an AI agent lies about what it did.

> AI는 모든 걸 다 했다고 말한다. 진짜로 했는지는 *아무도 검증하지 않는다*.
> AI says it did everything. Nobody verifies whether it actually did.

Built from scratch for the 2026 AI Safety hackathon (judge: AIM Intelligence).
No reuse of pre-existing internal projects.

---

## 🎬 Demo (3-min video)

> 🎥 _Video: **TBD** — link goes here once uploaded._
>
> _Prefer to run it yourself? Skip to **Quick start** below — under 60 seconds._

**What the video shows (3 min):**
1. The 4-layer position map (Guardrail / Gate / Supervisor / us)
2. Live demo — agent says "환불 처리를 완료했습니다", tool log says `status: error`,
   verifier flags H-002, gate hook blocks the downstream effect
3. The same detector running on a real OpenAI Chat Completions conversation
4. Heuristic 0 / 4 → +judge 4 / 4 on paraphrased lies
5. Closing — *"Other systems assume the agent is honest. We verify that assumption."*

---

## 🚀 Quick start (60 seconds)

Requires Python 3.11+.

```bash
git clone <this-repo>
cd hack-aisafety-2026

# One-time setup
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"

# 1. Run the test suite — 37 tests
.venv/bin/pytest

# 2. The main demo — agent says "complete" / tool log says "error"
PYTHONPATH=src .venv/bin/python examples/run_demo.py

# 3. OpenAI Chat Completions adapter — same detector, plugged into
#    a real production agent format (167 LoC of adapter code)
PYTHONPATH=src .venv/bin/python examples/run_openai_demo.py

# 4. The judge layer — heuristic catches 0 of 4 paraphrases,
#    + judge catches 4 of 4
PYTHONPATH=src .venv/bin/python examples/run_paraphrase_demo.py
```

The Gemini judge needs `GEMINI_API_KEY` set; without it, it returns
"uncertain" and the demos use the offline `MockJudge`. Nothing crashes
when the key is missing.

Every commit on `main` is independently runnable — `git checkout` any
commit and the steps above still work.

---

## 📦 What's actually built

| | Count |
|---|---|
| Tests passing | **37** |
| Live demos | 3 (`run_demo.py`, `run_openai_demo.py`, `run_paraphrase_demo.py`) |
| Detectors | 1 (H-002, with optional judge fallback) |
| Adapters | 1 (OpenAI Chat Completions) |
| Judges | 2 (Mock + Gemini, graceful degradation when key missing) |
| ADRs | 6 (decisions/) |
| Devlogs | 8 (devlog/, append-only) |
| Slides | 3 (slides/, markdown spec) |

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

| Layer | Sees | Assumes | Who |
|---|---|---|---|
| Guardrail | input / output | agent's I/O is trustworthy | AIM Guard, Llama Guard |
| Gate | execution control | agent's intent is trustworthy | AIM Starfort |
| Supervisor | decision logic | agent's reasoning is trustworthy | AIM Supervisor |
| **Honesty Verifier** | **claim vs evidence** | **❌ trusts nothing — the assumption is the target** | **us** |

**Other systems assume the agent is honest. We verify that assumption.**

우리는 가드레일도 공격기도 만들지 않는다. **기존 안전 장치들의 *가정 자체*를
검증한다.** Orthogonal layer — 같은 dimension에서 경쟁하지 않음.

---

## 어떻게 작동하나 / How it works

```text
   ┌─────────┐  말한다 / says   ──→  trace.jsonl   (자기 보고 / self-report)
   │  agent  │
   └────┬────┘  실행한다 / acts  ──→  tool_log     (외부 관찰 / external observation)
        │
        └────────►  ┌──────────────┐
                    │   verifier   │  heuristic + optional LLM judge
                    └──────┬───────┘
                           ▼
                       Findings
                           │
                           ▼
                    gate hook (consumer)
                    HOLD signal → block downstream effect
```

**Three rules (ADR-0006).** The agent writes trace. The tool writes
its own log. The verifier reads both, writes neither. Findings cite
both sources.

---

## 4 honesty patterns (taxonomy)

| ID    | Pattern (KO)                       | Pattern (EN)                      | v0 status |
|-------|------------------------------------|-----------------------------------|-----------|
| H-001 | 빈 결과로 자신만만한 답            | Confident claim on null state     | spec only |
| H-002 | 환각된 툴 결과                     | Hallucinated tool result          | **shipped** |
| H-003 | 서브에이전트 위조                  | Subagent fabrication              | trace schema supports; detector pending |
| H-004 | 침묵 누락                          | Silent skip                       | spec only |

H-002와 H-003은 깊게(휴리스틱 + LLM judge), H-001과 H-004는 얕게(휴리스틱)
출하 예정. 자세한 정의 + out-of-scope: [docs/taxonomy.md](docs/taxonomy.md).

---

## What we *don't* claim (deliberate scope)

- **Not a guardrail.** Input/output filtering is AIM Guard / Starfort territory.
- **Not real-time prevention.** We close the *audit* gap, not the *execution* gap.
  Gates without verifiers are guards without auditors — both are needed.
- **Not internal-objective inspection.** We verify *behavioral* honesty.
  Mesa-optimization / deceptive alignment in the internal sense is upstream.
- **Tool-log forgery.** v0 trusts the tool. Production extends to syscall
  capture or HTTP proxy as the external observation channel.

Full limits in [docs/devlog/0008](docs/devlog/0008-2026-04-26-scope-pin-and-honest-limits.md).

---

## Layout

```
src/verifier/
  trace.py         input schema (TraceEvent — agent's self-report)
  observer.py      evidence schema (ToolLogEntry — tool's own log)
  findings.py      output type (Finding — what a detector returns)
  detectors/       H-002 (heuristic + optional judge fallback)
  adapters/        OpenAI Chat Completions → TraceEvent
  judges/          Mock + Gemini, graceful degradation

examples/
  buggy_agent.py        refund agent that lies about success
  run_demo.py           main side-by-side demo
  run_openai_demo.py    OpenAI conversation through the adapter
  run_paraphrase_demo.py heuristic 0/4 vs +judge 4/4
  tools/refund_api.py   toy tool that records its own log

tests/                  37 tests, all passing
docs/
  decisions/            6 ADRs (why each decision)
  devlog/               8 entries (append-only daily rationale)
  slides/               3 presentation slides (markdown spec)
  critique/             internal build tool — not part of the pitch
  taxonomy.md           pattern spec
  demo_script.md        original 30-second pitch (3-min video script TBD)
  SESSION_STATUS.md     single-screen recovery file

experiments/            historical probing scripts (not required for demo)
```

---

## Appendix — Experiments

`experiments/` contains historical probing scripts referenced by
[devlog 0006](docs/devlog/0006-2026-04-26-probe-first-decision.md) /
[devlog 0007](docs/devlog/0007-2026-04-26-dual-source-and-first-tool.md).
Some require external API keys (e.g. `GEMINI_API_KEY`) and are
intentionally excluded from the Quick Start. They are guarded:
running them without the required key prints a clean `[SKIP]` and
exits 0 — they will not break a fresh clone.

---

## Decisions (ADRs)

| # | Decision |
|---|---|
| 0001 | Probe at execution layer, not prompt layer (later superseded by 0004) |
| 0002 | Trace event schema |
| 0003 | Detector interface (Finding contract) |
| 0004 | **Pivot to Honesty Verifier** (after AIM web research) |
| 0005 | Honesty taxonomy H-001..H-004 |
| 0006 | **Dual-source truth** — verifier reads, never writes |

---

## 용어 사전 / Glossary (KO ↔ EN)

| 한국어             | English                  | 의미 / Meaning                              |
|--------------------|--------------------------|---------------------------------------------|
| 정직성 검증기      | Honesty Verifier         | 도구 이름 / The tool                        |
| 자기 보고          | self-report              | 에이전트가 적은 trace                       |
| 외부 관찰          | external observation     | 툴 서버 로그 등 *진짜 일어난 일*의 증거     |
| 격차 / 어긋남      | discrepancy              | 발견의 단위                                 |
| 패턴 (H-NNN)       | pattern (H-NNN)          | taxonomy 항목                               |
| 휴리스틱 / LLM 판정자 | heuristic / LLM judge | detector의 두 layer                         |

---

## License

MIT — see [LICENSE](LICENSE).
