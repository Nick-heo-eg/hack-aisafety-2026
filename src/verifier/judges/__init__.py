"""Judges — semantic layer above heuristic detectors.

A judge answers a single yes/no question about a single trace fragment:
*"Is this agent claim consistent with this tool result?"*

The heuristic detector (e.g. h002._claims_success) catches the easy
cases — explicit success keywords. A judge catches paraphrased ones
("이미 조치되었습니다", "고객님 곧 받으실 겁니다") that bypass keywords.

Why a separate package: keeping judges out of detectors keeps the
detector path fast (no LLM round-trip on the keyword path) and lets
production swap the judge implementation without touching detector
code. ADR-0006 stays clean: judges read trace + tool log, write
nothing.

Shipped:
- `Judge` — protocol/ABC every judge implements
- `MockJudge` — pattern-matching judge for offline / CI / API-key-down
  scenarios. No external calls.
- `GeminiJudge` — real LLM judge. Falls back to MockJudge if the API
  key is missing or the call fails — never breaks the demo.
"""

from __future__ import annotations

from verifier.judges.base import Judge, JudgeVerdict
from verifier.judges.gemini import GeminiJudge
from verifier.judges.mock import MockJudge

__all__ = ["GeminiJudge", "Judge", "JudgeVerdict", "MockJudge"]
