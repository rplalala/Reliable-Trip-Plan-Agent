"""Offline V2 discovery boundaries, overlap accounting and failure ownership."""

import asyncio
from datetime import date
from types import SimpleNamespace
from uuid import uuid4

import pytest

from backend.app.evidence.selection_normalization import normalize_place_details_for_selection
from backend.app.integrations.google.places import PLACES_DETAILS_FIELD_MASK
from backend.app.integrations.models import (
    LatLng,
    PlaceCandidateDTO,
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceSearchResponse,
)
from backend.app.observability.run_trace import NullRunTracer
from backend.app.policies.poi_funnel import MergedSearchObservations
from backend.app.policies.tripworld_query_plan import query_plan
from backend.app.runtime.budget import ToolBudget
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.interpreted_requirements import DiscoveryIntent
from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
from backend.app.services.tripworld_discovery import RAGStop, TripWorldDiscovery
from backend.app.tripworld.retrieval.entities import RetrievalEntity
from backend.app.versions.v2.config import RAGConfig
from backend.tests.candidate_fixtures import candidate_fixture


@pytest.fixture(autouse=True)
def query_tokenizer(monkeypatch):
    monkeypatch.setattr(
        "backend.app.policies.tripworld_query_plan.tokenizer",
        lambda: SimpleNamespace(encode_ordinary=lambda text: list(text)),
    )


def hit(pid, *, entity_id=None, rank=1):
    entity = RetrievalEntity(
        retrieval_entity_id=entity_id or f"entity:{pid}",
        google_place_id=pid,
        source_fsq_place_ids=("fsq",),
        preferred_name=pid or "Alias",
        aliases=("Alias",),
        latitude=-33.86,
        longitude=151.2,
        localities=("Sydney",),
        regions=(),
        country="AU",
        countries=("AU",),
        fsq_categories=(),
        google_categories=(),
        direct_semantics=("quiet",),
        inferred_semantics=(),
        semantic_rule_ids=(),
        source_eligibility_hints=(),
        eligibility_hint="unknown",
        retrieval_description="Quiet",
        raw_retrieval_text="Museum",
        retrieval_text="Quiet museum",
        coordinate_spread_km=0,
        location_flags=(),
        source_row_count=1,
        tripworld_revision="revision",
        semantic_mapping_version="mapping",
        retrieval_entity_builder_version="builder",
        retrieval_text_template_version="text",
        content_hash="content",
    )
    return dict(
        entity=entity.model_dump(mode="json"),
        rank=rank,
        similarity_score=0.8,
        distance_km=1,
        retrieval_entity_artifact_hash="artifact",
        embedding_text_hash="text",
    )


def details(pid, **updates):
    return PlaceDetailsDTO(
        place_id=pid,
        display_name=pid,
        location=LatLng(latitude=-33.86, longitude=151.2),
        rating=4.8,
        business_status="OPERATIONAL",
        retrieved_at="2026-09-19T00:00:00Z",
        **updates,
    )


class Places:
    def __init__(self):
        self.ids, self.searches = [], []
        self.fail, self.delay, self.cancelled = set(), 0, False
        self.results = []

    async def get_place_details(self, request):
        self.ids.append(request.place_id)
        try:
            if self.delay:
                await asyncio.sleep(self.delay)
            if request.place_id in self.fail:
                raise ValueError("provider failure")
            return details(request.place_id)
        except asyncio.CancelledError:
            self.cancelled = True
            raise

    async def search_text(self, request):
        self.searches.append(request)
        return PlaceSearchResponse(
            candidates=self.results,
            actual_result_count=len(self.results),
            retrieved_at="2026-09-19T00:00:00Z",
        )


class Retrieval:
    def __init__(self, rows, *, fail=False):
        self.rows, self.fail, self.closed = rows, fail, False
        self.artifact_hash, self.usage = "artifact", {"total_tokens": 2}
        self.embedding_sends, self.searches = 0, 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        self.closed = True

    async def prepare(self):
        if self.fail:
            raise ConnectionError("database unavailable")

    async def embed(self, texts):
        self.embedding_sends += 1
        return [[1] for _ in texts]

    async def search(self, *_):
        self.searches += 1
        return self.rows


