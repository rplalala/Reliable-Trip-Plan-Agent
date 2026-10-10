# V1 tools, requirements and transport development

Historical engineering observations, September 2026. Current rules belong to
[requirements/evidence](../../0002-requirements-evidence.md),
[transport](../../0003-itinerary-transport.md) and
[operations](../../0007-application-operations.md). This record groups major developments;
[V1 milestones](v1-milestone.md) distinguish original freezes from later reopening, and
[selector experiments](v1-selector-experiments.md) own QCGRE/B1/B2 method results.

## Original provider/capture baseline — 2026-09-12

The independent graph extracted requirements, checked dates, resolved/discovered places,
shortlisted, obtained Details/Weather/Routes, generated and checked final dates. No Reviews,
Web, RAG or Repair ran. Destination plus three category searches produced minimal identity/
location/status candidates; only up to eight shortlisted places obtained rich Details.
The original mask included rating and `userRatingCount`, unlike the later revised review
path. Weather requested the provider ten-day horizon and filtered to requested dates.
Missing facts were not synthesized.

The runtime separated global hard limits, strict nonsecret YAML and per-run reservations.
Original normal/hard limits were:

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

Web/Page/review counters were configured but unused by original V1-A. Deployment secrets
stayed in environment; budget/timezone/logging policy came from YAML. Request-local caches
reused keyed evidence; metadata-only traces retained identities/events/config/budgets and
redacted credentials, but not complete provider payloads. Trace failure preserved planning;
Details/Weather/Routes failures could produce partial evidence while critical requirements/
dates/candidates/generation failures stopped execution.

The original date window was reference+9; trusted reference was captured once. Product
had no override, browser dates were UX guidance. YAML later owned Australia/Sydney;
current +13 selection does not rewrite that old input window.

### Original Sydney route observations

Run `83b678ac-3331-43b7-b9b0-847662d1a7e6`, reference September 12, trip September 15,
two travelers, harbour/wildlife/beaches/moderate walking. Four searches yielded **16**
candidates, **8** shortlisted/Details; one Weather succeeded but its daily payload was
not retained and cannot be reconstructed. WALK 8×8 (**64 elements**) found **42 directed
nonwalkable** results, collapsed to **21 pairs**, admitted **8**, truncated **13**.
Metadata retained P1–P8 in shortlist order, not a normalized name map:

| Ref | Place ID |
| --- | --- |
| P1 | `ChIJV_wrHl2uEmsR92Q_ubhgXDI` |
| P2 | `ChIJLat3W0euEmsRCQCK0yaDjTc` |
| P3 | `ChIJQyYU8QOrEmsRFno4dKGQTYo` |
| P4 | `ChIJf2-DIACvEmsRgudjrmfw2Lo` |
| P5 | `ChIJi4HdHKCZEmsRYPPy-Wh9AQ8` |
| P6 | `ChIJm_XsjvyqEmsRQNv6iYFYSXA` |
| P7 | `ChIJswapWjeuEmsR_QZi2zrhtRI` |
| P8 | `ChIJ7fQkR0y3EmsRAvF7TJkyUd4` |

Queries were P5→P6, P3→P5, P8→P5, P4→P5, P1→P5, P2→P5, P5→P7, P8→P6.
Origin grouping made **six TRANSIT calls/eight observed elements**, with eight labelled
reverse-duration estimates, at representative September 15 12:00 +10. Total Routes:
**seven calls/72 elements**. Budget observations were baseline 64/64, alternative 8/8,
alternative calls 6/8, Weather 1/2, search 4/4, Details 8/8, candidates 16/20; Web/review zero.
Date validation passed; these are acquisition/integration observations, not timetable
proof or a formal V0/V1 comparison.

## Revised Places/review and official Web integration

September 14 V1-A introduced typed named intent, required identity protection, duration
capacities K=min(16,2D+2), R=max(10, K+2), C=max(20,2R), review cap=min(6, ceil(K/3)).
Destination search had 1/1, candidate 12/12; these were execution ceilings, not interest
quotas. Structured status separated permanent closure, temporary risk and future opening.
Review-only acquisition used up to five deduplicated reviews; Profile references/identity/
counts/taxonomy were validated, confidence low at one review and medium at two-plus.
Review failure was neutral, not fabricated experience. Actual rating was separate from
Profile; no `userRatingCount` in the revised path. Selection/review policy later changed
through the separately recorded selector experiments.

