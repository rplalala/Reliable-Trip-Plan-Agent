# Ticket 09 local answer clearing

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

## Pre-review validation

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
