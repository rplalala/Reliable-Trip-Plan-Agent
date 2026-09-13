"""Source-bound official assessments, accepted claims, and gap outcomes."""

import hashlib
from datetime import date, datetime, time
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.evidence.scope_models import SubjectScope
from backend.app.evidence.web_models import OfficialInformationNeed
from backend.app.integrations.web.page_models import PageContentBlock


class OfficialModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class SourceKind(StrEnum):
    NATIVE_SNIPPET = "native_snippet"
    FETCHED_HTML = "fetched_html"


class TemporalBasis(StrEnum):
    CURRENT_GENERAL_POLICY = "current_general_policy"
    EXPLICIT_DATE_OR_RANGE = "explicit_date_or_range"
    CURRENT_POINT_STATUS = "current_point_status"
    UNSPECIFIED = "unspecified"


class HoursScheduleScope(StrEnum):
    DAILY = "daily"
    WEEKLY_PATTERN = "weekly_pattern"
    UNSPECIFIED = "unspecified"


class DateRelevance(StrEnum):
    YES = "yes"
    NO = "no"
    UNCERTAIN = "uncertain"


class ReasonerConfidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class OfficialClaimKind(StrEnum):
    CURRENT_OPEN = "current_open"
    CURRENT_CLOSED = "current_closed"
    TEMPORARY_CLOSURE = "temporary_closure"
    MAINTENANCE_CLOSURE = "maintenance_closure"
    REOPENING = "reopening"
    SPECIAL_OPENING = "special_opening"
    EARLY_CLOSURE = "early_closure"
    SPECIAL_HOURS = "special_hours"
    REGULAR_HOURS = "regular_hours"
    FREE_GENERAL_ADMISSION = "free_general_admission"
    PAID_ADMISSION = "paid_admission"
    TICKET_REQUIRED = "ticket_required"
    TICKET_NOT_REQUIRED = "ticket_not_required"
    ADVANCE_TICKET_PURCHASE_REQUIRED = "advance_ticket_purchase_required"
    ADVANCE_TICKET_PURCHASE_NOT_REQUIRED = "advance_ticket_purchase_not_required"
    RESERVATION_REQUIRED = "reservation_required"
    RESERVATION_NOT_REQUIRED = "reservation_not_required"


class EvidenceSourceBlock(OfficialModel):
    task_id: str
    source_kind: SourceKind
    source_url: str
    final_url: str | None = None
    redirect_chain: tuple[str, ...] = ()
    text: str = Field(min_length=1)
    body_sha256: str | None = None
    page_title: str | None = None
    content_blocks: tuple[PageContentBlock, ...] = ()

    @property
    def source_key(self) -> str:
        """Application-owned identity for one exact supplied source block."""

        parts = (
            self.task_id,
            self.source_kind.value,
            self.source_url,
            self.final_url or "",
            self.body_sha256 or "",
            self.text,
            self.page_title or "",
            *(
                f"{block.text}\x1e{'|'.join(block.section_headings)}"
                for block in self.content_blocks
            ),
        )
        return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:24]


class OfficialClaimCandidate(OfficialModel):
    source_key: str | None = None
    place_id: str
    place_name: str
    information_need: OfficialInformationNeed
    claim_kind: OfficialClaimKind
    value_text: str = Field(min_length=1)
    source_kind: SourceKind
    source_url: str
    final_url: str | None = None
    supporting_excerpt: str = Field(min_length=1, max_length=500)
    subject_scope: SubjectScope = SubjectScope.UNKNOWN
    subject_text: str | None = None
    predicate_text: str | None = None
    scope_text: str | None = None
    temporal_basis: TemporalBasis = TemporalBasis.UNSPECIFIED
    applicable_start_date: date | None = None
    applicable_end_date: date | None = None
    date_text: str | None = None
    time_text: str | None = None
    schedule_scope: HoursScheduleScope | None = None
    schedule_text: str | None = None
    opens_at: time | None = None
    closes_at: time | None = None
    amount: str | None = None
    amount_text: str | None = None
    currency: str | None = None
    updated_at: date | None = None
    updated_at_text: str | None = None


class EvidenceReasonerAssessment(OfficialModel):
    """One bounded semantic proposal; audit judgments are never acceptance rules."""

    relevant: bool
    supports_information_need: bool
    relevant_to_requested_dates: DateRelevance = DateRelevance.UNCERTAIN
    proposed_relation_to_baseline: str | None = None
    confidence: ReasonerConfidence | None = None
    brief_rationale: str | None = None
    candidate: OfficialClaimCandidate | None = None

    @model_validator(mode="after")
    def coherent_assessment(self) -> Self:
        if not self.relevant and self.candidate is not None:
            raise ValueError("Irrelevant assessment cannot contain a claim")
        if self.supports_information_need and (not self.relevant or self.candidate is None):
            raise ValueError("Supported information need requires a relevant claim")
        return self


class OfficialCurrentEvidence(OfficialClaimCandidate):
    authority_basis: str
    retrieved_at: datetime
    source_ref: str


class OfficialGapStatus(StrEnum):
    AVAILABLE = "available"
    PARTIAL = "partial"
    UNKNOWN = "unknown"
    UNAVAILABLE = "unavailable"


class OfficialGapOutcome(OfficialModel):
    task_id: str
    place_id: str
    information_need: OfficialInformationNeed
    status: OfficialGapStatus
    accepted_evidence: tuple[OfficialCurrentEvidence, ...] = ()
    meaningful_evidence: tuple[OfficialCurrentEvidence, ...] = ()
    conflict_source_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()
    page_target_attempts: int = 0
    extraction_calls: int = 0
    bounded_check_completed: bool = False
