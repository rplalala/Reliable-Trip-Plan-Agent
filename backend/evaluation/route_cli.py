"""Prepare or score same-day routes using local independent material only."""

import argparse
import json
from pathlib import Path

from .intake import _read, load_batch
from .records import MaterialError
from .routes import PREPARATION_VERSION, REPORT_VERSION, prepare_routes, score_routes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("prepare", "score"):
        sub = commands.add_parser(command)
        sub.add_argument("manifest", help="Delivered batch manifest")
        sub.add_argument("identity_report", help="Replayed independent identity report JSON")
        if command == "score":
            sub.add_argument("snapshot_directory", help="Frozen evidence-phase snapshot")
            sub.add_argument("--expected-plan", help="Optional trusted full snapshot plan JSON")
        sub.add_argument("--context", help="Reviewed IANA time context JSON")
        sub.add_argument("--occupancy-reviews", help="Independent occupancy correspondence JSON")
        sub.add_argument("--route-reviews", help="Source-linked Input mode review JSON")
        sub.add_argument(
            "--coordinates", help="Independent canonical coordinate/query options JSON"
        )
        sub.add_argument("--paired", action="store_true", help="Include available V3 projections")
    args = parser.parse_args(argv)
    try:
        intake = load_batch(args.manifest)
        identity, identity_hash = _read(Path(args.identity_report))
        files, hashes = {}, {"identity": identity_hash}
        for name, attribute in (
            ("schedule_context", "context"),
            ("occupancy_reviews", "occupancy_reviews"),
            ("route_reviews", "route_reviews"),
            ("coordinate_evidence", "coordinates"),
        ):
            path = getattr(args, attribute)
            files[name], hashes[attribute] = _read(Path(path)) if path else (None, None)
        if args.command == "prepare":
            result = prepare_routes(intake, identity, **files, paired=args.paired).to_dict()
        else:
            expected, hashes["expected_plan"] = (
                _read(Path(args.expected_plan)) if args.expected_plan else (None, None)
            )
            result = score_routes(
                intake,
                identity,
                args.snapshot_directory,
                **files,
                paired=args.paired,
                expected_plan=expected,
            ).to_dict()
        result["preparation_file_sha256"] = hashes
    except MaterialError as exc:
        result = {
            "schema_version": PREPARATION_VERSION if args.command == "prepare" else REPORT_VERSION,
            "status": "needs_material_correction",
            "results": [],
            "diagnostics": [exc.diagnostic],
        }
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
