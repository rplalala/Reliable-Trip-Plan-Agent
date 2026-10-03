"""Frozen post-primary inputs; measured targets and scopes are deliberately absent."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.evidence.effective_models import EffectivePlaceEvidence
from backend.app.evidence.models import PlaceEvidence, RouteEvidenceBundle
from backend.app.evidence.selection_models import PlaceSelectionInput
from backend.app.policies.poi_funnel import NamedPlaceResolution
from backend.app.policies.transport import TransportModeDecision
from backend.app.runtime.config_models import RuntimeConfig
from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
from backend.app.schemas.itinerary_projection import V1Itinerary
from backend.app.schemas.poi_semantics import POISemanticAssessment
from backend.app.tripworld.retrieval.geography import GeographicScope


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class FrozenCall(FrozenModel):
    operation: Literal[
        "repair_model",
        "places_search",
        "places_details",
        "route_matrix",
        "rag_embed",
        "rag_search",
        "poi_semantics",
    ]
    request: dict
    response: object = None
    error: str | None = None
    duration_seconds: float = Field(default=0, ge=0)

    @model_validator(mode="after")
    def failure_or_response(self):
        if self.error is not None and (not self.error.strip() or self.response is not None):
            raise ValueError("Declare one frozen response or a nonempty failure")
        return self


class FrozenCacheEntry(FrozenModel):
    key: tuple
    value_type: Literal["search", "details", "routes", "json"]
    value: object
    provider_envelope: bool = False


class FrozenAttempt(FrozenModel):
    key: tuple
    status: Literal["reserved_not_sent", "sent_incomplete", "sent_failed", "sent_succeeded"]


class SemanticState(FrozenModel):
    cache: dict[str, POISemanticAssessment] = Field(default_factory=dict)
    named_bindings: dict[str, str] = Field(default_factory=dict)
    calls: int = Field(default=0, ge=0)
    elapsed: float = Field(default=0, ge=0)
    failed: bool = False


class ControlledCase(FrozenModel):
    schema_version: Literal["rtpeval_controlled_case_1"]
    case_id: str = Field(min_length=1)
    revision: str = Field(min_length=1)
    role: Literal["target", "control"]
    original_input: dict
    primary: V1Itinerary
    requirements: InterpretedTripRequirements
    reference_date: date
    supply_ids: tuple[str, ...]
    places: tuple[PlaceEvidence, ...]
    transport: TransportModeDecision
    routes: RouteEvidenceBundle
    runtime: RuntimeConfig
    quantity_review: bool
    request_remaining: float = Field(ge=0)
    named_resolutions: tuple[NamedPlaceResolution, ...] = ()
    effective_places: tuple[EffectivePlaceEvidence, ...] = ()
    enriched: tuple[PlaceSelectionInput, ...] = ()
    admitted: tuple[PlaceSelectionInput, ...] = ()
    semantic_assessments: tuple[POISemanticAssessment, ...] = ()
    geographic_scope: GeographicScope | None = None
    original_rag: dict = Field(default_factory=dict)
    calls: tuple[FrozenCall, ...]
    cache: tuple[FrozenCacheEntry, ...] = ()
    attempts: tuple[FrozenAttempt, ...] = ()
    semantics: SemanticState | None = None
    rag_artifact_hash: str | None = None
    rag_embedding_allowed: bool = False
    rag_search_allowed: bool = False

    @model_validator(mode="after")
    def linked_primary(self):
        if self.runtime.v3_repair is None:
            raise ValueError("Frozen V3 repair configuration is required")
        if self.rag_search_allowed and not self.rag_artifact_hash:
            raise ValueError("Frozen retrieval capability requires an artifact hash")
        for field in ("destination", "start_date", "end_date"):
            value = str(getattr(self.primary, field))
            if value != str(self.original_input.get(field)) or value != str(
                getattr(self.requirements.requirements, field)
            ):
                raise ValueError(f"Original input/primary/requirements mismatch: {field}")
        ids = [p.place_id for p in self.places]
        if len(ids) != len(set(ids)) or len(self.supply_ids) != len(set(self.supply_ids)):
            raise ValueError("Duplicate frozen supply identity")
        if not set(self.supply_ids) <= set(ids):
            raise ValueError("Frozen supply has missing place evidence")
        return self
