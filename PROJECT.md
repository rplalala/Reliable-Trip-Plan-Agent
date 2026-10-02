# Capstone Project Context

Current source of truth. Updated 2026-10-02.
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

| Ticket | Implementation checkpoint |
| --- | --- |
| 01: Intake/projection | Implemented and offline-validated, including provenance and transport-source corrections |
| 02: Usage capture/report | Implemented and offline-validated; opt-in attempt capture, no automatic formal run |
| 03: Identity/adjudication | Implemented and offline-validated; strict supplied-ID and name-search paths, manual review and automatic-result audit |
| 04: Evidence snapshots | Implemented and offline-validated through injected transport; not a built-in operational Google client |
| 05: Requirement/schedule metrics | Implemented and offline-validated; [#17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17) closed as completed; local code publication pending |
| 06: Opening checks | Offline parser/scorer/CLI implemented under the 2026-10-02 approval; offline acceptance complete; Standards/Spec reviews clear, full regression 2148 passed / 10 skipped; all ten skips passed in subsequently approved scoped supplements; [#18](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18) closed as completed; [acceptance](.scratch/rtpeval/ticket-06-acceptance.md) |
| 07: Route checks | Offline preparation/scorer/CLI implemented and validated; longest unstated-departure fragment, zero-grace hard boundaries and decisive partial FAIL; Standards/Spec reviews clear; 86 dedicated tests passed; approved existing-test repair removes the former exclusion, latest unfiltered backend gate 2234 passed / 10 skipped / zero deselections; implementation and repair committed locally under the approved three-group closeout; [#19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19) closed/completed; [acceptance](.scratch/rtpeval/ticket-07-acceptance.md) |
| 08: Multimetric report | Approved offline report/CLI implemented; 39 dedicated tests passed; full offline gate 2273 passed / 10 skipped / zero deselections; committed at 5625f81 before clear Standards/Spec reviews; exact shared-mask verified scores and separate availability/provenance; [#20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20) closed/completed; [acceptance](.scratch/rtpeval/ticket-08-acceptance.md) |
| 09: Blinded ranking | Approved independent offline package/import/report and React renderer implemented; dedicated backend 26 passed and frontend 6 passed; final offline gates 2299 backend passed / 10 skipped and 89 frontend passed; pre-review implementation commits and separate privacy fix retained; both reviews clear after correction; actual file:// browser acceptance pending; [acceptance](.scratch/rtpeval/ticket-09-acceptance.md); Issue #21 stays open |
| 10-12 | Later approved work-plan tickets; no implementation is claimed here |

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
count/date quotas still apply. Ticket 05 implements these rules after accepted intake;
see its [offline acceptance](.scratch/rtpeval/ticket-05-acceptance.md). Unknown
applicability, identity, date/time or journey correspondence remains visible rather
than shrinking a denominator. Old identity reports require offline replay for the
extended fixed-time subject policy.

RTPEval migrated to [GitHub parent Issue #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12)
on 2026-10-01 under explicit publication/tracker authorization. All 12 Tickets are
published as #13-#24; 01-04 were closed/completed using their existing offline evidence.
GitHub owns live task state, dependencies and discussion. Detailed contracts and
acceptance records remain in the repository; local source tickets and the old
breakdown are preserved as historical snapshots. Other local feature trackers
retain their authority. See the [migration acceptance](.scratch/rtpeval-github-migration/migration-acceptance.md).

Current contracts and task links: [work index](.scratch/rtpeval/ticket-breakdown.md),
[evaluator design](docs/evaluator_design.md),
[package guide](backend/evaluation/README.md), and
[Ticket 05](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17).

## 5. Configuration, evidence and limitations

`config/runtime.yaml` and the typed runtime configuration own active tunable limits;
[config reference](config/README.md) explains them. Do not copy old budget values
from dated run plans into a new execution. Entry-point request deadlines and stage
budgets are distinct. [Development guide](docs/development_guide.md) owns commands.

Latest recorded backend gate, 2026-10-02, after the approved existing timeout-test repair:
**2234 passed, 10 skipped in 196.39s, zero deselections**. Both previously excluded
parameters now participate and pass; independent cold-process checks and all **16** runtime
retrieval tests also pass. The same actual-source red/green loop confirms the handshake
hang is fixed. The only executable follow-up change is that existing test function;
production budgets/behavior remain unchanged. Backend Ruff, changed-test compilation,
English/link and diff checks pass; Standards and Spec reviews each have zero findings.
Dedicated Ticket 07 route/CLI results remain **86 passed**. See
[repair acceptance](.scratch/timeout-test-diagnosis/repair-acceptance.md) and
[Ticket 07 acceptance](.scratch/rtpeval/ticket-07-acceptance.md) for the distinct historical
filtered/pre-boundary gates, original failures, corrections and retests.
The ten skips are nine opt-in database tests and one host symlink-privilege case;
Ticket 06 approved supplements do not count as Ticket 07 verification. Earlier results
remain in [Ticket 06 acceptance](.scratch/rtpeval/ticket-06-acceptance.md) and
[Ticket 05 acceptance](.scratch/rtpeval/ticket-05-acceptance.md).

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

Ticket 06 ([#18](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18))
completed its approved offline parser/scorer/CLI, tests, Standards/Spec reviews and
corrections. The [preflight](.scratch/rtpeval/ticket-06-preflight.md) preserves accepted
interface decisions; [acceptance](.scratch/rtpeval/ticket-06-acceptance.md) preserves the
implementation and database/UAC supplementary failure, correction and retest sequence.
All ten originally skipped checks passed in scoped supplements; the original full-suite
checkpoint remains unchanged. No persistent Windows security setting changed.

On 2026-10-02 the user authorized Ticket 06 workspace cleanup, current documentation,
local research archive, Issue #18/parent #12 synchronization and local commits, then
explicitly approved the three logical commit groups. The implementation and directly
related tests are committed at ee085d3; the independent database-test path correction
is committed at f62c07f. The third group records current contracts, preflight, acceptance
and project/package documentation. These commits remain local and unpublished.
Ticket 05 is committed locally at ed4c9a9; earlier migration/closeout approvals are
historical and do not grant additional Git actions in this task. Ignored research notes,
credentials, source payloads, logs and generated files are excluded from staging.

On 2026-10-02 the user authorized Ticket 07 route specification preflight
([#19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19)). Current interfaces
and primary provider documentation were checked; 59 existing snapshot/occupancy/time
regressions passed. The [preflight](.scratch/rtpeval/ticket-07-preflight.md) preserves
initial proposals, explanatory clarification and all three accepted user decisions:
allow waiting/use the longest continuous fragment when departure is unstated; honor
explicit departure; zero grace at applicable non-travel protections; independently
proved distance/time failure is decisive even with another UNKNOWN component.

The consolidated proposal defines deterministic ties, source-selected claims, independent
request mode review, exact query/time/endpoint applicability, raw provider precision,
preparation/scorer/CLI interfaces and separate component/coverage/burden reporting.
Specification preflight is complete; the user subsequently approved its concrete offline
implementation scope. Ticket 07 is implemented and offline-validated with clear reviews;
its original existing-test exception and subsequent approved correction are recorded in
[acceptance](.scratch/rtpeval/ticket-07-acceptance.md).
Preparation, raw interpretation, coverage and observed burden preserve missing evidence;
no planner path or Ticket 05/06 policy was changed. The original implementation/repair
validation used base 3427784b plus uncommitted changes. Issue #19 is closed/completed and parent #12
records 01-07 completed; subsequent tracker supplements retain historical validation and
record the corrected unfiltered gate. The user separately approved diagnosis and repair
of the existing embedding timeout-test hang.
[Diagnosis](.scratch/timeout-test-diagnosis/diagnosis.md) confirms an unbounded handler
handshake after a 20ms timeout expires during SDK cold preparation. The approved patch
is now applied to only that test function: direct timeout observation, bounded handshake,
child-task cleanup, ten-second scenario watchdog and five-second test-only SDK deadline.
[Repair acceptance](.scratch/timeout-test-diagnosis/repair-acceptance.md) records cold-process,
module and unfiltered full regression, and clear reviews. Production Retrieval budgets
and V0-V3 behavior remain unchanged. Ticket 08 specification preflight/implementation
requires separate approval; no next-ticket work is included.

The implementation approval covers offline route preparation/scoring/CLI, synthetic TDD,
relevant/full offline regressions, Standards/Spec review/corrections and related
documentation/archive/Issue updates. No formal case, real provider/model/database call,
commit/push, branch switch, freeze or Ticket 08+ work was included in that approval.
V0-V3 planner behavior and independent entry points remain unchanged.

On 2026-10-02 the user separately approved Ticket 07 closeout and three local commit
groups. Route implementation and directly related tests are committed at 2b66c9f;
the independent timeout-test repair is committed at b18daef. The approved third group
records current contracts, preflight, acceptance, diagnosis and project/package docs.
Before committing, the route/CLI, shared requirement/schedule and runtime retrieval
subset passed **166 tests in 34.26s**, with backend Ruff and diff checks passing.
The earlier full gate remains **2234 passed / 10 skipped / zero deselections**; no code
changed after that validation. No database/native supplement, live call, push, branch
switch, freeze or Ticket 08 work was added. Ignored archives, credentials, provider
payloads, runtime logs and generated pytest files are excluded from all three groups.
The [acceptance closeout](.scratch/rtpeval/ticket-07-acceptance.md#approved-local-git-closeout--2026-10-02)
preserves the actual commit responsibilities and pre-commit validation.

Ticket 08 [preflight](.scratch/rtpeval/ticket-08-preflight.md) was initially authorized
without implementation; its 275-test seam regression remains historical. The user then
explicitly approved the concrete offline implementation and local commits without push,
using the updated commit-before-review workflow. The review base is f1d6ecf.

Ticket 08 now implements a thin offline quality report/CLI over current scorers,
validated primary-visit identities and frozen evidence. Five verified scores use exact
P/(P+F+U), one mask/equal rational weights per request, true no-check zero contribution
and null unresolved-denominator scores/affected totals. Raw checks, magnitude/basis/
coverage/descriptive/burden records and exact source/rule hashes remain separate.
Label/content conflicts retain existing role-review diagnostics; there is no new
classifier/label penalty. Resource/human/mechanism reports remain not integrated, with
source usage/optional V3 availability distinct from actual analytical report availability.
Final v0-v3 reports only; paired deltas, formal comparisons and later tickets remain
separately authorized work. Planner/scorer policies and V0-V3 entry points are unchanged.

[Acceptance](.scratch/rtpeval/ticket-08-acceptance.md) owns actual red/green, regressions,
review and local Git closeout. Dedicated checks passed **39 tests**; the latest full
unfiltered offline gate passed **2273 tests / 10 skipped in 191.66s, zero deselections**.
Initial failures/corrections remain in acceptance. Implementation/direct tests are
committed at 5625f81 before Standards/Spec review; both axes returned zero findings.
Nine database opt-ins and one host symlink
case remain skipped; no database/native or live supplement is inferred from
Ticket 06 approval. Issue #20 is closed/completed and parent #12 records 01-08 completed
while remaining open. Initial automatic approval rejection was resolved after checking
the approved tracker scope/remote and reducing newly published metadata; final bodies
were read back exactly. The [tracker record](.scratch/rtpeval/ticket-08-tracker-update.md)
preserves that sequence without treating local files/commits as published source.
Local implementation/docs are unpublished; no push or freeze occurred during Ticket 08.

### Ticket 09 specification preflight — 2026-10-02

The user completed [specification preflight](.scratch/rtpeval/ticket-09-preflight.md)
and subsequently approved implementation with local commits and no push. Existing product itinerary rendering exposes provenance and can
omit unbound transfers; the proposed local anonymous renderer requires a separate
source-preserving display boundary. Researcher preparation/redaction is accepted,
with private source linkage and preserved travel facts/uncertainty. New complete
submitted answer revisions supersede old effective answers; older revisions remain
audit-only, drafts do not supersede submissions, and same-revision conflicts are errors.
Missing source arrivals may additionally show explicitly labelled departure-plus-duration
inference; this preserves the missing original field and never becomes scorer input.
The independent offline package/import/report and React renderer now implement these
rules, frozen balanced anonymous assignments, source-authoritative transport display,
ties/unjudgeable/N/A/drafts, save/resume and JSON backup/import, effective submitted
revisions, six mapped pairs and separate hidden-duplicate consistency. Original source
bytes, product routes and planner/scorer behavior remain unchanged. Dedicated checks
passed 26 backend and 6 frontend tests. Final committed post-review full gates passed
2299 backend tests / 10 skipped and 89 frontend tests; both static builds, Ruff,
compilation and lint passed. Implementation commits 6095877/d36b52d precede dual review;
Spec's single P1 exposed transport-source display differences. Separate fix 5f43b5d
unifies neutral Travel/time/duration fields and private batch-alias linkage. Standards
and Spec rechecks have no residual findings. Human reports remain independent of the
automatic quality report; V0-V3 behavior and execution paths remain unchanged.

Browser Use explicitly rejected file:// navigation; no workaround was attempted.
Manual synthetic direct-file display/narrow layout/refresh/download/reimport acceptance
is pending. [Acceptance](.scratch/rtpeval/ticket-09-acceptance.md) owns the actual sequence,
limits and local commit/review record. Issue #21 and parent #12 remain open. No actual
rater session, formal comparison, live/native supplement, push or freeze is authorized.

## 7. Keeping this file current

This file owns current scope, version boundaries, status, limitations and next work.
Update the relevant section in place when the state changes. Keep only the latest
clearly dated validation summary here; place full failure/correction/retest sequences,
per-run budgets, identifiers and commit diaries in their linked development or
acceptance records. Use [docs/README.md](docs/README.md) to locate those records.

Historical statements labelled Current/Next remain historical when preserved in a
record. They must not override this current summary or authorize another execution.
