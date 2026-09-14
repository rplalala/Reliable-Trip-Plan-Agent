# V1-A Milestones: Original Freeze and Revised Implementation

## Current Status and Historical Scope

**Original V1-A freeze: explicitly approved on 2026-09-12.**
**Revised V1-A: implemented and offline regression tested; final identical Smoke A
live re-validation and explicit re-freeze approval are pending.**
**Full V1: unfinished and not frozen; V1-B Phase 3 is pending.**

The sections below beginning with "Historical Execution Flow and Comparability"
record the 2026-09-12 as-built checkpoint and its acceptance history. Their
shortlist-first flow, masks, budgets, test counts, and limitations are historical
facts, not the revised selection design or current V1-B completion status.
The revised implementation status is recorded separately below. Actual code remains
authoritative for implemented behavior; `docs/v1_design.md` describes the
current architecture and future V1-B boundary.

After the original freeze, V1-A was intentionally reopened for Google-backed
rating/review evidence and POI-selection realignment. The revised implementation
progressively narrows candidates, acquires ratings and reviews selectively,
normalizes reviews into `ExperienceProfile`, and selects the final POIs
deterministically. `rating` remains separate from the Profile. The revised path
does not request or use `userRatingCount`; its appearance in a historical mask
below is a record of the original implementation, not current behavior.

The former V1-C milestone is retired. Its Places-review responsibility is folded
into V1-A because it affects POI selection. Reddit/TripAdvisor acquisition is not
part of the current approved rating/review direction. V1-B supplements final
selected POIs with official/current evidence; its Phase 1/2 implementation remains
the accepted baseline and is not yet integrated into the graph/planner.

The code-based V1-B compatibility assessment in `docs/v1_design.md` identifies
integration-only impact (category B), with no required redesign of the accepted
Web evidence engine. The revised implementation does not authorize V1-B Phase 3,
frontend rating/review display, or a full V1 freeze.

At the original checkpoint, V1-A asked whether normalized live Places, Weather,
and Routes evidence improved the otherwise comparable V0 planner. It implemented
neither Places review enrichment nor official Web Evidence. It included no RAG,
general feasibility-validation/repair loop, or persistent evidence database. The
following record is implementation history, not a formal research conclusion.

## Revised V1-A Implementation Status (2026-09-14)

### Implemented Flow and Selection Contract

The current independent V1 graph executes:

```text
requirements extraction (TravelRequirements + typed NamedPlaceIntent)
-> shared requested-date validation
-> destination resolution
-> generated/deduplicated search intents -> Places candidate discovery
-> C_raw neutral selection -> R_pool structured/rating Details
-> no-review selection baseline
-> counterfactual decision-sensitive review acquisition
-> ExperienceProfile -> deterministic E_exp -> final deterministic POI selection
-> Weather -> chunked Routes -> evidence-informed itinerary generation
-> shared final itinerary-date validation
```

The LLM extracts requirements and interprets retrieved review text into a bounded
Profile, but does not choose the final POI set. Reviews and Profile influence
selection only; neither is passed to the current itinerary prompt. The selected
Place IDs are projected in final order into aligned `PlaceCandidate[]` and
`PlaceEvidence[]` for current planning and future V1-B Phase 3 input.

The inclusive trip duration `D` determines algorithmic maxima:

```text
K_final         = min(16, 2D + 2)
R_pool          = max(10, K_final + 2)
C_raw           = max(20, 2R_pool)
review_pool_cap = min(6, ceil(K_final / 3))
```

Runtime budgets can explicitly lower effective capacities. The final selector
protects eligible reconciled required Place IDs and greedily scores the rest by
`Q_rel + C_cov + G_geo + R_rating + E_exp`: weighted real search-hit relevance,
uncovered intent coverage, geographic grouping, bounded quantitative rating,
and bounded review-derived experience fit. Stable provider-rank/Place-ID
tie-breakers make the selected set deterministic. Missing rating is neutral;
review/Profile failure gives `E_exp = 0` and leaves structured
`PlaceEvidence.availability` unchanged. Selection conflicts remain explicit.

