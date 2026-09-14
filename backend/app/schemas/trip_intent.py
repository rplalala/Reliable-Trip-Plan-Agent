"""Provider-independent semantic intents extracted once for V1 and later versions."""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.evidence.scope_models import SubjectScope
from backend.app.evidence.selection_models import SearchIntentKind
from backend.app.evidence.web_models import OfficialInformationNeed, RequestedFacet
from backend.app.schemas.named_place_intent import NamedPlaceIntent
from backend.app.schemas.request import TravelRequirements


class ExperiencePreference(StrEnum):
    AVOID_CROWDS = "AVOID_CROWDS"
    PREFER_LESS_WALKING = "PREFER_LESS_WALKING"
    PREFER_ACCESSIBLE = "PREFER_ACCESSIBLE"
    PREFER_FAMILY_FRIENDLY = "PREFER_FAMILY_FRIENDLY"
    PREFER_SHORT_VISIT = "PREFER_SHORT_VISIT"
    PREFER_LONG_VISIT = "PREFER_LONG_VISIT"


class TravelMode(StrEnum):
    DRIVE = "DRIVE"
    WALK = "WALK"
    BICYCLE = "BICYCLE"
    TRANSIT = "TRANSIT"


class RequestedTemporalScope(StrEnum):
    GENERAL = "GENERAL"
    CURRENT = "CURRENT"
    TRIP_DATES = "TRIP_DATES"
    EXPLICIT_DATE = "EXPLICIT_DATE"


class SemanticIntentModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class RequestedPlaceInformation(SemanticIntentModel):
    """One user question, without a provider identity or Web execution decision."""

    target_surface: str = Field(min_length=1, max_length=160)
    target_source_text: str = Field(min_length=1, max_length=320)
    source_text: str = Field(min_length=1, max_length=400)
    requested_facet: RequestedFacet | None
    operational_need: OfficialInformationNeed | None
    subject_scope: SubjectScope = SubjectScope.WHOLE_VENUE
    scope_text: str | None = Field(default=None, max_length=160)
    temporal_scope: RequestedTemporalScope = RequestedTemporalScope.GENERAL
    date_source_text: str | None = Field(default=None, max_length=100)
    requested_start_date: date | None = None
    requested_end_date: date | None = None

    @model_validator(mode="after")
    def valid_kind_and_scope(self) -> "RequestedPlaceInformation":
        if (self.requested_facet is None) == (self.operational_need is None):
            raise ValueError("Exactly one requested facet or operational need is required")
        if self.operational_need not in (
            None,
            OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS,
            OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
            OfficialInformationNeed.SPECIAL_DATE_HOURS,
        ):
            raise ValueError("Only operational information needs are permitted")
        if self.operational_need is OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS and (
            self.temporal_scope
            not in (RequestedTemporalScope.GENERAL, RequestedTemporalScope.CURRENT)
        ):
            raise ValueError("Current status cannot represent a date-specific question")
        if self.operational_need in (
            OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
            OfficialInformationNeed.SPECIAL_DATE_HOURS,
        ) and self.temporal_scope not in (
            RequestedTemporalScope.TRIP_DATES,
            RequestedTemporalScope.EXPLICIT_DATE,
        ):
            raise ValueError("Date-specific operational questions require date scope")
        if self.subject_scope is SubjectScope.UNKNOWN:
            raise ValueError("Requested subject scope must be known")
        if (self.subject_scope is SubjectScope.WHOLE_VENUE) != (self.scope_text is None):
            raise ValueError("Sub-scope text must accompany a specific subject scope")
        if (self.temporal_scope is RequestedTemporalScope.EXPLICIT_DATE) != (
            self.date_source_text is not None
        ):
            raise ValueError("Explicit date scope requires its source text")
        if self.temporal_scope is RequestedTemporalScope.EXPLICIT_DATE:
            if self.requested_start_date is None or self.requested_end_date is None:
                raise ValueError("Explicit date scope requires normalized dates")
            if self.requested_start_date > self.requested_end_date:
                raise ValueError("Requested date range is reversed")
        elif self.requested_start_date is not None or self.requested_end_date is not None:
            raise ValueError("Only explicit date scope can provide normalized dates")
        return self


class ExperiencePreferenceIntent(SemanticIntentModel):
    preference: ExperiencePreference
    importance: SearchIntentKind
    source_text: str = Field(min_length=1, max_length=320)

    @model_validator(mode="after")
    def explicit_importance(self) -> "ExperiencePreferenceIntent":
        if self.importance is SearchIntentKind.FALLBACK:
            raise ValueError("User experience preference cannot be fallback discovery")
        return self


class TransportPreferenceIntent(SemanticIntentModel):
    mode: TravelMode
    source_text: str = Field(min_length=1, max_length=320)


class PoiInterest(SemanticIntentModel):
    surface: str = Field(min_length=1, max_length=160)
    importance: SearchIntentKind
    source_text: str = Field(min_length=1, max_length=320)

    @model_validator(mode="after")
    def explicit_importance(self) -> "PoiInterest":
        if self.importance is SearchIntentKind.FALLBACK:
            raise ValueError("User POI interest cannot be fallback discovery")
        return self


class TripIntentExtractionResult(SemanticIntentModel):
    """One bounded requirements extraction with separate semantic capabilities."""

    requirements: TravelRequirements
    named_place_intents: tuple[NamedPlaceIntent, ...] = Field(max_length=24)
    requested_place_information: tuple[RequestedPlaceInformation, ...] = Field(max_length=32)
    experience_preferences: tuple[ExperiencePreferenceIntent, ...] = Field(max_length=16)
    transport_preference: TransportPreferenceIntent | None
    poi_interests: tuple[PoiInterest, ...] = Field(max_length=24)
