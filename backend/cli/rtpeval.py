"""Discover repository evaluation commands without initializing online runtimes."""

import argparse
import sys
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None, *, http_client=None) -> int:
    parser = argparse.ArgumentParser(
        prog="rtpeval",
        description="RTPEval: offline validation, preparation/replay and online evaluation.",
        epilog="validate MANIFEST: read a source-bound batch and emit intake JSON to stdout.",
    )
    parser.add_argument("command", choices=("validate", "evaluate"), help="Evaluation task group")
    parser.add_argument("arguments", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if args.command == "validate":
        from backend.evaluation.__main__ import main as command
    else:
        from backend.cli.evaluate import main as command

    # The native parser derives usage from argv[0]; retain the installed subcommand.
    program = sys.argv[0]
    try:
        sys.argv[0] = f"{parser.prog} {args.command}"
        if args.command == "evaluate":
            return command(args.arguments, http_client=http_client)
        return command(args.arguments)
    finally:
        sys.argv[0] = program
