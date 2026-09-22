# Known issues and coverage limits

<a id="b-f91feff05852-0"></a>

Historical issue inventory from the earlier quality_first_1 pair (2026-09-20).
The current checkpoint triage below supersedes its coverage and next-action statements. None of these
items automatically authorizes new implementation, paid runs or budget increases. They do not
block preserving the current source baseline, but limit the corresponding capability claims.

<a id="b-f91feff05852-1"></a>

| Priority / type | Current evidence | Effect on claims | Smallest next step |
| --- | --- | --- | --- |
| P1 tool integration: Weather | Repeated actual HTTP 404; normal weather path not shown in these cases | Cannot claim successful weather integration from these samples | Diagnose saved requests, endpoint and configuration before a separately authorized fix |
| P1 product input | Frontend budget optional; backend amount/currency mandatory; clarification issues missing from frontend type | UI/backend contract incomplete | Separate small input/response alignment task |
| P2 Web integration | Retrieval occurred but accepted current facts were zero | Does not alone prove the evidence gate is wrong or working correctly | Trace saved retrieval, extraction and gate reasons; distinguish insufficient data from wiring |
| P2 SQL performance | Exact retrieval has large execute/read variation; EXTERNAL/TOAST observations persist | Longer timeout is functional allowance, not optimized performance or SLA | Preserve diagnosis; separately approve a measured storage/index experiment if needed |
| P2 Web performance/usage | V2 Web 29.12 s; reasoner token usage unknown | Total latency and complete model cost cannot be attributed precisely | Inspect per-task capture and local observation gap before changes |
| P2 visitor suitability | Some places may be businesses or staff-only facilities | Place identity/type does not establish public tourist access | Define evidence-based suitability evaluation before a new filter |
| P2 repeated experience | Different IDs may refer to the same building/complex | Canonical dedup does not guarantee experiential diversity | Inspect saved examples and define evaluation criterion |
| P2 cost quality | Activity costs unknown | Budget compliance remains unverified | Specify an honest cost-coverage evaluation; do not invent prices |
| P2 preference/feasibility | Both versions scheduled eight places with different options | Equal count proves neither equal quality nor RAG benefit | Prepare separately approved evaluation criteria |
| P2 uncovered paths | No K16 ten-day live, nonzero Reviews/Profile, or live fallback/failed-cache/cancellation coverage in this pair | Normal-path acceptance is not all-branch acceptance | Reuse offline evidence; authorize targeted live only when necessary |
| P2 product dispatch | Product/developer APIs expose V0 only; developer UI retains older input | CLI independence is not product version-selection support | Decide explicit UI/API scope before implementing |
| P2 named identity | Melbourne same-name market/station remains unresolved before RAG | Conservative REQUIRED clarification; not a retrieval performance defect | Retain clarification until an approved typed disambiguation change |

<a id="b-f91feff05852-2"></a>

Nearby success cannot repair sparse main itineraries or prove every day is appropriate.
A reference is not a scheduled visit, measured walk, current price or accessibility guarantee.
No full correctness, production-ready status, formal comparison or automatic re-freeze is claimed.

<a id="b-f91feff05852-3"></a>

At that earlier checkpoint, the proposed next task was saved-capture Weather diagnosis.
Subsequent Tokyo/Sydney evidence distinguished coverage from successful acquisition. Do not reopen candidate-selection research as a prerequisite.
Detailed dated evidence remains in [Phase 6 history](v2_development.md)
and the [V1 design history](v1_development.md).


## Sydney maximum-window evidence and baseline closure (2026-09-20)

The earlier table describes the quality_first checkpoint, not the later Sydney coverage.
Evidence: ../logs/sydney_max_duration_smoke_20260920T072203Z/manifest.json,
assessment.json and each version's result.json in that directory. These local ignored artifacts
are not guaranteed available in another checkout. Historical raw outputs must not be overwritten.
Sydney demonstrated ten forecast dates, K16/256 baseline route elements, nonzero Reviews/Profile
and RAG fallback; cancellation, failed-cache and provider-failure branches remain untested there.

Sydney failures remain fixed future evaluation/V3 samples: V2 four trailing empty days, raw first-day
ordering inversion, MCA ending 17:30 while its note claims a 17:00 closing limit; V1 repeated
canonical visits; same-day past times; unknown costs and visitor access; nearby/subvenue redundancy.
The ordering issue is now addressed at the shared output boundary, not by rewriting this run.
All other itinerary-level findings remain observations, not baseline repair features.

