"""Offline producer-side material commands."""

import argparse
import json
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="rtpeval batch", description="Offline material staging.")
    commands = parser.add_subparsers(dest="operation", required=True)
    collect_parser = commands.add_parser(
        "collect",
        help="Collect explicitly selected sources offline",
        description="Offline exact-byte collection into unqualified producer staging.",
    )
    collect_parser.add_argument("config", type=Path)
    collect_parser.add_argument(
        "--directory", required=True, type=Path, help="Fresh staging directory"
    )
    args = parser.parse_args(argv)
    from backend.cli.collection import CollectionError, collect

    try:
        result = collect(args.config, args.directory)
    except (CollectionError, OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print(json.dumps({"status": "needs_material_correction", "diagnostics": [str(exc)]}))
        return 2
    print(json.dumps(result))
    return 0
