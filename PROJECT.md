# Capstone Project Context

Current source of truth. Updated 2026-09-24.

## Purpose and implemented scope

An LLM-Based Travel Planning System for Feasible and Reliable Itinerary Generation studies a
sequence of independently runnable mechanisms: V0 plain LLM, V1 external information/tools,
V2 RAG discovery, and V3 validation/targeted repair/re-validation. All four runners exist;
V3 has offline-tested structured findings, a read-only validator, bounded feedback-driven repair,
request resource assembly and final-primary Nearby wiring. The A/B/C checkpoints additionally
cover elastic time/real adjacency, conditional coverage and adjacent moves, and evidence-scoped
operating/transfer repair; these changes are implemented + offline-validated only. See the latest
checkpoint in docs/v3_design.md for supported evidence and limitations. Historical development
live records remain separate and do not validate these later corrections retroactively.
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
conservative clarification limitation. Product/developer APIs remain V0-only; frontend budget,
clarification and developer input/version selection need separate alignment.

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
ceilings, acceptance rules, ledger accounting and sizing limits are in `docs/v3_design.md`.

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
`docs/v3_design.md`; primary sizing is not relabeled as Repair sizing.

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
record, previous test failures and unchanged actual Repair sizing remain in docs/v3_design.md.
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
`docs/v3_design.md`; this revision has no live evidence. Historical three-day no-Repair and
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
chronology, exact sizing, limits and unsupported capabilities are in docs/v3_design.md. No live,
benchmark, vector/SQL/Weather/primary-budget change, commit or freeze accompanies this checkpoint.
Historical three-day/seven-day observations and preexisting work remain; the full seven-day
rejection cause is not claimed resolved. Further live work needs separate authorization.
