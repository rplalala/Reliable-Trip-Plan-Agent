"""Replay requirement and schedule metrics using local JSON preparation only."""

import argparse
import json
from pathlib import Path

from .intake import _read, load_batch
from .records import MaterialError
from .requirement_schedule import REPORT_VERSION, score_requirement_schedule


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Delivered batch manifest")
    parser.add_argument("identity_report", help="Replayed independent identity report JSON")
    parser.add_argument("--context", help="Optional independently reviewed IANA time context JSON")
    parser.add_argument("--occupancy-reviews", help="Optional source-linked occupancy review JSON")
    parser.add_argument("--paired", action="store_true", help="Also score available V3 projections")
    args = parser.parse_args(argv)
    intake = load_batch(args.manifest)
    try:
        identity, identity_hash = _read(Path(args.identity_report))
        context, context_hash = _read(Path(args.context)) if args.context else (None, None)
        reviews, review_hash = (
            _read(Path(args.occupancy_reviews)) if args.occupancy_reviews else (None, None)
        )
        report = score_requirement_schedule(intake, identity, context, reviews, paired=args.paired)
        result = report.to_dict()
        result["preparation_file_sha256"] = {
            "identity": identity_hash,
            "context": context_hash,
            "occupancy_reviews": review_hash,
        }
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
