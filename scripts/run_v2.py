"""Independent command-line entry point for V2 TripWorld discovery."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run():
    from backend.app.versions.v2.runner import main
    return main()


if __name__ == "__main__":
    raise SystemExit(run())
