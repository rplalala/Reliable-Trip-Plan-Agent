# Reviewed iteration commit groups

Status: Execution authorized after successful offline browser acceptance; reviewed groups below.
Date: 2026-09-26

## Execution receipt

- `0652222`: workflow configuration (4 files).
- `014c726`: backend capability, direct regressions and required tool migrations (71 files).
- `29647ef`: frontend completion presentation and regressions (6 files).
- `9c910b2`: new capture/replay tools and regressions (6 files).
- The final `docs: close semantic and quantity validation iteration` commit contains this
  receipt and the 18-file documentation group. Its hash is reported after creation, rather
  than embedded in its own content.

No push, PR or branch switch. Temporary integration hosts were stopped. Runtime artifacts,
local dependency links, caches and raw captures remain ignored and are not commit candidates.

Inspected branch: `feature/v3`; HEAD: `7748f3e91500b8dd5a6db11bd04900145ab0b83b`.
Index: empty at closeout. Entry inventory: 71 tracked modifications + 23 untracked files.
Final planned nonignored inventory: 105 files (includes API and approved review-policy follow-ups).

## Scope and execution boundary

This plan inventories the entire current uncommitted iteration, not just the last D run.
The user authorized reasonable grouping and local commits after offline acceptance without another approval. No branch switch, push or PR is authorized.
Order: 1, then 2, then 3 and 4 (both depend on 2), then 5. Implementation and direct
regressions stay together. Group 4 also carries integration regressions across the group 2
observer interfaces; existing core semantic tests remain in group 2.

Group review moved six existing diagnostic/acceptance files and their harness migration into
group 2: core regression tests directly import these adapters. New capture/replay capabilities
and their tests remain in group 4. A tracked-HEAD export plus groups 1-2 is used to check the
backend commit independently; no production changes are made to force a split. The initial
export lacked the local virtualenv and offline tokenizer vocabularies, causing environment
failures. Those local dependencies are supplied for validation only and are never staged.

The latest combined backend run is 1648 passed / 9 skipped, including API and review-policy fixes.
The exported backend candidate tree passed 1608 tests / 9 skipped after supplying local
test dependencies; the separately added tooling group passed its 40 tests. Frontend validation
was freshly repeated: 59 tests and TypeScript/Vite build passed. Source hashes match the
passing implementation checkpoint. Staged paths and whitespace are checked before each commit.

## Excluded evidence and other work

- Never stage `.env*` credentials, `logs/`, `artifacts/`, raw model/provider payloads,
  runtime captures, build outputs or dependency caches. Existing ignore rules cover them.
- Local ignored inventory: `artifacts/iteration_closeout_20260926/inventory.json`.
- No P3 implementation. No Penguin Beach / London Zoo follow-up: user declined it.
- Default quantity review and removal of the obsolete repetition switch are approved and included.
- No parent/exhibit policy changes, new live run, budget increase, version freeze
  or formal research work. Agent skill files outside this repository are not included.

## Group 1: `chore(agents): configure local issue and skill workflow`

Agent setup only. These changes predate the quantity task and must not be folded into its claim. No runtime dependency.

Exact candidate files (4):

