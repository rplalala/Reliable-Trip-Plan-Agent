# Capstone Project Context

Current source of truth. Updated 2026-10-03.
Detailed design, development and acceptance records are indexed in
[docs/README.md](docs/README.md).

## 1. Purpose and responsibility

This Capstone / Thesis B project builds an LLM-based travel planner for feasible
and reliable itinerary generation. It maintains four independently runnable
versions so their mechanisms remain distinguishable.

Current work covers system design, implementation, engineering validation and
approved RTPEval implementation. Formal benchmark construction/execution,
version-comparison experiments, thesis writing and final research conclusions
require separate authorization. Development smoke results are bounded evidence,
not general quality rankings or automatic version freezes.

[AGENTS.md](AGENTS.md) owns collaboration, language, approval, Git and archive rules.
Repository content is English; user-facing development discussion is Chinese.

## 2. Architecture and version boundaries

Use a modular monolith: React frontend; FastAPI API/application/backend services;
shared LLM, evidence, RAG and orchestration components with version-specific
entry points; PostgreSQL + pgvector for TripWorld retrieval.
External provider payloads are normalized before entering application policies.

| Version | Implemented mechanism | Independent entry point |
| --- | --- | --- |
| V0 | Plain LLM with shared input interpretation; model-estimated transport and optional model-knowledge references | `scripts/run_v0.py` |
| V1 | External place, weather, route and supported official/current evidence; shared candidate supply and post-primary Nearby | `scripts/run_v1.py` |
| V2 | V1 plus bounded TripWorld RAG discovery, Google identity resolution and canonical merge | `scripts/run_v2.py` |
| V3 | V2 plus structured validation, authorized targeted Repair and re-validation | `scripts/run_v3.py` |

V1-V3 share the tools-generation pipeline; V3 adds its own post-primary extension.
Shared correctness fixes must preserve the intended behavior of dependent versions.
Earlier milestone freezes retain their original scope; later changes are separately
recorded and do not automatically re-freeze any version.

Product UI/API uses V3 and an allowlisted presentation contract. Developer mode
exposes V0-V3 independently. Current input assistance includes destination suggestions,
currency/date controls and optional user-reviewed preference polishing.

