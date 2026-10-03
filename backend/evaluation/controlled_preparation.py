"""Source-linked V3-only intake for reuse of independent evaluation scorers."""

import hashlib
import json
from copy import deepcopy

from backend.app.versions.v3.state import V3Outcome

from .controlled_models import ControlledCase
from .intake import _requirements
from .preparation import _review_provenance
from .projection import project
from .records import IntakeResult, canonical_digest, freeze, require


def prepare_controlled_case(value, replay, requirement_spec):
    """Project executed sources, without copying producer quality verdicts into checks."""
    saved = ControlledCase.model_validate(deepcopy(value))
    replay, spec = deepcopy(replay), deepcopy(requirement_spec)
    digest = canonical_digest(saved.model_dump(mode="json"))
    require(
        replay.get("schema_version") == "rtpeval_controlled_replay_1"
        and replay.get("case_hash") == digest
        and (replay.get("case_id"), replay.get("revision")) == (saved.case_id, saved.revision),
        "replay",
        "Foreign/stale controlled replay",
    )
    replay_hash = canonical_digest({k: v for k, v in replay.items() if k != "replay_hash"})
    require(replay.get("replay_hash") == replay_hash, "replay", "Replay content hash mismatch")
    require(
        replay.get("status") == "complete" and not replay.get("diagnostics"),
        "replay",
        "Execution material errors cannot enter quality scoring",
    )
    outcome = V3Outcome.model_validate(replay["outcome"]).model_dump(mode="json")
    require(
        outcome["draft"] == saved.primary.model_dump(mode="json"),
        "replay",
        "Replay draft differs from frozen primary",
    )
    input_hash = canonical_digest(saved.original_input)
    _requirements(spec, saved.case_id, input_hash, saved.original_input)
    _review_provenance(spec["review"], "requirement_spec.review")
    result = {"system_version": "v3", "itinerary": outcome["final_primary"], "v3": outcome}
    raw = json.dumps(
        result, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    )
    result_hash = hashlib.sha256(raw.encode()).hexdigest()
    batch_id = "controlled:" + saved.case_id
    context = {
        "batch_id": batch_id,
        "group_id": saved.case_id,
        "run_id": saved.case_id + ":" + replay_hash[:16],
        "artifact_sha256": result_hash,
    }
    optional = {
        label: project(outcome[label], context, "/v3/" + label, version="v3")
        for label in ("draft", "final_primary")
    }
    return IntakeResult(
        "accepted",
        freeze(
            {
                "schema_version": "rtpeval_controlled_preparation_1",
                "batch_id": batch_id,
                "revision": saved.revision,
                "case_hash": digest,
                "replay_hash": replay_hash,
                "source_hashes": {
                    "case": digest,
                    "replay": replay_hash,
                    "input": input_hash,
                    "requirement_spec": canonical_digest(spec),
                },
                "material_diagnostics": [],
                "projection_diagnostics": [],
                "track_availability": {"quality_preparation": True},
                "inventory": [
                    {
                        "group_id": saved.case_id,
                        "input": saved.original_input,
                        "input_sha256": input_hash,
                        "requirement_spec": spec,
                        "requirement_spec_sha256": canonical_digest(spec),
                        "protected_intervals": [
                            o for o in spec["obligations"] if o["kind"] == "protected_time"
                        ],
                        "runs": {
                            "v3": {
                                "final": project(result["itinerary"], context, version="v3"),
                                "optional": optional,
                                "paired_available": True,
                            }
                        },
                    }
                ],
                "result_sources": {
                    "schema_version": "rtpeval_v3_result_sources_1",
                    "batch_id": batch_id,
                    "batch_revision": saved.revision,
                    "records": [
                        {
                            "group_id": saved.case_id,
                            "run_id": context["run_id"],
                            "input_sha256": input_hash,
                            "result_sha256": result_hash,
                            "raw_utf8": raw,
                        }
                    ],
                },
            }
        ),
    )
