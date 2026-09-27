"""Batch-local wire references; canonical identities never depend on output order."""

import hashlib
import json

from backend.app.schemas.poi_semantics import SemanticAssessmentBatch

PROJECTION_VERSION = "poi_semantics_wire_1"


class SemanticProjection:
    def __init__(self, places, canonical_payload):
        self.candidates = {f"p{i:02d}": p for i, p in enumerate(places, 1)}
        self.sources = {f"e{i:02d}": p.source_ref for i, p in enumerate(places, 1)}
        reverse = {p.place_id: ref for ref, p in self.candidates.items()}
        data = json.loads(canonical_payload)
        self.bindings = {
            key: reverse[pid]
            for key, pid in data["application_named_bindings"].items()
            if pid in reverse
        }
        data["application_named_bindings"] = self.bindings
        data["wire_version"] = PROJECTION_VERSION
        self.places = []
        for i, row in enumerate(data["places"], 1):
            row.pop("place_id")
            row["candidate_ref"] = f"p{i:02d}"
            row["source_ref"] = f"e{i:02d}"
            self.places.append(
                places[i - 1].model_copy(
                    update={"place_id": row["candidate_ref"], "source_ref": row["source_ref"]}
                )
            )
        self.payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.mapping = {
            ref: {"place_id": p.place_id, "source_ref": p.source_ref, "evidence_ref": f"e{i:02d}"}
            for i, (ref, p) in enumerate(self.candidates.items(), 1)
        }
        self.sha256 = hashlib.sha256(json.dumps(self.mapping, sort_keys=True).encode()).hexdigest()

    def resolve(self, validated):
        """Expand only after complete coverage and evidence ownership validation."""
        rows = []
        for assessment in validated.assessments:
            row = assessment.model_dump(mode="json")
            row["place_id"] = self.candidates[row["place_id"]].place_id
            row["evidence_refs"] = [self.sources[ref] for ref in row["evidence_refs"]]
            for match in row["matches"]:
                match["evidence_refs"] = [self.sources[ref] for ref in match["evidence_refs"]]
            rows.append(row)
        return SemanticAssessmentBatch.model_validate({"assessments": rows})