- `AGENTS.md`
- `docs/agents/domain.md`
- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`

## Group 2: `feat(planning): add semantic goals and scoped visit repair`

Shared contracts, Foundry adapter, semantic policy/service, supply, V3 validation/repair, Product backend fields, configuration and direct regressions. Includes the approved Spec, named-visit, soft-quality and reference corrections in their final form. Keep intertwined backend changes together; do not create artificial chronological commits. Optional capture hooks and required migrations of existing tools belong here; new capture and replay adapters follow in group 4.

Exact candidate files (71):

- `backend/tests/runtime/test_config.py`
- `backend/tests/versions/v3/test_material_feedback.py`
- `backend/tests/versions/v3/test_minimum_coverage.py`
- `backend/tests/versions/v3/test_multiround.py`
- `backend/app/api/product/planning.py`
- `backend/tests/api/test_product_completion.py`
- `backend/app/llm/azure_foundry/client.py`
- `backend/app/llm/azure_foundry/dto.py`
- `backend/app/llm/client.py`
- `backend/app/policies/acquisition_opportunities.py`
- `backend/app/policies/generation_diagnostics.py`
- `backend/app/policies/generation_policy.py`
- `backend/app/policies/planning_supply.py`
- `backend/app/policies/poi_semantic_output.py`
- `backend/app/policies/visit_multiplicity.py`
- `backend/app/runtime/config_models.py`
- `backend/app/schemas/generation_diagnostics.py`
- `backend/app/schemas/interpreted_requirements.py`
- `backend/app/schemas/planning_supply_result.py`
- `backend/app/schemas/poi_semantics.py`
- `backend/app/schemas/product.py`
- `backend/app/services/candidate_acquisition.py`
- `backend/app/services/candidate_details.py`
- `backend/app/services/planning_supply_pipeline.py`
- `backend/app/services/poi_semantics.py`
- `backend/app/services/poi_semantics_prompts.py`
- `backend/app/services/preference_prompts.py`
- `backend/app/services/product_presentation.py`
- `backend/app/versions/v1/graph.py`
- `backend/app/versions/v1/runner.py`
- `backend/app/versions/v3/models.py`
- `backend/app/versions/v3/repair_acceptance.py`
- `backend/app/versions/v3/repair_candidates.py`
- `backend/app/versions/v3/repair_components.py`
- `backend/app/versions/v3/repair_feedback.py`
- `backend/app/versions/v3/repair_models.py`
- `backend/app/versions/v3/repair_pending.py`
- `backend/app/versions/v3/repair_projection.py`
- `backend/app/versions/v3/repair_service.py`
- `backend/app/versions/v3/repair_targets.py`
- `backend/app/versions/v3/validation.py`
- `backend/app/versions/v3/wiring.py`
- `backend/tests/fixtures/poi_semantics_london.json`
- `backend/tests/fixtures/preference_gate/historical_rich_trip_ambiguity.json`
- `backend/tests/llm/azure_foundry/test_requirement_boundary.py`
- `backend/tests/services/test_poi_semantics.py`
- `backend/tests/services/test_preference_gate_alignment.py`
- `backend/tests/services/test_preference_taxonomy_alignment.py`
- `backend/tests/services/test_quality_first.py`
- `backend/tests/services/test_request_wide_preference.py`
- `backend/tests/services/test_soft_quality_alignment.py`
- `backend/tests/services/test_visit_requirements.py`
- `backend/tests/versions/v0/fakes.py`
- `backend/tests/versions/v1/fakes.py`
- `backend/tests/versions/v1/test_runner.py`
- `backend/tests/versions/v1/test_supply_integration.py`
- `backend/tests/versions/v3/test_b_targets.py`
- `backend/tests/versions/v3/test_closeout_corrections.py`
- `backend/tests/versions/v3/test_repair.py`
- `backend/tests/versions/v3/test_semantic_repair.py`
- `backend/tests/versions/v3/test_target_locality.py`
- `backend/tests/versions/v3/test_validation.py`
- `backend/tests/versions/v3/test_wiring.py`
- `config/README.md`
- `config/runtime.yaml`
- `tools/diagnostics/repair_payload.py`
- `backend/tests/llm/azure_foundry/test_requirement_acceptance_harness.py`
- `tools/diagnostics/itinerary_payload.py`
- `tools/validation/requirement_acceptance.py`
- `tools/validation/requirement_capture.py`
- `tools/validation/runtime_acceptance.py`

## Group 3: `feat(frontend): show incomplete itinerary policy status`

Frontend presentation and transport/page tests. Depends on Product fields from group 2. Keep these six files together.

Exact candidate files (6):

- `frontend/src/features/planning/api.test.ts`
- `frontend/src/routes/product/PlanTripPage.test.tsx`
- `frontend/src/features/planning/components/ItineraryView.test.tsx`
- `frontend/src/features/planning/components/ItineraryView.tsx`
- `frontend/src/features/planning/types.ts`
- `frontend/src/routes/product/PlanTripPage.tsx`

## Group 4: `feat(devtools): capture and replay semantic repair evidence`

New semantic acceptance/diagnostic tools, normalized bounded capture/replay and corresponding SDK/graph/capture regression suites. Depends on group 2 interfaces, prompts and hooks. This is offline tooling plus previously authorized pilot support; no new live execution is part of a commit.

Exact candidate files (6):

- `backend/tests/llm/azure_foundry/test_poi_semantics_acceptance.py`
- `backend/tests/services/test_semantic_reference_capture.py`
- `backend/tests/versions/v3/test_quantity_replay.py`
- `tools/diagnostics/poi_semantics_payload.py`
- `tools/validation/poi_semantics_acceptance.py`
- `tools/validation/repair_replay.py`

## Group 5: `docs: close semantic and quantity validation iteration`

Current contracts/design annotations, chronological bounded acceptance, local specs and this closeout/plan. Depends on final behavior and validation of groups 2-4. Historical checkpoint statements remain explicitly historical.

Exact candidate files (18):

- `.scratch/iteration-closeout/commit-plan.md`
- `.scratch/quantity-quality-reuse/implementation.md`
- `.scratch/quantity-quality-reuse/spec.md`
- `PROJECT.md`
- `docs/README.md`
- `docs/frontend_design.md`
- `docs/poi_semantics_closeout.md`
- `docs/shared_architecture.md`
- `docs/shared_itinerary_output.md`
- `docs/shared_minimum_daily_coverage.md`
- `docs/shared_poi_semantics_plan.md`
- `docs/shared_poi_supply.md`
- `docs/shared_requirements.md`
- `docs/v0_design.md`
- `docs/v1_design.md`
- `docs/v2_design.md`
- `docs/v3_design.md`
- `docs/v3_development.md`
