"""Researcher-only descriptive pair outcomes, separate from automatic quality scores."""

from datetime import datetime

from .human_answers import validate_answers
from .human_tasks import DIMENSIONS
from .intake import VERSIONS
from .records import canonical_digest, require

PAIRS = tuple((left, right) for i, left in enumerate(VERSIONS) for right in VERSIONS[i + 1 :])


def _outcomes(answer, mapping, dimension):
    response = answer["responses"][dimension] if answer else {"status": "missing"}
    if response["status"] != "ranked":
        return {"status": response["status"], "reason": response.get("reason"), "pairs": {}}
    positions = {
        mapping["labels"][label]: position
        for position, group in enumerate(response["tie_groups"])
        for label in group
    }
    pairs = {
        f"{left}_vs_{right}": "tie"
        if positions[left] == positions[right]
        else "win"
        if positions[left] < positions[right]
        else "loss"
        for left, right in PAIRS
    }
    return {"status": "ranked", "pairs": pairs}


def build_human_report(public, private, bundles, *, generated_at):
    """Validate all material before selecting revisions and joining the private mapping."""
    try:
        require(
            datetime.fromisoformat(generated_at).utcoffset() is not None,
            "generated_at",
            "Expected offset-aware generation timestamp",
        )
    except (ValueError, TypeError) as exc:
        require(False, "generated_at", f"Invalid generation timestamp: {exc}")
    imported = validate_answers(public, private, bundles)
    effective = {a["task_id"]: a for a in imported["effective"]}
    task_results = []
    aggregates = {
        d: {f"{a}_vs_{b}": {"win": 0, "tie": 0, "loss": 0, "available": 0} for a, b in PAIRS}
        for d in DIMENSIONS
    }
    missingness = {
        d: {s: 0 for s in ("ranked", "unable_to_judge", "not_applicable", "missing", "draft_only")}
        for d in DIMENSIONS
    }
    draft_ids = {a["task_id"] for a in imported["records"] if a["state"] == "draft"}
    for mapping in private["tasks"]:
        tid = mapping["task_id"]
        selected = effective.get(tid)
        dimensions = {d: _outcomes(selected, mapping, d) for d in DIMENSIONS}
        if not selected and tid in draft_ids:
            for outcome in dimensions.values():
                outcome["status"] = "draft_only"
        task_results.append(
            {
                "task_id": tid,
                "group_id": mapping["group_id"],
                "answer_revision": selected["answer_revision"] if selected else None,
                "answer_hash": canonical_digest(selected) if selected else None,
                "dimensions": dimensions,
            }
        )
        if "duplicate_of" not in mapping:
            for d, outcome in dimensions.items():
                missingness[d][outcome["status"]] += 1
                for pair, verdict in outcome["pairs"].items():
                    aggregates[d][pair][verdict] += 1
                    aggregates[d][pair]["available"] += 1
    duplicates = []
    for i, mapping in enumerate(private["tasks"]):
        if "duplicate_of" not in mapping:
            continue
        original = task_results[mapping["duplicate_of"]]
        duplicate = task_results[i]
        dimensions = {}
        for d in DIMENSIONS:
            left, right = original["dimensions"][d]["pairs"], duplicate["dimensions"][d]["pairs"]
            comparable = set(left) & set(right)
            agreeing = sum(left[p] == right[p] for p in comparable)
            dimensions[d] = {
                "agreeing_pairs": agreeing,
                "comparable_pairs": len(comparable),
                "agreement": agreeing / len(comparable) if comparable else None,
            }
        duplicates.append(
            {
                "original_task_id": original["task_id"],
                "duplicate_task_id": duplicate["task_id"],
                "dimensions": dimensions,
            }
        )
    report = {
        "schema_version": "rtpeval_human_report_1",
        "generated_at": generated_at,
        "batch_id": public["batch_id"],
        "batch_revision": public["batch_revision"],
        "presentation_id": public["presentation_id"],
        "presentation_hash": public["presentation_hash"],
        "mapping_hash": private["content_hash"],
        "source_hashes": private["preparation"]["source_hashes"],
        "main_task_count": sum("duplicate_of" not in t for t in private["tasks"]),
        "tasks": task_results,
        "aggregates": aggregates,
        "missingness": missingness,
        "duplicate_consistency": duplicates,
        "retained_answers": imported["records"],
        "limitations": [
            "Pairs within a task are correlated",
            "Descriptive within-rater consistency only",
        ],
    }
    report["content_hash"] = canonical_digest(report)
    return report