Identical Opera House revalidation cleared unresolved required identity. The larger
Smoke B acquired reviews that changed one membership, reached **16** selected POIs and
**256 WALK elements** in four 4×16 chunks, then a valid nine-day itinerary. Those revised
V1-A runs preceded Web Phase 3.

Broad Web smoke created **16 exception tasks**, spent Web 6/6 and Page 6/6, accepted **zero**
claims and retained UNKNOWN. Targeted-trigger revision on a comparable nine-day/16-POI
case produced **zero tasks/sends**. Australian Museum's explicit admission/fee/ticket/
advance/reservation request created **two Group 1 tasks**, accepted two first-party claims,
and resolved general admission/free fee 0; ticket/advance/reservation stayed UNKNOWN.
A major-exhibition claim was not broadened to general entry. Phase 3 backend **545 passed**;
Ruff/diff passed, with an unchanged existing runner formatting warning.

Melbourne lost fee/ticket facets in a phrase classifier; one-call typed extraction
preserved all four requested facets in identical live revalidation. Inaccessible pages
left facts UNKNOWN, so this did not validate claim acceptance. Singapore run
`ca93496f-53dc-467c-8a28-975fb65f7828` completed providers/Web but range `1.00-10.00`
violated point-valued domain Money, losing the itinerary. V1-only hardening let identical
reference-date September 15 run `d69ddaeb-d5cd-4154-ab29-3c0fda1c9404` complete four days,
11 activities/nine distinct selected POIs, including required National Gallery/Gardens.
Its repeated range at day 0/activity 2 became **5.50 SGD** midpoint, not verified spending.
National Gallery whole-venue facts remained UNKNOWN. Final complete-V1 backend **605**,
Ruff/diff and affected formatting passed; these were developmental, not statistical results.

## Reopened supply and requirement-boundary failures — 2026-09-19

The planning-supply replacement was offline validated (**193 focused; 673 backend,
9 skipped**), but its approved B/A live attempts both stopped before discovery: B
redeclared reserved party (`invalid_subject_ids`), A's temporary discovery ID exceeded40
characters. No evaluator/Google/selection/generation followed; these were not E2E passes.

The systematic requirement boundary then assigned canonical IDs in the application,
validated opaque temporary references/source integrity and distinguished failure classes.
`interpreted_requirements_2` and default-off private pre-DTO capture retained provider
structure/application resource/link checks. Affected **262**, backend **711/9 skipped**,
Ruff/diff passed; it did not change supply/cache/HARD policy or produce live evidence.

The frozen nine-case matrix's first attempt stopped with OpenAIConnectionError after
one client/HTTP attempt, **0.453 seconds**, no response/usage; eight cases were unexecuted.
Later network-authorized continuation yielded **8 completed schema/DTO/canonical/source
passes**. One separate invocation failed before HTTP from harness shared-client cleanup;
remaining seven used a harness-only correction, not production changes. Destination-as-
REQUIRED, ordinary negatives promoted HARD and pronoun attribution stayed semantic issues.

Prompt 3/semantic policy 1 then distinguished trip scope versus actual visit, tradeable
polarity versus hard strength, mentioned people versus travelers/preference owners/party.
Affected **275**, backend **724/9 skipped**. The ten-call no-retry/no-downstream matrix
produced **8 accepted canonical outputs and 2 extraction-issue stops**. Optional unknown
counts still became blocking issues; the Spanish expectation was qualified as ambiguous,
not counted successful. Later shared-input events retain their own scope in
[semantic correction](semantic-reference-correction.md) and
[development pilots](development-pilots.md). Neither valid wire nor larger supply proved
correct semantic interpretation or trip quality.

## Nearby implementation and bounded live evidence — 2026-09-19

