"""Rebuildable geographic stratification for a bounded development spike."""

import hashlib
import math
from collections import defaultdict
from pathlib import Path
from time import perf_counter

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from backend.app.tripworld.artifacts import write_json_if_changed
from backend.app.tripworld.retrieval.entities import mode_text
from backend.app.tripworld.retrieval.geography import (
    EARTH_RADIUS_KM,
    GeographicScope,
    bounding_box,
    valid_coordinates,
)
from backend.app.tripworld.source import sha256_file


def geographic_mask(
    latitudes: np.ndarray,
    longitudes: np.ndarray,
    countries: np.ndarray,
    scope: GeographicScope,
) -> tuple[np.ndarray, np.ndarray]:
    lo, hi, half_width = bounding_box(scope)
    valid = (
        np.isfinite(latitudes)
        & np.isfinite(longitudes)
        & (np.abs(latitudes) <= 90)
        & (np.abs(longitudes) <= 180)
        & ~((latitudes == 0) & (longitudes == 0))
    )
    coarse = (
        valid
        & (latitudes >= lo - 1e-9)
        & (latitudes <= hi + 1e-9)
        & (np.abs((longitudes - scope.longitude + 180) % 360 - 180) <= half_width + 1e-9)
    )
    if scope.country:
        # Missing country does not erase a valid coordinate match.
        normalized = np.array([str(c or "").casefold() for c in countries])
        coarse &= (normalized == scope.country.casefold()) | (normalized == "")
    indices = np.flatnonzero(coarse)
    lat = np.radians(latitudes[indices])
    center = math.radians(scope.latitude)
    a = np.sin((lat - center) / 2) ** 2 + np.cos(center) * np.cos(lat) * (
        np.sin(np.radians(longitudes[indices] - scope.longitude) / 2) ** 2
    )
    distances = 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    exact = np.zeros(len(latitudes), dtype=bool)
    exact[indices[distances <= scope.radius_km + 1e-9]] = True
    return coarse, exact


def select_destinations(
    entities: Path,
    directory: Path,
    *,
    radius_km: float = 15,
    cap_per_destination: int = 384,
) -> dict:
    if cap_per_destination < 20:
        raise ValueError("A diagnostic destination sample must allow at least Top-20")
    geometry = pq.read_table(
        entities,
        columns=[
            "retrieval_entity_id",
            "latitude",
            "longitude",
            "country",
            "localities",
        ],
    )
    latitude = geometry["latitude"].to_numpy()
    longitude = geometry["longitude"].to_numpy()
    countries = np.array(geometry["country"].to_pylist(), dtype=object)
    ids = geometry["retrieval_entity_id"].to_pylist()
    localities = geometry["localities"].to_pylist()
    cells = defaultdict(list)
    for i in range(len(ids)):
        if countries[i] and valid_coordinates(latitude[i], longitude[i]):
            # Global grid candidates, not a handpicked city list or locality equality filter.
            cell = (countries[i], math.floor(latitude[i] * 4), math.floor(longitude[i] * 4))
            cells[cell].append(i)
    candidates = []
    for (country, cell_lat, cell_lon), indices in cells.items():
        if len(indices) < 40:
            continue
        candidates.append(
            {
                "country": country,
                "cell": [cell_lat, cell_lon],
                "cell_count": len(indices),
                "latitude": float(np.median(latitude[indices])),
                "longitude": float(np.median(longitude[indices])),
                "label": mode_text(value for i in indices for value in localities[i]) or country,
            }
        )
    candidates.sort(key=lambda row: (-row["cell_count"], row["country"], row["cell"]))
    chosen = []
    used_countries = set()
    for tier, minimum, maximum in (
        ("high", 3000, math.inf),
        ("medium", 300, 3000),
        ("low", 40, 300),
    ):
        for candidate in candidates:
            if candidate["country"] in used_countries:
                continue
            if not minimum <= candidate["cell_count"] < maximum:
                continue
            scope = GeographicScope(
                latitude=candidate["latitude"],
                longitude=candidate["longitude"],
                radius_km=radius_km,
                country=candidate["country"],
            )
            start = perf_counter()
            coarse, exact = geographic_mask(latitude, longitude, countries, scope)
            elapsed = perf_counter() - start
            # Strata reflect actual radius-filtered global counts as well as the seed grid.
            if not minimum <= int(exact.sum()) < maximum:
                continue
            pool = np.flatnonzero(exact).tolist()
            pool.sort(key=lambda i: hashlib.sha256(ids[i].encode()).hexdigest())
            sample = pool[:cap_per_destination]
            destination = {
                **candidate,
                "tier": tier,
                "scope": scope.model_dump(),
                "bounding_box_count": int(coarse.sum()),
                "global_radius_count": int(exact.sum()),
                "filter_seconds": elapsed,
                "sample_count": len(sample),
                "sample_fraction": len(sample) / len(pool),
                "sample_entity_ids": sorted(ids[i] for i in sample),
            }
            chosen.append(destination)
            used_countries.add(candidate["country"])
            if sum(item["tier"] == tier for item in chosen) == 2:
                break
    if len(chosen) != 6:
        raise ValueError("Corpus does not supply two distinct-country destinations per stratum")
    selected_ids = sorted({value for row in chosen for value in row["sample_entity_ids"]})
    selected_set = set(selected_ids)
    table = pq.read_table(entities)
    selected = table.filter(pa.array([value in selected_set for value in ids]))
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "sample_entities.parquet"
    temporary = output.with_suffix(".parquet.part")
    pq.write_table(selected, temporary, compression="zstd", version="2.6")
    if output.exists() and sha256_file(output) == sha256_file(temporary):
        temporary.unlink()
    else:
        temporary.replace(output)
    report = {
        "sampling_version": "tripworld-geographic-spike-v1",
        "entity_artifact_sha256": sha256_file(entities),
        "global_entity_count": len(ids),
        "sample_artifact_sha256": sha256_file(output),
        "sample_entity_count": len(selected),
        "method": (
            "0.25-degree global grid seeds; high >=3000, medium 300-2999, low 40-299 entities "
            "in both grid and radius; descending seed coverage; two countries per tier; "
            "six distinct countries; uniform deterministic SHA256(entity ID) cap per destination"
        ),
        "candidate_cell_count": len(candidates),
        "cap_per_destination": cap_per_destination,
        "destinations": chosen,
        "limitations": (
            "Geographic proxy centers are derived from the corpus, not geocoded city boundaries. "
            "Exact retrieval is over sampled entities only; unsampled relevant POIs can be absent. "
            "This is a development spike, not a benchmark or global recall estimate."
        ),
    }
    write_json_if_changed(directory / "destinations.json", report)
    return report
