"""Read existing evidence only; reconstruct the authorized prompt-5 V3 budget audit."""

import hashlib
import json
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "logs/semantic_short_reference_revalidation_20260927/sydney_v3"
TRACE = next((CASE / "trace").glob("*/events.jsonl"))
events = [json.loads(line) for line in TRACE.read_text().splitlines()]
assert [e["sequence"] for e in events] == list(range(1, len(events) + 1))
result = json.loads((CASE / "result.json").read_text())
config = yaml.safe_load((CASE / "runtime.yaml").read_text())


def payloads(name):
    return [e["payload"] for e in events if e["event"] == name]


rows = []


def add(name, used, limit, source):
    assert 0 <= used <= limit, (name, used, limit)
    rows.append(dict(metric=name, used=used, limit=limit, source=source))


ordinary = payloads("request_cache_lookup")
assert all(not p["cache_hit"] and p["outcome"] == "success" for p in ordinary)
counts = Counter(p["operation"] for p in ordinary)
supply = payloads("planning_supply_completed")[0]["tool_usage"]
for name in [
    "destination_search_calls",
    "candidate_search_calls",
    "place_detail_calls",
    "candidates",
    "final_pois",
    "review_detail_calls",
    "experience_profile_llm_calls",
]:
    add(
        "primary." + name,
        supply[name]["used"],
        supply[name]["limit"],
        "events:planning_supply_completed.tool_usage (stage snapshot)",
    )
assert (
    counts["places_search"]
    == supply["destination_search_calls"]["used"] + supply["candidate_search_calls"]["used"]
)
assert counts["place_details"] == supply["place_detail_calls"]["used"]
add(
    "primary.weather_calls",
    counts["weather_daily"],
    config["budget"]["weather"]["calls"],
    "events:request_cache_lookup",
)
route = payloads("initial_route_work")[-1]
for name, value in route["budget"].items():
    add(
        "primary." + name,
        value["used"],
        value["limit"],
        "events:initial_route_work final cumulative snapshot",
    )
matrix = [p for p in ordinary if p["operation"] == "route_matrix"]
baseline = payloads("route_baseline_chunk_completed")
assert (
    len(matrix)
    == route["budget"]["baseline_route_matrix_calls"]["used"]
    + route["budget"]["alternative_route_matrix_calls"]["used"]
)
baseline_elements = sum(p["requested_elements"] for p in baseline)
assert baseline_elements == route["budget"]["baseline_route_matrix_elements"]["used"]
alternative_elements = sum(p["requested_elements"] for p in matrix) - baseline_elements
add(
    "primary.alternative_route_elements",
    alternative_elements,
    config["budget"]["routes"]["alternative_elements"],
    "events:request_cache_lookup minus baseline chunks",
)
web = payloads("official_web_integration_completed")[0]
for key in ["web", "page"]:
    value = web[key + "_budget_after"]
    add(
        "primary." + key, value["used"], value["limit"], "events:official_web_integration_completed"
    )

rag = result["rag_discovery"]
rag_calls = payloads("rag_provider_result")
for operation, field, cap in [
    ("details", "details_sends", "details_calls"),
    ("fallback", "fallback_sends", "fallback_calls"),
]:
    assert sum(p["operation"] == operation and not p["cache_hit"] for p in rag_calls) == rag[field]
    add(
        "rag." + field,
        rag[field],
        config["tripworld_discovery"][cap],
        "result.rag_discovery plus events:rag_provider_result",
    )
for field, cap in [
    ("retrieval_queries", "max_queries"),
    ("returned_positions", "max_positions"),
    ("elapsed_seconds", "deadline_seconds"),
]:
    add("rag." + field, rag[field], config["tripworld_discovery"][cap], "result.rag_discovery")
assert rag["embedding_sends"] == len(result["request_resources"]["http_attempts"]) == 1

