"""Exact qualifying claim revisions and independent, source-bound human reviews."""

import copy

import pytest

from backend.evaluation.official_audit import build_audit_queue, report_audit
from backend.evaluation.records import canonical_digest
from backend.tests.evaluation.test_mechanism_report import selected
from backend.tests.versions.v1.test_official_web_integration import FakeWeb, _run, _service


def preparation():
    service, *_ = _service(FakeWeb())
    claim = _run(service).accepted_evidence[0].model_dump(mode="json")
    base = selected(version="v1").to_dict()
    run = base["runs"][0]
    link = {k: run[k] for k in ("group_id", "run_id", "version", "input_sha256", "result_sha256")}
    sha = canonical_digest(claim)
    capture = {
        **link,
        "schema_version": "rtpeval_mechanism_capture_1",
        "collection_status": "available",
        "catalog": [{"claim": claim, "claim_sha256": sha}],
        "prepared_calls": [],
        "occurrences": [
            {
                "occurrence_id": f"call:{i}",
                "reason": "model_input_submission",
                "source_refs": [claim["source_ref"]],
                "claim_links": [{"source_ref": claim["source_ref"], "claim_sha256": sha}],
                "round_index": i,
                "representation": {
                    "value_text": claim["value_text"],
                    "source_refs": [claim["source_ref"]],
                },
            }
            for i in (1, 2)
        ],
        "missing_fields": [],
        "diagnostics": [],
    }
    run["channels"]["capture"] = {
        "status": "available",
        "diagnostics": [],
        "records": [
            {
                **link,
                "channel": "capture",
                "content": capture,
                "content_sha256": canonical_digest(capture),
            }
        ],
    }
    return base


def test_repeated_submission_and_rule_are_one_claim_with_three_occurrences():
    base = preparation()
    capture = base["runs"][0]["channels"]["capture"]["records"][0]
    occurrence = copy.deepcopy(capture["content"]["occurrences"][0])
    occurrence.update(occurrence_id="rule:1", reason="rule_selection")
    capture["content"]["occurrences"].append(occurrence)
    capture["content_sha256"] = canonical_digest(capture["content"])
    queue = build_audit_queue(base)
    assert len(queue["units"]) == 1
    assert len(queue["units"][0]["occurrences"]) == 3
    assert queue["units"][0]["qualifying_reasons"] == ["model_input_submission", "rule_selection"]
    report = report_audit(queue)
    assert report["counts"]["qualifying"] == 1
    assert report["counts"]["reviewed"] == 0
    assert report["supported_fraction"]["fraction"] is None


def review(queue, verdict="supported"):
    return {
        "schema_version": "rtpeval_official_audit_reviews_1",
        "queue_sha256": queue["content_hash"],
        "records": [
            {
                "unit_sha256": queue["units"][0]["unit_sha256"],
                "verdict": verdict,
                "reviewer_ref": "independent-human",
                "reviewed_at": "2026-10-04T01:00:00Z",
                "rationale": "Checked exact admission claim and date scope.",
                "supporting_source_refs": ["https://alpha.example.org/admission"],
            }
        ],
    }


@pytest.mark.parametrize("verdict", ["supported", "contradicted", "scope_mismatch", "unavailable"])
def test_independent_verdict_retains_review_and_verifiable_coverage(verdict):
    queue = build_audit_queue(preparation())
    report = report_audit(queue, review(queue, verdict))
    assert report["status"] == "complete"
    assert report["counts"]["reviewed"] == 1
    assert report["counts"]["verifiable"] == (verdict != "unavailable")
    assert report["units"][0]["review"]["verdict"] == verdict


def test_stale_and_contradictory_reviews_fail_without_losing_qualifying_units():
    queue = build_audit_queue(preparation())
    for change in ("stale", "contradictory"):
        reviews = review(queue)
        if change == "stale":
            reviews["records"][0]["unit_sha256"] = "f" * 64
        else:
            other = copy.deepcopy(reviews["records"][0])
            other["verdict"] = "contradicted"
            reviews["records"].append(other)
        report = report_audit(queue, reviews)
        assert report["status"] == "needs_material_correction"
        assert report["counts"]["qualifying"] == 1
        assert report["units"][0]["review"] is None


def test_prepared_only_and_accepted_unused_are_excluded():
    base = preparation()
    row = base["runs"][0]["channels"]["capture"]["records"][0]
    row["content"]["occurrences"] = []
    row["content_sha256"] = canonical_digest(row["content"])
    queue = build_audit_queue(base)
    assert queue["units"] == []
    assert queue["runs"][0]["accepted_unused_count"] == 1


@pytest.mark.parametrize("change", ["hash", "claim", "representation", "occurrence_conflict"])
def test_invalid_capture_is_a_channel_error_and_cannot_qualify_claim(change):
    base = preparation()
    row = base["runs"][0]["channels"]["capture"]["records"][0]
    capture = row["content"]
    if change == "hash":
        row["content_sha256"] = "f" * 64
    else:
        if change == "claim":
            capture["catalog"][0]["claim"]["value_text"] = "Changed admission"
        elif change == "representation":
            capture["occurrences"][0]["representation"] = {}
        else:
            other = copy.deepcopy(capture["occurrences"][0])
            other["round_index"] = 3
            capture["occurrences"].append(other)
        row["content_sha256"] = canonical_digest(capture)
    queue = build_audit_queue(base)
    assert queue["units"] == []
    assert queue["runs"][0]["coverage"] == "needs_material_correction"


def test_partial_catalog_and_submission_remain_observed_coverage_not_full_population():
    base = preparation()
    row = base["runs"][0]["channels"]["capture"]["records"][0]
    row["content"].update(
        collection_status="partial", missing_fields=["rule_selection_observation"]
    )
    row["content_sha256"] = canonical_digest(row["content"])
    queue = build_audit_queue(base)
    assert len(queue["units"]) == 1
    assert queue["runs"][0]["coverage"] == "partial"
