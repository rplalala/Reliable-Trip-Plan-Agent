"""Deterministic V1-A acquisition, normalization, budgeting, and deduplication."""

import math
from collections import defaultdict
from collections.abc import Awaitable, Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import TYPE_CHECKING, Literal, TypeVar
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from backend.app.evidence.models import (
    DestinationContext,
    EvidenceAvailability,
    NonWalkablePairEvidence,
    PlaceCandidate,
    PlaceEvidence,
    RouteElementEvidence,
    RouteElementEvidenceType,
    RouteEvidence,
    RouteEvidenceBundle,
    RouteEvidencePurpose,
    WeatherEvidence,
)
from backend.app.evidence.normalization import (
    merge_baseline_route_chunks,
    normalize_place_details,
    normalize_routes,
    normalize_weather,
    unavailable_place_details,
    unavailable_routes,
    unavailable_weather,
)
from backend.app.evidence.selection_models import (
    PlaceSearchIntent,
    PlaceSelectionInput,
    RatingAcquisitionState,
    SearchIntentKind,
)
from backend.app.evidence.selection_normalization import (
    normalize_place_details_for_selection,
    normalize_place_search_hit,
)
from backend.app.integrations.google.places import (
    PLACES_CANDIDATE_FIELD_MASK,
    PLACES_DESTINATION_FIELD_MASK,
    PLACES_DETAILS_FIELD_MASK,
)
from backend.app.integrations.google.routes import ROUTE_MATRIX_FIELD_MASK
from backend.app.integrations.models import (
    LatLng,
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceReviewsRequest,
    PlaceSearchRequest,
    PlaceSearchResponse,
    RouteMatrixDTO,
    RouteMatrixRequest,
    RouteWaypoint,
    WeatherForecastDTO,
    WeatherRequest,
)
from backend.app.integrations.protocols import PlacesProvider, RoutesProvider, WeatherProvider
from backend.app.llm.client import StructuredLLMClient
from backend.app.observability.run_trace import RunTracer, TracePayloadMode
from backend.app.policies.poi_capacity import (
    EffectivePOICapacities,
    apply_poi_operating_budgets,
    derive_poi_capacities,
)
from backend.app.policies.poi_funnel import (
    MergedSearchObservations,
    NamedPlaceResolution,
    NamedPlaceResolutionStatus,
    build_place_search_intents,
    merge_search_observations,
    normalize_exact_name,
    opening_dates_compatible,
    resolve_named_place_intents,
)
from backend.app.policies.poi_selection import (
    POISelectionResult,
    SelectionConflict,
    evaluate_poi_eligibility,
    select_pois,
)
from backend.app.policies.route_matrix_chunking import partition_baseline_origins
from backend.app.policies.transport import (
    MAX_WALK_DISTANCE_METERS,
    MAX_WALK_DURATION_SECONDS,
    DirectedWalkTrigger,
    TransportModeDecision,
    TravelMode,
    collapse_non_walkable_pairs,
    find_directed_non_walkable_pairs,
    select_alternative_route_pairs,
)
from backend.app.policies.trip_dates import TRIP_DATE_WINDOW_DAYS, TripDateWindow
from backend.app.runtime.budget import ToolBudget, ToolBudgetExceededError, ToolBudgetKey
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent
from backend.app.schemas.request import TravelRequirements

ValueT = TypeVar("ValueT")

if TYPE_CHECKING:
    from backend.app.services.review_selection import ReviewAwareSelectionResult


class NoViableCandidatesError(RuntimeError):
    """External acquisition could not produce a usable destination or POI pool."""


class PlaceSearchUnavailableError(RuntimeError):
    def __init__(self, error_type: str | None, *, cache_hit: bool) -> None:
        self.cache_hit = cache_hit
        super().__init__(f"Places provider unavailable ({error_type})")


@dataclass(frozen=True)
class _ProviderResult[ValueT]:
    value: ValueT | None = None
    error_type: str | None = None


@dataclass(frozen=True)
class SearchIntentExecution:
    intent_id: str
    status: Literal["provider_success", "provider_failed", "budget_not_attempted"]
    cache_hit: bool = False


@dataclass(frozen=True)
class CandidateFunnelResult:
    """Inspectable no-review V1-A baseline; Phase 4 may refine it with reviews."""

    capacities: EffectivePOICapacities
    search_intents: tuple[PlaceSearchIntent, ...]
    named_place_resolutions: tuple[NamedPlaceResolution, ...]
    observations: tuple[PlaceSelectionInput, ...]
    merged: MergedSearchObservations
    c_raw_selection: POISelectionResult
    c_raw_candidates: tuple[PlaceSelectionInput, ...]
    r_pool_selection: POISelectionResult
    rating_contenders: tuple[str, ...]
    enriched_candidates: tuple[PlaceSelectionInput, ...]
    details_failures: tuple[tuple[str, str], ...]
    no_review_selection: POISelectionResult
    conflicts: tuple[SelectionConflict, ...]
    must_visit_place_ids: frozenset[str]
    excluded_place_ids: frozenset[str]
    unresolved_required_names: tuple[str, ...]
    search_executions: tuple[SearchIntentExecution, ...] = ()
    finality: Literal["pending_review_enrichment"] = "pending_review_enrichment"


