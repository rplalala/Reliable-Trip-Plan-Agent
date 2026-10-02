# Ticket 09 implementation acceptance

## Current clearing-enabled acceptance - 2026-10-02

The user confirmed native display/time-zone and narrow-window checklist items 1-2
on public-no-hints, then requested Clear answers to test item 3. The
[clearing addition](ticket-09-clear-answers.md) commits implementation at 3a2e3d9
before review, followed by separate pending-import P2 fix d514508. Final frontend
98 passed / 13 files in 32.64s; TypeScript/blind build/lint passed. Both final review
axes are clear. Source/public bytes/mapping and answer/report schemas remain unchanged.
Current ignored renderer: artifacts/rtpeval/ticket09/public-clear-answers-final/review.html.
Submit/refresh/download/clear/refresh/reimport and a brief updated-display check still
require the user; Issue #21 and parent #12 remain open. Earlier sections are history.

## Latest scoped acceptance - 2026-10-02

At clean base 290ef20 the user requested acceptance. The
[scoped recheck](ticket-09-final-acceptance.md) records 11 frontend tests passed,
initial backend temporary-directory permission setup failures, then the same 26
backend tests passed with an isolated workspace temporary root and inaccessible cache
disabled. Exact package/private/source/asset linkage and actual synthetic CLI import/
report checks passed. No application code changed. Full native browser acceptance
still awaits the user's direct-file/zone/narrow-window/refresh/JSON checklist result;
Issue #21 and parent #12 stay open. Earlier sections retain their observed sequence.

## Current consolidated status - 2026-10-02

Documentation checkpoint: b232ae0 on feature/evaluation, initially clean tree/index;
this update changes documentation and tracker summaries only. Implementation and
offline review are complete; full native browser acceptance is pending. Issue #21
and parent #12 remain open. Sections below preserve their original observed sequence;
their earlier display rules/packages are superseded by the current checkpoint.

Current display: UTC-default IANA selector, converted dates and 24-hour HH:mm clocks;
no Original timestamp controls, dedicated Uncertainty/unknowns fields, item notices or
time-warning text. Inferred arrival labels, ordinary source notes/preferences and
duration basis remain. Unknown-zone clocks stay local, invalid values stay raw and
missing values display Not supplied. Original source/public/private data, hashes,
answer revisions, reports and V0-V3 behavior are unchanged.

Latest implementation f1f0cc0 precedes independent Standards/Spec reviews, both clear.
The selected hint-removal regression first failed (1 failed / 7 not selected); the
correction passed the full frontend suite (94 passed / 13 files in 25.49s), TypeScript,
blind-review build and lint. Earlier backend 2299 passed / 10 skipped / zero deselections
in 150.85s remains a separate gate; nine database opt-ins and one symlink case were
not supplemented for Ticket 09. No implementation tests are rerun for this docs update.
Detailed later display history is in [time-zone acceptance](ticket-09-timezone-display.md),
[timestamp cleanup](ticket-09-display-cleanup.md) and
[hint removal](ticket-09-uncertainty-display.md).

Current ignored synthetic renderer: artifacts/rtpeval/ticket09/public-no-hints/review.html;
validation-no-hints.json links renderer hashes to f1f0cc0 and preserves pending browser
status. Remaining manual checks cover direct-file display/time-zone switching, narrow
layout, submit/save/refresh recovery and JSON download/reimport. Static/jsdom checks
and the user's cropped screenshot do not establish that full acceptance. No push,
live/native supplement, real rater session, formal comparison, freeze or Ticket 10+ work.

## Original implementation checkpoint

Date: 2026-10-02, Australia/Sydney. Review base:
`541c684a4ae58001b513a9508b65a1d99507b0bf`, branch `feature/evaluation`.
Initial worktree/index were clean. The user explicitly approved implementation within
[preflight](ticket-09-preflight.md), local commits and no push. Status at this checkpoint:
implemented offline interfaces and renderer; final offline regressions/review complete;
actual file:// visual/persistence/export/import acceptance pending human verification.

## Scope and behavior

- `human_tasks` prepares exact source-linked prospective display material, requires
  complete researcher review and manual redaction/legitimate-name flag decisions,
  then re-reads original byte/hash-linked artifacts to build separate public/private data.
  Original Input and travel facts/uncertainty survive; Nearby, source IDs, provider badges,
  planner findings and automatic scores are excluded. Source authority remains V0
  transport Activities and V1-V3 Transfers. Unbound claims stay visible; timing-consistent
  duplicate transfers merge distinct meaningful fields, conflicts remain alternatives.
- Missing source arrivals may show explicitly labelled departure-plus-duration inference,
  with missing-source notice. No reserve, provider query, inferred zone, scorer claim or
  source mutation. Invalid/missing/date-only operands leave inference unavailable.
