# Capstone Project Context

Current source of truth. Updated 2026-10-05.
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
| 02: Usage capture/report | Implemented and offline-validated; opt-in capture plus [offline cost/bill accounting](docs/contracts/0002-intake-identity-usage.md#offline-cost-accounting); no automatic formal run or bill fetching |
| 03: Identity/adjudication | Implemented and offline-validated; independent supplied-ID/name-search paths, manual review and automatic-result audit; structural claims and optional typed-address evidence supported |
| 04: Evidence snapshots | Implemented and offline-validated through injected transport; linked identity snapshots also supply route coordinates offline; not a built-in operational Google client |
| 05: Requirement/schedule metrics | Implemented, offline-validated and published; [#17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17) closed as completed |
| 06: Opening checks | Offline parser/scorer/CLI implemented and reviewed; [#18](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18) completed; [acceptance and scoped supplements](docs/records/evaluation/opening.md#rtpeval-ticket-06-acceptance) |
| 07: Route checks | Offline preparation/scorer/CLI implemented and reviewed, including decisive partial FAIL, zero-grace hard boundaries and the [snapshot-coordinate bridge](docs/records/evaluation/routes.md#snapshot-coordinate-bridge-2026-10-03); [#19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19) completed; [original acceptance](docs/records/evaluation/routes.md#rtpeval-ticket-07-acceptance) |
| 08: Multimetric report | Offline report/CLI implemented and reviewed; exact shared-mask scores with separate availability/provenance; [#20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20) completed; [acceptance](docs/records/evaluation/quality-report.md#rtpeval-ticket-08-acceptance) |
| 09: Blinded ranking | Offline package/import/report and React renderer completed; IANA time-zone selection, HH:mm and confirmed answer clearing; user-reported browser acceptance complete; [#21](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21) completed; [acceptance](docs/records/evaluation/blinded-ranking-record.md#rtpeval-ticket-09-acceptance) |
| 10: V3 before/after | Offline preparation/report/CLI implemented, reviewed and published; adopted source lineage precedes unique fallback and residual review; separate paired mask, exact deltas and independent continuity; [contract](docs/contracts/0005-quality-human-review.md#v3-pairs) and [acceptance](docs/records/evaluation/v3-pair-report.md); [#22](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22) completed |
| 11: Controlled Repair | Offline real V3 replay, strict frozen ports/time/cache, independent targets/controls, human supplementation and CLI implemented, reviewed and published; [contract](docs/contracts/0001-evaluation-artifacts.md#controlled-repair) and [acceptance](docs/records/evaluation/2026-10-04-controlled-repair.md); [#23](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23) completed; formal case construction/execution remains separately authorized |
| 12: Mechanism/evidence audit | Selected-source mechanism report, exact official-claim audit queue/reviews, researcher CLI and default-off local submission/selection capture implemented, reviewed and published; [contract](docs/contracts/0001-evaluation-artifacts.md#mechanism-official-audit) and [offline acceptance](docs/records/evaluation/2026-10-04-mechanism-official-audit.md); [#24](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24) completed; formal audit/execution remains separately authorized |

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

Latest recorded full backend gate: **2705 passed, 10 skipped in 421.67s**, from the
2026-10-05 [short-reference delivery validation](docs/records/v0-v3/semantic-reference-correction.md#short-reference-live-regression-execution-2026-10-05),
tracked under [#66](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/66).
Earlier review corrections passed **89** executor/Repair and **42** native-policy
tests; Standards and Spec rechecks have no remaining findings.
Primary generation, Repair, review profiling, official reasoning and Product decoration
now restore supplied identities from short model references. The subsequent authorized
six-case live adapter smoke passed in **18.016 seconds**, with six model sends and no
retries, tools or Google calls. Reported usage was **12,832 input / 1,604 output**;
the Standard retail estimate is **USD 0.0020852**, excluding unpriced cache-write or
regional adjustments; actual billing is unavailable. The V0 evaluator test produced
nine bounded proposals, with zero native adoptions. This is selected-boundary evidence,
not full planner orchestration or an identity-accuracy result. Four V0 routes remain UNKNOWN.
The preceding Issue #59 gate was **2655 passed, 10 skipped in 323.62s**, before review
corrections; subsequent focused gates were **80**, **288, 1 skipped**, and **95**.
The [offline cost acceptance](docs/records/evaluation/intake-identity-usage.md#offline-cost-acceptance-2026-10-05)
retains failures, corrections, retests and dual-axis review evidence.
Earlier Issue #57, Issue #53 and Ticket 11/12 results remain historical in their records.
The skips are environment/opt-in cases. No live services or formal corpus were used
in the offline test gates;
earlier approved supplements remain distinct evidence.
The separately approved [V0 structured transport smoke](docs/records/evaluation/intake-identity-usage.md#v0-structured-transport-live-2026-10-05)
completed on 2026-10-05: one V0 run, two Foundry invocations, 30.516 seconds,
four structured transport declarations and 4/4 native bindings with no unbound claims
or projection diagnostics. Each day has two declared primary POIs. Original Seoul
evidence remains unchanged. This verifies the new representation in one live sample;
no independent route feasibility, four-version score comparison or freeze is claimed.
The subsequent [bounded V0 route diagnostic](docs/records/evaluation/routes.md#new-v0-route-execution-2026-10-05)
under [#61](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/61) sent nine
successful Places searches in 3.328 seconds, with no Details, Routes, LLM calls or retries.
All four route verdicts remain UNKNOWN: identity handling stopped on high-impact human
review and restrictive address-component parsing. The observed retail estimate is
USD 0.315; actual billing is unavailable. Offline replay was identical and original
V0/older Seoul evidence remained unchanged. Route feasibility is still unverified.
The subsequent [V0-only identity pilot](docs/records/evaluation/routes.md#v0-identity-assistance-pilot-2026-10-05)
under [#63](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/63) made one
`gpt-6-luna` request and produced nine bounded matching proposals, including two name
variants, consistent with owner-agent checking of the existing candidate fields.
Reported usage was 4,213 input / 1,007 output tokens; retail estimate USD 0.0009248,
actual billing unavailable. Native adoption remains zero and four routes remain UNKNOWN.
No production integration, genuine human accuracy estimate or V1-V3 change is claimed.
The later reference audit prepared a separate short-ID packet for those same nine
references and twelve candidates. Programmatic re-encoding/restoration was identical;
all 61 old authorized file hashes remained unchanged. This did not rerun the model,
establish a new accuracy result or change the four UNKNOWN route verdicts.
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

Separately authorized 2026-10-04 Seoul four-day pilot completed the real V0-V3 →
saved originals/usage/mechanism → independent Google evidence → Evaluator → reports
chain with agent reviews. All four live invocations completed; 82 independent sends
returned HTTP 200 without retries. The final replay audit passed 29 requirements.
V1-V3 auxiliary totals were 100 in their implemented metric populations; V0's total
remained unavailable due to unresolved transport association and one identity.
V3 adopted one added visit (7 → 8); independent paired quality stayed 100 → 100.
This is one engineering smoke, not a version ranking or human participant study.
No frozen controlled case was replayed and the official-claim audit population was
empty. Production/runtime behavior was unchanged. The
[dated pilot record](docs/records/evaluation/2026-10-04-seoul-live-pilot.md) owns the
actual inputs, agent-review boundaries, failure/correction/retest sequence and
known association limitations; raw artifacts stay ignored and local.

The user-authorized 2026-10-04 evaluator density change now adds source-linked
ordinary/relaxed/rich daily deductions to final and V3 paired reports. The original
five-dimensional `auxiliary_total` remains diagnostic; `overall_total` subtracts the
mean requested-date deduction, clamped at zero. Matching explicit daily counts override
defaults. Nonempty user preferences require independent density review; unresolved
policy/counts keep the adjusted total unavailable. Report schemas are version 2;
planner V0-V3 behavior is unchanged. The final table in
[Issue #52](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/52) uses
`rtpeval_daily_density_2`: ordinary three-visit days deduct 10; relaxed
three/four/five-visit days deduct 40/70/90; rich pace has the smallest four/five-visit
deductions. An offline replay of the preserved Seoul evidence
produced V1 85, V2 90, V3 100 and V3 draft/final 95 → 100; V0 remains unavailable.
This is development acceptance of the revised rules, not a new live run or formal
version comparison. The [density contract](docs/contracts/0005-quality-human-review.md#daily-density)
and [acceptance record](docs/records/evaluation/2026-10-04-daily-density.md) own the rules,
validation and limitations.

The 2026-10-04 evaluator correction under
[Issue #53](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/53) removes title
vetoes of structured role/identity claims, excludes declared free time from POI counts,
and prevents unrelated notes from changing V0 mode/transport association. Genuine
unknown roles, date attribution, endpoint conflicts and identity review/audit remain.
That correction introduced projection policy `structural_claims_directed_occurrences_4`
and identity association `structural_claims_typed_addresses_3`. The density table and
V0-V3 planners were unchanged by that correction.
See the [intake contract](docs/contracts/0002-intake-identity-usage.md#claims) and
[correction acceptance](docs/records/evaluation/intake-identity-usage.md#free-text-scoring-corrections-2026-10-04).

The separately authorized density delivery through `300ee039` was merged in
[PR #54](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/54), with both review
axes clear and Issue #52 verified closed. The separately authorized Issue #53 release
was merged on 2026-10-05 in [PR #55](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/55)
through `96e4f6d`, including the earlier `main_poi` correction. Both review axes had
zero remaining findings; Issue #53's nine acceptance criteria were verified checked
and its state CLOSED. No new code testing was needed for the final documentation-only
review correction; its 2576-pass/10-skip gate remained valid at that publication checkpoint.

The subsequent authorized 2026-10-05 Seoul offline replay used these delivered policies
and preserved original observations and agent decisions. Updated identity, route plans,
snapshot bindings and V3 edit provenance passed the native evaluator entry points twice
with identical output bytes. Network/DNS calls were blocked, with zero attempts; all
313 source files and 5 density-baseline files retained their hashes. Scores remained
V0 unavailable, V1 85, V2 90, V3 100 and V3 draft/final 95 to 100. Visit counts,
deductions, substantive primary metrics, schedule measures and occupancy were unchanged.
V0 still has four unresolved candidate commitments/modes and one unresolved identity;
its non-overlap denominator makes the total unavailable. Changed policy/hash/observation
references describe replay linkage, not new observations or new adjudications. This
single-case regression does not establish live failure frequency or a formal ranking.
See the [publication and replay acceptance](docs/records/evaluation/intake-identity-usage.md#prose-publication-and-seoul-replay-2026-10-05).

The 2026-10-05 implementation under
[Issue #57](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/57) adds V0
`Activity.transport` declarations: mode and directed activity IDs. V0's provider
schema/mapping/prompt emits them; the evaluator reads them before prose, with
independent per-field review precedence. Projection policy is now
`structural_claims_directed_occurrences_5`. Missing/null objects retain legacy input
compatibility, while invalid IDs and null/unsupported modes remain unresolved.
V1-V3 provider schemas and transfer authority, identity rules and density penalties
remain unchanged. Validation is offline; preserved Seoul results are not retrofitted,
and this task supplies no new live result or score comparison. See the
[structured transport acceptance](docs/records/evaluation/intake-identity-usage.md#v0-structured-transport-2026-10-05).

## 6. Next work and authorization boundary

On 2026-10-05 the user approved creating and preparing two follow-ups:
[short-reference live regression #66](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/66)
and [V0-only proposal adoption/route handoff #67](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/67).
The user subsequently authorized #66 implementation and its live budget. Its executor,
offline SDK preflight, dual-axis review and six-case live smoke are complete. The user
also authorized publication and #66 closeout through
[PR #68](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/68); GitHub owns final
merge and Issue lifecycle state. No short-reference
restoration failure occurred in these six samples. See the dated
[execution acceptance](docs/records/v0-v3/semantic-reference-correction.md#short-reference-live-regression-execution-2026-10-05).
The user subsequently approved finalizing #67 and publishing its two implementation
slices: [offline V0 identity adoption #69](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/69),
then [independent route request preparation #70](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/70),
which is blocked by #69. The specification retains default-off V0 model-assisted
association, source/replay validation and genuine high-impact/audit review. It
distinguishes raw address wire validity from native semantic-comparison diagnostics.
Implementation and subsequent independent acquisition still require separate approval;
both tickets remain open, and neither authorizes live calls. Earlier offline source/hash
and proposal restoration checks add no adopted identity or route evidence. The new
V0's four routes remain UNKNOWN. See the dated
[regression preparation](docs/records/v0-v3/semantic-reference-correction.md#short-reference-live-regression-preparation-2026-10-05)
and [specification finalization](docs/records/evaluation/routes.md#v0-adoption-specification-finalization-2026-10-05).

Tickets 01-12 have completed their approved implementation, offline validation,
review and engineering delivery scopes. On 2026-10-04, the user separately authorized
a normal push of feature/evaluation and verified acceptance updates/closure of
Tickets 10-12, followed by parent #12. The 56 prepared commits were published through
`bab0d5315f9a6dcaecb8327c1017bfe94269f2c1`; exact remote head and seven linked
contract/acceptance/navigation blobs were verified. Tickets 01-12 (#13-#24) and
parent #12 were then verified closed/completed. Documentation migration #36 remains
separately completed. See the [published parent acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12#issuecomment-5973135724)
and [delivery record](docs/records/evaluation/2026-10-04-mechanism-official-audit.md#engineering-publication-and-tracker-closeout--2026-10-04).
GitHub owns live lifecycle state; these observations describe this delivery checkpoint.

The user separately approved offline CLI usage acceptance under
[#49](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/49). The five synthetic
workflows and two material-error examples passed through actual module processes;
the new regression gate passed 9 tests and the full backend gate passed 2490 with 10
skipped. This task adds tests and usage documentation, with no production behavior change
or live/formal execution. See the [usage guide](backend/evaluation/README.md#start-with-the-synthetic-usage-packet)
and [dated record](docs/records/evaluation/2026-10-04-evaluation-usage.md). At that
acceptance checkpoint, its new commits and documentation were local pending publication.

The 2026-10-03 documentation migration consolidates durable scratch specifications
into core docs and dated records, preserves local spec/child-ticket working files,
and maps completed legacy work to GitHub Issues. `.scratch/` is local and ignored;
published documents depend only on tracked repository assets or accessible remote
URLs. GitHub owns task state; local ticket copies are planning aids, not a second
live tracker. See [tracker conventions](docs/agents/issue-tracker.md) and the
[core design/proposal index](docs/README.md).

That earlier delivery published the existing engineering work and synchronized acceptance;
it created no PR or merge and did not switch branches. No additional test/live run,
budget increase, formal corpus/comparison/analysis or version freeze occurred. The
final documentation closeout records these observed outcomes in a separate commit.

No further development or research task is authorized by completion. Read PROJECT.md,
the relevant current contract and live Issues before proposing a separately scoped
next task. Future push, PR creation, merge, branch switching and Issue mutations retain
the repository's explicit authorization rules.

Per-ticket approvals and task discussion remain in the relevant GitHub Issues.

## 7. Keeping this file current

This file owns current scope, version boundaries, status, limitations and next work.
Update the relevant section in place when the state changes. Keep only the latest
clearly dated validation summary here; place full failure/correction/retest sequences,
per-run budgets, identifiers and commit diaries in their linked development or
acceptance records. Use [docs/README.md](docs/README.md) to locate those records.

Historical statements labelled Current/Next remain historical when preserved in a
record. They must not override this current summary or authorize another execution.
