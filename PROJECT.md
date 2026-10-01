# Capstone Project Context

Current source of truth. Updated 2026-10-01.
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

Details: [shared architecture](docs/shared_architecture.md),
[frontend design](docs/frontend_design.md), and the
[version design index](docs/README.md#version-and-engineering-records).

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

Details: [requirements](docs/shared_requirements.md),
[POI supply](docs/shared_poi_supply.md),
[landmark discovery](docs/shared_landmark_discovery.md), and
[V2 retrieval](docs/v2_tripworld_retrieval.md).

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

Details: [shared output](docs/shared_itinerary_output.md),
[minimum coverage](docs/shared_minimum_daily_coverage.md),
[V3 current design](docs/v3_design.md), and
[transport correction acceptance](.scratch/rtpeval/transport-correction-acceptance.md).

## 4. RTPEval implementation status

Evaluation is independently run over a curated, source-linked batch. Planner
validation, caches and internal decisions are not independent factual ground truth.

| Ticket | Current status |
| --- | --- |
| 01: Intake/projection | Implemented and offline-validated, including provenance and transport-source corrections |
| 02: Usage capture/report | Implemented and offline-validated; opt-in attempt capture, no automatic formal run |
| 03: Identity/adjudication | Implemented and offline-validated; strict supplied-ID and name-search paths, manual review and automatic-result audit |
| 04: Evidence snapshots | Implemented and offline-validated through injected transport; not a built-in operational Google client |
| 05: Requirement/schedule metrics | `ready-for-agent`; specification closed, implementation approval pending |
| 06-12 | Later approved work-plan tickets; no implementation is claimed here |

Evaluation uses transport activities for V0 and application transfers for V1-V3,
including optional V3 draft/final projections. Ignored sources retain provenance
and diagnostics but contribute no transport occupancy or fallback. Missing transfers
remain missing. Independent evidence is still needed for factual feasibility.

Accepted Ticket 05 decision: same-scope overlapping protected intervals become one
occupancy blocker while preserving and checking each original obligation separately.
Different scopes must not be flattened. Protections are conflict boundaries, not
additional non-overlap score units. Explicit dated fixed-visit checks support exact
start, whole-window containment and minimum/exact duration. Unstated named-visit
counts permit exactly one visit for the trip, including fixed-time-only obligations.
Only explicit repeated-visit permission enables at-least-one time matching; explicit
count/date quotas still apply. These rules are not yet implemented.

Current contracts and dependencies: [work plan](.scratch/rtpeval/ticket-breakdown.md),
[evaluator design](docs/evaluator_design.md),
[package guide](backend/evaluation/README.md), and
[Ticket 05](.scratch/rtpeval/issues/05-requirement-schedule-metrics.md).

## 5. Configuration, evidence and limitations

`config/runtime.yaml` and the typed runtime configuration own active tunable limits;
[config reference](config/README.md) explains them. Do not copy old budget values
from dated run plans into a new execution. Entry-point request deadlines and stage
budgets are distinct. [Development guide](docs/development_guide.md) owns commands.

Latest recorded closeout regression: **1983 passed, 10 skipped** on 2026-09-30;
Ruff and diff checks passed. Skips were optional database tests and a Windows
symlink-privilege case. This is a dated validation checkpoint, not a permanent
claim about all later workspaces.

The authorized Berlin three-day smoke ran V0-V3 once each. V0 produced six estimated
transport activities. V1/V2/V3 produced no model transport activities and application
bindings for all 8/6/5 cross-place adjacencies. V3 had no authorized Repair targets,
so this batch did not exercise live Repair. The allowance is exhausted.

Remaining limits include partial RAG/evidence coverage, UNKNOWN opening/access/cost
facts, incomplete billed usage, retrieval performance variation and unresolved
semantic/identity cases. Structural transfer binding does not prove real-world
route feasibility. Earlier live Repair observations do not validate every later path.

Evidence owners: [latest smoke and closeout](docs/transport_responsibility_smoke.md),
[V3 development history](docs/v3_development.md),
[shared development history](docs/development_record.md), and
[known issues](docs/known_issues.md). Local logs/artifacts and ignored thesis archives
are evidence records, not current project authority or guaranteed fresh-clone assets.

## 6. Next work and authorization boundary

Ticket 05 specification closure is complete; see the
[requirement/schedule contract](.scratch/rtpeval/requirement-schedule-contract.md).
Next proposed task: approve and implement its typed requirement checks, independent
time/occupancy preparation and offline report/CLI, including focused tests and
Standards/Spec review. Opening, routes and the auxiliary total retain separate tickets.
No Ticket 05 implementation or additional live run is currently authorized.

Previously approved snapshot, transport and smoke closeout changes have been committed.
That authorization does not authorize future Git writes, pushes, formal experiments
or version freezes. See AGENTS.md for the approval workflow.

## 7. Keeping this file current

This file owns current scope, version boundaries, status, limitations and next work.
Update the relevant section in place when the state changes. Keep only the latest
clearly dated validation summary here; place full failure/correction/retest sequences,
per-run budgets, identifiers and commit diaries in their linked development or
acceptance records. Use [docs/README.md](docs/README.md) to locate those records.

Historical statements labelled Current/Next remain historical when preserved in a
record. They must not override this current summary or authorize another execution.
