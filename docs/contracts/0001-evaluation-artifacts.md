# Evaluation artifacts, scope and time

Current shared contract, reconciled with the implemented Tickets 01-11 on 2026-10-04.
[PROJECT.md](../../PROJECT.md) owns scope; [evaluation architecture](../0006-independent-evaluation.md)
owns implemented/deferred boundaries. GitHub owns task state. This reference states current
rules together; dated proposals, approvals and validation remain in linked history.

<a id="rtpeval-spec"></a>
<a id="scope"></a>

## Batch ownership and reader separation

The final-quality workflow consumes an explicitly selected, producer-attested batch of
four-version groups.
It does not select cases, rerun planners, recompute workflow completion or improve the source
itineraries. The isolated Ticket 11 controlled V3 replay has the execution boundary
below; it does not require invented V0-V2 outputs. A qualifying group means workflow completion
was established upstream, not that
its itinerary is factually correct. Failed construction attempts stay upstream.

Quality readers use original Input, reviewed RequirementSpec, projected itinerary claims,
independent identity/evidence and versioned rules. Planner requirements, candidate ledgers,
RAG origins, internal validation, Repair findings and cache contents do not decide independent
quality. Mechanism readers have a separate channel. Human reviewers see anonymous original
request/itinerary material; RequirementSpec, automatic scores and private mappings are hidden.

The request/group is the comparison unit; visits, obligations and legs are nested observations.
Formal selection, sampling, cross-request inference and research conclusions remain separately
authorized work. Shared normalized DTOs do not make planner decisions independent evidence.

<a id="rtpeval-artifact-contract"></a>
<a id="rtpeval-artifact-contract--batch-layout-and-integrity"></a>
<a id="rtpeval-artifact-contract--requirementspec-wire-shape"></a>
<a id="rtpeval-artifact-contract--selected-run-provenance-wire---2026-09-30"></a>
<a id="rtpeval-spec--ownership-and-batch-lifecycle"></a>
<a id="rtpeval-spec--requirementspec-field-proposal--2026-09-28"></a>
<a id="batch-layout-and-integrity"></a>
<a id="requirementspec-wire-shape"></a>
<a id="selected-run-provenance-wire---2026-09-30"></a>
<a id="ownership-and-batch-lifecycle"></a>
<a id="requirementspec-field-proposal--2026-09-28"></a>

<a id="integrity"></a>

## Material integrity and source identity

`rtpeval_batch_1` contains `batch_id`, `revision`, `created_at`, `qualification_policy_ref`,
ordered `selected_group_ids` and `groups`. Each group has `group_id`,
`completion_attested=true`, `input_ref`, `requirement_spec_ref` and `selected_runs` with exactly
four entries keyed by v0-v3. Every run has a globally unique `run_id`, `result_ref`, `usage_ref` and required
`provenance_ref`. Optional files are explicitly referenced, never guessed from filenames.

Artifact references carry a relative path, exact-byte SHA-256, media type and availability;
schema version is declared where the envelope defines it. A result identifies its own
system version and itinerary output version, rather than an invented result schema name.
Paths resolve within the batch root, including link/junction resolution. Duplicate JSON keys,
escaping paths, duplicate IDs, missing required material and wrong linkage require whole-batch
correction; no convenient smaller cohort is silently scored.

The complete original input hash includes preference text; `structured_hash` is insufficient.
Each `rtpeval_provenance_1` sidecar binds `group_id`, `run_id`, `version`, `input_sha256` and
`result_sha256`. These must match the selected group and exact saved bytes. Configuration and
source revision metadata retain missing values; filenames do not supply provenance.

Sources are identified by batch/group/run, artifact-byte hash and JSON pointer. Derived IDs
also bind the projection contract. Original array positions, raw values and timestamps stay
intact; sorted views do not rewrite pointers. Activity IDs are itinerary-scoped, not global
identities or proof of cross-Repair correspondence. Source changes require relinking/replay.

Original result bytes are immutable. Canonical object digests, exact-file hashes and generated
report hashes have distinct domains. Hashes establish supplied-material linkage/integrity,
not cryptographic authorship, provider authenticity or factual correctness. Preserve trusted
plan/manifest hashes when operational provenance requires them. Secrets are excluded.

