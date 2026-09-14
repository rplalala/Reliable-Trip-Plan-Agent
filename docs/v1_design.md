# V1 Architecture Design

## Status and Authority

This document describes the implemented V1-A and V1-B architecture.
`docs/v1_milestone.md` preserves the original 2026-09-12 V1-A freeze as a
historical checkpoint and separately records later implementation and live
validation. Actual code is authoritative for behavior.

- Stage 0 shared date policy: implemented and approved.
- V1-A: originally frozen on 2026-09-12; reopened for Google-backed rating/review
  evidence and deterministic POI selection; identical Smoke A live re-validation
  succeeded and the revised implementation was explicitly re-frozen on 2026-09-14.
- V1-B: Phase 1/2 evidence subsystem and Phase 3 graph/planner integration are
  implemented; targeted full-V1 development live validation was accepted.
- Complete V1: explicitly frozen on 2026-09-15 after the one-call semantic-intent
  migration, V1-only itinerary cost hardening, final offline checks, and an
  identical Singapore cross-country development live re-validation.
- Former V1-C: retired from the current architecture. Google Places review-derived
  selection evidence belongs to V1-A; Reddit/TripAdvisor acquisition is not an
  active milestone or part of this realignment.

The active V1 milestones are V1-A and V1-B within one research version. The
**complete V1 milestone is frozen as of 2026-09-15**. This status does not
authorize V2 work or retroactively add later capabilities to either historical
V1-A freeze.

## Research Definition

The research versions are:

```text
V0 = Plain LLM
V1 = V0 + External Information / Tools
V2 = V1 + RAG
V3 = V2 + Validation + Targeted Repair + Re-validation
```

V1 asks whether adding normalized live external evidence to an otherwise stable V0
planner improves itinerary realism, feasibility, and reliability.

The intended V1 flow is:

```text
Requirement Extraction
-> External Information Acquisition
-> Evidence Normalization
-> Evidence-Informed Itinerary Generation
```

V1 does not include:

- Embeddings, a vector database, pgvector, or a persistent corpus (V2)
- General constraint-validation or repair loops (V3)
- A free-form agentic tool loop
- Persistent application or evidence storage

V0 and V1 must remain independently runnable through explicit graphs and entry points.

## Shared Project-Wide Date Contract

### Invariant

Every V0/V1/future V2/V3 run shares this deterministic invariant:

```text
reference_date <= start_date <= end_date <= reference_date + 9 days

Final itinerary dates
subset of Requested trip dates
subset of [reference_date, reference_date + 9 days]
```

The allowed window contains ten inclusive calendar dates. `max_trip_days = 10` is not
an equivalent rule: a short trip outside the allowed window is still invalid.

### Stage 0 Implementation

The shared implementation is owned by `backend/app/policies/trip_dates.py`. It:

- Computes an immutable `TripDateWindow`
- Validates requested start and end dates
- Validates final itinerary dates against the requested range
- Validates itinerary top-level dates, itinerary-day dates, and activity start/end
  calendar dates
- Raises stable deterministic policy errors

Invalid dates fail without retry, regeneration, repair, or date mutation. This is a
shared input/output contract, not V3-style itinerary feasibility validation.

### Fixed Run Reference Date

The trusted date is read once when a run starts and is reused by requirement parsing,
date validation, future provider requests, and final-output validation. No graph node or
provider may independently re-read the current date.

Current Product behavior uses the backend's configured IANA-zone date through
`SystemDateProvider`. Product requests cannot contain `reference_date`. Developer API,
CLI, and programmatic tests may supply a fixed reference date as trusted
research/testing functionality.

### Explicit Production Time Zone

V1-A first moved from implicit host-local time to an explicit IANA time zone
configured through `APP_TIME_ZONE`. The later project-wide configuration refactor
moved this non-secret policy into `config/runtime.yaml`; the current shared setting is:

```text
app.time_zone: Australia/Sydney
```

Conceptually:

```python
datetime.now(ZoneInfo(config.app.time_zone)).date()
```

The runtime includes `tzdata` for platforms that do not bundle IANA zone data. The
implementation preserves one fixed date per run, deterministic injected clocks, no
Product `reference_date` bypass, and trusted Developer/CLI overrides.

### Product Frontend

The Product date picker is a UX boundary with browser-local calendar semantics:

```text
start min = browser-local today
start max = browser-local today + 9 days
end min   = selected start, or today before selection
end max   = browser-local today + 9 days
```

The form validates the same range before submission. It does not use UTC
`toISOString()` slicing. Backend validation remains authoritative for direct API calls.

## V0/V1 Comparability Contract

For requests valid under the shared date contract, V1 must preserve as much of V0 as
possible:

- `TravelRequest` and `TravelRequirements`
- The unchanged base `TravelRequirements` meaning and V0 extraction contract;
  V1 extends the same requirements call with separate typed intent capabilities
- Microsoft Foundry endpoint, deployment, and client behavior
- Model and temperature behavior
- Base planning objective and general itinerary semantics
- Final `Itinerary` and `PlanningResult` contracts
- Fail-fast handling of missing critical requirements

The current Foundry client does not explicitly pass a temperature. V1 must use the same
client construction and provider-default behavior unless a later separately approved
research decision changes both versions consistently.

V1's principal research variable is the normalized external evidence supplied to final
generation. V1 must not introduce a different model, a free-form planning agent, or a
different final output schema merely to use tools.

