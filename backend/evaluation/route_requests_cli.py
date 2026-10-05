"""Prepare a frozen V0 route inventory and budget offline; never execute acquisition."""

import argparse
import json
from pathlib import Path

from .intake import _read
from .route_requests import prepare_v0_route_requests


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle")
    parser.add_argument("identity_report")
    parser.add_argument("--prepared-at", required=True, help="Offset-aware preparation timestamp")
    parser.add_argument("--context")
    parser.add_argument("--occupancy-reviews")
    parser.add_argument("--route-reviews")
    parser.add_argument("--details-snapshot")
    args = parser.parse_args(argv)
    try:

        def read(path):
            return _read(Path(path))[0] if path else None

        report = prepare_v0_route_requests(
            args.bundle,
            read(args.identity_report),
            prepared_at=args.prepared_at,
            schedule_context=read(args.context),
            occupancy_reviews=read(args.occupancy_reviews),
            route_reviews=read(args.route_reviews),
            details_snapshot_directory=args.details_snapshot,
        ).to_dict()
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(json.dumps({"status": "needs_material_correction", "diagnostic": str(exc)}))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    if report["status"] != "complete":
        return 2
    return (
        3
        if any(
            leg["request_state"] != "ready_for_approval"
            for leg in report["legs"]
            if leg["verdict"] != "N/A"
        )
        else 0
    )


if __name__ == "__main__":
    raise SystemExit(main())
