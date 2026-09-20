# V1 development record

Dated records below preserve original scope, status and evidence; they are not current runtime instructions. Current design is maintained separately. Proposed or unexecuted steps remain unexecuted unless a later explicitly identified record establishes otherwise.

<a id="m-b97ee221ab4b"></a>
## 2026-09-19 - Post-itinerary nearby references (product correction; design only)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-b97ee221ab4b-0"></a>

The user superseded supply-leftover/model-allocated V1 references. The target is independent
nearby discovery after successful primary generation and identity/date checks, anchored only
to actual scheduled canonical places with known coordinates. Main itinerary activities remain
unchanged. V0 retains one model generation call and no external tools. This correction does
not resolve the two-place/empty-third-day primary generation limitation recorded above.

<a id="b-b97ee221ab4b-1"></a>

Read-only inspection confirmed the current shared Foundry reference DTO, supply-only source
validator, graph ending after date validation, Text Search location bias, request-local cache
and no-retry transport. Official Google documentation supports a dedicated Nearby Search
adapter with a circle restriction and Pro-tier display fields. The proposed limits are three
searches, ten candidates each, 800-metre radius, 300-metre representative-anchor reuse,
ten-second phase deadline/four-second per-call cap, zero retries and zero to three final
references per trip. These implementation parameters remain pending approval.

<a id="b-b97ee221ab4b-2"></a>

The detailed plan in docs/v1_design.md covers the V1-only primary model DTO, independent
nearby identity/anchor ledger, application-owned provenance, separate budget/cache namespace,
deterministic distance/type/deduplication policy, unchanged-primary fallback and offline/live
test plan. PROJECT.md and docs/poi_selection.md identify this as the current product target
while preserving earlier implementation and smoke history. No executable file, prompt or
runtime setting was changed. No tests, live provider calls, model calls, deletion, stage,
commit, push, V2/V3 implementation or re-freeze occurred. No thesis archive was changed.

<a id="m-cbc1274c0bc6"></a>
## 2026-09-19 - Post-itinerary nearby references (implemented; offline only)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-cbc1274c0bc6-0"></a>

V1 now completes primary generation, validates original-supply activity identities and trip
dates, then runs discover_reference_recommendations before END. References are independently
discovered around scheduled, resolved anchors, not allocated from leftover primary supply.
The application appends zero to three untimed references without changing days, activities,
identities, costs or V1 cost diagnostics. Primary success and reference-phase outcome are
reported separately. Nearby errors/empty results preserve the successful primary itinerary.

<a id="b-cbc1274c0bc6-1"></a>

The versioned nearby_references_1 defaults are three actual attempts per trip, ten results
per request, 800-metre straight-line radius, 300-metre non-transitive representative reuse,
ten-second phase deadline, at most four seconds/request constrained by remaining time, zero
retries, DISTANCE ranking and mixed restaurant/cafe/park/museum types. This adds zero to
three external Nearby Search requests, NOT zero additional acquisition; it adds zero model
calls, Details, Reviews/Profile, Routes or Web calls. Cache hits do not spend attempts and
failed sends do. The first three representative areas are prioritized; later areas and
reused-circle edge coverage may be missed. Types are not balanced or quota-filled.

<a id="b-cbc1274c0bc6-2"></a>

V1 uses FoundryPrimaryItineraryDTO without model references; V0 retains FoundryItineraryDTO,
one generation call and model-knowledge references subordinate to the main itinerary, with
no tools or external identities. Final Itinerary remains itinerary_2. Primary, nearby and
scheduled-anchor ledgers stay separate. Names, addresses, source_ref and attribution are
taken from nearby evidence; anchor activity/day, representative, distance, call ID and
retrieval timestamp are retained in the normalized trace ledger. Address means returned
address, not an independently established neighborhood. No frontend changes were needed.
The old reference allocation instruction was also removed from planner_supply_projection.

<a id="b-cbc1274c0bc6-3"></a>

OutputRoleSummary retains legacy unused_candidate_ids (supply minus both output roles) and
now additionally exposes supply_not_scheduled_ids and references_outside_supply_ids. This
makes overlapping/new nearby IDs explicit without redefining historical fields. References
never satisfy REQUIRED, count as scheduled visits, or contribute to planned expenses.

<a id="b-cbc1274c0bc6-4"></a>

Offline validation accounting:
- Initial focused run: 109 passed, 1 failed (old topology assertion); assertion migrated.
- Related adapter/DTO/graph/V0/runtime checks before full suite: 167 passed.
- Exactly one full backend run: 829 passed, 9 skipped, 8 failed. Do not relabel it all green.
- Six failures used obsolete V1 reference-bearing mock responses; one expected the old trace
  file count. Fixtures/assertions were migrated to the new DTO/evidence artifact.
- One failure exposed an event-loop timer precision boundary: a phase-limited timeout could
  fire before a subsequent clock read reached the nominal deadline and schedule another
  request. A phase-limited timeout now ends scheduling unconditionally; cancellation is
  awaited and user cancellation still propagates.
- Affected harness/trace/discovery/supply/runner modules after corrections: 53 passed.
- Backend Ruff and git diff --check passed. No second full suite or live call was performed.

<a id="b-cbc1274c0bc6-5"></a>

Tests cover outside-supply references, actual anchors only, no leftover fallback, stable
reuse/round-robin selection, radius and exclusions, attribution, cache and failed attempts,
partial/all failure, deadline/cancellation, no-anchor output, attachment failure, primary
public-field/private-cost invariance, independent DTOs and unchanged other acquisition.
The prior checkpoint's 813 passed / 9 skipped / 1 failed full run and later runner correction
remain historical and are not retrospectively made green.

<a id="b-cbc1274c0bc6-6"></a>

Limitations: unknown hours/prices/accessibility and semantic preference satisfaction remain
unknown; references are not factual certification or a walking-route guarantee. Exact
name suppression may omit distinct branches. A provider without Nearby capability reports
provider_unavailable and preserves the main plan. This migration does not fix sparse main
itineraries or missing date coverage and adds no density validator or selector redesign.

<a id="b-cbc1274c0bc6-7"></a>

Follow-up requires separate authorization: at most one V0 and one V1 complete development
run with identical frozen valid input, the existing repaired harness, version-specific
prompt/DTO/config hashes, primary-before/after snapshots, nearby ledger/attempts and role
summaries. Accept empty/partial results without replacement runs; report actual coverage.
No live validation, frontend feature/engine switch, B2 cleanup, V2/V3, database/embedding
work, stage, commit, push or re-freeze occurred in this implementation checkpoint.

<a id="m-7ad4fe58cee6"></a>
## Post-itinerary nearby references live check - 2026-09-19 (bounded development evidence)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7ad4fe58cee6-0"></a>

One actual run_v0 and one actual run_v1 used the identical frozen complete P request:
Sydney, 2026-09-21 to 2026-09-23, three travelers, total budget AUD 1800, required Opera House,
distinctive/local preference and mother's softer less-walking preference. Both completed.
V0 generated six timed activities and two model-knowledge references, with no external
acquisition or external identities. V1 supplied eight candidates (one REQUIRED, seven
OPTIONAL), scheduled five distinct canonical places, and independently appended three
Nearby references. All three days contain primary activities in this particular sample.
The change from the earlier two-place sample is not attributed to reference discovery.

<a id="b-7ad4fe58cee6-1"></a>

The three 800-metre DISTANCE mixed-type searches used the actual scheduled Opera House,
Cafe Sydney Restaurant and Hyde Park anchors. Each returned ten raw candidates. Two closed
and two scheduled results were rejected; 26 were eligible, with three chosen and 23 left
unused by the final cap. Western Foyers (65.67 m), Barista 12 (4.60 m) and 3 Steps Takeaway
(133.72 m) are all outside primary supply and have actual Nearby provenance. Distances are
straight-line, not walking routes. No extra model or other acquisition followed the primary
itinerary. Ho Jiak and Harbour Bridge anchors were uncovered by the three-area cap; no
anchor reuse/cache-hit branch occurred. Returned attribution collections were empty.

<a id="b-7ad4fe58cee6-2"></a>

Primary-before/after business hashes match, cost diagnostics and REQUIRED/supply decisions
are unchanged, and separate main/reference/anchor identity checks pass. Nearby completed
in 1.157 s; primary run-start to date validation took 53.125 s; total V1 request 54.359 s.
V0 total was 23.234 s. These are two development samples, not a performance comparison.
V0 used two model calls / 8,347 tokens; V1 five / 30,927 tokens. All seven calls had one HTTP
send, no retry, and intact SDK usage. Reference-stage model calls: zero. Google sends:
4 Text Search (destination 1, named 1, default 2), Details 10, Reviews 3, Weather 1,
Routes 4 with 68 requested elements, and Nearby 3. Official Web/page, RAG and evaluator: zero.

<a id="b-7ad4fe58cee6-3"></a>

Raw captures and audit are ignored under logs/nearby_reference_acceptance_20260919_095712.
Production/config hashes are unchanged; capture errors are empty and session closed once.
No tests were rerun. Historical full suite remains 829 passed, 9 skipped, 8 failed, followed
by 53 passing affected tests; the earlier full run is not reclassified as all green.

<a id="b-7ad4fe58cee6-4"></a>

