# Quality scores and anonymous human review

Current implemented Tickets 08-10 contract, updated 2026-10-04. Automatic verified compliance,
paired diagnostics, human preference, resources and mechanism/controlled-Repair tracks have separate meanings.
[Evaluation architecture](../0006-independent-evaluation.md) owns status; formal comparative
analysis and new implementation require separately authorized work.

<a id="rtpeval-metrics-contract"></a>
<a id="rtpeval-metrics-contract--rtpeval-unified-metrics-contract--draft"></a>
<a id="rtpeval-metrics-contract--population-sources-and-units"></a>
<a id="rtpeval-metrics-contract--common-report-contract"></a>
<a id="rtpeval-metrics-contract--a-independent-itinerary-metrics"></a>
<a id="rtpeval-metrics-contract--b-resource-metrics"></a>
<a id="rtpeval-metrics-contract--ticket-05-specification-closure--2026-10-01"></a>
<a id="rtpeval-metrics-contract--ticket-06-preflight-metric-clarification--2026-10-02"></a>
<a id="rtpeval-metrics-contract--ticket-06-executable-measurements--2026-10-02"></a>
<a id="rtpeval-metrics-contract--ticket-07-specification-preflight-closure--2026-10-02"></a>
<a id="rtpeval-metrics-contract--ticket-07-executable-route-measurements--2026-10-02"></a>
<a id="rtpeval-metrics-contract--ticket-08-specificationinterface-preflight--2026-10-02"></a>
<a id="rtpeval-metrics-contract--ticket-08-implemented-report--2026-10-02"></a>
<a id="rtpeval-unified-metrics-contract--draft"></a>
<a id="population-sources-and-units"></a>
<a id="common-report-contract"></a>
<a id="a-independent-itinerary-metrics"></a>
<a id="b-resource-metrics"></a>
<a id="ticket-06-preflight-metric-clarification--2026-10-02"></a>
<a id="ticket-08-implemented-report--2026-10-02"></a>

<a id="metrics"></a>

## Units, states and metric ownership

Each metric preserves sources, unit/scope, applicable/known/unresolved populations, raw
counts, evidence coverage, reason codes and rule hashes. PASS meets the applicable rule;
FAIL has sufficient contradiction; UNKNOWN retains applicable unresolved facts; N/A has no
applicable checks. Material failure requires correction, not a zero quality score. Empty or
unestablished denominators produce null rates rather than perfect compliance.