V0 keeps its explicit two-node graph and successful two-call behavior:

```text
START
-> extract_requirements
-> generate_itinerary
-> END
```

V1 owns a separate state, graph, prompts, runner, and `scripts/run_v1.py` entry point.

## Active Delivery Milestones

### V1-A: Google-Backed Travel Evidence and POI Selection

The implemented revised V1-A includes candidate discovery, lower-cost structured
narrowing, cost-aware rating acquisition, selective Google Places reviews,
review-derived `ExperienceProfile`, deterministic rating/review-aware final POI
selection, Google Weather, and Google Routes. Shared date validation, typed
normalization, bounded acquisition, request-scoped cache, ToolBudget, and Run Trace
remain.

Rating and reviews are selection evidence before the final POI set. Not every
candidate receives rating; not every rating-enriched candidate receives reviews.
The implementation does not request or use `userRatingCount`. The LLM interprets
review text into a bounded Profile but does not choose the final POI set.

### V1-B: Official and Current Web Evidence

V1-B supplements only FINAL selected POIs with current first-party official
operational or policy evidence: closures/disruptions, special opening hours,
admission/ticket rules, and reservation requirements.

The integrated V1-B path includes deterministic residual-gap and concrete-risk task
planning, bounded Luna native Web Search acquisition, provider normalization,
request-scoped caching and budgeting, optional bounded page retrieval, one
EvidenceReasoner, deterministic Grounding / Provenance checks, a claim-scoped
EvidenceResolver, and accepted/effective evidence projection to the planner.
The old broad proactive check for every selected POI was removed. Evidence-level
checks are not V3 itinerary-feasibility validation.

The rating/review realignment did not invalidate this accepted baseline. The
code-based assessment below identifies category B integration-only impact.

### Historical Milestone Allocation

The original plan assigned visitor-experience enrichment to V1-C. That allocation
is retired. Google Places rating and reviews now belong to V1-A because both
participate directly in POI selection. No active V1-C source configuration, Web
experience pipeline, or separate completion gate remains.

The revised V1-A re-freeze was approved after identical Smoke A live
re-validation. V1-B Phase 3 integration, the later semantic-intent migration,
and final itinerary cost hardening were completed and checked before the
explicit complete-V1 freeze on 2026-09-15.

## V1 Semantic Input Boundary

One V1 requirements LLM call returns `TripIntentExtractionResult`: the unchanged
base `TravelRequirements`, `NamedPlaceIntent`, `RequestedPlaceInformation`,
`ExperiencePreferenceIntent`, typed transport preference, and `PoiInterest`.
One compound request may yield multiple independent requested facets. These
bounded contracts describe what the user asks, including target, source span,
subject scope, and applicable date where needed; they do not decide provider
calls or assert an external fact. The separate EvidenceReasoner interprets only
what acquired official source text supports.

The application validates schemas, enums, copied source spans, scope/date
consistency, and conservative Place-ID identity; then it deduplicates, scores,
budgets, triggers tasks, grounds claims, resolves evidence, and routes execution.
Active integrated V1 does not fall back to raw-text phrase/regex classification
for named-place inclusion, requested Web facets, experience preferences,
transport, or POI interests. Older compatibility helpers remain outside this
active semantic path. V0 retains its original requirements schema and calls.

## Implemented V1 Graph and State

The fixed, non-agentic graph is:

```text
one requirements extraction (TravelRequirements + bounded typed trip intents)
-> shared requested-date validation
-> destination resolution
-> candidate search-intent generation and Places discovery
-> C_raw neutral selection -> R_pool structured/rating Details
-> no-review selection baseline
-> decision-sensitive review acquisition -> ExperienceProfile -> deterministic E_exp
-> final deterministic POI selection
-> Weather -> chunked Routes -> targeted official Web acquisition, grounding, and resolution
-> evidence-informed itinerary generation
-> shared final itinerary-date validation
```

`acquire_candidate_funnel` owns discovery through the no-review baseline;
`select_review_aware_pois` owns the bounded review loop and final selection.
`versions/v1/graph.py` then projects selected IDs into aligned `PlaceCandidate[]`
and `PlaceEvidence[]` in final selection order. After Weather and Routes, the
official Web node projects selected structured evidence into targeted tasks,
grounds acquired observations, resolves accepted claims, and prepares bounded
planner evidence. The final generator receives normalized Places, Weather,
Routes, accepted/effective official facts, and explicit uncertainty. It does
not receive rating, raw reviews, `ExperienceProfile`, raw Web observations, or
rejected claims. Profile affects selection only; the LLM does not pick the
final POI set. Raw provider payloads do not enter planner prompts.

## Integration Boundaries

Third-party calls must not be made directly from LangGraph nodes:

```text
Graph Node
-> Evidence Acquisition Service
-> Budget and Request Cache
-> Provider Protocol
-> Concrete Provider Adapter
-> Provider DTO
-> Deterministic Normalizer
-> Evidence Schema
```

Expected provider interfaces include:

- `PlacesProvider`
- `WeatherProvider`
- `RoutesProvider`
- A generic V1-B `WebEvidenceProvider` abstraction

Provider authentication, HTTP errors, response DTOs, and field mapping remain behind
the adapters. Tests inject fake providers/transports and never call real services.

## Places Strategy: Cost-Aware Progressive Selection

