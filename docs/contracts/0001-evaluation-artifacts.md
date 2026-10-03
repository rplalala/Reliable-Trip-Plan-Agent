# Evaluation artifacts, scope and time

Current shared contract, reconciled with the implemented Tickets 01-09 on 2026-10-03.
[PROJECT.md](../../PROJECT.md) owns scope; [evaluation architecture](../0006-independent-evaluation.md)
owns implemented/deferred boundaries. GitHub owns task state. This reference states current
rules together; dated proposals, approvals and validation remain in linked history.

<a id="rtpeval-spec"></a>
<a id="scope"></a>

## Batch ownership and reader separation

Evaluation consumes an explicitly selected, producer-attested batch of four-version groups.
It does not select cases, rerun planners, recompute workflow completion or improve the source
itineraries. A qualifying group means workflow completion was established upstream, not that
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
individual scorers does not implement Ticket 10's before/after report.

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

Ticket 12 separates mechanism exposure/usage from independent quality and causality. Official
Evidence Audit includes only accepted facts exposed to a model or used by a rule, with separate
independent supported/contradicted/scope-mismatch/unavailable outcomes. Rejected/unused/search-
only material is outside that denominator. Exact extraction/reporting remains deferred.
See [Ticket 11](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23) and
[Ticket 12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24).

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
