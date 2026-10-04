"""Offline evaluator assistance uses reversible references without identity adoption."""

import pytest

from backend.evaluation.identity_assistance import IdentityAssistancePacket


def test_identity_proposals_restore_source_links_and_reject_cross_case_candidate():
    cases = [
        {
            "reference_id": "a" * 64,
            "claim": {"place_name": "Museum A"},
            "candidates": [{"place_id": "ChIJ" + "a" * 30, "display_name": "Museum A"}],
        },
        {
            "reference_id": "b" * 64,
            "claim": {"place_name": "Museum B"},
            "candidates": [{"place_id": "ChIJ" + "b" * 30, "display_name": "Museum B"}],
        },
    ]
    packet = IdentityAssistancePacket(cases)
    assert packet.payload["cases"][0]["reference_id"] == "r01"
    assert packet.payload["cases"][0]["candidates"][0]["place_id"] == "p01"
    wire = {
        "decisions": [
            {
                "reference_id": "r01",
                "decision": "match",
                "candidate_id": "p01",
                "rationale": "Name and location",
                "evidence_fields": ["display_name"],
            },
            {
                "reference_id": "r02",
                "decision": "unknown",
                "candidate_id": None,
                "rationale": "Insufficient",
                "evidence_fields": [],
            },
        ]
    }
    result = packet.resolve(wire)
    assert result["decisions"][0]["reference_id"] == "a" * 64
    assert result["decisions"][0]["candidate_id"] == "ChIJ" + "a" * 30
    wire["decisions"][0]["candidate_id"] = "p02"
    with pytest.raises(ValueError, match="candidate"):
        packet.resolve(wire)


@pytest.mark.parametrize(
    "rows",
    [
        [],
        [("r01", "match", "p01"), ("r01", "match", "p01")],
        [("r99", "match", "p01")],
        [("r01", "match", "p99")],
        [("r01", "unknown", "p01")],
        [("r01", "no_supported_match", "p01")],
    ],
)
def test_identity_packet_rejects_missing_duplicate_and_unbound_decisions(rows):
    packet = IdentityAssistancePacket(
        [{"reference_id": "a" * 64, "candidates": [{"place_id": "ChIJ" + "a" * 40}]}]
    )
    with pytest.raises(ValueError):
        packet.resolve(
            {
                "decisions": [
                    {
                        "reference_id": ref,
                        "decision": decision,
                        "candidate_id": candidate,
                        "rationale": "Observed candidate",
                        "evidence_fields": [],
                    }
                    for ref, decision, candidate in rows
                ]
            }
        )
