# Planning input UX commit proposal

Status: resolved
Fixed point: 40b0b26 (HEAD before this iteration)
Approval: The user approved all four groups on 2026-09-26.
Action: Four approved local commit groups completed; no push, live call, or version freeze.

## Approved logical commits

1. `feat: improve shared trip inputs and compact weather` — Task 01. Stage the currency
   list/select, strict ISO date policy and calendar, compact weather view, related styling,
   shared Product/Dev form wiring and their direct tests. This includes the Task 01 hunks in
   `PlanningForm.tsx`, `DeveloperPlannerPage.tsx`, both page tests and `global.css`.
2. `feat: add GeoDB destination suggestions` — Task 02. Stage the GeoDB adapter, bounded
   destination service and GET assistance route, router registration, destination config,
   shared combobox and planning API, relevant Product/Dev wiring/styles and tests. Stage only
   Task 02 hunks in files also changed by Tasks 01 or 03.
3. `feat: add reviewed preference polishing` — Task 03. Stage the model adapter and transport
   schemas, service/prompts, POST assistance route, polish config and config reference, numeric
   policy trace handling, shared preview/Apply/Undo UI and relevant tests. Stage only Task 03
   hunks in overlapping files.
4. `docs: record planning input UX implementation` — this spec, its three local task records,
   and this commit proposal, after the implementation commits.

Partial staging was used for `PlanningForm.tsx`, `api.ts`, `api.test.ts`, `global.css`, both page
tests, `input_assistance.py`, `config_models.py` and `runtime.yaml`; these contain hunks from
more than one proposed commit. Do not split an implementation hunk from its direct test.

The four pre-existing dirty closeout documents — `.scratch/iteration-closeout/commit-plan.md`,
`PROJECT.md`, `docs/README.md`, and `docs/poi_semantics_closeout.md` — are outside this proposal
and must remain untouched/unstaged here. No ignored generated output, credential, provider
payload or runtime log belongs in any group.

## Final offline evidence

TDD began with missing-module failures for the GeoDB API/combobox and polish API/UI. Review
then exposed client-cleanup handling, date/currency preservation and invalid-model error
mapping; new regression tests reproduced those gaps before fixes. The first full backend
suite found two config integration failures (trace token limits and missing YAML reference
rows); both were fixed. Final backend suite: 1,673 passed, 9 skipped. Final frontend suite:
82 passed. ESLint, Ruff, TypeScript/Vite build and `git diff --check` passed. Standards and
Spec reviews were rechecked after fixes with no remaining findings.

Local-browser acceptance used FastAPI with GeoDB MockTransport and fake model responses,
plus the Vite frontend; no real GeoDB or model calls. Product and Dev displayed suggestions,
manual fallback and preference preview. Apply/Undo, uncertainty and sanitized blocked error
were visible. At 375 px, the preview used one column with no horizontal document overflow.
Real free-instance compatibility/terms and real-model Gate-success changes remain unverified.

## Commit execution checks

- `9a147d6` contains Task 01. Its staged snapshot passed 70 frontend tests and the production build.
- `1ec1738` contains Task 02. Its staged snapshot passed 75 frontend tests, 16 relevant backend
  tests (GeoDB, trace, and config documentation), and the production build.
- `31071c9` contains Task 03. The staged implementation matched the previously validated final
  working files; 25 relevant backend tests, all 82 frontend tests, build, ESLint and Ruff passed.
- This document and the local spec/task records form the fourth documentation commit.

The split initially introduced one trailing blank line in the staged-only Task 02 API file;
`git diff --cached --check` caught it, it was removed, and the check passed before committing.
No production implementation was changed to create the split. The four excluded closeout
documents were checked against their original byte hashes and remain outside all four commits.
