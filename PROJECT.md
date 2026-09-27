# Capstone Project Context

## V0 transport and Nearby prompt alignment - 2026-09-28

The user requested transport and Nearby content across versions. V0 now explicitly
prompts same-day inter-visit transport activities with estimated times/modes and
uncertainty, plus one to three suitable nearby model-knowledge recommendations when
available. It remains one primary generation with no tools or added repair mechanism.
Transport uses existing activity_kind=transport, not provider-backed transfers;
references remain optional, unscheduled, capped at three, and empty when unsupported.
V1/V2 already attach Nearby through their shared post-itinerary service; both produced
three references in the Berlin run. No V1/V2/V3 behavior change was needed.
The authorized single Berlin V0 revalidation passed: six days, 17 main visits,
11 explicitly estimated transport activities and one contextual optional reference.
All inter-venue legs were represented without overlaps and roles counted separately.
Standards/Spec: zero findings; combined relevant regression: 176 passed; Ruff passed.
See the [acceptance record](.scratch/v0-transport-nearby/assessment.md). No real-world
route/access/cost verification or version freeze is implied.

## Trace capture limit adjustment - 2026-09-28

The user accepted V1 repeat visits as an observation within that version's limited
scope, not a current repair task, and authorized increasing the runtime trace payload
threshold to 10 MB (10,000,000 bytes). The configured threshold now applies to trace
and V3 audit capture; planning behavior and provider budgets are unchanged. Redaction,
raw-payload exclusion and oversized-payload truncation remain in place. The completed
Berlin batch retains its frozen 1 MB configuration and failed evidence gate; no trace
reconstruction is possible from the cap adjustment. Observability/config/V3 wiring
checks passed (92 tests); synthetic near-limit payload retention, truncation and
redaction checks passed. This cap adjustment itself adds no live or blind-review run.

## Preference and landmark feature closeout - 2026-09-28

The user accepted closing this iteration and authorized logical local commits without
another approval. Tickets 01-03, focus-rule convergence and bounded Melbourne V3
revalidation are complete. Current behavior is ordinary target 1, sourced focus target 2,
explicit quantities/exclusions/exclusive restrictions preserved, no inferred themed volume,
and independent landmark opportunities after preference saturation. V0 remains prompt-only;
V0-V3 execution paths, resource ceilings and V3 Repair permissions are preserved.
The earlier Melbourne failure remains historical; the later single-case acceptance passed
with museum 2/2, architecture 2/1, gardens 1/1 and six scheduled nominated landmarks.
UNKNOWNs, broader model reliability and explicit maximum enforcement remain bounded limits.
This is feature closeout, not a version freeze or formal evaluation. No further live runs
are planned. See [closeout](.scratch/preference-landmark-balance/closeout.md).
Final combined regression: **1808 passed / 9 skipped (77.43s)**; Ruff/diff checks passed.
An earlier run stalled in an existing cancellation-test area and was interrupted; the
16-test file and subsequent full rerun passed without retrieval changes. Local commits
`4084a2f` (implementation/tests) and `274ab27` (bounded pilot tools/tests) save this capability;
the related documentation commit completes closeout. Earlier dated status remains historical.

## Melbourne focus live revalidation - 2026-09-28

One separately authorized unchanged-input V3 attempt passed the bounded focus acceptance
in99.781s, exit0, complete captures and recorded budgets within limits. Museum focus has
exact sourced soft target2 and final coverage2; architecture2/1 and gardens1/1 are covered.
Eight resolved/qualified nominees reached supply, six appear among eight final main visits
(3/3/2 by day). No authorized Repair targets; initial equals final,11 UNKNOWNs remain.
This is limited live support for the correction, not universal quality, full feasibility,
formal comparison or freeze. No retries or commit. See [assessment](.scratch/preference-landmark-balance/pilot/focus-revalidation-assessment.md).

## Focus rule convergence - 2026-09-28

The user approved removing inferred themed travel behavior after the Melbourne failure.
Current prompt18/wire12 and domain scope expose ordinary/exclusive only. Ordinary category
interests target one, sourced current-trip focus two; explicit quantities/exclusions and
explicit category-only restrictions retain existing meaning. Whole-trip category labels
cannot bypass soft coverage, and only exclusive scope bypasses general exploration.
The targets are not maxima: independent landmark value survives saturation. V0 remains
prompt-only; V1-V3 share the grounded policies. No budgets or Repair permissions changed.
See [implementation record](.scratch/preference-landmark-balance/focus-convergence.md).
The correction is implemented; no new live run or commit. Historic themed payloads remain
evidence and are rejected by the narrowed current schema. Prior live outcomes below are
unchanged; real-model reliability after the correction is not yet established.
Final backend regression: **1807 passed / 9 skipped**; Ruff/diff and Standards/Spec reviews
passed. Next step is a separately approved bounded Melbourne V3 live verification.

## Preference and landmark V3 live checkpoint - 2026-09-28

The user authorized preparation through three sequential one-shot V3 live cases.
All completed with complete captures: Sydney 89.890s, Melbourne 118.296s, Brisbane
67.079s. Sydney retained ordinary target 1 and scheduled seven nominated landmarks
among eight visits. Brisbane kept three main visits and reported three interests as
unassessed. Melbourne failed the required focus interpretation: the explicit museum
focus became `goal/themed` with no soft target 2, and museum-related options dominated.
Therefore full feature acceptance has **not passed** despite successful execution.
All three skipped Repair with no authorized targets; UNKNOWN findings remain.
No repair, rerun, commit or freeze was performed. Recommended next scope is an offline
regression and correction of focus classification, followed by separately bounded live
verification. See [pilot assessment](.scratch/preference-landmark-balance/pilot/assessment.md)
and the [development record](docs/development_record.md) for evidence and limitations.

## Integrated preference and landmark balance - 2026-09-28

Tickets 01-03 are implemented. V1-V3 balance soft-preference candidate opportunities
with resolved landmark value through admission and final supply. Target plus one keeps
replacement opportunities; only final distinct scheduled matches count as coverage.
Explicit restrictions and facts retain authority. V0 remains prompt-only and V3 Repair
permissions are unchanged. No resource ceilings were increased or live tests run.

