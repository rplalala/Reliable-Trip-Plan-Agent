"""Deterministic V1-B residual-need and operational-risk task policy."""

import hashlib
import re
import unicodedata
from collections.abc import Mapping, Sequence
from datetime import date
from urllib.parse import urlsplit

from backend.app.evidence.models import EvidenceAvailability, PlaceCandidate, PlaceEvidence
from backend.app.evidence.scope_models import SubjectScope
from backend.app.evidence.web_models import (
    InformationGap,
    OfficialInformationNeed,
    RequestedFacet,
    WebEvidenceTask,
    WebTriggerReason,
    canonical_facets,
)
from backend.app.integrations.web.models import WebEvidenceSearchRequest
from backend.app.runtime.config_models import WebEvidenceConfig
from backend.app.schemas.request import TravelRequest, TravelRequirements

WEB_TASK_TEMPLATE_VERSION = "official_web_v2"
LEXICAL_TRIGGER_VERSION = "official_needs_en_v1"
EXPLICIT_NEED_PHRASES: dict[str, tuple[str, ...]] = {
    "current_status": ("open now", "currently open", "currently closed", "is it open"),
    "date_closure": ("closed", "closure", "maintenance", "reopening"),
    "special_hours": ("holiday hours", "special hours", "open on", "hours on"),
    "admission": ("ticket", "tickets", "admission", "entry fee", "entrance fee", "free entry"),
    "reservation": (
        "reservation",
        "booking required",
        "need to book",
        "book in advance",
        "prebook",
        "pre-book",
    ),
}
DATE_SCOPE_PHRASES = (
    "during my trip",
    "during our trip",
    "on my trip date",
    "on our trip date",
    "when we visit",
    "on christmas",
    "on new year",
    "on easter",
)
MUST_VISIT_PHRASES = ("must visit", "must see", "definitely visit")
NAMED_CURRENT_STATUS_TEMPLATES = (
    "is {place} open",
    "is {place} closed",
    "will {place} be open",
    "will {place} be closed",
)
_KNOWN_STATUSES = {"OPERATIONAL", "CLOSED_TEMPORARILY", "CLOSED_PERMANENTLY", "FUTURE_OPENING"}
_NEED_ORDER = {
    OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION: 0,
    OfficialInformationNeed.SPECIAL_DATE_HOURS: 1,
    OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS: 2,
    OfficialInformationNeed.RESERVATION_REQUIREMENT: 3,
    OfficialInformationNeed.ADMISSION_TICKET: 4,
}


def normalize_phrase(value: str) -> str:
    """Normalize English policy phrases without inferring aliases or translations."""

    folded = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[^\W_]+", folded, flags=re.UNICODE))


def _has_phrase(text: str, phrase: str) -> bool:
    return f" {normalize_phrase(phrase)} " in f" {text} "


def _has_any(text: str, phrases: Sequence[str]) -> bool:
    return any(_has_phrase(text, phrase) for phrase in phrases)


def _has_named_current_status(text: str, place_name: str) -> bool:
    return _has_any(
        text,
        tuple(template.format(place=place_name) for template in NAMED_CURRENT_STATUS_TEMPLATES),
    )


def _sentences(value: str) -> list[str]:
    return [normalize_phrase(item) for item in re.split(r"[.!?\n]+", value)]


def _authorized_domain(value: str, *, uri: bool) -> str | None:
    if uri:
        parts = urlsplit(value)
        if parts.scheme.lower() != "https" or parts.username or parts.password:
            return None
        domain = parts.hostname
    else:
        if "/" in value or ":" in value or "@" in value:
            return None
        domain = value
    if not domain:
        return None
    try:
        ascii_domain = domain.rstrip(".").encode("idna").decode("ascii").casefold()
    except UnicodeError:
        return None
    if ascii_domain == "localhost" or ascii_domain.endswith(".localhost"):
        return None
    if not re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+", ascii_domain):
        return None
    return ascii_domain


def canonicalize_allowed_domains(values: Sequence[str]) -> tuple[str, ...]:
    """Canonicalize domains for provider requests and semantic cache identity."""

    domains: set[str] = set()
    for value in values:
        host = _authorized_domain(value, uri=False)
        if host is None:
            raise ValueError(f"Invalid authorized Web domain: {value}")
        domains.add(host)
    return tuple(sorted(domains))


