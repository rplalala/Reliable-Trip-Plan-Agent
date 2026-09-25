# V1 external-information design

Shared correctness correction (2026-09-25, offline-validated): route timing checks use the
continuous free interval at the bound departure, including WALK/basic DRIVE. A later gap cannot
justify departing across fixed rest. No mode, budget or primary-generation policy changed.
See [review correction evidence](v3_closeout.md#authorized-post-checkpoint-review-corrections--2026-09-25).

Current shared/V3 engineering checkpoint (2026-09-25): see [closeout](v3_closeout.md)
for current configuration, shared ownership and artifact-verified evidence. Earlier dated
implementation/live statements below retain their original scope. V0 remains tool-free;
V1/V2 do not run Repair; the product default remains V0. Provider recovery UI is offline-only.


## Google discovery, identity and shared acquisition

The V1 runner owns request-level providers, cache, budgets and trace. Named/default/semantic Google
discovery precedes canonical admission and acquisition. REQUIRED identity uncertainty is not
silently dropped; EXCLUDED identities remain excluded. Existing typed provider evidence resolves
named places; first rank or a fuzzy name is not identity proof. Melbourne market/station ambiguity
remains a separate known limitation. Search bias is not a strict nearby guarantee.

Destination/candidate searches, Details and selective Reviews retain separate counters. Shared
[supply](shared_poi_supply.md) owns C/G/K, cache/attempt handling, Profile and deterministic selection.
Final supply receives Weather/Routes/Official Web before primary generation. Provider failures
are explicit partial/unavailable evidence, not permission to re-interpret or repair the request.
V2 reuses these components without a second tool architecture.

## Weather Design

<a id="b-e1bc78c1062d-0"></a>

Current V1/V2 use the shared Open-Meteo Weather Forecast adapter. Google Weather was retired
on 2026-09-22; historical runs retain their original provider identity. No current/hourly/history,
alerts, extra geocoding or second-provider fallback is introduced.
Weather is supplied for itinerary scheduling and planning; V1 does not reselect
the final POI set from weather observations.

<a id="b-e1bc78c1062d-1"></a>

One request to https://api.open-meteo.com/v1/forecast uses explicit start_date/end_date,
timezone=auto, temperature_unit=celsius and wind_speed_unit=kmh. It requests only the trip's dates,
including delayed departures, rather than today's first D days. The provider-neutral DTO and
normalizer retain only destination-local records satisfying:

```text
requested_start <= weather_date <= requested_end
```

No pre-trip or post-trip provider record may reach the planner.

The minimal evidence is:

<a id="b-e1bc78c1062d-5"></a>

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

<a id="b-2cbe63deb3b2-0"></a>

The adapter and normalized `PlaceEvidence` retain `currentOpeningHours` and
`regularOpeningHours` separately. For each requested planning date, V1 uses
applicable current/date-sensitive hours only inside their supported date window;
otherwise it uses the matching regular weekly description as a baseline;
otherwise the day's hours are `unknown`. The planner sees this per-day basis,
not an undifferentiated provider hours blob. Regular weekly hours do not prove
that no holiday or special-date exception exists. V1-B can acquire official
evidence when a decision-relevant date-specific need or concrete risk remains.

## Implemented Routes Design

<a id="b-58f6e0026185-0"></a>

Routes support grouping and transfer feasibility, not POI discovery. The final
POI count is at most 20. The baseline is a complete **directed** N x N Route
Matrix, including same-place cells. Instead of truncating POIs to fit one
request, V1 partitions consecutive origins deterministically while each chunk
retains all destinations. The normal baseline budget is 64 elements per request,
400 elements per run, and at most seven calls. N=16 still uses four 4 x 16 chunks;
N=20 uses six 3 x 20 chunks plus one 2 x 20 chunk. This preserves every directed pair
without changing the 64-element per-request limit or alternative-route allowance.
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
logical pairs, not another full N x N matrix. The default quality_first_1 policy permits 16 pairs/calls and 16 measured one-way elements,
grouped by canonical origin.
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

<a id="b-bd65aa33b648-1"></a>

```text
Final selected POIs + aligned structured Places evidence
-> Deterministic residual needs and concrete operational/date risks
-> Bounded WebEvidenceProvider acquisition / optional bounded page retrieval
-> Single EvidenceReasoner
-> Deterministic Evidence Acceptance Gate
-> Claim-scoped EvidenceResolver
-> Accepted/effective facts and explicit uncertainty in planner context
```

<a id="b-bd65aa33b648-2"></a>

The current provider uses Luna/Azure Foundry Web Search behind the
`WebEvidenceProvider` abstraction. Web Search fills decision-relevant gaps; it
does not repeat already sufficient structured observations or create broad
operational-exception tasks for all selected POIs. Optional page retrieval is
used only when native evidence is insufficient. The Gate checks source,
authority, support, subject/scope, and applicability before a claim can become
`OfficialCurrentEvidence`. No experience Web Search path exists.

<a id="b-bd65aa33b648-3"></a>

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

<a id="b-bd65aa33b648-4"></a>

V1-B uses place identity, relevant structured facts, first-party website guidance,
requested dates, requested facets, and subject scope. Rating or a review-derived
summary is not an authority-domain source and must not become official evidence.
The Reasoner interprets only supplied source text; QUERY CONTEXT remains separate
from SOURCE EVIDENCE. Grounding checks cited sources/provenance, while the Resolver
handles accepted facts by dimension, subject scope, and date.

<a id="b-bd65aa33b648-5"></a>

The implemented contracts live in `evidence/web_models.py`,
`evidence/official_models.py`, `evidence/effective_models.py`,
`services/web_evidence_acquisition.py`, `services/official_web_grounding.py`,
`services/official_web_integration.py`, `versions/v1/official_web.py`, and
`versions/v1/official_planner.py`. Phase 3 preserves the Phase 1/2 evidence
semantics while connecting the final-shortlist boundary.

## V1 Planner Estimated-Cost Contract

<a id="b-53bcc5df7d09-0"></a>

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

<a id="b-b250cbdb0be2-1"></a>

```text
authoritative official source
> authoritative structured provider
> other recent web source
> visitor/community experience
```

<a id="b-b250cbdb0be2-2"></a>

Rating and review-derived experience cannot override confirmed factual evidence,
including official date-specific closure. Accepted V1-B Grounding and Resolver
semantics remain in force; incompatible facts preserve conflict and uncertainty.
This is pre-planning evidence handling, not V3 itinerary validation or repair.

<a id="nearby-discovery"></a>
## Post-itinerary Nearby discovery

Only successful primary generation and existing validation reach discover_reference_recommendations.
Extract anchors from scheduled source_place_id resolved in existing supply coordinates. Skip
generic/unlocatable activities with reasons; no anchor Details or fuzzy identity. Sort by date,
start time and activity ID, deduplicate places. Representatives use non-transitive 300 m reuse,
with only the first three areas eligible to search. Reused results must remain within 800 m of
the actual associated anchor, not merely the representative. Early areas may leave days uncovered.

Google Nearby uses DISTANCE, an 800 m circle, restaurant/cafe/park/museum, ten results/request,
three actual sends/trip and zero retries. RequestCache keys include center, radius, types, rank,
language and field mask. Hits do not consume sends; failed sends do. Deadline is ten seconds;
each request at most four seconds and remaining time. Cancellation/cleanup is awaited, preventing
background output mutation. No type quotas, fill loops or fairness/clustering research are added.

Field mask: places.id, places.displayName, places.location, places.formattedAddress,
places.primaryType, places.types, places.businessStatus, places.attributions. No wildcard, rating,
reviews, opening hours or routing summaries. Check real identity/name/coordinates, suitable type,
radius, known exclusions/ineligibility, and scheduled/reference dedup. UNKNOWN does not reject
alone or establish preference satisfaction. Stable distance/ID sort and anchor round-robin select
at most three references. Application reasons use type/anchor/straight-line relationship only.

No new recommendation model, full Details, Profile, Routes or Web stage is added. Preserve actual
attribution. Search failure, timeout, no anchors, exhaustion or invalid attachment returns primary
with partial/empty references and status. User cancellation propagates. Main fields remain unchanged;
[output](shared_itinerary_output.md) owns the three ledgers. Nearby cannot repair sparse main plans.

## Shared first-draft checkpoint

Shared generation guidance, explicit activity roles and observational daily diagnostics
apply before Nearby. Long-trip supply is K18/K20 for nine/ten days; acquisition is still
bounded at C64/G32/send40/P8. Full baseline Routes support 400 directed elements in at
most seven requests. Alternatives and all discovery/enrichment budgets are unchanged.
This does not guarantee daily coverage or introduce post-generation refill/repair.
See [shared output](shared_itinerary_output.md#first-generation-roles-and-diagnostics)
and [shared supply](shared_poi_supply.md) for the single detailed contract.

## Open-Meteo mapping, uncertainty and terms

Official references checked2026-09-22: [forecast](https://open-meteo.com/en/docs) and
[terms](https://open-meteo.com/en/terms). Forecast documentation supports up to16 days; project
selection remains14 dates with maximum10 travel days. This is not a completeness guarantee.

| API daily field | Internal field | Meaning/unit |
| --- | --- | --- |
| weather_code | condition | Documented WMO description; unknown codes remain null |
| temperature_2m_min/max | min/max_temperature_c | Daily extrema in Celsius |
| precipitation_probability_max | precipitation_probability_percent | Daily maximum probability, percent; not precipitation amount or guaranteed rain |
| wind_speed_10m_max | max_wind_speed_kph | Daily maximum in km/h |

Units are checked, not assumed. Missing/nonfinite/unusable values remain null. Source is
open_meteo:daily_forecast; evidence retains the returned IANA time zone, attribution and missing_dates.
A present but entirely null date is missing usable coverage. Partial fields/dates give PARTIAL;
no usable observations or provider failure gives UNAVAILABLE. Actual dates with partial fields remain
inspectable; no adjacent-day copying occurs. Cache identity includes provider, coordinates, exact
start/end, timezone and fixed metric/aggregation selection. Retries, cancellation and Weather budget
are unchanged. The shared factory still uses the same Google Places/Routes clients and credentials.

Free endpoint terms permit non-commercial public research/education with CC BY4.0 attribution;
published limits include fewer than10000 calls/day,5000/hour and600/minute. Commercial deployment
requires separate service eligibility review. Normalized data link Open-Meteo and retain attribution;
UI includes conditional forecast attribution and the license link. No key is needed for this endpoint.
Model forecasts are uncertain, especially at longer lead times; UNKNOWN is not good weather.

Implemented with bounded Tokyo development-live evidence on2026-09-22. V1 and the separately
authorized V2 rerun each returned all five fields for all ten requested dates; raw, normalized and
planner projections matched. This is one request, not a general coverage guarantee. The earlier
London direct probe and historical Google404 results retain their original outcomes. Detailed
execution, the initial V2 capture-factory failure and limitations are in the
[shared development record](development_record.md#tokyo-weather-window-live-20260922).


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


## Shared first-generation mixed transport (current offline checkpoint)

V1/V2/V3 now use shared baseline routing, bounded pre-generation mixed-mode options,
one primary generation, and actual-adjacency/time transfer binding before the version's
post-primary step. V1/V2 report conflicts and UNKNOWN without repairing activities.
V3 reuses the same evidence and adopted transfers in its existing validator and Repair.
V0 remains tool-free. This is a shared baseline upgrade, not V3-exclusive mechanism value.

The normal planning supply is unchanged: this does not rediscover omitted POIs, increase K,
or add a second discovery pass. Default WALK preference permits evidence-supported TRANSIT
and DRIVE alternatives; explicit supported requirements remain restrictive. Representative
TRANSIT never inherits final-time PASS. Provider duration and DRIVE application reserve are
separate. The primary projection retains all directed baseline facts in a compact catalogue;
it drops redundant wrappers, not inconvenient facts. No selective fact omission is performed.
Unbound actual adjacencies remain in application-owned `route_diagnostics`, including
per-mode facts and unresolved alternatives; absent transfers do not erase obligations.

Primary input is 252000, output 16384. Supplementary totals are 32 directed pairs / 32 sends /
64 requested elements; post-generation reservations are 16 / 16 / 32 within those totals.
Baseline remains 7 / 400 / 64. Cumulative route-work wall time is 120 seconds with 30 seconds
reserved for post-generation, always inside the original request deadline. Other acquisition,
Repair and Nearby limits are unchanged. Common transport policy now belongs to `transport`
in runtime.yaml; Repair-only authority and added-burden policy remain version-specific.

Implementation and tests are recorded in `docs/v1_development.md`. This checkpoint has only
offline evidence; historical development live records are unchanged and do not validate it.
No new live, evaluation, freeze, commit or push is implied.


## Shared preference input gate checkpoint (2026-09-25)

Implemented + offline-validated only. All V0-V3 entries reuse the existing single preference
interpretation call to assess request-level input issues before travel acquisition. Application
policy checks exact provenance and returns rewrite/clarification or dedicated safety outcomes;
VALID does not certify feasibility or override hard-requirement/capability checks. Empty input
still skips interpretation. Model contract/provider failures remain system failures. Product
engine selection and travel budgets are unchanged. Historical live runs were not retroactively
validated with this feature. See [shared preference input checkpoint](shared_preference_input.md)
for contracts, compatibility, API/UI behavior, actual test chronology and serializer limits.


### Minimum daily coverage update (2026-09-25)

Shared output now reports the one-primary-visit minimum independently of 2-5 review
quantity guidance. V0-V2 remain diagnostic-only; V3 prioritizes confirmed minimum gaps
below hard protections and above optional reviews. Explicit source-linked full-day time
protections support exemptions; uncertain applicability remains unknown. Product output
includes coverage status without research metadata or source quotations. The primary
prompt, default engine and budgets are unchanged. See [shared minimum coverage](shared_minimum_daily_coverage.md)
for counting, compatibility, exemption and partial-result boundaries, and the V3 development
checkpoint for offline and live evidence. This does not retroactively validate historical runs.
