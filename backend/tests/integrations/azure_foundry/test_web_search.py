"""Offline mapping tests for Luna application-visible Web Search output."""

import asyncio
from datetime import date

import pytest

from backend.app.integrations.azure_foundry.web_search import (
    AzureFoundryWebEvidenceProvider,
    normalize_luna_response,
)
from backend.app.integrations.web.models import WebActionType, WebEvidenceSearchRequest
from backend.app.runtime.config_loader import load_runtime_config


def _request():
    return WebEvidenceSearchRequest(
        task_id="trace-only",
        place_id="alpha",
        place_name="Alpha Zoo",
        information_need="date_specific_operational_exception",
        applicable_start_date=date(2026, 12, 25),
        applicable_end_date=date(2026, 12, 25),
        allowed_domains=("example.org",),
        task_instruction="Find an official dated maintenance notice only.",
        template_version="official_web_v1",
    )


def test_maps_actions_results_citations_and_usage_without_inventing_completion() -> None:
    raw = {
        "id": "resp-1",
        "status": "completed",
        "output": [
            {
                "type": "web_search_call",
                "status": "completed",
                "action": {
                    "type": "search",
                    "queries": ["Alpha Zoo closure", {"search_term": "maintenance"}],
                    "sources": [{"url": "https://example.org/official-notice"}],
                },
                "results": [
                    {
                        "url": "https://example.org/official-notice",
                        "title": "Notice",
                        "snippet": "Closed on December 25",
                    },
                    {"url": "https://evil.example.com/page", "title": "Unrelated", "snippet": "x"},
                ],
            },
            {
                "type": "web_search_call",
                "status": "searching",
                "action": {"type": "open_page", "url": "https://example.org/official-notice"},
            },
            {
                "type": "message",
                "content": [
                    {
                        "annotations": [
                            {
                                "type": "url_citation",
                                "url": "https://example.org/official-notice",
                                "title": "Notice",
                                "start_index": 0,
                                "end_index": 10,
                            },
                        ]
                    }
                ],
            },
        ],
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150,
            "output_tokens_details": {"reasoning_tokens": 20},
        },
    }
    result = normalize_luna_response(raw, _request(), latency_ms=1200)
    assert [action.action_type for action in result.actions] == [
        WebActionType.SEARCH,
        WebActionType.OPEN_PAGE,
    ]
    assert result.actions[0].queries == ("Alpha Zoo closure", "maintenance")
    assert result.actions[1].status == "searching"
    assert result.partial is True
    assert result.hits[0].snippet == "Closed on December 25"
    assert result.hits[0].allowed_domain is True
    assert result.hits[1].allowed_domain is False
    assert result.citations[0].url == "https://example.org/official-notice"
    assert result.usage.total_tokens == 150
    assert result.usage.reasoning_tokens == 20


def test_source_only_result_and_malformed_partial_fields() -> None:
    raw = {
        "status": "completed",
        "output": [
            {
                "type": "web_search_call",
                "status": "completed",
                "action": {
                    "type": "search",
                    "sources": [
                        {"url": "https://example.org/source-only"},
                        {"url": None},
                    ],
                },
                "results": "malformed",
            },
            None,
        ],
    }
    result = normalize_luna_response(raw, _request(), latency_ms=1)
    assert result.partial is True
    assert len(result.hits) == 1
    assert result.hits[0].url == "https://example.org/source-only"
    assert result.hits[0].snippet is None


def test_citation_only_url_remains_visible_as_source_without_page_support() -> None:
    raw = {
        "status": "completed",
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "annotations": [
                            {
                                "type": "url_citation",
                                "url": "https://example.org/notice",
                                "title": "Official notice",
                            }
                        ]
                    }
                ],
            }
        ],
    }
    result = normalize_luna_response(raw, _request(), latency_ms=5)
    assert len(result.citations) == len(result.hits) == 1
    assert result.hits[0].allowed_domain is True
    assert result.hits[0].snippet is None
    assert result.hits[0].action_index == -1


def test_rejects_malformed_top_level_response() -> None:
    with pytest.raises(ValueError, match="Malformed"):
        normalize_luna_response({"output": "bad"}, _request(), latency_ms=1)


class FakeResponses:
    def __init__(self):
        self.calls = []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        return {"id": "response-1", "status": "completed", "output": []}


def test_adapter_uses_application_defined_envelope() -> None:
    fake = FakeResponses()
    provider = AzureFoundryWebEvidenceProvider(
        endpoint="https://example.services.ai.azure.com/openai/v1",
        deployment="luna-deployment",
        api_key="test-key",
        config=load_runtime_config().web_evidence,
        responses_client=fake,
    )
    observation = asyncio.run(provider.search(_request()))
    assert observation.response_id == "response-1"
    call = fake.calls[0]
    assert call["input"] == _request().task_instruction
    assert call["model"] == "luna-deployment"
    assert call["tools"][0]["filters"]["allowed_domains"] == ["example.org"]
    assert call["reasoning"] == {"effort": "low"}
    assert call["max_tool_calls"] == 2
    assert call["tools"][0]["search_context_size"] == "low"
    assert len(fake.calls) == 1
