"""Prepare the pinned TripWorld metadata source and retrieval corpus."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run() -> int:
    """Load and execute the TripWorld preparation CLI from the repository root."""

    from tools.data.tripworld.cli import main

    return main()


if __name__ == "__main__":
    raise SystemExit(run())
