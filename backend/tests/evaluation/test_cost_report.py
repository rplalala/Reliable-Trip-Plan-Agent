"""Offline money accounting with explicit, synthetic prices and invoice bindings."""

import copy
import json

import pytest

from backend.evaluation.cost_report import build_cost_report


def source(namespace="planner", version="v3"):
    return {
        "sha256": "a" * 64,
        "usage": {
            "schema_version": "rtpeval_usage_1",
            "group_id": "g",
            "run_id": "r",
            "version": version,
            "namespace": namespace,
            "result_sha256": "b" * 64,
            "collection_status": "available",
            "coverage": {"adapter_coverage": "default_adapters"},
            "timing": {"started_at": "2026-10-04T00:00:00+00:00"},
            "model_calls": [
                {
                    "event_id": "m",
                    "provider": "fixture",
                    "operation": "chat",
                    "model": "test",
                    "outcome": "completed",
                    "input_tokens": 1000,
                    "cached_input_tokens": 400,
                    "output_tokens": 200,
                    "reasoning_tokens": 100,
                }
            ],
            "provider_events": [
                {
                    "event_id": "h",
                    "provider": "fixture",
                    "operation": "model_http",
                    "outcome": "completed",
                    "model_event_id": "m",
                    "model_provider": "fixture",
                },
                {
                    "event_id": "api",
                    "provider": "fixture",
                    "operation": "matrix",
                    "outcome": "completed",
                    "element_count": 6,
                },
            ],
            "cache_events": [],
            "repair_summary": {"model_event_ids": ["m"], "provider_event_ids": []},
        },
    }


def prices():
    return {
        "schema_version": "rtpeval_prices_1",
        "currency": "USD",
        "rows": [
            {
                "price_id": "model",
                "source": "https://example.test/official",
                "as_of": "2026-10-05",
                "valid_from": "2026-10-01",
                "valid_until": "2026-11-01",
                "match": {
                    "kind": "model",
                    "provider": "fixture",
                    "operation": "chat",
                    "model": "test",
                },
                "rates": {"input_tokens": "2", "cached_input_tokens": "0.5", "output_tokens": "4"},
                "per": "1000000",
            },
            {
                "price_id": "matrix",
                "source": "https://example.test/official",
                "as_of": "2026-10-05",
                "valid_from": "2026-10-01",
                "valid_until": "2026-11-01",
                "match": {"kind": "provider", "provider": "fixture", "operation": "matrix"},
                "rates": {"element_count": "5"},
                "per": "1000",
            },
        ],
    }


def test_worked_cached_tokens_matrix_and_repair_subset_are_not_double_charged():
    report = build_cost_report([source()], prices())
    run = report["runs"][0]
    assert run["estimated_observed_subtotal"] == "0.0322"  # tokens .0022 + matrix .03
    assert run["best_available_observed_subtotal"] == "0.0322"
    assert run["best_available_total"] == "0.0322"
    assert run["repair"]["best_available_observed_subtotal"] == "0.0022"
    assert run["categories"]["matrix"]["estimated_observed_subtotal"] == "0.03"
    assert run["events"][0]["pricing"]["price_id"] == "model"


def test_reported_cache_writes_are_separate_from_ordinary_and_cached_input():
    item, catalog = source(), prices()
    item["usage"]["model_calls"][0]["cache_write_input_tokens"] = 300
    catalog["rows"][0]["rates"]["cache_write_input_tokens"] = "3"
    run = build_cost_report([item], catalog)["runs"][0]
    # 300 ordinary * 2 + 400 read * .5 + 300 write * 3 + 200 output * 4, per million.
    assert run["categories"]["models"]["estimated_total"] == "0.0025"
    assert run["estimated_total"] == "0.0325"
    assert run["events"][1]["status"] == "transport_only"


def test_missing_cache_writes_use_only_an_explicit_conservative_price_assumption():
    item, catalog = source(), prices()
    catalog["rows"][0]["rates"]["cache_write_input_tokens"] = "3"
    assert build_cost_report([item], catalog)["runs"][0]["estimated_total"] is None
    catalog["rows"][0]["unreported_cache_policy"] = "uncached_write_rate"
    run = build_cost_report([item], catalog)["runs"][0]
    assert run["estimated_total"] == "0.0328"  # 600 unknown non-read inputs priced at 3.
    assert run["events"][0]["pricing"]["assumptions"] == [
        "Unreported cache writes: all non-read input priced at the cache-write rate."
    ]
    assert "cache_write_input_tokens" not in item["usage"]["model_calls"][0]


