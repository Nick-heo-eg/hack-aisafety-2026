# Critique Engine — 내부 빌드 도구

> **이 디렉토리는 발표에서 언급하지 않는다.** 우리 자체 결정 도구.
> "심사위원이 *진짜 묻는다면* 어디서 깨지나"를 *재현 가능하게* 추적.
> 발표 자료가 아닌 이유: 메시지 분산 위험. (devlog 0008 참고)

---

## 루프 4단계

```
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   │  ① ASK                                                  │
   │     questions.jsonl 에서                                │
   │     status=open OR strength<green 인 질문 뽑기           │
   │                                                         │
   │  ② ANSWER                                               │
   │     현재 코드/문서 보고 답 작성                            │
   │     → rounds/NNN-YYYY-MM-DD-slug.md                     │
   │                                                         │
   │  ③ SCORE                                                │
   │     red / yellow / green                                │
   │     이유와 evidence (코드/문서 인용)                       │
   │                                                         │
   │  ④ REMEDIATE                                            │
   │     red/yellow → 보강 작업 큐로                          │
   │     보강 후 같은 Q 재평가 → 다음 round                    │
   │                                                         │
   │            ↑ ──────────────────────────── ↓            │
   └─────────────────────────────────────────────────────────┘
```

---

## Scoring rubric

| 강도   | 의미                                                    |
|--------|---------------------------------------------------------|
| 🟢 green  | 답이 *코드/문서로 시연 가능*. 심사위원 후속 질문에 답 있음. |
| 🟡 yellow | 답이 *원리적으로 있음*. 시연 부분적 또는 ADR로만 존재.       |
| 🔴 red    | 답이 약함. *말로만 있고* 시연/코드 없음. 추격당하면 깨짐.  |
| ⚪ open   | 아직 평가 안 함.                                          |

**원칙:** strength 평가는 *이 시점*의 상태. 보강하면 다음 round에서 올라감.

---

## 파일 구조

```
docs/critique/
├── README.md                          ← 이 문서 (엔진 spec)
├── questions.jsonl                    ← 질문 카탈로그 (구조화)
├── score.md                           ← 한 화면 현재 상태 (truncated 안 되게 짧게)
└── rounds/
    ├── 001-2026-04-26-baseline.md     ← 첫 라운드: Q1~Q12 baseline 진단
    ├── 002-NNN.md                     ← 보강 후 재평가
    └── ...
```

---

## Question 스키마 (`questions.jsonl` 한 줄 = 한 질문)

```json
{
  "id": "Q4",
  "category": "technical | positioning | meta | future",
  "question": "Heuristic은 paraphrase로 우회됩니다. 시연도 키워드 매칭 아닌가요?",
  "asker_persona": "AIM Supervisor 팀 엔지니어",
  "blast_radius": "high | medium | low",
  "strength": "red | yellow | green | open",
  "current_round": "001",
  "remediation_queue": ["heuristic +5 패턴", "한계 슬라이드"]
}
```

**필드 의미:**
- `category` — 질문 성격
- `asker_persona` — 누가 이 질문을 *가장 날카롭게* 던질 인물상
- `blast_radius` — 답 못 하면 발표가 *얼마나 깨지나*
- `strength` — 현재 답 강도 (위 rubric)
- `current_round` — 마지막 평가된 round 파일
- `remediation_queue` — 강도 올리려면 해야 할 작업들

---

## Round 파일 형식 (`rounds/NNN.md`)

```markdown
# Round NNN — title (YYYY-MM-DD)

## Scope
이번 라운드에서 다룬 질문 ID

## Q-NN
**Question:** ...
**Answer:** ...
**Evidence:** 파일 경로 / 라인 / 인용
**Strength:** red | yellow | green
**Why this strength:** 솔직히 어디가 약한가
**Remediation:** 강도 올리려면 무엇이 필요한가

(반복)

## Round summary
- 통과 (green): N개
- 보강 필요 (yellow): N개
- 위험 (red): N개
- 다음 라운드 진입 조건: ...
```

---

## 사용법

**새 질문 추가:**
```bash
# questions.jsonl에 한 줄 append
# strength=open, current_round="" 로 시작
```

**라운드 시작:**
1. `score.md` 읽고 strength<green 인 질문 식별
2. `rounds/NNN-...md` 새로 만들고 답 작성
3. `questions.jsonl` 의 strength + current_round 갱신
4. `score.md` 갱신

**다음 세션 회복:**
- `score.md` 한 화면이 SSOT
- 마지막 round 파일 보면 *왜* 그 강도인지 인용까지

---

## 무엇이 *아닌가*

- ❌ 발표 자료 — 메타 미학 카드는 메시지 분산 위험으로 거절 (devlog 0008)
- ❌ Verifier core 일부 — ADR-0006과 무관, 우리 메타 도구
- ❌ 자동화된 LLM judge — v0는 인간이 평가. Gemini 키 받으면 vN에서 LLM judge 추가 가능 (단, 이 도구가 *발표 무기가 되는 순간* 메시지 분산 — 빌드 전용 유지)

---

## 트리거 규칙 (언제 라운드를 도나)

- **자동:** 새 detector / 새 demo / 새 ADR이 추가될 때마다 영향 받는 질문 재평가
- **수동:** 사용자가 "이 질문 다시 봐달라" 또는 "새 질문 추가"
- **시간:** 발표 D-1에 전체 재평가 강제
