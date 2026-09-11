"""Tests that lock down the V0 LangGraph behavior."""

import asyncio
from datetime import date

import pytest

from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.planning import SystemVersion
from backend.app.schemas.request import TravelRequest, TravelRequirements
from backend.app.versions.v0.graph import (
    MissingRequiredFieldsError,
    V0StageError,
    build_v0_graph,
)
from backend.app.versions.v0.runner import run_v0
from backend.tests.versions.v0.fakes import (
    FakeStructuredLLMClient,
    make_itinerary,
    make_requirements,
)


def test_v0_graph_has_exact_two_node_topology() -> None:
    graph = build_v0_graph(FakeStructuredLLMClient([])).get_graph()

    assert set(graph.nodes) == {
        "__start__",
        "extract_requirements",
        "generate_itinerary",
        "__end__",
    }
    assert {(edge.source, edge.target) for edge in graph.edges} == {
        ("__start__", "extract_requirements"),
        ("extract_requirements", "generate_itinerary"),
        ("generate_itinerary", "__end__"),
    }


def test_v0_runs_exactly_the_two_intended_structured_stages() -> None:
    client = FakeStructuredLLMClient([make_requirements(), make_itinerary()])

    result = asyncio.run(
        run_v0(
            TravelRequest(request_text="Plan one day in Kyoto."),
            client,
            reference_date=date(2026, 9, 11),
        )
    )

    assert [call.response_schema for call in client.calls] == [TravelRequirements, Itinerary]
    assert "2026-09-11" in client.calls[0].user_prompt
    assert "Kyoto" in client.calls[1].user_prompt
    assert result.system_version is SystemVersion.V0
    assert set(result.model_dump(mode="json")) == {
        "system_version",
        "requirements",
        "itinerary",
    }


def test_v0_reports_missing_critical_requirements_without_generation() -> None:
    client = FakeStructuredLLMClient(
        [TravelRequirements(destination="Kyoto", unresolved_fields=[])]
    )

    with pytest.raises(MissingRequiredFieldsError) as captured:
        asyncio.run(
            run_v0(
                TravelRequest(request_text="Plan a trip to Kyoto."),
                client,
                reference_date=date(2026, 9, 11),
            )
        )

    assert captured.value.unresolved_fields == ("start_date", "end_date")
    assert captured.value.requirements.unresolved_fields == ["start_date", "end_date"]
    assert len(client.calls) == 1


def test_v0_does_not_retry_after_extraction_failure() -> None:
    client = FakeStructuredLLMClient([RuntimeError("provider failure")])

    with pytest.raises(V0StageError, match="extract_requirements") as captured:
        asyncio.run(
            run_v0(
                TravelRequest(request_text="Plan one day in Kyoto."),
                client,
                reference_date=date(2026, 9, 11),
            )
        )

    assert captured.value.stage == "extract_requirements"
    assert len(client.calls) == 1


def test_v0_does_not_retry_or_repair_after_generation_failure() -> None:
    client = FakeStructuredLLMClient([make_requirements(), RuntimeError("schema failure")])

    with pytest.raises(V0StageError, match="generate_itinerary") as captured:
        asyncio.run(
            run_v0(
                TravelRequest(request_text="Plan one day in Kyoto."),
                client,
                reference_date=date(2026, 9, 11),
            )
        )

    assert captured.value.stage == "generate_itinerary"
    assert len(client.calls) == 2