Typed `NamedPlaceIntent` marks a specific named place `REQUIRED` when the user
clearly expects it in the final trip, including *must visit*, *want to visit*,
*would like to visit*, and *hope to visit*. Conditional/optional names are
`OPTIONAL`; generic categories are not named must-visits. Exact Places identity
reconciliation protects resolved required Place IDs through the funnel. An
unresolved required name is reported, not replaced by a guessed POI. Aliases
such as `MCA` that do not exactly match the provider display name are not
fuzzily resolved.

### Bounded Places, Reviews, and Opening Hours

All supported candidate intents are generated and deduplicated before provider
execution. Destination Text Search has separate normal/hard limits of **1/1**;
candidate Text Search has **12/12**. Twelve is a provider execution budget, not
a semantic maximum on user interests. Execution priority is required named
places, explicit ordinary preferences/categories, then fallback. Excess intents
are traced as `budget_not_attempted`; only actual provider hits contribute to
`Q_rel` and `C_cov`. Broad search keeps an identity/location/status/`openingDate`
mask without rating or reviews. Only the narrowed `R_pool` receives
structured/rating Details; an even smaller decision-sensitive set receives
separate review-only Details. The current normal budgets are `candidates=36`,
`detail_calls=18`, `review_detail_calls=6`, `review_enriched_places=6`,
`profile_llm_calls=6`, and `final_pois=16`.

`CLOSED_PERMANENTLY` is a hard exclusion. `CLOSED_TEMPORARILY` remains with a
date-verification risk. `FUTURE_OPENING` is treated conservatively and excluded
when its known earliest opening is after the trip. Places structured status
does not prove availability on a requested date. Each attempted POI contributes
at most five usable deduplicated reviews to a retrieved-review-only structured
summarizer. Review sensitivity tests reachable `E_exp` values under the same
deterministic selector and attempts only candidates whose membership could
change. Application validation checks Profile Place ID, references, counts,
and signal taxonomy. Confidence is application-derived: one cited review is
`low`, two or more are `medium`, and no `high` value exists. Unsupported signals
remain absent; a failed/unavailable Profile is neutral, with no repair/retry.

Current and regular opening hours remain separate. For each requested date,
planning uses applicable current/date-sensitive hours within their supported
window; otherwise it uses regular weekly hours as a baseline; otherwise hours
are `unknown`. Regular hours are not a guarantee against a holiday or
special-date exception. Official/date-specific verification belongs to future
V1-B integration.

### Weather, Routes, and Evidence Boundary

Weather remains one Daily Forecast request for the provider horizon, normalized
strictly to requested trip dates. The complete directed baseline Route Matrix
supports `N <= 16` final POIs, with at most **64 elements per request**, **256
baseline elements per run**, and **four baseline calls**. Consecutive origin
chunks retain all destinations; N=16 uses four 4 x 16 chunks rather than dropping
POIs. Partial or unavailable elements remain explicit.

An explicitly supported transport mode does not automatically fan out. Default
WALK uses deterministic directed triggers: distance > 3,000 m, duration > 2,700
s, or `ROUTE_NOT_FOUND`, excluding same-place cells. Triggered directions collapse
to logical unordered Place-ID pairs ranked by the more severe directed result.
Sparse TRANSIT acquisition uses one canonical Place-ID direction per selected
pair, bounded by the normal eight logical-pair/eight-call limits; it does not
issue a second full matrix. A provider-observed TRANSIT duration may supply a
reverse **duration-only** `mirrored_reverse_estimate`. The reverse is never
described as provider-measured, and canonical unavailability creates no
fabricated reverse duration. These are representative transport signals, not
line, station, fare, or timetable evidence.

The V1-B Phase 1/2 Official Web Evidence subsystem exists independently but is
**not integrated** into the active V1 graph or itinerary prompt. Phase 3 can
consume the final aligned candidate/structured-evidence projection; it must not
receive Profile objects just because selection used them. Official Web evidence
does not currently affect itinerary generation. The former V1-C is retired.

### Development Validation and Pending Re-validation

These live runs checked integration behavior; they are **not formal benchmarks**
or statistical reliability results.

- Smoke A first selected Sydney Opera House while its required named identity
  remained unresolved. Typed `NamedPlaceIntent` and exact Place-ID
  reconciliation were implemented and covered offline. The identical Smoke A
  live re-validation after this correction remains pending in the current
  acceptance flow.