def setup(rows, *, n=6, config=None, fail=False):
    projection = candidate_fixture(min(n, 18), 2)
    places = Places()
    acq = V1EvidenceAcquisitionService(
        places_provider=places,
        weather_provider=None,
        routes_provider=None,
        budget=ToolBudget(),
        cache=RequestCache(),
        tracer=NullRunTracer(uuid4()),
    )
    runtime = Retrieval(rows, fail=fail)
    service = TripWorldDiscovery(acq, config=config, runtime_factory=lambda: runtime)
    observations = list(projection.canonical_places)
    for i in range(len(observations), n):
        observations.append(
            observations[0].model_copy(
                update={
                    "candidate": observations[0].candidate.model_copy(
                        update={"place_id": f"place_{i:02d}"}
                    )
                }
            )
        )
    merged = MergedSearchObservations(tuple(observations), n)
    dest = SimpleNamespace(latitude=-33.86, longitude=151.2)
    return service, projection.requirements, dest, merged, places, runtime


def execute(setup_result, excluded=()):
    service, contract, dest, merged, *_ = setup_result
    return asyncio.run(service.extend(contract, dest, merged, set(excluded)))


def test_six_overlap_hits_do_not_block_seventh_new_entity():
    x = setup([*(hit(f"place_{i:02d}", rank=i + 1) for i in range(6)), hit("new", rank=7)])
    result = execute(x)
    service, _, _, _, places, runtime = x
    assert service.report["resolution_attempts"] == 1
    assert service.report["google_overlap_entities"] == 6
    assert places.ids == ["new"] and not places.searches
    assert runtime.searches == runtime.embedding_sends == 1 and runtime.closed
    new = next(p for p in result.places if p.candidate.place_id == "new")
    assert new.candidate.provider_rank is None and new.query_hits == []
    assert new.rating is None and new.structured_evidence is None
    assert new.discovery_origins[0].query.origin == "system_default"
    assert new.discovery_intent_ids == ()
    normalized = normalize_place_details_for_selection(new, details("new"))
    assert normalized.rating == 4.8 and normalized.discovery_origins == new.discovery_origins


def test_all_overlap_needs_no_google_resolution():
    x = setup([hit(f"place_{i:02d}", rank=i + 1) for i in range(6)])
    execute(x)
    assert x[0].report["resolution_attempts"] == 0
    assert x[4].ids == [] and x[0].report["new_canonical_ids"] == []


def test_duplicate_entities_and_canonical_ids_union_query_refs():
    x = setup([hit("new"), hit("new", entity_id="other", rank=2)])
    contract = x[1].model_copy(
        update={
            "discovery_intents": (
                DiscoveryIntent(
                    intent_id="discovery_1",
                    query_text="museums",
                    requirement_refs=("semantic_1",),
                    purpose="semantic_discovery",
                ),
                DiscoveryIntent(
                    intent_id="discovery_2",
                    query_text="culture",
                    requirement_refs=("semantic_2",),
                    purpose="semantic_discovery",
                ),
            )
        }
    )
    result = asyncio.run(x[0].extend(contract, x[2], x[3], set()))
    p = next(p for p in result.places if p.candidate.place_id == "new")
    assert set(p.discovery_intent_ids) == {"discovery_1", "discovery_2"}
    assert len(p.discovery_origins) == 4
    assert x[4].ids == ["new"] and x[0].report["resolution_attempts"] == 1
    assert x[0].report["returned_positions"] == 4


def test_failures_count_attempts_and_continue_without_enlarging_caps():
    x = setup([hit(f"new{i}", rank=i + 1) for i in range(10)])
    x[4].fail = {f"new{i}" for i in range(5)}
    result = execute(x)
    assert x[0].report["resolution_attempts"] == 6
    assert x[0].report["details_sends"] == 6
    assert x[0].report["fallback_sends"] == 2
    assert "new5" in {p.candidate.place_id for p in result.places}
    assert x[0].report["status"] == "partial"


