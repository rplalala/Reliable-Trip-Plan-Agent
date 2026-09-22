"""Bounded static discovery provenance; never current factual evidence."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RetrievalQuery(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    query_id: str
    text: str = Field(min_length=1, max_length=200)
    origin: Literal["user", "system_default"]
    intent_ids: tuple[str, ...] = ()
    requirement_refs: tuple[str, ...] = ()
    version: Literal["rag_query_plan_1"] = "rag_query_plan_1"

    @model_validator(mode="after")
    def valid_links(self):
        if self.origin == "system_default" and (self.intent_ids or self.requirement_refs):
            raise ValueError("System defaults cannot claim user intent")
        if self.origin == "user" and (not self.intent_ids or not self.requirement_refs):
            raise ValueError("User queries require originating links")
        return self


class TripWorldOrigin(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", allow_inf_nan=False)
    source: Literal["tripworld"] = "tripworld"
    entity_id: str = Field(min_length=1)
    query: RetrievalQuery
    rank: int = Field(ge=1, le=20)
    cosine: float = Field(ge=-1.00001, le=1.00001)
    distance_km: float = Field(ge=0)
    artifact_hash: str = Field(min_length=1)
    text_hash: str = Field(min_length=1)
    space_id: str = Field(min_length=1)
    policy_version: str = Field(min_length=1)
    resolution: Literal["google_observation", "request_resolved", "direct_id", "fallback"]
    evidence_ref: str = Field(min_length=1)