- Initial Smoke B showed that a shared three-call candidate search budget left
  six explicit interests out of Q/C metadata. The N=16 chunked Routes path
  succeeded and the planner accepted that large integrated request.
- The identical revised Smoke B re-validation used destination search **1/1**
  and candidate search **9/12**: all nine supported explicit intents were
  generated and executed. It recorded 123 raw search observations and 85
  unique Place IDs before `C_raw`; effective pools were `C_raw=36/36`,
  `R_pool=18/18`, final POIs `16/16`, and review/Profile `6/6`. Routes used
  four 4 x 16 WALK baseline chunks (256 elements); structured itinerary
  generation and final date validation succeeded.

The latest backend offline regression after the revised corrections passed
**507 tests**; Ruff lint also passed. Standalone V0 and V1-B Phase 1/2
compatibility checks passed; none of these claims implies V1-B graph/planner
integration. The recorded Smoke B runs checked bounded live integration, but
the pending identical Smoke A re-validation prevents a final live-acceptance
claim. No revised V1-A re-freeze has been approved. These checks do not prove
that generated itineraries always obey every supplied feasibility fact.

### Known Limits and Pending Work

Provider-display-name aliases are not fuzzily resolved. The bounded candidate
search budget may leave additional supported intents `budget_not_attempted`.
Places reviews are a small qualitative sample; Profile interpretation remains
model-dependent despite application provenance checks. Regular opening hours
are only a baseline, and some POIs have unknown hours. Selective TRANSIT covers
only bounded logical pairs. The generator may still imperfectly follow route,
hours, or other supplied evidence. V1 does not perform post-generation general
feasibility validation, targeted repair, or re-validation; that mechanism
belongs to V3, not an unfinished V1-A loop.

Frontend rating/review presentation remains future work: for a final-itinerary
POI, a future Product UI may show only an actually acquired Places rating and,
when available, one concise retrieved-review-derived Profile summary. It must
not invent either or display `userRatingCount`. Full V1 remains unfinished and
unfrozen until separately approved V1-B Phase 3 integration and later validation.

## Historical Execution Flow and Comparability

The independent V1 entry point is `scripts/run_v1.py`. Its fixed, non-agentic
graph is:

```text
START
-> extract_requirements
-> validate_trip_dates
-> resolve_destination
-> search_place_candidates
-> shortlist_places
-> enrich_place_details
-> acquire_weather
-> acquire_routes
-> generate_evidence_informed_itinerary
-> validate_itinerary_dates
-> END
```

Provider calls go through `V1EvidenceAcquisitionService`, provider protocols,
Google adapters, and typed normalization rather than directly from graph nodes.
The V0 requirement-extraction prompt/schema, Foundry client/deployment behavior,
provider-default temperature behavior, base planning objective, and final
`Itinerary`/`PlanningResult` schemas remain the comparison baseline. V0 retains
its independent `scripts/run_v0.py` path and uses no external evidence. V1's
main changed input to generation is normalized external evidence; raw provider
JSON is not passed to the planner.

## Shared Ten-Day Date Contract

`backend/app/policies/trip_dates.py` enforces the project-wide inclusive window:

```text
reference_date <= requested_start <= requested_end <= reference_date + 9 days
final itinerary dates subset of requested trip dates
```

The trusted reference date is captured once at run start in the configured
IANA time zone and reused for relative-date extraction and both validation
boundaries. Product API callers cannot inject an arbitrary reference date;
trusted Developer/CLI/test paths may inject one for reproducibility. Validation
checks itinerary-level, day, and activity start/end dates. Product frontend
pickers use browser-local dates as UX guidance; backend validation also rejects
out-of-window direct API calls. This date contract is not V3 feasibility repair.

## Runtime Configuration and Safety Limits

Final configuration has three layers:

```text
backend/app/runtime/budget_limits.py  global hard safety envelope
config/runtime.yaml                   validated non-secret runtime policy
ToolBudget                            one run's actual reservations and usage
```