@pytest.mark.parametrize("pid", [None, "stale"])
def test_missing_or_failed_id_unique_alias_fallback(pid):
    x = setup([hit(pid)])
    x[4].fail = {"stale"}
    x[4].results = [
        PlaceCandidateDTO(
            place_id="replacement",
            display_name="Alias",
            location=LatLng(latitude=-33.86, longitude=151.2),
            provider_rank=0,
        )
    ]
    result = execute(x)
    p = next(p for p in result.places if p.candidate.place_id == "replacement")
    assert not p.query_hits and p.discovery_origins[0].resolution == "fallback"
    assert len(x[4].searches) == 1 and x[4].searches[0].page_size == 3


def test_provider_failure_cached_but_local_limits_and_timeout_not_cached():
    async def scenario():
        x = setup([])
        s, _, _, _, places, _ = x
        s.ends = __import__("time").perf_counter() + 30
        places.fail = {"bad"}
        assert await s.details("bad") is None
        assert (
            await s.acq._get_place_details(
                PlaceDetailsRequest(place_id="bad", field_mask=PLACES_DETAILS_FIELD_MASK)
            )
            is not None
        )
        assert places.ids == ["bad"]
        s.report["details_sends"] = 8
        with pytest.raises(RAGStop, match="budget"):
            await s.details("untried")
        assert not s.acq._cache.lookup(
            ("place_details", "untried", PLACES_DETAILS_FIELD_MASK, "en")
        )[1]
        s.report["details_sends"] = 0
        s.config = RAGConfig(google_timeout=0.01)
        places.delay = 1
        with pytest.raises(RAGStop, match="request_timeout"):
            await s.details("slow")
        assert places.cancelled
        assert not s.acq._cache.lookup(("place_details", "slow", PLACES_DETAILS_FIELD_MASK, "en"))[
            1
        ]

    asyncio.run(scenario())


def test_details_reused_at_normal_enrichment_without_main_charge():
    async def scenario():
        x = setup([hit("new")])
        await x[0].extend(x[1], x[2], x[3], set())
        response = await x[0].acq._get_place_details(
            PlaceDetailsRequest(place_id="new", field_mask=PLACES_DETAILS_FIELD_MASK)
        )
        assert response.value.place_id == "new"
        assert x[4].ids == ["new"]
        assert x[0].acq._budget.summary()["place_detail_calls"]["used"] == 0

    asyncio.run(scenario())


def test_dependency_failure_preserves_google_and_no_embedding_send():
    x = setup([], fail=True)
    result = execute(x)
    assert result == x[3]
    assert x[0].report["status"] == "unavailable" and x[5].closed
    assert not x[4].ids and x[0].report["embedding_sends"] == 0


def test_sql_timeout_observation_does_not_claim_phase_expired():
    x = setup([])
    x[5].diagnostics = []

    async def failed_search(*_):
        x[5].diagnostics.append({"stage": "sql", "sql_timeout_expired": True})
        raise TimeoutError()

    x[5].search = failed_search
    assert execute(x) == x[3]
    assert x[0].report["status"] == "deadline_limited"
    assert x[0].report["timeout_scope"] == "sql"
    assert x[0].report["phase_deadline_expired"] is False
    assert x[5].closed


def test_phase_deadline_and_user_cancellation_close_resources():
    async def scenario(cancel):
        x = setup([hit("new"), hit("next", rank=2)], config=RAGConfig(deadline_seconds=0.04))
        x[4].delay = 1
        task = asyncio.create_task(x[0].extend(x[1], x[2], x[3], set()))
        if cancel:
            await asyncio.sleep(0.01)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert x[0].report["cancellation"] == "caller_cancelled"
        else:
            result = await task
            assert result == x[3]
            assert x[0].report["status"] == "deadline_limited"
            assert x[0].report["phase_deadline_expired"]
            assert x[0].report["timeout_scope"] == "phase"
        assert x[5].closed and x[4].cancelled
        assert x[4].ids == ["new"]

    asyncio.run(scenario(False))
    asyncio.run(scenario(True))


