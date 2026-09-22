# Shared structured input and semantic requirements

## Authoritative form and dates

Current PlanningRequest uses planning_request_2. Destination, date-only start/end, strict positive
traveler count and whole-trip Money are mandatory. Money is a finite non-negative Decimal with
explicit uppercase three-letter currency; boolean amounts are rejected. Empty/null/whitespace
preferences become empty; nonblank text is preserved. Additional preferences are bounded at
24,000 characters and 8,000 engineering tokens. request_id is optional. End cannot precede start.
The selectable window contains 14 calendar dates, from trusted today through today+13 inclusive.
Trip duration is independently limited to 1-10 inclusive days. The trusted date uses the configured
application time zone (currently Australia/Sydney), not the browser or destination clock.
Product requests cannot supply the CLI's research reference-date override.

## One interpretation and canonical identity

Nonempty preferences receive one shared interpretation; empty preferences skip the model.
Form facts are never converted to prose for re-extraction. Conflicts are reported, not used to
override the form. Current canonical contract is interpreted_requirements_3. Historical _2
records retain their original meaning. Model handles (up to 256 characters) are temporary;
application-owned canonical identities are independent of V1/V2 and discovery provider.
Attribution distinguishes party, specified people/subgroups, and unresolved targets. first_ref
does not confer priority. Unknown links fail; empty attribution is not silently made party-wide.

## Open text with structural bounds

SemanticRequirement contains requirement_id, normalized_text (up to 320 characters), kind
(preference/constraint/goal), polarity (favor/avoid), strength (low/medium/high/hard), scope
(individual_poi/selected_poi_set/whole_trip/itinerary_style/transport), subjects and source_refs.
The vocabulary of normalized_text remains open; it is not a fixed interest taxonomy.

Draft bounds: 24 semantic requirements, 24 named intentions, eight subjects, eight discovery
intents, 32 requested-place-information items, 120 linked experience requests, six operational
conflicts and eight extraction issues. Each item has one to three source quotes of at most 320
characters plus occurrence; canonical references retain validated offsets and match mode.
Each semantic item has up to nine canonical subject references. DiscoveryIntent links one to four
requirements, contains at most 200 characters, and has activity_or_category or semantic_discovery
purpose. Runtime query work has its own smaller limit. Source integrity does not itself prove
semantic interpretation correct. Deduplication rewrites links without double reward.

## Operational meanings and enforceability

Named place text (up to 160 characters) retains REQUIRED/OPTIONAL/EXCLUDED; the model cannot invent
Google identity. RequestedPlaceInformation and transport remain typed because acquisition/routing
have mechanical meanings. Experience requests use evidence-specific dimensions with up to three
preferred and avoided values, dimension membership, uniqueness and disjointness checks. They do
not define the whole semantic preference vocabulary or turn category priors into experience facts.

The application owns RequirementAssessment. Current assess_requirements assigns evidence_assessment
for linked review requests and semantic_only otherwise, initially not_acquired/unknown. There is
no registered predicate certifying arbitrary open text. HARD semantics receive clarify and trigger
unsupported_hard_requirements; soft requirements advise. Explicit REQUIRED identity resolution is
a separate operational boundary. Neither an LLM belief nor UNKNOWN can certify satisfaction.
No downstream keyword/regex reinterpretation of raw preferences is introduced.

Source owners: schemas/request.py, schemas/interpreted_requirements.py,
schemas/requirement_boundary.py, policies/interpreted_requirements.py,
services/preference_interpretation.py and the Foundry DTO/mapping. Migration evidence belongs to
[development_record](development_record.md), not this design contract.


## Calendar support versus same-day remaining-time planning

Current trip_dates admits today through today+13, with end-start+1 <=10. The shared validator
serves V0/V1/V2, CLI and development runners; capacity depends on duration, not departure offset.
GET /api/planning/date-window publishes the server's bounds without initializing any model/provider.
The frontend end-date maximum is min(start+9, allowedEnd); backend submission validation is authoritative.
The developer page initializes its explicitly editable research reference date from the same endpoint.
Unavailable date-policy loading disables product submission; no browser-local fallback is guessed.

Same-day remaining-hour planning remains unsupported. Accepting today's date does not claim that
past hours will be avoided. The earlier proposal for future evaluation (start >= reference+2)
was constrained to eight days under the old +9 window. That arithmetic is historical: delayed
10-day trips now fit. No formal evaluation protocol is implemented or authorized by this extension.
The historical Sydney ten-day smoke and its original checkpoint remain unchanged.

## Default generation objective versus user requirements

The shared 2-5 main-POI/full-day objective is application generation guidance, not a new
user HARD requirement or semantic extraction rule. Explicit pace/rest and long REQUIRED
visits may justify fewer visits. Diagnostics preserve linked semantic requirement IDs
without interpreting raw words or converting target misses into clarification or failure.
Same-day remaining-hour feasibility is still unsupported. Named and HARD boundaries
are unchanged; REQUIRED count above 16 still reports a capacity conflict.
