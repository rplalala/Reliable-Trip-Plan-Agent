# Transport responsibility correction acceptance

Date: 2026-09-30. Base commit: 1eb441f47cb0de65eb1c687eb56a45dba286aa86.
Branch: feature/evaluation. Existing uncommitted Ticket 04 work preserved.
Status: Implemented and validated offline; not frozen.

## Scope

- V0 retains its explicit model-estimated transport instructions and DTO.
- V1-V3 share a primary DTO excluding transport and output acceptance rejecting declared model transport before route binding. Initial and Repair prompts prohibit transport authoring; the shared policy no longer advertises the forbidden transport role. Application route selection, budgets and transfer construction are unchanged.
- V3 Repair retains its existing operation-only patch permissions; transport role/mode injection is rejected.
- Evaluator final and optional V3 projections select activities for V0 and transfers for V1-V3. Ignored-source records and diagnostics retain provenance without occupancy/fallback. Repeated actual journeys stay occurrence-specific.
- Ticket 05 metrics and protected-time union implementation remain pending.

## Verification history

Acceptance and DTO tests first failed on the missing version boundary, then passed after implementation. Six evaluator cases reproduced use of the forbidden activity source. They now pass with explicit version selection. Existing duplicate/conflict tests now compare authoritative transfers with each other. DTO construction fixtures were updated to the primary day schema; cost behavior is unchanged. A new optional-projection test initially used the wrong result nesting and was corrected to run.optional.

Related combined tests: 190 passed, 1 skipped. Intake/mixed Routes/V0 prompt checks after occurrence coverage: 78 passed, 1 skipped.

Standards review: zero findings. Spec review identified a P2 contradiction in the appended shared role vocabulary. A failing composed-prompt regression reproduced it; removing that shared transport suggestion while retaining V0's explicit instruction fixed it. V0/V1/shared-policy retest: 22 passed. Spec follow-up: zero remaining findings. Ruff and compilation passed; no static typechecker is configured.

First full-suite attempt stalled without reporting a failure around the retrieval tests and was interrupted. Exact test/cause was not established from a stack. The runtime retrieval file passed separately (16 tests). A final full rerun enabled faulthandler timeout diagnostics.

## Limitations

All checks use local artifacts or fake dependencies, with no real Google/model/database calls or formal experiments. Declared forbidden transport fails generation without an extra retry. Prompt instructions cannot establish comprehensive detection of transport prose hidden under another role; evaluator ambiguity remains reviewable. Independent evidence remains necessary to assess factual route feasibility. No commit, push, benchmark or freeze.


The next full run completed with 5 failed, 1968 passed and 10 skipped in 83.54s. All five failures were old V3 fixtures expecting declared model transport to pass output acceptance into schedule/semantic/coverage validation. Updated those cases to assert the newly required rejection at the shared boundary, retaining non-transport assertions. The four affected files passed 119 tests; Spec follow-up found no remaining issue. The application rejects this invalid generated input, whereas independent evaluation can still intake historical delivered outputs and preserve/ignore their transport source records. A final full run verifies these updated expectations.


Final full backend regression: **1973 passed, 10 skipped in 85.49s**. The ten skips are nine opt-in database cases and the existing native Windows symlink privilege case. Ruff, compilation and diff whitespace checks passed. Standards and Spec have zero remaining actionable findings. No live service was called, no files were staged or committed, and no version was frozen.
