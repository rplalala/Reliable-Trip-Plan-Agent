# Quality scores and anonymous human review

Current implemented Tickets 08-09 contract, updated 2026-10-03. Automatic verified compliance,
human preference, resources and later mechanism/Repair tracks have separate meanings.
[Evaluation architecture](../0006-independent-evaluation.md) owns status; formal comparative
analysis and later-ticket implementation are outside this document's execution scope.

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
| Date coverage, density, canonical repetition | [Descriptive schedule](0003-requirement-schedule.md#descriptive): requested dates, source occurrences and adopted identities; no extra quality penalty |
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
immutable `QualityReportResult`; `to_dict()` exports `rtpeval_quality_report_1`.
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
from linked usage envelopes and optional projection availability. Descriptive density,
repetition, raw transfer burden, resources and V3 internal findings add no penalties.
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

V3 before/after correspondence/masks remain accepted but unimplemented Ticket 10 work.
Controlled Repair and mechanism/official-evidence reporting remain Tickets 11-12; their
accepted independent outcome/eligibility boundaries are in
[follow-up scope](0001-evaluation-artifacts.md#planned). No optional-track metric becomes
part of this final four-version total by implication. Human results remain separate from
automatic scores; no overall human total or inferential analysis is supplied.

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
