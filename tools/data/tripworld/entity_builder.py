"""Deterministic global identity grouping and versioned retrieval documents."""

import itertools
import os
from collections import Counter
from collections.abc import Iterable
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from backend.app.tripworld.artifacts import load_json_object, payload_fingerprint
from backend.app.tripworld.hashing import sha256_file
from backend.app.tripworld.manifest import TripWorldManifest
from backend.app.tripworld.retrieval.entities import ENTITY_VERSION, TEXT_VERSION, RetrievalEntity
from backend.app.tripworld.retrieval.geography import haversine_km, valid_coordinates
from tools.data.tripworld.artifact_persistence import artifact_is_current, write_json_if_changed
from tools.data.tripworld.semantics import build_retrieval_description, clean_text


def stable_union(values: Iterable[object]) -> tuple[str, ...]:
    """NFKC/whitespace normalization; order-independent case-insensitive union."""
    unique: dict[str, str] = {}
    for value in values:
        text = clean_text(value)
        if text:
            key = text.casefold()
            unique[key] = min(text, unique.get(key, text))
    return tuple(unique[key] for key in sorted(unique))


def mode_text(values: Iterable[object]) -> str | None:
    texts = [text for value in values if (text := clean_text(value))]
    if not texts:
        return None
    counts = Counter(text.casefold() for text in texts)
    return min(stable_union(texts), key=lambda text: (-counts[text.casefold()], text.casefold()))


def identity(row: dict) -> str:
    google_id = clean_text(row.get("google_place_id"))
    fsq_id = clean_text(row.get("fsq_place_id"))
    if google_id:
        return "google:" + google_id
    if not fsq_id:
        raise ValueError("An FSQ-only source row requires fsq_place_id")
    return "fsq:" + fsq_id


def representative_location(rows: list[dict]) -> tuple[float | None, float | None, float]:
    points = sorted(
        (float(row["fsq_latitude"]), float(row["fsq_longitude"]), row["fsq_place_id"])
        for row in rows
        if valid_coordinates(row.get("fsq_latitude"), row.get("fsq_longitude"))
    )
    if not points:
        return None, None, 0.0
    distances = [[haversine_km(a[0], a[1], b[0], b[1]) for b in points] for a in points]
    index = min(range(len(points)), key=lambda i: (sum(distances[i]), points[i]))
    return points[index][0], points[index][1], max(map(max, distances))


