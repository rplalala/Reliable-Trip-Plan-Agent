"""Fixtures for deterministic TripWorld data-preparation tests."""

from pathlib import Path

import pytest

from backend.app.tripworld.manifest import TripWorldManifest, load_manifest
from backend.app.tripworld.semantics import CategorySemanticMapping, load_semantic_mapping
from backend.app.tripworld.source import sha256_file

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
TINY_SOURCE = (
    REPOSITORY_ROOT / "backend" / "tests" / "fixtures" / "tripworld" / ("metadata_tiny.parquet")
)


@pytest.fixture
def tiny_source() -> Path:
    return TINY_SOURCE


@pytest.fixture
def tripworld_manifest() -> TripWorldManifest:
    return load_manifest(REPOSITORY_ROOT / "data" / "tripworld" / "manifest.json")


@pytest.fixture
def tiny_manifest(tripworld_manifest: TripWorldManifest) -> TripWorldManifest:
    dataset = tripworld_manifest.dataset.model_copy(
        update={
            "sha256": sha256_file(TINY_SOURCE),
            "size_bytes": TINY_SOURCE.stat().st_size,
            "row_count": 6,
        }
    )
    return tripworld_manifest.model_copy(update={"dataset": dataset})


@pytest.fixture
def semantic_mapping() -> CategorySemanticMapping:
    return load_semantic_mapping(
        REPOSITORY_ROOT / "data" / "tripworld" / "category_semantics.v1.json"
    )
