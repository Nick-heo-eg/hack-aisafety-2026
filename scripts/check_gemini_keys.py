"""Smoke-test all Gemini API keys present in the environment.

Usage:
    set -a; source ~/.env; set +a
    python scripts/check_gemini_keys.py

Probes each GEMINI_API_KEY[_N] with a single 1-token generation call and
reports liveness. Does not log key values (only last 4 chars for matching
against the announcements channel post).

This script is not part of the verifier itself — it lives under scripts/
for ad-hoc env validation.
"""

from __future__ import annotations

import os
import sys
import time

from google import genai
from google.genai import errors as genai_errors

KEY_VARS = ["GEMINI_API_KEY", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3"]
MODEL = "gemini-2.5-flash"
PROMPT = "Reply with the single word: pong"


def mask(key: str) -> str:
    return f"...{key[-4:]}" if len(key) >= 4 else "?"


def probe(key: str) -> tuple[bool, str]:
    # google-genai prefers GOOGLE_API_KEY / GEMINI_API_KEY env vars over the
    # api_key kwarg if they are set, which silently routes every probe through
    # the same key and invalidates the test. Strip both for the duration of
    # the call so the explicit kwarg is the only source of authority.
    saved = {k: os.environ.pop(k, None) for k in ("GOOGLE_API_KEY", "GEMINI_API_KEY")}
    try:
        client = genai.Client(api_key=key)
        t0 = time.perf_counter()
        try:
            resp = client.models.generate_content(model=MODEL, contents=PROMPT)
        except genai_errors.APIError as e:
            return False, f"APIError: {e.code} {e.message[:120]}"
        except Exception as e:  # noqa: BLE001 — surface anything during smoke test
            return False, f"{type(e).__name__}: {str(e)[:120]}"
        dt = (time.perf_counter() - t0) * 1000
        text = (resp.text or "").strip()
        return True, f"{dt:.0f}ms — {text!r}"
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


def main() -> int:
    found = [(v, os.environ[v]) for v in KEY_VARS if os.environ.get(v)]
    if not found:
        print("No GEMINI_API_KEY[_N] in env. Did you `source ~/.env`?", file=sys.stderr)
        return 2

    failed = 0
    for var, key in found:
        ok, detail = probe(key)
        status = "OK " if ok else "FAIL"
        print(f"[{status}] {var:<18} ({mask(key)}): {detail}")
        if not ok:
            failed += 1
    print(f"\nSummary: {len(found) - failed}/{len(found)} keys live.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
