# Frontend and API design

Current shared/V3 engineering checkpoint (2026-09-25): see [closeout](v3_closeout.md)
for current configuration, shared ownership and artifact-verified evidence. Earlier dated
implementation/live statements below retain their original scope. V0 remains tool-free;
V1/V2 do not run Repair; the product default remains V0. Provider recovery UI is offline-only.


React separates product routes / and /plan from /dev/planner. Vite proxies /api and /health to
FastAPI in development. Product POST /api/planning dispatches through PlanningService to V0;
developer POST /api/dev/planning is explicitly V0-only. Neither exposes V1/V2/config selection.

The product form has structured destination/dates/travelers/preferences, but budget remains
optional while backend total amount/currency is mandatory. Frontend response types omit some
clarification issues. Developer UI retains older free-text input against a structured backend.
These gaps are not completed migrations. ItineraryView separates primary and reference roles;
references are not scheduled or costed activities. Supplied-place wording is stale for Nearby.

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

Status: accepted product direction and TODO, not implemented or validated by this record.
V3 is still being updated. Defer the concrete implementation plan, file breakdown, event/API
contracts and integration work until its current behavior can be checked again. The current
implementation described above and the historical frontend milestone remain separate from this
backlog. Keep the existing MVP layout and basic styling; visual redesign has lower priority.

### Product execution and input

- [ ] Switch Product planning through `PlanningService` to the programmatic V3 runner. Keep
  `/` and `/plan`, a version-agnostic Product API, and no user-facing engine selector or automatic
  fallback to V0.
- [ ] Align the form with the current shared `PlanningRequest`: destination, start/end dates,
  traveler count and whole-trip budget amount/currency are required; additional preferences are
  optional. Continue obtaining date bounds from the backend, with authoritative backend validation.
  Product users do not supply `reference_date`.
- [ ] Display a valid returned itinerary even when repair leaves unresolved findings. Existing
  user-relevant findings may be translated into concise notices, distinguishing confirmed issues
  from insufficient evidence. Completion means execution finished, not whole-trip feasibility or
  quality approval. Do not add a frontend evaluator or reject an available itinerary solely because
  findings remain. Formal evaluation belongs to separately authorized later research work.
- [ ] Keep research versions, provider/stage debug details and raw JSON panels out of Product UX.
  User-facing weather/route attribution remains appropriate. Map presentation data in the backend;
  do not send unrestricted research output and merely hide it in the browser.

### Developer execution and isolation

- [ ] Move the workbench directly to `/dev`, replacing `/dev/planner` as its page location.
  Retain the separate Developer layout and local-development deployment warning.
- [ ] Replace the legacy raw `request_text` form with the shared structured input, retaining the
  visible research `reference_date`. One Run all action starts V0, V1, V2 and V3 simultaneously
  from the same input snapshot and reference date.
- [ ] Give each run an independent identity, progress stream, result, error, cache and mutable
  usage counters. Sharing configured limit values must not pool consumed budget across versions.
  Each version follows its own applicable tool/token/deadline limits; V3 repair rounds share only
  that V3 run's cumulative repair allowance. Do not add a combined four-version budget.
- [ ] Keep failures, exhausted budgets, timeouts and single-run cancellation isolated. They must
  not automatically cancel the other versions. External provider quotas and machine/database
  capacity can still be shared and may independently affect several runs.
- [ ] Show all four progress bars, with each version's itinerary and expandable detailed events
  and complete result/debug JSON. Support individual reruns using the same input snapshot.
- [ ] Lock the input form while any run in the group is active, and display the group's input
  summary. Editing requires all active runs to finish or Stop all first. A new input creates a new
  group; late events and results must not be mixed into another group.

This is a multi-version execution workbench, not an automated ranking or formal research
comparison system. Clarification UX is deferred: preserve the minimal generic Product handling
and Developer details for now, without adding conversational clarification, partial continuation
or a new clarification design. One version requiring clarification does not stop the others.

### Real execution progress and lifecycle

- [ ] Product has one stage-based progress bar and short, understandable English messages, such
  as "Finding places for your trip", "Checking the weather", "Planning your days", "Checking
  travel times" and "Adjusting your itinerary". Show only stages actually executed.
- [ ] Developer has four independent stage-based bars plus detailed chronological events:
  acquired, filtered and generation-input POI counts; validation findings and types; selected
  repair targets; current repair operations/round; and re-validation outcomes. Report attempted
  repair separately from issues confirmed resolved. Counts must come from actual runtime data.
- [ ] In each Developer run, display actual elapsed time when each mechanism/stage ends, next
  to its terminal status and details. Measure duration on the backend with a monotonic clock
  between the matching start and end, rather than from browser event arrival times. Identify
  repeated executions separately, including each repair and re-validation round. Failed or
  cancelled stages report elapsed time until termination; skipped stages are labelled skipped
  without an invented duration. Show whole-run elapsed time separately. Nested or overlapping
  stage durations must not be summed as if they equal whole-run time. These timings support
  development inspection and are not formal benchmark results.
