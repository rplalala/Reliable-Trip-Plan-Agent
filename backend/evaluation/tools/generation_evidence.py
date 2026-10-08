"""Local evidence inventory; availability is separate from batch qualification."""

import hashlib
import json


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_evidence_index(output, manifest, raw, usage, *, adapter_coverage):
    missing = []
    if not (output / "usage.json").is_file():
        missing.append("usage")
    diagnostics = list(raw.diagnostics) if raw else [{"reason": "raw_capture_not_started"}]
    events = raw.events if raw else []
    mechanism_path = output / "mechanism.json"
    if mechanism_path.is_file():
        mechanism = json.loads(mechanism_path.read_bytes())
        missing.extend(f"mechanism.{name}" for name in mechanism["missing_fields"])
        diagnostics.extend(mechanism["diagnostics"])
    else:
        missing.append("mechanism")
    if adapter_coverage != "default_adapters":
        missing.append("verified_adapter_coverage")
    observed_ids = {row["event_id"] for row in events}
    for event in usage.get("provider_events", []):
        if event.get("source") == "http_request_hook" and event["event_id"] not in observed_ids:
            missing.append(f"http.{event['event_id']}")
    for row in events:
        for kind in ("request", "response"):
            if row.get(f"{kind}_body_status") != "complete":
                missing.append(f"http.{row['event_id']}.{kind}_body")
    artifacts = []
    trace_found = False
    vectors = 0
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.name in (
            "manifest.json",
            "provenance.json",
            "evidence-index.json",
        ):
            continue
        name = path.relative_to(output).as_posix()
        artifacts.append({"path": name, "sha256": sha(path)})
        if name.startswith("evidence/vectors/") and path.suffix == ".npz":
            vectors += 1
        if name.startswith("evidence/trace/") and path.suffix == ".json":
            value = json.loads(path.read_bytes())
            if path.name == "run.json":
                trace_found = value.get("status") != "running" and not value.get("truncated")
            if value.get("truncated"):
                missing.append(f"trace.{name}")
    if not trace_found:
        missing.append("finished_trace")
    embeddings = sum(
        row["operation"] == "embedding" and row["outcome"] == "completed"
        for row in usage.get("model_calls", [])
    )
    if vectors < embeddings:
        missing.append("query_vectors")
    result = output / "result.json"
    if not result.is_file():
        missing.append("result_sha256")
    return {
        "schema_version": "rtpeval_generation_evidence_1",
        "group_id": manifest["group_id"],
        "run_id": manifest["run_id"],
        "version": manifest["version"],
        "input_sha256": manifest["input_sha256"],
        "result_sha256": sha(result) if result.is_file() else None,
        "source_revision": manifest["source_revision"],
        "outcome": usage["outcome"],
        "runtime_policy_sha256": manifest["runtime_policy_sha256"],
        "adapter_coverage": adapter_coverage,
        "qualified_four_version_batch": False,
        "collection_status": "partial" if missing or diagnostics else "available",
        "missing_fields": missing,
        "diagnostics": diagnostics,
        "http_events": events,
        "artifacts": artifacts,
        "scope": "Credential-filtered local observations; no proof of external receipt or billing.",
    }


def finish_trace_if_running(tracer, usage):
    """Retain runner-owned finalization; optional trace IO cannot fail planning."""
    try:
        path = tracer.run_directory / "run.json"
        if path.is_file() and json.loads(path.read_bytes()).get("status") == "running":
            outcome = usage["outcome"] if usage else "incomplete"
            tracer.finish(status=outcome, requirements=None, tool_usage={}, outcome=None)
    except Exception:
        # The inventory reports a missing/unfinished trace instead of adopting false evidence.
        pass
