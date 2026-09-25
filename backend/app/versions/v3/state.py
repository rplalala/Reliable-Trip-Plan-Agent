"""V3 history and adopted output, without rewriting the primary supply ledger."""

from pydantic import Field

from backend.app.evidence.models import PlaceEvidence
from backend.app.schemas.itinerary import Itinerary
from backend.app.versions.v1.state import V1State
from backend.app.versions.v2.state import V2PlanningResult
from backend.app.versions.v3.models import ValidationModel, ValidationReport
from backend.app.versions.v3.repair_models import RepairResult, RepairScope


class V3Outcome(ValidationModel):
    review_policy: dict = Field(default_factory=dict)
    quantity_review_enabled: bool
    draft: Itinerary
    original_report: ValidationReport
    scope: RepairScope | None
    repair: RepairResult | None
    final_primary: Itinerary
    final_report: ValidationReport
    final_identity_ids: tuple[str, ...]
    final_places: tuple[PlaceEvidence, ...]
    draft_cost_projections: tuple[dict, ...] = ()
    final_cost_projections: tuple[dict, ...] = ()
    original_rag_discovery: dict = Field(default_factory=dict)
    reason: str


class V3State(V1State):
    v3_outcome: V3Outcome


class V3PlanningResult(V2PlanningResult):
    v3: V3Outcome
    nearby_ledger: dict = Field(default_factory=dict)
    nearby_diagnostics: dict = Field(default_factory=dict)
    request_resources: dict = Field(default_factory=dict)
