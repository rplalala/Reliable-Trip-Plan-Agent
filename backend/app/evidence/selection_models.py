"""Inputs for evidence-informed POI selection."""

from datetime import date
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.evidence.models import PlaceCandidate, PlaceEvidence
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent
from backend.app.schemas.tripworld_discovery import TripWorldOrigin


class PlaceSelectionModel(BaseModel):
    """Keep selection metadata separate from shared planning evidence."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class SearchIntentKind(StrEnum):
    EXPLICIT_REQUIREMENT = "explicit_requirement"
    NORMAL_PREFERENCE = "normal_preference"
    FALLBACK = "fallback"


class PlaceSearchIntent(PlaceSelectionModel):
    """One bounded, application-classified Places query, not a semantic score."""

    intent_id: str = Field(min_length=1)
    term: str = Field(min_length=1)
    query: str = Field(min_length=1)
    kind: SearchIntentKind
    named_place_intent: NamedPlaceIntent | None = None

    @model_validator(mode="after")
    def named_place_kind_matches_inclusion(self) -> Self:
        if self.named_place_intent is None:
            return self
        expected = (
            SearchIntentKind.EXPLICIT_REQUIREMENT
            if self.named_place_intent.inclusion is NamedPlaceInclusion.REQUIRED
            else SearchIntentKind.NORMAL_PREFERENCE
        )
        if self.kind is not expected:
            raise ValueError("Named-place search kind must match its typed inclusion")
        return self


class QueryIntentHit(PlaceSelectionModel):
    """One original position in one unfiltered Places search response."""

    intent_id: str = Field(min_length=1)
    source_query: str = Field(min_length=1)
    provider_rank: int = Field(ge=0)
    actual_result_count: int = Field(ge=1)
    intent_kind: SearchIntentKind = SearchIntentKind.FALLBACK

    @model_validator(mode="after")
    def rank_within_response(self) -> Self:
        if self.provider_rank >= self.actual_result_count:
            raise ValueError("provider_rank must be inside the raw result list")
        return self


class PlaceOpeningDate(PlaceSelectionModel):
    """Source-supported Places opening date parts, not a trip availability claim."""

    year: int | None = Field(default=None, ge=1, le=9999)
    month: int | None = Field(default=None, ge=1, le=12)
    day: int | None = Field(default=None, ge=1, le=31)

    @model_validator(mode="after")
    def valid_full_date(self) -> Self:
        if self.year is not None and self.month is not None and self.day is not None:
            date(self.year, self.month, self.day)
        return self


class RatingAcquisitionState(StrEnum):
    NOT_ATTEMPTED = "not_attempted"
    AVAILABLE = "available"
    MISSING = "missing"
    DETAILS_FAILED = "details_failed"


class CoordinateState(StrEnum):
    VALID = "valid"
    MISSING = "missing"
    INVALID = "invalid"


class PlaceSelectionInput(PlaceSelectionModel):
    """Keep search and rating state outside shared V1-B-facing place contracts."""

    candidate: PlaceCandidate
    query_hits: list[QueryIntentHit] = Field(default_factory=list)
    discovery_origins: tuple[TripWorldOrigin, ...] = Field(default=(), max_length=80)
    search_opening_date: PlaceOpeningDate | None = None
    search_opening_date_observations: tuple[PlaceOpeningDate, ...] = ()
    details_opening_date: PlaceOpeningDate | None = None
    opening_date_conflict: bool = False
    structured_evidence: PlaceEvidence | None = None
    rating: float | None = Field(default=None, ge=0, le=5)
    rating_state: RatingAcquisitionState = RatingAcquisitionState.NOT_ATTEMPTED
    coordinate_state: CoordinateState = CoordinateState.VALID

    @model_validator(mode="after")
    def rating_matches_state(self) -> Self:
        if not self.query_hits and not self.discovery_origins:
            raise ValueError("Selection candidates need a real discovery origin")
        if (self.rating_state is RatingAcquisitionState.AVAILABLE) != (self.rating is not None):
            raise ValueError("rating is present exactly when rating_state is available")
        return self

    @property
    def discovery_intent_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {h.intent_id for h in self.query_hits}
                | {i for o in self.discovery_origins for i in o.query.intent_ids}
            )
        )
