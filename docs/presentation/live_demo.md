# Live Demo — Cheatsheet

> 1초. 한 줄. cache 기반. live API 호출 없음.

---

## 사전 점검 (시연 30초 전)

```bash
make check
```

→ tests passing / cache present / main demo runs — 세 줄 확인.

---

## 시연

### 30초 컷 (메인)

```bash
make demo
```

### 말 (3 문장)

> "같은 요청입니다."
> "바꾼 건 하나 — pressure 입니다."
> "결과는 다릅니다."

→ 출력이 설명합니다. 길게 말하지 않습니다.

---

## 1-2 분 컷 (확장)

```bash
make demo
make demo-mismatch     # 좌우 분할 시각
```

추가 멘트:

> "이건 위반이 아닙니다."
> "상황에 따라 출력이 변합니다."
> "그 변형 *순간* 을 본 도구가 감지합니다."

---

## 3 분 컷 (풀)

```bash
make demo
make demo-mismatch
make demo-paraphrase   # heuristic 0/5 → judge 5/5
make demo-openai       # OpenAI conversation → 같은 detector
```

---

## Q&A 카드

- *"adversarial 실험인가요?"* → "아닙니다. baseline / authority / distress / combined — 모두 *현실 production 프롬프트*."
- *"Air Canada 같은 사고를 막는다는 뜻인가요?"* → "아닙니다. Air Canada 는 Gate 영역. 본 도구는 *그 이후* 단계, 정책 통과 후 깨지는 순간."
- *"정책을 자동 생성하나요?"* → "아닙니다. 정책 *교정 입력* 만 제공. 정책 결정은 인간."
- *"실제 LLM 의 응답인가요?"* → "예. cache 는 12 live Gemini calls verbatim. `runs/red_team_results.jsonl`."
- *"tool calling 진짜인가요?"* → "v0 setup 은 1-turn 시뮬레이션. 동일 mechanism 은 Sharma et al. 2023 (Anthropic) 에서 5 SOTA 모델로 검증됨."

---

## Fail-safe

| 시연 fail | 대응 |
|---|---|
| `make demo` 실행 fail | `cat runs/red_team_results.jsonl \| head -30` — verbatim 출력 직접 |
| 터미널 한글/이모지 깨짐 | GitHub `docs/presentation/PITCH.md` 직접 보여주기 |
| 시간 부족 | 30초 컷만 + PITCH 가리킴 |
| 명령어 타이핑 실수 | `make help` — alias 목록 |

---

## 백업 자산

- **메인 백업:** [`PITCH.md`](PITCH.md) — 한 페이지 pitch
- **데이터:** [`runs/red_team_results.jsonl`](../../runs/red_team_results.jsonl) — 12 entries verbatim
- **상세 분석:** [`incident_mapping.md`](incident_mapping.md), [`policy_pipeline.md`](policy_pipeline.md)
