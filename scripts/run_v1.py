"""Independent command-line entry point for the V1-A planner."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run() -> int:
    """Load and execute the V1 runner after configuring the project import path."""

    from backend.app.versions.v1.runner import main

    return main()


if __name__ == "__main__":
    raise SystemExit(run())
