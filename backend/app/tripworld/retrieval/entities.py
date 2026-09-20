"""Deterministic global identity grouping and versioned retrieval documents."""












from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ENTITY_VERSION = "tripworld-retrieval-entity-v1"


TEXT_VERSION = "tripworld-entity-text-v1"


class RetrievalEntity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)
    retrieval_entity_id: str
    google_place_id: str | None
    source_fsq_place_ids: tuple[str, ...]
    preferred_name: str | None
    aliases: tuple[str, ...]
    latitude: float | None = Field(ge=-90, le=90)
    longitude: float | None = Field(ge=-180, le=180)
    localities: tuple[str, ...]
    regions: tuple[str, ...]
    country: str | None
    countries: tuple[str, ...]
    fsq_categories: tuple[str, ...]
    google_categories: tuple[str, ...]
    direct_semantics: tuple[str, ...]
    inferred_semantics: tuple[str, ...]
    semantic_rule_ids: tuple[str, ...]
    source_eligibility_hints: tuple[str, ...]
    eligibility_hint: Literal["eligible", "ineligible", "unknown"]
    retrieval_description: str
    raw_retrieval_text: str
    retrieval_text: str
    coordinate_spread_km: float
    location_flags: tuple[str, ...]
    source_row_count: int
    tripworld_revision: str
    semantic_mapping_version: str
    retrieval_entity_builder_version: str
    retrieval_text_template_version: str
    content_hash: str
