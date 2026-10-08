# Opening

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="rtpeval-ticket-06-acceptance"></a>

<a id="rtpeval-ticket-06-acceptance--ticket-06-offline-opening-acceptance"></a>

## Ticket 06 offline opening acceptance

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

<a id="rtpeval-ticket-06-acceptance--authority-and-implemented-boundary"></a>

### Authority and implemented boundary

[PROJECT](../../../PROJECT.md) and [approved preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18#issuecomment-5955697757) own
scope; [opening](../../contracts/0004-opening-routes.md#rtpeval-opening-contract), [time](../../contracts/0001-evaluation-artifacts.md#rtpeval-evidence-time-contract),
[snapshot](../../contracts/0002-intake-identity-usage.md#rtpeval-snapshot-contract) and [metrics](../../contracts/0005-quality-human-review.md#rtpeval-metrics-contract) own meaning.
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

<a id="rtpeval-ticket-06-acceptance--actual-development-sequence"></a>

### Actual development sequence

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

<a id="rtpeval-ticket-06-acceptance--final-gate-and-review"></a>

### Final gate and review

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

<a id="rtpeval-ticket-06-acceptance--tracker-and-limitations"></a>

### Tracker and limitations

GitHub CLI returned HTTP 401; the connected GitHub tool read #18 and its comments,
then appended the approved implementation checkpoint without rewriting imported history.
Detailed current contracts and code are local/unpublished. The final Issue acceptance/state update follows this passed gate; its confirmation
is recorded below. Dependency #16 is retained. No coordination reply was sent.

Offline synthetic fixtures do not establish actual Google field availability, future
venue access, historical correctness, bookings, evidence authenticity or operational
transport/retention suitability. Hashes establish supplied material linkage and integrity.
No Google/model/database service or live evidence was used. Routes, auxiliary total,
blind artifacts, Repair comparison and Ticket 07+ remain outside this task.


<a id="rtpeval-ticket-06-acceptance--final-tracker-and-workspace-confirmation"></a>

### Final tracker and workspace confirmation

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


<a id="rtpeval-ticket-06-acceptance--subsequent-approved-databasepermission-verification--2026-10-02"></a>

### Subsequent approved database/permission verification — 2026-10-02

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


<a id="rtpeval-ticket-06-acceptance--subsequently-authorized-elevated-symlink-verification--2026-10-02"></a>

### Subsequently authorized elevated symlink verification — 2026-10-02

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


<a id="rtpeval-ticket-06-acceptance--local-git-closeout-preparation--2026-10-02"></a>

### Local Git closeout preparation — 2026-10-02

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


<a id="rtpeval-ticket-06-acceptance--approved-local-commit-closeout--2026-10-02"></a>

### Approved local commit closeout — 2026-10-02

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

<a id="opening-access-boundary-proposal-2026-10-09"></a>

## Opening access boundary proposal — 2026-10-09

Status at the #88 checkpoint: advisory, not implemented or an authorization for evidence
acquisition. The subsequent [#89 acceptance](#regular-opening-fallback-acceptance-2026-10-09)
supersedes the proposed provisional verdict with ordinary regular-basis PASS/FAIL and
implements regular fallback. Access-intent and business-status refinements remain proposals.
Prepared
alongside [#88](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/88), at local
implementation revision `2f9dd6f` with related documentation pending and an excluded
pre-existing `.gitignore` edit. The implemented requirement correction is recorded in
[its acceptance owner](intake-identity-usage.md#requirement-physical-association-correction-2026-10-09).

The preserved fresh Sydney evidence has fourteen opening UNKNOWNs and no opening FAIL.
All fourteen requested both current and regular hours; HTTP 200 omitted both fields.
The affected venues are Opera House, Harbour Bridge, Darling Harbour, Bondi Beach,
The Rocks and Powerhouse Museum. Powerhouse additionally has undated
`CLOSED_TEMPORARILY` status. A minute-level grace cannot resolve missing evidence;
neither a public-space name nor unspecified visit intent proves unrestricted access.

The official [Places resource reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places)
defines current hours over the request-local seven-day window, regular hours as typical
weekly hours, an always-open sentinel, and business status separately from current
opening. Missing fields do not establish closure or unrestricted access. Those API
semantics motivate the following proposed boundaries, rather than prove Sydney access:

| Proposed boundary | PASS support | FAIL / UNKNOWN boundary |
| --- | --- | --- |
| Indoor entry | Applicable entry hours contain the complete submitted visit | Proven closed interval: FAIL; missing/conflicting hours: UNKNOWN |
| Outdoor/public-area access | Independent evidence covers the actual area, access conditions and visit interval | Do not assume parks, beaches, bridges or districts are always open; unresolved access stays UNKNOWN |
| Date-specific evidence | Current or official dated hours cover the requested date and interval | Exceptions without applicable hours stay UNKNOWN |
| Regular weekly evidence | Explicit provisional PASS when relevant regular hours cover the interval and no known exception or closure conflicts | Label projected basis separately from date-verified PASS; do not inflate verified coverage |
| Closure status | Consider dated closure evidence before positive hours | Applicable dated closure: FAIL; undated temporary closure blocks confident PASS and retains `closure_dates_unresolved` |

Visit/access intent should be recorded from original output or reviewed requirements
(`indoor_entry`, `outdoor_area`, `unspecified`) before scoring. An unspecified Opera
House visit must not be silently converted to an exterior walk to obtain PASS. A
separate official-evidence fallback can normalize applicable periods/closure dates with
URL, captured content hash, retrieval time, timezone, area and validity dates; evaluator
LLMs must not invent missing access facts.

Keep full-interval containment as the default entry check. Arrival-only access is a
different metric; if tolerance is introduced later, expose the configured allowance and
outside-interval seconds. Distinguish `hours_missing`, `access_scope_unresolved`,
`exception_hours_missing`, `closure_dates_unresolved` and `evidence_conflict` in reports.
Keep outcome, evidence basis and verified coverage separate. Exact schema, aggregation
and acquisition changes require a separately approved implementation scope.

<a id="regular-opening-fallback-acceptance-2026-10-09"></a>

## Regular opening fallback acceptance — 2026-10-09

Status: implemented and offline validated under
[#89](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/89). Review fixed base:
`fb517bbd6e122432e852f593fd0ccf26ec25adca`; implementation/test commit: `4043dba`.
Related final documentation is a separate coherent group. The pre-existing `.gitignore`
edit was excluded and retains its original bytes.

### Approved boundary and implementation

The user clarified that valid regular hours should determine PASS/FAIL unless evidence
applicable to the planned visit establishes an exception. An overnight query returning
`openNow=false` describes that instant, not later visit feasibility. This supersedes the
earlier provisional-PASS proposal. Google separately defines query-time `openNow`,
seven-day current schedules and temporary business closure in its
[official resource reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places).

`rtpeval_opening_rules_2` retains usable applicable current open/closed intervals and fills
only unresolved time with regular hours. Missing/null/malformed current fields, uncertain
collection dates and truncated boundaries can fall back; current established closure
still yields FAIL. Special markers and parsing defects remain diagnostic rather than
vetoing regular evidence. The actual adopted fields and fallback scope/open/closed spans
are visible in `basis_segments`. Source/timezone validation, local date/window bounds,
whole-interval zero grace, invalid-clock UNKNOWN and independent identity replay remain.
Undated business status, exterior access and new evidence collection are outside this fix.

### Failure, correction and checks

At the approved `score_opening` seam, three current-field defect cases first reproduced
UNKNOWN instead of the expected regular-basis PASS. Minimal fallback made all three pass.
The next marker-only regression reproduced UNKNOWN, then passed after removing that veto
and retaining a marker diagnostic. A mixed-interval provenance regression first failed
because the new fields were absent. After implementation, its expected span fixture needed
the existing `seconds` field; correcting that expectation completed the test.

The initial wider opening gate passed 83 tests and failed two former-policy expectations:
the final truncated minute and undated current evidence across collection midnight were
now decided from regular hours. Their assertions were updated to the approved policy,
retaining current diagnostics and actual mixed/regular basis. Added guards cover null and
invalid current payloads, malformed markers, regular FAIL, partial-current provenance,
preserved current closure and partial evidence without usable regular fallback.

The final scorer/actual CLI gate passed **96** tests. The actual CLI verifies the Sydney
02:00 query against a 10:00-11:00 visit: regular 09:00-17:00 gives PASS despite
`openNow=false`; explicit applicable current empty periods gives FAIL; absent schedules
stays UNKNOWN. Repeated CLI output is identical and socket access/source mutation is
blocked. The full backend gate passed **3124 tests, 10 skipped** in 287.56 seconds.
Ruff, changed-file formatting and diff checks passed. Independent Standards and Spec
reviews of the committed implementation each reported zero findings.

### Original-source recalculation and historical replay

The public opening CLI ran twice with identical output; the quality CLI also completed,
all exit 0. DNS/socket connection attempts were blocked and remained zero. Preparation
verification before/after and receipt hashes preserved all four original outputs, the
original report and all 205 receipt files. The separate opening report identifies rules
version 2; it does not replace the original acquisition or its receipt.

All fourteen real opening UNKNOWNs still lack both requested hours fields. Original
opening state/basis/time magnitudes are unchanged. All quality dimensions, density and
overall scores match the accepted #88 recalculation: V0 89.2857, V1 68.0000, V2 75.0000,
V3 81.1111. No missing facts were inferred and no additional provider/model cost occurred.
An isolated process loaded the trusted original opening parser/scorer and requirement
scorer from `ee0f4947edb32fe2f7a07f5b4fd7c1ee98fd6531`; formal CLI replay reproduced the
original report exactly with zero network attempts and no checkout mutation.

Local evidence identifiers, not published dependencies:
`artifacts/sydney-opening-policy-recalculation-20261009-r1/{opening.json,quality.json,recalculation-check.json,original-rules-replay-check.json}`.
The source package remains `artifacts/sydney-fresh-evaluation-preparation-20261009-r1/run`.

| Material | SHA-256 |
| --- | --- |
| Original report, unchanged | `09272f235cadc20aeb94f4c6a4f5945f35a77faaf89637611beb422695e0b459` |
| Original receipt, unchanged | `ca5852385f6fcdeb1279afbb25ddfdc8da8d11a64514836b88bf824406bae0e1` |
| Rules-2 opening report | `7fbd06aa0bd789484162bde710a4caab555fbf2bc173f69a50f3c25d27f53471` |
| Current quality recalculation | `b8e9b3328680e137c2b078acb5850e53e6ead621285d5bf7ccfd23f4ff0695d3` |

### Current project-state maintenance

PROJECT.md had grown to 858 lines, with repeated run approvals, intermediate failures,
request/cost inventories, commit histories and superseded claims labelled latest/current.
It now keeps current version mechanisms, capability/contract navigation, one latest
validation checkpoint, the current Sydney integration result, limitations and authorization
boundary. Execution details remain in their existing dated record owners; the full former
state is retained in Git at the fixed base. Removed historical statements do not renew
old allowances or obscure current acceptance. No new chronological task paragraph is
appended to the concise current-state file.

This correction includes no new access-intent schema, official evidence collector, planner
change, formal comparison, provider send, push, PR, merge, branch switch or version freeze.

<a id="missing-hours-access-acceptance-2026-10-09"></a>

## Missing-hours access assessment — 2026-10-09

[Issue #90](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/90) owns the
approved offline implementation. Review fixed point:
`8c687f162db4fd762239e4ffce054c76f0610564`. The user approved public `score_opening`
and actual preparation/import/execution/replay CLI seams, and requested medium reasoning.
Implementation/tests are committed as `40fe066`, with review correction `017c548`;
no paid execution or Git publication
is included. The existing unrelated `.gitignore` bytes retain SHA-256
`fdc63780f304bde2f8ac48b7e520330bc45254e8799cb4323cfe645c82a3ae02`.

### Behavior and evidence meaning

Validated `llm_access_reasonableness_1` material selects opening rules 3 and quality
profile `rtpeval_access_quality_3`; API-only scoring retains rules 2 and its original
profile. All four versions use the same public/exterior access standard. Existing
V1-V3 identity/requirement policies remain deterministic. No planner behavior changes.

The model only assesses verified original occurrences with known time/timezone and
neither API schedule supplied. Missing/null hours or periods can qualify, including
query-time `openNow=false` alone. Explicit empty or supplied malformed/incomplete periods
are not replaced. The packet contains source-bound activity intent, independent venue
facts, interval/timezone and retained Details provenance; activity notes are claims,
not factual evidence. Complete structured decisions cite original text and classify
access mode, full-window reasonableness and applicable restrictions. Supported public
outdoor/exterior access can PASS; indoor/ticketed/ambiguous or unsupported access stays
UNKNOWN. The model cannot repair an original activity, manufacture hours or override
an API-decided visit. Semantic model judgments remain fallible.

Model PASS contributes to ordinary verdict scoring with an explicit model basis.
Factual hours coverage, known-open/outside/unknown seconds and grounding FAILs remain
unchanged. Separate model-assessed/decidable counts identify the broader judgment basis.
Raw request/response, model/prompt/policy/source hashes, ordered timestamps and actual
token counts are retained. Import rebuilds the packet and rejects partial, foreign,
stale, unsupported-quote and inconsistent model material.

Incremental execution verifies the completed parent receipt/originals and replays identity,
then reuses saved Google evidence. Its separately approved digest permits one model
request, medium effort and zero retries under explicit token/time/reference-price limits.
Both completed and stopped attempts save captured HTTP/material, usage and receipts.
Full report replay validates those bytes and sends nothing. Incremental costs are distinct
from parent Google/V0 identity costs; actual billing remains unavailable.

### Validation sequence

The first public slice failed because the preparation CLI was absent. Initial eligibility
used an incorrect interval-status name, then a synthetic description field outside the
actual projection; these were corrected to the existing `known` interval and original
`notes` schema. The public walk then passed while API known-open seconds stayed zero
and its 3600 unknown seconds remained unchanged.

CLI integration first failed on the missing command. Its fixture initially omitted the
V1-V3 submitted IDs; supplied `pid-a`/`pid-b` restored the existing identity contract.
Blocking every socket before an asyncio execution also blocked Windows' local event-loop
pipe; the dispatch-reuse check was moved before the socket prohibition, while import
and synchronous replay still prohibit socket construction. No outbound network was used.

The query-instant regression reproduced an empty eligible cohort with `openNow=false`
and absent periods. Eligibility now inspects actual schedule absence rather than rejecting
the mere hours-object presence. Missing/malformed material, indoor/ticketed/unreasonable
PASS attempts, invalid identity/time, API closure priority, original quotes, complete
coverage, failed HTTP, missing usage, one-use approval and immutable receipts are covered.

Initial full backend gate: **3150 passed, 1 failed, 10 skipped** in 316.34 seconds. The
architecture import allowlist had not registered the approved isolated `opening_run`
HTTP entry; the scorer/import modules remained offline. The allowlist was extended for
that execution module only. Binding/intake/quality retest: **225 passed, 1 skipped**.
Implementation full backend gate: **3151 passed, 10 skipped** in 332.00 seconds. Public opening
and formal-flow integration gate: **136 passed**; final new fallback suite: **27 passed**.
Ruff, formatting of all thirteen changed code/test files and diff checks pass.
The broader format scan also reported existing mixed-line-ending files outside this task;
those unrelated files were left unchanged. No typechecker gate is configured.

Standards initially found zero actionable issues; Spec found one P2: standalone
preparation/import omitted implementation hashes although incremental execution retained
them. The public scorer regression first failed on absent `implementation_hashes`.
Correction `017c548` adds all evaluator source SHA-256 values to every packet; import
rebuilds and compares them. Current complete evaluator gate after that correction:
**1216 passed, 1 skipped** in 228.81 seconds. This is distinct from the pre-correction
full-backend checkpoint above, not another full-backend run. Both independent rechecks
found zero remaining issues. No shared planner/generation code changed.

### Real-source preparation and historical protection

The same four original Sydney outputs produce **14 eligible occurrences**: V0 2,
V1-V3 4 each. No real model decisions are imported or fabricated; accepted scores and
fourteen UNKNOWNs remain the API-only checkpoint until separately approved execution.
For example, V0 Opera House notes explicitly assume no tour/interior access, whereas
its Powerhouse activity describes exploring the museum. Eligibility alone is not PASS.

Final local preparation identifier: `artifacts/sydney-opening-access-preparation-20261009-r2`;
its `run/preparation.json` digest is
`d2db8c5b37d99042e958210b99546edb3a4db92718772159ac357d87351f604c`.
It supersedes the initial r1 draft after the implementation-binding correction.
Complete wire estimate plus 1024-token margin is 17254 tokens. Proposed ceilings:
32000 input tokens, 8000 output tokens, zero Google sends, one model send and zero
retries. The retained 2026-10-09 price snapshot yields USD 0.008 at those maximum token
allowances; proposed USD reference allowance is 0.05. These are reference/proxy amounts,
not actual billing or live authorization; the retained price validity ends 2026-10-10.
Actual incremental provider/model sends and incurred charges are zero. Original parent
execution costs are not erased or counted again. Raw artifacts remain ignored local aids.

An isolated historical CLI replay loads trusted parser/opening/requirement/quality/run
modules from `ee0f4947edb32fe2f7a07f5b4fd7c1ee98fd6531`. It reproduces the original
complete report exactly with zero network attempts and no checkout mutation. All 205
receipt-covered files and original source bindings remain unchanged. Original report
SHA-256: `09272f235cadc20aeb94f4c6a4f5945f35a77faaf89637611beb422695e0b459`;
receipt SHA-256: `ca5852385f6fcdeb1279afbb25ddfdc8da8d11a64514836b88bf824406bae0e1`.

Real model assessment and its final recalculated report remain a separate execution
approval. This record claims offline engineering readiness, not resolution of every
missing fact, a formal version comparison, publication, freeze or new live allowance.

### Authorized live assessment and final report acceptance

After the offline checkpoint, the user explicitly authorized the prepared package on
2026-10-09 (Australia/Sydney). Execution used source revision `eee95c6`, with only the
pre-existing unrelated `.gitignore` modification; its bytes remained unchanged. Under
the smoke policy, a current-session GPT-6.1 Sol child at medium effort executed the frozen
CLI once. The evaluator deployment itself was `gpt-6-luna`, also at medium effort.
Neither agent changed implementation, original itineraries or retained Google evidence.

Approved digest: `d2db8c5b37d99042e958210b99546edb3a4db92718772159ac357d87351f604c`.
Limits were zero Google sends, at most one model send, zero retries, 32000 input tokens,
8000 output tokens, 120 seconds per request, 900 seconds overall and USD 0.05 reference
allowance. The saved price window was valid through 2026-10-10. The actual invocation
returned HTTP 200 and CLI exit 0, with processing/acquisition complete and evidence unresolved.
Request time was 2026-10-09 04:59:24.421839 to 04:59:42.998055 Sydney time (18.576 seconds).
Actual sends: **0 Google, 1 model, 0 retries**. Actual response usage: **15530 input,
2709 output, 18239 total tokens**, with zero cached reads and 15527 reported cache-write
input tokens. Saved-price incremental estimate: **USD 0.003295675**; account billing
remains unavailable. Parent acquisition costs stay in the original report and are not repeated.

All fourteen eligible occurrences received complete source-bound judgments. Eight PASS
with model basis; six remain UNKNOWN. Dates and times below are original Sydney intervals.

| Reference | Version | Original activity | Date/time | Verdict | Assessment reason |
| --- | --- | --- | --- | --- | --- |
| visit001 | V0 | Sydney Opera House | Oct 14, 10:00-12:00 | PASS | Original notes explicitly exclude tours/interior access and describe building/harbour appreciation. |
| visit002 | V0 | Powerhouse Museum | Oct 17, 10:00-12:15 | UNKNOWN | Exploring the museum implies indoor admission. No hours establish entry; undated temporary closure does not prove future closure or availability. |
| visit003 | V1 | Sydney Opera House | Oct 14, 10:00-11:30 | UNKNOWN | Building name and missing-hours note do not establish exterior rather than indoor access. |
| visit004 | V1 | Sydney Harbour Bridge | Oct 14, 12:15-13:15 | UNKNOWN | Generic bridge name does not distinguish viewing, crossing or a paid climb. |
| visit005 | V1 | Darling Harbour | Oct 15, 13:30-14:30 | PASS | Public waterfront visit with a reasonable daytime interval; no specific indoor/paid activity is stated. |
| visit006 | V1 | Bondi Beach | Oct 17, 10:00-11:00 | PASS | Outdoor beach visit without a swimming commitment; drizzle affects comfort rather than establishing access closure. |
| visit007 | V2 | Sydney Opera House | Oct 14, 10:00-11:30 | UNKNOWN | Generic visit and conditional interior-access note leave the access mode unresolved. |
| visit008 | V2 | Sydney Harbour Bridge | Oct 14, 12:30-13:30 | PASS | Original notes specify a landmark and harbour-view stop, supporting exterior viewing. |
| visit009 | V2 | The Rocks | Oct 14, 14:30-15:45 | PASS | Exploring the named urban district supports an outdoor neighborhood visit. |
| visit010 | V2 | Darling Harbour | Oct 16, 14:00-15:30 | PASS | Spending time in the public waterfront area has a reasonable interval. |
| visit011 | V3 | Sydney Opera House | Oct 14, 10:00-11:30 | UNKNOWN | Generic building visit does not establish exterior rather than indoor access. |
| visit012 | V3 | Sydney Harbour Bridge | Oct 14, 12:30-13:30 | UNKNOWN | Generic visit and unconfirmed access details leave viewing/crossing/climb intent unresolved. |
| visit013 | V3 | The Rocks | Oct 14, 14:15-15:45 | PASS | Exploring the named district supports an outdoor neighborhood visit. |
| visit014 | V3 | Bondi Beach | Oct 17, 10:30-12:30 | PASS | Outdoor beach visit without a swimming commitment; the daytime duration is reasonable. |

These are model reasonableness judgments, not independently certified opening schedules.
All six UNKNOWNs have plausible durations; the unresolved issue is access mode or indoor
availability. Generated weather notes were not adopted as independent weather facts.
The remaining automatic UNKNOWN inventory contains exactly these six opening checks.

The parent independently ran the actual `replay-opening` CLI with socket creation and DNS
resolution prohibited. Exit 0 and exact JSON equality reproduced the complete report;
network attempts were zero. Original source hashes and all **205** parent receipt-covered
files passed verification. The new closed execution receipt also passed verification.
A separate offline API-only baseline under the current implementation confirmed identical
identity, requirement/schedule and route reports. All opening evidence statuses, API basis
segments and known-open/outside/unknown seconds remained identical; unassessed opening
checks were unchanged. This isolates the access-judgment effect without rewriting history.

| Version | Final overall score | Opening PASS / UNKNOWN | Grounding FAIL |
| --- | ---: | ---: | ---: |
| V0 | 92.1429 | 6 / 1 | 0 |
| V1 | 72.0000 | 8 / 2 | 2 |
| V2 | 82.5000 | 7 / 1 | 0 |
| V3 | 85.5556 | 7 / 2 | 0 |

Hard Opera House exact-once obligations, non-overlap and applicable route checks remain
PASS in every version. Two V1 grounding FAILs remain `api_address_mismatch`: Harbour
Bridge (Oct 14) and Australian National Maritime Museum (Oct 15). Six existing auxiliary
pace FAILs also remain: V0 Oct 17 (one primary visit); V1 Oct 14/16 (three each);
V2 Oct 14 (three) and Oct 17 (one); V3 Oct 14 (three). These reflect the existing relaxed
pace heuristic and soft penalties, not newly inferred hard quotas or opening failures.
No additional hard-check FAIL or non-opening UNKNOWN appeared. Agent inspection is not
genuine human review; acceptance here verifies execution, binding, accounting and policy
application, while final human agreement on residual judgments remains separate.

Local evidence identifier: `artifacts/sydney-opening-access-preparation-20261009-r2`.
`execute-opening.stdout.json`, `execute-opening.stderr.txt` (empty) and
`execute-opening.exit.json` retain dispatch results outside the closed receipt.
`run/execution/` retains the raw HTTP, model material, usage, final report and receipt.
`replay-opening.stdout.json`, `current-api-only-report.json` and `acceptance-audit.json`
retain independent offline acceptance. These identifiers are ignored local evidence,
not published-document dependencies. An initial audit helper failed to resolve the
repository import path, then its inspection failed on the Windows default text codec;
using the repository root and explicit UTF-8 corrected both local inspection issues.
No provider request was repeated.

| Artifact | SHA-256 |
| --- | --- |
| Final report | `71a60426d3296c97fc10d6e8cdb7376a68c8351f20d5462653580ee4ccfe2ebc` |
| Incremental receipt | `0f3b77f03e011b5a2f50bc678a15f048da013a8a9b460f972636ce30c40dbe6c` |

The authorized one-use package is consumed. This engineering smoke demonstrates the
four-original automatic evaluation path through real assessment and offline replay,
including explicit FAIL/UNKNOWN results. It does not authorize another live attempt,
itinerary repair, official evidence acquisition, formal benchmark, version ranking,
freeze, push, PR, merge or branch switch.
