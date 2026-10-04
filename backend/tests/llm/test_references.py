"""Request-local identity transport preserves canonical IDs and text."""

import pytest

from backend.model_references import ShortReferences


def test_round_trip_keeps_names_text_and_original_payload():
    long_id = "ChIJ" + "Z" * 40
    payload = {
        "place_id": long_id,
        "notes": long_id,
        "routes": [{"origin_place_id": long_id}],
        "places_by_id": {long_id: {"name": "Museum"}},
    }
    refs = ShortReferences(
        payload, {"place_id": "p", "origin_place_id": "p"}, keyed={"places_by_id": "p"}
    )
    wire = refs.encode(payload)
    assert wire["place_id"] == wire["routes"][0]["origin_place_id"] == "p01"
    assert wire["places_by_id"] == {"p01": {"name": "Museum"}}
    assert wire["notes"] == long_id and payload["place_id"] == long_id
    assert refs.decode({"place_id": "p01"}) == {"place_id": long_id}


def test_unknown_reference_and_canonical_echo_are_rejected():
    refs = ShortReferences({"place_id": "long-canonical-identity"}, {"place_id": "p"})
    for identifier in ("p99", "long-canonical-identity"):
        with pytest.raises(ValueError, match="Unknown model reference"):
            refs.decode({"place_id": identifier})
    assert refs.decode({"place_id": None}) == {"place_id": None}


def test_equal_prefixes_and_concurrent_packets_have_separate_exact_mappings():
    first, second = "same-prefix-" + "a" * 60, "same-prefix-" + "b" * 60
    one = ShortReferences({"place_ids": [first, second]}, {"place_ids": "p"})
    another = ShortReferences({"place_ids": [second]}, {"place_ids": "p"})
    assert one.decode({"place_ids": ["p02", "p01"]}) == {"place_ids": [second, first]}
    assert another.decode({"place_ids": ["p01"]}) == {"place_ids": [second]}
    assert one.sha256 != another.sha256


def test_output_enum_preserves_null_and_schema_input():
    schema = {"properties": {"place_id": {"anyOf": [{"type": "string"}, {"type": "null"}]}}}
    refs = ShortReferences({"place_id": "long"}, {"place_id": "p"})
    bounded = refs.constrain_schema(schema)
    assert bounded["properties"]["place_id"]["enum"] == ["p01", None]
    assert "enum" not in schema["properties"]["place_id"]
