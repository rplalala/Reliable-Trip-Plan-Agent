"""Replay opening metrics using local batch, identity and frozen snapshot preparation."""

import argparse
import json
from pathlib import Path

from .intake import _read, load_batch
from .opening import REPORT_VERSION, score_opening
from .records import MaterialError


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Delivered batch manifest")
    parser.add_argument("identity_report", help="Replayed independent identity report JSON")
    parser.add_argument("snapshot_directory", help="Frozen evidence-phase snapshot directory")
    parser.add_argument("--context", help="Optional independently reviewed IANA time context JSON")
    parser.add_argument("--expected-plan", help="Optional trusted full acquisition plan JSON")
    parser.add_argument("--opening-judgment", help="Saved source-bound access model material JSON")
    parser.add_argument("--paired", action="store_true", help="Also score available V3 projections")
    args = parser.parse_args(argv)
    try:
        intake = load_batch(args.manifest)
        identity, identity_hash = _read(Path(args.identity_report))
        context, context_hash = _read(Path(args.context)) if args.context else (None, None)
        expected, expected_hash = (
            _read(Path(args.expected_plan)) if args.expected_plan else (None, None)
        )
        judgment, judgment_hash = (
            _read(Path(args.opening_judgment)) if args.opening_judgment else (None, None)
        )
        result = score_opening(
            intake,
            identity,
            args.snapshot_directory,
            context,
            paired=args.paired,
            expected_plan=expected,
            opening_judgment=judgment,
        ).to_dict()
        result["preparation_file_sha256"] = {
            "identity": identity_hash,
            "context": context_hash,
            "expected_plan": expected_hash,
        }
        if judgment is not None:
            result["preparation_file_sha256"]["opening_judgment"] = judgment_hash
    except MaterialError as exc:
        result = {
            "schema_version": REPORT_VERSION,
            "status": "needs_material_correction",
            "results": [],
            "diagnostics": [exc.diagnostic],
        }
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
