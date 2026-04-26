"""Finding — the only output type a detector returns.

See ADR-0003. Closed model: extending it is a schema change, not a
config change.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Finding(BaseModel):
    pattern_id: str
    run_id: str
    agent_id: str
    trigger_step: int = Field(ge=0)
    evidence_steps: list[int] = Field(default_factory=list)
    summary: str

    model_config = {"extra": "forbid"}
