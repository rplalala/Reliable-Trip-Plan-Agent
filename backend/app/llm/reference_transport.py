"""Project the existing canonical model inputs at the provider boundary."""

import json

from backend.model_references import ShortReferences

PLACE_FIELDS = dict.fromkeys(
    (
        "place_id",
        "source_place_id",
        "origin_place_id",
        "destination_place_id",
        "place_ids",
        "required_canonical_ids",
        "optional_canonical_ids",
        "candidate_ids",
        "removable_place_ids",
    ),
    "p",
)
REPAIR_FIELDS = {
    **PLACE_FIELDS,
    **dict.fromkeys(
        (
            "activity_id",
            "activity_ids",
            "from_activity_id",
            "to_activity_id",
            "trigger_activity_ids",
            "changed_activity_ids",
            "activated_by",
            "window_roots",
            "root_id",
            "root_activity_id",
            "affected_adjacency",
            "fragment_id",
            "related_activity_ids",
            "lineage",
        ),
        "a",
    ),
    **dict.fromkeys(
        ("target_id", "target_ids", "finding_id", "parent_id", "deferred_review_target_ids"), "t"
    ),
}


def primary_references(prompt):
    """Parse only application-owned JSON sections, preserving original request text."""
    sections = []
    boundary = prompt.rfind("</travel_requirements>")
    boundary = boundary + len("</travel_requirements>") if boundary >= 0 else 0
    for marker in (
        "<external_evidence>\n",
        "<requirement_conflicts>\n",
        "<official_current_evidence>\n",
        "Planning candidate supply contract:\n",
    ):
        start = prompt.rfind(marker, boundary)
        if start >= 0:
            start += len(marker)
            value, size = json.JSONDecoder().raw_decode(prompt[start:])
            sections.append((start, start + size, value))
    if not sections:
        return None, prompt
    values = [value for _, _, value in sections]
    route_ids = [
        row[field]
        for value in values
        if isinstance(value, dict)
        for row in value.get("routes", {}).get("directed_facts", [])
        for field in ("origin", "destination")
    ]
    refs = ShortReferences(
        [*values, {"place_ids": route_ids}],
        PLACE_FIELDS,
        keyed={"landmarks": "p", "review_evidence_relations": "p"},
    )

    def encode(value):
        value = refs.encode(value)
        if isinstance(value, dict):
            for row in value.get("routes", {}).get("directed_facts", []):
                for field in ("origin", "destination"):
                    row[field] = refs.forward["p"][row[field]]
        if isinstance(value, list):
            for row in value:
                if isinstance(row, dict) and row.get("place_id_or_name") in refs.forward["p"]:
                    row["place_id_or_name"] = refs.forward["p"][row["place_id_or_name"]]
        return value

    for start, end, value in sorted(sections, reverse=True):
        prompt = prompt[:start] + json.dumps(encode(value), ensure_ascii=True) + prompt[end:]
    return refs, prompt


def profile_references(prompt):
    """Reviews already use application-owned short review_N identifiers."""
    try:
        value = json.loads(prompt)
    except json.JSONDecodeError:
        return None, prompt
    refs = ShortReferences(value, {"place_id": "p"})
    return refs, json.dumps(refs.encode(value), ensure_ascii=True)


def repair_references(prompt):
    value = json.loads(prompt)
    refs = ShortReferences(
        value, REPAIR_FIELDS, keyed={"scheduled_coordinates": "p", "lineage": "a"}
    )
    return refs, json.dumps(refs.encode(value), ensure_ascii=True, separators=(",", ":"))