def merge_entity(rows: list[dict], manifest: TripWorldManifest) -> RetrievalEntity:
    if not rows or len({identity(row) for row in rows}) != 1:
        raise ValueError("Entity merging requires one nonempty identity group")
    google_id = clean_text(rows[0].get("google_place_id"))
    preferred = mode_text(row.get("google_name") for row in rows) or mode_text(
        row.get("fsq_name") for row in rows
    )
    aliases = tuple(
        text
        for text in stable_union(
            row.get(field) for row in rows for field in ("fsq_name", "google_name")
        )
        if not preferred or text.casefold() != preferred.casefold()
    )

    def union(field: str) -> tuple[str, ...]:
        return stable_union(value for row in rows for value in (row.get(field) or []))

    localities = stable_union(row.get("fsq_locality") for row in rows)
    regions = stable_union(row.get("fsq_region") for row in rows)
    countries = stable_union(row.get("fsq_country") for row in rows)
    country = mode_text(row.get("fsq_country") for row in rows)
    latitude, longitude, spread = representative_location(rows)
    flags = []
    if latitude is None:
        flags.append("missing_valid_coordinates")
    if spread > 1:
        flags.append("coordinate_spread_over_1km")
    if spread > 10:
        flags.append("coordinate_spread_over_10km")
    if len(countries) > 1:
        flags.append("country_conflict")
    hints = union("semantic_eligibility_hints")
    # Conflicting evidence remains UNKNOWN; no automatic blacklist or row removal.
    meaningful_hints = set(hints) - {"unknown"}
    eligibility = next(iter(meaningful_hints)) if len(meaningful_hints) == 1 else "unknown"
    fsq_categories = union("normalized_fsq_categories")
    google_categories = union("normalized_google_categories")
    direct = union("direct_semantics")
    inferred = union("inferred_semantics")
    description = build_retrieval_description(direct, inferred)
    lines = []
    if preferred:
        lines.append("Name: " + preferred)
    if aliases:
        lines.append("Aliases: " + "; ".join(aliases))
    for label, values in (
        ("Localities", localities),
        ("Regions", regions),
        ("Countries", countries),
        ("FSQ categories", fsq_categories),
        ("Google categories", google_categories),
    ):
        if values:
            lines.append(label + ": " + "; ".join(values))
    raw_text = "\n".join(lines)
    enriched = raw_text + ("\nDescription: " + description if description else "")
    payload = dict(
        retrieval_entity_id=identity(rows[0]),
        google_place_id=google_id,
        source_fsq_place_ids=tuple(sorted({row["fsq_place_id"] for row in rows})),
        preferred_name=preferred,
        aliases=aliases,
        latitude=latitude,
        longitude=longitude,
        localities=localities,
        regions=regions,
        country=country,
        countries=countries,
        fsq_categories=fsq_categories,
        google_categories=google_categories,
        direct_semantics=direct,
        inferred_semantics=inferred,
        semantic_rule_ids=union("semantic_rule_ids"),
        source_eligibility_hints=hints,
        eligibility_hint=eligibility,
        retrieval_description=description,
        raw_retrieval_text=raw_text,
        retrieval_text=enriched,
        coordinate_spread_km=spread,
        location_flags=tuple(flags),
        source_row_count=len(rows),
        tripworld_revision=manifest.dataset.revision,
        semantic_mapping_version=manifest.semantic_mapping_version,
        retrieval_entity_builder_version=ENTITY_VERSION,
        retrieval_text_template_version=TEXT_VERSION,
    )
    return RetrievalEntity(**payload, content_hash=payload_fingerprint(payload))


def entity_schema() -> pa.Schema:
    lists = {
        "source_fsq_place_ids",
        "aliases",
        "localities",
        "regions",
        "countries",
        "fsq_categories",
        "google_categories",
        "direct_semantics",
        "inferred_semantics",
        "semantic_rule_ids",
        "source_eligibility_hints",
        "location_flags",
    }
    floats = {"latitude", "longitude", "coordinate_spread_km"}
    return pa.schema(
        [
            pa.field(
                name,
                pa.list_(pa.string())
                if name in lists
                else (
                    pa.float64()
                    if name in floats
                    else (pa.int64() if name == "source_row_count" else pa.string())
                ),
            )
            for name in RetrievalEntity.model_fields
        ]
    )


