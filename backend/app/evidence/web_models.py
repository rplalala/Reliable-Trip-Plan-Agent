"""Acquisition-only contracts for the first V1-B Web Evidence phase."""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.evidence.scope_models import SubjectScope
from backend.app.integrations.web.models import WebSearchObservation


class OfficialInformationNeed(StrEnum):
    CURRENT_OPERATIONAL_STATUS = "current_operational_status"
    DATE_SPECIFIC_OPERATIONAL_EXCEPTION = "date_specific_operational_exception"
    SPECIAL_DATE_HOURS = "special_date_hours"
    ADMISSION_TICKET = "admission_ticket"
    RESERVATION_REQUIREMENT = "reservation_requirement"


class RequestedFacet(StrEnum):
    GENERAL_ADMISSION_POLICY = "general_admission_policy"
    ADMISSION_FEE = "admission_fee"
    TICKET_REQUIREMENT = "ticket_requirement"
    ADVANCE_TICKET_PURCHASE_REQUIREMENT = "advance_ticket_purchase_requirement"
    RESERVATION_REQUIREMENT = "reservation_requirement"


_ADMISSION_FACETS = {
    RequestedFacet.GENERAL_ADMISSION_POLICY,
    RequestedFacet.ADMISSION_FEE,
    RequestedFacet.TICKET_REQUIREMENT,
    RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
}


def canonical_facets(values: tuple[RequestedFacet, ...]) -> tuple[RequestedFacet, ...]:
    """Make merged task facets independent of detection order."""

    return tuple(sorted(set(values), key=lambda item: item.value))


class WebTriggerReason(StrEnum):
    RESIDUAL_MISSING = "residual_missing"
    RESIDUAL_FAILED_OR_PARTIAL = "residual_failed_or_partial"
    RESIDUAL_CONFLICT = "residual_conflict"
    EXPLICIT_USER_NEED = "explicit_user_need"
    EXPLICIT_DATE_QUESTION = "explicit_date_question"
    CLOSED_TEMPORARILY = "closed_temporarily"
    FUTURE_OPENING_UNCERTAIN = "future_opening_uncertain"
    OPENING_DATE_CONFLICT = "opening_date_conflict"
    PROACTIVE_CRITICAL_CURRENT = "proactive_critical_current"


class WebTaskStatus(StrEnum):
    NO_AUTHORIZED_DOMAIN = "no_authorized_domain"
    BUDGET_NOT_ATTEMPTED = "budget_not_attempted"
    COMPLETED_WITH_SOURCES = "completed_with_sources"
    COMPLETED_NO_SOURCES = "completed_no_sources"
    PARTIAL_RESPONSE = "partial_response"
    PROVIDER_FAILED = "provider_failed"


class WebPhaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class InformationGap(WebPhaseModel):
    place_id: str = Field(min_length=1)
    place_name: str = Field(min_length=1)
    information_need: OfficialInformationNeed
    requested_facets: tuple[RequestedFacet, ...] = ()
    requested_subject_scope: SubjectScope = SubjectScope.WHOLE_VENUE
    requested_scope_text: str | None = None
    applicable_start_date: date
    applicable_end_date: date
    reason: WebTriggerReason
    source_refs: tuple[str, ...] = ()


class WebEvidenceTask(WebPhaseModel):
    task_id: str = Field(min_length=1)
    place_id: str = Field(min_length=1)
    place_name: str = Field(min_length=1)
    information_need: OfficialInformationNeed
    requested_facets: tuple[RequestedFacet, ...] = ()
    requested_subject_scope: SubjectScope = SubjectScope.WHOLE_VENUE
    requested_scope_text: str | None = None
    applicable_start_date: date
    applicable_end_date: date
    allowed_domains: tuple[str, ...]
    trigger_reasons: tuple[WebTriggerReason, ...]
    priority_group: int = Field(ge=1, le=5)
    shortlist_index: int = Field(ge=0)

    @model_validator(mode="after")
    def valid_request_scope_and_facets(self) -> "WebEvidenceTask":
        if self.requested_subject_scope is SubjectScope.UNKNOWN:
            raise ValueError("Requested subject scope must be known")
        if self.requested_subject_scope is SubjectScope.WHOLE_VENUE:
            if self.requested_scope_text is not None:
                raise ValueError("Whole-venue request cannot name a sub-scope")
        elif not self.requested_scope_text:
            raise ValueError("Named sub-scope is required")
        if self.requested_facets != canonical_facets(self.requested_facets):
            raise ValueError("Requested facets must be unique and canonically ordered")
        if self.information_need is OfficialInformationNeed.ADMISSION_TICKET:
            if any(item not in _ADMISSION_FACETS for item in self.requested_facets):
                raise ValueError("Admission task has an incompatible facet")
        elif self.information_need is OfficialInformationNeed.RESERVATION_REQUIREMENT:
            if self.requested_facets not in ((), (RequestedFacet.RESERVATION_REQUIREMENT,)):
                raise ValueError("Reservation task has an incompatible facet")
        elif self.requested_facets:
            raise ValueError("Operational task cannot request admission facets")
        return self


class WebTaskOutcome(WebPhaseModel):
    task: WebEvidenceTask
    status: WebTaskStatus
    cache_hit: bool = False
    observation: WebSearchObservation | None = None
    error_type: str | None = None
