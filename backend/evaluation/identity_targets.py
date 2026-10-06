"""Version-owned target judgments over shared independent acquisition references."""

from .identity import _intake_dict, _observation_index, identity_references
from .records import canonical_digest


def versioned_references(intake):
    """Share source evidence, never target judgments, between submitted versions."""
    prepared = _intake_dict(intake)
    groups = {g["group_id"]: g for g in prepared["inventory"]}
    references = []
    for ref in identity_references(prepared):
        if ref["kind"] != "requirement_subject":
            references.append(ref)
            continue
        group = groups[ref["group_id"]]
        subject = next(
            s
            for s in group["requirement_spec"]["subjects"]
            if s["subject_id"] == ref["source"]["subject_id"]
        )
        for version in ("v0", "v1", "v2", "v3"):
            if version not in group["runs"]:
                continue
            source = {**ref["source"], "version": version}
            references.append(
                {
                    **ref,
                    "source": source,
                    "reference_id": canonical_digest(source),
                    "audit_key": canonical_digest(source),
                    "version": version,
                    "claimed_place_id": subject.get("source_place_id"),
                    "evidence_reference_id": ref["reference_id"],
                }
            )
    return references


def versioned_observations(intake, evidence, references):
    prepared = _intake_dict(intake)
    observed = _observation_index(
        evidence, identity_references(prepared), prepared, allow_incomplete=True
    )
    return {
        ref["reference_id"]: observed[origin]
        for ref in references
        if (origin := ref.get("evidence_reference_id", ref["reference_id"])) in observed
    }
