"""Command-line orchestration for offline TripWorld data preparation."""

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict, is_dataclass
from pathlib import Path

from backend.app.tripworld.manifest import load_manifest
from tools.data.tripworld.corpus import build_corpus
from tools.data.tripworld.preprocessing import project_source
from tools.data.tripworld.profiling import write_profile_outputs
from tools.data.tripworld.semantics import load_semantic_mapping
from tools.data.tripworld.source import download_source

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST = REPOSITORY_ROOT / "data" / "tripworld" / "manifest.json"
DEFAULT_MAPPING = REPOSITORY_ROOT / "data" / "tripworld" / "category_semantics.v1.json"
DEFAULT_SOURCE = REPOSITORY_ROOT / "data" / "tripworld" / "raw" / "metadata_all.parquet"
DEFAULT_SELECTED = (
    REPOSITORY_ROOT / "data" / "tripworld" / "processed" / "tripworld_selected.parquet"
)
DEFAULT_CORPUS = (
    REPOSITORY_ROOT / "data" / "tripworld" / "artifacts" / "retrieval_corpus.parquet"
)
DEFAULT_REPORT_DIRECTORY = REPOSITORY_ROOT / "data" / "tripworld" / "reports"


def _path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare pinned TripWorld POI metadata without changing application runtime."
    )
    parser.add_argument("--manifest", type=_path, default=DEFAULT_MANIFEST)
    subparsers = parser.add_subparsers(dest="command", required=True)

    download = subparsers.add_parser("download", help="Download and validate the pinned Parquet")
    download.add_argument("--output", type=_path, default=DEFAULT_SOURCE)

    preprocess = subparsers.add_parser("preprocess", help="Project the fixed 11 source fields")
    preprocess.add_argument("--source", type=_path, default=DEFAULT_SOURCE)
    preprocess.add_argument("--output", type=_path, default=DEFAULT_SELECTED)

    profile = subparsers.add_parser("profile", help="Profile the projected TripWorld corpus")
    profile.add_argument("--input", type=_path, default=DEFAULT_SELECTED)
    profile.add_argument("--output-directory", type=_path, default=DEFAULT_REPORT_DIRECTORY)

    corpus = subparsers.add_parser("corpus", help="Build deterministic retrieval documents")
    corpus.add_argument("--input", type=_path, default=DEFAULT_SELECTED)
    corpus.add_argument("--mapping", type=_path, default=DEFAULT_MAPPING)
    corpus.add_argument("--output", type=_path, default=DEFAULT_CORPUS)

    all_steps = subparsers.add_parser("all", help="Run download, preprocess, profile, and corpus")
    all_steps.add_argument("--source", type=_path, default=DEFAULT_SOURCE)
    all_steps.add_argument("--selected", type=_path, default=DEFAULT_SELECTED)
    all_steps.add_argument("--mapping", type=_path, default=DEFAULT_MAPPING)
    all_steps.add_argument("--corpus", type=_path, default=DEFAULT_CORPUS)
    all_steps.add_argument(
        "--report-directory", type=_path, default=DEFAULT_REPORT_DIRECTORY
    )
    return parser


def _print_result(value: object) -> None:
    if is_dataclass(value):
        payload = asdict(value)
    else:
        payload = value
    print(json.dumps(payload, indent=2, default=str, sort_keys=True))


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = load_manifest(args.manifest)
    if args.command == "download":
        _print_result(download_source(manifest, args.output))
    elif args.command == "preprocess":
        _print_result(project_source(args.source, args.output, manifest))
    elif args.command == "profile":
        _print_result(write_profile_outputs(args.input, args.output_directory, manifest))
    elif args.command == "corpus":
        mapping = load_semantic_mapping(args.mapping)
        _print_result(build_corpus(args.input, args.output, manifest, mapping))
    elif args.command == "all":
        _print_result(download_source(manifest, args.source))
        _print_result(project_source(args.source, args.selected, manifest))
        _print_result(write_profile_outputs(args.selected, args.report_directory, manifest))
        mapping = load_semantic_mapping(args.mapping)
        _print_result(build_corpus(args.selected, args.corpus, manifest, mapping))
    else:
        raise AssertionError(f"Unhandled command: {args.command}")
    return 0
