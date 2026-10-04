"""Strict answer import with explicit revisions and frozen presentation linkage."""

from datetime import datetime

from .human_tasks import DIMENSIONS, LABELS
from .intake import VERSIONS
from .records import canonical_digest, require

IDENTITY_FIELDS = (
    "batch_id",
    "batch_revision",
    "presentation_id",
    "presentation_hash",
    "rater_ref",
)
ANSWER_FIELDS = set(IDENTITY_FIELDS) | {
    "answer_schema_version",
    "task_id",
    "answer_revision",
    "updated_at",
    "state",
    "responses",
}


def validate_presentation(public, private):
    """Check researcher-frozen content and exact anonymous version associations."""
    require(
        isinstance(public, dict) and isinstance(private, dict), "presentation", "Expected objects"
    )
    require(
        public.get("schema_version") == "rtpeval_human_package_1"
        and private.get("schema_version") == "rtpeval_human_mapping_1",
        "presentation",
        "Unsupported presentation wire",
    )
    require(
        public.get("presentation_hash")
        == canonical_digest({k: v for k, v in public.items() if k != "presentation_hash"}),
        "presentation",
        "Public presentation hash mismatch",
    )
    require(
        private.get("public_sha256") == canonical_digest(public)
        and private.get("content_hash")
        == canonical_digest({k: v for k, v in private.items() if k != "content_hash"}),
        "mapping",
        "Frozen mapping linkage mismatch",
    )
    require(
        public.get("dimensions") == list(DIMENSIONS), "dimensions", "Unsupported ranking dimensions"
    )
    tasks, mappings = public.get("tasks"), private.get("tasks")
    require(
        isinstance(tasks, list)
        and tasks
        and isinstance(mappings, list)
        and len(tasks) == len(mappings),
        "tasks",
        "Frozen task count mismatch",
    )
    ids = set()
    for i, (task, mapping) in enumerate(zip(tasks, mappings, strict=True)):
        tid = task.get("task_id")
        require(
            isinstance(tid, str) and tid not in ids and mapping.get("task_id") == tid,
            "tasks",
            "Invalid/repeated task linkage",
        )
        ids.add(tid)
        labels = mapping.get("labels")
        require(
            isinstance(labels, dict)
            and set(labels) == set(LABELS)
            and set(labels.values()) == set(VERSIONS)
            and set(task.get("plans", {})) == set(LABELS),
            tid,
            "Expected exact four-plan permutation",
        )
        if "duplicate_of" in mapping:
            original = mapping["duplicate_of"]
            require(
                type(original) is int
                and 0 <= original < i
                and "duplicate_of" not in mappings[original]
                and mappings[original]["group_id"] == mapping["group_id"],
                tid,
                "Invalid duplicate linkage",
            )


def _answer(record, public, task_ids):
    require(
        isinstance(record, dict) and set(record) == ANSWER_FIELDS,
        "answer",
        "Unexpected/missing answer fields",
    )
    require(
        record.get("answer_schema_version") == "rtpeval_human_answer_1",
        "answer",
        "Unsupported answer schema",
    )
    require(
        all(record[k] == public[k] for k in IDENTITY_FIELDS),
        "answer",
        "Stale/unlinked presentation or rater",
    )
    require(record["task_id"] in task_ids, "answer", "Unknown task")
    revision = record["answer_revision"]
    require(type(revision) is int and revision > 0, "answer_revision", "Expected positive revision")
    try:
        require(
            datetime.fromisoformat(record["updated_at"]).utcoffset() is not None,
            "updated_at",
            "Expected offset-aware answer timestamp",
        )
    except (ValueError, TypeError) as exc:
        require(False, "updated_at", f"Invalid timestamp: {exc}")
    state = record["state"]
    require(state in ("draft", "submitted"), "state", "Unsupported answer state")
    responses = record["responses"]
    require(
        isinstance(responses, dict)
        and set(responses) <= set(DIMENSIONS)
        and (state == "draft" or set(responses) == set(DIMENSIONS)),
        "responses",
        "Submitted answer requires all three dimensions",
    )
    for dimension, response in responses.items():
        require(
            isinstance(response, dict) and set(response) <= {"status", "tie_groups", "reason"},
            dimension,
            "Unsupported response fields",
        )
        if "reason" in response:
            require(isinstance(response["reason"], str), dimension, "Expected reason text")
        status = response.get("status")
        require(
            status in ("ranked", "unable_to_judge", "not_applicable", "pending")
            and (status != "pending" or state == "draft"),
            dimension,
            "Unsupported response status",
        )
        if status == "ranked":
            groups = response.get("tie_groups")
            require(
                isinstance(groups, list) and all(isinstance(g, list) and g for g in groups),
                dimension,
                "Expected nonempty tie groups",
            )
            labels = [label for group in groups for label in group]
            require(
                all(isinstance(label, str) and label in LABELS for label in labels)
                and len(labels) == len(set(labels))
                and (state == "draft" or set(labels) == set(LABELS)),
                dimension,
                "Ranking must partition all four labels exactly once",
            )
        else:
            require(
                "tie_groups" not in response, dimension, "Unassessable response cannot rank labels"
            )


def validate_answers(public, private, bundles):
    """Import complete bundles atomically; retain revisions and select newest submissions."""
    validate_presentation(public, private)
    require(isinstance(bundles, list), "bundles", "Expected explicit answer bundle array")
    records = {}
    tasks = {t["task_id"] for t in public["tasks"]}
    for bundle in bundles:
        require(
            isinstance(bundle, dict)
            and set(bundle) == {"schema_version", "answers"}
            and bundle["schema_version"] == "rtpeval_human_answers_1"
            and isinstance(bundle["answers"], list),
            "bundle",
            "Unsupported answer bundle",
        )
        for record in bundle["answers"]:
            _answer(record, public, tasks)
            key = (record["task_id"], record["rater_ref"], record["answer_revision"])
            require(
                key not in records or records[key] == record,
                "answer_revision",
                "Conflicting content at the same revision",
            )
            records[key] = record
    ordered = [records[k] for k in sorted(records)]
    effective = {}
    for record in ordered:
        if record["state"] == "submitted":
            effective[record["task_id"]] = record
    return {
        "schema_version": "rtpeval_human_import_1",
        "records": ordered,
        "effective": [effective[k] for k in sorted(effective)],
    }