Uncovered live branches: empty/partial/failed/timeout Nearby, attachment fallback, no anchors,
cache/close-anchor reuse, same-supply rediscovery, nonempty attribution and user cancellation.
Existing offline tests support failure isolation; this run did not inject failures. Main
costs remain mostly unknown (one AUD 20-40 midpoint becomes AUD 30, not a trip total or
verified invoice). V0 references are general model suggestions with weak explicit anchor
explanation. Nearby identity/distance checks do not establish independent venue value,
accessibility, opening hours or soft-preference alignment; subvenues/co-located venues can
provide limited extra value. No provider/DTO/provenance/isolation wiring blocker was observed.
Recommendation: the post-itinerary reference feature can close this bounded development
checkpoint, preserving these quality/coverage limits. Not a freeze, benchmark or general
factual approval. Both scenarios are spent: no replacement run, additional feature or V2/V3.

<a id="m-5b6e5e07b446"></a>
## Frozen input and identities

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Post-itinerary nearby references live check - 2026-09-19 (bounded development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-5b6e5e07b446-0"></a>

```json
{
  "input_version": "planning_request_2",
  "destination": "Sydney, Australia",
  "start_date": "2026-09-21",
  "end_date": "2026-09-23",
  "traveler_count": 3,
  "budget": {
    "amount": "1800.00",
    "currency": "AUD"
  },
  "additional_preferences": "I definitely want to visit the Sydney Opera House. I prefer distinctive local places rather than tourist traps. My mother prefers less walking.",
  "request_id": null
}
```

<a id="b-5b6e5e07b446-1"></a>

Reference date: 2026-09-19. Request SHA-256: 000146c0c1bb27c79de4451542b72bc1788dc5552c76172cf8b49d0570f20b39.
Both dispatches use the explicit version runner recorded in manifest.json; product dispatch is unchanged.

<a id="b-5b6e5e07b446-2"></a>

| Identity | SHA-256 |
| --- | --- |
| V0 generation prompt | 82f5404a476bd6edaea3549332990e8c523eed33ebf2a3b37e9f8c693a57dfe2 |
| V1 generation prompt | 34945afea6ab7105374e05bd32ae0eca65bd61dcab9312b9244446de11197e32 |
| V0 generation schema | b992fa0b2e22adaaedd77c9b7778103b4aa3e3900382842ffa0fa12035f78af0 |
| V1 primary generation schema | 6958c240a4cd09e603d1a99763fb6cf708a39faa450c484e5fb4b34dd8e2be4e |
| Runtime config | 61452faedbe4675868df56804afd24f7f0df2ae48c5fb0a7cc25bf2d39c3ef63 |
| Requirement prompt | da2d7944a894d695b59b43dacf12772b5f1aea8d69ad9fa9bf1dc495ae1d3a6e |
| Requirement wire schema | 197bb06e7f192858eb4e8b4a75ee25c9d9ddabbd86d5b6517b6e9da46908e323 |
| Requirement model config | 3beebfea846aa58175e7a502993d0546403c32b14164939808c831d93317cbb8 |

<a id="b-5b6e5e07b446-3"></a>

Input planning_request_2; output itinerary_2; requirement prompt preference_prompt_5;
contract interpreted_requirements_3; reference policy nearby_references_1; actual model gpt-5.6-luna.

<a id="m-6d1933caf7dd"></a>
## V0 actual generated primary itinerary

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Post-itinerary nearby references live check - 2026-09-19 (bounded development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6d1933caf7dd-0"></a>

The following titles, places, times and notes are generated content, not an independent factual endorsement.
| Date | Time (+10:00) | Place / activity | Estimated cost |
| --- | --- | --- | --- |
| 2026-09-21 | 10:00-12:00 | Sydney Opera House | Unknown |
| 2026-09-21 | 14:00-15:30 | Royal Botanic Garden Sydney | Unknown |
| 2026-09-22 | 10:30-12:30 | Art Gallery of New South Wales | Unknown |
| 2026-09-22 | 14:30-16:00 | Sydney Fish Market | Unknown |
| 2026-09-23 | 10:30-12:00 | Harbour ferry sightseeing ride | Unknown |
| 2026-09-23 | 14:00-15:30 | Museum of Contemporary Art Australia | Unknown |

<a id="b-6d1933caf7dd-1"></a>

Actual activity notes:
- sydney-opera-house-visit: The required visit. Keep the pace gentle, prioritizing seated or short-distance viewing opportunities for the mother.
- royal-botanic-garden-gentle-outing: Choose a short, flexible section with places to pause rather than attempting to cover the gardens extensively.
- art-gallery-nsw-visit: Focus on a small selection of galleries and take regular seated breaks to reduce walking.
- sydney-fish-market-experience: A distinctive local food and harbour experience. Keep the visit focused and unhurried rather than walking through every section.
- harbour-ferry-sightseeing: A low-walking way to experience the harbour; choose seating and keep transfers to a minimum.
- museum-of-contemporary-art-visit: Select a compact gallery route with opportunities to sit; the visit can end early if the group is tired.

<a id="b-6d1933caf7dd-2"></a>

Actual untimed references:
- The Grounds of Alexandria (2026-09-22; address/area: Alexandria): A distinctive Sydney venue with a strong local character and a relaxed atmosphere, suitable as an optional short outing if the group wants another experience. Uncertainty: Model-knowledge suggestion; current opening arrangements, accessibility details, and prices were not checked.
- Spice Alley (2026-09-23; address/area: Chippendale): An atmospheric local food precinct that can offer a different side of Sydney from the main harbour sights; consider it only if a meal stop suits the group. Uncertainty: Model-knowledge suggestion; current opening arrangements, seating, and prices were not checked.

<a id="m-36ed70397c44"></a>
## V1 actual generated primary itinerary

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Post-itinerary nearby references live check - 2026-09-19 (bounded development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-36ed70397c44-0"></a>

The following titles, places, times and notes are generated content, not an independent factual endorsement.
| Date | Time (+10:00) | Place / activity | Estimated cost |
| --- | --- | --- | --- |
| 2026-09-21 | 10:30-12:00 | Sydney Opera House | Unknown |
| 2026-09-21 | 13:30-15:00 | Cafe Sydney Restaurant | Unknown |
| 2026-09-22 | 10:30-12:00 | Hyde Park | Unknown |
| 2026-09-22 | 13:30-15:00 | Ho Jiak Haymarket | 30.00 AUD |
| 2026-09-23 | 11:00-12:30 | Sydney Harbour Bridge | Unknown |

<a id="b-36ed70397c44-1"></a>

Actual activity notes:
- sydney-opera-house-20260921: Required visit. Date-specific opening hours and operational status are unknown in the supplied evidence, so verify availability before attending. Listed accessibility options include wheelchair-accessible parking, entrance, restrooms, and seating.
- cafe-sydney-20260921: The supplied current-hours baseline lists Monday availability from 12:00 to 22:30, but date-specific exceptions are unknown. Allow a relaxed transfer and rest period to limit walking.
- hyde-park-20260922: Current date-window evidence lists the park as open 24 hours on Tuesday. Keep the visit seated and unhurried; the evidence does not establish walking distances within the park.
- ho-jiak-haymarket-20260922: The supplied current-hours baseline lists Tuesday availability from 11:00 to 23:00, but date-specific exceptions are unknown. Supplied place evidence does not list wheelchair-accessible entrance, restrooms, seating, or parking; allow extra transfer time and avoid relying on a long walk.
- sydney-harbour-bridge-20260923: Date-specific opening hours and operational status are unknown in the supplied evidence. Keep this as a short sightseeing stop rather than a bridge walk to reduce exertion; the listed place evidence confirms a wheelchair-accessible entrance but does not verify a specific viewing route.

<a id="b-36ed70397c44-2"></a>

Actual untimed references:
- Western Foyers (2026-09-21; address/area: Shop 14/2 Circular Quay E, Sydney NSW 2000, Australia): Restaurant near Sydney Opera House (approximately 66 m straight-line). Uncertainty: Availability, prices and accessibility are unverified; straight-line distance is not a walking route.
- Barista 12 (2026-09-21; address/area: 31, Alfred St, Sydney NSW 2000, Australia): Restaurant near Cafe Sydney Restaurant (approximately 5 m straight-line). Uncertainty: Availability, prices and accessibility are unverified; straight-line distance is not a walking route.
- 3 Steps Takeaway (2026-09-22; address/area: 110 Elizabeth St, Sydney NSW 2000, Australia): Cafe near Hyde Park (approximately 134 m straight-line). Uncertainty: Availability, prices and accessibility are unverified; straight-line distance is not a walking route.

<a id="m-7bfd8002eba7"></a>
## V1 sources, anchors and role accounting

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Post-itinerary nearby references live check - 2026-09-19 (bounded development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7bfd8002eba7-0"></a>

Application associations below are separate from generated primary prose.
| Reference | Anchor / day | Type | Straight-line m | In supply | Source |
| --- | --- | --- | --- | --- | --- |
| Western Foyers | Sydney Opera House / 2026-09-21 | restaurant | 65.67 | False | google_places_nearby:nearby-4fef51b3-6d16-4f46-8229-3f124530c4ab:0 |
| Barista 12 | Cafe Sydney Restaurant / 2026-09-21 | restaurant | 4.60 | False | google_places_nearby:nearby-cb368694-1545-4f3a-9ae1-75515e930c50:2 |
| 3 Steps Takeaway | Hyde Park / 2026-09-22 | coffee_shop | 133.72 | False | google_places_nearby:nearby-b814ec49-687a-43a5-a41b-b0e49fe52449:1 |

<a id="b-7bfd8002eba7-1"></a>

Canonical supply ledger (REQUIRED is Opera House; all others OPTIONAL):
- Sydney Opera House: ChIJ3S-JXmauEmsRUcIaWtf4MzE
- Sydney Harbour Bridge: ChIJ49XqJV2uEmsRPsTAF7eOlGg
- Sydney Place: ChIJKc8tok6vEmsRsafPJow_QCs
- Hyde Park: ChIJDflB7BWuEmsRYPbx-Wh9AQ8
- Ho Jiak Haymarket: ChIJKWuQkCSuEmsRHNk3-wIWksY
- WILD LIFE Sydney Zoo: ChIJLat3W0euEmsRCQCK0yaDjTc
- Luna Park Sydney: ChIJ384_FGCuEmsRFAbHLAWVPGg
- Cafe Sydney Restaurant: ChIJOahrAxKuEmsRiJOniUNkOZY

<a id="b-7bfd8002eba7-2"></a>

Role sets (references are not scheduled visits):
```json
{
  "scheduled_place_ids": [
    "ChIJ3S-JXmauEmsRUcIaWtf4MzE",
    "ChIJ49XqJV2uEmsRPsTAF7eOlGg",
    "ChIJDflB7BWuEmsRYPbx-Wh9AQ8",
    "ChIJKWuQkCSuEmsRHNk3-wIWksY",
    "ChIJOahrAxKuEmsRiJOniUNkOZY"
  ],
  "reference_place_ids": [
    "ChIJHc6Q2mmuEmsRnvB9ysqcKrE",
    "ChIJWRhhJtevEmsROjx9Bto9tmg",
    "ChIJoVOojGauEmsRKrmCjyzBbbI"
  ],
  "unused_candidate_ids": [
    "ChIJ384_FGCuEmsRFAbHLAWVPGg",
    "ChIJKc8tok6vEmsRsafPJow_QCs",
    "ChIJLat3W0euEmsRCQCK0yaDjTc"
  ],
  "unscheduled_required_ids": [],
  "unlinked_activity_ids": [],
  "supply_not_scheduled_ids": [
    "ChIJ384_FGCuEmsRFAbHLAWVPGg",
    "ChIJKc8tok6vEmsRsafPJow_QCs",
    "ChIJLat3W0euEmsRCQCK0yaDjTc"
  ],
  "references_outside_supply_ids": [
    "ChIJHc6Q2mmuEmsRnvB9ysqcKrE",
    "ChIJWRhhJtevEmsROjx9Bto9tmg",
    "ChIJoVOojGauEmsRKrmCjyzBbbI"
  ]
}
```

<a id="b-7bfd8002eba7-3"></a>

Search representative/anchor coordinates and parameters:
- Sydney Opera House: ChIJ3S-JXmauEmsRUcIaWtf4MzE; center {'latitude': -33.856784399999995, 'longitude': 151.21529669999998}; call nearby-4fef51b3-6d16-4f46-8229-3f124530c4ab; raw 10, normalized 10, status success, timeout 4.0 seconds.
- Cafe Sydney Restaurant: ChIJOahrAxKuEmsRiJOniUNkOZY; center {'latitude': -33.8621894, 'longitude': 151.2109059}; call nearby-cb368694-1545-4f3a-9ae1-75515e930c50; raw 10, normalized 10, status success, timeout 4.0 seconds.
- Hyde Park: ChIJDflB7BWuEmsRYPbx-Wh9AQ8; center {'latitude': -33.8715202, 'longitude': 151.21162429999998}; call nearby-b814ec49-687a-43a5-a41b-b0e49fe52449; raw 10, normalized 10, status success, timeout 4.0 seconds.

<a id="b-7bfd8002eba7-4"></a>

All three used radius=800, maxResultCount=10, rankPreference=DISTANCE, language=en, mixed restaurant/cafe/park/museum, includeFutureOpeningBusinesses=false. Stage limit=10 s; per-request cap=4 s; retries=0; final cap=3; cache hits=0. Field mask: places.id,places.displayName,places.location,places.formattedAddress,places.primaryType,places.businessStatus,places.types,places.attributions.

<a id="b-7bfd8002eba7-5"></a>

Per-candidate decisions reconstructed from the captured raw response and retained ledger (not a rerun):
- Western Foyers (ChIJoVOojGauEmsRKrmCjyzBbbI), provider rank 0, selected_round_robin; retained-anchor distance 65.67259530526982 m.
- Midden by Mark Olive (ChIJda0Zi6-vEmsRxpgmepbRKdI), provider rank 1, eligible_not_selected_final_cap; retained-anchor distance 66.95783984559351 m.
- Bennelong (ChIJQcmNYGauEmsR84D5HAJJUhw), provider rank 2, eligible_not_selected_final_cap; retained-anchor distance 89.65659760031312 m.
- Winnie's Sydney (ChIJUTPuO-mvEmsRpdEn9qn2sUo), provider rank 3, eligible_not_selected_final_cap; retained-anchor distance 148.40893730679392 m.
- Bennelong Lawn (ChIJlxQGXmuuEmsR1jMD-M_7-Lc), provider rank 4, eligible_not_selected_final_cap; retained-anchor distance 201.6028508911499 m.
- Opera Bar (ChIJB5NuYGauEmsROhQEpJXe5qo), provider rank 5, eligible_not_selected_final_cap; retained-anchor distance 245.0916458336572 m.
- Australian Rockery Lawn (ChIJb-9-DGauEmsRd7cRx8uwisQ), provider rank 6, eligible_not_selected_final_cap; retained-anchor distance 298.9788655685105 m.
- Aria Restaurant Sydney (ChIJdxxU1WeuEmsR11c4fswX-Io), provider rank 7, eligible_not_selected_final_cap; retained-anchor distance 328.0850142672534 m.
- Whalebridge (ChIJB6Wq7KivEmsRlI_upCt0LoM), provider rank 8, eligible_not_selected_final_cap; retained-anchor distance 372.29346274105717 m.
- The East Chinese Restaurant (ChIJdxxU1WeuEmsRVDYDCJjmuT4), provider rank 9, eligible_not_selected_final_cap; retained-anchor distance 373.10883822100175 m.
- Harris Cafe (ChIJQUdF4mevEmsRuF7tR4qVPz0), provider rank 0, rejected_known_closed; retained-anchor distance None m.
- Cafe Sydney Restaurant (ChIJOahrAxKuEmsRiJOniUNkOZY), provider rank 1, rejected_scheduled_identity; retained-anchor distance None m.
- Barista 12 (ChIJHc6Q2mmuEmsRnvB9ysqcKrE), provider rank 2, selected_round_robin; retained-anchor distance 4.601904039705398 m.
- Quay Bar (ChIJEUXt0WmuEmsRfu7nTw81Si4), provider rank 3, rejected_known_closed; retained-anchor distance None m.
- Deux Frères (ChIJ4c9H4LCvEmsRh7jks6UZeH4), provider rank 4, eligible_not_selected_final_cap; retained-anchor distance 24.706133010326237 m.
- Salvador Coffee kiosk (ChIJjXCBCgCvEmsRT8TfLC_blf0), provider rank 5, eligible_not_selected_final_cap; retained-anchor distance 27.503357135814323 m.
- Lana (ChIJy5rTDTavEmsRMzWjIWyf0yw), provider rank 6, eligible_not_selected_final_cap; retained-anchor distance 36.604012056804514 m.
- Grana (ChIJvyZ8WvCvEmsRTqM2KE94_aw), provider rank 7, eligible_not_selected_final_cap; retained-anchor distance 36.604012056804514 m.
- Hinchcliff House (ChIJP8X3qK6vEmsRkasWfKpD9ok), provider rank 8, eligible_not_selected_final_cap; retained-anchor distance 36.604012056804514 m.
- Bouillon L'Entrecôte (ChIJAdgvpTSvEmsRG2zKBNpxNTo), provider rank 9, eligible_not_selected_final_cap; retained-anchor distance 44.89947592146167 m.
- Hyde Park (ChIJDflB7BWuEmsRYPbx-Wh9AQ8), provider rank 0, rejected_scheduled_identity; retained-anchor distance None m.
- 3 Steps Takeaway (ChIJWRhhJtevEmsROjx9Bto9tmg), provider rank 1, selected_round_robin; retained-anchor distance 133.7187953677695 m.
- Metro St James (ChIJIUO0ZhWuEmsRcL3eIiKOZMM), provider rank 2, eligible_not_selected_final_cap; retained-anchor distance 142.23520751234585 m.
- Rebels N Misfits - St James (ChIJu32xhoivEmsR1HAEdce6uG0), provider rank 3, eligible_not_selected_final_cap; retained-anchor distance 165.00632219804234 m.
- Coffee Shop Sheraton (ChIJV6DPKD6uEmsR-8Yc8tO35AQ), provider rank 4, eligible_not_selected_final_cap; retained-anchor distance 165.65582824166165 m.
- The Gallery (ChIJb4j7LD6uEmsRRjZXfC_Ljgg), provider rank 5, eligible_not_selected_final_cap; retained-anchor distance 172.88098475856498 m.
- Sydney Common (ChIJc0mMtOavEmsRDppT8X7Muus), provider rank 6, eligible_not_selected_final_cap; retained-anchor distance 176.76239324238392 m.
- Sandringham Memorial Garden and Fountain (ChIJS3blvhWuEmsRIPvy-Wh9AQ8), provider rank 7, eligible_not_selected_final_cap; retained-anchor distance 182.56077205900894 m.
- Tattersalls Club (ChIJA6bWJT6uEmsRfptvqOsr_1k), provider rank 8, eligible_not_selected_final_cap; retained-anchor distance 184.87295532996444 m.
- Peter's Brasserie (ChIJjxKl_9GvEmsRomgZnXySrXw), provider rank 9, eligible_not_selected_final_cap; retained-anchor distance 194.01875716116027 m.

<a id="m-74866807dfd5"></a>
## Usage and capture

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Post-itinerary nearby references live check - 2026-09-19 (bounded development evidence). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-74866807dfd5-0"></a>

| Case / task | Input | Output | Reasoning (included) | Cached input (included) | Cache write (included) | Captured seconds |
| --- | --- | --- | --- | --- | --- | --- |
| V0_P / InterpretationDraft | 3946 | 742 | 407 | 0 | 3943 | 8.266 |
| V0_P / Itinerary | 1995 | 1664 | 623 | 0 | 1992 | 14.922 |
| V1_P / InterpretationDraft | 3946 | 784 | 440 | 3943 | 0 | 7.422 |
| V1_P / ExperienceProfileDraft | 1303 | 284 | 147 | 0 | 1300 | 4.203 |
| V1_P / ExperienceProfileDraft | 1019 | 327 | 147 | 0 | 0 | 3.609 |
| V1_P / ExperienceProfileDraft | 986 | 451 | 313 | 0 | 0 | 5.250 |
| V1_P / V1Itinerary | 19809 | 2018 | 1032 | 0 | 19806 | 19.766 |

<a id="b-74866807dfd5-1"></a>

Usage is counted once from SDK responses; reasoning/cache are subsets, not extra totals. Actual invoice cost is unknown. Main-stage time uses run_started to successful date validation; case times include dispatch/finalization overhead. All 25 external HTTP sends returned 200; Routes requested 64+2+1+1 elements. Nearby HTTP durations were 0.391, 0.375 and 0.344 s; full reference phase was 1.157 s.

<a id="b-74866807dfd5-2"></a>

Primary business SHA-256 before and after: f2dc5e6a3b8a116d08d3abfb44ecf1840e25d6a440f8b032c56395e711fbe1b0. Before snapshot/hash was persisted on the existing successful date-validation trace event, before Nearby. All audit identity/invariance checks passed. Existing AcceptanceSession/run_matrix handled ownership and dispatch; scoped diagnostic observers recorded snapshots and timestamps without modifying outputs or production files. No new harness file was created.

<a id="b-74866807dfd5-3"></a>

No tests, provider reruns, production edits, frontend changes, B2 deletion, database/embedding work, staging, commit/push or re-freeze in this live task. Keep the preceding same-pool history and offline failures intact. Stop after these two cases.

<a id="m-c0085008c5f1"></a>
## New supply migration live limitation (2026-09-19)

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-c0085008c5f1-0"></a>

The approved B/A runs each made one Requirement LLM call, then failed before discovery:
B invalid_subject_ids (reserved party redeclared); A temporary DiscoveryIntent ID longer
than40 characters. New supply is offline validated but not end-to-end live validated.
No B2 evaluator/enumerator or Google call occurred. No retry or supply tuning followed.
Retain B2 code until separate acceptance/cleanup; keep V1 reopened. Detailed actual
metrics and unmeasured downstream outcomes are in the current selection/evolution records.

<a id="m-f0f6792282c6"></a>
## Post-itinerary references - 2026-09-19 (implemented; offline only)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f0f6792282c6-0"></a>

Primary deterministic supply and REQUIRED/OPTIONAL decisions are unchanged. The planner
supply projection no longer offers untimed references as an output allocation. V1 generation
produces the primary itinerary only; after identity/date checks, the application searches
near actual scheduled canonical anchors and appends 0-3 optional references. Unused supply
is never a fallback; independently rediscovered supply members can qualify.

<a id="b-f0f6792282c6-1"></a>

The separate nearby_references_1 budget allows 0-3 Nearby requests, ten results each, radius
800 m, representative reuse 300 m, phase deadline 10 s, individual timeout at most 4 s,
DISTANCE ranking and zero retries. No extra models, Details, Reviews/Profile, Routes or Web.
Unknown preference satisfaction stays unknown. Failure returns the successful main itinerary.
References do not satisfy REQUIRED, increase scheduled counts or alter costs. Summary fields
now distinguish supply_not_scheduled_ids from references_outside_supply_ids in addition to
historical unused_candidate_ids. No public Itinerary or frontend shape change is needed.

<a id="b-f0f6792282c6-2"></a>

See docs/v1_design.md for implemented ledgers, limits and offline checks. Full backend ran
once: 829 passed, 9 skipped, 8 failed; affected modules passed 53 tests after corrections.
No live validation. Earlier sections retain old same-pool implementation/live history and
must not override this mechanism. Sparse main itineraries remain a separate quality issue.

<a id="m-d9a3eb002644"></a>
## Historical proposal: post-itinerary reference discovery - 2026-09-19

_Source context: Current V1 Architecture. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-d9a3eb002644-0"></a>

The following section records the preceding design-only checkpoint. The implemented status
and validation results above supersede its pending-approval/runtime statements.

<a id="m-dde78dfc9f4d"></a>
## Scope and observed implementation

_Source context: Current V1 Architecture / Historical proposal: post-itinerary reference discovery - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-dde78dfc9f4d-0"></a>

The user-approved product correction supersedes the earlier requirement that V1 references
come from unused primary supply in the same model response without additional acquisition.
It does not authorize executable changes. Earlier entries below preserve implementation and
live history; the runtime still uses the old mechanism. Sparse main output (two canonical
visits and an empty third day in the latest sample) remains a separate quality limitation.

<a id="b-dde78dfc9f4d-1"></a>

Currently both Foundry bindings use FoundryItineraryDTO, including references. V1 generation
calls validate_output_sources against place_evidence restricted to selected supply IDs;
reference names, addresses and source_ref are projected from that same ledger. The graph ends
after validate_itinerary_dates. GooglePlacesProvider only implements Text Search and Details/
Reviews; its Text Search locationBias circle is not a hard nearby restriction.

<a id="m-080b8f196332"></a>
## Proposed graph boundary and ownership

_Source context: Current V1 Architecture / Historical proposal: post-itinerary reference discovery - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-080b8f196332-0"></a>

Keep the entire primary acquisition, deterministic supply, requirements, generation and date
policy unchanged. Change only V1 generation's reference responsibility. Proposed tail:

<a id="b-080b8f196332-1"></a>

```text
generate_evidence_informed_itinerary (primary output only; primary identity validation)
-> validate_itinerary_dates
-> discover_reference_recommendations (application-owned, bounded, optional)
-> END
```

<a id="b-080b8f196332-2"></a>

Insert the node where backend/app/versions/v1/graph.py currently connects
validate_itinerary_dates to END. runner.py injects a reference service with the request-local
cache and separate reference limits; state.py retains its evidence ledger/status. Final
output-role tracing moves after attachment. Primary failure does not trigger discovery.
No reference result changes supply, day activities, order, times, costs or REQUIRED decisions.
Preserve V1 private cost diagnostics when copying the final itinerary.

<a id="m-f261dda92b99"></a>
## Deterministic discovery proposal (parameters require approval)

_Source context: Current V1 Architecture / Historical proposal: post-itinerary reference discovery - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f261dda92b99-0"></a>

1. Read scheduled activities in date/start-time/activity-ID order. Resolve non-null canonical
   IDs strictly against the actual primary supply evidence. Skip unlinked or unlocatable
   activities without blocking output. Deduplicate anchor IDs, retaining earliest occurrence.
2. The first anchor is a search representative. Reuse a representative's result pool for
   later anchors within 300 metres of that representative; no transitive clustering. Create
   separate representatives for other areas, at most three in chronological order. Record
   uncovered anchors; do not expand limits. This intentionally favors earlier anchors when
   more than three distinct areas exist, without promising coverage of every day.
3. Each representative gets one mixed-type Nearby Search, radius 800 metres, maxResultCount
   10, rankPreference DISTANCE, includedTypes restaurant/cafe/park/museum. Do not issue one
   search per type, paginate, expand radius or fall back to Text Search. Up to 30 raw results.
4. Validate actual ID, name, finite coordinates and allowed returned types. Recalculate
   straight-line distance to an eligible actual anchor in that representative's group and
   require <=800 metres. Associate the closest such anchor (chronological tie-break), never
   an unused supply candidate or another reference. Reuse is bounded and can miss places
   near the edge of a later anchor's circle; completeness is not promised.
5. Reject scheduled IDs, resolved excluded IDs, duplicates and known typed incompatibility
   (for example permanently or temporarily closed business status). Check available evidence
   for explicit contradictions without acquiring enrichment. Unknown hours, accessibility,
   price, crowding or soft alignment are not a blocking failure or verified satisfaction.
   Only registered typed exclusion mappings can be applied; do not parse raw preferences or
   guess unresolved excluded identities by name. Existing semantic limits remain visible.
6. Sort eligible results in each representative pool by distance then canonical ID; select
   round-robin across chronological representative pools, globally deduplicated, maximum
   three. No minimum count, category quotas, rating scorer or model judgment. Repeated exact
   normalized names are conservatively omitted to respect the existing output duplicate
   rule; this is not identity resolution and may suppress distinct branches. Conflicting
   records for one ID use earliest successful response. All references require new nearby
   evidence even if their IDs happen to appear in original supply.
7. Template the reason from returned type and anchor name. Optional measured distance must
   be labeled straight-line, never walking time/accessibility. associated_day comes from
   the actual anchor date; it does not schedule the recommendation. Availability and costs
   remain unverified. Do not infer quietness, local appeal or suitability from categories.

<a id="m-7b8f397ae0c9"></a>
## Adapter, fields, cache and cost

_Source context: Current V1 Architecture / Historical proposal: post-itinerary reference discovery - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-7b8f397ae0c9-0"></a>

Add search_nearby to GooglePlacesProvider via a small NearbyPlacesProvider protocol and
PlaceNearbySearchRequest. Reuse the normalized candidate response, extending optional types
and provider attribution fields as necessary. Do not reuse the expensive Details mask.
Use POST places:searchNearby with locationRestriction.circle, not locationBias.
Proposed mask: places.id, places.displayName, places.location, places.formattedAddress,
places.primaryType, places.types, places.businessStatus, places.attributions.
Keep includeFutureOpeningBusinesses false. Preserve provider attribution in the evidence
record; source_ref is an application-owned provenance reference, not model text.

<a id="b-7b8f397ae0c9-1"></a>

These fields use Nearby Search Pro; rating/opening-hours fields would invoke a higher tier.
Official references checked 2026-09-19:
- https://developers.google.com/maps/documentation/places/web-service/nearby-search
- https://developers.google.com/maps/documentation/places/web-service/place-types
- https://developers.google.com/maps/billing-and-pricing/pricing

<a id="b-7b8f397ae0c9-2"></a>

Proposed separate reference_discovery limits: three actual requests, ten results/request,
800-metre radius, 300-metre anchor reuse, ten-second total phase deadline, four-second maximum
per request capped by remaining phase time, zero retries. Sequential execution simplifies
accounting. Reserve an attempt before dispatch; record success/failure/timeout/cache hits.
Never borrow primary search, Details, model or routing budgets. No new model calls, per-place
Details, Reviews/Profile, Routes, Official Web or RAG. Existing transport has no retries;
bound its await locally without changing primary transport configuration.

<a id="b-7b8f397ae0c9-3"></a>

Use the existing RequestCache with a distinct operation key including exact representative
coordinates, radius, sorted types, field mask, language, rank and maximum results. Spatial
reuse is decided explicitly before cache access. Cache hits do not consume request counts.
RequestCache does not cache exceptions: retain an attempted-key set in the phase so failures
are not retried. No persistent cache or database change.

<a id="b-7b8f397ae0c9-4"></a>

Published first paid volume tier is USD 32/1,000 Nearby Search Pro requests with a monthly
5,000-request free usage cap. Three requests correspond to USD 0.096 at that paid rate before
credits, discounts, tax or currency conversion; actual billing depends on the account.
Returned candidate count is not a per-place Details charge. This is a documentation-based
estimate, not measured spend; no provider request was made for this design.

<a id="m-19300e86e44a"></a>
## DTO, final output and identity ledgers

_Source context: Current V1 Architecture / Historical proposal: post-itinerary reference discovery - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-19300e86e44a-0"></a>

Keep final Itinerary itinerary_2 and ReferenceRecommendation fields unchanged. Add a V1-only
strict Foundry primary-output DTO without reference_recommendations; reuse day/activity DTOs.
Bind V1Itinerary to it and map references to an application-owned empty list before discovery.
Adjust V1 cost projection for that DTO without changing cost policy. V0 retains its existing
two-role DTO and one generation call. Change V1 prompt to primary-only; V0 prompt states that
model-knowledge references are subordinate to actual primary activities, with no fabricated
IDs, source_ref, measured distances or travel times. Do not retain a V1 model-reference fallback.

<a id="b-19300e86e44a-1"></a>

Separate primary activity validation (original supply ledger) from reference validation
(successful nearby evidence ledger). An internal entry records canonical ID, name, address,
coordinates, types, provider timestamp/attribution, application source_ref, search call ID,
anchor_place_id, anchor activity/day and calculated distance. No public anchor field is needed
initially: trace/ledger provides association and associated_day already exists in the API.
Project reference names/source_ref/area from nearby evidence; preserve existing length bounds
and omit unavailable/oversized optional address rather than fabricate an area. Every anchor
must resolve to an actual scheduled primary activity. New reference IDs need not be in supply.

<a id="b-19300e86e44a-2"></a>

Keep output_role_summary fields: scheduled IDs come only from primary activities; reference
IDs from the appended list; unscheduled REQUIRED is required minus scheduled, never minus
references; unused_candidate_ids retains supply minus scheduled minus references (nearby-only
IDs have no effect on this set). Also trace supply_not_scheduled_ids = supply minus scheduled
to distinguish unscheduled supply from use in either output role, plus references outside
supply. Do not silently redefine historical summary fields or count references as visits.

<a id="m-dac918db4ae4"></a>
## Failure isolation and invariance

_Source context: Current V1 Architecture / Historical proposal: post-itinerary reference discovery - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-dac918db4ae4-0"></a>

Keep the validated primary itinerary as the immutable fallback. Missing anchors, no results,
budget exhaustion, provider failure or local timeout returns empty/partial references and
an explicit phase outcome/reasons. Reject invalid discovery entries individually before
assembly; a reference attachment validation error falls back to the primary itinerary and
records the error, never claims a successful reference phase. No primary regeneration or
silent conversion of REQUIRED references into visits. External cancellation must propagate;
do not suppress it as a nearby-provider error. Preserve primary public fields and private
cost diagnostics; verify primary serialization before/after in tests. Unexpected reference
errors must be observable even when the successful primary output is returned.

<a id="b-dac918db4ae4-1"></a>

Suggested trace outcomes: completed, partial, empty, no_anchors, deadline_exceeded,
budget_exhausted, provider_error, attachment_error, with per-request outcomes and rejection
counts. No new public output schema or UI change is needed for phase status at this stage.

<a id="m-8c8597c13a60"></a>
## Planned file impact and verification

_Source context: Current V1 Architecture / Historical proposal: post-itinerary reference discovery - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-8c8597c13a60-0"></a>

Implementation candidates (not changed at this checkpoint):
- integrations/models.py, integrations/protocols.py, integrations/google/places.py: Nearby contract/adapter.
- services/reference_discovery.py (new): bounded phase, internal ledger and deterministic selection.
- runtime/config_models.py and config/runtime.yaml: separate reference-only limits.
- versions/v1/runner.py, graph.py, state.py: injection, post-date-validation stage and trace.
- policies/itinerary_output.py: distinct ledgers and final role accounting.
- llm/azure_foundry/dto.py, client.py, mapping.py, itinerary_cost_projection.py: V1 primary DTO/binding.
- versions/v0/prompts.py and versions/v1/prompts.py: distinct generation responsibilities.
- Related adapter, schema/mapping, output-policy, service and V0/V1 graph/runner tests.
All backend paths above are relative to backend/app. Final API schemas/frontend need no
planned field changes. Reuse neutral distance arithmetic without restoring B2 selection.

<a id="b-8c8597c13a60-1"></a>

Offline fake-provider tests must cover: unused supply alone cannot create references;
scheduled-only anchors; null/unresolved anchors skipped; close-anchor reuse without transitive
clustering; separated areas/cap; strict radius boundary and invalid coordinates; results
outside original supply; independently rediscovered original candidates; excluded/closed/
duplicate rejection; unknown evidence retained without factual claims; date association;
empty/partial/failure/timeout/attachment failure preserving primary days, IDs, costs and
private diagnostics; exact cache keys and zero retries; limits across errors/cache hits;
distinct DTO bindings, no V1 model references; no added model/Details/Reviews/Routes/Web calls;
V0 zero external calls and null external identities. Assert final role-summary semantics.

<a id="b-8c8597c13a60-2"></a>

After implementation and offline checks, seek separate authorization for at most one V0
and one V1 complete run using the same frozen valid request and existing repaired harness.
Capture primary-before/after, actual anchors, nearby call masks/counts/results, reference
ledger, usage, deadlines and failures. Empty results are accepted coverage limitations, not
a reason for reruns. V0 gets zero external requests; V1 at most three new nearby requests
and no additional model call. Neither this plan nor this checkpoint authorizes those runs.
No benchmark, main itinerary redesign, V2/V3 implementation, commit or re-freeze is included.

<a id="m-103073a8c729"></a>
## Pre-migration implementation checkpoints (historical input behavior)

_Source context: Current V1 Architecture. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-103073a8c729-0"></a>

Updated 2026-09-19: deterministic planning candidate supply is the active reopened V1
implementation, offline validated; **V1 is not re-frozen**. Historical B2 code/tests
remain pending separate cleanup. V0 is unchanged. TripWorld Phases 1-5 are preserved;
V2 RAG integration and V3 are not implemented. Historical freezes stay in V1 milestones.

<a id="m-bc8713b9865d"></a>
## Active flow and responsibility

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-bc8713b9865d-0"></a>

Requirement LLM -> open normalized requirements/provenance/subjects -> unsupported HARD
clarification -> dates/destination/discovery/named identities -> canonical factual gate
-> bounded Details -> selective Reviews/Profile -> direct deterministic planning supply
-> explicit REQUIRED/OPTIONAL ledger -> Weather/Routes/Official Web -> itinerary/date checks.

<a id="b-bc8713b9865d-1"></a>

The exact current policy is in `docs/poi_selection.md`; history is in
`docs/poi_selection_evolution.md`. B2's historical measurements remain in
`docs/b2_implementation.md`. No active direct Stage A/B selector, Semantic Evaluator,
minimum-subset enumerator, QCGRE weighted total, or hidden fallback exists.

<a id="b-bc8713b9865d-2"></a>

The application owns identity, eligibility, tool budgets, supply capacity and membership.
One Requirement LLM interprets arbitrary semantics; Review LLM interprets supplied reviews;
Itinerary LLM chooses a coherent optional subset with user must-visits and soft trade-offs.
Unknown or neutral does not make a candidate useless. Soft conflicts affect priority,
not eligibility. Supply fills normal capacity when credible candidates exist, retaining
feasible required overflow within unchanged hard budgets. No new visits-per-day minimum.

<a id="b-bc8713b9865d-3"></a>

The current V1 result contract is planning_supply_1, exposing planning_supply separately
from itinerary. It reports required/optional IDs, shortfall, deterministic diagnostics
and zero evaluator/enumerator calls. Short supply is explicitly degraded_selection.
Missing required facts/identity and unsupported HARD semantics still clarify.

<a id="b-bc8713b9865d-4"></a>

ExperienceEvidenceRequest adds optional preferred/avoided typed values for existing
review dimensions; missing direction stays UNKNOWN. The Requirement draft uses explicit
party/specified/unresolved targets and opaque temporary handles. The application allocates
canonical IDs, rewrites links and validates source-grounded membership; no silent party
autofill or identifier-spelling interpretation occurs. V0 extraction,
model settings, generation contract and result schema remain unchanged.

<a id="b-bc8713b9865d-5"></a>

Supply checkpoint: focused 193 passed; full backend once 673 passed, 9 skipped. The later
systematic Requirement-boundary checkpoint: affected 262 passed; full backend once
711 passed, 9 skipped; Ruff and diff checks passed. Live development results and limitations are recorded in the current
POI selection document. A larger supply alone does not establish good itinerary quality.
No post-generation repair, V1 re-freeze, V2/V3, commit or push is authorized by completion.

<a id="b-bc8713b9865d-6"></a>

The two authorized development live runs each stopped at Requirement validation:
B redeclared reserved party in subjects; A generated a temporary discovery ID longer
than40 characters. No Google/evaluator/selection/itinerary call followed. The new supply
path is not yet end-to-end live validated. A systematic boundary pass has since been
implemented/offline validated; it supersedes the narrow-patch recommendation. Current
contract is interpreted_requirements_2, with application-owned subject/semantic/named/
discovery IDs, strict draft/reference validation, classified failures, and default-off
private response capture before DTO mapping. Provider schema owns structure; resource
bounds, source integrity and link validity remain application checks. Full ownership,
migration examples, bounds and limitations are recorded in docs/poi_selection.md.
Nine Requirement-only acceptance cases/checks are frozen but not executed. This pass
made no live/paid calls and leaves supply/budgets/cache/HARD policy unchanged. Further
live validation and B2 cleanup require separate approval. Earlier live authorization
is exhausted; the historical failed results are not retrospectively marked successful.

<a id="b-bc8713b9865d-7"></a>

Subsequent limited live attempt (2026-09-19): the frozen matrix was authorized, but its
first case stopped at transport with OpenAIConnectionError (one client/HTTP attempt,
0.453 seconds). No completed response or usage was available; eight cases were unexecuted.
No DTO/canonical/semantic acceptance result can be claimed. All downstream calls stayed
zero and no production logic was changed. Transport access needs separate investigation
before further live acceptance. The complete manifest/results are in docs/poi_selection.md;
the prior paragraph describes the offline checkpoint, not an executed nine-case success.

<a id="b-bc8713b9865d-8"></a>

Later network-authorized continuation: 8 completed Requirement responses accepted the
wire schema and passed DTO/canonical/source checks. One additional client invocation
failed before HTTP because of harness shared-client cleanup; that case was not repeated.
The remaining seven ran with a harness-only lifecycle correction. Production stayed fixed.
Destination-as-REQUIRED-visit, ordinary negative preference interpreted as HARD, and
ambiguous pronoun attribution remain semantic issues despite valid contracts. Complete
four-layer results, separate execution segments, usage and private artifact hashes are
recorded in docs/poi_selection.md. No end-to-end acceptance or further implementation is
authorized by these observations; the next recommendation is a semantic/product decision.

<a id="b-bc8713b9865d-9"></a>

Current semantics checkpoint: policy version 1 and Requirement prompt version 3 distinguish
trip scope/actual visit, tradeable polarity/non-negotiable strength, and mentioned people/
confirmed travelers/preference owners/party total using the existing contract. Source
validation still checks integrity, not entailment; HARD policy and candidate supply are
unchanged. Offline affected 275 passed; full backend once 724 passed, 9 skipped.
The authorized fixed ten-case matrix completed ten Requirement calls, without retries or
downstream calls. Eight canonical outputs validated; two extraction-issue cases stopped
before release. Destination/area, soft/HARD and clear/ambiguous attribution contrasts were
preserved. A remaining material mismatch is optional unknown count being promoted to a
blocking extraction issue. It was not fixed or re-run. The original Spanish expectation
is separately qualified as ambiguous, not retrospectively counted as success. Resolve
optional uncertainty versus blocking clarification narrowly before end-to-end acceptance.

<a id="m-ad8de01f4f51"></a>
## Shared Project-Wide Date Contract

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-675836fce13e"></a>
## Invariant

_Source context: Current V1 Architecture / Shared Project-Wide Date Contract. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-675836fce13e-0"></a>

Every V0/V1/future V2/V3 run shares this deterministic invariant:

<a id="b-675836fce13e-1"></a>

```text
reference_date <= start_date <= end_date <= reference_date + 9 days

Final itinerary dates
subset of Requested trip dates
subset of [reference_date, reference_date + 9 days]
```

<a id="b-675836fce13e-2"></a>

The allowed window contains ten inclusive calendar dates. `max_trip_days = 10` is not
an equivalent rule: a short trip outside the allowed window is still invalid.

<a id="m-2c2aaeda8bf6"></a>
## Stage 0 Implementation

_Source context: Current V1 Architecture / Shared Project-Wide Date Contract. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2c2aaeda8bf6-0"></a>

The shared implementation is owned by `backend/app/policies/trip_dates.py`. It:

<a id="b-2c2aaeda8bf6-1"></a>

- Computes an immutable `TripDateWindow`
- Validates requested start and end dates
- Validates final itinerary dates against the requested range
- Validates itinerary top-level dates, itinerary-day dates, and activity start/end
  calendar dates
- Raises stable deterministic policy errors

<a id="b-2c2aaeda8bf6-2"></a>

Invalid dates fail without retry, regeneration, repair, or date mutation. This is a
shared input/output contract, not V3-style itinerary feasibility validation.

<a id="m-5dbabb1254f5"></a>
## Fixed Run Reference Date

_Source context: Current V1 Architecture / Shared Project-Wide Date Contract. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-5dbabb1254f5-0"></a>

The trusted date is read once when a run starts and is reused by requirement parsing,
date validation, future provider requests, and final-output validation. No graph node or
provider may independently re-read the current date.

<a id="b-5dbabb1254f5-1"></a>

Current Product behavior uses the backend's configured IANA-zone date through
`SystemDateProvider`. Product requests cannot contain `reference_date`. Developer API,
CLI, and programmatic tests may supply a fixed reference date as trusted
research/testing functionality.

<a id="m-97def8055fd5"></a>
## Explicit Production Time Zone

_Source context: Current V1 Architecture / Shared Project-Wide Date Contract. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-97def8055fd5-0"></a>

V1-A first moved from implicit host-local time to an explicit IANA time zone
configured through `APP_TIME_ZONE`. The later project-wide configuration refactor
moved this non-secret policy into `config/runtime.yaml`; the current shared setting is:

<a id="b-97def8055fd5-1"></a>

```text
app.time_zone: Australia/Sydney
```

<a id="b-97def8055fd5-2"></a>

Conceptually:

<a id="b-97def8055fd5-3"></a>

```python
datetime.now(ZoneInfo(config.app.time_zone)).date()
```

<a id="b-97def8055fd5-4"></a>

The runtime includes `tzdata` for platforms that do not bundle IANA zone data. The
implementation preserves one fixed date per run, deterministic injected clocks, no
Product `reference_date` bypass, and trusted Developer/CLI overrides.

<a id="m-eb5675eef153"></a>
## Product Frontend

_Source context: Current V1 Architecture / Shared Project-Wide Date Contract. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-eb5675eef153-0"></a>

The Product date picker is a UX boundary with browser-local calendar semantics:

<a id="b-eb5675eef153-1"></a>

```text
start min = browser-local today
start max = browser-local today + 9 days
end min   = selected start, or today before selection
end max   = browser-local today + 9 days
```

<a id="b-eb5675eef153-2"></a>

The form validates the same range before submission. It does not use UTC
`toISOString()` slicing. Backend validation remains authoritative for direct API calls.

<a id="m-e1bc78c1062d"></a>
## Weather Design

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e1bc78c1062d-2"></a>

```text
requested_start <= weather_date <= requested_end
```

<a id="b-e1bc78c1062d-3"></a>

No pre-trip or post-trip provider record may reach the planner.

<a id="b-e1bc78c1062d-4"></a>

The minimal evidence is:

<a id="b-e1bc78c1062d-6"></a>

Provider failure becomes explicit unavailable evidence. The LLM must never generate or
fill weather values.

Verbatim passages shared with another maintained section: [1](v1_development.md), [2](v1_development.md), [3](v1_development.md). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-58f6e0026185"></a>
## Implemented Routes Design

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-58f6e0026185-1"></a>

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

Verbatim passages shared with another maintained section: [1](v1_development.md). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-bd65aa33b648"></a>
## Web Evidence Architecture

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-bd65aa33b648-0"></a>

The integrated V1-B path is:

Verbatim passages shared with another maintained section: [1](v1_development.md), [2](v1_development.md), [3](v1_development.md), [4](v1_development.md), [5](v1_development.md). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-b250cbdb0be2"></a>
## Evidence Precedence and Conflicts

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-b250cbdb0be2-0"></a>

For factual/current information:

Verbatim passages shared with another maintained section: [1](v1_development.md), [2](v1_development.md). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-ca600ee0c684"></a>
## Runtime, validation and stop

_Source context: Current V1 Architecture. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ca600ee0c684-0"></a>

Runtime schema6 has one semantic_evaluator section: development input32k, output16384, low reasoning,
timeout90s, transport retries0. Shared provider/cache/budget policies are unchanged.
The full backend suite uses fake providers/models and blocks external sockets. Exact B2
counts, sizing, performance and limitations are in the checkpoint. B1 live results are
historical development evidence, not evidence for B2. No benchmark conclusions are made.

<a id="b-ca600ee0c684-1"></a>

Scripts run_v0.py and run_v1.py remain independent. Future V2 adds canonicalized TripWorld
discovery before shared selection. V3 alone adds general post-generation feasibility
validation/repair. Do not start either, run B2 live validation, commit/push or re-freeze
without explicit approval.

<a id="m-e82d24472987"></a>
## Implemented Flow and Selection Contract

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Revised V1-A Implementation and Re-Freeze (2026-09-14). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-e82d24472987-0"></a>

At the 2026-09-14 revised V1-A checkpoint, the independent V1 graph executed:

<a id="b-e82d24472987-1"></a>

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

<a id="b-e82d24472987-2"></a>

The LLM extracts requirements and interprets retrieved review text into a bounded
Profile, but does not choose the final POI set. Reviews and Profile influence
selection only; neither is passed to the itinerary prompt. The selected Place
IDs are projected in final order into aligned `PlaceCandidate[]` and
`PlaceEvidence[]` for V1-B Phase 3. This Web stage was added after the revised
V1-A re-freeze; the V1-A live checks in this section predate that integration.

<a id="b-e82d24472987-3"></a>

The inclusive trip duration `D` determines algorithmic maxima:

<a id="b-e82d24472987-4"></a>

```text
K_final         = min(16, 2D + 2)
R_pool          = max(10, K_final + 2)
C_raw           = max(20, 2R_pool)
review_pool_cap = min(6, ceil(K_final / 3))
```

<a id="b-e82d24472987-5"></a>

Runtime budgets can explicitly lower effective capacities. The final selector
protects eligible reconciled required Place IDs and greedily scores the rest by
`Q_rel + C_cov + G_geo + R_rating + E_exp`: weighted real search-hit relevance,
uncovered intent coverage, geographic grouping, bounded quantitative rating,
and bounded review-derived experience fit. Stable provider-rank/Place-ID
tie-breakers make the selected set deterministic. Missing rating is neutral;
review/Profile failure gives `E_exp = 0` and leaves structured
`PlaceEvidence.availability` unchanged. Selection conflicts remain explicit.

<a id="b-e82d24472987-6"></a>

Typed `NamedPlaceIntent` marks a specific named place `REQUIRED` when the user
clearly expects it in the final trip, including *must visit*, *want to visit*,
*would like to visit*, and *hope to visit*. Conditional/optional names are
`OPTIONAL`; generic categories are not named must-visits. Exact Places identity
reconciliation protects resolved required Place IDs through the funnel. An
unresolved required name is reported, not replaced by a guessed POI. Aliases
such as `MCA` that do not exactly match the provider display name are not
fuzzily resolved.

<a id="m-4a028a603d29"></a>
## Bounded Places, Reviews, and Opening Hours

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Revised V1-A Implementation and Re-Freeze (2026-09-14). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-4a028a603d29-0"></a>

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

<a id="b-4a028a603d29-1"></a>

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

<a id="b-4a028a603d29-2"></a>

Current and regular opening hours remain separate. For each requested date,
planning uses applicable current/date-sensitive hours within their supported
window; otherwise it uses regular weekly hours as a baseline; otherwise hours
are `unknown`. Regular hours are not a guarantee against a holiday or
special-date exception. Targeted V1-B official evidence may address a remaining
date-specific need or concrete operational risk.

<a id="m-bb288b19f625"></a>
## Live Validation Observations

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Final V1-B Integration and Development Validation (2026-09-14). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-bb288b19f625-0"></a>

The identical Sydney Opera House must-visit re-test corrected the earlier
selected-but-unresolved contradiction: one resolved Place ID carried
`must_visit=true` and no unresolved-required conflict. A larger revised V1-A
case acquired real reviews/Profiles; this evidence changed one final POI
membership. The final set naturally reached 16 POIs. Four 4 x 16 directed WALK
chunks requested 256 baseline Route Matrix elements, and a structured nine-day
itinerary passed final date validation. These V1-A observations preceded Phase 3.

<a id="b-bb288b19f625-1"></a>

An initial full-V1 Web smoke exposed the cost of broad proactive checking:
16 selected POIs generated 16 exception tasks, consumed Web 6/6 and Page 6/6,
and produced zero accepted official claims. With no-negative-inference, the
effective Web state remained `UNKNOWN`. After the targeted trigger revision,
a comparable nine-day case still selected 16 POIs but generated zero Web tasks,
used Web 0/6 and Page 0/6, and completed itinerary generation and date
validation. This is an integration observation, not a formal efficiency study.

<a id="b-bb288b19f625-2"></a>

The targeted Australian Museum one-day case explicitly asked about admission,
fees, ticketing, advance purchase, and reservations. It generated two Group-1
Web tasks, retrieved first-party `australian.museum` sources, and produced two
Gate-accepted `OfficialCurrentEvidence` claims. Resolver marked
`general_admission_policy=AVAILABLE` and `admission_fee=AVAILABLE/free/0` for
general entry. `ticket_requirement`, `advance_ticket_purchase_requirement`,
and `reservation_requirement` remained `UNKNOWN`; a major-exhibition scoped
claim was not broadened to general entry. Accepted facts and references reached
the planner, while rejected candidates did not. The final one-day itinerary
passed date validation without cross-facet negative inference.

<a id="b-bb288b19f625-3"></a>

The Phase 3 checkpoint offline regression passed **545 backend tests**. Ruff lint
and `git diff --check` passed; formatting passed for the checked files except
an unchanged existing warning in `backend/tests/versions/v1/test_runner.py`.
No suite was rerun solely for commit grouping or documentation.
These live runs are development-time validation, not a formal benchmark or
statistical comparison with V0.

<a id="m-96e6c00046e4"></a>
## Final Development-Time Validation

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Complete V1 Freeze (2026-09-15). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-96e6c00046e4-0"></a>

The earlier named-place live failure and identical re-test established that
typed `NamedPlaceIntent` preserves a required Sydney Opera House Place ID and
`must_visit=true`. A separate revised V1-A live run observed review/Profile
evidence change one selected-POI membership and complete the natural N=16
case with four 4 x 16 directed Routes chunks, 256 baseline elements, and a
valid nine-day itinerary. The broad full-V1 Sydney Web smoke spent Web/Page
budgets 6/6 and 6/6 with no accepted claim; a comparable case under the
targeted trigger produced zero unnecessary Web tasks. The Australian Museum
case accepted official general/free-admission evidence into the planner while
ticket, advance-purchase, and reservation facets stayed `UNKNOWN`.

<a id="b-96e6c00046e4-1"></a>

The subsequent Melbourne request exposed loss of `ADMISSION_FEE` and
`TICKET_REQUIREMENT` in a raw-text phrase classifier before Web planning. The
one-call typed semantic migration preserved all four explicit requested facets
through task planning in an identical live re-test. Its inaccessible official
pages left those facts `UNKNOWN`; this was not claim-acceptance validation.

<a id="b-96e6c00046e4-2"></a>

In the first Singapore cross-country full-V1 smoke
(`ca93496f-53dc-467c-8a28-975fb65f7828`), upstream semantics, Places/reviews,
Weather, Routes, and targeted Web completed, but planner output contained
`Money.amount="1.00-10.00"`. The Foundry DTO permitted a string while shared
domain `Money` required a point-valued non-negative Decimal; domain validation
lost the entire itinerary before final date validation. This was a narrow
output-contract issue, not a semantic, provider-evidence, Resolver, or transient
failure. The identical request with reference date 2026-09-15 succeeded after
V1-only hardening (`d69ddaeb-d5cd-4154-ab29-3c0fda1c9404`). The same range
reappeared at `days[0].activities[2].estimated_cost` as `1.00-10.00 SGD` and
became `Decimal("5.50") SGD`. Its valid itinerary had four days, 11 activities,
and nine distinct selected POIs scheduled; National Gallery Singapore and
Gardens by the Bay were both required and scheduled. Final date validation
passed. National Gallery whole-venue facets remained `UNKNOWN`; the derived
activity estimate did not change official evidence or Resolver state.

<a id="b-96e6c00046e4-3"></a>

The final offline regression passed **605 backend tests** and Ruff. Diff
whitespace checks passed; 25 affected files passed the whole-file format check.
Five formatting suggestions in three other affected files were confirmed as
unchanged pre-existing lines and left intact. These live cases are
development-time integration observations, not formal benchmarks, statistical
accuracy estimates, universal generalization, or a V0/V1 superiority claim.

<a id="m-34dd83416425"></a>
## Historical Execution Flow and Comparability

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-34dd83416425-0"></a>

The independent V1 entry point is `scripts/run_v1.py`. Its fixed, non-agentic
graph is:

<a id="b-34dd83416425-1"></a>

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

<a id="b-34dd83416425-2"></a>

Provider calls go through `V1EvidenceAcquisitionService`, provider protocols,
Google adapters, and typed normalization rather than directly from graph nodes.
The V0 requirement-extraction prompt/schema, Foundry client/deployment behavior,
provider-default temperature behavior, base planning objective, and final
`Itinerary`/`PlanningResult` schemas remain the comparison baseline. V0 retains
its independent `scripts/run_v0.py` path and uses no external evidence. V1's
main changed input to generation is normalized external evidence; raw provider
JSON is not passed to the planner.

<a id="m-cbbb4a47d8ed"></a>
## Shared Ten-Day Date Contract

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-cbbb4a47d8ed-0"></a>

`backend/app/policies/trip_dates.py` enforces the project-wide inclusive window:

<a id="b-cbbb4a47d8ed-1"></a>

```text
reference_date <= requested_start <= requested_end <= reference_date + 9 days
final itinerary dates subset of requested trip dates
```

<a id="b-cbbb4a47d8ed-2"></a>

The trusted reference date is captured once at run start in the configured
IANA time zone and reused for relative-date extraction and both validation
boundaries. Product API callers cannot inject an arbitrary reference date;
trusted Developer/CLI/test paths may inject one for reproducibility. Validation
checks itinerary-level, day, and activity start/end dates. Product frontend
pickers use browser-local dates as UX guidance; backend validation also rejects
out-of-window direct API calls. This date contract is not V3 feasibility repair.

<a id="m-1b2433c28f42"></a>
## Runtime Configuration and Safety Limits

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-1b2433c28f42-0"></a>

Final configuration has three layers:

<a id="b-1b2433c28f42-1"></a>

```text
backend/app/runtime/budget_limits.py  global hard safety envelope
config/runtime.yaml                   validated non-secret runtime policy
ToolBudget                            one run's actual reservations and usage
```

<a id="b-1b2433c28f42-2"></a>

One global `TOOL_BUDGET_HARD_LIMITS` mapping defines the project-wide hard
ceilings. Strict Pydantic models reject missing/unknown YAML keys, duplicates,
invalid types, and budgets outside that envelope. The normal committed policy
sets `app.time_zone: Australia/Sydney`, `logging.level: INFO`, and a metadata
Run Trace in project-relative `logs/`. Relative trace paths resolve from the
repository root, independently of the shell working directory.

<a id="b-1b2433c28f42-3"></a>

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

<a id="b-1b2433c28f42-4"></a>

The last three counters are configured for the shared budget model but unused
by V1-A. `.env` remains for deployment-specific Foundry endpoint/deployment,
Foundry API key, and Google Maps API key. Budget, time-zone, logging, and trace
policy are not `.env` overrides. Changing an in-range runtime budget requires
only `config/runtime.yaml`; changing a hard ceiling is centralized in
`budget_limits.py`.

<a id="m-3474e64a79c9"></a>
## Places and Weather Evidence

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-3474e64a79c9-0"></a>

Places uses the API (New) in stages. One minimal-mask destination lookup obtains
a coordinate; up to three category Text Searches use location bias, minimal
identity/location/classification fields, and no reviews/photos/rating/hours.
The candidate mask is `places.id,places.displayName,places.location,`
`places.formattedAddress,places.primaryType,places.businessStatus`.
Candidates are deduplicated by Place ID and non-operational statuses removed.
The deterministic shortlist round-robins provider-ranked query categories,
uses stable Place-ID tie-breaking, and is bounded by eight places, the details
budget, and the square root of the baseline Route Matrix element limit.

<a id="b-3474e64a79c9-1"></a>

Only shortlisted places receive Place Details. The detail mask is `id,`
`displayName,location,formattedAddress,primaryType,businessStatus,timeZone,`
`currentOpeningHours,regularOpeningHours,rating,userRatingCount,websiteUri,`
`priceLevel,priceRange,accessibilityOptions`. `PlaceEvidence` keeps place
identity, location, type/status, applicable opening information, timezone,
selected rating/price/accessibility/site fields, availability, and provenance.
An individual details failure is represented as partial/unavailable evidence.
There is no V1-A review request.

<a id="b-3474e64a79c9-2"></a>

Weather uses one Google Daily Forecast request for the provider's full ten-day
horizon, then normalizes **only** dates inside the requested trip range. This
avoids provider/local-calendar boundary mismatches without allowing extra days
into the planner. `WeatherEvidence` contains availability and requested-date
daily condition, temperature range, precipitation probability, and maximum
wind speed when supplied. Provider failure remains explicitly unavailable;
the LLM must not fill missing weather facts.

<a id="m-80b9eb040c30"></a>
## Final Routes and Logical-Pair Transport Policy

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-80b9eb040c30-0"></a>

The original V1-A design used one mode-specific matrix. Live testing showed
that a default WALK matrix could identify an impossible walking transfer but
could not offer an alternative. The approved final policy retains a fully
directional, bounded baseline matrix and adds selective TRANSIT evidence only
for default WALK. A user-explicit supported mode remains single-mode and does
not trigger an automatic alternative. `DRIVE` uses `TRAFFIC_UNAWARE`;
non-DRIVE modes do not send that routing preference.

<a id="b-80b9eb040c30-1"></a>

For default WALK, each directed pair is non-walkable when distance is strictly
greater than 3,000 m, duration strictly greater than 2,700 s, or the condition
is `ROUTE_NOT_FOUND`. Same-place elements are excluded. The two directions of
a POI pair collapse into one unordered logical pair, ranked by the more severe
directed WALK result. Stable ascending Place-ID order chooses the canonical
TRANSIT direction. The highest-ranked pairs are selected within both the
`alternative_route_pairs` and `alternative_route_matrix_calls` budgets; pairs
sharing a canonical origin are grouped into sparse one-origin matrices. No
full second N-by-N TRANSIT matrix is issued.

<a id="b-80b9eb040c30-2"></a>

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

<a id="m-f38116455112"></a>
## Request Cache, Run Trace, and Failure Semantics

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f38116455112-0"></a>

Each run creates one in-memory `RequestCache` and `ToolBudget`. Canonical
request keys deduplicate identical Places searches/details, Weather requests,
and ordered Route Matrix requests, including mode, field mask, departure time,
and relevant options. Cache hits do not consume a second provider budget;
there is no persistent evidence cache.

<a id="b-f38116455112-1"></a>

The CLI creates one immutable `run_id` and a best-effort local trace at
`<project-root>/logs/<UTC timestamp>_<run_id>/`. `run.json` records input,
fixed reference date/window, requested dates, status, tool usage, final outcome,
the allowlisted effective runtime configuration, and its deterministic SHA-256
hash. `events.jsonl` records graph progress, provider/cache activity, routing
trigger evaluation, selected/truncated logical pairs, canonical directions,
representative departure time, alternative results, and failures. Optional
`llm/`, `tools/`, and `evidence/` payloads depend on the configured level.
The frozen default is `metadata`, with raw provider payload capture disabled.

<a id="b-f38116455112-2"></a>

Trace serialization recursively redacts recognized credential keys, bearer
tokens, assignments, and sensitive URL query parameters. The project-owned
console logging handler also redacts provider URL credentials, including
credentials that HTTP client INFO logging might otherwise print. `logs/` is
gitignored and is observability output, not application persistence. Tests use
disabled tracing or temporary directories. A trace write failure disables
tracing without changing planner output or provider semantics.

<a id="b-f38116455112-3"></a>

Missing critical requirements, invalid trip dates, no viable candidates,
generation failure, and final-date violations stop a run. Individual Places
Details failures, partial Routes results, and Weather unavailability remain
explicit partial/unavailable evidence. No V1-A validation/repair loop follows
generation.

<a id="m-6ceb8b3dd346"></a>
## Final Sydney Live-Flow Acceptance Case

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-6ceb8b3dd346-0"></a>

The final complete live flow used this new request: a one-day Sydney trip for
two travellers on 2026-09-15, interested in harbour views, wildlife, and
beaches, preferring moderate walking without unnecessarily long walking
transfers. The run used `reference_date = 2026-09-12`; the allowed window was
2026-09-12 through 2026-09-21. Requirements and final itinerary dates were
both 2026-09-15 and passed the shared date checks.

<a id="b-6ceb8b3dd346-1"></a>

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

<a id="b-6ceb8b3dd346-2"></a>

For a compact record of the actual canonical TRANSIT selections, `P1` through
`P8` denote the eight Places in `shortlist_created` order in this run's
`events.jsonl` (run ID `83b678ac-3331-43b7-b9b0-847662d1a7e6`). The
metadata trace retained Place IDs, not a complete normalized name mapping:

<a id="b-6ceb8b3dd346-3"></a>

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

<a id="b-6ceb8b3dd346-4"></a>

Canonical directions queried:

<a id="b-6ceb8b3dd346-5"></a>

```text
P5 -> P6, P3 -> P5, P8 -> P5, P4 -> P5,
P1 -> P5, P2 -> P5, P5 -> P7, P8 -> P6
```

<a id="b-6ceb8b3dd346-6"></a>

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

<a id="b-6ceb8b3dd346-7"></a>

The run completed and its metadata trace recorded the config snapshot/hash,
logical-pair trigger and grouping events, observed/mirrored counts, budgets,
and final date validation. The redaction check found no configured API key in
the trace. This was an **integration and evidence-acquisition acceptance case**,
not proof of a perfectly feasible generated itinerary or a formal V0/V1
quality comparison.

## Shared changes and latest joint acceptance

The complete shared input, output and joint quality events live in [development_record](development_record.md). Latest V1 conclusions are indexed by [milestones](v1_milestone.md); no complete joint run is duplicated here.
