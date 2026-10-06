"""Prepare evaluation request plans or replay snapshots; no live acquisition command."""

import argparse
import json
from pathlib import Path

from .intake import _read, load_batch
from .snapshot import build_evidence_plan, build_identity_plan, identity_evidence, load_snapshot


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("identity-plan", "evidence-plan"):
        sub = commands.add_parser(name)
        sub.add_argument("manifest")
        sub.add_argument("--paired", action="store_true")
        if name == "evidence-plan":
            sub.add_argument("identity_report")
            sub.add_argument(
                "route_contexts", help="JSON object with contexts array; empty allowed"
            )
    for name in ("replay", "identity-evidence"):
        sub = commands.add_parser(name)
        sub.add_argument("directory")
        sub.add_argument("--expected-plan")
        if name == "identity-evidence":
            sub.add_argument(
                "--historical",
                action="store_true",
                help="Derive the original evidence wire for historical report replay",
            )
    args = parser.parse_args(argv)
    try:
        if args.command.endswith("plan"):
            intake = load_batch(args.manifest)
            if args.command == "identity-plan":
                output = build_identity_plan(intake, paired=args.paired)
            else:
                report, _ = _read(Path(args.identity_report))
                contexts, _ = _read(Path(args.route_contexts))
                output = build_evidence_plan(
                    intake, report, contexts["contexts"], paired=args.paired
                )
        else:
            expected = _read(Path(args.expected_plan))[0] if args.expected_plan else None
            snapshot = load_snapshot(args.directory, expected_plan=expected)
            output = (
                identity_evidence(snapshot, historical=args.historical)
                if args.command == "identity-evidence"
                else snapshot
            )
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(
            json.dumps(
                {
                    "status": "needs_snapshot_correction",
                    "error_type": type(exc).__name__,
                    "explanation": str(exc),
                }
            )
        )
        return 2
    print(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
