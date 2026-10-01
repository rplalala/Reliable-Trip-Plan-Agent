# Ticket 06 offline opening acceptance

Current closeout: implementation, review and supplementary validation are complete.
The user approved the three local commit groups. Implementation/tests are committed at
ee085d3 and the database-test path correction at f62c07f; this record accompanies the
third documentation group. No push occurred. The sections below preserve their dated
original checkpoints; see the final approved closeout section.

Date: 2026-10-02, Australia/Sydney. Code checkpoint:
`ed4c9a9d4724263925748588878eadc22d21978a` on `feature/evaluation`, plus the
uncommitted Ticket 06 implementation and inherited approved preflight documents.
Status: Implemented and offline-validated; Standards/Spec reviews clear, full backend gate passed.
No commit, push, branch switch, version freeze or later-ticket work.

## Authority and implemented boundary

[PROJECT](../../PROJECT.md) and [approved preflight](ticket-06-preflight.md) own
scope; [opening](opening-contract.md), [time](evidence-time-contract.md),
[snapshot](snapshot-contract.md) and [metrics](metrics-contract.md) own meaning.
The user approved offline implementation, TDD/regressions, Standards/Spec review,
corrections and related documentation/archive/GitHub #18 updates. The execution
transfer preserved the existing uncommitted documents. This is development validation,
not a formal benchmark, experiment, version-level retrospective or research conclusion.

The public seam is `score_opening(intake, identity_report, snapshot_directory,
schedule_context=None, *, paired=False, expected_plan=None)`, with immutable
`OpeningResult.to_dict()`. Its local CLI is `backend.evaluation.opening_cli`.
The private `_opening_hours` calendar parser consumes original raw Places objects from
verified snapshots, never planner hours/findings or the reduced identity bridge.
`preparation.identity_ready` and `schedule_timezones` share existing Ticket 05 neutral
checks; requirement/schedule behavior is retained. `normalize_interval` adds the
explicit `allow_cross_date=False` option; earlier same-date defaults are unchanged.

Checks retain primary occurrences, source hashes, independent identities, selected
details attempts/raw references, context, actual timezone-file basis and rules.
Source/identity/paired/phase linkage and the entire snapshot are validated first.
Mixed route snapshots retain and validate supplied contexts through plan rebuilding;
no route selection/acquisition or route verdict is added. Corruption requires batch
correction; stale identity requires replay. Failed sends, wrong returned IDs, missing
timezone/hours and semantic provider defects remain source-linked visit UNKNOWN.

Current evidence uses the selected attempt's place-local request date. Applicable
current defects cannot be erased with regular hours. Original explicit empty periods
establish closed time; absence/null differs. Regular sentinel, split/overnight/week
rollover, optional components, literal dates/truncation and DST remain distinct.
Collection crossing local midnight only proves dated open spans; completeness remains
uncertain. A truncated final 23:59 endpoint does not establish the last minute's closure
or an infinite opening. Special dates without usable current evidence stay UNKNOWN.

Any positive known-closure overlap yields FAIL, including partial evidence. Exact
half-open equality and zero grace remain binding. Conditional compliance uses
PASS/(PASS+FAIL); complete evidence and decisive verdict coverage are separate.
Unresolved role populations suppress full-scope percentages. Per-visit exact outside
seconds are null when incomplete; confirmed lower bounds and unknown portions remain.
Batch magnitudes are labelled observed per-visit subtotals, never a global-time union.
Unavailable evidence basis differs from the candidate/selected basis per date.

## Actual development sequence

- Initial scorer tracer was RED: missing `opening` module. The first attempted
  implementation regression then had 13 passed / 65 setup errors because the host's
  default temporary directory was inaccessible. A repository-local fresh basetemp
  was used; its missing parent and a fixture's omitted `max_sends` were corrected.
  The baseline scorer plus existing time/requirement regression passed **78 tests**.
- Provider presence/regular parser slice: **9 failed / 4 passed** before correction,
  then **13 passed**. Defects included absent/invalid periods conflation, malformed
  endpoint batch failure, missing-close/sentinel handling and boolean clocks. A
  fractional overrun exposed float subtraction residue; complement spans and integer
  microsecond measurement now preserve the exact one-microsecond FAIL.
