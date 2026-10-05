"""Small synthetic evidence packages; not a formal controlled corpus."""

import asyncio
import json

from backend.evaluation.controlled_preparation import prepare_controlled_case
from backend.evaluation.identity import identity_references
from backend.evaluation.identity import resolve_legacy_identities as resolve_identities
from backend.evaluation.records import canonical_digest
from backend.evaluation.routes import prepare_routes
from backend.evaluation.snapshot import AcquisitionPolicy, Response, acquire_snapshot
from backend.tests.evaluation.test_controlled_preparation import requirements
from backend.tests.evaluation.test_identity import details
from backend.tests.versions.v3.test_validation import NOW


def material(
    value, execution, root, *, spec=None, hours=None, hours_by_place=None, route_fields=None
):
    spec = spec or requirements(value)
    prepared = prepare_controlled_case(value, execution, spec).to_dict()
    refs = identity_references(prepared)
    observations = [
        details(r, r["name"], place_id=r["claimed_place_id"], address="Fixture") for r in refs
    ]
    evidence = {
        "schema_version": "rtpeval_identity_evidence_1",
        "batch_id": prepared["batch_id"],
        "batch_revision": prepared["revision"],
        "records": observations,
    }
    reviews = {
        "schema_version": "rtpeval_identity_reviews_1",
        "batch_id": prepared["batch_id"],
        "batch_revision": prepared["revision"],
        "records": [
            {
                "reference_id": r["reference_id"],
                "evidence_hash": canonical_digest(o),
                "revision": 1,
                "decision": "confirm",
                "canonical_place_id": r["claimed_place_id"],
                "reviewer_ref": "synthetic-independent-reviewer",
                "reviewed_at": NOW.isoformat(),
                "rationale": "Synthetic independent identity evidence",
            }
            for r, o in zip(refs, observations, strict=True)
        ],
    }
    audit = {
        "schema_version": "rtpeval_identity_audit_1",
        "batch_id": prepared["batch_id"],
        "batch_revision": prepared["revision"],
        "seed": "synthetic",
        "sample_count": 1,
    }
    identity = resolve_identities(prepared, evidence, reviews, audit).to_dict()
    context = {
        "schema_version": "rtpeval_schedule_context_1",
        "batch_id": prepared["batch_id"],
        "revision": "1",
        "groups": [
            {
                "group_id": value["case_id"],
                "input_sha256": prepared["inventory"][0]["input_sha256"],
                "timezone": "UTC",
                "source_ref": "synthetic-independent-timezone",
                "reviewer_ref": "reviewer",
                "reviewed_at": NOW.isoformat(),
            }
        ],
    }
    coords = {
        "schema_version": "rtpeval_route_coordinates_1",
        "batch_id": prepared["batch_id"],
        "revision": "1",
        "records": [
            {
                "place_id": pid,
                "latitude": 0,
                "longitude": 0,
                "evidence_sha256": "a" * 64,
                "source_ref": "synthetic-independent-coordinates",
                "reviewer_ref": "reviewer",
                "reviewed_at": NOW.isoformat(),
            }
            for pid in sorted({r["canonical_place_id"] for r in identity["records"]})
        ],
    }
    route_review = {
        "schema_version": "rtpeval_route_reviews_1",
        "batch_id": prepared["batch_id"],
        "revision": "1",
        "groups": [
            {
                "group_id": value["case_id"],
                "input_sha256": prepared["inventory"][0]["input_sha256"],
                "reviewer_ref": "reviewer",
                "reviewed_at": NOW.isoformat(),
                "status": "unrestricted",
            }
        ],
    }
    routes = prepare_routes(
        prepared,
        identity,
        context,
        route_reviews=route_review,
        coordinate_evidence=coords,
        paired=True,
    ).to_dict()
    assert routes["status"] == "complete", routes["diagnostics"]

    async def transport(request):
        if request["operation"] == "places_details":
            payload = {
                "id": request["parameters"]["place_id"],
                "timeZone": {"id": "UTC"},
                "regularOpeningHours": {"periods": [{"open": {"day": 0, "hour": 0, "minute": 0}}]},
            }
            if hours is not None:
                payload = {**payload, **hours}
            if hours_by_place:
                payload = {**payload, **hours_by_place.get(request["parameters"]["place_id"], {})}
        else:
            payload = [
                {
                    "originIndex": 0,
                    "destinationIndex": 0,
                    "status": {},
                    "condition": "ROUTE_EXISTS",
                    "duration": "600s",
                    "distanceMeters": 100,
                }
            ]
            if route_fields is not None:
                payload[0].update(route_fields)
                if payload[0].get("duration") is None:
                    payload[0].pop("duration", None)
        return Response(200, json.dumps(payload).encode())

    asyncio.run(
        acquire_snapshot(routes["evidence_plan"], root, transport, AcquisitionPolicy(max_sends=100))
    )
    return {
        "requirement_spec": spec,
        "identity_report": identity,
        "snapshot_directory": root,
        "schedule_context": context,
        "route_reviews": route_review,
        "coordinate_evidence": coords,
        "expected_plan": routes["evidence_plan"],
    }


def expectations(value, execution, *, targets=(), guards=()):
    return {
        "schema_version": "rtpeval_controlled_expectations_1",
        "case_id": value["case_id"],
        "case_hash": execution["case_hash"],
        "revision": "1",
        "reviewer_ref": "synthetic-reviewer",
        "reviewed_at": NOW.isoformat(),
        "rationale": "Synthetic development goals",
        "supporting_refs": ["synthetic:goals"],
        "targets": list(targets),
        "guards": list(guards),
    }
