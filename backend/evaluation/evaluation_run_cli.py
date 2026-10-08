"""Prepare, execute or replay a complete independent four-final evaluation run."""

import argparse
import asyncio
import json
import os
from pathlib import Path

from .evaluation_run import execute_run, prepare_run, replay_run
from .intake import _read


def main(argv=None, *, http_client=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare", help="Offline source, context and limit validation")
    prepare.add_argument("manifest")
    for option in ("directory", "options", "prices"):
        prepare.add_argument("--" + option, required=True)
    for option in ("context", "occupancy-reviews", "route-reviews", "density-reviews"):
        prepare.add_argument("--" + option)
    execute = commands.add_parser(
        "execute", help="Fresh independent Google and V0-only model acquisition"
    )
    execute.add_argument("directory")
    execute.add_argument("--approved-sha256", required=True)
    execute.add_argument("--env-file")
    replay = commands.add_parser(
        "replay", help="Recompute final reports with no network or credentials"
    )
    replay.add_argument("directory")
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            context = {
                "schedule_context": _read(Path(args.context))[0] if args.context else None,
                **{
                    name: _read(Path(getattr(args, name)))[0] if getattr(args, name) else None
                    for name in ("occupancy_reviews", "route_reviews", "density_reviews")
                },
            }
            result = prepare_run(
                args.manifest,
                args.directory,
                options=_read(Path(args.options))[0],
                prices=_read(Path(args.prices))[0],
                **context,
            )
            result = {
                "status": result["status"],
                "directory": result["directory"],
                "preparation_sha256": result["content_sha256"],
                "identity_request_count": len(result["identity_plan"]["requests"]),
            }
        elif args.command == "execute":
            if args.env_file:
                from dotenv import load_dotenv

                load_dotenv(args.env_file, override=False)
            preparation = _read(Path(args.directory) / "preparation.json")[0]
            result = asyncio.run(
                execute_run(
                    preparation,
                    approved_sha256=args.approved_sha256,
                    google_api_key=os.environ.get("GOOGLE_MAPS_API_KEY"),
                    model_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
                    http_client=http_client,
                )
            )
        else:
            result = replay_run(args.directory)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        result = {
            "processing_status": "needs_material_correction",
            "error_type": type(exc).__name__,
            "reason": str(exc),
        }
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return (
        0
        if result.get("status") == "prepared" or result.get("processing_status") == "complete"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