- Current applicability/partial closure/special date slice: **6 failed / 15 passed**,
  then **21 passed**. Timezone/context/population slice: **7 failed / 21 passed**,
  then **28 passed**. Cross-date/DST/time regressions passed **53 tests**.
- CLI tracer was RED for the missing module, then passed its deterministic/no-socket/
  source-immutability test. Snapshot linkage slice exposed a corrupt route leg:
  **1 failed / 56 passed**, then **57 passed** after whole-plan linkage reconstruction.
- Expanded endpoint and CLI checks: **1 failed / 73 passed** exposed contradictory
  date/weekday narrowing of unknown scope. Corrected to require consistent dates and
  weekdays before bounded completeness. Evaluation regression: **309 passed / 1 skipped**.
- Final basis/empty-scope slice: **2 failed / 74 passed**, then opening scorer/CLI
  **82 passed**. Unusable candidate fields now retain selected basis while reporting
  factual basis unavailable; empty applicable scope reports N/A and unavailable rates.
- Ruff passes for the evaluator and evaluation tests after import/format corrections.
  Test counts overlap across runs and are not summed into a fictitious acceptance total.

Exact temporary run directories were `.scratch/ticket06-testtmp/run01` through
`run22`; they contain generated synthetic material, not live evidence, and are removed
after the passed final gate. The full gate used the sibling `full-final` directory. The first RED used pytest's default temp/cache path; subsequent
runs use `-p no:cacheprovider --basetemp <fresh-path>` and
`TRIPWORLD_TEST_DATABASE=0`. Source tests are under `backend/tests/evaluation/`.

## Final gate and review

Standards initial review found one current-state documentation inconsistency and one
low-priority duplicate-date-validation heuristic. PROJECT's Ticket 06 row is now aligned
with the implemented state, and `_point` reuses `_date`. Follow-up Standards review: clear.

Spec initial review found one P2: a prior-week DST endpoint error erased closed evidence
on an unrelated date. Public scorer RED reproduced the Wednesday case (run19), then
specialty/time retest passed 97 tests (run20). Follow-up review found the same defect at
a half-open midnight end: run21 had 1 failed / 1 passed. The actual occupied last date
now uses end minus one microsecond. Related DST/cross-date regressions passed 11 tests
(run22), and Spec re-review confirmed the original cases plus preserved UNKNOWN for
an affected overnight DST gap. No remaining Standards or definite Spec findings.

Ruff on all backend code, backend compilation and `git diff --check` passed. Checked
194 local Markdown targets with no missing files and verified English Ticket 06 source,
tests and documents. These are development checks; no static typechecking was performed.
Final full backend regression: **2148 passed, 10 skipped in 149.88 seconds**.
Command: `.venv/Scripts/python.exe -m pytest backend/tests -q -p no:cacheprovider
--basetemp .scratch/ticket06-testtmp/full-final --tb=short`, with
`TRIPWORLD_TEST_DATABASE=0`. Skips are the disabled opt-in database tests and the
Windows symlink-privilege case. The full gate passed on its first final run after
review corrections. No claim of live V0-V3 execution follows; their planner code and
independent script entry points are unchanged and existing offline regressions passed.
The final CLI help check also passed. No separate static typechecker was installed.
Review fixed point is the handoff HEAD above; the review includes working-tree diff
and new untracked source/test files because the user prohibited commits. No separate
static typechecker is configured; compilation is not a typecheck.

## Tracker and limitations

GitHub CLI returned HTTP 401; the connected GitHub tool read #18 and its comments,
then appended the approved implementation checkpoint without rewriting imported history.
Detailed current contracts and code are local/unpublished. The final Issue acceptance/state update follows this passed gate; its confirmation
is recorded below. Dependency #16 is retained. No coordination reply was sent.

Offline synthetic fixtures do not establish actual Google field availability, future
venue access, historical correctness, bookings, evidence authenticity or operational
transport/retention suitability. Hashes establish supplied material linkage and integrity.
No Google/model/database service or live evidence was used. Routes, auxiliary total,
blind artifacts, Repair comparison and Ticket 07+ remain outside this task.


## Final tracker and workspace confirmation

