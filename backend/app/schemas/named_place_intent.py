"""Reusable user-intent contracts for specifically named places."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.app.schemas.request import TravelRequirements


class NamedPlaceInclusion(StrEnum):
    """Whether the user expects one named place in the final itinerary."""

    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"


class NamedPlaceIntent(BaseModel):
    """A user-mentioned place surface, without provider identity inference."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    place_text: str = Field(min_length=1, max_length=160)
    inclusion: NamedPlaceInclusion
    source_text: str = Field(min_length=1, max_length=320)
    additional_source_texts: tuple[str, ...] = ()

    @field_validator("place_text", "source_text")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Named-place text must not be blank")
        return value


class RequirementsWithNamedPlaceIntents(BaseModel):
    """One extraction result with unchanged base requirements and separate intents."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    requirements: TravelRequirements
    named_place_intents: tuple[NamedPlaceIntent, ...]
