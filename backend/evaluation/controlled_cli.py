"""Offline controlled V3 execution, independent preparation and outcome reporting."""

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from .controlled_batch import build_controlled_batch
from .controlled_preparation import prepare_controlled_case
from .controlled_replay import replay_controlled_case
from .controlled_report import build_controlled_report
from .identity import identity_references, resolve_identities
from .intake import _read
from .records import MaterialError
from .routes import prepare_routes
from .snapshot import build_identity_plan


def read(path):
    return _read(Path(path))[0] if path else None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    replay = commands.add_parser("replay", help="Execute frozen real V3 post-primary chain")
    replay.add_argument("case")
    prepare = commands.add_parser("prepare", help="Project real executed V3 sources")
    report = commands.add_parser("report", help="Report independent controlled outcomes")
    for command in (prepare, report):
        for name in ("case", "execution", "requirements"):
            command.add_argument(name)
    references = commands.add_parser(
        "identity-references", help="Export independent identity subjects"
    )
    references.add_argument("preparation")
    identity_plan = commands.add_parser(
        "identity-plan", help="Prepare independent identity acquisition requests"
    )
    identity_plan.add_argument("preparation")
    identity = commands.add_parser(
        "identity", help="Resolve separately collected identity observations"
    )
    for name in ("preparation", "evidence", "audit"):
        identity.add_argument(name)
    identity.add_argument("--reviews")
    evidence_plan = commands.add_parser(
        "evidence-plan", help="Prepare paired independent evidence acquisition"
    )
    evidence_plan.add_argument("preparation")
    evidence_plan.add_argument("identity")
    report.add_argument("expectations")
    report.add_argument("identity")
    report.add_argument("snapshot")
    options = {
        "schedule_context": "context",
        "occupancy_reviews": "occupancy-reviews",
        "route_reviews": "route-reviews",
        "coordinate_evidence": "coordinates",
    }
    for command in (evidence_plan, report):
        for option in options.values():
            command.add_argument("--" + option)
    report.add_argument("--expected-plan")
    report.add_argument("--correspondence-reviews")
    report.add_argument("--factual-reviews")
    report.add_argument("--generated-at")
    batch = commands.add_parser(
        "batch", help="Assemble linked per-case reports; retain unavailable units"
    )
    batch.add_argument("manifest")
    batch.add_argument("--generated-at")
    args = parser.parse_args(argv)
    try:
        if args.command == "replay":
            result = asyncio.run(replay_controlled_case(read(args.case)))
        elif args.command == "prepare":
            result = prepare_controlled_case(
                read(args.case), read(args.execution), read(args.requirements)
            ).to_dict()
        elif args.command == "identity-references":
            prepared = read(args.preparation)
            result = {
                "schema_version": "rtpeval_controlled_identity_references_1",
                "status": "complete",
                "batch_id": prepared["batch_id"],
                "batch_revision": prepared["revision"],
                "records": identity_references(prepared),
            }
        elif args.command == "identity-plan":
            result = build_identity_plan(read(args.preparation), paired=True)
        elif args.command == "identity":
            result = resolve_identities(
                read(args.preparation), read(args.evidence), read(args.reviews), read(args.audit)
            ).to_dict()
        elif args.command == "batch":
            result = build_controlled_batch(
                read(args.manifest),
                Path(args.manifest).resolve().parent,
                generated_at=args.generated_at or datetime.now(UTC).isoformat(),
            )
        else:
            files = {
                name: read(getattr(args, flag.replace("-", "_"))) for name, flag in options.items()
            }
            if args.command == "evidence-plan":
                result = prepare_routes(
                    read(args.preparation), read(args.identity), **files, paired=True
                ).to_dict()
            else:
                result = build_controlled_report(
                    read(args.case),
                    read(args.execution),
                    read(args.expectations),
                    read(args.requirements),
                    read(args.identity),
                    args.snapshot,
                    **files,
                    expected_plan=read(args.expected_plan),
                    correspondence_reviews=read(args.correspondence_reviews),
                    factual_reviews=read(args.factual_reviews),
                    generated_at=args.generated_at or datetime.now(UTC).isoformat(),
                )
    except (MaterialError, ValueError, KeyError, TypeError, OSError) as exc:
        result = {
            "status": "needs_material_correction",
            "diagnostics": [
                exc.diagnostic
                if isinstance(exc, MaterialError)
                else {"reason": "material_invalid", "explanation": str(exc)}
            ],
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
    return 0 if result.get("status", "complete") in {"complete", "accepted"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
