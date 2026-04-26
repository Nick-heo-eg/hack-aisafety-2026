"""Detector registry. Adding a detector = one import + one dict line.

H-002 lands first because its heuristic is the cleanest demo signal:
agent says "completed" / tool log says "error" → mismatch obvious.
"""

from __future__ import annotations

from collections.abc import Callable

from verifier.detectors import h002
from verifier.findings import Finding
from verifier.observer import ToolLogEntry
from verifier.trace import TraceEvent

DetectorFn = Callable[[list[TraceEvent], list[ToolLogEntry]], list[Finding]]

DETECTORS: dict[str, DetectorFn] = {
    h002.PATTERN_ID: h002.detect,
}

__all__ = ["DETECTORS", "DetectorFn"]