### Named Places and Search Execution

V1 requirement extraction returns the typed bundle above, including
`TravelRequirements`, `NamedPlaceIntent`, and `PoiInterest`.
A specifically named place is `REQUIRED` when the user clearly expects it in the
trip, including *must visit*, *want to visit*, *would like to visit*, and *hope to
visit*. Conditional/optional names are `OPTIONAL`; generic categories are not
named must-visits. Deterministic reconciliation requires a matching Places
identity and protects resolved `REQUIRED` Place IDs through the funnel and final
selection. Unresolved required names remain explicit conflicts, not inferred
substitutes. Provider-display-name aliases such as `MCA` are not fuzzily resolved.

All supported search intents are generated and deduplicated before execution.
The candidate Text Search execution budget of 12 is **not** a semantic limit on
the number of user intents. Provider calls are prioritized deterministically:
required named places, explicit ordinary preferences/categories, then fallback.
Intents beyond the budget are recorded as `budget_not_attempted`. Only real
provider hits contribute to selection relevance and coverage; skipped or failed
queries do not create synthetic hits. Destination Text Search has a separate
one-call budget.

### Acquisition and Capacity

For inclusive trip duration `D`, the algorithmic pool maxima are:

```text
K_final        = min(16, 2D + 2)
R_pool         = max(10, K_final + 2)
C_raw          = max(20, 2R_pool)
review_pool_cap = min(6, ceil(K_final / 3))
```

`config/runtime.yaml` limits can lower the effective capacities; reductions are
visible rather than silently changing the formulas. Candidate Text Search uses a
cheap identity/location/status/`openingDate` mask, not broad rating or reviews.
Deduplicated Place IDs are narrowed neutrally to `C_raw`, then to `R_pool` before
Details. Only `R_pool` contenders receive structured/rating Place Details;
selection then computes a no-review baseline. Only decision-sensitive contenders
receive a separate review-only Details request. A review attempt is not made just
to fill a quota.

The current candidate mask is `places.id,places.displayName,places.location,`
`places.formattedAddress,places.primaryType,places.businessStatus,places.openingDate`.
The Details mask is `id,displayName,location,formattedAddress,primaryType,`
`businessStatus,openingDate,timeZone,currentOpeningHours,regularOpeningHours,`
`rating,websiteUri,priceLevel,priceRange,accessibilityOptions`. Review Details
request only `id,reviews.name,reviews.text,reviews.publishTime,`
`reviews.googleMapsUri`. No stage requests or uses `userRatingCount`.

`businessStatus` and `openingDate` inform deterministic eligibility without
pretending to confirm trip-date operation. `CLOSED_PERMANENTLY` is excluded;
`CLOSED_TEMPORARILY` remains with a verification risk; `FUTURE_OPENING` is
excluded only when known earliest opening is after the trip and otherwise remains
date-risky. Failed structured Details cannot be selected as a final POI. Missing
rating contributes a neutral score, not an invented average.

### Deterministic Selection and Review Sensitivity

The selector protects eligible resolved required IDs first, then greedily scores
remaining candidates using:

```text
Q_rel + C_cov + G_geo + R_rating + E_exp
```

`Q_rel` reflects actual weighted search-hit relevance; `C_cov` rewards uncovered
executed intents; `G_geo` favors nearby grouping; `R_rating` is a bounded
quantitative Places-rating adjustment (missing rating is zero); and `E_exp` is a
bounded qualitative fit adjustment derived from Profile signals and explicit
experience needs. Stable provider-rank/Place-ID tie breakers make selection
deterministic. V1 does not ask an LLM to choose POIs. Selection conflicts,
including unresolved/ineligible required names, remain observable.

The review-sensitivity policy calculates reachable `E_exp` values from the
approved signal taxonomy and asks whether a candidate's final-set membership
could change under the **same** selector. It attempts the most decision-sensitive
eligible candidates first, bounded by `review_pool_cap` distinct POIs and the
normal runtime review/Profile budgets. Resolved must-visits do not need reviews
to determine their protected membership. This is bounded information acquisition,
not a validation/repair loop.

### ExperienceProfile and Evidence Separation

At most five usable, deduplicated Places reviews per attempted POI are converted
into `ReviewEvidence`. A structured LLM summarizer may produce one concise
review-derived summary and supported signals for crowding, walking intensity,
accessibility impressions, family friendliness, and visit duration. It receives
only retrieved review text and may not infer official operating facts or use
world knowledge. Unsupported or contradictory dimensions stay absent.

Each signal and any summary cite retrieved review IDs. Application-side checks
validate Place ID, counts, referenced IDs, and allowed signal/value combinations.
Confidence is application-derived: one cited review is `low`, two or more is
`medium`; there is no `high` level. `ExperienceProfile` retains availability,
summary, signals, review count, retrieval/provenance, and explicit unavailability.
Failure of review acquisition or Profile generation yields unavailable Profile and
`E_exp = 0`; it does not change structured `PlaceEvidence.availability`, trigger
V1-B operational-gap logic, or cause automatic retry/repair.

Keep these responsibilities distinct:

| Evidence | Role |
| --- | --- |
| Structured Places fields | Identity, discovery, and structured POI facts |
| Rating | Quantitative POI-selection evidence |
| Reviews / ExperienceProfile | Qualitative POI-selection evidence |
| Official Web | Current official operational/policy evidence |
| Weather | Requested-date weather evidence |
| Routes | Transport-feasibility evidence |

