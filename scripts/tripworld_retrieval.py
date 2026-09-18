"""Standalone global TripWorld entity and retrieval spike entry point."""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run() -> int:
    from backend.app.tripworld.manifest import load_manifest
    from backend.app.tripworld.retrieval.entities import build_entities
    from backend.app.tripworld.retrieval.geography import GeographicScope
    from backend.app.tripworld.retrieval.sampling import select_destinations
    from backend.app.tripworld.retrieval.spike import query_spike, run_spike

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT / "data" / "tripworld")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("entities")
    commands.add_parser("estimate")
    sample = commands.add_parser("sample")
    sample.add_argument("--radius-km", type=float, default=15)
    sample.add_argument("--cap", type=int, default=384)
    spike = commands.add_parser("spike")
    spike.add_argument("--batch-size", type=int, default=64)
    query = commands.add_parser("query")
    query.add_argument("--semantic-query", required=True)
    query.add_argument("--latitude", type=float, required=True)
    query.add_argument("--longitude", type=float, required=True)
    query.add_argument("--radius-km", type=float, required=True)
    query.add_argument("--country")
    query.add_argument("--top-k", type=int, default=10)
    query.add_argument("--variant", choices=("raw", "enriched"), default="enriched")
    query.add_argument("--exclude-ineligible", action="store_true")
    args = parser.parse_args()
    root = args.root
    if args.command == "entities":
        result = build_entities(
            root / "artifacts" / "retrieval_corpus.parquet",
            root / "artifacts" / "retrieval_entities.parquet",
            load_manifest(root / "manifest.json"),
        )
    elif args.command == "estimate":
        from backend.app.tripworld.retrieval.embedding import EmbeddingConfig
        from backend.app.tripworld.retrieval.estimation import estimate_embeddings

        config = EmbeddingConfig.model_validate_json((root / "embedding_model.v1.json").read_text())
        result = estimate_embeddings(
            root / "artifacts" / "retrieval_entities.parquet",
            root / "reports" / "phase4_cost_estimate.json",
            config,
        )
    elif args.command == "sample":
        result = select_destinations(
            root / "artifacts" / "retrieval_entities.parquet",
            root / "artifacts" / "phase4",
            radius_km=args.radius_km,
            cap_per_destination=args.cap,
        )
    elif args.command == "spike":
        result = run_spike(root, batch_size=args.batch_size)
    else:
        result = query_spike(
            root,
            args.semantic_query,
            GeographicScope(
                latitude=args.latitude,
                longitude=args.longitude,
                radius_km=args.radius_km,
                country=args.country,
            ),
            args.top_k,
            args.variant,
            exclude_ineligible=args.exclude_ineligible,
        )
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
