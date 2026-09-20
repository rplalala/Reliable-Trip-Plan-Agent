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
| [development_record](development_record.md) | Cross-version evolution index and complete shared/joint events |
| [frontend_design](frontend_design.md) | Actual UI/API boundaries and outstanding alignment |
| [frontend_milestone](frontend_milestone.md) | Original frontend acceptance and dated changes |

## Maintenance policy

Designs describe current behavior with short rationale, not test/token/timing diaries. Development
records own full events. Milestones summarize implementation/configuration, offline/live scope,
limitations, acceptance and freeze status, linking the full event. A joint run is recorded once.
Old configuration and proposals stay explicitly dated/superseded. Similar attempts with different
inputs or settings are not duplicates; overlapping tests are not summed. No V3 placeholder exists.

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
