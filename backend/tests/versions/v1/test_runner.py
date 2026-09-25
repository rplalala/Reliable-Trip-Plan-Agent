"""Tests for V1 settings and independently runnable CLI behavior."""

import json
from pathlib import Path
from uuid import UUID

import pytest

from backend.app.observability.run_trace import NullRunTracer
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.versions.v1.config import V1Settings
from backend.app.versions.v1.runner import main
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_itinerary,
)
from backend.tests.versions.v1.fakes import RevisedFakeLLM as FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    make_revised_extraction as make_extraction,
)


class _NoSourceWeb:
    cache_identity = "offline-no-sources"

    async def search(self, request):
        from backend.app.integrations.web.models import WebSearchObservation

        return WebSearchObservation(provider_status="completed")


class _UnusedPageRetriever:
    async def fetch(self, request):
        raise AssertionError("No visible Web source should trigger page retrieval")


class _UnusedReasoner:
    async def reason(self, task, sources, baseline):
        raise AssertionError("No visible Web source should trigger reasoning")


@pytest.fixture(autouse=True)
def input_json_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    request = make_request("Plan a trip.", requirements=None)
    (tmp_path / "request.json").write_text(request.model_dump_json(), encoding="utf-8")


def test_v1_settings_reuse_v0_foundry_config_and_add_bounded_google_config(
    monkeypatch,
) -> None:
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.services.ai.azure.com/openai/v1")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "same-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "foundry-key")
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", "google-key")

    settings = V1Settings(_env_file=None)

    assert settings.azure_openai_deployment == "same-deployment"
    assert settings.google_maps_api_key.get_secret_value() == "google-key"
    assert settings.app_time_zone == "Australia/Sydney"
    assert settings.tool_budget_limits().max_route_matrix_elements == 64
    assert settings.tool_budget_limits().max_baseline_route_matrix_elements_per_request == 64
    assert settings.tool_budget_limits().max_baseline_route_matrix_elements == 400
    assert settings.tool_budget_limits().max_baseline_route_matrix_calls == 7
    assert settings.tool_budget_limits().max_alternative_route_pairs == 32
    assert settings.tool_budget_limits().max_alternative_route_matrix_calls == 32


def test_v1_cli_outputs_shared_planning_result_with_offline_injections(capsys) -> None:
    exit_code = main(
        ["--input-json", "request.json", "--reference-date", "2026-09-11"],
        llm_client=FakeStructuredLLMClient([make_extraction(), make_itinerary()]),
        places_provider=FakePlacesProvider(),
        weather_provider=FakeWeatherProvider(),
        routes_provider=FakeRoutesProvider(),
        tracer=NullRunTracer(UUID("00000000-0000-0000-0000-000000000001")),
    )

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert exit_code == 0
    assert captured.err == ""
    assert output["system_version"] == "v1"
    assert set(output) == {
        "semantic_assessment",
        "generation_diagnostics",
        "system_version",
        "requirements",
        "itinerary",
        "interpreted_requirements",
        "selection_status",
        "selection_contract_version",
        "planning_supply",
        "output_role_summary",
    }
    assert output["selection_status"] == "degraded_selection"
    assert output["planning_supply"]["shortfall"] == 1
    assert len(output["planning_supply"]["selected_place_ids"]) == 9
    assert output["planning_supply"]["evaluator_calls"] == 0


def test_v1_cli_trace_records_effective_config_without_live_providers(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.services.ai.azure.com/openai/v1")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "same-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-foundry-secret")
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", "test-google-secret")
    config = load_runtime_config()
    trace = config.trace.model_copy(update={"directory": tmp_path})
    monkeypatch.setattr(
        "backend.app.versions.v1.runner.load_runtime_config",
        lambda: config.model_copy(update={"trace": trace}),
    )
    monkeypatch.setattr(
        "backend.app.versions.v1.runner._create_tool_providers",
        lambda settings, tracer: (
            FakePlacesProvider(),
            FakeWeatherProvider(),
            FakeRoutesProvider(),
        ),
    )
    monkeypatch.setattr(
        "backend.app.versions.v1.runner._create_official_web_providers",
        lambda settings, web_config, **kwargs: (
            _NoSourceWeb(),
            _UnusedPageRetriever(),
            _UnusedReasoner(),
        ),
    )

    exit_code = main(
        ["--input-json", "request.json", "--reference-date", "2026-09-11"],
        llm_client=FakeStructuredLLMClient([make_extraction(), make_itinerary()]),
    )
    capsys.readouterr()
    run_files = list(tmp_path.glob("*/run.json"))

    assert exit_code == 0
    assert len(run_files) == 1
    run = json.loads(run_files[0].read_text(encoding="utf-8"))
    assert run["runtime_config"]["trace"]["directory"] == str(tmp_path)
    assert run["runtime_config"]["effective_tool_budget"]["alternative_route_pairs"] == 32
    assert (
        run["runtime_config"]["effective_tool_budget"]["baseline_route_matrix_elements_per_request"]
        == 64
    )
    assert len(run["runtime_config_sha256"]) == 64
    assert "test-foundry-secret" not in run_files[0].read_text(encoding="utf-8")
    assert "test-google-secret" not in run_files[0].read_text(encoding="utf-8")
