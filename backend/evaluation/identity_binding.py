"""Explicit applicability of complete V0 judgment sets across batch envelopes."""

from .records import canonical_digest

RESULT_VERSION = "rtpeval_identity_model_result_2"


def _facts(value):
    if isinstance(value, list):
        return [_facts(item) for item in value]
    if not isinstance(value, dict):
        return value
    return {
        key: ({"sha256": item["sha256"]} if key == "raw" and item else _facts(item))
        for key, item in value.items()
        if key not in ("reference_id", "observation_id")
    }


def case_bindings(intake, cases):
    """Bind source occurrences, claims, candidate facts and captured provenance."""
    groups = {group["group_id"]: group for group in intake["inventory"]}
    bindings = {}
    for case in cases:
        source = case["source"]
        group = groups[source["group_id"]]
        if case["kind"] == "requirement_subject":
            spec = group["requirement_spec"]
            relevant = {
                "subject": next(
                    s for s in spec["subjects"] if s["subject_id"] == source["subject_id"]
                ),
                "obligations": [
                    o for o in spec["obligations"] if o.get("subject_ref") == source["subject_id"]
                ],
                "input_sha256": group["input_sha256"],
            }
            anchor = {"group_id": source["group_id"], "subject_id": source["subject_id"]}
        else:
            anchor = {
                key: source[key]
                for key in (
                    "group_id",
                    "run_id",
                    "artifact_sha256",
                    "pointer",
                    "projection_version",
                )
            }
            relevant = None
        key = canonical_digest(
            {"anchor": anchor, "kind": case["kind"], "projection": case["projection"]}
        )
        if key in bindings:
            raise ValueError("Duplicate V0 binding occurrence")
        bindings[key] = {
            "reference_id": case["reference_id"],
            "facts": canonical_digest(
                {
                    "claim": case["claim"],
                    "candidates": case["candidates"],
                    "observation": _facts(case["observation"]),
                    "requirement": relevant,
                }
            ),
        }
    return bindings


def reference_mapping(source_intake, source_cases, intake, cases):
    old, current = case_bindings(source_intake, source_cases), case_bindings(intake, cases)
    if old.keys() != current.keys() or any(
        old[key]["facts"] != current[key]["facts"] for key in old
    ):
        raise ValueError("V0 judgment binding facts changed")
    return {old[key]["reference_id"]: current[key]["reference_id"] for key in old}
