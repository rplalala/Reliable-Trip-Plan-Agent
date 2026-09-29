"""Offline resource report validation and missingness regressions."""

import pytest

from backend.evaluation.usage_report import summarize


@pytest.fixture
def envelope():
    return {
        "schema_version": "rtpeval_usage_1",
        "collection_status": "available",
        "coverage": {"adapter_coverage": "default_adapters"},
        "model_calls": [],
        "provider_events": [],
        "cache_events": [],
    }


@pytest.mark.parametrize("field", ["model_calls", "provider_events", "cache_events"])
@pytest.mark.parametrize("state", ["missing", "null"])
def test_collected_usage_requires_explicit_event_arrays(envelope, field, state):
    if state == "missing":
        del envelope[field]
    else:
        envelope[field] = None
    with pytest.raises(ValueError, match="event array"):
        summarize(envelope)


def test_unavailable_envelope_does_not_require_event_arrays():
    result = summarize({"schema_version": "rtpeval_usage_1", "collection_status": "unavailable"})
    assert all(value is None for value in result["metrics"].values())


@pytest.mark.parametrize("values,expected", [([None], None), ([None, 7], 7), ([0], 0)])
def test_repair_token_subtotal_distinguishes_unknown_from_zero(envelope, values, expected):
    envelope["model_calls"] = [
        {"event_id": str(i), "total_tokens": v} for i, v in enumerate(values)
    ]
    envelope["repair_summary"] = {"model_event_ids": [str(i) for i in range(len(values))]}
    assert summarize(envelope)["repair_token_observed_subtotal"] == expected


@pytest.mark.parametrize("field", ["model_calls", "provider_events", "cache_events"])
def test_duplicate_events_are_rejected(envelope, field):
    envelope[field] = [{"event_id": "same", "outcome": "cache_hit"}] * 2
    with pytest.raises(ValueError, match="Duplicate event IDs"):
        summarize(envelope)
