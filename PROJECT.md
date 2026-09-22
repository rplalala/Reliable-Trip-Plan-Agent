# Capstone Project Context

Current source of truth. Updated 2026-09-22.

## Purpose and implemented scope

An LLM-Based Travel Planning System for Feasible and Reliable Itinerary Generation studies a
sequence of independently runnable mechanisms: V0 plain LLM, V1 external information/tools,
V2 RAG discovery, and future V3 validation/targeted repair/re-validation. V0/V1/V2 runners exist;
V3 is not implemented. Current responsibility is engineering design, implementation and development
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
targeted repair and re-validation. Its runtime, schemas, repair loops and runner are not
implemented. Shared baseline fixes are not V3 contributions. Future evaluation must use
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