Positive ratings or reviews must never override an official date-specific closure.
Optional review/profile availability remains separate from the structured
Places availability used by V1-B. Profile evidence is selection-only and is not
passed to the itinerary generator.

### Final Selected-POI Contract

V1-A produces a stable final selected order with aligned `PlaceCandidate[]` and
`PlaceEvidence[]`, preserving Place IDs, names, candidate status/search context,
structured hours/status/website, and provenance. Phase 3 connects this final
projection to the Web task planner and supplies resolved named/must-visit Place
IDs and structured opening-date conflicts. It removes rating from the Web
input; reviews and Profile objects never enter the official evidence engine.

### Future Product Display

Frontend rating/review display is future work. For an actually enriched POI that
appears in the itinerary, a future Product UI may display the acquired rating and
one concise review-derived summary from retrieved reviews / ExperienceProfile.
It must not manufacture a summary from LLM world knowledge or use/display
`userRatingCount`. This frontend presentation is not implemented.

## Weather Design

V1-A uses Google Weather Daily Forecast only. It does not initially request current
conditions, hourly forecast, history, or public alerts.
Weather is supplied for itinerary scheduling and planning; V1 does not reselect
the final POI set from weather observations.

One provider request covers the full supported ten-day forecast horizon.
The normalizer then retains only records whose destination-local display dates satisfy:

```text
requested_start <= weather_date <= requested_end
```

No pre-trip or post-trip provider record may reach the planner.

The minimal evidence is:

```text
WeatherEvidence
- destination
- latitude
- longitude
- availability
- days
- retrieved_at
- source_ref

WeatherDayEvidence
- date
- condition
- min_temperature_c
- max_temperature_c
- precipitation_probability_percent
- max_wind_speed_kph
```

Provider failure becomes explicit unavailable evidence. The LLM must never generate or
fill weather values.

## Opening-Hours Temporal Applicability

The adapter and normalized `PlaceEvidence` retain `currentOpeningHours` and
`regularOpeningHours` separately. For each requested planning date, V1 uses
applicable current/date-sensitive hours only inside their supported date window;
otherwise it uses the matching regular weekly description as a baseline;
otherwise the day's hours are `unknown`. The planner sees this per-day basis,
not an undifferentiated provider hours blob. Regular weekly hours do not prove
that no holiday or special-date exception exists. V1-B can acquire official
evidence when a decision-relevant date-specific need or concrete risk remains.

## Implemented Routes Design

Routes support grouping and transfer feasibility, not POI discovery. The final
POI count is at most 16. The baseline is a complete **directed** N x N Route
Matrix, including same-place cells. Instead of truncating POIs to fit one
request, V1 partitions consecutive origins deterministically while each chunk
retains all destinations. The normal baseline budget is 64 elements per request,
256 elements per run, and at most four calls. Thus N=16 uses four 4 x 16 chunks.
Provider status/condition, distance, and duration are normalized with explicit
partial or unavailable elements; a failed element is never a measured route.
`not_observed` means no provider result was observed for that directed element;
it is distinct from an observed `ROUTE_NOT_FOUND` result.

An explicitly supported user transport mode is used without automatic
alternative fan-out. With no explicit mode, WALK is the local baseline. Directed
non-walkable triggers are deterministic: distance > 3,000 m, duration > 2,700 s,
or `ROUTE_NOT_FOUND`; same-place cells are excluded. Triggered directions collapse
into unordered logical Place-ID pairs. Each pair's severity is the maximum of
its triggered directed WALK severities; stable Place-ID order defines one
canonical TRANSIT direction. Bounded sparse TRANSIT requests query only selected
logical pairs, not another full N x N matrix. The normal budget is at most eight
logical pairs and eight alternative matrix calls, grouped by canonical origin.
TRANSIT uses a representative departure time at trip-start destination-local
noon. An observed duration may yield a reverse **duration-only**
`mirrored_reverse_estimate`, clearly distinguished from provider-observed
evidence; no reverse distance/status/condition is copied or fabricated. A
canonical unavailable result yields no fabricated reverse duration. TRANSIT
durations are representative planning signals, not line, station, fare, or
timetable evidence. Trace records directed triggers, collapsed/selected/truncated
pairs, canonical directions, departure time, provenance, and usage.

## Web Evidence Architecture

The integrated V1-B path is:

```text
Final selected POIs + aligned structured Places evidence
-> Deterministic residual needs and concrete operational/date risks
-> Bounded WebEvidenceProvider acquisition / optional bounded page retrieval
-> Single EvidenceReasoner
-> Deterministic Evidence Acceptance Gate
-> Claim-scoped EvidenceResolver
-> Accepted/effective facts and explicit uncertainty in planner context
```

The current provider uses Luna/Azure Foundry Web Search behind the
`WebEvidenceProvider` abstraction. Web Search fills decision-relevant gaps; it
does not repeat already sufficient structured observations or create broad
operational-exception tasks for all selected POIs. Optional page retrieval is
used only when native evidence is insufficient. The Gate checks source,
authority, support, subject/scope, and applicability before a claim can become
`OfficialCurrentEvidence`. No experience Web Search path exists.

