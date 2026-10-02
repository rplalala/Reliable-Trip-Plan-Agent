# Ticket 09 scoped acceptance recheck

Date: 2026-10-02, Australia/Sydney. Starting revision:
290ef203c20fa18e8d4f3ab05aa4e5b5ecf6cda7, feature/evaluation, initially clean tree/index.
The user requested Ticket 09 acceptance. This scope checks the current synthetic
package, existing offline tests and import/report interfaces; it does not authorize
real raters, live providers, formal evaluation, push or later tickets. No runtime
implementation or dependency changes were made. Status: offline recheck Validated;
complete native direct-file browser acceptance still pending user evidence.

## Actual validation sequence

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

## Remaining native acceptance

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

## Documentation and tracker checks

Six English documentation files and 192 local Markdown target occurrences passed;
prior acceptance remains exact and the tracked diff contains documentation only.
Diff whitespace passed. Issue #21/#12 updates were independently read back as exact
intended bodies, open states, original labels/comment counts and unchanged historical
suffixes/checkboxes. No native result has yet been received. Generated evidence and
the research archive remain ignored and excluded from the local documentation commit.

## Subsequent user browser feedback

The user reported checklist items 1-2 have no problems: current direct-file display/
time-zone behavior and narrow-window interaction pass by user report. This is user
evidence, not independent tool observation. Item 3 remains untested because the user
needs a clear/reset button to repeat submission/refresh/JSON recovery from empty state.
The user requested that button; its narrowly scoped implementation will have separate
TDD/review/commit evidence. Full acceptance remains pending item 3 and checking the
updated renderer; the earlier no-result statements above preserve their checkpoint.

## Clearing-enabled follow-up

The requested [Clear answers addition](ticket-09-clear-answers.md) now has confirmed
package-scoped persistence reset, failure preservation and backup restoration.
Implementation 3a2e3d9 precedes review; independent Spec found one pending-import
race, separately corrected at d514508 with a red/green regression. Full frontend
98 passed / 13 files in 32.64s; TypeScript/blind build/lint passed; both final review
axes are clear. Current native target is public-clear-answers-final/review.html under
the same ignored Ticket 09 artifact directory. User report establishes items 1-2 on
the preceding renderer; item 3 remains pending against this updated package. Earlier
unchecked/no-result statements remain their original chronological checkpoints.

## User-confirmed completion - 2026-10-02

At clean documentation base ff00057, the user explicitly reported checklist item 3
passed after receiving the final clearing-enabled renderer. Earlier reports confirmed
items 1-2. The accepted recovery sequence is submission/refresh, JSON download,
confirmed clear/blank refresh and JSON reimport restoring answers/revisions. Combined
with retained offline gates and clear Standards/Spec rechecks, Ticket 09 acceptance
is complete. Native observations are user reports; no independent tool browser pass
or additional test run is claimed. Previous pending statements remain their original
checkpoints. Issue #21 closed/completed, parent #12 marks 01-09 completed and stays
open for 10-12; source commits/documents remain local/unpublished, no push or freeze.
