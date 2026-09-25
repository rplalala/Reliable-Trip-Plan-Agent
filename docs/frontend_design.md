# Frontend and API design

## Semantic completion presentation implemented — 2026-09-26

Product results now carry policy_completion and policy_reasons. ItineraryView displays an explicit incomplete-policy message while preserving the latest adopted itinerary and Nearby references. Semantic assessment errors follow the existing system-error path, not preference rewrite. V0/unassessed inputs are not falsely marked semantically verified. Two targeted frontend suites passed (30 tests); direct TypeScript no-emit checks and changed-file ESLint passed. See the [checkpoint](shared_poi_semantics_plan.md#12-implementation-checkpoint--2026-09-26).

Current shared/V3 engineering checkpoint (2026-09-25): see [closeout](v3_closeout.md)
for current configuration, shared ownership and artifact-verified evidence. Earlier dated
implementation/live statements below retain their original scope. V0 remains tool-free;
V1/V2 do not run Repair. Product API activation of V3 is recorded in the third checkpoint below;
React migration is implemented with offline validation and bounded Product/four-version Developer
live acceptance after the approved transport-isolation fix. Not every repair/retrieval branch was
live-tested; the dated records below retain their original scope.
Provider recovery UI is offline-only.


React separates product routes / and /plan from /dev. Vite proxies /api and /health to
FastAPI in development. Product POST /api/planning dispatches through PlanningService to V3
with an allowlisted presentation projection. Developer POST /api/dev/planning now accepts
V0-V3 via the request-scoped programmatic runtime and four independent React run panels.
Neither API exposes runtime configuration selection.

Both forms require structured destination/dates/travelers/whole-trip budget and accept optional
preferences. Product uses backend date bounds; Developer retains an explicit reference date.
Product displays daily weather, optional introductions, transfer estimates and nested Nearby from
the final safe projection. Developer retains complete research JSON and mechanism events/timings.
Nearby remains optional, not scheduled or costed. The old `/dev/planner` page has been removed.

[Shared requirements](shared_requirements.md) and [output](shared_itinerary_output.md) own contracts.
[Frontend milestone](frontend_milestone.md) preserves original API/builder behavior and tests;
current documents do not rewrite it as if later input changes existed at the original checkpoint.

## Date and attribution alignment (2026-09-22)

Product date controls load GET /api/planning/date-window from the backend, using its configured-zone
reference date. The14-date calendar window is separate from the10-day maximum inclusive trip.
End max=min(start+9, allowedEnd); backend validation remains authoritative across midnight.
The developer reference-date initial value also comes from the server, but remains an explicit
research override. No default-engine or broader request-form migration is included.
Itinerary presentation includes conditional Open-Meteo attribution and CC BY4.0 link. It does not
claim V0 fetched weather or that forecasts prove future conditions.

## Accepted backlog: Product V3 and four-version Developer MVP (2026-09-25)

Status: implementation authorized after the V3 engineering closeout; work is in progress.
Checked items mean implemented with offline coverage, not real-provider live acceptance.
Unchecked items remain TODO, not fully validated by this record. The current
implementation described above and the historical frontend milestone remain separate from this
backlog. Keep the existing MVP layout and basic styling; visual redesign has lower priority.

### Product execution and input

- [x] Switch Product planning through `PlanningService` to the programmatic V3 runner. Keep
  `/` and `/plan`, a version-agnostic Product API, and no user-facing engine selector or automatic
  fallback to V0.
- [x] Align the form with the current shared `PlanningRequest`: destination, start/end dates,
  traveler count and whole-trip budget amount/currency are required; additional preferences are
  optional. Continue obtaining date bounds from the backend, with authoritative backend validation.
  Product users do not supply `reference_date`.
- [x] Display a valid returned itinerary even when repair leaves unresolved findings. Existing
  user-relevant findings may be translated into concise notices, distinguishing confirmed issues
  from insufficient evidence. Completion means execution finished, not whole-trip feasibility or
  quality approval. Do not add a frontend evaluator or reject an available itinerary solely because
  findings remain. Formal evaluation belongs to separately authorized later research work.
- [x] Keep research versions, provider/stage debug details and raw JSON panels out of Product UX.
  User-facing weather/route attribution remains appropriate. Map presentation data in the backend;
  do not send unrestricted research output and merely hide it in the browser.

### Developer execution and isolation

- [x] Move the workbench directly to `/dev`, replacing `/dev/planner` as its page location.
  Retain the separate Developer layout and local-development deployment warning.
- [x] Replace the legacy raw `request_text` form with the shared structured input, retaining the
  visible research `reference_date`. One Run all action starts V0, V1, V2 and V3 simultaneously
  from the same input snapshot and reference date.
- [x] Give each run an independent identity, progress stream, result, error, cache and mutable
  usage counters. Sharing configured limit values must not pool consumed budget across versions.
  Each version follows its own applicable tool/token/deadline limits; V3 repair rounds share only
  that V3 run's cumulative repair allowance. Do not add a combined four-version budget.
- [x] Keep failures, exhausted budgets, timeouts and single-run cancellation isolated. They must
  not automatically cancel the other versions. External provider quotas and machine/database
  capacity can still be shared and may independently affect several runs.
- [x] Show all four progress bars, with each version's itinerary and expandable detailed events
  and complete result/debug JSON. Support individual reruns using the same input snapshot.
- [x] Lock the input form while any run in the group is active, and display the group's input
  summary. Editing requires all active runs to finish or Stop all first. A new input creates a new
  group; late events and results must not be mixed into another group.

This is a multi-version execution workbench, not an automated ranking or formal research
comparison system. Preserve the implemented preference rewrite, safety and provider-blocked
Product feedback and Developer details. Do not add conversational clarification, partial
continuation or a new clarification design. One version requiring clarification does not stop
the others.

### Real execution progress and lifecycle

- [x] Product has one stage-based progress bar and short, understandable English messages, such
  as "Finding places for your trip", "Checking the weather", "Planning your days", "Checking
  travel times" and "Adjusting your itinerary". Show only stages actually executed.
- [x] Developer has four independent stage-based bars plus detailed chronological events:
  acquired, filtered and generation-input POI counts; validation findings and types; selected
  repair targets; current repair operations/round; and re-validation outcomes. Report attempted
  repair separately from issues confirmed resolved. Counts must come from actual runtime data.
- [x] In each Developer run, display actual elapsed time when each mechanism/stage ends, next
  to its terminal status and details. Measure duration on the backend with a monotonic clock
  between the matching start and end, rather than from browser event arrival times. Identify
  repeated executions separately, including each repair and re-validation round. Failed or
  cancelled stages report elapsed time until termination; skipped stages are labelled skipped
  without an invented duration. Show whole-run elapsed time separately. Nested or overlapping
  stage durations must not be summed as if they equal whole-run time. These timings support
  development inspection and are not formal benchmark results.
- [x] Do not show numeric percentages or invented time estimates. Advance a determinate fill
  from real stage events (see the latest checkpoint below), rather than a looping slider;
  stages may be skipped or repeated without moving the bar backwards. Final result delivery ends
  the bar; failure or cancellation is a distinct terminal state, not successful completion.
- [x] Deliver real structured progress through HTTP streaming. Reuse existing tracing where
  suitable and add missing start events; a completed-round artifact cannot represent a live
  "repairing now" event. Do not expose model chain-of-thought or infer progress by parsing logs.
  Retain JSON endpoints and add POST streaming endpoints using fetch-readable SSE. Events carry
  run identity, sequence, stage occurrence/round, status and measured elapsed time. Product and
  Developer projections differ; HTTP errors after streaming starts become terminal stream events.
- [x] Provide Product Stop, Developer Stop per version and Stop all. Page departure/disconnection
  requests cooperative backend cancellation and resource cleanup. Already dispatched third-party
  work may not stop immediately. This MVP has no persistent background jobs, reload recovery or
  reconnect/resume guarantee.
- [x] Ensure run-scoped metadata/tracing and independent model transports; cancellation isolation
  is covered offline and by the bounded live retest below.
- [ ] Exercise an active V2/V3 retrieval subprocess on Windows during dedicated integration;
  successful four-version execution alone does not establish coverage of every retrieval branch.

### Product itinerary details

- [x] Show acquired weather matched to each itinerary date, including available summary and
  temperature fields with attribution. Missing coverage is explicitly unavailable, not invented.
- [x] Show one short introduction next to each POI when supplied by the backend stage below.
- [x] Display returned Nearby recommendations directly beneath the scheduled POI to which they
  are linked. Use a compact nested list with indentation, smaller readable text and lower visual
  emphasis, like child entries in a directory. Label these as optional nearby suggestions; they
  remain outside the scheduled itinerary and do not acquire activity times, planned costs or
  inclusion in the main transport sequence merely because they are displayed under a stop.
- [x] Preserve the backend's Nearby-to-final-anchor association in the Product presentation data.
  Verify the mapping after repair when integration is planned; an associated day alone does not
  identify the parent activity. Do not infer the parent from display order or similar names.
- [x] Between adjacent scheduled activities, show the selected transport mode, estimated duration,
  distance and source when available. Show the preceding end and following start times so the
  connection is understandable. Present boarding/transfer allowances separately from route time,
  only when supported by the actual scheduling policy. State vehicle-arrangement needs and
  unverified costs where applicable; do not imply a booking exists.
- [x] Distinguish provider estimates from conservative scheduling allowances. For example,
  "Driving: about 18 min, 7.2 km; allow another 10 min for transfers" requires the corresponding
  route and allowance. If only a 45-minute fallback allowance exists, show "Route unverified;
  45 min reserved" without inventing mode, distance or Google attribution. These values are
  illustrative, not new hardcoded policies.
- [x] Associate presentation data with V3's final adopted activities, dates and actual adjacency
  after repair. Do not reuse routes for replaced or reordered stops. Missing matching evidence
  stays unavailable. Display existing relevant connection warnings without implementing a second
  feasibility evaluator in React.

### Product-only final POI introductions

- [x] After V3 returns its final itinerary, but before returning the Product response, make one
  batch LLM call in a separate application presentation service for final scheduled POIs only.
  Developer requests and all research runners/CLIs do not call this service. Do not modify the
  research PlanningResult or include introduction generation in research mechanism timings.
  Use existing `description`/`summary` as context where available. When absent, the model may
  generate the introduction from its own knowledge; verification is explicitly not required.
  These introductions are display text and must not become verified planning/validation evidence.
- [x] Generate introductions in the backend, not in the browser. Do not change the adopted
  schedule or trigger another planning/repair cycle to obtain descriptions.
- [x] Apply a separate introduction-call timeout within the existing V3 whole-request deadline.
  Skip when insufficient time remains; on failure or timeout, preserve and return the available
  itinerary with missing introductions omitted. Record failure/skip in internal Product telemetry,
  not the Developer planner result. Nearby uses existing reasons/context without another LLM call.
  Product can show "Preparing place introductions" while this stage runs.

- [x] Product displays only an officially returned final itinerary, never an intermediate draft
  after technical failure or cancellation. Developer retains received progress/diagnostics but
  does not mark an interrupted run completed. A normally completed itinerary with unresolved
  findings is still eligible for display; this is not an additional quality gate.

### Authorized implementation sequence

1. Build a request-scoped programmatic V0-V3 runtime boundary and extend Developer dispatch.
   Validate structured input before constructing provider resources; isolate clients, mutable
   metadata, caches and deadlines, and close owned resources after success/failure/cancellation.
   The API explicitly activates the configured bounded request timeout without changing CLI policy.
2. Add structured streaming progress, monotonic mechanism durations and cooperative cancellation.
   Keep JSON APIs. Four Developer requests run independently; no persistent jobs or aggregate budget.
3. Add allowlisted Product presentation mapping and Product-only introductions, then activate V3
   for Product. Shared Itinerary now contains research diagnostics: do not switch the public engine
   before its safe response projection is ready. Bind weather/routes/Nearby to the final itinerary.
4. Align Product form requirements and add progress/Stop plus weather, introductions, transfers
   and nested Nearby, preserving current preference feedback and basic MVP styling.
5. Move Developer to /dev with a locked shared structured snapshot, explicit reference date, four
   independent panels, per-run/all cancellation and same-snapshot reruns with stale-event isolation.
6. Run focused and full offline regression, Ruff, frontend tests/lint/build and git diff --check;
   then perform authorized real Product V3 and concurrent V0-V3 live acceptance. Record actual
   outcomes separately from baseline test results. No automatic commits, push or version freeze.

Expected touchpoints: backend/app/services/planning.py, a new application runtime module,
backend/app/api/dependencies.py, API schemas and Product/Developer endpoints; frontend routing,
PlanningForm, PlanTripPage, DeveloperPlannerPage, ItineraryView, shared API/types and new progress
and presentation components; corresponding backend/frontend tests. Keep research algorithms,
prompts and independent entry points unchanged. Any necessary observer hooks are optional and
default to no effect; cross-version regression is required before claiming compatibility.

### Deferred integration checks and scope

- [x] Following V3 closeout, inspect its current programmatic outputs,
  evidence associations, progress hooks, deadline semantics and dependency lifecycle. Define
  concrete contracts and implementation steps above, without treating this backlog as a completed
  migration or V3 freeze.
- [x] Verify offline invalid input rejection before planner/provider execution, correct version dispatch,
  identical group inputs, four-run budget/error/cancellation isolation, truthful progress,
  stage-duration attribution across repeated rounds and terminal states, and final
  weather/route/description and Nearby-to-anchor mapping, including the nested Nearby display.
  Include description failure preserving the itinerary and one
  run exhausting its budget while others continue.
- [x] Run backend/frontend regression, lint, build and diff checks, followed by bounded real
  Product V3 and simultaneous four-version Developer smoke acceptance (see dated records below).
- [x] Verify actual React router departure aborts Product/all Developer requests and ignores late
  events; display multiple repair rounds, targets and revalidation using controlled frontend tests.
  This is automated routing/event verification, not real-provider repair acceptance.
- [ ] Live exercise remaining repair/retrieval branches when relevant; not required to claim the
  bounded acceptance already recorded, and not a formal benchmark.

Auth, Profile, Saved Trips, new persistence infrastructure, full UI polish, formal comparison and
thesis evaluation remain outside this backlog. Existing retrieval database integration is required
by the relevant runners, not a new user-data persistence feature. Developer access must be
protected or disabled before public deployment. Implementation is authorized for this sequence;
Git operations still require separate authorization.

### First implementation checkpoint: runtime and Developer API

Implemented: request-scoped provider assembly, programmatic V0-V3 dispatch, input validation
before provider construction, explicit configured API deadline, cleanup on normal/error/cancel
paths, and complete subclass serialization in the Developer JSON response. The API has no
combined four-run budget or automatic cross-version cancellation. Existing research runners
continue to create their own tool budgets/cache and own retrieval lifetimes.

For local Windows API execution use `uv run python scripts/run_api.py --env-file .env` (or the
appropriate existing local environment file). This launcher uses SelectorEventLoop, matching
the async PostgreSQL requirement of V2/V3; it does not add reload/workers or modify research CLIs.
The loop selection is offline-tested, not a claim of live database/provider acceptance.

Product still uses V0; no streaming, new React UI, Product introductions or new presentation
projection is implemented by this checkpoint. Do not interpret this as whole-backlog completion.

Validation snapshot for this checkpoint: the first focused run passed 107 tests and had one
fixture setup error caused by permissions on an existing pytest temporary directory. Re-running
with a fresh isolated temporary directory passed all 108 focused tests. Three Ruff formatting
findings were corrected; Ruff subsequently passed. Full backend regression then passed 1479 tests
with 9 skips. The subsequently added API launcher test passed separately (1 test); it was not in
that full-run count. Frontend initially could not write Vite/TypeScript caches under sandbox
permissions; the authorized normal-permission rerun passed 33 tests in 6 files, lint and build.
Final Ruff and git diff --check passed. V0-V3 implementation directories, research runner scripts
and backend/app/llm have no diff. No new live execution, formal comparison, commit or push occurred.

### Second implementation checkpoint: streaming and observation

Implemented at the backend only; React progress bars and Stop controls remain pending.

- POST `/api/planning/stream` and POST `/api/dev/planning/stream` accept the same request bodies
  as their JSON counterparts, which remain available. Structured/date validation failures return
  HTTP 422 before streaming or provider construction. Once headers have been sent, execution
  failures are terminal `error` events with `http_status`, not a second HTTP response.
- SSE events are `started`, `stage`, Developer-only `detail`, and terminal `result`, `error` or
  `cancelled`. Every event has `run_id`, increasing `sequence` and whole-run `elapsed_ms`.
  A stage has `stage`, `stage_id`, `occurrence`, `parent_id`, `status` and a fixed English message;
  terminal executed stages include monotonic `duration_ms`. Skips have no invented duration.
  Nested stage durations overlap and must not be summed. A result event carries the existing
  response contract: a clarification/safety/provider-blocked result is not itinerary completion.
- Product progress excludes research versions and detail payloads. Developer adds `version`,
  observed admission/selection/generation-input counts, validation finding IDs/types/status counts,
  per-round repair target IDs and permitted operations, and returned target outcomes. Permissions
  are not a claim that an edit was performed or a problem resolved. Final JSON remains complete.
  No prompt, chain-of-thought, intermediate draft or raw trace payload is streamed as progress.
- Optional request-local observation covers requirements, destination, candidate acquisition,
  retrieval, weather, routes, official information, generation, date checks, transfer binding,
  validation, repair stage/round/preparation/model/revalidation and Nearby where executed.
  Repeated validations have distinct occurrences and parent links to their enclosing repair work.
- Each connection owns one producer task. Iterator closure, disconnect and ASGI send failure
  cancel it and await cleanup, including through Starlette cancellation scopes. Four connections
  remain independent. Heartbeats every 15 seconds are comments, not synthetic progress. The
  bounded 256-event buffer reports `dropped_events` if a slow consumer misses progress; it does
  not promise a complete replayable audit log. The final event remains deliverable.
- Product's still-V0 execution now uses the same request-owned runtime rather than a cached
  mutable model client. V0 source and all research CLI scripts remain unchanged. Shared preference
  interpretation and V1/V3 mechanisms have optional observation hooks; outside an observation
  scope they preserve inputs, results, exceptions and policies. No algorithm, prompt, repair budget
  or model-call policy was changed. Product-only introductions are not implemented yet.

Abort the POST fetch to request cancellation; no separate cancellation endpoint, persistent job,
reconnect or reload recovery is added. Disconnected clients cannot be promised a final cancellation
event. Already dispatched provider work may still finish remotely. Public deployment must protect
or disable Developer endpoints. Live provider/proxy streaming acceptance is still pending.

Validation snapshot: the first focused run passed 124 tests with one heartbeat test failure: the
test assumed a released producer must finish before the next heartbeat. It now explicitly waits
for producer completion instead of depending on a 10 ms scheduling race. Subsequent focused
tests passed, including iterator closure, ASGI disconnect and ASGI 2.4 send-failure cleanup.
Actual V0 execution and the V3 graph/repair chain were tested with external boundaries faked;
their real mechanism hooks emitted progress without extra model calls. Full backend regression
passed 1498 tests with 9 skips. Frontend baseline passed 33 tests in 6 files, lint and build.
Ruff formatting/line-length findings were corrected; final Ruff and git diff --check passed.
V0 implementation, backend/app/llm and all four research runner scripts still have no diff.
V1/V3 and shared services contain the optional observation changes listed above, not research
algorithm changes. No live Azure/provider run, formal evaluation, commit or push occurred.

### Review corrections: cleanup and truthful repair timing

The review of the first two batches identified two lifecycle/observation defects and one coupling
issue. These corrections supersede the corresponding second-checkpoint behavior:

- Application dependency release now happens outside the planning execution timeout. Async close
  operations are shielded and awaited on the same event loop, including repeated caller
  cancellation. Partial setup still closes already-created clients; one client close failure does
  not prevent the others from being attempted or replace the original setup exception. Cleanup
  may extend wall-clock request completion beyond the planning allowance; it grants no additional
  planning/model/provider work. Resource close failures are logged with a generic message, not
  provider payloads. A permanently non-returning close remains a limitation: no new forced-close
  policy or independent cleanup timeout has been introduced.
- Executed repair stages/rounds end with an execution status and actual duration even when the
  business repair result is SKIPPED. Developer details separately carry repair_status, reason,
  model_attempted and target outcomes. Only explicitly unexecuted mechanisms use a skipped event
  without duration. Successful mechanism execution still does not mean successful repair.
- The V3 repair boundary explicitly emits repair_targets metadata, linked by stage_id, with round
  index, target IDs and permitted operations. The generic observer no longer inspects positional
  repair arguments. Positional and keyword calls have the same observation behavior.

Focused verification initially passed 35 tests covering delayed async cleanup, deadline crossing,
timeouts/failures/cancellation, repeated cancellation, truthful timing, actual V3 metadata via
positional/keyword invocation and stream disconnect paths. An additional partial-setup test checks
that all created clients are closed exactly once even when one close fails. No extra model calls,
research algorithm changes, Product V3 activation or React feature work are included in this fix.

Final correction regression: 1506 backend tests passed, 9 skipped; frontend 33 tests in 6 files
passed, with lint and build passing. Ruff and git diff --check passed. V0, backend/app/llm and the
four independent research launcher scripts have no diff. No live execution, commit or push.


### Third implementation checkpoint: Product V3 presentation backend

Product JSON and streaming endpoints now run V3 through the request-owned runtime, with no V0
fallback. A dedicated allowlisted Product contract replaces serialization of research itinerary
objects. It exposes final activities, per-day weather availability, identity-matched transfers,
nested Nearby and optional introductions, without research version identifiers, source place IDs,
route diagnostic ledgers or V3 repair reports. Existing input rewrite feedback is projected to
user-relevant fields; Developer output remains the full research result.

Normalized weather and experience summaries are collected in memory through the existing tracing
boundary. Weather is matched to the requested destination and final dates. Nearby requires a
matching final anchor identity and day. Transfers use V3's final application-owned adjacency ledger,
including elastic-window handling, and check final identities/times. Provider travel time remains
separate from application reserve; unsupported routes do not invent a mode, distance or attribution.

Only Product invokes one optional introduction batch after successful final planning, for primary
POIs only. Existing normalized summaries are supplied where available; otherwise unverified model
knowledge is allowed. Nearby and Developer never trigger this call. It uses the remaining existing
request deadline, capped at 30 seconds, with no retries or new planning allowance. Failure, invalid
output or timeout omits introductions without losing the final itinerary; cancellation propagates
and resources close. Introductions do not change research output, validation or repair decisions.

Offline acceptance includes the real V3 graph with fake model/provider/retrieval boundaries, final
mapping with residual findings, introduction degradation, stale evidence exclusion and unchanged
Developer behavior. The initial full regression found one old test constructing a Product response
directly from a research itinerary; it was updated to exercise the explicit Product projection and
verify research fields are excluded. Its 16-test module then passed. Final full backend regression:
1535 passed, 9 skipped. Frontend baseline: 33 passed; lint and production build passed. Ruff and
git diff --check passed. V0 implementation, shared LLM files and all four research launcher scripts
have no diff. Concurrent route/repair and research-document changes in the working tree are outside
this Product implementation batch. No commit or push was made.
React still needs the required-budget form migration, new response
types, weather/transfer/Nearby/introduction rendering, progress consumption and four-run `/dev`
workbench. No live Azure/provider acceptance is claimed for this checkpoint.

### Fourth implementation checkpoint: React Product and Developer migration

Product `/plan` now requires the whole-trip budget amount/currency, consumes the POST event stream,
shows one indeterminate progress bar with Product messages, and offers Stop. Only a terminal result
can render an itinerary. Existing preference rewrite, safety and provider-blocked states remain;
errors stay generic. Final per-day weather, optional introductions, nested smaller Nearby entries,
route duration/distance/attribution and separate reserves are rendered from the safe Product contract.
Unavailable weather and unverified routes are explicit. The browser performs no extra LLM calls or
feasibility assessment. Research fields and debug panels remain outside Product presentation.

The Developer page is now `/dev`; `/dev/planner` is no longer a page. The unused free-text form was
removed in favor of the shared required fields and an explicit research reference date. Run all
launches four independent POST streams from one copied input snapshot. Each panel has its own
progress bar, backend elapsed/stage durations, repeated-stage identity, detailed counters/findings,
final itinerary and expandable complete result/error JSON. Backend stage completion is not presented
as proof of successful repair. No stage durations are summed into a synthetic total or percentage.

Inputs stay locked while any run is active. Stop per run, Stop all, same-snapshot reruns and page
unmount cancellation are implemented. Editing an idle form clears the previous result group.
Controller/group identity checks exclude late events/results from cancelled or superseded runs.
Stream parsing handles UTF-8/chunk boundaries, heartbeat comments, sequence duplicates, terminal
errors and premature EOF without automatically retrying. Developer history keeps at most 500 events
per run and reports omitted events, including backend buffer losses. Full final JSON remains separate.
No persistence, reconnect/resume, ranking, evaluation, authentication or research algorithm changes
were added. External provider quotas remain shared; stopping local requests cannot guarantee that
already-dispatched remote work stops immediately.

Validation chronology: the first run passed 31 frontend tests and failed three new Developer tests
because their beforeEach hook returned a mock function; changing it to return void fixed the hook.
Lint identified a cleanup-ref warning, which was removed by relying on owned controller identity.
TypeScript rejected an inferred Object.fromEntries cast for the initial four-run state; explicit typed
initial entries fixed it. The next 43-test regression and lint/build passed. Added cross-group,
cancellation and reference-date tests then produced the final result: **47 frontend tests passed in
7 files; frontend lint and production build passed**. Focused backend stream/Product-V3/progress
regression passed **22 tests**. Ruff and git diff --check passed. The previous full-backend snapshot
of 1535 passed / 9 skipped belongs to the preceding batch; it was not rerun for this React-only code
change. V0 implementation, backend/app/llm and all four research scripts remain unchanged.

Real browser/provider streaming, Product V3 and concurrent V0-V3 live acceptance remain pending;
offline tests do not establish provider quota behavior or proxy buffering characteristics. No commit,
push or version freeze was performed.

### Product review corrections after React migration

Two scoped review findings were fixed without changing research execution or Developer behavior:

- Product ignores skipped-stage messages when updating its active progress text. Skipped Repair
  or official-information stages no longer appear to be executing. Later executed stages still
  update the progress message; Developer retains its detailed skipped events.
- Product preserves a final conflicting connection whose departure is bound to the preceding
  activity's actual end, even when that end exceeds the following activity's start. It retains
  the backend CONFIRMED/UNKNOWN state without re-evaluating feasibility. Identity, final adjacency
  and ledger-time matching remain required; early or arbitrary late departures and stale ledger
  entries remain excluded. The React view displays the existing conflict warning and both times
  alongside the returned itinerary.

Focused backend mapping/Product-V3/stream regression passed 28 tests. Frontend regression passed
48 tests in 7 files; lint and production build passed. Ruff and git diff --check passed. These
checks passed on the first post-fix run. No full backend rerun, live provider call, research algorithm
change, commit or push accompanied these fixes. V0, shared LLM files and all four research launcher
scripts still have no diff. Real-provider acceptance remains pending.

### Live acceptance attempt and client-lifecycle blocker

The local API (scripts/run_api.py with the existing environment) and React were started for a
bounded browser acceptance attempt. Browser permission review initially timed out; the permitted
single retry succeeded. Product input: Beijing, 2026-10-01 through 2026-10-03, two travelers,
2000 AUD, preferences "Local food and quiet mornings." Invalid reversed dates disabled submission;
an invalid direct streaming request returned HTTP 422 at request-schema validation.

The valid Product stream returned HTTP 200 and the browser rendered the final three-day itinerary.
Real Azure, Places, Routes and Weather calls succeeded. Daily forecasts, five place introductions,
route estimates and three anchor-nested Nearby suggestions were visible. Product progress/form
locking was observed; no research version or debug panel was visible. This is a bounded functional
observation, not itinerary-quality evaluation or complete branch acceptance.

The subsequent Developer Run all dispatched V0-V3, but all four failed during requirements with
requirement_provider_failed / transport_failure. Independent failure statuses and mechanism durations
were displayed. A single V0 rerun and direct JSON request reproduced HTTP 502 in under one second.
Developer successful completion and live cancellation acceptance therefore remain unverified.

A no-network probe with dummy settings established the lifecycle cause: separately constructed
LangChain-backed planner adapters share a cached HTTP transport; closing one adapter closes the
other, and a later adapter receives the already-closed transport. Request ownership at the wrapper
level is insufficient. Existing mocked dependency tests did not cover this real SDK behavior.
No evidence of provider quota exhaustion was observed. The proposed fix is optional explicit HTTP
client injection in the shared LLM adapter, used by the API to own independent transports while
leaving research entry-point defaults unchanged. Implementation is paused for approval because
backend/app/llm was explicitly excluded from changes. No workaround, cache-clearing patch or
protected-file modification was applied.

Full offline backend regression during this attempt: 1541 passed, 9 skipped. Passing offline tests
does not override this live blocker. No commit, push or additional phase was started.

### Approved transport isolation fix and bounded live retest

Following explicit approval, the shared Azure adapter gained optional sync/async HTTP-client
injection. The API dependency factory supplies and owns fresh transports per request, including
cleanup on partial setup. Unspecified injection preserves existing research defaults. V0 files
and all four research launcher scripts have no diff.

A no-network regression using real SDK objects first reproduced shared transport identity and
then passed with independent clients: closing one request leaves another and subsequent requests
usable. An initial test invocation hit existing temporary-directory permissions; a fresh test
directory resolved that environment issue. The next targeted run exposed 25 harness failures from
forwarding absent injection keywords; omitting those keywords when unset restored compatibility.
The targeted suite then passed 191 tests. Final offline snapshot: 1542 backend tests passed,
9 skipped; 48 frontend tests passed in 7 files. Ruff, frontend lint, production build and
git diff --check passed.

On the restarted real API, Developer V0-V3 all completed from the same Beijing input. Detailed
mechanism events/timings and research JSON remained available. The observed V3 run took about
44.6 seconds, including requirements, candidates, weather, routes, generation, validation and
Nearby; repair was skipped, so this run does not validate an actual repair round.

Cancellation checks: stopping a V0 rerun left a concurrent V1 rerun running and it completed;
Stop all cancelled the sole active rerun without clearing completed siblings. Product stop
displayed the stopped state; immediate resubmission completed and rendered three daily forecasts,
place introductions, anchor-nested Nearby and walking/car estimates with separate pickup/drop-off
reserve. Product showed no research selector or debug panel. These checks demonstrate local
cancellation/reuse, not guaranteed termination or billing cancellation at remote providers.

The earlier invalid-date frontend block and direct HTTP 422 remain the live validation observations;
offline boundary tests establish that invalid requests do not construct planner dependencies.
Page-exit cancellation and every repair/retrieval branch were not live-tested in this retest.
This is development acceptance, not a benchmark, itinerary-quality conclusion or version freeze.
No commit or push was performed.

## Compatible transfer output update (2026-09-25)

The latest frontend-only progress checkpoint is recorded at the end of this document;
earlier implementation checkpoints describe the UI as it existed at that time.

The shared itinerary DTO now accepts optional `transfers` (missing defaults empty).
Current V3 binds and presents verified/unknown per-leg route estimates and separate
application reserves; V0-V2 do not fabricate transfers or acquire additional routes for
this field. Primary model DTO/prompt, K, existing version entry points and product default
are unchanged. The frontend can render this optional data when supplied; this does not
implement the deferred Product V3/API selection or the whole frontend backlog.
See [V3 design](v3_design.md#shared-output-and-frontend) and the
[development verification record](v3_development.md#mixed-transport-and-joint-components-2026-09-25).
This is shared output compatibility, not evidence of a V3-only quality gain or a re-freeze.


## Preference feedback checkpoint (2026-09-25)

Offline-validated. `needs_clarification.issues` carries input disposition and separate issue rows
with exact original quotes, application-owned reasons/actions and current structured field values.
A separate `safety_blocked` response displays support text without echoing sensitive quotes.
React renders quotes as text, never HTML. The form remains populated; edits and resubmission clear
old issue/safety/error/itinerary state. Pending submission remains disabled. System failures stay
neutral and do not request a preference rewrite. See
[shared preference input checkpoint](shared_preference_input.md) for tests and real-model limits.


### Minimum daily coverage update (2026-09-25)

Shared output now reports the one-primary-visit minimum independently of 2-5 review
quantity guidance. V0-V2 remain diagnostic-only; V3 prioritizes confirmed minimum gaps
below hard protections and above optional reviews. Explicit source-linked full-day time
protections support exemptions; uncertain applicability remains unknown. Product output
includes coverage status without research metadata or source quotations. The primary
prompt, default engine and budgets are unchanged. See [shared minimum coverage](shared_minimum_daily_coverage.md)
for counting, compatibility, exemption and partial-result boundaries, and the V3 development
checkpoint for offline and live evidence. This does not retroactively validate historical runs.


### Provider-filtered preference recovery (2026-09-25)

The product response union adds provider_blocked with application-authored message/action.
The planner displays "Please revise your preferences" and explains provider content filtering;
editing clears the result, and only manual submission starts another request. This response is
separate from needs_clarification and structured safety_blocked. Raw provider errors/IDs and
sensitive quotes are not displayed. Other dependency failures keep the generic failure UI.
The page's16 tests and TypeScript/production build passed; no new live evidence.

### Frontend review and determinate progress checkpoint (2026-09-25)

The full working-tree review separated Frontend/API integration and optional observers from
concurrent backend corrections (continuous transfer windows, repair configuration ownership and
final repair-stage summaries). The mixed repair_service file requires hunk-level commit grouping.
No blocking execution defect was confirmed; stale current-status documentation was corrected
without rewriting the earlier live-failure history. Routing cancellation and multi-round repair
display tests passed: 51 frontend tests and 56 focused backend tests at the review checkpoint.

Product now shows one determinate workflow-position bar; Developer shows four independent bars.
Positions are frontend estimates based on actual stage events, not measured work percentages or
remaining-time forecasts. Earlier versions use shorter workflow maps; nested/repeated stages do
not regress the fill. Repair rounds advance within a bounded region without assuming a fixed
number of rounds. Skipped/unknown stages do not advance it; later observed stages can jump ahead.
No timer fabricates progress. Only successful completion fills the bar; failed, paused and
cancelled runs preserve position, while editing/restarting resets it. Product exposes no version
identifier through this mapping. A bounded event history cannot reset Developer progress.

Generate/Run remain primary actions; Stop controls share an outlined stop style, and Rerun uses
a secondary style. Controls share dimensions, focus/hover/disabled behavior. Progress transitions
respect reduced-motion preferences; no numeric percentage is shown.

The first frontend check exposed Windows case-insensitive module resolution between the helper
and component names. Renaming the component to PlanningProgressBar resolved it. The subsequent
suite passed 55 tests across 8 files; lint and production build passed. A real Product browser
check observed forward stage movement and the styled Stop control; cancellation retained position
and restored the form. It was a short cancelled run, not another completed-trip acceptance or
live repair test. No backend/research implementation change accompanied this UI checkpoint.
