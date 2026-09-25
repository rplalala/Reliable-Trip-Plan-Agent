# Documentation responsibilities and reading order

The root README directly introduces the project and quick start. PROJECT directly states current
scope/status and next approval. This index routes readers; detailed contracts and experiment
records have one responsibility owner instead of being copied into the entry documents.

## Recommended reading order

1. [Shared architecture](shared_architecture.md): version mechanisms and evidence authority.
2. [Requirements](shared_requirements.md): structured form, open semantics, subjects and HARD boundary.
3. [POI supply](shared_poi_supply.md): C/G/K, Details, cache, Profile and deterministic policy.
4. [Output](shared_itinerary_output.md): primary/reference roles, ledgers and generation ownership.
5. [V0](v0_design.md), [V1](v1_design.md), [V2](v2_design.md): version-specific orchestration.
6. [Development guide](development_guide.md): actual commands, configuration, scripts and preservation.
7. [Known issues](known_issues.md): bounded unresolved work and claim limitations.

## Version and engineering records

| Document | Responsibility |
| --- | --- |
| [v0_design](v0_design.md) | Tool-free shared-input/generation flow |
| [v0_milestone](v0_milestone.md) | Original freeze and later authorized changes |
| [v1_design](v1_design.md) | Google/tools and post-primary Nearby acquisition |
| [v1_development](v1_development.md) | V1-specific implementation, tool and Nearby records |
| [v1_milestone](v1_milestone.md) | Dated scope, checks, limitations and freeze boundaries |
| [v1_selector_experiments](v1_selector_experiments.md) | QCGRE/B1/B2 methods, observations and replacement rationale |
| [v2_design](v2_design.md) | RAG query/resolution/merge/budget/degradation integration |
| [v2_tripworld_data](v2_tripworld_data.md) | Pinned source, preprocessing, profiling method and entity text |
| [v2_tripworld_retrieval](v2_tripworld_retrieval.md) | Space, persistence, exact search and runtime diagnostics |
| [v2_development](v2_development.md) | V2-only retrieval/performance events and superseded proposals |
| [v2_milestone](v2_milestone.md) | Foundation/integration/limited-live acceptance scope |
| [v3_design](v3_design.md) | Current V3 validation, mixed transport and targeted Repair design |
| [v3_development](v3_development.md) | Chronological checkpoints, tests and bounded live evidence |
| [v3_milestone](v3_milestone.md) | Current delivery/evidence limits; not an automatic freeze |
| [development_record](development_record.md) | Cross-version evolution index and complete shared/joint events |
| [frontend_design](frontend_design.md) | Actual UI/API boundaries and accepted Product V3/four-version Developer MVP backlog; implementation deferred |
| [frontend_milestone](frontend_milestone.md) | Original frontend acceptance and dated changes |

## Evaluation design

[RTPEval evaluator research design](evaluator_design.md) owns the accepted evaluation design
with specification items still open. It includes the supplementary **V3 vs Codex + Travel
Planning Skill** comparison direction alongside the main V0-V3 study. Execution details
remain open; this is not a benchmark freeze or implementation/experiment authorization.

## Maintenance policy

Designs describe current behavior with short rationale, not test/token/timing diaries. Development
records own full events. Milestones summarize implementation/configuration, offline/live scope,
limitations, acceptance and freeze status, linking the full event. A joint run is recorded once.
Old configuration and proposals stay explicitly dated/superseded. Similar attempts with different
inputs or settings are not duplicates; overlapping tests are not summed. V3 current design, chronological development evidence and milestone status are separate.

Original section headings and context remain inspectable through stable m-/b- anchors. Exact repeated
passages may share a destination. The migration ledger recorded original occurrences, hashes,
line ranges and destinations at migration time; it and the recovery snapshots were later deleted
by user authorization. They are not available recovery or audit inputs now. Old artifact path
strings remain historical references. The creation and subsequent deletion are described in the
[documentation migration record](development_record.md#documentation-migration-20260920).

## Configuration cleanup after migration

The user subsequently approved quality_first_1 as the sole default runtime.yaml and removal of
unused RevisedV1PlanningResult. Historical section anchors and records retain their original
configuration paths; current operating instructions reflect the new default. This is not a new
live acceptance or broader B2 cleanup. The now-deleted document migration ledger described pre-cleanup content; it is not an available
restoration source or an immutable specification for later current-design edits.

Runtime/tool cleanup and evidence relocation are recorded in [the development record](development_record.md#runtime-tool-cleanup-20260920). Historical selector entries are evidence narratives, not supported executable commands.


## Current checkpoint navigation

[V2 implementation acceptance](v2_milestone.md#current-implementation-acceptance-2026-09-20)
is supported by the [joint Tokyo/Sydney evidence](development_record.md#v2-current-checkpoint-acceptance).
[Issue triage and Weather TODO](known_issues.md#current-checkpoint-triage-2026-09-20),
[clean-environment reconstruction](v2_tripworld_retrieval.md#clean-environment-reproducibility-audit-2026-09-20)
and the [approved exact-path commit grouping and execution](development_record.md#checkpoint-commit-plan)
have different responsibilities. The approved Git checkpoint saves this baseline; new provider
implementation and evaluation execution still require separate authorization.

- [Shared preference input gate](shared_preference_input.md): request dispositions, exact provenance, API/UI stop boundaries, offline tests and sizing; no real-model classification evidence.

- [Shared minimum daily coverage](shared_minimum_daily_coverage.md): product minimum, exemptions and version boundaries.

- [V3 final engineering closeout](v3_closeout.md): combined-tree validation, current limits,
  artifact-backed live/offline boundaries and checkpoint restrictions.
