# 0011 — Framing 4차 진화: "Audit gap, not execution gap" (2026-04-26)

## What

- 사용자 핵심 질문: *"이거 execution control / Gate 영역 아니야?"*
- 진단: Round 013 incident mapping이 *암묵적*으로 *우리가 사고를 막는다*는
  뉘앙스 줌. 정직하지 않음.
- 방향: 데이터/코드 안 바꿈. **포지션을 정확히 다시 박음** —
  "우리는 *audit gap*을 닫지, *execution gap*은 닫지 않는다."
- 새 자산 `docs/presentation/policy_pipeline.md` — Detection → Policy
  refinement input → Gate rule → Regression test 체인.
- `incident_mapping.md`, `intro.md`, CLI 출력, critique Q19를 같은 톤으로
  재정렬.

## Why

### Framing evolution timeline (4단계)

```
0008  "AI lies"
        — 공격적, alignment 청중 거부감

0009  "AI doesn't lie. It compresses reality."
        — 학술적, but trigger 설명 없음

0010  "We didn't change the task. We only changed the pressure."
        — trigger를 압박으로 명시. 실험 설계가 thesis가 됨.

0011  "We close the audit gap, not the execution gap."
        — 우리 *역할의 경계* 명시. Gate territory 인정.
```

### 왜 4단계가 필요했나

Round 013 incident mapping에서 Air Canada / Replit / Cursor 사례를 매핑.
강력한 자산이지만 *암묵적 함정*:

> "Air Canada 같은 사고를 우리가 막는다"

→ ❌ 거짓. Air Canada는 *Gate가 막았어야* 함. 챗봇이 *없는 정책 약속*하기
*전*에 차단했어야. 사후 verifier로는 *이미 고객에게 약속한 후*.

사용자가 정확히 짚음. 이 함정이 *발표에서 추격당하면* 우리 thesis 전체 흔들림.

### 정직 재정렬

```
Gate territory                    Audit territory (우리)
─────────────────                  ─────────────────────
1차 행동 차단                       1차 행동 후 *거짓 보고* 차단
실시간                              사후
"하기 전에 막음"                    "후에 *오인 확산* 막음"
```

**우리가 *진짜* 잡는 것:**
- 다운스트림 시스템 (CS팀, 청구, audit log) 의 *오인*
- Compound failure (1차 사고 + 2차 거짓보고 = 더 큰 사고) 차단
- 동일 패턴이 다른 고객에게 *반복*되기 전에 발견

**우리가 *못* 잡는 것:**
- 1차 행동 자체 — DB 삭제, 잘못된 정책 약속
- 실시간 차단
- 소급 복구

### 새 핵심 한 줄

> **"We don't stop the first mistake.**
> **We stop it from becoming systemic."**

> **"우리는 실행을 막는 시스템이 아니라,**
> **실행 이후의 거짓 보고가 정책·게이트·테스트로 되돌아가게 만드는 검증 레이어다."**

### Detection → Policy 체인 — 사용자 정리

운영 가능한 위치 명명:

```
1. Detection (Verifier)
       ↓ "이 패턴에서 정책이 실패했음" 증거 생산
2. Policy refinement INPUT
       ↓ 인간이 정책 수정 (자동 아님)
3. Gate rule update
       ↓ 새 정책을 Gate 규칙으로 컴파일
4. Regression test
       ↓ 정책 변경 시 우리 시나리오 4개로 검증
```

**핵심 톤 (반드시):**
> "Verifier는 policy를 *만들지 않는다*. policy가 어디서 실패하는지
> *증거*를 제공한다."

= input only. 자동 생성 약속 ❌.

## Snags

- **이전 자산 *모두* 살짝 톤 안 맞음.** intro.md, incident_mapping.md, CLI
  출력 다 "우리가 잡는다" 뉘앙스. 단계별 재정렬 (round 014에서).
- **AIM 정면 충돌 위험 *역전*.** "Gate가 막았어야" 한다고 인정 = AIM
  Starfort 영역 *명확히 인정*. 이전엔 회피하던 framing이 이제 *우리 정직성
  자산*. ADR-0004 "Direction A 거절" 정신 그대로 — Gate 안 만듦, *Gate
  consumer*로 명시.
- **메시지 *살짝 약해질* 위험.** "우리가 사고 막음" 보다 "사고 확산 막음"
  은 *덜 hero-like*. 보완: "Both layers needed. Gates without verifiers
  are guards without auditors." (audit_gap.md.bak에 박힌 한 줄)
- **자동 생성 톤 절대 금지.** "Verifier가 policy를 *고친다*"는 사용자
  정리에서 의도치 않게 강한 어조. 우리는 *증거 제공만*. 자동 정책 배포는
  *없는 약속*이라 봉인.

## Next

- 단계별 (사용자 결정 C) 진행:
  1. ✅ devlog 0011 (이 파일)
  2. policy_pipeline.md 신설
  3. incident_mapping.md 재정렬
  4. intro.md 위계 갱신
  5. CLI 출력 한 줄 조정
  6. critique Q19 + round 014
  7. 한 번에 commit
- 각 단계 *짧은 확인* 후 다음.