def authorized_domains(
    place: PlaceEvidence,
    need: OfficialInformationNeed,
    config: WebEvidenceConfig,
) -> tuple[str, ...]:
    """Provide bounded acquisition domains, not final source authority."""

    domains: set[str] = set()
    if place.website_uri:
        host = _authorized_domain(place.website_uri, uri=True)
        if host:
            domains.add(host)
    for override in config.authority_domain_overrides:
        if override.place_id != place.place_id or need.value not in override.information_needs:
            continue
        for value in override.domains:
            host = _authorized_domain(value, uri=False)
            if host:
                domains.add(host)
    return canonicalize_allowed_domains(tuple(domains))


def _date_context(text: str, start: date, end: date) -> bool:
    if _has_any(text, DATE_SCOPE_PHRASES):
        return True
    for match in re.findall(r"\b\d{4} \d{2} \d{2}\b", text):
        try:
            if start <= date.fromisoformat(match.replace(" ", "-")) <= end:
                return True
        except ValueError:
            continue
    return False


def _specific_hours_sufficient(place: PlaceEvidence, start: date, end: date) -> bool:
    hours = place.opening_hours
    return bool(
        hours
        and hours.applicability == "date_specific_verified"
        and start == end
        and hours.next_open_time
        and hours.next_close_time
        and hours.next_open_time.date() == start
        and hours.next_close_time.date() == end
    )


def _status_gap_reason(place: PlaceEvidence, candidate: PlaceCandidate) -> WebTriggerReason | None:
    if (
        place.business_status is not None
        and candidate.business_status is not None
        and place.business_status != candidate.business_status
    ):
        return WebTriggerReason.RESIDUAL_CONFLICT
    if place.availability is not EvidenceAvailability.AVAILABLE:
        return WebTriggerReason.RESIDUAL_FAILED_OR_PARTIAL
    if place.business_status not in _KNOWN_STATUSES:
        return WebTriggerReason.RESIDUAL_MISSING
    return None


def _opening_date_conflict_affects_trip(
    latest_possible_openings: tuple[date | None, ...] | None, trip_start: date
) -> bool:
    """Ignore a date conflict only when every supported date is before the trip."""

    return latest_possible_openings is not None and (
        not latest_possible_openings
        or any(value is None or value >= trip_start for value in latest_possible_openings)
    )


def _task_id(
    place_id: str,
    need: OfficialInformationNeed,
    start: date,
    end: date,
    scope: SubjectScope,
    scope_text: str | None,
    facets: tuple[RequestedFacet, ...],
) -> str:
    canonical = "|".join(
        (
            place_id,
            need.value,
            start.isoformat(),
            end.isoformat(),
            scope.value,
            normalize_phrase(scope_text or ""),
            ",".join(item.value for item in facets),
        )
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20]


def _admission_facets(text: str, place_name: str) -> tuple[RequestedFacet, ...]:
    """Classify only explicit admission intent for a conservatively named place."""

    admission_context = _has_any(text, EXPLICIT_NEED_PHRASES["admission"])
    place_cost = _has_phrase(text, f"how much does {place_name} cost")
    if not admission_context and not place_cost:
        return ()
    facets: set[RequestedFacet] = set()
    ticket = _has_any(text, ("ticket", "tickets"))
    advance = (
        ticket
        and _has_any(text, ("in advance", "ahead of time"))
        and _has_any(text, ("buy", "purchase", "pay for"))
    )
    if advance:
        facets.add(RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT)
    elif ticket and _has_any(
        text,
        (
            "need a ticket",
            "need tickets",
            "ticket required",
            "tickets required",
            "without a ticket",
        ),
    ):
        facets.add(RequestedFacet.TICKET_REQUIREMENT)
    if place_cost or _has_any(text, ("how much", "price", "entry fee", "entrance fee")):
        facets.add(RequestedFacet.ADMISSION_FEE)
    elif _has_any(text, ("free admission", "free entry", "admission free")):
        facets.add(RequestedFacet.ADMISSION_FEE)
    if not facets and ticket and _has_any(text, EXPLICIT_NEED_PHRASES["reservation"]):
        return ()
    return canonical_facets(tuple(facets or {RequestedFacet.GENERAL_ADMISSION_POLICY}))


def _requested_scope(text: str) -> tuple[SubjectScope, str | None] | None:
    named = tuple(
        phrase
        for phrase in ("permanent exhibitions", "special exhibitions")
        if _has_phrase(text, phrase)
    )
    if len(named) > 1:
        return None
    if named:
        return SubjectScope.EXHIBITION, named[0]
    return SubjectScope.WHOLE_VENUE, None


