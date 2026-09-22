"""Deterministic profiling for the selected TripWorld POI metadata."""

import math
from collections import Counter
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

from backend.app.tripworld.hashing import sha256_file
from backend.app.tripworld.manifest import SELECTED_FIELD_NAMES, TripWorldManifest
from tools.data.tripworld.artifact_persistence import write_json_if_changed, write_text_if_changed
from tools.data.tripworld.preprocessing import validate_projected_file
from tools.data.tripworld.semantics import (
    clean_text,
    normalize_fsq_categories,
    normalize_google_categories,
)

SYDNEY_CBD = (-33.8688, 151.2093)
SYDNEY_RADII_KM = (10, 25, 50, 75, 100)
AUSTRALIA_COUNTRY_KEYS = {"au", "aus", "australia"}
NON_TRAVEL_CATEGORY_TERMS = {
    "apartment",
    "automotive repair",
    "child care",
    "corporate office",
    "dentist",
    "distribution center",
    "doctor",
    "factory",
    "gas station",
    "government building",
    "hospital",
    "office",
    "police station",
    "residential building",
    "school",
    "storage facility",
    "warehouse",
}


def _is_valid_coordinate(latitude: object, longitude: object) -> bool:
    return (
        isinstance(latitude, (int, float))
        and isinstance(longitude, (int, float))
        and math.isfinite(latitude)
        and math.isfinite(longitude)
        and -90 <= latitude <= 90
        and -180 <= longitude <= 180
        and not (latitude == 0 and longitude == 0)
    )


def _haversine_km(latitude: float, longitude: float) -> float:
    lat1, lon1 = map(math.radians, SYDNEY_CBD)
    lat2, lon2 = math.radians(latitude), math.radians(longitude)
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    value = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    )
    return 6371.0088 * 2 * math.asin(math.sqrt(value))


def _normalized_name(value: object) -> str | None:
    text = clean_text(value)
    return text.casefold() if text else None