V1 moved references after successful primary identity/date checks, discovering around
actual resolved scheduled anchors rather than leftover supply. Zero to three untimed
references preserved primary fields/cost diagnostics; errors/empty outcomes preserved
primary success. The historical policy 1 had three attempts, ten results each, 800-m radius,
300-m nontransitive representative reuse, ten-second phase/four-second requests, zero
retries, DISTANCE mixed restaurant/cafe/park/museum types. It added actual Nearby sends,
no model/Details/Reviews/Routes/Web calls; references never fulfilled required visits,
entered expenses or became scheduled POIs. Output retained legacy unused IDs plus explicit
supply-not-scheduled and outside-supply-reference sets. V0 retained its model-reference DTO.

Offline full gate was **829 passed, 9 skipped, 8 failed**: seven stale response/trace fixtures
and one real timer boundary that could schedule again after a phase-limited timeout.
Correction stops unconditionally at that timeout and awaits cancellation; **53 affected
checks passed**, Ruff/diff passed. No second full gate was run. The earlier **813/9/1**
checkpoint also remains a failed full run, not retrospectively green.

One identical frozen P input completed each version: V0 **six timed activities/two model
references**, V1 **eight supplied (one required), five scheduled/three independent references**.
This sample covered three primary days, without attributing improvement over an earlier
two-place sample to Nearby. Three searches returned 30 rows, rejected two closed/two
scheduled, retained 26 eligible, selected 3 and left 23 at the final cap. Ho Jiak/Bridge
anchors were uncovered; no reuse/cache/nonempty-attribution branch occurred.

| Reference | Anchor / day | Type | Straight-line m | In supply | Source |
| --- | --- | --- | --- | --- | --- |
| Western Foyers | Sydney Opera House / 2026-09-21 | restaurant | 65.67 | False | google_places_nearby:nearby-4fef51b3-6d16-4f46-8229-3f124530c4ab:0 |
| Barista 12 | Cafe Sydney Restaurant / 2026-09-21 | restaurant | 4.60 | False | google_places_nearby:nearby-cb368694-1545-4f3a-9ae1-75515e930c50:2 |
| 3 Steps Takeaway | Hyde Park / 2026-09-22 | coffee_shop | 133.72 | False | google_places_nearby:nearby-b814ec49-687a-43a5-a41b-b0e49fe52449:1 |

All three selected references were outside supply. Observed straight-line distances were
65.67259530526982,4.601904039705398,133.7187953677695 meters, not walking routes.
Search centers were Opera House(-33.856784399999995,151.21529669999998),
Cafe Sydney(-33.8621894,151.2109059), Hyde Park(-33.8715202,151.21162429999998).
Each returned ten normalized rows and used four-second timeout. Captured raw responses/
ledger retain the complete candidate inventory; selected/rejected coverage is summarized here.

### Frozen input and identities

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

Reference date: 2026-09-19. Request SHA-256: 000146c0c1bb27c79de4451542b72bc1788dc5552c76172cf8b49d0570f20b39.
Both dispatches use the explicit version runner recorded in manifest.json; product dispatch is unchanged.

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

Input planning_request_2; output itinerary_2; requirement prompt preference_prompt_5;
contract interpreted_requirements_3; reference policy nearby_references_1; actual model gpt-5.6-luna.

Generated content is not independent factual endorsement. The actual timed visits were:

V0:

| Date | Time (+10:00) | Place / activity | Estimated cost |
| --- | --- | --- | --- |
| 2026-09-21 | 10:00-12:00 | Sydney Opera House | Unknown |
| 2026-09-21 | 14:00-15:30 | Royal Botanic Garden Sydney | Unknown |
| 2026-09-22 | 10:30-12:30 | Art Gallery of New South Wales | Unknown |
| 2026-09-22 | 14:30-16:00 | Sydney Fish Market | Unknown |
| 2026-09-23 | 10:30-12:00 | Harbour ferry sightseeing ride | Unknown |
| 2026-09-23 | 14:00-15:30 | Museum of Contemporary Art Australia | Unknown |

V1:

| Date | Time (+10:00) | Place / activity | Estimated cost |
| --- | --- | --- | --- |
| 2026-09-21 | 10:30-12:00 | Sydney Opera House | Unknown |
| 2026-09-21 | 13:30-15:00 | Cafe Sydney Restaurant | Unknown |
| 2026-09-22 | 10:30-12:00 | Hyde Park | Unknown |
| 2026-09-22 | 13:30-15:00 | Ho Jiak Haymarket | 30.00 AUD |
| 2026-09-23 | 11:00-12:30 | Sydney Harbour Bridge | Unknown |

V0 suggested Grounds of Alexandria (Sep 22) and Spice Alley (Sep 23), explicitly unverified.
V1 appended the three source-linked references above. Main notes retained gentle/seated
travel intent and unresolved hours/access; V1 noted applicable provider hours without
turning date exceptions or accessibility into guarantees. Ho Jiak's AUD 20–40 estimate
became 30, not a whole-trip amount or invoice. Co-located/subvenues could add limited value.

Canonical supply ledger (REQUIRED is Opera House; all others OPTIONAL):
- Sydney Opera House: ChIJ3S-JXmauEmsRUcIaWtf4MzE
- Sydney Harbour Bridge: ChIJ49XqJV2uEmsRPsTAF7eOlGg
- Sydney Place: ChIJKc8tok6vEmsRsafPJow_QCs
- Hyde Park: ChIJDflB7BWuEmsRYPbx-Wh9AQ8
- Ho Jiak Haymarket: ChIJKWuQkCSuEmsRHNk3-wIWksY
- WILD LIFE Sydney Zoo: ChIJLat3W0euEmsRCQCK0yaDjTc
- Luna Park Sydney: ChIJ384_FGCuEmsRFAbHLAWVPGg
- Cafe Sydney Restaurant: ChIJOahrAxKuEmsRiJOniUNkOZY

Scheduled IDs were Opera House, Bridge, Hyde Park, Ho Jiak and Cafe Sydney; unused/
supply-not-scheduled were Luna Park, Sydney Place and WILD LIFE. References remained
outside that supply, with no unscheduled required or unlinked activities.

### Usage, invariance and remaining live coverage

| Case / task | Input | Output | Reasoning (included) | Cached input (included) | Cache write (included) | Captured seconds |
| --- | --- | --- | --- | --- | --- | --- |
| V0_P / InterpretationDraft | 3946 | 742 | 407 | 0 | 3943 | 8.266 |
| V0_P / Itinerary | 1995 | 1664 | 623 | 0 | 1992 | 14.922 |
| V1_P / InterpretationDraft | 3946 | 784 | 440 | 3943 | 0 | 7.422 |
| V1_P / ExperienceProfileDraft | 1303 | 284 | 147 | 0 | 1300 | 4.203 |
| V1_P / ExperienceProfileDraft | 1019 | 327 | 147 | 0 | 0 | 3.609 |
| V1_P / ExperienceProfileDraft | 986 | 451 | 313 | 0 | 0 | 5.250 |
| V1_P / V1Itinerary | 19809 | 2018 | 1032 | 0 | 19806 | 19.766 |

SDK usage counted each response once; reasoning/cache are subsets, actual invoice unknown.
V0 total **23.234 seconds, 2 calls, 8347 tokens**; V1 **54.359 seconds, 5 calls, 30927 tokens**.
V1 primary **53.125 seconds**, Nearby phase **1.157 seconds**; three HTTP durations 0.391/0.375/0.344 seconds.
All 25 external sends returned 200: Google Text Search 4 (destination 1/named 1/default 2),
Details 10, Reviews 3, Weather 1, Routes 4 with 64+2+1+1=68 elements, Nearby 3; seven model
calls each sent once, no retry. Web/page/RAG/evaluator zero. These samples were not a
controlled performance comparison.

Primary before/after business SHA-256:
`f2dc5e6a3b8a116d08d3abfb44ecf1840e25d6a440f8b032c56395e711fbe1b0`.
Cost/required/supply/role checks were unchanged; captures had no errors. Local source:
`logs/nearby_reference_acceptance_20260919_095712/`. Production/configuration was fixed
and no tests repeated. Failed/empty/timeout/attachment/no-anchor/cache/cancellation
branches remained offline-only. Names/addresses were supplied evidence, not certified
neighborhood/accessibility/price/value. Nearby did not fix sparse primary coverage.