def bill(scope="event", **extra):
    return {
        "bill_id": "line1",
        "scope": scope,
        "usage_sha256": "a" * 64,
        "result_sha256": "b" * 64,
        "currency": "USD",
        "amount": "0.1",
        "source": "imported-invoice.csv:1",
        "event_id": "m",
        "kind": "model",
        **extra,
    }


def test_event_bill_overrides_estimate_and_aggregate_bill_is_unallocated():
    aggregate = {
        "bill_id": "month",
        "scope": "aggregate",
        "currency": "USD",
        "amount": "12.34",
        "source": "invoice.csv:2",
    }
    report = build_cost_report([source()], prices(), bills=[bill(), aggregate])
    run = report["runs"][0]
    assert run["actual_observed_subtotal"] == "0.1"
    assert run["best_available_total"] == "0.13"
    assert run["repair"]["best_available_observed_subtotal"] == "0.1"
    assert report["unallocated_bills"] == [aggregate]


def test_missing_cache_and_failed_requests_keep_total_unknown():
    item = source()
    del item["usage"]["model_calls"][0]["cached_input_tokens"]
    item["usage"]["provider_events"][1]["outcome"] = "failed"
    run = build_cost_report([item], prices())["runs"][0]
    assert run["best_available_total"] is None
    assert run["best_available_observed_subtotal"] is None
    assert {e["missing_reason"] for e in run["events"] if e["status"] == "unpriced"} == {
        "missing_cached_input_tokens",
        "charge_uncertain",
    }


def test_complete_run_bill_does_not_invent_repair_or_category_attribution():
    item = bill("run", complete=True)
    item.pop("event_id")
    item.pop("kind")
    run = build_cost_report([source()], prices(), bills=[item])["runs"][0]
    assert run["actual_total"] == run["best_available_total"] == "0.1"
    assert run["repair"]["actual_total"] is None
    assert run["repair"]["best_available_total"] is None
    assert run["categories"]["models"]["actual_total"] is None


@pytest.mark.parametrize("change", ["duplicate", "foreign", "ambiguous", "currency"])
def test_bad_bill_bindings_are_rejected(change):
    rows = [bill()]
    if change == "duplicate":
        rows.append(copy.deepcopy(rows[0]))
    elif change == "foreign":
        rows[0]["usage_sha256"] = "c" * 64
    elif change == "ambiguous":
        rows.append({**bill(), "bill_id": "second"})
    else:
        rows[0]["currency"] = "KRW"
    with pytest.raises(ValueError):
        build_cost_report([source()], prices(), bills=rows)


def test_oracle_is_separate_and_duplicate_sources_are_rejected():
    oracle = source("oracle", "v0")
    oracle["sha256"] = "d" * 64
    report = build_cost_report([source(), oracle], prices())
    assert [r["namespace"] for r in report["runs"]] == ["planner", "oracle"]
    with pytest.raises(ValueError, match="Duplicate"):
        build_cost_report([source(), source()], prices())


def test_cli_hashes_files_and_reports_single_version_offline(tmp_path, monkeypatch):
    import socket

    from backend.evaluation.cost_report import main

    def forbidden(*args, **kwargs):
        raise AssertionError("Cost reporting must stay offline")

    monkeypatch.setattr(socket.socket, "connect", forbidden)
    paths = [tmp_path / n for n in ("usage.json", "prices.json", "report.json")]
    paths[0].write_text(json.dumps(source()["usage"]), encoding="utf-8")
    paths[1].write_text(json.dumps(prices()), encoding="utf-8")
    before = paths[0].read_bytes()
    assert (
        main(["--usage", str(paths[0]), "--prices", str(paths[1]), "--output", str(paths[2])]) == 0
    )
    report = json.loads(paths[2].read_bytes())
    assert report["runs"][0]["best_available_total"] == "0.0322"
    assert paths[0].read_bytes() == before


