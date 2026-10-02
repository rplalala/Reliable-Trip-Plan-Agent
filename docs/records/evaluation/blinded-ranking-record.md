# Blinded Ranking Record

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="rtpeval-ticket-09-acceptance"></a>

<a id="rtpeval-ticket-09-acceptance--ticket-09-implementation-acceptance"></a>

## Ticket 09 implementation acceptance

<a id="rtpeval-ticket-09-acceptance--completed-acceptance---2026-10-02"></a>

### Completed acceptance - 2026-10-02

At clean documentation base ff00057, the user reported the third browser checklist
item passed after receiving public-clear-answers-final/review.html. Together with
previous user-confirmed display/time-zone and narrow-window items 1-2, this completes
native development acceptance. Evidence is explicit user reports, not independent
browser tool observation; file:// restrictions were never circumvented.

The [clearing addition](blinded-ranking-record.md#rtpeval-ticket-09-clear-answers) commits implementation at 3a2e3d9
before review, followed by separate pending-import P2 fix d514508. Final frontend
98 passed / 13 files in 32.64s; TypeScript/blind build/lint passed; both final review
axes are clear. Earlier backend full and scoped package/CLI checks remain separate
retained evidence. No new implementation test run for this documentation closeout.
Source/public bytes/mapping, answer/report schemas and V0-V3 paths remain unchanged.

Current accepted synthetic renderer: artifacts/rtpeval/ticket09/public-clear-answers-final/review.html.
Issue #21 is closed/completed; parent #12 marks 01-09 completed and remains open for
10-12. Local commits remain unpublished. No real rater, formal comparison, live service/
native test supplement, push, freeze or later-ticket implementation is included.
Earlier incomplete/no-result sections below preserve their historical checkpoints.

<a id="rtpeval-ticket-09-acceptance--latest-scoped-acceptance---2026-10-02"></a>

### Latest scoped acceptance - 2026-10-02

At clean base 290ef20 the user requested acceptance. The
[scoped recheck](blinded-ranking-record.md#rtpeval-ticket-09-final-acceptance) records 11 frontend tests passed,
initial backend temporary-directory permission setup failures, then the same 26
backend tests passed with an isolated workspace temporary root and inaccessible cache
disabled. Exact package/private/source/asset linkage and actual synthetic CLI import/
report checks passed. No application code changed. Full native browser acceptance
still awaits the user's direct-file/zone/narrow-window/refresh/JSON checklist result;
Issue #21 and parent #12 stay open. Earlier sections retain their observed sequence.

<a id="rtpeval-ticket-09-acceptance--current-consolidated-status---2026-10-02"></a>

### Current consolidated status - 2026-10-02

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
Detailed later display history is in [time-zone acceptance](blinded-ranking-record.md#rtpeval-ticket-09-timezone-display),
[timestamp cleanup](blinded-ranking-record.md#rtpeval-ticket-09-display-cleanup) and
[hint removal](blinded-ranking-record.md#rtpeval-ticket-09-uncertainty-display).

Current ignored synthetic renderer: artifacts/rtpeval/ticket09/public-no-hints/review.html;
validation-no-hints.json links renderer hashes to f1f0cc0 and preserves pending browser
status. Remaining manual checks cover direct-file display/time-zone switching, narrow
layout, submit/save/refresh recovery and JSON download/reimport. Static/jsdom checks
and the user's cropped screenshot do not establish that full acceptance. No push,
live/native supplement, real rater session, formal comparison, freeze or Ticket 10+ work.

<a id="rtpeval-ticket-09-acceptance--original-implementation-checkpoint"></a>

### Original implementation checkpoint

Date: 2026-10-02, Australia/Sydney. Review base:
`541c684a4ae58001b513a9508b65a1d99507b0bf`, branch `feature/evaluation`.
Initial worktree/index were clean. The user explicitly approved implementation within
[preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21#issuecomment-5955704071), local commits and no push. Status at this checkpoint:
implemented offline interfaces and renderer; final offline regressions/review complete;
actual file:// visual/persistence/export/import acceptance pending human verification.

<a id="rtpeval-ticket-09-acceptance--scope-and-behavior"></a>

### Scope and behavior

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

<a id="rtpeval-ticket-09-acceptance--actual-redgreen-sequence"></a>

### Actual red/green sequence

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

<a id="rtpeval-ticket-09-acceptance--browser-boundary-and-remaining-acceptance"></a>

### Browser boundary and remaining acceptance

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

<a id="rtpeval-ticket-09-acceptance--commitreview-and-boundaries"></a>

### Commit/review and boundaries

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

<a id="rtpeval-ticket-09-acceptance--subsequently-approved-time-zone-display-extension"></a>

### Subsequently approved time-zone display extension

The user requested and approved an IANA-zone dropdown, default UTC, with converted
dates and 24-hour HH-mm clocks. Source day grouping and inspectable timestamps remain;
missing zones are never guessed, invalid values retain explicit uncertainty, and
presentation/mapping/source/answer/scorer data remain unchanged. Current extension
scope and actual red/green/gate/review evidence are recorded separately in
[time-zone display](blinded-ranking-record.md#rtpeval-ticket-09-timezone-display), review base dfe2695, implementation
f600315. The initial 89-test frontend gate above remains a distinct historical run;
extension final post-fix full frontend passed 94 tests across 13 files with builds/lint.
No backend regression or live/native supplement was repeated for this UI-only change.
New ignored synthetic public-timezone-final/review.html supersedes public-final for the
remaining browser gate, with unchanged public JSON bytes/presentation hash/private
mapping and separately retained renderer hashes. No actual browser pass is claimed.
Spec's compact-offset omission was fixed separately at 29df5fd; both review rechecks
have zero residual findings. Detailed red/green and separate gate counts remain in
the extension record; no earlier checkpoint is rewritten as a post-fix pass.

<a id="rtpeval-ticket-09-acceptance--subsequent-user-display-cleanup-and-hhmm-correction"></a>

### Subsequent user display cleanup and HH:mm correction

[Cleanup acceptance](blinded-ranking-record.md#rtpeval-ticket-09-display-cleanup) records explicit removal of the
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

<a id="rtpeval-ticket-09-acceptance--subsequent-explicit-uncertainty-hint-removal"></a>

### Subsequent explicit uncertainty-hint removal

[Current display acceptance](blinded-ranking-record.md#rtpeval-ticket-09-uncertainty-display) records the user's request
to hide dedicated unknowns/item/time-warning hints. Source JSON and ordinary notes,
inference labels, times and answers remain. The selected UI regression first failed
because Uncertainty still rendered; final full frontend 94 passed / 13 files in 25.49s,
TypeScript/blind build/lint passed. f1f0cc0 precedes independent clear Standards/Spec
reviews. Current ignored public-no-hints/review.html supersedes earlier examples;
actual complete file:// browser acceptance remains pending. No new backend/live run.

<a id="rtpeval-ticket-09-clear-answers"></a>

<a id="rtpeval-ticket-09-clear-answers--ticket-09-local-answer-clearing"></a>

## Ticket 09 local answer clearing

Date: 2026-10-02, Australia/Sydney. Review base cbb716a2d0995bcbe062e09c0e07489d87b791f1,
feature/evaluation, clean initial tree/index. The user confirmed browser checklist
items 1-2 and requested a clear button to test item 3. This authorizes a narrow
BlindReview UI addition, existing React user-operation seam tests and local commits;
no push, live provider, real rater or later-ticket work.

Provide Clear answers with an explicit confirmation that it clears all saved answers,
drafts and revisions for the current frozen review package/rater in this browser.
Cancel preserves saved data and unsaved form edits. Confirm writes an empty answer
bundle only to the existing current-package storage key, then clears in-memory answers
and form, returns to the first task and removes submitted indicators. Other packages,
time-zone view preference, presentation/source/private mapping, downloaded backups and
researcher import/report data remain unchanged. Storage failure retains current answers,
form and task, shows a visible error and keeps JSON download available. Existing valid
JSON backups can be imported after clearing, restoring original revisions normally.
Reset starts a new local session; downloaded/submitted external revision history is not
erased, and conflicting same-number revisions still require existing import validation.

Use TDD on the existing public BlindReview interaction/persistence boundary: cancel/
confirm/reload and cross-package isolation, storage failure, and JSON recovery. Run full
frontend tests, TypeScript/blind-review build/lint. Commit implementation/direct tests
before independent Standards and Spec review; corrections use separate commits. Create
a new ignored synthetic renderer with unchanged presentation bytes/mapping. Native
browser item 3, and a brief confirmation that the updated renderer retains items 1-2,
remain pending the user. No file:// workaround or actual browser pass is inferred.

<a id="rtpeval-ticket-09-clear-answers--pre-review-validation"></a>

### Pre-review validation

First confirmation/reset interaction regression failed because Clear answers was
absent (1 failed / 8 not selected, 3.70s); minimal UI implementation made it pass
(1 passed / 8 not selected, 2.57s). Additional external-boundary checks cover storage
failure preserving answers/unsaved form and actual downloaded-Blob JSON reimport
restoring draft/submitted revision history. BlindReview file: 11 passed in 5.71s.
Full frontend: 97 passed / 13 files in 28.31s. TypeScript via blind-review build and
lint passed. No new backend run is claimed for this frontend-only addition. Earlier
scoped backend 26-pass and native user-reported items 1-2 remain separate evidence.
Implementation/direct tests and this accepted scope are committed before dual review;
review outcomes and final regenerated renderer will be recorded afterward.

<a id="rtpeval-ticket-09-clear-answers--initial-committed-review-and-correction"></a>

### Initial committed review and correction

Implementation/direct tests committed at 3a2e3d9 before review. Standards reported
zero documented breaches/actionable heuristics. Spec reported one P2: pending
FileReader import could complete after a confirmed clear and re-persist old answers.
The delayed-import regression reproduced this (1 failed / 11 not selected, 2.46s).
A local import generation increments only after successful empty-bundle persistence;
earlier read successes/errors are ignored afterward. Failed or canceled clears do
not invalidate imports. Selected regression passed (1 passed / 11 not selected, 2.59s).
This is a required clearing-correctness fix, not a general import redesign.

<a id="rtpeval-ticket-09-clear-answers--final-committed-rechecks-and-package"></a>

### Final committed rechecks and package

d514508 commits the delayed-import correction and direct regression separately.
Post-fix full frontend: **98 passed / 13 files in 32.64s**; TypeScript via blind-review
build and lint passed. Standards recheck: zero documented breaches/actionable
heuristics. Spec recheck: original P2 resolved, zero remaining findings; reviews
were read-only and did not independently rerun the suite.

Current ignored synthetic renderer: artifacts/rtpeval/ticket09/public-clear-answers-final/
review.html. validation-clear-answers-final.json records code/asset hashes, unchanged
public JSON bytes and valid existing private mapping. Older renderer packages remain
historical. User-confirmed display/time-zone/narrow-window items 1-2 apply to the
previous public-no-hints package; the new button and final item 3 still need native
checking on this updated renderer. No tool file:// workaround or completed gate is
claimed; Issue #21 and parent #12 remain open.

Final closeout checks passed: seven English documentation files, 198 local Markdown
target occurrences, final generated package/public-byte/asset-hash/CSP checks, approved
source scope and diff whitespace. Issue #21/#12 exact-body/open-state/unchanged-label/
comment/history checks passed. No pending native-check result is inferred from these
checks; final documentation is a separate local commit without generated/ignored data.

<a id="rtpeval-ticket-09-clear-answers--user-confirmed-completion---2026-10-02"></a>

### User-confirmed completion - 2026-10-02

At clean documentation base ff00057, the user explicitly reported checklist item 3
passed after receiving the final clearing-enabled renderer. Earlier reports confirmed
items 1-2. The accepted recovery sequence is submission/refresh, JSON download,
confirmed clear/blank refresh and JSON reimport restoring answers/revisions. Combined
with retained offline gates and clear Standards/Spec rechecks, Ticket 09 acceptance
is complete. Native observations are user reports; no independent tool browser pass
or additional test run is claimed. Previous pending statements remain their original
checkpoints. Issue #21 closed/completed, parent #12 marks 01-09 completed and stays
open for 10-12; source commits/documents remain local/unpublished, no push or freeze.

<a id="rtpeval-ticket-09-display-cleanup"></a>

<a id="rtpeval-ticket-09-display-cleanup--ticket-09-user-requested-timestamp-control-removal"></a>

## Ticket 09 user-requested timestamp control removal

Date: 2026-10-02, Australia/Sydney. Review base:
4c9d57218b3c200fc76690a7b8c47f38e2b3c2e4, feature/evaluation; initial tree/index clean.
The user explicitly requested removal of Original timestamp and asked what the
uncertainty/inferred-arrival notices in the screenshot mean. This narrow UI correction
is authorized by that request and overrides the prior inspectable-timestamp UI rule.
Approved local-commit/no-push policy and existing BlindReview React test seam apply.

Remove Original timestamp controls, related page instructions and unused styles.
Keep UTC-default IANA dropdown, converted dates/HH-mm clocks, source-day grouping,
unknown-zone/invalid-time handling and source uncertainty/inferred-arrival notices.
Original source/public/private JSON bytes and hashes, answers, scoring and V0-V3 paths
remain unchanged. Missing/invalid time values still retain their explicit original
value when no conversion is possible; removal concerns the optional timestamp control,
not suppression of malformed source evidence.

Explain in chat that source Travel time uncertain describes uncertain travel duration,
while the inferred-arrival notice describes a missing source arrival supplemented by
departure-plus-duration display arithmetic. These can coexist; no actual arrival is
verified by arithmetic. No wording or factual claim in either notice is changed.

Validate via the existing React seam: converted compact/hour-only offset timestamps
remain correct, and neither the control nor its raw valid ISO strings are displayed.
Run full frontend tests, TypeScript, isolated build and lint; commit implementation/
direct tests before Standards/Spec review, then document actual results and regenerate
a separate synthetic package. Actual file:// browser acceptance remains pending; no
browser policy workaround, live/native run, formal comparison or later ticket is included.

<a id="rtpeval-ticket-09-display-cleanup--actual-validation-and-review"></a>

### Actual validation and review

Updated existing UI regression first failed (1 failed/7 passed): two Original timestamp
controls still rendered. Removed controls, helper instruction and unused CSS. Final
full frontend: 94 passed across 13 files in 38.28s; TypeScript, blind build and lint
passed. The same regression verifies compact/hour-only offset conversion remains
correct without exposing valid raw ISO strings. No backend or product-route change.
Implementation/direct tests and this scope record are committed before review;
review and final package evidence will be appended at their actual checkpoints.

<a id="rtpeval-ticket-09-display-cleanup--subsequent-user-clock-format-correction"></a>

### Subsequent user clock-format correction

During closeout, the user explicitly corrected the desired clock format to HH:mm.
This supersedes the earlier HH-mm request for current display. Use colon-separated
24-hour clocks for converted timestamps and valid missing-zone local clocks; retain
dates, source grouping, uncertainty, parsing and Original timestamp removal. Original
source strings, artifacts, answer schemas and scoring remain unchanged. The existing
UI test's expected literals were updated; the selected inferred-arrival regression
first failed for 10:30 because the UI still displayed 10-30 (1 failed, 7 not selected).
The renderer and its instruction now use HH:mm. Actual final results will be recorded
after validation; the earlier 94-test removal gate is a separate checkpoint.

Original timestamp removal commit 6725071 received independent Standards/Spec reviews:
zero documented/actionable Standards findings and zero Spec findings. The Spec reviewer
independently checked converted offsets, missing zones, invalid values and removed raw
valid strings; no full-test rerun or browser acceptance by reviewers is claimed.
After the user format correction, final full frontend: 94 passed / 13 files in 36.49s.
TypeScript, final blind build and lint passed. The format change/direct expected literals
and this accepted correction record are committed separately before its final review.

<a id="rtpeval-ticket-09-display-cleanup--final-local-closeout-checkpoint"></a>

### Final local closeout checkpoint

7809b33 (fix: display blinded review times as HH:mm) preserves the user's format
correction as a separate commit after 6725071 (fix: remove original timestamp controls
from blinded review). Both Standards and Spec reviewed 6725071...7809b33 and report
zero residual findings. Spec independently rendered converted/local clocks, missing
zones, invalid values and removed controls; no full test or browser pass is inferred.

Generated ignored artifacts/rtpeval/ticket09/public-display-final/review.html from final
assets; validation-display-final.json records HH:mm, removed control, renderer hashes
and code revision. Exact public JSON bytes/presentation hash and private mapping match
the earlier frozen material. Older package checkpoints remain unchanged. This new
package supersedes earlier examples for the remaining manual browser acceptance.
The user's cropped screenshot shows source uncertainty and inference notice text only;
it does not establish the full package's responsive/persistence/export/import gate.

Issue #21 and parent #12 were updated with removal, format correction and clear final
reviews, then independently fetched to verify exact bodies, unchanged labels and open
states. Browser-dependent acceptance remains unchecked. Source uncertainty explains
the uncertain traffic duration; the separate missing-arrival notice identifies display
arithmetic, not a verified arrival. Neither claim was altered to suppress uncertainty.
No backend/planner/scorer/dependency/source/answer change, push, live/native supplement,
real rater session, formal comparison, freeze or later-ticket work occurred.

Final closeout checks: eight English documents and 191 local Markdown target
occurrences passed, along with diff whitespace. Backend executable code, scripts and
dependency manifests are unchanged against the review base. Documentation is a
separate coherent local commit; generated package/validation and the development
archive remain ignored. Manual acceptance is not inferred from automated checks.

<a id="rtpeval-ticket-09-final-acceptance"></a>

<a id="rtpeval-ticket-09-final-acceptance--ticket-09-scoped-acceptance-recheck"></a>

## Ticket 09 scoped acceptance recheck

Date: 2026-10-02, Australia/Sydney. Starting revision:
290ef203c20fa18e8d4f3ab05aa4e5b5ecf6cda7, feature/evaluation, initially clean tree/index.
The user requested Ticket 09 acceptance. This scope checks the current synthetic
package, existing offline tests and import/report interfaces; it does not authorize
real raters, live providers, formal evaluation, push or later tickets. No runtime
implementation or dependency changes were made. Status: offline recheck Validated;
complete native direct-file browser acceptance still pending user evidence.

<a id="rtpeval-ticket-09-final-acceptance--actual-validation-sequence"></a>

### Actual validation sequence

1. Existing frontend BlindReview/answers tests: **11 passed / 2 files in 5.34s**.
   They cover ranking/submission/revision persistence, storage failure, time-zone
   conversion including DST/compact offsets, HH:mm and hidden dedicated hints.
   These are jsdom checks, not native file:// evidence.
2. The first dedicated backend run failed during fixture setup: **26 errors / 2 warnings
   in 10.83s**. Every error was PermissionError/WinError 5 while pytest tried to scan
   the default C:/Users/70522/AppData/Local/Temp/pytest-of-Ding root; warnings also
   reported an inaccessible default .pytest_cache. Assertions were not reached.
   This is an observed temporary-directory permission failure, not a database failure.
3. Repeated the same four backend files with a new workspace-contained --basetemp
   and -p no:cacheprovider. Result: **26 passed in 3.90s**, no skips/deselections.
   No permission change or application/test-source modification was needed.
4. Rebuilt the source-linked package through build_human_package using the original
   synthetic manifest, config-final and review-final. Public/private objects exactly
   match the latest package/mapping. Public JSON bytes remain equal to public-final.
   Validated mapping/presentation hashes, embedded HTML data and renderer JS/CSS hashes
   against validation-no-hints.json; offline CSP and lack of external assets passed.
   Public delivery still contains only review.html and presentation.json.
5. Generated explicitly synthetic revision fixtures for the current frozen package.
   Ran the actual human_cli import with the same bundle twice and human_cli report.
   Six records are retained once; four effective submissions are selected. Revision 2
   supersedes revision 1 while later draft revision 3 remains audit-only. Each dimension
   derives six version pairs; three main tasks determine aggregates, and one hidden
   duplicate contributes separate six-pair consistency without extra main-task weight.

Commands:

```powershell
npm.cmd --prefix frontend test -- src/features/blind-review/BlindReview.test.tsx src/features/blind-review/answers.test.ts
.venv/Scripts/python.exe -m pytest backend/tests/evaluation/test_human_tasks.py backend/tests/evaluation/test_human_answers.py backend/tests/evaluation/test_human_report.py backend/tests/evaluation/test_human_cli.py -q -p no:cacheprovider --basetemp artifacts/rtpeval/ticket09/acceptance-20261002-1910/pytest-tmp --junitxml artifacts/rtpeval/ticket09/acceptance-20261002-1910/backend-junit.xml
```

Ignored evidence directory: artifacts/rtpeval/ticket09/acceptance-20261002-1910/.
backend-junit.xml records the successful backend run; integrity.json records package
checks and the synthetic CLI outcome; synthetic-answers.json, imported.json and
report.json retain the actual local replay artifacts. The initial setup failure and
frontend result are observed tool output summarized here, not invented saved logs.
Earlier full frontend 94-pass/build/lint and backend 2299-pass/10-skip gates remain
separate historical runs, not rerun by this scoped acceptance.

<a id="rtpeval-ticket-09-final-acceptance--remaining-native-acceptance"></a>

### Remaining native acceptance

Current target: artifacts/rtpeval/ticket09/public-no-hints/review.html.
Browser Use previously rejected file:// and forbade alternate-browser/server/raw-protocol
circumvention; no such workaround was attempted. A self-contained manual checklist was
sent to the user during this recheck. No result has yet been received at this checkpoint.

- [ ] Original request and complete A/B/C/D itineraries display; changing the IANA zone
  correctly converts dates/HH:mm clocks. Original timestamp controls and dedicated
  uncertainty/item/time-warning hints stay absent; Inferred arrival remains labelled.
- [ ] Narrow-window display remains readable and controls are usable.
- [ ] Submit an answer, refresh and confirm recovery; download JSON and reimport it,
  confirming effective answers and revision history.

These pending checks prevent full acceptance and Issue #21 closure. Parent #12 and
its Ticket 09 checkbox remain open/unchecked. No research conclusion or version freeze
is inferred from synthetic development validation.

<a id="rtpeval-ticket-09-final-acceptance--documentation-and-tracker-checks"></a>

### Documentation and tracker checks

Six English documentation files and 192 local Markdown target occurrences passed;
prior acceptance remains exact and the tracked diff contains documentation only.
Diff whitespace passed. Issue #21/#12 updates were independently read back as exact
intended bodies, open states, original labels/comment counts and unchanged historical
suffixes/checkboxes. No native result has yet been received. Generated evidence and
the research archive remain ignored and excluded from the local documentation commit.

<a id="rtpeval-ticket-09-final-acceptance--subsequent-user-browser-feedback"></a>

### Subsequent user browser feedback

The user reported checklist items 1-2 have no problems: current direct-file display/
time-zone behavior and narrow-window interaction pass by user report. This is user
evidence, not independent tool observation. Item 3 remains untested because the user
needs a clear/reset button to repeat submission/refresh/JSON recovery from empty state.
The user requested that button; its narrowly scoped implementation will have separate
TDD/review/commit evidence. Full acceptance remains pending item 3 and checking the
updated renderer; the earlier no-result statements above preserve their checkpoint.

<a id="rtpeval-ticket-09-final-acceptance--clearing-enabled-follow-up"></a>

### Clearing-enabled follow-up

The requested [Clear answers addition](blinded-ranking-record.md#rtpeval-ticket-09-clear-answers) now has confirmed
package-scoped persistence reset, failure preservation and backup restoration.
Implementation 3a2e3d9 precedes review; independent Spec found one pending-import
race, separately corrected at d514508 with a red/green regression. Full frontend
98 passed / 13 files in 32.64s; TypeScript/blind build/lint passed; both final review
axes are clear. Current native target is public-clear-answers-final/review.html under
the same ignored Ticket 09 artifact directory. User report establishes items 1-2 on
the preceding renderer; item 3 remains pending against this updated package. Earlier
unchecked/no-result statements remain their original chronological checkpoints.

<a id="rtpeval-ticket-09-final-acceptance--user-confirmed-completion---2026-10-02"></a>

### User-confirmed completion - 2026-10-02

At clean documentation base ff00057, the user explicitly reported checklist item 3
passed after receiving the final clearing-enabled renderer. Earlier reports confirmed
items 1-2. The accepted recovery sequence is submission/refresh, JSON download,
confirmed clear/blank refresh and JSON reimport restoring answers/revisions. Combined
with retained offline gates and clear Standards/Spec rechecks, Ticket 09 acceptance
is complete. Native observations are user reports; no independent tool browser pass
or additional test run is claimed. Previous pending statements remain their original
checkpoints. Issue #21 closed/completed, parent #12 marks 01-09 completed and stays
open for 10-12; source commits/documents remain local/unpublished, no push or freeze.

<a id="rtpeval-ticket-09-timezone-display"></a>

<a id="rtpeval-ticket-09-timezone-display--ticket-09-approved-time-zone-display-extension"></a>

## Ticket 09 approved time-zone display extension

Date: 2026-10-02, Australia/Sydney. Review base:
dfe26954bfcad7a22f2f7c87c3302dbd767fe9f3, feature/evaluation; clean initial tree/index.
The user approved the following extension, local commits and no push.

<a id="rtpeval-ticket-09-timezone-display--accepted-scope-and-test-seam"></a>

### Accepted scope and test seam

Add a time-zone dropdown to the independent blind-review page, defaulting to UTC,
with available IANA zones. Explicit-offset activity start/end, travel departure/supplied
arrival and inferred arrival convert to the selected zone. Display a 24-hour HH-mm
clock together with its date, including converted cross-day dates. Keep original source
day grouping and indicate it as such; selecting a display zone does not move activities
between source days. Preserve original timestamps as inspectable source information.
Date-only request/day values do not identify instants and are not shifted.

Missing-zone local timestamps/clocks remain unconverted, use HH-mm when valid and state
that their time zone was not supplied. Missing/invalid values remain visible without
inventing a date, offset or clock. Free-text notes and preferences are not rewritten.
Inferred-arrival notices and source uncertainty remain. Presentation/source hashes,
private mapping, imported/exported answers and automatic scoring do not change.

Use browser Intl data without a provider call or new dependency. This is display-only;
the original preflight's source-preservation requirements still apply. No planner/scorer,
real rater, live/native supplement, formal comparison or later-ticket change is included.

Approved seam: the existing BlindReview React interface. Observe dropdown changes,
displayed clocks/dates, cross-day and daylight-saving transitions, missing-zone/invalid
source handling, retained uncertainty and unchanged answer/presentation linkage. Use
literal expected times independent of implementation and real Intl behavior. Run related
UI tests, full frontend tests, TypeScript, both builds and lint. Commit implementation/
direct tests before independent Standards and Spec review; preserve correction commits.
Regenerate a separate final synthetic package after the renderer build. Actual file://
browser acceptance remains a pending user check because tool navigation is prohibited.

<a id="rtpeval-ticket-09-timezone-display--validation-and-review"></a>

### Validation and review

Initial UI red: 2 failed / 2 passed, because the dropdown and formatted inferred arrival
did not exist. The first sandbox run could not write Vite's bundled config; an authorized
normal-permission retry reached those observed behavior failures. After implementation,
4 UI tests passed. Added missing-zone/invalid-time checks exposed JS date rollover and
invalid clocks; strict date/clock validation corrected them, with 6 UI tests passed.
Daylight-saving departure/inferred-arrival checks passed with real Intl.

The first full frontend run passed 92 tests and failed 1: the new fractional-offset test
selected Asia/Kolkata even though the runtime's enumerated option was Asia/Calcutta.
The test now selects the actual offered IANA alias at the UI seam, retaining literal
expected India clocks. Final full frontend: 93 passed across 13 files in 38.99s;
7 BlindReview tests plus 3 existing answer tests participate. TypeScript, isolated
blind-review build, product build and lint passed. No new dependency or backend change.
Implementation/direct tests and this approved scope record will be committed before
Standards/Spec review; review results and the final synthetic artifact remain pending.
No new full backend run is claimed for this frontend-only extension.

<a id="rtpeval-ticket-09-timezone-display--committed-review-correction-and-final-acceptance-checkpoint"></a>

### Committed review, correction and final acceptance checkpoint

f600315 (feat: add time zone selection to blinded review) commits implementation,
direct UI tests and the accepted scope before independent review. Standards: zero
documented breaches and zero actionable heuristics. Spec: one P2, explicit compact
offsets accepted at the existing projection boundary were not converted by the UI.
New UI regression failed for +0200/+02 before correction; offset normalization now
converts both while retaining exact original strings. Separate fix 29df5fd preserves
implementation history. Related 11 UI/answer tests passed in 4.44s; TypeScript,
blind build and lint passed. Final committed full frontend: 94 passed / 13 files
in 39.39s. Earlier 93-test gate above is a separate pre-correction run.

Both reviewers rechecked f600315...29df5fd: original P2 resolved, zero residual findings
on either axis. Spec independently checked positive/negative compact/hour offsets,
existing colon/Z offsets, invalid offsets and missing-zone behavior. No edits or
full-test rerun by reviewers are claimed.

Generated ignored artifacts/rtpeval/ticket09/public-timezone-final/review.html with
the final renderer; exact public JSON bytes, presentation hash and private mapping
remain unchanged from public-final. Separate validation-timezone-final.json records
renderer hashes, revision and the pending browser gate. Earlier renderer checkpoints
remain unchanged. Manual check request now targets this final package, including zone
switching, HH-mm/date/inference display, narrow layout, refresh and JSON backup/import.
Browser Use's file:// prohibition is unchanged; no circumvention or actual browser pass.

Issue #21 and parent #12 were updated with approved extension and review/fix status,
then independently fetched to verify exact bodies, unchanged labels and open states.
The browser-dependent acceptance criteria/parent checkbox remain unchecked. No push,
branch switch, planner/scorer change, source/answer rewrite or later-ticket work occurred.

Final documentation checks: eight English documents and 195 local Markdown target
occurrences passed; diff whitespace passed. Backend executable code, scripts and
frontend dependency files have no diff against the review base. Final documentation
is a separate coherent local commit; ignored renderer/validation/archive files are
excluded. Pending manual browser acceptance is not converted into a completion claim.

<a id="rtpeval-ticket-09-timezone-display--subsequent-explicit-display-corrections"></a>

### Subsequent explicit display corrections

The user requested removal of the Original timestamp UI and corrected clocks to HH:mm.
[Display cleanup](blinded-ranking-record.md#rtpeval-ticket-09-display-cleanup) supersedes the inspectable-control and
HH-mm UI requirements above. Source strings remain frozen in artifacts, and malformed/
unknown values, original day grouping and distinct uncertainty/inference notices remain.
Earlier gate/review records apply to their original renderer revisions and are preserved.

<a id="rtpeval-ticket-09-uncertainty-display"></a>

<a id="rtpeval-ticket-09-uncertainty-display--ticket-09-user-requested-uncertainty-hint-removal"></a>

## Ticket 09 user-requested uncertainty hint removal

Date: 2026-10-02, Australia/Sydney. Review base:
925ad71b8c4c360e5af079957c9463674f39e2f7, feature/evaluation; clean initial tree/index.
The user explicitly requested no uncertainty-factor hints. This authorizes the narrow
display correction and supersedes earlier requirements to show dedicated hint blocks.
Approved local-commit/no-push policy and existing BlindReview React test seam apply.

Remove the dedicated Uncertainty/unknowns field, all item notice blocks and warning
text adjoining displayed times, including missing-zone and invalid-time conversion
notices. Remove unused hint styling. Keep UTC-default IANA selector, converted dates,
24-hour HH:mm clocks, source-day grouping, supplied/missing time values and the neutral
Inferred arrival label. No new time-zone/date/arrival fact is invented; unknown-zone
clocks remain unconverted, invalid values remain raw, null remains Not supplied.
Ordinary source notes/preferences and display duration/basis fields are not rewritten.

Frozen source/public/private JSON, unknowns/notices records, hashes, answers, reports
and V0-V3 behavior remain unchanged. This is UI hint suppression, not source erasure,
provider verification or a claim of certainty. No backend or dependency change.

Use the existing React seam to verify missing hint fields/text while retaining inferred
arrival, correct times, unknown-zone local clocks and invalid/missing values. Update
the old hint-preservation assertions to the user's new display rule. Run full frontend
tests, TypeScript, blind build and lint; commit implementation/direct tests before
Standards/Spec review, then record actual results and regenerate a separate synthetic
renderer. No file:// workaround, live/native supplement, real rater session, formal
comparison, freeze or later-ticket work is included. Manual browser acceptance pending.

<a id="rtpeval-ticket-09-uncertainty-display--actual-validation-and-review"></a>

### Actual validation and review

The selected existing UI regression first failed because Uncertainty still rendered
(1 failed, 7 not selected). Filtered unknowns fields at the renderer boundary, removed
item notice rendering/time-warning text and unused hint CSS. Parsing and timezone
arithmetic remain unchanged. Final full frontend: 94 passed / 13 files in 25.49s;
TypeScript, blind build and lint passed. Existing regressions verify inference/time-zone/
DST/compact-offset/unknown-zone/raw-invalid values and answer revision behavior.
Implementation/direct tests/scope are committed before Standards/Spec review; actual
review, final artifact and tracker closeout results will be appended when available.

<a id="rtpeval-ticket-09-uncertainty-display--committed-review-and-closeout-checkpoint"></a>

### Committed review and closeout checkpoint

f1f0cc0 (fix: hide uncertainty hints in blinded review) commits implementation/direct
tests/scope before review. Standards: zero documented breaches and actionable heuristics.
Spec: zero missing/wrong/unrequested behaviors under the new user request. Spec independently
rendered the real UI and observed hidden fields/notices/time warnings, retained inferred
label/local clocks/raw-invalid/missing values/source notes/preferences/duration basis,
and unchanged presentation JSON. Reviews were read-only; no repeated full/browser pass.

Generated ignored artifacts/rtpeval/ticket09/public-no-hints/review.html with final
renderer. validation-no-hints.json records code/asset hashes and hidden-hint flags;
exact public JSON bytes/hash and private mapping remain unchanged. Previous packages
remain preserved. Actual complete direct-file/responsive/refresh/export/import evidence
is still pending; the final package supersedes earlier manual-check examples.

Issue #21 and parent #12 updates were independently fetched to verify intended exact
bodies, open states and original labels. The live first renderer criterion now records
retained source uncertainty in frozen material and explicitly user-requested UI hint
suppression; imported historical criteria/source and pinned links are unchanged.
Browser-dependent criteria and parent Ticket 09 checkbox remain unchecked. New public
summaries omit detailed local revision/test metadata. No comment, assignment, close,
push, live/native supplement, formal study, freeze or later-ticket execution occurred.

Final closeout checks: seven English documents and 196 local Markdown target
occurrences passed, as did diff whitespace. Backend executable code, scripts and
dependency manifests have no diff against the review base. Final documentation is
a separate local commit; ignored renderer/validation/archive files are excluded.
No automated result completes the pending actual browser gate.