def build_task_instruction(task: WebEvidenceTask) -> str:
    """Create one versioned, application-owned instruction for Luna."""

    scope = (
        f"{task.place_name} (place_id {task.place_id}) during "
        f"{task.applicable_start_date.isoformat()} through "
        f"{task.applicable_end_date.isoformat()}"
    )
    if task.requested_subject_scope is not SubjectScope.WHOLE_VENUE:
        scope += (
            f", specifically {task.requested_subject_scope.value} "
            f"{normalize_phrase(task.requested_scope_text or '')}"
        )
    if task.information_need is OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION:
        need = (
            "Find only official, date-applicable material operational notices: temporary or "
            "maintenance closure, reopening, special-date early closure, or special-date opening. "
            "Do not re-verify ordinary Places facts or ordinary opening hours."
        )
    else:
        need = {
            OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS: (
                "Find the current official operational status because structured status "
                "is incomplete."
            ),
            OfficialInformationNeed.SPECIAL_DATE_HOURS: (
                "Find official special or holiday opening hours for the requested dates only."
            ),
            OfficialInformationNeed.ADMISSION_TICKET: (
                "Find only official facts for these requested admission facets: "
                + ", ".join(
                    item.value
                    for item in (
                        task.requested_facets or (RequestedFacet.GENERAL_ADMISSION_POLICY,)
                    )
                )
                + ". Distinguish fee, ticket requirement, and advance purchase."
            ),
            OfficialInformationNeed.RESERVATION_REQUIREMENT: (
                "Find official booking or reservation requirements for this place only."
            ),
        }[task.information_need]
    return (
        f"Template {WEB_TASK_TEMPLATE_VERSION}. For {scope}: {need} "
        "Return only application-visible source URLs and directly exposed supporting snippets or "
        "results. If no acceptable notice or answer is found, report no result; absence of a "
        "result does not confirm that no closure or exception exists."
    )


def build_search_request(task: WebEvidenceTask) -> WebEvidenceSearchRequest:
    return WebEvidenceSearchRequest(
        task_id=task.task_id,
        place_id=task.place_id,
        place_name=task.place_name,
        information_need=task.information_need.value,
        requested_facets=tuple(item.value for item in task.requested_facets),
        requested_subject_scope=task.requested_subject_scope.value,
        requested_scope_text=task.requested_scope_text,
        applicable_start_date=task.applicable_start_date,
        applicable_end_date=task.applicable_end_date,
        allowed_domains=task.allowed_domains,
        task_instruction=build_task_instruction(task),
        template_version=WEB_TASK_TEMPLATE_VERSION,
    )


