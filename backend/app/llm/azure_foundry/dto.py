"""Strict transport DTOs for Microsoft Foundry structured output."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class FoundryTransportDTO(BaseModel):
    """Base contract for values returned directly by Microsoft Foundry."""

    model_config = ConfigDict(extra="forbid", strict=True)


class FoundryMoneyDTO(FoundryTransportDTO):
    """Transport representation of a monetary amount."""

    amount: str
    currency: str


class FoundryRequestedPlaceInformationDTO(FoundryTransportDTO):
    target_surface: str
    target_source_text: str
    source_text: str
    requested_facet: (
        Literal[
            "general_admission_policy",
            "admission_fee",
            "ticket_requirement",
            "advance_ticket_purchase_requirement",
            "reservation_requirement",
        ]
        | None
    )
    operational_need: (
        Literal[
            "current_operational_status",
            "date_specific_operational_exception",
            "special_date_hours",
        ]
        | None
    )
    subject_scope: Literal["whole_venue", "sub_area", "exhibition", "ticket_product"]
    scope_text: str | None
    temporal_scope: Literal["GENERAL", "CURRENT", "TRIP_DATES", "EXPLICIT_DATE"]
    date_source_text: str | None
    requested_start_date: str | None
    requested_end_date: str | None


class FoundryTransportPreferenceIntentDTO(FoundryTransportDTO):
    mode: Literal["DRIVE", "WALK", "BICYCLE", "TRANSIT"]
    source_text: str


class FoundrySourceQuoteDTO(FoundryTransportDTO):
    quote: str
    occurrence: int


class FoundrySubjectDTO(FoundryTransportDTO):
    local_key: str
    label: str
    source_refs: list[FoundrySourceQuoteDTO]


class FoundryPartyTargetDTO(FoundryTransportDTO):
    kind: Literal["party"]


class FoundrySpecifiedTargetDTO(FoundryTransportDTO):
    kind: Literal["specified"]
    first_ref: str
    additional_refs: list[str]


class FoundryUnresolvedTargetDTO(FoundryTransportDTO):
    kind: Literal["unresolved"]
    reason: str


class FoundrySemanticDTO(FoundryTransportDTO):
    local_key: str
    normalized_text: str
    kind: Literal["preference", "constraint", "goal"]
    polarity: Literal["favor", "avoid"]
    strength: Literal["low", "medium", "high", "hard"]
    scope: Literal[
        "individual_poi", "selected_poi_set", "whole_trip", "itinerary_style", "transport"
    ]
    subject_target: FoundryPartyTargetDTO | FoundrySpecifiedTargetDTO | FoundryUnresolvedTargetDTO
    source_refs: list[FoundrySourceQuoteDTO]


class FoundryNamedRequirementDTO(FoundryTransportDTO):
    place_text: str
    inclusion: Literal["REQUIRED", "OPTIONAL", "EXCLUDED"]
    source_refs: list[FoundrySourceQuoteDTO]


class FoundryDiscoveryDTO(FoundryTransportDTO):
    requirement_refs: list[str]
    purpose: Literal["activity_or_category", "semantic_discovery"]
    query_text: str


class FoundryEvidenceRequestDTO(FoundryTransportDTO):
    requirement_ref: str
    dimension: Literal[
        "crowding", "walking_intensity", "accessibility", "family_friendliness", "visit_duration"
    ]
    preferred_values: list[
        Literal[
            "LOW",
            "MODERATE",
            "HIGH",
            "LIGHT",
            "ACCESSIBLE",
            "MIXED",
            "LIMITED",
            "FAMILY_FRIENDLY",
            "NOT_FAMILY_FRIENDLY",
            "SHORT",
            "MEDIUM",
            "LONG",
        ]
    ]
    avoided_values: list[
        Literal[
            "LOW",
            "MODERATE",
            "HIGH",
            "LIGHT",
            "ACCESSIBLE",
            "MIXED",
            "LIMITED",
            "FAMILY_FRIENDLY",
            "NOT_FAMILY_FRIENDLY",
            "SHORT",
            "MEDIUM",
            "LONG",
        ]
    ]


class FoundryOperationalConflictDTO(FoundryTransportDTO):
    field: Literal[
        "destination",
        "start_date",
        "end_date",
        "traveler_count",
        "budget.amount",
        "budget.currency",
    ]
    source_refs: list[FoundrySourceQuoteDTO]


class FoundryInterpretationDTO(FoundryTransportDTO):
    operational_conflicts: list[FoundryOperationalConflictDTO]
    named_places: list[FoundryNamedRequirementDTO]
    requested_place_information: list[FoundryRequestedPlaceInformationDTO]
    transport_preference: FoundryTransportPreferenceIntentDTO | None
    semantic_requirements: list[FoundrySemanticDTO]
    subjects: list[FoundrySubjectDTO]
    discovery_intents: list[FoundryDiscoveryDTO]
    experience_evidence_requests: list[FoundryEvidenceRequestDTO]
    extraction_issues: list[str]
    overflow: bool


class FoundryDateTimeDTO(FoundryTransportDTO):
    """Transport datetime split into explicit, independently required components."""

    date: str
    time: str
    utc_offset: str


class FoundryActivityDTO(FoundryTransportDTO):
    """Transport representation of one itinerary activity."""

    activity_kind: Literal["main_poi", "generic_activity", "transport", "free_time", "unknown"]
    activity_id: str
    title: str
    source_place_id: str | None
    place_name: str | None
    location: str | None
    start_time: FoundryDateTimeDTO
    end_time: FoundryDateTimeDTO
    estimated_cost: FoundryMoneyDTO | None
    notes: str | None


class FoundryItineraryDayDTO(FoundryTransportDTO):
    """Transport representation of one itinerary day."""

    date: str
    activities: list[FoundryActivityDTO]


class FoundryReferenceRecommendationDTO(FoundryTransportDTO):
    """Model-authored reference content; provenance is assigned by the application."""

    place_name: str
    source_place_id: str | None
    reason: str
    associated_day: str | None
    area: str | None
    uncertainty: str | None


class FoundryPrimaryItineraryDTO(FoundryTransportDTO):
    """V1 model output contains only the primary itinerary."""

    output_version: Literal["itinerary_2"]
    destination: str
    start_date: str
    end_date: str
    days: list[FoundryItineraryDayDTO]


class FoundryItineraryDTO(FoundryPrimaryItineraryDTO):
    """V0 model output includes subordinate model-knowledge references."""

    reference_recommendations: list[FoundryReferenceRecommendationDTO]


class FoundryExperienceSignalDTO(FoundryTransportDTO):
    dimension: Literal[
        "crowding", "walking_intensity", "accessibility", "family_friendliness", "visit_duration"
    ]
    value: Literal[
        "LOW",
        "MODERATE",
        "HIGH",
        "LIGHT",
        "ACCESSIBLE",
        "MIXED",
        "LIMITED",
        "FAMILY_FRIENDLY",
        "NOT_FAMILY_FRIENDLY",
        "SHORT",
        "MEDIUM",
        "LONG",
    ]
    review_refs: list[str]


class FoundryExperienceProfileDTO(FoundryTransportDTO):
    place_id: str
    summary: str | None
    summary_review_refs: list[str]
    signals: list[FoundryExperienceSignalDTO]
    review_count_used: int
