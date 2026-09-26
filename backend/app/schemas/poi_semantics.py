"""Model-authored semantic judgments; never provider or operating facts."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SEMANTICS_VERSION = "poi_semantics_1"


class SemanticContract(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class RequirementMatch(SemanticContract):
    requirement_id: str
    relation: Literal["supported", "related_alternative", "mismatch", "unresolved"]
    evidence_refs: list[str] = Field(max_length=8)


class POISemanticAssessment(SemanticContract):
    place_id: str = Field(min_length=1)
    visit_object: str = Field(min_length=1, max_length=200)
    role: Literal["attraction", "exception_only", "non_main", "unresolved"]
    categories: list[str] = Field(max_length=4)
    reason: str = Field(min_length=1, max_length=480)
    evidence_refs: list[str] = Field(max_length=8)
    matches: list[RequirementMatch] = Field(max_length=24)
    exception_requirement_ids: list[str] = Field(max_length=4)

    @property
    def main_eligible(self):
        return self.role == "attraction" or (
            self.role == "exception_only" and bool(self.exception_requirement_ids)
        )


class SemanticAssessmentBatch(SemanticContract):
    assessments: list[POISemanticAssessment] = Field(min_length=1, max_length=32)


class SemanticAssessmentError(RuntimeError):
    """Terminal system error: never a user rewrite or successful Repair fallback."""

    def __init__(self, message, *, details=None):
        super().__init__(message)
        self.details = details or {}


class SemanticPreparationLimit(RuntimeError):
    """Pre-send engineering stop; already assessed material remains usable."""


class FoundryRequirementMatch(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    requirement_id: str
    relation: Literal["supported", "related_alternative", "mismatch", "unresolved"]
    evidence_refs: list[str]


class FoundryPOIAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    place_id: str
    visit_object: str
    role: Literal["attraction", "exception_only", "non_main", "unresolved"]
    categories: list[str]
    reason: str
    evidence_refs: list[str]
    matches: list[FoundryRequirementMatch]
    exception_requirement_ids: list[str]


class FoundrySemanticAssessmentBatch(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    assessments: list[FoundryPOIAssessment]
