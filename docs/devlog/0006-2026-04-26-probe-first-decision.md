# 0006 — Probe-first 결정 (2026-04-26)

## What

코드 가기 전 한 라운드 더 고민. 결과:

- 데모 시나리오를 *상상으로 박지 말고 LLM 행동을 먼저 측정*하기로.
- 1시간짜리 탐사(probe) 단계 추가 — 시나리오 5개 × 3회 = 15콜.
- L1~L4 스펙트럼 중 **L3** (LLM 진짜 판단 + 환경은 우리가 통제)로
  목표 잡음.
- 시나리오: S1 빈 DB / S2 tool error / S3 tool 회피 유혹 /
  S4 subagent 죽음 / S5 부분 성공.
- `experiments/` 디렉토리에 격리. 결과 jsonl은 `.gitignore`,
  요약만 devlog에.

## Why

- **상상한 honesty 실패만 잡는 detector는 가짜.** 실제 Gemini가
  *어떻게* 거짓말하는지 모르고 짜면 시연에서 안 나옴.
- L1/L2(하드코딩)는 "원리 증명"에 그침. AIM 심사위원에겐 "그래서
  실제 LLM에서 일어나나?" 받음.
- 1시간 투자가 다음 5시간을 정직하게 만듦 — *honesty verifier가
  honesty 원칙으로 만들어진다*는 메타 일관성.
- 결과가 어떻게 나와도 발표 자료가 됨: 위반 잘 일어나면 detector
  근거, 안 일어나면 "Gemini는 H-X에 강하다" 측정값.

## Snags

- 비결정성. 같은 프롬프트가 다른 응답 줌 → 시나리오당 3회 반복으로
  분포 보기.
- Gemini가 너무 정직할 위험. 보정 옵션은 압박 프롬프트 / 정직 결과
  그대로 쓰기 / 둘 다 보여주기 — 데이터 보고 결정.

## Next

- ADR-0006 작성 (probe-first 원칙).
- `experiments/probe_runner.py` + `scenarios.yml` 골격.
- 15콜 실행 → 결과 같이 읽음 → 그 다음 detector / 발표 시나리오 결정.
