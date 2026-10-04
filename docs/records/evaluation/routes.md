# Routes

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="snapshot-coordinate-bridge-2026-10-03"></a>

## Snapshot-coordinate bridge — 2026-10-03

Review fixed point: e8e75b01307fc5ecc39910262249a4cceb5dbaea on feature/evaluation;
the starting tracked tree was clean. The user adopted the preceding audit recommendation,
authorizing a bounded offline coordinate bridge, relevant tests, local commits, dual-axis
review/corrections and related documentation. No live acquisition or publication is included.
Current behavior is owned by the [opening/route contract](../../contracts/0004-opening-routes.md#accepted-snapshot-coordinate-extension-2026-10-03).

### Reproduction and implemented boundary

The audit's three public probes showed 8 resolved visits but no route query context without
a separate coordinate envelope. Preparing already-saved coordinates yielded 1 V0 context
without any additional send. Existing relevant tests passed 48 cases (67 unrelated cases
deselected). These fixtures establish a missing preparation bridge, not live coverage or
a scoring defect. Source/raw preservation and manual route preparation already worked.

`prepare_snapshot_coordinates` now replays an identity-phase snapshot, recomputes its intake
plan and verifies derived evidence against the adopted identity report. Only exact adopted
IDs contribute coordinates. Its immutable `rtpeval_snapshot_coordinates_1` output preserves
manifest/plan/intake/identity hashes and each request/raw hash, candidate pointer and retrieval
time. It declares independent_snapshot provenance without inventing human review metadata.
Finite/ranged agreeing coordinates are usable; missing, malformed or contradictory points
remain local diagnostics, retaining candidate populations. Foreign/corrupt/stale sources
reject preparation atomically. Unresolved identities stay unresolved.

Route prepare/score and the final quality-report API/CLI accept optional
identity_snapshot_directory / --identity-snapshot. Existing reviewed --coordinates remains
supported; selecting both sources is rejected. Automatic extraction uses existing default
query options. Manual and automatic evidence digests differ, so replay uses the corresponding
prepared query plan rather than borrowing an old query. Planner runtime, budgets, provider
field masks, acquisition policy, source IDs and final score/mask rules remain unchanged.

### Actual development validation

1. Initial test setup could not create a nested basetemp because its parent did not exist.
   Creating only the ignored task artifact parent enabled the actual red test.
2. Snapshot-to-route preparation initially failed at the missing keyword interface, then
   passed with linked extraction. Four malformed-coordinate cases then failed; local
   invalid diagnostics fixed them without dropping the unaffected place.
3. Conflicting repeated coordinates incorrectly produced a query; the regression failed,
   then passed after exact agreement checks. Matching duplicates remained accepted.
4. Route CLI, route scoring, quality-report API and quality CLI each failed at the missing
   interface before being connected. A scoring fixture initially omitted independent mode
   review and therefore produced UNKNOWN; supplying its existing review made the intended
   PASS assertion valid without a production scoring change.
5. Additional public checks cover corruption/linkage, absent coordinates, paired optional
   tracks, Search/Details agreement, source-only provenance, competing source inputs,
   unadopted IDs, unresolved identities, deterministic no-socket replay and unchanged bytes.
   A huge out-of-range integer exposed OverflowError in the finite-number check; checking
   range first fixed the reproduction and retained local coordinate uncertainty.
6. Complete evaluator regression: 527 passed, 1 Windows symlink-privilege skip in 85.14s.
   All 25 new cases participate; existing reviewed-coordinate/quality behavior remains
   covered. Ruff and six-file format checks pass; no static typechecker is configured.

Complete backend gate: 2356 passed, 10 skipped in 198.85s, no deselections. Nine opt-in
PostgreSQL tests and one Windows symlink privilege test were skipped; no database supplement
or native elevation was run. Implementation and direct tests were committed before review:
f07b495 — feat: prepare route coordinates from independent snapshots.

Standards review reported 0 hard violations and 0 actionable smells. Spec review found one P2:
Search `places: null` was unavailable in converted identity evidence but raw coordinate
iteration raised TypeError, wrongly rejecting the whole batch even with valid Details.
The public route-preparation regression first failed (1 failed / 25 deselected), then passed
after filtering requests by the existing converted observation status. Valid Details and
other places remain usable; malformed Search evidence remains in the original snapshot.
All 26 coordinate tests passed in 2.69s. Separate correction commit:
5ddf9ae — fix: retain usable coordinates beside malformed search evidence.
Both axes rechecked this committed correction: Standards 0 new findings; Spec P2 closed,
0 new findings. The final evaluator gate passed 528 tests with 1 Windows symlink-privilege
skip in 65.70s. Ruff/format and diff checks passed. The earlier full-backend result above
precedes this bounded correction; the full backend was not repeated after it.

Initial patch inspection found a duplicated contract section after a patch retry; it was
deduplicated before final document validation. No ignored file is a published dependency.

### Remaining limits

Only linked identity-phase snapshots are read. Old snapshots may omit coordinates; no
automatic backfill or follow-up request is made. Independent acquisition still uses a
caller-owned injected transport; no built-in operational Google client is supplied.
Coordinates prove correspondence to observed evidence, not factual perfection or future
route guarantees. Close agreeing-but-different coordinates remain explicitly conflicting,
without an unapproved tolerance policy. Manual reviewed coordinates remain an alternative.
No formal comparison, database/model/provider live call, Ticket 10 implementation, Issue
mutation, push or freeze is claimed by this extension.

<a id="rtpeval-ticket-07-acceptance"></a>

<a id="rtpeval-ticket-07-acceptance--ticket-07-offline-same-day-route-acceptance"></a>

## Ticket 07 offline same-day route acceptance

Date: 2026-10-02, Australia/Sydney. Base revision:
`3427784b87d5864aba25dcba8b48430ec4de9dac` on `feature/evaluation`, plus the
uncommitted approved preflight, implementation, tests and documentation.
Status: Implemented and offline-validated; both review axes are clear. The original
existing-test exception below was subsequently resolved under separate user-approved
repair scope: latest unfiltered gate 2234 passed / 10 skipped / zero deselections.
See the supplemental repair section; original checkpoint results remain historical.
Implementation and the independent test repair are committed locally under the
subsequently approved three-group closeout below. All changes remain unpublished;
this acceptance belongs to the approved documentation group. No freeze is implied.

<a id="rtpeval-ticket-07-acceptance--authority-and-scope"></a>

### Authority and scope

[PROJECT](../../../PROJECT.md), the [approved preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19#issuecomment-5955699412),
[route contract](../../contracts/0004-opening-routes.md#rtpeval-route-contract), [time contract](../../contracts/0001-evaluation-artifacts.md#rtpeval-evidence-time-contract),
[snapshot contract](../../contracts/0002-intake-identity-usage.md#rtpeval-snapshot-contract) and [metrics contract](../../contracts/0005-quality-human-review.md#rtpeval-metrics-contract)
own the approved offline behavior. GitHub [#19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19)
owns live task state; [#12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12)
owns overall progress. Historical local ticket/import statements remain dated history.

The user approved preparation/scoring/local CLI, synthetic TDD, relevant and full offline
regressions, Standards/Spec review and corrections, and related docs/archive/Issue updates.
No provider/model/database live call, formal case, experiment, auxiliary total, V3 delta,
commit/push, branch switch, freeze or later-ticket implementation was included.
V0-V3 planner behavior and independent entry points are unchanged.

<a id="rtpeval-ticket-07-acceptance--implemented-behavior-and-interfaces"></a>

### Implemented behavior and interfaces

`backend.evaluation.routes` exposes immutable public `prepare_routes` and `score_routes`
results with independent `to_dict()` copies. `backend.evaluation.route_cli` exposes local
JSON `prepare`/`score` commands. Exit 0 includes quality FAIL/UNKNOWN; exit 2 identifies
material correction/identity replay without a partial cohort. Inputs are never rewritten.
The [package guide](../../../backend/evaluation/README.md#ticket-07-offline-same-day-routes)
owns signatures, new route review/coordinate formats and query defaults.

- Preserve same-day consecutive primary occurrences, independent canonical identities
  and version-selected transport: V0 Activity, V1-V3 Transfer, no ignored-source fallback.
  Inter-day legs are excluded; confirmed same-canonical transitions are N/A. Repeated
  occurrences stay separate even when acquisition requests are deduplicated.
- Prepare occupancy, reviewed Input mode restrictions and independently reviewed coordinates
  without route observations. Extract only neutral Ticket 05 validators into
  `_schedule_preparation.py`; keep existing obligation wire/policies unchanged.
- Honor explicit departure. Otherwise allow waiting, select the longest continuous free
  fragment and break ties by earliest UTC start before seeing provider outcomes. Do not
  concatenate gaps, seek a better departure after failure or silently switch modes.
- Applicable non-travel/fixed occupancy deadlines have zero grace. The separate 300-second
  schedule tolerance applies only to the next visit. DRIVE reserve is 600 seconds once;
  cap tolerance is independently 300 seconds, with no WALK distance tolerance. Shared
  `_route_rules.py` constants drive both arithmetic and reported rules/hash.
- Preserve uncertainty locally: known disjoint alternative occupancies do not contaminate
  another leg. A guaranteed common occupation starting at its deadline is a hard boundary;
  a merely possible boundary cannot borrow the next-visit tolerance and stays UNKNOWN.
- Verify raw snapshot integrity and entire identity/occurrence/request/paired linkage.
  Foreign or corrupt material yields no partial cohort; valid inapplicable mode, departure,
  coordinate or option context is UNKNOWN. Deliberate time-independent WALK/basic DRIVE
  and applicable explicit departure contexts stay distinguishable without date shifts.
- Independently parse raw element status/condition and nanosecond duration. Accept valid
  traffic-calculation fallback; explicit no-route FAILs without invented duration.
  Missing WALK distance/duration remains UNKNOWN for that component. Any independently
  proved component FAIL is decisive; all required components must PASS for combined PASS.
- Report components, raw overruns/deficits, source/query/attempt/hash provenance, separate
  structural/response/full-component/decisive/duration coverage and conditional P/(P+F).
  Partial decisive FAIL is not complete evidence. Unknown travel stays null, never zero.
  Daily/request duration sum/median/max are observed subtotals with missing and unresolved
  population counts; reserve stays separate. Unresolved potential legs suppress relevant
  full-scope rates and complete burden claims without discarding observed measurements.

<a id="rtpeval-ticket-07-acceptance--actual-development-and-correction-sequence"></a>

### Actual development and correction sequence

Public preparation/scorer/CLI seams drove synthetic tests. No third-party network was used.
Initial tracer tests were RED for missing modules, then implemented. A default temporary
directory attempt emitted setup errors without a retained complete result; no count or
cause is inferred. Subsequent runs use explicit repository-local `--basetemp`.

1. Neutral validator extraction initially omitted `OBLIGATION_FIELDS`: **27 failed /
   39 passed**, then the import correction yielded **66 passed** across new baseline and
   existing requirement/schedule tests. No Ticket 05 policy change was made.
2. Malformed status message: **1 failed / 21 passed**, corrected to **22 passed**.
   Expanded context tests exposed a fixture carrying modified source state between builds:
   **1 failed / 39 passed**; each build now restores its original source results, and the
   combined subset passed **41 tests**. This fixture correction does not change production.
3. Unresolved adjacency: **1 failed / 44 passed**, corrected to **45 passed**. Missing
   tolerance classification and non-string clock handling produced two RED cases;
   corrections yielded **48 passed**. Further route cases passed **63 tests**.
4. Expanded local CLI and evaluation regression: **392 passed / 1 skipped**. First full
   backend gate before review corrections: **2221 passed / 10 skipped in 158.36s**.
5. Spec review regressions for disjoint alternatives and unresolved population burden:
   **2 failed / 1 passed**, corrected to **3 passed**. Added applicability, provenance,
   precision and repeated-occurrence cases yielded **84 route/CLI tests passed**.
   The intermediate full backend run passed **2232 / 10 skipped in 200.72s**.
6. Follow-up Spec review found possible occupancy starting exactly at a deadline could
   borrow the 300-second tolerance. Both new boundary cases were RED (**2 failed**).
   Guaranteed-boundary/possible-boundary handling corrected them. Final route/CLI subset:
   **86 passed in 20.35s**. Common 10:30 occupation gives FAIL with a raw 120-second deficit;
   alternatives at 10:30/10:35 give UNKNOWN, never a fabricated free interval.
7. A subsequent bare `python` invocation selected host Python 3.13 without pytest and ran
   no tests. Verification immediately used the existing project `.venv` Python 3.12;
   dependencies and host settings were not changed.

The first post-boundary full run stopped making progress in the unchanged
`test_httpx2_embedding_timeout_and_cancel_close_owned_client` cases. Independent execution
also failed to complete; a 10-second faulthandler dump shows the test's asyncio run waiting.
Only these verified test processes were stopped, with exact PID/command identity checks.
The original test has an unbounded `entered.wait()` alongside a 20ms timeout. A handshake
timing race is a hypothesis, not a confirmed runtime diagnosis. No Retrieval code, test
assertion or product budget was changed. Earlier complete full runs passed these cases.

Final broad backend result: **2232 passed / 10 skipped / 2 deselected in 186.17s** after
the boundary correction, explicitly deselecting both parameters of that existing test.
This is a documented validation exception, not a claim that the final workspace passed
every backend test. The earlier unfiltered run was **2232 passed / 10 skipped in 200.72s**
before the last two new boundary tests/fix; these counts must not be merged. Remaining
tests are unchanged. A subsequent English/document link check found **165 existing local
Markdown targets**; AST comparison confirmed all **eight extracted definitions unchanged**.
Backend-wide Ruff, evaluation compilation, route CLI help and diff checks
passed. Incidental formatter changes to unchanged baseline files were removed.

All full-suite checkpoints deliberately set `TRIPWORLD_TEST_DATABASE=0`. Their ten skips
are nine opt-in PostgreSQL integration tests and one host symlink-privilege case. Earlier
Ticket 06 database/UAC supplements do not count as Ticket 07 verification. No new live,
database or elevated-native execution was performed or inferred from prior permissions.

<a id="rtpeval-ticket-07-acceptance--review-axes"></a>

### Review axes

**Standards:** no documented-standard breach. One initial nonblocking duplicated-rule
smell was corrected by centralizing caps, tolerances, reserve and query defaults.
Follow-up review found no remaining Standards issue.

**Spec:** two initial P2 findings (disjoint alternative poisoning and incomplete-population
burden) plus one follow-up P2 deadline-boundary finding were fixed with public regressions.
Final read-only follow-up confirmed all three resolved, with no remaining actionable
Spec issue or scope expansion. Tests are reported by the primary agent, not by reviewers.

<a id="rtpeval-ticket-07-acceptance--evidence-and-remaining-limits"></a>

### Evidence and remaining limits

Ignored local evidence: `thesis_notes/evaluation/ticket-07-validation/` contains separate
pre-review, post-initial-review, interrupted and final broad-regression logs. The local research record
`thesis_notes/evaluation/2026-10-02-ticket-07-implementation.md` preserves development
decisions and failures; neither is a fresh-checkout dependency or project authority.

Synthetic response/coordinate/review fixtures verify engineering behavior, not real
provider availability or coordinate facts. External mode/coordinate review is a supplied
trust boundary; unknown facts remain visible. No formal evaluation, historical/future
travel guarantee, cross-version ranking or version-level retrospective is claimed.
Ticket 08 report/auxiliary-score work requires its own approved preflight/scope.

<a id="rtpeval-ticket-07-acceptance--tracker-closeout"></a>

### Tracker closeout

Issue #19 was updated/read back as closed/completed with all five current acceptance
checks complete, actual validation exception and local/unpublished boundary. Parent #12
was updated/read back as open with 01-07 complete and later tickets unchanged. Imported
ticket/preflight/commit history was preserved. No new Issue, comment, assignment or label
was created. Research evidence remains ignored; no Git staging or commit was performed.

<a id="rtpeval-ticket-07-acceptance--final-workspace-checks"></a>

### Final workspace checks

All six generated Ticket 07 test/diagnostic roots were removed after their processes
ended and four archived regression logs were verified. Final English/local-link check:
**167 existing targets**. Index remains empty; HEAD remains 3427784b on feature/evaluation.
The actual content diff contains only approved Ticket 07 files. Four unchanged baseline
files touched by the formatter show checkout line-ending status entries but have zero
content diff against HEAD; they are not implementation changes or staged content.

<a id="rtpeval-ticket-07-acceptance--subsequent-diagnosis--2026-10-02"></a>

### Subsequent diagnosis — 2026-10-02

After Ticket 07 closeout, the user separately authorized diagnosis of the existing
embedding timeout-test hang. The [record](../v0-v3/v2-embedding-timeout.md#timeout-test-diagnosis-diagnosis) confirms
that SDK cold request preparation can outlast 20ms, leaving the test waiting forever for
a handler event after the embedding task already timed out. A bounded test-only candidate
passed both parameters in memory; no source repair/full-suite retest is yet authorized or
claimed. The Ticket 07 actual skip/deselection checkpoint above remains unchanged.

<a id="rtpeval-ticket-07-acceptance--approved-timeout-test-repair-supplement--2026-10-02"></a>

### Approved timeout-test repair supplement — 2026-10-02

The user subsequently approved applying the concrete test-only patch and targeted/full
offline validation. [Repair acceptance](../v0-v3/v2-embedding-timeout.md#timeout-test-diagnosis-repair-acceptance)
records one affected test function changed, direct timeout observation, bounded cancel
handshake/scenario and child cleanup, with a five-second synthetic deadline and original
assertions retained. Production Retrieval, usage hooks and runtime config are unchanged.

Actual-source feedback loop: pre-fix 1 failed/1 passed/14 deselected in 15.76s, post-fix
2 passed/14 deselected in 8.24s. Both parameters pass alone in separate cold processes;
all 16 module tests pass. Standards and Spec each report zero findings. The new unfiltered
full offline backend gate is **2234 passed / 10 skipped in 196.39s, zero deselections**.
Both formerly excluded parameters now participate and pass. Database/native skips are
not supplemented. Earlier numbers are distinct historical runs, not retroactive passes.
No provider/model/database live call, formal experiment, Git action, freeze or Ticket 08.

<a id="rtpeval-ticket-07-acceptance--approved-local-git-closeout--2026-10-02"></a>

### Approved local Git closeout — 2026-10-02

The user explicitly approved finishing Ticket 07 with the previously proposed three
local groups. This later approval supersedes only the earlier no-commit boundary;
push, branch switching, live/database/native supplements, freezes and Ticket 08 remain
outside scope. No executable correction was made during Git closeout.

1. **2b66c9f889ca8964f97dbc67b2a601ebb56be64c** —
   `feat: evaluate same-day routes from frozen evidence`.
   Seven new route/preparation modules, neutral validator extraction in the existing
   requirement/schedule module, and the two directly related test modules; ten files.
2. **b18daef4af2fecba36d7b84315c8946a772aeae8** —
   `test: bound embedding timeout and cancellation checks`.
   Only the independently approved existing test function; one file.
3. Approved documentation group — `docs: record route validation and local closeout`.
   Current route/metrics contracts, preflight/acceptance, permanent diagnosis/proposal/
   repair records, PROJECT, documentation index/glossary and package guide. The commit
   containing this entry supplies its own revision through Git history; ignored archive
   probes/logs, credentials, raw payloads and generated pytest files are excluded.

Pre-commit offline check: route tests, CLI tests, shared requirement/schedule tests and
the runtime retrieval module passed **166 tests in 34.26s**. Backend Ruff and diff checks
passed. The full unfiltered **2234 passed / 10 skipped / zero deselections** gate remains
the earlier actual run; it was not rerun or supplemented, and no code changed afterward.
The ten skips remain nine opt-in database cases and one host symlink privilege case.
Earlier filtered gates and red/correction/retest sequences remain dated history.
Four baseline files with zero normalized content diff require only index-stat refresh;
they contribute no staged content or commit changes. Generated closeout pytest files
are removed after process completion. No version freeze or later ticket is implied.
Closeout documentation check: English content and **180 existing local Markdown
targets** across ten documents passed. The permanent historical proposal passes
reverse-apply validation against the committed repair. Its unified-diff context markers
are preserved as patch syntax; they are not ordinary prose whitespace.