One global `TOOL_BUDGET_HARD_LIMITS` mapping defines the project-wide hard
ceilings. Strict Pydantic models reject missing/unknown YAML keys, duplicates,
invalid types, and budgets outside that envelope. The normal committed policy
sets `app.time_zone: Australia/Sydney`, `logging.level: INFO`, and a metadata
Run Trace in project-relative `logs/`. Relative trace paths resolve from the
repository root, independently of the shell working directory.

| Budget counter | Frozen runtime limit | Global hard maximum |
| --- | ---: | ---: |
| candidates | 20 | 40 |
| place_search_calls | 4 | 12 |
| place_detail_calls | 8 | 20 |
| weather_calls | 2 | 3 |
| route_matrix_elements | 64 | 100 |
| alternative_route_pairs | 8 | 16 |
| alternative_route_matrix_calls | 8 | 8 |
| web_search_queries | 6 | 20 |
| page_fetches | 6 | 20 |
| review_enriched_places | 3 | 8 |

The last three counters are configured for the shared budget model but unused
by V1-A. `.env` remains for deployment-specific Foundry endpoint/deployment,
Foundry API key, and Google Maps API key. Budget, time-zone, logging, and trace
policy are not `.env` overrides. Changing an in-range runtime budget requires
only `config/runtime.yaml`; changing a hard ceiling is centralized in
`budget_limits.py`.

## Places and Weather Evidence

Places uses the API (New) in stages. One minimal-mask destination lookup obtains
a coordinate; up to three category Text Searches use location bias, minimal
identity/location/classification fields, and no reviews/photos/rating/hours.
The candidate mask is `places.id,places.displayName,places.location,`
`places.formattedAddress,places.primaryType,places.businessStatus`.
Candidates are deduplicated by Place ID and non-operational statuses removed.
The deterministic shortlist round-robins provider-ranked query categories,
uses stable Place-ID tie-breaking, and is bounded by eight places, the details
budget, and the square root of the baseline Route Matrix element limit.

Only shortlisted places receive Place Details. The detail mask is `id,`
`displayName,location,formattedAddress,primaryType,businessStatus,timeZone,`
`currentOpeningHours,regularOpeningHours,rating,userRatingCount,websiteUri,`
`priceLevel,priceRange,accessibilityOptions`. `PlaceEvidence` keeps place
identity, location, type/status, applicable opening information, timezone,
selected rating/price/accessibility/site fields, availability, and provenance.
An individual details failure is represented as partial/unavailable evidence.
There is no V1-A review request.

Weather uses one Google Daily Forecast request for the provider's full ten-day
horizon, then normalizes **only** dates inside the requested trip range. This
avoids provider/local-calendar boundary mismatches without allowing extra days
into the planner. `WeatherEvidence` contains availability and requested-date
daily condition, temperature range, precipitation probability, and maximum
wind speed when supplied. Provider failure remains explicitly unavailable;
the LLM must not fill missing weather facts.

## Final Routes and Logical-Pair Transport Policy

The original V1-A design used one mode-specific matrix. Live testing showed
that a default WALK matrix could identify an impossible walking transfer but
could not offer an alternative. The approved final policy retains a fully
directional, bounded baseline matrix and adds selective TRANSIT evidence only
for default WALK. A user-explicit supported mode remains single-mode and does
not trigger an automatic alternative. `DRIVE` uses `TRAFFIC_UNAWARE`;
non-DRIVE modes do not send that routing preference.

For default WALK, each directed pair is non-walkable when distance is strictly
greater than 3,000 m, duration strictly greater than 2,700 s, or the condition
is `ROUTE_NOT_FOUND`. Same-place elements are excluded. The two directions of
a POI pair collapse into one unordered logical pair, ranked by the more severe
directed WALK result. Stable ascending Place-ID order chooses the canonical
TRANSIT direction. The highest-ranked pairs are selected within both the
`alternative_route_pairs` and `alternative_route_matrix_calls` budgets; pairs
sharing a canonical origin are grouped into sparse one-origin matrices. No
full second N-by-N TRANSIT matrix is issued.

