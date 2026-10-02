# Independent evaluation package

Tickets 01-09 are implemented for explicitly submitted immutable material and offline
development validation. Tickets 10-12 remain unimplemented. This package does not run
planners, construct a benchmark or perform formal comparative research.
[Evaluation architecture](../../docs/0006-independent-evaluation.md) owns scope.

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
Use that plan directly, or put the context array under `{"contexts": [...]}` in
`route-contexts.json` for the snapshot planning CLI; the full preparation report is not
that CLI input. `--expected-plan` optionally enforces trusted full-plan equality.

Library seams: `score_requirement_schedule`, `prepare_routes`, `score_opening`, and
`score_routes`. These and identity/snapshot plan commands support `--paired` where
declared, selecting available V3 draft/final-primary projections; paired scope must
remain consistent across inputs. This is not implemented Ticket 10 correspondence or
Repair delta reporting. Scorers exit 0 for complete processing, including FAIL/UNKNOWN,
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

## Verification and status boundary

Relevant regression tests live in `backend/tests/evaluation/`
and the [blind-review frontend](../../frontend/src/features/blind-review/BlindReview.tsx).
Actual historical results are in [evaluation record index](../../docs/records/README.md)
and linked Issues. Synthetic checks do not establish real provider availability,
formal benchmark outcomes or a version freeze. Before/after reporting, controlled
Repair and mechanism/official-evidence analysis remain the separately scoped Tickets 10-12.
