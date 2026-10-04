# Controlled V3 repair development evidence

Date: 2026-10-04, Australia/Sydney. Branch: `feature/evaluation`.
Review fixed point: `b6d9dd98af3dc6c7038a88a858df441dffd1bd63`.
The initial index/worktree was clean. Status: Implemented and offline Validated;
not Frozen and not a formal benchmark. Documentation was updated after implementation
and correction commits; local temporary evidence remains ignored.

## Authority and delivered scope

The user invoked `implement` and approved the accepted
[Ticket 11 controlled replay contract](../../contracts/0001-evaluation-artifacts.md#controlled-repair).
[Issue #23](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23) owns live task state;
[PROJECT](../../../PROJECT.md) owns current authorization. This delivery includes offline
implementation, synthetic development fixtures, local commits, Standards/Spec review,
in-scope corrections and durable documentation. No live service, budget increase, formal
24-target/8-control construction/execution, formal analysis, Ticket 12, publication,
branch switch or Issue mutation was authorized or performed.

The executor reconstructs the real V3 post-primary path from frozen original input,
primary itinerary, interpreted requirements, runtime/supply/evidence, cache and semantic
state. Actual validation, target/scope derivation, candidate preparation, model input,
component acceptance, revalidation and finalization run through production V3 code.
Call scripts bind exact requests to typed responses or declared failures. Logical time
also drives real asyncio timeout handles; no provider latency or live cost is measured.
Missing/mismatched calls and malformed typed responses retain an out-of-band material
error even when production repair catches an exception.

V3-only preparation emits genuine result sources without invented V0-V2 outputs. The
controlled report composes existing independent identity, requirement/schedule, opening,
route and Ticket 10 correspondence checks. Per-target detection, authorization,
opportunities, model attempts and adopted components remain separate from independent
outcomes. The batch reader preserves missing cases and expected-target denominators.
The CLI exposes replay, preparation, identity references/plan/replay, evidence planning,
reporting and batch assembly. The [package guide](../../../backend/evaluation/README.md#controlled-v3-offline-workflow)
documents commands and the [wire contract](../../contracts/0001-evaluation-artifacts.md#controlled-executable-wire)
documents case, review, fact and report schemas.

Controls permit lawful additions when independently supported and compatible with
reviewed obligations. An explicit exactly-one-visit guard detects a second visit as
regression even if production accepts it. Human supplements can establish separately
verified opening/route facts, with exact source/case/query linkage and contradiction
checks. They do not alter planner inputs, raw paired scores or deltas. Remaining missing
facts stay local UNKNOWN; missing/corrupt material does not become a zero or no-change.

The two shared clock seams preserve live defaults. Identity plan/replay accepts an
actual V3-only prepared inventory, while ordinary intake still requires all four
versions. Existing V0-V3 entry points and intended live behavior remain available.

## Observed validation and correction sequence

1. Synthetic public-seam tests exercised unchanged controls, missed detection, adopted
   overlap repair, explicit-count regression, supported additions, newly closed visits,
   human supplementation, corrupt material, strict frozen calls and missing batch reports.
   Fixtures supply independent observations, reviewed coordinates and injected snapshot
   responses; they are development cases, not the formal corpus.
2. The first larger evaluator/V3/semantic regression ended with **1 failed, 1063 passed,
   1 skipped**. The existing static intake test prohibited planner imports across every
   evaluation module, including the newly approved isolated controlled executor. The
   explicit exception now names only the nine controlled modules; ordinary readers and
   scorers keep the planner-free boundary. Its targeted retest passed.
3. The required shared-seam **full backend gate passed: 2433 passed, 10 skipped**.
   A subsequent public CLI check passed all three controlled CLI tests after adding the
   identity-plan wrapper. These are checkpoints at that stage, not a current repeated
   full-suite result.
4. Precommit audit exposed a real logical-time defect: service clocks advanced, but
   asyncio timeout handles still observed real time and could accept a reply declared
   later than the configured timeout. A new regression failed before correction. The
   exclusive replay loop now observes logical time, and due timeout handles run before
   a scripted reply is delivered. Replay tests then passed; the evaluator gate passed
   **605 tests, 1 skipped**, including 25 dedicated controlled tests.
5. Implementation and directly related tests were committed before parallel review.
   Standards reported no actionable findings. Spec reproduced two defects: malformed
   frozen repair-model material was reported as ordinary model failure, and an
   obligation-only protection target could not confirm independently established
   resolution because its activity selector was empty.
6. The malformed-response regression first failed (`complete` instead of
   `execution_material_error`). Frozen responses now validate the real `RepairPatch`
   schema, preserving existing defaults; invalid shapes enter the material-error ledger.
   Shape-valid unauthorized or ineffective patches still face real production acceptance.
   The targeted test passed after the correction.
7. The first protection regression fixture omitted the controlled projection and failed
   on that missing fixture context. After supplying the actual prepared projections,
   the test reproduced the intended UNKNOWN-versus-PASS defect. The corrected branch
   reuses the independent `protected_time` obligation check. A parameterized retest
   confirms that fully verified `primary_visits` resolve, while `scheduled_commitments`
   with uncertain transfer occupancy remain unresolved even when the original visit's
   conflict continuity resolves. UNKNOWN checks and absent blockers remain unresolved.
8. The focused correction run passed **23 tests**. The final complete evaluator gate
   passed **608 tests, 1 skipped**, including 26 dedicated controlled tests and two
   paired protection-goal cases. Ruff, formatting, Python compile checks and Git diff
   whitespace checks passed. No configured static type checker was available; a separate
   mypy/pyright result is not claimed. The full backend gate in step 3 precedes these
   offline corrections; step 8 is the affected-scope regression evidence.

## Commit and review record

Implementation/direct-test commit, before review:

- `91310cc` — `feat(evaluation): replay frozen V3 controlled repair cases`.

Separate review-fix commits, preserving the original implementation:

- `a816e27` — `fix(evaluation): reject malformed frozen repair responses`.
- `ae6b847` — `fix(evaluation): verify protected goals by obligation scope`.

Review command: `git diff b6d9dd98af3dc6c7038a88a858df441dffd1bd63...HEAD`.
The Standards and Spec axes are separate: initial Standards had zero actionable findings;
the two Spec findings were corrected with red/green tests and separate commits.
Post-correction Standards recheck found zero issues; Spec recheck closed both findings
and independently ran the three related regression cases successfully. The final
documentation/link gate is recorded at closeout below.

## Execution limitations and evidence boundaries

- Use a dedicated offline process, exclusive event loop and serial cases, with no other
  network work. Replay temporarily patches process-wide sockets and the active loop
  clock. Concurrent web-service execution or unrelated async tasks are unsupported.
- Frozen material must include the actual calls needed by the case, full cache values
  and relevant semantic state. Old evidence-only replay captures containing key hashes
  do not automatically become complete executable historical cases.
- Tokenizer assets must already be local. Tests use an offline structural tokenizer;
  they do not establish real model token counts, cost, latency or output quality.
- Snapshot acquisition remains an injected-transport API. This delivery neither adds
  an operational live acquisition CLI nor authorizes live collection.
- Supplemental route facts do not fabricate transfer occupancy. Existing source-backed
  occupancy reviews and unresolved coverage remain necessary where applicable.
- Raw independent paired metrics remain unchanged by supplemental facts. Reviewed
  checks/continuity establish local outcomes without claiming recomputed total scores.
- No formal repair rates, control harm rates, version comparison, causal claims or
  research conclusions are produced. Ticket 12 and remote tracker synchronization remain
  separate work requiring authorization.

Task-local pytest caches and synthetic snapshots are under
`artifacts/ticket11-implementation/`; the local documentation checker is
`artifacts/ticket11-preflight/check_docs.py`. These ignored paths identify local development
evidence locations, not dependencies of the published contract. Authoritative validation
counts above come from the observed command outputs; no missing raw live payloads or
measurements are reconstructed.

## Documentation closeout

The final documentation gate checked six changed documents and 120 repository-local
tracked links/anchors, with zero link or language errors. Git index membership was
verified, including the new acceptance record. Final current-contract/navigation and
acceptance changes form a separate documentation commit. The research archive records
the dated failure/decision sequence in ignored `thesis_notes/`; neither that archive nor
temporary test artifacts are staged. No remote update or version freeze is claimed.
