"""Pre-planner, claim-scoped effective evidence contracts."""

from datetime import date as Date
from datetime import time
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from backend.app.evidence.official_models import (
    HoursScheduleScope,
    OfficialGapStatus,
    TemporalBasis,
)
from backend.app.evidence.scope_models import SubjectScope
from backend.app.evidence.web_models import OfficialInformationNeed, RequestedFacet


class EffectiveModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class EvidenceDimension(StrEnum):
    OPERATIONAL_AVAILABILITY = "operational_availability"
    OPENING_HOURS = "opening_hours"
    ADMISSION_POLICY = "admission_policy"
    TICKET_REQUIREMENT = "ticket_requirement"
    ADVANCE_TICKET_PURCHASE_REQUIREMENT = "advance_ticket_purchase_requirement"
    RESERVATION_REQUIREMENT = "reservation_requirement"


class EvidenceRelation(StrEnum):
    DUPLICATE = "duplicate"
    COMPATIBLE_ADDITION = "compatible_addition"
    GENERAL_BASELINE = "general_baseline"
    DATE_SPECIFIC_EXCEPTION = "date_specific_exception"
    SCOPED_OVERRIDE = "scoped_override"
    CONFLICT = "conflict"
    UNRESOLVED = "unresolved"


class OperationalDayStatus(StrEnum):
    CONFIRMED_DATE_OPEN = "confirmed_date_open"
    CONFIRMED_DATE_CLOSED = "confirmed_date_closed"
    GENERAL_BASELINE = "general_baseline"
    UNKNOWN_DATE_STATUS = "unknown_date_status"
    UNRESOLVED_CONFLICT = "unresolved_conflict"


class EffectiveFact(EffectiveModel):
    dimension: EvidenceDimension
    subject_scope: SubjectScope
    scope_text: str | None = None
    date: Date | None = None
    applicable_start_date: Date | None = None
    applicable_end_date: Date | None = None
    value_kind: str
    value_text: str
    opens_at: time | None = None
    closes_at: time | None = None
    schedule_scope: HoursScheduleScope | None = None
    schedule_text: str | None = None
    temporal_basis: TemporalBasis
    relation: EvidenceRelation
    source_refs: tuple[str, ...]
    authority_bases: tuple[str, ...] = ()
    source_updated_at: Date | None = None
    unresolved_reason: str | None = None


class StructuredEvidenceClaim(EffectiveModel):
    """Optional date-scoped structured fact; no future status is inferred from Places."""

    place_id: str
    dimension: EvidenceDimension
    subject_scope: SubjectScope = SubjectScope.WHOLE_VENUE
    scope_text: str | None = None
    value_kind: str
    value_text: str
    temporal_basis: TemporalBasis
    applicable_start_date: Date | None = None
    applicable_end_date: Date | None = None
    opens_at: time | None = None
    closes_at: time | None = None
    schedule_scope: HoursScheduleScope | None = None
    schedule_text: str | None = None
    source_ref: str
    authority_basis: str = "google_places"
    source_updated_at: Date | None = None


class EffectiveOperationalDay(EffectiveModel):
    date: Date
    status: OperationalDayStatus
    source_refs: tuple[str, ...] = ()
    general_baseline: str | None = None
    unresolved_reason: str | None = None


class EffectiveNeedStatus(EffectiveModel):
    information_need: OfficialInformationNeed
    status: OfficialGapStatus
    source_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


class EffectiveFacetStatus(EffectiveModel):
    information_need: OfficialInformationNeed
    requested_facet: RequestedFacet
    requested_subject_scope: SubjectScope
    requested_scope_text: str | None = None
    status: OfficialGapStatus
    source_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


class EffectivePlaceEvidence(EffectiveModel):
    place_id: str
    operational_days: tuple[EffectiveOperationalDay, ...]
    facts: tuple[EffectiveFact, ...]
    need_statuses: tuple[EffectiveNeedStatus, ...]
    facet_statuses: tuple[EffectiveFacetStatus, ...] = ()
    conflict_source_refs: tuple[str, ...] = ()
