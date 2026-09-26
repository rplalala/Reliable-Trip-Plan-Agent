# Planning input assistance and itinerary presentation

Status: resolved
Approval: Task 01 approved directly; the user delegated Tasks 02 and 03 scope approval to a sub-agent. All three are implemented offline; the user approved the four local commit groups on 2026-09-26.
Date: 2026-09-26
Type: specification

## Goal and authority

Improve the shared Product/Dev form with GeoDB destination suggestions, currency selection,
locale-independent dates and optional preference polishing. Make daily weather subordinate
to the itinerary. The user selected GeoDB, replacing the earlier Google autocomplete proposal.
Preference polishing should improve the likelihood of Gate acceptance by expressing the same
intent more clearly, without weakening requirements or bypassing policy. Acceptance is not guaranteed.

PROJECT.md remains the project source of truth. This is a new proposed iteration after the
closed semantic/quantity iteration at 40b0b26. Existing uncommitted closure documentation is
outside these implementation tasks. This specification now records approved offline implementation;
no real provider call, subscription purchase, live run, version freeze or formal evaluation
was authorized. The later user approval permits the four local commit groups only.

## Current seams

- Shared form: frontend/src/features/planning/components/PlanningForm.tsx.
- Shared itinerary/weather view: frontend/src/features/planning/components/ItineraryView.tsx.
- Date policy: frontend/src/features/planning/datePolicy.ts; backend date-window endpoint.
- Product and Dev keep their existing planning and SSE endpoints and version dispatch.
- PlanningRequest accepts destination text and ISO calendar dates; budget is amount plus an
  uppercase three-letter currency. Existing preference ceiling is 24,000 characters / 8,000 tokens.
- Preference prompt/gate remain authoritative. Assistance is a separate application service,
  never a LangGraph node or an automatic preprocessor for every planning request.

## Required behavior

### 1. GeoDB destination suggestions

Use a keyboard-accessible combobox with city, region and country labels. Begin only after
two trimmed characters; debounce for 500 ms and space requests by at least 1.1 seconds.
Do not query during IME composition. Cancel obsolete frontend requests and discard stale
responses. Escape closes suggestions; arrows and Enter select without submitting the form.
Selecting a city fills a normalized city/region/country string. GeoDB IDs are UI identifiers,
not Google place IDs or planner evidence. Keep the existing destination string contract;
normal planning resolves its own destination. Editing a selection clears its selected identity.
No geolocation, automatic country restriction, geocoding or extra Details call is required.
Manual entry remains valid when there are no matches, missing configuration or service failures.
English-name prefix search is the first release; do not claim Chinese transliteration support.

### 2. Currency selection

Use a searchable, accessible single-select; submit only a listed currency code. Default AUD
in both surfaces. Proposed first-release list: AUD, USD, EUR, GBP, CNY, JPY, CAD, NZD, SGD,
HKD, CHF, KRW, INR, THB, MYR, IDR, VND, PHP, AED and ZAR, with English currency names.
Keep the list in one frontend module, not repeated inside pages. No inference from destination,
exchange-rate lookup, conversion, amount change or backend-wide currency restriction. Direct
API clients retain the existing three-letter validation contract. The UI list is intentionally
bounded, not represented as exhaustive worldwide currency coverage.

### 3. Compact daily weather

Show one compact horizontal strip on desktop: condition, temperature range, precipitation
probability and wind speed, with units. Use a compact attribution/source link; put longer
attribution and forecast caveats in an accessible disclosure without losing required credit.
Missing values are omitted; unavailable weather gets one short honest message. At narrow
widths allow wrapping without horizontal page overflow. Activities remain visually dominant.
Do not turn UNKNOWN into a weather value or change weather acquisition/planning behavior.

### 4. Locale-independent dates

Display and accept YYYY-MM-DD with an English calendar popover; do not rely on native
input[type=date] localization or on lang=en alone. Retain keyboard entry, labeled fields,
accessible calendar navigation, focus return and Escape behavior. Validate real calendar
dates before lexicographic range checks: reject impossible dates, partial dates and rollover.
Use existing server-authoritative 14-date window and 10-inclusive-day limit; Dev's reference
date also uses the same display component, while retaining its existing override semantics.
The date component is controlled; it does not fetch its own date window. No UTC/local date
shift is allowed. No new UI library is assumed; choose a small maintained accessible component
only after documenting dependency/version implications during implementation.

### 5. Gate-aware preference polishing

Add Polish preferences beside the field. It is an explicit user action, independent of
Generate itinerary. Preserve the original while showing a proposed English rewrite and
short change explanation, with Apply, Dismiss and one-step Undo. Empty input does not call
the service. Disable duplicate polish requests. Editing preferences or structured trip facts
while a request runs invalidates its response; applying text triggers normal onEdit handling.
Do not auto-apply or auto-submit. Repeated manual use is bounded, not an automatic retry loop.

