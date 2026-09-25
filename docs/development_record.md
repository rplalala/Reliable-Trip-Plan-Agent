# Shared development record

> Repository cleanup (2026-09-20): source/document/config recovery snapshots, including
> `D:/Workspace/Capstone/phase6_source_snapshots`, have been permanently deleted by user approval.
> Snapshot paths in dated entries describe historical actions, not available recovery locations.
> Retired selector implementations are no longer executable. Historical methods/results remain.

## Cross-version evolution index

| Event | Reason for change | Detailed owner |
| --- | --- | --- |
| QCGRE extension | Google-rank and fixed-vocabulary assumptions complicated RAG/open semantics. | [Record](v1_selector_experiments.md#m-f504c20b22a6) |
| B1 two-stage selector | Open semantic trade-offs motivated bounded model shortlisting/final choice. | [Record](v1_selector_experiments.md#m-0ed57281c9e1) |
| B2 evaluator | Separate semantic judgments from deterministic set selection. | [Record](v1_selector_experiments.md#m-4fab216c5669) |
| Minimum-set diagnosis | Fixed-input replay separated cardinality policy from evaluator value. | [Record](v1_selector_experiments.md#m-e278491d273d) |
| Deterministic supply | Retain open semantics and facts without a compulsory evaluator. | [Record](v1_selector_experiments.md#m-74fdef52eda9) |
| Shared structured input | Authoritative form fields and one optional shared interpretation. | [Record](development_record.md#m-32a5fafda908) |
| Shared output roles | Separate scheduled main activities from optional references. | [Record](development_record.md#m-c298da5e03e3) |
| Post-itinerary Nearby | Independent nearby discovery replaces same-pool reference allocation. | [Record](v1_development.md#m-cbc1274c0bc6) |
| Phase 6 integration/failure | RAG wiring required normal SQL/resolution evidence beyond Google-only fallback. | [Record](v2_development.md#m-4a1077481a18) |
| SQL diagnosis | Execute/read variance and missing original query vectors constrained replay. | [Record](v2_development.md#m-c25267e4e4c9) |
| 60/180 development validation | Longer bounded waiting allowed functionality checks, not an optimization claim. | [Record](v2_development.md#m-6d53b29b6f5c) |
| quality_first_1 | Separate new successes from sends and reuse every admitted compatible cache. | [Record](development_record.md#m-e2a7f5a4bbc3) |
| 160k and pre-send failures | Input sizing and observer failures required distinct records. | [Record](development_record.md#m-2b8be5c42c69) |
| Joint V1/V2 recovery acceptance | Approved fresh recovery supplied actual normal-path and capture evidence. | [Record](development_record.md#m-e07748f66be8) |

Dated records below preserve original scope, status and evidence; they are not current runtime instructions. Current design is maintained separately. Proposed or unexecuted steps remain unexecuted unless a later explicitly identified record establishes otherwise.

<a id="m-ca65baf1acb6"></a>
## Preamble

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ca65baf1acb6-0"></a>

> Historical record, preserved during the 2026-09-20 documentation consolidation.
> Statements such as Current, Proposed, or not implemented describe their original checkpoints.
> Use [PROJECT](../PROJECT.md) for current status and the [documentation index](../README.md) for current design.

<a id="m-5324ae603f58"></a>
## Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2

_Source context: original document introduction/navigation. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-5324ae603f58-0"></a>

Status: **quality_first_1 implemented + bounded development-live-validated after authorized recovery; historical initial observer failure preserved. Not a benchmark or re-freeze.**

<a id="m-f8410a308d5a"></a>
## Accepted baseline closeout and Git save proposal - 2026-09-20

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f8410a308d5a-0"></a>

User accepted the bounded quality_first_1 checkpoint. Current status:
**implemented + bounded development-live-validated**. Normal RAG main-candidate integration,
two-pass Details,G/send separation,common comparison and supply have normal-path evidence.
No formal benchmark,all-branch acceptance,production-ready declaration or V1/V2 re-freeze.
Budgets/selection/Tokyo repetitions stop here. This is documentation and Git planning only.
The earlier checkpoints below are historical snapshots, not current unimplemented gates.

<a id="b-f8410a308d5a-1"></a>

Evidence index: logs/quality_first_1_live_20260920/recovery/{manifest.json,audit.json,
v1_result.json,v2_result.json,retrieval_capture.json,usage_unredacted_metadata.json,
session_summary.json}; initial pre-send failures stay in the parent directory. Earlier
60/180 success remains in logs/phase6_development_window_20260920. Source hashes checked
against the recovery manifest: no implementation differences at closeout.

<a id="b-f8410a308d5a-2"></a>

V1:24 ordinary new successes ->24 comparison ->12 supply ->8 scheduled.
V2:16 RAG Details,15 admitted cached successes plus24 ordinary new successes ->39 comparison
->12 supply ->8 scheduled,2 RAG-only. WHAT MUSEUM was resolved but outside C;21 retrieved
entities remained unparsed due the16-attempt limit; mixed sources reached no final supply.
All admitted compatible caches considered does not mean all resolved candidates must be selected.
Application caches are independent per run; this is not cross-version free reuse. Profile/Reviews
were not triggered. Initial two pre-send failures and separately approved recovery are distinct.

<a id="b-f8410a308d5a-3"></a>

Actual ordinary/RAG Details: V1 24/0,V2 24/16; baseline144 and alternative16 measured elements
per run; Nearby3 each. Google total42/61 is work, not invoice cost. V2 reasoner usage unknown.
RAG36.56s,Web29.12s,primary generation15.09/13.65s,total42.05/106.41s. Do not attribute the whole
delta to retrieval or call different-query SQL26.20/1.03s a cold/hot experiment. Eight scheduled
places each means equal count with different choices, not proof of RAG value or lack of value.

<a id="m-61a2c7801de0"></a>
## Explicit reproducible development entry points

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Accepted baseline closeout and Git save proposal - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-61a2c7801de0-1"></a>

Save this complete input as request.json locally (not a manifest wrapper):

Verbatim passages shared with another maintained section: [1](development_guide.md#b-61a2c7801de0-0), [2](development_guide.md#b-61a2c7801de0-2), [3](development_guide.md#b-61a2c7801de0-3), [4](development_guide.md#b-61a2c7801de0-4), [5](development_guide.md#b-61a2c7801de0-5), [6](development_guide.md#b-61a2c7801de0-6), [7](development_guide.md#b-61a2c7801de0-7). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-544e9ea4b7c3"></a>
## Finite outstanding issues (not implementation authorization)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Accepted baseline closeout and Git save proposal - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-544e9ea4b7c3-0"></a>

No item below blocks saving the accepted normal-path capacity checkpoint. Each limits a specific
future capability/evaluation claim; none automatically requires another complete live run.

<a id="b-544e9ea4b7c3-1"></a>

| Priority / issue | Current evidence / type | Blocks this closeout? | Later claim or evaluation impact | Smallest next step |
|---|---|---|---|---|
| P1 Weather404 | Both accepted runs sent one request and received404; tool/integration | No | Normal weather capability unproven in these cases | Inspect saved HTTP request/response, adapter endpoint/date/parameters and service configuration; distinguish API/path/access/data causes before any repair or paid rerun |
| P1 frontend budget | Form/types allow absent budget; backend requires amount/currency; product contract | No | Product submission can fail before planning; UI is not a faithful backend evaluation entry | Separately approve minimal required-budget/clarification UI alignment and focused frontend tests |
| P2 Web zero accepted facts | V2 one search,three reasoner calls,two pages yielded zero accepted facts; evidence/integration | No | Cannot claim current official facts were successfully grounded for that gap | Trace saved sources -> extracted claims -> gate reason codes; distinguish missing support from mapping/gate defects without loosening gate by assumption |
| P2 exact retrieval variability |26.20/1.03s for DIFFERENT queries; prior1.13s to15s timeout/TOAST evidence; performance | No | No production SLA or cold/hot inference | Preserve exact baseline/query vectors; separately choose measured storage/resource experiment if latency becomes a goal; no timeout/SQL change now |
| P2 Web overhead and usage |29.12s integration; three reasoner token usages unknown; performance/observability | No | Total V2 delta not all RAG; complete cost comparison unavailable | Account for existing search/extraction/page spans; propose local reasoner metadata observation separately |
| P2 visitor access | Architectural offices/staff cafeteria appear in supply/references; suitability | No | Identity/type does not prove public visitor access | Review saved candidates and define a bounded access-evidence policy before claiming suitability |
| P2 same-complex references | Sub-metre/same-building distinct IDs; recommendation quality | No | Canonical dedupe does not establish experiential diversity | Annotate existing examples and specify optional same-complex treatment; do not merge identities by guess |
| P2 cost/budget | All activity costs null; generation/evidence | No | User total budget preserved but feasibility against it cannot be verified | Define unknown-cost reporting/evidence requirements, without inventing fees |
| P2 soft preference/feasibility |8 places each but different sets, uncertainty in transfers/hours; generation quality | No | Counts cannot prove RAG benefit or uselessness; no V3 assurance | Retain inputs/outputs and define future checks only under separate evaluation authorization |
| P2 uncovered branches | No K16 live,nonzero Profile,fallback,failed-cache,cancel or empty references | No | Evidence restricted to tested offline cases and two normal live paths | Index existing offline coverage first; request a specifically bounded check only when needed |
| P2 version/UI dispatch | Product and dev APIs V0-only; CLI/Python V1/V2 available | No | Web UI cannot be presented as V2 or quality_first_1 | Separately specify explicit version/config injection; do not change defaults now |
| P2 Melbourne named ambiguity | Earlier REQUIRED ambiguity stopped before RAG; identity/product | No | General named identity resolution remains conservative | Preserve clarification; separate approved typed-evidence review if required, no name/ID hardcoding |

<a id="b-544e9ea4b7c3-2"></a>

Recommended next task AFTER baseline saving: narrow Weather404 diagnosis using saved captures
and adapter/configuration inspection. It is a concrete tool issue, not model quality, and does
not require repeating Tokyo or starting formal comparative evaluation. No such task starts here.

<a id="m-f40cb797224f"></a>
## Proposed Git save sequence (approval pending; no staging)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Accepted baseline closeout and Git save proposal - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f40cb797224f-0"></a>

Current HEAD60902ac on feature/v2. Inventory179 individual files:87 modified,11 already deleted,
81 untracked files (the usual short status collapses those into74 untracked entries).
Every pending path is assigned exactly once below. No new deletion is proposed.

<a id="b-f40cb797224f-1"></a>

1. `feat(planning): checkpoint shared V1 and V2 acquisition baseline` (165 paths).
   All changed backend/app,backend/tests,config,scripts,pyproject.toml and uv.lock together.
   Covers shared structured interpretation; deterministic supply; itinerary_2/Nearby; Phase6;
   quality_first_1/160k; runtime/caches/budgets; diagnostic/harness repairs and direct tests.
   Preserve inactive B2 implementations, DTOs, fixtures and analysis utilities in this checkpoint.
   This intentionally prioritizes a usable coherent backend over reconstructing a false series
   of historical features. graph/client/config/schema share interleaved changes. Tests directly
   import scripts.acceptance_session,requirement_acceptance,measure_quality_first_payload,
   diagnose_tripworld_sql,b2_development_fixtures and measure_b2_policy. Splitting those out
   would strand test/import dependencies. semantic_poi_pipeline is the ACTIVE acquisition base
   of PlanningCandidateSupplyPipeline, whose overridden selector bypasses the historical
   evaluator/subset enumeration; its filename is not evidence of obsolescence.
   Dependency: existing Phase1-5 commits. No default-engine switch or B2 reactivation.
2. `feat(frontend): preserve itinerary reference display` (3 paths).
   ItineraryView.tsx,ItineraryView.test.tsx,types.ts. Depends on1's output contract. Saves the
   existing display/type changes only; does not claim budget-form or version-selector alignment.
3. `docs(planning): record accepted baseline and remaining integration gaps` (11 paths).
   PROJECT,README,current/evolution/B1/B2/version records and existing Phase6 proposal.
   Depends on1/2 for accurate current descriptions. Includes the ALREADY DELETED old
   poi_selector_architecture_review.md, with current/evolution/B1 documents replacing its role.
   Exact original remains available at HEAD60902ac; this is not new historical code deletion.

<a id="b-f40cb797224f-2"></a>

Migration deletions in1: experience_selection,named_place_intent,review_sensitivity,trip_intent
policy modules and six older tests. Current responsibilities are in interpreted_requirements,
preference_interpretation,planning_supply/review_selection/semantic_poi_pipeline and their
new shared-input/V2 suites. Old test_phase6_integration.py was a V1-era contract test, not the
current V2 suite. Include replacement files and associated deletions together, never isolated.
No experiment file is dropped because its name contains semantic or B2. Historical tools may
still require ignored input archives and are not guaranteed to recreate missing historical data.

<a id="b-f40cb797224f-3"></a>

Do not rerun tests merely to save this checkpoint; preserve the recorded validation ledger.
On later commit authorization inspect staged stats/full diff,exact inventory,secrets/ignores
and dependency scopes; do not modify implementation to force a smaller split. Each message is
English and no commit is created by this proposal. Runtime behavior is reproducible only with
its documented dependencies and local data, not from code commits alone.

<a id="b-f40cb797224f-4"></a>

<details>
<summary>Exact pending path assignment at closeout (M modified, D pre-existing deletion, ?? untracked)</summary>

<a id="b-f40cb797224f-5"></a>

Group 1:

<a id="b-f40cb797224f-6"></a>

```text
 M backend/app/api/developer/planning.py
 M backend/app/api/product/planning.py
 M backend/app/api/schemas/planning.py
 M backend/app/evidence/experience_models.py
 M backend/app/evidence/models.py
 M backend/app/evidence/selection_models.py
 M backend/app/evidence/selection_normalization.py
 M backend/app/integrations/google/places.py
 M backend/app/integrations/http.py
 M backend/app/integrations/models.py
 M backend/app/integrations/protocols.py
 M backend/app/llm/azure_foundry/client.py
 M backend/app/llm/azure_foundry/dto.py
 M backend/app/llm/azure_foundry/itinerary_cost_projection.py
 M backend/app/llm/azure_foundry/mapping.py
 M backend/app/observability/run_trace.py
 M backend/app/policies/experience_profile.py
 D backend/app/policies/experience_selection.py
 D backend/app/policies/named_place_intent.py
 M backend/app/policies/official_web.py
 M backend/app/policies/poi_capacity.py
 M backend/app/policies/poi_funnel.py
 M backend/app/policies/poi_selection.py
 D backend/app/policies/review_sensitivity.py
 M backend/app/policies/transport.py
 D backend/app/policies/trip_intent.py
 M backend/app/runtime/budget.py
 M backend/app/runtime/budget_limits.py
 M backend/app/runtime/cache.py
 M backend/app/runtime/config_loader.py
 M backend/app/runtime/config_models.py
 M backend/app/schemas/__init__.py
 M backend/app/schemas/itinerary.py
 M backend/app/schemas/named_place_intent.py
 M backend/app/schemas/planning.py
 M backend/app/schemas/request.py
 M backend/app/schemas/trip_intent.py
 M backend/app/services/evidence_acquisition.py
 M backend/app/services/official_web_integration.py
 M backend/app/services/planning.py
 M backend/app/services/review_selection.py
 M backend/app/services/web_evidence_acquisition.py
 M backend/app/versions/v0/graph.py
 M backend/app/versions/v0/prompts.py
 M backend/app/versions/v0/runner.py
 M backend/app/versions/v0/state.py
 M backend/app/versions/v1/graph.py
 M backend/app/versions/v1/official_web.py
 M backend/app/versions/v1/prompts.py
 M backend/app/versions/v1/runner.py
 M backend/app/versions/v1/state.py
 M backend/tests/api/test_developer_planning.py
 M backend/tests/api/test_product_planning.py
 M backend/tests/conftest.py
 M backend/tests/evidence/test_opening_hours.py
 M backend/tests/integrations/google/test_adapters.py
 M backend/tests/llm/azure_foundry/test_client.py
 M backend/tests/llm/azure_foundry/test_dto.py
 M backend/tests/llm/azure_foundry/test_mapping.py
 M backend/tests/llm/azure_foundry/test_v1_itinerary.py
 M backend/tests/observability/test_run_trace.py
 D backend/tests/policies/test_experience_selection.py
 D backend/tests/policies/test_named_place_intent.py
 M backend/tests/policies/test_official_web.py
 M backend/tests/policies/test_poi_funnel.py
 M backend/tests/policies/test_poi_selection.py
 D backend/tests/policies/test_semantic_intent_migration.py
 M backend/tests/policies/test_transport.py
 D backend/tests/policies/test_trip_intent.py
 M backend/tests/runtime/test_config.py
 M backend/tests/schemas/test_request.py
 M backend/tests/services/test_planning.py
 M backend/tests/services/test_route_matrix_chunking.py
 M backend/tests/services/test_transport_evidence.py
 D backend/tests/services/test_v1_candidate_funnel.py
 M backend/tests/services/test_v1_review_selection.py
 M backend/tests/versions/v0/test_graph.py
 M backend/tests/versions/v0/test_runner.py
 M backend/tests/versions/v1/fakes.py
 M backend/tests/versions/v1/test_graph.py
 M backend/tests/versions/v1/test_named_place_extraction.py
 M backend/tests/versions/v1/test_official_planner_size.py
 M backend/tests/versions/v1/test_official_web_integration.py
 D backend/tests/versions/v1/test_phase6_integration.py
 M backend/tests/versions/v1/test_places_contracts.py
 M backend/tests/versions/v1/test_runner.py
 M config/runtime.yaml
 M pyproject.toml
 M uv.lock
?? backend/app/integrations/dispatch.py
?? backend/app/llm/azure_foundry/requirement_capture.py
?? backend/app/policies/acquisition_opportunities.py
?? backend/app/policies/interpreted_requirements.py
?? backend/app/policies/itinerary_output.py
?? backend/app/policies/planning_supply.py
?? backend/app/policies/semantic_evaluation.py
?? backend/app/policies/semantic_projection.py
?? backend/app/policies/semantic_set_selection.py
?? backend/app/policies/tripworld_query_plan.py
?? backend/app/runtime/token_counting.py
?? backend/app/schemas/interpreted_requirements.py
?? backend/app/schemas/planning_supply_result.py
?? backend/app/schemas/requirement_boundary.py
?? backend/app/schemas/revised_v1_result.py
?? backend/app/schemas/semantic_evaluation.py
?? backend/app/schemas/tripworld_discovery.py
?? backend/app/services/candidate_details.py
?? backend/app/services/generation_resources.py
?? backend/app/services/planning_supply_pipeline.py
?? backend/app/services/preference_interpretation.py
?? backend/app/services/preference_prompts.py
?? backend/app/services/reference_discovery.py
?? backend/app/services/semantic_evaluator.py
?? backend/app/services/semantic_poi_pipeline.py
?? backend/app/services/tripworld_discovery.py
?? backend/app/tripworld/retrieval/diagnostics.py
?? backend/app/tripworld/retrieval/query_tokens.py
?? backend/app/tripworld/retrieval/runtime.py
?? backend/app/versions/v2/__init__.py
?? backend/app/versions/v2/config.py
?? backend/app/versions/v2/graph.py
?? backend/app/versions/v2/runner.py
?? backend/app/versions/v2/state.py
?? backend/tests/fixtures/requirement_boundary/captured_b_domain_draft.json
?? backend/tests/fixtures/requirement_boundary/live_acceptance_cases.json
?? backend/tests/fixtures/requirement_boundary/semantic_acceptance_cases.json
?? backend/tests/fixtures/requirement_boundary/shared_structured_cases.json
?? backend/tests/integrations/google/test_nearby.py
?? backend/tests/llm/azure_foundry/test_open_contracts.py
?? backend/tests/llm/azure_foundry/test_requirement_acceptance_harness.py
?? backend/tests/llm/azure_foundry/test_requirement_boundary.py
?? backend/tests/llm/azure_foundry/test_requirement_semantics.py
?? backend/tests/policies/test_grouped_semantic_contract.py
?? backend/tests/policies/test_planning_supply.py
?? backend/tests/policies/test_semantic_evaluation.py
?? backend/tests/policies/test_semantic_set_selection.py
?? backend/tests/request_fixtures.py
?? backend/tests/services/test_b2_acquisition.py
?? backend/tests/services/test_itinerary_references.py
?? backend/tests/services/test_planning_supply_pipeline.py
?? backend/tests/services/test_quality_first.py
?? backend/tests/services/test_reference_discovery.py
?? backend/tests/services/test_request_wide_preference.py
?? backend/tests/services/test_shared_planning_input.py
?? backend/tests/services/test_tripworld_discovery.py
?? backend/tests/tripworld/test_runtime_retrieval.py
?? backend/tests/tripworld/test_sql_diagnostic.py
?? backend/tests/versions/v1/test_b2_integration.py
?? backend/tests/versions/v1/test_interpreted_requirements.py
?? backend/tests/versions/v1/test_provenance_profile_regressions.py
?? backend/tests/versions/v1/test_reference_stage.py
?? backend/tests/versions/v1/test_semantic_safety.py
?? backend/tests/versions/v2/test_v2_runner.py
?? config/runtime_quality_first_1.yaml
?? config/v2_development_override.json
?? scripts/acceptance_session.py
?? scripts/analyze_b2_decision.py
?? scripts/b2_development_fixtures.py
?? scripts/diagnose_tripworld_sql.py
?? scripts/measure_b2_contract.py
?? scripts/measure_b2_policy.py
?? scripts/measure_quality_first_payload.py
?? scripts/prepare_tokenizer.py
?? scripts/requirement_acceptance.py
?? scripts/run_v2.py
```

<a id="b-f40cb797224f-7"></a>

Group 2:

<a id="b-f40cb797224f-8"></a>

```text
 M frontend/src/features/planning/components/ItineraryView.tsx
 M frontend/src/features/planning/types.ts
?? frontend/src/features/planning/components/ItineraryView.test.tsx
```

<a id="b-f40cb797224f-9"></a>

Group 3:

<a id="b-f40cb797224f-10"></a>

```text
 M PROJECT.md
 M README.md
 D docs/poi_selector_architecture_review.md
 M docs/tripworld_phase6_proposal.md
 M docs/v0_milestone.md
 M docs/v1_design.md
 M docs/v1_milestone.md
?? docs/b2_implementation.md
?? docs/poi_selection.md
?? docs/poi_selection_evolution.md
?? docs/v1_selector_implementation.md
```

<a id="b-f40cb797224f-11"></a>

</details>

<a id="m-c18e3f1ba5a0"></a>
## Git scope versus local experimental materials

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Accepted baseline closeout and Git save proposal - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-c18e3f1ba5a0-0"></a>

Git should save current source/config/tests/lockfile and existing English records, including
harness recovery and160k YAML. pre_quality_first_1_20260919T202927Z is NOT a substitute:
at that checkpoint its source/scripts/acceptance_session.py differed and it contained no
quality_first_1 YAML. That source snapshot was later deleted by user authorization.
Recovery manifests contain implementation hashes, not complete replacement source backups.
The revised baseline remains in the uncommitted workspace until separately approved commits.
No claim of an independent current-source backup or verified database backup is made.

<a id="b-c18e3f1ba5a0-1"></a>

Already tracked static metadata: data/tripworld/{manifest.json,category_semantics.v1.json,
embedding_model.v1.json,retrieval_queries.v1.json}; database space/policy definitions in source;
compose.tripworld.yaml pins the DB image and declares tripworld_pgdata. These do not contain
all generated corpus/vector/database state. Actual mounted volume identity/backup health was
not queried in this task; the compose declaration alone is not a verified DB backup.

<a id="b-c18e3f1ba5a0-2"></a>

The following was the preservation inventory proposed at that historical checkpoint, not a
new backup instruction. Deleted recovery material is identified explicitly:
- thesis_notes/, especially V2/events/V2-05_bounded_runtime_integration.md;
- logs/quality_first_1_live_20260920/ (initial failures and separately authorized recovery),
  recovery/manifest.json,audit.json,session_summary.json,SDK/HTTP traces,usage metadata and
  query_vectors/; plus earlier logs/phase6_acceptance_20260920 and
  logs/phase6_development_window_20260920 when present;
- logs/source_snapshots/ and historical B2 decision artifacts/pickles were listed then; source
  snapshots and retired pickle snapshots were later deleted. Surviving selected research results
  do not restore those source checkpoints;
- data/tripworld/raw,processed,artifacts,reports including retrieval_entities.parquet and its
  generated manifest,phase5_embedding_run.json and phase5 checkpoints/query_checkpoints;
- populated PostgreSQL volume/database, including vectors and corpus/space compatibility rows;
- .cache/tokenizer for the current offline tokenizer and data/tripworld/tokenizer_cache
  for data-layer tooling. Pin/checksum source is Git; cache bytes are not.

<a id="b-c18e3f1ba5a0-3"></a>

Real .env/.env.tripworld and secrets stay outside Git and require separate secure provisioning,
not inclusion in an experiment archive with provider payloads. Existing ignore rules verified.
Changed-file literal key/private-key pattern scan found no matches; this is a limited check,
not a proof that all private information has been removed. The four small requirement fixtures
are parsed/synthetic contract examples, not raw provider captures; captured_b_domain_draft.json
explicitly records parsed-draft provenance and its non-raw limitation. Retain that distinction.
No force-add, data copy, export or backup operation was performed.

<a id="m-e07748f66be8"></a>
## Authorized recovery: quality_first_1 bounded live checkpoint - 2026-09-20

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-e07748f66be8-0"></a>

Status: implemented + bounded development-live-validated for the opt-in shared acquisition
policy and160k guard. Both fresh runs completed after the user explicitly authorized recovery
from the pre-send observer fault. This is not a full correctness proof, production SLA,
formal V1/V2 benchmark, ten-day long-context validation or automatic re-freeze.
The preceding failed attempt and its incorrect shared-fault continuation remain historical.

<a id="m-a7efb5d89c3e"></a>
## Minimal recovery and offline evidence

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Authorized recovery: quality_first_1 bounded live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-a7efb5d89c3e-0"></a>

AcceptanceSession.observe_json_transport now replaces only the project JSON adapter's local
HTTP dependency reference. It adds hooks to real adapter-owned clients; the global httpx module
and AsyncClient class remain unchanged. Owned clients still close normally. A wrapped TypeError
is treated conservatively as a shared development-execution failure before another case.
No production acquisition, prompt, model, timeout, budget, SQL or source policy changed.
Actual installed SDK/MockTransport tests exercise Google observation alongside the five-case
model matrix, exact sends, non-duplicated usage, resource closure and wrapped-fault stopping.
62 affected checks passed in30.38s; Ruff/diff passed. These overlap the earlier103 passing
checks and are not added. Full-suite history remains911 passed/9 skipped/1 failed, followed
by documented targeted fixes; no full-suite rerun or retrospective all-green claim.

<a id="b-a7efb5d89c3e-1"></a>

Same frozen request and effective config as the preceding record: Tokyo,2026-09-21..23,
3 travelers,180000 JPY, Meiji Jingu required, small museums/distinctive local architecture.
Request hash70515e8d598be104571ed892a5b6b44f8dc31332ad9cd653df9d9375f7fd1b71.
Config hashaec5fb5d2b07dffb486b0d8211ae4b339bf6006af980a2cd1ede47f85746d722.
Implementation/prompt/schema/corpus/space/policy hashes were frozen again before recovery.
Actual dispatch run_v1 then run_v2,600s outer, independent request caches, no DB prewarming.
Normal/effective values both C48/G24/ordinary sends32/K12/P6; one resolved REQUIRED.

<a id="m-8f9141727025"></a>
## Candidate acquisition and source accounting

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Authorized recovery: quality_first_1 bounded live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-8f9141727025-0"></a>

| Actual observation | V1 | V2 |
|---|---:|---:|
| Google candidate observations (excluding destination) |41|41|
| Google canonical identities before RAG |40|40|
| Canonical union |40|56|
| Admitted / omitted by common capacity |40 /0|48 /8|
| Compatible successful Details reused in admitted set |0|15|
| Ordinary new sends / new qualified successes |24 /24|24 /24|
| Ordinary failed/ineligible Details |0|0|
| Qualified comparison pool |24|39|
| Actual supply / shortfall |12 /0|12 /0|
| Scheduled distinct canonical POIs |8|8|
| Unscheduled supply / required |4 /0|4 /0|
| Unlinked activities |0|0|
| Independent Nearby references |3|3|

<a id="b-8f9141727025-1"></a>

Both ordinary stages stopped at new_success_target24, not at32 sends. Full first-pass cache
inspection follows from the completed cache-first loop without deadline and the admitted
sets40/48; it is not a separately instrumented per-key lookup counter. All15 compatible RAG
Details admitted in V2 were qualified, including late positions beyond the old10 truncation.
Cache reuse spent neither ordinary sends nor G. No repeated identical Details path/mask send
occurred; success and source identities were unique. Failed/terminal-cache branches did not
occur live and retain their offline coverage only. The remaining16/9 admitted candidates were
not newly acquired after G was met, not rejected as invalid places.

<a id="b-8f9141727025-2"></a>

V2 used two user DiscoveryIntent queries, not four forced/default queries: 'places with
distinctive local architecture' and 'small museums'. One embedding batch/one HTTP200 attempt,
7 total tokens; no retry. Actual query vectors and integrity/space/text hashes were saved.
Two original exact SQL queries each returned20 positions (40 unique entities). Three known
Google overlaps merged provenance.16 new entity attempts all resolved directly with16 RAG
Details, zero fallback sends, zero RAG-resolution cache hits;21 remaining entities were marked
entity_budget. This is the report's partial status, not failed SQL or Google-only degradation.

<a id="b-8f9141727025-3"></a>

| V2 source class | Admitted | Compared | Supply | Scheduled |
|---|---:|---:|---:|---:|
| Google-only |31|23|8|6|
| RAG-only |15|15|4|2|
| Mixed |2|1|0|0|

<a id="b-8f9141727025-4"></a>

One of16 newly resolved places (WHAT MUSEUM) was outside common admission C48, so its already
paid Details did not enter comparison. One mixed source was also outside admission; another
admitted mixed source was beyond ordinary G and unacquired.15 admitted RAG-only entries were
all considered;11 were not selected by the unchanged final supply policy. Four RAG-only supply
places: ESP MUSEUM, Min-on Music Museum, Bunkamura THE MUSEUM, and the former residence site
of Shimazaki Toson (original provider name/ID preserved in artifacts). The first two were
scheduled. Google ID resolution is not Google discovery; no RAG quota or extra reward exists.

<a id="m-96791a2992bd"></a>
## Actual generated outputs

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Authorized recovery: quality_first_1 bounded live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-96791a2992bd-0"></a>

The following lists summarize actual output only. All times are Tokyo local (+09:00).
All16 activity estimated_cost values across the two runs are null; references have no cost.

<a id="b-96791a2992bd-1"></a>

| Date | V1 primary itinerary | V2 primary itinerary |
|---|---|---|
| Sep21 |09:00-11:00 Meiji Jingu;13:00-15:00 Samurai Museum TOKYO Shinjuku;16:00-17:15 Tokyo Metropolitan Government Building|09:30-12:00 Meiji Jingu;13:00-14:30 ESP MUSEUM;15:00-16:30 Ueshima Museum|
| Sep22 |11:00-12:30 Ueshima Museum;14:00-15:30 Shinkenchiku-sha Aoyama House;16:30-18:00 Japan Traditional Crafts Aoyama Square|11:00-12:30 Min-on Music Museum;14:00-15:30 Tokyo Metropolitan Government Building;16:00-17:30 Samurai Museum TOKYO Shinjuku|
| Sep23 |10:00-12:00 Former Prince Asaka Imperial Family Residence;15:00-16:30 Extinct Media Museum|11:00-12:30 Shinkenchiku-sha Aoyama House;14:00-15:30 DAIKANYAMA T-SITE GARDEN GALLERY|

<a id="b-96791a2992bd-2"></a>

V1 unused supply: Shinjuku Gyoen Museum,Ghibli Museum,HANAKENCHIKU INC.,North Observation Deck
of Tokyo Metropolitan Government Building No.1. V2 unused supply: Shimazaki Toson former
residence site,North Observation Deck,Shigeru Ban Architects,Bunkamura THE MUSEUM.

<a id="b-96791a2992bd-3"></a>

Nearby references (all associated with Sep21, not scheduled; distances are straight-line):
- V1: Treasure Hall Lawn -> Meiji Jingu336.770m (garden/park); Bikkuri Donkey -> Samurai Museum0m
  (family_restaurant);32nd Floor Staff Cafeteria -> Government Building2.369m (restaurant).
- V2: Treasure Hall Lawn -> Meiji Jingu336.770m; Mushiya Seiro Shibuya -> ESP MUSEUM0.436m
  (Japanese izakaya); museum tea room 'Kankaian' -> Ueshima Museum0m (provider art_museum).
  Exact original Japanese display name remains in raw artifacts; these are display translations.

<a id="b-96791a2992bd-4"></a>

All reference IDs were in successful current Nearby ledgers and outside original supply;
all anchor IDs were actually scheduled with known coordinates. Source refs, types, names,
addresses, attributions (returned empty arrays) and distances were retained. Both phases
completed,3 sends/30 raw results/3 references,zero cache hits; five later anchors each were
uncovered under the first-three-representative policy. No reference/top-up/model call or
identity guessing. Main fields including dates/order/times/identity/cost diagnostics were
byte-equivalent under canonical JSON excluding reference_recommendations. Hashes:
V1 8dd86561da4bcceff67b02f647ad5de7bc1d6d4b328035945d9e3403522226bb;
V2 ccc2b414bb7a14f5d547796f7138cf2088bc2ad20940fb481a252bde5452bbc6.

<a id="m-3720267afc83"></a>
## Actual work, tokens and timing

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Authorized recovery: quality_first_1 bounded live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-3720267afc83-0"></a>

| Work | V1 | V2 |
|---|---:|---:|
| Text Search (destination + candidate) |1+3|1+3|
| Ordinary Details / RAG Details |24 /0|24 /16|
| Independent Reviews / Profile / Semantic Evaluator |0 /0 /0|0 /0 /0|
| Weather sends |1 (404)|1 (404)|
| Baseline WALK matrix requests / elements |3 /144|3 /144|
| Alternative TRANSIT requests / measured elements |7 /16|10 /16|
| Nearby actual sends |3|3|
| Total Google HTTP sends |42|61|
| Official Web search-model / reasoner calls |0 /0|1 /3|
| Page tasks / actual HTTP (including redirects) |0 /0|2 /3|
| Query embedding batch / HTTP sends / SQL |0 /0 /0|1 /1 /2|
| Requirement / primary generation sends |1 /1|1 /1|

<a id="b-3720267afc83-1"></a>

Baseline144 cells have no duplicate pair, all12 supply identities are present; alternatives
measure16 one-way pairs, mirrored reverse estimates are not extra API elements. Actual field
masks and modes/features are retained in captures/audit; request counts are not invoice cost.
No Review/Profile evidence need was triggered, so its live ordering/6-place limit is uncovered.
V2's one normal Official Web gap caused the existing search/reasoning/page chain, zero accepted
current facts. This extra work is not solely query embedding or SQL latency, nor a new stage.
Three reasoner calls have unknown token usage in current adapter metadata; do not estimate it.
Embedding prompt subcount was redacted in aggregated trace; total7 and HTTP1 remain observed.

<a id="b-3720267afc83-2"></a>

| Model task | Input | Output incl.reasoning | Reasoning subset | Cached input subset | Cache-write subset |
|---|---:|---:|---:|---:|---:|
| V1 Requirement |3939|633|307|0|3936|
| V1 primary |38166|1984|505|0|38163|
| V2 Requirement |3939|589|265|3936|0|
| V2 primary |37517|1920|484|1477|36037|
| V2 Official Web search |8588|402|229|unknown|unknown|

<a id="b-3720267afc83-3"></a>

SDK response IDs/actual attempts deduplicate usage; callbacks are not added again. Both primary
responses completed with max_output_tokens16384 and no incomplete details. Engineering inputs
40441 (V1) and39792 (V2) include2048 framing and differ from provider counts by methodology.
Both generator projections contain exactly12 supplied places, not the24/39 comparison pools.
Provider prompt caching is observed independently of fresh application caches; no V1 results
were injected into V2. Total model token spend cannot be fully totaled with missing reasoner usage.

<a id="b-3720267afc83-4"></a>

| Phase seconds | V1 | V2 |
|---|---:|---:|
| Interpretation (trace phase) |8.017|6.112|
| RAG |0|36.560|
| Ordinary Details |9.390|10.397|
| Official Web integration |0.044|29.119|
| Primary generation |15.088|13.651|
| Primary ready (runner start through validated snapshot) |40.889|104.278|
| Nearby |1.125|2.109|
| Total runner |42.045|106.414|

<a id="b-3720267afc83-5"></a>

RAG SQL execute26.195713/1.024916s;fetch/decode0.000698/0.004942s;SQL total26.196463/1.029918s.
Two different query vectors; do not treat this as a controlled cold/hot comparison.60s/360s
remain development ceilings, not optimized latency; TOAST/I/O concerns and shadow-table pause
are preserved. RAG embedding1.881s,resolution7.176s. The total difference also includes Web and
route work and does not establish general V1/V2 latency or quality superiority.

<a id="m-978772c81cbd"></a>
## Limitations, evidence health and stop

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Authorized recovery: quality_first_1 bounded live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-978772c81cbd-0"></a>

Weather404 remains; source-valid output does not prove free-text facts or transport feasibility.
All days contain activities, no repeated canonical visits, REQUIRED scheduled in both; this is
not an activity-density guarantee. Fees remain unknown. Architecture-related businesses and
same-complex Nearby items may be weak visitor choices. Staff-cafeteria access is not verified;
sub-metre provider-coordinate distances do not establish entrance proximity or walking time.
V1 itself warns some walking baselines do not support realistic transfers; no V3 repair occurred.
All reference reasons disclose unverified availability/prices/accessibility.

<a id="b-978772c81cbd-1"></a>

No live failure/cancellation/fallback/empty-reference/failed-Details/4-query/K16/over160k branch
was forced. V0 was not run. Those are offline-only or untested limits, not broad live coverage.
Capture errors zero, traces healthy, session closed exactly once, model HTTP and DB connection
closed, implementation hashes unchanged during recovery. Protected capture files required a
read-only elevated metadata extraction; no calls were repeated to recover token observations.
Original failure artifacts remain. Recovery artifacts: logs/quality_first_1_live_20260920/recovery
(manifest,raw outputs/capture,query vectors,audit,usage metadata,session summary).

<a id="b-978772c81cbd-2"></a>

Recommendation: close this bounded quality_first_1 development acceptance checkpoint. No new
acquisition/cache/identity/DTO wiring defect was observed in these two recovered cases. Retain
performance,visitor suitability,free-text/fee and observation-coverage limits for later work;
do not increase caps or automatically run another case. No SQL/storage rebuild, frontend,
Melbourne contract,B2 cleanup,V3,stage/commit/push or re-freeze.

<a id="m-2b8be5c42c69"></a>
## Historical quality_first_1 160k guard and blocked acceptance attempt - 2026-09-20

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-2b8be5c42c69-0"></a>

Current status: the approved opt-in input guard is implemented and directly offline checked;
quality_first_1 still has no successful live acquisition/generation acceptance. The following
96k implementation checkpoint remains historical. Earlier conservative normal-RAG live evidence
is unchanged. This is not a production SLA, universal input guarantee, benchmark or re-freeze.

<a id="b-2b8be5c42c69-1"></a>

Only the selected quality YAML input cap changed from96,000 to160,000; the shared schema's
permitted maximum was extended, while its default remains96,000. Output remains16,384 including
reasoning; framing2,048 is included once. No serializer, prompt, evidence projection, model,
retry, provider budget, timeout, capacity, product default or SQL/storage change occurred.
Direct config/preflight/actual-SDK MockTransport/trace/session tests:103 passed in35.76s.
Ruff and diff checks passed. The preceding complete run remains911 passed,9 skipped,1 failed,
followed by the documented affected-module fixes; no full-suite rerun or retroactive green claim.

<a id="b-2b8be5c42c69-2"></a>

| Unchanged payload | Engineering tokens including framing | New headroom |
|---|---:|---:|
| Saved real K8 |22,458|137,542|
| Synthetic3-day K12/P6 |43,057|116,943|
| Synthetic10-day K16/P8 |80,643|79,357|
| Same legal long-text K16/P8 |103,429|56,571|

<a id="b-2b8be5c42c69-3"></a>

All four prompt hashes and counts match the preserved96k measurements; no content reduction.
The previous long fixture passes this cap; an over160k input still fails before dispatch.
Actual configured deployment is gpt-5.6-luna, Responses/v1, zero retries. The official model page
lists1,050,000 context and128,000 maximum output, with no apparent public-spec conflict;
private deployment limits are not independently established. No paid long-context probe occurred.
Source: https://developers.openai.com/api/docs/models/gpt-5.6-luna

<a id="b-2b8be5c42c69-4"></a>

Frozen request: Tokyo, Japan;2026-09-21 through23;3 travelers;whole-trip180000 JPY.
Reference date2026-09-20 (Sydney). Exact additional preferences:
`I definitely want to visit Meiji Jingu. I prefer small museums and places with distinctive local architecture.`
Input/output planning_request_2/itinerary_2. Expected normal C48/G24/sends32/K12/P6;
REQUIRED-adjusted values were never reached. Effective config SHA-256:
`aec5fb5d2b07dffb486b0d8211ae4b339bf6006af980a2cd1ede47f85746d722`.

<a id="m-13b018ea95f7"></a>
## Actual failed execution and boundary deviation

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Historical quality_first_1 160k guard and blocked acceptance attempt - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-13b018ea95f7-0"></a>

Actual run_v1 and run_v2 were each invoked once using existing AcceptanceSession and independent
runner request caches. V1 failed after0.309s and V2 after0.048s, both in preference interpretation,
before any HTTP send. The temporary execution-only provider observer replaced the global
httpx.AsyncClient class with a function. Installed OpenAI's httpx2 compatibility code calls
`isinstance(value, module.AsyncClient)` and raised TypeError. This was caused by the acceptance
invocation instrumentation, not by the user's input, the model,160k or the acquisition policy.
No permanent harness or production change introduced this wrapper; the process and patch ended.
The103 passing tests did not exercise that temporary live invocation wrapper.

<a id="b-13b018ea95f7-1"></a>

The existing classifier labeled the wrapped TypeError content_or_business_failure; consequently
the orchestration incorrectly continued to V2 after a shared-client fault. This violated the
requested shared-fault stop boundary. Original classification/error artifacts are retained;
postmortem.json separately corrects the interpretation. Do not rewrite V2 as not attempted.
No repair-and-rerun or replacement sample was performed. Both allowed runner attempts are over.

<a id="b-13b018ea95f7-2"></a>

Each case prepared one Requirement model invocation but recorded zero HTTP sends/responses.
All Google/tool counters are zero; no RuntimeRetrieval instance was created, no SQL or embedding
was run, and no new query vector exists. Provider token usage is unavailable (no response),
not a successful zero-token response. There is no itinerary/reference output to display.
Discovery/admission/cache reuse/ordinary acquisition/comparison/supply/source adoption/Routes/
Reviews/generation/Nearby and their timings are NOT REACHED, not successful empty results.
No new paid provider requests were sent. Disk capture errors zero; both traces persisted;
owned session closed once and HTTP client closed; frozen implementation hashes stayed unchanged.

<a id="b-13b018ea95f7-3"></a>

Artifacts: ignored logs/quality_first_1_live_20260920 contains preserved96k YAML/measurements,
160k measurements, offline test output, frozen manifest and implementation/prompt/schema/config/
corpus-space-policy identities, both original captures/failures, postmortem and closure summary.

<a id="b-13b018ea95f7-4"></a>

Decision: do not close quality_first_1 live acceptance. Next proposed bounded work is to remove
class-replacing execution observation, use hooks on owned client instances or a module-local
transport observation seam, and offline-test the exact acceptance invocation against the
installed SDK MockTransport, including shared wrapped-TypeError stop-before-V2. Do not adjust
production policy or budgets. A new bounded live attempt requires separate approval; none is
started here. No successful three-day or ten-day/long-context live claim is supported.

<a id="m-e2a7f5a4bbc3"></a>
## Approved quality_first_1 coordinated development policy - 2026-09-20

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-e2a7f5a4bbc3-0"></a>

Historical pre-live status: approved/implemented with offline evidence at that time. Current accepted recovery and closeout appear above.
Q1-Q8 retain the approved design rationale and baseline-to-new comparisons. Implementation
and actual validation evidence are recorded at the end of Q8. Earlier proposal wording is
superseded by the user's implementation authorization and its precise send-ledger constraints.
Default product selection is unchanged. The historical96k overflow below is superseded only by the approved160k guard; no successful quality_first_1 live acceptance is claimed.

<a id="m-5b62807df6e5"></a>
## Q1. Quantities, policy identity, and configuration ownership

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-5b62807df6e5-0"></a>

Keep four separate concepts in configuration, trace, CLI, and acceptance reports:

<a id="b-5b62807df6e5-1"></a>

- Capacity: maximum distinct canonical identities admitted/compared (C) or supplied (K).
- Normal target: new qualified identities obtained by ordinary Details sends (G); K is also
  the normal supply target. Targets are attempted when resources/candidates permit, not promises.
- Hard work/time ceilings: actual HTTP sends, matrix elements, phase deadlines, tokens.
- Actual usage: what this request did, including cache reuse, failed sends, qualified successes,
  omitted candidates, remaining budget, and a deterministic stop reason.

<a id="b-5b62807df6e5-2"></a>

Implemented policy identifier quality_first_1 is separate from planning_request_2/itinerary_2,
identity, corpus, embedding space, and retrieval mechanism versions. Those contracts remain.
The number in a budget is not a desired API spend and the user's trip Money never controls it.
Raising G WILL increase normal paid work on sufficiently rich inputs. Increased candidate
count or RAG adoption is not itself demonstrated quality improvement.

<a id="b-5b62807df6e5-3"></a>

Implemented configuration approach: keep one RuntimeConfig schema and one shared
algorithm. Extend existing load_runtime_config_file/path selection with an explicit optional
runtime_config argument at the V1/V2 runner boundary and --runtime-config at CLI. Supply one
validated effective immutable object to budgets, capacity calculation, graph, model adapter,
Web and RAG factories; do not allow a selected profile to fall back to a global singleton.
Use an opt-in config/runtime_quality_first_1.yaml, initially leaving config/runtime.yaml as
the historical conservative default. This is one complete non-secret policy snapshot using
an existing loader, not an inheritance/profile registry. Assert unchanged fields against the
baseline to detect drift. No engine default change. Old code/behavior was recoverable then
from a preimplementation checkpoint, since deleted by user authorization; old numeric snapshots
alone must not be claimed to
reproduce the superseded early-Details gating algorithm. Do not maintain two acquisition
algorithms merely to reproduce history. An allowlisted code snapshot was authorized and created without a commit.

<a id="b-5b62807df6e5-4"></a>

Existing config/v2_development_override.json remains the historical SQL60/RAG180 override.
Do not apply it on top of quality_first_1 and silently reduce 360 to180: reject that combination.
Log selected path, policy ID, config hash, formula inputs, required expansion, effective
limits and actual usage. The 600-second wrapper is an explicit development execution setting,
not a production SLA. V0 does not acquire tools or inherit these V1/V2 acquisition changes.

<a id="m-62a7bb0d7285"></a>
## Q2. Current to proposed settings and absolute boundaries

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-62a7bb0d7285-0"></a>

Locations: YAML = config/runtime*.yaml; CAP = policies/poi_capacity.py;
BUD = runtime/budget.py + budget_limits.py + config_models.py;
RAG = versions/v2/config.py + policies/tripworld_query_plan.py + services/tripworld_discovery.py;
GEN = versions/v1/graph.py + llm/azure_foundry/client.py.
The new column is implemented only when quality_first_1 is explicitly selected; the baseline column is historical.

<a id="b-62a7bb0d7285-1"></a>

| Quantity | Baseline | Approved opt-in | Kind | Location / protection |
|---|---|---|---|---|
| K | min(16,2D+2), three-day8 | min(16,max(8,2D+6)), three-day12 | supply target/cap | versioned CAP formula; absolute16 |
| C | max(20,2*r_pool), YAML36/hard40 | max(48,4K), three-day48 | shared admission/comparison cap | YAML/CAP/BUD; absolute64 |
| G | r_pool=max(10,K+2), cached results consume pool | 2K new qualified successes, three-day24 | normal target | YAML/CAP; absolute32 |
| Ordinary Details sends |18, hard20 | G+8, three-day32 | sends cap including failures | YAML/CAP/BUD; absolute40 |
| Reviews/Profile | three-day3; configured/hard6 | P=min(8,ceil(K/2)), three-day6 | eligible places and sends/model caps | CAP/BUD; all three absolute8 |
| Destination search |1 |1 | send cap | unchanged YAML/BUD |
| Main candidate search |12, page20 |12, page20, no pagination | send/result cap | unchanged YAML/provider DTO |
| RAG query texts |2 |4 | query cap | RAG; range1..4 |
| Query embedding |1 batch |1 batch | actual batch cap | RAG/runtime; remains single batch |
| Top-K / positions |10 /20 |20 /80 | result/processing caps | RAG; Top-K1..20; positions<=80 |
| New resolution attempts |6 |16 | attempted entity cap | RAG; 0..16, failures count |
| RAG Details sends |8 |20 | actual sends cap | RAG; 0..20 |
| RAG fallback sends |2 |4 | actual sends cap | RAG; 0..4; one fallback/entity; page3 |
| Query text/token bounds |200 chars/512 each/1024 total |200/512/2048 | resource caps | query planner; no added raw request embedding |
| Baseline Routes |64/batch,256/run,4 calls |unchanged | sends/elements caps | YAML/BUD/chunking |
| Alternative Routes |8 pairs/8 calls |16 pairs/16 calls | work caps | YAML/BUD; calls hard cap must move8->16 |
| Alternative billable elements |charged through pair count |explicit effective cap16; absolute safety ceiling32 | work cap | BUD + acquisition atomic charges |
| Web tasks / page fetches |6/6 |8/8 | request/task caps | YAML; retain existing hard20/internal limits |
| Weather |2 calls |unchanged | request cap | YAML |
| Nearby |3 calls,10 results,3 final,800m,300m reuse,10s/4s |unchanged | independent caps | YAML; no reference quota per main POI |
| SQL / RAG phase |3/30 default;60/180 opt-in |60/360 for this profile | time caps | RAG; bounded numeric ranges up to60/360 |
| Embed/connect/RAG Google |8/2/4 seconds |unchanged | time caps | RAG |
| Ordinary Details stage |no explicit stage deadline |120 seconds proposed, per send min(20,remaining) | time cap | shared acquisition config, V1/V2 |
| Development whole request |360 last validation |600 seconds | outer time cap | explicit development wrapper/config |
| Main generation input |no explicit token preflight |96,000 engineering tokens | safety ceiling | YAML main-generation section / GEN |
| Main generation output |no explicit project cap |16,384 inclusive of reasoning | API cap | YAML / GEN, not evaluator config |
| Retries |0 |0 | control policy | unchanged |

<a id="b-62a7bb0d7285-2"></a>

The new ordinary Details deadline120 is an additional approval item, not a measured optimum:
it gives one explicit bound to the proposed stop rule without changing the generic20-second
transport default. Cache checks/normalization are inside this stage. No background work
survives timeout; retain qualified partial results and required diagnostics. The outer600
can still stop the whole request. RAG360 + Details120 does not reserve guaranteed time for
all later providers/models; upper bounds do not imply all stages can consume their maxima.
Do not silently add a second whole-run retry or reduce model/provider timeouts.

<a id="b-62a7bb0d7285-3"></a>

Cross-field validation must fail contradictory config rather than silently min-clipping:
C<=64; G<=C; K<=G<=C; main_sends>=G and <=40; P<=K and <=8; all review counters>=P;
query_count*TopK<=position_cap<=80; query_token_total<=2048; maximum actual query SQL count4;
4*512<=2048; required max16; K*K<=baseline256 and computed block count<=4;
alternative pairs<=16, calls<=16, billable elements<=32, and configured effective element
cap supports one direction per selected pair. Fixed mechanism versions/retry0 remain typed;
tunable quantities use bounded integers, not Literal(6), Literal(10), etc.

<a id="b-62a7bb0d7285-4"></a>

Other hidden caps to update together: search(...,10), rows[:10], range(10), query planner2,
TripWorldOrigin.rank<=10 ->20, PlaceSelectionInput.discovery_origins max20 ->80 (deduplicated
entity/query provenance within80 visited positions). Retain real Google ranks and corpus
cosines in separate ledgers. Provider fallback page3 and Google page20 remain unchanged.
Do not modify database search_query SQL or runtime vector space/filter semantics.

<a id="m-32c4add94e80"></a>
## Q3. Effective values for every supported duration

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-32c4add94e80-0"></a>

Values before a REQUIRED expansion; ordinary/new Details and RAG incremental Details remain
separate counters. The last column excludes Reviews requests.

<a id="b-32c4add94e80-1"></a>

| Days | C | G | Ordinary sends | K | P | V2 ordinary+RAG Details ceiling |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 48 | 16 | 24 | 8 | 4 | 44 |
| 2 | 48 | 20 | 28 | 10 | 5 | 48 |
| 3 | 48 | 24 | 32 | 12 | 6 | 52 |
| 4 | 56 | 28 | 36 | 14 | 7 | 56 |
| 5 | 64 | 32 | 40 | 16 | 8 | 60 |
| 6 | 64 | 32 | 40 | 16 | 8 | 60 |
| 7 | 64 | 32 | 40 | 16 | 8 | 60 |
| 8 | 64 | 32 | 40 | 16 | 8 | 60 |
| 9 | 64 | 32 | 40 | 16 | 8 | 60 |
| 10 | 64 | 32 | 40 | 16 | 8 | 60 |

<a id="b-32c4add94e80-2"></a>

Let R be the unique feasible resolved REQUIRED count. R>16 remains an explicit capacity
conflict, never a silent drop. If R<=16, K_effective=max(K_normal,R); recompute C/G/sends/P
from K_effective with the same formulas and boundaries (C<=64,G<=32,sends<=40,P<=8).
Log normal and expanded values separately. REQUIRED gets first acquisition/supply positions
and counts in every shared identity set. Cached REQUIRED does not consume new-success G.
Unresolved identity/ineligible/unavailable REQUIRED retains existing explicit handling; do
not equate ordinary target shortfall with an invalid request or hard conflict.

<a id="m-fa5d7091bcd9"></a>
## Q4. Shared opportunities and early Details policy revision

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-fa5d7091bcd9-0"></a>

Code audit: V2 extend runs before shared eligibility/admission, not after Google consumes
admission slots. admission_order starts REQUIRED, round-robins strength/requirement buckets,
then sorts canonical IDs. It does NOT use provider_rank; RAG has provider_rank=None. The
PlaceSelectionInput.discovery_intent_ids property unions Google query hits and RAG query
intent IDs. Links survive. Missing subject balancing at admission and early ID ties are real
limitations; generic claims of Google-first reservation or discarded RAG links are unsupported.
The shared enrichment loop currently walks that order and stops when len(rich)==r_pool.
It does not first sweep successful cached Details. Thus paid RAG evidence can be stranded.

<a id="b-fa5d7091bcd9-1"></a>

Proposed minimal acquisition order: canonical merge; existing cheap factual exclusions;
REQUIRED first; then strength tiers; within a tier round-robin subjects, then linked intents.
Use deduplicated requirement links; one canonical choice consumes one opportunity, removing
that ID from all buckets and crediting one selected bucket. Within an equally entitled bucket
reuse existing typed category-diversity/destination-distance tie concepts, with canonical ID
last. Unknown category receives no invented category; unknown tie information falls through
to deterministic ID. Use only cheap fields common to both sources: no early rating advantage,
cosine/rank conversion, cached-status preference, provider-source quota, or source order.
Fallback/no-positive-link candidates fill remaining positions with the same cheap tie rule.
Trace bucket, tier, tie basis and omitted IDs. This is a small disclosed acquisition-order
revision; it does not claim distance is user willingness or infer semantics from text.
Keep the final select_planning_supply policy otherwise unchanged (including its evidence
relations, rating abstention, diversity and distance ties). No RAG final quota.

<a id="b-fa5d7091bcd9-2"></a>

Admit once up to C from the actual discovered canonical union. No scanning unrelated cache
entries/database entities and no extra discovery to fill C. No admission backfill outside
that bounded processed identity set in this first revision. Sweep all admitted identities
for compatible, successful request-local Details before sending new ordinary requests.
Compatibility requires canonical ID, exact effective field mask and language, same request
lifetime, and valid response/evidence. Re-run normalization, opening-date consistency and the
same factual eligibility predicate. A failed/invalid cached response is not positive evidence;
do not reissue the identical failed or cancelled RAG request in the ordinary queue under a
"retry=0" label. Share attempted/incomplete-key state or an acquisition ledger so absence of
a successful cache entry cannot create a hidden second send. Different approved fallback
requests remain distinct operations, not an identical-request retry.

<a id="b-fa5d7091bcd9-3"></a>

All qualified reused candidates enter comparison, bounded by C, without consuming G or a
new ordinary send. Deduplicate by canonical ID. Process missing compatible evidence using
the same source-neutral opportunity order; ordinary acquisition can include either discovery
source. Count G only on the first qualified identity created by an ACTUAL ordinary send.
Keep ordinary send count separate: failures/ineligible results consume sends but not G.
Budget payer, discovery sources, and evidence source are independent trace dimensions.
This explicitly supersedes the old rule that early Details still competes for r_pool slots.
Already paid evidence earns no final selection bonus. No source gains duplicate rewards from
multiple query hits. Comparison pool<=C; generation receives only final supply<=K_effective.

<a id="m-ea4cd75755e4"></a>
## Q5. Deterministic stop rules (implemented semantics)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ea4cd75755e4-0"></a>

```text
freeze effective policy, input hashes and shared required/excluded identities
Google discovery: execute finite planned searches, within destination1/candidate12/page20
                 do not paginate or create queries to fill a capacity
V2 only:
  plan <=4 unique eligible query texts, or one labelled system default
  embed missing queries in <=1 batch; retrieve each once, TopK<=20
  visit <=80 positions in stable query-round-robin rank order; merge entity origins
  for each unique entity:
    check cancellation and phase deadline
    excluded -> record, skip
    known canonical or verified compatible cached identity -> merge origins, no new attempt
    no attempt budget -> record remaining as unattempted; still allow no-I/O overlap merges
    no applicable send budget -> record budget stop; no unsupported response inference
    otherwise reserve one attempt, resolve under independent send/time caps
    direct Details failure may use ONE allowed fallback(page3), then compatible Details
    failure counts, no repeated identical request, no second retrieval round
  on RAG failure keep prior Google observations and already resolved RAG results

admitted = first C unique cheap-eligible identities under shared opportunity order
comparison = qualified compatible Details for ALL admitted identities, including early RAG
pending = admitted identities without compatible successful or terminal attempted evidence
ordinary_new_successes = 0
for candidate in required-first/shared-opportunity(pending):
  stop on cancellation/deadline, no pending, len(comparison)==C,
          ordinary_new_successes==G, or actual ordinary sends==send_cap
  recheck compatible cache; cache success -> gate/add once; does not consume G
  terminal failed request -> record, skip (no hidden retry)
  otherwise reserve/send once with remaining stage timeout; failures consume send allowance
  normalize/check factual gate; first new qualified canonical -> add and increment G

preserve REQUIRED handling; ordinary shortfall is diagnostic, not clarification
selective Reviews/Profile <=P for relevant evidence on the comparison pool
select up to K_effective from actual comparison pool; never pad/refetch to reach K
Routes/Web/generation see only final supplied identities and associated evidence
validate main itinerary; run unchanged post-itinerary Nearby; never replan to fill references
```

<a id="b-ea4cd75755e4-1"></a>

Reviews are applied to the comparison candidates relevant to typed evidence requests before
final selection, not retroactively to change evidence after final selection. Required-first
review opportunity and subject allocation remain existing policy. Zero relevant requests
means zero Reviews/Profile even if P is large.

<a id="b-ea4cd75755e4-2"></a>

Examples: 15 discovered qualified identities -> at most15 comparison entries, no query loop
for24/48; 24 new successes -> stop at24 sends even with send_cap32; eight failures can consume
replacement allowance, but target achievement is not promised; 16 early qualified Details
plus24 ordinary successes can form40 distinct entries, all within C48; early16 are not promised
12 final positions. A raw union above48 is jointly admitted, never48 Google plus48 RAG.

<a id="m-cbd8ad6a457a"></a>
## Q6. Downstream coherence and payload guard

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-cbd8ad6a457a-0"></a>

Offline call of existing partition_baseline_origins with synthetic identities (no provider):
K8 ->[64]; K10 ->[60,40]; K12 ->[60,60,24]; K14 ->[56,56,56,28];
K16 ->[64,64,64,64]. Each full K*K directed grid, including current diagonal semantics,
has no duplicate pairs. Existing block strategy supports K12/16 without any SQL/route change.
Request count3/4 and total144/256 fit existing ceilings. Charge only cache-miss chunks.

<a id="b-cbd8ad6a457a-1"></a>

Current alternatives collapse a logical pair, request ONE canonical direction, group by
origin, and label reverse estimates as mirrored_reverse_estimate. Therefore16 pairs mean
at most16 billable elements, at most16 sends and up to32 displayed directional entries.
Do not count mirrored estimates as provider-observed/billable. Implemented with this
semantics: configured billable ceiling16, protective ceiling32; no new reverse fetches.
Increasing call cap8->16 requires updating its hard bound. Add explicit element usage/cap
reservation with pair/call counters atomically, not a disconnected report-only number.

<a id="b-cbd8ad6a457a-2"></a>

Keep Web internals, Nearby, Weather, date/input/identity policy unchanged. Reviews cap P must
apply simultaneously to places, Reviews sends and Profile calls; per-place5 reviews/1200chars
remain. Requested evidence may remain unknown; do not spend merely to fill P or Web8.

<a id="b-cbd8ad6a457a-3"></a>

Saved real main payload has8 supplied identities. Local o200k engineering count:19,661 prompt
+749 DTO schema=20,410; provider actually reported20,183 input and1,735 output (741 reasoning
included). These are different counting methods, not a failed equality assertion. There is
NO real K12/K16 full payload in this capture: missing Details/routes/Web must not be fabricated.
Do not linearly extrapolate8->16; routing grows quadratically and date evidence also grows.

<a id="b-cbd8ad6a457a-4"></a>

Approved 96,000 ENGINEERING input ceiling and16,384 max_output_tokens for V1/V2 primary
itinerary only. Count system+user+transport schema and a documented framing reserve before
sending; do not borrow evaluator limits. Implemented reserve2,048 engineering tokens (not a
provider guarantee), so preflight = local content count+2,048 <=96,000. Do not change prompt
meaning, model reasoning effort, Requirement/Profile caps, or V0 behavior in this package.
Overflow -> explicit generation-input-resource error before model send; no silent candidate
removal, new summary model, split generation or automatic lower-K retry. Existing raw capture
and incomplete/identity validation stay intact. No instruction to consume the output budget.

<a id="b-cbd8ad6a457a-5"></a>

The saved SDK response reports gpt-5.6-luna. Official model documentation lists1,050,000 context
and128,000 maximum output; proposed96,000+16,384 is below published model limits. This does
NOT prove an Azure/private deployment quota or actual K16 payload fits. MockTransport must
verify the installed LangChain Responses path emits max_output_tokens=16384 and counts
reasoning within output; later bounded live verifies actual deployment acceptance, without
fallback/retry on rejection. Official sources accessed read-only on2026-09-20:
https://developers.openai.com/api/docs/models/gpt-5.6-luna
https://developers.openai.com/api/docs/guides/reasoning

<a id="b-cbd8ad6a457a-6"></a>

Before implementation acceptance: build explicitly synthetic schema-valid K12/K16 payloads
using current serializers, complete144/256 route grids,10 supported dates and bounded Web8/
Profile8 evidence; measure all sections. Label synthetic facts as fixtures, never actual Tokyo.
Also measure available real captures. Larger legal strings can still exceed96k: the guard is
a resource refusal, not proof every schema-valid payload fits. No context-limit paid probe.

<a id="m-6d76eaad906c"></a>
## Q7. Saved Tokyo evidence and counterfactual limits

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-6d76eaad906c-0"></a>

Read-only analysis artifact: artifacts/diagnostics/candidate_supply/analysis.json; executable analysis
source analyze.py is local/ignored, with no credentials/network/SQL. Saved responses are fed
through the actual Google adapter using an in-memory transport, then the real normalizer and
factual gate. No new Details, retrieval, itinerary or Profile is synthesized.

<a id="b-6d76eaad906c-1"></a>

Current fixed canonical union46; observed valid independent Details15; unobserved Details31.
All six RAG Details share the needed field mask/en language and pass the common factual gate.

<a id="b-6d76eaad906c-2"></a>

| RAG candidate | Old shared order | Old fate | Fixed-union C48/cache-sweep consequence |
|---|---:|---|---|
| Beni Museum |5 |admitted/enriched/supplied/scheduled |still eligible comparison evidence |
| Min-on Music Museum |11 |admitted; r_pool10 stop |cached evidence can enter comparison |
| Wakayama Domain Kii Family Mansion Remains |14 |admitted; r_pool10 stop |cached evidence can enter comparison |
| Remains of Kirishitan Yashiki |22 |C20 admission stop |C48 admits; cached evidence can enter comparison |
| Sannomaru Shozokan |25 |C20 admission stop |C48 admits; cached evidence can enter comparison |
| Fushimi-yagura |38 |C20 admission stop |C48 admits; cached evidence can enter comparison |

<a id="b-6d76eaad906c-3"></a>

This fixed46 set fits48 independently of new tie order. That supports six comparison entries,
not six final selections or scheduled visits. Existing9 ordinary successful Details occurred
LATER in the historical stage; do not relabel them as pre-existing at a fresh run's start to
pretend ordinary G is free. Full saved evidence permits a restricted15-known comparison,
not a complete expanded acquisition evaluation. New TopK20 positions and up to10 additional
resolution attempts have no saved outcomes; do not extrapolate success or quality. No tuned
parameter search or claimed improvement in a generated itinerary was performed.

<a id="m-6f1f84f56685"></a>
## Q8. Costs, implementation files, and acceptance sequence

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-6f1f84f56685-0"></a>

Three-day V1: ordinary target24 successes, sends<=32. V2 adds<=20 identity Details and<=4
fallback searches, so ordinary+RAG Details<=52, excluding<=6 separate Reviews calls. All-day
maximum is40+20=60 Details plus up to8 Reviews. Distinct candidates and sends are different.
With sufficient eligible inputs, ordinary24 and RAG16 attempts are expected to be pursued;
zero retries does not imply low usage. Deadlines/overlap/exhaustion can lower actual counts.
Main candidate search remains12x20, destination1; no discovery refill. Invoice amounts unknown.
V1/V2 use identical shared targets/gates/selection/generation policy; RAG is the V2 increment.
Historical conservative live versus quality_first_1 is confounded by policy changes and must
not be called a formal source-only V1/V2 comparison. Future matched smoke freezes profile and
request while separating acquisition payer, discovery provenance, final supply and schedule.

<a id="b-6f1f84f56685-1"></a>

Implemented responsibility groups:

<a id="b-6f1f84f56685-2"></a>

1. config/runtime_quality_first_1.yaml (new opt-in snapshot); runtime/config_models.py,
   config_loader.py, budget_limits.py, budget.py; policies/poi_capacity.py; versions/v2/config.py.
   One effective config injection through versions/v1/runner.py, graph.py and versions/v2/runner.py;
   existing CLI wrappers/AcceptanceSession accept that same object; no independent loader globals.
2. services/planning_supply_pipeline.py and shared acquisition helpers in semantic_poi_pipeline.py:
   deterministic opportunity ordering + cache sweep + G/send separation. services/evidence_acquisition.py
   exposes compatible cache lookup/send outcome and atomic budget attribution; runtime/cache.py only
   if needed for shared attempted-key ledger. Keep inactive evaluator algorithms otherwise intact.
3. policies/tripworld_query_plan.py; services/tripworld_discovery.py removes literal query/TopK loops,
   handles free reliable cached identity and terminal attempted keys; schemas/tripworld_discovery.py
   rank bound and evidence/selection_models.py provenance bound. RuntimeRetrieval already accepts
   Top-K as argument; retain original SQL builder, storage, embeddings and cancellation semantics.
4. services/evidence_acquisition.py / policies/transport.py / budget records for alternative elements;
   normal ReviewSelectionService can reuse effective limits; route_matrix_chunking.py should need no
   algorithm change. Preserve its complete-grid behavior in focused regression.
5. V1 main-generation graph/client boundary + runtime/token_counting.py reuse for token preflight;
   separate primary-generation settings, unchanged final itinerary schema/prompts. CLI/trace/result
   diagnostics distinguish capacity, normal targets, actual sends/success/reuse, stops and timings.
   Extend schemas/planning_supply_result.py if needed for typed diagnostics, not a new output contract.
6. Existing docs/poi_selection.md, this proposal, PROJECT.md and evolution record updated in this task.
   Old Phase6 records remain historical. The corresponding V2 development event records this new policy separately.

<a id="b-6f1f84f56685-3"></a>

Approved offline verification scope (actual results below):
- all D1..10 formulas, explicit old/new config hashes, injected V1/V2 equal shared policy, V0 no tools;
  no hidden36/40/18/r_pool/rank10/origins20 clipping; invalid cross-field config fails clearly;
- REQUIRED R<=16 expansion, R>16 explicit conflict, ordinary underfill never clarification;
- permutation/source invariance, no provider rank requirement, subject fairness, duplicate origins
  cannot multiply rewards; ID only final tie; no fixed source quota;
- all admitted compatible cache positives gated exactly once regardless old order; stale/mismatched/
  failed/partial/cancelled evidence not accepted/retried; cache doesn't consume G/send; exclusions;
- ordinary24 successes stop despite32 allowance; failure replacement charged; pool C boundary;
  fake-clock120 stage expiry preserves partial results; user cancellation propagates and cleans up;
- RAG4/20/80/16/20/4 and2048tokens; fewer queries not padded; default labelled; one batch; failures count;
  duplicate known/cached identities free; one fallback/entity; no duplicate Details sends;
- K12/16 baseline144/256 complete directed unique pairs within3/4 requests; alternative16 billable
  <=16 under existing direction semantics and<=32 guard, reverse estimates never billed; cached chunks free;
- P synchronization and zero requests when unneeded; Web8 retains internal limits; Nearby unchanged;
- actual installed SDK MockTransport checks primary cap16384,96k preflight/schema overhead, incomplete
  metadata, no retries, V0/Requirement/Profile unaffected; full C never reaches generation payload;
- supply/reference identity ledgers, cost diagnostics and before/after Nearby main invariance;
  focused runtime/acquisition/V1/V2/graph/schema/transport tests, Ruff/diff; a single full backend run
  appropriate for shared acquisition/graph changes, record first outcome and targeted fixes honestly.

<a id="b-6f1f84f56685-4"></a>

Proposed subsequent live, separately approved ONLY after offline checkpoint and payload/capture gates:
one V1 +one V2 fresh run with same complete valid Tokyo request and quality_first_1, existing
AcceptanceSession,600-second cap, no replacements/retries/tuning. Record entire source funnel,
reused evidence versus new G successes/sends, stops, tokens, phase times, real final itinerary and
references. Nonempty RAG adoption is not forced and not a success quota. No Melbourne, extra
embedding/corpus rebuild, failure injection, default engine switch or claimed quality benchmark.

<a id="m-c5f2f83b28f6"></a>
## Q8 implementation checkpoint - 2026-09-20

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-c5f2f83b28f6-0"></a>

Status: **Implemented; offline regression issues corrected with affected-module checks;
not live-validated, not Frozen. A legal long-text payload exceeds the approved input cap.**
Normal RAG already has successful development-live evidence under the older60/180 override;
that is not validation or evidence of quality improvement for this new shared acquisition policy.

<a id="b-c5f2f83b28f6-1"></a>

Implementation uses one RuntimeConfig and one acquisition implementation. Explicit
`--runtime-config config/runtime_quality_first_1.yaml` or the immutable runner object selects
this policy. `--development-timeout-seconds 600` is explicit. Product defaults remain unchanged.
Old numeric values do not restore the superseded algorithm. The source checkpoint available
at implementation time was subsequently deleted and is no longer a restore option.

<a id="b-c5f2f83b28f6-2"></a>

Effective configuration SHA-256:
`edc5d9208e8eb553a81a31481dc7c4dfc632175a749622775684bf5d1e75529c`.
The runner records path/hash and the derived normal/effective capacities plus actual usage.
Conflicting quality-first component overrides and historical60/180 stacking are rejected.

<a id="b-c5f2f83b28f6-3"></a>

Implemented flow: canonical union -> source-neutral admission -> ALL admitted compatible
Details checked/normalized/gated -> ordinary new-success acquisition -> selective Reviews/Profile
-> unchanged final deterministic supply -> downstream evidence/main generation -> unchanged Nearby.
Cached qualified candidates consume neither G nor ordinary sends and receive no selection bonus.
G counts first newly qualified canonical identities from ordinary sends. Failed/ineligible sends
consume only sends. Stops: G, queue exhaustion, C, send budget, deadline or cancellation.
Pre-send dependency/budget failure is not a place failure or terminal key. Production Places
transport marks/charges immediately before its one send; fake providers use their invocation
as the simulated boundary. Failed/incomplete sent keys prevent hidden same-key repeats.
Acquisition order is REQUIRED, strength, subject round-robin, intent round-robin, cheap category
spread/destination distance, canonical ID. No rank/cosine/cache/source reward or RAG quota.

<a id="b-c5f2f83b28f6-4"></a>

K=min(16,max(8,2D+6)); C=max(48,4K); G=2K; ordinary sends=G+8; P=min(8,ceil(K/2)).
REQUIRED<=16 extends K and dependent limits; >16 clarifies. Ordinary underfill does not clarify.
Normal/effective supply are separately reported. Review places/sends/Profile all receive P;
without typed evidence requests they remain zero. Web tasks/pages8/8. No refill discoveries.
RAG4queries/one embedding batch/TopK20/80positions/16newattempts/20Details/4fallback;
200characters/512tokens each,2048total; fewer valid queries are not padded. Existing default,
identity,15km/1km bounds, original SQL, corpus/vector space and zero retries remain unchanged.
SQL60/RAG360; embedding/connect/Google8/2/4. Ordinary Details120-second stage includes cache
and normalization, each request<=min(20,remaining); outer600 explicitly selected. These are
engineering development ceilings, not latency targets or a guarantee that all stages fit.
Baseline Routes64 per batch/256 total/4calls. Alternatives16pairs/16calls/16billable elements
(absolute guard32); actual origin*destination charges are atomic. Reverse estimates are not
billable. Weather/Nearby/input/identity/required semantics and primary prompts remain unchanged.

<a id="b-c5f2f83b28f6-5"></a>

Primary V1/V2 generation has96,000 engineering input and16,384 output including reasoning.
Preflight counts system+user+current transport DTO schema+2,048 framing reserve. Installed SDK
MockTransport verifies the actual output parameter through AcceptanceSession. Requirement,
Profile,V0 and reasoning effort are unchanged. Overflow stops before generation without
truncation, summary models or lower-K retries. Only final supply enters this model payload.

<a id="m-7796a96fbdb8"></a>
## Checkpoint and recovery scope

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20 / Q8 implementation checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-7796a96fbdb8-0"></a>

`logs/source_snapshots/pre_quality_first_1_20260919T202927Z/` contained the317-file allowlisted
source/config/test/harness/doc snapshot and manifest with Git HEAD/status/11 existing deletions.
Final audit found four static TripWorld JSON policy/manifests omitted by the initial whitelist;
`supplement/` preserved them separately, byte-identical to the prior snapshot at that time.
The original317 files, supplement and manifest were created for development protection, then
deleted by user authorization on 2026-09-20. They cannot now restore uncommitted intermediate
states. They never included environments, credentials, datasets, vectors or a DB backup;
ignored captures and local thesis notes are separate from these deleted recovery materials.

<a id="m-e7f463f475ec"></a>
## Actual offline validation

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20 / Q8 implementation checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-e7f463f475ec-0"></a>

- One complete backend execution: **911 passed,9 skipped,1 failed**,18.45seconds.
- Failure: new numeric token-budget keys were redacted, breaking saved effective config.
  Fixed by exact nonnegative-integer allowlisting; credential strings remain redacted.
  Affected observability/runtime/quality/V1/V2 runner checks: **86 passed**.
- Final normal/effective REQUIRED-capacity reporting correction: **51 passed** in affected
  quality/supply modules. Do not rewrite the first complete run as green; no second full run.
- Earlier focused broad check:275 passed/1 failed (nested new wall-clock telemetry was not
  excluded by a determinism assertion), followed by43 affected passes. Another focused check
  had122 passes. Counts overlap and are not independent additive totals. No added skips/xfails
  or deleted tests. Logs preserve intermediate outcomes.
- Ruff and final diff/artifact checks are recorded in the task manifest. Tests use fake
  providers/DB and MockTransport; no paid/live calls or actual DB retrieval in this task.

<a id="b-e7f463f475ec-1"></a>

Final capture audit: the primary-only generation config is serialized to JSON for development
artifacts while the original immutable object still reaches the model adapter. This closes a
capture-only type-serialization gap found by inspection; disk-backed SDK MockTransport capture
has no capture errors. The added20-Details/four-fallback fixture initially omitted its required
provider_rank field (58 passes/1 fixture failure); corrected fixture and capture/quality modules:
**59 passed**. No additional full suite. Final Ruff (`backend scripts`) and `git diff --check`
passed. No live or real database calls were used to validate capture.

<a id="m-3db21c3b4b46"></a>
## Real serializer/tokenizer sizing

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20 / Q8 implementation checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-3db21c3b4b46-0"></a>

Artifacts: `artifacts/diagnostics/candidate_supply/payload_sizing.json` and reusable
`scripts/measure_quality_first_payload.py`. Synthetic fixtures are schema-validated, have
complete directed routes,16 billable plus16 mirrored alternative entries,8 Web tasks/pages,
and P6/P8 profiles projected before final supply. They are not Tokyo observations or a
universal maximum. Diagnostic section counts are non-additive. No provider usage is inferred.

<a id="b-3db21c3b4b46-1"></a>

| Case | System | User | Schema | Framing | Total | Headroom | Outcome |
|---|---:|---:|---:|---:|---:|---:|---|
| Saved real K8 |962|18699|749|2048|22458|73542|Within cap|
| Synthetic3-day K12/P6 |962|39298|749|2048|43057|52943|Within cap|
| Synthetic10-day K16/P8 |962|76884|749|2048|80643|15357|Within cap|
| Synthetic legal long-text K16/P8 |962|99670|749|2048|103429|-7429|Explicit resource overflow|

<a id="b-3db21c3b4b46-2"></a>

The long fixture uses24,000 preference characters/3,601 actual tokens,24 semantic requirements,
24 evidence requests,256 baseline cells and48 accepted synthetic Web facts. It meets input and
domain bounds but exceeds96k by7,429. This is a remaining supported-input resource limitation,
not proof that every K16 input fails. No cap increase or prompt compaction was performed.
Increasing G may increase actual paid work: three-day V2<=32 ordinary+20 incremental Details,
excluding<=6 Reviews; these are sends, not52 unique POIs and not an invoice estimate.

<a id="m-1ab5169ba6b5"></a>
## Changed responsibilities and next boundary

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Approved quality_first_1 coordinated development policy - 2026-09-20 / Q8 implementation checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-1ab5169ba6b5-0"></a>

- Config/limits/capacity: runtime models/loader/budget/limits, quality YAML, poi_capacity, V2 config.
- Acquisition: candidate_details, acquisition_opportunities, common/planning supply pipelines,
  evidence_acquisition, RequestCache, dispatch marker and Places/HTTP adapter send observation.
- RAG: query planner/discovery/rank and provenance bounds; original SQL/runtime DB code unchanged.
- Injection/model: V1 runner/graph, V2 runner, primary generation resource guard/Foundry client,
  AcceptanceSession forwarding and exact numeric trace allowlist.
- Direct tests, existing Q1-Q8/PROJECT/current POI/evolution and V2-05 development event updated.

<a id="b-1ab5169ba6b5-1"></a>

Next decision is acceptance of this offline checkpoint with the explicit long-input limitation.
A separately approved bounded live may use at most one V1 and one V2 fresh run with the SAME
complete Tokyo request,quality_first_1 and existing AcceptanceSession,600-second cap. Freeze
dates/hashes/capture readiness first; record source funnel, cache/new-success/send counters,
actual supply/schedule/Nearby, tokens and stage time. No replacement samples, forced RAG
adoption, tuning or supplemental queries. Development smoke only, not a benchmark.
No live/paid provider/real SQL, storage/index/vector change, frontend/default switch, B2 deletion,
stage/commit/push, re-freeze or V3. TOAST/I/O variance and Melbourne ambiguity remain pending.

<a id="m-1a07353c5289"></a>
## POI Selection Evolution: QCGRE, B1, B2

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-2bacb856e39c"></a>
## Accepted baseline closeout - 2026-09-20

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2bacb856e39c-0"></a>

The user accepted quality_first_1 as implemented + bounded development-live-validated, not
benchmark/all-branch acceptance or V1/V2 re-freeze. No more budget/selection tuning or Tokyo
repetition is authorized. Current executable source matches the recovery manifest; saving it
must include the new160k YAML and repaired AcceptanceSession, not only the older source snapshot.
Current CLI/config/API gaps,finite prioritized issues,exact179-path three-commit proposal and
Git-versus-local archive boundary are in docs/tripworld_phase6_proposal.md; commands in README.md.
The product/developer APIs remain V0-only; V1/V2 run independently via CLI/Python. Frontend
budget remains optional despite the backend mandatory contract. No executable-code/config changes or tests were run
for this closeout. Suggested next work after Git saving: saved-capture Weather404 diagnosis.
Everything below is dated implementation/history evidence; its old 'Proposed',design-only or
not-yet-live language must not override this accepted current status.

<a id="b-2bacb856e39c-1"></a>

Canonical decision history, updated 2026-09-20. This is engineering/development history,
not a formal benchmark, thesis conclusion or claim of empirical B2 superiority.
Current runtime specification: [POI selection](development_record.md). Historical dates and
acceptance are preserved; V1 is reopened and **not re-frozen**. TripWorld Phases 1-5
remain accepted. Phase 6 runtime is implemented and full regression passed; normal RAG
has bounded development-live evidence under the explicit 60/180-second override.
This is not a production SLA or re-freeze. V3 remains unimplemented.

<a id="m-e4cce0f09d09"></a>
## Current quality_first_1 recovery checkpoint - 2026-09-20

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e4cce0f09d09-0"></a>

Implemented + bounded development-live-validated after explicit user authorization to recover
from the preceding pre-send observer failure. Only opt-in input guard160k/output16384;
product defaults and acquisition/SQL budgets unchanged. Development observer now preserves
global HTTP types; wrapped TypeError stops following cases.62 affected checks passed; earlier
103 checks overlap. Full history911 passed/9 skipped/1 failed remains unchanged, with documented
focused fixes and no rerun. Original failed attempts remain below as historical records.

<a id="b-e4cce0f09d09-1"></a>

Same Tokyo Sep21-23/3 travelers/180000 JPY request: V1 completed42.045s,V2 completed106.414s.
V1:40 admitted,0 cache,24 new successes/24 sends,24 compared,12 supplied,8 scheduled.
V2:48 admitted,15 cache plus24 new successes/24 sends,39 compared,12 supplied,8 scheduled;
4 RAG-only supplied and2 scheduled (ESP MUSEUM/Min-on Music Museum). One additional resolved
RAG place was outside admission. Both REQUIRED visits scheduled;3 independent Nearby references
each,primary business fields unchanged. Google sends42/61; no Reviews/Profile triggered.
V2 normal exact SQL returned20+20 hits,16 direct resolutions,1 embedding HTTP; no retry.
Weather404,unknown costs,visitor suitability/same-building references and SQL variance remain.
Recommendation: close bounded development acceptance; not a benchmark, ten-day live proof,
production SLA or re-freeze. Exact evidence and usage are in the existing Phase6 recovery section.
Artifacts: ignored logs/quality_first_1_live_20260920/recovery. No additional live is started.

<a id="m-36db51cc7ad8"></a>
## Historical quality_first_1 96k implementation checkpoint - 2026-09-20

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-36db51cc7ad8-0"></a>

Implemented as an explicit opt-in shared V1/V2 acquisition policy; product defaults unchanged.
For D days: K=min(16,max(8,2D+6)), C=max(48,4K), G=2K, ordinary sends<=G+8,
P=min(8,ceil(K/2)); REQUIRED extends effective values up to16. All admitted compatible Details
are checked first without spending G; new qualified sends then pursue G within send/deadline
limits. Acquisition uses source-neutral subject/intent opportunities; final deterministic supply
is unchanged. Reviews/Profile precede final supply. No new selection LLM or RAG quota.

<a id="b-36db51cc7ad8-1"></a>

Opt-in RAG4/20/80/16/20/4,SQL60/RAG360; ordinary Details120s,per-send20s; explicit outer600s.
Baseline Routes64/256/4; alternatives16 billable elements; Web8/8; Weather/Nearby unchanged.
Primary V1/V2 generation96k input/16,384 output; full effective config/usage are traceable.
Normal RAG's earlier60/180 live evidence does not validate this new policy or prove better quality.
New G may increase actual paid work. This policy has NOT run live and is NOT Frozen.

<a id="b-36db51cc7ad8-2"></a>

One complete backend run:911 passed,9 skipped,1 failed (numeric config redaction); corrected
and86 affected checks passed. Final normal/effective capacity diagnostics:51 affected passes.
Disk-backed capture serialization and final quality checks:59 passed; Ruff/diff checks passed.
No repeat full suite or retrospective all-green claim. K8/K12/K16 engineering sizing:
22,458/43,057/80,643 tokens including framing; a schema-valid long K16 input reaches103,429
and is explicitly blocked by96k. This supported-input resource limitation remains unresolved;
no cap increase, truncation or automatic retry. See existing Phase6 Q8 for exact evidence.

<a id="b-36db51cc7ad8-3"></a>

Historical source checkpoint (deleted on 2026-09-20): logs/source_snapshots/pre_quality_first_1_20260919T202927Z
(317 original files, plus4 separately verified unchanged static policy/manifests; HEAD/status
and11 prior deletions). Old numeric values alone do not recreate the old acquisition algorithm.
Captures/thesis notes remain ignored in place. No paid/live/real DB work, SQL/storage/vector
change, frontend/default switch, B2 cleanup, stage/commit/push or re-freeze. TOAST/I/O and
Melbourne ambiguity remain separate. Next bounded V1/V2 live requires separate approval.

<a id="m-0cfe133a7980"></a>
## Historical quality_first_1 proposal - 2026-09-20 (superseded by approval)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-0cfe133a7980-0"></a>

A coordinated opt-in shared V1/V2 acquisition policy is proposed in the existing Phase6
proposal (Q1-Q8). It separates C admission/comparison capacity, G ordinary new-success target,
K supply target and actual send/time limits, and revises early Details reuse without changing
identity, SQL, vector storage, final selection architecture or Nearby. Three-day proposal:
C48/G24/K12, ordinary sends32, reviews6; V2 incremental attempts16/Details20/fallback4.
No values are implemented or approved by this document. Current conservative defaults and
explicit SQL60/RAG180 development override remain active/available as before.

<a id="b-0cfe133a7980-1"></a>

Saved Tokyo analysis:46 canonical candidates,15 observed Details,31 unobserved. All six RAG
Details pass the existing common factual gate; C48 and a complete admitted-cache sweep would
make them comparable in that fixed set, not guarantee final adoption. Existing baseline Routes
supports K12/16 with144/256 unique elements in3/4 chunks. Alternatives currently bill one
direction per logical pair;16 pairs mean at most16 billable elements, not32 reverse observations.
Proposed120-second ordinary acquisition stage and generation96k/16384 guards need approval.
Only existing docs and ignored offline analysis updated; no production/test/fixture change,
SQL, paid call, full suite, stage/commit/push, re-freeze or future-version implementation.

<a id="m-3e60cb9d7939"></a>
## Bounded live checkpoint: upstream failures (2026-09-19)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-3e60cb9d7939-0"></a>

Exactly one B and one A were run after the offline checks above. Both stopped before
Google destination/discovery, so downstream supply and itinerary behavior remain
**not live validated**. There was no retry, policy tuning or post-generation repair.

<a id="b-3e60cb9d7939-1"></a>

| Observation | B | A |
| --- | --- | --- |
| Failure | canonical invalid_subject_ids | InterpretationDraft intent_id length >40 |
| Requirement LLM seconds | 10.362 | 9.937 |
| End-to-end failed-run seconds | 10.564 | 10.148 |
| Model calls | 1 Requirement | 1 Requirement |
| Input / output / total tokens | 3201 / 1174 / 4375 | 3238 / 1258 / 4496 |
| Google / Web / Page calls | 0 / 0 / 0 | 0 / 0 / 0 |
| Evaluator / subset enumerator calls | 0 / 0 | 0 / 0 |

<a id="b-3e60cb9d7939-2"></a>

B returned nonempty subject_refs but illegally redeclared the implicit party inside
custom subjects. It also identified requesting_traveler, a required Opera House,
less walking, crowd avoidance, family friendliness, and unusual local culture; walking,
crowding and family directional targets were valid. The canonical contract correctly
rejected the reserved subject ID instead of silently fixing it. No canonical REQUIRED
ledger or candidate pool was produced.

<a id="b-3e60cb9d7939-3"></a>

A failed on discovery_intents.0.intent_id =
discovery_distinctive_architectural_cultural (44 characters, maximum 40).
This was not the earlier empty-subject_refs error. No validated extraction survived;
the instrumentation did not retain the complete invalid DTO, so father/mother/party
attribution cannot be claimed verified from this run.

<a id="b-3e60cb9d7939-4"></a>

For both: observations/canonical/admitted/Details/enriched counts are zero because
acquisition never started. Planning supply, required/optional pool sizes, actual unique
scheduled POIs, unused options, route matrix size, Profile/selection/itinerary timings
and itinerary-quality observations are **not available**, not successful zero-sized
outputs. Weather, Profile and itinerary calls are zero. No required-presence, optional
usage, repetition, density, unsupported-claim or route-use outcome can be evaluated.
Combined measured model usage: 6439 input +2432 output =8871 tokens, including1032
reasoning output tokens. No evaluator cost was incurred, but failed early exits are
not evidence of faster successful planning.

<a id="b-3e60cb9d7939-5"></a>

Recommendation: keep the implemented supply direction and pause before cleanup/final
V1 review. A narrow Requirement transport/domain alignment pass is needed for reserved
subject identities and short temporary IDs, followed only by separately authorized
bounded live validation. Do not change supply coefficients or restore B2 because the
runs never reached selection. This task's live authorization is exhausted. V1 remains
reopened; B2 code is retained. No V2/V3, refreeze, DB/embedding work, commit or push.

<a id="m-070191c38618"></a>
## 2026-09-19: systematic Requirement-boundary reliability pass

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-070191c38618-0"></a>

Status: **Implemented and offline validated; not live validated or frozen**. The user
superseded the preceding narrow-fix recommendation with a systematic draft/canonical
boundary audit. The B/A failures above remain historical failures; neither reached
discovery or evaluated the deterministic supply path.

<a id="b-070191c38618-1"></a>

Root cause was mixed ownership: model-generated temporary bookkeeping was subjected
to canonical ID rules, while the protocol both implicitly owned party and allowed
custom subject definitions. Validator patches could reject outputs but could not
remove these avoidable representation ambiguities. The implemented v2 requirement
contract separates semantic drafts from application-owned canonical identity:

<a id="b-070191c38618-2"></a>

- Remove discovery intent IDs and unreferenced named keys from model output.
- Keep only bounded opaque semantic/subject handles required for internal links.
- Allocate canonical IDs after exact namespace/reference validation and stable ordering.
- Represent party, specified people/subgroups and unresolved attribution explicitly.
- Preserve source-grounded text, negation, conditions, strengths and named meanings;
  no truncation, fuzzy link repair, identifier semantics or extra LLM is used.
- Keep local bounds/source/evidence validation distinct from provider JSON structure.
- Separate invalid contracts and provider/config/transport errors from clarification.
- Add opt-in, default-off sanitized completed-response capture before DTO mapping.

<a id="b-070191c38618-3"></a>

Actual SDK parsing with MockTransport exercises final wire schema, DTO, draft,
canonicalization and downstream projections. The final affected run passed 262 tests;
the complete backend suite ran once and passed 711, with 9 opt-in PostgreSQL skips.
Ruff and git diff --check passed. Metamorphic tests cover consistent handle renaming,
1/44/100/256-character lengths, permutations, idempotence and preserved attribution;
rejection tests cover dangling/duplicate/missing/null/contradictory contracts.

<a id="b-070191c38618-4"></a>

The saved B parsed-domain draft is labeled as such and explicitly re-expressed in a
test fixture. A's full failed response remains unavailable; synthetic long-handle tests
are not faithful replay. Directional Profile tests are synthetic; the old B supply
snapshot's UNKNOWN directions are not retroactively filled in.

<a id="b-070191c38618-5"></a>

Nine frozen Requirement-only live cases/checks are prepared but unexecuted. The proposed
next boundary is separately authorized extraction-only acceptance, at most one call per
case and no retries or Google/Routes/itinerary spend. This checkpoint made no live or paid
calls. It leaves supply ranking/capacity/budgets/cache, HARD/UNKNOWN policy, Review/Profile,
V0 and TripWorld unchanged, retains inactive B2, and performs no commit/push or re-freeze.
Full ownership and capture details live in the existing docs/poi_selection.md, with an
implementation entry in docs/v1_selector_implementation.md. No thesis archive was changed.

<a id="m-d93c52e87f98"></a>
## 2026-09-19: limited Requirement-only live attempt stopped at transport

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-d93c52e87f98-0"></a>

Status: **Transport-blocked, not live validated**. The nine previously prepared requests,
semantic checks and expected outcomes were frozen in an ignored manifest before execution
(SHA256 70e8d211825b05f6d79f50e866bfafffa95851576312f0c7aa45212e67caf438).
Expected outcomes: seven canonical extractions, one genuine clarification, one unsupported-HARD
clarification. Planned languages: seven English, one Spanish, one German; no Chinese case.

<a id="b-d93c52e87f98-1"></a>

The first case, solo_requester (Kyoto), made one configured gpt-5.6-luna client invocation
and one HTTP attempt through the production Requirement node, then raised OpenAIConnectionError
at transport after 0.453 seconds. No completed response, returned model ID, usage, draft or
canonical object exists. Provider/schema acceptance and server-side inference/billing are
unknown. DTO, provenance, semantic fidelity, attribution and links were not evaluated.
No successful or incorrect clarification can be inferred. Eight cases remained unexecuted.
The matrix stopped without retries, repairs, replacement samples or production tuning.

<a id="b-d93c52e87f98-2"></a>

An import-path harness error occurred before freezing/network execution, was corrected,
and a fake production-node dry-check passed. It is separate from the live transport failure.
All downstream Google/Review/Profile/Evaluator/Weather/Routes/Web/Itinerary calls were zero.
No production logic/config, supply, HARD, V0 or TripWorld change was made. No complete backend
rerun, B2 cleanup, V2/V3 work, re-freeze, commit or push. Only artifact/document checks followed.

<a id="b-d93c52e87f98-3"></a>

The full frozen requests, per-layer results and artifact hashes are recorded in the existing
current document docs/poi_selection.md. Ignored artifacts: logs/requirement_live_20260919/.
An explicitly authorized development archive event V1A-19 preserves this attempt; no formal
benchmark or research conclusion is claimed. Recommendation: resolve transport access under
separate authorization before another Requirement acceptance attempt or full-trip spend.
This observation does not establish a new contract defect or semantic product limitation.

<a id="m-9004f60b2951"></a>
## Network-authorized Requirement continuation (2026-09-19)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-9004f60b2951-0"></a>

Status: **Limited provider/contract evidence; semantic limitations remain**. The user
explicitly authorized the configured Azure endpoint and fees. The original manifest
70e8d211825b05f6d79f50e866bfafffa95851576312f0c7aa45212e67caf438 stayed unchanged.

<a id="b-9004f60b2951-1"></a>

Keep segments separate: the original restricted attempt had one connection failure.
The authorized continuation first completed solo_requester, then whole_party failed before
HTTP because the harness closed a shared cached HTTP client. An offline reproduction
confirmed the lifecycle cause. No whole_party retry occurred. Only the seven untouched
cases then ran with harness-only per-case hook removal and end-of-matrix client close.
No production prompt, schema, canonicalizer, policy or configuration changed.

<a id="b-9004f60b2951-2"></a>

Current authorization totals: 9 client invocations, 8 HTTP requests, 8 completed responses.
All eight accepted the actual wire schema and passed DTO/reference/source/domain checks;
no invalid-model-contract rejection. This is not a semantic success rate. Kyoto and Lisboa
were incorrectly also marked REQUIRED named visits. Lisbon's avoidance became HARD and
triggered unexpected clarification against the frozen expectation. The missing-information
case correctly clarified destination/dates but attributed ambiguous She to sister and
inferred two travelers. Other inspected cases preserved distinct people, subgroups, shared
preferences, German required/excluded names, and explicit no-stairs HARD clarification.
Quiet was not mapped to crowding; accessibility did not certify stairs. No live walking
versus hiking direction contrast was covered. whole_party remained provider-untested.

<a id="b-9004f60b2951-3"></a>

Completed usage: 28077 input + 6406 output = 34483 tokens; 3873 reasoning tokens are already
included in output. Cache read 24094; SDK cache creation 3959, with no billing inference.
Completed latency median 8.2185s, range 4.454-14.360s. Actual languages: English 6, Spanish 1,
German 1; no Chinese. No SLA, formal benchmark or general semantic-accuracy conclusion.

<a id="b-9004f60b2951-4"></a>

All downstream providers and Review/Profile/Evaluator/Itinerary LLM calls were zero.
Private ignored raw responses, draft/canonical objects and hashes remain under
logs/requirement_live_20260919_network_authorized/ and logs/requirement_live_20260919_remaining/.
The existing current document contains per-layer/per-case findings; the authorized V1A-19
archive event preserves this continuation without rewriting the earlier transport stop.
Only artifact/document checks were run, not the complete backend suite. No production logic,
V0/TripWorld, supply/HARD change, B2 cleanup, V2/V3, re-freeze, commit or push.

<a id="b-9004f60b2951-5"></a>

Recommendation: a semantic/product decision remains around destination vs named visit,
negative preference strength and genuinely ambiguous attribution. Do not mask these with
keyword validators or silently weaken HARD. No next implementation or full-trip test is
started; the missing whole-party case must not be presented as tested.

<a id="m-68619d3a907b"></a>
## 2026-09-19: bounded Requirement semantics alignment

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-68619d3a907b-0"></a>

Status: **Implemented, offline validated, bounded live inspected; one material outcome
mismatch remains.** Original evidence audit distinguishes errors from ambiguity: Kyoto/
Lisboa scope was wrongly duplicated as required visits; original Spanish "Preferimos sitios
locales, no atracciones artificiales" admits a preference or exclusion reading, so its
normal-only expectation was over-specific. A separate audit-expectation v2 preserves that
qualification without relabeling or re-running the old result. Ambiguous She and inferred
party size lacked grounding.

<a id="b-68619d3a907b-1"></a>

Policy defined before editing: destination vs actual visit intent; polarity independent of
non-negotiable strength; mentioned person vs traveler vs owner vs total count. Existing
fields suffice. V1 prompt version 3 adds 397 system tokens, context-based contrasts and
source guidance; schema/output/config remain fixed. Client change is diagnostic prompt
version only. Source checks remain text integrity, not semantic entailment.

<a id="b-68619d3a907b-2"></a>

The new development harness owns one shared SDK client for the matrix, removes each request
hook and closes once. MockTransport tests cover sequential reuse, middle invalid response,
unique capture, no overwrite, distinct invocation/HTTP/completed counts and shared failure
stop. Historical harness failures stay separate; no production client ownership was altered.
Offline: 13 new tests, affected 275 passed, full backend once 724 passed/9 PostgreSQL skips;
Ruff/diff passed. Fake-output tests establish representation/program behavior, not language.

<a id="b-68619d3a907b-3"></a>

Frozen ten-case manifest f4f4658da71384504165af569860dbc0d6a674c5d8eb3c580f8da88673e5c956:
four contrast pairs plus whole_party and held-out combination; Chinese 4, English 3, Spanish
2, German 1. Exactly 10 client/HTTP calls and 10 completed responses, no retry/repair/tuning.
All DTO/draft checks passed. Eight canonical outputs validated; two extraction-issue cases
stopped before canonical release. Explicit HARD correctly clarified after canonicalization.
Destination/area, soft/HARD, clear/ambiguous owner and complete count behaved as expected;
whole_party and German hope-to-visit/explicit exclusion were preserved.

<a id="b-68619d3a907b-4"></a>

Remaining material mismatch: the incomplete-count case correctly emitted null count but
also an extraction issue, triggering clarification although total count is optional under
current mandatory destination/date policy. Frozen expectation was normal release with null;
it remains a failed application expectation, not a fabricated count or malformed contract.
Do not repair or rerun it in this pass. Other wording/SOFT-level differences were noncritical.
Review is qualitative development/model-assisted inspection, not independent human annotation.

<a id="b-68619d3a907b-5"></a>

Usage: 39056 input + 4986 output = 44042 tokens; 3000 reasoning already included in output.
Cache read 34551; SDK cache creation 4475. Median elapsed 5.500s, range 4.438-8.891s, with
no SLA or cross-matrix speed claim. Private artifacts/hashes: logs/requirement_semantics_20260919/.
All downstream providers and Review/Profile/Evaluator/Itinerary calls zero. Supply/budgets,
HARD release, V0 and TripWorld unchanged; no B2 cleanup, V2/V3, freeze, commit or push.
Recommendation: decide optional uncertainty versus blocking extraction issues narrowly before
end-to-end acceptance; do not redesign selection or start another live tuning loop.

<a id="m-32a5fafda908"></a>
## Shared structured-input migration - 2026-09-19 (Implemented, offline checkpoint)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-32a5fafda908-0"></a>

After the Requirement-only development observations, the user specified mandatory form
fields and optional preference text. An initial V1-only migration proposal retained old
V0 extraction and proposed changing product dispatch. That proposal was superseded before
implementation: the approved migration shares input/semantics across V0 and V1 and keeps
product dispatch on V0. V0 remains LLM-only; V1 retains evidence and deterministic supply.
The change removes operational re-extraction and treats empty preference as normal. It
preserves old measurements as historical, not acceptance evidence for the revised boundary.
No B2 removal, live calls, formal comparison, V2/V3 runtime or re-freeze occurred.

<a id="b-32a5fafda908-1"></a>

Offline validation: affected 657 passed; final focused 56 passed; complete backend once
769 passed, 9 skipped (opt-in PostgreSQL tests). Ruff and diff checks passed.

<a id="m-ce4bbd1754c1"></a>
## 2026-09-19: shared-input bounded live acceptance (partial, harness-blocked)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ce4bbd1754c1-0"></a>

Status: attempted, NOT accepted as complete. This is development evidence, not a formal
comparison or a new freeze. Production sources, prompts, schemas, models, budgets and
supply policy stayed fixed. No failed case was repeated or replaced.

<a id="m-a4c4fc5bf5ba"></a>
## Frozen manifest and dispatch

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: shared-input bounded live acceptance (partial, harness-blocked). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a4c4fc5bf5ba-0"></a>

Reference date 2026-09-19; Sydney, Australia; 2026-09-21 through 2026-09-23;
three travelers; total-trip budget 1800.00 AUD. E uses empty additional_preferences.
P uses exactly: "I definitely want to visit the Sydney Opera House. I prefer distinctive
local places rather than tourist traps. My mother prefers less walking."
HARD uses exactly: "Absolutely no stairs."

<a id="b-a4c4fc5bf5ba-1"></a>

The five ordered cases were V0-E, V1-E, V0-P, V1-P, and shared HARD interpretation/readiness.
Paired requests were identical. Actual run_v0/run_v1 entry points were invoked; HARD called
the shared interpreter only. Contract versions: planning_request_2,
interpreted_requirements_3, preference_prompt_4, preference_draft_3. The unchanged client
configuration still reports the stale diagnostic contract label requirement_draft_2;
it is not the actual wire schema. Model deployment: gpt-5.6-luna; configured retries: zero.
Frozen canonical-JSON manifest SHA256:
1fe61be61421f29376e5fd0e282922f764aa19189bd59d06ffdf3700d21de64b.
Exact inputs, expectation/configuration/source hashes and wire schema are privately retained
under logs/shared_input_acceptance_20260919_8e48/.

<a id="b-a4c4fc5bf5ba-2"></a>

| Case | Outcome | Total seconds | Scope established |
| --- | --- | ---: | --- |
| V0-E | Completed | 14.329 | Empty semantics, preserved form, plain generation |
| V1-E | Generation transport failure | 10.187 | Empty semantics, discovery/supply/evidence completed |
| V0-P | Interpretation transport failure before HTTP | 0.266 | Constructed interpretation request only |
| V1-P | Interpretation transport failure before HTTP | 0.062 | Constructed interpretation request only |
| HARD | Interpretation transport failure before HTTP | 0.063 | No readiness outcome established |

<a id="b-a4c4fc5bf5ba-3"></a>

Five scenarios entered, one completed, four failed; zero entirely unattempted scenarios.
Failed timings are time to failure. V1-E generation completion, both P interpretations and
all their downstream stages, and HARD semantic/readiness validation remain unexecuted.
The two P model-input records differ only by call_id: system/user prompts, schema and
configuration match. This establishes constructed input parity, NOT live semantic fidelity.
Both E canonical records preserve form facts, use skipped_empty, and contain no invented
preferences. Default V1 discovery queries are system behavior, not user interests.

<a id="m-408424809491"></a>
## Harness defects and evidence limitations

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: shared-input bounded live acceptance (partial, harness-blocked). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-408424809491-0"></a>

The observer created separate model instances but closed the first instance's underlying
async client after V0-E. LangChain caches that transport across identical configurations;
later instances reused a closed transport. Offline diagnosis confirmed identical client
identity and that closing the first also closes the second. This is a harness lifecycle
error, not evidence of a production requirement/selection failure. The stop guard failed
to classify the SDK transport_failure as shared infrastructure failure and incorrectly
entered three more scenarios. Those calls failed before network submission. No retry or
mid-matrix fix followed. This procedural failure prevents complete acceptance.

<a id="b-408424809491-1"></a>

The HTTP interceptor targeted httpx, while the installed model SDK sends through httpx2.
Consequently the successful V0 generation has model-level input/output but no captured
provider usage/raw HTTP response. Its HTTP attempts were not independently counted;
zero intercepted model requests MUST NOT be reported as zero model use. Token input,
output/reasoning/cache usage and monetary cost are unavailable, not zero. Google HTTP
capture worked. A pre-call hash-guard issue caused by redacting the token_counting.py
path key was corrected before any scenario/network call, with an additive recovery record
and full unredacted source hashes; frozen inputs and expectations were unchanged.

<a id="m-975fa44e2f80"></a>
## V1-E candidate supply and external accounting

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: shared-input bounded live acceptance (partial, harness-blocked). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-975fa44e2f80-0"></a>

57 observations -> 52 unique canonical candidates -> 20 admitted -> 10 Details attempts /
10 successes -> 10 factually eligible enriched -> 8 supply candidates (0 REQUIRED,
8 OPTIONAL). Capacity was eight and shortfall zero. All eight selection steps were
eligible_fill; empty preferences did not stop supply early. Profiles were absent, with
empty evidence relations rather than negative observations. Existing factual gates and
budgets ran unchanged, but REQUIRED protection, soft-conflict priority and evidence-linked
Review direction were not substantively exercised by this empty case.

<a id="b-975fa44e2f80-1"></a>

The options, in policy order, were Sydney Opera House, Sydney Harbour Bridge,
Chau Chak Wing Museum, Hyde Park, Clam Bar, Museum of Contemporary Art Australia,
The Oriana Sydney, and Luna Park Sydney. The actual constructed planner input includes
planning_supply_1, explicit required_canonical_ids=[], eight optional IDs, current evidence,
and instructions that UNKNOWN is neither failure nor satisfaction and options are not
mandatory visits. It was constructed but the model never received this V1 payload.
Unused optional candidates and actual V1 scheduling therefore cannot be assessed.

<a id="b-975fa44e2f80-2"></a>

Captured Google requests: destination search 1; named search 0; discovery 3; Details 10
(no cache reuse: ten acquisitions produced ten HTTP requests); Reviews 0; Weather 1;
Routes 7; Web/page operations 0. All 22 HTTP responses were 200. Routes submitted one
8x8 baseline matrix (64 elements including diagonal) plus six one-pair alternatives
(6 elements): 70 submitted matrix elements total, not seven billable elements. This is
work-unit accounting, not a bill estimate. No forced Web or Review task was added.
V0 external acquisition was zero; failed P/HARD cases acquired nothing.

<a id="b-975fa44e2f80-3"></a>

Model task invocations: preference interpretation 3 attempted / 0 completed responses;
itinerary generation 2 attempted / 1 completed response; Review/Profile, Semantic
Evaluator and Official Web reasoning all zero. Subset enumeration was also zero.
The four unsuccessful model invocations failed before HTTP; the one completed generation
is known model use even though raw transport/usage capture missed it.

<a id="b-975fa44e2f80-4"></a>

V1-E observed stage seconds: destination 0.625; discovery 1.797; ten Details total 3.156;
policy selection 0.000154 (wrapper 0.015); Weather 1.281; Routes 3.172; Web integration
0.031 with zero external operations; failed generation approximately 0.016. Supply pipeline
4.968 includes discovery/Details/selection and must not be added to them again. Empty
interpretation/preflight timers rounded to zero. V0-E generation took 13.453 seconds;
total 14.329 includes setup/trace overhead. No successful V1 latency comparison is possible.

<a id="m-f4df9b7220cc"></a>
## Actually generated itinerary and quality inspection

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: shared-input bounded live acceptance (partial, harness-blocked). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f4df9b7220cc-0"></a>

Only V0-E generated an itinerary, preserving the submitted dates and operational facts.
Day 1: The Rocks and Circular Quay; Museum of Contemporary Art Australia;
Sydney Opera House and Royal Botanic Garden; Circular Quay dinner.
Day 2: Bondi Beach to Coogee Beach; Coogee Beach lunch; Art Gallery of New South Wales;
Surry Hills dinner.
Day 3: Darling Harbour; Australian National Maritime Museum; Darling Harbour lunch;
Barangaroo Reserve; Barangaroo dinner.

<a id="b-f4df9b7220cc-1"></a>

There are 13 activity rows and 12 distinct exact place_name strings. Darling Harbour
repeats within day 3; no exact name repeats across days. Several entries are compound
areas/routes rather than individual canonical POIs, so 12 is not a verified Google-ID
count. Adjacent areas also overlap. No REQUIRED visit was requested in E; required-place
coverage is not exercised, even though the Opera House appears voluntarily.
Inter-activity gaps range from zero to 90 minutes; no obvious whole-day vacancy is visible.
Day 1 lunch is not explicitly scheduled. These observations do not establish travel-time
feasibility or candidate starvation. The model estimated 600 AUD across activity rows,
not a complete accommodation/transport/meal budget. Museum zero-price assumptions,
opening compatibility (including the gallery ending at 18:00) and sunset labeling have
no current external verification. No supplied weather/routes/opening evidence existed in
V0, and V1 did not generate; evidence use by a successful V1 itinerary is untested.

<a id="m-fff0f086fd10"></a>
## Disposition and boundaries

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: shared-input bounded live acceptance (partial, harness-blocked). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-fff0f086fd10-0"></a>

A specific shared-boundary acceptance harness defect remains (client ownership,
shared-failure stopping and transport/usage accounting). Recommend an OFFLINE harness
repair/verification pass, followed only by separate authorization for further live work.
Do not declare backend ready for final frontend alignment/review on this matrix alone.
No production prompt/schema/model/budget/policy adjustment is justified by these failures.

<a id="b-fff0f086fd10-1"></a>

Frontend budget and developer UI remain unaligned; /api/planning still defaults to V0.
No V2/RAG integration, V3 validation/repair, B2 cleanup or re-freeze occurred. The earlier
769-pass/9-skip offline checkpoint remains historical and was not rerun. This task only
adds ignored observation artifacts and documentation, including the authorized development
archive event. No commit/push or additional live scenario followed diagnosis.

<a id="m-590df98f9424"></a>
## 2026-09-19: acceptance harness reliability (implemented, offline validated)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-590df98f9424-0"></a>

The previous shared-input matrix remains a FAILED ACCEPTANCE RUN with useful partial
evidence. This follow-up changes development harnesses/tests/documentation only. No live
model/provider calls, scenario reruns, prompt/schema/configuration changes, policy changes,
provider budget/cache changes, dependency changes, cleanup, freeze, commit or push occurred.

<a id="m-9bece22deb48"></a>
## Root cause and actual stack

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: acceptance harness reliability (implemented, offline validated). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-9bece22deb48-0"></a>

Original construction: ignored acceptance.py -> create_foundry_client ->
AzureFoundryStructuredLLMClient -> ChatOpenAI -> root_async_client (AsyncOpenAI) ->
LangChain _AsyncHttpxClientWrapper -> httpx2.AsyncClient. Each case constructed a new
wrapper, but langchain_openai.chat_models._client_utils._cached_async_httpx_client uses
lru_cache keyed by endpoint/timeout/socket options. The case-finally call to
await client._chat_model.root_async_client.close() closed the transport reused by later
wrappers. Offline reproduction uses two actual project factories, confirms alias identity,
closes the first, then observes the second's local closed-client failure. No request can
escape the network blocker. The shared stop guard misclassified this wrapped transport
failure and the legacy httpx monkeypatch missed model HTTPX2 traffic.

<a id="b-9bece22deb48-1"></a>

Installed AND uv.lock versions: openai 3.13.0, langchain-openai 1.6.2,
langchain-core 1.6.2, httpx2 2.12.0, httpx 0.28.1. Google remains on legacy httpx.
Previous Requirement-only tests injected one legacy-httpx mock into one SDK instance.
They checked sequential case reuse but not repeated factory construction, cached aliases,
the actual HTTPX2 family, or the separate disposable shared-input harness. A passing test
of that older runner did not establish safety for the subsequently introduced harness.

<a id="b-9bece22deb48-2"></a>

Official references consulted: [OpenAI SDK documentation](https://developers.openai.com/api/docs/libraries),
[SDK resource ownership and HTTP configuration](https://github.com/openai/openai-python),
and [LangChain ChatOpenAI response metadata](https://docs.langchain.com/oss/python/integrations/chat/openai).
Current SDK documentation names HTTPX2 and DefaultAsyncHttpx2Client; the installed
DefaultAsyncHttpxClient compatibility export also derives from HTTPX2. Older httpx-only
examples are not a transport-family guarantee. Current upstream documentation describes
some custom-hook exceptions propagating directly, while this installed SDK wraps the
observed closed-client RuntimeError in APIConnectionError; local source/tests govern the
classification here. No dependency upgrade was needed.

<a id="m-3fdbca00482e"></a>
## Session ownership and observation contract

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: acceptance harness reliability (implemented, offline validated). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-3fdbca00482e-0"></a>

scripts/requirement_acceptance.py is the single reusable frozen runner for shared
interpretation and explicit run_v0/run_v1 cases. scripts/acceptance_session.py contains
small development-only ownership/observer helpers. Cases remain plain manifest data;
production provider objects are explicit borrowed injections for V1. The CLI remains
suitable for shared interpretation; V1 workflows supply providers through run_matrix's
programmatic interface, rather than constructing another disposable execution loop.

<a id="b-3fdbca00482e-1"></a>

An owned session constructs fresh sync/async OpenAI default HTTP clients within its
running event loop. A synchronous scoped constructor adapter passes these through
ChatOpenAI's supported http_client/http_async_client arguments while invoking the real
project factory. This bypasses SDK-wrapper default caches without changing or clearing
production caches. No production injection seam was added. This adapter is for sequential,
single-thread development execution, not a concurrent production service facility.

<a id="b-3fdbca00482e-2"></a>

The session holds strong references to the domain client, ChatOpenAI, SDK and transports.
Cases never close them. Shutdown removes only its hooks/callback/instance observer and
closes owned transports once, including setup failure, case failure and cancellation.
Externally supplied clients are explicitly borrowed and never closed. Sessions cannot be
re-entered or used across event loops. A new owned session never receives the previous
session's transport. SDK cleanup of an injected transport is not treated as independent
ownership; only the outer session releases it. No close suppression or automatic recovery
exists. Separate HTTP observers attach to actual injected clients, supporting both Google
httpx and model httpx2 without replacing global send methods.

<a id="b-3fdbca00482e-3"></a>

Each model method invocation has a unique call ID and separate invocation, HTTP-send,
HTTP-response, SDK-response, domain-mapping and scenario status. A temporary instance-level
SDK _process_response adapter observes already-buffered non-streaming JSON before SDK/domain
parsing; it does not consume streaming responses or alter their parsing. LangChain
on_llm_end independently retains AIMessage usage_metadata/response_metadata before business
conversion. Request IDs, response IDs, model, status, refusal/incomplete data and raw
response diagnostics remain available even if parsing/mapping subsequently fails.

<a id="b-3fdbca00482e-4"></a>

Accounting uses SDK usage once per (call, send attempt, response ID). Repeated SDK
observations deduplicate; LangChain/HTTP records corroborate and are never summed again.
Distinct attempts remain distinct. Absent usage is None, not zero; explicit zero remains
zero. Reasoning/cache detail fields are retained inside the original provider usage object,
not added to output/input totals. A response timeout is not proof of zero charge.

<a id="b-3fdbca00482e-5"></a>

The SDK adapter accesses a private method and is deliberately version-sensitive and
covered against the installed stack. Streaming usage recovery is not implemented; this
checkpoint covers the current non-streaming planning/interpretation path only. Dependency
upgrades require revalidating this adapter before another live acceptance run.

<a id="b-3fdbca00482e-6"></a>

Local readiness checks precede every case, including V1-E before any provider acquisition.
Closed/replaced transports, loop mismatch, shared configuration/authentication failures,
or unhealthy essential capture prevent further dispatch. Wrapped provider/network failures
stop the remaining dependent matrix conservatively. Content/domain failures can continue
with healthy resources; legitimate HARD clarification is a business result and does not
break the session. No paid readiness probe or retry/reconstruction is introduced.

<a id="b-3fdbca00482e-7"></a>

Diagnostic writes are best-effort for the current application result. Failure is retained
separately in capture health; subsequent cases become unexecuted, never retried. Artifacts
use unique session/case/call IDs and exclusive writes. Frozen manifest/source/configuration
checks and a spent-matrix marker prevent rerunning a spent matrix. Runtime raw artifacts
remain ignored and known credentials are redacted. Historical captures were not edited.

<a id="m-55fc427236fc"></a>
## Offline validation and limits

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: acceptance harness reliability (implemented, offline validated). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-55fc427236fc-0"></a>

Focused harness: 24 tests passed. Focused harness plus affected SDK client, Requirement
boundary and V1 itinerary mapping regression: 98 passed. Changed-file Ruff and diff checks
passed. The full backend suite was not rerun. Socket/DNS guards prevent external network;
only Windows asyncio's internal wakeup socket pair is allowed. Model responses use actual
HTTPX2 MockTransport and installed SDK/LangChain serialization/parsing. Real run_v0/run_v1
are exercised; Google acquisition uses existing deterministic provider fixtures.

<a id="b-55fc427236fc-1"></a>

The five-case V0-E -> V1-E -> V0-P -> V1-P -> HARD sequence runs twice in one process,
repeated three times: six complete mocked matrices, 30 case outcomes, 42 model HTTP sends.
Each matrix has four completed fixture itineraries and one expected HARD clarification;
seven distinct responses total 280 fixture tokens (30 input + 10 output per response).
Reasoning 4 is included in the 10 output and cache-read 5 in the 30 input, not extra usage.
All owned transports close once, each second session has new transport identity, and
case cleanup does not close the next case's client. Additional tests cover:

<a id="b-55fc427236fc-2"></a>

- original cached-factory failure reproduction and cross-loop rejection;
- closed model client preventing V1 provider acquisition;
- content failure followed by a healthy case and HARD followed by another case;
- exception/cancellation cleanup and borrowed resource/hook preservation;
- malformed JSON and valid DTO followed by domain failure retaining usage;
- missing usage, explicit zero, deduplication and distinct attempts;
- refusal/incomplete response diagnostics;
- capture on/off yielding identical model requests, semantic/application results and
  provider request sequence after excluding diagnostic timings/IDs;
- file-write None/exception preserving the successful result and stopping later cases;
- spent-matrix rejection, immutable artifacts and unique response call IDs;
- both actual HTTP families and wrapped 401/503 stopping without retries.

<a id="b-55fc427236fc-3"></a>

Fixtures establish harness mechanics, not real-model preference fidelity, itinerary
quality or global provider reliability. Simplified fixture itineraries are intentionally
not travel-quality acceptance evidence. The prior live run is not relabeled after these
fixes. Its V0-E usage remains unavailable, V1-E retains 22 Google requests / 70 submitted
route elements / eight optional candidates with unsent generation, and P/P/HARD remain
pre-send failures. No timings are combined across runs.

<a id="m-cff3b29f4967"></a>
## Proposed minimum live resumption (NOT executed or authorized here)

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19: acceptance harness reliability (implemented, offline validated). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-cff3b29f4967-0"></a>

Saved V1-E model input contains the full system prompt (4067 characters), full user prompt
(69072 characters), V1Itinerary schema identifier, deployment/default parameters and config
identity. Both prompts/schema identifier match the independent generation-request trace
exactly. The original monitored production source/config hashes still match, including
Foundry DTO/mapping and generation binding; dependency versions are unchanged. These are
sufficient to invoke the same application generation boundary using saved evidence after
separate approval and a fresh integrity/configuration check. No prompt is reconstructed
from prose. Raw model HTTP bytes were never captured, so do not claim byte-for-byte wire
replay. Preserve the historical dates/evidence explicitly, not as newly acquired current
facts; endpoint credentials must be supplied securely without changing the recorded model.

<a id="b-cff3b29f4967-1"></a>

Propose one saved-evidence V1-E generation-only invocation, plus new narrowly bounded
V0-P, V1-P and shared HARD executions. Freeze a new manifest with dates supported at that
execution time for the new executions. The ordinary P cases each need interpretation and,
if released, generation; V1-P may additionally need authorized Reviews/Profile/Web under
existing budgets. Thus this is not simply four model calls. Do not rerun V0-E for usage.

<a id="b-cff3b29f4967-2"></a>

One fresh complete V1 run is still needed; V1-P can satisfy that requirement if it reaches
successful generation through the full production path, avoiding a redundant extra run.
The saved-evidence continuation validates only generation against stored input. Its latency
must remain separate from the old acquisition latency. No automatic resumption is added.

<a id="b-cff3b29f4967-3"></a>

Current product limitations persist: frontend budget/developer UI mismatch, V0 default
product dispatch, no V2/RAG runtime, no V3 validation/repair, no B2 deletion and no re-freeze.

<a id="m-96a7a4d38e94"></a>
## 2026-09-19 - Limited shared-input live recovery (development evidence)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-d0f0f7145570"></a>
## Authorization, manifest and integrity

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Limited shared-input live recovery (development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-d0f0f7145570-0"></a>

This is a separately authorized development recovery, not a formal benchmark or version
freeze. Previous FAILED ACCEPTANCE RUN artifacts remain untouched under
logs/shared_input_acceptance_20260919_8e48/. New private, ignored artifacts are under
logs/shared_input_recovery_20260919_a17e/: recovery_manifest.json, its digest, fresh manifest,
capture, V1_P_traces and analysis.json. The four-case manifest was frozen before any call;
its canonical SHA-256 is fc21b246e1b7905e844ffba98c769bb2828d9d1eb3812dcb8861453217bbefa4.

<a id="b-d0f0f7145570-1"></a>

Execution order and actual outcomes:

<a id="b-d0f0f7145570-2"></a>

| Case | Boundary | Outcome | Seconds | Model invocations |
| --- | --- | --- | ---: | ---: |
| V1_E_SAVED | V1 generation adapter, saved evidence only | Completed | 19.204 | 1 |
| V0_P | Actual run_v0 | Completed | 25.688 | 2 |
| V1_P | Actual run_v1 | Completed | 47.672 | 5 |
| HARD | Shared interpretation/readiness only | Unexpected clarification: extraction_ambiguity | 5.312 | 1 |

<a id="b-d0f0f7145570-3"></a>

All four were executed once. Three itineraries completed; zero expected-code HARD outcomes,
one unexpected clarification, zero transport failures and zero unexecuted cases. No manual
or SDK retry occurred. No fifth scenario, V0-E rerun or post-success fresh V1 run occurred.

<a id="b-d0f0f7145570-4"></a>

Fresh P inputs are identical: Sydney, Australia; 2026-09-21 through 2026-09-23; three
travelers; total budget 1800.00 AUD. The exact preference is:

<a id="b-d0f0f7145570-5"></a>

> I definitely want to visit the Sydney Opera House. I prefer distinctive local places rather than tourist traps. My mother prefers less walking.

<a id="b-d0f0f7145570-6"></a>

HARD uses the same complete form with "Absolutely no stairs." Reference date is 2026-09-19.
Expected outcomes are outside model prompts. Wire contracts are planning_request_2,
interpreted_requirements_3, preference_prompt_4 and preference_draft_3. A legacy diagnostic
requirement_draft_2 label in configuration was not changed and is not the actual wire schema.
Returned model identifier for every response is gpt-5.6-luna.

<a id="b-d0f0f7145570-7"></a>

Preflight verified the original 145 monitored source/configuration hashes, the three
repaired harness/test hashes, installed dependency versions, configuration and open clients.
A local capture write/read probe used no network. Saved system/user prompts matched the
independent original generation trace and current system prompt; V1Itinerary schema and
mapping matched. Saved dates and evidence around 05:39 UTC were retained. No provider
acquisition, interpretation or Profile ran for V1_E_SAVED. Normal generation mapping and
trip-date validation were used; this is generation-only continuation using a saved evidence
snapshot, not a fresh end-to-end run or byte-for-byte HTTP replay. Its duration is not
combined with previous acquisition time. The existing acceptance session owned clients;
fresh cases used the reusable run_matrix. No new harness implementation was introduced.

<a id="m-29aba2f8f0a7"></a>
## Shared semantics and the HARD mismatch

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Limited shared-input live recovery (development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-29aba2f8f0a7-0"></a>

V0-P and V1-P interpretation payloads (system/user/schema) match exactly. Both preserve
Opera House REQUIRED, the requester's distinctive/local preference and the mother's
less-walking preference. Canonical source offsets are 0:50, 51:111 and 112:143 respectively.
Walking evidence direction is LIGHT preferred / HIGH avoided, linked to the mother.
No form mutation, invented HARD promotion, extraction issue or operational conflict occurs
in P. The local preference scope varies (selected_poi_set versus itinerary_style), as do
query phrasings; core meaning survives but fresh outputs are not identical.
V0 generation receives named intent without requiring Google identity. V1 receives the
canonical required ID, seven optional IDs, subjects and semantic requirements through
planning_supply_1. Optional candidates are not all mandatory visits.

<a id="b-29aba2f8f0a7-1"></a>

HARD retains kind=constraint, strength=hard, polarity=avoid, whole_trip scope and the exact
source span. The model marks subject_target unresolved and asks which traveler/subgroup is
covered. canonicalize_requirements stops at extraction_ambiguity before releasing the
canonical contract and before require_resolved_hard. Accessibility is requested in the
draft but no evidence is acquired and no accessibility cue is accepted as no-stairs proof.
Form values remain unchanged; external acquisition and generation are zero.

<a id="b-29aba2f8f0a7-2"></a>

This does not pass the frozen unsupported_hard_requirements expectation. It is also not
proof of prompt disobedience: preference_prompts.py explicitly says never silently replace
missing attribution with party and to retain genuine ambiguity. Clarify the approved
precedence for unqualified whole-trip HARD restrictions, absent subject attribution and
unsupported-HARD readiness. Do not silently default party, weaken HARD, change the frozen
expectation retroactively or reinterpret UNKNOWN as PASS. No fix or replacement sample
was authorized or performed.

<a id="m-2a8cf235bf95"></a>
## Fresh V1 funnel and evidence authority

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Limited shared-input live recovery (development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2a8cf235bf95-0"></a>

41 raw observations (1 named, 20 semantic, 20 default) -> 28 canonical -> 20 admitted ->
10 Details attempts / 10 successes -> 10 eligible -> 8 supplied. Capacity and effective
capacity are both eight; shortfall is zero. Supply keeps the required Opera House and adds
seven discovery opportunities; it does not stop when a preference has a match. Evaluator
calls and minimum-subset enumeration are both zero.

<a id="b-2a8cf235bf95-1"></a>

Three Review acquisitions return five reviews each; three Profile calls follow:

<a id="b-2a8cf235bf95-2"></a>

| POI | Walking signal | Effect |
| --- | --- | --- |
| Opera House | HIGH, medium confidence, review references 1/2 | Conflicts with mother's soft preference; REQUIRED survives |
| Harbour Bridge | LIGHT, medium confidence, references 2/5 | Positive linked evidence relation |
| MCA | Walking dimension absent; visit-duration signal only | Walking remains UNKNOWN |

<a id="b-2a8cf235bf95-3"></a>

Other candidates' unavailable walking evidence remains UNKNOWN, not negative or verified.
Profiles are review-derived judgments, not guaranteed facts or deterministic HARD proof.
Additional Profile dimensions do not become new user requirements.

<a id="m-5ae62f117f30"></a>
## Supply versus actual itineraries

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Limited shared-input live recovery (development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-5ae62f117f30-0"></a>

Output activities have activity IDs, not canonical Place IDs. Counts below use exact-name
matching against supplied canonical records; they are not direct output-ID validation.

<a id="b-5ae62f117f30-1"></a>

Saved V1-E: eight OPTIONAL candidates supplied; fourteen activity rows, seven distinct
matched places scheduled. MCA unused. Chau Chak Wing Museum appears on two separate days
(total five hours); transfers repeating destination names are not extra visits. Multiple
2-3 hour flexible blocks have limited explanation for the empty-preference request.
Available route/weather evidence is used and unknown hours/transit limitations are noted.
The Oriana estimate is 70 AUD from a bounded 20-120 range, not a verified complete trip cost.

<a id="b-5ae62f117f30-2"></a>

V0-P: fifteen activity rows and fourteen unique location strings, including generic cafes,
dining areas and accommodation. These are NOT fourteen confirmed canonical POIs. Opera
House is included. Taxi/seated/short-walk suggestions acknowledge the mother; local areas
reflect semantic judgment without acquired evidence. The repeated generic cafe label does
not establish an actual duplicate venue. "Use a short accessible section" at Wendy Whiteley
Garden lacks verified accessibility evidence. Every activity uses +11:00; local ZoneInfo
Australia/Sydney gives +10:00 on the trip dates. Existing date validation does not validate
destination UTC offsets. No V3 mechanism or correction was added.

<a id="b-5ae62f117f30-3"></a>

Fresh V1-P: eight supplied (one REQUIRED, seven OPTIONAL), seven distinct scheduled
(one required, six optional); Bridge Stairs unused, no repeated place:

<a id="b-5ae62f117f30-4"></a>

| Date | Scheduled places |
| --- | --- |
| 2026-09-21 | Museum of Contemporary Art Australia; The Rocks Self-Guided Walking Tour |
| 2026-09-22 | Sydney Opera House; Royal Botanic Garden Sydney |
| 2026-09-23 | Sydney Harbour Bridge; Cahill Walk Lookout; Pool of Reflection |

<a id="b-5ae62f117f30-5"></a>

MCA is scheduled within supplied Monday hours; the Tuesday closure is avoided. Matched
route examples include MCA -> Rocks 154 m / about 2 min and Opera -> Garden 917 m / about
12 min. Activity offsets are +10:00. All cost estimates are null, so budget feasibility
is not established. Days end around 15:00/16:00 and dining/accommodation detail is absent.
Two visits per day can be consistent with less walking; neither unused optionals nor rest
periods alone prove failure. A two-hour walking-tour slot remains a soft-preference tradeoff,
even with an abbreviation note. Famous attractions dominate, so distinctive/local alignment
is limited. "Quiet reflection" is semantic description, not acquired quietness evidence.
A full supply does not prove itinerary quality or resolve all walking feasibility concerns.

<a id="m-53738e9682db"></a>
## Provider work, usage and latency

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Limited shared-input live recovery (development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-53738e9682db-0"></a>

Fresh V1 alone makes 20 Google requests: destination search 1; named search 1; semantic
search 1; default discovery 1; Details 10 (no cache reuse, all successful); Reviews 3
(no cache hits); Weather 1; Routes 2. Routes submit 65 elements: WALK 8x8=64 including
self-pairs, plus TRANSIT alternative 1x1=1. Web search/page/reasoner operations are zero;
no evidence request was invented to activate Web. Saved replay, V0 and HARD have zero
external acquisition. Google counts come from completed provider exchanges and budget/trace
records; independent raw HTTP status interception was not installed. Request count is not
a billing estimate. Historical failed-run 22 Google / 70 route elements remain separate.

<a id="b-53738e9682db-1"></a>

Nine client invocations, HTTP sends, HTTP responses, SDK responses and successful domain
mappings are recorded. Three interpretations, three Profiles, three generations; zero
Semantic Evaluator or Web reasoner. SDK usage is counted once; repeated layers are not added.

<a id="b-53738e9682db-2"></a>

| Task | Input | Output | Reasoning (inside output) | Cache read | Cache write | Approx. capture seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Saved V1 generation | 20500 | 2391 | 516 | 0 | 20497 | 19.202 |
| V0-P interpretation | 3811 | 613 | 239 | 0 | 3808 | 6.887 |
| V0-P generation | 1531 | 2494 | 448 | 0 | 1528 | 18.732 |
| V1-P interpretation | 3811 | 892 | 515 | 3808 | 0 | 8.925 |
| Opera Profile | 1303 | 238 | 100 | 0 | 1300 | 3.844 |
| Bridge Profile | 986 | 311 | 142 | 0 | 0 | 4.000 |
| MCA Profile | 1379 | 285 | 158 | 0 | 1376 | 3.955 |
| V1-P generation | 18150 | 1764 | 597 | 1249 | 16898 | 17.357 |
| HARD interpretation | 3789 | 414 | 209 | 3672 | 114 | 5.264 |

<a id="b-53738e9682db-3"></a>

Total 55,260 input + 9,402 output = 64,662 tokens. Reasoning 2,924 is already included in
output; cache read 8,729 is included in input; provider-reported cache write 45,521 is not
added to totals. No monetary charge is inferred. No usage field above is missing.

<a id="b-53738e9682db-4"></a>

Scenario durations use runner elapsed timers. Model intervals above are approximate artifact
write-time intervals, not independently measured provider latency. V1 trace stage intervals:
destination 0.503 s; discovery/admission 2.216 s; Weather 1.081 s; Routes 0.729 s;
Web integration (zero work) about 0.022 s; final generation about 17.368 s. Details/review
acquisition and normalization have no separately instrumented complete stage timer; do not
invent exact values or subtract mixed clocks. Deterministic supply reports about 0.199 ms.
Preflight latency is unavailable. run.json context creation precedes V0-P; use V1 run_started
and runner elapsed, not context-created time, for fresh V1 total duration.

<a id="m-21e3758c3b0e"></a>
## Health, changes and recommendation

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Limited shared-input live recovery (development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-21e3758c3b0e-0"></a>

Capture errors are empty and provider trace health is good. No client lifecycle, transport,
usage-loss or mapping failure recurs. Private SDK instrumentation remains version-sensitive
and limited to the tested non-streaming path. One successful bounded run is not a universal
reliability guarantee. Raw captures remain ignored and private; old artifacts are preserved.

<a id="b-21e3758c3b0e-1"></a>

Only existing PROJECT.md, docs/v1_design.md, docs/poi_selection.md,
docs/poi_selection_evolution.md and the explicitly authorized V1A-20 development event are
updated. No production or harness source, prompt, schema, configuration, dependency, budget
or retry setting changed. No tests were rerun during this live task. No frontend change,
engine switch, B2 deletion, V2/V3, embeddings, database rebuild, commit, push or re-freeze.

<a id="b-21e3758c3b0e-2"></a>

Recommendation: a specific business/contract issue remains. Resolve the intended HARD
attribution/readiness precedence in a separately approved scope; do not declare complete
backend acceptance or automatically start another test/fix cycle. Fresh V1-P satisfies the
pending end-to-end execution check. The independent V0 offset/output-quality limitations
also remain recorded. These are development observations, not formal comparative research
conclusions. Stop after reporting and await the user's decision.

<a id="m-913132d00b7d"></a>
## 2026-09-19 - Request-wide versus personal attribution alignment

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-913132d00b7d-0"></a>

Status: implemented prompt-only policy alignment; offline checks passed; two authorized-in-
attachment requirement-only live cases remain unexecuted because automatic approval review
requires direct chat authorization. No new paid call, HTTP send or itinerary execution occurred.
The prior successful ordinary-path recovery and original HARD mismatch remain historical.

<a id="b-913132d00b7d-1"></a>

Root cause: the prompt defined party only as the entire traveling party and said "Never
silently replace missing attribution with party." Combined with required subject_target,
this encouraged treating a direct itinerary condition as missing personal attribution.
The accepted product distinction does not infer a disability: an itinerary must not require
stairs is a request condition, whereas a mother's inability belongs to the mother.

<a id="b-913132d00b7d-2"></a>

Existing fields reused: normalized_text preserves the condition and exceptions; scope
states where it applies; subject_target party denotes request/party applicability, specified
references source-grounded people/subgroups, and unresolved retains genuine ambiguity.
Canonical party remains the implicit subject_refs=(party,) with no fabricated participant
record. Normalized meaning distinguishes applicability from personal attributes; the schema
does not separately type that distinction. Current consumers do not interpret party as a
medical fact. No ontology, schema or extra interpretation layer is needed for this pass.

<a id="b-913132d00b7d-3"></a>

Exact revised prompt attribution block:

<a id="b-913132d00b7d-4"></a>

```text
Every semantic item has one explicit subject_target:
- {"kind":"party"} means applicability to the shared planning request or entire traveling party;
  no subject definition is needed. Request applicability does not assert personal attributes.
- {"kind":"specified","first_ref":"person_handle","additional_refs":[]} identifies one or more
  declared people/subgroups. first_ref is mandatory, not a priority weight. additional_refs may
  name up to seven additional declared subjects. Declare these subjects using local_key, label,
  and source_refs. Their handles have no reserved spellings and are never canonical party IDs.
- {"kind":"unresolved","reason":"..."} means the user's attribution is genuinely unclear.
Distinguish the scope of an itinerary condition from the identity of its experiencer. A direct
request-wide condition may use party without naming a person: "Absolutely no stairs" constrains
the requested itinerary, whereas "My mother absolutely cannot use stairs" belongs to the mother.
This does not infer disability or a limitation shared by all travelers. Preserve explicit
personal/subgroup attribution and exceptions for other travelers. An ambiguous "she" with
multiple plausible antecedents remains unresolved. Do not infer party from HARD strength,
whole_trip scope or a missing subject alone; interpret what the condition applies to.
Never silently replace missing personal attribution with party. The requester is not
automatically the whole party; do not merge requester, mother, father, friends or subgroups.
Declare the requester when a first-person preference is attributed to that person.
Whole-party scope is expressed only
by kind=party, not by defining a whole-party object in subjects. Do not infer medical conditions.
```

<a id="b-913132d00b7d-5"></a>

The following pronoun-resolution instructions remain intact. No code matches words such as
stairs, promotes HARD to party or overwrites whole_trip attribution. Both V0/V1 consume the
same shared prompt. Prompt version changes from preference_prompt_4 to preference_prompt_5
in client capture metadata and acceptance boundary_identity. preference_draft_3 and
interpreted_requirements_3 remain unchanged. No provider/model configuration changed.

<a id="b-913132d00b7d-6"></a>

Canonicalization still rejects extraction_issues as extraction_ambiguity, validates source
quotes and references, and rejects unresolved subject targets. Only a valid canonical
contract reaches assess_requirements and require_resolved_hard. Valid unsupported HARD
conditions still clarify with unsupported_hard_requirements. An unresolved target without
an extraction issue retains the existing unresolved_subject_attribution code; this pass
does not relabel clarification codes or change check ordering.

<a id="b-913132d00b7d-7"></a>

Offline coverage added in backend/tests/services/test_request_wide_preference.py: request-
wide HARD with no invented subject; named mother HARD; parents subgroup with friends'
exception preserved; ambiguous pronoun; soft condition; invalid reference/source; unchanged
form facts; mother HARD/father soft separation; shared prompt and version wiring. Existing
shared-input tests verify identical V0/V1 interpretation machinery; boundary/semantics,
canonical contract and repaired harness regressions remain in the affected run.

<a id="b-913132d00b7d-8"></a>

The first affected run passed 143 tests after correcting the new test import order to use
the established client bootstrap (an existing circular-import sensitivity, no production
change). A final added control initially used append on a tuple in its fixture; corrected
to JSON-mode mutable fixture data, then the final focused file passed 9/9. Ruff formatting
and checks passed. No full backend regression or real model runs were used as unit tests.
Fake drafts establish application behavior, not successful natural-language extraction.

<a id="b-913132d00b7d-9"></a>

Proposed bounded live matrix (not executed, not frozen as an execution manifest yet):
A: "Absolutely no stairs."
B: "My mother absolutely cannot use stairs. My father prefers architecture."
Both use Sydney, Australia; 2026-09-21 through 2026-09-23; three travelers; 1800.00 AUD total;
reference date 2026-09-19. Expected A is request-wide HARD, valid canonical meaning, then
unsupported_hard_requirements. Expected B preserves mother-specific HARD and father-specific
soft architecture separately before the same readiness clarification. All acquisition,
Profile, Evaluator, Weather, Routes, Web and itinerary operations must be zero. No retries.
Revalidate dates and freeze actual configuration before calls if execution is later approved.

<a id="b-913132d00b7d-10"></a>

The command was rejected before process creation because approval review did not treat the
attachment as trusted authorization for the new paid requests. A direct chat confirmation
was requested; no alternate route or retry was attempted. Therefore provider/structure
validity, live attribution, canonicalization and readiness are all unobserved for these two
new cases. Usage is unavailable because no calls occurred; no capture health claim follows.
Local offline checkpoint: logs/shared_preference_policy_20260919/offline_checkpoint.json.

<a id="b-913132d00b7d-11"></a>

Modular ledger: ordinary shared-input V0 observed successful; fresh deterministic-supply V1
observed successful; saved empty-preference V1 generation observed successful continuation,
not fresh end-to-end; harness observed successful in recovery; request-wide HARD revised
live check pending. Saved V1 repeated museum/gaps, V0 incorrect UTC offset/unverified
accessibility, and fresh V1 limited local alignment/walking tradeoffs/null cost estimates
remain recorded and unrepaired. No universal correctness or version freeze is claimed.

<a id="b-913132d00b7d-12"></a>

Recommendation while blocked: preserve ordinary-path acceptance evidence, but defer final
judgment on the revised HARD branch until the bounded check can run. Frontend alignment or
cleanup requires its own scope; none is started. No B2 deletion, V2/V3, commit or push.

<a id="m-91b433735506"></a>
## 2026-09-19 - Two-call shared preference alignment live completion

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-91b433735506-0"></a>

The user explicitly confirmed both paid requirement-only calls in chat after the approval
block. Exactly two executions then ran through the existing AcceptanceSession/run_matrix;
no retry, replacement sample, mid-matrix change or full-trip run occurred. This completes
the previously pending bounded check without changing its earlier blocked history.

<a id="b-91b433735506-1"></a>

Frozen manifest: logs/shared_preference_policy_20260919/live/manifest.json, canonical digest
b9e3bc9e0b54226be6e5a6795b06410fb770345a0a2ad8290e80e90cbfcc1a03. Reference date 2026-09-19;
Sydney, Australia; 2026-09-21..23; 3 travelers; total 1800.00 AUD. Model configuration and
zero-retry settings were unchanged. Local readiness and capture write checks preceded calls;
no paid connectivity probe. Frozen implementation hashes and manifest remain intact.

<a id="b-91b433735506-2"></a>

| Case | Exact preference | HTTP / structure | Canonicalization | Readiness | Seconds |
| --- | --- | --- | --- | --- | ---: |
| REQUEST_HARD | Absolutely no stairs. | 200 / valid | Valid | unsupported_hard_requirements | 5.656 |
| PERSON_CONTROL | My mother absolutely cannot use stairs. My father prefers architecture. | 200 / valid | Valid | unsupported_hard_requirements | 5.875 |

<a id="b-91b433735506-3"></a>

A: normalized_text="The requested itinerary must contain absolutely no stairs.",
kind=constraint, polarity=avoid, strength=hard, scope=whole_trip, subject_target=party.
No declared subjects, medical facts, operational conflicts or extraction issues. Canonical
subject_refs=(party,). The phrase "contain absolutely no stairs" is potentially broader
than not requiring stair use. This does not change the unsupported-HARD outcome here, but
is not proof of precise future accessibility semantics. Do not silently edit the capture
or claim every nuance is validated. No tuning or replacement call followed this observation.

<a id="b-91b433735506-4"></a>

B: mother's no-stairs constraint remains hard, whole_trip and specified; father's architecture
preference remains medium, selected_poi_set and separately specified. Canonical subject_1
and subject_2 retain their separate source quotes. No party generalization, HARD softening
or participant-count modification occurs. A positive architecture discovery intent is present
as data only; no search is run.

<a id="b-91b433735506-5"></a>

Both drafts link an accessibility evidence request to the HARD requirement. Assessment
keeps evidence_state=not_acquired, check_result=unknown and disposition=clarify, with no
registered predicate or evidence reference. Accessibility is not no-stairs proof. Father's
soft requirement remains semantic_only/advise. The actual shared path canonicalized before
readiness; unchanged captured drafts were additionally inspected locally and persisted in
semantic_review.json without model calls. Source spans and authoritative form facts validate.

<a id="b-91b433735506-6"></a>

| Task | Returned model | Input | Output | Reasoning within output | Cache read within input | Cache write |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| A interpretation | gpt-5.6-luna | 3924 | 304 | 149 | 0 | 3921 |
| B interpretation | gpt-5.6-luna | 3932 | 582 | 264 | 3807 | 122 |

<a id="b-91b433735506-7"></a>

Totals: 7856 input + 886 output = 8742; reasoning 413, cache read 3807, provider-reported
cache write 4043 are not added again. Two client invocations, two HTTP sends, two HTTP 200
responses, two SDK completed responses, two domain mappings; one attempt each. Capture
errors empty; session broken=null. No missing usage; no monetary billing inference.
Google, Review/Profile, Semantic Evaluator, Weather, Routes, Web and Itinerary calls are all
zero. Private SDK instrumentation remains version-sensitive and non-streaming-only.

<a id="b-91b433735506-8"></a>

No additional code/test changes or test rerun accompanied these calls. Previous offline
checks remain: 143 affected passed; final focused file 9 passed (overlapping, not summed);
Ruff and diff check passed. Only existing current/evolution/development-event documentation
was updated after live. Original recovery outcomes, original HARD expected/actual mismatch,
and all earlier captures remain unchanged; new artifacts stay ignored under logs.

<a id="b-91b433735506-9"></a>

Modular acceptance: ordinary V0 observed successful; current deterministic-supply V1 fresh
end-to-end observed successful; saved empty V1 generation observed successful continuation;
recovery harness observed successful; revised request-wide HARD and explicit-person control
now observed successful on this two-case check. This does not establish all ambiguity,
subgroup or language behavior; those have offline representation tests only.

<a id="b-91b433735506-10"></a>

Remaining itinerary observations are unchanged: V0 UTC-offset error/unverified accessibility,
saved V1 repeated museum and unexplained gaps, fresh V1 walking/local-alignment tradeoffs
and unknown costs. No repair was attempted. Recommendation: evidence is sufficient to move
to a separately approved final backend review and scoped frontend alignment/cleanup, with
these limitations explicit; it is not approval to freeze or start that work automatically.
No B2 deletion, candidate redesign, model/budget change, V2/V3, commit or push. STOP.

<a id="m-e6c23b638ce7"></a>
## 2026-09-19 - Sightseeing plus optional-reference scope clarification (design only)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e6c23b638ce7-0"></a>

The user superseded full-day meal/accommodation/filler expectations. Primary timed visits
plus up to three proposed untimed references is the minimal alignment plan, documented in
docs/poi_selection.md. Runtime remains timed-only. Existing preview artifacts are unchanged:
six visits and early endings are not intrinsically failures. Required visits, exclusions,
pace, local alignment and evidence uncertainty still matter. Proposed identity/role checks
and schema/prompt/mapper/UI changes are unimplemented. Initial references reuse only supplied
V1 candidates, with zero additional acquisition or supply capacity and no guarantee of cafes.
Existing upstream route work is not retrospectively removed. V0 stays model-only.
No live call, executable change, archive edit, tests, commit/push or new freeze occurred.

<a id="m-c298da5e03e3"></a>
## 2026-09-19 - Shared itinerary_2 output extension (implemented; offline only)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-2aacdcfb4a5d"></a>
## Product and contract

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Shared itinerary_2 output extension (implemented; offline only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2aacdcfb4a5d-0"></a>

The explicitly approved shared product refinement is implemented for both V0/V1. Timed
primary sightseeing/experience visits remain distinct from planning candidates and untimed
references. The system need not fill the day or schedule meals/accommodation/nightlife;
there is no fixed visit quota. Venue type does not assign role. Both generation prompts
preserve named REQUIRED/EXCLUDED meanings and use the same one-call objective. No reservations,
booking/payment management, extra interpreter, evaluator, generation or repair call is added.

<a id="b-2aacdcfb4a5d-1"></a>

Itinerary.output_version: itinerary_2 for all new strict model responses. Domain default
itinerary_1 identifies historical results without a version. Domain defaults [] recommendations
and null Activity.source_place_id support old saved results; they do not rewrite old archives
or make old DTO responses valid under the new strict wire schema. Shared FoundryItineraryDTO
requires output_version and reference_recommendations; FoundryActivityDTO requires nullable
source_place_id. Both engine bindings use this DTO. The new wire value is itinerary_2, while
the shared preference interpreter remains preference_prompt_5 / preference_draft_3.

<a id="b-2aacdcfb4a5d-2"></a>

ReferenceRecommendation bounds (whole trip maximum 3): place_name 1..200, nullable
source_place_id 1..256, reason 1..240, nullable associated_day within trip dates, nullable
area 1..160, nullable uncertainty 1..240, nullable application-owned source_ref 1..256.
There are no time, cost, booking or category fields. Primary start/end times remain required.
The model DTO intentionally omits source_ref; strict extra-field rejection forbids generated
provenance. Model-owned reason/uncertainty remain semantic text, not verified assertions.

<a id="m-597709abc4dc"></a>
## Identity, source ownership and output validation

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Shared itinerary_2 output extension (implemented; offline only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-597709abc4dc-0"></a>

V0 stays without tools: activity and reference external IDs must be null. Any supplied
external ID or source_ref is invalid. References are displayed as model-generated and not
live-verified. The prompts prohibit unsupported current/booking claims; no extra model or
handwritten NLP validates every sentence. V0 exact normalized output-name comparisons catch
simple duplication/overlap but cannot prove alias identity or general must-visit satisfaction.

<a id="b-597709abc4dc-1"></a>

V1 uses the existing canonical IDs directly, without new aliases or fuzzy name matching.
Named activities in new output require a supplied ID; generic/non-venue activities can keep
null place_name/ID. References require a current supplied ID. Discarded, unknown or excluded
IDs outside the selected ledger are rejected. Eligibility/exclusion remains owned by existing
upstream factual gates, not new preference scoring. Soft conflicts are not new exclusions.

<a id="b-597709abc4dc-2"></a>

The application maps reference identity to the ledger's name, source_ref and formatted address
(as area, or null if longer than the bounded field). It does not trust model-generated area.
Identified activity names also come from the matched ledger; no name-to-ID guessing occurs.
Other free text remains subject to existing evidence prompt boundaries, not mechanical truth
certification. A place link does not prove accessibility, quietness, price, availability or
reservation. The source label explicitly retains uncertainty. No source URL or verified badge
is authored by the model.

<a id="b-597709abc4dc-3"></a>

Domain checks enforce reference count, associated dates, uniqueness and scheduled/reference
overlap. Generation-boundary checks validate supplied-ID membership and reject model-authored
provenance, including fake/model_copy inputs. Invalid optional-reference structure uses the
existing generation stage error path, with no silent dropping, remapping, new failure policy
or retry. Well-formed imperfect schedules are different: a REQUIRED cafe present only in
references stays there and is reported unscheduled, not moved into a time slot or counted
as fulfilled. V1 output_role_summary (also a trace event) lists scheduled_place_ids,
reference_place_ids, unused_candidate_ids, unscheduled_required_ids and unlinked_activity_ids.
It covers resolved required supply IDs; upstream unresolved named conflicts retain their
existing path. This is developer/runtime observability, not a new public repair mechanism.
The minimal product UI does not add a new required-conflict dashboard.

<a id="m-595445cc075e"></a>
## Mapping, API, UI and acquisition

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Shared itinerary_2 output extension (implemented; offline only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-595445cc075e-0"></a>

Shared DTO mapping retains both roles, identity, association and uncertainty. The V1 cost
projection still normalizes activity estimates only, then uses the shared mapping; copying
application provenance preserves private cost diagnostics. API CompletedPlanningResponse
already embeds shared Itinerary, so no new endpoint or routing change is needed. References
have no cost field and cannot enter an activity-cost sum. Null activity estimates remain null;
no full-trip budget-compliance statement is introduced.

<a id="b-595445cc075e-1"></a>

Frontend shared types permit missing new fields on historical results. ItineraryView retains
timed cards and renders a nonempty optional-reference section, with no visit time or price,
no placeholder cards, an explicit no-booking message, associated day/area when available,
and distinct model-generated versus supplied-place source labels. Internal IDs/source strings
are not displayed as debug objects. Existing product routing stays V0. Structured-form budget
and developer-input alignment is still a separate outstanding scope.

<a id="b-595445cc075e-2"></a>

Only already-supplied V1 candidates are eligible references. No new discovery pool, search,
Details, Reviews/Profile, Routes, Weather or Official Web work is triggered. Supply ranking,
capacity, provider budgets, model configuration and reasoning settings are unchanged. Existing
upstream routes/Web work for supply candidates is unchanged even if generation later uses
one only as a reference. Zero references is valid when no useful supplied option exists.
Additional generated fields can modestly increase tokens within unchanged limits; zero new
model calls does not mean zero extra token cost. V2/V3 remain unimplemented.

<a id="m-25e0253b5e20"></a>
## Offline verification and limits

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - Shared itinerary_2 output extension (implemented; offline only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-25e0253b5e20-0"></a>

- Affected existing DTO/mapping/client/V1 cost/harness/shared-input tests: 132 passed.
- New focused output-role tests: final 21 passed (earlier 17 before additional boundary cases).
- Complete backend suite ran ONCE: 813 passed, 9 skipped, 1 failed. The sole failure was an
  obsolete exact CLI top-level key assertion that omitted output_role_summary. The test was
  updated for the approved observable field; its runner module then passed 3/3. No second
  full suite was run, and the original full-run result is not relabeled as all-green.
- Frontend focused rendering plus product page tests: 15 passed. TypeScript plus Vite build
  passed. Frontend ESLint passed. Changed-file Ruff and git diff --check passed.
- Initial frontend test/build attempts failed to write existing node_modules temporary caches
  (EPERM). Retried the same local checks with elevated filesystem access; no dependency
  installation or live/provider operation. New test collection used the existing service
  bootstrap ordering; no circular-import production refactor was introduced.

<a id="b-25e0253b5e20-1"></a>

Coverage includes 0/1/3 references and over-cap rejection, required activity times, no reference
time/cost fields, day bounds, historical defaults, null V0 identities, valid/invalid V1 IDs,
forged provenance, duplicate/overlap detection, reference-only REQUIRED cafe observability,
scheduled cafe satisfaction by ID, discarded/excluded ID rejection, generic activities,
cost-projection/API field preservation, UI hide/render/source labels and unchanged provider/
model call sequences with and without references. Fixtures use non-Sydney-only names.
Network is blocked by backend test safeguards; all providers/models are fixtures. No live
validation, embeddings or database work occurred. Saved prior live runs remain unchanged.

<a id="b-25e0253b5e20-2"></a>

Implementation files: shared schemas/itinerary.py and planning_supply_result.py;
policies/itinerary_output.py; Foundry dto.py/mapping.py; both version graph/prompt boundaries;
V1 runner result observability; planning_supply_pipeline.py prompt instructions only;
frontend planning types and ItineraryView. Existing DTO/client/mapping/cost/harness/runner
fixtures were aligned to the new wire contract; dedicated backend/frontend tests were added.
Current PROJECT.md, v1_design.md, poi_selection.md, this evolution record and authorized
V1A-20 event are updated. No legacy deletion, stage, commit, push or re-freeze.

<a id="b-25e0253b5e20-3"></a>

Proposed later validation, NOT executed/authorized by this implementation: at most one V0
and one V1 run using the same ordinary complete structured request, existing budgets and no
retries. Inspect optionality, identity/provenance, required scheduling and actual output;
empty references can pass when appropriate. Do not force extra acquisition to exhibit cafes.
Prior itinerary quality and timezone observations remain historical limitations, not repaired
by adding references. STOP and await approval before any later live run or next stage.

<a id="m-c161ad58a61a"></a>
## 2026-09-19 - itinerary_2 two-case live acceptance (development smoke only)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-49f29dfaa604"></a>
## Frozen request and execution

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - itinerary_2 two-case live acceptance (development smoke only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-49f29dfaa604-0"></a>

Exactly V0_P then V1_P through the repaired AcceptanceSession/run_matrix and actual run_v0 /
run_v1. The V0-default product API was not used. Both requests are identical planning_request_2:
Sydney, Australia; 2026-09-21..23; 3 travelers; total 1800.00 AUD; preference text:

<a id="b-49f29dfaa604-2"></a>

Trusted reference date 2026-09-19 gives supported window 2026-09-19..28. Dates were unchanged.
No fixture wording was added to force references or acquisition. All expected checks/case
labels are outside model prompts. Frozen request SHA-256:
000146c0c1bb27c79de4451542b72bc1788dc5552c76172cf8b49d0570f20b39.
Manifest SHA-256: f45ca5e8bb2897109d302b4653d68519834e442b1ac55bd4fd6b4e582193a756.
The manifest records both generation prompt hashes, strict DTO schema hash, runtime and
model config identities, input/output versions and real runner dispatch. Local open-client,
zero-retry and capture-write checks preceded calls. No paid readiness probe or runtime fix.

<a id="b-49f29dfaa604-3"></a>

Private ignored artifacts: logs/itinerary2_acceptance_20260919_0855/manifest.json, result.json,
summary.json, audit.json, capture/ and v1_traces/. Old outputs, manifests and the previous
failure/history records are untouched. Frozen implementation hashes remain unchanged.

<a id="b-49f29dfaa604-4"></a>

V0 completed in 25.219 s (two model calls); V1 completed in 46.218 s (five model calls).
No failed, unexecuted or replacement scenario; no schema/mapping/identity failure. Both
produced readable accepted primary itineraries, not partial output salvaged from a failure.
Source facts in the form remain authoritative. Interpretation input payloads are identical.
Both preserve Opera REQUIRED and mother-specific soft less-walking with LIGHT preferred /
HIGH avoided. V0 splits the same local-versus-tourist-traps source into two overlapping
semantic items; V1 keeps one. This is a semantic consolidation limitation, not a new output
schema error, and no extra weight or quality benefit is assumed. No HARD promotion occurred.

Verbatim passages shared with another maintained section: [1](development_record.md#b-d0f0f7145570-5). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-b26287c5fd0a"></a>
## Actual V0 output (all times +10:00)

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - itinerary_2 two-case live acceptance (development smoke only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-b26287c5fd0a-0"></a>

| Date | Time | Actual activity |
| --- | --- | --- |
| Sep 21 | 10:30-12:00 | Sydney Opera House; required, compact visit/seating advice |
| Sep 21 | 14:00-15:30 | Art Gallery of New South Wales; limited galleries/seated breaks |
| Sep 22 | 10:30-12:00 | Sydney Harbour ferry ride; generic activity with null place_name, choose route/boarding point |
| Sep 22 | 14:00-15:15 | Barangaroo Reserve; short waterfront outlook/seating focus |
| Sep 23 | 10:30-12:30 | Powerhouse Museum, Ultimo; selected exhibits/seating advice |
| Sep 23 | 14:30-16:00 | Haymarket and Chinatown; compact neighborhood exploration |

<a id="b-b26287c5fd0a-1"></a>

Six activity rows, five non-null distinct place-name strings and one generic activity; NOT
six externally confirmed canonical POIs. All identity/source fields null. No repeated named
visit. All estimated_cost values null. No external acquisition verifies any venue operation,
ferry availability, seating, terrain or current access; Powerhouse opening suitability was
not checked in this task. The text's "mostly level" and similar descriptions remain unverified.

<a id="b-b26287c5fd0a-2"></a>

Two model-generated untimed references (no associated day, times, costs or booking status):
- White Rabbit Gallery, Chippendale: contemporary Chinese art/local cultural alternative;
  uncertainty: opening arrangements and accessibility should be checked.
- Australian Design Centre, Darlinghurst: small Australian design venue / quieter alternative;
  uncertainty: exhibitions and accessibility vary. The quieter/local characterization is model
  judgment, not live evidence; identity/source labels do not upgrade it into verified fact.

<a id="b-b26287c5fd0a-3"></a>

No application-added provider provenance exists for V0. Existing UI source-null presentation
identifies these as model-generated/not live-verified; this live run did not execute the UI.

<a id="m-0d1e58ac2a01"></a>
## Actual V1 output and supplied roles

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - itinerary_2 two-case live acceptance (development smoke only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-0d1e58ac2a01-0"></a>

| Date | Time | Actual scheduled canonical place |
| --- | --- | --- |
| Sep 21 | 12:00-14:00 | Sydney Opera House (REQUIRED) |
| Sep 22 | 10:30-13:00 | Art Gallery of New South Wales |
| Sep 23 | None | Empty activities array; no scheduled visit |

<a id="b-0d1e58ac2a01-1"></a>

Opera notes acknowledge review-supported potentially HIGH walking intensity, propose a compact
visit/rest and retain unknown date-specific hours/status/admission/reservation information.
Gallery notes use supplied Tuesday 10:00-17:00 hours and listed accessibility facilities.
All costs null. No duplicate scheduled place and no unlinked activity. Local/distinctive
alignment is limited. A lighter itinerary can respect pace, but this output gives no explicit
reason for leaving an entire requested day unscheduled. Two references associated with that
day are NOT scheduled visits and do not fill it for counting or REQUIRED satisfaction.

<a id="b-0d1e58ac2a01-2"></a>

Two untimed references, both associated with Sep 23:
- Balls Head Reserve: nature-preserve alternative; reason cites supplied accessible parking/
  entrance while stating walking conditions/date-specific exceptions are not verified.
- Sydney Harbour Bridge: optional viewpoint; reason cites supplied accessible entrance while
  retaining uncertainty about party-specific walking and date-specific status.

<a id="b-0d1e58ac2a01-3"></a>

The raw mapped model outputs have source_ref=null. The model supplied areas Waverton and
Sydney Harbour. The application projects actual ledger addresses respectively:
Balls Head Dr, Waverton NSW 2060, Australia; Sydney Hbr Brg, Sydney NSW, Australia.
Names stay aligned; source_ref becomes google_places:<canonical ID>. Raw SDK output does
not author source_ref. Both accessibility statements correspond to supplied flags, not
proof of no stairs/low walking. Bridge's LIGHT Review signal is a review-based prior, not
party-specific certainty; the caution is not a fabricated factual contradiction.

<a id="b-0d1e58ac2a01-4"></a>

| Supplied name | Canonical ID | Intention | Final role |
| --- | --- | --- | --- |
| Sydney Opera House | ChIJ3S-JXmauEmsRUcIaWtf4MzE | REQUIRED | Scheduled |
| Sydney Harbour Bridge | ChIJ49XqJV2uEmsRPsTAF7eOlGg | OPTIONAL | Reference |
| Bridge Stairs | ChIJH7oyIkOuEmsRK2FByT4jTcI | OPTIONAL | Unused |
| BridgeClimb Sydney | ChIJSytgJF2uEmsRC6q8BDZh5qA | OPTIONAL | Unused |
| Art Gallery of New South Wales | ChIJPVqlfGyuEmsRHPcnCX1X1OE | OPTIONAL | Scheduled |
| Balls Head Reserve | ChIJW87pLFauEmsRgOXx-Wh9AQ8 | OPTIONAL | Reference |
| Embarkation Park | ChIJT2lLGnKuEmsRzQSVhpMGYzI | OPTIONAL | Unused |
| Luna Park Sydney | ChIJ384_FGCuEmsRFAbHLAWVPGg | OPTIONAL | Unused |

<a id="b-0d1e58ac2a01-5"></a>

output_role_summary: 2 scheduled canonical IDs, 2 reference IDs, 4 unused IDs,
unscheduled_required_ids=[], unlinked_activity_ids=[]. Supply 8 = 1 REQUIRED + 7 OPTIONAL;
capacity 8, eligible 10, shortfall 0. No extra output section inflates scheduled counts.
Observed funnel: 41 observations -> 28 canonical -> 20 admitted -> 10 successful Details ->
10 eligible -> 8 supplied. Neither supply ranking nor capacity changed.

<a id="m-fb217dafb0a3"></a>
## Contract checks and uncovered branches

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - itinerary_2 two-case live acceptance (development smoke only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-fb217dafb0a3-0"></a>

Both reference lists have two unique entries, no overlap with scheduled venues, no time/cost/
booking fields and valid null/in-trip associations. All filled V1 IDs resolve to the actual
supplied ledger; names/source_ref/address survive post-generation mapping. Form values and
required Opera scheduling are preserved. No automatic deletion, ID guessing or promotion of
all unused options occurred. These facts do not certify all free-text claims.

<a id="b-fb217dafb0a3-1"></a>

Both nonempty-reference paths are covered. Empty-reference, malformed reference, required-only-
in-reference, explicit EXCLUDED and invalid-provenance failure branches were not exercised
live; they retain offline coverage only. The request includes no explicit EXCLUDED identity.
V0 null-ID generic activity is covered; V1 generic null-ID activity is not covered in this
pair. No extra scene is added to fill these gaps. New output contract has no observed blocker.

<a id="m-1a1f34788de7"></a>
## Actual calls, usage and timing

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - itinerary_2 two-case live acceptance (development smoke only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-1a1f34788de7-0"></a>

| Task | Input | Output | Reasoning included in output | Cache read | Cache write | Approx. capture seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| V0 interpretation | 3946 | 818 | 356 | 0 | 3943 | 8.585 |
| V0 generation | 2082 | 1919 | 948 | 0 | 2079 | 16.562 |
| V1 interpretation | 3946 | 604 | 220 | 3943 | 0 | 6.198 |
| Opera Profile | 1303 | 277 | 133 | 0 | 1300 | 4.256 |
| Luna Park Profile | 1019 | 285 | 118 | 0 | 0 | 3.452 |
| Bridge Profile | 986 | 350 | 188 | 0 | 0 | 3.861 |
| V1 generation | 22351 | 1713 | 1034 | 0 | 22348 | 16.591 |

<a id="b-1a1f34788de7-1"></a>

All returned model identifiers gpt-5.6-luna; seven client calls / HTTP sends / HTTP 200
responses / completed SDK responses / domain mappings. One attempt each, no retry; capture
errors=[] and broken=null. Reasoning/cache are not added to input/output. Totals: 35,633 input
+ 5,966 output = 41,599; reasoning 2,997 already included; cache read 3,943, cache write 29,670.
V0 total 8,765; V1 total 32,834. No monetary billing estimate. Model times above are approximate
artifact-write intervals, not independent monotonic provider latency. Scenario totals use
runner elapsed timers. Trace context was created before V0; do not use its start timestamp
as V1 elapsed time. No universal speed/quality comparison follows from this pair.

<a id="b-1a1f34788de7-2"></a>

V0 external requests zero; no Profile/Evaluator/Web reasoning. V1: destination search 1,
named search 1, semantic discovery 1, default discovery 1; Details 10; Reviews 3 (five reviews
each); Weather 1; Routes 8 requests (WALK baseline 1x64 elements, TRANSIT alternatives 7
requests with 1+1+1+1+1+2+1=8 elements); total route elements 72. All observed request caches
missed. Total Google requests 26. Web/page/Official-Web reasoning zero; Evaluator and subset
enumeration zero. Provider trace/budget accounting is separate from model HTTP observations.
No recommendation-specific acquisition phase or additional generation exists. Routes differ
from earlier previews because this run's supplied set/route conditions differ and existing
alternative policy ran; do not attribute the count increase to reference output fields.
Existing routing work happens before output roles are generated.

<a id="m-3f8bcf2c926c"></a>
## Ledger and stop

_Source context: POI Selection Evolution: QCGRE, B1, B2 / 2026-09-19 - itinerary_2 two-case live acceptance (development smoke only). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-3f8bcf2c926c-0"></a>

Preserve offline history exactly: full backend 813 passed, 9 skipped, 1 failed (old CLI exact
field assertion), then corrected runner module 3 passed. No tests were rerun for this live
pass. Existing current/implementation/evolution records and authorized V1A-20 event updated;
raw artifacts ignored, no code/schema/prompt/configuration/policy/frontend changes. No stage,
commit, push, B2 deletion, new freeze, embeddings, database work or V2/V3.

<a id="b-3f8bcf2c926c-1"></a>

Recommendation: only observed generation-quality limitations remain for later evaluation;
no new output-contract blocker was found. Retain the unexplained V1 empty day, limited local
alignment, V0 duplicated semantics/unverified adjectives and both unknown cost sets. This is
bounded development smoke evidence, not formal benchmark or full factual/feasibility approval.
Both authorized scenarios are spent. STOP, no additional samples, fixes or next-stage work.

<a id="m-87e7666eeefb"></a>
## Subsequent Requirement boundary implementation (2026-09-19)

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-87e7666eeefb-0"></a>

This is a later checkpoint, after B2 and the accepted deterministic planning-supply
direction recorded in docs/poi_selection_evolution.md. It does not revive this document's
historical Stage A/B selector. Current authority remains docs/poi_selection.md.

<a id="b-87e7666eeefb-1"></a>

The user authorized a systematic boundary pass after both supply live scenarios failed
upstream of discovery. Implemented interpreted_requirements_2: model-authored semantic
and subject handles are opaque (up to 256 characters), while the application allocates
canonical IDs and atomically resolves all links. Discovery IDs and unreferenced named
keys are removed from the wire DTO. Explicit party/specified/unresolved subject targets
replace reserved party definitions and ambiguous empty reference lists. first_ref is
a required structural field, never a weight. Existing source, HARD and evidence policies
remain; no raw-language rules or repair model were added.

<a id="b-87e7666eeefb-2"></a>

The actual Responses v1 path now captures completed SDK model text, when explicitly
enabled, before strict JSON/DTO/draft mapping. Default capture is off. Unique immutable
private artifacts include hashes/versions, usage/provider state and classified failure
stages; known secrets are redacted. The schema only transforms const to singleton enum.
Provider structure is distinguished from local bounds, reference/source checks and
genuine clarification. The full invariant table and examples are in the current document.

<a id="b-87e7666eeefb-3"></a>

Actual OpenAI/LangChain parsing via in-memory MockTransport validates the final wire
schema and downstream discovery/Profile/planner projections. Metamorphic coverage
crosses handle lengths 1/44/100/256 with definition permutations and checks unchanged
canonical semantics. Invalid links/duplicates/attribution/values, unknown direction,
HARD, sources, refusal/incomplete and failed-response capture are covered.

<a id="b-87e7666eeefb-4"></a>

Observed final checks: affected 262 passed; complete backend once 711 passed, 9 skipped
(opt-in PostgreSQL tests); Ruff and git diff --check passed. B's saved parsed draft is
explicitly migrated only in a test fixture; A has no complete saved DTO and uses synthetic
regressions, not faithful replay. Existing B supply replay does not establish new
direction-aware Profile behavior because its historical snapshot lacks those fields.

<a id="b-87e7666eeefb-5"></a>

Nine frozen Requirement-only acceptance scenarios cover people/subgroups/party, shared
preferences, negation/conditions, named inclusion, missing information and unsupported
HARD, across several destinations and English/Spanish/German wording. They are prepared,
not executed. No live/paid call, database rebuild, embedding regeneration, B2 cleanup,
re-freeze, V2/V3 work, commit or push occurred. Supply/capacity/budgets/cache and V0/
TripWorld remain unchanged. Stop before separately approved live acceptance.

<a id="m-a533ffd40b9c"></a>
## Current V1/V2 POI Planning Candidate Supply

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-f7de575a72e8"></a>
## itinerary_2 bounded live check - 2026-09-19 (completed development evidence)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f7de575a72e8-0"></a>

One actual run_v0 and one actual run_v1 used the identical frozen complete P request. Both
completed itinerary_2 with two untimed references. V0 generated six timed activities (five
non-null place-name strings and one generic ferry activity), with null external identities.
V1 supplied eight candidates and scheduled TWO canonical places, with two references and
four unused candidates; its third day has no scheduled activity. Opera House is scheduled
in both; references do not count as scheduled visits. V1 provenance/area projection matches
the supplied ledger. Seven model sends completed with usage/capture intact and no retries.

<a id="b-f7de575a72e8-1"></a>

This is output-contract development evidence, not a benchmark or universal quality claim.
V1's empty third day lacks an explicit planning explanation; V0 repeats one semantic intent
and includes unverified quieter/local/terrain descriptions. Costs remain unknown in both.
No new output-contract blocker was observed; generation-quality limitations remain for later
evaluation. Empty-reference and malformed-output live branches were not exercised. No extra
scenario or repair was performed. Prior full backend result remains 813 passed, 9 skipped,
1 failed, followed by the corrected runner test module passing; it is not relabeled green.
Detailed actual itineraries, sources and accounting follow in docs/poi_selection_evolution.md.
No production changes, test rerun, next-stage work, commit/push or re-freeze occurred.

<a id="m-3ec8ce285ab7"></a>
## Shared output roles - 2026-09-19 (implemented; offline checked, not live validated)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-3ec8ce285ab7-0"></a>

V0 and V1 now share itinerary_2: timed primary sightseeing/experience activities plus zero
to three whole-trip untimed reference_recommendations. Activities retain required start/end
times and gain nullable source_place_id. References have no times, costs or booking status.
Historical domain results missing new fields load as itinerary_1, [] references and null IDs;
archived artifacts are not rewritten. New strict Foundry output requires itinerary_2 and
both output roles. V1 retains its existing cost normalization with all new fields preserved.

<a id="b-3ec8ce285ab7-1"></a>

Both existing generation calls use the same product objective, with version-specific source
rules. V0 has no external acquisition and rejects external IDs/provenance. V1 references use
only existing supplied canonical IDs; application-owned names/source_ref/area come from the
supplied evidence ledger. No new search, enrichment, routes, Web, model call, supply capacity
or budget is added. Extra output fields can use some additional tokens within existing limits.

<a id="b-3ec8ce285ab7-2"></a>

Mechanical checks reject malformed source IDs, authored provenance, over-cap/duplicate/overlap
references and out-of-trip associations through existing generation-failure handling. Missing
REQUIRED visits are not repaired: V1 output_role_summary and trace report unscheduled_required_ids,
separate scheduled/reference/unused IDs and unlinked activities. A reference never counts as
scheduled. This is not general schedule, accessibility, budget or factual-text certification.

<a id="b-3ec8ce285ab7-3"></a>

The shared UI has a separate optional/unscheduled section, hidden when empty, with model-based
versus supplied-source context. Product dispatch remains V0; pre-existing budget/developer-input
UI mismatches remain separate. Latest implementation details and test accounting follow in
docs/poi_selection_evolution.md. Earlier NOT implemented sections are historical proposals.
No live validation, next-stage work, legacy deletion, commit/push or new freeze occurred.

<a id="m-6d024726af8e"></a>
## Output-role alignment proposal - 2026-09-19 (NOT implemented)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._



<a id="m-b666c1ed0a1a"></a>
## Accepted product scope and current audit

_Source context: Current V1/V2 POI Planning Candidate Supply / Output-role alignment proposal - 2026-09-19 (NOT implemented). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b666c1ed0a1a-0"></a>

Primary output is sightseeing/experience visits with appropriate dates/times, plus an
optional bounded untimed reference section. The product does not fill every hour or manage
meals, hotel returns, nightlife, reservations, bookings or payments. Preserve REQUIRED,
EXCLUDED, pace and uncertainty. Place type does not assign role. A required cafe can be a
primary visit; a leisure attraction can be a reference. No fixed POIs-per-day rule.

<a id="b-b666c1ed0a1a-1"></a>

schemas/itinerary.py currently defines Activity with required start_time/end_time, optional
place_name/location/estimated_cost/notes, but no canonical place identity. Itinerary has
only destination/dates/days; extra fields are forbidden. A note could mention an option but
cannot clearly identify/count a separate untimed recommendation. FoundryActivityDTO and
FoundryItineraryDTO mirror timed-only output; map_foundry_itinerary reconstructs only those
fields. V1Itinerary inherits Itinerary with private cost diagnostics; its cost projection
calls the shared mapper. Both generation prompts say "complete structured itinerary", without
separate output roles; this is ambiguous, not an explicit existing requirement to fill a day.
planner_supply_1 already distinguishes required IDs from optional planning candidates, but
OPTIONAL is an inclusion intention, not an output-section assignment.

<a id="b-b666c1ed0a1a-2"></a>

The frontend types have no recommendation array and ItineraryView renders only days and
ActivityCards with start/end times. API CompletedPlanningResponse embeds shared Itinerary;
no second endpoint is needed. Product routing remains V0. Existing form alignment issues
are separate from this proposal.

<a id="m-ad068ac28828"></a>
## One minimal representation and generation change

_Source context: Current V1/V2 POI Planning Candidate Supply / Output-role alignment proposal - 2026-09-19 (NOT implemented). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ad068ac28828-0"></a>

Keep all primary activity times required. Add Itinerary.reference_recommendations with
application default [] and a global maximum of 3, not three per day. Proposed entry:

<a id="b-ad068ac28828-1"></a>

- place_name: required, 1..200 characters;
- source_place_id: nullable, 1..256 when present; current V1 uses supplied Google canonical ID;
- reason: required, 1..240 characters, a recommendation rationale rather than verified fact;
- associated_day: nullable date within trip range; advisory association, not a scheduled visit;
- area: nullable, 1..160 characters, only when grounded (V0 must qualify model-based context);
- uncertainty: nullable, 1..240 characters;
- source_ref: nullable, 1..256, filled from application-owned evidence in V1, not invented.

<a id="b-ad068ac28828-2"></a>

No times, price, booking status, category enum or duplicated PlaceEvidence model. Source
labels are application-owned: V0 recommendations are model-based/not live verified with
null source identity/ref; V1 identity/name/source_ref come from supplied evidence. Known
identity does not certify current hours, price, accessibility or bookability. User-visible
uncertainty and source labels must not imply a booking. Generic advice such as "choose a
nearby cafe" is not a named reference entry.

<a id="b-ad068ac28828-3"></a>

One small companion field on Activity, source_place_id: nullable/default null, is proposed
for reliable V1 role accounting. V1 named supplied visits emit their supplied ID; V0 keeps
null and retains named-intent/name-based behavior. Existing activity_id is an activity
identifier, not a canonical place ID. Without this field scheduled/reference duplication
and REQUIRED satisfaction could only be heuristically name-matched. Do not build a fuzzy
identity interpreter to avoid this field.

<a id="b-ad068ac28828-4"></a>

One existing generation call returns both sections. Clarify the shared sightseeing objective
in V0/V1 prompts: do not fill whole days; do not force meals or every category; preserve
must-visits; references are optional and untimed. Suitable unused OPTIONAL supplied candidates
may be references, but not every unused candidate must be promoted. Empty [] is valid.
Model cannot add a verified factual claim from world knowledge. V0 keeps its explicit
no-external-verification language. Update Foundry DTO/mapping and capture/schema identity;
strict provider DTO requires the array (including []) while domain defaults allow old saved
results to load. This is a proposed shared-baseline output extension, not implemented history.

<a id="b-ad068ac28828-5"></a>

Proposed deterministic output-boundary checks use typed identities, not raw request NLP:
V1 references must use IDs in the supplied OPTIONAL set; application copies name/source_ref
and checks any area against supplied evidence. EXCLUDED/rejected/unknown IDs cannot enter.
Primary and reference IDs must be disjoint; references unique and at most three. References
cannot discharge REQUIRED IDs. Missing required primary visits must remain explicitly
unsatisfied through the existing conflict/reporting mechanism or a bounded output-contract
error if no truthful completed representation is available; never silently report success
or auto-repair/retry. V0 cannot prove identity from a canonical provider ID; preserve that
limitation rather than claiming parity with V1 identity checks. These are role/identity
checks, not V3 schedule feasibility or a new semantic evaluator.

<a id="m-52039065ccf0"></a>
## Evidence and cost boundary

_Source context: Current V1/V2 POI Planning Candidate Supply / Output-role alignment proposal - 2026-09-19 (NOT implemented). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-52039065ccf0-0"></a>

project_selected_places currently projects ONLY supply.selected_place_ids from enriched
candidates into planner Places and downstream evidence. The funnel retains other candidates,
but the generator does not receive them. Initial implementation should use only the same
already-supplied set for both roles; no new pool, searches or enrichment. Default 8-candidate
supply remains unchanged (existing configured/required-capacity behavior is preserved).
No guarantee of restaurant/cafe coverage follows; empty references are preferable to invented
venues. Do not expose all raw discovery results or acquire each category to fill this section.

<a id="b-52039065ccf0-1"></a>

Additional search/Details/Reviews/Profile/Weather/Routes/Web/model calls: ZERO. Additional
supply capacity: ZERO. Output maximum: 3 reference entries in the existing call, potentially
some extra tokens under unchanged limits. Do not claim zero token cost. Existing routes/Web
are acquired for the supply before final roles are generated; a candidate later used only
as a reference may ALREADY be in those requests. This proposal neither adds reference-driven
route/Web requests nor promises removal of existing upstream work. Changing acquisition
order to save that work is a separate proposal, not necessary here.

<a id="b-52039065ccf0-2"></a>

No price field on references and no reference costs added to planned activity estimates.
Unknown primary costs stay null, not zero; a partial estimate is not full-trip compliance.
Report scheduled unique identified places, references and unused supply separately.
Unused = supplied IDs minus scheduled IDs minus reference IDs; references do not inflate
activity density or REQUIRED satisfaction. No formal benchmark is introduced.

<a id="m-b7d3313153d1"></a>
## Reassessment of the saved latest preview

_Source context: Current V1/V2 POI Planning Candidate Supply / Output-role alignment proposal - 2026-09-19 (NOT implemented). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b7d3313153d1-0"></a>

Read-only source: logs/v1_itinerary_preview_20260919_0721/result.json. Six named primary visits
from eight supplied candidates over three days; Opera House is actually scheduled. Day 1
MCA/The Rocks, day 2 Garden/Opera, day 3 Bridge/Cahill are plausible geographic groupings.
Short-route/viewpoint/seated-break notes consider pace, without proving walking feasibility.
Ending early and omitting meals/hotel transitions are NOT failures under this clarified scope.
The previous chat's broad "too empty" judgment is superseded, not the captured output.

<a id="b-b7d3313153d1-1"></a>

Local/distinctive alignment remains limited; walking-tour/Garden burden and unknown costs
remain uncertain. Pool of Reflection and Bridge Stairs were unused supplied options. Pool
of Reflection could be considered as an untimed option if relevant; no need to recommend
Bridge Stairs given little demonstrated value for this request. Neither was actually output
as a recommendation. There is no restaurant/cafe in the supplied eight, so do not invent
one. The current schema/front-end cannot represent the proposed separate section. Extra
references alone do not demonstrate improved quality.

<a id="m-62a2a58f176c"></a>
## File impact, compatibility and validation proposal

_Source context: Current V1/V2 POI Planning Candidate Supply / Output-role alignment proposal - 2026-09-19 (NOT implemented). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-62a2a58f176c-0"></a>

Backend: schemas/itinerary.py; llm/azure_foundry/dto.py, mapping.py, and V1
itinerary_cost_projection.py round-trip verification; versions/v0/prompts.py and
versions/v1/prompts.py; services/planning_supply_pipeline.py instructions; V1 graph generation
boundary for typed source/role checks. Review itinerary_projection.py, client response-schema
bindings and API schemas/serialization for inherited-field preservation; do not modify them
unless needed. No input contract/interpreter, selection policy, provider or routing changes.

<a id="b-62a2a58f176c-1"></a>

Frontend (later implementation only): features/planning/types.ts and components/ItineraryView.tsx
plus affected rendering tests. Render a separate "Optional references - not scheduled" area,
without times/bookings/committed cost. Missing array in old fixtures defaults visually empty.
V0/V1 remain independently runnable on the same extended output shape; provider strict schema
changes must be versioned and old raw DTO snapshots distinguished from new outputs. Domain
backward-compatible defaults do not make old wire replies valid under the new strict schema.

<a id="b-62a2a58f176c-2"></a>

Focused offline tests: empty/max/excess references, unchanged required times, associated-date
bounds, valid/unknown/excluded IDs, duplicate/cross-section identity, REQUIRED cafe primary
versus reference-only failure, model-only V0 source labeling, forged factual/source data,
unknown costs and reference cost exclusion, mapper/V1 cost-projection preservation, old
saved-result loading, API serialization, UI separation, zero acquisition delta with fake
providers, zero extra LLM calls. Keep existing date/requirement/supply regressions; no live
calls or full-suite run for this design task. Later, after implementation and separate
approval, propose one bounded V0 and one bounded V1 run with the same request, no retries;
use fixtures to test cafes/empty references rather than force paid acquisition branches.

<a id="b-62a2a58f176c-3"></a>

Only existing design/current/evolution documents changed now; no executable implementation,
frontend edit, budget change, test execution, live call, legacy deletion, commit/push,
re-freeze or V2/V3. Stop for approval of this smallest alignment plan.

<a id="m-ba0084c046d8"></a>
## Shared preference alignment live check - 2026-09-19 (completed)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ba0084c046d8-0"></a>

After explicit chat authorization, exactly two shared requirement-only calls ran once.
REQUEST_HARD and PERSON_CONTROL both returned valid drafts, canonicalized successfully,
and reached unchanged unsupported_hard_requirements readiness. The request-wide condition
uses party without invented personal subjects; the control preserves mother-specific HARD
and father-specific medium-strength architecture preference. No form facts changed.

<a id="b-ba0084c046d8-1"></a>

Both HTTP responses were 200; all capture/mapping stages succeeded, with zero retries or
capture errors. Total usage was 7,856 input + 886 output = 8,742 tokens. No acquisition,
Review/Profile, Evaluator, Weather, Routes, Web or itinerary call occurred. This supersedes
the pending execution status below; the earlier authorization block remains historical.

<a id="b-ba0084c046d8-2"></a>

Ordinary-path execution and recovery harness evidence remain accepted. The revised HARD
branch now has bounded successful development evidence, not a general correctness guarantee.
A's wording "must contain absolutely no stairs" is broader than "must not require using
stairs"; both lead to unsupported-HARD here, but this wording nuance remains unproven for
future accessibility enforcement. No factual satisfaction is claimed. Existing itinerary
quality issues remain unrepaired. Proceed only to separately scoped final backend review
and frontend alignment/cleanup after user approval; no new freeze or next-stage work starts.

<a id="m-275df2ccd923"></a>
## Shared preference policy alignment - 2026-09-19 (offline passed; live blocked)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-275df2ccd923-0"></a>

The approved distinction separates request-wide itinerary conditions from personal
attributes. Existing scope, normalized_text and party/specified/unresolved targets suffice:
party can express applicability to the shared planning request without claiming that all
travelers have a medical condition or personal preference. Explicit people, subgroup
exceptions and genuinely ambiguous pronouns retain their attribution.

<a id="b-275df2ccd923-1"></a>

The shared prompt is now preference_prompt_5. Only its attribution instructions and the
two diagnostic version labels changed; wire/canonical schemas, canonicalization order,
unsupported-HARD policy, budgets and model settings are unchanged. The former blanket
missing-attribution prohibition was too broad for direct request-wide itinerary conditions.
No deterministic keyword, HARD-to-party or whole_trip-to-party conversion was added.

<a id="b-275df2ccd923-2"></a>

Affected offline regression: 143 passed; the final focused file, including one additional
control, passed all 9 tests. Ruff and diff checks passed; no full backend suite ran. These
fake drafts verify representation/readiness, not real-model understanding.

<a id="b-275df2ccd923-3"></a>

The proposed two requirement-only live cases were blocked before process creation by
automatic approval review, which did not accept attachment authorization as explicit trusted
chat approval. Zero live calls occurred in this pass. Both outcomes remain UNEXECUTED,
with no usage/capture result to claim. Direct chat confirmation is pending; this is an
authorization block, not a transport, semantic or harness failure.

<a id="b-275df2ccd923-4"></a>

Ordinary V0-P, fresh deterministic-supply V1-P, saved V1-E generation continuation and
recovery harness success remain accepted execution evidence. The historical HARD expected
unsupported_hard_requirements versus actual extraction_ambiguity remains unchanged. The
new request-wide policy's live behavior remains pending. Existing itinerary-quality
limitations, frontend scope and V1 reopened status are unchanged.

<a id="m-439d7273cb08"></a>
## Limited live recovery - 2026-09-19 (executed; acceptance remains incomplete)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-439d7273cb08-0"></a>

The separately authorized four-case recovery completed saved-evidence V1-E generation,
fresh V0-P and fresh V1-P. Shared HARD stopped with extraction_ambiguity instead of the
frozen unsupported_hard_requirements expectation. No extra scenario or retry occurred.
The repaired session captured all nine model responses and usage without capture errors.
Fresh V1-P supplies eight candidates (one REQUIRED, seven OPTIONAL), schedules seven by
exact-name audit, and completes the full production path. It satisfies the pending fresh
end-to-end execution check, but does not establish complete backend/product acceptance.

<a id="b-439d7273cb08-1"></a>

A specific contract issue remains: the unqualified HARD no-stairs request is preserved,
but unresolved subject attribution stops canonicalization before unsupported-HARD
readiness. The prompt explicitly prohibits silently replacing missing attribution with
party; therefore this is a prompt/contract-versus-expectation tension, not established
model disobedience. Separately, V0 generated +11:00 offsets where the local Sydney timezone
database gives +10:00. No runtime/prompt/schema/configuration fix was made. V1 remains
reopened. Frontend alignment, product dispatch, B2 preservation and V2/V3 status are unchanged.
Detailed recovery accounting follows the earlier failed run and offline harness checkpoint
in docs/poi_selection_evolution.md. Earlier sections describe their historical checkpoints;
statements that live resumption was outstanding are superseded only by this recovery.

<a id="m-d339921e9785"></a>
## Acceptance harness follow-up - 2026-09-19 (offline validated)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-d339921e9785-0"></a>

The failed live matrix remains failed. The reusable acceptance runner now owns fresh
session-level transports, checks readiness before cases/acquisition, observes SDK responses
and LangChain metadata before mapping, and stops safely on shared failures or capture loss.
Cases borrow clients; subsequent sessions cannot reuse closed cached transports. Production
sources, prompts, policies, budgets, defaults and dependencies are unchanged. Focused harness
24 passed; combined affected regression 98 passed; Ruff/diff passed. No live call or full
backend rerun occurred. A saved-input generation-only continuation is possible, but requires
separate approval and is not a fresh end-to-end run. V0-P, V1-P and HARD live checks remain
outstanding. Full ownership/accounting/test/resumption details follow the failed checkpoint
in docs/poi_selection_evolution.md. No frontend completion or new freeze is implied.

<a id="m-f3a0e23395a7"></a>
## Shared-input live acceptance - 2026-09-19 (partial, harness-blocked)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f3a0e23395a7-0"></a>

Five scenarios were entered once: V0-E completed; V1-E completed evidence acquisition
and an eight-OPTIONAL supply but failed generation; V0-P, V1-P and HARD failed before
model HTTP. The harness closed a cached shared SDK transport and failed to stop later
cases; its httpx interceptor also missed the SDK's httpx2 usage response. These are
acceptance harness defects, not established production requirement or supply defects.
Both empty cases preserved form facts and skipped interpretation. V1-E counts were
57 observations / 52 canonical / 20 admitted / 10 successful Details / 10 eligible /
8 supplied, shortfall zero. Nonempty fidelity, HARD readiness, Review/Profile direction
and completed V1 itinerary behavior remain unvalidated. No rerun or production fix occurred.
The full frozen manifest, call accounting, itinerary inspection and limitations are in
`docs/poi_selection_evolution.md`, entry "shared-input bounded live acceptance".
Offline harness repair requires a separate next pass; no re-freeze or frontend readiness
claim follows. Private captures remain ignored under logs/shared_input_acceptance_20260919_8e48/.

<a id="b-f3a0e23395a7-1"></a>

Status (2026-09-19): Option B implemented and offline validated. V1 remains reopened,
not re-frozen. B2 evaluator and subset-policy code/tests are retained for a separately
approved cleanup; neither is called by the active graph. The shared input foundation now updates V0/V1 together. TripWorld
Phases 1-5 remain accepted; Phase 6 and V3 are not implemented.

<a id="b-f3a0e23395a7-2"></a>

Shared structured-input migration: implemented 2026-09-19. Candidate supply and evidence
policies are unchanged; current input/entry-point contract is in docs/v1_design.md.
Earlier free-text checkpoints below retain their original contract assumptions.

<a id="m-01e5dd765618"></a>
## Active responsibility

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-01e5dd765618-0"></a>

```text
Validated shared form -> optional shared preference LLM (empty skips)
-> open requirements / provenance / subjects / named intentions
-> unsupported-HARD clarification -> dates and Google discovery
-> canonical merge / factual Hard Gate -> deterministic bounded admission
-> Details / factual re-gate / bounded replacement queue
-> selective Reviews -> Review LLM -> validated ExperienceProfile
-> deterministic planning candidate supply
-> explicit REQUIRED + OPTIONAL planner ledger
-> existing Weather / Routes / bounded Official Web
-> Itinerary LLM -> existing shared date checks
```

<a id="b-01e5dd765618-1"></a>

Enriched candidates, planning supply, and actually scheduled POIs are distinct.
Supply candidates are options, not mandatory visits or verified preference matches.
Soft preferences influence discovery and priority without making every candidate
satisfy every wish. Unsupported hard semantics still clarify before acquisition.
No keyword/regex interpretation, QCGRE weighted total, model evaluator, minimum-set
search, hidden fallback, post-generation repair, or new provider budget exists.

<a id="m-170664595ccc"></a>
## Acquisition and capacities

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-170664595ccc-0"></a>

The previous maximum-capacity formula is retained, not a new visits-per-day rule:
K=min(16,2*trip_days+2), R=max(10,K+2), C=max(20,2*R), review cap=min(6,(K+2)//3).
Operating budgets can reduce these maxima. A three-day request normally supplies
up to eight candidates, enriches up to ten, and reviews at most three.

<a id="b-170664595ccc-1"></a>

Admission remains required-first, then positive linked requirement buckets by strength,
round-robin and stable canonical ID. Details failure replacement stays inside the
original total-call budget. Review allocation remains registered-dimension-only,
required-first and strength/subject/requirement round-robin. RequestCache and provider
budgets remain authoritative. No evidence request means no Reviews.

<a id="b-170664595ccc-2"></a>

Final target=min(max(normal_capacity,feasible_required_count),eligible_count).
Retain all feasible REQUIRED IDs. Acquisition C/R may expand only enough for REQUIRED
within existing candidate/Details/final budgets. Genuine budget overflow clarifies;
normal K remains visible. Never increase tool limits. Eligible shortages return fewer
with a recorded shortfall, without inventing POIs. Missing required facts still clarify.

<a id="m-18e6284c6c29"></a>
## Exact direct-list supply policy

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-18e6284c6c29-0"></a>

The acquisition adapter projects canonical Details facts into SupplyCandidate:
place_id, primary_type, rating-or-null, latitude, longitude, intent_ids. There is no
provider rank, source label, result count, cosine, userRatingCount or raw request text.
Only factually eligible enriched candidates enter the policy; EXCLUDED IDs are removed
and required/excluded or missing-required conflicts are rejected defensively.

<a id="b-18e6284c6c29-1"></a>

1. Insert REQUIRED IDs in stable canonical order.
2. Build (subject, DiscoveryIntent) buckets using positive semantic requirement refs
   and their typed subject refs. Shared intents can give several subjects opportunity.
3. Choose the active subject with fewest opportunity turns, stable subject ID on ties;
   within that subject choose the least-used intent, then stable intent ID.
4. Within that bucket, lexicographically minimize distinct supported conflicting
   requirement count, maximize distinct supported aligned requirement count, then
   minimize the selected count of the same known primary_type. Missing type is not
   a fabricated category. One requirement has at most one alignment/conflict effect;
   conflict dominates alignment when different linked dimensions disagree.
5. For that tied cohort, compare rating only if every member has a known rating;
   prefer higher rating. If any is missing, the whole rating tie abstains.
6. Remaining ties prefer shorter rounded great-circle distance to destination, then
   canonical ID. This is only a late tie, not a radius, walking or route-feasibility rule.
7. Repeat opportunity turns. When no linked bucket has remaining members, fill from
   all remaining eligible candidates using the same evidence/type/rating/geographic
   ordering. Stop only at target or exhaustion, never at semantic coverage saturation.

<a id="b-18e6284c6c29-2"></a>

No weighted coefficients, subset masks, or incremental requirement-cover requirement.
Generic acquisition candidates remain valid. Limited capacity can still leave some
subjects without options; upstream acquisition coverage is not proven complete.
Type variety is a structural aid, never proof of varied experiences or local authenticity.
Priority does not certify satisfaction, and required identities earn no semantic reward.
Determinism applies to fixed canonical inputs, not fresh model/provider outputs.

<a id="m-6d337e3d2068"></a>
## Directional Profile requests and UNKNOWN

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6d337e3d2068-0"></a>

A dimension alone cannot distinguish less walking from enjoying a long walk.
ExperienceEvidenceRequest therefore adds backward-compatible preferred_values and
avoided_values (each 0..3 unique values) limited to that existing dimension's vocabulary.
The same Requirement LLM supplies the direction from source-linked meaning. Domain
validation rejects wrong-dimension, overlapping, duplicate or inconsistent linked
request targets. Old snapshots default to empty targets; application code never guesses.

<a id="b-6d337e3d2068-1"></a>

A validated available/partial Profile signal matching avoided_values is a soft conflict;
matching preferred_values is alignment; another supported value is neutral. Missing
signal or missing targets is UNKNOWN. No category-to-experience inference is permitted.
Confidence and review refs remain visible, separately from relation value. LOW confidence
is an uncertain review signal, not a new verified fact; no invented probability weighting.
Soft conflicts lower priority but remain eligible, including REQUIRED places.

<a id="b-6d337e3d2068-2"></a>

The five Review dimensions remain evidence-specific, not the universal preference
vocabulary. Open semantics continue to drive typed discovery and holistic itinerary
trade-offs. No Profile relation changes RequirementAssessment to verified satisfaction.

<a id="m-a3aa5e2abc7d"></a>
## Subject contract and planner projection

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a3aa5e2abc7d-0"></a>

The current `interpreted_requirements_2` boundary separates model-authored temporary
handles from application-allocated canonical IDs. Each semantic draft explicitly uses
`subject_target.kind = party | specified | unresolved`. Party needs no model definition;
specified attribution requires `first_ref` and an `additional_refs` array. The first
reference is not a priority weight. Unknown links are rejected; empty attribution never
defaults to party. The canonical consumer still receives bounded `subject_refs` and
source-grounded subjects. The systematic boundary checkpoint below supersedes the
earlier subject-array validator patch without changing supply policy.

<a id="b-a3aa5e2abc7d-1"></a>

The V1-only planning_supply_1 result contains planning_supply, with selected IDs,
required_canonical_ids, optional_canonical_ids, normal/effective capacity, eligible
count, shortfall, selection-step diagnostics, Profile relations, CPU/wall timings and
zero evaluator/subset-enumerator counts. Historical b2_1 remains a retained schema,
but is not the active runner output. V0 PlanningResult is unchanged.

<a id="b-a3aa5e2abc7d-2"></a>

The model-visible ledger includes required/optional IDs, open normalized semantics,
subjects and uncertain typed review relations. Raw review text/summaries and provider
rank are not exposed as preference truth. Full provenance remains in the application
contract. The exact planner prompt is captured after this projection is appended.
The planner must attempt REQUIRED visits and may use a suitable OPTIONAL subset;
soft trade-offs are allowed. No required-omission repair is implemented.

<a id="b-a3aa5e2abc7d-3"></a>

Weather remains destination/date-based. Routes consume the supplied pool under existing
budgets (eight POIs allow an 8x8 matrix). Official Web stays within existing 6 task/6 page
limits; missing evidence and exhaustion are not permission to expand them. Downstream
facts do not trigger reselection. Itinerary quality remains independently observable.

<a id="m-7a86b41bc19c"></a>
## Offline checkpoint and saved B replay

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7a86b41bc19c-0"></a>

Focused policy/contract/integration plus retained historical policy tests: 193 passed.
Full backend once: 673 passed, 9 skipped. Ruff and git diff --check passed.

<a id="b-7a86b41bc19c-1"></a>

The unchanged saved B input has ten factually eligible enriched candidates. New supply
returns eight, priority indices 1,9,7,6,5,0,3,8 in the saved canonical order. Required
Opera House is retained. Old directional targets do not exist: all Profile relations
remain UNKNOWN; no manual targets or fabricated rank were inserted.

<a id="b-7a86b41bc19c-2"></a>

Relative to B2 counterfactual {1,2,3,4,5,7,8,9}, add Artspace (0) and Finger Wharf (6),
remove Rocks Discovery Museum (2) and Customs House (4). Relative to the offline baseline
{0,1,2,3,4,5,7,9}, add Finger Wharf (6) and BridgeClimb (8), remove 2 and 4. This follows
structural type variety and rating: Justice and Police Museum 4.5 outranks Rocks 4.4,
and Finger Wharf 4.6 outranks Customs House 4.5 within their respective types. The older
baseline had a separately declared walking mapping; this replay does not retrofit it.
These memberships are observations, not hard-coded outputs or a quality benchmark.

<a id="b-7a86b41bc19c-3"></a>

See the chronological implementation/evolution documents for historical B2 evidence.
Live development observations below do not imply V1 freeze or formal research results.

<a id="m-a22c44743d09"></a>
## Bounded live checkpoint: upstream failures (2026-09-19)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a22c44743d09-5"></a>

Recommendation at that checkpoint: keep the implemented supply direction and pause before cleanup/final
V1 review. A narrow Requirement transport/domain alignment pass is needed for reserved
subject identities and short temporary IDs, followed only by separately authorized
bounded live validation. Do not change supply coefficients or restore B2 because the
runs never reached selection. This task's live authorization is exhausted. V1 remains
reopened; B2 code is retained. No V2/V3, refreeze, DB/embedding work, commit or push.

Verbatim passages shared with another maintained section: [1](development_record.md#b-3e60cb9d7939-0), [2](development_record.md#b-3e60cb9d7939-1), [3](development_record.md#b-3e60cb9d7939-2), [4](development_record.md#b-3e60cb9d7939-3), [5](development_record.md#b-3e60cb9d7939-4). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-2d321ca583b2"></a>
## Systematic Requirement boundary checkpoint (2026-09-19)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2d321ca583b2-0"></a>

Implemented and offline validated, not live validated or re-frozen. This supersedes
the proposed narrow follow-up above. The two historical failures remain failed runs.
Adding a reserved-word exception or increasing one discovery-ID limit would leave the
same ownership problem elsewhere: model bookkeeping was mistaken for canonical identity,
and local validators were mistaken for provider-constrained generation.

<a id="b-2d321ca583b2-1"></a>

The active boundary is:

<a id="b-2d321ca583b2-2"></a>

```text
One Requirement LLM / Azure Responses v1, strict dictionary JSON schema
-> SDK response content (optional private development capture)
-> strict JSON parse -> FoundryInterpretationDTO -> InterpretationDraft
-> reference/source validation and lossless application canonicalization
-> InterpretedTripRequirements v2 -> unchanged discovery/evidence/supply/planner consumers
```

<a id="b-2d321ca583b2-3"></a>

The Requirement-only adapter passes a dictionary schema through LangChain `bind` so
the OpenAI SDK uses Responses `create`, preserving completed text before Pydantic
mapping. Other model bindings retain their prior parsing path. Duplicate JSON keys
and partial JSON are rejected, not repaired. The only schema transformation replaces
singleton `const` with equivalent `enum`; no dynamic per-request schema is introduced.

<a id="b-2d321ca583b2-4"></a>

Azure's documented structured-output subset supports required object properties,
enums and nested `anyOf`, with all fields required and `additionalProperties:false`.
It does not support the string-length and array-cardinality keywords needed for these
local bounds. Its documented object-property/nesting limits also apply; local DTO
validation is not proof of remote enforcement. Refusal and incomplete responses need
separate handling. Sources: [Azure structured outputs](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
and [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

<a id="m-31f926517188"></a>
## Invariant ownership

_Source context: Current V1/V2 POI Planning Candidate Supply / Systematic Requirement boundary checkpoint (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-31f926517188-0"></a>

| Invariant | Owner | Implemented check or boundary |
| --- | --- | --- |
| Object shape, primitive types, required fields, enum values, no extra fields | A: provider structure, then local DTO | Final Responses `text.format` is strict; provider refusal/incomplete is not successful extraction |
| Explicit party/specified/unresolved variant and presence of first_ref | A: provider structure, then local DTO | Nested anyOf; first_ref is required for specified, but provider presence does not prove nonblank or resolvable |
| Canonical subject/semantic/named/discovery IDs | B: application canonicalization | Allocate subject_N, semantic_N, named_N, discovery_N; party is application-owned |
| Ordering, exact duplicate consolidation and atomic link rewriting | B | Stable source/content order independent of temporary-handle spelling and order-independent definition order |
| Counts, string sizes, nonblank handles, unique namespaces, reference membership | C: application validation | Draft bounds and exact lookup; no truncation, fuzzy repair or spelling interpretation |
| Source quotes, occurrences, offsets, named surface, information/transport grounding | C | Existing exact occurrence/unique casefold-equivalent policy; source text must actually exist |
| Evidence dimension/value compatibility, disjoint direction, conflicting definitions | C | Shared ALLOWED_VALUES, local validation and canonical linked-pair conflict checks |
| Canonical graph and request association | C | Version, application ID sequence, membership, source offsets and request hash are revalidated |
| Missing trip information or unresolved attribution | D: user clarification | Separate missing-field/clarification outcome, never an invented party or preference |
| Unsupported semantic HARD | Existing application policy | Preserve hard strength and clarify; unknown never becomes verified/pass |

<a id="m-04049742e7ff"></a>
## IDs, references, subjects and bounds

_Source context: Current V1/V2 POI Planning Candidate Supply / Systematic Requirement boundary checkpoint (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-04049742e7ff-0"></a>

- Model-generated discovery `intent_id` and named-place `local_key` are removed: neither
  has an inbound draft reference. Application IDs are allocated only after validation.
- Semantic and declared-subject `local_key` remain opaque temporary handles because
  discovery/evidence and semantic attribution genuinely reference them. Namespaces are
  separate; handles are nonblank and at most 256 characters, independent of canonical
  IDs' 40-character limit. Duplicate definitions within a namespace are rejected.
- Evidence `requirement_ref` is a link to a semantic handle, not a new evidence ID.
  Information requests and evidence requests have no model-authored record IDs.
- Party maps to the sole canonical `party` identity. Specified subjects map to app IDs;
  requester, mother, father and subgroups remain distinct. A temporary handle spelled
  `party` is ordinary data when referenced by `specified`, not a reserved identity.
- Semantic exact duplicates consolidate only when normalized text, kind, polarity,
  strength, scope and canonical subject set match. Source references are unioned within
  the existing limit; aliases rewrite all links. No fuzzy semantic deduplication occurs.
  Identical discovery query/purpose records union their validated links. Conflicting
  evidence directions for one consolidated requirement/dimension fail explicitly.
- Draft bounds: 24 semantic and 24 named items; 8 custom subjects; 8 discovery intents;
  32 information and 120 evidence requests. Semantic text is 320 characters/item and
  6000 total; source quotes are 1..3/item, 320 characters/quote, 12000 source characters
  overall including information/transport. Discovery text is 200/item and 1200 total,
  with 1..4 semantic links. Specified target has one first plus at most seven additional
  refs. Evidence has at most three preferred and three avoided values. Draft serialized
  text is bounded at 180000 characters; received model text at 250000. These are local
  resource checks, not provider generation guarantees. Overflows fail; nothing is cut.

<a id="b-04049742e7ff-1"></a>

Source ordering and stable content tie-breakers determine canonical allocation. Renaming
all handles consistently or permuting independent definitions does not alter canonical
semantics or downstream output. The documented canonical-input path validates an existing
envelope against the original request without renumbering it (idempotence).

<a id="b-04049742e7ff-2"></a>

Illustrative fragments, not complete responses:

<a id="b-04049742e7ff-3"></a>

```json
{
  "before": {
    "subjects": [{"subject_id": "party", "label": "Traveling party"}],
    "semantic": {"local_key": "quiet", "subject_refs": ["party"]},
    "discovery": {"intent_id": "discovery_distinctive_architectural_cultural"}
  },
  "after_wire": {
    "subjects": [],
    "semantic": {"local_key": "arbitrary_temporary_handle", "subject_target": {"kind": "party"}},
    "discovery": {"requirement_refs": ["arbitrary_temporary_handle"], "purpose": "semantic_discovery", "query_text": "Local cultural places"}
  },
  "after_canonical": {
    "semantic": {"requirement_id": "semantic_1", "subject_refs": ["party"]},
    "discovery": {"intent_id": "discovery_1", "requirement_refs": ["semantic_1"]}
  }
}
```

<a id="b-04049742e7ff-4"></a>

For a mother's stated preference the wire uses a declared subject handle and
`{"kind":"specified","first_ref":"mother_handle","additional_refs":[]}`;
it becomes a reference to the source-grounded canonical subject, never to party.
`{"kind":"unresolved","reason":"Unclear pronoun referent"}` requests clarification.
Canonicalization preserves open text, negation, conditions, strength and named inclusion;
source integrity cannot by itself prove that the LLM's semantic interpretation is correct.

<a id="m-a8a2cfa9cf59"></a>
## Failure outcomes and development capture

_Source context: Current V1/V2 POI Planning Candidate Supply / Systematic Requirement boundary checkpoint (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a8a2cfa9cf59-0"></a>

| Outcome | Representation |
| --- | --- |
| Missing operational user information | Existing MissingRequiredFieldsError |
| Ambiguous extraction or unresolved subject | ClarificationRequired with specific code |
| Unsupported HARD | ClarificationRequired: unsupported_hard_requirements; no weakening |
| Invalid model JSON/DTO/draft/source/reference/canonical contract | RequirementBoundaryError: invalid_model_contract, stage and structured errors where available |
| Refusal / incomplete | provider_refusal / provider_incomplete |
| Authentication, permission, bad API request / service or connection failure | configuration_failure / transport_failure |

<a id="b-a8a2cfa9cf59-1"></a>

No additional Requirement or repair LLM is introduced. One invocation, max_retries=0
and existing semantic policy remain. The runner reports boundary failures separately
from user clarification. Local validator errors expose locations/types, not raw inputs.

<a id="b-a8a2cfa9cf59-2"></a>

`DevelopmentRequirementCapture` is explicit constructor injection and defaults to off.
It records exact SDK-exposed model content before JSON/DTO mapping, provider status,
refusal/incomplete details, usage, response ID/hash, call UUID, scenario/request identity,
prompt/schema/config versions and hashes, and later validation outcome. Per-stage UUID
files use exclusive creation; failures cannot overwrite previous calls. Known API keys
and explicitly supplied secret strings are redacted. It does not collect HTTP headers.
The hash identifies pre-redaction content; this is not a byte-exact HTTP-envelope archive.
If no SDK message exists (for example a transport failure), no raw response is invented.

<a id="b-a8a2cfa9cf59-3"></a>

Use a private directory under ignored logs. Capture also creates a local ignore rule;
POSIX files are owner-only, while Windows inherits the directory ACL. The caller must
choose a suitably private Windows directory. This is not general PII anonymization.
Runtime capture write failures are best effort and do not trigger model retries.

<a id="m-abd741882d56"></a>
## Offline evidence and next acceptance boundary

_Source context: Current V1/V2 POI Planning Candidate Supply / Systematic Requirement boundary checkpoint (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-abd741882d56-0"></a>

Final affected suite: **262 passed**. Complete backend, run once after implementation:
**711 passed, 9 skipped** (opt-in local PostgreSQL integration tests). Ruff and
`git diff --check` passed. Actual OpenAI SDK 3.13.0 / langchain-openai 1.6.2 /
Pydantic 2.13.5 / httpx 0.28.1 were exercised via MockTransport, not live endpoints.
The intercepted final wire schema contains 63 object properties. Its schema and
SDK-version audit are retained in ignored development logs.

<a id="b-abd741882d56-1"></a>

Coverage includes 1/44/100/256-character handle renaming crossed with definition
permutation, dangling/duplicate definitions, missing/null/blank attribution, party vs
people/subgroups/shared targets, idempotence, exact dedup link rewriting, condition and
negation survival, HARD preservation, source occurrence/Unicode regressions, direction
compatibility/contradiction/UNKNOWN, canonical tampering, planner/Profile projections,
strict JSON, provider outcome classification, and capture before DTO/canonical failure.
Duplicated wire/domain semantic enum sets and evidence values have parity assertions.

<a id="b-abd741882d56-2"></a>

B has a saved parsed-domain draft, re-expressed explicitly as a v2 test fixture. This
is not an exact raw-wire replay. A's complete invalid DTO was not saved; long-handle
coverage is a synthetic regression, not a reconstructed real response. The earlier B
supply snapshot still lacks preference-direction fields: its replay demonstrates supply
behavior, not full new Profile alignment. Direction tests here use synthetic evidence.

<a id="b-abd741882d56-3"></a>

The prepared `backend/tests/fixtures/requirement_boundary/live_acceptance_cases.json`
contains nine frozen scenarios/checks: solo Kyoto; party-wide Paris; contrasting people
in Barcelona; subgroup Tokyo; shared Vienna; Spanish conditional/negative Lisbon;
German named required/excluded Berlin; genuine missing/ambiguous trip information;
Sydney unsupported HARD plus a required named place. Version requirement_acceptance_1,
reference date 2026-09-19, SHA256
`a9c2e8ed5c6f94efe0247638aa7a8ffe07b23592c08af76b86b48da2ff38dfca`.
Proposed limit: one Requirement call/case, nine total, no retries or downstream providers.
Not executed; separate approval is required. If execution occurs after the fixed dates
expire, revise and re-freeze the date fixtures before running, retaining semantic checks.

<a id="b-abd741882d56-4"></a>

Supply ranking/cardinality, budgets/cache, Review/Profile policy, soft prioritization,
UNKNOWN neutrality, HARD policy, V0 and TripWorld are unchanged by this pass. B2 remains
preserved and inactive. No live/paid calls, embeddings, database rebuild, V2/V3 work,
re-freeze, commit or push occurred. Passing offline checks does not guarantee extraction
for all future language or prove Azure deployment acceptance; that remains a bounded
Requirement-only live question. Stop here before cleanup or further live work.

<a id="m-91477765f294"></a>
## Limited Requirement-only live attempt (2026-09-19)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-91477765f294-0"></a>

Status: **Transport-blocked; no completed model response; not an extraction acceptance pass.**
The user authorized the existing nine cases, at most one invocation each. Requests and checks
were frozen before execution. No production prompt/schema/configuration was changed.

<a id="m-083471c23fdb"></a>
## Frozen manifest

_Source context: Current V1/V2 POI Planning Candidate Supply / Limited Requirement-only live attempt (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-083471c23fdb-0"></a>

Manifest SHA256: `70e8d211825b05f6d79f50e866bfafffa95851576312f0c7aa45212e67caf438`. Reference date: 2026-09-19.
Configured deployment: `gpt-5.6-luna`; prompt requirement_prompt_2; wire requirement_draft_2;
canonical interpreted_requirements_2; execution requirement_execution_1. Exact prompt, wire,
canonical schema, config, endpoint and per-request hashes are in the ignored manifest.
Language coverage was planned as English (7), Spanish (1), German (1); Chinese was absent.
No language has completed live semantic coverage in this attempt.

<a id="b-083471c23fdb-1"></a>

| Case ID | Language | Frozen expected outcome | Actual execution |
| --- | --- | --- | --- |
| solo_requester | en | canonical_extraction | Transport failure |
| whole_party | en | canonical_extraction | Unexecuted |
| contrasting_people | en | canonical_extraction | Unexecuted |
| subgroup | en | canonical_extraction | Unexecuted |
| shared_subjects | en | canonical_extraction | Unexecuted |
| conditional_negation | es | canonical_extraction | Unexecuted |
| named_identities | de | canonical_extraction | Unexecuted |
| missing_information | en | genuine_clarification | Unexecuted |
| unsupported_hard | en | unsupported_hard_clarification | Unexecuted |

<a id="b-083471c23fdb-2"></a>

Exact frozen requests and semantic checks (not changed after observation):

<a id="b-083471c23fdb-3"></a>

**solo_requester**

<a id="b-083471c23fdb-4"></a>

I am travelling alone to Kyoto from 2026-09-21 to 2026-09-23. I enjoy small craft workshops rather than crowded shopping streets. Budget JPY 60000.

<a id="b-083471c23fdb-5"></a>

Acceptance checks: One traveler; requester attribution is source-grounded. Keep craft interest and shopping/crowding avoidance; no invented companions.
Input SHA256: `828683341fc4e0579b1f21dfa25ccd4980b85a0a6eca524950d680275165fa28`.

<a id="b-083471c23fdb-6"></a>

**whole_party**

<a id="b-083471c23fdb-7"></a>

All four of us will visit Paris from 2026-09-21 to 2026-09-23. We all prefer parks to shopping malls. Budget EUR 1200.

<a id="b-083471c23fdb-8"></a>

Acceptance checks: Whole-party preference uses kind=party; no party definition in subjects. Comparison survives normalization; four travelers remain operational metadata.
Input SHA256: `2e3bd4a38682c62253352c7b8be5021fe0aed017ccd2489b7148c78dd95dbfa2`.

<a id="b-083471c23fdb-9"></a>

**contrasting_people**

<a id="b-083471c23fdb-10"></a>

Plan Barcelona for three adults from 2026-09-21 to 2026-09-23. My mother prefers quiet places; my father loves architecture. I enjoy contemporary art.

<a id="b-083471c23fdb-11"></a>

Acceptance checks: Mother, father and requester remain distinct, with correct preference links. Quiet is not automatically a crowding evidence request. Open architecture/art meanings remain available to discovery.
Input SHA256: `b3b300bc49a1464ff7afc03cd760be52f820fd4efdb018cfebd8f0ca8b2f8163`.

<a id="b-083471c23fdb-12"></a>

**subgroup**

<a id="b-083471c23fdb-13"></a>

Our group of five will visit Tokyo from 2026-09-22 to 2026-09-24. The two friends travelling with us want evening food markets. The rest of us prefer early evenings.

<a id="b-083471c23fdb-14"></a>

Acceptance checks: Two friends are a subgroup, not the whole party. Other stated subgroup keeps its contrasting style preference. Do not invent which named individuals belong to an unspecified group.
Input SHA256: `dca7059f458ec4a0ca509a68f097f3dad5cf54f22aa62f59fbb8d5c6e60e9a76`.

<a id="b-083471c23fdb-15"></a>

**shared_subjects**

<a id="b-083471c23fdb-16"></a>

Visit Vienna from 2026-09-21 to 2026-09-23: my mother, my father and me. My mother and I both enjoy art galleries. My father prefers gardens.

<a id="b-083471c23fdb-17"></a>

Acceptance checks: Shared art preference links requester and mother; first_ref order is not priority. Father garden preference stays separate.
Input SHA256: `2e29dac66240327d3958e16338fefbd1cdb66bdfc9d726407b6e1c276359cf8c`.

<a id="b-083471c23fdb-18"></a>

**conditional_negation**

<a id="b-083471c23fdb-19"></a>

Somos dos adultos. Queremos visitar Lisboa del 21 al 23 de septiembre de 2026. Preferimos sitios locales, no atracciones artificiales. Aceptamos viajar mas lejos solo si el lugar es realmente singular.

<a id="b-083471c23fdb-20"></a>

Acceptance checks: Preserve local versus artificial attraction comparison. Farther travel remains conditional on distinctiveness, not an unconditional distance goal. Source quotes remain exact Spanish; normalized semantics may be English.
Input SHA256: `d145d089789fce54dd2dd1dd7a27acce21710118814c64ebfdebf0d3cfd8549e`.

<a id="b-083471c23fdb-21"></a>

**named_identities**

<a id="b-083471c23fdb-22"></a>

Wir sind zwei Erwachsene und besuchen Berlin vom 21. bis 23. September 2026. Wir wollen unbedingt das Brandenburger Tor besuchen, aber nicht den Fernsehturm.

<a id="b-083471c23fdb-23"></a>

Acceptance checks: Named Brandenburger Tor is REQUIRED; Fernsehturm is EXCLUDED. Copy source-supported place surfaces; do not generate Place IDs or duplicate semantic rewards.
Input SHA256: `5f240e5c724e1f0abae9c52b6bfddcc8e143eea8d2f360f4ab6cff710fe36a11`.

<a id="b-083471c23fdb-24"></a>

**missing_information**

<a id="b-083471c23fdb-25"></a>

My sister and her friend discussed a trip. She prefers museums. Can you plan it?

<a id="b-083471c23fdb-26"></a>

Acceptance checks: Do not invent destination or dates. If pronoun attribution is ambiguous, mark unresolved rather than assigning party. Missing required trip information or unresolved attribution requires clarification.
Input SHA256: `512771d004abfc1fad966de0ad9010d07f9122e1bf8e78c0dcc1f134a602126b`.

<a id="b-083471c23fdb-27"></a>

**unsupported_hard**

<a id="b-083471c23fdb-28"></a>

Plan Sydney for two adults from 2026-09-21 to 2026-09-23. Absolutely no stairs anywhere. I definitely want to visit the Sydney Opera House.

<a id="b-083471c23fdb-29"></a>

Acceptance checks: Keep no-stairs HARD; do not soften it or equate accessible with stair-free. Opera House stays operational REQUIRED. Existing unsupported-HARD policy must clarify, with no downstream provider spending.
Input SHA256: `c478c30d6a4f87c78309be71d3779f1dd81a642f92d4ffeba9c7369b42ae6303`.

<a id="m-18b833c32127"></a>
## Execution and four-layer result

_Source context: Current V1/V2 POI Planning Candidate Supply / Limited Requirement-only live attempt (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-18b833c32127-0"></a>

Only `solo_requester` was attempted, through the actual production graph extraction node.
The harness exposes no downstream providers and stops before discovery; date validation
would run only after successful extraction. Both client and SDK max_retries were zero.
An HTTP request hook enforces one attempt per case; on-disk invocation markers prevent
restarting a spent matrix. There was no repair, replacement sample or second attempt.

<a id="b-18b833c32127-1"></a>

| Layer | solo_requester | Other eight cases |
| --- | --- | --- |
| A: Provider/transport | OpenAIConnectionError; no SDK response; provider/schema acceptance unavailable | Unexecuted |
| B: DTO/canonicalization/source/domain | Not reached; no draft or canonical object | Unexecuted |
| C: Semantic fidelity/subjects/negation/conditions/named intent/evidence directions | Not evaluable; no model content | Not tested |
| D: Application | transport_failure, stage transport; expected canonical extraction not reached | Frozen expectations remain untested |

<a id="b-18b833c32127-2"></a>

Observed counts: **1 client invocation, 1 HTTP attempt, 0 completed provider responses,
8 unexecuted cases**. A sent attempt is not proof that the provider accepted or billed
an inference; actual server-side execution is unavailable. No provider-reported usage,
returned model identifier, response ID, refusal/incomplete state or response hash exists.
Input/output/reasoning/cache tokens are unavailable, not zero. Elapsed time for the failed
attempt was 0.453 seconds; this is not successful inference latency.
No median or SLA/accuracy claim is appropriate.

<a id="b-18b833c32127-3"></a>

The capture records call ID `e9a0b55dd46a44a4a958bee172e6a793`, scenario, hashes/versions
and the transport error. No raw model response or canonical output could be preserved
because neither existed at the SDK boundary. No rerun was made to reconstruct them.
No invalid-model-contract defect, missing/invented meaning, subject error or correct
clarification can be established from this attempt. Existing HARD/UNKNOWN policy remains.

<a id="m-0f62311d66b1"></a>
## Artifacts, checks and limitations

_Source context: Current V1/V2 POI Planning Candidate Supply / Limited Requirement-only live attempt (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-0f62311d66b1-0"></a>

Ignored artifact root: `logs/requirement_live_20260919/`.
- `manifest.json` / `manifest.sha256`: fixed inputs, expected outcomes and hashes.
- `wire_schema.json`: actual adapter schema frozen before the invocation.
- `solo_requester/result.json`: elapsed time, counts and classified error.
- `solo_requester/responses/d0f008f9e4b742d38f5f3e1b7c9c3d27.json`: sanitized error metadata only.
- `acceptance_review.json` / `artifact_hashes.json`: four-layer results and file hashes.

<a id="b-0f62311d66b1-1"></a>

Result artifact SHA256: `82016bf12a85357c57e49004632b9a26202714ccfc7122c71cecd2f71af28c77`.
Error capture SHA256: `0fcecc9afb9dc3ee60e245c09fe2579adeaa07393c10efb0cde1c74432b2d7da`.

<a id="b-0f62311d66b1-2"></a>

Before live execution the harness had an import-path error; it made zero network/model
calls, was corrected before freezing, and passed a fake production-node dry-check.
This was not a model failure or replacement live sample. No production logic was edited.
The complete backend suite was not rerun; only harness/artifact/document checks were used.

<a id="b-0f62311d66b1-3"></a>

Google Places/Reviews/Weather/Routes/Web, Review/Profile LLM, Semantic Evaluator and
Itinerary LLM calls were all zero. No supply/HARD policy changes, B2 cleanup, V0/TripWorld
changes, V2/V3 work, V1 re-freeze, commit or push occurred. The authorized development
archive event is V1A-19; ignored archive files remain ignored.

<a id="b-0f62311d66b1-4"></a>

Recommendation: **not ready for end-to-end supply validation on this evidence**. First
address transport access in a separately authorized diagnostic step. The precise network
cause is not established by the sanitized exception, and no new contract or semantic
defect is demonstrated. Do not tune validators or spend the remaining matrix automatically.

<a id="m-7eea75becaed"></a>
## Network-authorized Requirement continuation (2026-09-19)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7eea75becaed-0"></a>

Status: **Provider compatibility observed; semantic limitations remain; not ready for unqualified end-to-end acceptance.**
The user explicitly authorized the configured Azure endpoint and possible fees after the
initial network-permission rejection. No call occurred at the approval rejection. The prior
0.453-second restricted-network attempt remains separate and is not erased.

<a id="m-c936c794a565"></a>
## Frozen input and harness segments

_Source context: Current V1/V2 POI Planning Candidate Supply / Network-authorized Requirement continuation (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-c936c794a565-0"></a>

All nine exact requests, languages, reference date and expected checks are unchanged from
manifest SHA256 `70e8d211825b05f6d79f50e866bfafffa95851576312f0c7aa45212e67caf438`
listed above. The actual production extraction/date nodes, adapter, prompt and schema were
unchanged. Configured and returned model for all completed responses: gpt-5.6-luna.

<a id="b-c936c794a565-1"></a>

| Segment | Client invocations | HTTP attempts | Completed responses | Note |
| --- | --- | --- | --- | --- |
| Initial restricted-network attempt (historical) | 1 | 1 | 0 | Connection error; delivery unknown |
| Network-authorized segment 1 | 2 | 1 | 1 | Solo completed; whole_party failed before HTTP due to harness lifecycle |
| Remaining seven, harness lifecycle corrected | 7 | 7 | 7 | Only untouched cases; no repeated samples |

<a id="b-c936c794a565-2"></a>

The harness originally closed the SDK client after each case. A no-network reproduction
confirmed that separate ChatOpenAI instances share a cached HTTP client, so closing the
first also closed the second. whole_party failed locally in 0.016 seconds with zero HTTP
attempts; production wrapping classified it as OpenAIConnectionError. This is a harness
failure, not model-content rejection or another proven network failure. It was not retried.
For the seven untouched cases only, the ignored harness removes per-case request hooks
and closes the shared client once at the end. No production lifecycle or parser was edited.
These segments are reported separately, without a combined unexplained acceptance rate.

<a id="b-c936c794a565-3"></a>

Current authorization: **9 client invocations, 8 HTTP requests, 8 completed responses**.
All nine case slots were attempted; whole_party remains untested against the provider.
Including the earlier explicitly reauthorized connection attempt gives 10 historical client
invocations and 9 HTTP attempts, with 8 known completed responses. No automatic retries.
Only the eight completed responses have usage; billing for unavailable responses is unknown.

<a id="m-2670c632d1a7"></a>
## Four-layer observations

_Source context: Current V1/V2 POI Planning Candidate Supply / Network-authorized Requirement continuation (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2670c632d1a7-0"></a>

For all eight completed responses, the provider returned completed, with no refusal or
incomplete state. The actual strict wire schema was accepted. DTO, temporary-reference
resolution, canonical domain and source-offset checks all passed. There was no observed
invalid_model_contract response. This does not imply semantic acceptance.

<a id="b-2670c632d1a7-1"></a>

| Case | Provider / contract | Semantic review | Application outcome |
| --- | --- | --- | --- |
| solo_requester | Completed; DTO/canonical/source/domain accepted | semantic_issue | canonical_extraction |
| whole_party | No HTTP; no DTO/canonical result | harness_unassessed | transport_failure |
| contrasting_people | Completed; DTO/canonical/source/domain accepted | observed_checks_satisfied | canonical_extraction |
| subgroup | Completed; DTO/canonical/source/domain accepted | observed_checks_satisfied | canonical_extraction |
| shared_subjects | Completed; DTO/canonical/source/domain accepted | observed_checks_satisfied | canonical_extraction |
| conditional_negation | Completed; DTO/canonical/source/domain accepted | semantic_issue_and_unexpected_clarification | unsupported_hard_clarification |
| named_identities | Completed; DTO/canonical/source/domain accepted | observed_checks_satisfied | canonical_extraction |
| missing_information | Completed; DTO/canonical/source/domain accepted | correct_application_clarification_but_semantic_issue | genuine_clarification |
| unsupported_hard | Completed; DTO/canonical/source/domain accepted | observed_checks_satisfied | unsupported_hard_clarification |

<a id="b-2670c632d1a7-2"></a>

- **solo_requester**: Requester and craft-over-crowded-shopping comparison preserved. Kyoto is incorrectly promoted from destination to an additional REQUIRED named visit. LOW/HIGH crowding direction is source-supported.
- **whole_party**: No HTTP request. The preceding per-case close shut down a LangChain-cached shared HTTP client. No response or semantic assessment; case not repeated.
- **contrasting_people**: Mother quiet, father architecture, requester contemporary art remain distinct. Quiet stays open; no crowding evidence request. Positive discovery links point to the correct requirements.
- **subgroup**: Two friends and rest of group remain distinct subgroups; evening markets are discoverable, early evenings stay itinerary style. No invented individual identities.
- **shared_subjects**: One art-gallery requirement references mother and requester; father gardens remains separate. No duplicate preference votes.
- **conditional_negation**: Local preference, avoidance and conditional farther-only-if-distinctive meaning survive. Lisboa is also incorrectly a REQUIRED named visit. Artificial-attraction avoidance is labeled HARD, triggering unexpected clarification versus the frozen normal-extraction expectation. That avoidance appears both in a comparative preference and a separate constraint; possible duplicate emphasis, not a measured double reward. Wording of no can admit a strong reading: this is a strength-policy interpretation question, not proof that all negatives should be soft.
- **named_identities**: Brandenburger Tor REQUIRED and Fernsehturm EXCLUDED; original German surfaces, no semantic duplicates, no discovery query for the exclusion.
- **missing_information**: Destination/dates stay missing and application correctly clarifies. Ambiguous She is nevertheless resolved to sister rather than unresolved; source substring integrity cannot prove this attribution. Traveler count 2 is also inferred from people discussing a trip, which does not explicitly establish the final traveling party.
- **unsupported_hard**: No stairs everywhere remains HARD and party-scoped; Sydney Opera House is REQUIRED. No accessibility evidence request or stair-free certification is invented. Existing HARD policy correctly clarifies.

<a id="b-2670c632d1a7-3"></a>

Subject examples from observed canonical outputs:
- Barcelona: mother -> quiet, father -> architecture, requester -> contemporary art; three distinct subject IDs.
- Vienna: one art requirement references mother and requester; father garden requirement is separate.
- Tokyo: two friends and rest of group retain separate subject IDs and different scopes.
- Sydney HARD and Lisbon semantics use the app party identity without custom party definitions.
- Missing-information case violates intended ambiguity handling by selecting sister for She.

<a id="b-2670c632d1a7-4"></a>

No preference priority is derived from first_ref. No demographic/medical attribute was
invented in the completed detailed-person cases. The missing-information traveler count
is an additional inference limitation, not a certified party composition.

<a id="b-2670c632d1a7-5"></a>

Discovery links resolve to intended positive requirements in the inspected outputs.
Negative named Fernsehturm does not become a positive query. The conditional farther
tradeoff stays downstream-only. Only the Kyoto response requests crowding LOW preferred /
HIGH avoided; dimensions and directions are valid. Quiet was not mapped to crowding and
no-stairs was not mapped to accessibility. No completed case tests less walking versus
substantial hiking, so that direction contrast remains offline-only, not live established.
No itinerary or supply reward was measured; overlapping Lisbon wording is a potential
duplicate-emphasis risk, not proof of an actual double reward.

<a id="b-2670c632d1a7-6"></a>

The genuine missing-fields clarification and explicit no-stairs HARD clarification match
application expectations. Lisbon unexpectedly clarifies because of extracted HARD strength.
The application correctly enforced its existing policy on that output; whether ordinary
negative preferences warrant that strength remains a product/semantic interpretation decision.
Do not silently relabel the frozen Lisbon expectation after seeing this response.

<a id="m-372b1b8ff2c7"></a>
## Usage and latency

_Source context: Current V1/V2 POI Planning Candidate Supply / Network-authorized Requirement continuation (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-372b1b8ff2c7-0"></a>

| Case | Seconds | Input | Output | Reasoning (within output) | Cache read | Cache creation reported |
| --- | --- | --- | --- | --- | --- | --- |
| solo_requester | 14.36 | 3513 | 1251 | 932 | 0 | 3510 |
| whole_party | 0.016 | unavailable | unavailable | unavailable | unavailable | unavailable |
| contrasting_people | 10.313 | 3510 | 907 | 430 | 3442 | 65 |
| subgroup | 8.218 | 3515 | 792 | 422 | 3442 | 70 |
| shared_subjects | 8.219 | 3513 | 822 | 438 | 3442 | 68 |
| conditional_negation | 13.313 | 3518 | 1324 | 960 | 3442 | 73 |
| named_identities | 4.454 | 3509 | 370 | 194 | 3442 | 64 |
| missing_information | 5.953 | 3490 | 541 | 306 | 3442 | 45 |
| unsupported_hard | 4.672 | 3509 | 399 | 191 | 3442 | 64 |

<a id="b-372b1b8ff2c7-1"></a>

Completed-response totals: input 28077, output 6406, total 34483 tokens.
Reasoning 3873 is already in output and is not added again. Cache read 24094;
SDK-reported cache creation 3959 is recorded as exposed, without a billing inference.
Completed-case elapsed median 8.218s, range 4.454-14.360s.
Timing covers the Requirement node/local boundary, not just server inference. Nine heterogeneous
case slots and eight responses do not establish an SLA, accuracy rate or travel-planner quality.
Actual completed language coverage: English 6, Spanish 1, German 1. No Chinese; the dedicated
whole-party contrast case is untested, though other responses exercised party representation.

<a id="m-5370546e6da6"></a>
## Preserved artifacts and integrity

_Source context: Current V1/V2 POI Planning Candidate Supply / Network-authorized Requirement continuation (2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-5370546e6da6-0"></a>

Ignored roots: `logs/requirement_live_20260919_network_authorized/` (segment 1) and
`logs/requirement_live_20260919_remaining/` (seven untouched cases, measurements and review).
Each completed call retains SDK-exposed raw content, response-content hash, unique call ID,
usage/status, versions/hashes, draft and canonical output. whole_party retains error metadata
only. Capture directories are private; they required elevated read access for hash inspection.
This read inspection made no network calls. Key redaction is not general PII anonymization.

<a id="b-5370546e6da6-1"></a>

| Case | Response-content SHA256 | Raw capture file (under the corresponding case responses directory) |
| --- | --- | --- |
| solo_requester | 92981e220059acd34bec16a451b882c4f0eb99f27a5c679d68b0fbbcd53a8caa | c23fbb860c1a4ed5b472d815fd6e0340.json |
| whole_party | unavailable | No response |
| contrasting_people | 3980bbefbdfe5cace4c22a978e9676e8aebfc0f20264bb63a0d0c10924979782 | 0a04592c06ff4e9d9b89bc552ef31ea8.json |
| subgroup | 5fb11bef5b082166b5b5359b1414fe88896859c7f0ee9f98ed63378f8950dcf1 | c2fc33dad78347eea1b8380bd39f71fa.json |
| shared_subjects | 1102df69efc89e4b335b562b3f305df33965ec3c65757071f649804612025e0a | 7d0d2577582448cfb5d95647420083b4.json |
| conditional_negation | 471fa529b76d03c2f52f68b1c3b19ac8c1882c15d63d7dad7775125eb791f403 | 9b50611b688a4176820ebeeb3438839f.json |
| named_identities | e91e8e19c76c455fefc63db4f72ed4b15ff6d3aab1a9395b74b8cf7b26af069a | 29a1b7b24c514e15979f5e3bd38812df.json |
| missing_information | e1a0e6d41ef8934be137e13e0fd707ac33ceba15796cadd1069ea72995391756 | 0b8068a78ae6413cb350237c1988900f.json |
| unsupported_hard | 58d1dd3b3604f0402f5d408f70721cf591f8749c1e41870d1e9e5c26fa25cb6c | 8443b813dde148338bbf70010024df5c.json |

<a id="b-5370546e6da6-2"></a>

Exact paths, separate file SHA256 hashes and all capture-stage file hashes are in
`measurements.json`; `semantic_review.json` records the manual per-case assessment.
No credentials or raw response payloads were put in tracked documentation.

<a id="b-5370546e6da6-3"></a>

Only ignored harness/artifact and existing documentation/archive changes were made.
Production-file hashes were compared with the frozen baseline; prompt/schema/config and
supply/HARD/V0/TripWorld were unchanged. Artifact/hash and diff checks passed; no full backend
rerun. Google/Reviews/Weather/Routes/Web, Review/Profile LLM, Semantic Evaluator and Itinerary
LLM calls were all zero. No B2 cleanup, V2/V3, re-freeze, commit or push.

<a id="b-5370546e6da6-4"></a>

Recommendation: **a semantic limitation requires a product decision rather than another
validator patch**. Clarify the boundary between destination and operational named visit,
how ordinary negative preferences imply HARD strength, and how ambiguous attribution
should remain unresolved. The bookkeeping/structured-output boundary now has limited live
evidence, but a valid source substring does not prove the interpretation. Do not add keyword
rules, silently soften HARD, or claim the missing whole-party scenario passed. Stop before
any production changes, repeated case or end-to-end supply validation.

<a id="m-5870f2578698"></a>
## Requirement semantics alignment policy (2026-09-19, policy version 1)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-5870f2578698-0"></a>

This policy is defined before the next prompt/matrix change. Keep the structural v2
contract, one Requirement call, canonical IDs and existing unsupported-HARD policy.

<a id="m-18cb27a242a6"></a>
## Audit of the prior frozen requests

_Source context: Current V1/V2 POI Planning Candidate Supply / Requirement semantics alignment policy (2026-09-19, policy version 1). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-18cb27a242a6-0"></a>

- Kyoto: "I am travelling alone to Kyoto ..." establishes trip scope, not a separate
  required stop. Additional REQUIRED Kyoto is a place-role interpretation error (A).
- Lisbon: "Queremos visitar Lisboa del 21 al 23 de septiembre de 2026" establishes the
  trip destination in context; a duplicate required visit is not justified by its name.
- Full Spanish preference: "Preferimos sitios locales, no atracciones artificiales.
  Aceptamos viajar mas lejos solo si el lugar es realmente singular." The first sentence
  can mean a tradeable comparative preference OR an actual exclusion. Its strength is
  genuinely ambiguous (B); freezing normal extraction as the only correct outcome was
  over-specific (C). The farther-only-if-distinctive condition was preserved; different
  English normalization is not an error (D). Keep the original run/expectation unchanged.
  Prospective audit expectation v2 accepts grounded strength clarification; it does not
  retroactively turn the old result into a new validation or certify its HARD reading.
- "My sister and her friend discussed a trip. She prefers museums." does not disambiguate
  She or establish the final traveling party. Assigning sister and total count two adds
  unsupported certainty (A arising from B). Missing destination/date clarification was
  correct but does not validate those inferences.
- The previous whole_party slot failed in the harness before HTTP. It is neither a
  model failure nor a semantic success and is explicitly authorized for one new attempt.

<a id="m-2b2d52fb4322"></a>
## Rules

_Source context: Current V1/V2 POI Planning Candidate Supply / Requirement semantics alignment policy (2026-09-19, policy version 1). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2b2d52fb4322-0"></a>

1. Destination describes trip geographic scope, not automatically an additional named
   required visit. A named target requires source context showing an intended visit/stop.
   Cities, towns, districts and areas may legitimately be explicit visit targets. "Want
   to visit" and "hope to visit" can express expected inclusion; optionality and hearsay
   are distinct. No destination-equality deletion, geographic-type ban, name list or
   capitalization/regex rule. Unsupported multi-destination scope uses extraction issues
   for clarification rather than being disguised as a single named POI.
2. Polarity and strength are independent. Ordinary favorable/negative preferences are
   tradeable. Genuine prohibitions, inability and non-negotiable conditions retain HARD.
   No isolated word or translation determines strength. Materially ambiguous strength
   uses existing extraction issues/clarification; no application keyword classifier.
3. Mentioned person, confirmed traveler, preference owner and total party size differ.
   Resolve pronouns with sufficient context; do not choose a nearby antecedent over other
   plausible ones or reject all pronouns. First-person within a group is not whole-party.
   Count requires explicit total or a complete unambiguous participant description.
   Partial lists, advisers, ambiguous pronouns and "we" alone do not prove a total.
   Keep unknown count null and ambiguous ownership unresolved.
4. Request context-bearing source spans for role, ownership, prohibition/tradeoff and
   participation, within existing bounds. Name/pronoun occurrence alone does not prove
   meaning. Application offsets/reference checks establish source integrity, not entailment.

<a id="b-2b2d52fb4322-1"></a>

Existing fields express these decisions: destination, nullable traveler_count, named
inclusion, polarity/strength, subject_target and extraction_issues. Operational traveler
count has no dedicated source-span field; retain its context in the original request and
inspect grounding during development. Do not invent a new provenance field. Ambiguous
attribution/strength cannot produce a released partial canonical plan: current policy
clarifies the request. No new semantic ontology, model judge or repair call is introduced.

<a id="m-6e53d6cffcba"></a>
## Semantics alignment implementation and fixed live checkpoint

_Source context: Current V1/V2 POI Planning Candidate Supply / Requirement semantics alignment policy (2026-09-19, policy version 1). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6e53d6cffcba-0"></a>

Implemented policy version 1 after the preceding audit, before any new invocation.
The original nine-case requests/expectations and prior failed runs are untouched. The
prospective Spanish audit v2 records ambiguity without crediting the old HARD response
as a newly successful run. This is qualitative development/model-assisted inspection,
not an independently human-annotated benchmark.

<a id="m-b7687f73dd87"></a>
## Exact production change and offline checks

_Source context: Current V1/V2 POI Planning Candidate Supply / Requirement semantics alignment policy (2026-09-19, policy version 1) / Semantics alignment implementation and fixed live checkpoint. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-b7687f73dd87-0"></a>

Only V1 Requirement prompt instructions changed, plus its diagnostic version label to
requirement_prompt_3. Added context-based destination/visit distinction, independent polarity
and strength, sufficient-context pronouns, complete participant-count evidence and contextual
source quotes. Contrasts use Oslo/Grunerlokka and compromise versus inability, not Kyoto/
Lisboa/She patches. No output schema, model settings, canonicalizer, validator, source rule,
HARD release policy, supply or budget change. Current fields suffice; no new semantic enum.
The exact added prompt text is preserved below:

<a id="b-b7687f73dd87-1"></a>

```text
Keep mentioned people, confirmed travelers, preference owners and total party size distinct.
Set traveler_count only from an explicit total or a complete, unambiguous participant list.
Partial lists, advisers, pronouns or 'we' alone do not establish the total; otherwise use null.
Polarity is independent of strength: ordinary avoidance is tradeable; genuine prohibitions,
inability and non-negotiable conditions are not. Interpret the full context, never an isolated
word or translation such as no/only/must/want/hope. If materially ambiguous, report the issue
in extraction_issues for clarification instead of inventing hard or soft certainty.
Contrast: 'prefer to skip crowds, but can compromise' is soft; 'cannot tolerate any stairs'
is HARD. Positive wishes may still express expected named visits.
Choose spans with relevant role, ownership, participation and prohibition/tradeoff context,
not just an isolated name or pronoun. Source occurrence alone does not prove the assigned meaning.
Resolve a pronoun when context supports its owner; do not choose the nearest of multiple
plausible antecedents. Preserve genuine ambiguity with subject_target kind=unresolved.
Do not mark every pronoun ambiguous: an explicitly identified speaker can own a later preference.
Destination is trip geographic scope, not automatically an extra REQUIRED visit. A named target
needs evidence of an intended actual visit/stop. Cities, towns, districts and areas CAN be
explicit visit targets; do not remove one merely because its name matches the destination.
Contrast: 'Plan a trip based in Oslo' sets scope; 'include Grunerlokka as a stop' requests a visit.
'I want/hope to visit X' can mean expected inclusion; 'if time permits' is optional and a
friend's recommendation alone is not a required visit. Use context rather than keyword rules.
If multiple destinations cannot be represented faithfully, record an extraction issue rather
than disguising the unsupported scope as a required POI.
```

<a id="b-b7687f73dd87-2"></a>

System prompt tokens: 1657 -> 2054 (+397); output schema is unchanged. Prompt SHA256:
`87fc57f14449c19abb44908a28a29a10188da3c35f8ca16e7511ade273e834f3` (raw UTF-8 text).
Capture hashes use sorted JSON serialization and therefore differ from raw text/file hashes.

<a id="b-b7687f73dd87-3"></a>

New reusable development harness scripts/requirement_acceptance.py runs the production
extraction/date nodes with one matrix-owned SDK client. It attaches/removes one request
hook per case and closes once at matrix end; no production client-ownership change.
It freezes hashes, prevents spent-matrix restarts and counts client invocations, HTTP
attempts and completed responses separately. Raw capture precedes parsing; unique files
and call IDs preserve invalid outputs. No downstream service is available to the harness.

<a id="b-b7687f73dd87-4"></a>

Offline: 13 new focused representation/harness tests passed; affected suite 275 passed.
Full backend ran once after changes: **724 passed, 9 skipped** (opt-in PostgreSQL). Ruff
and git diff checks passed. Fake outputs cover scope-only destination, attraction/area
visits, soft negative/HARD, clear/unresolved pronouns and complete/null counts. MockTransport
covers three sequential cases on one client, invalid middle response retention, unique IDs,
configuration/pre-HTTP failures, counters, no grading text in requests, no overwrite and
no forced clarification for null count. These prove representation/program behavior, not
language understanding. No full-suite rerun followed the live matrix.

<a id="m-75a680830775"></a>
## Frozen matrix and observations

_Source context: Current V1/V2 POI Planning Candidate Supply / Requirement semantics alignment policy (2026-09-19, policy version 1) / Semantics alignment implementation and fixed live checkpoint. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-75a680830775-0"></a>

Manifest digest: `f4f4658da71384504165af569860dbc0d6a674c5d8eb3c580f8da88673e5c956`.
Reference date 2026-09-19; trip dates 2026-09-21 through 2026-09-23.
Exact requests and pre-run checks: backend/tests/fixtures/requirement_boundary/semantic_acceptance_cases.json
(Chinese requests stored as JSON Unicode escapes; labels/checks remain English).
Full immutable manifest with each input hash, prompt/schema/config/code hashes:
logs/requirement_semantics_20260919/live/manifest.json. No labels/checks were sent to the model.
Four same-language contrast pairs plus the previously failed whole_party slot and one
held-out German combination: Chinese 4, English 3, Spanish 2, German 1.

<a id="b-75a680830775-1"></a>

| Case | Language | Frozen expectation | Actual application | Canonical output | Semantic inspection |
| --- | --- | --- | --- | --- | --- |
| destination_scope_zh | zh | canonical_extraction | canonical_extraction | Validated | satisfied |
| area_visit_zh | zh | canonical_extraction | canonical_extraction | Validated | satisfied |
| avoidance_soft_es | es | canonical_extraction | canonical_extraction | Validated | satisfied |
| prohibition_hard_es | es | unsupported_hard_clarification | unsupported_hard_clarification | Validated | satisfied |
| pronoun_clear_en | en | canonical_extraction | canonical_extraction | Validated | satisfied |
| pronoun_ambiguous_en | en | genuine_clarification | genuine_clarification | Not released: extraction issue | satisfied |
| count_complete_zh | zh | canonical_extraction | canonical_extraction | Validated | satisfied |
| count_incomplete_zh | zh | canonical_extraction | genuine_clarification | Not released: extraction issue | material_outcome_mismatch |
| whole_party | en | canonical_extraction | canonical_extraction | Validated | satisfied |
| combined_heldout_de | de | canonical_extraction | canonical_extraction | Validated | satisfied |

<a id="b-75a680830775-2"></a>

- **destination_scope_zh**: Taipei only as destination; no named visits; two adults and dates correct.
- **area_visit_zh**: Dadaocheng REQUIRED with the full actual-stop clause as source; Taipei remains scope only.
- **avoidance_soft_es**: Avoid commercial attractions is medium-strength preference with compromise retained; no HARD or fabricated evidence mapping.
- **prohibition_hard_es**: Non-negotiable commercial-attraction exclusion is HARD; correct unsupported-HARD clarification, not a failure.
- **pronoun_clear_en**: Sister owns museums; two travelers explicit; no party substitution.
- **pronoun_ambiguous_en**: Owner unresolved with both alternatives stated, no guessed antecedent; existing extraction_ambiguity clarification occurs before canonical release.
- **count_complete_zh**: Exclusive complete participant list supports three travelers; no invented semantics or named visits.
- **count_incomplete_zh**: Count correctly remains null, but model adds an extraction issue solely for optional count uncertainty. This blocks although destination/date are complete and count is not mandatory. Expected normal release remains frozen; do not relabel this as success.
- **whole_party**: Party-wide parks over malls, four travelers, budget and dates preserved; app party requires no custom subject; positive park query only.
- **combined_heldout_de**: Hope to visit Miniatur Wunderland is REQUIRED, Reeperbahn EXCLUDED, Hamburg scope only; quiet is soft and party-wide, not crowding evidence.

<a id="b-75a680830775-3"></a>

All ten provider responses completed and all ten transport DTO/draft validations passed.
Eight canonical envelopes were produced/validated, including the explicit HARD case that
correctly clarifies later. Two extraction-issue cases exit before canonical release, so
do not claim all ten completed canonical/domain/provenance validation. Their literal source
quotes were inspected post-run; that does not create a canonical result or prove entailment.
No refusal, incomplete output, invalid-model-contract rejection or harness failure occurred.
The previous whole_party harness failure remains historical; this newly authorized call is
a new result, not a retroactive repair.

<a id="b-75a680830775-4"></a>

Critical remaining finding: optional uncertainty is promoted to a blocking extraction issue.
The count-incomplete source explicitly names some participants and allows additional people.
The model correctly emits traveler_count=null and unresolved_fields=[traveler_count], but also:
```text
The total party size is unresolved because the request names three participants but also says there may be additional people.
```
Current canonicalization clarifies whenever extraction_issues is nonempty. The production
mandatory fields are destination/start_date/end_date, so this is an unnecessary refusal to
continue relative to the frozen policy. It is NOT fabricated count, malformed references
or a justified rewrite of the expected outcome. General class: optional unknown versus
material ambiguity that must block. Keep this result; no prompt/validator fix or retry here.

<a id="b-75a680830775-5"></a>

Other critical checks showed the intended distinctions in these samples: no destination
duplicate visits, no soft-avoidance-to-HARD conversion in the explicit tradeable pair, no
weakening of explicit prohibition/exclusion, no guessed ambiguous owner, no invented total.
Complete normal requests proceeded. Noncritical differences in wording, scope choice and
low versus medium SOFT strength were not treated as failures. Some source spans still omit
helpful contextual words (German hope), despite correct inspected intent; raw request context
remains necessary. No application entailment guarantee is claimed.

<a id="m-a87d0fd4c321"></a>
## Measurements and artifacts

_Source context: Current V1/V2 POI Planning Candidate Supply / Requirement semantics alignment policy (2026-09-19, policy version 1) / Semantics alignment implementation and fixed live checkpoint. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a87d0fd4c321-0"></a>

Configured and returned model: gpt-5.6-luna. Exactly **10 client invocations, 10 HTTP attempts,
10 completed responses**, no unexecuted cases, repairs, retries or replacement samples.
Previous matrix counters remain separate. Current request bodies/output schema/settings
were fixed throughout, verified by per-case implementation hashes.

<a id="b-a87d0fd4c321-1"></a>

| Case | Seconds | Input | Output | Reasoning within output | Cache read | Cache creation reported |
| --- | --- | --- | --- | --- | --- | --- |
| destination_scope_zh | 4.547 | 3894 | 205 | 91 | 0 | 3891 |
| area_visit_zh | 5.344 | 3909 | 419 | 261 | 3839 | 67 |
| avoidance_soft_es | 4.547 | 3904 | 388 | 196 | 3839 | 62 |
| prohibition_hard_es | 5.516 | 3907 | 443 | 247 | 3839 | 65 |
| pronoun_clear_en | 7.39 | 3906 | 657 | 411 | 3839 | 64 |
| pronoun_ambiguous_en | 8.859 | 3903 | 796 | 476 | 3839 | 61 |
| count_complete_zh | 4.438 | 3894 | 335 | 222 | 3839 | 52 |
| count_incomplete_zh | 5.484 | 3899 | 396 | 259 | 3839 | 57 |
| whole_party | 5.953 | 3907 | 506 | 290 | 3839 | 65 |
| combined_heldout_de | 8.891 | 3933 | 841 | 547 | 3839 | 91 |

<a id="b-a87d0fd4c321-2"></a>

Totals: 39056 input + 4986 output = 44042 tokens. Reasoning 3000 is included
in output. Cache read 34551; SDK-reported cache creation 4475, without billing inference.
Elapsed median 5.500s, range 4.438-8.891s. No cost estimate, SLA,
accuracy generalization or latency comparison to the different prior matrix is justified.

<a id="b-a87d0fd4c321-3"></a>

Private ignored root: logs/requirement_semantics_20260919/live/. Each case retains raw SDK
content, hashes/versions/usage/state, draft, classified outcome, and canonical output when
available. measurements.json contains exact raw paths, file/content hashes and stage-file
hashes; semantic_review.json contains separate transport/structure/place/strength/subject/
count/source/application judgments. prompt_change.diff and original_expectation_audit_v2.json
are preserved in the parent ignored directory. No raw response or credential was committed.

<a id="b-a87d0fd4c321-4"></a>

All Google/Reviews/Weather/Routes/Web, Review/Profile LLM, Semantic Evaluator and Itinerary
LLM calls were zero. Requirement calls are the only authorized provider calls. V0, TripWorld,
canonical schema/source policy, candidate supply/budgets and HARD release policy are unchanged.
No B2 cleanup, V2/V3, re-freeze, commit or push. Development event V1A-20 records this pass.
No further stage is started.

<a id="b-a87d0fd4c321-5"></a>

Recommendation: **hold end-to-end acceptance pending a narrowly scoped decision on optional
unknowns versus blocking extraction issues**. The explicit critical semantic contrasts have
encouraging bounded evidence, but optional-count over-clarification remains material. Do not
redesign selection or start another live tuning loop. Untested cases include broad ambiguous
negative phrasing, richer mixed-language/pronoun contexts, arbitrary multi-destination scope
and safety constraints beyond these fixtures.

<a id="m-e9c26e3c645a"></a>
## Current V1 Architecture

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-4f7929630380"></a>
## Product scope clarification - 2026-09-19 (accepted scope; alignment NOT implemented)

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-4f7929630380-0"></a>

The product provides a primary sightseeing/experience itinerary plus a small optional,
untimed reference section. It does not organize the entire day or provide reservations,
hotel bookings, payments or booking management. Meals, hotel returns, nightlife and filler
are not mandatory. No fixed daily POI count is introduced. Role follows interpreted visit
intent/context, not place type: a REQUIRED cafe must be a scheduled visit when feasible.
A reference mention never satisfies a REQUIRED visit. Existing exclusion and evidence
boundaries apply to both roles.

<a id="b-4f7929630380-1"></a>

Current runtime still outputs timed activities only. The proposed smallest alignment adds
0..3 untimed references to the shared itinerary, reuses only existing supplied V1 candidates,
and uses the existing generation call. No acquisition, supply capacity or budget increase
is proposed. V0 remains model-only; V1 remains deterministic supply plus bounded evidence.
Detailed unimplemented contract and file/test impact are in the output-role proposal in
docs/poi_selection.md. Earlier full-day completeness critiques are superseded as acceptance
criteria, while the original generated outputs and other quality limitations remain intact.

<a id="m-be97941b2d97"></a>
## Shared structured-input foundation: implemented 2026-09-19

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-be97941b2d97-0"></a>

The user approved a common-baseline migration for V0 and V1, superseding the V1-only
proposal below. Input format and model interpretation are now shared infrastructure;
research versions differ by their evidence/validation mechanisms. No product-engine
switch, V2/V3 implementation, B2 deletion, live calls or re-freeze accompanies this change.

<a id="m-3f55743db696"></a>
## Shared contract and ownership

_Source context: Current V1 Architecture / Shared structured-input foundation: implemented 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-3f55743db696-0"></a>

`backend/app/schemas/request.py::PlanningRequest` is the sole user form for both engines:
required destination, start_date, end_date, traveler_count, budget.amount and budget.currency;
optional additional_preferences defaults to empty. `input_version = planning_request_2`
is internal/defaulted, separate from system_version. Budget remains TOTAL trip Decimal
Money, finite and nonnegative (zero allowed), with three-uppercase-letter currency format.
No conversion, currency inference or traveler multiplier occurs. Count is a strict positive
integer. Date values use YYYY-MM-DD and the existing trusted inclusive ten-day window.

<a id="b-3f55743db696-1"></a>

Omitted/null/whitespace-only preferences normalize to empty. Nonblank text is preserved
exactly, bounded to 24,000 characters and 8,000 tokens. Schema validation and shared preflight
reject malformed inputs before calls, including model_copy/direct runner inputs. Backend
input validity is not budget satisfaction or whole-itinerary feasibility validation.

<a id="b-3f55743db696-2"></a>

`services/preference_interpretation.py` and `services/preference_prompts.py` own the common
boundary. Both graphs use the same prompt, draft/Foundry DTO, configured model client,
canonicalizer and source validators. Read-only form facts and preference text are separate
JSON input fields. Only semantics are model output: named intentions, subjects, open
requirements, conditions/tradeoffs, discovery/evidence links, information and transport
intentions. Extra operational output fields are rejected. Application code constructs
TravelRequirements from the form; no active operational re-extraction model binding remains.

<a id="b-3f55743db696-3"></a>

The canonical contract is interpreted_requirements_3, prompt preference_prompt_4, wire
preference_draft_3. It retains request_sha256 for interpreted preference text, adds
structured_input_sha256, input_version, structured field paths and interpretation_origin.
Source offsets/hash bind to exact preference text, never synthetic form prose. Structured
hashing preserves Decimal precision. IDs remain application-owned and discovery-source neutral.
Private capture remains opt-in; origin skipped_empty is not fabricated model success.

<a id="m-cd817372a3a5"></a>
## Execution and conflicts

_Source context: Current V1 Architecture / Shared structured-input foundation: implemented 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-cd817372a3a5-0"></a>

Empty text constructs empty semantics and skips interpretation in both engines. V0 runs
plain itinerary generation from form/context and model knowledge, without discovery,
Google IDs, external evidence, Reviews/Profile, vector search or supply gates. Named
REQUIRED/OPTIONAL/EXCLUDED intentions reach generation as user-mentioned names. V1 runs
existing destination-default discovery, factual gates and bounded deterministic supply;
no experience request means no selection-driven Reviews. Default queries are system policy,
not invented user preferences. Existing provider shortfalls remain observable.

<a id="b-cd817372a3a5-1"></a>

Nonempty text invokes one shared semantic call. Up to six operational_conflicts identify
one of destination/start_date/end_date/traveler_count/budget.amount/budget.currency plus
1-3 grounded quotes, without replacement values. The application validates references,
preserves form facts and returns structured_input_conflict clarification before downstream
work. Mentioned relatives never mechanically change count. There is no keyword parser or
repair call in the shared boundary. Model conflict detection may miss meaning; source and
shape checks do not prove semantic completeness.

<a id="b-cd817372a3a5-2"></a>

Existing extraction ambiguities and unsupported-HARD clarification remain blocking. The
current HARD assessment has no provider dependency: no registered predicate certifies
arbitrary semantic text, so sharing it does not require V0 to acquire V1 evidence. This is
input-policy handling, not V3 validation. V1 identity resolution, eligibility, dedupe,
Details, Review mappings, ranking, capacities and budgets are unchanged. V1 generation
still receives resolved required identities, optional candidates, shared semantics/subjects,
current evidence and uncertainty. No evaluator or minimum-covering-set objective returns.

<a id="m-f44877078e77"></a>
## Entry points, cleanup and compatibility

_Source context: Current V1 Architecture / Shared structured-input foundation: implemented 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f44877078e77-0"></a>

- `/api/planning` accepts the common form and STILL uses PlanningService -> V0.
- `/api/dev/planning` keeps its existing V0 engine support with an explicit envelope:
  version, request (the same form), optional controlled reference_date. No new V1 HTTP
  dispatch is implied; V1 remains independently runnable through its runner/CLI.
- Both runners validate the same request. Both CLIs accept `--input-json FILE`; obsolete
  free-text `--request` no longer bypasses required input. Date overrides remain development-only.
- `scripts/requirement_acceptance.py` freezes complete structured cases and calls the common
  interpreter directly, not a V1-only graph. Empty cases record skipped_empty with zero calls.
  Versioned A/B/HARD examples are in `shared_structured_cases.json`; they have not run live.
- Removed obsolete TravelRequest, synthetic form-to-prose serialization, V0 extraction
  prompt, operational extraction DTO/mapping/binding, duplicated missing-extracted-field
  handlers and the unused earlier size validator. Semantic prompts moved to shared ownership.
  Preserved B2 experiments; their fixture builder was adapted, not deleted.
- Historical free-text fixtures/results are preserved. Tests of the superseded extraction
  path were explicitly migrated to form authority. No exact historical output parity is claimed.
- Frontend remains unchanged: optional budget and the free-text developer form are mismatches.
  Complete product submissions can use the backend; UI migration is not complete.

<a id="b-f44877078e77-1"></a>

Future V0/V1 comparisons must use the same shared-foundation revision and compatible model
configuration; old-input V0 measurements cannot be mixed with revised V1 and described as
only a tool-access difference. No formal benchmark is authorized or conducted.

<a id="m-e9d5d07e943f"></a>
## Offline checkpoint and next approval

_Source context: Current V1 Architecture / Shared structured-input foundation: implemented 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e9d5d07e943f-0"></a>

Affected offline regression: 657 passed. Final focused shared-boundary/harness check:
56 passed. The complete backend suite ran once: **769 passed, 9 skipped** (14.79 seconds).
The nine skipped tests require an explicitly enabled isolated PostgreSQL test database;
no database was started or rebuilt. `ruff check .` and `git diff --check` passed. All model/provider behavior used fakes or MockTransport;
no live calls, embeddings, database rebuilds or paid operations were performed.

<a id="b-e9d5d07e943f-1"></a>

Proposed separate live approval: one complete empty-preference case and one complete
meaningful-preference case through each engine (four runs, no automatic repetitions), plus
one complete unsupported-HARD Requirement-only case. Fix form/dates, request counts, tool
budgets and stop conditions before execution. Verify 0/1 interpretation calls, V0 zero
external calls, V1 default supply/no empty-preference Reviews, and conflict/HARD behavior.
This plan is not live authorization. Stop after implementation and offline validation.

<a id="m-b955f4e053db"></a>
## Superseded V1-only proposal (historical design, not the active contract)

_Source context: Current V1 Architecture. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b955f4e053db-0"></a>

Status: request-boundary design checkpoint, 2026-09-19. The user now requires complete
structured trip inputs and one optional preference field. This specification supersedes
the earlier proposal to treat missing traveler count as an ordinary valid product request.
Historical free-text tests, acceptance results and their original expectations remain
historical evidence; they do not validate this new boundary. The implementation and
historical checkpoint descriptions below have not been retroactively changed.

<a id="m-346a06f73ee2"></a>
## Actual boundary audit

_Source context: Current V1 Architecture / Superseded V1-only proposal (historical design, not the active contract). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-346a06f73ee2-0"></a>

| Current component | Actual behavior | Proposed change |
| --- | --- | --- |
| `api/schemas/planning.py`: ProductPlanningRequest | Structured destination/dates/count; optional Money; optional nonblank additional_preferences | Use a V1-specific required-input contract; accept empty preferences |
| `api/product/planning.py`, `services/planning.py`, API dependencies | `/api/planning` serializes the form to prose and calls V0 through PlanningService | Explicitly route the product endpoint to a V1 adapter; never round-trip form values through extraction |
| `api/developer/planning.py` | Free-text developer endpoint supports only version v0 | Preserve its V0 behavior |
| V1 runner/state/CLI (`scripts/run_v1.py` delegates to runner) | TravelRequest.request_text, not structured trip fields | Accept the same validated V1 request as the product API; CLI reads structured JSON |
| `scripts/requirement_acceptance.py` and earlier development harnesses | Free-text cases; call extraction/canonicalization using original request text | Add explicitly versioned structured cases through the production boundary; retain old cases as historical |
| V1 graph/prompt and Foundry Interpretation DTO/mapping | Model returns operational TravelRequirements plus semantics; graph uses the V0 request-text prompt builder | V1-only semantic draft and prompt; application supplies operational requirements |
| `policies/interpreted_requirements.py` | Validates source quotes and links, assigns IDs, hashes the original free-text request | Reuse validators with separate form provenance and immutable preference text |
| V1 itinerary prompt and planner projection | Prompt still accepts TravelRequest; supply projection preserves REQUIRED/OPTIONAL ledger | Consume validated form fields and canonical semantics without another operational extraction |
| Frontend form/types | Budget is optional; posts to `/api/planning` | Future UI alignment needed; no frontend implementation in this task |

<a id="b-346a06f73ee2-1"></a>

Paths in the table are relative to `backend/app` unless explicitly qualified. Existing
product API tests currently test V0-backed behavior. Their old results cannot be described
as structured V1 acceptance. Repointing the product route is an explicit migration, not
an incidental dependency change. Keep independent V0 runner and developer API unchanged.

<a id="m-357abef40975"></a>
## Required input and validation

_Source context: Current V1 Architecture / Superseded V1-only proposal (historical design, not the active contract). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-357abef40975-0"></a>

Introduce one `V1PlanningRequest` in `backend/app/schemas/v1_request.py`, with a defaulted
literal `input_version = "v1_structured_1"` and optional existing request ID. Do not
change shared V0 TravelRequest or the requiredness of shared TravelRequirements.

<a id="b-357abef40975-1"></a>

| Field | Proposed rule |
| --- | --- |
| destination | Required nonempty trimmed string |
| start_date, end_date | Required date values; end >= start; reuse the trusted inclusive ten-day window, reference date through reference date + 9 days |
| traveler_count | Required integer >= 1; reject booleans and fractional values rather than coercing them |
| budget | Required Money object with required amount and currency |
| budget.amount | Finite point-valued Decimal >= 0; reject booleans, ranges and malformed amounts |
| budget.currency | Explicit uppercase three-letter code using existing Money validation; no currency-symbol inference |
| additional_preferences | The only optional text field; omitted/null/whitespace-only becomes empty string; preserve nonblank text exactly |

<a id="b-357abef40975-2"></a>

Existing Money uses Decimal with ge=0 and a three-uppercase-letter currency pattern.
This is format validation, not an ISO currency registry. The product serializer explicitly
says **total budget**: preserve total-trip meaning, no traveler multiplier, currency
conversion, per-person reinterpretation or new arbitrary budget cap. Zero remains valid
input; that does not prove an itinerary can satisfy it. Preserve Decimal precision and
reuse Money; place any stricter V1 input checks in the V1 adapter, not shared V0 behavior.

<a id="b-357abef40975-3"></a>

Reject unknown fields, invalid mandatory values and oversized preference input before
model/provider calls. Retain existing preference-input resource bounds (24,000 characters
and 8,000 tokens); do not truncate. Capture the trusted date once per run. Do not accept a
product-supplied reference date override; controlled development fixtures may inject one.
Backend validation applies to HTTP, direct runner and CLI/harness input, not just the UI.
HTTP input failures return 422; CLI/harness return classified input failures with zero
model/provider invocations. Input validity is separate from eventual budget feasibility.

<a id="m-2fe5150cf164"></a>
## Application assembly and the one optional interpretation call

_Source context: Current V1 Architecture / Superseded V1-only proposal (historical design, not the active contract). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-2fe5150cf164-0"></a>

Application code constructs TravelRequirements from the validated operational fields.
Legacy semantic arrays are not populated by guessing preferences. A nonempty preference
field triggers one bounded V1 Requirement interpretation call with two distinct inputs:
read-only structured trip context and the exact preference text. The model returns only
the existing semantic contribution: open requirements, named visit intentions, subjects,
conditions/tradeoffs, discovery/evidence links, requested information and supported
transport intentions, plus bounded issues/overflow. It cannot return destination, dates,
party size or budget. Remove those model-output fields from the V1 draft/Foundry DTO and
mapping; rejecting extra fields enforces authority rather than relying on prompt wording.
Application canonicalization combines that draft with validated operational fields.
V0 TravelRequirements generation and Foundry bindings remain intact.

<a id="b-2fe5150cf164-1"></a>

Empty text builds an empty semantic/named/subject/discovery/evidence/information contribution
without a model call. The structural party target may remain application-owned; it is not
an invented user preference. Existing default discovery uses destination plus `top attractions`,
`local food`, and `museums and cultural attractions`. These are system discovery defaults,
not extracted preferences. Existing factual gates, bounded Details and deterministic supply
continue. No linked experience requests means no selection-driven Reviews or Review LLM.
The itinerary LLM still runs later with structured fields and the REQUIRED/OPTIONAL ledger.
Provider failures or insufficient credible candidates retain current failure/shortfall
behavior; empty preferences do not guarantee a full supply and do not mean empty supply.

<a id="m-74d7173b6302"></a>
## Conflicts, uncertainty and provenance

_Source context: Current V1 Architecture / Superseded V1-only proposal (historical design, not the active contract). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-74d7173b6302-0"></a>

Recommend a minimal bounded `operational_conflicts` extension to the semantic draft:
at most six entries, one per operational field path (destination, start_date, end_date,
traveler_count, budget.amount, budget.currency).
Each entry identifies a field and 1-3 existing source-quote references, using existing
quote bounds. The application assigns `structured_input_conflict`, checks the field and
quote integrity, and returns clarification. There is no proposed replacement operational
value to apply. A later user submission resolves the conflict. This tiny typed extension
is needed because current extraction_issues strings lack field/span linkage.

<a id="b-74d7173b6302-1"></a>

The one semantic LLM recognizes explicit replacement/contradiction, not application
keyword/regex rules. Mentioning mother and father does not imply a new total party size.
Valid form values remain unchanged even when conflict clarification blocks discovery.
Retain other extraction issues and existing blocking HARD policy; do not downgrade all
issues to warnings. Optional semantic uncertainty is distinct from missing mandatory
input, but this migration does not introduce a broader uncertainty-policy relaxation.
Conflict detection is model-mediated and can miss a contradiction; structural validation
does not prove complete semantic detection. Form authority remains protected regardless.

<a id="b-74d7173b6302-2"></a>

Use a new canonical contract version for the changed provenance boundary. Keep
`request_sha256` as a hash of original interpreted text (now the immutable preference
field), never silently redefine it as a hash of synthesized form prose. Add explicit
input-version and structured-input hash/provenance, using deterministic serialization
including exact Decimal normalization, dates and field paths. Semantic source offsets
remain relative only to preference text; model citations into context JSON are invalid.
Empty text has its real empty-text hash and no source spans. Preserve exact nonblank text,
hashes and captures under current privacy controls, not ordinary logs. Distinguish skipped
interpretation from a successful model response in traces. Requirement IDs remain
source/version-independent; the contract version describes structure, not discovery source.

<a id="m-c391bfc155e9"></a>
## Concrete migration/file impact

_Source context: Current V1 Architecture / Superseded V1-only proposal (historical design, not the active contract). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-c391bfc155e9-0"></a>

1. Add the V1 request contract and a shared preflight boundary. Reuse Money/date policy.
2. Adapt `schemas/interpreted_requirements.py`, canonicalization policy, V1 prompts,
   Foundry DTO/mapping/client binding and diagnostic version labels for semantic-only
   output, conflict references and split provenance. No second parser or repair model.
3. Adapt V1 graph/state/runner and itinerary projection to authoritative fields, the
   zero-call empty path and unchanged semantic/HARD checks. Preserve supply and tool budgets.
4. Add a V1 service adapter and deliberately switch `/api/planning` to that adapter via
   product schema/router/dependencies. Keep existing V0 service/developer endpoint behavior.
   Add V1 clarification details (issue code, field, source references) through an explicit
   V1 response mapping; do not silently change V0 response serialization. Preserve the
   product completed response shape where possible and map existing V1 failure/shortfall
   outcomes explicitly rather than claiming success without an itinerary.
5. Migrate V1 CLI to structured JSON input, and the acceptance harness to that exact
   production boundary. Update trace input typing/redaction for V1 without changing V0.
   Older B2/free-text measurement harnesses remain historical, not new product acceptance.
6. Add versioned structured fixtures and offline tests. Preserve historical artifacts and
   old measured outcomes. Update README/API instructions after implementation; record that
   the existing optional-budget frontend needs a separately scoped form update. Do not
   present the product UI as migrated before that integration is complete.

<a id="b-c391bfc155e9-1"></a>

The deliberate product-route cutover rejects formerly accepted missing budgets. Complete
existing form submissions retain familiar field names. This is an intentional product
contract change, while V0's research semantics remain independently runnable. No frontend,
B2 deletion, ranking/supply policy, review semantics, tool-budget, TripWorld or V2/V3 work
belongs in this migration. Implementation still requires approval.

<a id="m-116f02bf3be4"></a>
## Proposed smoke fixtures and offline checks (not executed)

_Source context: Current V1 Architecture / Superseded V1-only proposal (historical design, not the active contract). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-116f02bf3be4-0"></a>

At controlled reference date 2026-09-19, normal A is:

<a id="b-116f02bf3be4-1"></a>

```json
{"input_version":"v1_structured_1","destination":"Sydney, Australia","start_date":"2026-09-21","end_date":"2026-09-23","traveler_count":3,"budget":{"amount":"1800.00","currency":"AUD"},"additional_preferences":""}
```

<a id="b-116f02bf3be4-2"></a>

Normal B is:

<a id="b-116f02bf3be4-3"></a>

```json
{"input_version":"v1_structured_1","destination":"Sydney, Australia","start_date":"2026-09-21","end_date":"2026-09-23","traveler_count":3,"budget":{"amount":"1800.00","currency":"AUD"},"additional_preferences":"I definitely want to visit the Sydney Opera House. My mother prefers quiet places and my father likes architecture. I prefer fewer, deeper visits rather than rushing."}
```

<a id="b-116f02bf3be4-4"></a>

Unsupported-HARD semantic case is:

<a id="b-116f02bf3be4-5"></a>

```json
{"input_version":"v1_structured_1","destination":"Sydney, Australia","start_date":"2026-09-21","end_date":"2026-09-23","traveler_count":3,"budget":{"amount":"1800.00","currency":"AUD"},"additional_preferences":"Absolutely no stairs."}
```

<a id="b-116f02bf3be4-6"></a>

Refresh dates against the trusted clock for a later authorized live run. These are proposed
fixtures, not modified executable fixture files or live results. A expects zero Requirement
calls and no selection-driven Reviews, but permits the unchanged downstream planning calls.
B expects one interpretation and source-grounded semantics. HARD expects semantic-policy
clarification when unsupported, not missing-input failure.

<a id="b-116f02bf3be4-7"></a>

Offline negative tests use fakes/spies and require zero actual network calls:

<a id="b-116f02bf3be4-8"></a>

- Omit/null each mandatory field or nested budget amount/currency; empty destination.
- Invalid dates, reversed range or dates outside the existing ten-day window.
- Malformed, fractional, boolean, zero or negative traveler count.
- Negative/nonfinite/malformed/boolean amount; missing or malformed currency; ambiguous
  currency symbol without a code. No silent currency normalization or inference.
- Non-string or over-budget preference input, unknown fields or unsupported input version.
- For each preflight failure: zero Requirement and zero external-provider invocations.
- Empty/omitted/null/whitespace preferences are positive cases; preserve nonblank whitespace
  and span offsets. With complete input, fake default discovery must supply candidates and
  fake itinerary generation must still run; no semantic preference or Review call invented.
- Complete form plus explicit count/date/budget conflict: one fake interpretation,
  unchanged operational values, source-linked clarification and zero downstream calls.
- Mentioned relatives without an explicit count change must not cause count conflict.
- Model operational overrides, fabricated spans/context citations and broken links fail;
  supported named REQUIRED/OPTIONAL semantics and existing HARD handling remain intact.
- API/runner/CLI/harness converge on the same canonical contract; V0 regressions verify
  the unchanged independent extraction, model binding and response behavior.

<a id="b-116f02bf3be4-9"></a>

After approval: implement boundary and semantics, wire entry points, run affected offline
tests and one appropriate broader backend pass for shared binding/API changes, then stop
and report. Only a separately approved bounded live checkpoint may run A/B/HARD. No new
live calls, runtime tests, code changes, commit, push or re-freeze occurred in this design task.

<a id="m-37f06ab57a1f"></a>
## V0 As-Built Milestone

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-9e0784c2a3a5"></a>
## Research Definition and Scope

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-9e0784c2a3a5-0"></a>

V0 is the plain-LLM research baseline. It uses the configured model's pretrained
knowledge in two structured LLM stages: requirement extraction followed by itinerary
generation.

<a id="b-9e0784c2a3a5-1"></a>

```text
TravelRequest
-> Requirement Extraction
-> TravelRequirements
-> Itinerary Generation
-> Itinerary
-> PlanningResult(system_version="v0")
```

<a id="b-9e0784c2a3a5-2"></a>

V0 provides an explicit, independently runnable baseline for later comparison with
V1, V2, and V3.

<a id="m-dde916530d1e"></a>
## Non-Scope

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-dde916530d1e-0"></a>

V0 does not include:

<a id="b-dde916530d1e-1"></a>

- External tools or web search
- Google Places, routes, weather, or other live information sources
- RAG
- Database persistence
- Memory or a LangGraph checkpointer
- Constraint validation
- Retry, regeneration, repair, or re-validation
- A V0-specific FastAPI planning endpoint
- Benchmark or formal experiment logic

<a id="m-4dc7eb610b95"></a>
## Final Graph Topology

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-4dc7eb610b95-0"></a>

The V0 LangGraph topology is fixed:

<a id="b-4dc7eb610b95-1"></a>

```text
START
-> extract_requirements
-> generate_itinerary
-> END
```

<a id="b-4dc7eb610b95-2"></a>

The minimal `V0State` contains `request`, `reference_date`, `requirements`, and
`itinerary`. A successful run makes exactly one LLM call in each node.

<a id="m-c13ee7b8f2b8"></a>
## Requirement Extraction

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-c13ee7b8f2b8-0"></a>

The `extract_requirements` node receives the original `TravelRequest` and a
`reference_date`. It:

<a id="b-c13ee7b8f2b8-1"></a>

- Extracts only requirements stated by the user or directly resolvable from the
  reference date
- Does not invent a destination, dates, traveler count, budget, activities,
  exclusions, or preferences
- Uses `null` for unknown scalar values
- Records missing or uncertain fields in `unresolved_fields`
- Normalizes explicitly stated currencies to ISO 4217 codes

<a id="b-c13ee7b8f2b8-2"></a>

If `destination`, `start_date`, or `end_date` is missing after extraction, V0 fails
before itinerary generation. An explicitly supplied reference date is used to resolve
relative dates; otherwise, the system's current local date is used.

<a id="m-2ecf7ce4d907"></a>
## Itinerary Generation

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2ecf7ce4d907-0"></a>

The `generate_itinerary` node receives the original request, extracted
`TravelRequirements`, and reference date. It generates a structured itinerary using
only the model's pretrained general knowledge.

<a id="b-2ecf7ce4d907-1"></a>

It does not claim that opening hours, availability, prices, routes, travel times,
weather, events, or disruptions were checked. For every activity start and end, the
Azure Foundry transport representation requires:

<a id="b-2ecf7ce4d907-2"></a>

- `date`: exactly `YYYY-MM-DD`
- `time`: exactly `HH:MM:SS`
- `utc_offset`: exactly `+HH:MM` or `-HH:MM`

<a id="m-12e9892e78b9"></a>
## Shared Domain Schemas

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-12e9892e78b9-0"></a>

V0 uses the provider-independent shared domain schemas:

<a id="b-12e9892e78b9-1"></a>

- `TravelRequest`
- `Money`
- `TravelRequirements`
- `Activity`
- `ItineraryDay`
- `Itinerary`
- `PlanningResult`
- `SystemVersion.V0`

<a id="b-12e9892e78b9-2"></a>

Pydantic validation on these models is the final domain contract. The stable shared
`PlanningResult` contract contains only `system_version`, `requirements`, and
`itinerary`.

<a id="m-fe4327d9b001"></a>
## Azure Foundry and StructuredLLMClient Architecture

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-fe4327d9b001-0"></a>

LangGraph nodes depend only on the provider-independent `StructuredLLMClient`
protocol. They do not depend directly on Azure Foundry, LangChain's OpenAI client, or
provider-specific transport models.

<a id="b-fe4327d9b001-1"></a>

```text
V0 node
-> StructuredLLMClient
-> AzureFoundryStructuredLLMClient
-> Provider-native JSON Schema structured output
-> Azure Foundry DTO
-> Deterministic mapper
-> Shared domain model
```

<a id="b-fe4327d9b001-2"></a>

The Azure Foundry adapter uses `ChatOpenAI` with the OpenAI-compatible `/openai/v1`
endpoint, the Responses API, provider-native JSON Schema structured output with
`strict=True`, and `max_retries=0`.

<a id="b-fe4327d9b001-3"></a>

`LLM_MODEL` records the underlying model used by the system.
`AZURE_OPENAI_DEPLOYMENT` identifies the Azure Foundry deployment passed in the API
request's `model` field. The implementation does not assume that these values are
always identical.

<a id="m-25474f8ea665"></a>
## Azure Foundry DTOs and Deterministic Mapping

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-25474f8ea665-0"></a>

Both structured-output stages use provider-specific transport DTOs:

<a id="b-25474f8ea665-1"></a>

- `FoundryMoneyDTO`
- `FoundryTravelRequirementsDTO`
- `FoundryDateTimeDTO`
- `FoundryActivityDTO`
- `FoundryItineraryDayDTO`
- `FoundryItineraryDTO`

<a id="b-25474f8ea665-2"></a>

The DTOs use strict validation and forbid additional fields. The mapping layer:

<a id="b-25474f8ea665-3"></a>

- Strictly validates ISO dates, times, and UTC offsets
- Constructs timezone-aware domain datetimes from complete transport components
- Converts transport DTOs into the existing shared domain models

<a id="b-25474f8ea665-4"></a>

It does not guess, fill, normalize, repair, or semantically correct values. Missing,
invalid, or ambiguous values fail immediately.

<a id="m-8178f33b38a6"></a>
## Programmatic Runner and CLI

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8178f33b38a6-0"></a>

The programmatic entry point is:

<a id="b-8178f33b38a6-1"></a>

```python
await run_v0(request, llm_client, reference_date=...)
```

<a id="b-8178f33b38a6-2"></a>

The independent command-line entry point is:

<a id="b-8178f33b38a6-3"></a>

```shell
uv run python scripts/run_v0.py \
  --request "Plan a 1-day trip to Kyoto on 2026-10-01 for one traveler." \
  --reference-date 2026-09-11
```

<a id="b-8178f33b38a6-4"></a>

On success, the CLI writes a `PlanningResult` JSON object. It uses ASCII-safe JSON
escaping so Unicode output is safe on Windows GBK/cp936 consoles while preserving the
original Unicode values after JSON parsing.

<a id="m-4d67438bf122"></a>
## Error and Fail-Fast Behavior

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-4d67438bf122-0"></a>

- Missing critical requirements fail after the extraction call and produce CLI exit
  code `2`.
- Extraction provider or schema failures are reported for the
  `extract_requirements` stage.
- Itinerary provider, DTO, mapping, or domain failures are reported for the
  `generate_itinerary` stage.
- Stage and unexpected execution failures produce CLI exit code `1`.
- V0 performs no automatic retry, regeneration, normalization, or repair.
- The Azure Foundry provider client is configured with `max_retries=0`.

<a id="m-cc49d1a8af9f"></a>
## Independent Execution

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-cc49d1a8af9f-0"></a>

V0 is defined under `backend/app/versions/v0/` and remains independently runnable
through `scripts/run_v0.py`. Later versions must use their own explicit graphs and
entry points rather than dynamically modifying the V0 graph. Changes to shared code
must not silently change V0 research behavior.

<a id="m-901201a48354"></a>
## Live Azure Foundry Smoke Tests

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-901201a48354-0"></a>

Development smoke testing confirmed successful Azure Foundry endpoint,
authentication, and deployment connectivity. Synthetic Kyoto, Sydney, and Paris
requests completed the full V0 path, including requirement extraction, DTO conversion,
domain validation, and `PlanningResult` generation.

<a id="b-901201a48354-1"></a>

The final Paris CLI smoke test exited with code `0`, produced valid JSON, and preserved
Unicode content through JSON serialization and parsing. These smoke tests verified the
implementation only; they were not benchmark runs.

<a id="m-9e6e8f42effa"></a>
## Post-Milestone Shared Date-Policy Update

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-9e6e8f42effa-0"></a>

This section records a later approved Stage 0 shared-infrastructure change. The
ten-day date rule described here was not part of the original V0 milestone and must
not be interpreted as original milestone behavior.

<a id="b-9e6e8f42effa-1"></a>

The V0 planner architecture remains unchanged:

<a id="b-9e6e8f42effa-2"></a>

```text
START
-> extract_requirements
-> generate_itinerary
-> END
```

<a id="b-9e6e8f42effa-3"></a>

For requests that satisfy the shared date contract, V0 still makes exactly two LLM
calls and retains the same prompts, Microsoft Foundry model/provider behavior, final
itinerary schema, base planning objective, and plain-LLM generation semantics.

<a id="b-9e6e8f42effa-4"></a>

Stage 0 added the project-wide invariant:

<a id="b-9e6e8f42effa-6"></a>

The final-date check covers the itinerary's top-level start and end dates, every
itinerary-day date, and every activity start/end calendar date. A violation fails
deterministically. V0 does not repair, regenerate, retry, or alter the invalid dates.

<a id="b-9e6e8f42effa-7"></a>

This invariant is a shared V0/V1/future V2/V3 input/output contract, not external
evidence, V1 functionality, or V3-style validation and repair.

<a id="b-9e6e8f42effa-8"></a>

The Product planning path now obtains one trusted backend host-local reference date
at run start. Product clients cannot submit `reference_date`. The independently
runnable V0 CLI, Developer API, and programmatic test interface retain explicit fixed
reference dates as trusted research/testing functionality. The fixed date is captured
once per run so a midnight boundary cannot change the allowed window mid-run.

<a id="b-9e6e8f42effa-9"></a>

Stage 0 regression results after this post-milestone update were:

<a id="b-9e6e8f42effa-10"></a>

- Backend test suite: 91 passed
- V0 version-specific tests: 16 passed
- Ruff: passed
- Frontend tests: 21 passed
- Frontend ESLint and production build: passed
- `git diff --check`: passed

<a id="b-9e6e8f42effa-11"></a>

This update changes only the accepted date contract for V0. It is not a redesign of
the V0 research baseline.

Verbatim passages shared with another maintained section: [1](v1_development.md#b-675836fce13e-1). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-a29cd3670351"></a>
## Purpose and Scope

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a29cd3670351-0"></a>

The Frontend MVP established the minimum complete planning path from a user-facing
React application to the real research planner:

<a id="b-a29cd3670351-1"></a>

```text
React Product UI
-> Product API
-> PlanningService
-> active research planner
-> Azure Foundry
-> structured itinerary
```

<a id="b-a29cd3670351-2"></a>

It also established a separate Developer / Research UI for testing natural-language
requirement extraction and inspecting the complete research response. This milestone
covers only the planning vertical slice; account, persistence, and later research-version
functionality are outside its scope.

<a id="m-58038cad50a8"></a>
## Product and Developer Architecture

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-58038cad50a8-0"></a>

One React + TypeScript application contains two separate route and layout trees:

<a id="b-58038cad50a8-1"></a>

- The Product UI is user-facing and version-agnostic.
- The Developer UI is intended for local development and research and is explicitly
  aware of research versions that actually exist.
- The Product API does not expose research or debug fields such as `system_version`,
  provider or stage details, or research version identifiers.
- The Product UI does not provide a raw JSON or debug panel.
- The Developer UI displays the complete `PlanningResult` and V0 debug errors.

<a id="b-58038cad50a8-2"></a>

The Developer UI has no authentication in this milestone. It must be protected or
disabled before any public production deployment.

<a id="m-8376b4198b9a"></a>
## React Routes and Layouts

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8376b4198b9a-0"></a>

| Route | Layout | Responsibility |
| --- | --- | --- |
| `/` | `ProductLayout` | Product landing page |
| `/plan` | `ProductLayout` | Structured planning form and itinerary display |
| `/dev` | `DeveloperLayout` | Redirect to `/dev/planner` |
| `/dev/planner` | `DeveloperLayout` | Research workbench and raw JSON display |
| `*` | Standalone | Not Found page |

<a id="b-8376b4198b9a-1"></a>

Product and Developer navigation, visual treatment, inputs, and output presentation are
kept separate.

<a id="m-95cd0c51184e"></a>
## Product Planning Form

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-95cd0c51184e-0"></a>

The Product form requires:

<a id="b-95cd0c51184e-1"></a>

- `destination`
- `start_date`
- `end_date`
- `traveler_count`

<a id="b-95cd0c51184e-2"></a>

Budget is optional. If supplied, both `budget.amount` and `budget.currency` are required.
The optional `additional_preferences` textarea is the only free-text Product input.

<a id="b-95cd0c51184e-3"></a>

The Product form does not accept raw `request_text` and does not display a research
version or `reference_date`. The frontend derives `reference_date` from the browser-local
year, month, and day values rather than from a UTC ISO timestamp.

<a id="m-15f551e944e6"></a>
## Product API Contract

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-15f551e944e6-0"></a>

The Product endpoint is:

<a id="b-15f551e944e6-1"></a>

```text
POST /api/planning
```

<a id="b-15f551e944e6-2"></a>

Example request:

<a id="b-15f551e944e6-3"></a>

```json
{
  "destination": "Beijing",
  "start_date": "2026-10-01",
  "end_date": "2026-10-03",
  "traveler_count": 2,
  "budget": {
    "amount": "2000",
    "currency": "AUD"
  },
  "additional_preferences": "Local food and quiet mornings.",
  "reference_date": "2026-09-11"
}
```

<a id="b-15f551e944e6-4"></a>

`budget`, `additional_preferences`, and `reference_date` are optional. `reference_date`
is an internal transport value used for compatibility with the planner interface and is
not a user-facing Product form field.

<a id="b-15f551e944e6-5"></a>

A completed response contains:

<a id="b-15f551e944e6-6"></a>

```json
{
  "status": "completed",
  "requirements": {},
  "itinerary": {}
}
```

<a id="b-15f551e944e6-7"></a>

A defensive clarification response contains:

<a id="b-15f551e944e6-8"></a>

```json
{
  "status": "needs_clarification",
  "requirements": {}
}
```

<a id="b-15f551e944e6-9"></a>

`needs_clarification` covers the defensive case in which the canonical request contains
the structured fields but the active planner still cannot extract them reliably. The
Product UI uses a neutral message and does not imply that the user necessarily omitted an
already completed field.

<a id="b-15f551e944e6-10"></a>

An active-planner failure produces a Product-safe HTTP 502 response without exposing
internal provider or execution details.

<a id="m-e328fd461192"></a>
## Developer API Contract

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e328fd461192-0"></a>

The Developer endpoint is:

<a id="b-e328fd461192-1"></a>

```text
POST /api/dev/planning
```

<a id="b-e328fd461192-2"></a>

Example request:

<a id="b-e328fd461192-3"></a>

```json
{
  "version": "v0",
  "request_text": "Plan a trip to Beijing from 2026-10-01 to 2026-10-03 for 2 travelers.",
  "reference_date": "2026-09-11"
}
```

<a id="b-e328fd461192-4"></a>

At Frontend MVP milestone completion, `v0` was the only accepted version. A successful
response is the complete research-facing `PlanningResult`:

<a id="b-e328fd461192-5"></a>

```json
{
  "system_version": "v0",
  "requirements": {},
  "itinerary": {}
}
```

<a id="b-e328fd461192-6"></a>

The Developer API preserves raw natural-language `request_text`, explicit
`reference_date`, explicit research-version selection, missing-requirement details, and
stage/provider failure details. The Developer UI renders successful and error responses as
raw JSON.

<a id="m-384b2ab7ba8f"></a>
## PlanningService Boundary

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-384b2ab7ba8f-0"></a>

`PlanningService` is the version-agnostic application boundary between the Product API and
the research planners. At Frontend MVP milestone completion, the Product active planner was
V0 and the path was:

<a id="b-384b2ab7ba8f-1"></a>

```text
ProductPlanningRequest
-> deterministic canonical request builder
-> TravelRequest
-> programmatic run_v0(...)
-> PlanningResult
-> Product response mapping
```

<a id="b-384b2ab7ba8f-2"></a>

The integration calls the programmatic V0 entry point that returns `PlanningResult`. It
does not invoke the CLI, capture stdout, or serialize and parse CLI JSON.

<a id="b-384b2ab7ba8f-3"></a>

`DeveloperPlanningService` is a separate version-aware boundary that preserves direct V0
execution and the complete research response. The V0 graph, prompts, runner behavior,
DTO/mapping, and CLI entry point were not modified for this milestone.

<a id="m-455969d67f76"></a>
## Deterministic Canonical Request Builder

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-455969d67f76-0"></a>

`build_canonical_request_text()` is a deterministic pure function that uses only validated
values explicitly supplied in the Product request.

<a id="b-455969d67f76-1"></a>

For the example Product request above, the exact output is:

<a id="b-455969d67f76-2"></a>

```text
Plan a trip to Beijing from 2026-10-01 to 2026-10-03 for 2 travelers with a total budget of 2000 AUD. Additional preferences: Local food and quiet mornings.
```

<a id="b-455969d67f76-3"></a>

The builder does not infer missing information, convert currencies, rewrite preferences,
add activities or purposes, alter dates or traveler counts, or perform semantic
normalization. The Product UI does not display the generated canonical text.

<a id="m-51a542a50e0e"></a>
## Product Validation

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-51a542a50e0e-0"></a>

Frontend validation requires:

<a id="b-51a542a50e0e-1"></a>

- All required structured fields
- An integer `traveler_count` of at least one
- An `end_date` on or after `start_date`
- Both amount and currency when either budget field is supplied
- A non-negative budget amount
- A three-letter uppercase currency code
- No duplicate submission while planning is in progress

<a id="b-51a542a50e0e-2"></a>

Backend Pydantic validation independently enforces the structured contract, date range,
traveler count, budget constraints, and forbidden extra fields. Product requests containing
research fields such as `version` or raw `request_text` are rejected.

<a id="b-51a542a50e0e-3"></a>

Invalid Product requests return HTTP 422 before `PlanningService`, V0, or Azure Foundry is
invoked. Schema and domain validation are therefore present in this milestone. What is not
yet implemented is external-evidence-based feasibility and constraint validation of the
generated itinerary.

<a id="m-f298f9cbd529"></a>
## Separation from Research Versions

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f298f9cbd529-0"></a>

The Product frontend depends only on the stable Product contract and neither imports nor
submits `system_version`. At Frontend MVP milestone completion, the Developer frontend
explicitly exposed only the implemented V0 research version; it contained no V1, V2, or V3
placeholders, disabled panels, or fake implementations.

<a id="b-f298f9cbd529-1"></a>

This separation allows the Product active planner to change behind `PlanningService`
without making research-version selection part of the normal Product experience.

<a id="m-542e2cf525e3"></a>
## Expected Direction After V3

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-542e2cf525e3-0"></a>

After V3 is implemented and independently verified, the Product active planner is expected
to move from V0 to V3 behind `PlanningService`. The core Product API should remain
version-agnostic, and existing Product clients should remain backward compatible. V3 may add
justified user-facing information through backward-compatible optional fields.

<a id="b-542e2cf525e3-1"></a>

The Developer UI should add V1, V2, and V3 only as those versions are actually implemented.
Formal comparison functionality remains subject to separate approval and design.

<a id="m-cdd8194f9ff7"></a>
## Future Product UI Evidence Display

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-cdd8194f9ff7-0"></a>

This is future work, not part of the Frontend MVP or the current Product UI. For a POI
that appears in the final itinerary, a future Product UI may display its actual
acquired Google Places `rating`. If that POI also has retrieved review evidence and
an `ExperienceProfile` summary, the UI may display one concise review-derived
summary. The summary must come from the retrieved reviews and `ExperienceProfile`,
not from the planner's or an LLM's general knowledge. Do not fabricate ratings or
review summaries for POIs without the corresponding acquired evidence. Do not
display `userRatingCount`.

<a id="m-607092cb8921"></a>
## Project context before documentation consolidation

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-607092cb8921-0"></a>

Historical snapshot; [PROJECT](../PROJECT.md) is the current authority.
The following original context and README are preserved without rewriting their checkpoint claims.

<a id="m-8480b542ea32"></a>
## Original PROJECT.md

_Source context: Project context before documentation consolidation. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-2a22b367aec5"></a>
## Capstone Project Context

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-f60b2863a7e4"></a>
## Title

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f60b2863a7e4-0"></a>

**An LLM-Based Travel Planning System for Feasible and Reliable Itinerary Generation**

<a id="m-2e75a015b81c"></a>
## Research Goal

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2e75a015b81c-0"></a>

This project studies how to make LLM-generated travel itineraries more feasible and reliable. A practical motivation is that travelers may not know a destination well enough to recognize hidden errors in a plausible-looking plan.

<a id="b-2e75a015b81c-1"></a>

The system develops through four comparable research versions:

<a id="b-2e75a015b81c-2"></a>

```text
V0  Plain LLM
V1  V0 + external information and tools
V2  V1 + RAG
V3  V2 + explicit feasibility validation, targeted repair, and re-validation
```

<a id="b-2e75a015b81c-3"></a>

The versions should differ mainly by their intended added mechanism. Preserving that distinction is essential for later evaluation.

<a id="m-9731f5d34c9e"></a>
## Current Scope

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-f0b849896c55"></a>
## Post-itinerary nearby references - 2026-09-19 (implemented; offline only)

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f0b849896c55-0"></a>

V1 now finishes and validates its primary itinerary before independent nearby discovery.
Only scheduled, identity-resolved places with existing coordinates are anchors. Application
references are not leftover primary supply; their own Google Nearby ledger supplies identity,
name/address, provenance and attribution. The main itinerary and costs remain unchanged.
V1 has a primary-only model DTO; V0 keeps one tool-free generation with subordinate model
references. Final output stays itinerary_2. No competing V1 model-reference path remains.

<a id="b-f0b849896c55-1"></a>

Reference defaults: 3 requests/trip, 10 results/request, 800 m straight-line radius, 300 m
non-transitive anchor reuse, 10 s phase deadline, at most 4 s/request, no retries, DISTANCE,
restaurant/cafe/park/museum, and 0-3 final references. These are engineering limits, not user
preferences. External acquisition increases by 0-3 Nearby requests; model calls do not
increase. Main acquisition budgets are unchanged. Failures preserve primary output and are
reported independently. Early regions are favored; geographic completeness is not promised.

<a id="b-f0b849896c55-2"></a>

One full backend run: 829 passed, 9 skipped, 8 failed; after fixing obsolete mock DTO/trace
assertions and a phase-timeout scheduling boundary, affected modules passed (53 tests).
Related pre-full checks passed (167 tests); backend Ruff passed. No second full run or live
validation. Prior 813/9/1 history remains intact. Detailed changes/accounting are in
docs/v1_design.md and docs/poi_selection_evolution.md. The sparse two-POI main itinerary and
empty third day remain separate generation-quality limitations. No density validator,
selector redesign, frontend changes, V2/V3, B2 cleanup, commit/push or re-freeze.

<a id="m-9f1f6dbeb820"></a>
## Shared preference policy alignment - 2026-09-19 (offline passed; live blocked)

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-9f1f6dbeb820-5"></a>

**Shared structured-input migration (2026-09-19), implemented and offline validated
(769 passed, 9 skipped); subsequent bounded live recovery is partial with a contract issue,
not re-frozen:** V0/V1 use one `PlanningRequest`
(`planning_request_2`) with required destination, dates, count and total-trip Money budget.
One optional preference field drives a common semantic-only interpreter; empty text skips
that call. Form facts are application-owned. `/api/planning` still dispatches to V0;
V0 remains LLM-only and V1 retains external evidence and deterministic candidate supply.
This explicitly supersedes both optional-count product input and the V1-only compatibility
proposal. Historical freezes/results remain historical; revised comparisons must use the
same shared foundation. Frontend budget/developer-input alignment remains outstanding.
Current details: `docs/v1_design.md` and README. No V2/V3 runtime, B2 deletion, live calls,
commit, push or new freeze is part of this migration.

<a id="b-9f1f6dbeb820-6"></a>

The subsequent authorized five-scenario live matrix completed only V0-E. V1-E supplied
eight optional candidates and acquired downstream evidence before a harness closed-client
failure; both preference cases and HARD also failed before model HTTP. A cached-client
lifecycle error, failed shared-stop guard and model usage capture gap caused that failed run.
A subsequent authorized harness-only reliability pass is implemented and offline validated:
24 focused harness tests and 98 combined affected tests passed, with Ruff/diff checks.
Session-owned injected transports, pre-case readiness, SDK/LangChain response capture and
capture-health stopping replace the disposable loop. That offline checkpoint made no live calls. A separately authorized four-case recovery
subsequently completed saved-evidence V1-E generation and fresh V0-P/V1-P. Shared HARD
returned extraction_ambiguity rather than the frozen unsupported_hard_requirements
expectation: unresolved subject attribution stops canonicalization before HARD readiness.
The current prompt prohibits silently defaulting missing attribution to party; policy and
acceptance expectations need alignment. Nine model calls were captured successfully with
usage and no retries. V1-P supplied eight candidates (one required, seven optional) and
scheduled seven by exact-name audit. V0 output used an incorrect Sydney UTC offset.
No production/harness changes, extra scenarios, or new freeze followed this recovery.
No production behavior changed; no complete backend live acceptance
is claimed. See the 2026-09-19 shared-input entry in docs/poi_selection_evolution.md.

<a id="b-9f1f6dbeb820-7"></a>

The current stage is system design and development: architecture, backend and necessary frontend implementation, provider integration, evidence normalization, runtime configuration, observability, and implementation testing.

<a id="b-9f1f6dbeb820-8"></a>

Formal benchmark design, cross-version evaluation, experiment analysis, thesis writing, and final research conclusions are deferred. Small pilot scenarios and live-provider runs may verify integrations and implementation behavior, but are not formal research results.

<a id="b-9f1f6dbeb820-9"></a>

Introduce infrastructure only when the current version has a concrete need for it. V0 and V1 do not require an application database.

Verbatim passages shared with another maintained section: [1](development_record.md#b-275df2ccd923-0), [2](development_record.md#b-275df2ccd923-1), [3](development_record.md#b-275df2ccd923-2), [4](development_record.md#b-275df2ccd923-3), [5](development_record.md#b-275df2ccd923-4). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-bbedebc3ac9b"></a>
## Research Versions

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-799275ed817a"></a>
## V0 — Plain LLM

_Source context: Research Versions. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-799275ed817a-0"></a>

```text
Structured trip form → Shared optional preference interpretation → LLM generation → Structured itinerary
```

<a id="b-799275ed817a-1"></a>

V0 is the plain-LLM baseline. It does not acquire external planning evidence, use RAG, or perform general feasibility validation and repair.

<a id="b-799275ed817a-2"></a>

V0 may still enforce shared project-level input and output contracts, including the trip-date policy below. For requests valid under those contracts, preserve its requirement extraction, model configuration, output schema, base planning objective, and general generation semantics where practical.

<a id="m-40e4f5c4b799"></a>
## V1 — External Information and Tools

_Source context: Research Versions. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-40e4f5c4b799-0"></a>

V1 adds bounded, application-controlled external evidence to the otherwise comparable V0 planning flow:

<a id="b-40e4f5c4b799-1"></a>

```text
Structured trip form + shared optional preference interpretation
→ External information acquisition
→ Typed evidence normalization
→ Evidence-informed itinerary generation
```

<a id="b-40e4f5c4b799-2"></a>

V1 is **one research version** with two active implementation milestones:

<a id="b-40e4f5c4b799-3"></a>

| Milestone | Purpose | Status |
| --- | --- | --- |
| V1-A | Google-backed travel evidence and POI selection | Revised implementation live-validated and explicitly re-frozen on 2026-09-14 |
| V1-B | Official and current Web evidence for final selected POIs | Phase 1/2 and Phase 3 implemented and development-live-validated |

<a id="b-40e4f5c4b799-4"></a>

**Historical complete V1 was frozen on 2026-09-15** following final offline checks and cross-country development live validation. The original V1-A 2026-09-12 freeze and revised V1-A 2026-09-14 re-freeze remain separate historical checkpoints.

<a id="b-40e4f5c4b799-5"></a>

**V1 explicitly reopened on 2026-09-18. Deterministic planning candidate supply is
implemented and offline validated as of 2026-09-19.** One Requirement LLM preserves open
semantics, subjects, provenance, named identities and discovery/evidence requests.
Canonical factual gates, bounded Details and selective Reviews/Profile precede direct
source-blind candidate supply and an explicit REQUIRED/OPTIONAL planner ledger. Existing
Weather/Routes/Official Web and itinerary generation follow. No active Semantic Evaluator
or minimum-subset enumeration remains; B2 code/tests are retained pending separate cleanup.
V1 remains reopened, not re-frozen. The supply checkpoint passed 673 backend tests
(9 skipped). The subsequent systematic Requirement-boundary pass is implemented and
offline validated: 262 affected tests passed; full backend once 711 passed, 9 skipped.
Live observations and current limitations are recorded in `docs/poi_selection.md`.
Current authority: `docs/v1_design.md` and `docs/poi_selection.md`; chronological history:
`docs/poi_selection_evolution.md` and `docs/b2_implementation.md`. Historical pre-redesign
code is recoverable at `60902ac09a1331f6eebddba8963efd24f6e8e61a`.
The following paragraphs describe historical V1 milestones, not the active supply policy.
TripWorld Phases 1-5 remain accepted; Phase 6 runtime integration remains paused.

<a id="b-40e4f5c4b799-6"></a>

The two authorized development live runs each stopped at Requirement validation:
B redeclared reserved party in subjects; A generated a temporary discovery ID longer
than40 characters. No Google/evaluator/selection/itinerary call followed. The new supply
path is not yet end-to-end live validated. The subsequent boundary pass replaces model
canonical IDs with bounded temporary references, application-owned IDs and explicit
party/specified/unresolved attribution. It adds classified failures and opt-in private
diagnostic capture, without changing supply, budgets or HARD policy. The later authorized
nine-case Requirement-only acceptance attempt stopped on its first case with a transport
OpenAIConnectionError: one client/HTTP attempt, no completed response, eight cases unexecuted.
That initial attempt had no provider/schema/semantic evidence. After explicit endpoint/fee
authorization, a separate continuation made 9 client invocations and 8 HTTP requests,
receiving 8 completed responses. The dedicated whole-party case failed before HTTP due to
a harness shared-client lifecycle error and was not repeated; the seven untouched cases
ran after a harness-only correction. All 8 responses passed DTO/reference/source/domain
checks, but destination-as-REQUIRED-visit, negative-preference HARD strength and ambiguous
pronoun attribution remain semantic concerns. Missing-fields and explicit no-stairs HARD
clarification worked at the application layer. All downstream calls remained zero.
The subsequent authorized semantics pass defined contextual role/strength/attribution/count
policy, updated only the V1 Requirement prompt (version 3) and its diagnostic version label,
and added a tested development harness. Schema/canonicalization/HARD/supply remain unchanged.
Offline: affected 275 passed; full backend once 724 passed, 9 skipped. A fixed multilingual
matrix made 10 Requirement calls with 10 completed responses; 8 canonical outputs validated,
and 2 extraction-issue cases stopped before canonical release. Most contrasts behaved as
expected, but an optional unknown traveler count was unnecessarily elevated to a blocking
extraction issue. The original Spanish normal-only expectation is now documented as disputed,
without retrospectively changing the old result. The then-proposed optional-uncertainty
follow-up is superseded by the newly specified structured-input migration above. No further live work,
V1 re-freeze, commit or push. Full evidence and history are in docs/poi_selection.md.

<a id="b-40e4f5c4b799-7"></a>

V1-A discovers and selects POIs using Google Places evidence, alongside Google Weather and Routes. The revised selection flow is cheap candidate discovery, structured narrowing, selective Place Details plus rating, further narrowing, selective reviews, review-derived `ExperienceProfile`, and final POI selection. Rating and reviews inform selection; neither is required for every candidate. Do not use or display `userRatingCount`.

<a id="b-40e4f5c4b799-8"></a>

V1-A was originally frozen on 2026-09-12, then intentionally reopened for rating/review-aware POI selection and explicitly re-frozen on 2026-09-14. The original freeze remains a separate historical checkpoint. The former V1-C milestone is retired from the active architecture; Places review evidence now belongs to V1-A.

<a id="b-40e4f5c4b799-9"></a>

After the revised V1-A checkpoint, V1 migrated free-form user semantics into one V1 requirements LLM call returning unchanged `TravelRequirements` plus bounded `NamedPlaceIntent`, `RequestedPlaceInformation`, `ExperiencePreferenceIntent`, transport preference, and `PoiInterest`. Application code validates source spans and typed values, reconciles Place IDs, and deterministically executes selection, routing, and evidence acquisition. The active V1 graph does not use raw-text keyword/regex fallback to reinterpret these meanings. V0's requirements contract and execution path remain unchanged.

<a id="b-40e4f5c4b799-10"></a>

V1-B addresses decision-relevant official/current information gaps that structured providers cannot reliably answer, such as temporary closures, special opening hours, admission, tickets, and reservations. It does not broadly re-check every selected POI or facts already sufficiently answered by structured evidence.

<a id="b-40e4f5c4b799-11"></a>

V1-B supplements only final selected POIs with current first-party official evidence. Its integrated path projects stable selected Place IDs and structured facts, plans targeted Web tasks for explicit residual needs or concrete operational/date risks, acquires bounded Luna Web and optional official pages, then runs EvidenceReasoner, a deterministic Grounding / Provenance Gate, and a claim-scoped EvidenceResolver. Accepted/effective facts and explicit uncertainty reach the planner; raw search observations and rejected claims do not. Normal Web/Page budgets are 6/6. These are pre-planning evidence controls, not V3 itinerary-feasibility validation.

<a id="b-40e4f5c4b799-12"></a>

Rating remains a quantitative Places signal. `ExperienceProfile` represents retrieved-review evidence for deterministic POI selection; unsupported signals remain unknown. The LLM does not select the final POI set, and reviews/Profile are not passed to the itinerary prompt. Neither rating nor reviews may override an official date-specific closure. Any future frontend rating/review display must use actually acquired evidence for itinerary POIs; frontend work is not implemented.

<a id="b-40e4f5c4b799-13"></a>

V1 may instruct the generator to use supplied evidence carefully—for example, not to plan a clearly non-walkable transfer as an ordinary walk or invent unsupported transit details. This is still **evidence-informed generation**, not general post-generation feasibility validation. An itinerary may therefore violate supplied evidence even when that evidence was acquired correctly.

<a id="b-40e4f5c4b799-14"></a>

V1 retains point-valued shared `Money` and optional activity `estimated_cost`. At its Foundry mapping boundary, V1 preserves valid points, converts a clear finite same-currency two-endpoint numeric range to a Decimal midpoint, and sets unsupported optional costs to `null`. This uses no LLM repair call and does not turn a derived activity estimate into accepted official admission evidence or alter V0.

<a id="b-40e4f5c4b799-15"></a>

V1 does not implement RAG, a free-form agentic tool loop, general violation detection, targeted repair, or re-validation.

<a id="m-2ea9f999e32a"></a>
## V3 — Validation, Targeted Repair, and Re-validation

_Source context: Research Versions. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2ea9f999e32a-0"></a>

V3 adds explicit feasibility checking after evidence-informed generation:

<a id="b-2ea9f999e32a-1"></a>

```text
Draft itinerary
→ Feasibility validation
→ Violation detection
→ Targeted repair when needed
→ Re-validation
```

<a id="b-2ea9f999e32a-2"></a>

Candidate checks include budget, opening hours, transfer time, weather suitability, activity density, required or excluded activities, and operationalized user preferences.

<a id="b-2ea9f999e32a-3"></a>

Validation should be deterministic where practical. Repair should focus on affected itinerary components and preserve already-valid content rather than defaulting to full regeneration.

<a id="b-2ea9f999e32a-4"></a>

Shared date input/output checks in V0–V3 are project-wide contracts. They are **not** the general feasibility-validation mechanism studied in V3.

<a id="m-90c003172048"></a>
## Shared Trip-Date Policy

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-90c003172048-0"></a>

Every version uses the same supported planning window. Fix the runtime reference date once at run start:

<a id="b-90c003172048-1"></a>

```text
reference_date <= start_date <= end_date <= reference_date + 9 days
```

<a id="b-90c003172048-2"></a>

The final itinerary may contain dates only within the requested trip range:

<a id="b-90c003172048-3"></a>

```text
Final itinerary dates
⊆ Requested trip dates
⊆ [reference_date, reference_date + 9 days]
```

<a id="b-90c003172048-4"></a>

The backend enforces this contract deterministically, including for direct API calls. Frontend date restrictions provide user guidance but are not the authority. Tests may inject a fixed date; production requests must not use arbitrary caller-supplied reference dates to bypass the real runtime window.

<a id="m-a4e48277cf25"></a>
## Engineering Architecture

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a4e48277cf25-0"></a>

Use a modular monolith:

<a id="b-a4e48277cf25-1"></a>

```text
React + TypeScript frontend
          ↓ HTTP / JSON
FastAPI backend
          ├─ Version-specific planning graphs and entry points
          ├─ Application services and evidence acquisition
          ├─ Typed schemas, policies, and evidence normalization
          ├─ LLM and external-provider integrations
          ├─ Runtime configuration and Run Trace
          └─ RAG, validation, repair, and persistence only when needed
```

<a id="b-a4e48277cf25-2"></a>

Planning, orchestration, evidence acquisition, RAG, validation, and repair belong in the backend. The frontend collects requirements, calls the APIs, and presents results; it should not own research-critical planning logic.

<a id="b-a4e48277cf25-3"></a>

Keep V0, V1, V2, and V3 independently runnable through explicit version-specific graphs and entry points, such as `scripts/run_v0.py` through `scripts/run_v3.py`. Do not implement all versions as one large graph controlled mainly by version conditionals. Do not create future-version modules before they are required.

<a id="m-95db18ee029f"></a>
## Provider and Evidence Boundaries

_Source context: Engineering Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-95db18ee029f-0"></a>

LangGraph nodes should call internal services, not third-party APIs directly:

<a id="b-95db18ee029f-1"></a>

```text
Graph node → Acquisition service → Provider integration → External API
```

<a id="b-95db18ee029f-2"></a>

Provider integrations own authentication, API requests, provider DTOs, response mapping, and provider-specific errors. The evidence layer deterministically converts provider-facing models into typed internal planning evidence. Raw provider payloads should not be passed through the graph or directly into planner prompts.

<a id="b-95db18ee029f-3"></a>

Use evidence types suited to their purpose rather than requiring one universal `Evidence` schema. Preserve source identity, retrieval time, availability, uncertainty, and provenance where relevant. Distinguish provider-observed information from derived estimates.

<a id="b-95db18ee029f-4"></a>

Evidence authority depends on the claim. Official notices are usually strongest for official operational changes; structured route and weather providers are appropriate for their respective measurements; visitor accounts can support subjective experience. Do not silently promote uncertain or subjective evidence into confirmed factual claims.

<a id="m-6df0281d260f"></a>
## Bounded Tool Use

_Source context: Engineering Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6df0281d260f-0"></a>

External acquisition is deterministic and application-controlled where practical. Use a request-level ToolBudget for candidate search, enrichment, weather, routes, web queries, and other provider work. Avoid hidden fan-out and unconstrained LLM-selected tool loops.

<a id="b-6df0281d260f-1"></a>

Request-scoped caching may deduplicate identical operations within a run. Do not introduce persistent evidence caching solely for V1.

<a id="m-fc11a817612a"></a>
## Runtime Configuration and Observability

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-fc11a817612a-0"></a>

`config/runtime.yaml` is the global source for non-secret runtime policy, including normal ToolBudget limits, application time zone, logging, and Run Trace settings. One centralized code-level definition sets project-wide ToolBudget hard safety ceilings:

<a id="b-fc11a817612a-1"></a>

```text
Global hard limit → runtime.yaml limit → per-run usage
```

<a id="b-fc11a817612a-2"></a>

Changing a normal limit within its hard boundary should require only a YAML change. Policies should not introduce hidden secondary ToolBudget caps. Invalid, missing, malformed, or out-of-range runtime configuration must fail fast rather than silently fall back.

<a id="b-fc11a817612a-3"></a>

Keep secrets and genuine deployment-specific values outside committed runtime policy, typically in `.env`. Never commit credentials, raw provider or LLM payloads, or runtime logs.

<a id="b-fc11a817612a-4"></a>

Each development run should have a `run_id` and lightweight Run Trace sufficient to inspect its configuration, progression, evidence provenance, tool usage, failures, and outcome. Record a sanitized effective runtime configuration and stable hash for reproducibility. Payload capture should be configurable, and credentials must be redacted from traces and runtime logs.

<a id="b-fc11a817612a-5"></a>

Trace and logging **write failures** should be best-effort and should not change planning semantics. This does not apply to configuration validation failures, which must fail fast.

<a id="m-cbb1f124e53a"></a>
## Database Direction

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-cbb1f124e53a-0"></a>

Do not introduce PostgreSQL, pgvector, or another persistence system merely because it is in the preferred stack. V0 and V1 can use per-run state, request-scoped cache/deduplication, and file-based Run Trace without an application database.

<a id="b-cbb1f124e53a-1"></a>

Introduce persistence or vector storage only when a concrete capability—potentially V2 retrieval or later saved application data—requires it. Run Trace is observability, not an application evidence database.

<a id="m-0cfd0385f0d1"></a>
## Version Preservation and Development Rules

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-0cfd0385f0d1-0"></a>

Keep versions comparable by preserving, where practical, the shared input contract, requirement-extraction behavior, LLM model/configuration, output schema, and base planning objective. Later versions may reuse shared schemas, policies, services, and integrations, but must not silently redefine earlier research behavior.

<a id="b-0cfd0385f0d1-1"></a>

Implementation completion and freeze are separate. Passing tests or a live smoke run does not freeze a milestone; freeze requires explicit user approval and accurate documentation. Detailed V1 architecture and milestone history belong in `docs/v1_design.md` and `docs/v1_milestone.md`, not this project-level document.

<a id="b-0cfd0385f0d1-2"></a>

Development principles:

<a id="b-0cfd0385f0d1-3"></a>

- Add only the mechanism required by the current approved stage.
- Preserve independently runnable and comparable V0–V3 paths.
- Keep external evidence acquisition separate from general feasibility validation.
- Use typed normalized evidence with explicit uncertainty and provenance.
- Keep tool use bounded, observable, reproducible, and application-controlled.
- Keep secrets separate from committed runtime policy.
- Prefer focused tests with fake providers; use live runs for integration verification, not formal evaluation.
- Avoid premature databases, microservices, future-version modules, and unnecessary frontend complexity.
- Document meaningful post-freeze changes without rewriting historical milestones.
- Do not begin formal research evaluation or thesis work until explicitly requested.

<a id="m-e72174ece7d3"></a>
## Original README.md

_Source context: Version Preservation and Development Rules. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-ea709af7ed4c"></a>
## Reliable Trip Plan Agent

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ea709af7ed4c-0"></a>

An LLM-based travel planning system focused on generating feasible and reliable itineraries.

<a id="b-ea709af7ed4c-1"></a>

The project will be developed as four independently runnable versions:

<a id="b-ea709af7ed4c-2"></a>

- V0: plain LLM planning
- V1: V0 plus external information and tools
- V2: V1 plus retrieval-augmented generation
- V3: V2 plus constraint validation, targeted repair, and re-validation

<a id="b-ea709af7ed4c-3"></a>

V0, V1 and V2 now share the structured-input foundation (`planning_request_2`):

<a id="b-ea709af7ed4c-4"></a>

```text
Validated trip form -> optional shared preference interpretation -> canonical context
V0: context -> plain LLM itinerary
V1: context -> bounded external evidence / deterministic candidate supply -> itinerary
```

<a id="b-ea709af7ed4c-5"></a>

V0 has no external travel tools or RAG. Empty preferences skip interpretation in both
versions. V1 retains Google Places, selective Reviews/Profile, Weather, Routes and bounded
Official Web. Phase6 V2 RAG and opt-in quality_first_1 are implemented with accepted bounded
development-live evidence. V1/V2 are not re-frozen; V3 is not implemented. Product defaults
remain V0. See the existing [Phase6 closeout](v2_development.md) for limits.
Historical free-text V0 results predate this intentional common-baseline update.

<a id="m-c60df242cc9c"></a>
## Current explicit development baseline

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-c38a9001ce6c"></a>
## Explicit reproducible development entry points

_Source context: Reliable Trip Plan Agent / Current explicit development baseline. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-c38a9001ce6c-1"></a>

Save this complete input as request.json locally (not a manifest wrapper):

Verbatim passages shared with another maintained section: [1](development_guide.md#b-61a2c7801de0-0), [2](development_guide.md#b-61a2c7801de0-2), [3](development_guide.md#b-61a2c7801de0-3), [4](development_guide.md#b-61a2c7801de0-4), [5](development_guide.md#b-61a2c7801de0-5), [6](development_guide.md#b-61a2c7801de0-6), [7](development_guide.md#b-61a2c7801de0-7). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-0b33efb0487b"></a>
## Requirements

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-0b33efb0487b-0"></a>

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

<a id="m-2f369eb5415e"></a>
## Setup

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2f369eb5415e-0"></a>

Install the project and development dependencies:

<a id="b-2f369eb5415e-1"></a>

```shell
uv sync
```

<a id="b-2f369eb5415e-2"></a>

Copy `.env.example` to `.env`, then provide the Microsoft Foundry endpoint, deployment, and
API key. `LLM_MODEL` records the underlying model shared by all system versions, while
`AZURE_OPENAI_DEPLOYMENT` identifies the deployment sent in the API request's `model` field.
The two values may differ and neither is hard-coded in a graph or node. The Foundry endpoint
uses the OpenAI-compatible `/openai/v1` API and does not require an API version setting.

<a id="b-2f369eb5415e-3"></a>

V1-A additionally requires `GOOGLE_MAPS_API_KEY`. `APP_TIME_ZONE` controls the explicit IANA
calendar time zone used by production date sources and defaults to `Australia/Sydney`.

<a id="m-7c8794e848c7"></a>
## Run V0

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7c8794e848c7-0"></a>

Save the shared form as `request.json` (refresh dates for the current planning window):

<a id="b-7c8794e848c7-1"></a>

```json
{
  "destination": "Sydney, Australia",
  "start_date": "2026-09-21",
  "end_date": "2026-09-23",
  "traveler_count": 3,
  "budget": {"amount": "1800.00", "currency": "AUD"},
  "additional_preferences": ""
}
```

<a id="b-7c8794e848c7-2"></a>

All trip fields including total-trip budget amount and currency are mandatory.
`additional_preferences` is optional. The input version defaults internally; users do not
need to enter a version. Nonblank preference text is preserved exactly. No form values
are converted to prose for model re-extraction.

<a id="b-7c8794e848c7-3"></a>

```shell
uv run python scripts/run_v0.py --input-json request.json --reference-date 2026-09-19
```

<a id="b-7c8794e848c7-4"></a>

`--reference-date` is a trusted research and testing override. Normal Product requests use the
backend's configured-zone runtime date and cannot supply an alternative reference date.

<a id="b-7c8794e848c7-5"></a>

Every planner version shares an inclusive ten-day planning window. For a reference date of
`2026-09-11`, requested and generated itinerary dates must stay between `2026-09-11` and
`2026-09-20`. A short trip outside that window is invalid even when its duration is less than
ten days.

<a id="b-7c8794e848c7-6"></a>

The command prints a `PlanningResult` JSON object. Invalid required form fields fail before
any model/provider call. Explicit form/text conflicts and unsupported HARD semantics return
clarification. Input validation is not whole-itinerary feasibility verification.

<a id="m-6e1e9c6c2521"></a>
## Run V1-A

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6e1e9c6c2521-0"></a>

Run the independent V1 entry point after enabling Places API (New), Weather API, and Routes API
for the configured Google Maps Platform key:

<a id="b-6e1e9c6c2521-1"></a>

```shell
uv run python scripts/run_v1.py --input-json request.json --reference-date 2026-09-19
```

<a id="b-6e1e9c6c2521-2"></a>

The trusted `--reference-date` research override is also supported. Normal V1 CLI runs create a
best-effort local trace under `logs/`; raw provider and LLM payloads remain disabled unless
`V1_TRACE_PAYLOAD_MODE=raw` is explicitly configured. The Product API continues to use V0.

<a id="m-9eb94720a2dd"></a>
## Development checks

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-9eb94720a2dd-0"></a>

Run the test suite:

<a id="b-9eb94720a2dd-1"></a>

```shell
uv run pytest
```

<a id="b-9eb94720a2dd-2"></a>

Run static lint checks:

<a id="b-9eb94720a2dd-3"></a>

```shell
uv run ruff check .
```

<a id="b-9eb94720a2dd-4"></a>

Run the development API:

<a id="b-9eb94720a2dd-5"></a>

```shell
uv run uvicorn backend.app.main:app --reload
```

<a id="b-9eb94720a2dd-6"></a>

The health endpoint is available at `GET /health`.

<a id="m-8d84f46058d5"></a>
## Run the frontend

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8d84f46058d5-0"></a>

Install the frontend dependencies:

<a id="b-8d84f46058d5-1"></a>

```shell
cd frontend
npm install
```

<a id="b-8d84f46058d5-2"></a>

Start the Vite development server:

<a id="b-8d84f46058d5-3"></a>

```shell
npm run dev
```

<a id="b-8d84f46058d5-4"></a>

The frontend uses relative API URLs. During local development, Vite proxies `/api` and
`/health` to the FastAPI server at `http://127.0.0.1:8000`.

<a id="b-8d84f46058d5-5"></a>

The product routes are `/` and `/plan`. Product planning calls `POST /api/planning` through a
version-agnostic service boundary. The service currently uses the programmatic V0 planner and
can later switch to V3 without exposing a research version to product clients. Product clients
submit the shared form shown above, including mandatory budget and optional preferences.
The service passes it directly to V0. The current frontend still labels budget optional;
missing budget now produces backend 422. Frontend alignment is outstanding, not completed.

<a id="b-8d84f46058d5-6"></a>

The developer workbench is available at `/dev/planner` and calls `POST /api/dev/planning` with
an explicit implemented research version. It currently supports only V0 and intentionally
shows raw planning and debug responses. Its backend now accepts
`{"version":"v0","request":{...shared form...},"reference_date":"2026-09-19"}`.
The existing free-text developer UI has not yet been migrated. This local development functionality must be protected
or disabled before a public production deployment.

<a id="b-8d84f46058d5-7"></a>

Run the frontend checks:

<a id="b-8d84f46058d5-8"></a>

```shell
npm run test
npm run lint
npm run build
```

<a id="m-ca14b8a5e2af"></a>
## Current structure

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ca14b8a5e2af-0"></a>

```text
backend/
├── app/
│   ├── api/
│   ├── evidence/
│   ├── integrations/
│   ├── llm/
│   ├── observability/
│   ├── policies/
│   ├── runtime/
│   ├── schemas/
│   ├── services/
│   └── versions/
│       ├── v0/
│       └── v1/
└── tests/
frontend/
└── src/
    ├── app/
    ├── features/
    ├── layouts/
    ├── routes/
    └── shared/
scripts/
├── run_v0.py
└── run_v1.py
```

<a id="b-ca14b8a5e2af-1"></a>

Future version-specific code and entry points will be added only when each version is approved.
Shared result schemas remain limited to fields common to every version; evidence, retrieval,
validation, and repair data use version-specific contracts.

<a id="m-867134a0b5d6"></a>
## Reliable Trip Plan Agent

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-867134a0b5d6-0"></a>

A Capstone travel-planning project with independently runnable V0 (plain LLM), V1 (external
tools) and V2 (RAG). V3 targeted validation/repair is not implemented.

<a id="b-867134a0b5d6-1"></a>

Current status: **implemented + bounded development-live-validated** for Phase 6 and explicitly
selected quality_first_1. This is not a formal benchmark, production SLA or automatic re-freeze.
The product API still defaults to V0; quality_first_1 is not automatically enabled.

<a id="m-969ad08d3151"></a>
## Start here

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-969ad08d3151-0"></a>

- [PROJECT](../PROJECT.md): current scope, accepted state and approval boundaries.
- [Documentation index](README.md): current topics versus historical records.
- [Operations](development_guide.md): setup, exact V0/V1/V2 commands, configuration hashes,
  script purposes and experimental-material preservation.
- [Architecture](shared_architecture.md): shared input, tools, RAG and output roles.
- [Known issues](known_issues.md): product gaps and bounded validation limits.

<a id="m-97960d993e89"></a>
## Basic setup

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-97960d993e89-0"></a>

Use Python 3.12 and uv:

<a id="b-97960d993e89-1"></a>

```shell
uv sync
uv run uvicorn backend.app.main:app --reload
```

<a id="b-97960d993e89-2"></a>

Copy non-secret examples from `.env.example` into a private local `.env` and configure the
required model/provider credentials. Never commit secret files. Retrieval requires the optional
retrieval dependencies and existing compatible local corpus/database; see Operations before
running any ingestion or paid embedding command.

<a id="b-97960d993e89-3"></a>

Shared `planning_request_2` requires destination, dates, traveler count, whole-trip budget and
currency. `additional_preferences` is optional. Empty preferences skip interpretation.
The final output is `itinerary_2`: timed primary activities and optional unplanned references.

<a id="m-3179d5bf02cb"></a>
## Repository map

_Source context: Reliable Trip Plan Agent. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-3179d5bf02cb-0"></a>

| Path | Responsibility |
| --- | --- |
| `backend/app/versions/v0`, `v1`, `v2` | Version-specific orchestration and runners |
| `backend/app/services`, `policies`, `schemas` | Shared application contracts and policy |
| `backend/app/integrations`, `llm`, `tripworld` | Provider adapters and retrieval |
| `backend/tests` | Offline and opt-in integration tests |
| `frontend` | Product/developer UI; known backend alignment gaps remain |
| `scripts` | Independent runners and documented engineering utilities |
| `config` | Conservative defaults and explicitly selected development configuration |
| `docs/current` | Current design and operating guide |
| `docs/history` | Preserved proposals, milestones, failures and development evidence |
| `data/tripworld` | Versioned manifests plus ignored local corpus/artifacts |

<a id="b-3179d5bf02cb-1"></a>

No scripts, datasets or historical experiments are disposable merely because they are outside
the ordinary runtime. See the script inventory before proposing cleanup.

<a id="m-b06cb7306591"></a>
## Capstone Project Context

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-b06cb7306591-0"></a>

Current source of truth. Updated 2026-09-20.

<a id="m-6196549f4371"></a>
## Purpose and version boundary

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6196549f4371-0"></a>

**An LLM-Based Travel Planning System for Feasible and Reliable Itinerary Generation**
studies reliable travel planning through independently runnable mechanisms:

<a id="b-6196549f4371-1"></a>

| Version | Mechanism | Current execution |
| --- | --- | --- |
| V0 | Plain LLM; no external travel acquisition | Independent CLI/Python; product API default |
| V1 | External information and deterministic candidate supply | Independent CLI/Python |
| V2 | V1 plus TripWorld main-candidate discovery | Independent CLI/Python |
| V3 | Validation, targeted repair and re-validation | Not implemented |

<a id="b-6196549f4371-2"></a>

Phase 6, post-itinerary Nearby references, and opt-in `quality_first_1` are
**implemented + bounded development-live-validated**. This is not a formal benchmark,
all-branch correctness proof, production SLA, or automatic V1/V2 re-freeze.
Historical freezes and their later authorized changes remain recorded in history.

<a id="m-290767151447"></a>
## Active foundation

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-290767151447-0"></a>

- Shared `planning_request_2`: destination, dates, traveler count, total budget and currency
  are mandatory; `additional_preferences` is optional.
- Nonempty preferences receive one shared interpretation; empty preferences skip it.
  Application code owns canonical identities, subjects, source validation and mechanical policy.
- V1/V2 use deterministic main-candidate supply, selective Reviews/ExperienceProfile,
  REQUIRED/OPTIONAL inputs and evidence-informed primary itinerary generation.
- Shared final output is `itinerary_2`. V1/V2 append bounded independent Nearby references
  after primary validation, without changing the primary itinerary.
- V2 alone adds bounded TripWorld retrieval and Google-backed resolution before shared admission.
  TripWorld is discovery evidence, not current factual truth.
- B1/B2 evaluators and subset experiments are historical and inactive. Shared acquisition code
  bearing older names still has active dependencies; do not delete it by filename.

<a id="m-c460dcaa49db"></a>
## Current configuration and product boundary

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-c460dcaa49db-0"></a>

`config/runtime_quality_first_1.yaml` is explicitly selected for the accepted development
baseline. It is not the product default. Never layer the historical 60/180 override over it.
The [operations guide](development_guide.md) owns exact commands, hashes and time limits;
[POI supply](shared_poi_supply.md) owns shared capacity and acquisition policy.
Product and developer planning APIs currently dispatch only V0. Frontend budget/response
alignment and developer input/version selection remain incomplete.

<a id="m-08d213a16a0a"></a>
## Work authorization and next step

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-08d213a16a0a-0"></a>

Current work is engineering design, implementation and development validation, not formal
benchmarking or thesis conclusions. Follow [AGENTS.md](../AGENTS.md), including English repository
content, Chinese chat, explicit commits and explicit version freezes.

<a id="b-08d213a16a0a-1"></a>

The accepted documentation consolidation does not authorize code cleanup, live calls, SQL or
storage changes, V3, default-engine changes, or Git commits. The pending source baseline needs
an explicitly approved save. The earlier three-group commit proposal is historical scope:
document moves in this consolidation require refreshing its path inventory before staging.
After baseline saving, the recommended next task is saved-capture diagnosis of Weather 404.
No next task starts automatically.

<a id="m-37b8c2edfc7c"></a>
## Documentation ownership

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-37b8c2edfc7c-0"></a>

Start with the [documentation index](README.md). Current behavior has one topic owner;
detailed observations and superseded proposals belong to history. Do not append the same live
report to multiple current documents. `thesis_notes/` and ignored captures are separate local
archives, not the current source of truth or automatically backed up by Git.

<a id="m-b23d44dba340"></a>
## Documentation index

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-b23d44dba340-0"></a>

[PROJECT](../PROJECT.md) owns current status and scope. Current documents describe implemented
behavior; history preserves decisions and observations at their original dates.

<a id="m-18bbf00cb5fb"></a>
## Current reading set

_Source context: Documentation index. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-18bbf00cb5fb-0"></a>

| Question | Authoritative topic |
| --- | --- |
| How do versions, inputs, evidence and outputs fit together? | [Architecture](shared_architecture.md) |
| How are candidates acquired, compared and supplied? | [POI selection](shared_poi_supply.md) |
| What does TripWorld add, and how are identities resolved? | [TripWorld](v2_design.md) |
| How do I run it; which scripts/configuration/artifacts matter? | [Operations and script inventory](development_guide.md) |
| What remains unresolved or untested? | [Known issues](known_issues.md) |

<a id="m-87687cc74155"></a>
## Historical record map

_Source context: Documentation index. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-87687cc74155-0"></a>

| Preserved document | Meaning; not current executable guidance |
| --- | --- |
| [V0 milestone](v0_milestone.md) | Original baseline and subsequent dated changes |
| [V1 milestone](v1_milestone.md) | Milestone, freeze and post-milestone evidence |
| [V1 design log](v1_development.md) | Input/output and Nearby migration proposals and checkpoints |
| [B1 selector](v1_selector_experiments.md) | Shared selector implementation and superseded decisions |
| [B2 implementation](v1_selector_experiments.md) | Evaluator experiments, failures and offline/live checkpoints |
| [Supply implementation log](development_record.md) | Deterministic supply, Requirement and shared-input migrations |
| [Evolution record](development_record.md) | Detailed chronological decision evidence |
| [TripWorld Phase 4](v2_development.md) | Entity corpus, OpenAI prototype and profiling |
| [TripWorld Phase 5](v2_development.md) | Persistent retrieval and corpus acceptance |
| [TripWorld Phase 6](v2_development.md) | Old proposals, integration, SQL diagnosis and quality_first_1 acceptance |
| [Frontend milestone](frontend_milestone.md) | Historical UI scope; current gaps are in known issues |
| [Previous root context](development_record.md) | Original PROJECT/README before consolidation |

<a id="m-05bdec00339b"></a>
## Decision navigation

_Source context: Documentation index. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-05bdec00339b-0"></a>

QCGRE was followed by the B1 shared selector and B2 evaluator experiments, then the accepted
current deterministic planning-candidate supply. Open semantic requirements survived that
change; model evaluation is no longer the compulsory selection core. Shared structured input
and `itinerary_2` followed. Same-pool model references were replaced for V1/V2 by post-itinerary
Nearby discovery. Phase 6 integrated TripWorld before admission; `quality_first_1` then revised
shared acquisition opportunities and cache reuse. Follow the historical records above for
actual approvals, failures and test counts rather than inferring them from this navigation.

<a id="m-304401474c5c"></a>
## Maintenance rules

_Source context: Documentation index. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-304401474c5c-0"></a>

- Edit one current topic for a behavioral change; update PROJECT only for status/scope changes.
- Record detailed development results once in the relevant historical log and link to them.
- Keep unique failed attempts, unknown usage and superseded decisions. Do not relabel old tests.
- Preserved history intentionally retains original wording and some repeated evidence; it is
  not a second current specification. No new reports should be copied across these files.
- Historical path mentions inside code spans describe their original locations. Relative links
  are maintained separately. The pre-existing deleted selector architecture review remains in
  Git history; this consolidation neither restores nor newly deletes it.
- This move does not authorize reading or editing ignored thesis notes.

<a id="m-812f6b127a9b"></a>
## Current planning architecture

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-812f6b127a9b-0"></a>

Status: implemented + bounded development-live-validated; see [PROJECT](../PROJECT.md).

<a id="m-5cd6495818d2"></a>
## Shared input and semantic boundary

_Source context: Current planning architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-5cd6495818d2-0"></a>

`planning_request_2` requires destination, start/end dates, traveler count and whole-trip budget
with explicit currency. Preferences are optional. Form facts are authoritative; they are not
converted into prose for re-extraction. The shared inclusive ten-day window is evaluated from
a trusted request reference date, with the configured application time zone.

<a id="b-5cd6495818d2-1"></a>

One shared interpreter handles nonempty preferences. Open normalized semantic requirements,
subjects, discovery intents, named intentions and evidence requests preserve source provenance.
Application validation owns IDs, references and registered enforceability. It does not parse
raw preferences again with keyword rules. Unsupported HARD requirements and unresolved REQUIRED
identities retain their clarification boundary; UNKNOWN is not verified satisfaction.
Fixed experience dimensions serve Review/Profile evidence, not a universal preference taxonomy.

<a id="m-19fec32e2d1c"></a>
## Version flow

_Source context: Current planning architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-19fec32e2d1c-0"></a>

```text
Validated form -> optional shared interpretation -> application-owned context
V0 -> one plain-LLM generation -> shared final output
V1 -> Google discovery ------------------------------+
V2 -> Google discovery + TripWorld/Google resolution -+-> canonical union
   -> shared admission -> Details/optional Reviews/Profile -> deterministic supply
   -> Weather/Routes/Official Web as applicable -> primary generation + existing validation
   -> bounded Nearby references -> final itinerary_2
```

<a id="b-19fec32e2d1c-1"></a>

The V2 runner injects discovery before shared admission. V1 does not call RAG and V0 has no
external travel acquisition. V3 validation/targeted repair is not implemented. Deterministic
supply is detailed in [POI selection](development_record.md); retrieval in [TripWorld](v2_design.md).

<a id="m-eca6bc43125e"></a>
## Evidence and generation

_Source context: Current planning architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-eca6bc43125e-0"></a>

Providers are normalized behind service/client boundaries. Google canonical identity,
structured current facts, date-applicable opening information, review-derived experience and
validated official claims retain distinct provenance. Static corpus enrichment and model world
knowledge must not become verified current facts. Weather/Routes/Web failures and missing data
remain explicit. Unknown prices do not demonstrate budget feasibility.

<a id="b-eca6bc43125e-1"></a>

The generator receives the final bounded supply, REQUIRED/OPTIONAL decisions and relevant
evidence, not the entire admission pool. A supplied place need not be scheduled. Primary
activities retain dates/times and are validated against the main supply identity ledger.
The existing date/identity checks are not comprehensive itinerary feasibility validation.

<a id="m-852d4d3cd13e"></a>
## Two output roles and three identity ledgers

_Source context: Current planning architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-852d4d3cd13e-0"></a>

V1/V2 use a primary-only model DTO. After successful primary generation and validation, the
application obtains anchors only from scheduled canonical IDs with existing evidence coordinates.
Independent Nearby results supply optional references. Main supply, scheduled anchors, and
Nearby results are separate ledgers. The application adds source references, names and addresses.
References do not satisfy REQUIRED, count as scheduled visits, or add to planned costs.

<a id="b-852d4d3cd13e-1"></a>

Nearby visits anchors in date/start-time/activity-ID order, deduplicating places. Representatives
use non-transitive 300 m reuse; at most three representative areas are searched. Reused candidates
are checked again within 800 m of the actual associated anchor. Stable distance/ID ordering and
anchor round-robin choose up to three references. Scheduled/excluded/duplicate/known-ineligible
places are filtered. An old supply candidate is eligible only if independently found nearby.
Early regions may consume the budget; coverage of every day is not promised.

<a id="b-852d4d3cd13e-2"></a>

Search uses DISTANCE, restaurant/cafe/park/museum, up to ten results per request, three actual
requests, no retry, a ten-second phase deadline and at most four seconds per call constrained
by remaining time. Cache hits do not consume sends; failed sends do. Identity/name/location,
address/types/status/attributions are requested, not rating/reviews/opening hours.
Search failure or invalid reference attachment preserves the validated primary output with
partial/empty references and diagnostics; user cancellation propagates. No second model,
Details/Profile/Routes/Web collection is added for references. Straight-line distance is not
walking time. Unknown suitability is not represented as verified satisfaction.

<a id="b-852d4d3cd13e-3"></a>

V0 retains one generation producing primary activities and optional subordinate model-knowledge
references. It fabricates neither Google identity nor application evidence and performs no Nearby.

<a id="m-6e3321f845f1"></a>
## Code ownership

_Source context: Current planning architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6e3321f845f1-0"></a>

- `backend/app/services/preference_interpretation.py`: shared interpretation.
- `backend/app/versions/v0/`, `v1/`, `v2/`: independent runners and orchestration.
- `backend/app/services/planning_supply_pipeline.py`: active shared supply adapter.
- `backend/app/services/reference_discovery.py`: post-itinerary Nearby stage.
- `backend/app/llm/azure_foundry/`: provider DTOs, mapping and generation boundary.
- `backend/app/schemas/itinerary.py`: shared final output.

<a id="b-6e3321f845f1-1"></a>

Historical implementation and evidence: [V1 design log](v1_development.md),
[supply log](development_record.md), [Phase 6](v2_development.md).

<a id="m-320444fee366"></a>
## Operations, configuration and script inventory

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-320444fee366-0"></a>

This is the current engineering entry guide, not authorization to run paid scenarios, rebuild
corpora or modify a database. See [PROJECT](../PROJECT.md) for scope and approval boundaries.

<a id="m-8df8d48ff10e"></a>
## Budget and timeout interpretation

_Source context: Operations, configuration and script inventory. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8df8d48ff10e-0"></a>

The selected quality configuration separates capacities, normal success targets, hard sends
and actual usage. [POI selection](development_record.md) owns the duration-dependent C/G/K/P values.
[TripWorld](v2_design.md) owns incremental retrieval/resolution limits.

<a id="b-8df8d48ff10e-1"></a>

- SQL: up to 60 seconds constrained by remaining RAG time; RAG phase: 360 seconds.
- Ordinary Details: 120-second phase, each request at most 20 seconds and remaining phase time.
- Embedding/connect/RAG Google timeouts remain 8/2/4 seconds. Zero runtime retries.
- The explicit 600-second development wrapper bounds the entire request; individual phase
  ceilings cannot all be exhausted while promising completion inside that boundary.
- Main-generation input ceiling is 160,000 engineering tokens including 2,048 framing tokens;
  output cap is 16,384 including reasoning. Oversize input stops before sending, without silently
  dropping candidates, summarizing through another model, or retrying with a smaller K.
- Routes preserve the directed matrix including diagonal entries: K12 uses 144 elements in
  three requests; K16 uses 256 in four, at most 64 per request. Alternative routes measure at
  most 16 one-way elements; reverse estimates are not additional measured elements.
- Web tasks/page-fetch caps are 8/8; Nearby and Weather remain independent existing budgets.

<a id="b-8df8d48ff10e-2"></a>

Effective-config hash and YAML byte hash above identify different representations. Do not
reinterpret an effective hash as a file checksum. The shared default input ceiling remains
96,000; only the explicit quality configuration selects 160,000.

<a id="m-0e64dbb408d9"></a>
## Acceptance evidence index

_Source context: Operations, configuration and script inventory. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-0e64dbb408d9-0"></a>

The detailed result owner is the [Phase 6 recovery record](development_record.md#m-e07748f66be8).
The ignored recovery directory contains `manifest.json`, `v1_result.json`, `v2_result.json`,
`audit.json`, session/capture summaries, primary-before/after snapshots and query-vector capture.
Exact artifact filenames in the preserved log remain the authority if a local listing differs.
No raw/private payload is copied into Git by this consolidation.

<a id="b-0e64dbb408d9-1"></a>

The accepted request produced V1 24 new/24 compared/12 supplied/8 scheduled;
V2 16 RAG Details, 15 admitted reusable results plus 24 ordinary successes, 39 compared,
12 supplied, 8 scheduled including two RAG-only places. One resolved RAG identity missed
admission; 21 retrieval entities were not further resolved. Mixed sources did not reach supply.
Those observations neither require further expansion nor demonstrate a quality improvement.

<a id="b-0e64dbb408d9-2"></a>

Ordinary Details sends were 24 each, plus 16 RAG sends in V2. Both used baseline 144 and
alternative 16 measured route elements and three Nearby calls. Reviews/Profile did not run.
V2 Web reasoner usage remains unknown. RAG took 36.56 s, V2 Web 29.12 s, main generation
15.09/13.65 s and total V1/V2 42.05/106.41 s. Do not attribute all elapsed difference to RAG
or infer a complete bill. Different SQL queries taking 26.20/1.03 s are not a controlled
cold/warm experiment.

<a id="b-0e64dbb408d9-3"></a>

Preserve the two pre-send observer failures separately from explicitly approved recovery.
Historical complete quality regression remains 911 passed / 9 skipped / 1 failed, followed
by focused corrections. The later 103 input-guard checks and 62 harness checks overlap;
they do not retroactively make the earlier complete run green. This documentation task runs
no backend suite and does not claim additional runtime coverage.

<a id="m-8a56ee69ed6f"></a>
## Git save planning

_Source context: Operations, configuration and script inventory. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8a56ee69ed6f-0"></a>

The previous proposal grouped the coherent backend/config/scripts/tests checkpoint, the
existing frontend display changes, then documentation. It remains approval-pending. The old
179-path listing in [Phase 6 history](v2_development.md) is a snapshot,
not an instruction to stage now: these document moves require an updated inventory. Preserve
replacement files together with prior deletions and include current harness/160k changes.
Do not force-add captures, thesis notes, credentials, datasets or vectors.

<a id="m-8cd9200cc899"></a>
## Current POI acquisition and supply

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8cd9200cc899-0"></a>

The active policy prepares a useful bounded planning supply. It does not minimize a subset,
run B1/B2 evaluators, or restore QCGRE. See [architecture](shared_architecture.md) for the full flow.

<a id="m-37b19fce2d23"></a>
## Current TripWorld retrieval and V2 integration

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-37b19fce2d23-0"></a>

Phase 1-5 data/retrieval foundations are complete. Phase 6 main-candidate integration has bounded
normal-path development-live evidence. Old proposal text in history does not mean integration
is still pending. This does not freeze all V2 behavior or establish production performance.

<a id="m-f09bdc79ee48"></a>
## Corpus and persistence

_Source context: Current TripWorld retrieval and V2 integration. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f09bdc79ee48-0"></a>

Pinned metadata ingestion projects the approved eleven FSQ/Google identity, name, geographic and
category fields. Reviews, travel behaviors and place attributes are not part of this corpus.
Deterministic entity documents retain metadata identities/coordinates outside embedding text.
Production eligibility, entity deduplication and category enrichment precede persisted retrieval.
`retrieval_entities` artifacts/manifests and generated vector checkpoints are local ignored data.

<a id="b-f09bdc79ee48-1"></a>

OpenAI `text-embedding-3-small`, 1536 dimensions, normalized cosine vectors and ENRICHED text
remain the established space. PostgreSQL/pgvector performs geographic-filtered exact retrieval
with stable identity ties and compatibility checks. Runtime embeds bounded query texts only;
it does not regenerate corpus vectors. No ANN, inline shadow table or storage migration has
been applied as part of the accepted runtime path.

<a id="b-f09bdc79ee48-2"></a>

Versioned Git manifests live under `data/tripworld/`: `manifest.json`,
`embedding_model.v1.json`, `category_semantics.v1.json`, `retrieval_queries.v1.json`.
Exact historical counts/policy and corpus provenance remain in
[Phase 4](v2_development.md) and [Phase 5](v2_development.md).
The offline embedding job's retry/batch settings are not runtime query budgets.

<a id="m-f10c71668009"></a>
## Runtime ownership and evidence

_Source context: Current TripWorld retrieval and V2 integration. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f10c71668009-0"></a>

`backend/app/versions/v2/runner.py` and `config.py` own V2 entry/configuration;
`backend/app/policies/tripworld_query_plan.py` builds queries;
`backend/app/services/tripworld_discovery.py` handles bounded resolution and provenance;
`backend/app/tripworld/retrieval/runtime.py` owns database/query execution and compatibility.
Timing/error diagnostics distinguish connection/prepare, execute and fetch/decode, SQL timeout,
phase deadline and cancellation. SQLSTATE remains unknown when unavailable.

<a id="b-f10c71668009-1"></a>

Query vectors are captured only through opt-in development capture. Historical Tokyo vectors
were missing; compatible museums/cultural vectors were diagnostic substitutes, not exact replay.
Later accepted captures retain real query vectors and hashes. Original 3/30 failures, 60/180
functional validation, I/O variance and paused storage proposals remain in
[Phase 6 history](v2_development.md). Longer waiting budgets are not a
performance optimization. Current timeouts and backup boundaries are in [operations](development_guide.md).


<a id="m-03a6868a0b07"></a>
## Reproducible development entry points

_Source context: Operations, configuration and script inventory. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-03a6868a0b07-1"></a>

Save this complete input as request.json locally (not a manifest wrapper):

Verbatim passages shared with another maintained section: [1](development_guide.md#b-61a2c7801de0-0), [2](development_guide.md#b-61a2c7801de0-2), [3](development_guide.md#b-61a2c7801de0-3), [4](development_guide.md#b-61a2c7801de0-4), [5](development_guide.md#b-61a2c7801de0-5), [6](development_guide.md#b-61a2c7801de0-6), [7](development_guide.md#b-61a2c7801de0-7). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="documentation-migration-20260920"></a>
## Documentation migration - 2026-09-20

Docs-only reorganization by responsibility and version; no code/configuration/runtime change.
Original files, including uncommitted content, were copied byte-for-byte before migration to
`logs/document_migrations/version_docs_20260919T225025Z/originals/`. Its manifest recorded paths,
sizes, SHA-256 and original Git state. This ignored, docs-only recovery point protected migration
and did not replace a source/database backup or alter captures/thesis notes. The snapshot, manifest
and associated migration materials were later deleted by user authorization on 2026-09-20.

The section migration ledger (deleted with the migration recovery materials on 2026-09-20) mapped every original
heading (including inherited context), source file hash and line range to stable destination
anchors, moved/merged/retained-as-superseded action, block-level shared locations and gaps.
The adjacent JSON ledger held the machine-readable mapping; a CSV supported inspection then.
Neither is available now.
No unique section is discarded merely because it is superseded. Navigation wrappers and former
root context are recorded as such. Verbatim repeated passages share content, while distinct attempt
context was recorded in the ledger; similar text with changed numbers was retained independently.

Current design was statically checked against request/requirement contracts, runner dispatch/CLI,
configuration, supply/acquisition, corpus builder and provider wiring. Current interpreted_requirements_3
is distinct from historical _2. Old six/eight task/pair limits stay in their historical records;
current V1 design distinguishes conservative defaults from explicit quality configuration.
The original 96k, 3/30, 60/180 and failed full regressions remain historical facts. No semantic-loss
claim is based on size/hash alone: causal conclusions, experiment conditions and uncertainty were
reviewed separately, especially the minimum-set diagnosis and bounded evaluator-value conclusion.

Frozen captures retain their old file paths. No executable source/test/script references to the
removed docs paths were found in the scoped static search; AGENTS examples are updated only for
new document locations. No compatibility shim containing duplicate prose is required.

At migration time, restoration used the manifest paths and verified original SHA-256 values.
That procedure is no longer available: the originals, manifest, ledger and check report were
subsequently deleted by user authorization. No .env/provider payload, raw dataset, vector or
database was included. Current documents preserve the narrative, not a recoverable copy of
every uncommitted intermediate document state.

Final migration checks: 549 original sections have destinations; no uncovered sections or missing
body blocks were found. 212 verbatim block occurrences share a maintained destination. All21
snapshot file hashes verified. Local maintained links/anchors, code fences and table shapes were
checked. Non-document hashes stayed unchanged. These mechanical checks supplement, rather than
replace, the causal/experimental-condition review in the local semantic_review.json artifact.
No backend/frontend tests, services, API calls or database operations were run. The old17 documents
and two directory layers were removed only after the recorded coverage verification. Original
bytes were recoverable outside active docs at that time, but the later authorized deletion
removed that recovery option; the original migration audit cannot now be fully repeated. The prior Git grouping needs a refreshed path inventory; staging,
commit/push and re-freeze remain unperformed.

<a id="single-runtime-config-20260920"></a>
## Single runtime configuration and unused result cleanup - 2026-09-20

User-approved default-policy promotion and limited cleanup, implemented and offline checked.
Prior quality_first_1 live observations remain explicit-config historical runs; no new live
acceptance, production SLA or version re-freeze is inferred from this change.

config/runtime.yaml now contains exactly the former runtime_quality_first_1.yaml bytes, SHA-256
416320cf286241cd1f00f84cc73e62ec388e03a7f41188456c0bb6fd652b84a0. Policy identity and numerical
values are unchanged. V1/V2 now select quality_first_1 automatically. The600s development wrapper
still needs its explicit argument. Product/developer APIs remain V0. Schema constructor defaults
remain available for explicit historical tests; normal runners load the canonical YAML.

Deleted the duplicate quality YAML, historical v2_development_override.json, its unused production
loader and unreferenced schemas/revised_v1_result.py (RevisedV1PlanningResult / b2_1). Active
PlanningSupplyPlanningResult and V2PlanningResult remain; no other B2 implementation was deleted.
Historical60/180 adapter tests construct typed values directly. Tests also exercise default60/360
and conflicting RAG override rejection. Payload sizing now reads config/runtime.yaml.

Pre-change recovery files and their SHA-256 manifest were created under
logs/config_consolidation/20260919T232229Z/ for the configuration migration. They were later
deleted by user authorization and are no longer available for restoration. Historical captures/manifests, thesis notes, database
and vectors are unchanged. Default selection changed, not the already accepted quality policy.

Offline results (overlapping scopes, not additive): initial focused modules104 passed/7 failed;
first correction86 passed/2 failed; subsequent affected modules50 passed. Broader affected
version/runtime/acquisition/API checks then239 passed/4 failed; the four affected modules passed32
tests after correction. Failures were old default-value, supply-count or implicit legacy override
assumptions, plus an incomplete test-only RuntimeConfig construction during correction. Tests for
legacy overrides now explicitly select conservative acquisition; normal-path tests use the new
default. Production selection/validation was not weakened. Ruff and git diff --check passed.
No full backend suite, paid/API/live call, DB operation, commit/push or re-freeze occurred.

<a id="runtime-tool-cleanup-20260920"></a>
## Runtime, tools and evidence cleanup - 2026-09-20

### Authority and behavior boundary

The user authorized deletion of retired algorithms and exclusive experiments, composition-based
extraction of active acquisition, maintenance-tool relocation, and permanent recovery-snapshot removal.
No replacement snapshots were created. No live/API/database calls, corpus/vector rebuilds, frontend
changes, stage/commit/push/reset/clean or re-freeze occurred. Contract/cache/policy/space versions,
active budgets, prompts, SQL and logging collection policy were not changed.

### Current dependencies and extracted responsibilities

| Previous location | Current owner | Consumers |
| --- | --- | --- |
| semantic_poi_pipeline.py active run/Profile/identity logic | services/candidate_acquisition.py | PlanningCandidateSupplyPipeline; V1 graph/state/projections and V2 shared graph |
| Old pipeline selection hooks | planning_supply_pipeline.py using composition | Existing deterministic supply policy |
| B2 fixture contract/candidate construction | tests/candidate_fixtures.py, no evaluator/projection object | Current review opportunities and RAG discovery tests |
| test_b2_integration.py active assertions | test_supply_integration.py | Current graph, costs, provenance, Profile and routes tests |
| test_b2_acquisition.py review assertions | test_review_opportunities.py | Evidence-linked Profile allocation |
| retrieval/entities.py builder functions | tools/data/tripworld/entity_builder.py | Corpus tools/tests; RetrievalEntity stays in runtime |
| retrieval/embedding.py batch functions | tools/data/tripworld/embedding_build.py | Data tools; vector validation/contracts stay in runtime |
| database/vectors.py write operations | tools/data/tripworld/vector_store.py | Database tools; space identity/validation stays in runtime |
| source.py hashing | tripworld/hashing.py | Shared integrity checks; download/validation moved to data tools |
| Data preparation, category enrichment, ingestion, batch embedding | tools/data/tripworld | Offline preparation and reconstruction |
| Database migration SQL and migration driver | tools/data/tripworld/migrations and database_connection.py | Explicit offline database tool only; SQL file contents unchanged |
| AcceptanceSession and requirement matrix | tools/validation | Offline tests and separately authorized live validation |
| SQL diagnosis and payload sizing | tools/diagnostics | Current mechanism diagnostics |
| Test-module payload evidence helpers | tools/diagnostics/itinerary_fixtures.py | Payload tool and current size test |

Static import closure from the three runners includes 36/86/102 modules respectively. This is an
import graph, not a claim that every imported function executes in every request. No application
module imports tools/tests or retired evaluator modules. Runtime tripworld keeps data contracts,
integrity helpers, geographic rules, exact SQL reading, query embedding and runtime observations.
The API continues to dispatch V0; independent V1/V2 scripts remain.

### Actual retirement

Removed SemanticEvaluator, semantic_evaluation, semantic_projection, semantic_set_selection,
the mixed semantic_poi_pipeline module, SemanticEvaluation schemas, six evaluator transport DTOs,
Foundry evaluator binding/options, SemanticEvaluatorConfig and its YAML section. Removed four B2
analysis/measurement/fixture scripts and three exclusive policy test modules; evaluator-only DTO
and configuration tests were removed from mixed modules. Current assertions remain without filtering
out hypothetical evaluator calls. The dead generic structured-client evaluator response branch was
removed; current requirement interpretation still uses its unchanged dedicated path.

QCGRE/B1 exclusive implementations were already absent at this checkpoint; active eligibility,
identity resolution and result structures in poi_selection/poi_funnel were not deleted by label.
Zero evaluator/subset counters in existing diagnostics remain zero without executable implementations.

### Logs, artifacts, cache and recovery deletion

Real planner/model/provider call records remain in logs, including historical runs; their dates,
identities, payloads and failed outcomes were not rewritten. Five inspected obsolete launchers plus
the inspected B1 live_matrix launcher were deleted. Three obsolete evaluator pickle object snapshots,
retired sizing/inventory files and bytecode of retired launchers were removed. No raw call response
was deleted. An initial broad cleanup command was rejected by automatic review; it did not execute.
Subsequent explicit operations used inspected files and authorized backup paths.

Retained artifacts each have a current purpose:

| Location | Reason |
| --- | --- |
| artifacts/diagnostics/retrieval_execution | Exact SQL failure-layer and timing evidence |
| artifacts/diagnostics/retrieval_storage | Pending EXTERNAL/TOAST/resource diagnosis |
| artifacts/diagnostics/candidate_supply | Current capacity/payload analysis and original validation outcomes |
| artifacts/validation/rag_integration | Current RAG implementation offline checkpoint |
| artifacts/validation/runtime_capture | Current harness lifecycle/recovery evidence |
| artifacts/validation/itinerary_output | Shared output contract checkpoint |
| artifacts/validation/requirement_boundary | Current input interpretation boundary evidence |
| artifacts/validation/shared_planner | Original failed/successful regression records, not retrospective all-green |
| artifacts/research/selection_objective | Key causal study explaining exit from minimum-set policy; no executable implementation retained |
| artifacts/maintenance/repository_cleanup | This task's path decisions, unreadable list and actual check outputs; no source copies |

Tokenizer vocabulary moved to .cache/tokenizer with its pinned integrity check unchanged.
Deleted logs/source_snapshots, logs/document_migrations, logs/config_consolidation and the external
D:/Workspace/Capstone/phase6_source_snapshots. Historical references now denote deleted checkpoints,
not usable recovery instructions. No backup was made of these removals.

Deleted file logical size: 9,427,502.0 bytes; recovery backups account for 8,958,575.0 bytes.
These are summed file lengths, not a measurement of physical disk allocation reclaimed.

Thirty-three inaccessible capture subtrees across twelve run roots were retained. Their parent
runs and embedded one-off scripts were not guessed disposable. Exact paths are in the cleanup
unreadable inventory. This exception means logs is not claimed perfectly free of all old scripts.

Logging remains console=true, trace enabled, metadata payload level, raw_provider_payloads=false,
LLM/tool/evidence capture flags=true, with unchanged redaction and usage semantics. File logging
is not claimed to contain every raw response under these defaults.

### Verification and limitations

- An initial focused command named a nonexistent test path: no tests ran; corrected invocation follows.
- First focused execution: 593 passed, 9 skipped, 19 failed (38.64s).
- Failures: one old test Review-service access path; eighteen acceptance tests blocked by a stale
  self-hash filename. Fixed without loosening assertions or adding skips.
- Affected modules: 62 passed (22.13s).
- Final dependency/tool/current-fixture focused checks: 34 passed (17.43s).
- Exactly one full backend execution: 834 passed, 9 skipped (50.82s). Existing optional database
  tests remained disabled with TRIPWORLD_TEST_DATABASE=0; no real database work.
- Subsequent saved-capture diagnostic check: 1 passed (1.76s).
- Final payload fixture ownership extraction: affected modules 37 passed (4.04s).
- No full-suite rerun after these narrow checks; no skip/xfail was added.
- Ruff and diff/link checks are recorded separately in cleanup artifacts.

The previous whole-config hash no longer applies because the unused evaluator section was deleted;
active numerical settings and policy identifiers are unchanged.
Current config/runtime.yaml SHA-256: `8842758f2e104d204e2bf42f75a4e17e39638c6cdfc1fe8ae2b169d271320e16`.

## Narrow runtime/offline responsibility split (2026-09-20)

The preceding cleanup completed the main dependency migration, not the separation of every
mixed helper module. This follow-up removes the remaining offline responsibilities in five
explicitly approved modules without changing planner behavior.

| Original module | Runtime responsibility retained | Offline destination |
| --- | --- | --- |
| `app/tripworld/artifacts.py` | Canonical JSON, fingerprints, JSON loading | `tools/data/tripworld/artifact_persistence.py` |
| `app/tripworld/manifest.py` | Immutable manifest contracts and loading | `tools/data/tripworld/source_schema.py` |
| `app/tripworld/database/vectors.py` | Space identity and compatibility | `tools/data/tripworld/embedding_config.py` |
| `app/tripworld/retrieval/embedding.py` | Shared vector validation | `tools/data/tripworld/embedding_config.py` |
| `app/llm/azure_foundry/requirement_capture.py` | Digest moved to `app/runtime/fingerprints.py` | `tools/validation/requirement_capture.py` |

The `app/` paths above are relative to `backend/`. Direct consumers and tests now import the
responsibility-specific modules. No compatibility wrapper remains. Runtime does not import tools;
offline tools reuse the runtime contracts. Timing/error telemetry and opt-in query-vector capture
remain runtime capabilities. Neither logging policy nor contract, corpus, policy or space IDs changed.

Twenty-four moved or retained definitions match their pre-move AST fingerprints. These fingerprints
are integrity records, not source recovery snapshots. Shared-integrity tests also assert single
definitions and stable canonical bytes, digest outputs and embedding-space identity.

### Verification evidence and incomplete full-run status

Evidence directory: `artifacts/maintenance/runtime_offline_split/` (local, ignored).

- Focused tests: **237 passed, 9 skipped in 28.20s**, recorded in `focused.txt`.
- One full backend run was started. Its redirected output stopped advancing for several minutes;
  the process was terminated rather than left waiting indefinitely. Exit code **-1**, no final
  pytest summary. `full_backend_first.txt` preserves the partial output. Buffered output advanced
  on termination, so the precise blocked test is not established. This is **not** a full pass.
- Health endpoint isolation: **1 passed in 1.95s**. This does not establish the cause of the stall.
- Remaining health/network/TripWorld/version modules: **191 passed, 9 skipped in 6.27s**,
  recorded in `remaining_modules.txt`.
- Preceding Web acquisition module plus health: **9 passed in 2.14s**,
  recorded in `health_preceding_module.txt`.
- These runs overlap; their counts must not be added or described as a successful single full run.
- The nine existing optional database skips used `TRIPWORLD_TEST_DATABASE=0`; no new skip/xfail
  or relaxed business assertion was introduced.
- Ruff and diff checks passed. No live calls, database work, new backup, staging or commit occurred.

Implementation and focused verification are complete. A successful single full-suite execution
remains unproven for this follow-up. The prior cleanup's 834/9 result remains a separate historical
checkpoint. Further investigation should capture the active test and stack at a bounded timeout,
not silently repeat an uninstrumented full run or change production behavior to obtain a pass.

### Full-suite lifecycle diagnosis and closure (2026-09-20)

Runtime/tool responsibility restructuring is complete. This follow-up addressed only the
unfinished full regression, without further module moves or architecture changes.

The previous run had buffered dot output, no per-test lifecycle trace and no final summary.
Consequently its precise blocking phase and root cause remain unknown. Health was not established
as the cause. The earlier interrupted run remains interrupted; it is not retrospectively passed.

One new diagnostic full run used the standard `python -m pytest backend/tests` entry with `-u`,
`-vv`, `--capture=tee-sys`, JUnit output and an artifact-local diagnostic plugin. The plugin flushed
collection, setup, test-body, teardown, session-finish and unconfigure events independently of
stdout. A supervisor imposed a 180-second process limit; no business timeout changed. Periodic
30-second faulthandler snapshots were observational only, not test failures or cancellation.

The run naturally completed: **848 collected, 839 passed, 0 failed, 9 skipped in 33.36s; exit 0**.
Supervisor elapsed time, including process startup/shutdown, was **36.58s**. The outer limit did not
fire. Lifecycle records show 848 completed setup/teardown pairs, 839 completed test bodies, normal
session finish/unconfigure and no unfinished phase. The longest recorded test phase was 3.16s.
The nine existing optional database tests remained disabled; no new skip or xfail was added.

The hang did not reproduce. There is no evidence identifying it as either a cleanup regression or
a pre-existing resource bug, and no production/test implementation repair was justified. No isolated
reproducer or affected-module rerun was needed after this successful diagnostic full run, and no
second full run was performed. This establishes the current complete regression result, not a
root-cause explanation or proof that the historical transient cannot recur.

Local diagnostic evidence is in `artifacts/maintenance/pytest_hang_diagnosis/`: `pytest.txt`,
`junit.xml`, `lifecycle.jsonl`, `lifecycle_summary.json`, `stacks.txt` and `process.json`. The small
diagnostic plugin/supervisor are investigation artifacts, not application dependencies or backups.
Ruff and `git diff --check` passed. No live provider/database calls, snapshots, staging, commits or
re-freeze occurred. The runtime/tool cleanup can close with this successful full regression;
historical hang causation remains explicitly unconfirmed.


## Baseline closure after Sydney maximum-window smoke (2026-09-20)

Authorized scope: static audit, minimal shared chronological normalization, focused offline
verification and metric definitions. No live rerun or V3 implementation. The historical Sydney
run at logs/sydney_max_duration_smoke_20260920T072203Z remains unchanged.

Audit found accepted calendar dates but no remaining-hours contract; no reliable structured
private/employee-only visitor-access field; and no null-to-zero or null-to-budget-PASS conversion.
Commercial Google candidates with OPERATIONAL status and available Details therefore remain
visitor-suitability UNKNOWN. No admission, cost, date-window, prompt or budget change was justified.

Shared output validation now applies stable per-day start-time sorting after identity validation,
before downstream date validation/Nearby. All activity fields and references are preserved.
Private cost diagnostic field paths are reindexed to retain attribution; the diagnostic values
are unchanged. V0 calls this boundary directly; V1 and V2 share the tools graph boundary.

The metric-only definitions are in shared_itinerary_output.md and future-date evaluation policy
in shared_requirements.md. Requiring a two-day lead within the current ten-calendar-day window
limits future evaluation cases to eight days. No formal evaluation harness or freeze was created.
Verification results are recorded below after execution.

Focused offline execution: 78 passed in 3.01 seconds, exit 0. Scope: new ordering tests,
shared references, V0/V1 graphs, V1 reference stage, V2 tests and V1 itinerary cost mapping.
No full backend suite, live/provider/database calls or historical result rewriting occurred.
Ruff passed for the changed production and test modules; git diff --check passed.
A documentation append initially failed on the Windows default text encoding; it was retried
with explicit UTF-8. This was not a test or runtime failure.

The user clarified that this is a formal-evaluation baseline checkpoint, not permanent source
freeze. Shared correctness/contract/infrastructure fixes remain allowed in shared implementation
for every dependent version. Material changes require checkpoint impact recording and an explicit
evaluation-rerun decision. V3 adds only post-generation validation/targeted repair/re-validation;
it must not claim ordinary shared bug fixes as version-specific advantages.


<a id="v2-current-checkpoint-acceptance"></a>
## V2 current implementation acceptance and repository checkpoint audit (2026-09-20)

Status: **V2 current implementation checkpoint accepted.** User-authorized finite audit and
English documentation/local research-note updates only. No production/config/prompt/schema edits,
tests, live/API/database commands, stage/commit/push or re-freeze occurred in this task. The working
source remains unsaved in Git pending approval. This checkpoint ends primary V2 development/smoke
work and permits preparation planning, not automatic formal evaluation or V3 implementation.

### Evidence and chronology

- Tokyo: logs/cleanup_wiring_smoke_20260920T065908Z/{manifest,assessment,completion,retrieval_resources}.json,
  per-version *_result.json, *_events.json and calls/traces. Three real runners returned; V0/V1/V2
  elapsed approximately 23.55/40.06/104.98 s, with 9/5/7 primary activities. V2 normal RAG reached the
  final itinerary. Japan Weather 404 remained unavailable; this coverage outcome is not a RAG bug.
  Nearby preserved primary fields; completion/resource evidence records clean shutdown.
- Sydney: logs/sydney_max_duration_smoke_20260920T072203Z/{manifest,assessment,completion,retrieval_resources}.json
  and v0/v1/v2 result/events/calls plus primary_model_output and trace records. Frozen request:
  Sydney, 2026-09-20 through 2026-09-29, three travelers, total 6000 AUD, Opera House required,
  small museums/industrial heritage/local architecture and less-crowded preferences.
  Request hash 8fff6bcad6c9bffdb06900c2f7a6758fe5dfe34ceef96e525921989d077a02b2;
  effective config hash 50e3f70a7a7b878246c58f6cac17716c310404780e7f0a8d38caaee0137af8fc;
  config file hash 8842758f2e104d204e2bf42f75a4e17e39638c6cdfc1fe8ae2b169d271320e16.
  planning_request_2 / itinerary_2; gpt-5.6-luna; quality_first_1.
- Later shared stable chronological sorting is a separate offline correction, not rewritten
  Sydney output. Previous task's focused command covered itinerary ordering, references, V0/V1/V2
  graph/reference paths and V1 DTO: 78 passed in 3.01 s, exit 0; targeted Ruff/diff passed.
- Cleanup's completed full run: 848 collected, 839 passed, 9 skipped, zero failed, exit 0.
  Earlier incomplete/hanging/full-failure records retain their own outcomes. No new full run here.

| Sydney observation | V0 | V1 | V2 |
| --- | --- | --- | --- |
| Natural completed elapsed seconds | 41.99 | 106.88 | 90.22 |
| Primary activities / distinct identity | 17 / 17 name strings, no canonical verification | 21 / 14 canonical | 10 / 10 canonical |
| Empty dates | 0 | 0 | 4 (September 26-29) |
| References | 2 model knowledge | 3 Nearby | 3 Nearby |
| Admission / comparison / supply | Not applicable | 37 / 32 / 16 | 54 / 45 / 16 |
| Qualified cached Details / ordinary new successes | Not applicable | 0 / 32 | 13 / 32 |
| Baseline Routes | None | 4 requests / 256 elements | 4 requests / 256 elements |
| Reviews requests / Profile model calls | None | 8 / 8 | 8 / 7 |
| Weather | No external tools | HTTP 200, all 10 dates | HTTP 200, all 10 dates |

D10 effective C64/G32/ordinary send cap40/K16/P8 are limits/targets, not actual sends. Each V1/V2
ordinary acquisition stopped after 32 new successes. V2 had two user queries, one embedding batch
(10 tokens), two SQL result sets Top-K20, 40 positions/34 unique entities, 16 resolution attempts,
13 resolved (12 direct, one fallback), four fallback searches and 18 unattempted entities at cap.
V2 comparison: 32 Google-only plus 13 RAG-only; supply eight each; scheduled five each, no mixed.
RAG elapsed 9.6869 s: embedding 2.1204, retrieval 0.26165, resolution 7.01844. SQL execute
0.24636/0.01329 s, fetch 0.000493/0.000828 s. These are not a controlled cold/warm pair.

Generation engineering inputs were 79578/79232 tokens for V1/V2 (provider inputs 77303/76957),
below 160000; output cap remained 16384. Shared capacities worked, but repeats, uncertain visitor
access, opening/time contradictions and empty days mean itinerary quality is not established.
All unknown costs remain unknown. Profile evidence can remain partial/unavailable. V2's saved
actual query-vector NPZ is local evidence; early Tokyo vectors remain missing, not reconstructed.

Nearby invariance was supported by saved primary/final business-field comparisons, allowing
reference/source/role diagnostics only. The saved model-domain primary is earlier than the exact
post-identity-validation instant; do not describe that capture as a newly instrumented snapshot
at that instant. Resource captures report closed clients/DB/embedding resources, no pending tasks,
and natural process exit; they are bounded evidence, not a universal leak proof.

### Finite engineering triage

Sydney Web tasks 06f15a500f2583091cb7 (477 Pitt St, ChIJGc9K8EGuEmsRDrot7_uI1xg) and
2c528cefde4d15b7603d (Surry Hills, ChIJW7w1-SGuEmsRkMwyFmh9AQU) were residual_missing operational
needs. Both supplied Place records had website_uri=null and tasks allowed_domains=[]; no Web/page
request was made. PlacesAdapter and normalization preserve websiteUri; configured HTTPS domain
policy is unchanged. This is expected lack-of-authorized-evidence behavior in the inspected cases,
not a demonstrated mapping failure. Tokyo task 2d8af70b54e4d4506b28 bound Bunkamura's
www.bunkamura.co.jp, completed_with_sources with one search and two page targets, but zero accepted
facts. Its sufficiency/extraction outcome is separate from Sydney's pre-send authorization gate.

No new material baseline correctness defect was established. SQL remains performance diagnosis;
visitor suitability remains UNKNOWN without supported public/private access evidence; chronological
sorting is fixed shared correctness. Missing evidence/provider coverage cannot be repaired by
inventing facts. Future V3 targets are explicit plan-level validation and targeted repair, not a
new candidate selector or a place to hide unfixed shared bugs. See the current known-issues triage.

### Checkpoint governance and follow-up scope

The formal-evaluation baseline checkpoint binds intended mechanisms to code/config/prompts/schema,
corpus/space and provider/deployment state. Shared correctness fixes remain allowed across every
dependent version, with a new checkpoint and explicit impact/rerun decision. No individual-case
prompt/budget tuning; no shared bug fixed only in V3. This is not permanent source freeze,
production readiness, formal benchmark completion or a RAG-superiority claim.

Weather -> Open-Meteo and [today,today+14] selectable dates with an independent <=10-day duration
are future shared infrastructure/request-contract TODOs. Current code remains [today,today+9].
No new provider, date logic or capacity change is implemented. Same-day remaining-hour limitation
persists; evaluation preparation should avoid it using a separately frozen future-date convention.

Reproducibility: source/build/schema/space are explicit; a functionally equivalent build is
supported by current code, but current relocated files must be committed. Exact saved vectors
and broad historical validation inputs remain local. The clean-room guide distinguishes public
rebuild, hash-verifiable artifacts and identical database contents; no new snapshot was created.


<a id="checkpoint-commit-plan"></a>
### Responsibility-based Git save: original proposal and execution

The following proposal and inventory describe the pre-commit audit. The subsequent execution
record below supersedes its pending-approval and test-execution instructions.

Audit base: feature/v2, HEAD 60902ac, empty index. Expanded inventory: 102 modified, 36 deleted,
121 untracked files = 259 paths; ordinary status collapses the latter to 75 entries. Historical
B1/B2 files created and deleted entirely in the uncommitted workspace do not appear as new Git
removals. Do not invent their deletion in a staged diff. Existing source/data/DB foundation commits
remain history; current relocation is not a fresh global embedding implementation.

| # | Proposed commit message | Responsibility / tests / dependency / risk |
| --- | --- | --- |
| 1 | refactor(tripworld): separate offline tools from runtime contracts | Relocate existing build/ingest/embedding/validation tools with pure runtime contracts/hash helpers and their migrated TripWorld tests. Standalone after HEAD; do not omit deleted old entry points, migration SQL or package initializers. No data rebuild or SQL policy change |
| 2 | feat(planning): establish shared structured-input and candidate-supply pipeline | Coherent shared contracts, interpretation, acquisition, quality capacities, two-pass Details, supply, output/Nearby, V0/V1 wiring and direct tests. Depends on 1. Includes inert RAG config/provenance contracts and extension seam required by common imports, not V2 execution. Splitting this into historical proposals would require unapproved transitional implementations |
| 3 | feat(v2): integrate bounded TripWorld discovery with shared planning | Runtime query planning/embedding/SQL/resolution/merge, independent runner/graph, RAG tests. Depends on 1-2. Do not omit timeouts/cleanup or confuse discovery source with Google resolution |
| 4 | chore(validation): preserve runtime acceptance and diagnostic tooling | Acceptance/capture plus candidate/payload/SQL diagnostics and tools-dependent tests. Depends on 1-3. Runtime send/usage hooks remain with their shared consumers in 2; tools own resource/capture orchestration. Excluding harness fixes would lose the validated checkpoint |
| 5 | fix(itinerary): normalize activity order without changing visit fields | Only stable sorting and private cost-path remapping hunks, plus test_itinerary_ordering.py. Depends on 2-3. Do not include scheduling/feasibility repair or rewrite historical smoke results |
| 6 | feat(frontend): display optional reference recommendations | Three current frontend files, including its direct test. Depends on shared output in 2. Does not fix form alignment or change engine dispatch |
| 7 | docs: record accepted V2 checkpoint and consolidate repository guidance | Current/historical documentation migration, root guidance, AGENTS policy delta and ignored artifacts/cache rules. Depends on 1-6. No thesis notes, raw evidence or snapshots; preserve historical failures and non-frozen boundaries |

Each group should import/build and pass its relevant tests at its own checkpoint. This is a
static plan, not a claim of tested intermediate commits: no staging or temporary checkout was
performed here. Most direct tests stay with implementation. Tests directly using acceptance/
diagnostic tooling, including requirement fixture replay and payload sizing, belong to 4; they
must not import not-yet-committed tools from 2. A static import scan found those dependencies and
moved their planned ownership accordingly. Full tests of all final paths remain necessary at the
final checkpoint if authorized by the later commit task; do not run paid tests.

**Required hunk split:** backend/app/policies/itinerary_output.py belongs primarily to 2.
Its dataclasses.replace and V1Itinerary imports, normalize_activity_order definition, and the two
return-site changes wrapping itinerary/result in normalize_activity_order belong to 5. Commit 2
returns the identity-validated object directly; commit 5 adds ordering and matching tests. Do not
stage the whole new file in 2 with sorting and then claim a later independent fix.

Other multi-responsibility files are deliberately kept coherent: config/runtime.yaml and
runtime/config_models.py include RAGConfig's inert typed settings in 2 together with
versions/v2/config.py and __init__.py; schemas/tripworld_discovery.py supports the shared source
union contract in 2. runner/graph extension callbacks are inert without V2 orchestration in 3.
Foundry client/DTO/mapping, evidence_acquisition, cache/budget and V0/V1 graphs carry the current
shared contract together; separating them by historical date would break imports/DTOs. Capture
hooks in those runtime files are prerequisites, not reverse dependencies on tools. Final status
and historical documentation go to 7 so earlier commits do not prematurely assert acceptance.

On later approval: inspect intended index stat/full diff and secret exclusions for each group;
verify the actual partial index/commit state, not merely a working tree containing later files.
Run the authorized offline checks appropriate to that state; stop on failures. Never alter
implementation just to manufacture a prettier split. No current intermediate group has been
tested by this audit. No stage/commit/push is authorized yet.

#### Exact changed-path inventory

Every changed/untracked Git-visible path is assigned below. A deleted path means retire/migrate it
in that group; it does not mean restore it. The one explicit cross-group hunk above is additional
to the primary path ownership. Unchanged pinned manifests, compose and tiny Parquet fixture are
already tracked and do not need artificial new commits.

##### Commit 1: 68 primary paths

- `backend/app/tripworld/__init__.py`
- `backend/app/tripworld/artifacts.py`
- `backend/app/tripworld/cli.py` (deleted)
- `backend/app/tripworld/corpus.py` (deleted)
- `backend/app/tripworld/database/audit.py` (deleted)
- `backend/app/tripworld/database/build.py` (deleted)
- `backend/app/tripworld/database/connection.py` (deleted)
- `backend/app/tripworld/database/ingestion.py` (deleted)
- `backend/app/tripworld/database/migrations/001_retrieval.sql` (deleted)
- `backend/app/tripworld/database/service.py` (deleted)
- `backend/app/tripworld/database/validation.py` (deleted)
- `backend/app/tripworld/database/vectors.py`
- `backend/app/tripworld/hashing.py`
- `backend/app/tripworld/manifest.py`
- `backend/app/tripworld/preprocessing.py` (deleted)
- `backend/app/tripworld/profiling.py` (deleted)
- `backend/app/tripworld/retrieval/embedding.py`
- `backend/app/tripworld/retrieval/entities.py`
- `backend/app/tripworld/retrieval/estimation.py` (deleted)
- `backend/app/tripworld/retrieval/openai_adapter.py` (deleted)
- `backend/app/tripworld/retrieval/sampling.py` (deleted)
- `backend/app/tripworld/retrieval/search.py` (deleted)
- `backend/app/tripworld/retrieval/spike.py` (deleted)
- `backend/app/tripworld/semantics.py` (deleted)
- `backend/app/tripworld/source.py` (deleted)
- `backend/tests/tripworld/conftest.py`
- `backend/tests/tripworld/test_database.py`
- `backend/tests/tripworld/test_manifest_source.py`
- `backend/tests/tripworld/test_openai_embeddings.py`
- `backend/tests/tripworld/test_preprocessing.py`
- `backend/tests/tripworld/test_profile_corpus.py`
- `backend/tests/tripworld/test_retrieval_foundation.py`
- `backend/tests/tripworld/test_semantics.py`
- `scripts/prepare_tripworld.py` (deleted)
- `scripts/tripworld_database.py` (deleted)
- `scripts/tripworld_retrieval.py` (deleted)
- `tools/__init__.py`
- `tools/data/__init__.py`
- `tools/data/prepare_tripworld.py`
- `tools/data/tripworld/__init__.py`
- `tools/data/tripworld/artifact_persistence.py`
- `tools/data/tripworld/cli.py`
- `tools/data/tripworld/corpus.py`
- `tools/data/tripworld/database_audit.py`
- `tools/data/tripworld/database_build.py`
- `tools/data/tripworld/database_connection.py`
- `tools/data/tripworld/database_ingestion.py`
- `tools/data/tripworld/embedding_build.py`
- `tools/data/tripworld/embedding_config.py`
- `tools/data/tripworld/entity_builder.py`
- `tools/data/tripworld/estimation.py`
- `tools/data/tripworld/migrations/001_retrieval.sql`
- `tools/data/tripworld/openai_adapter.py`
- `tools/data/tripworld/preprocessing.py`
- `tools/data/tripworld/profiling.py`
- `tools/data/tripworld/sampling.py`
- `tools/data/tripworld/search.py`
- `tools/data/tripworld/semantics.py`
- `tools/data/tripworld/source.py`
- `tools/data/tripworld/source_schema.py`
- `tools/data/tripworld/spike.py`
- `tools/data/tripworld/vector_store.py`
- `tools/data/tripworld_database.py`
- `tools/data/tripworld_retrieval.py`
- `tools/diagnostics/__init__.py`
- `tools/diagnostics/retrieval_service.py`
- `tools/validation/__init__.py`
- `tools/validation/retrieval_validation.py`

##### Commit 2: 128 primary paths

- `backend/app/api/developer/planning.py`
- `backend/app/api/product/planning.py`
- `backend/app/api/schemas/planning.py`
- `backend/app/evidence/experience_models.py`
- `backend/app/evidence/models.py`
- `backend/app/evidence/selection_models.py`
- `backend/app/evidence/selection_normalization.py`
- `backend/app/integrations/dispatch.py`
- `backend/app/integrations/google/places.py`
- `backend/app/integrations/http.py`
- `backend/app/integrations/models.py`
- `backend/app/integrations/protocols.py`
- `backend/app/llm/azure_foundry/client.py`
- `backend/app/llm/azure_foundry/dto.py`
- `backend/app/llm/azure_foundry/itinerary_cost_projection.py`
- `backend/app/llm/azure_foundry/mapping.py`
- `backend/app/observability/run_trace.py`
- `backend/app/policies/acquisition_opportunities.py`
- `backend/app/policies/experience_profile.py`
- `backend/app/policies/experience_selection.py` (deleted)
- `backend/app/policies/interpreted_requirements.py`
- `backend/app/policies/itinerary_output.py`
- `backend/app/policies/named_place_intent.py` (deleted)
- `backend/app/policies/official_web.py`
- `backend/app/policies/planning_supply.py`
- `backend/app/policies/poi_capacity.py`
- `backend/app/policies/poi_funnel.py`
- `backend/app/policies/poi_selection.py`
- `backend/app/policies/review_sensitivity.py` (deleted)
- `backend/app/policies/transport.py`
- `backend/app/policies/trip_intent.py` (deleted)
- `backend/app/runtime/budget.py`
- `backend/app/runtime/budget_limits.py`
- `backend/app/runtime/cache.py`
- `backend/app/runtime/config_loader.py`
- `backend/app/runtime/config_models.py`
- `backend/app/runtime/fingerprints.py`
- `backend/app/runtime/token_counting.py`
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/interpreted_requirements.py`
- `backend/app/schemas/itinerary.py`
- `backend/app/schemas/named_place_intent.py`
- `backend/app/schemas/planning.py`
- `backend/app/schemas/planning_supply_result.py`
- `backend/app/schemas/request.py`
- `backend/app/schemas/requirement_boundary.py`
- `backend/app/schemas/trip_intent.py`
- `backend/app/schemas/tripworld_discovery.py`
- `backend/app/services/candidate_acquisition.py`
- `backend/app/services/candidate_details.py`
- `backend/app/services/evidence_acquisition.py`
- `backend/app/services/generation_resources.py`
- `backend/app/services/official_web_integration.py`
- `backend/app/services/planning.py`
- `backend/app/services/planning_supply_pipeline.py`
- `backend/app/services/preference_interpretation.py`
- `backend/app/services/preference_prompts.py`
- `backend/app/services/reference_discovery.py`
- `backend/app/services/review_selection.py`
- `backend/app/services/web_evidence_acquisition.py`
- `backend/app/versions/v0/graph.py`
- `backend/app/versions/v0/prompts.py`
- `backend/app/versions/v0/runner.py`
- `backend/app/versions/v0/state.py`
- `backend/app/versions/v1/graph.py`
- `backend/app/versions/v1/official_web.py`
- `backend/app/versions/v1/prompts.py`
- `backend/app/versions/v1/runner.py`
- `backend/app/versions/v1/state.py`
- `backend/app/versions/v2/__init__.py`
- `backend/app/versions/v2/config.py`
- `backend/tests/api/test_developer_planning.py`
- `backend/tests/api/test_product_planning.py`
- `backend/tests/candidate_fixtures.py`
- `backend/tests/conftest.py`
- `backend/tests/evidence/test_opening_hours.py`
- `backend/tests/fixtures/requirement_boundary/captured_b_domain_draft.json`
- `backend/tests/fixtures/requirement_boundary/live_acceptance_cases.json`
- `backend/tests/fixtures/requirement_boundary/semantic_acceptance_cases.json`
- `backend/tests/fixtures/requirement_boundary/shared_structured_cases.json`
- `backend/tests/integrations/google/test_adapters.py`
- `backend/tests/integrations/google/test_nearby.py`
- `backend/tests/llm/azure_foundry/test_client.py`
- `backend/tests/llm/azure_foundry/test_dto.py`
- `backend/tests/llm/azure_foundry/test_mapping.py`
- `backend/tests/llm/azure_foundry/test_open_contracts.py`
- `backend/tests/llm/azure_foundry/test_v1_itinerary.py`
- `backend/tests/observability/test_run_trace.py`
- `backend/tests/policies/test_experience_selection.py` (deleted)
- `backend/tests/policies/test_named_place_intent.py` (deleted)
- `backend/tests/policies/test_official_web.py`
- `backend/tests/policies/test_planning_supply.py`
- `backend/tests/policies/test_poi_funnel.py`
- `backend/tests/policies/test_poi_selection.py`
- `backend/tests/policies/test_semantic_intent_migration.py` (deleted)
- `backend/tests/policies/test_transport.py`
- `backend/tests/policies/test_trip_intent.py` (deleted)
- `backend/tests/request_fixtures.py`
- `backend/tests/runtime/test_config.py`
- `backend/tests/schemas/test_request.py`
- `backend/tests/services/test_itinerary_references.py`
- `backend/tests/services/test_planning.py`
- `backend/tests/services/test_planning_supply_pipeline.py`
- `backend/tests/services/test_reference_discovery.py`
- `backend/tests/services/test_review_opportunities.py`
- `backend/tests/services/test_route_matrix_chunking.py`
- `backend/tests/services/test_shared_planning_input.py`
- `backend/tests/services/test_transport_evidence.py`
- `backend/tests/services/test_v1_candidate_funnel.py` (deleted)
- `backend/tests/services/test_v1_review_selection.py`
- `backend/tests/versions/v0/test_graph.py`
- `backend/tests/versions/v0/test_runner.py`
- `backend/tests/versions/v1/fakes.py`
- `backend/tests/versions/v1/test_graph.py`
- `backend/tests/versions/v1/test_interpreted_requirements.py`
- `backend/tests/versions/v1/test_named_place_extraction.py`
- `backend/tests/versions/v1/test_official_web_integration.py`
- `backend/tests/versions/v1/test_phase6_integration.py` (deleted)
- `backend/tests/versions/v1/test_places_contracts.py`
- `backend/tests/versions/v1/test_provenance_profile_regressions.py`
- `backend/tests/versions/v1/test_reference_stage.py`
- `backend/tests/versions/v1/test_runner.py`
- `backend/tests/versions/v1/test_semantic_safety.py`
- `backend/tests/versions/v1/test_supply_integration.py`
- `config/runtime.yaml`
- `pyproject.toml`
- `tools/data/prepare_tokenizer.py`
- `uv.lock`

##### Commit 3: 12 primary paths

- `backend/app/policies/tripworld_query_plan.py`
- `backend/app/services/tripworld_discovery.py`
- `backend/app/tripworld/retrieval/diagnostics.py`
- `backend/app/tripworld/retrieval/query_tokens.py`
- `backend/app/tripworld/retrieval/runtime.py`
- `backend/app/versions/v2/graph.py`
- `backend/app/versions/v2/runner.py`
- `backend/app/versions/v2/state.py`
- `backend/tests/services/test_tripworld_discovery.py`
- `backend/tests/tripworld/test_runtime_retrieval.py`
- `backend/tests/versions/v2/test_v2_runner.py`
- `scripts/run_v2.py`

##### Commit 4: 17 primary paths

- `backend/tests/llm/azure_foundry/test_requirement_acceptance_harness.py`
- `backend/tests/llm/azure_foundry/test_requirement_boundary.py`
- `backend/tests/llm/azure_foundry/test_requirement_semantics.py`
- `backend/tests/runtime/test_dependency_boundaries.py`
- `backend/tests/runtime/test_shared_integrity.py`
- `backend/tests/services/test_candidate_supply_diagnostic.py`
- `backend/tests/services/test_quality_first.py`
- `backend/tests/services/test_request_wide_preference.py`
- `backend/tests/tripworld/test_sql_diagnostic.py`
- `backend/tests/versions/v1/test_official_planner_size.py`
- `tools/diagnostics/candidate_supply.py`
- `tools/diagnostics/itinerary_fixtures.py`
- `tools/diagnostics/itinerary_payload.py`
- `tools/diagnostics/retrieval_performance.py`
- `tools/validation/requirement_acceptance.py`
- `tools/validation/requirement_capture.py`
- `tools/validation/runtime_acceptance.py`

##### Commit 5: 1 primary paths

- `backend/tests/policies/test_itinerary_ordering.py`

##### Commit 6: 3 primary paths

- `frontend/src/features/planning/components/ItineraryView.test.tsx`
- `frontend/src/features/planning/components/ItineraryView.tsx`
- `frontend/src/features/planning/types.ts`

##### Commit 7: 30 primary paths

- `.gitignore`
- `AGENTS.md`
- `PROJECT.md`
- `README.md`
- `docs/README.md`
- `docs/development_guide.md`
- `docs/development_record.md`
- `docs/frontend_design.md`
- `docs/frontend_milestone.md`
- `docs/frontend_mvp_milestone.md` (deleted)
- `docs/known_issues.md`
- `docs/poi_selector_architecture_review.md` (deleted)
- `docs/shared_architecture.md`
- `docs/shared_itinerary_output.md`
- `docs/shared_poi_supply.md`
- `docs/shared_requirements.md`
- `docs/tripworld_phase4.md` (deleted)
- `docs/tripworld_phase5.md` (deleted)
- `docs/tripworld_phase6_proposal.md` (deleted)
- `docs/v0_design.md`
- `docs/v0_milestone.md`
- `docs/v1_design.md`
- `docs/v1_development.md`
- `docs/v1_milestone.md`
- `docs/v1_selector_experiments.md`
- `docs/v2_design.md`
- `docs/v2_development.md`
- `docs/v2_milestone.md`
- `docs/v2_tripworld_data.md`
- `docs/v2_tripworld_retrieval.md`


#### Secret/generated-artifact scope and preservation

The 259 candidate paths were inspected for file types/size and high-signal key/private-key/
credential-URL patterns without exposing values: no matching secret pattern, binary file or file
over 1 MB occurred in this changed set. This is a bounded heuristic audit, not a cryptographic
absence-of-secrets guarantee. Existing tracked .env.example contains examples; the tracked tiny
TripWorld Parquet fixture is intentional. No full dataset/vector/database/capture was found among
the proposed paths. Review staged diffs again before any future commit.

thesis_notes, logs, artifacts, .cache, local .env/.env.tripworld and full TripWorld raw/processed/
artifacts/reports remain ignored. No ignore change was made in this task. DB lives in a Docker
named volume. Deleted source/document/config snapshots remain unavailable, not reintroduced.
Live captures and query vectors are local-only evidence, not backed up by the proposed commits.
No new backup/archive/recovery system was created. Some historical raw capture folders remain
permission-restricted; accessible summaries are not represented as a complete raw-response audit.


### Documentation-only audit checks

The 168 relative Markdown links/anchors in the twelve touched documentation/note files resolve;
code fences are balanced. One new milestone anchor was corrected before final verification.
A saved-artifact read initially used the Windows default codec and failed; the UTF-8 reread
succeeded without changing the artifact. All 259 Git-visible changed paths have one primary
commit-group owner; sorting alone has the explicit additional hunk split. High-signal secret
pattern checks over 387 Git-visible paths found no matches; no file over 1 MB was found in that
set. The existing 4692-byte tracked Parquet is the intentional tiny test fixture, not the dataset.
Non-document file SHA-256 values match the in-memory pre-edit audit; no production/config/test/tool
file was changed. git diff --check passed. Existing CRLF normalization notices are not test errors.
thesis_notes remains ignored, the index remains empty and no test/API/database work was performed.


### Approved seven-commit checkpoint execution

The user accepted the V2 current implementation checkpoint and authorized the seven groups above.
This was Git organization only: no backend/frontend tests, Ruff, build, live/API/model/embedding
calls, database operations or new implementation validation were performed. Earlier validation
remains historical evidence; intermediate commits were not independently built or tested.

| Group | Commit | Primary inventory paths | Responsibility |
| --- | --- | ---: | --- |
| 1 | dc0b871123d897214c5ffa16f21fade08c4230ed | 68 | TripWorld offline/runtime separation |
| 2 | a99dd983096609e0ea3a7072bdbdaedefcc93d5e | 128 | Shared structured input, acquisition, supply and output |
| 3 | 255b1ecebf535ce348c5c10d82df8ecded5768ae | 12 | V2 runtime RAG integration |
| 4 | 7959602753a5fc296c757c8e0691a0409ac3b0d5 | 17 | Acceptance and diagnostics |
| 5 | d9cb57e8beac4e52377048ddd9c3f76543da79d2 | 1 plus output sorting hunks | Stable chronological normalization |
| 6 | 39c5164ae3ca6c17d99d39d0f7f07d3b0330c4af | 3 | Frontend optional references |
| 7 | This documentation commit | 30 | Documentation and repository guidance |

The inventory still covers 259 unique paths; rename-aware Git file counts differ. The output
foundation was partially staged in group 2 without sorting imports/function/wrappers. Group 5
contains those sorting hunks and cost diagnostic index remapping, together with its direct test.
No other file required partial staging. Pure RAG settings/provenance and shared capture hooks
remain in group 2 as documented; execution is in group 3 and harness ownership in group 4.

The only new .gitignore hunk is generic /artifacts/ and /.cache/ exclusion, assigned to group 7.
TripWorld data/vector exclusions already existed. No thesis_notes ignore-policy change was made.
Approved whitespace-only cleanup removed extra EOF blank lines from six tools/data/tripworld
files (artifact_persistence, embedding_build, entity_builder, source, source_schema, vector_store),
candidate_acquisition.py, test_open_contracts.py and requirement_capture.py. No executable semantics
were changed to create commit boundaries.

Each group receives staged stat, name/status, full diff, whitespace and limited high-signal
secret/generated-file inspection before commit. These checks are not business validation or an
absolute security guarantee. Local thesis notes, captures, artifacts, corpus, vectors, credentials
and database contents remain outside the commits. No snapshots, temporary worktrees, push, tag,
history rewrite, re-freeze or next-stage work are included.

Committed build/database tooling closes the former clean-clone source gap. Functional rebuilding
is now repository-supported, not freshly demonstrated here. A complete immutable distributable
artifact bundle remains missing, and exact historical vectors/database state cannot be recovered
from Git alone. Existing local evidence remains necessary and is not backed up by these commits.

<a id="first-generation-coverage-20260920"></a>
## Shared first-generation coverage checkpoint - 2026-09-20

Status: authorized implementation and offline checks; no new live acceptance, benchmark
or re-freeze. Parent Git checkpoint: c8be30650ab7a66c9671770b9ab166f9edcf49a3.

### Motivation and preserved observations

Sydney's earlier ten-day outputs above remain unchanged. London run
bd3ba5e6-e380-44d6-b359-4d8f9c3415d7 completed at 2026-09-20T10:12:11.748730+00:00
in 51.2645 seconds, with four main visits on September 21-24 and empty September 25-27.
Its capture is logs/london_seven_day_smoke_20260920T101120Z/ (manifest.json, result.json,
retrieval.json, assessment.json, execution.json and traces/calls). Request hash:
40e27714f8093320bf482653a1041b53fbbf73ba34ac8b52c8ac4ac3ed6b48fe.
The request was London, September 21-27, three travelers, total4200GBP, with hiking,
zoo and amusement-park preferences. 44 admitted ->32 compared ->16 supplied ->4 scheduled;
three Nearby references were separate. Model output itself contained the empty dates.
This does not reveal the model's internal reason or prove the unused supply was unsuitable.

RAG stopped in connection establishment at about2.00035 seconds (prepare2.00125), before
embedding or SQL. RAG total2.08767 seconds did not exhaust360 seconds. TimeoutError had
no SQLSTATE. This is not a60-second SQL timeout. Connection tolerance is a separate
engineering change; no new database/provider calls were made to verify it here.

### Decision and implemented scope

The approved minimum extension uses K=max(min(16,max(8,2D+6)),2D), rather than a larger
buffer. D1-10 K:8,10,12,14,16,16,16,16,18,20. Acquisition uses the prior basis: long-trip
C64/G32/send40/P8. REQUIRED expansion remains <=16 and cannot silently extend upstream
work from K20. Baseline Routes400 elements/seven sends/64 per request; alternatives
unchanged. Shared prompts require full-range first-draft attention and a default2-5 main
visits, not mandatory daily compliance. Explicit roles and observational diagnostics
separate main visits, name proxies, canonical counts and non-main activities. No new
post-generation tools/model calls, repair or itinerary mutation were added.

An offline comparison in the preceding proposal considered K16/20/24: complete matrices
require256/400/576 elements and4/7/12 calls. K24 long synthetic input exceeded160k in that
proposal. These were diagnostic scenarios, not production capacities or measured live
quality. The selected K20 provides no spare unique supply above2D for a ten-day request;
shortfalls still return a legal observable draft.

### New-schema offline sizing and checks

Actual updated prompt/DTO serialization with local tokenizer, no network: K20 ten-day
normal input106111 tokens; long input131969, leaving28031 below160000. Both include400
baseline route elements,16 measured alternative elements plus16 mirrored estimates,
eight Profiles and48 synthetic accepted dated Web facts. Output cap remains16384 including
reasoning. These synthetic fixtures are not London/Sydney facts, worst-case bounds or
proof that a feasible schedule exists. Over-limit inputs still fail explicitly without
truncation, reduction, summary or regeneration.

Artifacts (ignored/local): artifacts/first_generation_coverage/payload_sizing.json,
focused.txt, focused_recheck.txt, focused_recheck_final.txt, full_backend.txt,
full_backend.xml, full_execution.json and post_full_recheck.txt.

- First focused run:426 passed,4 failed in31.19s. Old result-field/route-message assertions
  needed the approved new contract. First recheck54 passed,1 failed in4.74s exposed an
  edit-induced Unicode fixture encoding change; restored the original Unicode sample.
- Affected focused recheck:55 passed in3.72s, exit0.
- One full backend execution:870 collected,859 passed,9 skipped,2 failed in31.40s,
  exit1 (wrapper33.953s). Failures were API/shared-result exact-field assertions missing
  generation_diagnostics, not a hanging process. Preserve this run as failed.
- Corrected those assertions and added runner diagnostic assertions; affected recheck:
  45 passed in3.83s, exit0. No second full run; do not relabel the first run all-green.
- Existing mocked runtime tests cover SQL/cancellation/cleanup; added effective connection
  timeout check observes10 seconds for connect,60 for compatibility and60000ms server
  statement_timeout, with phase360 unchanged. No real waiting or database connection.

### Evaluation and future responsibility

This changes the shared prompt/DTO/output and capacity checkpoint. Do not attribute its
first-draft changes to RAG or V3; future comparisons require the same baseline and impact
review for any completed evaluation. There is no new live evidence of improved density.
[V3 design](v3_design.md) now records validation inputs, findings, eight categories,
targeted repair, finite work, UNKNOWN and re-validation plus16 future TODOs. It remains
unimplemented. Required/excluded protection and Nearby boundaries are preserved.

Final static checks for this package: Ruff (backend/tools) passed; git diff --check
passed; 22 introduced Markdown links/anchors checked with no errors. Local thesis note
V2-07 preserves this baseline-versus-V3 distinction and remains ignored. No live, API,
SQL query, vector/database rebuild, frontend change or push was performed.


<a id="london-coverage-live-20260920"></a>
## London seven-day V2 first-generation follow-up (2026-09-20)

Recorded on2026-09-22 from the existing run artifacts; no new London execution was performed.
Source: logs/london_coverage_smoke_20260920T112755Z/{manifest,result,session,retrieval,execution}.json
and its trace. Run3d7d5ea7-e2f4-41a8-914c-06c40cca55aa used real run_v2, London September21-27,
3 travelers,total4200GBP; English hiking/zoo/amusement-park preferences. One fresh run completed
in75.8645s, with no pending tasks and closed recorded clients. This was the Google Weather baseline.

Daily distinct main counts1/1/2/3/2/1/1: no empty or zero-main dates; three within default target,
four below. Eleven visits represented10 distinct canonical places, including a repeated Camley
Street Natural Park. Six free-time blocks and three Nearby references do not increase main counts.
Shared pool55 admitted ->11 cached qualified RAG Details +32 ordinary successes ->43 comparison
->16 supply ->10 unique scheduled. Three RAG-only scheduled identities were London Eye,
SEA LIFE London Aquarium and The London Dungeon; seven scheduled were Google-only, zero mixed.

RAG:3 queries/60 returned positions/53 entities,16 resolution attempts,13 resolved,11 admitted;
37 entities not attempted under the cap. SQL durations2.212/0.037/0.035s; connect0.017s;
RAG total15.12s. Ordinary Details13.79s, generation27.53s, Nearby1.719s. Weather returned200.
Two model calls used77354 input/4062 output tokens;1042 reasoning tokens are included in output.
Embedding1 batch/1 HTTP,12 tokens. Details32 ordinary+13 RAG; search8 including4 fallbacks;
Routes12 requests; Nearby3. No Profile/Official Web acquisition was triggered.

The user observed the absence of empty days as progress. This does not isolate prompt effects:
retrieval/provider evidence also differed from the prior run. Remaining limitations include four
below-target dates, repeated visits, club/event suitability and unknown prices. No repair/re-run,
formal comparison or universal first-draft guarantee follows from this observation.

<a id="shared-weather-date-20260922"></a>
## Shared Open-Meteo and date-window transition (2026-09-22)

Status: implemented and offline-validated; integrated planner live remains pending. The task's
final instruction explicitly authorized a minimal direct provider probe before editing. No other
live, model, Google, embedding or database operations were performed. Database reproduction was
deferred: no dump, bundle, isolated restore or reproducibility tooling work.

### Direct probe before implementation

Official forecast/terms documentation was checked. Application reference date2026-09-22
(Australia/Sydney), UTC request timestamp2026-09-21T16:19:05.814479Z. London coordinates51.5074,
-0.1278; explicit September27-October6 inclusive dates exercise delayed departure and10-day length.
Daily weather_code,min/max Celsius temperatures,maximum precipitation probability; timezone=auto.
The initial sandbox attempt failed locally with WinError10013. A separately permission-enabled
send returnedHTTP200 in1.437s,timezone Europe/London,10 date labels. October6 was null for all four
requested fields; nine dates contained values. This is partial actual coverage, not ten valid
forecasts. Wind was added to the final adapter from documented daily fields and tested offline;
it was not part of the live probe. No retries inside either HTTP client.
Evidence: logs/open_meteo_probe_20260921T161842Z/probe.json and network_probe.json.

### Implemented shared boundary

OpenMeteoWeatherProvider replaces Google Weather only. The shared tool factory still constructs
Google Places/Routes unchanged. One exact-date daily request, no geocoding or provider fallback;
neutral metric DTOs, documented WMO condition mapping, daily maximum precipitation probability
and wind. Response units/time zone are checked. Missing/invalid values remain unknown; a null
whole day is recorded in missing_dates, partial observations are retained, and failures degrade.
Provider/date/coordinate/timezone/metric selection separate cache identities. Existing budgets,
no-retry/cancellation semantics and request-local caching remain unchanged.

The shared calendar window is today..today+14 inclusive, independent of maximum duration10.
The previous capacity duration check no longer references the selectable-window constant.
The product frontend reads the same server-owned date window through /api/planning/date-window;
its end limit is min(start+9,allowedEnd). The developer page initializes its explicitly editable
reference date from that endpoint too. This fixes browser-zone drift without a time-planning engine.
Existing developer free-text/backend structured-request and optional-budget UI gaps remain out of scope.

Open-Meteo free API is non-commercial with CC BY4.0 attribution and published request limits;
public research/education are listed uses. Evidence and UI retain attribution. Forecast data may be
incomplete or inaccurate. Commercial deployment conditions need separate review. No source identity
or availability guarantee is inferred from a successful HTTP status.

No acquisition/supply formula, K20, Routes capacity, config numbers, prompts, activity roles,
generation diagnostics, RAG SQL/connection limits, engine default or database content changed.
V0 shares dates but calls no Weather. V1/V2 share the new provider; future V3 inherits it.

### Offline checks and exact first results

- First focused run:420 passed,14 failed,8.17s. Ten new capacity cases imported a misspelled
  function; four existing window tests retained old date boundaries/expected end. These were test
  migration errors, not reasons to weaken the new date contract. Corrected affected modules:
  56 passed,2.49s. Additional provider/cache/cancellation/runtime checks:82 passed,17.68s.
- One complete backend run:899 collected,890 passed,9 existing optional DB skips,0 failed,
  31.60s,exit0. No full-run repetition. External tests use fake providers/MockTransport.
- Frontend initial attempt could not create Vite temporary config under sandbox permissions.
  Permission-enabled first test execution:21 passed,3 failed (missed developer-page date-helper
  consumer). Updated developer consumer and mocks:24 passed,10.82s. No skip/xfail added.
- Frontend lint and TypeScript/Vite build passed. Ruff passed. Git diff check is recorded in
  the final task report. Reports: artifacts/weather_date_transition/. Existing regression/smoke
  checkpoints retain their original results and do not acquire this provider retrospectively.

### Next live proposal, not executed

At actual execution, freeze the same complete Sydney10-day request for V0/V1/V2 with
start=trusted_today+5,end=trusted_today+14. Retain the existing complete structured fixture's
non-date fields; no extra inducing preferences. At most one fresh run per version, separately
approved. V0 checks shared date/role output with zero tools; V1 checks Open-Meteo and shared K20,
Routes, diagnostics and Nearby; V2 additionally checks normal RAG. Record actual capacity/usage,
partial Weather dates and all UNKNOWN fields; never require all20 candidates to be available or
scheduled. No extra run for incomplete Weather, sparse output or RAG nonselection. The goal is
wiring/contract validation, not perfect itineraries, universal quality or a benchmark.

V3 validation/targeted repair/re-validation remains unimplemented. Shared fixes are not V3
contributions. There is no final live-validated closure or re-freeze at this checkpoint.


<a id="weather-window-14-20260922"></a>
## Fourteen-date product policy adjustment (2026-09-22)

The user superseded the15-date proposal with14 selectable dates including today:
start >= today,end <= today+13,inclusive duration1..10. The prior London probe is unchanged.
Its farthest requested day had null fields, motivating a conservative product choice, not a
claim that Open-Meteo supports only14 days, that15 days always fail, or that14 guarantees coverage.
Official maximum horizon, product admission and actual field coverage are distinct.

Only the shared window constant, boundary tests and current wording change. The frontend still
reads authoritative server limits. Duration, K20, budgets, Weather request/normalization, RAG,
roles, diagnostics, Nearby and no-retry policy remain unchanged. The earlier Sydney live proposal
is superseded by one frozen Tokyo ten-day request (today+4..today+13) for V0/V1/V2 sequentially,
conditional on offline checks. Actual execution outcomes will be recorded separately below;
this policy approval is not live acceptance. Same-day remaining hours remain unsupported.


<a id="tokyo-weather-window-live-20260922"></a>
## Fourteen-date Tokyo integrated smoke and authorized V2 rerun

### Policy, offline checks and frozen input

The user reduced the product window to today..today+13 inclusive (14 dates), retaining maximum
inclusive duration10. The earlier London null farthest-day observation motivated a conservative
product choice, not an API maximum or a guarantee of complete values inside the window.
The original probe at ../logs/open_meteo_probe_20260921T161842Z/ remains unchanged.
Focused backend96 passed in2.94s; frontend24 passed in10.59s; Ruff/diff passed.
Artifacts: ../artifacts/weather_window_14/focused.txt and frontend.txt.
The prior899-collected/890-passed/9-skipped full suite was not repeated or retroactively changed.

Frozen planning_request_2: Tokyo, Japan;2026-09-26..2026-10-05;3 travelers;600000 JPY total budget.
Preferences exactly: "I definitely want to visit Meiji Jingu. I prefer small museums and distinctive
local architecture. I also prefer less crowded places when possible." The manifest retains the
single-line original. Trusted reference date2026-09-22, Australia/Sydney; returned weather timezone
Asia/Tokyo. Both clocks had the same calendar date; no implicit date shifting occurred.
Request SHA-256:bcbce21449dcc5e4931c6e9e6ed614394007713dacce5146d8a639f2e877f322.
Effective config SHA-256:862d694487bdd1313ec1fc62856abca2cb5d0d56c0beb75a6dc771be7630eb36.
Current config/runtime.yaml, quality_first_1, gpt-5.6-luna, itinerary_2, explicit600s development
ceiling. C64/G32/send40/K20/P8, SQL60/RAG360/connect10 and160000/16384 unchanged.
Manifests hash implementation/prompt/schema files without copying source. Actual run_v0/run_v1/run_v2
used AcceptanceSession and independent request-local caches. Model cached tokens are provider-side,
not reuse of Google/Weather/Routes evidence across versions.

### Original failure and separate authorization

Original sequence: ../logs/tokyo_weather_window_smoke_20260921T170923Z/.
V0 began17:09:24 UTC,V1 at17:10:18,initial V2 at17:12:29. All returned itineraries, but initial V2
encountered TypeError before runtime construction: the assistant's capture factory accepted cfg,
whereas TripWorldDiscovery invokes a zero-argument factory. This invocation error was NOT proof
of database unavailability or a production retrieval failure. Embedding/SQL sends were zero.
Its129.56s Google-only result, full paid workload and itinerary remain intact.

The user then reported starting the database and explicitly authorized another V2 run.
Only the capture factory invocation was corrected; production, prompts, config and input stayed
unchanged. New run: ../logs/tokyo_weather_window_v2_authorized_retry_20260921T171522Z/,
17:15:22..17:17:56 UTC. No evidence cache was copied. There were FOUR actual planner executions:
V0 once,V1 once,V2 twice, the last separately authorized. No automatic retry or hidden replacement.
The original assessment.json covers both sequences and labels the first V2 as initial_degraded.

### Independent outcomes

| Measure | V0 | V1 | Authorized final V2 |
| --- | --- | --- | --- |
| Total seconds including cleanup | 53.95 | 131.39 | 153.66 |
| Main activity visits | 20 | 17 | 19 |
| Distinct primary identities | 20 name proxies | 14 canonical | 13 canonical |
| Days meeting default2-5 target | 9 | 7 | 9 |
| Empty/missing dates | 0 | 0 | 0 |
| Cross-day repeated visits | 0 name proxy | 3 | 6 |
| Supply / unused | Not applicable | 20 / 6 | 20 / 7 |
| References | 3 model knowledge | 3 Nearby | 3 Nearby |

Daily counts: V0=2/3/2/2/1/2/2/2/2/2;V1=2/1/2/2/2/1/2/2/1/2;
final V2=1/2/2/2/2/2/2/2/2/2. Meiji Jingu was scheduled in all three, by name only in V0.
V1 had3 unlinked free_time activities; all main activities in V1/final V2 were supply-linked.
All estimated_cost values remained null. Counts do not establish feasibility or visitor access.
V0's raw modern-art museum title/place_name discrepancy remains in its original result.

V1 and both V2 attempts each sent one independent Open-Meteo request forSep26..Oct5,timezone=auto,
Celsius/kmh. Each returnedHTTP200,Asia/Tokyo,10 dates with any valid field and10 complete dates:
all50 requested weather_code,temperature_2m_min/max,precipitation_probability_max,wind_speed_10m_max
values were present. Zero all-null/partial/missing dates; normalized available. Every date/value
matched the WMO/unit mapping and external_evidence.weather sent to generation. Evidence is each
open_meteo_daily_forecast.json,weather_evidence.json,itinerary_generation_request.json, plus
assessment.json. This single-case completeness is neither a future guarantee nor forecast truth.
V0 made zero external tool calls. Null/zero and failure live branches were not deliberately forced.

### RAG, acquisition and actual work

V1:41 Google observations ->40 canonical/admitted ->32 ordinary successes/comparison ->20 supply.
Final V2:41 Google observations ->56 union ->54 admitted ->13 cached qualified RAG Details plus32
ordinary successes =45 comparison ->20 supply. Two resolved RAG places were ineligible, not blocked
by C64. Both ordinary queues stopped at G32, not the40-send cap.

Final V2 ran two user queries: "Distinctive local architecture in Tokyo" and "Small museums in Tokyo",
linked to semantic_1/semantic_2. One embedding batch/HTTP200 attempt,10 tokens,2x1536 vectors in the
existing text-embedding-3-small enriched space. Two exact queries returned20 each,40 unique entities.
Execute21.5804/0.8584s; fetch/decode0.000327/0.000486s. Retrieval22.4402s; embedding3.8346s;
resolution10.7976s; RAG37.2326s. Different queries/uncontrolled caches are not a cold/warm experiment.
16 resolution attempts:15 direct-ID successes,1 non-unique fallback;15 Details,1 fallback search.
Two known Google overlaps retained mixed sources;22 entities were unattempted at the entity cap.
RAG partial reflects bounded processing, not SQL failure.

| Stage | Google-only | RAG-only | Mixed |
| --- | --- | --- | --- |
| Admission | 39 | 13 | 2 |
| Comparison | 30 | 13 | 2 |
| Supply | 14 | 6 | 0 |
| Scheduled unique | 10 | 3 | 0 |

Scheduled RAG-only identities: Murabayashi Building,Tokyo Building TOKIA,Shibuya Duplex B's.
Resolution does not convert discovery origin to Google; Nearby is not RAG adoption.
Actual query vectors and text/space/vector hashes are in the final run's v2/query_vectors/
query-49a038fa628445c9bdd22d15078a9720.npz. No corpus/vector rebuild occurred.

| Actual workload | V0 | V1 | Final V2 |
| --- | --- | --- | --- |
| Interpretation / Profile / generation calls | 1/0/1 | 1/8/1 | 1/8/1 |
| Text Search incl.destination/fallback | 0 | 4 | 5 |
| Ordinary / RAG Details | 0/0 | 32/0 | 32/15 |
| Review fetches | 0 | 8 | 8 |
| Weather | 0 | 1 | 1 |
| Baseline Routes requests/elements | 0/0 | 7/400 | 7/400 |
| Alternative Routes requests/elements | 0/0 | 9/16 | 8/16 |
| Nearby | 0 | 3 | 3 |
| Web search/reasoner/page fetch | 0 | 0 | 0 |

Initial degraded V2 additionally consumed1 interpretation,8 Profile,1 generation,4 searches,
32 Details,8 Reviews,1 Weather,16 Routes requests/416 elements,3 Nearby. Its input/output tokens
were121040/9214. This paid workload is not omitted; no complete invoice amount is inferred.

| SDK tokens, counted once per response | V0 | V1 | Final V2 |
| --- | --- | --- | --- |
| Input | 6284 | 121023 | 120119 |
| Output including reasoning | 6130 | 8247 | 7298 |
| Reasoning subset | 1245 | 3392 | 2308 |
| Cached input subset | 0 | 3943 | 9439 |

V1/final V2 engineering primary inputs111500/110842, remaining48500/49158 below160000.
Output cap16384 unchanged. Engineering and provider input counts use different framing conventions.
V1/final V2 seconds: interpretation9.44/7.70; discovery including RAG3.32/41.47; ordinary Details
21.40/24.08; Reviews/Profile/selection45.83/36.80; Weather1.34/1.25; Routes6.38/5.98;
Web decision0.05/0.05(zero external Web); generation41.44/35.03; Nearby2.14/1.13.
RAG is nested in discovery, not additive again. V0 provider timestamps give14s/38s for interpretation/
generation at integer resolution; exact client stage latency was not captured.

### Integrity, limits and stop

Before/after Nearby main activity/date/order/identity/cost hashes match, as do generation diagnostics.
Main IDs belong to supply and references to successful Nearby ledgers. References do not overlap
scheduled IDs or count as visits/costs/REQUIRED. First-three-region bounds left11/10 V1/final-V2
anchors uncovered. Same-complex references remain (Ueshima tea room,Anjin within T-SITE).
A Profile ValueError occurred for ChIJA0JUXp6MGGARqD42zEq-4h8 in each V1/final V2; it degraded locally
without retry. Crowd support, public access, costs, repetition and target misses remain limited.

Both AcceptanceSessions closed owned model resources exactly once. Auxiliary clients closed;
final V2 PostgreSQL/embedding clients closed. No capture errors or pending asyncio tasks;
processes exited0. Runtime/config hashes were unchanged. This is observed cleanup health, not
an exhaustive leak proof. The initial V2 had no retrieval resource to close.

A: Shared14-date and independent runner wiring have bounded evidence; normal RAG only passed in
the authorized rerun. B: Weather had all50 fields in these requests. C: Generation targets were
not universally met. None implies the other, formal benchmark success, production readiness or
re-freeze. No post-generation repair, database reproduction, commit or V3 work was performed.

<a id="weather-date-closeout-profile-20260922"></a>
## Weather/date closeout: saved Profile response classification

This follow-up inspected existing captures and current code only. No production/tool code,
prompt, configuration or test changed; no tests, live calls or database operations were run.
The user accepts the bounded Weather/date/K20/Routes/input-protection and normal RAG evidence,
not universal correctness, a quality benchmark or re-freeze.

The user additionally reports that the database was not started during the first V2 attempt,
and was started before the authorized rerun. This is retained as user-provided environment
context, not a newly measured cause. The recorded invocation TypeError happened before database
initialization, so the old attempt cannot establish a connection timeout. No connection investigation,
timeout change or rerun follows this clarification.

The capture factory issue belonged to the one-off invocation, not AcceptanceSession or a reusable
validation entry. TripWorldDiscovery calls runtime_factory() without arguments. Its production
default already closes over self.config. The successful development invocation likewise used a
zero-argument factory returning RuntimeRetrieval(config.tripworld_discovery,
capture_directory=case/"query_vectors"). No compatibility wrapper or production patch is required.
The first paid Google-only result and separate authorized normal RAG result remain distinct above.

### Two independently captured Profile failures

| Run | Existing session.json | Call ID |
| --- | --- | --- |
| V1 | ../logs/tokyo_weather_window_smoke_20260921T170923Z/v1/session.json | 5052ccfb84864578a8a912404eb7ab7e |
| Authorized V2 | ../logs/tokyo_weather_window_v2_authorized_retry_20260921T171522Z/v2/session.json | 8ce8f492ca2d4747b53d1bf123d39c84 |

Both concern place ChIJA0JUXp6MGGARqD42zEq-4h8. Each model_input contains exactly one bounded
review, review_1. Its content describes design/branding services, not the supported visitor-experience
dimensions. The prompt explicitly requires review_count_used to equal the supplied usable count.
Each raw SDK response independently contains summary=null, summary_review_refs=[], signals=[],
review_count_used=0. Each domain_output preserves those values. Both HTTP responses completed;
each used577 input/94 output tokens, including39 reasoning tokens. These are already included in
the preceding run totals, not additional calls.

Foundry DTO parsing and domain mapping succeeded. The next shared validation in
policies/experience_profile.py::validate_profile_draft checks the matching Place ID, then rejects
0 != len(reviews)==1. The identifying guard's message is
"Profile review_count_used differs from bounded input". Historical trace saved only ValueError,
not its message/stack; this exact branch is established from saved input/domain output and the
current unchanged validation code, not claimed as an originally captured exception message.

Classification: controlled model-output contract violation, correctly rejected; no shared mapping,
configuration or provider-transport bug was found. Lack of supported experience evidence is a
separate observation: an empty signals/summary response would be legitimate with count1, but the
actual count0 violates the existing contract. The model's internal reason for choosing0 is unknown.

Both completed-profile events accurately report unavailable, signal_count0, review_count_used1
(the actual bounded input count) and profile_invalid_or_unavailable:ValueError. This is neither
"no reviews retrieved" nor negative crowding evidence. No returned valid signal or cited summary
was discarded: both were empty. The supplied review supports no defensible crowding/accessibility/
walking/family/duration inference; unrelated business-description text is not fabricated into one.
No retry, count rewriting, partial-response salvage or prompt change is warranted for these samples.

The Weather/14-date migration can close as implemented with bounded development-live validation.
This narrow review found no confirmed correctness blocker requiring repair before V3. Default-target
misses, repeated visits, unknown costs/access and unvalidated opening/route feasibility remain;
9/10 days meeting a count target is not9/10 days of validated itinerary quality. V0 name proxies
remain distinct from V1/V2 canonical statistics. Future shared correctness bugs remain fixable in
shared code; this closeout does not permanently freeze implementation.


## 2026-09-25: Shared Preference provider-response diagnostics

Case4/5 diagnostics alignment is implemented + offline-validated, not newly live-validated.
The shared adapter retains bounded provider facts; unknown HTTP400 is no longer presumed to be
configuration failure. Refusal/incomplete never fabricates a domain Safety/input classification.
Capture/cleanup preserve primary failure; internal details remain outside public error payloads.
See the Case4/5 checkpoint in shared_preference_input.md for the contract and actual chronology:
76 pass/2 fail (fixtures),146 pass;9 Ruff long lines;15 pass/1 fail (SDK usage unwrapping),16 pass;
148-pass affected regression; final Ruff/diff checks. Historical captures remain unchanged.
No prompt, taxonomy, budget, retries, model, travel functionality or frontend was changed.


## 2026-09-25: Three bounded shared Preference fixes

Implemented offline: explicit provider content_filter gets a distinct product provider_blocked
rewrite prompt without inventing Gate classification; services planning exports are lazy to break
the reproducible standard V0 CLI import cycle; preference_prompt_13 separates budget amount from
expense inclusion scope. V0-V3 shared contracts and product default remain intact. No retry or
budget change. New tests cover fresh CLI processes, public API isolation, compatible budget scope
and genuine budget conflicts. Tests:121 backend pass; frontend initial EPERM then16 pass; Ruff
formatting issues corrected; frontend build pass; affected backend76 pass; final static checks pass.
No real-model claim: prompt13 and the new user-facing recovery path await separate live approval.
