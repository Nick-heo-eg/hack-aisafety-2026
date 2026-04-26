# 30초 발표 스크립트

> **타깃:** AIM Intelligence 심사위원.
> **포지션:** AIM의 Guardrail / Gate / Supervisor 위 또는 옆에서 동작.
> **데모 한 줄:** "Other systems assume the agent is honest. We verify that assumption."

---

## ⏱ 타임라인

| 시간 | 내용 | 화면 |
|---|---|---|
| 0:00 - 0:05 | Slide 1 — Guardrail vs Gate 비유 | `docs/slides/01_guardrail_vs_gate.md` |
| 0:05 - 0:08 | "We work underneath." 한 줄 | (검은 화면 전환) |
| 0:08 - 0:25 | 라이브 데모 (`run_demo.py`) | 터미널 |
| 0:25 - 0:30 | 마무리 한 줄 + 차별 표 | (슬라이드 2) |

---

## 🎤 멘트 (그대로 읽으면 됨)

### 0:00 — 슬라이드 1 띄움

> "Guardrails check the input.
> Gates control execution.
> Different layers, both well-covered."

### 0:05 — 검은 화면 전환

> "We don't compete with either of them.
> We work **underneath**."

### 0:08 — 데모 실행

```bash
python examples/run_demo.py
```

화면에 좌우 분할 출력이 뜨면, 손가락으로 가리키며:

> "On the left — the agent says
> *'환불 처리를 완료했습니다.'*"

(0.5초 멈춤)

> "On the right — the tool's own log says
> the API call **failed.**"

(1초 멈춤. 심사위원이 좌우 비교하게 둠)

### 0:18 — 트리거 한 줄

> "**This is a silent failure.**
> Every guardrail downstream of this agent
> would believe the agent."

### 0:22 — 우리 도구 등장

> "Our verifier compares both sides
> and surfaces the lie — **without trusting either.**"

> "Then a gate hook receives the signal
> and stops the customer notification."

### 0:27 — 마무리 한 줄

> "**Other systems assume the agent is honest.
> We verify that assumption.**"

---

## 💬 예상 Q&A 대비

### Q1. "AIM Guard / Supervisor와 뭐가 다른가요?"

> "Guard는 input을 봅니다.
> Supervisor는 decision logic을 봅니다.
> 우리는 *말한 것 vs 실제 일어난 것*을 봅니다.
> 같은 dimension이 아닙니다 — orthogonal layer입니다."

표 보여주기:

| | Guardrail | Supervisor | Honesty Verifier |
|---|---|---|---|
| 봄 | input/output | decision logic | execution truth |
| 가정 | 에이전트 입출력은 신뢰 가능 | 에이전트 추론은 신뢰 가능 | **둘 다 검증 대상** |

### Q2. "Tool이 자기 로그 위조할 수도 있잖아요?"

> "그렇습니다. 우리 도구는 *agent vs tool* 신뢰 격차에 관한 것입니다.
> tool 자체 위조는 별도 위협 모델이며,
> 프로덕션에서는 syscall capture 또는 HTTP proxy로 한 단계 더
> 외부화할 수 있습니다 (ADR-0004 명시)."

### Q3. "Real-world에서 정말 일어나나요?"

> "이미 일어나고 있습니다.
> 모르고 있을 뿐입니다.
> 환불 안 됐는데 '됐다'고 답하는 챗봇은
> 매일 CS팀에 도착합니다 — 우리는 그 인과를 *기록*합니다."

### Q4. "왜 honesty인가? Hallucination이랑 뭐가 다른가요?"

> "Hallucination은 답이 틀린 것입니다.
> Honesty는 *행동*을 거짓 보고하는 것입니다.
> 후자가 훨씬 위험합니다 — 다운스트림 audit이 전부 무너지니까요."

---

## 🛡 안전 장치

- 데모는 hardcoded fixture (Gemini API 의존 ❌). 키 없어도 100% 동작.
- 1번 실행하면 `runs/demo/` 매번 새로 생성 (멱등).
- 테스트 21개 통과 — `pytest` 한 번 보여주는 것도 옵션.

---

## 📂 데모에 쓰는 파일들

- `examples/buggy_agent.py` — refund 거짓말하는 에이전트
- `examples/tools/refund_api.py` — 자기 자신 로깅하는 toy tool
- `src/verifier/detectors/h002.py` — Hallucinated Tool Result 감지
- `examples/run_demo.py` — 좌우 분할 출력 + GATE HOOK 한 줄
- `runs/demo/trace.jsonl` — agent의 자기보고 (gitignored)
- `runs/demo/refund_api.log.jsonl` — tool의 진짜 로그 (gitignored)