The task policy runs only after final POI selection. It deduplicates by Place ID,
information need, trip dates, subject scope, and scope text, merging requested
facets for an equivalent task, then orders
tasks by: (1) required-place explicit residual needs, (2) other named-place
explicit residual needs, (3) required-place concrete operational/date risks,
(4) other named-place risks, and (5) other selected-place risks. Concrete risks
include `CLOSED_TEMPORARILY`, `FUTURE_OPENING`, conflicting or unavailable
structured operational status, and trip-relevant opening-date conflict. A
selected POI with no decision-relevant uncertainty creates no Web task. The
normal six-task budget controls attempted breadth; unattempted tasks remain
explicit, and finding no exception never proves that none exists.
Explicit user needs come from validated typed `RequestedPlaceInformation`, not
another reading of raw user text. Structured residual gaps can still generate
tasks when operational evidence is missing, partial, or conflicting.

V1-B uses place identity, relevant structured facts, first-party website guidance,
requested dates, requested facets, and subject scope. Rating or a review-derived
summary is not an authority-domain source and must not become official evidence.
The Reasoner interprets only supplied source text; QUERY CONTEXT remains separate
from SOURCE EVIDENCE. Grounding checks cited sources/provenance, while the Resolver
handles accepted facts by dimension, subject scope, and date.

The implemented contracts live in `evidence/web_models.py`,
`evidence/official_models.py`, `evidence/effective_models.py`,
`services/web_evidence_acquisition.py`, `services/official_web_grounding.py`,
`services/official_web_integration.py`, `versions/v1/official_web.py`, and
`versions/v1/official_planner.py`. Phase 3 preserves the Phase 1/2 evidence
semantics while connecting the final-shortlist boundary.

## V1 Planner Estimated-Cost Contract

The shared domain `Money` remains a non-negative point-valued Decimal amount,
and `Activity.estimated_cost` remains optional. V1 alone projects the Foundry
itinerary DTO into that domain contract: a valid point is preserved; a clear,
finite, same-currency two-endpoint numeric range may become its Decimal
arithmetic midpoint; an unsupported or ambiguous optional cost becomes `null`.
Other itinerary fields and shared date validation remain strict. The projection
does not invoke a planner LLM repair/retry, change V0, or promote a derived
activity estimate into accepted official admission-price evidence.

## Evidence Precedence and Conflicts

For factual/current information:

```text
authoritative official source
> authoritative structured provider
> other recent web source
> visitor/community experience
```

Rating and review-derived experience cannot override confirmed factual evidence,
including official date-specific closure. Accepted V1-B Grounding and Resolver
semantics remain in force; incompatible facts preserve conflict and uncertainty.
This is pre-planning evidence handling, not V3 itinerary validation or repair.

## Hybrid Orchestration

The application controls:

- Shared date invariant and fixed run context
- Provider selection and field masks
- Search-intent priority, candidate/detail/review limits, and capacity formulas
- Bounded staged candidate narrowing, counterfactual review sensitivity, and
  deterministic final POI selection
- Tool Budget
- Separate Places structured/rating and review-only acquisition
- Transport-mode policy and Route Matrix limit
- Request cache/deduplication
- Targeted V1-B official information-gap and operational-risk triggers
- Evidence precedence
- Run Trace

The LLM controls:

- One-call requirement understanding and bounded typed extraction of named
  places, requested information, experience preferences, transport, and POI interests
- Retrieved-review-only bounded ExperienceProfile interpretation
- Final evidence-informed itinerary reasoning

Typed experience needs are mapped to the bounded signal taxonomy by
application policy. The LLM does not choose provider calls or the final POI set.

## Tool Budget

Every run owns a bounded ToolBudget. Global hard safety limits remain centralized
in `backend/app/runtime/budget_limits.py`; normal non-secret policy remains in
`config/runtime.yaml`. Current normal limits include destination Text Search 1,
candidate Text Search 12, candidates 36, structured/rating Details 18,
review-only Details 6, review-enriched POIs 6, Profile LLM calls 6, final POIs 16,
Weather calls 2, baseline Routes 64 elements/request and 256/run in at most four
calls, selective TRANSIT at most eight logical pairs/eight calls, and Web/Page
limits of six tasks/six logical page fetches. The
algorithmic POI formulas above may yield smaller effective pools; runtime limits
can also reduce them explicitly. Historical 2026-09-12 limits remain labeled
historical in `docs/v1_milestone.md`.

V1-B task breadth is controlled by the Web task budget; acquisition and page
fallback are separately bounded. Cache hits do not consume another Web task.
Check capacity before dispatch; cache hits must not incur duplicate provider
charges, and pagination or retries must not create hidden fan-out. Date validity
remains an independent shared invariant.

## Request-Scoped Cache and Deduplication

The cache exists only for one run. Canonical keys include all request characteristics
that affect a response:

- Places search query, location context, page size, and FieldMask
- Place ID, FieldMask, and language for structured/rating Details and separately
  for review-only Details
- Profile Place ID, usable review identity/content hash, retrieval time, prompt
  version, and LLM configuration identity
- Weather location, date horizon, and units
- Ordered Route Matrix endpoints, selected mode, preference, and FieldMask
- Current Web acquisition identity: place, need/facets/scope, dates, canonical domains,
  task instruction/template, provider identity, and effective provider options

