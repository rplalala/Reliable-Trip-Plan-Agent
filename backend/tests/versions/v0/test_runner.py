"""Tests for V0 configuration and independent CLI behavior."""

import io
import json
import sys
from datetime import date

from backend.app.llm.azure_foundry import AzureFoundryStructuredLLMClient
from backend.app.versions.v0.config import V0Settings
from backend.app.versions.v0.runner import (
    create_foundry_client,
    main,
    parse_reference_date,
)
from backend.tests.versions.v0.fakes import (
    FakeStructuredLLMClient,
    make_itinerary,
    make_requirements,
)


def test_v0_settings_keep_underlying_model_and_deployment_distinct(
    monkeypatch,
) -> None:
    monkeypatch.setenv("LLM_MODEL", "underlying-model")
    monkeypatch.setenv(
        "AZURE_OPENAI_ENDPOINT",
        "https://example.services.ai.azure.com/openai/v1",
    )
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "configured-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-key")

    settings = V0Settings(_env_file=None)

    assert settings.llm_model == "underlying-model"
    assert str(settings.azure_openai_endpoint) == (
        "https://example.services.ai.azure.com/openai/v1"
    )
    assert settings.azure_openai_deployment == "configured-deployment"
    assert settings.azure_openai_api_key.get_secret_value() == "test-key"


def test_v0_foundry_client_uses_deployment_for_api_model(monkeypatch) -> None:
    monkeypatch.setenv("LLM_MODEL", "underlying-model")
    monkeypatch.setenv(
        "AZURE_OPENAI_ENDPOINT",
        "https://example.services.ai.azure.com/openai/v1",
    )
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "configured-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-key")
    settings = V0Settings(_env_file=None)

    client = create_foundry_client(settings)

    assert isinstance(client, AzureFoundryStructuredLLMClient)
    assert client._chat_model.model_name == "configured-deployment"
    assert client._chat_model.openai_api_base == (
        "https://example.services.ai.azure.com/openai/v1"
    )
    assert client._chat_model.use_responses_api is True
    assert client._chat_model.max_retries == 0


def test_reference_date_parser_accepts_iso_date() -> None:
    assert parse_reference_date("2026-09-11") == date(2026, 9, 11)


def test_v0_cli_outputs_planning_result_json(capsys) -> None:
    client = FakeStructuredLLMClient([make_requirements(), make_itinerary()])

    exit_code = main(
        [
            "--request",
            "Plan one day in Kyoto.",
            "--reference-date",
            "2026-09-11",
        ],
        llm_client=client,
    )

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert exit_code == 0
    assert captured.err == ""
    assert output["system_version"] == "v0"
    assert set(output) == {"system_version", "requirements", "itinerary"}


def test_v0_cli_preserves_unicode_through_cp936_safe_json(
    monkeypatch,
) -> None:
    itinerary = make_itinerary()
    activity = itinerary.days[0].activities[0].model_copy(
        update={"title": "Visit shrine 😀"}
    )
    day = itinerary.days[0].model_copy(update={"activities": [activity]})
    itinerary = itinerary.model_copy(update={"days": [day]})
    client = FakeStructuredLLMClient([make_requirements(), itinerary])

    output_buffer = io.BytesIO()
    cp936_stdout = io.TextIOWrapper(output_buffer, encoding="cp936", errors="strict")
    monkeypatch.setattr(sys, "stdout", cp936_stdout)

    exit_code = main(
        [
            "--request",
            "Plan one day in Kyoto.",
            "--reference-date",
            "2026-09-11",
        ],
        llm_client=client,
    )
    cp936_stdout.flush()
    serialized = output_buffer.getvalue().decode("cp936")
    parsed = json.loads(serialized)

    assert exit_code == 0
    assert "\\ud83d\\ude00" in serialized
    assert parsed["itinerary"]["days"][0]["activities"][0]["title"] == (
        "Visit shrine 😀"
    )


def test_v0_cli_reports_unresolved_fields(capsys) -> None:
    client = FakeStructuredLLMClient([make_requirements().model_copy(update={"end_date": None})])

    exit_code = main(
        ["--request", "Plan a trip to Kyoto."],
        llm_client=client,
    )

    captured = capsys.readouterr()
    error = json.loads(captured.err)
    assert exit_code == 2
    assert captured.out == ""
    assert error == {
        "error": "missing_required_fields",
        "unresolved_fields": ["end_date"],
    }


def test_v0_cli_reports_provider_failure_without_retry(capsys) -> None:
    client = FakeStructuredLLMClient([RuntimeError("provider unavailable")])

    exit_code = main(
        ["--request", "Plan one day in Kyoto on 2026-10-01."],
        llm_client=client,
    )

    captured = capsys.readouterr()
    error = json.loads(captured.err)
    assert exit_code == 1
    assert captured.out == ""
    assert error == {
        "error": "v0_stage_failed",
        "stage": "extract_requirements",
        "message": "provider unavailable",
    }
    assert len(client.calls) == 1
