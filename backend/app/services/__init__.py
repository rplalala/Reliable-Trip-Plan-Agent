"""Application services coordinating product and developer use cases."""

from backend.app.services.evidence_acquisition import (
    NoViableCandidatesError,
    V1EvidenceAcquisitionService,
)

__all__ = [
    "DeveloperPlanningService",
    "NoViableCandidatesError",
    "PlanningFailedError",
    "PlanningNeedsClarificationError",
    "PlanningService",
    "V1EvidenceAcquisitionService",
]


def __getattr__(name):
    """Load planner exports only on demand; leaf services must not import graphs."""
    if name in {
        "DeveloperPlanningService", "PlanningFailedError",
        "PlanningNeedsClarificationError", "PlanningService",
    }:
        from backend.app.services import planning
        return getattr(planning, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
