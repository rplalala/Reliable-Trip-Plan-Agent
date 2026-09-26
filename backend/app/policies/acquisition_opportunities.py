"""Source-neutral typed acquisition opportunities; no model or provider scores."""

from collections import Counter
from math import ceil

from backend.app.policies.planning_supply import _distance


def opportunity_order(places, required, contract, destination, *, exploration_fraction=0):
    by_id = {p.candidate.place_id: p for p in places}
    chosen = sorted(set(required) & by_id.keys())
    requirements = {r.requirement_id: r for r in contract.semantic_requirements}
    strength = {"hard": 0, "high": 1, "medium": 2, "low": 3}
    buckets = {}
    for intent in contract.discovery_intents:
        for ref in set(intent.requirement_refs):
            req = requirements[ref]
            if req.polarity != "favor":
                continue
            for subject in set(req.subject_refs):
                key = (strength[req.strength], subject, intent.intent_id)
                buckets.setdefault(key, set()).update(
                    pid
                    for pid, place in by_id.items()
                    if intent.intent_id in place.discovery_intent_ids
                )
    for named in contract.named_places:
        if named.inclusion != "EXCLUDED":
            buckets[(1 if named.inclusion == "REQUIRED" else 2, "party", named.requirement_id)] = {
                pid for pid, p in by_id.items() if named.requirement_id in p.discovery_intent_ids
            }
    subjects, intents = Counter(), Counter()
    themed = any(
        r.experience_goal and r.experience_goal.trip_scope in {"themed", "exclusive"}
        for r in contract.semantic_requirements
    )
    optional_count = 0
    categories = Counter(by_id[p].candidate.primary_type for p in chosen)
    while len(chosen) < len(by_id):
        remaining = by_id.keys() - set(chosen)
        active = {key: ids & remaining for key, ids in buckets.items() if ids & remaining}
        key = (
            min(active, key=lambda k: (k[0], subjects[k[:2]], k[1], intents[k], k[2]))
            if active
            else None
        )
        cohort = active[key] if key else remaining
        general = remaining - set().union(*buckets.values()) if buckets else remaining
        if (
            not themed
            and general
            and exploration_fraction
            and (
                ceil((optional_count + 1) * exploration_fraction)
                > ceil(optional_count * exploration_fraction)
            )
        ):
            key, cohort = None, general

        def tie(pid):
            candidate = by_id[pid].candidate
            return (
                categories[candidate.primary_type] if candidate.primary_type else 0,
                _distance(candidate, (destination.latitude, destination.longitude)),
                pid,
            )

        pid = min(cohort, key=tie)
        chosen.append(pid)
        optional_count += 1
        if by_id[pid].candidate.primary_type:
            categories[by_id[pid].candidate.primary_type] += 1
        if key:
            subjects[key[:2]] += 1
            intents[key] += 1
    return tuple(chosen)
