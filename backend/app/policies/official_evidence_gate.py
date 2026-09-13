"""Mechanical grounding and provenance validation for official Web claims."""

import hashlib
import re
import unicodedata
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit

from backend.app.evidence.models import PlaceEvidence
from backend.app.evidence.official_models import (
    EvidenceSourceBlock,
    OfficialClaimCandidate,
    OfficialClaimKind,
    OfficialCurrentEvidence,
    SourceKind,
    SubjectScope,
    TemporalBasis,
)
from backend.app.evidence.web_models import OfficialInformationNeed, WebEvidenceTask
from backend.app.integrations.web.models import WebSearchObservation
from backend.app.policies.official_temporal import (
    parse_official_amounts,
    parse_official_date_scope,
    parse_official_times,
)
from backend.app.policies.official_web import normalize_phrase
from backend.app.runtime.config_models import WebEvidenceConfig

_DATED_KINDS = {
    OfficialClaimKind.TEMPORARY_CLOSURE,
    OfficialClaimKind.MAINTENANCE_CLOSURE,
    OfficialClaimKind.REOPENING,
    OfficialClaimKind.SPECIAL_OPENING,
    OfficialClaimKind.EARLY_CLOSURE,
    OfficialClaimKind.SPECIAL_HOURS,
}
_HOURS_KINDS = {
    OfficialClaimKind.SPECIAL_HOURS,
    OfficialClaimKind.REGULAR_HOURS,
    OfficialClaimKind.EARLY_CLOSURE,
}
_NEED_KINDS = {
    OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS: {
        OfficialClaimKind.CURRENT_OPEN,
        OfficialClaimKind.CURRENT_CLOSED,
    },
    OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION: _DATED_KINDS
    - {OfficialClaimKind.SPECIAL_HOURS},
    OfficialInformationNeed.SPECIAL_DATE_HOURS: {
        OfficialClaimKind.SPECIAL_HOURS,
        OfficialClaimKind.REGULAR_HOURS,
        OfficialClaimKind.EARLY_CLOSURE,
    },
    OfficialInformationNeed.ADMISSION_TICKET: {
        OfficialClaimKind.FREE_GENERAL_ADMISSION,
        OfficialClaimKind.PAID_ADMISSION,
        OfficialClaimKind.TICKET_REQUIRED,
        OfficialClaimKind.TICKET_NOT_REQUIRED,
        OfficialClaimKind.ADVANCE_TICKET_PURCHASE_REQUIRED,
        OfficialClaimKind.ADVANCE_TICKET_PURCHASE_NOT_REQUIRED,
    },
    OfficialInformationNeed.RESERVATION_REQUIREMENT: {
        OfficialClaimKind.RESERVATION_REQUIRED,
        OfficialClaimKind.RESERVATION_NOT_REQUIRED,
    },
}


