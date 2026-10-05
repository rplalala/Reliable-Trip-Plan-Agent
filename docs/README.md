# Core design documentation

[PROJECT.md](../PROJECT.md) owns current scope and authorization. Start with the
[project proposal](proposal.md), then read the responsibility relevant to your task.
These core files consolidate current behavior; dated implementation diaries do not
belong in this directory. Task specifications and iteration state live in GitHub Issues.

## Core designs

| Owner | Contents |
| --- | --- |
| [0001 System architecture](0001-system-architecture.md) | Layers, Product V3, independent V0-V3 and lifecycle |
| [0002 Requirements and evidence](0002-requirements-evidence.md) | Interpretation, source provenance, semantic policy and supply |
| [0003 Itinerary and transport](0003-itinerary-transport.md) | Primary/reference roles, transport ownership and uncertainty |
| [0004 Retrieval (V2/V3)](0004-retrieval-persistence%28v2v3%29.md) | Corpus, persistent exact search and compatibility |
| [0005 Validation and repair (V3)](0005-validation-repair%28v3%29.md) | Permissions, components, re-validation and adoption |
| [0006 Independent evaluation](0006-independent-evaluation.md) | Submitted artifacts, evidence/scoring and planned boundaries |
| [0007 Application and operations](0007-application-operations.md) | API/UI, assistance, resources and engineering verification |

## Architecture decisions

- [0001 Version isolation](adr/0001-version-isolation.md)
- [0002 Application-owned transport](adr/0002-transport-ownership.md)
- [0003 Persistent exact retrieval (V2/V3)](adr/0003-persistent-exact-retrieval%28v2v3%29.md)
- [0004 Independent evaluation](adr/0004-independent-evaluation.md)

These ADRs record established consequential decisions, not a new implementation or freeze.

## Detailed technical contracts

Evaluation has five consolidated contract references: [artifacts](contracts/0001-evaluation-artifacts.md),
[intake/identity/usage](contracts/0002-intake-identity-usage.md),
[requirements/schedule](contracts/0003-requirement-schedule.md),
[opening/routes](contracts/0004-opening-routes.md), and
[quality/human review and V3 pairs](contracts/0005-quality-human-review.md).
These are continuous current rules with one owner per topic. Superseded proposals and
approval/validation history remain in records and linked Issues; legacy deep links resolve
to the corresponding current topic. Implementation status stays explicit in the evaluation
core design. Read only relevant contract sections.

## Other responsibilities

- [Development commands](guides/development.md) and [runtime configuration](../config/README.md).
- [Historical records](records/README.md): milestone freezes, development evidence,
  topic-specific validation and benchmark-design history. They do not override core design.
- [Agent entry point](../AGENTS.md) routes to [task/Git/skill workflow](agents/workflow.md),
  [version lifecycle](agents/versions.md) and [live smoke delegation](agents/smoke-tests.md).
  [Tracker conventions](agents/issue-tracker.md), [triage labels](agents/triage-labels.md)
  and [document ownership/archive rules](agents/domain.md) configure the engineering skills.
- [Current consolidation Issue #36](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/36)
  records this task's specification and acceptance; old-design comments identify successors.

Use numbered responsibility names for core design/ADRs. Add a version suffix only for
version-specific documents, such as `(v3)` or `(v2v3)` before `.md`. Shared documents
need no artificial all-version suffix. Merge related design into its existing owner.
Published links target tracked assets or accessible remote revisions; optional local
scratch and raw runtime evidence are not published dependencies.
