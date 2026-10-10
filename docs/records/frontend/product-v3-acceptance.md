# Product V3 live acceptance and transport isolation

Historical development observations from September 2026; not a version freeze or benchmark.

## Live acceptance attempt and client-lifecycle blocker

The bounded local API/browser acceptance used Product input: Beijing, 2026-10-01 through 2026-10-03, two travelers,
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
leaving research entry-point defaults unchanged. The adapter was outside the original change scope, so diagnosis preceded separate
approval; the fix described below was not yet implemented at this first checkpoint.

Full offline backend regression during this attempt: 1541 passed, 9 skipped. Passing offline tests
does not override this live blocker.

## Approved transport isolation fix and bounded live retest

Following explicit approval, the shared Azure adapter gained optional sync/async HTTP-client
injection. The API dependency factory supplies and owns fresh transports per request, including
cleanup on partial setup. Unspecified injection preserves existing research defaults. V0 files
and all four research launcher scripts have no diff.

A no-network regression using real SDK objects first reproduced shared transport identity and
then passed with independent clients: closing one request leaves another and subsequent requests
usable. The next targeted run exposed 25 harness failures from
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