GitHub #18 was updated with the self-contained accepted scope, test/review sequence and
local/unpublished evidence disclaimer, then closed with `state_reason=completed`.
The connected tool confirmed the resulting closed/completed state; the final read-back
confirmed it. Imported history and completed predecessor #16 were preserved. Only #18
was mutated; no parent/dependency/other-ticket task expansion or coordination reply.
Generated `.scratch/ticket06-testtmp/` was removed after verifying its resolved absolute
workspace-contained root. No source fixtures or user materials were removed. HEAD and
branch remain unchanged; all Ticket 06 changes and inherited preflight documents are
local/uncommitted, with no staged changes, commit or push. The ignored thesis archive
records observed facts, corrections and the final bounded validation; it is not authority.
Stop at Ticket 06. Ticket 07+ requires the next human instruction.
Final closeout document check: 197 local Markdown targets exist; English content passed.
V0-V3 script entry points exist, and the generated test root is absent.


## Subsequent approved database/permission verification — 2026-10-02

After Ticket 06 closeout, the user stated that the database was running and approved
execution of checks previously blocked by permissions. This extends validation only to
isolated local PostgreSQL and the skipped symlink check; no provider/model call,
production database operation, formal evaluation, commit/push or later ticket is added.
The original 2148-pass/10-skip offline checkpoint above remains historical and unchanged.

The ten previously skipped checks were selected, rather than repeating the 2148 passing
checks. Outside-sandbox execution was granted. Initial supplement: 9 database setup
errors because the test process lacked TRIPWORLD_DB_PASSWORD; 1 symlink check still
skipped for native Windows privilege. Credentials were then loaded from the existing
.env.tripworld into the test process only, with loopback host validation and database
name forced to tripworld_test. Credentials were not printed or changed. The existing
fixture asserts that database name before resetting its test schema; production was
not targeted. External provider factories in these tests are fake/forbidden.

Database supplement: **8 passed, 1 failed (8.50s)**. The failure referenced the old
backend/app/tripworld/database/migrations path, before reaching the checksum assertion.
Only that test's path was corrected to tools/data/tripworld/migrations/001_retrieval.sql,
matching the migration runner's current file. Targeted checksum retest: **1 passed
(0.70s)**; Ruff passed and the one-line diff was reviewed. All nine identified database
checks have now passed across these scoped runs. No additional full-suite run was made;
do not relabel this as a single combined full-suite result.

The symlink check remains skipped even outside the sandbox. Execution approval does
not grant Windows SeCreateSymbolicLinkPrivilege or enable Developer Mode. No OS security
setting, privilege or UAC configuration was changed. This is the one remaining native
host limitation, not a database or opening-scorer failure.

Generated supplementary basetemp directories and JUnit XML reports are removed after
recording these observed outcomes. Evidence owners are this record, the test source,
and the scoped command/output in the same Codex conversation. Code and docs remain
local/uncommitted; #18 stays completed, with this supplement disclosed separately.


## Subsequently authorized elevated symlink verification — 2026-10-02

The user explicitly approved the Windows permissions needed for symlink creation.
Inspection showed the outside-sandbox user was an administrator-group member with a
filtered, non-elevated token. A Windows UAC elevation launched only
backend/tests/evaluation/test_intake.py::test_link_escape_resolves_before_read in a
hidden PowerShell helper. No Developer Mode, persistent user right, registry setting,
UAC policy or OS security configuration was changed.

Observed result: the helper confirmed an elevated administrator token, pytest exited
0, and the test passed: **1 passed in 0.33s**. JUnit independently reported one test,
zero errors, zero failures and zero skips. The real symlink was created and the intake
path-escape rejection assertion executed; the test was not bypassed or modified.
Together with the preceding nine database checks, all ten originally skipped checks
have passed across scoped supplementary runs. The historical full-suite checkpoint
remains **2148 passed, 10 skipped**; no new combined full-suite result is claimed.

Revision: ed4c9a9d4724263925748588878eadc22d21978a on feature/evaluation, with the existing
uncommitted Ticket 06 implementation/docs and the preceding migration-test path fix.
This supplement changes documentation only. Evidence is the scoped command/output in
this Codex conversation and the unchanged symlink test source; the temporary helper,
log, result JSON, JUnit XML and basetemp directory are removed after recording results.
No database/provider/model call, formal evaluation, commit/push or later-ticket work
was performed in this supplement. Issue #18 remains completed.

