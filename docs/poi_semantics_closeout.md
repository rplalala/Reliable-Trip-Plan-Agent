# POI semantics iteration closeout — 2026-09-26

Status: CLOSED by explicit user confirmation on 2026-09-26. Implementation, bounded development
acceptance, offline browser integration, inventory review and five local commits are complete.
This is iteration closure, not a new version freeze or formal evaluation.

## Final closure record

The completed sequence on `feature/v3` is `0652222` (workflow), `014c726` (backend),
`29647ef` (frontend), `9c910b2` (capture/replay tools), and `40b0b26` (documentation).
All 105 inventoried files were committed in the reviewed groups; the index and nonignored
worktree were clean after execution. No push, PR or branch switch occurred. The subsequent
user-requested closure-status documentation update is separate from those five commits.

Final behavior: Product and Dev V3 default to quantity review; the obsolete optional repetition
switch/report field is removed. Unauthorized-repeat repair and authorized revisit protections
remain active. Product JSON/SSE preserve completion fields, and incomplete results remain
visible with appropriate UI wording. Budgets, local addition permissions and V0-V2 boundaries
are preserved; overfull review remains disabled.

Validation: combined backend 1648 passed / 9 skipped; isolated backend commit tree 1608 passed /
9 skipped; new tooling group 40 passed; frontend 59 passed and TypeScript/Vite build passed.
The initial isolated export lacked local test dependencies; supplying the existing virtualenv
and offline vocabularies resolved those environment failures without production edits.
Real-browser offline business submissions passed without retries; only synthetic external
ports were used. Temporary servers were stopped. The detailed sequence below preserves setup
corrections and earlier live observations without treating them as a formal benchmark.

P3 remains deferred, factual UNKNOWNs remain, and no further Penguin Beach / London Zoo work
is scheduled. Historical A/B/C/D evidence remains stage-specific, not a single final-code live
matrix. No new live run, implementation, formal research, version freeze or Git action follows
automatically from closure. The next stage requires a new user instruction.

## Delivered scope

- Shared requirement interpretation distinguishes ordinary interests, one-off category goals,
  exact/minimum counts, distinct-date obligations and sourced primary-role exceptions.
  Executable named-place revisits use VisitRequirement without a duplicate unsupported-hard
  semantic obligation; independent unsupported hard conditions retain the existing gate.
- Request-owned POI semantic assessment supports candidate roles, goal matching, provenance,
  exploration and main-visit qualification. V3 supports scoped automatic repeat correction
  and unpublished compensation groups; rejected partial changes do not become the itinerary.
- Four approved Spec corrections unify canonical counting across role labels, enforce category
  cardinality/date goals, propagate named obligations to completion, and prioritize explicit
  category goals within existing supply capacity. Product exposes incomplete policy status.
- Prompt 16 preserves ordinary rich/varied trip wishes as soft meaning rather than blocking
  clarification. Semantic prompt 2 specifies exact same-candidate evidence references;
  invalid references still fail, with bounded diagnostics and prompt-aware cache identity.
- Opt-in development capture preserves requirements, semantic input/output/outcome and one
  bounded pre-Repair typed snapshot. Offline replay inspects saved stage scope/windows/pool
  without providers or models. The subsequent approved policy update defaults quantity review
  on; explicit per-run disabling remains available.

The complete comparison pool was already wired into Repair. Tests verified that existing
path; no new quantity selection policy, hardcoded London/date rule or larger allowance was added.
Shared interpreter changes apply to V0-V3; candidate judgments apply to evidence-bearing
versions; targeted Repair remains V3-only. All four entry points remain independently runnable.

## Validation and correction sequence

The originating [implementation record](shared_poi_semantics_plan.md) preserves the detailed
sequence, including unsuccessful attempts; later success does not rewrite those attempts.

1. The four Spec fixes were developed against failing behavior tests. The initial full suite
   ended at 1590 passed / 9 skipped / 1 failed. Isolated diagnosis showed the old fixture
   violated confirmed-repeat target priority. The approved fixture-only correction preserved
   its adopted-loss assertion; the full suite then passed 1591 / 9 skipped.
2. The first live batch stopped at a transport dependency failure. A separately authorized
   network-enabled batch completed A and B, then stopped at C's unsupported-hard gate. A
   supplied eight distinct visits; B satisfied exact two museums on different dates and at
   least two parks. These runs did not exercise every repeat/count Repair branch.
3. After the approved named-visit routing correction, offline validation passed 1602 / 9
   skipped. A separately authorized captured C retest completed: British Museum exactly twice
   on different dates, complete policy status and no duplicate hard semantic obligation.
4. D first stopped on rich-trip ambiguity. Prompt 16 and nine controlled regressions brought
   the full suite to 1611 / 9 skipped. The next approved D attempt passed interpretation but
   failed semantic reference validation. Semantic prompt/capture corrections then required a
   partial-write cap fix and a test-only exclusion of random telemetry call IDs; final full
   offline validation passed 1625 / 9 skipped.
