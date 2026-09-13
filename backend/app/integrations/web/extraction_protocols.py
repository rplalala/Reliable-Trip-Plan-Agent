"""Tool-free semantic reasoning over already acquired official source blocks."""

from typing import Protocol, runtime_checkable

from backend.app.evidence.models import PlaceEvidence
from backend.app.evidence.official_models import EvidenceReasonerAssessment, EvidenceSourceBlock
from backend.app.evidence.web_models import WebEvidenceTask


@runtime_checkable
class OfficialEvidenceReasoner(Protocol):
    async def reason(
        self,
        task: WebEvidenceTask,
        sources: tuple[EvidenceSourceBlock, ...],
        baseline: PlaceEvidence,
    ) -> tuple[EvidenceReasonerAssessment, ...]:
        """Interpret bounded supplied source text without acquiring more information."""

        ...