- Config supplies opaque public identifiers, seed, explicit task order and duplicate
  references/minimum spacing. Shuffled Latin blocks balance all shown version/label
  positions to maximum-minus-minimum at most one; actual mapping and separate main/
  duplicate/combined position counts remain private. No study/sample quota is hardcoded.
- `human_answers` rejects invalid whole bundles, stale linkage, nonpartitioned submitted
  ranks and conflicting same-revision content. Ties, unable-to-judge, N/A and incomplete
  drafts remain distinct. Idempotent imports retain history; latest complete submitted
  revision is effective independently of import order and later drafts.
- `human_report` joins the frozen private mapping after validation, exports six correlated
  pair outcomes, available denominators/missingness and version-based duplicate consistency.
  Duplicates do not add main-result weight; empty comparability yields null agreement.
  No quality total, inferential statistic or automatic-score integration.
- `human_cli` separates preparation, public package/private mapping delivery, import and
  report. Public output is anonymous JSON plus one HTML file embedding isolated React
  assets. Source text is inert escaped JSON/text; CSP prevents network/remote assets.
  Existing output paths are refused, and private mapping must stay outside public output.
- Independent React UI supports rank positions/ties, alternate response states, drafts,
  correction submissions, best-effort local storage and explicit JSON download/import.
  Save/restore failures are visible. The user saves drafts before changing tasks; browser
  storage is not the only backup. Product routes and backend planner/scorer code are unchanged.

## Actual red/green sequence

New package, answer, report, CLI and renderer boundary tests first failed for missing
modules/components, then passed after their corresponding implementation slices.
Subsequent behavior tests exposed missing free-text leakage blocking, fixed label
assignments/invalid duplicate acceptance, omitted unbound transfers and duplicate journey
rows. Source-linked redaction, seeded balancing/selection checks, source-authoritative
transport display and meaningful-field merging corrected these observed failures.
An additional date-only departure test failed because Python accepted the date as midnight;
the inferred-arrival boundary now requires an actual supplied clock. Its retest passed.
An endpoint-display check then exposed missing readable referenced destination text;
the renderer now preserves source-referenced names without exposing endpoint IDs.

Frontend's first attempt could not write Vite's temporary bundled config under the
sandbox. Authorized test retry outside that filesystem restriction reached the expected
missing-component red failure; renderer implementation then passed. This is environment
permission handling, not an approval-review rejection or a frontend behavior defect.
Ruff initially found formatting and imported-fixture redefinition issues. Formatting and
the existing pytest_plugins fixture convention corrected them; relevant Ruff passed.

Pre-review dedicated backend checks: 25 passed in 2.81s. Earlier combined new checks plus
intake: 80 passed / 1 host symlink skip before the additional date-only test. Dedicated
frontend: 5 passed across two files. Independent TypeScript/static build and frontend
lint passed; backend evaluation Ruff and compilation passed. Initial full backend gate:
2298 passed / 10 skipped in 152.33s. After readable endpoint display, full retest:
2298 passed / 10 skipped in 148.80s. Pre-review full frontend: 88 passed in 27.33s;
both blind and product static builds and lint passed. Counts describe separate runs.
No database/native/live supplement was run.

## Browser boundary and remaining acceptance

Generated four-task synthetic package/private mapping and source/config/review records
at ignored `artifacts/rtpeval/ticket09/`; no real study material or rating was generated.
Browser Use rejected file:// navigation because only http/https protocols are allowed
and forbade circumvention. No alternate browser, raw protocol, local-server workaround
or security setting change was attempted. User manual checks requested: direct local
display (including inferred arrival), narrow layout, submission/refresh restoration and
JSON download/reimport. This remains missing evidence until the user reports results.
Automated jsdom interaction/build checks do not establish actual file:// browser behavior.
After the review correction, regenerated the final synthetic package at
`artifacts/rtpeval/ticket09/public-final/review.html` with a distinct presentation identity/
revision, plus private-final mapping/config/review and validation.json outside the public
directory. Final public JSON metadata-key inspection passed. Renderer asset hashes and
presentation hash are retained in ignored validation.json. Earlier synthetic material
remains unchanged, and its browser check request is superseded by the final package request.

## Commit/review and boundaries

Implementation/direct tests were committed before both review axes:

- `6095877` — feat: prepare blinded ranking packages and revision-aware reports.
- `d36b52d` — feat: add standalone offline blinded review interface.
- `5f43b5d` — fix: normalize anonymous transport display and source aliases.
- `4be6e01` — chore: format blinded package renderer (quote formatting only).

Standards reviewed 541c684...d36b52d: zero documented breaches and zero actionable
heuristic smells. Spec found one P1: V0 traffic Activity/Start/End versus Transfer/
Departure/Arrival and provider_duration_seconds exposed source representation. Root's
post-commit audit independently reproduced this with a failing neutral-shape test.
The separate fix emits common travel/departure/arrival/duration_seconds display fields
and adds explicit private source_batch alias linkage. It preserves original wording,
uncertainty and source pointers; no raw claim is rewritten. A React regression verifies
the neutral heading and explicitly labelled inference. Both reviewers rechecked
d36b52d...5f43b5d: P1 resolved; zero residual Standards or Spec findings.

