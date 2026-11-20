"""API contract for saving a Simple Reaction Time session.

Schemas describe the JSON the API accepts and returns. They are separate from
the SQLAlchemy models in app/models, which describe how data is stored.
JSON uses camelCase (matching the TypeScript types); Python uses snake_case.
"""

from datetime import UTC, datetime
from typing import Self

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel

# Must match ANTICIPATION_THRESHOLD_MS in frontend/src/features/reactionTime/reactionTimer.ts.
# Anything faster is a guess, so the frontend already marks it premature.
MIN_VALID_REACTION_MS = 100
# Sanity cap: a "reaction" slower than this means the athlete wasn't paying attention.
MAX_VALID_REACTION_MS = 5000
# Bounds the request size. A normal session is 5 valid trials plus a few premature ones.
MAX_TRIALS_PER_SESSION = 50


class CamelModel(BaseModel):
    """Base for every API schema: camelCase JSON, unknown fields rejected."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
        extra="forbid",
    )


class ReactionTrialCreate(CamelModel):
    """One trial as sent by the frontend."""

    trial_index: int = Field(ge=0, strict=True)
    reaction_time_ms: int | None = Field(strict=True)
    is_premature: bool = Field(strict=True)

    @model_validator(mode="after")
    def check_time_matches_premature_flag(self) -> Self:
        if self.is_premature:
            if self.reaction_time_ms is not None:
                raise ValueError("A premature trial must have reactionTimeMs set to null.")
            return self

        if self.reaction_time_ms is None:
            raise ValueError("A valid trial must include reactionTimeMs.")
        if not MIN_VALID_REACTION_MS <= self.reaction_time_ms <= MAX_VALID_REACTION_MS:
            raise ValueError(
                f"reactionTimeMs must be between {MIN_VALID_REACTION_MS} and "
                f"{MAX_VALID_REACTION_MS} for a valid trial."
            )
        return self


class ReactionSessionCreate(CamelModel):
    """Request body for saving one completed reaction-time session."""

    started_at: AwareDatetime
    completed_at: AwareDatetime
    trials: list[ReactionTrialCreate] = Field(min_length=1, max_length=MAX_TRIALS_PER_SESSION)

    @field_validator("started_at", "completed_at")
    @classmethod
    def convert_to_utc(cls, value: datetime) -> datetime:
        # SQLite drops timezone info, so store everything in one zone: UTC.
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def check_session_is_consistent(self) -> Self:
        if self.completed_at < self.started_at:
            raise ValueError("completedAt cannot be before startedAt.")

        indexes = [trial.trial_index for trial in self.trials]
        if indexes != list(range(len(self.trials))):
            raise ValueError(
                "trialIndex values must be 0, 1, 2, ... in order, with no gaps or repeats."
            )

        if all(trial.is_premature for trial in self.trials):
            raise ValueError("A session needs at least one valid (non-premature) trial.")
        return self


class ReactionSessionRead(CamelModel):
    """Response after a session is saved."""

    id: int
    test_type: str
    started_at: datetime
    completed_at: datetime
    trial_count: int
    valid_trial_count: int