Details: [shared architecture](docs/0001-system-architecture.md),
[frontend design](docs/0007-application-operations.md), and the
[version design index](docs/README.md#core-designs).

## 3. Current behavioral contracts

### Requirements and candidate supply

- `planning_request_2` supplies destination, supported dates, traveler count,
  whole-trip budget/currency and optional additional preferences.
- Nonempty preferences use one shared interpretation stage; empty preferences
  skip that model call. Application-owned requirements retain exact source and
  subject provenance. Unsupported hard conditions and unresolved required identities
  preserve clarification boundaries.
- Ordinary positive POI interests use soft targets of one distinct qualifying POI,
  or two for an explicitly sourced trip focus. Explicit counts, dates, exclusions
  and exclusive restrictions take priority. Broad enjoyment does not invent quotas.
- V1-V3 use bounded discovery, evidence acquisition, semantic assessment and
  deterministic candidate supply. Shared landmark opportunities remain available
  after preference targets are met. Candidate opportunity is not final fulfillment.
- V2/V3 use the existing TripWorld exact geographic retrieval and canonical merge;
  no new vector rebuild, ANN index or alternate persistence layer is implied.

Details: [requirements](docs/0002-requirements-evidence.md),
[POI supply](docs/0002-requirements-evidence.md),
[landmark discovery](docs/0002-requirements-evidence.md), and
[V2 retrieval](docs/0004-retrieval-persistence%28v2v3%29.md).

### Itinerary, transport and Repair

- The shared output is `itinerary_2`. Primary visits and optional unscheduled Nearby
  references stay separate. References do not satisfy required visits or count as
  scheduled activities or planned costs.
- V0 generates explicitly estimated transport activities without Routes calls.
- V1-V3 model output must not contain transport activities. Their primary DTO and
  shared output acceptance enforce the declared-role boundary; prompts also prohibit
  disguised transport. Application-owned `transfers` use Routes evidence. Models may
  use supplied route evidence to leave suitable gaps between visits.
- A forbidden declared transport activity fails generation without automatic deletion
  or an extra retry. Comprehensive semantic detection of disguised prose is not claimed.
- V3 uses bounded, permissioned patches and re-validates proposed/adopted results.
  It preserves prior accepted improvements when later attempts fail. No unsupported
  evidence is manufactured to turn UNKNOWN into PASS.
- Minimum daily coverage and optional quantity review are distinct. Sparse/overfull
  days do not automatically authorize arbitrary changes; review flags and permissions
  are recorded per run.

Details: [shared output](docs/0003-itinerary-transport.md),
[minimum coverage](docs/0003-itinerary-transport.md),
[V3 current design](docs/0005-validation-repair%28v3%29.md), and
[transport correction acceptance](docs/records/evaluation/intake-identity-usage.md#rtpeval-transport-correction-acceptance).

## 4. RTPEval implementation status

Evaluation is independently run over a curated, source-linked batch. Planner
validation, caches and internal decisions are not independent factual ground truth.

| Ticket | Implementation checkpoint |
| --- | --- |
| 01: Intake/projection | Implemented and offline-validated, including provenance, transport sources and [ordinary-output compatibility](docs/records/evaluation/intake-identity-usage.md#rtpeval-ticket-01-03-acceptance) |
| 02: Usage capture/report | Implemented and offline-validated; opt-in attempt capture, no automatic formal run |
| 03: Identity/adjudication | Implemented and offline-validated; independent supplied-ID/name-search paths, manual review and automatic-result audit; structural claims and optional typed-address evidence supported |
| 04: Evidence snapshots | Implemented and offline-validated through injected transport; linked identity snapshots also supply route coordinates offline; not a built-in operational Google client |
| 05: Requirement/schedule metrics | Implemented and offline-validated; [#17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17) closed as completed; local code publication pending |
| 06: Opening checks | Offline parser/scorer/CLI implemented and reviewed; [#18](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18) completed; [acceptance and scoped supplements](docs/records/evaluation/opening.md#rtpeval-ticket-06-acceptance) |
| 07: Route checks | Offline preparation/scorer/CLI implemented and reviewed, including decisive partial FAIL, zero-grace hard boundaries and the [snapshot-coordinate bridge](docs/records/evaluation/routes.md#snapshot-coordinate-bridge-2026-10-03); [#19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19) completed; [original acceptance](docs/records/evaluation/routes.md#rtpeval-ticket-07-acceptance) |
| 08: Multimetric report | Offline report/CLI implemented and reviewed; exact shared-mask scores with separate availability/provenance; [#20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20) completed; [acceptance](docs/records/evaluation/quality-report.md#rtpeval-ticket-08-acceptance) |
| 09: Blinded ranking | Offline package/import/report and React renderer completed; IANA time-zone selection, HH:mm and confirmed answer clearing; user-reported browser acceptance complete; [#21](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21) completed; [acceptance](docs/records/evaluation/blinded-ranking-record.md#rtpeval-ticket-09-acceptance) |
| 10: V3 before/after | Offline preparation/report/CLI implemented; adopted source lineage precedes unique fallback and residual review; separate paired mask, exact deltas and independent continuity; [contract](docs/contracts/0005-quality-human-review.md#v3-pairs) and [acceptance](docs/records/evaluation/v3-pair-report.md); [#22](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22) remains open pending separately authorized tracker synchronization/publication |
| 11-12 | Later approved work-plan tickets; no implementation is claimed here |

Evaluation uses transport activities for V0 and application transfers for V1-V3,
including optional V3 draft/final projections. Ignored sources retain provenance
and diagnostics but contribute no transport occupancy or fallback. Missing transfers
remain missing. Independent evidence is still needed for factual feasibility.

Route preparation can reuse coordinates already present in a verified independent identity
snapshot after canonical ID adoption. Missing, invalid or conflicting coordinates remain
local uncertainty; extraction adds no provider requests or planner/model work. The reviewed
coordinate envelope remains available. This bridge preserves V0-V3 planning behavior and
existing evaluation score/mask rules; see the [current contract](docs/contracts/0004-opening-routes.md#accepted-snapshot-coordinate-extension-2026-10-03).

Accepted Ticket 05 decision: same-scope overlapping protected intervals become one
occupancy blocker while preserving and checking each original obligation separately.
Different scopes must not be flattened. Protections are conflict boundaries, not
additional non-overlap score units. Explicit dated fixed-visit checks support exact
start, whole-window containment and minimum/exact duration. Unstated named-visit
counts permit exactly one visit for the trip, including fixed-time-only obligations.
Only explicit repeated-visit permission enables at-least-one time matching; explicit
count/date quotas still apply. Ticket 05 implements these rules after accepted intake;
see its [offline acceptance](docs/records/evaluation/requirements.md#rtpeval-ticket-05-acceptance). Unknown
applicability, identity, date/time or journey correspondence remains visible rather
than shrinking a denominator. Old identity reports require offline replay for the
extended fixed-time subject policy.

RTPEval migrated to [GitHub parent Issue #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12)
on 2026-10-01 under explicit publication/tracker authorization. All 12 Tickets are
published as #13-#24; 01-04 were closed/completed using their existing offline evidence.
GitHub owns formal specs, live task state, dependencies and discussion. Detailed
contracts remain in core docs and acceptance records in docs/records/; local source tickets are
historical planning aids. Completed legacy features are mapped in the
[2026-10-03 consolidation](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/36#issuecomment-5956795623). See the original [migration acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12#issuecomment-5956797691).

Current task state: [GitHub parent #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12).
Technical references: [historical work breakdown](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12#issuecomment-5956237972),
[evaluator design](docs/0006-independent-evaluation.md),
[package guide](backend/evaluation/README.md), and
[Ticket 05](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17).

## 5. Configuration, evidence and limitations

`config/runtime.yaml` and the typed runtime configuration own active tunable limits;
[config reference](config/README.md) explains them. Do not copy old budget values
from dated run plans into a new execution. Entry-point request deadlines and stage
budgets are distinct. [Development guide](docs/guides/development.md) owns commands.

Latest recorded full backend gate: **2409 passed, 10 skipped**, from the
2026-10-03 Ticket 10 post-review implementation, including **580 passed, 1 skipped**
evaluator cases and 52 new paired tests. Both review axes are closed after separate
correction commits. The skips are environment/opt-in cases; earlier
approved supplements remain distinct evidence.
Latest recorded full frontend gate: **98 passed**, with TypeScript, blind build and
lint passing for Ticket 09. These are dated development checkpoints, not formal
benchmark results. Failure/correction/retest sequences stay
in the [RTPEval records](docs/README.md#detailed-technical-contracts).

The authorized Berlin three-day smoke ran V0-V3 once each. V0 produced six estimated
transport activities. V1/V2/V3 produced no model transport activities and application
bindings for all 8/6/5 cross-place adjacencies. V3 had no authorized Repair targets,
so this batch did not exercise live Repair. The allowance is exhausted.

Remaining limits include partial RAG/evidence coverage, UNKNOWN opening/access/cost
facts, incomplete billed usage, retrieval performance variation and unresolved
semantic/identity cases. Structural transfer binding does not prove real-world
route feasibility. Earlier live Repair observations do not validate every later path.

Evidence owners: [latest smoke and closeout](docs/records/v0-v3/transport-responsibility-smoke.md),
[V3 development history](docs/records/v0-v3/v3-development.md),
[shared development history](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/development_record.md), and
[known issues](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/known_issues.md). Local logs/artifacts and ignored thesis archives
are evidence records, not current project authority or guaranteed fresh-clone assets.

## 6. Next work and authorization boundary

Tickets 01-10 have completed their approved implementation scopes. Ticket 10 local
delivery and offline acceptance do not authorize publication/tracker mutation or a
formal run. Tickets 11-12 require their own scope approval. Read the live
Issue and relevant contract before proposing the next task.

The 2026-10-03 documentation migration consolidates durable scratch specifications
into core docs and dated records, preserves local spec/child-ticket working files,
and maps completed legacy work to GitHub Issues. `.scratch/` is local and ignored;
published documents depend only on tracked repository assets or accessible remote
URLs. GitHub owns task state; local ticket copies are planning aids, not a second
live tracker. See [tracker conventions](docs/agents/issue-tracker.md) and the
[core design/proposal index](docs/README.md).

Local implementation/documentation commits are not automatically published. This
task authorizes document migration, legacy Issue mapping/closure and local commits;
it adds no live run, formal evaluation, next-ticket implementation or version freeze.
Push, merge and branch switching require separate authorization.

Per-ticket approvals and task discussion remain in the relevant GitHub Issues.

## 7. Keeping this file current

This file owns current scope, version boundaries, status, limitations and next work.
Update the relevant section in place when the state changes. Keep only the latest
clearly dated validation summary here; place full failure/correction/retest sequences,
per-run budgets, identifiers and commit diaries in their linked development or
acceptance records. Use [docs/README.md](docs/README.md) to locate those records.

Historical statements labelled Current/Next remain historical when preserved in a
record. They must not override this current summary or authorize another execution.
