# V3 paired report development evidence

Date: 2026-10-03, Australia/Sydney. Branch: `feature/evaluation`.
Review fixed point: `d08083d5d50573e0bec6345f45ed12beb2b77855`.
The index/worktree was clean at that fixed point. Status: Implemented;
validation/review closeout is recorded below. Not Frozen or a formal benchmark.

## Authority and delivered scope

The user approved implementation of the [accepted source-driven Ticket 10 preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22#issuecomment-5955706453)
after the coordinate bridge. [Issue #22](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22)
owns live tracker state; [PROJECT](../../../PROJECT.md) and the
[paired contract](../../contracts/0005-quality-human-review.md#v3-pairs) own current scope
and behavior. Approved work includes offline TDD, local implementation/test commits,
independent Standards/Spec review, in-scope corrections and durable documentation.
No live provider/model/database runs, planner instrumentation, extra budget, frontend,
Tickets 11-12, formal evaluation, push, PR, merge, branch change or tracker mutation.

The immutable preparation/report and CLI reuse current intake, identity replay, paired
frozen snapshots and public scorers. Original source IDs and adopted rounds/components/
window fragments establish occurrence lineage; independent identity establishes venue
continuity, and independent checks establish compliance. Repeated visits, moves,
replacement and splits do not require manual review solely due to their complexity.
Residual ambiguity stays local while defined aggregate stage deltas remain available.
No internal Repair success/PASS verdict becomes an independent outcome.

The new report uses a separate two-stage union mask, exact rational signed deltas,
retained raw checks/coverage, losses/replacements and participant/route continuity.
Missing pairs remain visible; absent facts, empty masks and unresolved denominators
are not zero-filled. Quality arithmetic was extracted unchanged into a shared internal
adapter; Ticket 08 retains its final-only wire, rules, masks and paired-scope rejection.
The changes introduce no runtime planner imports or V0-V3 execution-path changes.

## Observed test and correction sequence

1. Public report and source-preparation tests first failed on missing modules/interfaces.
   Minimal slices established explicit missing-pair records, unchanged-pair exact zeros,
   existing scorer composition and repeated-visit retime lineage.
2. Deletion, same-slot replacement and cross-day movement exposed missing supported edit
   fields and correspondence wiring. Added validated state/patch membership, loss context
   and the pair-union accounting rule. A split test failed without root/fragment composition;
   complement validation and composed origins then preserved free-time lineage without
   inventing primary visits.
3. Partially accepted component tests initially treated rejected/pending/rolled-back adds
   as adopted. Restrict effective edits to actually accepted component membership and
   observed states. Inconsistent embedded round inputs fall back with diagnostics, while
   stale/foreign supplied source material remains a correction error.
4. Independent continuity first lacked conflict tracking. Fixture corrections supplied the
   required fixed-time match field and a real 15-minute query window: a zero-gap route was
   correctly UNKNOWN, so production scoring was preserved. Opening FAIL-to-PASS is reported
   alongside requirement/route regressions; retained participants support conflict resolution,
   and original protection obligations/scopes remain present.
5. Duplicate-venue fallback initially greedily matched a leftover occurrence. Global canonical
   uniqueness now prevents that false certainty. Review wiring briefly had a signature mismatch;
   completing the public preparation/review boundary restored all tests. Residual reviews use
   exact stage refs and cannot override established lineage or label changed content unchanged.
6. The CLI test failed until preparation/report commands existed. A normalization test exposed
   the difference between adopted snapshots and producer output sorting, ledger name changes
   and refreshed transfers. Explicit source-backed reconciliation now preserves lineage.
   Population/subtotal tests then added exact observed differences with null/coverage retention.
7. Additional source/route tests exposed missing replacement/loss counts and deletion topology.
   Route connection lineage is now separate from venue-compatible quality comparison; insertion
   reports the removed direct leg and two added legs. Ordered replacements retain both round
   pointers without multiplying final visit-loss counts. No-Repair/skipped/rejected source
   snapshots remain eligible. Two skipped/rejected tests used the wrong output key initially;
   expectations were corrected to `auxiliary_total`.
8. Material tests cover stale/foreign source bytes, forged preparation, invalid review refs,
   duplicate participation, naive timestamps, cardinality, corrupt snapshots and stale identity.
   Replay tests prohibit socket construction, compare source bytes before/after, repeat CLI JSON
   and prove creation-time changes do not change semantic content hashes. Properly relinked
   internal-findings-only changes preserve independent scores and correspondence facts.
9. Opening/route lower bounds and observed subtotals remain labelled. Partial improvement uses
   exact comparable FAIL magnitudes, excluding incomplete route evidence. An added regression
   found that a same-slot replacement with UNKNOWN venue identity could falsely certify a
   retained protection fix. Primary participant continuity now requires independently confirmed
   same-venue identity; the test changed from `resolved` to `unresolved_correspondence`, and the
   15-test edge suite passed afterward.

All fixtures are synthetic, local development evidence. Snapshot acquisition used injected
transport; no real Google client, LLM, PostgreSQL, live Repair or formal cases were executed.
Ruff import/format/line-length issues were corrected. Accidental formatting of unrelated
existing modules was restored; only intended task changes are staged.

## Validation, review and local delivery

- Intermediate evaluator gate: **571 passed, 1 skipped in 84.20s**.
- First full backend gate: **2402 passed, 10 skipped in 230.18s**, before the final
  UNKNOWN-replacement protection correction. This is intermediate evidence, not the final gate.
- Pre-review full backend gate after that correction: **2403 passed, 10 skipped in 211.62s**,
  zero deselections. Its JUnit inventory contains **574 passed, 1 skipped** evaluator
  cases, including all **46 new paired tests**. These subset counts are from the same
  full run, not an additional evaluator run. Backend Ruff, ten-file formatting, CLI help
  and diff whitespace checks passed.
- Implementation/direct-test commit: `f65cd0f` —
  `feat: report independent V3 draft and final diagnostics`, before code review.
- Standards: zero documented-standard violations; one nonblocking P3 duplicated-content
  comparison smell. `_content` now supplies both fallback and review semantics; targeted
  independent recheck confirmed the finding resolved.
- Spec: two reproduced P2 findings, multi-occurrence manual removal/addition counted as
  one relation, and traffic conflict removal compared transfer refs against activity refs.
  Four public regressions initially failed, then passed after per-occurrence counting and
  independently linked endpoint/topology attribution. Paired/Ticket 08 regression:
  **76 passed in 19.09s**. Commit `e24ce0e` —
  `fix: attribute paired visit and journey changes correctly` preserves the original commit.
  Both original findings passed independent recheck. Full evaluator after this first fix:
  **578 passed, 1 skipped in 92.49s**.
- Spec recheck exposed one new P2: a complex many-to-many set could supply a false new
  journey attribution through structural-leg flags. A public regression failed; a same/
  changed canonical-venue parameterization exposed the equivalent membership inference.
  Only unique endpoint correspondence or explicit added/removed endpoints now establishes
  concrete leg changes. Venue-change participant/loss attribution also requires 1:1
  correspondence. Complex groups retain constituent observations and unresolved attribution.
  Paired/Ticket 08 regression: **78 passed in 16.89s**. Commit `45b13d9` —
  `fix: preserve uncertainty in complex route correspondence` is a separate second correction.
- Targeted independent Spec recheck: original three public repros plus six formal correction
  regressions **9 passed**; the third P2 is resolved, with no new issue in the limited recheck.
  Both axes are closed: Standards 0 hard violations/1 P3 addressed; Spec 3 P2 findings across
  two rounds, all addressed. No original implementation/correction commit was rewritten.
- Final post-review full backend: **2409 passed, 10 skipped in 216.22s**, zero
  deselections. Its JUnit inventory contains **580 passed, 1 skipped** evaluator cases
  and all **52 new paired tests**. These are subset counts from that full run.
  Backend Ruff, eleven-file formatting, CLI help and diff whitespace checks passed.
  Seven changed documents and 143 local link targets passed the tracked-target/English
  checks; no new formal document depends on ignored scratch or raw local evidence.

Existing skips are nine opt-in PostgreSQL cases and one Windows symlink privilege case;
no supplement was inferred or run. Temporary fixture directories and JUnit evidence remain
ignored under `artifacts/ticket10-dev/`; these are local evidence identifiers, not published
document dependencies. The ignored thesis archive preserves this development decision history.

GitHub #22 remains open/read-only in this task; implementation approval did not authorize
tracker mutation or publication. No claim is made that local commits are remotely available.

## Remaining limits

Legacy/contradictory embedded edit metadata can disable source-lineage claims; unique content
and independent canonical fallback/review remain available. No history can be reconstructed
uniquely from indistinguishable observations without sufficient original evidence. A valid
aggregate delta describes two observed populations, not causal Repair efficacy or an overall
success rate. Controlled Repair and mechanism reporting remain separate Tickets 11-12.
Existing injected-transport and formal-run authorization boundaries remain in force.
