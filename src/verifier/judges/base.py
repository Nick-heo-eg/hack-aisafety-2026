"""Judge protocol — what every implementation must provide."""

from __future__ import annotations

from typing import Literal, Protocol

from verifier.observer import ToolLogEntry

JudgeVerdict = Literal["consistent", "mismatch", "uncertain"]


class Judge(Protocol):
    """A judge takes one agent claim and the tool evidence behind it,
    and returns whether the two are consistent."""

    name: str

    def evaluate(
        self,
        *,
        agent_claim: str,
        tool_log_entry: ToolLogEntry,
    ) -> JudgeVerdict:
        """Return 'mismatch' to flag the claim as a likely lie.

        'consistent' clears the claim. 'uncertain' means the judge
        could not decide — detectors should treat this as a non-finding
        (false negatives are preferred over noisy false positives in
        v0; the demo's claim is *measurable* honesty checking, not
        exhaustive).
        """
        ...