def plan_official_web_tasks(
    request: TravelRequest,
    requirements: TravelRequirements,
    shortlist: Sequence[PlaceCandidate],
    places: Sequence[PlaceEvidence],
    config: WebEvidenceConfig,
    *,
    named_place_ids: frozenset[str] | None = None,
    must_visit_place_ids: frozenset[str] | None = None,
    opening_date_conflicts: Mapping[str, tuple[date | None, ...]] | None = None,
) -> tuple[list[WebEvidenceTask], list[InformationGap], list[dict[str, object]]]:
    """Build all eligible tasks before any request-level budget truncation."""

    if requirements.start_date is None or requirements.end_date is None:
        raise ValueError("Complete trip dates are required for official Web tasks")
    start, end = requirements.start_date, requirements.end_date
    if len(shortlist) != len(places):
        raise ValueError("Shortlist and Place Evidence must have matching lengths")

    if (named_place_ids is None) != (must_visit_place_ids is None):
        raise ValueError("Explicit named and must-visit Place IDs must be supplied together")
    selected_ids = {candidate.place_id for candidate in shortlist}
    if named_place_ids is not None and (
        not named_place_ids <= selected_ids or not must_visit_place_ids <= named_place_ids
    ):
        raise ValueError("Explicit named and must-visit Place IDs must belong to the shortlist")
    if opening_date_conflicts is not None and not opening_date_conflicts.keys() <= selected_ids:
        raise ValueError("Opening-date conflicts must belong to the shortlist")

    sentences = _sentences(request.request_text)
    whole = normalize_phrase(request.request_text)
    named_ids = (
        named_place_ids
        if named_place_ids is not None
        else {candidate.place_id for candidate in shortlist if _has_phrase(whole, candidate.name)}
    )
    tasks: dict[
        tuple[str, OfficialInformationNeed, date, date, SubjectScope, str], WebEvidenceTask
    ] = {}
    gaps: list[InformationGap] = []
    assessments: list[dict[str, object]] = []

    def add_task(
        place: PlaceEvidence,
        need: OfficialInformationNeed,
        reason: WebTriggerReason,
        priority_group: int,
        index: int,
        *,
        gap: bool,
        facets: tuple[RequestedFacet, ...] = (),
        subject_scope: SubjectScope = SubjectScope.WHOLE_VENUE,
        scope_text: str | None = None,
        additional_reasons: tuple[WebTriggerReason, ...] = (),
    ) -> None:
        if gap:
            gaps.append(
                InformationGap(
                    place_id=place.place_id,
                    place_name=place.name,
                    information_need=need,
                    requested_facets=facets,
                    requested_subject_scope=subject_scope,
                    requested_scope_text=scope_text,
                    applicable_start_date=start,
                    applicable_end_date=end,
                    reason=reason,
                    source_refs=(place.source_ref,),
                )
            )
        key = (place.place_id, need, start, end, subject_scope, normalize_phrase(scope_text or ""))
        old = tasks.get(key)
        all_reasons = (
            (*old.trigger_reasons, reason, *additional_reasons)
            if old
            else (reason, *additional_reasons)
        )
        reasons = tuple(sorted(set(all_reasons)))
        merged_facets = canonical_facets((*old.requested_facets, *facets) if old else facets)
        task = WebEvidenceTask(
            task_id=_task_id(
                place.place_id, need, start, end, subject_scope, scope_text, merged_facets
            ),
            place_id=place.place_id,
            place_name=place.name,
            information_need=need,
            requested_facets=merged_facets,
            requested_subject_scope=subject_scope,
            requested_scope_text=scope_text,
            applicable_start_date=start,
            applicable_end_date=end,
            allowed_domains=authorized_domains(place, need, config),
            trigger_reasons=reasons,
            priority_group=min(priority_group, old.priority_group) if old else priority_group,
            shortlist_index=index,
        )
        tasks[key] = task
        assessments.append(
            {
                "place_id": place.place_id,
                "information_need": need.value,
                "requested_facets": [item.value for item in merged_facets],
                "requested_subject_scope": subject_scope.value,
                "requested_scope_text": scope_text,
                "decision": "merged" if old else "task_created",
                "reason": reason.value,
                "trigger_reasons": [item.value for item in reasons],
            }
        )

    for index, (candidate, place) in enumerate(zip(shortlist, places, strict=True)):
        if place.place_id != candidate.place_id:
            raise ValueError("Shortlist and Place Evidence IDs must align")
        name = normalize_phrase(candidate.name)
        named = candidate.place_id in named_ids
        target_sentences = [item for item in sentences if _has_phrase(item, name)]
        target_text = " ".join(target_sentences)
        required_text = " ".join(normalize_phrase(x) for x in requirements.required_activities)
        required = (
            candidate.place_id in must_visit_place_ids
            if must_visit_place_ids is not None
            else _has_phrase(required_text, name)
            or (named and any(_has_any(item, MUST_VISIT_PHRASES) for item in target_sentences))
        )
        targeted = named or required
        residual_group = 1 if required else 2
        risk_group = 3 if required else (4 if named else 5)
        before_place_tasks = len(tasks)

        status_reason = _status_gap_reason(place, candidate)
        structured_statuses = {candidate.business_status, place.business_status}
        date_risk_status = bool(structured_statuses & {"CLOSED_TEMPORARILY", "FUTURE_OPENING"})
        date_conflict = _opening_date_conflict_affects_trip(
            (opening_date_conflicts or {}).get(place.place_id), start
        )
        date_scoped = _date_context(target_text, start, end) if named else False
        closure = named and _has_any(target_text, EXPLICIT_NEED_PHRASES["date_closure"])
        current_status_intent = named and (
            _has_any(target_text, EXPLICIT_NEED_PHRASES["current_status"])
            or _has_named_current_status(target_text, name)
        )
        special = named and (
            _has_any(target_text, ("holiday hours", "special hours"))
            or (_has_any(target_text, ("open on", "hours on")) and date_scoped)
        )
        dated_operational_intent = bool(
            date_scoped and (closure or current_status_intent) and not special
        )
        specific_intent = dated_operational_intent or special
        if targeted and current_status_intent and status_reason is not None and not specific_intent:
            add_task(
                place,
                OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS,
                status_reason,
                residual_group,
                index,
                gap=True,
            )
        elif status_reason is not None and not specific_intent and not date_risk_status:
            add_task(
                place,
                OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS,
                status_reason,
                risk_group,
                index,
                gap=True,
            )
        else:
            assessments.append(
                {
                    "place_id": place.place_id,
                    "information_need": OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS.value,
                    "decision": (
                        "superseded_by_specific_need"
                        if specific_intent
                        else (
                            "sufficient" if status_reason is None else "date_risk_takes_precedence"
                        )
                    ),
                }
            )

        if named:
            # Specific date/trip-scoped intent wins over the overlapping generic "is it open".
            if dated_operational_intent:
                if not closure and _specific_hours_sufficient(place, start, end):
                    assessments.append(
                        {
                            "place_id": place.place_id,
                            "information_need": (
                                OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION.value
                            ),
                            "decision": "sufficient",
                        }
                    )
                else:
                    add_task(
                        place,
                        OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
                        WebTriggerReason.EXPLICIT_DATE_QUESTION,
                        residual_group,
                        index,
                        gap=True,
                    )
            elif special:
                if not _specific_hours_sufficient(place, start, end):
                    add_task(
                        place,
                        OfficialInformationNeed.SPECIAL_DATE_HOURS,
                        WebTriggerReason.EXPLICIT_DATE_QUESTION,
                        residual_group,
                        index,
                        gap=True,
                    )
                else:
                    assessments.append(
                        {
                            "place_id": place.place_id,
                            "information_need": OfficialInformationNeed.SPECIAL_DATE_HOURS.value,
                            "decision": "sufficient",
                        }
                    )
            elif current_status_intent:
                if status_reason is None:
                    assessments.append(
                        {
                            "place_id": place.place_id,
                            "information_need": (
                                OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS.value
                            ),
                            "decision": "sufficient",
                        }
                    )
            for sentence in target_sentences:
                facets = _admission_facets(sentence, name)
                if not facets:
                    continue
                requested_scope = _requested_scope(sentence)
                if requested_scope is None:
                    assessments.append(
                        {
                            "place_id": place.place_id,
                            "information_need": OfficialInformationNeed.ADMISSION_TICKET.value,
                            "decision": "ambiguous_requested_scope",
                        }
                    )
                    continue
                add_task(
                    place,
                    OfficialInformationNeed.ADMISSION_TICKET,
                    WebTriggerReason.EXPLICIT_USER_NEED,
                    residual_group,
                    index,
                    gap=True,
                    facets=facets,
                    subject_scope=requested_scope[0],
                    scope_text=requested_scope[1],
                )
            for sentence in target_sentences:
                if not _has_any(sentence, EXPLICIT_NEED_PHRASES["reservation"]):
                    continue
                requested_scope = _requested_scope(sentence)
                if requested_scope is None:
                    assessments.append(
                        {
                            "place_id": place.place_id,
                            "information_need": (
                                OfficialInformationNeed.RESERVATION_REQUIREMENT.value
                            ),
                            "decision": "ambiguous_requested_scope",
                        }
                    )
                    continue
                add_task(
                    place,
                    OfficialInformationNeed.RESERVATION_REQUIREMENT,
                    WebTriggerReason.EXPLICIT_USER_NEED,
                    residual_group,
                    index,
                    gap=True,
                    facets=(RequestedFacet.RESERVATION_REQUIREMENT,),
                    subject_scope=requested_scope[0],
                    scope_text=requested_scope[1],
                )

        if "CLOSED_TEMPORARILY" in structured_statuses:
            risk_reason = WebTriggerReason.CLOSED_TEMPORARILY
        elif "FUTURE_OPENING" in structured_statuses:
            risk_reason = WebTriggerReason.FUTURE_OPENING_UNCERTAIN
        else:
            risk_reason = None
        if risk_reason is not None:
            add_task(
                place,
                OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
                risk_reason,
                risk_group,
                index,
                gap=not dated_operational_intent,
                additional_reasons=(
                    (status_reason,) if status_reason is WebTriggerReason.RESIDUAL_CONFLICT else ()
                ),
            )
        if date_conflict:
            add_task(
                place,
                OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
                WebTriggerReason.OPENING_DATE_CONFLICT,
                risk_group,
                index,
                gap=not dated_operational_intent and risk_reason is None,
            )
        if len(tasks) == before_place_tasks:
            assessments.append(
                {
                    "place_id": place.place_id,
                    "information_need": (
                        OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION.value
                    ),
                    "decision": "no_task",
                    "reason": "no_decision_relevant_uncertainty",
                }
            )

    ordered = sorted(
        tasks.values(),
        key=lambda item: (
            item.priority_group,
            _NEED_ORDER[item.information_need],
            item.shortlist_index,
            item.place_id,
            item.requested_subject_scope.value,
            normalize_phrase(item.requested_scope_text or ""),
        ),
    )
    return ordered, gaps, assessments