Visitor suitability has three conceptual evidence states: explicitly visitor-facing, explicitly
non-public/private/non-visitor, and UNKNOWN. These are audit categories, not new schema fields.
Current Places contracts expose type, operational status and wheelchair accessibility, but no
reliable public-visitor-access predicate. TripWorld categories are static discovery priors.
OPERATIONAL is not tourist suitability; wheelchair access is not public admission. UNKNOWN can
remain in the candidate pool but must not be described as verified visitor access.

In the Sydney V2 saved supply, Warren and Mahoney Architects and Sydney Architect Group have
primary_type=service; distinctive Living Design has primary_type=general_contractor. All three
are OPERATIONAL with available Details and wheelchair-access fields, without explicit non-public
access evidence. All are Google-only discovery, not TripWorld category conversions. The actual
Google query plan included `distinctive local architecture in Sydney, Australia`; the search
semantics can surface commercial services. The saved metadata does not retain each raw search
response, so exact per-result query attribution is not independently proven here. Current factual
eligibility rejects exclusions, permanent closure, definite future opening incompatibility,
invalid coordinates or unavailable required Details; none proves these firms non-public.
Their retention is a discovery precision and missing visitor-evidence limitation, not a proven
lost private-access flag. No name blacklist, type ban, suitability model or admission change was made.

Cost nulls remain null through mapping/output. Range midpoints carry projection diagnostics;
no baseline budget PASS is computed. Whole-trip affordability remains UNKNOWN with incomplete
cost evidence. No price provider, prompt tuning or generation repair was added.


## Current checkpoint triage (2026-09-20)

