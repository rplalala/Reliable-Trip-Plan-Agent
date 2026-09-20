# Capstone Project Context

Current source of truth. Updated 2026-09-20.

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

A future shared Weather provider change to Open-Meteo and a 15-selectable-date horizon is a TODO,
not implemented. Proposed horizon is today through today+14 inclusive, independently capped at
10 travel days; current code still uses today through today+9. Same-day remaining-hour planning
is unsupported. No provider, budget, prompt, default engine or database change is part of acceptance.
Exact historical vectors require retained local artifacts; a clean clone is not an exact DB backup.
