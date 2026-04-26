"""Detector registry. Adding a detector = one import + one dict line."""

from __future__ import annotations

from collections.abc import Callable

from verifier.detectors import f001
from verifier.findings import Finding
from verifier.trace import TraceEvent

DetectorFn = Callable[[list[TraceEvent]], list[Finding]]

DETECTORS: dict[str, DetectorFn] = {
    f001.PATTERN_ID: f001.detect,
}

__all__ = ["DETECTORS", "DetectorFn"]
