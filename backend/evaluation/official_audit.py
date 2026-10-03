"""Qualifying accepted official claims and exact-unit independent human review."""

from datetime import datetime

from .mechanism_preparation import (
    diagnostic,
    linkage,
    unique_rows,
    validated_preparation,
    value_dict,
)
from .records import canonical_digest, require, text

VERDICTS = ("supported", "contradicted", "scope_mismatch", "unavailable")
REASONS = ("model_input_submission", "rule_selection")


def _representation_refs(value):
    refs = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ("source_refs", "evidence_refs", "unresolved_conflict_source_refs"):
                require(
                    isinstance(child, list) and all(text(r) for r in child),
                    "representation",
                    "Invalid explicit refs",
                )
                refs.update(child)
            else:
                refs.update(_representation_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.update(_representation_refs(child))
    return refs


def _run_units(run):
    channel = run["channels"]["capture"]
    summary = {
        **linkage(run),
        "coverage": channel["status"],
        "diagnostics": list(channel["diagnostics"]),
        "accepted_count": None,
        "observed_accepted_count": None,
        "accepted_unused_count": None,
        "qualifying_count": None,
        "observed_qualifying_count": None,
        "prepared_calls": [],
        "capture_sha256s": [],
    }
    if run["version"] == "v0":
        summary.update(
            coverage="not_applicable",
            accepted_count=0,
            observed_accepted_count=0,
            accepted_unused_count=0,
            qualifying_count=0,
            observed_qualifying_count=0,
        )
        return [], summary
    if channel["status"] != "available":
        return [], summary
    try:
        captures = unique_rows(
            [r["content"] for r in channel["records"]],
            lambda r: (r["run_id"], r["schema_version"]),
            "capture",
        )
        # One attempt owns one normalized capture. Exact repeated delivery is harmless;
        # distinct contradictory captures for that attempt need producer correction.
        capture = captures[0]["value"]
        for record in channel["records"]:
            require(
                canonical_digest(record["content"]) == record["content_sha256"],
                "capture",
                "Capture content hash mismatch",
            )
        require(
            capture["schema_version"] == "rtpeval_mechanism_capture_1"
            and linkage(capture) == linkage(run),
            "capture",
            "Foreign capture envelope",
        )
        require(
            capture["collection_status"] in ("available", "partial", "unavailable"),
            "capture",
            "Invalid collection status",
        )
        catalogs = unique_rows(capture["catalog"], lambda r: r["claim_sha256"], "catalog")
        claims = {}
        for row in catalogs:
            item = row["value"]
            claim = item["claim"]
            require(isinstance(claim, dict), "catalog", "Typed claim object required")
            require(
                item["claim_sha256"] == canonical_digest(claim),
                "catalog",
                "Claim content hash mismatch",
            )
            for field in (
                "source_ref",
                "source_key",
                "place_id",
                "source_url",
                "supporting_excerpt",
                "claim_kind",
                "subject_scope",
                "temporal_basis",
                "authority_basis",
                "retrieved_at",
                "value_text",
            ):
                require(text(claim.get(field)), "catalog", f"Typed accepted claim missing {field}")
            require(
                claim["source_ref"].startswith("official_web:"),
                "catalog",
                "Accepted official reference required",
            )
            claims[item["claim_sha256"]] = claim
        occurrences = unique_rows(
            capture["occurrences"], lambda r: r["occurrence_id"], "occurrences"
        )
        units = {}
        calls = {r["call_id"]: r for r in capture["prepared_calls"]}
        for row in occurrences:
            occurrence = row["value"]
            if (
                occurrence["reason"] == "model_input_submission"
                and occurrence["occurrence_id"] in calls
            ):
                call = calls[occurrence["occurrence_id"]]
                require(
                    call["submitted"] is True
                    and call["representation"] == occurrence["representation"],
                    "occurrence",
                    "Submission contradicts prepared call",
                )
                occurrence = {
                    **occurrence,
                    "call_outcome": call.get("outcome", "unavailable"),
                    "call_error_type": call.get("error_type"),
                }
            require(
                occurrence["reason"] in REASONS and "representation" in occurrence,
                "occurrence",
                "Submission or selected-rule representation required",
            )
            require(
                isinstance(occurrence["source_refs"], list), "occurrence", "Explicit refs required"
            )
            representation_refs = _representation_refs(occurrence["representation"])
            require(
                set(occurrence["source_refs"]) <= representation_refs,
                "occurrence",
                "Occurrence refs are absent from submitted/selected representation",
            )
            require(
                isinstance(occurrence["claim_links"], list),
                "occurrence",
                "Exact claim links required",
            )
            claim_ids = [r["claim_sha256"] for r in occurrence["claim_links"]]
            require(len(claim_ids) == len(set(claim_ids)), "occurrence", "Duplicate claim link")
            for claim_link in occurrence["claim_links"]:
                sha, ref = claim_link["claim_sha256"], claim_link["source_ref"]
                require(
                    sha in claims
                    and claims[sha]["source_ref"] == ref
                    and ref in occurrence["source_refs"],
                    "occurrence",
                    "Unlinked claim revision",
                )
                unit = units.setdefault(
                    sha,
                    {
                        **linkage(run),
                        "claim_sha256": sha,
                        "claim": claims[sha],
                        "occurrences": [],
                        "qualifying_reasons": [],
                        "capture_sha256s": [canonical_digest(capture)],
                        "catalog_source_refs": next(
                            r["source_refs"] for r in catalogs if r["value"]["claim_sha256"] == sha
                        ),
                    },
                )
                unit["occurrences"].append(
                    {**occurrence, "observation_source_refs": row["source_refs"]}
                )
                if occurrence["reason"] not in unit["qualifying_reasons"]:
                    unit["qualifying_reasons"].append(occurrence["reason"])
        for unit in units.values():
            unit["qualifying_reasons"].sort()
            unit["unit_sha256"] = canonical_digest(unit)
        summary.update(
            coverage=capture["collection_status"],
            accepted_count=len(claims) if capture["collection_status"] == "available" else None,
            observed_accepted_count=len(claims),
            accepted_unused_count=(
                len(claims) - len(units) if capture["collection_status"] == "available" else None
            ),
            accepted_without_qualifying_observation_count=len(claims) - len(units),
            qualifying_count=len(units) if capture["collection_status"] == "available" else None,
            observed_qualifying_count=len(units),
            prepared_calls=capture["prepared_calls"],
            capture_sha256s=[canonical_digest(capture)],
            missing_fields=capture.get("missing_fields", []),
            capture_diagnostics=capture.get("diagnostics", []),
        )
        return list(units.values()), summary
    except (ValueError, KeyError, TypeError) as exc:
        summary.update(coverage="needs_material_correction", diagnostics=[diagnostic(exc)])
        return [], summary


def build_audit_queue(preparation):
    prepared = validated_preparation(preparation)
    units, runs = [], []
    for run in prepared["runs"]:
        rows, summary = _run_units(run)
        units.extend(rows)
        runs.append(summary)
    queue = {
        "schema_version": "rtpeval_official_audit_queue_1",
        "batch_id": prepared["batch_id"],
        "revision": prepared["revision"],
        "optional_diagnostics": prepared.get("optional_diagnostics", []),
        "preparation_sha256": canonical_digest(prepared),
        "units": units,
        "runs": runs,
        "interpretation": (
            "Application submission/selection; receipt, attention and truth are unverified."
        ),
    }
    queue["status"] = (
        "needs_material_correction"
        if any(r["coverage"] == "needs_material_correction" for r in runs)
        else "complete"
    )
    queue["content_hash"] = canonical_digest(queue)
    return queue


def report_audit(queue, reviews=None):
    queue = value_dict(queue)
    require(
        queue.get("schema_version") == "rtpeval_official_audit_queue_1"
        and queue.get("content_hash")
        == canonical_digest({k: v for k, v in queue.items() if k != "content_hash"}),
        "queue",
        "Audit queue content hash mismatch",
    )
    units = [{**u, "review": None} for u in queue["units"]]
    indexed = {u["unit_sha256"]: u for u in units}
    status = queue.get("status", "complete")
    diagnostics = [d for run in queue["runs"] for d in run["diagnostics"]]
    try:
        for unit in queue["units"]:
            require(
                unit["unit_sha256"]
                == canonical_digest({k: v for k, v in unit.items() if k != "unit_sha256"}),
                "queue",
                "Audit unit hash mismatch",
            )
        if reviews is not None:
            reviews = value_dict(reviews)
            require(
                reviews.get("schema_version") == "rtpeval_official_audit_reviews_1"
                and reviews.get("queue_sha256") == queue["content_hash"],
                "reviews",
                "Foreign/stale review queue",
            )
            for row in unique_rows(reviews["records"], lambda r: r["unit_sha256"], "reviews"):
                review = row["value"]
                require(review["unit_sha256"] in indexed, "reviews", "Foreign/stale review unit")
                require(review["verdict"] in VERDICTS, "reviews", "Unsupported review verdict")
                require(
                    all(text(review.get(k)) for k in ("reviewer_ref", "reviewed_at", "rationale")),
                    "reviews",
                    "Independent reviewer, time and rationale required",
                )
                stamp = datetime.fromisoformat(review["reviewed_at"].replace("Z", "+00:00"))
                require(
                    stamp.utcoffset() is not None, "reviews", "Offset-aware review time required"
                )
                require(
                    isinstance(review["supporting_source_refs"], list)
                    and bool(review["supporting_source_refs"])
                    and all(text(r) for r in review["supporting_source_refs"]),
                    "reviews",
                    "Independent supporting source references required",
                )
                indexed[review["unit_sha256"]]["review"] = {
                    **review,
                    "observation_source_refs": row["source_refs"],
                }
    except (ValueError, KeyError, TypeError) as exc:
        status, diagnostics = "needs_material_correction", [diagnostic(exc)]
        for unit in units:
            unit["review"] = None
    reviewed = [u["review"] for u in units if u["review"] is not None]
    verifiable = [r for r in reviewed if r["verdict"] != "unavailable"]
    verdict_counts = {v: sum(r["verdict"] == v for r in reviewed) for v in VERDICTS}
    population_complete = all(
        r["coverage"] in ("available", "not_applicable") for r in queue["runs"]
    )
    report = {
        "schema_version": "rtpeval_official_audit_report_1",
        "queue_sha256": queue["content_hash"],
        "reviews_sha256": canonical_digest(reviews) if reviews is not None else None,
        "status": status,
        "diagnostics": diagnostics,
        "units": units,
        "runs": queue["runs"],
        "counts": {
            "qualifying": len(units) if population_complete else None,
            "observed_qualifying": len(units),
            "reviewed": len(reviewed),
            "unreviewed": len(units) - len(reviewed),
            "verifiable": len(verifiable),
            **verdict_counts,
        },
        "review_coverage": {
            "numerator": len(reviewed),
            "denominator": len(units),
            "unit": "observed_qualifying_claim_revision",
            "qualifying_population_complete": population_complete,
        },
        "supported_fraction": {
            "numerator": verdict_counts["supported"] if verifiable else None,
            "denominator": len(verifiable) if verifiable else None,
            "unit": "independently_verifiable_reviewed_claim_revision",
            "fraction": verdict_counts["supported"] / len(verifiable) if verifiable else None,
        },
    }
    report["content_hash"] = canonical_digest(report)
    return report