Success, partial failure, and unavailable results are cached within one run so
repeated failure does not cause another provider call or Profile interpretation.
Each distinct budget counter is charged only for actual cache-miss work; the
review-enriched-place counter bounds distinct attempted POIs. No persistent
evidence cache is permitted in V1.

## Run Trace

Every V1 run receives a unique immutable `run_id`. A lightweight tracer records a
timeline without changing planning behavior:

```text
logs/<timestamp>_<run_id>/
├── run.json
├── events.jsonl
├── llm/
├── tools/
├── evidence/
└── error.json
```

`run.json` includes at least:

- Run ID and system version/stage
- Fixed runtime reference date and allowed window
- Requested dates
- Start/finish time and status
- Tool usage summary
- Final outcome
- Sanitized effective `config/runtime.yaml` snapshot and stable configuration hash

`events.jsonl` records ordered lifecycle events such as run start, typed
named-place extraction/reconciliation, date validation, generated and executed
search intents, pool narrowing, Details/rating outcomes, review sensitivity and
Profile availability, final selection scores, per-date opening-hours basis,
Weather, directed/chunked Routes, generation, and failures.

Payload levels are:

```text
metadata
normalized
raw
```

Raw logging is opt-in. Provider payloads and LLM inputs/outputs are recursively redacted
and size-limited before writing. API keys, Authorization headers, bearer tokens, Foundry
credentials, Google credentials, and other secrets must never be logged.

`/logs/` must be gitignored. Tests use `NullRunTracer` or temporary directories. A trace
write failure may produce one safe application warning, but cannot alter output, provider
calls, retries, API status, or planner semantics.

## Failure Semantics

Fatal failures stop the run:

- Invalid/missing critical requirements
- Trip outside the shared ten-day window
- No viable candidates
- Final generation failure
- Final itinerary date violation

Partial continuation is allowed for:

- Individual Place Details failure
- Partial Route Matrix elements
- Weather provider unavailable
- Official Web Evidence unavailable or insufficient
- Price/admission evidence unavailable

Optional enrichment failure is allowed for:

- Places review enrichment failure
- Experience summarizer unavailable

Failures are represented explicitly as unavailable, partial, or unknown. They are not
silently swallowed and do not invoke V3-style repair.

## Database Decision

V1 is database-free. It uses only:

```text
request
-> live evidence
-> in-memory request-scoped cache
-> normalized evidence
-> final itinerary
-> Run Trace
-> end
```

Do not introduce PostgreSQL, SQLAlchemy persistence, migrations, Redis, pgvector,
persistent cache, or a persistent raw evidence store. PostgreSQL/pgvector remains a later
direction for V2 RAG when persistent retrieval data is actually required.

## Testing and Verification

Normal automated tests are fully offline and use fake providers. The existing network
guard remains authoritative.

Required coverage includes:

- Shared date boundaries and fixed clock behavior
- Product API bypass rejection and final itinerary containment
- V0 graph/call/prompt/schema regression
- Places search/structured-Details/review-Details FieldMasks, capacity and
  deterministic selection behavior
- Typed named-place extraction/reconciliation and search-budget priority
- One-call typed trip-intent extraction, source-span validation, independent
  compound information facets, and active-path avoidance of raw-text fallback
- Counterfactual review sensitivity, Profile provenance, failure neutralization
- Per-date current/regular/unknown opening-hours applicability
- Final selected-ID/order alignment and separation of structured/review availability
- Complete directed chunked baseline and bounded selective TRANSIT provenance
- Tool Budget and hidden fan-out prevention
- Weather one-call behavior and exact date filtering
- Route Matrix cap and partial element failures
- Request cache/deduplication
- Run Trace lifecycle, payload modes, secret redaction, disabled tracing, and write failure
- Full fake-provider V1-A graph
- Targeted Web task projection, budget/trigger reasons, Gate diagnostics, effective
  evidence composition, and accepted-only V1 planner projection
- V1-only point/range/null optional cost projection, strict non-cost validation,
  and unchanged V0 Foundry itinerary mapping
- Frontend browser-local window and date ordering

Live smoke tests are separate, explicitly invoked development checks. They use minimal
budgets and do not constitute benchmark design or formal V0/V1 comparison.
The final frozen-V1 offline regression passed **605 backend tests**; Ruff lint
and diff whitespace checks passed. Twenty-five affected files passed the
whole-file format check. Five formatting suggestions in three other affected
files were verified against unchanged pre-existing `HEAD` lines and left intact.

## V1-B Phase 1/2 Compatibility Assessment (2026-09-14)

### Result: B - Integration-Only Impact

At the 2026-09-14 compatibility review, the accepted Web evidence engine remained
valid, while revised upstream selection changed the source, timing, and possible
ordering of its inputs. This was a preimplementation design finding, not the
current integration status. Phase 3 subsequently added the final selected-POI
projection and graph/planner orchestration without redesigning Reasoner, Gate,
or Resolver semantics.

The table below records the **preimplementation compatibility review** that led
to this projection; its proposed stages and then-current graph assumptions are
historical, not descriptions of active V1 code. The current graph includes the
official Web node after Routes and before itinerary generation.

### Preimplementation Dependencies and Phase 3 Adaptations