def build_entities(corpus: Path, output: Path, manifest: TripWorldManifest) -> dict:
    corpus_hash = sha256_file(corpus)
    source_meta = load_json_object(corpus.with_suffix(".parquet.manifest.json"))
    if source_meta["output_sha256"] != corpus_hash:
        raise ValueError("Retrieval corpus checksum mismatch")
    for key, expected in (
        ("semantic_mapping_version", manifest.semantic_mapping_version),
        ("retrieval_text_template_version", manifest.retrieval_text_template_version),
    ):
        if source_meta["inputs"][key] != expected:
            raise ValueError(f"Retrieval corpus {key} mismatch")
    if source_meta["row_count"] != manifest.dataset.row_count:
        raise ValueError("Retrieval corpus row count mismatch")
    inputs = {
        "tripworld_revision": manifest.dataset.revision,
        "source_retrieval_corpus_hash": corpus_hash,
        "retrieval_entity_builder_version": ENTITY_VERSION,
        "semantic_mapping_version": manifest.semantic_mapping_version,
        "source_text_template_version": manifest.retrieval_text_template_version,
        "retrieval_text_template_version": TEXT_VERSION,
        "pyarrow_version": pa.__version__,
    }
    fingerprint = payload_fingerprint(inputs)
    sidecar = output.with_suffix(".parquet.manifest.json")
    if artifact_is_current(output, sidecar, input_fingerprint=fingerprint):
        return {**load_json_object(sidecar), "reused": True}
    output.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "fsq_place_id",
        "google_place_id",
        "fsq_name",
        "google_name",
        "fsq_latitude",
        "fsq_longitude",
        "fsq_locality",
        "fsq_region",
        "fsq_country",
        "normalized_fsq_categories",
        "normalized_google_categories",
        "direct_semantics",
        "inferred_semantics",
        "semantic_rule_ids",
        "semantic_eligibility_hints",
    ]
    table = pq.read_table(corpus, columns=columns)
    if table.num_rows != manifest.dataset.row_count:
        raise ValueError("Retrieval corpus physical row count mismatch")
    ids = [identity(row) for row in table.select(["google_place_id", "fsq_place_id"]).to_pylist()]
    table = table.append_column("group_id", pa.array(ids)).sort_by(
        [("group_id", "ascending"), ("fsq_place_id", "ascending")]
    )
    del ids
    counts: Counter = Counter()
    flags: Counter = Counter()
    spread_bins: Counter = Counter()
    anomalies = []
    temporary = output.with_suffix(".parquet.part")
    buffer = []
    schema = entity_schema()
    rows = (row for batch in table.to_batches(max_chunksize=8192) for row in batch.to_pylist())
    try:
        with pq.ParquetWriter(temporary, schema, compression="zstd", version="2.6") as writer:
            for _, group in itertools.groupby(rows, key=lambda row: row["group_id"]):
                entity = merge_entity(list(group), manifest)
                counts["entity_count"] += 1
                counts["google_backed_count" if entity.google_place_id else "fsq_only_count"] += 1
                counts["merged_group_count"] += entity.source_row_count > 1
                counts["source_row_count"] += entity.source_row_count
                counts["max_group_size"] = max(counts["max_group_size"], entity.source_row_count)
                counts["empty_retrieval_text_count"] += not bool(entity.retrieval_text)
                counts["eligibility_" + entity.eligibility_hint] += 1
                flags.update(entity.location_flags)
                if entity.source_row_count > 1:
                    spread = entity.coordinate_spread_km
                    label = next(
                        (f"le_{x}km" for x in (0.1, 1, 10, 100) if spread <= x), "gt_100km"
                    )
                    spread_bins[label] += 1
                    anomalies.append(
                        {
                            "entity_id": entity.retrieval_entity_id,
                            "preferred_name": entity.preferred_name,
                            "spread_km": spread,
                            "source_row_count": entity.source_row_count,
                            "countries": entity.countries,
                            "localities": entity.localities,
                        }
                    )
                buffer.append(entity.model_dump())
                if len(buffer) == 8192:
                    writer.write_table(pa.Table.from_pylist(buffer, schema=schema))
                    buffer.clear()
                if counts["entity_count"] % 100000 == 0:
                    print(f"Built {counts['entity_count']} global entities", flush=True)
            if buffer:
                writer.write_table(pa.Table.from_pylist(buffer, schema=schema))
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    metadata = {
        "inputs": inputs,
        "input_fingerprint": fingerprint,
        **dict(counts),
        "row_count": counts["entity_count"],
        "duplicate_row_reduction": counts["source_row_count"] - counts["entity_count"],
        "location_flags": dict(flags),
        "merged_group_spread_bins": dict(spread_bins),
        "largest_spread_examples": sorted(anomalies, key=lambda x: -x["spread_km"])[:30],
        "representative_location_strategy": "observed-coordinate medoid; stable coordinate/FSQ tie",
        "output_sha256": sha256_file(output),
        "output_size_bytes": output.stat().st_size,
    }
    write_json_if_changed(sidecar, metadata)
    return {**metadata, "reused": False}
