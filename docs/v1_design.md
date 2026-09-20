# V1 external-information design

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

V1-A uses Google Weather Daily Forecast only. It does not initially request current
conditions, hourly forecast, history, or public alerts.
Weather is supplied for itinerary scheduling and planning; V1 does not reselect
the final POI set from weather observations.

<a id="b-e1bc78c1062d-1"></a>

One provider request covers the full supported ten-day forecast horizon.
The normalizer then retains only records whose destination-local display dates satisfy:

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
