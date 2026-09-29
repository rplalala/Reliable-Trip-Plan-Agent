"""Replay independent identity observations against a selected offline batch."""

import argparse
import json
from pathlib import Path

from .identity import resolve_identities
from .intake import _read, load_batch
from .records import MaterialError


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Accepted batch manifest")
    parser.add_argument("evidence", help="Independent identity observation JSON")
    parser.add_argument("audit_plan", help="Predeclared audit seed and sample count JSON")
    parser.add_argument("--reviews", help="Optional versioned adjudication JSON")
    args = parser.parse_args(argv)
    intake = load_batch(args.manifest)
    if intake.status != "accepted":
        print(json.dumps(intake.to_dict(), ensure_ascii=False, indent=2, allow_nan=False))
        return 2
    try:
        evidence, evidence_hash = _read(Path(args.evidence))
        audit_plan, audit_hash = _read(Path(args.audit_plan))
        reviews, review_hash = _read(Path(args.reviews)) if args.reviews else (None, None)
        report = resolve_identities(intake, evidence, reviews, audit_plan)
    except (MaterialError, ValueError, TypeError, KeyError) as exc:
        diagnostic = exc.diagnostic if isinstance(exc, MaterialError) else {"explanation": str(exc)}
        print(json.dumps({"status": "needs_evidence_correction", "diagnostic": diagnostic}))
        return 2
    result = report.to_dict()
    result["evidence_file_sha256"] = evidence_hash
    result["audit_plan_file_sha256"] = audit_hash
    result["review_file_sha256"] = review_hash
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if report.status == "complete" else 3


if __name__ == "__main__":
    raise SystemExit(main())