Rewrite spelling, grammar, clause separation and references when meaning is supported. Align
expression with the existing distinction between ordinary interests, soft quality wishes and
mandatory conditions. Preserve negation, modality, exact/minimum/maximum counts, names, dates,
time scopes, accessibility restrictions, exclusions, currencies, amounts and expense scope.
Never infer a numeric quota from rich/varied, turn a liking into a must, replace mountain
climbing with indoor climbing, or remove an unsupported hard condition to gain acceptance.
Structured trip facts are read-only context, not instructions to silently resolve conflicts.
Genuine contradictions or missing decisive meaning return needs_input and a focused question.
Irrelevant text must not become invented travel wishes. Provider/safety blocks are not repaired
by euphemisms or repeated calls. Original text remains available on every failure.

Use one draft call and, only for a candidate rewrite, one independent preservation-review
call over original, candidate and read-only context. The reviewer must explicitly find no
lost/added/strengthened/weakened meaning; fail closed to needs_input if uncertain. Deterministic
checks additionally catch length, malformed output and changed explicit numeric/date/currency
tokens; these are safeguards, not proof of semantic equivalence. Neither model may mutate
structured fields. Model-based review is fallible: preview remains mandatory, and normal
planning still executes the unchanged Gate. Do not show Gate passed based on polishing.

## Proposed application interfaces

Both surfaces share these FastAPI endpoints under /api/input-assistance. No new service,
database, queue or distributed cache is needed; keep external clients behind backend services.

| Interface | Input | Successful public output |
| --- | --- | --- |
| GET /destinations | q: trimmed string, 2..100 characters | suggestions: up to 5 {id, city, region: nullable, country, country_code, label}; source: geodb |
| POST /preferences/polish | original_text; context: {destination, start_date, end_date, traveler_count, budget}; client_revision: bounded opaque string | status: suggested / unchanged / needs_input; original_text; suggested_text: nullable; explanation; questions: bounded list; client_revision |

Polish context has no version selector or writable replacement fields. Use dedicated strict
schemas, not PlanningRequest's whole planning admission, so assistance can explain a conflict
without changing it. Context fields may be omitted when the form is incomplete; never guess them.
Only suggested returns a nonempty suggested_text; unchanged/needs_input never replaces input.
Render all provider/model text as plain text. Do not return prompts, credentials or raw envelopes.

Errors: 422 invalid/beyond assistance input limits; 429 application/provider throttling with
bounded retry-after when known; 503 unavailable configuration/service; 504 elapsed deadline;
502 invalid provider/model result. Errors use {error: {code, message}, client_revision?};
client_revision is echoed for polish requests when available. A provider/safety block returns
HTTP 422 with code polishing_blocked and a sanitized message, leaving the original intact;
it is an error outcome, not a fourth success status or a candidate rewrite. No automatic
provider/model fallback. GeoDB uses the explicitly selected free HTTP service described below;
this does not change model transport. No new planning endpoint fields are necessary.

## Proposed budgets (application limits, not provider-plan promises)

| Operation | Ceiling / behavior |
| --- | --- |
| Destination result | 5 suggestions, offset 0, no pagination or follow-up request |
| Destination provider send | 1 per admitted request; 3 s total; zero SDK/application retries |
| Destination process guard | 1 outbound request per 1.1 s; reject rather than queue; concurrent form tabs share this guard |
| Destination form allowance | 20 attempts per mounted form session; then manual input remains available; no client cache required |
| Destination development allowance | 100 outbound attempts per UTC day per backend process, including failed sends; restart resets this local guard |
| Polish source text | <=4,000 characters and <=1,500 tokens; do not truncate; longer text remains usable by normal planning |
| Polish model sends | <=2 per click: draft then preservation review; no automatic retries or Gate calls |
| Polish model tokens | <=8,000 input tokens per call including prompts/context; draft <=2,000 output, review <=1,000; total output <=3,000 |
| Polish deadline | 20 s per call within one 40 s end-to-end deadline; disconnect cancels pending work where supported |
| Polish form/process allowance | 3 clicks per form session; one in-flight request per process; 20 admitted operations per UTC day per process |

These are separately named input_assistance configuration values, with strict validation;
they must not consume/reset/increase planning, semantic assessment or Repair budgets. Provider
attempts already sent still count after cancellation. Reject locally before constructing clients
when input/configuration/budget fails. Per-process guards are bounded local-development controls,
not account-wide spending enforcement across restarts/workers. Before public deployment, confirm
model-provider account hard caps and shared-user limits; adding production abuse infrastructure is
outside this scope. GeoDB uses the public free service without a paid subscription; model cost
cannot be fixed without the selected model tariff. Existing destination budgets remain unchanged.

## GeoDB evidence and unresolved activation conditions

