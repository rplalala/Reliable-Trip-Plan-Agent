# Berlin six-day development smoke

Date: 2026-09-28, Australia/Sydney. Status: Executed; original evidence gate failed.
This allowance is exhausted. The plan below preserves its original execution contract,
not standing permission for another run. See assessment.md for the later separately
authorized itinerary-only blind review and subsequent cap/prompt changes.

The user authorized one V0-V3 Berlin live attempt per version in the `smoke tests`
conversation and approved the exact broad preference below. Iteration 2 prepares
and assesses; `smoke tests` executes and reports without changing production code.
This is development validation with a requested qualitative blind preference check,
not a formal benchmark, causal comparison, version freeze, or research conclusion.

## Shared input and freeze

Use adjacent `request.json` unchanged for every version: Berlin, Germany;
October 3-8, 2026 inclusive; two travelers; EUR 3000 whole-trip budget;
`We want to have an enjoyable trip in this city.` The user specified destination,
duration, and preference. Dates, travelers, and budget are neutral scenario defaults
following the earlier six-day setup; they are not additional user preferences.
The trip budget is not a provider spending cap.

Preparation revision: `e68d8e6` on `feature/v3`, plus the development-only launcher
and pre-existing documentation changes. `logs/berlin_six_day_20260928/manifest.json`
records the full HEAD, dirty paths, exact request/runtime/launcher hashes, all
backend Python, scripts, validation tools, YAML configs, dependency lock/project
files, local environment file hashes, corpus manifest/report hashes, and a hash
of relevant process environment overrides. No secret values are published.
The runtime copy changes only trace location and normalized capture level;
raw provider payloads remain disabled. V0 retains its independent CLI and reads
the frozen source runtime for logging. V1-V3 use the frozen runtime copy.

Preparation checks local settings, RAG credential presence, and local corpus
manifests without a database connection or HTTP request. It does not prove that
remote dependencies work or that the database contents have remained unchanged.
Do not rebuild, reindex, change credentials, code, prompts, or runtime limits.
The real Sydney date at each launch is the reference date; stop if the trip
is no longer future or outside the current supported window. Never backdate.

## Execution allowance and stop rules

- Exactly four sequential fresh-process attempts: V0, V1, V2, V3, one each.
  No concurrent cases, extra probes, reruns, alternate prompts, or discretionary
  model/provider retries. Existing bounded semantic correction and V3 targeted
  Repair remain product behavior, not permission to repeat a failed live case.
- 660 seconds outer process time per case, at most 2640 seconds (44 minutes)
  across the four planning processes. V1-V3 retain the shared 600-second request
  deadline. V0 has no such CLI flag and retains its provider timeout plus outer cap.
- V0 is plain LLM: one interpretation and one primary generation, no nomination,
  tools, RAG, validation, or Repair added by this launcher. Each V1-V3 request
  allows one interpretation, one nomination, and one primary generation.
  Nomination: 12 names, 8000 input/2000 output tokens, 20 seconds, zero retries.
- Per V1-V3 request: primary candidate searches 12 including at most 4 nomination
  supplements; destination search 1; primary Details 60. Duration-dependent supply
  and all route/weather/web/profile/Nearby limits remain those of the frozen runtime
  and current policy. These are not aggregate whole-batch or whole-V3 budgets.
- Semantics: 6 calls, 120 total seconds, 45 seconds per call, shared across primary
  preparation and Repair. Do not reset or add to the shared budget.
- V2/V3 initial RAG: 4 queries, 80 positions, 2048 query tokens, top_k 20,
  30 canonical resolution attempts, 30 Details, 4 fallbacks, 360-second stage
  within the remaining request deadline. Existing ledger/cache rules still apply.
- V3 only: quantity review enabled; overfull review disabled. At most 5 Repair
  rounds/model calls, stage/round/model ceilings 360/120/70 seconds within remaining
  request time; each call at most 252000 input/16384 output tokens. Repair acquisition
  stage totals: Google 6 including fallback 1, embedding 1, retrieval 1, canonical
  30, Details 30, route sends 24/elements 32, top_k 10. Existing reserves apply.
  No new Repair target, mandatory Repair run, or soft-gap repair authority is added.
- No Input Polish, autocomplete, frontend introductions, service startup, commit,
  push, production fixes, or automatic quality-driven rerun.