def test_embeddings_and_search_tool_units_are_distinct_from_backing_http():
    item = source()
    item["usage"]["model_calls"] = [
        {
            "event_id": "m",
            "provider": "fixture",
            "model": "test",
            "operation": "embedding",
            "outcome": "completed",
            "input_tokens": 1000,
        }
    ]
    item["usage"]["provider_events"] = [
        {
            "event_id": "h",
            "provider": "fixture",
            "operation": "embedding",
            "outcome": "completed",
            "model_event_id": "m",
            "model_provider": "fixture",
        },
        {
            "event_id": "t",
            "provider": "fixture",
            "operation": "web_search_tool",
            "outcome": "completed",
            "tool_calls": 2,
        },
    ]
    catalog = prices()
    catalog["rows"][0]["match"]["operation"] = "embedding"
    catalog["rows"][0]["rates"] = {"input_tokens": "0.02"}
    catalog["rows"][1]["match"]["operation"] = "web_search_tool"
    catalog["rows"][1]["rates"] = {"tool_calls": "10"}
    run = build_cost_report([item], catalog)["runs"][0]
    assert run["best_available_total"] == "0.02002"
    assert run["categories"]["embeddings"]["estimated_total"] == "0.00002"


@pytest.mark.parametrize("fault", ["expired", "ambiguous", "negative", "float", "coverage"])
def test_uncertain_prices_and_coverage_do_not_create_a_total(fault):
    item, catalog = source(), prices()
    if fault == "expired":
        catalog["rows"][0]["valid_until"] = "2026-10-02"
    elif fault == "ambiguous":
        catalog["rows"].append({**catalog["rows"][0], "price_id": "other"})
    elif fault in ("negative", "float"):
        catalog["rows"][0]["rates"]["input_tokens"] = "-1" if fault == "negative" else 0.1
        with pytest.raises(ValueError):
            build_cost_report([item], catalog)
        return
    else:
        item["usage"]["coverage"]["adapter_coverage"] = "unverified"
    assert build_cost_report([item], catalog)["runs"][0]["best_available_total"] is None


def test_annotations_require_original_hash_and_never_override_observation():
    item = source()
    annotation = {
        "usage_sha256": item["sha256"],
        "kind": "model",
        "event_id": "m",
        "source": "explicit user estimate assumption",
        "source_sha256": "c" * 64,
        "note": "No discount assumed; cache quantity is unobserved.",
        "fields": {"cached_input_tokens": 0},
    }
    with pytest.raises(ValueError, match="override"):
        build_cost_report([item], prices(), annotations=[annotation])
    del item["usage"]["model_calls"][0]["cached_input_tokens"]
    run = build_cost_report([item], prices(), annotations=[annotation])["runs"][0]
    assert run["estimated_total"] == "0.0328"
    assert run["events"][0]["annotation"]["note"] == annotation["note"]


def test_backing_http_bill_cannot_add_a_second_model_charge():
    with pytest.raises(ValueError, match="backing HTTP"):
        build_cost_report([source()], prices(), bills=[bill(kind="provider", event_id="h")])


def test_cli_rejects_output_overwriting_source_material(tmp_path):
    from backend.evaluation.cost_report import main

    usage = tmp_path / "usage.json"
    usage.write_text(json.dumps(source()["usage"]), encoding="utf-8")
    catalog = tmp_path / "prices.json"
    catalog.write_text(json.dumps(prices()), encoding="utf-8")
    before = usage.read_bytes()
    with pytest.raises(SystemExit):
        main(["--usage", str(usage), "--prices", str(catalog), "--output", str(usage)])
    assert usage.read_bytes() == before


@pytest.mark.parametrize("fault", ["failed", "incomplete", "foreign", "unlinked"])
def test_uncertain_backing_sends_remain_unknown(fault):
    item = source()
    event = item["usage"]["provider_events"][0]
    if fault in ("failed", "incomplete"):
        event["outcome"] = fault
    elif fault == "foreign":
        event["provider"] = "foreign"
    else:
        del event["model_event_id"]
    run = build_cost_report([item], prices())["runs"][0]
    assert run["best_available_total"] is None
    assert run["best_available_observed_subtotal"] == "0.0322"
    assert run["events"][1]["status"] == "unpriced"
    assert run["events"][1]["missing_reason"]


def test_observed_cache_writes_cannot_be_silently_priced_as_ordinary_input():
    item = source()
    item["usage"]["model_calls"][0]["cache_write_input_tokens"] = 300
    run = build_cost_report([item], prices())["runs"][0]
    assert run["estimated_total"] is None
    assert run["events"][0]["missing_reason"] == "missing_cache_write_price"


def test_cache_read_and_write_partitions_cannot_exceed_reported_input():
    item = source()
    item["usage"]["model_calls"][0]["cache_write_input_tokens"] = 700
    catalog = prices()
    catalog["rows"][0]["rates"]["cache_write_input_tokens"] = "3"
    run = build_cost_report([item], catalog)["runs"][0]
    assert run["estimated_total"] is None
    assert run["events"][0]["missing_reason"] == "invalid_cache_partition"