Checked 2026-09-26 using official-site search excerpts. Direct page opens timed out; no live
API request, account login, credential inspection or subscription change was performed.

- User selected the public free HTTP instance. Proposed backend request:
  GET http://geodb-free-service.wirefreethought.com/v1/geo/places with namePrefix=q,
  sort=-population, offset=0, limit=5, languageCode=en and types=CITY.
  No RapidAPI account, subscription, key or authentication headers are required for this route.
  [Test drive](https://geodb-cities-api.wirefreethought.com/docs/guides/getting-started/test-drive)
- Name-prefix search, population sorting and language-specific matching are supported.
  Region/country metadata disambiguates suggestions; prefix matching is not fuzzy spelling correction.
  [Find Places](https://geodb-cities-api.wirefreethought.com/docs/api/find-places)
- The official pricing page lists the public free service at 1 request/second, page size 10,
  population >=40,000 and no HTTPS. Small towns may be absent; manual input remains available.
  [Pricing](https://geodb-cities-api.wirefreethought.com/pricing)
- Published REST schema lists CITY among the places type filters and population sorting.
  It describes the RapidAPI host, so free-instance parity and runtime availability remain
  unverified until a separately approved live check.
  [REST schema](https://wirefreethought.github.io/geodb-rest-api-docs/)

Frontend calls only the application's backend; FastAPI calls the fixed free HTTP host. This
keeps browser requests on the application's existing origin/transport and avoids browser
mixed-content calls to GeoDB. The backend-to-GeoDB hop remains unencrypted. Send only the
destination prefix and fixed search parameters, never preferences, trip facts or credentials.
Disallow arbitrary hosts and automatic redirects; normalize and validate returned data as
untrusted plain text. No paid fallback or GEODB_RAPIDAPI_KEY configuration is included.

Before live activation, confirm free-instance availability, response fields, applicable usage
and attribution terms. No subscription/key approval is needed. Actual latency and coverage
remain unverified; fixtures are not proof of service availability. Offline implementation can
proceed after approval. Live calls remain separately gated by the user's no-live instruction.

## TDD seams and acceptance

Use real shared components, service/API boundaries and simulated external ports. Tickets below
define red/green slices, not tests against private implementation. Preserve prior date, SSE,
completion-state and independent-version regressions. Validate both Product and Dev in browser
using mocked services, including an OS/browser with Chinese locale. No real-provider acceptance
is authorized. A later narrowly scoped live check requires its own approval and budget.

All five behaviors must work together; stale assistance may never overwrite a newer form.
No misleading Gate-success badge, free-service promise or semantic-equivalence guarantee.
Use a small set of development examples to check rewrite fidelity and controlled Gate outcomes,
not a formal benchmark or claimed improvement percentage. Known-good rewrites must not introduce
new blocks; genuine hard conflicts must stay visible. Actual model Gate-success improvement
remains unverified until separately approved model testing.

## Tasks and sequence

1. [01: Shared form and compact weather](issues/01-shared-form-and-weather.md).
2. [02: GeoDB suggestions](issues/02-geodb-destination-suggestions.md), after 01.
3. [03: Gate-aware polishing](issues/03-preference-polishing.md), after 01; independent of 02.

Execution was sequential 01 -> 02 -> 03 to avoid shared-form conflicts. Each task used targeted
tests, followed by full-suite validation and Standards/Spec review. No task implies permission
to commit. Preserve the four existing closure-document modifications.

## Comments

- 2026-09-26: User authorized the local specification and three tasks only, with GeoDB research,
  interfaces, budgets, TDD points and acceptance criteria; implementation awaits approval.
- 2026-09-26: User selected free HTTP GeoDB. Replaced the RapidAPI proposal and removed
  subscription/key prerequisites; retained proxy architecture, call limits and manual fallback.
- 2026-09-26: User approved Task 01 only, using TDD, with no live run or commit.
- 2026-09-26: User later delegated scope approval for Tasks 02 and 03 to a sub-agent and asked
  for implementation, tests and code review through the commit-plan approval point. The agent
  approved 02 then 03 within this specification. No commit or external live call was performed.
- 2026-09-26: Offline Product/Dev browser checks used a local API with GeoDB MockTransport and
  fake model replies. They covered suggestions, selection, manual fallback, reviewed rewrite,
  Apply/Undo, uncertainty and blocked error. At 375 px the rewrite preview had one column and
  no horizontal document overflow. This does not validate real GeoDB availability or real-model
  Gate success. Two-axis review findings were repaired and rechecked.
- 2026-09-26: The user approved the four local commit groups. Implementation was committed as
  9a147d6 (01), 1ec1738 (02), and 31071c9 (03), followed by the local documentation group.
  Intermediate staged snapshots passed their relevant checks. The four prior closeout documents
  were preserved unchanged; no push or live verification was performed.
