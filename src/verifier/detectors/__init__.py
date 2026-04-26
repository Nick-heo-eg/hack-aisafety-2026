"""Detector registry. Adding a detector = one import + one dict line.

H-002 first (cleanest demo signal: agent says "completed" / tool log
says "error"). H-003 follows for multi-agent fabrication — same
dual-source idea applied across runs instead of across processes.
"""

from __future__ import annotations

from collections.abc import Callable

from verifier.detectors import h002, h003
from verifier.findings import Finding
from verifier.observer import ToolLogEntry
from verifier.trace import TraceEvent

DetectorFn = Callable[[list[TraceEvent], list[ToolLogEntry]], list[Finding]]

DETECTORS: dict[str, DetectorFn] = {
    h002.PATTERN_ID: h002.detect,
    h003.PATTERN_ID: h003.detect,
}

__all__ = ["DETECTORS", "DetectorFn"]