- Use existing Foundry, Google, weather, configured evidence, and TripWorld services
  only. Request network permission directly in the execution conversation before
  launching. A denial before process launch is not a live attempt; a runtime network
  error consumes the attempt. Stop on ambiguous infrastructure state.
- Stop before the next case on source/config/input/environment drift, expired dates,
  credential failure, missing/truncated capture or budget evidence, exceeded budget,
  outer timeout, secret exposure, or unexpected provider. The launcher records
  structural stops; executor also reviews stage counters and logs after each case.
- An ordinary application failure with sufficient safe evidence may be followed by
  the next distinct version. Never retry the failed version. Incomplete results
  disqualify the four-result blind assessment even if other versions finish.
- Call/time/token bounds are engineering ceilings, not a monetary price estimate.
  Record available usage; missing billed tokens/cost are unknown, never zero.

## Evidence and assessment

Preserve the manifest, frozen runtime, input, one-shot locks, launcher stdout/stderr,
each result/execution record, and V1-V3 trace/budget files. V1/V3 additionally use
existing normalized requirement/semantic capture; V3 records Repair capture if
reached. V0 has no injected trace instrumentation, and V2 retains its own CLI trace.
Do not claim equal diagnostic coverage across versions or add calls to fill gaps.

After each run, inspect process and application exit status separately, actual
version, six ordered unique dates, nonempty activities on every date, capture status,
stage limits, known errors, and missing usage. The launcher checks recorded primary
used/limit pairs; the executor must also inspect separate nomination, semantics,
RAG, Repair and Nearby counters against the frozen stage limits. Completion does
not establish factual accuracy, openings, costs, route feasibility, or user utility.

Write an English execution report under `logs/berlin_six_day_20260928/`, distinguishing
facts, inferences, and missing evidence. Report paths and issues to Iteration 2
`01a0e29d-405e-7d82-b894-d95eb7f67632`. Do not diagnose by modifying production.

## Conditional isolated blind assessment

Only after all four applications exit zero and return all six dates with activities,
with no unresolved batch stop, confirm `blind_review_eligible=true` and manually
verify the four complete outputs. Otherwise do not launch a blind reviewer.

The executor may prepare anonymous itinerary documents as reporting artifacts.
Randomize labels A-D once; save the mapping outside the reviewer packet and do not
reveal it until the review is returned. Use the same presentation rules for all four:
preserve destination, dates, every activity in order, title, place/location, start/end,
estimated cost (including unknowns), notes, and optional unscheduled recommendations.
If transfers are present, preserve user-relevant endpoints (resolved to activity
titles), mode, departure/arrival, duration, distance and uncertainty. Do not invent
transfers or fill missing content. Remove only internal IDs, schema/version labels,
provider/source identifiers, validation diagnostics, code paths, and generation
history. Retain user-facing uncertainty and substantive warnings. Verify projection
against source results; do not rewrite or improve the plans.

Then spawn the user-authorized subagent with `fork_turns="none"`. Supply only the
shared input and the four anonymous complete itineraries in the message. Do not
supply local paths, project background, mapping, version names, latency, counters,
or prior preferences/comparisons. Ask it to simulate the traveler, choose/rank plans
with reasons and tradeoffs based only on those contents, allowing ties/uncertainty.
Tell it not to use tools, files, browsing, or infer generation method. Save its full
response before revealing the mapping. No further agents or alternate blind runs.
This is one simulated-user judgment, not evidence of objective superiority.

## Offline preparation validation

Six launcher tests passed: full-order completion and one-shot behavior, source drift,
timeout stop, empty-day blind-review exclusion, recorded-budget overrun stop, and
independent version dispatch. All subprocess planning calls in these tests were
mocked; no live providers were contacted. Production behavior was not changed.

The first offline preparation rejected a copied launcher constant that incorrectly
retained France as Berlin's country; it stopped before creating the evidence directory
or making requests. The constant was corrected to Germany, and the command-dispatch
test now also compares the real input file to the fixed request. All six tests passed
again (2.89s), Ruff passed, and preparation succeeded. A separate fresh process then
verified all 219 frozen source/configuration hashes, launcher/input/runtime/environment
hashes and full HEAD, with zero started cases. Formatting issues found by the initial
lint pass were corrected before freezing. No live failure or retry occurred.
