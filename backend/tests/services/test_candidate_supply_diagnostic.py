"""Saved-evidence analysis stays offline and reports observed, not fixed, supply size."""

import asyncio
import json

from tools.diagnostics import candidate_supply


def test_saved_capture_analysis_uses_explicit_paths_and_actual_supply(tmp_path, monkeypatch):
    trace = tmp_path / "trace"
    (trace / "tools").mkdir(parents=True)
    events = [
        {"event": "semantic_candidate_admission", "payload": {
            "admitted_ids": ["one", "two", "three"], "omitted_ids": []}},
        {"event": "planning_supply_completed", "payload": {
            "selected_ids": ["one", "two", "three"], "details_attempts": []}},
    ]
    (trace / "events.jsonl").write_text("\n".join(json.dumps(x) for x in events))
    (tmp_path / "live_result.json").write_text(json.dumps({
        "trace_directory": str(trace), "result": {"rag_discovery": {"origins": {}}}}))
    generation = tmp_path / "generation.json"
    generation.write_text(json.dumps({"system_prompt": "system", "user_prompt": "user"}))
    monkeypatch.setattr(candidate_supply, "count_tokens", len)
    output = tmp_path / "analysis"
    asyncio.run(candidate_supply.analyze(tmp_path, output, None, generation))
    report = json.loads((output / "analysis.json").read_text())
    assert report["observed_union"] == 3
    assert report["payload"]["actual_supply_count"] == 3
    assert report["payload"]["actual_provider_input_tokens"] is None
    assert report["payload"]["actual_output_tokens"] is None
    assert report["input_hashes"] == {}
    assert all(row["total"] == row["unique"] == row["K"] ** 2 for row in report["routes"])
