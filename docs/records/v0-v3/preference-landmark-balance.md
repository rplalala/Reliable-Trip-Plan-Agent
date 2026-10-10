# Soft preference and landmark balance decisions

2026-09-28. Status: approved feature closeout, Implemented and offline Validated, with
one bounded subsequent focus revalidation. Current policy belongs to
[requirements/evidence](../../0002-requirements-evidence.md); historical pilot outputs
remain in the [V3 pilot record](v3-preference-landmark-pilot.md).

<a id="preference-landmark-balance-focus-convergence"></a>

## Focus convergence and grounded fulfillment

The initial three-case pilot completed, but Melbourne interpreted focus as a themed
whole-trip goal without target two. The approved convergence retained ordinary soft
interests at target one and exact sourced current-trip focus at two. Explicit quantities,
exclusions and category-only restrictions kept their own semantics. These targets were
not maxima; independent same-category landmarks retained value after preference saturation.
Only distinct supported scheduled POIs counted toward fulfillment, not candidate supply.

Domain/Foundry goal enums narrowed to ordinary/exclusive scope. Shared eligibility covered
whole-trip category goals so a scope label could not erase target/provenance. General
exploration was bypassed only by explicit exclusive scope. Prompt 18/wire 12 identified the
narrowed contract; canonical envelope 4 remained. Old themed payloads stayed historical
evidence, were invalid as new inputs and were not migrated into focus claims.

Regressions reproduced null `soft_coverage`, accepted themed enums and stale capture
prompt 17 metadata. Corrections aligned eligibility, DTO/domain validation and tool metadata.
The entry test retained target 2/matched 1/remaining 1, supplied alternatives and independent
landmark value rather than counting supply as fulfilled. An unsupplied synthetic POI fixture
was corrected without loosening production rules. Hard/count/Repair authority and budgets
were unchanged; V0 remained plain LLM and V1–V3 independently runnable.

## Validation and subsequent live outcome

The original Ticket 03 gate was **1793 passed, 9 skipped**. Convergence from `cc4d5a0`
passed **1807, 9 skipped**, 75.57 seconds; focused tests **48 passed**. Broader **109/110**
passed with one stale capture-version failure, then that nine-test file passed after fix.
Both review axes closed all findings; no backend static type checker was configured.

The separately approved unchanged-input Melbourne V3 attempt completed in **99.781 seconds**:
museums **2/2**, architecture **2/1**, gardens **1/1**. Eight qualified nominees reached
supply, six were in the **8-visit** itinerary (**3/3/2**). Captures were complete and
budgets within bounds; initial equalled final, Repair did not run and **11 UNKNOWN**
findings remained. No automatic retry occurred. See
[initial pilot](v3-preference-landmark-pilot.md#preference-landmark-balance-pilot-assessment)
and [revalidation](v3-preference-landmark-pilot.md#preference-landmark-balance-pilot-focus-revalidation-assessment).

The final closeout full gate passed **1808, 9 skipped**, 77.43 seconds, with Ruff/format/
diff checks. A prior interrupted run near existing embedding timeout/cancellation tests
was not counted as passing. The isolated retrieval suite passed **16**; a mock's 20-ms
deadline/unbounded entry wait suggested a scheduling race, not a reproduced production
defect. No retrieval code/test changed. Launcher/capture checks passed **11**. These
runs overlap and are not additive. Implementation/tool revisions: `4084a2f`, `274ab27`.
Original execution manifests/hashes were not altered by later commits or formatting.

## Parent-scenario evidence map

Controlled collaborators verify contract, selection, failure/budget and presentation
behavior. The original scenario mapping is retained for finding specific regressions:

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

Dedicated entry fixtures are `services/test_balanced_landmarks.py`; independent
version/quantity/identity/API regressions were included in the full backend gate.
No fake itinerary proves a live model consistently follows guidance.

## Remaining limits

Brisbane's maximum-three wording remained style preference, not a new executable count
validator. Melbourne's relatively light third day and self-guided-tour visit object
remained observations for possible separately scoped scrutiny. Fees/access/hours and
whole-trip affordability were not certified, Repair was not exercised by the accepted
focus run, and no cross-version superiority or universal model reliability was established.
The old pilot's failure remains unchanged after later success.