V2 current implementation checkpoint accepted. This finite static/capture audit found no new
material baseline correctness defect. It is not a proof that all branches or factual outputs are
correct. Categories: A confirmed bug (fixed where stated); B pending engineering diagnosis;
C accepted capability/evidence limitation; D future V3 capability. No implementation is authorized
by this inventory. Evidence and run identifiers are in the [acceptance record](development_record.md#v2-current-checkpoint-acceptance).

| Issue | Category and evidence | Next responsibility / effect on acceptance |
| --- | --- | --- |
| Activity array chronology | A, fixed offline: shared stable start-time sorting; Sydney original output retained | Shared structural correctness, not V3; 78 affected tests passed after the historical live run |
| Exact SQL variability | B, execute/read latency varies; successful Tokyo and Sydney retrieval, historical timeouts and EXTERNAL/TOAST observations | V2 retrieval performance engineering; no evidence here of incorrect results. Different queries/environments are not a controlled cold/warm experiment |
| Sydney no_authorized_domain | C for the two inspected tasks: 477 Pitt St and Surry Hills had null website_uri and empty allowed_domains | Expected bounded gate, not demonstrated domain loss. No external Web sends. Missing official evidence remains UNKNOWN |
| Tokyo Web accepted facts zero | B: Bunkamura had an authorized domain, completed_with_sources, one search/two page targets, zero accepted facts | Acquisition is demonstrated, factual sufficiency/gate reasons need separate diagnosis; zero acceptance alone proves neither a bug nor correctness |
| Weather coverage | C: Tokyo 404 versus Sydney HTTP 200 with ten projected dates | Coverage limitation is not a RAG defect. Future shared provider/date-contract TODO below |
| Visitor suitability | C: firms/service/general_contractor records were operational; no inspected typed private/employees-only evidence | UNKNOWN public access. Do not blacklist names/types or treat accessibility as tourist access; V3 may warn, not invent evidence |
| Same-day remaining hours | C: date-valid today can include already-past time slots | Product/input boundary. Evaluation preparation should use start >= trusted date + 2, not a permanent product rule |
| Empty/unbalanced days | D: Sydney V2 supplied 16 but days September 26-29 were empty | Detect unintended under-planning versus intentional rest; targeted day repair, no fixed attractions/day quota |
| Repeated/redundant visits | D: Sydney V1 21 activities/14 unique canonical places; distinct IDs may share a complex | Contextual validation, not blind deduplication; repetition can be intentional |
| Opening-hours conflict | D: Sydney MCA 15:30-17:30 versus a note mentioning 17:00 closure | Validate against trusted date-applicable evidence; regular weekly hours are not date-specific guarantees |
| Route/day feasibility | D: complete route matrices were supplied, but sequencing was not explicitly validated | Post-generation transition/window checks and targeted repair; matrix presence alone is not feasible itinerary proof |
| Costs/budget | C missing prices; D evidence-based budget validation | Current null costs remain null, not zero or PASS. Inadequate coverage must remain UNKNOWN |
| Melbourne required identity | C conservative ambiguity before RAG | Separate shared identity capability; never bypass REQUIRED to claim retrieval success |
| Web latency/unknown usage | B observability/performance; historical unknown reasoner usage retained | Do not infer zero tokens or attribute all V2 latency to RAG |
| Product input/dispatch | B known frontend/backend alignment gap and V0-only API dispatch | Separate product task; independent CLI V0/V1/V2 evidence does not prove UI version selection |

Places requests include websiteUri; PlacesAdapter maps it to website_uri and normalization
preserves it. Official Web tasks bind canonical place IDs, derive allowed domains from that
place's HTTPS website or configured exact overrides, and stop when the list is empty. Sydney
trace tasks 06f15a500f2583091cb7 and 2c528cefde4d15b7603d match the two null-website places.
Tokyo task 2d8af70b54e4d4506b28 used www.bunkamura.co.jp for a temporary-closure uncertainty.
This comparison supports the bounded Sydney conclusion; it does not certify every provider payload,
all mappings or every accepted/rejected Web fact. HTTP-only websites are not silently promoted to
HTTPS under the current authorization policy.

Business operational status and wheelchair fields do not prove public visitor access. The
inspected firms passed the existing factual eligibility boundary; no supported explicit private
access fact was found and ignored. Unknown prices remain nullable through DTO/mapping/projection;
there is no current verified whole-trip budget PASS. Future validation must distinguish lack of
evidence from a contradiction, including generated notes, times, place use and budget claims.

### Historical shared Weather/date proposal (superseded on 2026-09-22)

The requested direction is Google Weather -> Open-Meteo in the shared Weather abstraction, not a
V2-specific improvement and not a V2 acceptance blocker. Provider endpoint/coverage, licensing,
attribution, error mapping, timezone/day mapping and field compatibility require verification
before implementation. This audit made no provider calls or claims about current service terms.

Proposed selectable calendar window: [today, today + 14 days], inclusive (15 selectable dates).
Separately enforce end - start + 1 <= 10 days. Example trusted date 2026-09-20: latest selectable
date 2026-10-04; 2026-09-22 through 2026-10-01 is a valid ten-day example under the proposal.
At that proposal checkpoint, code used [today, today + 9]; this statement is historical.

Expected scope: shared trip_dates policy and request validation; Weather adapter/factory/protocol
and normalization/config/environment examples; V0/V1/V2 shared date tests; frontend date controls
and related documentation. The existing D<=10 C/G/send/K/P and route-matrix capacity envelope
remains sufficient; a later start is not a longer trip. Same-day remaining-hour planning remains
unsupported. No Weather rewrite, capacity redesign, V3 implementation or new validation run is
part of this checkpoint task.

<a id="first-draft-and-v3-boundary"></a>
## First-draft and V3 boundary - 2026-09-20

The later shared baseline adds full-date-range guidance, a normal full-day 2-5 distinct
main-POI target, declared roles, read-only diagnostics, K18/K20 for nine/ten days and
corresponding Routes capacity. These are implemented first-draft capabilities, not proof
that the historical Sydney/London outputs have improved. The target is not a schema rule.

| Remaining issue | Current status / responsibility | Future design |
| --- | --- | --- |
| Below-target or empty dates / early concentration | Still possible; diagnostics observe, no refill. Rest/pace and long REQUIRED visits may justify fewer visits. | [V3-1/T04](v3_design.md#violation-and-uncertainty-categories) |
| Repeated IDs / redundant subvenues | Repetition is visible, not automatically invalid; different IDs need not mean distinct experiences. | V3-2/T05 |
| Opening/time or generated-evidence contradictions | Date-specific evidence must support a conflict; notes alone are not verified hours. | V3-3/V3-8/T06 |
| Route transitions / overlaps | Array sorting and full matrices do not validate temporal feasibility. | V3-4/V3-5/T07 |
| Visitor access uncertainty | OPERATIONAL/service type does not prove public access or inaccessibility. | V3-6/T09 |
| Cost/budget uncertainty | Null is unknown, not zero; insufficient coverage cannot certify budget feasibility. | V3-7/T08 |
| London connection timeout | Tolerance changed 2 -> 10 seconds; effectiveness untested live, root cause unproven. SQL60/RAG360 unchanged. | Shared/V2 engineering, not V3 |
| SQL read variability, Weather coverage, Web sufficiency, identity ambiguity | Existing separate issues remain; none is solved by K20 or a longer connection wait. | Shared/V2 engineering/evidence |
| Same-day remaining hours | Diagnostics explicitly not_assessable; no remaining-hours planner was added. | Separate shared product capability |

[The V3 roadmap](v3_design.md) owns the concrete future design and TODO. Accepted V2
implementation does not mean all itinerary outputs are feasible. Repair, re-validation
and additional post-draft acquisition remain unimplemented. The prior issue triage and
its evidence retain their original checkpoint scope.

## Current shared Weather/date status (2026-09-22)

The proposal above is implemented and offline-validated, not integrated-live-accepted. One direct
Open-Meteo probe returned200 for10 delayed London dates; the last date had null requested fields.
Availability must remain partial/unknown as appropriate. Forecast completeness and forecast accuracy
are separate limitations. The free endpoint is for non-commercial use with attribution, not an
unrestricted commercial deployment promise. Browser date boundaries now come from the backend;
existing frontend budget/developer input/clarification gaps are deliberately unchanged.

The latest London V2 draft had no empty dates but four below-target days, one repeated park and an
unverified hiking-club activity. Prices and public/event access remain uncertain. These are not fixed
by changing Weather. V3 validation/repair is still unimplemented. Same-day elapsed hours, SQL
variation and Melbourne identity ambiguity remain open. Database reproduction is deferred.


<a id="weather-window-14-20260922"></a>
## Fourteen-date product policy adjustment (2026-09-22)

The user superseded the15-date proposal with14 selectable dates including today:
start >= today,end <= today+13,inclusive duration1..10. The prior London probe is unchanged.
Its farthest requested day had null fields, motivating a conservative product choice, not a
claim that Open-Meteo supports only14 days, that15 days always fail, or that14 guarantees coverage.
Official maximum horizon, product admission and actual field coverage are distinct.

Only the shared window constant, boundary tests and current wording change. The frontend still
reads authoritative server limits. Duration, K20, budgets, Weather request/normalization, RAG,
roles, diagnostics, Nearby and no-retry policy remain unchanged. The earlier Sydney live proposal
is superseded by one frozen Tokyo ten-day request (today+4..today+13) for V0/V1/V2 sequentially,
conditional on offline checks. Actual execution outcomes will be recorded separately below;
this policy approval is not live acceptance. Same-day remaining hours remain unsupported.


## Tokyo fourteen-date integrated follow-up (2026-09-22)

V1 and the authorized V2 rerun obtained all5 fields on all10 dates Sep26-Oct5; raw/normalized/planner
values matched. This closes the specific integrated-live coverage gap, not historical London nulls
or Google404s, and guarantees no future completeness. Initial V2 had a capture-factory TypeError
before DB initialization; the user-authorized rerun corrected only the invocation. Both are retained.
See [execution evidence](development_record.md#tokyo-weather-window-live-20260922).

Still open: V1/final V2 default-target misses on3/1 days,3/6 cross-day repetitions, unknown costs,
visitor access and same-complex Nearby overlap. One Profile ValueError degraded locally in each.
Web was not triggered and gained no new live coverage. SQL execute21.58/0.86s is not a controlled
comparison. Cancellation, Weather partial/failure live and repair were not forced. No automatic
budget change, rerun or V3 implementation follows these observations.

The [Profile closeout review](development_record.md#weather-date-closeout-profile-20260922)
resolved the cause classification: both models returned review_count_used=0 for one supplied
review, while summary/signals were empty. Shared validation correctly rejected the count mismatch;
unavailable was accurate and no valid returned Profile signal was lost. This is not an outstanding
confirmed shared correctness defect. No retries, prompt changes or code changes were introduced.
The user's clarification that the first V2 database was stopped is recorded separately from the
observed pre-connection factory TypeError; no database repair task remains in this closeout.
