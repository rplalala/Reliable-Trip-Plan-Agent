"""Discover repository evaluation commands without initializing online runtimes."""

import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="rtpeval",
        description="RTPEval repository commands. Validation is offline and never scores results.",
        epilog="validate MANIFEST: read a source-bound batch and emit intake JSON to stdout.",
    )
    parser.add_argument("command", choices=("validate",), help="Offline batch validation")
    parser.add_argument("arguments", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    from backend.evaluation.__main__ import main as validate

    return validate(args.arguments)