class V1EvidenceAcquisitionService:
    """Application-controlled external evidence pipeline for one V1 run."""

    def __init__(
        self,
        *,
        places_provider: PlacesProvider,
        weather_provider: WeatherProvider,
        routes_provider: RoutesProvider,
        budget: ToolBudget,
        cache: RequestCache,
        tracer: RunTracer,
    ) -> None:
        self._places = places_provider
        self._weather = weather_provider
        self._routes = routes_provider
        self._budget = budget
        self._cache = cache
        self._tracer = tracer
        self._counted_candidate_ids: set[str] = set()

    async def _cached_provider_call_with_status(
        self,
        *,
        key: tuple[object, ...],
        budget_key: ToolBudgetKey | None,
        budget_amount: int,
        additional_budget_charges: tuple[tuple[ToolBudgetKey, int], ...] = (),
        factory: Callable[[], Awaitable[ValueT]],
    ) -> tuple[_ProviderResult[ValueT], bool]:
        async def load() -> _ProviderResult[ValueT]:
            charges = additional_budget_charges
            if budget_key is not None:
                charges = ((budget_key, budget_amount), *charges)
            self._budget.consume_many(charges)
            try:
                return _ProviderResult(value=await factory())
            except Exception as exc:
                return _ProviderResult(error_type=type(exc).__name__)

        result, cache_hit = await self._cache.get_or_create(key, load)
        operation = str(key[0])
        self._tracer.event(
            "request_cache_lookup",
            {
                "operation": operation,
                "cache_hit": cache_hit,
                "outcome": "success" if result.value is not None else "unavailable",
                "error_type": result.error_type,
                "requested_elements": len(key[1]) * len(key[2])
                if operation == "route_matrix"
                else None,
            },
        )
        return result, cache_hit

    async def _cached_provider_call(
        self,
        *,
        key: tuple[object, ...],
        budget_key: ToolBudgetKey | None,
        budget_amount: int,
        additional_budget_charges: tuple[tuple[ToolBudgetKey, int], ...] = (),
        factory: Callable[[], Awaitable[ValueT]],
    ) -> _ProviderResult[ValueT]:
        result, _ = await self._cached_provider_call_with_status(
            key=key,
            budget_key=budget_key,
            budget_amount=budget_amount,
            additional_budget_charges=additional_budget_charges,
            factory=factory,
        )
        return result

    async def _search_places(
        self, request: PlaceSearchRequest, *, budget_key: ToolBudgetKey
    ) -> tuple[PlaceSearchResponse, bool]:
        key = (
            "places_search",
            request.text_query.casefold(),
            request.page_size,
            request.field_mask,
            request.include_future_opening_businesses,
            (
                request.location_bias.latitude,
                request.location_bias.longitude,
            )
            if request.location_bias is not None
            else None,
            request.language_code,
        )
        result, cache_hit = await self._cached_provider_call_with_status(
            key=key,
            budget_key=budget_key,
            budget_amount=1,
            factory=lambda: self._places.search_text(request),
        )
        if result.value is None:
            raise PlaceSearchUnavailableError(result.error_type, cache_hit=cache_hit)
        return result.value, cache_hit

    async def resolve_destination(self, destination: str) -> DestinationContext:
        """Resolve one destination coordinate using the same minimal candidate mask."""

        try:
            response, _ = await self._search_places(
                PlaceSearchRequest(
                    text_query=destination,
                    page_size=1,
                    field_mask=PLACES_DESTINATION_FIELD_MASK,
                ),
                budget_key=ToolBudgetKey.DESTINATION_SEARCH_CALLS,
            )
        except RuntimeError as exc:
            raise NoViableCandidatesError("Destination provider was unavailable") from exc
        if not response.candidates:
            raise NoViableCandidatesError("Destination could not be resolved")
        candidate = response.candidates[0]
        return DestinationContext(
            place_id=candidate.place_id,
            name=candidate.display_name,
            formatted_address=candidate.formatted_address,
            latitude=candidate.location.latitude,
            longitude=candidate.location.longitude,
        )

    def _candidate_queries(self, requirements: TravelRequirements) -> list[tuple[str, str]]:
        max_queries = 3
        return [
            (f"category_{index + 1}", intent.query)
            for index, intent in enumerate(
                build_place_search_intents(requirements, max_queries=max_queries)
            )
        ]

    async def search_candidate_observations(
        self,
        requirements: TravelRequirements,
        destination: DestinationContext,
        *,
        candidate_limit: int | None = None,
        intents: Sequence[PlaceSearchIntent] | None = None,
        failed_intent_ids: set[str] | None = None,
        intent_executions: list[SearchIntentExecution] | None = None,
    ) -> list[PlaceSelectionInput]:
        """Preserve each valid search hit before later merging or selection."""

        queries = (
            [(intent.intent_id, intent.query, intent.kind) for intent in intents]
            if intents is not None
            else [
                (category, query, SearchIntentKind.FALLBACK)
                for category, query in self._candidate_queries(requirements)
            ]
        )
        if not queries:
            raise NoViableCandidatesError("No candidate search budget remains")
        if candidate_limit is not None and not (
            1 <= candidate_limit <= self._budget.limits.max_candidates
        ):
            raise ValueError("candidate_limit must stay within the configured candidate budget")
        effective_limit = (
            candidate_limit if candidate_limit is not None else self._budget.limits.max_candidates
        )
        page_size = (
            20 if intents is not None else min(20, math.ceil(effective_limit / len(queries)))
        )
        observations: list[PlaceSelectionInput] = []
        for category, query, kind in queries:
            request = PlaceSearchRequest(
                text_query=query,
                page_size=page_size,
                field_mask=PLACES_CANDIDATE_FIELD_MASK,
                include_future_opening_businesses=True,
                location_bias=LatLng(
                    latitude=destination.latitude,
                    longitude=destination.longitude,
                ),
            )
            try:
                response, cache_hit = await self._search_places(
                    request, budget_key=ToolBudgetKey.CANDIDATE_SEARCH_CALLS
                )
            except ToolBudgetExceededError:
                execution = SearchIntentExecution(category, "budget_not_attempted")
                if intent_executions is not None:
                    intent_executions.append(execution)
                self._tracer.event(
                    "candidate_search_intent_completed",
                    {"intent_id": category, "status": execution.status, "cache_hit": False},
                )
                continue
            except PlaceSearchUnavailableError as exc:
                if failed_intent_ids is not None:
                    failed_intent_ids.add(category)
                self._tracer.event(
                    "places_search_failed",
                    {"category": category, "error": type(exc).__name__},
                )
                execution = SearchIntentExecution(category, "provider_failed", exc.cache_hit)
                if intent_executions is not None:
                    intent_executions.append(execution)
                self._tracer.event(
                    "candidate_search_intent_completed",
                    {"intent_id": category, "status": execution.status, "cache_hit": exc.cache_hit},
                )
                continue
            execution = SearchIntentExecution(category, "provider_success", cache_hit)
            if intent_executions is not None:
                intent_executions.append(execution)
            self._tracer.event(
                "candidate_search_intent_completed",
                {
                    "intent_id": category,
                    "status": execution.status,
                    "cache_hit": cache_hit,
                    "observation_count": len(response.candidates),
                },
            )
            observations.extend(
                normalize_place_search_hit(
                    item,
                    intent_id=category,
                    source_query=query,
                    actual_result_count=response.actual_result_count,
                    intent_kind=kind,
                )
                for item in response.candidates
            )
        return observations

    async def search_candidates(
        self,
        requirements: TravelRequirements,
        destination: DestinationContext,
    ) -> list[PlaceCandidate]:
        """Preserve the historical shortlist input until the later funnel phase."""

        deduplicated: list[PlaceCandidate] = []
        seen: set[str] = set()
        # Preserve the original 20-candidate V1-A graph until the funnel switch.
        legacy_limit = min(20, self._budget.limits.max_candidates)
        if requirements.end_date is None:
            raise ValueError("Complete trip dates are required for candidate eligibility")
        for observation in await self.search_candidate_observations(
            requirements, destination, candidate_limit=legacy_limit
        ):
            candidate = observation.candidate
            if (
                candidate.place_id in seen
                or not evaluate_poi_eligibility(
                    observation,
                    trip_end=requirements.end_date,
                    require_details=False,
                ).eligible
            ):
                continue
            seen.add(candidate.place_id)
            deduplicated.append(candidate)
            if len(deduplicated) == legacy_limit:
                break
        if not deduplicated:
            raise NoViableCandidatesError("No viable Places candidates were found")
        self._consume_new_candidates(item.place_id for item in deduplicated)
        return deduplicated

    def _consume_new_candidates(self, place_ids: Iterable[str]) -> None:
        identifiers = set(place_ids)
        new_ids = identifiers - self._counted_candidate_ids
        self._budget.consume(ToolBudgetKey.CANDIDATES, len(new_ids))
        self._counted_candidate_ids.update(new_ids)

    def shortlist(self, candidates: list[PlaceCandidate]) -> list[PlaceCandidate]:
        """Transitional graph-only shortlist; the new funnel uses select_pois."""

        route_limit = math.isqrt(self._budget.limits.max_route_matrix_elements)
        limit = min(8, self._budget.limits.max_place_detail_calls, route_limit)
        groups: dict[str, list[PlaceCandidate]] = defaultdict(list)
        category_order: list[str] = []
        for candidate in candidates:
            if candidate.category not in groups:
                category_order.append(candidate.category)
            groups[candidate.category].append(candidate)
        for values in groups.values():
            values.sort(key=lambda item: (item.provider_rank, item.place_id))

        shortlist: list[PlaceCandidate] = []
        offset = 0
        while len(shortlist) < limit:
            added = False
            for category in category_order:
                values = groups[category]
                if offset < len(values):
                    shortlist.append(values[offset])
                    added = True
                    if len(shortlist) == limit:
                        break
            if not added:
                break
            offset += 1
        if not shortlist:
            raise NoViableCandidatesError("No viable candidates remained after shortlisting")
        return shortlist

    async def enrich_places(self, shortlist: list[PlaceCandidate]) -> list[PlaceEvidence]:
        """Transitional graph-only details projection using the shared cached call."""

        evidence: list[PlaceEvidence] = []
        for candidate in shortlist:
            request = PlaceDetailsRequest(
                place_id=candidate.place_id,
                field_mask=PLACES_DETAILS_FIELD_MASK,
            )
            result = await self._get_place_details(request)
            if result.value is None:
                item = unavailable_place_details(
                    candidate,
                    f"Place Details unavailable ({result.error_type})",
                )
            else:
                item = normalize_place_details(result.value, candidate=candidate)
            evidence.append(item)
        self._tracer.payload(
            "evidence",
            "place_evidence",
            evidence,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return evidence

    async def _get_place_details(
        self, request: PlaceDetailsRequest
    ) -> _ProviderResult[PlaceDetailsDTO]:
        return await self._cached_provider_call(
            key=self._place_details_cache_key(request),
            budget_key=ToolBudgetKey.PLACE_DETAIL_CALLS,
            budget_amount=1,
            factory=lambda: self._places.get_place_details(request),
        )

    async def run_candidate_funnel(
        self,
        *,
        requirements: TravelRequirements,
        destination: DestinationContext,
        window: TripDateWindow,
        named_place_intents: Sequence[NamedPlaceIntent] = (),
        excluded_place_ids: frozenset[str] = frozenset(),
    ) -> CandidateFunnelResult:
        """Build the structured/rating funnel before review-aware final selection."""

        if requirements.start_date is None or requirements.end_date is None:
            raise ValueError("Complete trip dates are required for the candidate funnel")
        capacities = apply_poi_operating_budgets(
            derive_poi_capacities(requirements.start_date, requirements.end_date, window),
            self._budget.limits,
        )
        intents = build_place_search_intents(
            requirements,
            named_place_intents=named_place_intents,
        )
        self._tracer.event(
            "candidate_search_intents_generated",
            {
                "deduplicated_count": len(intents),
                "intents": [
                    {
                        "intent_id": intent.intent_id,
                        "term": intent.term,
                        "kind": intent.kind.value,
                        "weight": str(intent.weight),
                    }
                    for intent in intents
                ],
            },
        )
        self._tracer.event(
            "named_place_search_intents_created",
            {
                "intents": [
                    {
                        "intent_id": intent.intent_id,
                        "place_text": named.place_text,
                        "inclusion": named.inclusion.value,
                        "source_text": named.source_text,
                        "additional_source_texts": named.additional_source_texts,
                        "query": intent.query,
                        "weight": str(intent.weight),
                    }
                    for intent in intents
                    if (named := intent.named_place_intent) is not None
                ]
            },
        )
        failed_intent_ids: set[str] = set()
        intent_executions: list[SearchIntentExecution] = []
        observations = await self.search_candidate_observations(
            requirements,
            destination,
            candidate_limit=capacities.c_raw,
            intents=intents,
            failed_intent_ids=failed_intent_ids,
            intent_executions=intent_executions,
        )
        merged = merge_search_observations(observations)
        self._tracer.event(
            "candidate_search_observations_recorded",
            {
                "observations": [
                    {
                        "place_id": item.candidate.place_id,
                        "place_name": item.candidate.name,
                        "intent_id": hit.intent_id,
                        "provider_rank": hit.provider_rank,
                        "raw_result_count": hit.actual_result_count,
                    }
                    for item in observations
                    for hit in item.query_hits
                ]
            },
        )
        if not merged.places and not any(
            item.inclusion is NamedPlaceInclusion.REQUIRED for item in named_place_intents
        ):
            raise NoViableCandidatesError("No usable Places candidates were found")
        resolutions = resolve_named_place_intents(
            named_place_intents,
            intents,
            merged.places,
            failed_search_intent_ids=frozenset(failed_intent_ids),
            budget_not_attempted_intent_ids=frozenset(
                item.intent_id
                for item in intent_executions
                if item.status == "budget_not_attempted"
            ),
        )
        must_visit_ids = frozenset(
            item.resolved_place_id
            for item in resolutions
            if item.named_place_intent.inclusion is NamedPlaceInclusion.REQUIRED
            and item.resolved_place_id is not None
        )
        unresolved_names = tuple(
            item.named_place_intent.place_text
            for item in resolutions
            if item.named_place_intent.inclusion is NamedPlaceInclusion.REQUIRED
            and item.status is not NamedPlaceResolutionStatus.RESOLVED
        )
        self._tracer.event(
            "named_place_identities_reconciled",
            {
                "resolutions": [
                    {
                        "place_text": item.named_place_intent.place_text,
                        "source_text": item.named_place_intent.source_text,
                        "inclusion": item.named_place_intent.inclusion.value,
                        "search_intent_id": item.search_intent_id,
                        "outcome": item.status.value,
                        "matching_place_ids": item.matching_place_ids,
                        "resolved_place_id": item.resolved_place_id,
                        "must_visit": item.resolved_place_id in must_visit_ids
                        if item.resolved_place_id is not None
                        else False,
                    }
                    for item in resolutions
                ]
            },
        )
        # Only exact displayed-name exclusions are inferred; categories need a
        # separately approved controlled type mapping, never substring matching.
        excluded_names = {normalize_exact_name(name) for name in requirements.excluded_activities}
        resolved_exclusions = excluded_place_ids.union(
            place.candidate.place_id
            for place in merged.places
            if normalize_exact_name(place.candidate.name) in excluded_names
        )
        c_raw_selection = select_pois(
            merged.places,
            start_date=requirements.start_date,
            end_date=requirements.end_date,
            window=window,
            capacity=capacities.c_raw,
            must_visit_place_ids=must_visit_ids,
            excluded_place_ids=frozenset(resolved_exclusions),
            unresolved_required_names=unresolved_names,
            require_details=False,
        )
        merged_by_id = {item.candidate.place_id: item for item in merged.places}
        c_raw_candidates = tuple(
            merged_by_id[place_id] for place_id in c_raw_selection.selected_place_ids
        )
        self._consume_new_candidates(item.candidate.place_id for item in c_raw_candidates)
        r_pool_selection = select_pois(
            c_raw_candidates,
            start_date=requirements.start_date,
            end_date=requirements.end_date,
            window=window,
            capacity=capacities.r_pool,
            must_visit_place_ids=must_visit_ids,
            excluded_place_ids=frozenset(resolved_exclusions),
            unresolved_required_names=unresolved_names,
            require_details=False,
        )
        contenders = r_pool_selection.selected_place_ids
        enriched_by_id: dict[str, PlaceSelectionInput] = {}
        details_failures: list[tuple[str, str]] = []
        for place_id in contenders:
            request = PlaceDetailsRequest(place_id=place_id, field_mask=PLACES_DETAILS_FIELD_MASK)
            original = merged_by_id[place_id]
            try:
                result = await self._get_place_details(request)
            except ToolBudgetExceededError:
                result = _ProviderResult[PlaceDetailsDTO](error_type="budget_exhausted")
            if result.value is None:
                enriched_by_id[place_id] = original.model_copy(
                    update={"rating_state": RatingAcquisitionState.DETAILS_FAILED}
                )
                details_failures.append((place_id, result.error_type or "details_unavailable"))
                continue
            try:
                enriched = normalize_place_details_for_selection(original, result.value)
            except ValueError as exc:
                enriched_by_id[place_id] = original.model_copy(
                    update={"rating_state": RatingAcquisitionState.DETAILS_FAILED}
                )
                details_failures.append((place_id, type(exc).__name__))
                continue
            details_date = enriched.details_opening_date
            if details_date is not None and any(
                not opening_dates_compatible(details_date, observed)
                for observed in enriched.search_opening_date_observations
            ):
                enriched = enriched.model_copy(update={"opening_date_conflict": True})
            enriched_by_id[place_id] = enriched
        enriched_candidates = tuple(
            enriched_by_id.get(item.candidate.place_id, item) for item in c_raw_candidates
        )
        no_review_selection = select_pois(
            enriched_candidates,
            start_date=requirements.start_date,
            end_date=requirements.end_date,
            window=window,
            capacity=capacities.k_final,
            must_visit_place_ids=must_visit_ids,
            excluded_place_ids=frozenset(resolved_exclusions),
            unresolved_required_names=unresolved_names,
            require_details=True,
        )
        conflicts = tuple(
            dict.fromkeys(
                [
                    *c_raw_selection.conflicts,
                    *r_pool_selection.conflicts,
                    *no_review_selection.conflicts,
                ]
            )
        )
        self._tracer.event(
            "named_place_must_visit_propagated",
            {
                "places": [
                    {
                        "place_text": item.named_place_intent.place_text,
                        "resolved_place_id": item.resolved_place_id,
                        "inclusion": item.named_place_intent.inclusion.value,
                        "must_visit": item.resolved_place_id in must_visit_ids
                        if item.resolved_place_id is not None
                        else False,
                        "c_raw": item.resolved_place_id in c_raw_selection.selected_place_ids,
                        "r_pool": item.resolved_place_id in r_pool_selection.selected_place_ids,
                        "no_review_final": item.resolved_place_id
                        in no_review_selection.selected_place_ids,
                    }
                    for item in resolutions
                ]
            },
        )
        return CandidateFunnelResult(
            capacities=capacities,
            search_intents=intents,
            search_executions=tuple(intent_executions),
            named_place_resolutions=resolutions,
            observations=tuple(observations),
            merged=merged,
            c_raw_selection=c_raw_selection,
            c_raw_candidates=c_raw_candidates,
            r_pool_selection=r_pool_selection,
            rating_contenders=contenders,
            enriched_candidates=enriched_candidates,
            details_failures=tuple(details_failures),
            no_review_selection=no_review_selection,
            conflicts=conflicts,
            must_visit_place_ids=must_visit_ids,
            excluded_place_ids=frozenset(resolved_exclusions),
            unresolved_required_names=unresolved_names,
        )

    async def run_review_aware_selection(
        self,
        *,
        funnel: CandidateFunnelResult,
        requirements: TravelRequirements,
        window: TripDateWindow,
        llm_client: StructuredLLMClient,
        llm_config_identity: str,
    ) -> "ReviewAwareSelectionResult":
        """Refine the funnel with bounded review evidence for the active V1 graph."""

        from backend.app.services.review_selection import (
            ReviewSelectionService,
        )

        service = ReviewSelectionService(
            places_provider=self._places,
            llm_client=llm_client,
            llm_config_identity=llm_config_identity,
            budget=self._budget,
            cache=self._cache,
            tracer=self._tracer,
        )
        result = await service.run(funnel=funnel, requirements=requirements, window=window)
        self._budget.consume(ToolBudgetKey.FINAL_POIS, len(result.selected_place_ids))
        return result

    @staticmethod
    def _place_details_cache_key(request: PlaceDetailsRequest) -> tuple[object, ...]:
        return ("place_details", request.place_id, request.field_mask, request.language_code)

    @staticmethod
    def _place_reviews_cache_key(request: PlaceReviewsRequest) -> tuple[object, ...]:
        """Reserve a distinct identity for later budgeted review acquisition."""

        return ("place_reviews", request.place_id, request.field_mask, request.language_code)

    async def acquire_weather(
        self,
        *,
        requirements: TravelRequirements,
        destination: DestinationContext,
        reference_date: date,
    ) -> WeatherEvidence:
        """Make at most one Daily Forecast call and retain only requested dates."""

        if requirements.start_date is None or requirements.end_date is None:
            raise ValueError("Complete trip dates are required for Weather")
        # Weather starts from the provider's current destination-local forecast day,
        # which can lag the application's fixed calendar date at day boundaries.
        # Request the full allowed horizon once, then expose only requested dates.
        horizon_days = TRIP_DATE_WINDOW_DAYS
        request = WeatherRequest(
            location=LatLng(
                latitude=destination.latitude,
                longitude=destination.longitude,
            ),
            horizon_days=horizon_days,
            requested_start=requirements.start_date,
            requested_end=requirements.end_date,
        )
        key = (
            "weather_daily",
            request.location.latitude,
            request.location.longitude,
            request.horizon_days,
            request.requested_start,
            request.requested_end,
            request.language_code,
        )
        result: _ProviderResult[WeatherForecastDTO] = await self._cached_provider_call(
            key=key,
            budget_key=ToolBudgetKey.WEATHER_CALLS,
            budget_amount=1,
            factory=lambda: self._weather.get_daily_forecast(request),
        )
        if result.value is None:
            evidence = unavailable_weather(
                request,
                requirements.destination or destination.name,
                f"Weather unavailable ({result.error_type})",
            )
        else:
            evidence = normalize_weather(
                result.value,
                request=request,
                destination=requirements.destination or destination.name,
            )
        self._tracer.payload(
            "evidence",
            "weather_evidence",
            evidence,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return evidence

    async def acquire_routes(
        self,
        *,
        places: list[PlaceEvidence],
        mode: TransportModeDecision,
        requirements: TravelRequirements,
    ) -> RouteEvidenceBundle:
        """Acquire a complete directed baseline and bounded default-WALK alternatives."""

        waypoints = [
            RouteWaypoint(
                place_id=place.place_id,
                location=LatLng(latitude=place.latitude, longitude=place.longitude),
            )
            for place in places
        ]
        departure_time = (
            self._representative_departure_time(places, requirements)
            if mode.travel_mode is TravelMode.TRANSIT
            else None
        )
        baseline = await self._acquire_baseline_route_chunks(
            waypoints=waypoints,
            mode=mode,
            departure_time=departure_time,
        )
        self._tracer.event(
            "route_baseline_completed",
            {
                "travel_mode": baseline.travel_mode,
                "availability": baseline.availability.value,
                "element_count": len(baseline.elements),
                "representative_departure_time": baseline.representative_departure_time,
                "budget": self._route_budget_summary(),
            },
        )

        non_walkable_pairs: list[NonWalkablePairEvidence] = []
        alternatives: list[RouteEvidence] = []
        if (
            not mode.is_explicit
            and mode.travel_mode is TravelMode.WALK
            and baseline.availability is not EvidenceAvailability.UNAVAILABLE
        ):
            directed_triggers = find_directed_non_walkable_pairs(baseline)
            non_walkable_pairs = collapse_non_walkable_pairs(directed_triggers)
            selected, truncated = select_alternative_route_pairs(
                non_walkable_pairs,
                max_pairs=self._budget.remaining(ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS),
                max_calls=self._budget.remaining(ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS),
            )
            alternative_departure_time = (
                self._representative_departure_time(places, requirements) if selected else None
            )
            self._trace_alternative_trigger(
                directed_triggers=directed_triggers,
                logical_pairs=non_walkable_pairs,
                selected=selected,
                truncated=truncated,
                departure_time=alternative_departure_time,
            )
            alternatives = await self._acquire_transit_alternatives(
                selected=selected,
                waypoints=waypoints,
                departure_time=alternative_departure_time,
            )
        else:
            skip_reason = (
                "explicit_transport_mode"
                if mode.is_explicit
                else "baseline_unavailable"
                if baseline.availability is EvidenceAvailability.UNAVAILABLE
                else "baseline_mode_is_not_walk"
            )
            self._tracer.event(
                "route_alternative_trigger_evaluated",
                {
                    "triggered": False,
                    "skip_reason": skip_reason,
                    "detected_directed_walk_triggers": [],
                    "collapsed_logical_pairs": [],
                    "selected_logical_pairs": [],
                    "budget_truncated_logical_pairs": [],
                    "canonical_directions": [],
                    "representative_departure_time": None,
                    "budget": self._route_budget_summary(),
                },
            )

        bundle = RouteEvidenceBundle(
            baseline=baseline,
            alternatives=alternatives,
            non_walkable_pairs=non_walkable_pairs,
        )
        self._tracer.payload(
            "evidence",
            "route_evidence_bundle",
            bundle,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return bundle

    async def _acquire_baseline_route_chunks(
        self,
        *,
        waypoints: list[RouteWaypoint],
        mode: TransportModeDecision,
        departure_time: datetime | None,
    ) -> RouteEvidence:
        """Reserve each cached-miss chunk atomically and merge a complete grid."""

        fallback_reason: str | None = None
        if not waypoints:
            fallback_reason = "No selected POIs were supplied for baseline routing"
            blocks: tuple[tuple[RouteWaypoint, ...], ...] = ()
        elif mode.travel_mode is TravelMode.TRANSIT and departure_time is None:
            fallback_reason = "Transit unavailable because no valid destination timezone was found"
            blocks = ()
        else:
            try:
                blocks = partition_baseline_origins(
                    waypoints,
                    per_request_element_limit=(
                        self._budget.limits.max_baseline_route_matrix_elements_per_request
                    ),
                )
            except ValueError as exc:
                if len(waypoints) > self._budget.limits.max_final_pois:
                    raise
                fallback_reason = str(exc)
                blocks = ()
        chunks: list[tuple[RouteMatrixRequest, RouteEvidence]] = []
        for index, origins in enumerate(blocks):
            request = RouteMatrixRequest(
                origins=list(origins),
                destinations=waypoints,
                travel_mode=mode.travel_mode.value,
                routing_preference=mode.routing_preference,
                departure_time=departure_time,
                field_mask=ROUTE_MATRIX_FIELD_MASK,
            )
            element_count = len(origins) * len(waypoints)
            self._tracer.event(
                "route_baseline_chunk_started",
                {
                    "chunk_index": index,
                    "origin_place_ids": [item.place_id for item in origins],
                    "destination_place_ids": [item.place_id for item in waypoints],
                    "requested_elements": element_count,
                    "travel_mode": request.travel_mode,
                },
            )
            try:
                evidence = await self._acquire_route_matrix(
                    request,
                    mode_reason=mode.reason,
                    purpose=RouteEvidencePurpose.BASELINE,
                    budget_key=ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS,
                    call_budget_key=ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS,
                )
            except ToolBudgetExceededError as exc:
                evidence = unavailable_routes(
                    request,
                    mode_reason=mode.reason,
                    reason=f"Baseline route request not attempted ({exc.key.value} budget)",
                )
            chunks.append((request, evidence))
            self._tracer.event(
                "route_baseline_chunk_completed",
                {
                    "chunk_index": index,
                    "origin_place_ids": [item.place_id for item in origins],
                    "requested_elements": element_count,
                    "availability": evidence.availability.value,
                    "unavailable_reason": evidence.unavailable_reason,
                    "budget": self._route_budget_summary(),
                },
            )
        return merge_baseline_route_chunks(
            waypoints,
            chunks,
            travel_mode=mode.travel_mode.value,
            mode_reason=mode.reason,
            routing_preference=mode.routing_preference,
            departure_time=departure_time,
            fallback_reason=fallback_reason,
        )

    @staticmethod
    def _representative_departure_time(
        places: list[PlaceEvidence], requirements: TravelRequirements
    ) -> datetime | None:
        if requirements.start_date is None:
            return None
        for place in places:
            if place.timezone_id is None:
                continue
            try:
                destination_timezone = ZoneInfo(place.timezone_id)
            except (ValueError, ZoneInfoNotFoundError):
                continue
            return datetime.combine(
                requirements.start_date,
                time(hour=12),
                tzinfo=destination_timezone,
            )
        return None

    @staticmethod
    def _route_cache_key(request: RouteMatrixRequest) -> tuple[object, ...]:
        return (
            "route_matrix",
            tuple(
                (item.place_id, item.location.latitude, item.location.longitude)
                for item in request.origins
            ),
            tuple(
                (item.place_id, item.location.latitude, item.location.longitude)
                for item in request.destinations
            ),
            request.travel_mode,
            request.routing_preference,
            request.departure_time,
            request.field_mask,
        )

    async def _acquire_route_matrix(
        self,
        request: RouteMatrixRequest,
        *,
        mode_reason: str,
        purpose: RouteEvidencePurpose,
        budget_key: ToolBudgetKey,
        call_budget_key: ToolBudgetKey | None = None,
    ) -> RouteEvidence:
        matrix_elements = len(request.origins) * len(request.destinations)
        additional_charges = ((call_budget_key, 1),) if call_budget_key is not None else ()
        result: _ProviderResult[RouteMatrixDTO] = await self._cached_provider_call(
            key=self._route_cache_key(request),
            budget_key=budget_key,
            budget_amount=matrix_elements,
            additional_budget_charges=additional_charges,
            factory=lambda: self._routes.compute_route_matrix(request),
        )
        if result.value is None:
            return unavailable_routes(
                request,
                mode_reason=mode_reason,
                reason=f"Routes unavailable ({result.error_type})",
                purpose=purpose,
            )
        return normalize_routes(
            result.value,
            request=request,
            mode_reason=mode_reason,
            purpose=purpose,
        )

    async def _acquire_transit_alternatives(
        self,
        *,
        selected: list[NonWalkablePairEvidence],
        waypoints: list[RouteWaypoint],
        departure_time: datetime | None,
    ) -> list[RouteEvidence]:
        waypoint_by_id = {item.place_id: item for item in waypoints}
        destinations_by_origin: dict[str, list[str]] = {}
        for pair in selected:
            destinations_by_origin.setdefault(pair.place_id_a, []).append(pair.place_id_b)

        alternatives: list[RouteEvidence] = []
        for origin_id, destination_ids in destinations_by_origin.items():
            request = RouteMatrixRequest(
                origins=[waypoint_by_id[origin_id]],
                destinations=[waypoint_by_id[item] for item in destination_ids],
                travel_mode=TravelMode.TRANSIT.value,
                departure_time=departure_time,
                field_mask=ROUTE_MATRIX_FIELD_MASK,
            )
            if departure_time is None:
                evidence = unavailable_routes(
                    request,
                    mode_reason="selective_transit_missing_destination_timezone",
                    reason=(
                        "Transit alternative unavailable because no valid "
                        "destination timezone was found"
                    ),
                    purpose=RouteEvidencePurpose.NON_WALKABLE_ALTERNATIVE,
                )
                alternatives.append(evidence)
                self._tracer.event(
                    "route_alternative_completed",
                    {
                        "origin_place_id": origin_id,
                        "destination_place_ids": destination_ids,
                        "availability": evidence.availability.value,
                        "element_count": len(evidence.elements),
                        "provider_observed_element_count": 0,
                        "mirrored_reverse_estimate_count": 0,
                        "billable_matrix_element_count": 0,
                        "representative_departure_time": None,
                        "unavailable_reason": evidence.unavailable_reason,
                        "budget": self._route_budget_summary(),
                    },
                )
                continue
            self._tracer.event(
                "route_alternative_started",
                {
                    "origin_place_id": origin_id,
                    "destination_place_ids": destination_ids,
                    "matrix_elements": len(destination_ids),
                    "representative_departure_time": departure_time,
                },
            )
            evidence = await self._acquire_route_matrix(
                request,
                mode_reason="selective_transit_for_non_walkable_pair",
                purpose=RouteEvidencePurpose.NON_WALKABLE_ALTERNATIVE,
                budget_key=ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS,
                call_budget_key=ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS,
            )
            evidence = self._with_mirrored_reverse_estimates(evidence)
            alternatives.append(evidence)
            provider_observed_count = sum(
                item.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
                for item in evidence.elements
            )
            mirrored_count = sum(
                item.evidence_type is RouteElementEvidenceType.MIRRORED_REVERSE_ESTIMATE
                for item in evidence.elements
            )
            self._tracer.event(
                "route_alternative_completed",
                {
                    "origin_place_id": origin_id,
                    "destination_place_ids": destination_ids,
                    "availability": evidence.availability.value,
                    "element_count": len(evidence.elements),
                    "provider_observed_element_count": provider_observed_count,
                    "mirrored_reverse_estimate_count": mirrored_count,
                    "billable_matrix_element_count": len(destination_ids),
                    "representative_departure_time": departure_time,
                    "unavailable_reason": evidence.unavailable_reason,
                    "budget": self._route_budget_summary(),
                },
            )
        return alternatives

    @staticmethod
    def _with_mirrored_reverse_estimates(evidence: RouteEvidence) -> RouteEvidence:
        mirrored = [
            RouteElementEvidence(
                origin_place_id=item.destination_place_id,
                destination_place_id=item.origin_place_id,
                evidence_type=RouteElementEvidenceType.MIRRORED_REVERSE_ESTIMATE,
                derived_from_origin_place_id=item.origin_place_id,
                derived_from_destination_place_id=item.destination_place_id,
                duration_seconds=item.duration_seconds,
                availability=EvidenceAvailability.AVAILABLE,
            )
            for item in evidence.elements
            if item.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
            and item.availability is EvidenceAvailability.AVAILABLE
            and item.duration_seconds is not None
            and item.origin_place_id != item.destination_place_id
        ]
        if not mirrored:
            return evidence
        return evidence.model_copy(update={"elements": [*evidence.elements, *mirrored]})

    def _trace_alternative_trigger(
        self,
        *,
        directed_triggers: list[DirectedWalkTrigger],
        logical_pairs: list[NonWalkablePairEvidence],
        selected: list[NonWalkablePairEvidence],
        truncated: list[NonWalkablePairEvidence],
        departure_time: datetime | None,
    ) -> None:
        self._tracer.event(
            "route_alternative_trigger_evaluated",
            {
                "triggered": bool(logical_pairs),
                "thresholds": {
                    "walk_distance_meters": MAX_WALK_DISTANCE_METERS,
                    "walk_duration_seconds": MAX_WALK_DURATION_SECONDS,
                },
                "detected_directed_walk_triggers": [
                    {
                        "origin_place_id": item.origin_place_id,
                        "destination_place_id": item.destination_place_id,
                        "trigger": item.trigger.value,
                        "walk_distance_meters": item.walk_distance_meters,
                        "walk_duration_seconds": item.walk_duration_seconds,
                    }
                    for item in directed_triggers
                ],
                "collapsed_logical_pairs": [item.model_dump(mode="json") for item in logical_pairs],
                "selected_logical_pairs": [item.model_dump(mode="json") for item in selected],
                "budget_truncated_logical_pairs": [
                    item.model_dump(mode="json") for item in truncated
                ],
                "canonical_directions": [
                    {
                        "origin_place_id": item.place_id_a,
                        "destination_place_id": item.place_id_b,
                    }
                    for item in selected
                ],
                "representative_departure_time": departure_time,
                "budget": self._route_budget_summary(),
            },
        )

    def _route_budget_summary(self) -> dict[str, dict[str, int]]:
        summary = self._budget.summary()
        return {
            key.value: summary[key.value]
            for key in (
                ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS,
                ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS,
                ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS,
                ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS,
            )
        }