Post-fix relevant backend plus intake: 82 passed / 1 host symlink skip in 6.20s;
new dedicated backend: 26 passed in 3.02s. Dedicated frontend: 6 passed. Final committed
post-review full backend: **2299 passed / 10 skipped in 150.85s**, zero deselections.
Final full frontend: **89 passed in 25.46s**; blind/product builds and lint passed.
Nine database opt-ins and one native symlink check remain skipped; no supplements.
Ruff, compilation and CLI checks passed. No repeated full gate is inferred from earlier
passing checkpoints; final numbers are the actual post-fix runs.

A final format check found two quote-style differences in human_cli.py. Ruff formatting
corrected them without changing generated content. The first CLI-only retest encountered
two setup errors because the default host temporary directory was inaccessible; using
an explicit workspace basetemp and disabling the inaccessible pytest cache passed both
CLI tests in 0.42s. All eight new Python files then passed Ruff format checking.
This formatting-only commit did not require another full behavior regression.

Final documentation/tracker closeout preserves pending manual browser acceptance.
Eight English document files and 207 local Markdown target occurrences passed checks;
backend Ruff, evaluation compilation, CLI help and diff whitespace checks passed.
The backend/app and scripts diff against the implementation review base is empty.
Tracker #21/#12 writes and independent exact-body/open-state/label verification passed;
the first three implementation criteria are checked, while browser-dependent save/
restore/backup and report/visual criteria remain unchecked. Detailed tracker actions
are preserved in ticket-09-tracker-update.md. The ignored development archive records
accepted boundaries, observed failures/corrections and missing browser evidence.
No amend, squash or push occurred. Issue #21 must remain open until that evidence is
supplied; functional implementation/automated checks do not complete the visual gate.
V0-V3 independent paths, planner budgets, scored transport policy and automatic quality
reports remain unchanged. No formal comparison, real rater session, recruitment, live
acquisition, version freeze or Ticket 10+ work is authorized.

## Subsequently approved time-zone display extension

The user requested and approved an IANA-zone dropdown, default UTC, with converted
dates and 24-hour HH-mm clocks. Source day grouping and inspectable timestamps remain;
missing zones are never guessed, invalid values retain explicit uncertainty, and
presentation/mapping/source/answer/scorer data remain unchanged. Current extension
scope and actual red/green/gate/review evidence are recorded separately in
[time-zone display](ticket-09-timezone-display.md), review base dfe2695, implementation
f600315. The initial 89-test frontend gate above remains a distinct historical run;
extension final post-fix full frontend passed 94 tests across 13 files with builds/lint.
No backend regression or live/native supplement was repeated for this UI-only change.
New ignored synthetic public-timezone-final/review.html supersedes public-final for the
remaining browser gate, with unchanged public JSON bytes/presentation hash/private
mapping and separately retained renderer hashes. No actual browser pass is claimed.
Spec's compact-offset omission was fixed separately at 29df5fd; both review rechecks
have zero residual findings. Detailed red/green and separate gate counts remain in
the extension record; no earlier checkpoint is rewritten as a post-fix pass.

## Subsequent user display cleanup and HH:mm correction

[Cleanup acceptance](ticket-09-display-cleanup.md) records explicit removal of the
Original timestamp control and the subsequent HH:mm format correction. Removal at
6725071 and formatting at 7809b33 were independently committed before their reviews;
Standards and Spec are clear on both. Removal regression first failed for two surviving
controls; format regression first failed for the old dash clock. Separate actual full
frontend gates passed 94/13 files in 38.28s and then 36.49s; final TypeScript, blind
build and lint passed. No backend or product-route behavior changed.
Current ignored synthetic public-display-final/review.html supersedes previous packages
for pending manual browser acceptance. Source bytes/hashes, public/mapping and answers
are unchanged. Source travel uncertainty and the distinct inferred-arrival notice remain;
the screenshot is not full visual/resume/export/import evidence. Issue #21 remains open.

## Subsequent explicit uncertainty-hint removal

[Current display acceptance](ticket-09-uncertainty-display.md) records the user's request
to hide dedicated unknowns/item/time-warning hints. Source JSON and ordinary notes,
inference labels, times and answers remain. The selected UI regression first failed
because Uncertainty still rendered; final full frontend 94 passed / 13 files in 25.49s,
TypeScript/blind build/lint passed. f1f0cc0 precedes independent clear Standards/Spec
reviews. Current ignored public-no-hints/review.html supersedes earlier examples;
actual complete file:// browser acceptance remains pending. No new backend/live run.
