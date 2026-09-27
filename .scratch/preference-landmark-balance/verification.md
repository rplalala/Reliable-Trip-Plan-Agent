# Offline acceptance evidence map

Date: 2026-09-28. Base: `cc4d5a0`, with uncommitted ticket 03 changes.
This maps all parent-spec observable scenarios across the three implementation tickets.
Tests use controlled collaborators; they do not establish live quality or formal superiority.

| Parent scenario | Evidence under backend/tests | Observable coverage |
| --- | --- | --- |
| 1 | services/test_soft_preference_coverage.py | Ordinary/focus/emotional/ambiguous wording, exact provenance |
| 2 | services/test_landmark_discovery.py; policies/test_planning_supply.py; versions/v3/test_semantic_repair.py | Exclusion/exclusive admission, explicit quantities and maxima retain existing semantics |
| 3 | services/test_soft_preference_coverage.py; services/test_balanced_landmarks.py | Supported overlapping interests; distinct scheduled IDs; unsupported/repeated/reference exclusions |
| 4 | services/test_balanced_landmarks.py | Three same-category landmarks survive; multi-ref intent cannot bypass saturation |
| 5 | services/test_balanced_landmarks.py | Closed landmark excluded, replacements supplied; candidate supply not final fulfillment |
| 6 | services/test_balanced_landmarks.py; services/test_soft_preference_coverage.py | Eight interests/one day yields truthful gaps; broad goals retain non-count semantics |
| 7 | services/test_landmark_discovery.py; services/test_balanced_landmarks.py | General search with many interests; dense 63-candidate pools in three synthetic destinations |
| 8 | services/test_landmark_nomination.py; services/test_landmark_discovery.py | Destination-only nomination, no REQUIRED promotion, existing qualification |
| 9 | services/test_landmark_nomination.py; services/test_landmark_discovery.py | Exact reuse, ambiguity, alias rejection, later RAG identity changes |
| 10 | services/test_landmark_discovery.py | Named first, four within twelve, cache, exhausted and returned allocations |
| 11 | services/test_landmark_nomination.py; llm/azure_foundry/test_landmark_nomination_adapter.py | One send, strict DTO/token/deadline/timeout boundaries |
| 12 | services/test_landmark_nomination.py; services/test_landmark_discovery.py | Auxiliary fallback, cancellation, cleanup and unrelated hard errors |
| 13 | services/test_landmark_discovery.py; services/test_balanced_landmarks.py; services/test_quality_first.py | Roles, closed Details, unchanged resource/capacity checks |
| 14 | Shared FIRST_GENERATION_POLICY used by version runner tests | Variety, soft rank, dates/routes/time, explicit separate visits and no inferred site merge; prompt behavior is not live efficacy |
| 15 | services/test_landmark_nomination.py; services/test_soft_preference_coverage.py; versions/v0-v3 suites | Independent runners, V0 no nomination, V1/V2 no Repair, V3 no new soft-gap authority |
| 16 | observability/test_budget_summary.py; services/test_soft_preference_coverage.py; API/presentation suites | Missing usage retained; source-backed soft targets separate from counts |

Ticket 03 dedicated entry fixtures are in services/test_balanced_landmarks.py. Existing
quantity, identity, V3 and presentation regressions remain part of the full backend gate.
A fake generated itinerary cannot prove that a live model follows guidance. No live pilot,
formal experiment, version freeze, parent-site graph or new budget is claimed.
