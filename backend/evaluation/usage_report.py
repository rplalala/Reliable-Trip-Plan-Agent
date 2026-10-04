"""Researcher-facing usage comparisons, independent of itinerary quality scores."""

import argparse
import json
import math
from statistics import median

from .intake import _read

VERSIONS = ("v0", "v1", "v2", "v3")


def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def summarize(usage):
    if usage.get("schema_version") != "rtpeval_usage_1":
        raise ValueError("Unsupported usage schema")
    status = usage.get("collection_status")
    if status not in ("available", "partial", "unavailable"):
        raise ValueError("Explicit usage collection status required")
    for field in ("model_calls", "provider_events", "cache_events"):
        if field in usage or status != "unavailable":
            if not isinstance(usage.get(field), list):
                raise ValueError("Usage requires explicit event array: " + field)
    models, providers = usage.get("model_calls", []), usage.get("provider_events", [])
    for rows in (models, providers, usage.get("cache_events", [])):
        ids = [r["event_id"] for r in rows]
        if len(set(ids)) != len(ids):
            raise ValueError("Duplicate event IDs cannot be counted twice")
    # SDK tool billing observations are not application HTTP transport entries.
    providers = [r for r in providers if r.get("source") != "sdk_output_tool_calls"]
    covered = usage.get("coverage", {}).get("adapter_coverage") == "default_adapters" and usage.get(
        "collection_status"
    ) in ("available", "partial")
    elapsed = usage.get("timing", {}).get("elapsed_seconds")
    token_values = [r.get("total_tokens") for r in models]
    known = [v for v in token_values if number(v)]
    tokens_complete = covered and len(known) == len(models)
    repair_ids = set(usage.get("repair_summary", {}).get("model_event_ids", []))
    if not repair_ids <= {r["event_id"] for r in models}:
        raise ValueError("Repair usage must reference existing model events")
    repair_known = [
        r["total_tokens"]
        for r in models
        if r["event_id"] in repair_ids and number(r.get("total_tokens"))
    ]
    metrics = {
        "elapsed_seconds": elapsed if number(elapsed) else None,
        "total_tokens": sum(known) if tokens_complete else None,
        "model_calls": len(models) if covered else None,
        "http_sends": len(providers) if covered else None,
        "cache_hits": sum(r.get("outcome") == "cache_hit" for r in usage.get("cache_events", []))
        if covered
        else None,
    }
    return {
        "run_id": usage.get("run_id"),
        "outcome": usage.get("outcome", "unavailable"),
        "namespace": usage.get("namespace", "planner"),
        "timing_scope": usage.get("timing", {}).get("scope"),
        "metrics": metrics,
        "observed_token_subtotal": sum(known) if known else None,
        "observed_model_calls": len(models),
        "observed_http_sends": len(providers),
        "cache_lookup_hits": sum(
            r.get("outcome") == "cache_lookup_hit" for r in usage.get("cache_events", [])
        ),
        "observed_tool_http_sends": sum(
            r.get("operation") not in ("model_http", "embedding", "official_reasoning")
            for r in providers
        ),
        "token_observed_calls": len(known),
        "token_missing_calls": len(models) - len(known),
        "adapter_coverage": "declared_default_adapters" if covered else "unverified",
        "repair_model_calls": len(repair_ids),
        "repair_token_observed_subtotal": sum(repair_known) if repair_known else None,
        "failed_http_responses": sum(r.get("outcome") == "failed" for r in providers),
        "incomplete_http_sends": sum(r.get("outcome") == "incomplete" for r in providers),
        "missing_fields": usage.get("missing_fields", []),
    }


def compare_usage(envelopes):
    """Retain request-level pairing; do not assign an efficiency score or quality verdict."""
    groups = {}
    for usage in envelopes:
        gid, version = usage.get("group_id"), usage.get("version")
        if not gid or version not in VERSIONS:
            raise ValueError("Usage requires group and version linkage")
        group = groups.setdefault(gid, {})
        if version in group:
            raise ValueError("Choose one selected usage envelope per version/group")
        group[version] = summarize(usage)
    output = []
    for gid, runs in groups.items():
        if set(runs) != set(VERSIONS):
            raise ValueError("Selected comparison groups require four usage envelopes")
        comparisons = []
        for i, baseline in enumerate(VERSIONS):
            for candidate in VERSIONS[i + 1 :]:
                if baseline not in runs or candidate not in runs:
                    continue
                left, right = runs[baseline], runs[candidate]
                scope_ok = (
                    left["namespace"] == right["namespace"] and left["outcome"] == right["outcome"]
                )
                for metric, a in left["metrics"].items():
                    b = right["metrics"][metric]
                    compatible = scope_ok and (
                        metric != "elapsed_seconds"
                        or left["timing_scope"]
                        == right["timing_scope"]
                        == "selected_invocation_through_cleanup"
                    )
                    valid = compatible and a is not None and b is not None
                    comparisons.append(
                        {
                            "baseline": baseline,
                            "candidate": candidate,
                            "metric": metric,
                            "difference": b - a if valid else None,
                            "ratio": b / a if valid and a > 0 else None,
                            "reason": "scope_mismatch"
                            if not compatible
                            else "missing_measurement"
                            if not valid
                            else "zero_baseline"
                            if a == 0
                            else None,
                        }
                    )
        output.append({"group_id": gid, "runs": runs, "comparisons": comparisons})
    summaries = {}
    for version in VERSIONS:
        summaries[version] = {}
        for metric in (
            "elapsed_seconds",
            "total_tokens",
            "model_calls",
            "http_sends",
            "cache_hits",
        ):
            # Never mix failed attempts or different timing/namespace scopes into one median.
            cohorts = {}
            for group in output:
                run = group["runs"].get(version)
                if run and run["metrics"][metric] is not None:
                    key = (run["namespace"], run["outcome"], run["timing_scope"])
                    cohorts.setdefault(key, []).append(run["metrics"][metric])
            summaries[version][metric] = [
                {
                    "namespace": k[0],
                    "outcome": k[1],
                    "scope": k[2],
                    "available_count": len(v),
                    "median": median(v),
                }
                for k, v in cohorts.items()
            ]
    return {
        "schema_version": "rtpeval_resource_report_1",
        "groups": output,
        "descriptive_summaries": summaries,
        "quality_score_contribution": None,
        "audience": "researcher",
        "formal_inference": "not_performed",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("usage_files", nargs="+")
    args = parser.parse_args(argv)
    from pathlib import Path

    print(
        json.dumps(
            compare_usage([_read(Path(p))[0] for p in args.usage_files]),
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
