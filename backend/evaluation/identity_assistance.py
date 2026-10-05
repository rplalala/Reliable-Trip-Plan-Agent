"""Offline wire packet for bounded identity proposals; no model calls or adoption."""

import json

from ..model_references import INSTRUCTION, ShortReferences


class IdentityAssistancePacket:
    """Expose only local references while preserving independent candidate ownership."""

    def __init__(self, cases, *, additional_fields=None):
        cases = json.loads(json.dumps(cases))
        ids = [case["reference_id"] for case in cases]
        if not ids or len(set(ids)) != len(ids):
            raise ValueError("Identity references must be nonempty and unique")
        self.candidates = {}
        for case in cases:
            candidates = [item["place_id"] for item in case["candidates"]]
            if len(set(candidates)) != len(candidates):
                raise ValueError("Duplicate identity candidate")
            self.candidates[case["reference_id"]] = set(candidates)
        self.references = ShortReferences(
            cases,
            {
                "reference_id": "r",
                "place_id": "p",
                "candidate_id": "p",
                **(additional_fields or {}),
            },
        )
        self.payload = {"instructions": INSTRUCTION, "cases": self.references.encode(cases)}
        self.manifest = self.references.manifest
        self.mapping_sha256 = self.references.sha256

    def constrain_schema(self, schema):
        return self.references.constrain_schema(schema)

    def resolve(self, proposals):
        """Return canonical proposals only, never a native human-adjudication envelope."""
        result = self.references.decode(proposals)
        rows = result["decisions"]
        ids = [row["reference_id"] for row in rows]
        if len(ids) != len(self.candidates) or set(ids) != set(self.candidates):
            raise ValueError("Missing or duplicate identity proposal")
        for row in rows:
            decision, candidate = row["decision"], row["candidate_id"]
            if decision == "match":
                if candidate not in self.candidates[row["reference_id"]]:
                    raise ValueError("Identity candidate does not belong to the reference")
            elif decision not in ("unknown", "no_supported_match") or candidate is not None:
                raise ValueError("Invalid identity proposal decision")
            if not isinstance(row["rationale"], str) or not row["rationale"].strip():
                raise ValueError("Identity proposal requires rationale")
            if not isinstance(row["evidence_fields"], list) or not all(
                isinstance(item, str) for item in row["evidence_fields"]
            ):
                raise ValueError("Invalid identity proposal evidence fields")
        return result
