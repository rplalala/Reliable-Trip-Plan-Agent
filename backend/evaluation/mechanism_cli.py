"""Offline selected-source mechanism and independent official-evidence audit commands."""

import argparse
import json
from pathlib import Path

from .intake import _read
from .mechanism_preparation import diagnostic, prepare_sources, read_batch_sources
from .mechanism_report import report_mechanism
from .official_audit import build_audit_queue, report_audit


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser(
        "prepare", help="Read four-version manifest or saved V3-only preparation"
    )
    source = prepare.add_mutually_exclusive_group(required=True)
    source.add_argument("--manifest")
    source.add_argument(
        "--selection", help="Ticket 11 preparation containing its exact result_sources"
    )
    prepare.add_argument("--observations", help="JSON {records: linked optional observation rows}")
    for name in ("report", "audit-queue", "audit-report"):
        command = commands.add_parser(name)
        command.add_argument("input")
        if name == "audit-report":
            command.add_argument("--reviews")
        command.add_argument("--output")
    prepare.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            observations = _read(Path(args.observations))[0]["records"] if args.observations else []
            if args.manifest:
                result = read_batch_sources(args.manifest, observations=observations).to_dict()
            else:
                selection, _ = _read(Path(args.selection))
                result = prepare_sources(
                    selection, selection["result_sources"], observations=observations
                ).to_dict()
        else:
            value, _ = _read(Path(args.input))
            if args.command == "report":
                result = report_mechanism(value)
            elif args.command == "audit-queue":
                result = build_audit_queue(value)
            else:
                reviews = _read(Path(args.reviews))[0] if args.reviews else None
                result = report_audit(value, reviews)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        result = {"status": "needs_material_correction", "diagnostics": [diagnostic(exc)]}
    raw = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    if args.output:
        Path(args.output).write_text(raw + "\n", encoding="utf-8")
    else:
        print(raw)
    return 2 if result.get("status") == "needs_material_correction" else 0


if __name__ == "__main__":
    raise SystemExit(main())
