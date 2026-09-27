# 01: Carry soft preference coverage through planning and feedback

**What to build:** Travelers receive planning guidance that covers each ordinary
POI-based positive preference once, or twice when the original request explicitly
identifies it as a focus of this trip. Coverage is assessed from the final itinerary,
with truthful gaps and preserved explicit requirements. V0 expresses the same
principles through its existing prompts without new tools or enforcement stages.

**Parent:** [Preference coverage and local landmark balance](../spec.md).

**Blocked by:** None (can start immediately).

Status: resolved
Type: task

## Acceptance criteria

- [x] An ordinary independently interpretable POI preference has a soft target of
  one distinct qualifying scheduled POI. A current-trip focus has two only when
  backed by exact original user text. Emotional intensity alone and ambiguous
  focus wording retain one.
- [x] Product-derived soft targets and their provenance are represented separately
  from explicit user quantities. Existing exact/minimum/maximum fields are not
  populated with inferred one/two values. Explicit quantities, exclusions and
  exclusive scopes retain precedence.
- [x] Whole-trip enjoyment, relaxation and travel-burden goals do not gain a
  POI-count fulfillment claim. Vague preferences do not create artificial quotas.
- [x] One supported scheduled POI can cover multiple independent preferences.
  References, candidate-only matches and repeated visits to the same canonical
  identity do not inflate distinct coverage. Unresolved matches remain uncertain.
- [x] Grounded versions expose final scheduled coverage, target origin and remaining
  soft gaps through compatible existing progress/presentation mechanisms. They do
  not label a matching but unscheduled candidate as fulfilled.
- [x] Generation guidance stops adding priority for a satisfied preference while
  allowing further same-category places for independent merit or another uncovered
  preference. One/two is not a category maximum or an inferred trip proportion.
- [x] When interests compete with feasible scheduling, incomplete soft coverage is
  allowed and reported. The planner does not overcrowd the trip merely to cover
  every preference.
- [x] A soft gap alone does not generate a CONFIRMED violation, change scoped policy
  completion into a global quality claim, or authorize a new V3 Repair target.
- [x] V0 receives prompt-level coverage and classic-sight planning principles in its
  existing LLM flow. It acquires no nomination call, external identity resolver,
  candidate pipeline or additional enforcement stage; name-based observations do
  not become canonical evidence-backed fulfillment claims.
- [x] V1/V2 retain their no-Repair boundary and V3 retains existing validation/Repair
  authority. Independent version entry points and saved-output compatibility remain
  intact; any shared contract additions preserve their documented meaning.
- [x] Tests through existing injected planning boundaries cover ordinary/focus/
  emotional/ambiguous wording, explicit counts and restrictions, multi-interest
  coverage, unsupported matches, repeated identities, candidate-only coverage,
  constrained schedules and the V0 mechanism boundary.
- [x] Tests observe output/progress contracts and generation-boundary instructions;
  they do not claim that fake model responses establish live preference accuracy.
  V0 checks do not expect canonical counting that its architecture cannot support.
- [x] Relevant focused checks, shared-contract regression, Standards/Spec review and
  necessary corrections are complete. Related current design/configuration and
  presentation documentation describe implemented behavior and remaining limits.

## Verification and handoff

Use the accepted existing planning entry points with injected fake model/place/route/
retrieval collaborators. Include affected API/presentation consumers if progress
fields change. Run the full relevant backend suite when shared contracts change,
plus applicable lint/format checks. Include meaningful cross-version behavior checks
without asserting private helper order.

Deliver the soft-target/provenance contract, generation guidance and observable final
coverage path. Ticket 03 consumes these semantics when balancing actual candidate
opportunities with landmark metadata. Candidate selection is not final fulfillment;
do not reduce the eligible pool to exactly one/two matching candidates in this slice.

## Boundaries

Landmark nomination and search allocation belong to ticket 02. Combined landmark/
preference candidate prioritization belongs to ticket 03. Existing budgets remain
unchanged. No new live calls, formal evaluation, food-support capability, parent-site
mechanism, Git action or freeze is included in this ticket.

## Comments

- 2026-09-27: The user invoked implement after the recommendation to start ticket 01.
  Implementation is authorized with offline tests and review; no live or Git actions.

- 2026-09-27: The user approved this three-ticket breakdown and the two independent
  starting tickets. Publication is authorized; implementation remains pending.


## Answer

Implemented and offline validated on 2026-09-27 against uncommitted base `8f5e9b3`.
Soft targets/provenance, prompt guidance, grounded final diagnostics and Product feedback
are delivered. V0 remains prompt-only; V3 retains its prior Repair authority. Final tests:
1750 backend passed / 9 skipped, 83 frontend passed, TypeScript and scoped Ruff passed.
Standards/Spec review have zero remaining findings. No live quality claim or Git action.
See [current requirements](../../../docs/shared_requirements.md) and the
[Decisions-so-far](../map.md#decisions-so-far) handoff. Tickets 02/03 remain pending.
