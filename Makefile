.PHONY: demo demo-mismatch demo-paraphrase demo-openai test check help

# Default — what you run during the live demo.
demo:
	@PYTHONPATH=src .venv/bin/python examples/run_pressure_test.py

# Visual side-by-side mismatch (refund agent lies, tool log shows error).
demo-mismatch:
	@PYTHONPATH=src .venv/bin/python examples/run_demo.py

# Layered judge — heuristic 0/5 → MockJudge 3/5 → GeminiJudge 5/5.
demo-paraphrase:
	@PYTHONPATH=src .venv/bin/python examples/run_paraphrase_demo.py

# OpenAI Chat Completions → adapter → same H-002 detector.
demo-openai:
	@PYTHONPATH=src .venv/bin/python examples/run_openai_demo.py

# 43 tests, no external deps.
test:
	@.venv/bin/pytest -q

# Pre-demo sanity check (run 30 seconds before going live).
check:
	@echo "→ tests:"
	@.venv/bin/pytest -q | tail -1
	@echo "→ cache present:"
	@test -s runs/red_team_results.jsonl && echo "  ok ($$(wc -l < runs/red_team_results.jsonl) entries)" || echo "  MISSING"
	@echo "→ main demo runs:"
	@PYTHONPATH=src .venv/bin/python examples/run_pressure_test.py > /dev/null && echo "  ok" || echo "  FAILED"

help:
	@echo "make demo            — main pitch demo (cache-based, ~1 sec)"
	@echo "make demo-mismatch   — side-by-side trace vs tool log"
	@echo "make demo-paraphrase — heuristic vs Mock vs Gemini judge"
	@echo "make demo-openai     — OpenAI conversation through adapter"
	@echo "make test            — full test suite (43 tests)"
	@echo "make check           — pre-demo sanity check"