| Area | Then-current code / assumption | Impact and minimum correction | Planned stage |
| --- | --- | --- | --- |
| Final-shortlist timing | At the original compatibility review, `versions/v1/graph.py` ran `shortlist_places` before `enrich_place_details` and had no Web node. | The revised graph now completes review-aware final selection and projects the aligned final views; Web tasks must consume that set, not earlier contenders. | Connect Web only in Phase 3. |
| Input type and positional alignment | `services/web_evidence_acquisition.py::plan_tasks` accepts two typed lists. `policies/official_web.py::plan_official_web_tasks` requires equal lengths and equal Place IDs at every zipped position. | Select corresponding candidate/evidence records by stable Place ID, then pass both in the same final order. Preserve existing candidate records if a new selected wrapper is introduced; do not invent category/rank metadata to rebuild them. No Web engine interface change is required by the approved high-level design. | Preserve recoverable candidate/structured views in V1-A; perform any boundary projection in Phase 3. |
| Ordering and budget priority | `plan_official_web_tasks` assigns `shortlist_index` by enumeration and sorts by priority group, need order, shortlist index, then stable identity/scope. `WebEvidenceAcquisitionService.acquire` executes that order and reserves budget on cache misses. | Rating/review-driven final ordering can change which otherwise-equal Web tasks receive limited budget. Define the supplied order as final selection order, regenerate indices from it, and retain the existing stronger explicit/must-visit priority groups. This is an observable integration effect even though the engine stays unchanged. | Document the final-order contract in V1-A design; verify priority/truncation at Phase 3 integration. |
| Names and must-visit priority | `official_web.py` detects named places using normalized `PlaceCandidate.name` in the request. Required priority comes from `requirements.required_activities` or explicit must-visit phrases; task names come from `PlaceEvidence.name`. | Preserve those names, IDs, and requirements. A future selection-only must-visit flag or alias will not automatically be consumed by V1-B. Adding such a flag to V1-B would be a separately justified small contract change, not required by the approved realignment. | Preserve existing inputs in V1-A; only propose an extra contract if the next design demonstrates a need. |
| Residual status and hours gaps | `official_web.py::_status_gap_reason` compares candidate status with enriched status, checks `PlaceEvidence.availability`, and tests known statuses. `_specific_hours_sufficient` reads opening applicability and date-bound open/close times. | Retain the candidate and structured status views. A review/profile failure must not turn successfully acquired structured Places evidence into `PARTIAL` and spuriously create an operational Web gap. Optional selection-evidence absence remains separate. | Preserve these semantics during rating/review design/implementation; no current V1-B change is needed. |
| Official authority | `official_web.py::authorized_domains` derives acquisition domains from `PlaceEvidence.website_uri` and configured place/need overrides. `official_evidence_gate.py::_authority_basis` independently validates the first-party/configured relationship. | Preserve the structured website and source provenance for final POIs. Review URLs, rating, and profile text must not become official-domain inputs. More selective enrichment must not silently discard the website required by this existing boundary. | Preserve structured inputs in V1-A; pass them through in Phase 3. |
| Task facets and subject scope | `official_web.py::_admission_facets` and `_requested_scope` interpret explicitly named request sentences. `evidence/web_models.py::WebEvidenceTask` validates facets and scope. | Rating/review signals do not establish a request for a ticket product, exhibition, or operational claim. Leave the accepted facet/scope semantics unchanged and pass original request/requirements. | Phase 3 input wiring only. |
| Search cache identity | `services/web_evidence_acquisition.py::_semantic_cache_key` includes Place ID/name, need, facets, scope, dates, canonical domains, template/instruction, provider identity, and provider options. It excludes `shortlist_index`, priority, rating, and reviews. | Pure reordering changes execution priority, not acquisition identity. Changed names/domains/facets correctly change identity. Do not add review scores/profile content to this Web key. Rating/review caches remain a separate open design decision. | No current V1-B cache change; verify integration retains semantic inputs. |
| Grounding and Resolver | `services/official_web_grounding.py::ground` enforces task/Place ID alignment. `integrations/azure_foundry/evidence_reasoner.py::_baseline_context` exposes only the relevant status/hours and source reference. `policies/official_evidence_resolver.py` uses per-place structured/accepted official facts, not shortlist rank. | These components do not depend on how POIs were discovered or shortlisted. Supply the correct structured place and accepted tasks. No semantic redesign follows from adding selection evidence upstream. | Phase 3 wiring only. |

### Rating, Reviews, Profile, and Model Coexistence

At the preimplementation review, `PlaceEvidence` contained `rating` and
`user_rating_count`; the revised implementation removed `user_rating_count`.
The accepted V1-B policy, acquisition, Reasoner, Grounding, and Resolver paths
do not read rating, raw reviews, or ExperienceProfile.

Rating remains a separate quantitative selection signal. Review/Profile content
is retained for V1-A selection but does not enter the V1-B engine or itinerary
prompt. `EffectivePlaceEvidence` is an operational/policy result, not a
replacement or automatic pass-through for all Place/selection evidence.

Existing evidence/task models use `extra="forbid"`. Consequently, an arbitrary new
selection wrapper cannot be unpacked wholesale into an existing Web model.
The implemented final-ID projection provides the existing aligned candidate and
structured evidence types. Phase 3 consumes that projection rather than
unpacking the selection wrapper into Web task models.

### Category Boundaries and Verification Basis

- A is not the overall classification: final-shortlist timing/source and its
  budget-visible ordering require explicit Phase 3 orchestration/alignment.
