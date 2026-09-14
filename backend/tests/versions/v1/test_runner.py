"""Tests for V1 settings and independently runnable CLI behavior."""

import json
from pathlib import Path
from uuid import UUID

from backend.app.observability.run_trace import NullRunTracer
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.versions.v1.config import V1Settings
from backend.app.versions.v1.runner import main
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_extraction,
    make_itinerary,
)


def test_v1_settings_reuse_v0_foundry_config_and_add_bounded_google_config(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "AZURE_OPENAI_ENDPOINT", "https://example.services.ai.azure.com/openai/v1"
    )
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "same-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "foundry-key")
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", "google-key")

    settings = V1Settings(_env_file=None)

    assert settings.azure_openai_deployment == "same-deployment"
    assert settings.google_maps_api_key.get_secret_value() == "google-key"
    assert settings.app_time_zone == "Australia/Sydney"
    assert settings.tool_budget_limits().max_route_matrix_elements == 64
    assert settings.tool_budget_limits().max_baseline_route_matrix_elements_per_request == 64
    assert settings.tool_budget_limits().max_baseline_route_matrix_elements == 256
    assert settings.tool_budget_limits().max_baseline_route_matrix_calls == 4
    assert settings.tool_budget_limits().max_alternative_route_pairs == 8
    assert settings.tool_budget_limits().max_alternative_route_matrix_calls == 8


def test_v1_cli_outputs_shared_planning_result_with_offline_injections(capsys) -> None:
    exit_code = main(
        ["--request", "Plan two days in Sydney.", "--reference-date", "2026-09-11"],
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
    assert set(output) == {"system_version", "requirements", "itinerary"}


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
        "backend.app.versions.v1.runner._create_google_providers",
        lambda settings, tracer: (
            FakePlacesProvider(),
            FakeWeatherProvider(),
            FakeRoutesProvider(),
        ),
    )

    exit_code = main(
        ["--request", "Plan Sydney.", "--reference-date", "2026-09-11"],
        llm_client=FakeStructuredLLMClient([make_extraction(), make_itinerary()]),
    )
    capsys.readouterr()
    run_files = list(tmp_path.glob("*/run.json"))

    assert exit_code == 0
    assert len(run_files) == 1
    run = json.loads(run_files[0].read_text(encoding="utf-8"))
    assert run["runtime_config"]["trace"]["directory"] == str(tmp_path)
    assert run["runtime_config"]["effective_tool_budget"]["alternative_route_pairs"] == 8
    assert (
        run["runtime_config"]["effective_tool_budget"]["baseline_route_matrix_elements_per_request"]
        == 64
    )
    assert len(run["runtime_config_sha256"]) == 64
    assert "test-foundry-secret" not in run_files[0].read_text(encoding="utf-8")
    assert "test-google-secret" not in run_files[0].read_text(encoding="utf-8")
