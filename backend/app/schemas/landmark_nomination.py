"""Model nominations are discovery suggestions, never user requirements or facts."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class LandmarkNominationDraft(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    names: list[Annotated[str, StringConstraints(min_length=1, max_length=160, pattern=r"\S")]] = (
        Field(max_length=12)
    )


class LandmarkIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    name: str
    rank: int = Field(ge=1, le=12)
    origin: Literal["model_nomination"] = "model_nomination"
