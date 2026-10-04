"""Offline batch intake command; emits preparation records, never scores."""

import argparse
import json

from .intake import load_batch


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to the user-curated batch manifest")
    args = parser.parse_args(argv)
    result = load_batch(args.manifest)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result.status == "accepted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