def _compact(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _host(url: str) -> str | None:
    try:
        parts = urlsplit(url)
        if parts.scheme.casefold() != "https" or parts.username or parts.password:
            return None
        if parts.port not in (None, 443):
            return None
        return (parts.hostname or "").rstrip(".").encode("idna").decode("ascii").casefold()
    except (UnicodeError, ValueError):
        return None


def _in_domain(host: str | None, domain: str) -> bool:
    return bool(host and (host == domain or host.endswith(f".{domain}")))


def _authority_basis(
    source_url: str,
    place: PlaceEvidence,
    need: OfficialInformationNeed,
    config: WebEvidenceConfig,
) -> str | None:
    host = _host(source_url)
    website = _host(place.website_uri) if place.website_uri else None
    if website and _in_domain(host, website):
        return "places_first_party_website"
    for override in config.authority_domain_overrides:
        if override.place_id != place.place_id or need.value not in override.information_needs:
            continue
        if any(_in_domain(host, domain.casefold()) for domain in override.domains):
            return "configured_place_need_domain"
    return None


def _subject_bound(candidate: OfficialClaimCandidate, place_name: str) -> bool:
    """Require a visible venue anchor without a fixed predicate vocabulary."""

    subject = candidate.subject_text
    predicate = candidate.predicate_text
    if not subject or not predicate or candidate.subject_scope is SubjectScope.UNKNOWN:
        return False
    excerpt = candidate.supporting_excerpt
    subject_at = excerpt.find(subject)
    predicate_at = excerpt.find(predicate)
    if subject_at < 0 or predicate_at < subject_at + len(subject):
        return False
    bridge = excerpt[subject_at + len(subject) : predicate_at]
    if len(bridge) > 250 or any(mark in bridge for mark in ".!?;"):
        return False
    normalized_subject = normalize_phrase(subject)
    normalized_place = normalize_phrase(place_name)
    if normalized_subject.startswith("the "):
        normalized_subject = normalized_subject[4:]
    if candidate.subject_scope is SubjectScope.WHOLE_VENUE:
        if normalized_subject != normalized_place:
            return False
        # Do not allow a venue-name prefix to stand for a named sub-entity.
        if "\n" not in bridge and re.match(r"\s+[A-Z][a-z]+\b", bridge):
            return False
    else:
        if normalized_place not in normalized_subject and normalized_place not in normalize_phrase(
            candidate.scope_text or ""
        ):
            return False
        if not candidate.scope_text:
            return False
    return True


def _page_subject_bound(
    candidate: OfficialClaimCandidate,
    source: EvidenceSourceBlock,
    task: WebEvidenceTask,
    authority_basis: str,
) -> tuple[bool, str | None]:
    """Use a first-party page title and one primary-body section as source anchors."""

    if (
        authority_basis != "places_first_party_website"
        or source.source_kind is not SourceKind.FETCHED_HTML
        or not source.page_title
        or source.page_title not in source.text
    ):
        return False, None
    place = normalize_phrase(task.place_name)
    title = normalize_phrase(source.page_title)
    if f" {place} " not in f" {title} ":
        return False, None
    subject = normalize_phrase(candidate.subject_text or "")
    if not subject or not candidate.predicate_text:
        return False, None
    if candidate.subject_scope is SubjectScope.WHOLE_VENUE:
        if candidate.scope_text is not None:
            return False, None
    elif not candidate.scope_text or candidate.scope_text not in candidate.supporting_excerpt:
        return False, None
    for content in source.content_blocks:
        if (
            not content.section_headings
            or any(heading not in source.text for heading in content.section_headings)
            or any(
                span is not None and span not in content.text
                for span in (
                    candidate.subject_text,
                    candidate.predicate_text,
                    candidate.value_text,
                    candidate.scope_text,
                )
            )
        ):
            continue
        local_heading = normalize_phrase(content.section_headings[-1])
        local_scope = normalize_phrase(candidate.scope_text or "")
        if subject in {local_heading, local_scope}:
            return True, None
        if (
            candidate.subject_scope is task.requested_subject_scope
            and task.requested_scope_text
            and subject == normalize_phrase(task.requested_scope_text)
        ):
            # The model supplied a source-visible local subject and a secondary qualifier.
            # Keep the subject span as the canonical scope used by the Resolver.
            return True, candidate.subject_text
    return False, None


def _narrow_contradiction(candidate: OfficialClaimCandidate) -> bool:
    """Reject only direct mechanical inversions within the cited predicate."""

    predicate = _compact(candidate.predicate_text or "")
    if candidate.claim_kind in {
        OfficialClaimKind.RESERVATION_REQUIRED,
        OfficialClaimKind.TICKET_REQUIRED,
    }:
        if re.search(r"\bnot required\b", predicate):
            return True
        if re.search(r"\boptional\b", predicate) and not re.search(r"\bnot optional\b", predicate):
            return True
    if candidate.claim_kind is OfficialClaimKind.CURRENT_OPEN and "not open" in predicate:
        return True
    return candidate.claim_kind is OfficialClaimKind.CURRENT_CLOSED and "not closed" in predicate


def accept_official_candidate(
    candidate: OfficialClaimCandidate,
    *,
    task: WebEvidenceTask,
    observation: WebSearchObservation,
    sources: tuple[EvidenceSourceBlock, ...],
    place: PlaceEvidence,
    config: WebEvidenceConfig,
    retrieved_at: datetime | None = None,
) -> tuple[OfficialCurrentEvidence | None, str]:
    """Accept a semantic proposal only when its cited source and fields are grounded."""

    if candidate.place_id != task.place_id or place.place_id != task.place_id:
        return None, "place_id_mismatch"
    if normalize_phrase(candidate.place_name) != normalize_phrase(task.place_name):
        return None, "place_name_mismatch"
    if candidate.information_need is not task.information_need:
        return None, "information_need_mismatch"
    if candidate.claim_kind not in _NEED_KINDS[task.information_need]:
        return None, "claim_kind_mismatch"
    observed_urls = {hit.url for hit in observation.hits if hit.allowed_domain}
    if candidate.source_url not in observed_urls:
        return None, "unobserved_source_url"
    block = next(
        (
            item
            for item in sources
            if item.task_id == task.task_id
            and item.source_key == candidate.source_key
            and item.source_url == candidate.source_url
            and item.source_kind is candidate.source_kind
            and item.final_url == candidate.final_url
            and candidate.supporting_excerpt in item.text
        ),
        None,
    )
    if block is None:
        return None, "supporting_excerpt_not_in_source"
    for url in (candidate.source_url, block.final_url, *block.redirect_chain):
        if url is None:
            continue
        host = _host(url)
        if not any(_in_domain(host, domain) for domain in task.allowed_domains):
            return None, "unauthorized_source_or_redirect"
    if candidate.source_kind is SourceKind.FETCHED_HTML:
        if (
            not block.final_url
            or not block.body_sha256
            or (not block.redirect_chain and block.final_url != block.source_url)
        ):
            return None, "unverified_page_binding"
    elif candidate.final_url is not None:
        return None, "native_source_has_final_url"
    basis = _authority_basis(
        block.final_url or block.source_url, place, task.information_need, config
    )
    if basis is None:
        return None, "authority_not_bound_to_place"
    excerpt = candidate.supporting_excerpt
    spans = (
        candidate.subject_text,
        candidate.predicate_text,
        candidate.value_text,
        candidate.scope_text,
        candidate.date_text,
        candidate.time_text,
        candidate.schedule_text,
        candidate.amount_text,
        candidate.updated_at_text,
    )
    if any(span is not None and span not in excerpt for span in spans):
        return None, "source_span_not_in_excerpt"
    local_bound = _subject_bound(candidate, task.place_name)
    page_bound, page_scope_text = (
        (False, None) if local_bound else _page_subject_bound(candidate, block, task, basis)
    )
    if not (local_bound or page_bound):
        return None, "subject_scope_not_bound"
    if _narrow_contradiction(candidate):
        return None, "direct_predicate_contradiction"

    if candidate.claim_kind not in _HOURS_KINDS and (
        candidate.opens_at is not None
        or candidate.closes_at is not None
        or candidate.time_text is not None
        or candidate.schedule_scope is not None
        or candidate.schedule_text is not None
    ):
        return None, "unsupported_time_field"
    if (candidate.schedule_scope is None) != (candidate.schedule_text is None):
        return None, "incomplete_schedule_scope"
    if candidate.claim_kind in {
        OfficialClaimKind.REGULAR_HOURS,
        OfficialClaimKind.SPECIAL_HOURS,
    } and (candidate.opens_at is None or candidate.closes_at is None):
        return None, "incomplete_hours"
    if candidate.claim_kind is OfficialClaimKind.EARLY_CLOSURE and candidate.closes_at is None:
        return None, "incomplete_hours"
    if candidate.opens_at is not None or candidate.closes_at is not None:
        if not candidate.time_text:
            return None, "time_not_explicit"
        supported_times = parse_official_times(candidate.time_text)
        if any(
            value not in supported_times
            for value in (candidate.opens_at, candidate.closes_at)
            if value
        ):
            return None, "time_not_directly_supported"
    if candidate.claim_kind is not OfficialClaimKind.PAID_ADMISSION and any(
        value is not None for value in (candidate.amount, candidate.currency, candidate.amount_text)
    ):
        return None, "unsupported_price_field"
    if candidate.amount is not None or candidate.currency is not None:
        if not candidate.amount_text or candidate.amount is None:
            return None, "amount_not_explicit"
        try:
            amount = Decimal(candidate.amount)
        except InvalidOperation:
            return None, "invalid_amount"
        if amount not in parse_official_amounts(candidate.amount_text):
            return None, "amount_not_directly_supported"
        if candidate.currency is not None and _compact(candidate.currency) not in _compact(
            candidate.amount_text
        ):
            return None, "currency_not_directly_supported"
    elif candidate.amount_text is not None:
        return None, "orphan_amount_text"

    start, end = candidate.applicable_start_date, candidate.applicable_end_date
    if (start is None) != (end is None):
        return None, "incomplete_date_range"
    if (
        start
        and end
        and (start > end or end < task.applicable_start_date or start > task.applicable_end_date)
    ):
        return None, "date_outside_task"
    if candidate.temporal_basis is TemporalBasis.EXPLICIT_DATE_OR_RANGE:
        if not candidate.date_text or start is None or end is None:
            return None, "date_not_explicit"
        if parse_official_date_scope(candidate.date_text) != (start, end):
            return None, "date_not_directly_supported"
    elif candidate.date_text is not None or start is not None or end is not None:
        return None, "unsupported_date_scope"
    if (
        candidate.claim_kind in _DATED_KINDS
        and candidate.temporal_basis is not TemporalBasis.EXPLICIT_DATE_OR_RANGE
    ):
        return None, "date_not_explicit"
    if candidate.claim_kind in {
        OfficialClaimKind.CURRENT_OPEN,
        OfficialClaimKind.CURRENT_CLOSED,
    } and (
        candidate.temporal_basis
        not in {TemporalBasis.CURRENT_POINT_STATUS, TemporalBasis.EXPLICIT_DATE_OR_RANGE}
    ):
        return None, "invalid_point_status_basis"
    if candidate.claim_kind is OfficialClaimKind.REGULAR_HOURS and (
        candidate.temporal_basis is not TemporalBasis.CURRENT_GENERAL_POLICY
    ):
        return None, "invalid_regular_hours_basis"
    if candidate.updated_at is not None:
        if not candidate.updated_at_text:
            return None, "unsupported_updated_at"
        date_part = re.sub(r"^(?:updated|published)\s+", "", candidate.updated_at_text, flags=re.I)
        if date_part == candidate.updated_at_text or parse_official_date_scope(date_part) != (
            candidate.updated_at,
            candidate.updated_at,
        ):
            return None, "unsupported_updated_at"
    elif candidate.updated_at_text is not None:
        return None, "orphan_updated_at_text"
    source_ref = (
        "official_web:"
        + hashlib.sha256(
            "\x1f".join(
                (
                    candidate.place_id,
                    candidate.information_need.value,
                    candidate.source_key or "",
                    candidate.source_url,
                    candidate.source_kind.value,
                    candidate.claim_kind.value,
                    candidate.temporal_basis.value,
                    candidate.subject_scope.value,
                    page_scope_text or candidate.scope_text or "",
                    candidate.value_text,
                    str(start),
                    str(end),
                )
            ).encode("utf-8")
        ).hexdigest()[:20]
    )
    accepted_data = candidate.model_dump()
    if page_scope_text is not None:
        accepted_data["scope_text"] = page_scope_text
    accepted = OfficialCurrentEvidence(
        **accepted_data,
        authority_basis=basis,
        retrieved_at=retrieved_at or datetime.now(UTC),
        source_ref=source_ref,
    )
    return accepted, "accepted"