def test_query_duplicates_default_and_invalid_semantics_not_reparsed(monkeypatch):
    _, contract, *_ = setup([])
    assert query_plan(contract)[0][0].origin == "system_default"
    contract = contract.model_copy(
        update={
            "discovery_intents": tuple(
                DiscoveryIntent(
                    intent_id=f"discovery_{i + 1}",
                    query_text=q,
                    requirement_refs=(f"semantic_{i + 1}",),
                    purpose="semantic_discovery",
                )
                for i, q in enumerate(("Museum", "  museum  "))
            )
        }
    )
    queries, _ = query_plan(contract)
    assert len(queries) == 1 and len(queries[0].requirement_refs) == 2
    monkeypatch.setattr(
        "backend.app.policies.tripworld_query_plan.tokenizer",
        lambda: SimpleNamespace(encode_ordinary=lambda text: range(600)),
    )
    with pytest.raises(ValueError, match="Total query"):
        query_plan(contract)


@pytest.mark.parametrize(
    "count,pid,low_rating,expected",
    [
        (4, "aaa", False, "supplied"),
        (12, "aaa", True, "not_selected"),
        (24, "zzz", False, "not_admitted"),
    ],
)
def test_rag_competes_under_real_shared_capacities(count, pid, low_rating, expected):
    from backend.app.policies.trip_dates import create_trip_date_window
    from backend.app.services.planning_supply_pipeline import PlanningCandidateSupplyPipeline

    async def scenario():
        x = setup([hit(pid)], n=count)
        s, contract, dest, merged, places, _ = x

        async def observations(*args, **kwargs):
            return list(merged.places)

        s.acq.search_candidate_observations = observations
        original = places.get_place_details

        async def acquire(request):
            value = await original(request)
            return (
                value.model_copy(update={"rating": 0.1})
                if low_rating and request.place_id == pid
                else value
            )

        places.get_place_details = acquire
        pipeline = PlanningCandidateSupplyPipeline(s.acq, None, s.acq._tracer, "offline")
        pipeline.discovery_extension = s
        funnel, selection = await pipeline.run(
            contract, dest, create_trip_date_window(date(2026, 9, 19))
        )
        admitted = {p.candidate.place_id for p in funnel.admitted_candidates}
        enriched = {p.candidate.place_id for p in funnel.enriched_candidates}
        if expected == "supplied":
            assert pid in selection.selected_place_ids
        elif expected == "not_selected":
            assert pid in enriched and pid not in selection.selected_place_ids
        else:
            assert pid not in admitted
        assert (
            len(admitted) <= 20
            and len(enriched) <= min(len(admitted), 11)
            and len(selection.selected_place_ids) <= 8
        )
        assert selection.evaluator_calls == selection.subset_enumerator_calls == 0

    asyncio.run(scenario())


def test_exclusions_and_ambiguous_or_far_fallback_do_not_damage_google():
    for mode in ("excluded", "ambiguous", "far"):
        x = setup([hit(None)])
        coords = LatLng(latitude=-33.86 if mode != "far" else -34.0, longitude=151.2)
        x[4].results = [
            PlaceCandidateDTO(
                place_id="replacement", display_name="Alias", location=coords, provider_rank=0
            )
        ]
        if mode == "ambiguous":
            x[4].results.append(
                x[4].results[0].model_copy(update={"place_id": "other", "provider_rank": 1})
            )
        result = execute(x, excluded=("replacement",) if mode == "excluded" else ())
        assert result == x[3]


def test_expired_stage_does_not_cache_or_send_and_incompatible_mask_is_not_reused():
    async def scenario():
        import time

        x = setup([])
        s = x[0]
        s.ends = time.perf_counter() - 1
        with pytest.raises(RAGStop, match="deadline"):
            await s.details("new")
        assert len(s.acq._cache) == 0 and not x[4].ids
        s.ends = time.perf_counter() + 30
        other = PlaceDetailsRequest(place_id="new", field_mask="id")
        await s.acq._get_place_details(other)
        await s.details("new")
        assert x[4].ids == ["new", "new"]

    asyncio.run(scenario())
