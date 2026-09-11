"""Strict transport DTOs for Microsoft Foundry structured output."""

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
