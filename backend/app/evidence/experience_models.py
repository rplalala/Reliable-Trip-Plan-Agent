"""Review-derived evidence, separate from structured Places and Web contracts."""

from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.evidence.models import EvidenceAvailability


class ExperienceModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ExperienceDimension(StrEnum):
    CROWDING = "crowding"
    WALKING_INTENSITY = "walking_intensity"
    ACCESSIBILITY = "accessibility"
    FAMILY_FRIENDLINESS = "family_friendliness"
    VISIT_DURATION = "visit_duration"


class ExperienceValue(StrEnum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    LIGHT = "LIGHT"
    ACCESSIBLE = "ACCESSIBLE"
    MIXED = "MIXED"
    LIMITED = "LIMITED"
    FAMILY_FRIENDLY = "FAMILY_FRIENDLY"
    NOT_FAMILY_FRIENDLY = "NOT_FAMILY_FRIENDLY"
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"


ALLOWED_VALUES: dict[ExperienceDimension, frozenset[ExperienceValue]] = {
    ExperienceDimension.CROWDING: frozenset(
        {ExperienceValue.LOW, ExperienceValue.MODERATE, ExperienceValue.HIGH}
    ),
    ExperienceDimension.WALKING_INTENSITY: frozenset(
        {ExperienceValue.LIGHT, ExperienceValue.MODERATE, ExperienceValue.HIGH}
    ),
    ExperienceDimension.ACCESSIBILITY: frozenset(
        {ExperienceValue.ACCESSIBLE, ExperienceValue.MIXED, ExperienceValue.LIMITED}
    ),
    ExperienceDimension.FAMILY_FRIENDLINESS: frozenset(
        {
            ExperienceValue.FAMILY_FRIENDLY,
            ExperienceValue.MIXED,
            ExperienceValue.NOT_FAMILY_FRIENDLY,
        }
    ),
    ExperienceDimension.VISIT_DURATION: frozenset(
        {ExperienceValue.SHORT, ExperienceValue.MEDIUM, ExperienceValue.LONG}
    ),
}


class ReviewEvidence(ExperienceModel):
    review_id: str = Field(min_length=1)
    place_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    resource_name: str | None = None
    google_maps_uri: str | None = None
    publish_time: datetime | None = None


class ExperienceSignalDraft(ExperienceModel):
    dimension: ExperienceDimension
    value: ExperienceValue
    review_refs: list[str]

    @model_validator(mode="after")
    def valid_dimension_value(self) -> Self:
        if self.value not in ALLOWED_VALUES[self.dimension]:
            raise ValueError("Experience value is not allowed for its dimension")
        return self


class ExperienceProfileDraft(ExperienceModel):
    place_id: str = Field(min_length=1)
    summary: str | None = Field(default=None, max_length=240)
    summary_truncated: bool = False
    summary_review_refs: list[str] = Field(default_factory=list)
    signals: list[ExperienceSignalDraft] = Field(default_factory=list)
    review_count_used: int = Field(ge=0, le=5)

    @model_validator(mode="before")
    @classmethod
    def bound_diagnostic_summary(cls, value):
        if isinstance(value, dict) and isinstance(value.get("summary"), str):
            if len(value["summary"]) > 240:
                return {**value, "summary": value["summary"][:240], "summary_truncated": True}
        return value

    @model_validator(mode="after")
    def one_value_per_dimension(self) -> Self:
        dimensions = [item.dimension for item in self.signals]
        if len(dimensions) != len(set(dimensions)):
            raise ValueError("Experience dimensions must not be repeated")
        if self.summary is None and self.summary_review_refs:
            raise ValueError("A missing summary cannot have review refs")
        if self.summary is not None and not self.summary_review_refs:
            raise ValueError("A summary must cite reviews")
        return self


class ExperienceConfidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"


class ExperienceSignal(ExperienceModel):
    dimension: ExperienceDimension
    value: ExperienceValue
    review_refs: tuple[str, ...] = Field(min_length=1)
    confidence: ExperienceConfidence

    @model_validator(mode="after")
    def valid_dimension_value(self) -> Self:
        if self.value not in ALLOWED_VALUES[self.dimension]:
            raise ValueError("Experience value is not allowed for its dimension")
        return self


class ExperienceProfile(ExperienceModel):
    place_id: str = Field(min_length=1)
    availability: EvidenceAvailability
    summary: str | None = None
    summary_truncated: bool = False
    summary_review_refs: tuple[str, ...] = ()
    signals: tuple[ExperienceSignal, ...] = ()
    review_count_used: int = Field(default=0, ge=0, le=5)
    source: str = "google_places_reviews"
    retrieved_at: str | None = None
    unavailable_reason: str | None = None


def unavailable_profile(
    place_id: str,
    reason: str,
    *,
    review_count_used: int = 0,
    retrieved_at: str | None = None,
) -> ExperienceProfile:
    return ExperienceProfile(
        place_id=place_id,
        availability=EvidenceAvailability.UNAVAILABLE,
        review_count_used=review_count_used,
        retrieved_at=retrieved_at,
        unavailable_reason=reason,
    )