5. The dual-capture D retest completed with 14 distinct visits and four ordinary quantity
   gaps. The user accepted the semantic result. Offline diagnosis established that quantity
   review was disabled: Repair had not run, so repair-round exhaustion was not the cause.
6. The quantity capture/replay package added 15 tests. TDD corrected a synthetic Details-state
   mismatch and moved a network guard inside the Windows event loop to avoid blocking its
   internal socketpair. Focused V3 validation passed 421 tests; final backend validation passed
   **1640 / 9 skipped in 75.77 seconds**. Ruff and changed-file compilation passed. The recorded
   Standards/Spec reviews concern their respective deltas, not every intermediate commit.
7. The subsequent single quantity-enabled D pilot completed with full capture. During this
   documentation closeout, frontend tests additionally passed **56 tests across 8 files**;
   `npm run build` passed TypeScript and Vite. Existing dependencies were used offline.
   No production code changed in this closeout, so the backend suite was not repeated.

## Product API completion follow-up — 2026-09-26

The Product route rebuilt its response using only three older fields, silently replacing
policy completion/reasons with their defaults. SSE reused that route and had the same loss.
The route now converts the complete already-allowlisted ProductPlanResult. Internal runtime
diagnostics remain excluded. Request status `completed` is independent of policy completion;
an incomplete adopted itinerary still renders, with an unmet-requirements progress message.

TDD initially reproduced four API failures (complete/incomplete across JSON/SSE), with two
unassessed cases passing. All six pass after the fix. The new page regression initially used
an ambiguous status selector; after narrowing it, it reproduced the incorrect ready message
and passed after the UI correction. The transport fixture initially omitted required SSE
event metadata; correcting the fixture preserved the existing strict parser. Both transport
cases now pass without frontend transport changes. Final offline validation: **1646 backend
tests passed, 9 skipped (80.96 seconds); 59 frontend tests passed across 8 files**. TypeScript,
Vite build and scoped Ruff checks passed.

The Product page uses `/api/planning/stream`; the ordinary client uses `/api/planning`.
Both reach PlanningService and current V3 through RequestPlannerRuntime. Development proxy
targets port 8000. These are offline source/contract checks, not verification of a deployed
process. Production quantity review remains disabled; the last D pilot's explicit override
is not automatically enabled in the Product flow. No live calls, P3 changes or Git actions
were performed. This follow-up supersedes the documentation-only validation totals above.

## Review policy follow-up — 2026-09-26

After the API correction, the user approved default quantity review and removal of the
obsolete repetition-review scheme. V3 now loads quantity review as true from runtime.yaml,
including both Product and Dev requests. Overfull remains false. The removed repetition key
is absent from the configuration schema, optional review targets and V3 review_policy report.
Confirmed unauthorized repeats still enter Repair automatically; authorized count/date
revisits and UNKNOWN multiplicity retain their protections. V0-V2, budgets, local addition
permissions, adoption safeguards and stop conditions are unchanged.

TDD first reproduced the missing default quantity repair, then verified an adopted addition
with original activities unchanged and no move/revisit permissions. Explicit disabling still
skips quantity repair. A second red/green check covers removal and rejection of the obsolete
configuration key. The broader focused run had 532 passes and three expected migration
failures: an old default assertion, a YAML test intercepted by an explicit-off fixture, and
the old configuration table value. These were corrected without weakening repair assertions.
Existing conflict-focused graph fixtures now explicitly disable quantity review; the new
default-policy test exercises real YAML loading. Repeat repair, legal revisit and UNKNOWN
protection regressions remain in the suite. The diagnostic payload fixture was also migrated
off the removed optional target; its related 96 tests passed. One full run stalled near
existing retrieval timeout/cancellation tests and was interrupted; the isolated retrieval
suite passed all 16 tests. A fresh complete run with timeout stack diagnostics passed
**1648 tests, 9 skipped in 72.84 seconds**, with no timeout report. Scoped Ruff checks passed.
No retrieval implementation was changed. Frontend code is unchanged; its prior 59-test/build
result is retained rather than claimed as a new run.

Custom YAML must remove repetition_review_enabled. Historical evidence is preserved, not
rewritten; old typed snapshots may require matching historical code to replay. Existing backend
processes must restart because runtime configuration is cached. No process restart, live run,
P3 work, commit or freeze was performed. The earlier default-off records remain historical.

## Latest D quantity pilot

Run `8ebe8b6a-6a62-4e98-806b-b2efbc21807f`, London October 1-8, one traveler, AUD3000,
unchanged mountain/zoo/rich-trip input. One authorized run, exit0, 183.844 seconds.
The newly generated itinerary had three gaps (October 3/7/8), distinct from the prior D
sample's four dates. Two Repair rounds added three visits, from15 to18 distinct canonical
IDs. Final daily counts: **3/3/2/2/2/2/2/2**. Original activities remained unchanged.