- B applies: the evidence engine remains valid with the adapted final inputs.
- C is not currently required. It would become relevant only if the detailed
  design deliberately replaced required candidate/structured inputs, overloaded
  their availability, or required new must-visit metadata inside V1-B.
- D was not identified: there is no current dependency that requires review
  semantics to enter the Web Reasoner, Grounding, or Resolver.

The final tests cover targeted priority groups, shortlist order, semantic cache
identity, facets/scope, budget exhaustion with later cache hits, final-only
task creation, Place-ID alignment, review/structured availability separation,
accepted-only planner projection, graph wiring, and unchanged official
provenance/facet semantics. The Phase 1/2 evidence contract remains the accepted
baseline.

## Final V1 Development Validation and Limits

The revised V1-A live regression resolved Sydney Opera House as a required
`NamedPlaceIntent`, preserved one Place identity with `must_visit=true`, and
removed the earlier unresolved-required conflict. In a separate larger live
request, retrieved reviews and available Profiles changed one final POI
membership; the selected set naturally reached N=16. Four 4 x 16 directed
WALK Route Matrix chunks requested all 256 baseline elements, and the combined
planner produced a structured nine-day itinerary with valid requested dates.

The first full-V1 Web smoke exposed low value from broad proactive checks:
16 selected POIs generated 16 tasks, consuming Web/Page budgets 6/6 and 6/6
without an accepted claim. The narrowed policy was revalidated on a comparable
nine-day request with 16 selected POIs: zero Web tasks, zero Web/Page calls, and
a completed itinerary. Absence of a found exception remains `UNKNOWN`, never
proof that no exception exists.

The positive Australian Museum full-V1 smoke generated two explicit Group-1
admission/reservation tasks. Official `australian.museum` sources reached the
Reasoner and Gate; two claims were accepted. Resolver made
`general_admission_policy` available and `admission_fee` available as free/0.
`ticket_requirement`, `advance_ticket_purchase_requirement`, and
`reservation_requirement` remained `UNKNOWN`. Only accepted/effective facts
and their source references entered the planner; rejected candidates did not.
The planner completed the itinerary without promoting admission status into
unsupported ticket or reservation negatives.

The Melbourne development request then exposed a different boundary failure:
raw-text phrase classification dropped `ADMISSION_FEE` and
`TICKET_REQUIREMENT` before Web planning while preserving two other questions.
The approved semantic migration moved all free-form meanings into the same
one-call typed requirements extraction. The identical Melbourne live re-test
preserved all four requested facets through deterministic task planning. Its
official pages were inaccessible and the requested facets remained `UNKNOWN`;
the re-test validates preservation of user questions, not claim acceptance.

The initial Singapore cross-country full-V1 smoke completed upstream typed
semantics, Places/reviews/Profile, Weather, Routes, and targeted Web, but the
planner produced `Money.amount="1.00-10.00"`; the shared point-valued domain
contract rejected the whole itinerary before final date validation. After the
V1-only optional-cost projection, the **identical** Singapore request with
reference date 2026-09-15 naturally produced the range again at
`days[0].activities[2].estimated_cost`. It became `Decimal("5.50") SGD` without
changing official evidence. The final itinerary had four days, 11 activities,
and nine distinct selected POIs scheduled. National Gallery Singapore and
Gardens by the Bay, both required, were scheduled, and date validation passed.
National Gallery whole-venue requested facets remained `UNKNOWN`.

These are development integration observations, not a formal benchmark,
statistical accuracy measure, universal generalization, or population-level
reliability estimate. Provider relevance does not guarantee visitor suitability:
the Melbourne architecture interest produced professional-service firms as
selected exterior stops. V1 has no tourism-suitability validator or post-selection
repair. Display-name aliases such as `MCA` are not fuzzily expanded. Weather
and Routes affect scheduling but do not feed back into POI re-selection. The
planner may omit a selected POI unless an explicit contract requires it, and
may still imperfectly follow evidence because V1 has no V3-style general
itinerary feasibility validation, targeted repair, or re-validation. PageRetriever
may encounter inaccessible official pages. Bounded Reasoner output can be
truncated at `max_output_tokens`, causing that source assessment to fail safely
while other sources/tasks continue. Conservative subject/scope binding may
reject a plausible claim; bounded Web/Page acquisition may leave facets
`UNKNOWN`. The older `unsupported_price_field` case lacks recoverable causal
evidence; the later free-admission path succeeded without changing its contract.

## Expected V1 Code Ownership

The intended modular-monolith structure is approximately:

```text
backend/app/
├── evidence/
├── integrations/
├── observability/
├── policies/
├── runtime/
├── services/
└── versions/
    ├── v0/
    └── v1/

scripts/
├── run_v0.py
└── run_v1.py
```

Only create modules required by an approved implementation stage. Preserve the
existing V1-B Phase 1/2 baseline. Retired V1-C, RAG, validation/repair, and
database placeholders are not part of revised V1-A.

## Approval Gates

Revised V1-A was explicitly re-frozen after identical Smoke A re-validation.
V1-B Phase 1/2 and Phase 3, the later typed semantic-intent migration, and V1
itinerary cost hardening are implemented and development-live-validated. After
the final 605-test offline regression and identical Singapore re-validation,
the user explicitly approved the **complete V1 freeze on 2026-09-15**.

There is no active V1-C gate. No stage automatically authorizes the next one, and
no commit or push occurs without an explicit request.
