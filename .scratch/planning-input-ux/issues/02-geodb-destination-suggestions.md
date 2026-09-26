# GeoDB destination suggestions through backend proxy

Status: resolved
Type: task
Approval: Approved by the delegated scope agent under the user's 2026-09-26 instruction; implemented without live calls or commit.
Blocked by: Further live UI verification requires separate authorization.
Spec: [Planning input UX](../spec.md)

## Scope and files

Implement GET /api/input-assistance/destinations and the shared destination combobox. Proposed
modules: backend/app/api/input_assistance.py, API input-assistance schemas, services/destination_suggestions.py,
integrations/geodb/client.py, settings/config additions, frontend planning API/types and
DestinationCombobox.tsx. Register the router in main.py. Keep provider normalization inside
the adapter and direct HTTP outside graph nodes. No Google autocomplete, maps or new database.

Use the official GeoDB sources and activation caveats in the spec. Confirm current REST types
and metadata before finalizing the adapter; record the exact schema source. The user selected
https://geodb-free-service.wirefreethought.com/v1/geo/places, with types=CITY (HTTPS correction approved after address verification). No RapidAPI
subscription, key, authentication headers or paid fallback. Browser calls only our backend;
the backend-to-GeoDB hop uses HTTPS. Send no preferences, trip facts or credentials.

## Interfaces and limits

q is 2..100 trimmed characters; return <=5 normalized city/region/country choices with stable
IDs. Normal selection fills destination text without passing a GeoDB ID as a Google identity.
Manual input remains allowed. Apply spec budgets: 500 ms debounce, >=1.1 s spacing, 20 form
attempts, one outbound send/3 s deadline/no retries, process-wide 1.1 s guard and 100 daily
attempts. Reject rather than queue; cancellation cannot refund sent calls. Use a fixed host,
disable automatic redirects and validate responses. There is no GeoDB key prerequisite.

## TDD slices

1. Mock provider normalization: homonyms, missing region, Unicode names, zero matches,
   malformed responses; user q is encoded as a parameter, never concatenated into a URL.
2. API admission: short/long input, fixed HTTPS host and no auth headers, result cap, 429/timeout/error
   mapping, no retries, failed sends counted, aggregate rate/daily limits across requests.
   Check redirects are not followed and no unrelated form data is sent upstream.
3. Combobox: prefix debounce, IME composition, old response after newer typing, keyboard
   selection, Escape, edit-after-selection, no-match and manual-entry fallback.
4. Both pages submit the chosen label as the existing destination string. Labels are plain
   text; browser never calls GeoDB directly and there is no extra planning provider call.

## Acceptance and unresolved evidence

The separately approved address verification observed HTTP 308 to same-host HTTPS, then HTTPS
200. Offline replay normalized all five returned places. The approved fixed-URL correction is
implemented without further live calls. The HTTPS assertion first failed against the old URL;
after correction, all 73 API tests passed, including single-send, 3-second timeout configuration,
429, redirect rejection and timeout-without-retry checks. Ruff passed. Evidence is under
artifacts/input-assistance-diagnosis-20260926/. End-to-end live UI behavior remains unverified.

Mocked adapter/API tests plus frontend tests/build pass. Browser uses real proxy/API with a
fake GeoDB port to verify same-name cities and 429 fallback. Daily guard is explicitly local
per-process, not advertised as a durable account cap. Document the free tier's 1 request/second,
10-result page limit and population >=40,000 coverage constraint. Missing small towns must
not prevent manual submission. Confirm free-instance response compatibility, availability and
usage/attribution terms before enabling live use. No real-provider test in this task
without separate approval. Currency/date/weather changes remain intact.

## Comments

- 2026-09-26: User selected the public free HTTP GeoDB instance. RapidAPI plan/key prerequisites
  are removed. Existing budgets and manual fallback remain; implementation awaits approval.
- 2026-09-26: Implemented fixed-host backend proxy, normalized city labels, local process guards,
  shared Product/Dev combobox and failure fallback. The first API/component test run was red from
  missing modules; implementation made it green. A later Escape/edit regression initially failed
  because the test expected a request inside the specified 1.1 s rejection window; after modeling
  the interval correctly it passed. Local-browser checks used a fake GeoDB transport only.
  No real free-instance compatibility, uptime, coverage or attribution claim is established.