| Dimension/measurement | Authoritative owner and units |
| --- | --- |
| Requirement fulfillment | [Reviewed obligations](0003-requirement-schedule.md#obligations): one parent obligation, all count/date/time components retained |
| Grounding / claimed-ID consistency | [Independent identity](0002-intake-identity-usage.md#identity): primary source occurrences; wrong supplied ID remains separate from intended-place resolution |
| Non-overlap / occupied time | [Schedule](0003-requirement-schedule.md#non-overlap): logical commitments, pair/union measurements and protected boundaries |
| Opening | [Opening](0004-opening-routes.md#opening): primary visits; complete evidence versus partial decisive verdicts and outside-duration lower bounds |
| Routes / transfer burden | [Routes](0004-opening-routes.md#route-verdicts): same-day occurrence legs; one combined verdict with separate cap/time/distance evidence |
| Date coverage, density, canonical repetition | [Descriptive schedule](0003-requirement-schedule.md#descriptive): raw counts and adopted identities; [daily density](#daily-density) adds a reviewed pace deduction to the overall score |
| Latency, calls, tokens, HTTP/cache events | [Usage](0002-intake-identity-usage.md#usage): observed scope/namespace; Repair subsets are not added twice |

Conditional `P/(P+F)` is diagnostic compliance and accompanies coverage/UNKNOWN. It is not
the auxiliary score formula. Unresolved lookup is not a hallucination rate; shorter travel,
more activities and fewer repetitions are not automatic subjective improvement. Visits and
six within-group version pairs are correlated; request-level records remain the comparison
unit. Formal aggregation, inference and post-result weight tuning are not implemented here.

<a id="rtpeval-score-profile"></a>
<a id="rtpeval-metrics-contract--d-subscores-and-auxiliary-total"></a>
<a id="rtpeval-score-profile--dimension-scores-and-auxiliary-total--accepted-scoring-structure"></a>
<a id="rtpeval-score-profile--purpose"></a>
<a id="rtpeval-score-profile--accepted-five-dimensions"></a>
<a id="rtpeval-score-profile--accepted-verified-compliance-score"></a>
<a id="rtpeval-score-profile--accepted-applicability-and-zero-opportunity-rules"></a>
<a id="rtpeval-score-profile--accepted-structure-and-implementation-boundary"></a>
<a id="rtpeval-score-profile--terminology-and-companion-rates"></a>
<a id="rtpeval-score-profile--ticket-05-unit-specialization--2026-10-01"></a>
<a id="rtpeval-score-profile--ticket-08-specification-preflight--2026-10-02"></a>
<a id="rtpeval-score-profile--ticket-08-implemented-specialization--2026-10-02"></a>
<a id="d-subscores-and-auxiliary-total"></a>
<a id="dimension-scores-and-auxiliary-total--accepted-scoring-structure"></a>
<a id="accepted-verified-compliance-score"></a>
<a id="accepted-applicability-and-zero-opportunity-rules"></a>
<a id="terminology-and-companion-rates"></a>

<a id="scores"></a>

## Exact final-report scores, common masks and availability

`quality_report.build_quality_report` reuses the three independent offline scorers and
validated primary-visit identity records. It accepts intake, identity report, snapshot
directory and optional reviewed schedule/occupancy/route/coordinate envelopes, with an
optional trusted `expected_plan` and required offset-aware `generated_at`. It returns an
immutable `QualityReportResult`; `to_dict()` exports `rtpeval_quality_report_2`.
No provider client, planner graph or extra dependency is constructed.

Executable commands are in the [package guide](../../backend/evaluation/README.md).

All options are optional for CLI replay; missing independent evidence retains the
existing scorer policy. An absent `--generated-at` uses current UTC. Final-only
`paired=False` evidence is required; a valid paired snapshot receives the explicit
`unsupported_snapshot_scope` diagnostic. Optional V3 projection availability is exposed
without paired scores/deltas. Exit 0 means complete replay, including quality FAIL,
UNKNOWN and unavailable totals; material/replay correction emits empty groups and exit 2.

Root `components` preserves each scorer's schema, rules and source/hash metadata.
`source_hashes.artifacts` preserves intake's exact artifact hashes; independent identity/
review/audit/reference, preparation and snapshot/plan digests remain explicit. CLI exact
preparation-file SHA-256 is separate from canonical object hashing. `content_hash` covers
all output fields except `generated_at` and itself, including CLI file hashes. Explicit
time plus identical sources/rules reproduces sorted JSON. Sources are never mutated.

Each group exports the ordered common `included_dimensions`, exact rational
`dimension_weights`, included count, four keyed `versions` and `all_totals_available`.
Each version exports raw `primary_metrics`, normalized `dimensions`, `auxiliary_total`,
`daily_density`, `overall_total`,
descriptive/schedule/occupancy measurements and untouched component row hashes.

For established N=P+F+U>0, verified score is 100*P/N. Rates in 0-1 and exact count
fractions accompany coverage (P+F)/N, U/N, F/N and conditional P/(P+F). UNKNOWN remains
UNKNOWN; conditional compliance does not determine the score. Parent obligations,
logical commitments, primary visits and combined route legs retain one weight.
Grounding uses source occurrences/validated identity records rather than caller summary
counts. Claimed-ID conflicts and unknown role populations remain separate records.

All-four proven N=0 excludes a dimension jointly. Included single-version N=0 keeps
raw N/A/null rates and contributes zero. Unresolved applicability preserves partial
checks but makes its dimension/contribution and affected version total null, retaining
the mask and weights. Empty masks return null totals and an upstream reconciliation
diagnostic. Means use unrounded rational contributions, not rounded percentages.
Different requests retain their own masks; no pooled comparison or ranking is computed.

`stage_availability` distinguishes resource/human/mechanism reports (`not_integrated`)
from linked usage envelopes and optional projection availability. Raw density measurements
feed the reviewed daily deduction below. Repetition, raw transfer burden, resources and
V3 internal findings add no additional penalties.
Findings-only source changes preserve numeric scores after correct relinking/replay;
source/report hashes may change, and stale evidence remains invalid.

[Acceptance](../records/evaluation/quality-report.md#rtpeval-ticket-08-acceptance) records actual red/green,
regression, review, commits and limits. The [preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20#issuecomment-5955702362)
preserves the original no-implementation checkpoint and subsequent scope approval.

For a fixed established population, replacing PASS with UNKNOWN reduces verified credit;
replacing FAIL with UNKNOWN leaves it unchanged. UNKNOWN is not relabelled FAIL. This
lower-bound verified-compliance accounting does not prove immunity to activity deletion or
changed applicability; retain counts, coverage and unresolved populations. Totals with
different common masks do not measure identical content. Equal weights are a transparent
choice, not proof of statistical independence or overall travel usefulness.

<a id="daily-density"></a>

### Daily density policy and overall score (2026-10-04)

The current numeric authority is the final approved table in
[Issue #52](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/52), implemented
as `rtpeval_daily_density_2`. Earlier density curves are historical only. Final and
paired report wire shapes stay at version 2; their embedded density profile and rule
hash identify the current deductions.

The user's approved development-time scoring change preserves the five-dimensional
`auxiliary_total` and adds `overall_total = max(0, auxiliary_total - mean_daily_penalty)`.
The mean gives every inclusive requested date equal weight, including missing/empty
days. Calculate with exact rational values before emitting numeric percentages.
The rule/profile versions distinguish this report from historical five-dimensional-only
reports; old artifacts are not rewritten. `all_totals_available` now describes overall
totals. An unavailable auxiliary score or unresolved daily deduction keeps the overall
score null; even a 100-point deduction cannot make missing feasibility evidence available.

| Primary visit count | Ordinary | Relaxed | Rich |
| --- | ---: | ---: | ---: |
| 0 | 100 | 100 | 100 |
| 1 | 40 | 20 | 60 |
| 2 | 0 | 0 | 0 |
| 3 | 10 | 40 | 0 |
| 4 | 50 | 70 | 30 |
| 5 | 80 | 90 | 70 |
| 6 or more | 100 | 100 | 100 |

For four and five visits, deductions strictly increase from rich to ordinary to
relaxed. Ordinary pace now deducts 10 for three visits; relaxed pace deducts 40.
Uncertain ordinary counts spanning two and three visits therefore have deduction
bounds 0..10 and an unavailable exact deduction; they are not a zero-cost interval.

Counts reuse the requirement/schedule scorer's source-distinct primary occurrences;
transport, breaks and Nearby suggestions are excluded. Same-venue repeat occurrences
remain occurrences; canonical repetition is separately reported. This change does not
replace the legacy `<2`, `2..5`, `>5` descriptive categories or planner V3 quantity rules.
The 2..5 window is not a blanket exemption from busyness deductions.

`--density-reviews` supplies `rtpeval_density_reviews_1` with `batch_id`,
`batch_revision` and a `groups` array. Each reviewed group has `group_id`,
`input_sha256`, `reviewer_ref`, offset-aware `reviewed_at`, `review_origin` (`human`
or `agent`), `rationale`, a `default` policy and `days` overrides. A policy has exactly
`profile` (`ordinary`, `relaxed`, `rich`, `unresolved`), `exact_count` (null or a
nonnegative integer) and nonempty `source_refs` quoting original Input through
`field_path`, `quote` and optional existing quote occurrence/offset fields. A dated
override adds `date`; dates must be requested and unique. The reviewer must examine
the full original request for pace and count exceptions; mechanical quote validation
does not independently prove that its semantic interpretation is correct. Planner
requirements, internal findings and planner density summaries are never policy evidence.
Canonical review hashes and exact CLI file hashes bind this additional preparation.
Foreign, stale, duplicate or malformed material fails the whole batch.

Dated policies override the trip default. To retain the default profile while changing
only the count, repeat that profile explicitly in the dated policy. An explicit count
matching the actual count deducts zero, including requested rest days or 1/4/5/6+ visits.
A confirmed mismatch deducts 100 in this daily policy and is labelled
`explicit_count_mismatch`; it does not fabricate another named-place obligation in the
five-dimensional requirements metric. This requires an actual reviewed exact number:
relaxed/rich descriptions alone cannot supply one. A trip-wide explicit daily number
belongs in `default.exact_count`; a date-specific number belongs only in its override.

Without a review, a request with no `additional_preferences` defaults to ordinary.
Nonempty free text may contain pace/count exceptions, so missing review retains an
unresolved policy and unavailable deduction rather than silently choosing ordinary.
An explicitly reviewed unresolved profile also stays unavailable unless an exact count
determines the deduction. For uncertain visit populations, evaluate every reachable
penalty, retaining minimum/maximum bounds: penalty curves are nonmonotonic. Emit an
exact deduction only when all possible counts produce the same value. UNKNOWN is never
automatically zero, FAIL, or an assumed midpoint.

<a id="rtpeval-metrics-contract--c-human-and-independent-repair-reporting"></a>
<a id="quality-human-review"></a>
<a id="c-human-and-independent-repair-reporting"></a>

<a id="human"></a>

## Anonymous packages, answers and descriptive human reports

The human track is independent of automatic reports. It reads accepted, exact-byte-linked
final v0-v3 material and needs neither route/opening snapshots nor complete resource
observations. Real assessment requires separate approval.

The three dimensions are `preference`, `pace` and `usefulness`. Public A/B/C/D labels
stay fixed across dimensions within a task. Render the original request and the same
activity/place/time/notes/amount fields through one template for all versions. Nearby is
hidden; authoritative transport claims are displayed without duplicate journeys. Do not
invent ambiguous correspondence or use an LLM to rewrite travel meaning. Public material
and answers expose neither private version assignments, canonical IDs, raw source filenames,
internal validation/provider badges nor automatic scores. Content itself can still suggest
a version, so blinding is not an absolute guarantee.

Wire owners are `rtpeval_human_preparation_1`, `rtpeval_human_config_1`,
`rtpeval_human_display_reviews_1`, `rtpeval_human_package_1`, `rtpeval_human_mapping_1`,
`rtpeval_human_answer_1`, `rtpeval_human_answers_1`, `rtpeval_human_import_1` and
`rtpeval_human_report_1`. Root envelopes use `schema_version`; each answer uses
`answer_schema_version`. An answer contains public `batch_id`, `batch_revision`,
`presentation_id`, `presentation_hash`, `rater_ref`, `task_id`, positive `answer_revision`,
aware `updated_at`, `state=draft|submitted` and keyed `responses`. A response uses
`status=ranked|unable_to_judge|not_applicable|pending` with optional reason; pending is
draft-only. Ranked `tie_groups`, such as `[["A","C"],["B"],["D"]]`, partition all four
labels in a submitted response; unassessable responses contain no ordering. Bundles have
exactly `schema_version=rtpeval_human_answers_1` and an `answers` array. Submitted answers
require all three dimensions; drafts may be incomplete. The exact frozen presentation hash
links the public material, while the private mapping retains source/review hashes and actual
assignments. Report generation time must be offset-aware; pin it for reproducible replay.

Configuration uses `schema_version=rtpeval_human_config_1`, three opaque 32-character
lowercase hexadecimal identifiers (`public_batch_id`, `presentation_id`, `rater_ref`),
positive integer `revision`, explicit integer `seed`, positive `duplicate_min_gap` and
an ordered `tasks` array. A main entry is `{"group_id":"g"}`; a duplicate entry adds
`"duplicate_of":0`, the zero-based original main-task index. Repeated main groups,
references to duplicates, unknown groups and insufficient spacing are errors. There
are no fixed task/sample quotas. Seeded shuffled Latin blocks balance version/label
positions across all shown tasks; main/duplicate/combined counts are private diagnostics.
Use a fresh presentation identifier/revision when preparing a new assessment.

Executable commands are in the [package guide](../../backend/evaluation/README.md).

All output paths must be new. The public directory contains only `review.html` and
`presentation.json`; keep mapping/preparation/review files outside it and give only the
public files to the rater. Open `review.html` directly in a local browser; no server,
account, CDN, hosted submission or database is needed. Runtime CSP blocks network access.
Source text renders as inert text and dates/offsets are preserved. Missing arrivals may
add an explicitly labelled inferred arrival from supplied valid departure/duration;
the original arrival remains absent and inference never feeds automatic scoring.

The approved time-zone display extension adds a Time zone dropdown, default UTC, using
the browser's available IANA zones (a small common-zone fallback on older runtimes).
Explicit-offset start/end/departure/supplied-arrival/inferred-arrival timestamps display
their converted date and a 24-hour HH:mm clock, including midnight and daylight-saving
changes. Source day headings retain original grouping; they are not converted dates.
Following the user's display-cleanup request, the optional Original timestamp control
and its instructions are removed. Exact source strings remain in the frozen material.
Local timestamps/clocks without a supplied offset are not converted; invalid dates/
clocks remain original values and missing values display Not supplied.
Date-only request values and free-text notes are unchanged. Zone selection is a view
preference for the current window; it does not rewrite frozen public/private artifacts,
answer revisions/exports or automatic reports. Runtime time-zone names/rules come from
local Intl data; the renderer makes no external request or inferred destination zone.
[Time-zone scope and validation](../records/evaluation/blinded-ranking-record.md#rtpeval-ticket-09-timezone-display)
records this separately approved extension.
[Display cleanup](../records/evaluation/blinded-ranking-record.md#rtpeval-ticket-09-display-cleanup) records the user's
subsequent timestamp-control removal and HH:mm format correction.

The user's subsequent [uncertainty hint removal](../records/evaluation/blinded-ranking-record.md#rtpeval-ticket-09-uncertainty-display)
hides the dedicated Uncertainty/unknowns field, all item notices and time-conversion
warning text. Inferred arrival remains labelled, while HH:mm clocks, dates and the
time-zone selector remain. Ordinary source notes/preferences and duration basis remain
source text. Frozen public/private material still retains unknowns/notices and exact
hashes; UI suppression neither verifies a claim nor rewrites answers/scoring.

Preparation is researcher-only. Its `fields` list records `field_ref`, exact source-file
`source_sha256`, source pointer, `original`, canonical `original_sha256` and likely leakage
flags. A review has `schema_version=rtpeval_human_display_reviews_1`, the exact
`preparation_hash`, `reviewer_ref`, aware `reviewed_at`,
`preserves_facts_and_uncertainty=true`, `redactions` and `allowed_flags` arrays.
Each redaction names the field and both hashes, with `display_text` and `reason`.
Only remove explicit version/provider/internal-review identifiers; keep travel facts
and uncertainty. An allowed flag uses the same field/hash linkage and reason for a
legitimate name or meaning resembling an identifier; it is not permission to expose
version metadata. Review the entire prospective material, including unflagged prose;
lexical checks cannot guarantee semantic blinding. Unresolved flagged text blocks delivery.
Changing original bytes requires relinking the delivered batch and repeating review.

Rank each dimension with positions 1-4, equal positions for ties, or an explicit
unable-to-judge/N/A response. Save drafts before navigating and download JSON before
closing. Local storage is best-effort; a failure is visible and portable JSON remains
available. Import is atomic and validates the exact presentation/rater, states and
rank partition. Corrections create a higher complete submitted revision; it supersedes
old effective answers while old revisions stay audit-only. Drafts do not supersede
submissions; importing identical revisions is idempotent and contradictory same-revision
content blocks processing. Multiple answer files can be supplied to import/report.

The researcher report preserves effective revisions/hashes, all retained revisions,
six mapped pair outcomes per assessable dimension, available denominators and distinct
missing/unjudgeable/N/A/draft-only counts. Hidden duplicates contribute version-based
consistency only; no comparable pairs yields null agreement. Pairs from one request
are correlated. No overall human score, inferential analysis or automatic-quality
integration is supplied. Frozen mapping hashes verify integrity, not cryptographic
authorship. [Acceptance](../records/evaluation/blinded-ranking-record.md#rtpeval-ticket-09-acceptance) records actual
test/review/browser evidence and remaining limitations.

<a id="rtpeval-metrics-contract--e-remaining-decisions-and-technical-work"></a>
<a id="e-remaining-decisions-and-technical-work"></a>

<a id="planned"></a>

## Follow-up reporting boundary

Ticket 10 supplies a separate [V3 paired diagnostic](#v3-pairs), with source-driven
correspondence and independent checks. It does not alter the four-final report above.
Controlled Repair and mechanism/official-evidence reporting remain Tickets 11-12; their
accepted independent outcome/eligibility boundaries are in
[follow-up scope](0001-evaluation-artifacts.md#planned). No optional-track metric becomes
part of this final four-version total by implication. Human results remain separate from
automatic scores; no overall human total or inferential analysis is supplied.

<a id="v3-pairs"></a>

## V3 draft/final-primary diagnostic

The [accepted Ticket 10 specification](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22#issuecomment-5955706453)
owns the source-first decision. `build_v3_pair_report` and `v3_pair_cli` compare only
the selected same-run `/v3/draft` and `/v3/final_primary`. Every selected group remains
inventoried. Missing/invalid optional stages yield `pair_unavailable`, original intake
diagnostics and null paired deltas. `/itinerary` is never a substitute. Available
stages can retain standalone observations. If all pairs are unavailable, no fictional
snapshot is required. Otherwise require a verified `paired=True` evidence snapshot
and current identity replay, with the same original input and RequirementSpec.

The report calls the public requirement/schedule, opening and route scorers, verifies
all expected final/optional rows and source hashes, then selects the two V3 stages.
The reviewed-coordinate and saved identity-snapshot paths retain Ticket 07 semantics.
Foreign/stale supplied sources, preparation/reviews or corrupt snapshots fail atomically;
they do not silently shrink the cohort or become itinerary FAIL.

The five dimensions retain exact P/(P+F+U) arithmetic and equal weights. The **pair's**
common mask excludes a dimension only when both stages establish zero denominators.
An included true no-check stage has null raw rates and zero accounting contribution.
An unresolved denominator retains the dimension but makes its contribution and affected
total unavailable. An empty mask has null totals. Signed changes are final minus draft,
including exact rational score differences and percentage points. Defined identical
metrics give zero; unavailable values never acquire zero through imputation. This mask
and its auxiliary totals are distinct from Ticket 08's four-final comparison.

`rtpeval_v3_pair_report_2` applies the same reviewed density policy to both stages.
Each stage exports daily deductions and `overall_total`; `deltas.overall_total` is
the exact final-minus-draft overall change, while `deltas.auxiliary_total` preserves
the original five-dimensional delta. Mean deduction changes are also exported.
Independent mechanism preparation accepts historical pair report 1 and current report 2
with the same exact source/hash checks. Density improvement is not proof of repairing a
different feasibility conflict or of general travel usefulness.

Each stage preserves original checks, P/F/U/N/A counts, denominators, schedule commitments,
conflicts, evidence/basis coverage, duration subtotals, lower bounds and observed traffic
burden. The report exports population, date coverage, density/repetition and measurement
differences. A subtotal difference describes its observed populations; it is not an exact
full-trip difference when coverage changes or evidence is partial. Visit losses/additions,
venue replacements, role losses and unresolved correspondence remain separate.

### Source correspondence and review

`read_v3_result_sources` rereads selected manifest artifacts through the safe relative-path
and byte-hash rules. `prepare_v3_correspondence` emits immutable
`rtpeval_v3_edit_provenance_1`; its optional source envelope is
`rtpeval_v3_result_sources_1` with batch/revision and records containing group/run,
input/result SHA256 and original UTF-8 result bytes. Verify exact associations and stage
observations before using embedded material. A supplied preparation is recomputed against
original sources; an arbitrary caller-written edit summary is not accepted.

Within a checked chain, unique producer IDs identify edited slots. Validate Repair original,
ordered round inputs/adopted states, result original/final and cumulative final. Only
actually adopted changes, effective edits and accepted component membership establish
relations. Rejected/pending/rolled-back components do not enter adopted lineage. Compose
retime/move/replace/delete/add and free-time fragments across rounds; validate parent/root/
child membership, fragment complements, dates and collision-free IDs. Record edit pointers.
Sorting, source-ledger place-name normalization and transfer refresh are reconciled
separately. Identical validated source snapshots also support unchanged IDs without Repair.

Source lineage, canonical venue identity and quality are three separate facts. Replacement
can preserve a slot while changing the independently confirmed venue, or retaining the same
venue. Identity UNKNOWN does not invalidate known source lineage. Internal accepted/resolved/
PASS judgments never establish independent identity or compliance. Complex recorded edits
are automatically traceable; they do not require review solely because they are complex.

Missing/inconsistent embedded lineage gives explicit local diagnostics, then uniquely
unchanged content or globally unique independent canonical matching supplies weaker
fallback. Do not use title semantics, nearest time, array position, favorable outcomes or
greedy leftover venue matching. Residual occurrences produce review requests and coverage
counts; unresolved local correspondence does not erase valid aggregate deltas.

Optional `rtpeval_v3_correspondence_1` reviews carry batch/revision and records with
group/run/result SHA256, full `before`/`after` stage source refs, `relation`, `reviewer_ref`,
offset-aware `reviewed_at`, `rationale`, and optional string `supporting_refs`. Relations
are unchanged/modified/moved/replaced/split/merged/complex/added/removed. Check exact
membership, disjoint participation, cardinality and observable unchanged/moved claims.
A review cannot override contradictory established correspondence. Many-to-many groups
retain constituent checks without invented one-to-one edges or new success denominators.

### Independent continuity

Match requirements by original obligation ID; retain count/date/time components and
regressions. Compare opening/grounding only for independently compatible continued visits.
Deletion records removal; venue replacement retains old/new checks without repairing the
old venue's fact. Directed route endpoints retain connection lineage separately from venue
compatibility; inserted visits yield removed direct legs and added legs. Query/date/mode/
departure context changes remain explicit and each stage uses its own applicable evidence.

Overlap continuity uses independently continued participants, rather than generated check
IDs or equal clock spans. Protection continuity retains the original obligation/scope.
Removal is not resolution. Introduced conflicts require confirmed before non-conflict or
established new participants; uncertainty retains unresolved attribution. Compatible
FAIL-to-PASS can be resolved, FAIL-to-UNKNOWN is unverified change, and PASS-to-UNKNOWN is
lost verification. Partial improvement requires comparable exact FAIL magnitudes under the
same rule; missing or lower-bound magnitudes do not qualify. No overall Repair-success
classification, causal conclusion, live acquisition or planner instrumentation is supplied.

The current wire is `rtpeval_v3_pair_report_2`; `_1` remains a historical format
accepted by independent mechanism preparation. Reports preserve rule/component/source
hashes, per-group stage
availability, mask, exact deltas, correspondence and continuity. Content hashing excludes
creation time. CLI file-byte hashes remain distinct from canonical preparation digests.
Exit 0 means complete processing, including unavailable pairs and quality FAIL/UNKNOWN;
material/replay correction exits 2. Commands are in the [package guide](../../backend/evaluation/README.md).

<a id="ticket-05-specification-closure--2026-10-01"></a>
<a id="ticket-06-executable-measurements--2026-10-02"></a>
<a id="ticket-07-specification-preflight-closure--2026-10-02"></a>
<a id="ticket-07-executable-route-measurements--2026-10-02"></a>
<a id="ticket-08-specificationinterface-preflight--2026-10-02"></a>
<a id="purpose"></a>
<a id="accepted-five-dimensions"></a>
<a id="accepted-structure-and-implementation-boundary"></a>
<a id="ticket-05-unit-specialization--2026-10-01"></a>
<a id="ticket-08-specification-preflight--2026-10-02"></a>
<a id="ticket-08-implemented-specialization--2026-10-02"></a>

<a id="history"></a>

## Implementation and historical decisions

Code: [quality report](../../backend/evaluation/quality_report.py),
[human packages](../../backend/evaluation/human_tasks.py),
[answer validation](../../backend/evaluation/human_answers.py),
[human report](../../backend/evaluation/human_report.py) and
[renderer](../../frontend/src/features/blind-review/BlindReview.tsx).
Commands are in the [package guide](../../backend/evaluation/README.md).
The [score preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20#issuecomment-5955702362),
[score acceptance](../records/evaluation/quality-report.md#rtpeval-ticket-08-acceptance),
[human preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21#issuecomment-5955704071)
and [human acceptance](../records/evaluation/blinded-ranking-record.md#rtpeval-ticket-09-acceptance)
preserve approval/validation and the superseded UI controls. Current rendering uses IANA
zones and HH:mm, keeps Inferred arrival, and hides dedicated uncertainty/item-warning hints;
source artifacts retain their original uncertainty. This view choice is not factual verification.
