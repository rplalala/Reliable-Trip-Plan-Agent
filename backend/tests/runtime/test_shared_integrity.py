"""Shared integrity definitions survive the runtime/offline responsibility split."""

import ast
from pathlib import Path

from backend.app.runtime.fingerprints import digest
from backend.app.tripworld.artifacts import canonical_json_bytes, payload_fingerprint
from backend.app.tripworld.database.vectors import SPACE_ID
from backend.app.tripworld.retrieval.embedding import validate_vectors
from tools.data.tripworld import artifact_persistence, embedding_build, openai_adapter, vector_store
from tools.validation import requirement_acceptance


def test_tools_use_the_same_integrity_definitions():
    assert artifact_persistence.canonical_json_bytes is canonical_json_bytes
    assert embedding_build.validate_vectors is validate_vectors
    assert openai_adapter.validate_vectors is validate_vectors
    assert vector_store.validate_vectors is validate_vectors
    assert requirement_acceptance.digest is digest


def test_existing_hash_formats_and_space_identity_are_unchanged():
    payload = {"b": [1, None], "a": "caf\u00e9"}
    assert digest(payload) == "e0940afa0b71ca57d9b4126b3ff5f25de2017f681eca3ff7c04c6a50d07fc1d0"
    assert payload_fingerprint(payload) == (
        "6b2b85cca54036023392f22a48a8332155105a8abec65282e591eb17fa2b78fe"
    )
    assert SPACE_ID == "afa5ba967bb4dbf2978e5a8e99b1f9dca25a4e1e23a4c51f8cfe8572113259ec"


def test_artifact_persistence_preserves_fingerprint_and_reuse(tmp_path):
    value = {"b": [1, None], "a": "cafe"}
    path = tmp_path / "artifact.json"
    assert artifact_persistence.write_json_if_changed(path, value)
    assert path.read_bytes() == canonical_json_bytes(value)
    assert not artifact_persistence.write_json_if_changed(path, value)
    assert payload_fingerprint(value) == payload_fingerprint(dict(reversed(list(value.items()))))


def test_runtime_contains_no_offline_definitions_or_imports():
    root = Path(__file__).resolve().parents[3] / "backend/app"
    offline_names = {
        "DevelopmentRequirementCapture", "EmbeddingConfig", "EmbeddingProvider", "EncodedBatch",
        "write_json_if_changed", "write_text_if_changed", "artifact_is_current",
        "SourceSchemaError", "validate_source_schema", "production_config",
    }
    for path in root.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                assert node.name not in offline_names, (path, node.name)
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith("tools"), path
                assert not ({a.name for a in node.names} & offline_names), path