- [ ] Do not show numeric percentages or invented time estimates. Animate the active stage;
  stages may be skipped or repeated without moving the bar backwards. Final result delivery ends
  the bar; failure or cancellation is a distinct terminal state, not successful completion.
- [ ] Deliver real structured progress through HTTP streaming. Reuse existing tracing where
  suitable and add missing start events; a completed-round artifact cannot represent a live
  "repairing now" event. Do not expose model chain-of-thought or infer progress by parsing logs.
  Exact transport/event schemas remain deferred.
- [ ] Provide Product Stop, Developer Stop per version and Stop all. Page departure/disconnection
  requests cooperative backend cancellation and resource cleanup. Already dispatched third-party
  work may not stop immediately. This MVP has no persistent background jobs, reload recovery or
  reconnect/resume guarantee.
- [ ] Ensure run-scoped metadata/tracing and correct ownership of model, provider and retrieval
  resources. Cancelling one run must not close another run's resources. Verify Windows API event
  loop compatibility with V2/V3 async retrieval during integration.

### Product itinerary details

- [ ] Show acquired weather matched to each itinerary date, including available summary and
  temperature fields with attribution. Missing coverage is explicitly unavailable, not invented.
- [ ] Show one short introduction next to each POI, supplied by the backend stage below.
- [ ] Display returned Nearby recommendations directly beneath the scheduled POI to which they
  are linked. Use a compact nested list with indentation, smaller readable text and lower visual
  emphasis, like child entries in a directory. Label these as optional nearby suggestions; they
  remain outside the scheduled itinerary and do not acquire activity times, planned costs or
  inclusion in the main transport sequence merely because they are displayed under a stop.
- [ ] Preserve the backend's Nearby-to-final-anchor association in the Product presentation data.
  Verify the mapping after repair when integration is planned; an associated day alone does not
  identify the parent activity. Do not infer the parent from display order or similar names.
- [ ] Between adjacent scheduled activities, show the selected transport mode, estimated duration,
  distance and source when available. Show the preceding end and following start times so the
  connection is understandable. Present boarding/transfer allowances separately from route time,
  only when supported by the actual scheduling policy. State vehicle-arrangement needs and
  unverified costs where applicable; do not imply a booking exists.
- [ ] Distinguish provider estimates from conservative scheduling allowances. For example,
  "Driving: about 18 min, 7.2 km; allow another 10 min for transfers" requires the corresponding
  route and allowance. If only a 45-minute fallback allowance exists, show "Route unverified;
  45 min reserved" without inventing mode, distance or Google attribution. These values are
  illustrative, not new hardcoded policies.
- [ ] Associate presentation data with V3's final adopted activities, dates and actual adjacency
  after repair. Do not reuse routes for replaced or reordered stops. Missing matching evidence
  stays unavailable. Display existing relevant connection warnings without implementing a second
  feasibility evaluator in React.

### Backend TODO: final POI introductions

- [ ] After V3 chooses its final itinerary and completes repair, but before returning the final
  response, make one batch LLM call to generate a short introduction for the final itinerary POIs.
  Use existing `description`/`summary` as context where available. When absent, the model may
  generate the introduction from its own knowledge; verification is explicitly not required.
  These introductions are display text and must not become verified planning/validation evidence.
- [ ] Generate introductions in the backend, not in the browser. Do not change the adopted
  schedule or trigger another planning/repair cycle to obtain descriptions.
- [ ] Apply a separate introduction-call timeout within the existing V3 whole-request deadline.
  Skip when insufficient time remains; on failure or timeout, preserve and return the available
  itinerary with missing introductions omitted. Record the failure/skip in Developer diagnostics.
  Product can show "Preparing place introductions" while this stage runs.

### Deferred integration checks and scope

- [ ] Once V3's updates permit integration planning, inspect its current programmatic outputs,
  evidence associations, progress hooks, deadline semantics and dependency lifecycle. Define
  concrete contracts and implementation steps then, without treating this backlog as a completed
  migration or V3 freeze.
- [ ] Verify invalid input rejection before planner/provider execution, correct version dispatch,
  identical group inputs, four-run budget/error/cancellation isolation, truthful progress,
  stage-duration attribution across repeated rounds and terminal states, and final
  weather/route/description and Nearby-to-anchor mapping, including the nested Nearby display.
  Include description failure preserving the itinerary and one
  run exhausting its budget while others continue.
- [ ] Run appropriate backend/frontend regression checks, lint, build and diff checks, followed by
  real Product V3 and simultaneous four-version Developer smoke acceptance. No results for these
  future changes have been claimed or recorded here.

Auth, Profile, Saved Trips, new persistence infrastructure, full UI polish, formal comparison and
thesis evaluation remain outside this backlog. Existing retrieval database integration is required
by the relevant runners, not a new user-data persistence feature. Developer access must be
protected or disabled before public deployment. Implementation and Git operations require their
respective subsequent authorization.


## Compatible transfer output update (2026-09-25)

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
