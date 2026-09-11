"""Tests for V1 settings and independently runnable CLI behavior."""

import json
from uuid import UUID

from backend.app.observability.run_trace import NullRunTracer
from backend.app.versions.v1.config import V1Settings
from backend.app.versions.v1.runner import main
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_itinerary,
    make_requirements,
)


def test_v1_settings_reuse_v0_foundry_config_and_add_bounded_google_config(
    monkeypatch,
) -> None:
    monkeypatch.setenv("LLM_MODEL", "same-model")
    monkeypatch.setenv(
        "AZURE_OPENAI_ENDPOINT", "https://example.services.ai.azure.com/openai/v1"
    )
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "same-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "foundry-key")
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", "google-key")
    monkeypatch.setenv("APP_TIME_ZONE", "Australia/Sydney")

    settings = V1Settings(_env_file=None)

    assert settings.llm_model == "same-model"
    assert settings.azure_openai_deployment == "same-deployment"
    assert settings.google_maps_api_key.get_secret_value() == "google-key"
    assert settings.app_time_zone == "Australia/Sydney"
    assert settings.tool_budget_limits().max_route_matrix_elements == 64


def test_v1_cli_outputs_shared_planning_result_with_offline_injections(capsys) -> None:
    exit_code = main(
        ["--request", "Plan two days in Sydney.", "--reference-date", "2026-09-11"],
        llm_client=FakeStructuredLLMClient([make_requirements(), make_itinerary()]),
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
    assert set(output) == {"system_version", "requirements", "itinerary"}
