# Documentation responsibilities and reading order

The root README directly introduces the project and quick start. PROJECT directly states current
scope/status and next approval. This index routes readers; detailed contracts and experiment
records have one responsibility owner instead of being copied into the entry documents.

## Current context and detailed records

Start with [PROJECT.md](../PROJECT.md) for current scope, version boundaries,
RTPEval status and next work. Existing design documents own behavior contracts;
development records and `.scratch/` acceptance records own dated evidence.
The entries below include historical checkpoints: their Current/Next labels do
not override the current project summary. The original pre-cleanup PROJECT text
remains available in Git at `4736002:PROJECT.md`; the documentation cleanup is
recorded in [the development record](development_record.md#project-context-cleanup--2026-09-30).

## Berlin development smoke and follow-ups - 2026-09-28

Later, the user separately authorized an itinerary-only blind review despite the
original capture failure. One simulated traveler ranked V0 > V3 > V2 > V1 on the
saved outputs, before the V0 prompt adjustment; see the
[assessment addendum](../.scratch/berlin-six-day-smoke/assessment.md). This does not
change the original evidence gate or establish a general version ranking.

The subsequent user-requested [V0 transport/Nearby prompt alignment](shared_itinerary_output.md#v0-transport-and-nearby-content-alignment---2026-09-28)
uses model-estimated transport activities and optional nearby references. V1/V2 already
include Nearby. Eighty initial offline checks passed. The later authorized
[single V0 revalidation](../.scratch/v0-transport-nearby/assessment.md) passed with
17 main visits, 11 estimated transport activities and one Nearby suggestion;
combined relevant regression passed 176 tests. Real-world facts remain unverified.

Follow-up: the user accepted V1 repeats as a version limitation and authorized the
current [trace configuration](../config/README.md) increase to 10,000,000 bytes.
The old batch remains frozen at 1 MB with its missing trace and failed original gate.
The separately authorized blind review above used itinerary text only. The cap change
itself added no live run; V1 repeats remain an accepted intermediate-version limitation.

Outcome: all four applications completed, but V3's run trace was truncated and the
blind-review gate failed. V1 repeated visits; V3 repaired three sparse days while
retaining UNKNOWN findings. See the [assessment](../.scratch/berlin-six-day-smoke/assessment.md).

The archived [Berlin four-version plan](../.scratch/berlin-six-day-smoke/plan.md)
and [execution dispatch](../.scratch/berlin-six-day-smoke/dispatch.md) preserve the
identical six-day input and original limits. All four attempts were consumed; do not
reuse their commands as fresh authorization. Six offline launcher checks passed.
This is not a formal benchmark or freeze.

## Current preference and landmark closeout - 2026-09-28

The user approved [feature closeout](../.scratch/preference-landmark-balance/closeout.md)
and logical commits after the correction and bounded revalidation. No version freeze.

The subsequent [focus rule convergence](shared_requirements.md#focus-rule-convergence---2026-09-28)
removes inferred themed scope and keeps one/two soft targets. See the
[implementation and regression record](../.scratch/preference-landmark-balance/focus-convergence.md).
The [one-case Melbourne revalidation](../.scratch/preference-landmark-balance/pilot/focus-revalidation-assessment.md)
passed bounded focus acceptance in99.781s; it does not rewrite the earlier pilot failure
or establish universal reliability.

Tickets 01-03 are implemented; [integrated candidate balance](shared_poi_supply.md#preference-and-landmark-balance---2026-09-28) describes the current policy.
[Bounded landmark discovery](shared_landmark_discovery.md) describes the destination-only
model call, shared search allocation, exact identity, fallback and budget observability.
Candidate opportunity and final coverage remain distinct. The
[three-case V3 pilot assessment](../.scratch/preference-landmark-balance/pilot/assessment.md)
records successful execution but failed Melbourne focus-target interpretation at that
earlier checkpoint. The correction and revalidation above supersede that acceptance status.
No cross-version quality claim or freeze.

## Recommended reading order

1. [Shared architecture](shared_architecture.md): version mechanisms and evidence authority.
2. [Requirements](shared_requirements.md): structured form, open semantics, subjects and HARD boundary.
3. [POI supply](shared_poi_supply.md): C/G/K, Details, cache, Profile and deterministic policy.
   The [semantic extension checkpoint](shared_poi_semantics_plan.md#12-implementation-checkpoint--2026-09-26)
   owns candidate judgments, exploration, visit multiplicity and grouped compensation.
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
| [frontend_design](frontend_design.md) | Current Product/Developer UI/API boundaries, input assistance, and dated MVP backlog |
| [frontend_milestone](frontend_milestone.md) | Original frontend acceptance and dated changes |

## Evaluation design

[Benchmark construction design](benchmark_design.md) separately owns input construction,
completion screening, failure records and iteration recommendations. The user decides any
iteration and submits a curated batch to Evaluation; candidate admission does not trigger scoring.

[RTPEval evaluator research design](evaluator_design.md) owns the accepted evaluation design
with some specification items still open. It includes the supplementary **V3 vs Codex + Travel
Planning Skill** comparison direction alongside the main V0-V3 study. Tickets 01-04 have
separate offline implementation records. Ticket 05
[requirement/schedule specification](../.scratch/rtpeval/requirement-schedule-contract.md)
has an approved offline implementation and [acceptance record](../.scratch/rtpeval/ticket-05-acceptance.md).
No benchmark freeze or formal
experiment is implied.

RTPEval task state and discussion moved to [GitHub parent Issue #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12)
and its 12 children on 2026-10-01. Repository contracts/acceptance remain authoritative
for detailed meaning; local tickets are preserved historical snapshots. The
[migration acceptance](../.scratch/rtpeval-github-migration/migration-acceptance.md)
records actual mappings, state/label checks, 12 parent-child relations and 13 dependency
edges. This repository revision contains the tracker activation records. Other local
feature trackers are unchanged. [Ticket 05 #17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17)
is closed as completed after offline acceptance. Its
[completion comment](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17#issuecomment-5935469356)
and parent progress are updated; code and current acceptance documents remain local
and unpublished until a separately authorized push. The user approved one local
Ticket 05 feature commit; ignored thesis archives are retained locally.

The [readiness audit](evaluation_readiness_audit.md) checks the 2026-09-28 code checkpoint;
the [draft module specification](../.scratch/rtpeval/spec.md) records interfaces and remaining
rules. The [specification closeout audit](../.scratch/rtpeval/closeout-audit.md) separates
accepted scoring decisions from remaining contracts. These design documents alone do not
authorize later-ticket implementation or a formal run.

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

- [Preference coverage and local landmark balance specification](../.scratch/preference-landmark-balance/spec.md)
  (2026-09-27): **tickets 01-03 implemented**. Ordinary soft
  preference targets are one, or two for sourced trip focus. Final grounded coverage
  and Product feedback distinguish covered/gap/unassessed; V0 remains prompt-only.
  See [current semantics](shared_requirements.md#soft-preference-coverage--2026-09-27).
  Destination nomination and combined candidate balancing are implemented.
  Three V3 live cases completed on 2026-09-28; Melbourne failed focus-target interpretation.
  The later focus correction and one-case revalidation passed; user-approved closeout is
  recorded above. No formal evaluation or version comparison is claimed.

- [Planning input UX specification](../.scratch/planning-input-ux/spec.md): current GeoDB,
  currency/date, compact-weather and single-call Polish behavior, limits and evidence.
  [Frontend and API design](frontend_design.md#planning-input-assistance-update-2026-09-26)
  summarizes the current user and API flow. Historical review and two-call tests are dated
  in the local task records.

- [POI semantics iteration closeout](poi_semantics_closeout.md): current semantic/quantity
  completed acceptance, user-confirmed iteration closure, remaining boundaries and five executed
  local commit groups. Iteration closure does not constitute a new version freeze.

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

- [2026-09-27 semantic wire and budget closeout](development_record.md#semantic-wire-and-budget-acceptance-closeout-2026-09-27): three bounded live cases, offline budget audit, final regression, five local commits and remaining coverage limitations.

- RTPEval technical contracts: [artifact and human answers](../.scratch/rtpeval/artifact-contract.md), [evidence and time parsing](../.scratch/rtpeval/evidence-time-contract.md). Some offline modules are implemented; formal runs remain unauthorized.

- [Evaluation glossary](evaluation_glossary.md): shared benchmark/evaluation terminology; not project-wide context.

- [Ticket 10 V3 before/after preflight](../.scratch/rtpeval/ticket-10-preflight.md):
  current source/interface audit and accepted pair-mask/correspondence/review-first local
  uncertainty decisions, with complete specification confirmation. Implementation approval
  remains separate; no paired report is implemented.

- [Evaluation implementation work index](../.scratch/rtpeval/ticket-breakdown.md): live GitHub links for all 12 Tickets and the preserved pre-migration breakdown. GitHub owns current task state; repository acceptance records retain the approved offline scope.
- Local historical design archives: `thesis_notes/evaluation/` and `thesis_notes/benchmark/` (Git-ignored; not included in a fresh checkout). These are historical records, not project authority or formal research results.

- [Ticket 01 intake/projection contract](../.scratch/rtpeval/intake-projection-contract.md) (2026-09-29): implemented offline; preserves independent role/transport uncertainty.

- [Ticket 01 implementation guide](../backend/evaluation/README.md) and [offline acceptance](../.scratch/rtpeval/ticket-01-acceptance.md): batch preparation only; 38 passed, 1 platform-dependent skip. No scoring or live acquisition.

- [Ticket 02 capture/report guide](../backend/app/observability/USAGE.md) and [acceptance](../.scratch/rtpeval/ticket-02-acceptance.md): opt-in benchmark-side usage collection and independent researcher reports; no live experiment.

- [Ticket 03 identity contract](../.scratch/rtpeval/identity-implementation-contract.md), [guide](../backend/evaluation/README.md) and [acceptance](../.scratch/rtpeval/ticket-03-acceptance.md): offline identity association, adjudication replay and grounding report; independent live acquisition remains Ticket 04.

- [Ticket 04 snapshot contract](../.scratch/rtpeval/snapshot-contract.md), [guide](../backend/evaluation/README.md) and [acceptance](../.scratch/rtpeval/ticket-04-acceptance.md): injected acquisition, raw persistence and offline replay; no built-in live Google client.
- [Ticket 05 requirement/schedule contract](../.scratch/rtpeval/requirement-schedule-contract.md), [guide](../backend/evaluation/README.md) and [acceptance](../.scratch/rtpeval/ticket-05-acceptance.md): offline requirement/non-overlap scoring, independent time and occupancy review, descriptive schedule metrics; no five-dimension total or live execution.
- [Ticket 06 specification/interface preflight](../.scratch/rtpeval/ticket-06-preflight.md): checked opening provider encodings, existing snapshot/identity/time seams and proposed offline scope; accepted partial decisive-FAIL compliance denominator with separate evidence completeness. This preserves the pre-implementation inspection; the completed implementation is linked below.

- [Transport responsibility smoke and workspace closeout](transport_responsibility_smoke.md):
  three-day Berlin V0-V3 source/binding verification, unexercised live Repair,
  partial RAG/usage limits and the subsequent authorized commit checkpoint.


## Ticket 06 opening implementation — 2026-10-02

[Offline opening acceptance](../.scratch/rtpeval/ticket-06-acceptance.md) records the
implemented scope and actual failures/corrections/validation.
[Opening CLI and report wire](../backend/evaluation/README.md#ticket-06-offline-opening-compliance)
defines frozen-evidence replay, decisive partial FAIL, complete/partial coverage and
exact/lower-bound duration semantics. The
[preflight](../.scratch/rtpeval/ticket-06-preflight.md) preserves the original approved
interface audit. Current implementation/docs are local and unpublished; later tickets,
live evidence and formal evaluation still need separate approval.


## Ticket 07 offline route implementation — 2026-10-02

[Preflight](../.scratch/rtpeval/ticket-07-preflight.md) records current source authority,
snapshot/occupancy/time interfaces and independently checked provider semantics.
[Route contract](../.scratch/rtpeval/route-contract.md) retains accepted caps/reserve
and the accepted longest-interval/hard-protection/decisive-failure rules. The initial
59-test seam checkpoint preceded explicit implementation approval and remains historical.
[Offline acceptance](../.scratch/rtpeval/ticket-07-acceptance.md) records the implemented
preparation/scorer/CLI, actual failures/corrections, regression results and clear
Standards/Spec reviews. The
[package guide](../backend/evaluation/README.md#ticket-07-offline-same-day-routes) owns
route review/coordinate preparation, query applicability and report wire. Unknown
populations, partial decisive FAIL and observed burden remain separate from completeness.
The approved implementation/test closeout is committed locally and unpublished;
its [commit record](../.scratch/rtpeval/ticket-07-acceptance.md#approved-local-git-closeout--2026-10-02)
preserves three responsibility groups and the additional 166-test pre-commit check.
No live acquisition, formal evaluation,
auxiliary total, freeze or later-ticket implementation is included.

[Existing embedding timeout-test diagnosis](../.scratch/timeout-test-diagnosis/diagnosis.md)
records the subsequent diagnosis-only authorization, bounded reproduction, SDK cold-start
trigger and unbounded test-handshake defect. The user subsequently approved the single
test-function repair. [Repair acceptance](../.scratch/timeout-test-diagnosis/repair-acceptance.md)
records actual-source red/green, separate cold-process checks, 16 module tests passed,
clear reviews and **2234 passed / 10 skipped / zero deselections** in the full offline
backend gate. The original excluded-test checkpoint remains historical. No production
budget/behavior, live execution or later-ticket work changed. The separately approved
local test commit is b18daef; documentation accompanies the approved third group.

## Ticket 08 final quality report — 2026-10-02

[Preflight](../.scratch/rtpeval/ticket-08-preflight.md) maps the five quality dimensions
to current independent scorers, proposes the report/CLI wire and exact arithmetic,
and preserves shared masks, true N/A zero contributions and unresolved-denominator
availability. Existing source labeling conflicts remain role-review diagnostics;
identity UNKNOWN with a known visit count remains a scoreable outcome. Resource/human/
mechanism tracks and V3 pre/post work stay separate. The historical seam regression
passed 275 tests. Subsequent explicit approval authorized the implemented report/CLI,
synthetic tests and local commit-before-review closeout, without push. Current
[score profile](../.scratch/rtpeval/score-profile.md),
[metrics](../.scratch/rtpeval/metrics-contract.md) and
[artifact contract](../.scratch/rtpeval/artifact-contract.md) retain the proposed details.
The [acceptance](../.scratch/rtpeval/ticket-08-acceptance.md) records red/green, exact
mask/arithmetic/linkage checks, actual regressions and review/commit history. Dedicated
report/CLI checks passed 39 tests. The first full gate exposed a missing standard-library
fractions allowlist entry; only that directly related test permission changed.
Full retest: **2273 passed / 10 skipped / zero deselections**. Implementation/direct
tests were committed at 5625f81 before dual review; Standards and Spec returned zero
findings. [Package usage](../backend/evaluation/README.md#ticket-08-final-multimetric-report-and-auxiliary-scores)
documents the CLI and field scales. No formal result, live/native supplement, paired
V3 score or later-ticket work is included. [Tracker synchronization](../.scratch/rtpeval/ticket-08-tracker-update.md)
resolved the initial automatic approval rejection through verified existing tracker
authorization and a reduced metadata payload using the same GitHub interface. Issue #20
is closed/completed; parent #12 marks 01-08 completed and remains open. Local source/
documentation commits remain unpublished; no push occurred.

## Ticket 09 blinded ranking: completed acceptance - 2026-10-02

The independent offline anonymous package, revision-aware answer import, descriptive
pair/duplicate reports and React renderer are implemented. Current display uses a
UTC-default IANA selector, converted dates and HH:mm clocks. Original timestamp
controls and dedicated uncertainty/item/time-warning hints are removed; Inferred
arrival labels, ordinary source notes/preferences and frozen source facts remain.
Public/private hashes, answer/report schemas, scoring and V0-V3 behavior are unchanged.

Use [package usage](../backend/evaluation/README.md#ticket-09-local-blinded-ranking-workflow)
for preparation/import/report commands and reproducing the accepted synthetic checks.
[Consolidated acceptance](../.scratch/rtpeval/ticket-09-acceptance.md) owns the current
status and preserved validation history. Linked records distinguish
[preflight](../.scratch/rtpeval/ticket-09-preflight.md),
[time-zone conversion](../.scratch/rtpeval/ticket-09-timezone-display.md),
[timestamp-control/HH:mm cleanup](../.scratch/rtpeval/ticket-09-display-cleanup.md),
[uncertainty hint suppression](../.scratch/rtpeval/ticket-09-uncertainty-display.md) and
[tracker synchronization](../.scratch/rtpeval/ticket-09-tracker-update.md).

Latest UI gate: **98 passed / 13 files in 32.64s**, TypeScript/blind-review build/lint
passed and both review axes clear. Earlier backend gate: **2299 passed / 10 skipped /
zero deselections**; these are separate runs, with no new backend/native supplement.
Current ignored synthetic package is `artifacts/rtpeval/ticket09/public-clear-answers-final/review.html`.
[Confirmed clearing](../.scratch/rtpeval/ticket-09-clear-answers.md) clears only current
package local answers, preserves backups and handles failed writes/late imports.
Implementation precedes review; the pending-import P2 was fixed separately and both
rechecks are clear. User-reported display/time-zone/narrow checks passed on the prior
package; the user subsequently confirmed item 3 on the clearing-enabled workflow,
including submit/refresh, JSON download, clear/blank refresh and JSON reimport.
Native results are user reports, not independent tool observation; Browser Use's
file:// rejection was not circumvented. Ticket 09 acceptance is complete; Issue #21
is closed/completed, parent #12 marks 01-09 completed and remains open for 10-12.
Local commits/documents remain unpublished; this closeout reruns no implementation tests.
No real rater session, formal result, live/native supplement, push, freeze or later-ticket
implementation is included. An earlier
[scoped acceptance recheck](../.scratch/rtpeval/ticket-09-final-acceptance.md) passed
26 backend and 11 frontend tests plus exact package/asset and synthetic CLI replay
checks. Initial backend temporary-directory permissions were resolved using an
isolated workspace root/cache-disabled rerun; no runtime code changed during that
recheck. The complete observed sequence remains in the linked acceptance records.
