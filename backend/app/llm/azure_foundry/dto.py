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


class FoundryTravelRequirementsDTO(FoundryTransportDTO):
    """Transport representation of extracted travel requirements."""

    destination: str | None
    start_date: str | None
    end_date: str | None
    traveler_count: int | None
    budget: FoundryMoneyDTO | None
    required_activities: list[str]
    excluded_activities: list[str]
    preferences: list[str]
    unresolved_fields: list[str]


class FoundryNamedPlaceIntentDTO(FoundryTransportDTO):
    """A copied user place surface and controlled inclusion decision."""

    place_text: str
    inclusion: Literal["REQUIRED", "OPTIONAL"]
    source_text: str


class FoundryRequirementsWithNamedPlaceIntentsDTO(FoundryTravelRequirementsDTO):
    """V1+ extraction preserves every base field and adds one intent array."""

    named_place_intents: list[FoundryNamedPlaceIntentDTO]


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


class FoundryExperiencePreferenceIntentDTO(FoundryTransportDTO):
    preference: Literal[
        "AVOID_CROWDS",
        "PREFER_LESS_WALKING",
        "PREFER_ACCESSIBLE",
        "PREFER_FAMILY_FRIENDLY",
        "PREFER_SHORT_VISIT",
        "PREFER_LONG_VISIT",
    ]
    importance: Literal["explicit_requirement", "normal_preference"]
    source_text: str


class FoundryTransportPreferenceIntentDTO(FoundryTransportDTO):
    mode: Literal["DRIVE", "WALK", "BICYCLE", "TRANSIT"]
    source_text: str


class FoundryPoiInterestDTO(FoundryTransportDTO):
    surface: str
    importance: Literal["explicit_requirement", "normal_preference"]
    source_text: str


class FoundryTripIntentExtractionDTO(FoundryRequirementsWithNamedPlaceIntentsDTO):
    """One V1 provider response for all bounded user-semantic capabilities."""

    requested_place_information: list[FoundryRequestedPlaceInformationDTO]
    experience_preferences: list[FoundryExperiencePreferenceIntentDTO]
    transport_preference: FoundryTransportPreferenceIntentDTO | None
    poi_interests: list[FoundryPoiInterestDTO]


class FoundryDateTimeDTO(FoundryTransportDTO):
    """Transport datetime split into explicit, independently required components."""

    date: str
    time: str
    utc_offset: str


class FoundryActivityDTO(FoundryTransportDTO):
    """Transport representation of one itinerary activity."""

    activity_id: str
    title: str
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


class FoundryItineraryDTO(FoundryTransportDTO):
    """Transport representation of a complete itinerary."""

    destination: str
    start_date: str
    end_date: str
    days: list[FoundryItineraryDayDTO]


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
