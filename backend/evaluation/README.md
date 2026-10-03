# Independent evaluation package

Tickets 01-11 have offline implementations for explicitly submitted immutable material.
Ticket 12 remains unimplemented. Ordinary scoring consumes saved outputs; the isolated
Ticket 11 command executes only frozen V3 post-primary cases. No formal corpus or
comparative research is constructed by these commands.
[Evaluation architecture](../../docs/0006-independent-evaluation.md) owns scope.
Ticket 11's [controlled replay contract](../../docs/contracts/0001-evaluation-artifacts.md#controlled-repair)
defines execution inputs, independent conditions and human supplementation.

## Contract and module navigation

Current rules have one topic owner. Read the relevant contract before preparing inputs;
acceptance records and Issue comments preserve historical decisions, not alternate rules.

| Responsibility | Current contract | Implementation |
| --- | --- | --- |
| Batch/artifact wire and deferred tracks | [Artifacts](../../docs/contracts/0001-evaluation-artifacts.md) | [intake](intake.py), [records](records.py), [projection](projection.py) |
| Structural claims and occurrence association | [Intake/claims](../../docs/contracts/0002-intake-identity-usage.md#claims) | [preparation](preparation.py), [claims](_claims.py) |
| Independent identities and review | [Identity](../../docs/contracts/0002-intake-identity-usage.md#identity) | [identity](identity.py), [addresses](_addresses.py) |
| Request planning and frozen replay | [Snapshots](../../docs/contracts/0002-intake-identity-usage.md#snapshots) | [snapshot](snapshot.py) |
| Opt-in usage and descriptive resources | [Usage](../../docs/contracts/0002-intake-identity-usage.md#usage) | [usage capture](../app/observability/usage_capture.py), [usage_report](usage_report.py) |
| Reviewed requirements, time and occupancy | [Requirement/schedule](../../docs/contracts/0003-requirement-schedule.md) | [requirement_schedule](requirement_schedule.py), [schedule_time](schedule_time.py), [occupancy](occupancy.py) |
| Opening and route compliance | [Opening/routes](../../docs/contracts/0004-opening-routes.md) | [opening](opening.py), [routes](routes.py), [route preparation](_route_preparation.py) |
| Final five-dimension auxiliary report | [Quality](../../docs/contracts/0005-quality-human-review.md#scores) | [quality_report](quality_report.py) |
| Anonymous packages, revisions and human reports | [Human](../../docs/contracts/0005-quality-human-review.md#human) | [human_tasks](human_tasks.py), [human_answers](human_answers.py), [human_report](human_report.py) |
| Frozen V3 execution and controlled outcomes | [Controlled Repair](../../docs/contracts/0001-evaluation-artifacts.md#controlled-repair) | [controlled CLI](controlled_cli.py), [replay](controlled_replay.py), [report](controlled_report.py) |

## Offline workflow and CLI

Run from the repository root with the existing Python environment. Names below represent
researcher-prepared files; commands do not generate missing independent evidence. For each
CLI, `--help` gives executable arguments. Default reports go to stdout; save them outside
source artifacts. Human output paths must be new. No command below acquires live evidence.

<a id="entry-points"></a>
<a id="manifest-and-envelope-vocabulary"></a>
<a id="independent-review-replay"></a>
<a id="identity-replay-ticket-03"></a>
<a id="validation"></a>
<a id="ticket-04-independent-snapshots"></a>
<a id="independent-preparation-formats"></a>

### Intake and identity

```powershell
.venv/Scripts/python.exe -m backend.evaluation manifest.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli identity-plan manifest.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli replay identity-snapshot --expected-plan identity-plan.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli identity-evidence identity-snapshot
.venv/Scripts/python.exe -m backend.evaluation.identity_cli manifest.json identity-evidence.json audit-plan.json --reviews identity-reviews.json
```

An acquisition caller separately uses `build_identity_plan`, injected async
`acquire_snapshot`, immutable `load_snapshot`, then `identity_evidence`.
There is no built-in live Google client or acquisition CLI. The caller owns credentials,
authorization and explicit send ceilings. An identity audit plan is mandatory; unresolved
review cases remain visible instead of being silently accepted. Intake exits 0 for accepted
material or 2 for correction. Identity exits 0 for complete, 3 for pending review, 2 for
material/linkage errors; complete does not mean every identity is resolved.

<a id="offline-evaluation-preparation-and-metrics-tickets-01-06"></a>
<a id="ticket-05-offline-requirement-and-schedule-metrics"></a>
<a id="ticket-06-offline-opening-compliance"></a>
<a id="ticket-07-offline-same-day-routes"></a>
<a id="selection-and-scoring"></a>

### Independent schedule, opening and routes

```powershell
.venv/Scripts/python.exe -m backend.evaluation.requirement_schedule_cli manifest.json identity-report.json --context schedule-context.json --occupancy-reviews occupancy-reviews.json
.venv/Scripts/python.exe -m backend.evaluation.route_cli prepare manifest.json identity-report.json --context schedule-context.json --occupancy-reviews occupancy-reviews.json --route-reviews route-reviews.json --coordinates coordinates.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli evidence-plan manifest.json identity-report.json route-contexts.json
.venv/Scripts/python.exe -m backend.evaluation.opening_cli manifest.json identity-report.json evidence-snapshot --context schedule-context.json --expected-plan evidence-plan.json
.venv/Scripts/python.exe -m backend.evaluation.route_cli score manifest.json identity-report.json evidence-snapshot --context schedule-context.json --occupancy-reviews occupancy-reviews.json --route-reviews route-reviews.json --coordinates coordinates.json --expected-plan evidence-plan.json
```

Save prepared route contexts, build the evidence plan and acquire/replay its snapshot
through the separately authorized injected caller before scoring. Preparation does not
invent coordinates or transport restrictions. Missing optional context/review retains
UNKNOWN or applicability diagnostics. Route preparation exports `route_contexts` and its ready-made `evidence_plan`.

When the adopted identity report was resolved from an independent identity snapshot that
already contains coordinates, replace `--coordinates coordinates.json` with
`--identity-snapshot identity-snapshot` on route prepare/score or quality-report commands.
The library keyword is `identity_snapshot_directory`; direct inspection uses
`prepare_snapshot_coordinates` in [snapshot_coordinates](snapshot_coordinates.py).
Each replay verifies the snapshot and its exact identity linkage. Source-derived coordinate
records retain response hashes/pointers and retrieval times, without fabricated review fields.
Missing, invalid or conflicting coordinates stay diagnostic and do not trigger acquisition.
Select one coordinate source; the existing reviewed envelope and query options remain available.
The automatic path uses existing default query options and requires its own matching evidence
plan; previously prepared manual-coordinate query hashes are not interchangeable.
Use that plan directly, or put the context array under `{"contexts": [...]}` in
`route-contexts.json` for the snapshot planning CLI; the full preparation report is not
that CLI input. `--expected-plan` optionally enforces trusted full-plan equality.

Library seams: `score_requirement_schedule`, `prepare_routes`, `score_opening`, and
`score_routes`. These and identity/snapshot plan commands support `--paired` where
declared, selecting available V3 draft/final-primary projections; paired scope must
remain consistent across inputs. Ticket 10 combines these paired outputs below.
Scorers exit 0 for complete processing, including FAIL/UNKNOWN,
or 2 for material/replay correction. Snapshot commands exit 2 for invalid replay/input.

<a id="ticket-08-final-multimetric-report-and-auxiliary-scores"></a>

### Final report and resources

```powershell
.venv/Scripts/python.exe -m backend.evaluation.quality_report_cli manifest.json identity-report.json evidence-snapshot --context schedule-context.json --occupancy-reviews occupancy-reviews.json --route-reviews route-reviews.json --coordinates coordinates.json --expected-plan evidence-plan.json --generated-at 2026-10-03T00:00:00Z
.venv/Scripts/python.exe -m backend.evaluation.usage_report usage-v0.json usage-v1.json usage-v2.json usage-v3.json
```

`build_quality_report` combines the existing independent scorers and identity records.
It accepts final-only snapshots (`paired=False`); a paired snapshot reports
`unsupported_snapshot_scope`. It emits exact five-dimension scores/masks without resource,
human or mechanism penalties. Exit 0 means processing completed, not a passing itinerary
or available total; correction exits 2. `--generated-at` defaults to current UTC;
freeze it with the inputs for reproducible report content.

Usage envelopes come from opt-in [request-local capture](../app/observability/USAGE.md),
not automatic CLI/API collection. `compare_usage` keeps scopes/namespaces and missing
measurements explicit. Its CLI prints a descriptive report; invalid envelopes raise an
input error rather than partial comparisons. It adds no billing claim or quality penalty.

<a id="transport-responsibility-correction---2026-09-30"></a>
<a id="ticket-09-local-blinded-ranking-workflow"></a>

### Local blinded ranking

```powershell
npm --prefix frontend run build:blind-review
.venv/Scripts/python.exe -m backend.evaluation.human_cli prepare manifest.json selection.json --out preparation.json
.venv/Scripts/python.exe -m backend.evaluation.human_cli package manifest.json selection.json display-review.json --out public-review --private-out private-mapping.json --renderer-js frontend/dist-blind-review/review.js --renderer-css frontend/dist-blind-review/review.css
.venv/Scripts/python.exe -m backend.evaluation.human_cli import public-review/presentation.json private-mapping.json answers.json --out imported-revisions.json
.venv/Scripts/python.exe -m backend.evaluation.human_cli report public-review/presentation.json private-mapping.json answers.json --generated-at 2026-10-03T00:00:00Z --out human-report.json
```

Prepare and independently review display material before packaging. Deliver only
`review.html` and `presentation.json`; retain preparation, display review and private
mapping outside the public directory. Open `review.html` directly in a local browser.
The package needs no account, server, CDN or submission endpoint. Use synthetic material
for development; real assessment needs separate approval. Successful processing exits 0;
invalid material or output conflicts exit 2. Import/report can take multiple answer files.

The current renderer provides IANA zone selection and HH:mm clocks, labelled Inferred
arrival, drafts, submitted revision recovery, JSON download/import and confirmed Clear
answers. It hides Original timestamp controls and dedicated uncertainty/item/time-warning
hints; frozen material retains uncertainty. Clear only erases this package/rater's local
answer history. Download a backup first; researcher-held old revisions remain records.
The [human contract](../../docs/contracts/0005-quality-human-review.md#human) owns exact
answer, blinding and display semantics. Automated DOM checks do not prove native file://
storage behavior; the [acceptance record](../../docs/records/evaluation/blinded-ranking-record.md)
distinguishes automated checks from user-reported browser acceptance.

### V3 paired diagnostics

```powershell
.venv/Scripts/python.exe -m backend.evaluation.v3_pair_cli prepare manifest.json identity-report.json > edit-provenance.json
.venv/Scripts/python.exe -m backend.evaluation.v3_pair_cli report manifest.json identity-report.json paired-evidence-snapshot --context schedule-context.json --route-reviews route-reviews.json --coordinates coordinates.json --expected-plan paired-evidence-plan.json --edit-provenance edit-provenance.json --generated-at 2026-10-03T00:00:00Z > v3-pair-report.json
```

Prepare the current identity replay and frozen evidence plan with `--paired`. Save
stdout JSON as UTF-8. The commands read the original selected V3 result bytes
automatically; `--edit-provenance`
is optional and, when supplied, is checked against a fresh source replay. Additional
report options are `--occupancy-reviews`, `--correspondence-reviews` and
`--identity-snapshot` (as an alternative to `--coordinates`). No provider/model/database
call or input modification occurs. The snapshot argument can be omitted when no group
has an available pair; supplied snapshots are still verified.

Library seams are `read_v3_result_sources`, `prepare_v3_correspondence` and
`build_v3_pair_report`. Original adopted edit/fragment sources establish occurrence
lineage, independent identities establish venue continuity, and the scorers establish
quality. The report retains local uncertainty, pair availability, exact signed deltas,
losses/replacements, route topology/context and independent conflict transitions.
Its pair mask/auxiliary totals remain separate from Ticket 08's four-final report.
Exit 0 means complete processing, including unavailable pairs and FAIL/UNKNOWN checks;
corrupt/stale material exits 2. See the [paired contract](../../docs/contracts/0005-quality-human-review.md#v3-pairs).

## Verification and status boundary

Relevant regression tests live in `backend/tests/evaluation/`
and the [blind-review frontend](../../frontend/src/features/blind-review/BlindReview.tsx).
Actual historical results are in [evaluation record index](../../docs/records/README.md)
and linked Issues. Synthetic checks do not establish real provider availability,
formal benchmark outcomes or a version freeze. Formal controlled-case construction/execution
and Ticket 12 mechanism/official-evidence work remain separately authorized.

## Controlled V3 offline workflow

Run from the repository root with the existing Python environment. Commands emit JSON;
save artifacts as UTF-8 without BOM. Exit 0 means successful processing, including quality
FAIL/UNKNOWN outcomes; material/execution errors exit 2. Cases are supplied frozen
post-primary inputs, not ordinary planner captures automatically upgraded into runnable
cases. See the [case and review wire](../../docs/contracts/0001-evaluation-artifacts.md#controlled-executable-wire).
Use a dedicated offline process with an exclusive event loop and no other network work;
execute cases serially. The guard patches sockets and the loop clock. Do not embed this
executor in an active web-service event loop or run unrelated async tasks alongside it.

```text
python -m backend.evaluation.controlled_cli replay case.json
python -m backend.evaluation.controlled_cli prepare case.json execution.json requirements.json
python -m backend.evaluation.controlled_cli identity-references preparation.json
python -m backend.evaluation.controlled_cli identity-plan preparation.json
python -m backend.evaluation.controlled_cli identity preparation.json observations.json audit.json --reviews identity-reviews.json
python -m backend.evaluation.controlled_cli evidence-plan preparation.json identity.json --context context.json --route-reviews route-reviews.json --coordinates coordinates.json
python -m backend.evaluation.controlled_cli report case.json execution.json requirements.json expectations.json identity.json snapshot --context context.json --route-reviews route-reviews.json --coordinates coordinates.json --expected-plan plan.json --generated-at 2026-10-04T00:00:00Z
python -m backend.evaluation.controlled_cli batch controlled-batch.json --generated-at 2026-10-04T00:00:00Z
```

The evidence-plan command emits a route preparation containing `evidence_plan`; save that
plan separately for snapshot acquisition/verification. Collection remains the existing
injected-transport `acquire_snapshot` API and requires its own authorization if live.
The saved-snapshot replay and identity-evidence commands remain in `snapshot_cli`.
Independent identity observations, positive-count audit plan, schedule context, coordinates,
requirements and review material retain their existing schemas. No four-version manifest
is required for these controlled commands.

Both evidence preparation and reporting accept `--occupancy-reviews`. Reporting additionally
accepts `--correspondence-reviews` and `--factual-reviews` for separately linked human facts.
The raw Ticket 10 pair remains in `pair`; supplemental check outcomes remain in
`reviewed_checks`, with original scores/deltas untouched. A route fact may establish duration
compliance while a transfer commitment remains unknown; review occupancy through its own
source-backed channel rather than treating the route fact as a whole-itinerary PASS.

An expectations guard for an independently reviewed exact-one-visit requirement can be:

```json
{
  "goal_id": "one-visit-on-day",
  "basis": "explicit_requirement",
  "condition": {"kind": "daily_count", "date": "2026-09-26", "minimum": 1, "maximum": 1},
  "source": {"field": "additional_preferences", "quote": "Exactly one primary visit on this day."}
}
```

Place this in the reviewed expectations envelope's `guards` array and bind the envelope
to the emitted normalized `case_hash`. The quote must be present in that original request.
Such a guard is independent of the planner's interpreted requirements: a missed interpretation
can cause an internally adopted addition to be independently classified as regression.
Ordinary additions with supported new checks and preserved requirements are lawful changes.

Controlled batch manifests reference previously emitted reports with the standard relative
JSON artifact envelope (`path`, byte `sha256`, schema, media type and availability). Every
entry declares `case_id`, `role` and `expected_goal_ids`. Missing or invalid reports remain
unavailable inventory units. Counts describe submitted cases; no formal 32-case corpus,
live usage/cost measurement, version ranking or causal conclusion is produced.