def _top(counter: Counter[str], limit: int = 30) -> list[dict[str, object]]:
    return [
        {"value": value, "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def _coverage_record(non_null: int, usable: int, total: int) -> dict[str, object]:
    return {
        "non_null_count": non_null,
        "usable_count": usable,
        "null_count": total - non_null,
        "blank_or_empty_count": non_null - usable,
        "null_rate": round((total - non_null) / total, 8) if total else None,
        "usable_rate": round(usable / total, 8) if total else None,
    }


def _category_is_non_travel_candidate(category: str) -> bool:
    segments = [segment.strip().casefold().replace("_", " ") for segment in category.split(">")]
    return any(segment in NON_TRAVEL_CATEGORY_TERMS for segment in segments)


def build_profile(
    selected_path: Path,
    manifest: TripWorldManifest,
    *,
    batch_size: int = 20_000,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Profile the actual projected corpus and return report and full taxonomy payloads."""

    total = 0
    non_null = Counter[str]()
    usable = Counter[str]()
    country = Counter[str]()
    region = Counter[str]()
    locality = Counter[str]()
    australia_region = Counter[str]()
    australia_locality = Counter[str]()
    fsq_categories = Counter[str]()
    fsq_category_roots = Counter[str]()
    fsq_category_leaves = Counter[str]()
    google_categories = Counter[str]()
    non_travel_categories = Counter[str]()
    fsq_id_rows = Counter[str]()
    google_id_rows = Counter[str]()
    first_fsq_by_google: dict[str, str | None] = {}
    multi_fsq_by_google: dict[str, set[str]] = {}
    identity_key_rows = Counter[tuple[str, float, float]]()
    identity_key_sample: dict[tuple[str, float, float], dict[str, object]] = {}
    sydney_counts = {
        radius: Counter[str]() for radius in SYDNEY_RADII_KM
    }
    sydney_locality_50km = Counter[str]()
    sydney_fsq_categories_50km = Counter[str]()
    sydney_google_categories_50km = Counter[str]()
    both_names = 0
    same_normalized_name = 0
    valid_coordinate_count = 0
    zero_coordinate_count = 0
    invalid_coordinate_count = 0
    australia_count = 0

    validate_projected_file(selected_path, manifest)
    parquet = pq.ParquetFile(selected_path)
    for batch in parquet.iter_batches(batch_size=batch_size):
        for row in batch.to_pylist():
            total += 1
            for field in SELECTED_FIELD_NAMES:
                value = row.get(field)
                if value is not None:
                    non_null[field] += 1
                if isinstance(value, str):
                    usable[field] += bool(clean_text(value))
                elif isinstance(value, list):
                    usable[field] += bool(value)
                elif value is not None:
                    usable[field] += 1

            country_value = clean_text(row.get("fsq_country"))
            region_value = clean_text(row.get("fsq_region"))
            locality_value = clean_text(row.get("fsq_locality"))
            country[country_value or "<missing>"] += 1
            region[region_value or "<missing>"] += 1
            locality[locality_value or "<missing>"] += 1

            fsq_name = clean_text(row.get("fsq_name"))
            google_name = clean_text(row.get("google_name"))
            if fsq_name and google_name:
                both_names += 1
                same_normalized_name += fsq_name.casefold() == google_name.casefold()

            normalized_fsq = normalize_fsq_categories(row.get("fsq_category_labels"))
            normalized_google = normalize_google_categories(row.get("google_categories"))
            for category_value in normalized_fsq:
                fsq_categories[category_value] += 1
                segments = [part.strip() for part in category_value.split(" > ")]
                fsq_category_roots[segments[0]] += 1
                fsq_category_leaves[segments[-1]] += 1
                if _category_is_non_travel_candidate(category_value):
                    non_travel_categories[category_value] += 1
            for category_value in normalized_google:
                google_categories[category_value] += 1
                if _category_is_non_travel_candidate(category_value):
                    non_travel_categories[f"Google: {category_value}"] += 1

            fsq_id = clean_text(row.get("fsq_place_id"))
            google_id = clean_text(row.get("google_place_id"))
            if fsq_id:
                fsq_id_rows[fsq_id] += 1
            if google_id:
                google_id_rows[google_id] += 1
                first_fsq = first_fsq_by_google.setdefault(google_id, fsq_id)
                if fsq_id and first_fsq and fsq_id != first_fsq:
                    multi_fsq_by_google.setdefault(google_id, {first_fsq}).add(fsq_id)

            latitude = row.get("fsq_latitude")
            longitude = row.get("fsq_longitude")
            if latitude == 0 and longitude == 0:
                zero_coordinate_count += 1
            if _is_valid_coordinate(latitude, longitude):
                valid_coordinate_count += 1
                name_key = _normalized_name(fsq_name or google_name)
                if name_key:
                    identity_key = (name_key, round(float(latitude), 5), round(float(longitude), 5))
                    identity_key_rows[identity_key] += 1
                    identity_key_sample.setdefault(
                        identity_key,
                        {
                            "name": fsq_name or google_name,
                            "latitude": latitude,
                            "longitude": longitude,
                        },
                    )
            else:
                invalid_coordinate_count += 1

            is_australia = bool(
                country_value and country_value.casefold() in AUSTRALIA_COUNTRY_KEYS
            )
            if not is_australia:
                continue
            australia_count += 1
            australia_region[region_value or "<missing>"] += 1
            australia_locality[locality_value or "<missing>"] += 1
            if not _is_valid_coordinate(latitude, longitude):
                continue
            distance = _haversine_km(float(latitude), float(longitude))
            has_name = bool(fsq_name or google_name)
            has_categories = bool(normalized_fsq or normalized_google)
            has_google_id = bool(google_id)
            for radius in SYDNEY_RADII_KM:
                if distance <= radius:
                    counts = sydney_counts[radius]
                    counts["all_rows"] += 1
                    counts["named"] += has_name
                    counts["categorized"] += has_categories
                    counts["google_resolvable"] += has_google_id
                    counts["retrieval_usable"] += has_name and has_categories
                    counts["retrieval_usable_google_resolvable"] += (
                        has_name and has_categories and has_google_id
                    )
                    if radius == 50:
                        sydney_locality_50km[locality_value or "<missing>"] += 1
                        sydney_fsq_categories_50km.update(normalized_fsq)
                        sydney_google_categories_50km.update(normalized_google)

    duplicate_fsq_ids = {key: value for key, value in fsq_id_rows.items() if value > 1}
    duplicate_google_ids = {key: value for key, value in google_id_rows.items() if value > 1}
    duplicate_identity_keys = {
        key: value for key, value in identity_key_rows.items() if value > 1
    }
    identity_samples = []
    for key, count in sorted(
        duplicate_identity_keys.items(), key=lambda item: (-item[1], item[0])
    )[:25]:
        identity_samples.append({**identity_key_sample[key], "row_count": count})
    multi_google_samples = [
        {
            "google_place_id": google_id,
            "fsq_place_id_count": len(fsq_ids),
            "fsq_place_ids": sorted(fsq_ids)[:10],
            "row_count": google_id_rows[google_id],
        }
        for google_id, fsq_ids in sorted(
            multi_fsq_by_google.items(), key=lambda item: (-len(item[1]), item[0])
        )[:25]
    ]
    profile: dict[str, Any] = {
        "profile_version": "tripworld-profile-v1",
        "input": {
            "dataset_revision": manifest.dataset.revision,
            "source_sha256": manifest.dataset.sha256,
            "selected_artifact_sha256": sha256_file(selected_path),
            "selected_schema_version": manifest.selected_schema_version,
        },
        "row_count": total,
        "field_coverage": {
            field: _coverage_record(non_null[field], usable[field], total)
            for field in SELECTED_FIELD_NAMES
        },
        "coordinates": {
            "valid_count": valid_coordinate_count,
            "valid_rate": round(valid_coordinate_count / total, 8) if total else None,
            "invalid_or_missing_count": invalid_coordinate_count,
            "zero_pair_count": zero_coordinate_count,
        },
        "geography": {
            "country_distinct_count": len(country),
            "country_top": _top(country, 50),
            "region_distinct_count": len(region),
            "region_top": _top(region, 50),
            "locality_distinct_count": len(locality),
            "locality_top": _top(locality, 50),
            "australia": {
                "recognized_country_values": sorted(
                    value
                    for value in country
                    if value.casefold() in AUSTRALIA_COUNTRY_KEYS
                ),
                "row_count": australia_count,
                "region_top": _top(australia_region, 50),
                "locality_top": _top(australia_locality, 50),
            },
            "sydney": {
                "method": "great-circle distance from a fixed Sydney CBD reference point",
                "reference_latitude": SYDNEY_CBD[0],
                "reference_longitude": SYDNEY_CBD[1],
                "radius_counts": {
                    str(radius): dict(sydney_counts[radius])
                    for radius in SYDNEY_RADII_KM
                },
                "retrieval_usable_definition": (
                    "valid non-zero coordinates, at least one nonblank name, and at least "
                    "one FSQ or Google category"
                ),
                "localities_within_50km_top": _top(sydney_locality_50km, 100),
                "locality_distinct_count_within_50km": len(sydney_locality_50km),
                "fsq_categories_within_50km_top": _top(
                    sydney_fsq_categories_50km, 100
                ),
                "google_categories_within_50km_top": _top(
                    sydney_google_categories_50km, 100
                ),
            },
        },
        "categories": {
            "fsq_distinct_path_count": len(fsq_categories),
            "fsq_distinct_root_count": len(fsq_category_roots),
            "fsq_distinct_leaf_count": len(fsq_category_leaves),
            "fsq_paths_top": _top(fsq_categories, 100),
            "fsq_roots": _top(fsq_category_roots, len(fsq_category_roots)),
            "fsq_leaves_top": _top(fsq_category_leaves, 100),
            "google_distinct_count": len(google_categories),
            "google_top": _top(google_categories, 100),
            "non_travel_candidate_categories": _top(non_travel_categories, 100),
            "non_travel_note": (
                "Diagnostic category-level candidates only; no POIs were filtered or classified."
            ),
        },
        "identity": {
            "distinct_fsq_place_id_count": len(fsq_id_rows),
            "duplicate_fsq_place_id_count": len(duplicate_fsq_ids),
            "duplicate_fsq_row_excess": sum(value - 1 for value in duplicate_fsq_ids.values()),
            "distinct_google_place_id_count": len(google_id_rows),
            "duplicate_google_place_id_count": len(duplicate_google_ids),
            "duplicate_google_row_excess": sum(
                value - 1 for value in duplicate_google_ids.values()
            ),
            "google_ids_with_multiple_fsq_ids_count": len(multi_fsq_by_google),
            "google_ids_with_multiple_fsq_ids_samples": multi_google_samples,
            "normalized_name_and_rounded_coordinate_duplicate_group_count": len(
                duplicate_identity_keys
            ),
            "normalized_name_and_rounded_coordinate_row_excess": sum(
                value - 1 for value in duplicate_identity_keys.values()
            ),
            "normalized_name_and_rounded_coordinate_samples": identity_samples,
            "rows_with_both_names": both_names,
            "rows_with_equal_normalized_names": same_normalized_name,
            "equal_normalized_name_rate_when_both_present": (
                round(same_normalized_name / both_names, 8) if both_names else None
            ),
        },
    }
    taxonomy: dict[str, Any] = {
        "taxonomy_version": "tripworld-category-taxonomy-v1",
        "input": profile["input"],
        "fsq_paths": _top(fsq_categories, len(fsq_categories)),
        "fsq_roots": _top(fsq_category_roots, len(fsq_category_roots)),
        "fsq_leaves": _top(fsq_category_leaves, len(fsq_category_leaves)),
        "google_categories": _top(google_categories, len(google_categories)),
    }
    return profile, taxonomy


def _table(rows: list[dict[str, object]], limit: int = 20) -> list[str]:
    lines = ["| Value | Count |", "|---|---:|"]
    lines.extend(f"| {row['value']} | {row['count']} |" for row in rows[:limit])
    return lines


def render_profile_markdown(profile: dict[str, Any]) -> str:
    coverage = profile["field_coverage"]
    geography = profile["geography"]
    sydney = geography["sydney"]
    identity = profile["identity"]
    categories = profile["categories"]
    lines = [
        "# TripWorld Metadata Profile",
        "",
        f"Pinned dataset revision: `{profile['input']['dataset_revision']}`",
        "",
        f"Total POI rows: **{profile['row_count']:,}**",
        f"Australia POI rows: **{geography['australia']['row_count']:,}**",
        "",
        "## Field coverage",
        "",
        "| Field | Non-null | Blank/empty | Usable | Usable rate | Null rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for field in SELECTED_FIELD_NAMES:
        item = coverage[field]
        lines.append(
            f"| {field} | {item['non_null_count']:,} | "
            f"{item['blank_or_empty_count']:,} | {item['usable_count']:,} | "
            f"{item['usable_rate']:.2%} | {item['null_rate']:.2%} |"
        )
    lines.extend(
        [
            "",
            "## Observed geography values",
            "",
            "### Top country values",
            "",
            *_table(geography["country_top"], 20),
            "",
            "### Australia region values",
            "",
            *_table(geography["australia"]["region_top"], 20),
            "",
            "### Australia locality values",
            "",
            *_table(geography["australia"]["locality_top"], 30),
            "",
            "## Sydney geographic coverage",
            "",
            (
                "Counts use great-circle distance from Sydney CBD "
                f"(`{sydney['reference_latitude']}`, `{sydney['reference_longitude']}`), "
                "rather than locality equality."
            ),
            "",
            "| Radius | All rows | Retrieval usable | Google-resolvable usable |",
            "|---:|---:|---:|---:|",
        ]
    )
    for radius, counts in sydney["radius_counts"].items():
        lines.append(
            f"| {radius} km | {counts.get('all_rows', 0):,} | "
            f"{counts.get('retrieval_usable', 0):,} | "
            f"{counts.get('retrieval_usable_google_resolvable', 0):,} |"
        )
    lines.extend(
        [
            "",
            "### Top localities within 50 km",
            "",
            *_table(sydney["localities_within_50km_top"], 30),
            "",
            "### Top FSQ categories within 50 km",
            "",
            *_table(sydney["fsq_categories_within_50km_top"], 30),
            "",
            "### Top Google categories within 50 km",
            "",
            *_table(sydney["google_categories_within_50km_top"], 30),
            "",
            "## Category coverage",
            "",
            f"Distinct FSQ category paths: **{categories['fsq_distinct_path_count']:,}**",
            f"Distinct Google category values: **{categories['google_distinct_count']:,}**",
            "",
            "### Top FSQ category paths",
            "",
            *_table(categories["fsq_paths_top"], 30),
            "",
            "### Top Google categories",
            "",
            *_table(categories["google_top"], 30),
            "",
            "### Category-level travel eligibility review candidates",
            "",
            categories["non_travel_note"],
            "",
            *_table(categories["non_travel_candidate_categories"], 30),
            "",
            "## Identity diagnostics",
            "",
            (
                "- Google Place IDs assigned to multiple FSQ IDs: "
                f"**{identity['google_ids_with_multiple_fsq_ids_count']:,}**"
            ),
            (
                "- Duplicate FSQ ID groups: "
                f"**{identity['duplicate_fsq_place_id_count']:,}**"
            ),
            (
                "- Duplicate Google ID groups: "
                f"**{identity['duplicate_google_place_id_count']:,}**"
            ),
            (
                "- Normalized-name plus rounded-coordinate duplicate groups: "
                f"**{identity['normalized_name_and_rounded_coordinate_duplicate_group_count']:,}**"
            ),
            (
                "- Equal FSQ/Google normalized names when both are present: "
                f"**{identity['equal_normalized_name_rate_when_both_present']:.2%}**"
            ),
            "",
            "The profile is descriptive. It does not apply a production eligibility filter, "
            "deduplicate records, or alter runtime behavior.",
            "",
        ]
    )
    return "\n".join(lines)


def write_profile_outputs(
    selected_path: Path,
    report_directory: Path,
    manifest: TripWorldManifest,
) -> tuple[Path, Path, Path]:
    profile, taxonomy = build_profile(selected_path, manifest)
    report_directory.mkdir(parents=True, exist_ok=True)
    json_path = report_directory / "profile.json"
    markdown_path = report_directory / "profile.md"
    taxonomy_path = report_directory / "category_taxonomy.json"
    write_json_if_changed(json_path, profile)
    write_json_if_changed(taxonomy_path, taxonomy)
    write_text_if_changed(markdown_path, render_profile_markdown(profile))
    return json_path, markdown_path, taxonomy_path