Task 02 was committed as `9d25633` (implementation/tests), `e795aab` (budget reporting),
and `cc4d5a0` (documentation). Task 03 changes remain uncommitted. Current design:
[shared supply](docs/shared_poi_supply.md#preference-and-landmark-balance---2026-09-28).
Final validation: **1793 backend tests passed / 9 skipped**; scoped Ruff and both reviews
passed. Details are in the [development record](docs/development_record.md).
No freeze or cross-version quality claim. Any live pilot needs a separate approved plan.

## Landmark nomination implementation - 2026-09-27

Ticket 02 is implemented: V1-V3 initial discovery adds one destination-only model
nomination, exact provider identity resolution and at most four supplementary sends
within the existing twelve candidate-search sends. User-named discovery precedes
others; general discovery retains an opportunity when budget remains. Metadata reaches
qualified supply/generation; exclusions, exclusive scope and factual checks still apply.
V0 is unchanged and V3 Repair does not repeat nomination. Ticket 03 remains pending
for combined soft-target saturation and landmark-aware candidate balance.

The approved ticket 01 commits are `a04af97`, `4e0115e` and `64dbd4b`. Ticket 02 is
uncommitted. Final backend regression: **1784 passed / 9 skipped**; scoped Ruff and
Standards/Spec review passed. Validation details and limitations are in the
[development record](docs/development_record.md#landmark-nomination-ticket-02---2026-09-27);
[current discovery behavior](docs/shared_landmark_discovery.md) owns the design.
No live run, push, formal comparison or version freeze occurred.

## Soft preference coverage implementation — 2026-09-27

The user invoked implement for ticket 01 of the accepted preference/landmark plan.
Soft target one, or two for a sourced explicit trip focus, is now separate from user
quantities. Grounded final coverage and Product feedback distinguish supported
scheduled matches, soft gaps and unassessed relations. V0 receives prompt guidance
only, with no new tools/stages or canonical coverage claim. Existing explicit
requirements, primary exceptions, V3 Repair authority and resource ceilings remain.

Final offline validation: 1750 backend tests passed / 9 skipped; 83 frontend tests passed.
TypeScript, scoped Ruff and Standards/Spec review passed. No live run, commit or freeze.

At the ticket 01 checkpoint, tickets 02 and 03 remained pending. The later ticket 02
checkpoint above supersedes that implementation status. This implementation does not establish improved live itinerary quality.
See [current requirements](docs/shared_requirements.md#soft-preference-coverage--2026-09-27)
and the [ticket](.scratch/preference-landmark-balance/issues/01-soft-preference-coverage.md).

## Iteration commit checkpoint — 2026-09-27

The user authorized direct logical commits after workspace review, without another grouping
approval. The complete final working tree passed 1727 backend tests with 9 skipped
(73.39 seconds); scoped Ruff and diff checks passed. Commit groups cover collaboration
rules, acceptance tooling, semantic correction/short references, compact budget tracing and
development documentation/audit records. Ignored logs, raw captures, credentials and thesis
archives are excluded. No new live run, push, merge or version freeze is authorized by this
checkpoint. Historical validation counts below describe their respective earlier stages.

## Independent budget summary — 2026-09-27

File tracing now writes an independent budget.json on finalization, before large run.json
serialization. It retains the final primary tool pool plus separate semantic, RAG, Repair,
Nearby and primary-generation numeric observations and configured limits. Existing reported
usage is deduplicated by call/round; cumulative counters replace snapshots rather than being
added. Unavailable requirements/main-generation billed usage remains explicitly missing.
The summary does not contain itinerary, user text, model labels or raw provider content.

The artifact has a separate 64 KiB ceiling and at most 32 call records per tracked stage;
capacity loss is marked incomplete. Writes use a pending file and atomic rename. Summary
failure does not prevent ordinary final trace writing or alter planning. Tracing must be
enabled and finalized; this change does not add a new runner cancellation/finalization path.
All API/Repair budgets and V0-V3 planning behavior remain unchanged.

TDD reproduced missing summary and write-failure coupling, then verified both fixes. Full
backend regression passed 1726 tests with 9 skipped. Spec review identified missing RAG
cancellation/resolution counters; a failing regression reproduced it, and the small fix
passed 63 focused trace/RAG/V3 tests. No live calls or commits occurred.
Both independent review axes have zero remaining findings after re-review. See
[the summary spec](.scratch/semantic-reference-correction/budget-summary-spec.md).

## Current application-owned semantic references — 2026-09-27

Subsequent authorized prompt-5 live checkpoint: Sydney V1, Sydney V3 and Melbourne V1
each ran once and returned their complete requested dates. All four semantic batches
passed on their first call. Independent capture checks verified short-reference coverage,
same-candidate source ownership, mapping hashes and exact canonical restoration. This
accepts live wire integration for these cases, not correction efficacy or general semantic
accuracy. Sydney V3 also accepted one coverage Repair; remaining UNKNOWN findings and all
38 activity costs being null prevent a fully verified travel/budget claim. V1 sparse-day
and food-preference observations remain separate follow-up items, not wire failures.

The subsequent offline V3 budget audit reconstructed the recorded call/count budgets from
212 continuous events, the final result and acquisition ledgers: 45 range checks passed,
with no recorded overrun. Primary Details were 32/60, baseline routes 4/7 plus 256/400
elements, alternative routes 16/32; RAG Details 26/30 and fallback 4/4; Repair routes 12/24
in their separate pool; semantics 2/6 calls and 27.412/120 seconds; Nearby 3/3. Primary
pre-generation route stops reflected the 16-call reserve, not 96 extra sends or an overrun.

The original run.json remains truncated (4,908,309 original bytes versus a 1,000,000-byte
limit). Full requirement/main-generation billed usage and per-call latency remain missing;
recorded-counter compliance is not a provider invoice audit. The next recommended change
was an independent compact final budget/usage artifact, rather than enlarging the aggregate
payload alone. The user subsequently approved its implementation, recorded above. See the
[offline audit](.scratch/semantic-reference-correction/v3-budget-audit.md).
Evidence: `logs/semantic_short_reference_revalidation_20260927/report.md`. No commits,
automatic retries, production changes or version freeze occurred during these live cases.

The approved short-reference follow-up uses prompt 5 and wire projection version 1.
The application assigns batch-local candidate_ref pNN and source_ref/evidence refs eNN;
the model no longer has to repeat canonical IDs or full source references in its output.
Responses may be reordered: exact mapping, complete candidate coverage and same-candidate
evidence ownership are validated before canonical restoration and full domain revalidation.
Only accepted canonical assessments enter downstream supply or cache. Exception permissions
and semantic support requirements remain strict; source expansion does not establish truth.

Mappings stay fixed during correction and isolated between batches. Opt-in captures retain
wire inputs/outputs, mapping/hash/version and canonical accepted results. Canonical mappings
are not sent in the model prompt. Cache keys include canonical inputs and projection/prompt
versions; the offline replay tool shares that key implementation. Existing canonical
downstream schemas, V0, quantity Repair policy and all budgets are unchanged. This phase
authorizes offline implementation/testing/review only, with no live execution or commits.
See [the short-reference spec](.scratch/semantic-reference-correction/short-reference-spec.md)
for validation history. At this implementation checkpoint live integration was unverified;
the subsequent limited live result is recorded above, without a reliability claim.

Final offline validation: 1721 backend tests passed, 9 skipped. The initial full run exposed
old SDK mock fields and an offline replay cache-key dependency; both were synchronized,
their 41 affected tests passed, and the full suite was rerun successfully. Standards/Spec
review, including these compatibility fixes, found no actionable issues. Scoped Ruff and
formatting checks passed. No separate static typechecker is configured for the backend.

The preceding prompt-4 live revalidation completed three one-attempt cases: Sydney V1
corrected an identity error but introduced a match-reference typo on its second call;
Sydney V3 and Melbourne V1 generated complete date ranges after first-call semantic passes.
There was no successful live correction. Complete captures and the report are under
`logs/semantic_contract_revalidation_20260927/`. This evidence motivated the short wire
contract; it does not validate the new prompt-5 implementation.

## Current semantic contract correction — 2026-09-27

The approved minimum follow-up is implemented and offline validated. Prompt 4 explicitly
requires favor plus explicit_primary_exception=true, or an exactly bound REQUIRED named
place, as well as a supported match and exception_only role for primary exceptions.
Identity-set errors and exception authorization/ownership errors now share the existing
one-per-batch correction with citation errors. There is no additional allowance per error
class, silent ID mapping, claim removal or partial invalid-batch acceptance. Full validation
still precedes cache/ledger admission. Feedback is bounded and captures link both calls.

All defaults remain unchanged: 6 calls/request, 45 seconds/call, 120 seconds total,
32000 input and 8192 output tokens. Shared V1-V3 behavior changes; V0, quantity Repair and
unrelated schema/provider-error behavior are unchanged. No live or commit occurred in this
implementation phase; real-model correction efficacy remains unverified.

TDD first reproduced terminal identity and unauthorized-food failures, then passed after
the bounded extension. Full backend regression passed 1712 tests with 9 skipped. A subsequent
test-only expansion covered absent/unresolved named matches; the final focused suite passed
72 tests, with no production changes after the full run. Independent Standards and Spec
reviews found no actionable issues. The next step is a separately approved development live
revalidation executed by the smoke tests conversation; this conversation owns its plan and
result assessment. See [the approved spec](.scratch/semantic-reference-correction/spec.md).

## Network revalidation and offline diagnosis — 2026-09-27

A subsequent explicitly network-enabled three-case run passed requirement interpretation but
all three stopped before generation: Sydney V1 claimed unauthorized primary exceptions;
Sydney V3 and Melbourne V1 returned one changed canonical ID each. No citation correction
was triggered and no budget ceiling was reached. The preceding restricted-network attempts
below are historical; the correction still lacks live efficacy evidence.

Offline public-service replay reproduced all three failures and minimized each to one row.
Sydney V1's ten restaurant exception claims all referenced a continuing food preference with
explicit authorization false; no named bindings existed. The other cases changed an ID's last
character and repeated it in citations. Current input serialization roundtrips unchanged.
Strict rejection is correct. A proposed minimal follow-up would clarify authorization and
extend the existing one-per-batch correction to these contract errors, without weakening
validation or adding a new allowance. It was not implemented or approved at that diagnosis
checkpoint; the subsequent approved implementation is recorded above.
See [the diagnostic report](.scratch/semantic-reference-correction/non-reference-diagnosis.md)
and `logs/semantic_reference_network_revalidation_20260927/report.md` (local ignored evidence).
No production code or live calls were made during diagnosis; no commit or freeze occurred.

## Semantic correction live revalidation blocked — 2026-09-27

The three separately approved one-attempt runs (Sydney V1, Sydney V3, Melbourne V1)
all stopped in requirement-provider transport, before travel tools, RAG, generation or
POI semantics. Recorded semantic calls and travel-tool counters were zero. No itinerary
was returned. The provider diagnostics contain no HTTP status or usage, so the cause,
provider receipt and cost remain unknown. Execution-history review confirmed all three
launches used the default restricted sandbox, with no escalated network execution. This
is a preparation gap and a possible cause, not proof of the transport root cause. This neither validates nor refutes semantic correction. No retry is authorized.
See `logs/semantic_reference_revalidation_20260927/report.md` (ignored local evidence).
The following offline checkpoint remains valid; its no-live statement describes the
implementation checkpoint before these separately authorized attempts.

## Current semantic reference correction — 2026-09-27

Approved shared V1-V3 follow-up: invalid or missing evidence citations now receive at most
one corrective model assessment of the same batch with bounded diagnostic feedback.
Prompt 3 retains strict identity, citation and exception validation before caching. Both
attempts consume the existing 6-call/120-second semantic allowance and 45-second per-call
limit; correction input includes feedback in token accounting. Failed or unavailable
correction remains terminal. Ordinary candidate rejection, non-reference errors, V0 and
quantity Repair behavior are unchanged. Opt-in captures link both calls and pre-send stops.

Offline validation: full backend suite passed 1689 tests with 9 skipped. Two subsequent
SDK/deadline test additions and isolated boundary assertions passed the final targeted
suite (53 tests); production implementation was unchanged after the full run. Standards
and Spec review have no remaining findings. This is uncommitted work based on
`339e7e4a4a9eac133f2bdff69217b8b35c6990b4`; no live calls or version freeze occurred.
The Sydney/Melbourne development smoke motivated this change but does not validate it live.
See [the correction spec](.scratch/semantic-reference-correction/spec.md) and
[semantic design history](docs/shared_poi_semantics_plan.md).

## Current planning input UX — 2026-09-26

The shared Product/Dev form now offers GeoDB destination suggestions, a currency selector,
locale-independent dates and compact weather presentation. Selecting a city submits its
city/region/country label as the destination string; manual input remains possible. The
public free GeoDB endpoint is called through FastAPI over HTTPS. An approved two-request
check observed HTTP 308 to the same-host HTTPS endpoint, then HTTPS 200 with five places;
the captured payload normalized offline. This is point-in-time provider evidence, not an
availability guarantee. No RapidAPI account or key is used.

Preference polishing now uses one bounded model call per admitted operation. A schema-valid
rewrite is displayed for the user's Apply/Dismiss decision and can be undone; the original
remains available. The prompt requests meaning preservation, while the user reviews the
candidate and normal planning still executes its Gate. The earlier independent model review
and local numeric/date/currency suppression were removed by explicit user instruction.
Each operation owns its model HTTP clients, so a completed or failed request cannot close a
cached connection used by the next request. The model status schema accepts only supported
outcomes. Configuration, API errors, admission limits and budgets are documented in the
[input UX specification](.scratch/planning-input-ux/spec.md) and [config reference](config/README.md).

The final single-call implementation passed 1678 backend tests with 9 skipped, 82 frontend
tests, targeted Ruff and Standards/Spec review. Earlier bounded live Polish runs with
mountain-climbing and reading-books inputs passed when the two-call review still existed;
one input also included animals. These runs do not validate the final single-call behavior
live or establish improved Gate acceptance. The local backend was restarted and
direct/proxied health endpoints returned 200. The implementation and prior closeout documents
were saved in local commits `79ca61a`, `c8b9aa8` and `648d951` on `feature/v3`; no push or
new version freeze occurred.

## Current iteration closeout — 2026-09-26

Status: CLOSED by explicit user confirmation. Implementation, bounded development acceptance,
offline browser integration and five local commits are complete. Final implementation/documentation
checkpoint: `40b0b26` on `feature/v3`. The worktree was clean after those commits; this subsequent
closure-status documentation update is separate and is not automatically committed.

The POI semantics / quantity-reuse iteration is implemented with offline and bounded live
evidence. The [iteration closeout](docs/poi_semantics_closeout.md) is the current summary;
the dated checkpoints below retain their historical status. Latest backend validation:
1648 passed / 9 skipped. Commit-group validation additionally passed 1608 backend tests /
9 skipped, then 40 new-tooling tests. Frontend validation was repeated before committing:
59 passed; TypeScript/Vite build passed.
The subsequent Product API follow-up preserves policy completion/reasons in both JSON and
SSE responses; incomplete results remain visible without the misleading ready message.
Offline routing checks confirm the Product frontend uses current V3. This is source/test
verification, not a running deployment or new live acceptance.
Subsequent approved policy update: V3 quantity review now defaults on for Product and Dev.
The obsolete repetition-review switch/report entry has been removed; unauthorized-repeat
repair remains automatic. Overfull review stays off; budgets and permissions are unchanged.
Existing backend processes must restart to reload cached configuration. Earlier dated
default-off statements below describe historical checkpoints, not current configuration.
The final quantity-enabled D pilot used two Repair calls, changed15 visits to18, resolved
its three dynamically identified gaps, and preserved all original activities and budgets.

The user explicitly declined further Penguin Beach / London Zoo work. Their exhibit/parent
relationship is not an established defect or an open task. P3 remains deferred; factual
UNKNOWNs and bounded model-reliability evidence remain. Production quantity review stays
enabled following the separate policy approval. No new freeze, formal evaluation, live run
or Git action is authorized by closeout.
Offline browser integration subsequently passed using synthetic external ports: Product
quantity repair and incomplete-state presentation, plus Dev's four independent version runs.
Both V3 paths report quantity review enabled and omit the obsolete repetition flag. Temporary
servers were stopped. All five reviewed groups were committed; see the
[executed commit record](.scratch/iteration-closeout/commit-plan.md). Nothing was pushed.
This closes the iteration, not a new version freeze. No further implementation, live run,
research evaluation or Git action is implied; the next stage requires a new user instruction.

## Current POI semantics extension — 2026-09-26

The accepted [POI semantics extension](docs/shared_poi_semantics_plan.md#12-implementation-checkpoint--2026-09-26) is implemented with offline evidence. Shared one-pass goal/multiplicity interpretation and request-owned candidate semantic assessment now protect main-role qualification, scoped exceptions and exploration opportunities. V3 adds default unauthorized-repeat repair and unpublished grouped compensation. Product output distinguishes incomplete adopted itineraries. New semantic-model limits are separate from unchanged travel/primary/Repair limits. This post-closeout work now has bounded A/B live observations described below; historical closeout and smoke records do not validate the extension.

The approved [Spec review fixes](docs/shared_poi_semantics_plan.md#13-approved-spec-review-fixes-2026-09-26) unify canonical visit counting, enforce explicit category cardinality/date targets, propagate named visit obligations into completion, and prioritize explicit category counts in supply selection. Existing capacity and version boundaries remain. After the approved target-priority fixture correction, full offline validation passed: 1591 passed, 9 skipped, zero failures. The old fixture was aligned with confirmed-repeat priority while preserving every original adopted-loss isolation assertion; production logic was unchanged. The P3 pending-reason heuristic remains deferred.

Latest network-enabled acceptance (2026-09-26): A completed with eight distinct main POIs and complete policy status; B satisfied exact two museums on different dates and minimum two parks. Duplicate/count Repair branches were not triggered. C received HTTP 200 but stopped at `unsupported_hard_requirements` for `semantic_1`; the batch stopped without retry, and the user's eight-day London mountain/zoo/rich-trip case D remains unexecuted. This is partial live evidence, not a completed acceptance or freeze. See [the bounded acceptance record](docs/shared_poi_semantics_plan.md#15-network-enabled-bounded-acceptance-2026-09-26).

Named-visit routing follow-up (2026-09-26): `preference_prompt_15` makes executable named counts/dates authoritative in VisitRequirement while preserving independent hard conditions. A new opt-in one-case acceptance entry retains failed interpretation evidence without retries or gate changes. This follow-up passed the full offline backend suite (1602 passed, 9 skipped, zero failures). A separately authorized captured C retest passed once in 131.094 seconds: exact-two British Museum visits on October 5 and 6, no duplicate hard semantic requirement, complete Product status, no Repair, and complete normalized capture. This is limited live evidence, not a stability guarantee; D remains unexecuted. See [the implementation record](docs/shared_poi_semantics_plan.md#16-named-visit-prompt-routing-and-acceptance-capture-2026-09-26) and the subsequent captured retest record.

D captured acceptance (2026-09-26): after separate authorization, D ran once and stopped after 12.0 seconds at `preference_input_blocked`. The HTTP-200 prompt-15 draft classified `I also want to enjoy a rich trip` as a clarification-required semantic ambiguity. Complete normalized draft/rejection evidence was saved; recorded travel-tool usage is zero, with no itinerary or Product output. No retry was performed. D's mountain/zoo/diversity behavior remains unvalidated; the next proposed step is offline diagnosis of this input classification. See section 18 of `docs/shared_poi_semantics_plan.md` and `artifacts/poi_semantics_acceptance/20260926_D_captured/report.md`. Earlier unexecuted-D statements describe the preceding checkpoints.

Soft-quality boundary follow-up (2026-09-26): approved prompt 16 now distinguishes ordinary rich/varied/enjoyable/memorable trip wishes from missing decisive mandatory meaning. It preserves sourced soft semantics without invented counts, themes or luxury spending, while independent genuine input issues still block. Shared V0-V3 instructions and prompt metadata changed; gate, schema, budgets, supply and Repair did not. Nine new controlled SDK/instruction checks pass, and the full offline backend suite passed 1611 tests with 9 skipped. Standards and Spec review found no issues. The historical D fixture still reproduces the block by design; real-model compliance remains unvalidated until a separately approved captured D retest. No live run or commit occurred in this follow-up. See section 19 of `docs/shared_poi_semantics_plan.md`.

Captured prompt-16 D retest (2026-09-26): one separately authorized run passed input interpretation with all three sourced preferences and VALID/CLEAR, then failed after 95.312 seconds with `SemanticAssessmentError: Invalid match evidence references` in the first POI semantic call. No itinerary or Product was generated. Requirement capture is complete; raw downstream semantic output was not captured. This provides limited live evidence for the input correction, while mountain/zoo/diversity/repeat acceptance remains blocked. No retry or production edit occurred. See section 20 of `docs/shared_poi_semantics_plan.md`.

Semantic reference follow-up (2026-09-26): approved `poi_semantics_prompt_2` now specifies exact same-candidate citations. Strict reference rejection remains; errors add bounded offending/allowed reference details. The development acceptance entry adds default-off `--capture-semantics` for correlated normalized input, pre-membership output and outcome, with redaction and enforced 1 MiB/artifact, 4 MiB/case limits including partial-write failures. Shared V1-V3 semantic paths carry prompt fingerprints/cache identity; V0 remains tool-free and requirement prompt 16 is unchanged. After a review-found partial-write cap fix and a test-only exclusion of random call IDs, the final backend suite passed **1625 tests, 9 skipped, zero failures**; Standards and Spec reviews have no remaining findings. No live run or commit occurred. D still requires separate authorization for a retest with both capture flags. See section 21 of `docs/shared_poi_semantics_plan.md`.

Dual-capture D retest (2026-09-26): one authorized run completed in 133.797 seconds with both captures complete. Input interpretation and both semantic batches passed; 14 distinct main POIs have no cross-day repeats, the one-off zoo goal is satisfied, and two indoor climbing alternatives are explicitly distinguished from mountain climbing. Actual mountain climbing remains unfulfilled. Daily counts are 3/3/2/1/2/1/1/1: four days remain below the quantity target (NEEDS_REVIEW), while all meet minimum coverage. Product complete does not imply richness; unchanged quantity review is disabled, so no Repair was authorized. This is bounded improvement with remaining quality limitations, not full rich-trip acceptance or a benchmark. See section 22 of `docs/shared_poi_semantics_plan.md`.

Acceptance and sparse-day diagnosis (2026-09-26): the user accepted this semantic extension and D run; this is not a version freeze. Subsequent offline diagnosis found 16/16 selected supply from 37 eligible candidates, 14 used identities, and an unchanged initial/final itinerary. The two unused choices are animal venues, one about 26.9 km from the destination anchor; insertion feasibility is not established. Four sparse dates are NEEDS_REVIEW rather than missing minimum coverage. Quantity review is disabled, so no Repair ran; round/time exhaustion is not the cause. Pure validator replay with coverage review enabled creates four targets but does not prove repairs feasible. Production defaults and budgets remain unchanged. See the D artifact's `diagnosis/report.md` for evidence and limitations.

Offline sparse-day scope inspection (2026-09-26): actual scope/window/candidate preparation over saved original supply authorizes additions on the four sparse dates only, with no existing-activity move/retime/delete/replace or revisit permissions. Penguin Beach is the sole preliminary new identity, associated with October 4 and 7; the other dates and Eagle Heights fail geographic screening. Saved WALK routes for the two surviving associations exceed policy limits and no matching motor-route facts were retained, so insertion remains unverified. This replay excludes the full comparison pool and performs no acquisition/model/adoption. Enabling review or increasing rounds alone is not proof of four-day completion. See the D artifact's `diagnosis/repair_scope_report.md`; production defaults and the prior acceptance remain unchanged.

## Final engineering checkpoint — 2026-09-25

Current closeout status: **V3 ENGINEERING CLOSED — FINAL ENGINEERING CHECKPOINT RECORDED**. The [closeout record](docs/v3_closeout.md) supersedes
earlier current-state claims below; dated checkpoints remain historical. Shared mixed transport,
five-round Repair, minimum coverage, same-round component partial adoption and two final TRANSIT
legs have artifact-confirmed bounded live observations. Prompt13 budget scope and the latest
content-filter UI mapping remain offline-only. Benchmark Frozen: NO; Formal Evaluation: NOT STARTED.


Current source of truth. Updated 2026-09-25.

Frontend migration checkpoint: Product API now selects V3 through the request-owned application
runtime and projects an allowlisted final presentation contract. Product-only introductions are
optional and bounded by the remaining request deadline; Developer V0-V3 retains research output
without introduction calls. React now consumes streaming progress and Product presentation fields;
the `/dev` workbench runs four independent versions from one structured snapshot. Offline validation
is recorded separately from bounded real-provider acceptance: Product completion, Developer four-way
completion and cancellation isolation passed after the approved HTTP-client ownership fix.
This does not cover every repair/retrieval branch or establish itinerary quality.
See docs/frontend_design.md for implementation boundaries and validation status.

## Purpose and implemented scope

An LLM-Based Travel Planning System for Feasible and Reliable Itinerary Generation studies a
sequence of independently runnable mechanisms: V0 plain LLM, V1 external information/tools,
V2 RAG discovery, and V3 validation/targeted repair/re-validation. All four runners exist;
V3 has offline-tested structured findings, a read-only validator, bounded feedback-driven repair,
request resource assembly and final-primary Nearby wiring. The A/B/C checkpoints additionally
cover elastic time/real adjacency, conditional coverage and adjacent moves, and evidence-scoped
operating/transfer repair; these changes are implemented + offline-validated only. See the latest
checkpoint in docs/v3_development.md for supported evidence and limitations. Historical development
live records remain separate and do not validate these later corrections retroactively.
Google API evidence adoption has bounded live evidence from run
29b2a5f7-c6fa-45b8-9eba-31b9e89e3ea4: ten final opening checks and five WALK transfers passed;
one quantity addition was accepted, followed by two empty patches. This did not exercise C conflict
repair or establish overall trip quality. The subsequent material-feedback correction has offline validation and bounded first-round
live evidence from 4b0b018e-92ae-4563-a401-83f303d8c9cb (two additions, complete in one round): no-op/no-progress reconsiders target opportunities, rotates presentations,
and skips semantically unchanged model input. It preserves the latest adopted draft and all limits.
The separately saved ABC run 759ee785-05c6-44e6-9ef7-9a812a6e21bb retains its original evidence.
See the final v3_design checkpoint for supported boundaries, test chronology and sizing.
Current responsibility is engineering design, implementation and development
validation, not formal benchmark comparison, thesis writing or final research conclusions.

## Current accepted foundation

planning_request_2 requires destination, supported dates, traveler count, whole-trip budget and
currency. additional_preferences is optional. One shared interpreter handles nonempty preferences;
empty preferences skip interpretation. Application-owned canonical requirements retain subject and
source provenance. Current interpreted contract is interpreted_requirements_3. Unsupported HARD
semantics and unresolved REQUIRED identity retain clarification boundaries.

V1/V2 use deterministic admission/acquisition and planning-candidate supply, selective Reviews to
ExperienceProfile, REQUIRED/OPTIONAL projection, current external evidence and primary generation.
Retired B1/B2 evaluators and minimum-subset implementations have been removed. Shared
candidate acquisition is independent of historical experiment frameworks.

V2 adds bounded TripWorld query embedding, geographic exact retrieval, Google-backed resolution
and canonical source merge before common admission. Existing ENRICHED 1536-dimensional OpenAI
vectors and PostgreSQL/pgvector remain the retrieval foundation. No ANN, shadow table or vector
rebuild has replaced it. Post-primary Nearby uses actual scheduled anchors and appends optional
references; it does not modify primary activities or recover unused supply automatically.

The shared final contract is itinerary_2. V0's references remain unverified model knowledge without
travel tools; V1/V2 use application-owned Nearby evidence and a primary-only generation DTO.
References do not satisfy REQUIRED, count as scheduled visits or enter planned costs.

## Configuration, acceptance and limits

V2 current implementation checkpoint accepted. Core RAG and shared downstream wiring have
bounded Tokyo and Sydney end-to-end evidence. Primary V2 implementation/smoke work is complete;
formal-evaluation preparation and Git checkpoint planning are next, subject to separate approval.
This records experimental mechanism boundaries, not a permanent source freeze. Later shared
correctness fixes must apply to all dependent versions and trigger checkpoint/impact review.

Phase 6, post-itinerary Nearby and explicit quality_first_1 are implemented + bounded
development-live-validated. This is neither production-ready nor all-branch/formal benchmark
acceptance, and does not automatically re-freeze V1/V2. Original freezes retain their original
contract/configuration scope; later authorized changes are separate checkpoints.

The user approved quality_first_1 as the default V1/V2 runtime policy. config/runtime.yaml is now
the sole configuration file in config/, byte-identical to the previously accepted quality YAML.
The old dedicated quality YAML and historical60/180 JSON were removed, along with the unused
RevisedV1PlanningResult B2 output contract. Retired evaluator experiments and their exclusive configuration/tests have now been removed.
The 600-second whole-request ceiling requires an explicit development argument, not merely the YAML.
Longer SQL waiting allowed functional validation, not completion of storage/performance optimization.

Latest joint evidence supports normal V2 retrieval/resolution and shared two-pass Details/supply.
It does not establish RAG superiority, universal preference satisfaction or complete tool coverage.
Tokyo Weather coverage limitations (Sydney ten-day acquisition succeeded), Web accepted-fact/usage gaps, exact SQL variation, unknown costs, visitor suitability
and duplicate experiences remain open. Melbourne named-identity ambiguity remains a separate
conservative clarification limitation. The later frontend migration checkpoint above supersedes
the former V0-only API boundary; Product selects V3 and Developer exposes V0-V3.

## Current work and next approval

Repository responsibility cleanup is implemented and offline-validated. CandidateAcquisition now
owns shared acquisition; PlanningCandidateSupplyPipeline invokes it without inheriting any retired
selector framework. Semantic Evaluator, subset-selection implementation, exclusive DTO/configuration,
measurement scripts and algorithm-only tests were removed. Current assertions were migrated.

Planner scripts remain in scripts/. Offline data preparation is under tools/data; acceptance under
tools/validation; current retrieval/candidate/payload diagnostics under tools/diagnostics. Runtime
must not import those tools or tests. Contracts, prompts, active budgets, SQL, data/vectors and
V0/V1/V2 behavior remain unchanged. Contract/policy/space version naming was deliberately excluded.

Focused first execution: 593 passed, 9 skipped, 19 failed. The failures were one migrated Review
service test hook and the moved acceptance module's self-hash path. Affected modules then passed
62 tests; final dependency/tool/fixture checks passed 34 tests. The one complete backend run passed
834 tests with 9 existing optional database skips. No live/API/DB execution occurred.

Source/document/config recovery snapshots were permanently deleted, including the external
phase6_source_snapshots directory. Real run logs remain; selected offline results moved to artifacts;
tokenizer cache moved to .cache. Inaccessible capture directories were retained and enumerated.
Logging console behavior, payload defaults, redaction and usage semantics were not changed.

The cleanup task itself did not stage or commit. The subsequently approved seven-commit
responsibility-based checkpoint now saves the intended source, tests, configuration and documentation.
No push, re-freeze or V3 work is included. Historical experimental methods,
results and limitations remain in documentation; deleted implementations are not replay entry points.


## Latest bounded evidence and next-step boundaries

The later completed cleanup regression collected 848: 839 passed, 9 skipped, zero failed, exit 0.
The earlier 834-pass run above is a different checkpoint. Tokyo and Sydney cleanup smoke then
completed V0/V1/V2. Sydney used ten days, C64/G32/send40/K16/P8 and exercised Weather, 256 baseline
route elements, Reviews/Profile and V2 normal RAG. Later shared stable activity sorting passed
78 focused tests offline; Sydney raw evidence remains unchanged. No new tests or live calls were
performed during this acceptance/documentation task.

Empty days, repeated experiences, hours/route conflicts and evidence-based budget validation
motivate future V3 validation/targeted repair/re-validation. Missing prices, official domains or
public visitor-access evidence remain unknown; V3 cannot manufacture them. SQL variability remains
retrieval engineering work, not a V3 capability. Sydney's two no-domain Web tasks had no website
in supplied evidence; no propagation defect was established for those tasks.

The 2026-09-22 shared Weather/date extension replaces Google Weather with Open-Meteo daily
forecasts and admits today through today+13 inclusive, independently capped at 10 travel days.
It is implemented and offline-validated; the isolated provider probe succeeded with a null final
date, while integrated planner live validation is still pending. Earlier acceptance used the old
Google Weather/date checkpoint. Same-day remaining-hour planning is still unsupported.
Exact historical vectors require retained local artifacts; a clean clone is not an exact DB backup.

## Authorized first-generation baseline extension (2026-09-20)

Shared generation now targets the entire requested date range and normally 2-5 distinct
main POIs per normal full day, subject to explicit pace/rest, long REQUIRED visits and
evidence limits. New model output declares activity roles; historical missing roles are
unknown. Read-only daily diagnostics distinguish default misses from execution failure.
No refill, second generation or repair is implemented. V0 uses name proxies; V1/V2 use
validated canonical supply IDs. Nearby cannot inflate counts.

Nine/ten-day supply supports 18/20 places with C64/G32/send40/P8 unchanged. Baseline
Routes supports 400 directed elements/seven requests, 64 per request; alternatives remain
unchanged. The primary input/output limits remain 160000/16384. PostgreSQL connection
establishment tolerance is 10 seconds; SQL60/RAG360 and the explicit development600
boundary remain unchanged. This is not a SQL performance fix or new live acceptance.

V3 is documented as explicit post-generation feasibility validation, structured findings,
targeted repair and re-validation. Its Step 1 findings schema and partial read-only validator
are now implemented, along with the subsequent single-round repair service and independent
graph/runner wiring. See the later Step 3 checkpoint for the offline integration boundary.
Shared baseline fixes are not V3 contributions. Future evaluation must use
matched shared checkpoints; historical Tokyo, Sydney and London captures are unchanged.

## Shared Weather/date checkpoint (2026-09-22)

Open-Meteo serves V1/V2 through the shared factory; V0 remains tool-free. Exact requested dates,
metric daily aggregates, destination time zone, attribution and missing dates are retained in
weather evidence. Unknown values are never filled with sunny/zero defaults. Google Places/Routes,
quality_first_1 capacities, K20, activity roles, generation diagnostics, SQL60/RAG360/connect10,
model limits and product V0 default are unchanged. The frontend obtains authoritative calendar
bounds from GET /api/planning/date-window instead of its browser-local date; product/developer
input gaps unrelated to dates remain. The latest London V2 smoke completed in75.86s with daily
main counts1/1/2/3/2/1/1, no empty dates,10 distinct scheduled places and3 Nearby references.
This does not establish universal date coverage or resolve the default-target misses/repetition.

Offline full backend:899 collected,890 passed,9 skipped,0 failed,31.60s,exit0. Frontend corrected
suite24 passed; lint/build and Ruff passed. First focused and frontend failures remain in the
shared development record. The subsequent14-date adjustment passed96 focused backend tests and
24 frontend tests without repeating that full suite. The product window is today..today+13
inclusive; each trip remains at most10 days. This conservative choice followed a null farthest
date in the prior London probe; it is not a claim about the API maximum or universal coverage.

The Tokyo Sep26-Oct5 smoke returned V0/V1 itineraries. Initial V2 completed with Google-only
degradation because the development capture factory had the wrong signature, before any database
connection. A separately user-authorized V2 rerun corrected only that invocation and completed
normal embedding, two SQL queries, resolution and RAG adoption. V1/V2 each had all50 requested
weather values and exact evidence projection; no extra weather probe was executed. Default daily
targets were met on9/7/9 days in V0/V1/final V2, with zero empty days; V1/V2 had3/6 repeated visits.
Unknown costs, visitor access and scheduling quality remain unresolved. Nearby preserved the main
itinerary and diagnostics. These are bounded development observations, not formal evaluation or
re-freeze. No V3 runtime or database reproduction work has begun; export/restore remain deferred.

Weather/date closeout review classified both Profile ValueErrors as correctly rejected model
outputs: one supplied review but review_count_used=0, with no summary or signals. Raw responses
and mapped drafts agree; no shared code fix or new test run was needed. The unavailable fallback
retained the actual input count and invented no experience evidence. The user reports the database
was initially stopped; that context does not change the recorded pre-connection factory error.
No confirmed correctness blocker was found in this narrow review. The shared migration may close
with bounded development-live evidence; current work is Git grouping approval, not another live
or V3 implementation. Generation target counts are not itinerary-quality acceptance rates.

## V3 Step 1 offline checkpoint (2026-09-22)

The subsequent explicitly authorized task implements only `v3_validation_1` findings,
separate observations/improvement targets, and `versions/v3/validation.py::validate_draft`.
Shared schema/source/date checks remain preconditions. Cross-activity overlap and resolved
named REQUIRED/EXCLUDED conflicts can be confirmed. Default counts and repeated identities
are review findings; visitor access, route feasibility and verified total costs remain UNKNOWN.
Date-specific effective opening mismatches are reviewable, not confirmed visit prohibitions,
because the current Activity contract does not bind indoor/exterior visit mode.

The focused offline regression passed 154 tests, including 55 new V3 cases and relevant
shared/V0/V1/V2 checks. Ruff passed. No external services, database acquisition or live run.
The existing primary serializer/offline tokenizer measured synthetic inputs at 43,337,
106,130 and 131,988 tokens; this does not validate a future Repair payload. Full execution
ceilings, acceptance rules, ledger accounting and sizing limits are in `docs/v3_development.md`.

No graph, runner, Repair LLM or candidate/route acquisition is connected. Initial generation
prompts, K, budgets, Weather, SQL and V0/V1/V2 execution paths are unchanged. Step 1 completion
is not V3 milestone completion or a freeze. Next repair integration requires user approval.
The earlier Weather/date pending and Git-grouping paragraphs are historical checkpoints;
the accepted shared state is implemented + bounded development-live-validated, as recorded
in the later Weather/date closeout and the three committed shared-checkpoint changes.

## V3 Step 2 standalone checkpoint

The separately approved repair service is implemented with injected collaborators only.
It provides explicit operation/duration permissions, qualified candidate preparation,
original/repair/final identity ledgers, one strict Repair model call, bounded real input
serialization, directional transition evidence, atomic acceptance and reuse of the same
validator. Partial improvement remains distinct from resolved targets; initial observations,
augmented-evidence reassessment and proposed findings are separately preserved.

Acquisition limits are repair-local; optional failures/exhaustion do not prevent feasible
retiming with retained material. Stage/request deadlines, cancellation and zero retries are
enforced. No primary prompt/K/shared acquisition budget, Weather or SQL behavior changed.
New WALK temporal evidence, visitor/indoor-access semantics and verified total costs remain
unsupported/UNKNOWN. Complex inputs can legitimately exceed 64k and skip repair.

Affected offline regression:165 passed after a Windows event-loop guard-test correction;
subsequent V3-specific tests:104 passed. Actual Repair sizing:3,688 and10,817 tokens fit;
118,145 and76,705-token synthetic cases were rejected. The50-edit output example is2,956
tokens, not a model completion guarantee. Full chronological results/limits are in
`docs/v3_development.md`; primary sizing is not relabeled as Repair sizing.

No V3 graph, runner, runtime lifecycle or final Nearby chain is connected, and no live was
run. Those integration steps and a later live run need separate authorization. This is not
a complete V3 milestone, formal evaluation, production acceptance or version freeze.


## V3 Step 3 offline wiring checkpoint

The separately authorized integration now provides scripts/run_v3.py, its own graph/state,
request-scoped assembly and final-primary Nearby execution. It reuses the tools graph through
a default-off post-primary hook, after initial source/date checks and before Nearby. No
primary interpretation, discovery or generation repeats. Original supply/draft/reports remain
separate from repair whitelist, adopted output and final reports/cost associations.

Quantity review defaults off and is recorded per run. Automatic permissions cover overlap
retiming with preserved duration, resolved REQUIRED additions and explicit EXCLUDED removal
with loss records; repetitions/opening doubts do not authorize deletion. Existing partial
validation and bounded Repair service are reused without new visitor/cost/WALK capabilities.

V3 requires an explicit whole-request allowance from entry, including dependency preparation.
Repair/Nearby share that deadline with independent stage budgets. Request cache/failure state
and one lazily prepared RAG runtime persist across stages; owned resources close on every exit,
borrowed resources stay caller-owned. Repeated embedding client reuse and common CLI-owned SDK
cleanup are shared correctness changes, not V3 contributions. V0/V1/V2 behavior and product V0
default remain covered by affected offline regressions; primary prompts/K/budgets are unchanged.

Affected regression passed290; subsequent targeted ownership/policy/CLI regression passed18.
New TRANSIT integration cases passed2 after correcting a fixture field. The full chronological
record, previous test failures and unchanged actual Repair sizing remain in docs/v3_development.md.
The final new wiring/lifecycle/policy suite passed43; changed-code Ruff and diff checks passed.
V3 wiring is offline-validated only: no V3 live, database startup, SQL/vector changes, formal
evaluation, freeze or full version-level acceptance. Live requires separate user authorization.


## V3 target-addition candidate revision (2026-09-22)

The authorized local revision separates protected itinerary context, target/date operation
candidates and the application identity ledger. It retains the 28-ID input union, bounded
old-candidate reuse/new discovery, at most two round-wide exploration opportunities, one Repair
call and existing deadlines. Uncertainty is not ineligibility. Additions require actual input
membership and target authorization; original supply statistics remain independent of ledger
growth. Parsed patches, proposals and structured rejection comparisons are auditable with
redaction and visible size limits. Chronological offline tests and actual Repair sizing are in
`docs/v3_development.md`; this revision has no live evidence. Historical three-day no-Repair and
seven-day rejected-Repair observations are retained, not rerun or reinterpreted as successful
repair. Shared primary generation, budgets, Weather, SQL and earlier versions remain unchanged.


## V3 bounded multi-round/spatial configuration checkpoint (2026-09-22)

The authorized extension now uses up to three feedback-conditioned rounds with one shared
300-second Repair stage and unchanged stage acquisition totals. Runtime YAML owns all adjustable
Repair timing/input/acquisition/spatial policies; config/README.md documents every current YAML
path. The 28-ID per-call union, target authorization, independent identity ledger, fair comparison
and prior audit contracts remain. UNKNOWN candidates can be arranged without relabeling facts.
Spatial checks distinguish time-applicable Routes, untimed WALK layout measurements and the
short-distance conservative reserve. Added daily transport burden is cumulative against the
stage-original draft. Later failures preserve prior accepted improvements; Nearby runs once.

Affected offline regression passed 249 tests; subsequent scoped fixes/checks passed 35, 5, 3 and 103.
Actual Repair serializer stress cases remain rejected at the unchanged 64k ceiling. Full test
chronology, exact sizing, limits and unsupported capabilities are in docs/v3_development.md. No live,
benchmark, vector/SQL/Weather/primary-budget change, commit or freeze accompanies this checkpoint.
Historical three-day/seven-day observations and preexisting work remain; the full seven-day
rejection cause is not claimed resolved. Further live work needs separate authorization.

## Capacity calibration freeze candidate (2026-09-25)

Repair stage limits are Google total 5 (ordinary <=4, reserved fallback <=1),
canonical attempts 12, Details sends 10, Routes 6 requests/32 elements, per-call
identity union 32 and engineering input 72000. Output remains 16384; rounds,
time, primary supply and spatial/evidence acceptance policies are unchanged.
This is resource calibration, not a new V3 mechanism or a formal freeze. Google
and canonical headroom address observed exhaustion; input/Routes headroom is
preventive. The latest Tokyo live used only 19 identities and 26454 engineering
tokens and did not exercise no-op recovery across real model calls. See the
capacity checkpoint in docs/v3_development.md for validation and the separately
authorized Honolulu smoke. Further expansion requires explicit authorization.

The authorized Honolulu smoke was prepared but blocked by automatic approval
review before process creation (including a second submission citing explicit
attachment authorization). Zero live runs/services were started. Capacity
calibration remains offline-validated; no Honolulu outcome is claimed.

After explicit chat confirmation, the one Honolulu capacity smoke ran (a84b4286-
8e9b-4665-a9fd-14e7179e29bc), exit 0. Repair safely skipped before model dispatch
at 154653/72000 input tokens and retained its draft with two route conflicts.
Dateless route targets expanded candidate preparation across unrelated add dates;
per-operation opportunity counting also mixed add/replace edges. These require
an explicit follow-up decision before engineering closeout, not automatic budget
expansion. No fix or rerun was performed. See the capacity checkpoint for evidence.

### Explicit Details allowance update (2026-09-25)

Following separate user authorization, ordinary primary Details is now 60,
initial RAG Details 30, and Repair stage Details 30. YAML remains authoritative.
The quality_first_1 adapter now uses the configured primary send allowance
instead of r_pool + 8; its new-success goal remains unchanged (32 for seven/nine
days). This shared change applies to V1/V2/V3, not V0. RAG resolution remains
16 entities; Repair canonical attempts remain 12, so neither larger send budget
is a promise to acquire 30 distinct candidates. All time, input, review, search,
route and acceptance limits remain unchanged. Honolulu used the previous limits;
no live was executed for this update. Offline sequence: 135 related tests passed,
then a new real policy-adapter configuration test and its existing companion
passed 2/2; Ruff passed. No prior failure or test retry occurred. This update
does not fix the documented target-scope or payload-overflow issues.


### Active-target locality and capacity follow-up (2026-09-25)

Implemented and offline-validated only. Current-round scope now intersects active
finding dependencies, original permissions and the existing application operation
policy. Dateless route findings resolve through activity IDs; unresolved locality
never falls back to all addition dates. Deferred reviews retain their report and
future eligibility but no current candidate acquisition permission. Conditional
compensation remains local to active parents/children. Opportunity audit separates
ADD/REPLACE associations from unique identities and one global matching capacity.
RETIME/MOVE/DELETE do not independently request new candidate identities.

Capacity calibration is separate from the correctness fix: Repair now permits up
to four rounds/calls and 120000 input tokens, with all stage time, acquisition,
identity, output, spatial and evidence policies unchanged. Details remains the
previously authorized 60/30/30; resolver/canonical ceilings can stop well before
30 sends. The Honolulu saved-material reconstruction is 78511 tokens versus the
historical 154653, but only six historical selected routes were retained, so the
entire delta is not attributable to locality. A same-retained-evidence scope-only
ablation removes 50604 tokens. See the locality checkpoint in docs/v3_development.md
for full limits, test sequence and sizing. No new live or freeze is claimed.


### Authorized processing and stage-time alignment (2026-09-25)

The follow-up configuration is implemented and offline-validated: initial RAG
resolution_entities 16 -> 30, Repair canonical attempts 12 -> 30, and Repair stage
300 -> 360 seconds. YAML and typed upper-bound validation agree. Initial RAG
changes apply to V2/V3; Repair changes apply only to V3. This is capacity alignment,
not a new research mechanism or live validation.

Preparation stays 30 seconds, rounds/calls 4/4, model cap 70 seconds, explicit whole
request 600 seconds, Routes 6/32, Google 5, both RAG/Repair Details 30, identity
union 32 and input 120000. All other policies are unchanged. Four rounds share one
360-second maximum stage and acquisition state; the entry request deadline and
Nearby reservation may shorten it. First allocation with a full stage is 90
seconds; preparation reduces the model allowance below its 70-second maximum.
The old 16/12 processing caps no longer prevent reaching the 30-send allowance,
but fallback, cache reuse, input capacity, sufficiency and time can still stop work
earlier. No quota is a requirement to spend or a promise of successful candidates.

Validation sequence: 98 tests passed first (initial RAG, runtime config, Repair
capacity and multiround); targeted locality/material-feedback/graph regression
then passed 53 tests. Ruff passed. No runtime service was called. Prompt, DTO and
serializer were unchanged, so no repeated sizing was necessary. Historical live
records and earlier checkpoint numbers remain historical; no live or freeze is
claimed, and no files were staged or committed.


## Mixed transport and component Repair revision (2026-09-25)

Current architecture is in docs/v3_design.md; chronological checkpoints and tests are in
 docs/v3_development.md; delivery/live boundaries are in docs/v3_milestone.md.
The revision is implemented + offline-validated and introduces per-leg WALK/TRANSIT/DRIVE selection, compact joint target worksheets
and application-partitioned dependency-component acceptance. Optional transfers and their
frontend renderer are shared output compatibility, not a V3-exclusive quality contribution.
Initial prompts, K, shared acquisition, product default and independent V0-V2 execution remain
unchanged. Routes are now16 stage sends /32 elements (4 reserved for proposals); preparation
cap is45 seconds. No new live or freeze is implied.


## Shared first-generation mixed transport (current offline checkpoint)

V1/V2/V3 now use shared baseline routing, bounded pre-generation mixed-mode options,
one primary generation, and actual-adjacency/time transfer binding before the version's
post-primary step. V1/V2 report conflicts and UNKNOWN without repairing activities.
V3 reuses the same evidence and adopted transfers in its existing validator and Repair.
V0 remains tool-free. This is a shared baseline upgrade, not V3-exclusive mechanism value.

The normal planning supply is unchanged: this does not rediscover omitted POIs, increase K,
or add a second discovery pass. Default WALK preference permits evidence-supported TRANSIT
and DRIVE alternatives; explicit supported requirements remain restrictive. Representative
TRANSIT never inherits final-time PASS. Provider duration and DRIVE application reserve are
separate. The primary projection retains all directed baseline facts in a compact catalogue;
it drops redundant wrappers, not inconvenient facts. No selective fact omission is performed.
Unbound actual adjacencies remain in application-owned `route_diagnostics`, including
per-mode facts and unresolved alternatives; absent transfers do not erase obligations.

Primary input is 252000, output 16384. Supplementary totals are 32 directed pairs / 32 sends /
64 requested elements; post-generation reservations are 16 / 16 / 32 within those totals.
Baseline remains 7 / 400 / 64. Cumulative route-work wall time is 120 seconds with 30 seconds
reserved for post-generation, always inside the original request deadline. Other acquisition,
Repair and Nearby limits are unchanged. Common transport policy now belongs to `transport`
in runtime.yaml; Repair-only authority and added-burden policy remain version-specific.

Implementation and tests are recorded in `docs/v1_development.md`. This checkpoint has only
offline evidence; historical development live records are unchanged and do not validate it.
No new live, evaluation, freeze, commit or push is implied.


## Shared preference input checkpoint (2026-09-25)

The existing one-call interpreter now includes a bounded preference input assessment shared by
V0-V3. Exact-sourced user issues stop before travel tools; safety has separate product output.
Invalid DTO/provenance remains a system failure; real-world UNKNOWN is not input invalidity.
VALID does not override existing capability or hard-requirement checks. Empty preferences retain
no-model execution. Product engine, travel policies and budgets are unchanged. The gate, frontend
feedback and stop/cleanup paths are implemented + offline-validated; actual LLM classification
accuracy is untested. Historical records remain unchanged. See docs/shared_preference_input.md
for contracts, compatibility, test sequence and actual serializer sizing.


### Minimum daily coverage update (2026-09-25)

Shared output now reports the one-primary-visit minimum independently of 2-5 review
quantity guidance. V0-V2 remain diagnostic-only; V3 prioritizes confirmed minimum gaps
below hard protections and above optional reviews. Explicit source-linked full-day time
protections support exemptions; uncertain applicability remains unknown. Product output
includes coverage status without research metadata or source quotations. The primary
prompt, default engine and budgets are unchanged. See [shared minimum coverage](docs/shared_minimum_daily_coverage.md)
for counting, compatibility, exemption and partial-result boundaries, and the V3 development
checkpoint for offline and live evidence. This does not retroactively validate historical runs.


Minimum coverage live checkpoint (2026-09-25): the single authorized Honolulu run
`f9bd621d-0eb5-47d7-8af8-03825d57524b` repaired three zero-main-visit dates in round1;
all nine days meet the minimum, while one ordinary quantity review remains. Five actual
Repair calls retained eight additions (10 -> 18 main visits), exit0. This supplies limited
live evidence for the observed path only; exemptions/review-off remain offline-tested.
See `docs/v3_development.md` and the complete run report for counters, UNKNOWNs and limits.
No freeze or formal evaluation is implied.


Preference Gate contract-alignment checkpoint: prompt11/wire9/input2 reserves operational
conflict links structurally to structured issues and retains domain fail-closed enforcement.
The historical first smoke remains BLOCKED; see docs/shared_preference_input.md for offline
results and the separately authorized new interpreter-only smoke. No travel budget changes.


New Preference Gate smoke `9c8eb048-1e8c-47bd-b17f-9578a7c7c6f8` stopped before any model
send due to a capture-harness UnboundLocalError. All10 cases NOT_ATTEMPTED; SDK resources
closed. Alignment remains offline-validated; Step1 live remains BLOCKED. No rerun performed.

### Quantity comparison-pool reuse checkpoint (2026-09-26)

Offline verification confirms that V3 already passes the full enriched/admitted comparison
pool into Repair, including candidates outside the original selected supply. No candidate
selection, operation-permission, adoption, budget or production-default change was needed.
Dates/counts remain validator-derived; synthetic one/three/five-date tests exclude any
London, fixed-date or four-day special case.

The development acceptance tool now supports opt-in bounded pre-Repair snapshots and
explicit quantity-review pass-through. A separate offline replay entry reconstructs
typed scope/windows and evidence-only candidate preparation, preserving request/semantic
usage and missing evidence. Capture failures are explicit and do not rewrite planning
outcomes. Replay does not run providers, models, round localization or adoption, and does
not restore D's missing historical pool. Existing V0-V2 paths remain unchanged.

Validation: 15 new tests, 421 focused V3 tests, and final full backend suite 1640 passed /
9 skipped; Ruff and compilation passed. Synthetic CLI serialization/replay also passed.
No new live execution, commit, P3 work or freeze. Quantity improvement on D remains
unverified; the next step requires separate approval for a quantity-enabled captured pilot.
See [.scratch/quantity-quality-reuse/implementation.md](.scratch/quantity-quality-reuse/implementation.md)
for TDD corrections, the existing-policy regression matrix and replay limitations.

Quantity-review D pilot (2026-09-26): one separately authorized captured run completed
in 183.844 seconds, exit0. The new initial itinerary had three dynamic quantity gaps
(October 3/7/8); two Repair rounds added three visits, from15 to18 distinct canonical
IDs, yielding daily counts3/3/2/2/2/2/2/2. Original activities stayed unchanged. Two
additions came from the comparison pool and one from unused selected supply. Repair
reused37 qualified candidates without new search/Details/retrieval/semantic calls;
2/5 Repair model calls and18/24 route sends remained within existing budgets. All three
capture types completed and saved-snapshot offline replay succeeded.

This supports the current quantity/reuse mechanism only. Penguin Beach and its parent
London Zoo are distinct IDs on the same day, exposing a site-level richness limitation
beyond canonical nonrepetition. Final validation retains26 UNKNOWNs; no mountain-climbing
fulfillment or verified cost/access claim is implied. No rerun, production-default change,
P3 work, commit or freeze. See the [pilot report](artifacts/poi_semantics_acceptance/20260926_D_quantity_review/report.md).
