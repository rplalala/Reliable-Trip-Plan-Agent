"""Discover repository evaluation commands without initializing online runtimes."""

import argparse
import sys
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

    # The native parser derives usage from argv[0]; retain the installed subcommand.
    program = sys.argv[0]
    try:
        sys.argv[0] = f"{parser.prog} {args.command}"
        return validate(args.arguments)
    finally:
        sys.argv[0] = program
