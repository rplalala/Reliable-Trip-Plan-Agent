"""Discover repository evaluation commands without initializing online runtimes."""

import argparse
import sys
from collections.abc import Sequence

from backend.cli.tools import TASKS


def main(argv: Sequence[str] | None = None, *, http_client=None) -> int:
    parser = argparse.ArgumentParser(
        prog="rtpeval",
        description="RTPEval: offline validation, preparation/replay and online evaluation.",
        epilog="validate: offline source-bound batch intake; JSON to stdout.\n"
        "evaluate: automatic evaluation; prepare/replay offline, execute online.\n"
        + "\n".join(f"{name}: {task.description}" for name, task in TASKS.items()),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command", choices=("validate", "evaluate", *TASKS), help="Evaluation task group"
    )
    parser.add_argument("arguments", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if args.command == "validate":
        from backend.evaluation.__main__ import main as command
    elif args.command == "evaluate":
        from backend.cli.evaluate import main as command

    else:
        from backend.cli.tools import main as tools_main

        return tools_main(args.command, args.arguments, http_client=http_client)

    # The native parser derives usage from argv[0]; retain the installed subcommand.
    program = sys.argv[0]
    try:
        sys.argv[0] = f"{parser.prog} {args.command}"
        if args.command == "evaluate":
            return command(args.arguments, http_client=http_client)
        return command(args.arguments)
    finally:
        sys.argv[0] = program