Two additions came from the comparison pool and one from unused selected supply. Repair
reused37 qualified candidates, with no new search, Details, embedding, retrieval or semantic
calls. Usage was2/5 Repair model calls,18/24 route sends and18/32 elements; request-wide
semantic usage stayed2/6 calls and36.478/120 seconds. The existing limits/defaults were not
changed. Two requirement records, six semantic records and a1,395,829-byte Repair snapshot
were captured; typed offline replay and14 acceptance checks passed. Final findings include
22 PASS and26 UNKNOWN, with no confirmed violation or unresolved quantity-review target.

Evidence is local and ignored: `artifacts/poi_semantics_acceptance/20260926_D_quantity_review/`.
Its `report.md`, `checks.json`, `execution.json` and `offline_replay.json` provide the bounded
observations. Raw captures are not proposed for Git. This development pilot is not a benchmark
or a controlled comparison with the earlier D generation.

## User decisions and remaining boundaries

- The user decided not to pursue Penguin Beach / London Zoo further. The former is an
  internal exhibit and the latter the parent zoo; this is not two names for one identical
  object. Visiting the exhibit followed by other zoo areas can be reasonable. No defect has
  been established solely from that relationship. It is not an open issue, acceptance blocker
  or follow-up task in this iteration; no related policy or code change is authorized.
- The existing P3 pending-reason heuristic remains explicitly deferred and unchanged.
- UNKNOWN operating hours, admission/access, suitability and verified costs remain UNKNOWN.
  Indoor climbing is an explicitly labeled related alternative, not actual mountain climbing.
  Quantity success alone does not prove richness, feasibility or model stability.
- No additional live runs, budget increases, production-default changes, commits, pushes,
  branch changes, P3 work, thesis work or version freeze are implied by closeout.

## Offline browser acceptance and commit authorization — 2026-09-26

The user approved one offline frontend/backend integration acceptance and authorized reasonable
local commits without another grouping approval if it passed. Actual Product and Dev pages
ran through Vite's proxy, FastAPI SSE, application services, RequestPlannerRuntime and current
version runners. Only external LLM, Places, weather, routes, retrieval and introductions were
replaced with synthetic fixtures. No credentials or live services were used.

Product's quantity case displayed an adopted addition with the YAML default enabled. Its
incomplete case retained the itinerary and displayed both the incomplete warning and the
unmet-requirements progress message, without the ready message. Dev's single four-version
submission completed all four independent flows; the visible V3 debug JSON reported
quantity=true, overfull=false, no obsolete repetition field, and ACCEPTED_PARTIAL from the
controlled addition fixture. This verifies transport, routing and presentation, not live
itinerary quality or complete resolution of every synthetic quantity gap.

All business scenarios passed on their first submission without product changes. Setup
corrections moved the network guard after Windows event-loop socketpair creation and used
ISO accessibility setValue for native date inputs. No business request was retried. The
temporary frontend/backend processes were stopped and ports 5173/8000 confirmed closed.
Evidence and the temporary host remain ignored under artifacts/offline_integration_20260926/.
Frontend checks were freshly repeated: 59 tests passed across 8 files; TypeScript/Vite build passed.

Group review keeps workflow, backend, frontend, new capture/replay tools and documentation
separate. Six existing tool/harness migrations move into the backend group because its tests
depend on them; new tooling remains independent. Candidate-tree validation supplies the same
installed virtualenv and offline tokenizer vocabularies as the workspace. They are validation
dependencies only and are excluded from every commit. The initial export run had 30 failures,
1578 passes and 9 skips because the local virtualenv/tokenizer assets were absent. After
supplying those unchanged local dependencies, the backend candidate tree passed **1608 tests,
9 skipped in 72.92 seconds**. Adding the separate tooling group then passed its **40 tests
in 6.47 seconds**. Implementation hashes match the prior passing 1648-test workspace; only
closeout documentation changed during this acceptance. No live run, push, PR, branch switch,
P3 repair or version freeze is authorized by this step.

## Historical working-tree checkpoint

The inspected branch is `feature/v3`, HEAD `7748f3e`. At closeout entry,71 tracked files
were modified and23 nonignored files were untracked; the index was empty. This includes the
agent setup, the full semantic extension, later approved corrections, UI and developer tools,
not only the last quantity task. Counts are not attributed to the latest implementation alone.

The [reviewed commit plan](../.scratch/iteration-closeout/commit-plan.md) inventories every
nonignored changed file by responsibility and records dependencies. Shared backend files
contain intertwined semantic/Spec/capture-hook changes; they should not be split by
conversational chronology. Tests and their implementation remain together. No staging or
commit had occurred at the original closeout checkpoint. The subsequent authorization above
permits local commits after passing checks; earlier combined-tree results alone do not certify
hypothetical intermediate commits.
