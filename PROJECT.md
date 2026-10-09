# Capstone Project Context

Current source of truth. Updated 2026-10-09.
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

[AGENTS.md](AGENTS.md) and its linked policies own collaboration, language, approval,
Git and archive rules; detailed rules are loaded for the relevant operation.
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
Supplied model identities now use request-local short references at the affected
provider boundaries, with exact restoration before existing domain/ownership checks;
see the [identity transport contract](docs/0001-system-architecture.md#model-identity-references).
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
- V1-V3 acceptance restores the authorized source's name and complete formatted
  address, including after V3 Repair. Generic activities and V0 retain model text;
  raw model captures and historical submitted outputs remain immutable.
- V0 generates explicitly estimated transport activities without Routes calls.
  New output includes structured mode and directed activity endpoints; absent/null
  declarations remain compatible with historical outputs. These are model estimates.
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
- V3 Repair's optional quantity review optimizes source-linked daily pace toward zero
  deductions. It accepts legal partial reductions and preserves the best accepted
  result at stops; zero is not a failure constraint. V0-V2 and V3 initial generation
  have no zero-penalty requirement.

Details: [shared output](docs/0003-itinerary-transport.md),
[minimum coverage](docs/0003-itinerary-transport.md),
[V3 current design](docs/0005-validation-repair%28v3%29.md), and
[transport correction acceptance](docs/records/evaluation/intake-identity-usage.md#rtpeval-transport-correction-acceptance).

## 4. RTPEval implementation status

RTPEval runs independently over source-linked submitted outputs. Planner validation,
internal findings and caches are not independent factual ground truth. The operational
`evaluation_run_cli prepare / execute / replay` flow captures independent evidence,
records actual requests/usage and produces native automatic reports for V0-V3 finals.

| Capability | Current behavior | Detailed owner |
| --- | --- | --- |
| Intake and identity | Original claims, source hashes and version-owned targets; V0 model correspondence, V1-V3 independent API/program checks without evaluator-model fallback | [Intake/identity/usage](docs/contracts/0002-intake-identity-usage.md) |
| Evidence and accounting | Frozen Search/Details/Matrix snapshots, failure receipts, source-linked coordinates, actual usage and explicit retail estimates when billing is unavailable | [Artifacts](docs/contracts/0001-evaluation-artifacts.md), [usage](docs/contracts/0002-intake-identity-usage.md#offline-cost-accounting) |
| Requirements and schedule | Explicit counts/dates/exclusions/fixed times; verified occurrence associations with separate grounding; V0 declared transport occupancy and V1-V3 transfers | [Requirements/schedule](docs/contracts/0003-requirement-schedule.md) |
| Opening | Current/regular API schedules take priority; missing-hours LLM assessment can infer ordinary public-landmark viewing, while explicit restricted activities and museum admission need access evidence; factual coverage stays separate | [Opening/routes](docs/contracts/0004-opening-routes.md#opening) |
| Routes | Independent coordinates and mode/time-applicable route evidence against original reserved duration; unsupported provider scope remains unresolved | [Opening/routes](docs/contracts/0004-opening-routes.md#route-wire) |
| Quality and density | Five automatic dimensions with separate evidence availability; source-linked pace deductions adjust the final total without adding hard generation quotas | [Quality/density](docs/contracts/0005-quality-human-review.md) |
| Additional evaluation tracks | Blinded review, V3 paired reports, controlled Repair and mechanism/official-claim audit interfaces are implemented; their execution and research populations require their own scope | [Evaluation design](docs/0006-independent-evaluation.md), [artifacts](docs/contracts/0001-evaluation-artifacts.md) |

Current identity policies are `versioned_api_identity_4` and
`v0_identity_correspondence_3`; requirement/schedule rules are version 3. Opening retains
API-only rules 2 and selects rules 4 with validated policy-2 access judgments. Verified physical
associations can support occurrence matching,
opening and route checks while original grounding FAILs remain visible. Requirement
targets belong to their own version. Historical reports retain their original policies,
code and source bindings; a rule change produces a separate recalculation.

The latest Sydney engineering case has four original outputs, reviewed requirements,
fresh independent evidence and a completed native evaluator flow. V2/V3 generation
includes captured embedding/SQL retrieval; V3 exercised Repair. Zero-network replay
preserves all originals and the original execution receipt. The authorized incremental
missing-hours model assessment under current rules 4 has completed with a separately
authorized policy-2 response. Exact network-free replay reproduces the retained #91
report below, whose identity policy remains version 3. The separate version-4 address
recalculation is not a replacement full quality report:

| Version | Overall score | Opening UNKNOWN | Grounding FAIL |
| --- | ---: | ---: | ---: |
| V0 | 92.1429 | 1 | 0 |
| V1 | 76.0000 | 0 | 2 |
| V2 | 85.0000 | 0 | 0 |
| V3 | 90.0000 | 0 | 0 |

The hard Opera House exact-once obligation is PASS for all four outputs. Fourteen
opening checks lack both current and regular hours; successful HTTP acquisition does
not supply those missing facts. The retained #91 report's two V1 literal-address FAILs
reflect API abbreviations; the current equivalence policy accepts both from retained
Google component pairs in a separate offline identity recalculation.
All fourteen missing-hours occurrences were assessed: thirteen PASS with explicit
`llm_access_reasonableness` basis and one remains UNKNOWN: V0 Powerhouse indoor admission.
Ordinary Harbour Bridge/Opera House viewing passes under the same rule for all versions.
Factual hours coverage and API duration quantities remain unchanged.
Six density FAILs are auxiliary soft pace penalties. Powerhouse's undated temporary
closure is retained without proving access on the planned date. This one engineering
case establishes runnable integration, not a formal ranking or version freeze.
The implemented public-landmark default permits ordinary viewing inferred from original
text and venue category, without interpreting a generic visit as a paid activity. Museum
admission and explicit restricted activities retain their access-evidence requirements.
The complete source-bound report and exact replay are accepted as engineering flow evidence;
residual judgments remain visible for human review.

Evidence: [generation and host resumption](docs/records/v0-v3/development-pilots.md#sydney-generation-host-resumption-2026-10-08),
[fresh evaluator acceptance](docs/records/evaluation/intake-identity-usage.md#sydney-four-final-fresh-acceptance-2026-10-09),
[requirement correction](docs/records/evaluation/intake-identity-usage.md#requirement-physical-association-correction-2026-10-09),
and [opening fallback acceptance](docs/records/evaluation/opening.md#regular-opening-fallback-acceptance-2026-10-09).
Commands and input preparation: [evaluation package guide](backend/evaluation/README.md).
Missing-hours implementation and live acceptance:
[access acceptance](docs/records/evaluation/opening.md#missing-hours-access-acceptance-2026-10-09).
Public-landmark revision:
[policy acceptance](docs/records/evaluation/opening.md#public-landmark-default-acceptance-2026-10-09).

## 5. Configuration, evidence and limitations

`config/runtime.yaml` and typed runtime configuration own active limits;
[config reference](config/README.md) explains them. Entry-point deadlines and stage
budgets are distinct. Dated execution allowances do not become runtime defaults.
[Development guide](docs/guides/development.md) owns runnable commands.

Full backend checkpoint: **3224 passed, 10 skipped** on 2026-10-09 after the opening
request serialization correction. The **57-test** affected gate and independent
Standards/Spec implementation reviews pass. Native opening execution/replay and
manifest-based quality CLI composition agree offline without weakening evidence binding.
Historical packets retain their original implementation for exact replay.
Acceptance details: [source facts](docs/records/v0-v3/v3-development.md#google-backed-output-facts-2026-10-09)
and [serialization and fresh execution](docs/records/v0-v3/v3-development.md#source-protected-v3-cli-execution-2026-10-09).
The latest recorded frontend gate is **98 passed**, with TypeScript, build and lint
passing; this backend task does not rerun or imply new frontend validation.
Actual failure/correction/retest sequences belong in the linked acceptance records.

Remaining limitations:

- Missing opening/access facts, unsupported route-provider scopes and unresolved
  identity/time/role evidence remain visible. A complete process can contain UNKNOWN.
- V0 semantic correspondence is fallible. V1-V3 retain literal names and binary
  address equivalence; unexplained address differences fail. Google-supported aliases
  do not waive identity/provenance requirements.
- Undated business status does not establish future closure dates. Optional public/exterior
  access assessment is model reasoning, not certified hours. Official web acquisition is
  not implemented; ambiguous or indoor access can remain UNKNOWN after model assessment.
- The retained KR V0 route package has unresolved provider/departure support. Proposed
  alternate providers need an approved adapter/evidence scope; Sydney acceptance does
  not resolve those historical legs. See [route support](docs/records/evaluation/routes.md#kr-route-support-budget-2026-10-07).
- Provider invoices and some billed quantities are unavailable; explicit retail/proxy
  estimates are not actual bills. RAG coverage and retrieval performance remain bounded
  by corpus/runtime evidence, not a general availability guarantee.
- Opening request serialization is corrected for newly prepared material. Latest fresh
  live evaluator acceptance remains blocked: the V0 identity response contains one of
  eight required decisions. Import correctly rejects incomplete coverage; no current
  final scores or FAIL/UNKNOWN inventory exist for the latest V3.
- Blinded, controlled-Repair and official-audit interfaces exist, but the latest Sydney
  automatic run did not execute those separate tracks or a formal benchmark.

Detailed engineering history is indexed in [records](docs/records/README.md), including
[evaluator records](docs/records/evaluation/intake-identity-usage.md),
[V3 development](docs/records/v0-v3/v3-development.md) and
[shared transport validation](docs/records/v0-v3/transport-responsibility-smoke.md).
Ignored logs, artifacts and thesis notes are local evidence, not project authorities
or guaranteed fresh-clone assets.

## 6. Next work and authorization boundary

The completed [public-landmark access scope #91](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/91)
revises inference while preserving original outputs, prior reports and API factual coverage.
Its separately authorized one-use package is consumed. The automatic four-output flow
produces a source-bound final report, saved accounting and exact network-free replay.
Processing and binding acceptance do not require every itinerary check to PASS.

Current local implementation and offline acceptance cover
[address equivalence #92](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/92)
and [V3 soft pace optimization #93](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/93),
plus shared [planner source protection #94](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/94).
The latest source-protected V3 has eight visits with exact captured Google names/addresses
and zero draft/final pace deduction; Repair did not run because the draft already met
the objective. Generation evidence capture is complete. The previous live Repair
reduction and older final scores remain historical evidence, not this output's evaluation.

Next work is to bind complete V0 identity-decision coverage into the model request,
then prepare another bounded evaluator package. Current importer rejection, both stopped
receipts, original V0-V2 and the new V3 remain immutable. No opening assessment was
executed for this latest batch. Details belong in
[the execution record](docs/records/v0-v3/v3-development.md#source-protected-v3-cli-execution-2026-10-09).
The historical Powerhouse admission UNKNOWN still needs applicable access evidence or
human disposition. Further official acquisition, business-status policy, V0 baseline
changes and formal research are separate follow-ups. Current bounded execution allowances
do not authorize automatic retries, a version freeze or remote Git delivery.
GitHub Issues own specifications and live task state; earlier approvals and deliveries
remain in their dated records rather than a chronological status diary here.

## 7. Keeping this file current

Maintain current capability, version boundaries, latest validation, unresolved limits
and authorized next work in place. Keep one current validation checkpoint, with explicit
scope and date. Put request counts, cost inventories, commit diaries, approval sequences
and failure/correction/retest details in their existing dated record owners, then link
them from the relevant current topic. Do not append each completed task to this file.
Historical records and previous PROJECT revisions do not override current scope or
renew execution authority. Use [docs/README.md](docs/README.md) for detailed navigation.