## Shared output and mixed transport — 2026-09-25

### Compatible transfer output update (2026-09-25)

Optional `transfers` (missing→empty) and frontend rendering were added while preserving
primary DTO/prompt, independent entry points and then-Product default. At that stage
V3 bound verified/unknown leg estimates/reserves; V0–V2 did not invent fields or acquire
extra Routes just for compatibility. It did not implement Product V3 selection.
Later mixed transport extended shared V1–V3 baseline behavior, distinct from V3 Repair.

### 2026-09-25 - Shared first-generation mixed transport

The shared graph prepared directed options before one primary call, bound actual timed
adjacencies, then the optional V3 extension before final Nearby. Application-owned
transfers/diagnostics retained unknown locations and regenerated V3 adopted adjacency;
V1/V2 did not edit activities or run Repair. Shared schedule/route policies owned occupancy,
applicability and continuous windows; V3 retained operation authorization and atomic edits.

Historical capacity was primary 252000/output 16384/framing 2048, baseline 7 requests/
400 elements/64 per matrix; supplementary 32 directed pairs/32 sends/64 elements with
post-generation 16/16/32 reserve. Pair admission was not sends: new mode/time reused
admission but charged actual sends; failed sends counted and cache reuse survived
quota exhaustion. Shared Repair cache/failure history did not reset Repair's own budget.
Route work was cumulative120 seconds with 30 post reserve, no double-counting overlap and no
LLM/Web pause charge. Whole-request deadline/cancellation still applied; local route
stop preserved primary output. One WALK deficit did not prove all modes impossible;
mode policy and factual prohibition were distinct. Actual-departure TRANSIT, stable
WALK/basic DRIVE and separate DRIVE reserve retained evidence applicability.

A compact evidence catalog collided when different modes shared provider `source_ref`.
Correction keyed complete evidence while preserving provenance. Other failing assertions
were old capacities/topology/fixtures, migrated to approved policy rather than weakening
acceptance. A malformed-index fixture needed existing successful `{}` status. Final
shared/version/route/runtime affected gate **583 passed**,18.62 seconds; later shared
`transfer_time_check` consolidation **119 passed**,8.23 seconds. No full repository run or live
provider/model/embedding/database call was performed at this checkpoint.

### Serializer capacity evidence

Installed offline tokenizer/current prompt/schema/serializer measured system 1161,
schema 792, framing 2048. Sections are not extra additive partitions of total input.

| Synthetic case | User tokens | Complete input | Result |
| --- | ---: | ---: | --- |
| 3 days, K12 | 36019 | 40020 | within 252000 |
| 5 days, K16 | 58602 | 62603 | within 252000 |
| 10 days, K20 | 94481 | 98482 | within 252000 |
| 10 days, bounded additional mixed facts | 96859 | 100860 | within 252000 |
| 10 days, 24 semantic requirements / long text | 120339 | 124340 | within 252000 |
| Engineering-only near-limit padding | 247903 | 251904 | within ceiling |
| Engineering-only overflow padding | 248103 | 252104 | rejected |

The two padding cases test the engineering guard only; they are not claimed to pass every
upstream source-text/fact bound. Necessary facts were not deleted to fit. The compact
projection preserves all directed baseline facts; omission audit is empty because no selective
omission policy is enabled. Overflow fails closed instead of silently dropping requirements.

A schema-validated ten-day / 50-activity primary output is 6168 tokens, below 16384; adopted
transfers are not model output. This is output-capacity evidence, not proof of realistic model
completion, factual feasibility, or a promise that longer notes always fit. No provider usage
was estimated or reported as actual usage.

## Cross-checkpoint limitations

The earlier shared first-draft/role/K20 extension was offline-only and retained failed
full gates/targeted corrections in the [joint development history](development-pilots.md).
Mixed transport could use only supplied POIs, not rediscover omissions; unknown occupancy,
unsupported modes, unavailable routes/access/parking/prices and future reality remained.
Caps were execution bounds, not optimal-budget measurements. Capacity tests did not prove
real model completion, actual-time TRANSIT performance or repair of older seven-day failure.
