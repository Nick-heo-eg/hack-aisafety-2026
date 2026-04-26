# 0009 — "Compresses reality" framing + H-005 deferred (2026-04-26)

## What

- 새 framing 도입: **"AI doesn't lie. It compresses reality."**
- v0 코드는 *그대로*. 메시지만 흡수 (slides 00 / 02 / 07 + video_script).
- 향후 확장 ADR-0007 (Stage compression / H-005) 작성 — proposed status.
- taxonomy.md에 H-005 spec 추가 (구현 안 함, spec only).

## Why

### framing 진화의 출처

사용자 직관에서 출발:

> "결제 API인데. 했다의 의미가, 결제하라고 기능을 API에 전달했다. API가 그걸
> 받았다. 받고서 실행을 했다. 실행하고나서 통장에서 돈이 빠져나간 걸 봤다.
> 각각 했다의 의미가 다른데. 그걸 뭉뚱그려서 Agent가 출력할 땐 했다. 라고
> 할 수도 있고."

→ "완료"가 *단일 상태가 아니라 시퀀스*임을 짚음. 우리 v0는 그 시퀀스의
*모든 stage*를 하나의 binary로 압축해 비교 — 한계가 있음. 그러나 사용자가
짚은 framing은 *현상* 자체를 더 정확히 명명함:

> "AI는 거짓말하지 않는다. 현실을 압축한다."

### 왜 강한가

- **공격적이지 않음.** "agent lies"는 비난조 — alignment 회사인 AIM에 미묘한
  거부감. "compresses reality"는 *기계적/중립*. 더 학술적.
- **CFO/실무자 즉시 이해.** "결제 완료" / "돈 안 빠짐" — abstraction 0.
- **도메인 일반화.** payment/refund/deploy/order — 같은 패턴, 다른 라이프사이클.
  슬라이드 한 장이 *generality* 시연.
- **우리 컨셉 강화.** dual-source는 *어떻게* 잡는가. compresses reality는
  *왜 이게 문제인가*. 둘이 위계로 박힘.

### 왜 v0는 코드 안 건드리나

전체 H-005 구현(ToolLogEntry 확장 + payment_api toy + h005 detector + tests +
demo) = ~2시간. v0 submission이 이미 coherent하고 영상 timeline 박혔음.
ADR-0007에 cost-benefit 명시.

대신 *이득은 흡수*: 15분 슬라이드 수정으로 새 메시지 박힘. 코드는 *credible
roadmap*으로 ADR에 박힘 — Q&A에서 "다음 단계?" 받으면 "ADR-0007 보세요"로
정확한 답.

### 메시지 위계 (영상)

새 구조:
```
Top thesis    (현상): AI doesn't lie. It compresses reality.
Sub thesis    (구조): Two writers. One reader.
Implementation (방법): heuristic + LLM judge layered on dual-source
```

영상 02 컷이 이 위계 그대로. Top → Sub → 다이어그램.

## Snags

- **새 framing이 v0 데모와 어긋날 위험.** v0 데모(`run_demo.py`)는 binary
  mismatch만 보여줌. "compresses reality" 듣고 데모 보면 "어? 단계가 안
  보이네?" 받을 수 있음.
  → 완화: 멘트에서 *binary는 special case*임을 자연스럽게 박음. "오늘
  보여드리는 건 가장 단순한 압축 — 한 단계로 압축된 케이스. 더 깊은 lifecycle
  압축은 H-005, ADR-0007 참조."
- **ADR이 "proposed"인 게 일관성 깨질 수도.** 기존 ADR은 다 *accepted*.
  proposed 패턴은 처음. 단 ADR-0007이 "msg-only로 v0 채택, 코드는 deferred"
  명시 — status 라벨이 정직.
- **taxonomy "spec only" 패턴이 처음.** H-005가 *구현 없는 패턴*으로 박힘.
  README의 4 honesty patterns 표 갱신 필요? — 현재 H-005 안 써있음. 표는
  H-001~H-004로 두고, 본문에 "+ H-005 proposed" 한 줄 정도면 충분. 별도
  작업.

## Next

- 영상 녹화 시 새 멘트로 시연 (slides/00/02/07 + video_script 반영됨)
- critique engine round 008에 framing 흡수 기록
- (선택) README "4 honesty patterns" 표에 H-005 행 추가 (status: proposed)
- (deferred) H-005 풀 구현 — ADR-0007의 build plan 따름. v1 마일스톤.