The non-elevated cleanup initially could not remove the administrator-created basetemp
directory. A second UAC-elevated helper removed only that exact validated scratch root;
its result confirmed removal and a subsequent existence check returned false. The
cleanup helper and result file were then removed. No temporary artifacts remain.


## Local Git closeout preparation — 2026-10-02

The user authorized Ticket 06 workspace cleanup, documentation/archive/Issue updates
and local commits. Under AGENTS.md, the logical commit grouping must be approved before
creating commits. Proposed groups:

1. feat: add offline opening-hours evaluation — scorer, private parser, CLI, neutral
   preparation/time integration and their directly related tests.
2. test: fix TripWorld migration checksum fixture path — the independent one-line
   stale test-path correction identified during the approved database supplement.
3. docs: record RTPEval opening evaluation acceptance — contracts, preflight, this
   acceptance record, package guide, PROJECT and documentation index/design.

A fresh closeout regression selected all evaluation tests and database unit tests while
deselecting the ten already-passed native/database checks:
**327 passed, 10 deselected in 39.01s**. No test failed or skipped in this run.
Backend Ruff, evaluation compilation and opening CLI help passed. Prior full-backend
and scoped database/symlink results remain separately recorded; no totals are combined.
No new full-suite, database, provider/model or formal evaluation run occurred.

PROJECT's current authorization section was consolidated without rewriting historical
acceptance records. The documentation index now distinguishes preflight from completed
implementation. Parent #12 was synchronized to Tickets 01-06 completed, while #18 stays
closed/completed. Tracker records explicitly distinguish local commit preparation from
remote publication. Ticket 07 remains unimplemented and unapproved.

Revision at preparation: ed4c9a9d4724263925748588878eadc22d21978a, feature/evaluation,
plus the approved uncommitted Ticket 06 changes and one database-test correction.
The generated closeout basetemp directory is removed after recording results. Ignored
thesis notes remain local and are not force-added. No credentials, source payloads,
runtime logs or generated files are included in the proposed commits. Commit grouping
approval/execution remains pending; no push, branch switch or version freeze is included.

Final preparation checks: exactly 20 intended code/test/document files and an empty
index; no ignored files proposed for staging; 198 local Markdown targets exist;
English/private-key-marker and diff checks passed; V0-V3 entry points exist and generated
Ticket 06 test roots are absent. All three extracted Ticket 05 preparation helpers are
AST-equivalent to HEAD. Read-back confirms #12 open with Tickets 01-06 completed and
#18 closed/completed with pending Git closeout clearly disclosed.


## Approved local commit closeout — 2026-10-02

The user explicitly approved the three proposed commit groups after reviewing the
prepared scope and passing checks. Local commits on feature/evaluation:

- ee085d3e1286990595c842eb44abf6fe88b79ad4 — feat: add offline opening-hours evaluation.
  Ten implementation/integration/direct-test files; the extracted Ticket 05 helpers
  are AST-equivalent to the previous HEAD and cross-date normalization remains opt-in.
- f62c07f6ed2034e223ef5951cb5a0655d9739b20 — test: fix TripWorld migration checksum fixture path.
  One test-only file; no database implementation or credential change.
- docs: record RTPEval opening evaluation acceptance — nine contracts, preflight,
  acceptance, PROJECT, package-guide and documentation-index/design files. This record
  accompanies that third commit; its own hash is available in Git history and tracker
  closeout rather than embedded recursively in its contents.

The implementation and supplementary test results are unchanged: original full backend
2148 passed / 10 skipped; the nine database checks and one real UAC symlink test passed
in separate supplements; final closeout subset 327 passed / 10 deselected. Ruff,
compilation, CLI, English/document-link and diff checks passed. No code/test behavior
changed after that verification; subsequent changes only record approval and commits.

The implementation baseline remains ed4c9a9d4724263925748588878eadc22d21978a; earlier
pending/no-Git statements above are preserved historical checkpoints. Only the twenty
approved code/test/document files enter these three commits. The ignored local research
archive remains excluded, with no force-add. Generated test files were removed.
Issue #18 remains completed and parent #12 records Tickets 01-06 completed; tracker
closeout will identify all three actual local hashes and unpublished availability.

No push, branch switch, version freeze, formal evaluation, real provider/model call or
Ticket 07+ execution is included. Ticket 07 specification closure remains the proposed
next task and needs separate approval.
