# Activity scope and route adjacency — draft

Status: Shared evaluation scope consolidated; uncommitted locationless free-time use accepted; same-canonical route N/A accepted; inter-day travel excluded to align with checked current product scope. Not frozen or implemented.
Date: 2026-09-28.
Source: itinerary schema, itinerary_output and itinerary_schedule at checkpoint 8a435e2db0198e4fc8928b85e333b45b66c0c981; uncommitted documentation.

## Purpose and ownership

Use one version-neutral activity inventory to define visit counts, grounding, opening applicability, repetition, density and route adjacency. Preserve original artifacts. Evaluation-derived role decisions do not edit the itinerary. Quality scoring must not import planner OutputRoleSummary, schedule.lineage, Repair scope or candidate membership as ground truth.

Current public roles are main_poi, generic_activity, transport, free_time and unknown. Nearby is a separate unscheduled reference collection. Existing OutputRoleSummary includes every scheduled source_place_id without a main-visit distinction, so it is not the evaluator's visit denominator. The planner's elastic free-time classification depends on generation provenance and interpreted requirements unavailable to the independent quality reader; its result cannot be reused as a verdict.

## One-POI delivery constraint

The user confirms that a qualified itinerary cannot combine multiple POIs into one activity with a shared interval. Each primary visit represents one POI with its own explicit time span. Benchmark construction owns this qualification rule. If such a malformed block is nevertheless delivered, Evaluation returns an input-contract diagnostic, does not split visits/times, and does not silently score it as two complete visits. This is material conformance, not a new planner completion review.

## Shared inventory and confirmed scope

| Item | Evaluation treatment |
| --- | --- |
| Main visit | Retain as a scheduled visit even if canonical identity is unresolved; missing identity does not remove it from grounding coverage. |
| Concrete named visit labelled generic/unknown | Review role using output evidence; cannot evade checks merely through a role label. Preserve original label, independent decision and reasons. Exact automatic role rules remain OPEN. |
| Generic activity without a specific place | Treat as free-time/transition-like, preserving source role/text. Do not invent a venue; reviewed protected time remains occupied. |
| Transport activity / bound Transfer | Route-related record, not a primary visit. Reconcile representations of the same leg so it is not counted twice. |
| Free time | Not a primary visit. Uncommitted time can be travel slack under the accepted rule below. |
| Nearby | Excluded from main-visit counts, REQUIRED satisfaction, opening and main-route adjacency. |

Count visit occurrences, not unique IDs, for daily density and visit count; canonical uniqueness is a separate statistic. Same-place occurrences remain visible for repetition and minimum/exact/date obligations. A unresolved role remains a structural-evaluability observation, not a silent denominator deletion or automatic false place. Overlap and occupied-time calculations must reconcile a transport activity and a Transfer representing the same journey; their duplicate representation is not automatically two overlapping commitments.

## Adjacency and occupancy

Build the schedule from delivered activity timestamps and reviewed protected intervals, with stable source references. Independent identity resolution supplies endpoints; timestamps, mode and role ambiguities remain explicit. Sorting for evaluation does not rewrite the source order. Role-based visit metrics and occupancy are distinct: something outside POI counts can still occupy time or imply an intermediate location.

A plain A-to-B gap can use its applicable continuous interval. Generic no-POI placeholders do not create extra venue legs or unknown-location blockers. Reviewed protected intervals remain blockers: do not aggregate disjoint windows around them. Concrete named visits remain endpoints even when identity is unresolved; their uncertainty must not be erased by reclassifying them as free time.

Independently supplied mode rules, per-mode product caps, DRIVE reserve and five-minute route tolerances remain as accepted in the route contract. The activity-scope contract introduces no extra travel allowance.

## Scope decisions and code confirmation

1. Accepted locationless free-time rule: an explicitly free_time slot with no place/location, no stated reservation/commitment and no conflicting reviewed protected-time requirement may be used as travel slack. Fixed rest or any stated commitment cannot be consumed. If the role/text conflicts or flexibility is uncertain, retain an unresolved occupancy reason rather than assuming slack. Do not import V3 lineage to make this decision.
2. Day boundary: the user identifies overnight accommodation as outside product scope. Read-only code confirms V0 prompts same-day transport and shared initial-route binding, V3 transition binding and final diagnostics pair activities inside each day. Evaluation therefore does not create or score an inter-day last-POI-to-first-POI route. The earlier suggestion to add explicit cross-day journey checking is withdrawn as unnecessary scope expansion. Unexpected cross-day output is retained as out-of-scope information, not silently promoted into the v1 route denominator.
3. Accepted same-canonical venue rule: consecutive visits to the same independently confirmed venue do not create an inter-venue route leg; classify it N/A with a same-place reason, not an observed zero-duration PASS. Keep both visits in count/repetition/overlap checks and do not assume movement between different venues sharing an address is zero. Explicit distinct entrances or internal travel not resolved by the venue-level identity remain a documented scope limitation.

## Simple examples

A museum ends at 10:00, locationless free time occupies 10:00-10:30, and the next museum starts 10:30. Under the accepted free-time rule, that slot can accommodate the transfer if it is genuinely uncommitted; a reviewed fixed rest interval cannot. The evaluator does not move the museums to create more time.

Day 1 ends at A and day 2 starts at B: under the day-boundary scope, do not invent an overnight A-to-B leg. Two adjacent blocks at the same museum remain two recorded visit occurrences but do not each create a new between-venue transfer under the accepted same-place rule.

These are rule illustrations, not benchmark cases or observed results.

## Remaining technical contracts

Place-bearing role adjudication and audit, timestamp timezone consistency, generic intermediate activities, transfer/activity correspondence, overlap deduplication, and metric-specific structural denominators remain OPEN. Do not claim these details are frozen by the three proposals above.

## Future checks

Independent fixtures should verify unknown identity stays in visit coverage, role conflicts do not evade checks, Nearby cannot satisfy REQUIRED, transport representations are not double-counted, free-time proposals do not consume protected commitments, exclusion of inter-day travel, and same-ID versus same-address distinction. No fixtures or tests are implemented or executed by this document.


## Day-boundary source references

- V0 prompt: backend/app/versions/v0/prompts.py, same-day transport instruction.
- Shared initial transfer binding: backend/app/services/initial_routes.py, bind loops per itinerary day and pairs adjacent ordered activities within that day.
- V3 repair binding: backend/app/versions/v3/repair_routes.py, bind_transitions follows the same per-day pairing structure.
- V3 final diagnostics: backend/app/versions/v3/wiring.py, per-day ordered adjacent pairs.

A provider matrix may contain candidate pairs before scheduling; that does not establish an adopted inter-day itinerary transition. This is code inspection, not an executed end-to-end guarantee about arbitrary model text.


## Generic no-POI activities: superseding user decision

The latest user decision supersedes excluding generic no-POI activities from benchmark delivery: treat such items as free_time/transition-like for evaluation, without counting them as primary visits or inventing a venue. Preserve the original output role/text and record the evaluation classification. This does not erase explicit user-protected time or reclassify a concretely named but unresolved POI as free time. Ordinary no-POI placeholders alone do not disqualify a group.