Intake recognizes `planning_request_2`, `itinerary_1` and `itinerary_2`, recording historical
absence of an output version. Fatal structure failures prevent stable inventory; representable
quality issues stay diagnostic. Current live-request date limits do not reject historical
submitted inputs. Missing optional V3 draft/final-primary projections disable dependent paired
work only; they are not reconstructed. Usage may explicitly be unavailable, rather than zero.
Exact parsing/projection wire is owned by [intake](0002-intake-identity-usage.md#rtpeval-intake-projection-contract).

<a id="rtpeval-activity-scope-contract"></a>
<a id="rtpeval-activity-scope-contract--activity-scope-and-route-adjacency--draft"></a>
<a id="rtpeval-activity-scope-contract--purpose-and-ownership"></a>
<a id="rtpeval-activity-scope-contract--one-poi-delivery-constraint"></a>
<a id="rtpeval-activity-scope-contract--shared-inventory-and-confirmed-scope"></a>
<a id="rtpeval-activity-scope-contract--adjacency-and-occupancy"></a>
<a id="rtpeval-activity-scope-contract--scope-decisions-and-code-confirmation"></a>
<a id="rtpeval-activity-scope-contract--simple-examples"></a>
<a id="rtpeval-activity-scope-contract--remaining-technical-contracts"></a>
<a id="rtpeval-activity-scope-contract--future-checks"></a>
<a id="rtpeval-activity-scope-contract--day-boundary-source-references"></a>
<a id="rtpeval-activity-scope-contract--generic-no-poi-activities-superseding-user-decision"></a>
<a id="rtpeval-activity-scope-contract--ticket-01-specialization--2026-09-29"></a>
<a id="rtpeval-activity-scope-contract--superseding-transport-source-decision---2026-09-30"></a>
<a id="rtpeval-activity-scope-contract--transport-responsibility-correction---2026-09-30"></a>
<a id="rtpeval-activity-scope-contract--ticket-05-occupancy-specialization--2026-10-01"></a>
<a id="rtpeval-spec--activity-scope-and-adjacency-draft--2026-09-28"></a>
<a id="rtpeval-spec--superseding-generic-activity-decision--2026-09-28"></a>
<a id="activity-scope-and-route-adjacency--draft"></a>
<a id="one-poi-delivery-constraint"></a>
<a id="adjacency-and-occupancy"></a>
<a id="day-boundary-source-references"></a>
<a id="generic-no-poi-activities-superseding-user-decision"></a>
<a id="superseding-transport-source-decision---2026-09-30"></a>
<a id="transport-responsibility-correction---2026-09-30"></a>
<a id="ticket-05-occupancy-specialization--2026-10-01"></a>
<a id="activity-scope-and-adjacency-draft--2026-09-28"></a>
<a id="superseding-generic-activity-decision--2026-09-28"></a>

<a id="activity"></a>

## Activity, transport and occupancy scope

Each primary visit is one concrete place occurrence with its own interval. A confirmed
multi-POI block sharing an interval is a delivery diagnostic; do not split places or invent
times. Structural `main_poi`/`place_name` claims take precedence over ordinary descriptive
title wording, with bounded explicit competing-claim review. Unresolved named visits remain
visits with identity uncertainty. Generic locationless placeholders supply no invented venue.

Nearby is unscheduled and excluded from primary counts, required/excluded checks, opening
and main-route adjacency. Count visit occurrences separately from unique canonical identities.
An unresolved role remains visible as applicability uncertainty, not a deleted denominator.

Submitted transport authority is **V0 Activity; V1-V3 Transfer**, including optional V3 stages.
Ignored representations retain diagnostics/source records but provide no occupancy, mode,
time or fallback. Missing transfers stay missing. Same-source duplicates share one logical
journey; segments retain their intervals; conflicting claims stay alternatives. Independent
association does not certify identity, chronology or real route feasibility.

Route candidates join consecutive primary occurrences within each delivered day. Inter-day
travel is outside the product/evaluator scope. Independently confirmed same-canonical endpoints
are route N/A, not a measured zero-duration PASS. Different venues sharing an address are distinct.
Unknown intermediate roles retain uncertain adjacency. Sorting does not repair overlaps.

An explicitly uncommitted, locationless free-time slot can be travel slack. Fixed rest,
reservations and reviewed protected time cannot be consumed; unclear flexibility requires
independent review. Planner lineage cannot authorize that classification. Scoped protections
retain their original obligations and block applicable commitments without adding non-overlap
units. Detailed occupancy/counting is owned by
[requirements and schedule](0003-requirement-schedule.md#rtpeval-requirement-schedule-contract).

<a id="rtpeval-evidence-time-contract"></a>
<a id="rtpeval-evidence-time-contract--evidence-and-time-parsing-contract"></a>
<a id="rtpeval-evidence-time-contract--verified-provider-facts"></a>
<a id="rtpeval-evidence-time-contract--time-interpretation"></a>
<a id="rtpeval-evidence-time-contract--opening-parsing-truth-table"></a>
<a id="rtpeval-evidence-time-contract--route-response-truth-table"></a>
<a id="rtpeval-evidence-time-contract--identity-and-role-handling"></a>
<a id="rtpeval-evidence-time-contract--implementation-checks-and-limits"></a>
<a id="rtpeval-evidence-time-contract--opening-technical-follow-up--2026-10-02"></a>
<a id="rtpeval-evidence-time-contract--ticket-06-implemented-timeevidence-checkpoint--2026-10-02"></a>
<a id="verified-provider-facts"></a>
<a id="time-interpretation"></a>
<a id="opening-parsing-truth-table"></a>
<a id="route-response-truth-table"></a>

<a id="time"></a>

## Independent time and provider observations

Preserve timestamp strings and explicit offsets. Aware values identify instants; destination-
local rules require independently supported IANA context. Naive clocks are localized only
when the local interpretation is unique. Missing/conflicting zones, DST folds/gaps and
declared-day/offset inconsistencies keep dependent checks UNKNOWN. Host/browser timezones and
planner metadata are not substitutes. Consistent declared days can still support structural
date counts when precise instants are unavailable.

Intervals are half-open: touching endpoints do not overlap, and visit end equal to opening
close is allowed. Preserve microsecond timestamp precision; greater precision is unsupported
rather than truncated. Full-day protections use local midnight to next local midnight,
including 23/25-hour days. Ticket 06 permits explicit cross-date visit endpoints; no next-day
end is inferred. Duration comparisons use instants, not a fixed civil-day length.

Frozen snapshots retain original raw provider bytes, request parameters and ordered attempt/
collection times. Provider failure, explicit no-route/closed observations, incomplete evidence
and malformed material are distinct. Raw response replay precedes derived interpretation;
planner-rounded DTO values do not replace original precision or field-presence semantics.

Opening uses current request-local windows, regular weekly patterns and known/unknown spans;
any proven closure inside a visit is decisive FAIL, complete open containment is PASS, otherwise
UNKNOWN. Original explicit empty periods differ from missing/null/derived-empty values.
Route evidence keeps status, condition, direction, mode, departure and raw nanosecond duration.
An applicable successful no-route is FAIL with null duration; accepted traffic fallback remains
usable without silently switching endpoints, mode or date. The complete truth tables,
applicability and independent tolerances live in
[opening/routes](0004-opening-routes.md), rather than a second rule copy here.

<a id="rtpeval-artifact-contract--evaluation-artifact-and-human-answer-contract"></a>
<a id="rtpeval-artifact-contract--reports-and-numeric-serialization"></a>
<a id="rtpeval-artifact-contract--human-presentation-and-answers"></a>
<a id="rtpeval-artifact-contract--ticket-08-proposed-quality-report-specialization--2026-10-02"></a>
<a id="rtpeval-spec--automatic-checks-and-human-judgment"></a>
<a id="rtpeval-spec--human-assessment-boundary"></a>
<a id="rtpeval-spec--detailed-accepted-metric-and-reporting-constraints"></a>
<a id="rtpeval-spec--quality-checks-and-scorecard"></a>
<a id="rtpeval-spec--score-profile-proposal--2026-09-28"></a>
<a id="evaluation-artifact-and-human-answer-contract"></a>
<a id="reports-and-numeric-serialization"></a>
<a id="human-presentation-and-answers"></a>
<a id="ticket-08-proposed-quality-report-specialization--2026-10-02"></a>
<a id="automatic-checks-and-human-judgment"></a>
<a id="human-assessment-boundary"></a>
<a id="detailed-accepted-metric-and-reporting-constraints"></a>
<a id="quality-checks-and-scorecard"></a>
<a id="score-profile-proposal--2026-09-28"></a>

<a id="reports"></a>

## Report and track boundaries

Reports retain source/rule/preparation/review hashes, units, applicable populations, raw states,
coverage, reasons and null unavailable values. Material correction, UNKNOWN, N/A and a numeric
zero are distinct. Deterministic replay uses frozen inputs/rules; generation time is metadata.
Ticket 08's content hash excludes generation time and itself; CLI file hashes remain separate
from object digests. [Quality/human review](0005-quality-human-review.md) owns exact score,
mask and answer/report wire. Resources have a separate observed ledger and no implicit cost score.

Implemented outputs include intake, identity/adjudication, usage, snapshots, requirements/
schedule, opening, routes, final multimetric reports and anonymous human packages/import/reports.
Not every optional track is integrated into the quality report. Its availability metadata does
not manufacture resource/human/mechanism aggregation. Paired snapshot support in preparation/
individual scorers alone is distinct from the implemented Ticket 10 paired report.

<a id="rtpeval-spec--repair-and-controlled-cases"></a>
<a id="rtpeval-spec--presentation-of-mechanism-comparisons"></a>
<a id="rtpeval-spec--out-of-scope"></a>
<a id="rtpeval-spec--further-notes"></a>

<a id="planned"></a>

## Accepted follow-up design and deferred coverage

Ticket 10 retains independently evaluated V3 draft/final-primary under one compatible snapshot,
validated adopted-edit/activity/split provenance before content fallback and residual review,
and a paired common dimension mask. Unresolved local correspondence does not suppress an otherwise
valid paired aggregate. The offline reader/report/CLI is implemented; current behavior
is in the [paired contract](0005-quality-human-review.md#v3-pairs), with actual validation
and review corrections in [acceptance](../records/evaluation/v3-pair-report.md).

Ticket 11's accepted controlled composition is 24 targets plus 8 controls, with confirmed
evidence/policy conflicts distinguished from optional review opportunities. Independent target
outcomes include detection failures, residuals, regressions and control invariants; disappearance
of a planner target ID is insufficient. Cases/evidence/capability configuration must be frozen
for separately authorized work. No controlled cases or rates are created by this document.

<a id="controlled-repair"></a>

### Ticket 11 controlled replay contract

**Status: offline implementation approved and implemented; validation/review recorded separately.** The control and
human-review decisions were accepted on 2026-10-03. This section closes the local technical
preflight for [Ticket 11](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23);
it does not change the live Issue state or authorize publication, formal case construction,
execution or analysis. The accepted 24-target/8-control composition remains unchanged.

#### Cases, targets and controls

Consume separately supplied V3 cases with original input, reviewed obligations, a pre-repair
primary itinerary, frozen execution capabilities and separately sourced evaluation material.
Case metadata declares the expected target conditions, their subjects and classification,
the intended improvement and the conditions to preserve. Actual findings and permissions
are measured outputs, not caller-supplied authorizations. Keep confirmed factual conflicts,
explicit requirement violations, declared product-policy violations and optional review
opportunities distinguishable. A sparse, repeated or overfull itinerary is not automatically
defective; apply the actual user obligations and frozen policy/review configuration.

A control checks whether an initially compliant itinerary becomes worse against its declared
constraints or acquires new independently established problems. It does **not** require
byte-identical output or an empty Repair scope. Legitimate review-policy changes may occur;
report detection, authorization, attempted edits and adopted changes separately from harm.
An added visit is acceptable only when the user's requirements remain satisfied and the
relevant added schedule, identity, opening and route conditions are independently supported.
An internally accepted patch is not independent proof of this outcome.

For example, adding Gallery C to a feasible Museum A/Garden B day is not automatically a
control regression. If the user explicitly requires exactly one primary visit on Tuesday,
adding a second Tuesday visit violates that reviewed obligation, even if opening and route
checks pass or the planner accepts the patch. Generic quantity recommendations do not waive
explicit counts, dates, exclusivity, required visits or protected time. Updated diagnostics
and transfer presentation are not themselves harmful itinerary changes.

Identify regression units through original obligation IDs, independently established visit
correspondence, directed route endpoints and the applicable conflict/protection subjects.
Reuse [paired continuity](0005-quality-human-review.md#v3-pairs): retained comparable
FAIL-to-PASS is resolution; deletions, replacements, removed connections and changed contexts
remain explicit rather than proving the old fact repaired. PASS-to-FAIL is a confirmed
regression; PASS-to-UNKNOWN is lost verification, not a confirmed regression or safe change.
Check newly introduced visits/connections and retain missingness. Product-policy or optional
review goals use their declared applicable conditions, not invented factual obligations.

Retain every expected target and control in the inventory. For each expected target, distinguish
detection, authorization, candidate opportunity, model attempt, adoption and independent
outcome. A detection miss stays in the expected-target denominator; later skips, unavailable
capability, rejected patches or missing independent verdicts do not silently remove the unit.
Report residual conditions, partial improvements, regressions, valid no-change and lawful
changes separately. Do not import Ticket 08's four-final total or manufacture a causal verdict.

#### Human supplementation and unresolved outcomes

Missing provider fields do not alone prevent a human from establishing an evaluation fact.
Review may clarify an obligation from the original request or supply separately verified
opening/route/identity evidence. Record the reviewer, review time, rationale, supporting
source references, exact case/source revision, affected subject, date/query applicability
and rule context. Use the existing identity, requirement, correspondence and scoped evidence
review mechanisms where they cover the subject; add only the missing controlled-case linkage.
A bare assertion of success or safety is not a substitute for the relevant fact or condition.

Preserve the original planner/provider material. Human supplements enter the independently
versioned evaluation channel; they do not retroactively grant the replay planner additional
evidence, supply, budget or permissions. Changed supplements produce a new linked preparation
revision. They cannot silently override contradictory established evidence.

After review, supported subjects receive their independent verdict. Remaining local uncertainty
stays unresolved/UNKNOWN, with affected units and coverage visible; it proves neither successful
repair nor confirmed harm. Preserve unaffected, valid observations. Corrupt sources, stale or
foreign reviews, missing required execution inputs and incomplete replay scripts are material/
execution errors, distinct from an unresolved real-world fact or an itinerary FAIL.

#### Frozen execution and the real V3 path

Reuse production post-primary initialization, `assess`, `operation_scope`, `run_repair_stage`
and finalization through `final_primary`. Recompute schedule, transitions, visit bindings,
targets, scope and round localization from frozen original inputs. Do not inject a target,
scope, prepared authorization or an adopted itinerary to bypass these measured stages.
Candidate preparation, model input construction, patch/component acceptance, re-validation
and final source/date/transfer handling remain the real production operations.

Freeze the runtime/review/transport configuration, candidate supply, geographic/intention
inputs, semantic assessments and active ledger, request time remaining, cache values/attempt
states and external response scripts. A case may explicitly declare an empty cache; historical
key hashes alone do not restore captured cache behavior. Supply typed local responses or
declared failures for Places, Routes, retrieval/embedding and model/semantic requests actually
needed by that case. Match calls against their declared input context. Supply deterministic
logical time and declared call durations without measuring real provider latency.

Unexpected or mismatched calls, absent script entries and any unintended live model/provider/
database access fail replay integrity. Frozen adapters retain an out-of-band error ledger,
because production Repair may catch ordinary provider/model exceptions. Declared provider
failures remain valid frozen responses; swallowed script errors cannot become ordinary skips,
detection misses or no-change outcomes. Replay usage is declared/simulated usage, not observed
live cost or a model-quality estimate.

The existing `tools/validation/repair_replay.py` is evidence-only scope/candidate preparation;
it does not replay model proposals or adoption. Reuse its capture concepts where applicable,
but preserve that diagnostic contract and do not claim old snapshots contain complete replay
capabilities. A small shared production initialization/finalization seam can avoid maintaining
a second Repair implementation. Default live clocks, policies and version entry paths must
retain their behavior.

#### Approved implementation and validation boundary

The approved implementation is an offline V3-only case reader/preparation, frozen
execution adapters, controlled outcome report and CLI under `backend/evaluation/`, with a
small behavior-preserving shared seam in `backend/app/versions/v3/wiring.py` if needed.
Reuse the existing independent identity, requirement/schedule, opening, route and paired
correspondence checks. Add explicit controlled goal/invariant linkage rather than a second
general quality scorer or fake four-version batch. No formal 32-case corpus is generated.

Use synthetic development fixtures after implementation approval to verify real detection
misses, valid no-change, legitimate additions, explicit one-visit violations, reviewed and
unresolved evidence, rejected/adopted component lineage, newly introduced problems, strict
script errors and deterministic time/cache conditions. Follow TDD, implementation commits,
fixed-base Standards/Spec review, separate correction commits and final documentation.
Run relevant evaluator/V3 regressions and the required full backend gate for the shared seam.
No live service, budget increase, Ticket 12 work or formal benchmark is included.

#### Controlled executable wire

`backend.evaluation.controlled_cli` owns the isolated command workflow. Ordinary
four-version intake still requires V0-V3. Controlled preparation contains only actual
V3 final/draft/final-primary sources; it never synthesizes V0-V2 results. The production
V3 post-primary and POI semantic services accept an optional clock; live defaults and
existing entry points preserve their behavior. Replay logical time starts at zero,
with `request_remaining` as the frozen deadline and declared durations added at calls.

The strict `rtpeval_controlled_case_1` envelope is defined by `ControlledCase` in
`backend/evaluation/controlled_models.py`. It embeds original input, primary itinerary,
interpreted requirements, runtime, transport, supply, place/route evidence, review switch,
reference date and request time remaining. Optional frozen funnel, geographic, RAG and
semantic state retain the execution capability. `calls` is required; explicitly empty
cache/attempt lists are valid. Cache entries preserve full keys, typed values and provider
wrapping. Semantic state preserves its fingerprint cache, active assessments, calls,
elapsed time and failed flag. Recomputed targets, scope and adopted outputs are forbidden
case inputs.

External scripts declare an operation, exact JSON request, response or nonempty declared
failure, and nonnegative duration. Repeated identical requests consume that request's
response queue in order; unused capability responses are permitted. Operations cover
Repair and semantic model calls, Places search/Details, Routes, embedding and retrieval.
Model matching excludes usage callback objects. Missing/mismatched calls and malformed
typed model/semantic/provider/retrieval responses remain out-of-band execution errors even if Repair
catches them. Declared model/provider outages are execution observations. A fatal production
exception without a completed V3 outcome is `execution_failed`; it cannot enter scoring.
Network connects are blocked inside replay. Use an exclusive event loop in a dedicated
offline process with no other network work, and execute cases serially. The guard patches
process-wide socket functions and the active loop clock; unrelated async tasks would observe
logical time too. This is a CLI/development executor, not a concurrent web-service runner.
The real asyncio timeout handles run against logical time before scripted replies are
delivered, so a response exceeding a configured call timeout is not silently adopted.
Tokenizer assets must already be local;
tests use the repository's offline structural tokenizer rather than live token measurements.

Replay emits `rtpeval_controlled_replay_1` with normalized case hash, actual V3 outcome,
request ledger, logical elapsed time, diagnostics and replay hash. Preparation verifies
that hash and original draft, then emits `rtpeval_controlled_preparation_1`. The embedded
original-input hash is the canonical JSON digest, not an original external file-byte hash;
reviewed requirements must bind to that digest and case ID. Executed source JSON is
serialized deterministically into genuine Ticket 10 result-source records.

`rtpeval_controlled_expectations_1` binds case ID/hash and a reviewed revision, reviewer,
offset-aware time, rationale and supporting references. Its `targets` and `guards` have
unique `goal_id`, `basis` and `condition`; targets additionally declare a `detector`.
Basis is `confirmed_conflict`, `explicit_requirement`, `product_policy` or
`review_opportunity`. Explicit requirements cite `{field, quote}` in the original input.
Check conditions select an independent dimension and exact original activity IDs or
obligation ID; optional canonical venue/date further restrict applicability. Dimensions
are requirements, grounding, opening, routes, conflicts and protection conflicts. Count
conditions use `daily_count` with date or `repeat_count` with canonical venue, with a
declared minimum/maximum. These are reviewer-supplied conditions, not title inference or
automatic sparse/repeated-day defects. Daily bounds include uncertain role/date occurrences;
repetition bounds include unresolved identities. Detector selectors use production check,
optional reason, activity/place/requirement IDs and dates. Confirmed goals match CONFIRMED
findings; review opportunities match NEEDS_REVIEW findings.

Per-goal output retains initial detection and authorization, round-linked candidate and
identity-free opportunities, model attempt and dependency-linked component adoption.
Independent outcomes reuse paired continuity and preserve structural changes, residual
FAIL, partial improvement, regression and unresolved evidence. Missing/corrupt execution
material retains expected goal inventory with unavailable outcomes and null measured counts.
An obligation-only protection condition reuses the independently scored `protected_time`
check for that original obligation. A cleared visit conflict alone does not establish that
all applicable commitments are clear; uncertain transport/candidate occupancy remains UNKNOWN.
An absent protected blocker cannot prove compliance.
Control baselines with confirmed violations are invalid control material. Unknown initial
compliance remains unresolved. Control regression checks guards and introduced/continued
independent failures; a lawful changed control need not have an empty scope. Raw paired
checks/scores remain separate from reviewed check outcomes.

Optional `rtpeval_controlled_facts_1` binds exact case and replay hashes with reviewed
revision/provenance. Opening facts select canonical venue, declared date and timezone,
with verified offset-aware `open_intervals`/`closed_intervals`. They fill only supported
coverage using the existing interval arithmetic and cannot contradict known intervals
or timezone. Route facts bind `expected_context_hash` from an independently prepared leg;
`availability` is `route_exists` or `no_route`, with optional integer duration nanoseconds
and distance meters. The existing route component rules evaluate those facts, retaining
missing components and rejecting contrary established observations. An unapplied, stale
or duplicate fact is material error. No human PASS assertion is accepted. Remaining
occupancy uncertainty uses the existing occupancy review channel; route facts alone do
not fabricate transfer occupancy. Raw paired metrics and deltas are preserved, while
`reviewed_checks` exposes supplemental checks/continuity without claiming recalculated
five-dimension scores.

The optional `rtpeval_controlled_batch_1` manifest inventories case ID, role,
`expected_goal_ids` and content-addressed report artifact references under one root.
Its report assembler verifies file/content hashes and exact case/goal inventory, keeps
unavailable cases and expected targets, and exposes descriptive counts. It imposes no
case-count cap and does not generate the formal 24-target/8-control corpus.

The dated [implementation and review record](../records/evaluation/2026-10-04-controlled-repair.md)
retains development validation, corrections and execution limitations.

Ticket 12 separates mechanism exposure/usage from independent quality and causality. Official
Evidence Audit includes only accepted facts exposed to a model or used by a rule, with separate
independent supported/contradicted/scope-mismatch/unavailable outcomes. Rejected/unused/search-
only material is outside that denominator. Exact extraction/reporting remains deferred.
See [Ticket 11](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23) and
[Ticket 12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24).

<a id="mechanism-official-audit"></a>

### Ticket 12 technical checkpoint — 2026-10-04

**Status: read-only technical preflight completed; the delivery below is Proposed.**
The user authorized technical preflight after Ticket 11. This is not implementation,
capture activation, live collection, formal audit execution, publication or Issue mutation.
Issue #24 remains open/needs-info; its missing optional artifacts must not invalidate
independent quality material. Checkpoint: `7c9783bdeb1b57b7fe6fdfc258dec47cc5c3dcf7`.

#### Existing interfaces and observed gaps

| Required observation | Current source | Technical conclusion |
| --- | --- | --- |
| Initial findings, improvement targets and authorized scope | `V3Outcome.original_report` and `scope` in [V3 state](../../backend/app/versions/v3/state.py) | Complete saved outcomes already support mechanism-only trigger/authorization observations. Internal findings do not establish independent truth. |
| Rounds, model attempts, components, target links, adoption and stopping | `RepairResult.rounds`, `RepairRoundRecord.target_links`, per-round result and continuation reason in [repair models](../../backend/app/versions/v3/repair_models.py) | Use the real records. The top-level result is a cumulative summary, not an additional round. |
| Accepted official claims and resolved representations | `OfficialWebIntegrationResult.accepted_evidence`, [official planner projection](../../backend/app/versions/v1/official_planner.py), `EffectiveFact.source_refs` | Typed claims and provenance exist in memory; the ordinary final result does not preserve a complete official-claim catalog. |
| Primary model evidence | `official_planner_evidence_prepared` and the primary generation code in [V1 graph](../../backend/app/versions/v1/graph.py) | Preparation precedes input-budget checks and model invocation. Prepared evidence alone does not prove input submission. Raw request capture is optional. V2/V3 share this primary graph. |
| Repair model evidence | `effective_evidence` and selected hours in [repair input](../../backend/app/versions/v3/repair_projection.py), followed by [repair invocation](../../backend/app/versions/v3/repair_service.py) | The actual projection exists, but ordinary mechanism traces chiefly retain sizing/fingerprints rather than a complete per-call official-fact submission record. |
| Rule-selected operating evidence | `Finding.adopted_evidence.selected_hours` and evidence refs from [opening assessment](../../backend/app/evidence/opening_hours.py) | Selected evidence can be traced where complete validation reports survive. All effective evidence in context, or conditions merely reported as unverified, are not automatically rule-used facts. |
| Trace and resource availability | [run tracer](../../backend/app/observability/run_trace.py), [usage capture](../../backend/app/observability/usage_capture.py) and [usage report](../../backend/evaluation/usage_report.py) | Tracing is best-effort and may be disabled/truncated. Numeric usage already has run/result linkage and missingness; no duplicate resource collector is needed. |

The observed gap is capture provenance, not missing itinerary/transport correspondence
or a need to rerun validation. The proposed reader consumes saved observations; it must
not replay a rule and label newly reconstructed evidence as historically used.

#### Proposed mechanism units and denominators

Inventory selected source runs by group/version/run ID and exact original input/result
hashes. V3 Repair is not applicable to V0-V2; absence of V3 metadata is unavailable, not
zero triggers or zero model attempts. Distinguish available, partial, unavailable and
not-applicable coverage per observation. Positive zero is allowed only with complete
observations establishing that no event occurred.

Report initial improvement targets, initial authorized targets, model attempts, accepted
rounds, accepted/proposed components, per-round target presence and internal progress
separately. Trigger means a nonempty authorized scope, not merely a NEEDS_REVIEW finding.
For each optional fraction, expose its numerator, denominator, unit and covered/missing
run counts. A run acceptance fraction uses triggered runs; a round acceptance fraction
uses model-attempted rounds; component acceptance uses components actually evaluated,
with pending/not-evaluated components reported separately. Do not merge these fractions.

Original authorized targets use original finding IDs; round-local target links map back
to them. Newly activated related/coverage targets remain a separate inventory. Per-target
internal progress does not become an independent resolution rate. Independently supplied
Ticket 10/11 reports may be linked with exact source hashes, but their outcomes remain
separate and are never inferred from an accepted patch or vanished target ID.

Round identity is run ID plus round index. Identical repeated observations are counted
once with their source references retained; contradictory records for the same identity
are material errors in that observation channel. Do not count both embedded round records
and trace copies, count the cumulative result as a final extra round, sum cumulative
counter snapshots, or add cumulative usage to its per-round children. Incomplete trace
fragments may support explicitly observed cells, never a fabricated complete denominator.

#### Proposed qualifying official-fact audit

Use a run-linked catalog of Evidence-Gate-accepted typed official claims, preserving
source refs, claim content/hash, source identity, excerpt, retrieval/date applicability
and subject scope. Link the resolved representation actually submitted or selected to
its accepted supporting claims. A URL or reference alone is not a verified fact.

The qualifying set is accepted claims with established model-input submission or actual
rule selection; keep those qualifying reasons distinct. Record preparation-only evidence,
failed-before-submission calls, rejected claims, search-only material and unused accepted
claims outside that denominator. An input-submission observation records the application
handing the exact projected facts to the model invocation; it does not prove provider
receipt, successful generation, the model's attention or causal influence. Incomplete
submission observations remain unavailable. Operational-day and conflict representations
retain their date/scope/uncertainty rather than being rewritten as affirmative truths.

Count a qualifying claim once per run and exact claim/source revision, preserving every
call/round/rule occurrence separately. Identical values from different source revisions
do not silently merge. One accepted claim exposed in two rounds and selected by one rule
has one audit unit and three occurrence links. This is neither a website count nor an
exposure-frequency-weighted truth score.

Export an audit queue with exact run/input/result/capture hashes, claim and occurrence
links. Independently supplied reviews bind that exact unit and revision, identify the
reviewer/time/rationale/supporting sources and classify supported, contradicted,
scope-mismatch or unavailable. Preserve both all qualifying units and reviewed/verifiable
coverage. Missing reviews do not remove claims or become supported/contradicted zeros.
The planner gate's acceptance and its reasoner's confidence are not independent audit
verdicts. This ticket does not introduce automatic random website checks, additional
retrieval or universal ticket-price/admission correctness scoring.

#### Proposed minimum capture and delivery scope

Reuse complete saved V3 outcomes and existing compatible trace/usage observations.
For future runs, add an opt-in, best-effort local normalized capture of the accepted
claim catalog, actual primary/Repair model-input submission links and rule-selected
evidence links. Capture the facts at their existing seams without changing prompts,
model schemas, gate rules, Repair permissions, provider requests or runtime budgets.
Observe failed/uncertain submissions and capture truncation/write failure explicitly;
recording failures must not change planning. Do not require raw prompts/provider bodies
or enabled usage collection. Preserve existing trace redaction and size controls.

Old runs use only surviving, source-linked observations: complete V3 outcomes can still
support mechanism cells while the official audit is partial/unavailable. Historical
accepted/exposed/used facts must not be reconstructed from the final itinerary or by
rerunning the current gate. Existing Ticket 11 frozen material may supply actual replay
observations only when linked to that replay; it cannot certify an older live execution.

Proposed implementation: separate immutable mechanism reader/report and official audit
queue/review/report, researcher CLI and the minimum opt-in capture above. Reuse artifact
hash/link validation and usage summarization. Keep four-final quality scores, identity,
paired metrics and anonymous review unchanged. No frontend or new acquisition system.
The extension adds local serialization/storage work; it adds no model input/output
tokens or provider/model calls by design. Offline regressions must verify identical
prompts/call counts with capture disabled/enabled and best-effort failure behavior;
real overhead is not measured by this preflight.

Existing offline interface checks passed 77 tests across official integration, multiround
Repair, tracing, budget summaries and usage reporting. The initial run had 63 passes and
14 setup errors because the task-local temporary parent directory had not been created;
after directory setup, the same test selection passed. No production/test source changed,
new Ticket 12 implementation fixture, live service or formal audit was executed.
The remaining scope decision is whether to include the proposed minimum capture rather
than deliver a saved-material reader alone with correspondingly unavailable audit cells.

Whole-trip factual budget PASS, verified access/fees and false-certainty metrics remain deferred.
Amounts can be descriptive; source role does not certify affordability. V0-V3 comparisons are
incremental system comparisons; no extra strict module-ablation study is introduced.

<a id="rtpeval-artifact-contract--usage-file-shape-and-ownership"></a>
<a id="rtpeval-artifact-contract--verification-seams"></a>
<a id="rtpeval-artifact-contract--projection-specialization--2026-09-29"></a>
<a id="rtpeval-artifact-contract--ticket-02-implementation-specialization--2026-09-29"></a>
<a id="rtpeval-artifact-contract--ticket-05-semantic-wire-specialization--2026-10-01"></a>
<a id="rtpeval-artifact-contract--ticket-08-executable-wire--2026-10-02"></a>
<a id="rtpeval-artifact-contract--ticket-09-preflight-decisions--2026-10-02"></a>
<a id="rtpeval-artifact-contract--ticket-09-executable-wire--2026-10-02"></a>
<a id="rtpeval-artifact-contract--ticket-09-approved-time-zone-display-extension--2026-10-02"></a>
<a id="rtpeval-artifact-contract--subsequent-user-display-cleanup--2026-10-02"></a>
<a id="rtpeval-artifact-contract--subsequent-user-uncertainty-hint-removal--2026-10-02"></a>
<a id="rtpeval-spec--rtpeval-evaluation-module-specification"></a>
<a id="rtpeval-spec--problem-statement"></a>
<a id="rtpeval-spec--solution"></a>
<a id="rtpeval-spec--user-stories"></a>
<a id="rtpeval-spec--implementation-decisions"></a>
<a id="rtpeval-spec--input-contract"></a>
<a id="rtpeval-spec--illustrative-division-of-work"></a>
<a id="rtpeval-spec--automatic-evaluation-boundary"></a>
<a id="rtpeval-spec--output-contract"></a>
<a id="rtpeval-spec--resource-metrics"></a>
<a id="rtpeval-spec--accepted-usage-handoff-and-collection-gap"></a>
<a id="rtpeval-spec--testing-decisions"></a>
<a id="rtpeval-spec--comments"></a>
<a id="rtpeval-spec--input-contract-review-checkpoint--2026-09-28"></a>
<a id="rtpeval-spec--identity-contract-draft--2026-09-28"></a>
<a id="rtpeval-spec--opening-contract-draft--2026-09-28"></a>
<a id="rtpeval-spec--route-contract-draft--2026-09-28"></a>
<a id="rtpeval-spec--route-outcome-and-requested-tolerance-update--2026-09-28"></a>
<a id="rtpeval-spec--unified-metrics-contract--2026-09-28"></a>
<a id="rtpeval-spec--specification-closeout-audit--2026-09-28"></a>
<a id="rtpeval-spec--undefined-activities-and-fallback-clarification--2026-09-28"></a>
<a id="rtpeval-spec--google-route-result-simplification-accepted--2026-09-28"></a>
<a id="rtpeval-spec--technical-contract-checkpoint--2026-09-28"></a>
<a id="rtpeval-spec--ticket-05-specification-specialization--2026-10-01"></a>
<a id="rtpeval-spec--ticket-05-implementation-follow-up--2026-10-02"></a>
<a id="rtpeval-spec--ticket-05-closeout-follow-up--2026-10-02"></a>
<a id="rtpeval-spec--ticket-09-approved-offline-implementation--2026-10-02"></a>
<a id="evaluation-artifacts"></a>
<a id="purpose-and-ownership"></a>
<a id="shared-inventory-and-confirmed-scope"></a>
<a id="scope-decisions-and-code-confirmation"></a>
<a id="simple-examples"></a>
<a id="remaining-technical-contracts"></a>
<a id="future-checks"></a>
<a id="ticket-01-specialization--2026-09-29"></a>
<a id="usage-file-shape-and-ownership"></a>
<a id="verification-seams"></a>
<a id="projection-specialization--2026-09-29"></a>
<a id="ticket-02-implementation-specialization--2026-09-29"></a>
<a id="ticket-05-semantic-wire-specialization--2026-10-01"></a>
<a id="ticket-08-executable-wire--2026-10-02"></a>
<a id="ticket-09-preflight-decisions--2026-10-02"></a>
<a id="ticket-09-executable-wire--2026-10-02"></a>
<a id="ticket-09-approved-time-zone-display-extension--2026-10-02"></a>
<a id="subsequent-user-display-cleanup--2026-10-02"></a>
<a id="subsequent-user-uncertainty-hint-removal--2026-10-02"></a>
<a id="evidence-and-time-parsing-contract"></a>
<a id="identity-and-role-handling"></a>
<a id="implementation-checks-and-limits"></a>
<a id="opening-technical-follow-up--2026-10-02"></a>
<a id="ticket-06-implemented-timeevidence-checkpoint--2026-10-02"></a>
<a id="rtpeval-evaluation-module-specification"></a>
<a id="problem-statement"></a>
<a id="solution"></a>
<a id="user-stories"></a>
<a id="implementation-decisions"></a>
<a id="input-contract"></a>
<a id="illustrative-division-of-work"></a>
<a id="automatic-evaluation-boundary"></a>
<a id="output-contract"></a>
<a id="resource-metrics"></a>
<a id="accepted-usage-handoff-and-collection-gap"></a>
<a id="repair-and-controlled-cases"></a>
<a id="presentation-of-mechanism-comparisons"></a>
<a id="testing-decisions"></a>
<a id="out-of-scope"></a>
<a id="further-notes"></a>
<a id="comments"></a>
<a id="input-contract-review-checkpoint--2026-09-28"></a>
<a id="identity-contract-draft--2026-09-28"></a>
<a id="opening-contract-draft--2026-09-28"></a>
<a id="route-contract-draft--2026-09-28"></a>
<a id="route-outcome-and-requested-tolerance-update--2026-09-28"></a>
<a id="unified-metrics-contract--2026-09-28"></a>
<a id="specification-closeout-audit--2026-09-28"></a>
<a id="undefined-activities-and-fallback-clarification--2026-09-28"></a>
<a id="google-route-result-simplification-accepted--2026-09-28"></a>
<a id="technical-contract-checkpoint--2026-09-28"></a>
<a id="ticket-05-specification-specialization--2026-10-01"></a>
<a id="ticket-05-implementation-follow-up--2026-10-02"></a>
<a id="ticket-05-closeout-follow-up--2026-10-02"></a>
<a id="ticket-09-approved-offline-implementation--2026-10-02"></a>

<a id="history"></a>

## Decision and acceptance history

The [parent specification](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12),
[published work breakdown](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12#issuecomment-5956237972)
and [historical review](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12#issuecomment-5956197027)
preserve the earlier design/approval sequence. Implementation evidence is indexed in
[records](../records/README.md); executable commands are in the
[package guide](../../backend/evaluation/README.md). Legacy anchors resolve to their current
topic or this history section; they do not restore superseded wording as current policy.