Each selected logical pair requests exactly one real TRANSIT matrix element.
The request includes a representative departure time at the trip start date's
destination-local 12:00, converted to UTC by the Google adapter. A successful
`provider_observed` element belongs only to the queried direction. Its reverse
may receive a `mirrored_reverse_estimate` containing **duration only**; it does
not copy provider distance, status, condition, or directional timetable facts.
An unavailable canonical result produces no fabricated reverse duration.
`RouteEvidenceBundle` carries baseline WALK, bounded alternatives, and all
detected logical non-walkable pairs with explicit availability/provenance.
TRANSIT durations support coarse grouping and time allowance, not exact
navigation, fares, service lines, or timetables.

## Request Cache, Run Trace, and Failure Semantics

Each run creates one in-memory `RequestCache` and `ToolBudget`. Canonical
request keys deduplicate identical Places searches/details, Weather requests,
and ordered Route Matrix requests, including mode, field mask, departure time,
and relevant options. Cache hits do not consume a second provider budget;
there is no persistent evidence cache.

The CLI creates one immutable `run_id` and a best-effort local trace at
`<project-root>/logs/<UTC timestamp>_<run_id>/`. `run.json` records input,
fixed reference date/window, requested dates, status, tool usage, final outcome,
the allowlisted effective runtime configuration, and its deterministic SHA-256
hash. `events.jsonl` records graph progress, provider/cache activity, routing
trigger evaluation, selected/truncated logical pairs, canonical directions,
representative departure time, alternative results, and failures. Optional
`llm/`, `tools/`, and `evidence/` payloads depend on the configured level.
The frozen default is `metadata`, with raw provider payload capture disabled.

Trace serialization recursively redacts recognized credential keys, bearer
tokens, assignments, and sensitive URL query parameters. The project-owned
console logging handler also redacts provider URL credentials, including
credentials that HTTP client INFO logging might otherwise print. `logs/` is
gitignored and is observability output, not application persistence. Tests use
disabled tracing or temporary directories. A trace write failure disables
tracing without changing planner output or provider semantics.

Missing critical requirements, invalid trip dates, no viable candidates,
generation failure, and final-date violations stop a run. Individual Places
Details failures, partial Routes results, and Weather unavailability remain
explicit partial/unavailable evidence. No V1-A validation/repair loop follows
generation.

## Final Sydney Live-Flow Acceptance Case

The final complete live flow used this new request: a one-day Sydney trip for
two travellers on 2026-09-15, interested in harbour views, wildlife, and
beaches, preferring moderate walking without unnecessarily long walking
transfers. The run used `reference_date = 2026-09-12`; the allowed window was
2026-09-12 through 2026-09-21. Requirements and final itinerary dates were
both 2026-09-15 and passed the shared date checks.

The live path exercised Azure Foundry, Google Places, Google Weather, and
Google Routes. Four Places searches, including destination resolution,
yielded 16 bounded/deduplicated candidates and an eight-place shortlist;
only those eight received rich details. The one Weather call returned
available evidence; the default metadata-level trace did not retain its
daily condition/temperature payload, so no unverified weather values are
reconstructed here. The default baseline was one directional 8 x 8 WALK
matrix (64 requested elements). Threshold evaluation found 42 directed
non-walkable results, collapsed them to 21 logical pairs, selected eight,
and recorded 13 budget-truncated pairs.

For a compact record of the actual canonical TRANSIT selections, `P1` through
`P8` denote the eight Places in `shortlist_created` order in this run's
`events.jsonl` (run ID `83b678ac-3331-43b7-b9b0-847662d1a7e6`). The
metadata trace retained Place IDs, not a complete normalized name mapping:

```text
P1 ChIJV_wrHl2uEmsR92Q_ubhgXDI
P2 ChIJLat3W0euEmsRCQCK0yaDjTc
P3 ChIJQyYU8QOrEmsRFno4dKGQTYo
P4 ChIJf2-DIACvEmsRgudjrmfw2Lo
P5 ChIJi4HdHKCZEmsRYPPy-Wh9AQ8
P6 ChIJm_XsjvyqEmsRQNv6iYFYSXA
P7 ChIJswapWjeuEmsR_QZi2zrhtRI
P8 ChIJ7fQkR0y3EmsRAvF7TJkyUd4
```

Canonical directions queried:

```text
P5 -> P6, P3 -> P5, P8 -> P5, P4 -> P5,
P1 -> P5, P2 -> P5, P5 -> P7, P8 -> P6
```