semantic = result["semantic_assessment"]
add(
    "semantic.calls",
    semantic["calls"],
    config["poi_semantics"]["max_calls"],
    "result.semantic_assessment",
)
add(
    "semantic.seconds",
    semantic["elapsed_seconds"],
    config["poi_semantics"]["total_seconds"],
    "result.semantic_assessment",
)
assert len(payloads("poi_semantic_assessment")) == len(semantic["records"]) == semantic["calls"]
for rec in semantic["records"]:
    prefix = f"semantic.call_{rec['call']}."
    add(
        prefix + "seconds",
        rec["elapsed_seconds"],
        config["poi_semantics"]["call_timeout_seconds"],
        "result.semantic_assessment.records",
    )
    add(
        prefix + "engineering_input",
        rec["engineering_tokens"],
        config["poi_semantics"]["input_tokens"],
        "result.semantic_assessment.records",
    )
    add(
        prefix + "reported_output",
        sum(u["output_tokens"] for u in rec["usage"].values()),
        config["poi_semantics"]["output_tokens"],
        "result.semantic_assessment.records.usage",
    )

repair = result["v3"]["repair"]
limits = config["v3_repair"]["acquisition"]
for key in [
    "google",
    "fallback",
    "embedding",
    "retrieval",
    "canonical",
    "details",
    "routes",
    "elements",
]:
    add(
        "repair." + key,
        repair["counters"].get(key, 0),
        limits[key],
        "result.v3.repair.counters (Counter missing keys are zero)",
    )
add(
    "repair.preparation_routes",
    repair["counters"]["preparation_routes"],
    limits["routes"] - limits["post_proposal_route_reserve"],
    "result.v3.repair.counters",
)
add(
    "repair.model",
    repair["counters"]["model"],
    config["v3_repair"]["max_model_calls"],
    "result.v3.repair.counters",
)
add(
    "repair.rounds",
    len(repair["rounds"]),
    config["v3_repair"]["max_rounds"],
    "result.v3.repair.rounds",
)
sent = [p for p in repair["acquisition_audit"] if p["sent"]]
assert len(sent) == repair["counters"]["routes"] == 12
assert all(p["operation"] == "route_matrix" and p["outcome"] == "success" for p in sent)
assert payloads("v3_repair_round")[-1]["cumulative_counters"] == repair["counters"]
add(
    "repair.engineering_input",
    repair["sizing"]["total_tokens"],
    config["v3_repair"]["input"]["input_tokens"],
    "result.v3.repair.sizing",
)
add(
    "repair.reported_output",
    sum(u["output_tokens"] for u in repair["usage"].values()),
    config["v3_repair"]["input"]["output_tokens"],
    "result.v3.repair.usage",
)
nearby = result["nearby_diagnostics"]
add(
    "nearby.requests",
    nearby["requests_sent"],
    config["reference_discovery"]["max_requests"],
    "result.nearby_diagnostics",
)
assert nearby["requests_sent"] == len(nearby["calls"]) == 3
add(
    "nearby.seconds",
    nearby["elapsed_seconds"],
    config["reference_discovery"]["deadline_seconds"],
    "result.nearby_diagnostics",
)
primary = payloads("primary_generation_resources")[0]
add(
    "primary.engineering_input",
    primary["total_tokens"],
    primary["ceiling"],
    "events:primary_generation_resources",
)
execution = json.loads((CASE / "execution.json").read_text())
add(
    "application.seconds",
    execution["elapsed_seconds"],
    config["development_timeout_seconds"],
    "execution.json",
)
files = [TRACE, CASE / "result.json", CASE / "runtime.yaml", CASE / "execution.json"]
audit = dict(
    event_count=len(events),
    contiguous_sequences=True,
    budget_rows=rows,
    embedding_sends=rag["embedding_sends"],
    embedding_reported_tokens=rag["embedding_usage"],
    primary_route_stops=dict(Counter(route["stops"])),
    evidence_sha256={
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files
    },
    limitations=[
        "Application-level send counters, not provider invoices or packet capture.",
        "Requirement and primary-generation billed token usage unavailable in dedicated captures.",
        "Per-call provider latency audit incomplete; no monetary total inferred.",
    ],
)
out = CASE.parent / "v3-budget-audit.json"
out.write_text(json.dumps(audit, indent=2) + "\n")
print(json.dumps({"budget_checks_passed": len(rows), "events": len(events), "output": str(out)}))
