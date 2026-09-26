"""Unpublished deduplication branches; no coverage waiver or published partial deletion."""

from backend.app.versions.v3.repair_feedback import digest
from backend.app.versions.v3.repair_models import RepairPatch


def day_snapshot(itinerary, dates):
    return [d.model_dump(mode="json") for d in itinerary.days if str(d.date) in dates]


def retain_pending(budget, original, proposal, component, dependencies, after, comparison, spatial):
    """Only an otherwise valid deduplication group waiting for coverage may be pending."""
    reasons = set(comparison.reason.split("; "))
    if not spatial["accepted"] or not reasons <= {
        "New confirmed conflict",
        "Coverage regression is not authorized",
        "Review compensation must succeed atomically",
    }:
        return False
    dates = sorted(v for k, v in dependencies if k == "date")
    if any(
        f.status == "CONFIRMED" and f.check != "coverage" and set(map(str, f.dates)) & set(dates)
        for f in after.findings
    ):
        return False
    if not any(e.operation == "delete" for e in component.edits):
        return False
    entry = {
        "group_id": digest(component.model_dump(mode="json")),
        "status": "pending",
        "dates": dates,
        "base": digest(day_snapshot(original, dates)),
        "edits": component.model_dump(mode="json")["edits"],
        "proposal_days": day_snapshot(proposal, dates),
        "reason": "deduplication_awaiting_atomic_compensation",
    }
    groups = [g for g in getattr(budget, "pending_groups", []) if not set(g["dates"]) & set(dates)]
    if sum(len(g["edits"]) for g in groups) + len(entry["edits"]) > 50:
        return False
    budget.pending_groups = [*groups, entry]
    return True


def active_pending(budget, original):
    groups = getattr(budget, "pending_groups", [])
    # Independent accepted changes never depend on these dates. Recheck rather than overwrite.
    active = [g for g in groups if g["base"] == digest(day_snapshot(original, g["dates"]))]
    budget.pending_groups = active
    return tuple(active)


def combine_pending(patch, groups):
    """The model is told pending edits remain in the atomic proposal, never adopted yet."""
    submitted_ids = {e.activity_id for e in patch.edits if e.activity_id}
    edits = [e for g in groups for e in g["edits"] if e.get("activity_id") not in submitted_ids]
    return RepairPatch.model_validate(
        {
            "edits": [*edits, *[e.model_dump() for e in patch.edits]],
            "target_dispositions": patch.target_dispositions,
        }
    )


def complete_pending(budget, dependencies):
    dates = {v for k, v in dependencies if k == "date"}
    budget.pending_groups = [
        g for g in getattr(budget, "pending_groups", []) if not set(g["dates"]) & dates
    ]
