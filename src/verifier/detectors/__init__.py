"""Detector registry. Adding a detector = one import + one dict line.

Empty in v0 — see ADR-0004 / ADR-0005. H-001..H-004 land in subsequent
commits.
"""

from __future__ import annotations

from collections.abc import Callable

from verifier.findings import Finding
from verifier.trace import TraceEvent

DetectorFn = Callable[[list[TraceEvent]], list[Finding]]

DETECTORS: dict[str, DetectorFn] = {}

__all__ = ["DETECTORS", "DetectorFn"]
