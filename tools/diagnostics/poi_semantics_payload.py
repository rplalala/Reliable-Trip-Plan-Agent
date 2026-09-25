"""Offline measurements of the actual semantic and Repair serializers; no clients."""

import json

from backend.app.runtime.config_loader import load_runtime_config
from backend.app.services.poi_semantics import semantic_input_tokens, serialize_semantic_input
from backend.app.versions.v3.repair_projection import build_repair_input
from backend.tests.services.test_poi_semantics import Model
from backend.tests.versions.v3.test_validation import contract, place
from tools.diagnostics.repair_payload import enriched_fixture, fixture, retime_fixture


def measurements():
    import asyncio

    from backend.app.schemas.poi_semantics import POISemanticAssessment

    config = load_runtime_config()
    result = []
    for count, length in ((1, 0), (16, 0), (32, 0), (32, 5000)):
        places = [place(str(i), formatted_address="address " * length) for i in range(count)]
        payload = serialize_semantic_input(places, contract())
        tokens = semantic_input_tokens(payload, config.main_generation.framing_tokens)
        result.append(
            dict(
                sample=f"semantic_{count}_address_{length}",
                total=tokens,
                ceiling=config.poi_semantics.input_tokens,
                outcome="pre_send_overflow"
                if tokens > config.poi_semantics.input_tokens
                else "within_ceiling",
            )
        )
    for label, args in (
        ("repair_32", fixture(3, 32)),
        ("repair_long_requirements_32", enriched_fixture()),
        ("repair_retime", retime_fixture()),
    ):
        args = list(args)
        raw = asyncio.run(
            Model().generate_poi_semantics_structured(
                user_prompt=serialize_semantic_input(args[3].places, args[3].contract)
            )
        )
        args[3] = args[3].model_copy(
            update={
                "semantic_assessments": tuple(
                    POISemanticAssessment.model_validate(r) for r in raw["assessments"]
                )
            }
        )
        for later in (False, True):
            pending = (
                ()
                if not later
                else (
                    {
                        "group_id": "synthetic_pending",
                        "status": "pending",
                        "dates": [str(args[0].days[0].date)],
                        "base": "synthetic_hash",
                        "edits": [],
                        "proposal_days": [args[0].days[0].model_dump(mode="json")],
                        "reason": "deduplication_awaiting_atomic_compensation",
                    },
                )
            )
            _, _, counts = build_repair_input(
                *args, pending_groups=pending, feedback={"kind": "no_progress"} if later else None
            )
            result.append(dict(sample=label + ("_pending" if later else "_initial"), **counts))
    args = list(retime_fixture())
    args[0] = args[0].model_copy(deep=True)
    args[0].days[0].activities[0].notes = "protected context " * 140000
    try:
        _, _, counts = build_repair_input(*args)
        result.append(dict(sample="protected_pressure", outcome="within_ceiling", **counts))
    except ValueError as exc:
        result.append(
            dict(sample="protected_pressure", outcome=str(exc), **getattr(exc, "counts", {}))
        )
    return result


if __name__ == "__main__":
    print(json.dumps(measurements(), indent=2))