The two `P5` destinations and two `P8` destinations were grouped by canonical
origin, producing six sparse TRANSIT calls for eight real requested elements.
All eight real elements were provider-observed, with eight separately labeled
duration-only mirrored reverse estimates. The representative departure time
was 2026-09-15 12:00 Australia/Sydney (`+10:00`), not an itinerary timetable.
Routes usage was **one WALK call / 64 elements + six TRANSIT calls / eight
elements = seven calls / 72 requested elements**. ToolBudget recorded
`route_matrix_elements = 64/64`, `alternative_route_pairs = 8/8`,
`alternative_route_matrix_calls = 6/8`, `weather_calls = 1/2`,
`place_search_calls = 4/4`, `place_detail_calls = 8/8`, and
`candidates = 16/20`; Web/review counters remained zero.

The run completed and its metadata trace recorded the config snapshot/hash,
logical-pair trigger and grouping events, observed/mirrored counts, budgets,
and final date validation. The redaction check found no configured API key in
the trace. This was an **integration and evidence-acquisition acceptance case**,
not proof of a perfectly feasible generated itinerary or a formal V0/V1
quality comparison.

## Live Discoveries, Follow-Up Fixes, and Known Limits

The following were post-design discoveries, not capabilities present in the
initial V1-A proposal:

- **Provider/runtime defects fixed:** real Places `timeZone` is an object with
  `id`/`version`, so normalization extracts its IANA `id`; Weather requests
  the full provider ten-day horizon and then filters to requested dates;
  credential-bearing Google URLs visible in HTTP INFO logging prompted
  console URL redaction and regression tests.
- **Approved architecture follow-ups:** the initial one-mode WALK route design
  evolved first to selective directed alternatives, then to logical-pair
  collapse, stable canonical TRANSIT direction, one observed element per
  logical pair, and labeled mirrored reverse duration. Runtime configuration
  moved from scattered `.env` budget/trace policy to centralized hard limits
  plus one strictly validated global YAML file.
- **Prompt-level evidence-use follow-ups:** live generation exposed incorrect
  route-number attribution across Place IDs and a visit scheduled before
  supplied opening hours. V1's generation prompt gained exact route-pair ID
  matching and whole-visit opening-hours instructions; a later approved edit
  compressed repeated wording without intentionally changing these rules.
  These are model instructions, not deterministic feasibility enforcement.

Unresolved limitations remain explicit:

1. Evidence-following is not guaranteed. In the Sydney follow-up, matching
   WALK evidence required about 28 minutes while the generated schedule
   reserved about 15. V1-A supplies evidence but does not perform deterministic
   post-generation transfer-feasibility validation. The planned V3 mechanism
   is generation -> explicit validation -> targeted repair -> re-validation;
   none of that is implemented in V1-A.
2. Places-only discovery/selection can surface weak activity candidates. A
   `lodging`-typed place was used as a stop although accommodation was not
   requested. This POI relevance limitation was not redesigned during freeze.
3. TRANSIT is a representative duration at one departure time, not exact
   timetable, route, service, station, or fare evidence.
4. A `mirrored_reverse_estimate` may differ from the actual reverse duration;
   its duration is a planning proxy, not a provider observation.
5. At this checkpoint, V1-A had neither official/current Web Evidence nor
   review-derived experience evidence. Those were then planned as V1-B/V1-C;
   the current reopening above supersedes that milestone allocation.

## Verification and Freeze Boundary

The final complete live V1 flow completed through Places, Weather, Routes,
Foundry generation, and final date validation. The latest backend offline
regression run after the approved prompt compression reported **158 passed**;
Ruff and `git diff --check` passed. Normal automated tests use fake providers
and do not call live external services. The full live run preceded the final
prompt-only follow-ups; no additional full live flow is claimed afterward.

The 2026-09-12 freeze did not authorize subsequent V1-B or former V1-C work,
a commit, a push, a merge, or a formal benchmark. V0 and V1 remained independently
runnable; V2/V3 were not implemented or frozen at this checkpoint. Later
reopening, implementation, and partial live validation are recorded separately
above and must not be read back into this original checkpoint. The revised
V1-A is not yet re-frozen.
