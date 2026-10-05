"""Replay a frozen V0 candidate/model packet; never call a model or provider."""

import argparse
import json
from pathlib import Path

from .identity_adoption import resolve_v0_identities
from .intake import _read
from .records import MaterialError


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", help="Versioned source-linked V0 material manifest")
    parser.add_argument("--reviews", help="Optional genuine identity-review envelope")
    args = parser.parse_args(argv)
    try:
        reviews = _read(Path(args.reviews))[0] if args.reviews else None
        report = resolve_v0_identities(None, args.bundle, reviews)
    except (ValueError, TypeError, KeyError, OSError, StopIteration) as exc:
        diagnostic = exc.diagnostic if isinstance(exc, MaterialError) else {"explanation": str(exc)}
        print(json.dumps({"status": "needs_evidence_correction", "diagnostic": diagnostic}))
        return 2
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if report.status == "complete" else 3


if __name__ == "__main__":
    raise SystemExit(main())
