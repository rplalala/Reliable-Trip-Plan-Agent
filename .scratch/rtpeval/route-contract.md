# Route evaluator contract — draft

Current follow-up, 2026-10-02: the user authorized
[Ticket 07 specification/interface preflight](ticket-07-preflight.md). Existing
projection, occupancy, raw snapshot and time interfaces are checked; 59 existing seam
tests passed. The user selected waiting and the longest continuous interval when departure is
unstated (Q1); this supersedes the historical A.end default. Protection-boundary
tolerance is now Accepted as zero grace at non-travel protection (Q2); Q3 is Accepted: any proven distance/time failure is decisive even with another
UNKNOWN component. The consolidated offline interface proposal is specification-ready
for implementation scope approval; no route code exists yet. Issue #19 remains
open/ready-for-agent; implementation approval remains pending. Historical accepted caps/reserve/tolerances below remain in force;
no route implementation or live acquisition is claimed.

Historical status (2026-09-28): Accepted independence/coverage principles consolidated; stated-mode policy, product DRIVE reserve of 10 minutes and zero additional evaluator buffer accepted; five-minute tolerance applies separately to duration caps and schedule feasibility. Detailed adjacency and provider applicability remained OPEN at that checkpoint. No implementation, live queries or experiments.
Date: 2026-09-28.
Source checkpoint: 8a435e2db0198e4fc8928b85e333b45b66c0c981 with uncommitted evaluation documentation.

## Purpose and inputs

For transitions in the submitted itinerary, determine whether the available continuous travel interval can accommodate the adopted independent route evidence. This evaluates consistency with the frozen route snapshot, not a guarantee of actual arrival. Read itinerary activities/transfers, reviewed RequirementSpec, independent identities and snapshot, and EvaluationRules. Planner transfer validation_state, reserve_seconds and V3 findings are not ground truth.

Benchmark construction already selected groups; Evaluation neither reruns planners nor rechecks their workflow completion. Snapshot acquisition happens after the user's batch handoff. Preserve planner-to-oracle lag and the historical/future applicability of route observations. If the service cannot answer the planned departure date, do not silently shift the date to obtain a PASS.

## Checked repository contracts

- Activity contains timed roles and text but no universal structured per-leg mode. V0 transport can be a model-generated activity; Transfer has from/to activity IDs, canonical IDs, WALK/TRANSIT/DRIVE mode, departure/arrival, claimed duration/distance, reserve, evidence refs and validation state.
- RouteMatrixRequest accepts origins/destinations with canonical labels and coordinates, a travel_mode string, optional routing_preference, one timezone-aware departure_time and a field mask. The current adapter sends coordinates as waypoints, not place IDs. Preserve queried coordinates and independently resolved endpoints together.
- One matrix call shares mode, preference and departure across its elements. Legs with incompatible departure contexts cannot be batched merely because they share venues.
- The adapter returns raw dictionary elements and timestamps. Requested fields include duration, staticDuration, fallbackInfo, distanceMeters, status and condition. It can filter malformed entries; a missing element must remain distinguishable from a confirmed no-route condition.
- Existing normalization accepts status={} as success, requires ROUTE_EXISTS and a valid duration for availability, and rounds fractional nonnegative durations upward to whole seconds. These are code facts to check against primary provider semantics and independent fixtures before adoption, not an instruction to import planner compliance logic.
- Existing evidence distinguishes provider_observed, mirrored_reverse_estimate and not_observed. Reverse-derived duration cannot be treated as an independently queried directed leg. Matrix-level availability alone does not establish that every required leg is covered.

Additional inspection findings: current normalization can label a ROUTE_NOT_FOUND element as invalid_or_missing_duration because of reason precedence; classify raw status and condition independently rather than trusting that summary. Require a unique matching element per requested leg: the ordinary matrix availability calculation does not itself detect every omitted element. The adapter has no step/waiting breakdown. Activity and Transfer timestamps can be naive. Planner baseline evidence may use a representative first-day noon departure, which cannot substitute for arbitrary planned transit departures. Upstream intent vocabulary includes BICYCLE while final Transfer only permits WALK/TRANSIT/DRIVE; unsupported-mode treatment must remain explicit.

## Leg records and adjacency

A route check retains group/run, source and destination activity IDs, date, original claimed mode/departure, independently resolved endpoints, evidence key, candidate continuous interval, and any blockers. Preserve association conflicts rather than correcting planner artifacts. An adjudicated name may determine independent endpoints despite a wrong planner ID, with the conflict still reported separately.

Same-day consecutive main visits form the transition candidates. Generic no-POI activities are free-time/transition-like, not extra unknown-location endpoints. Preserve reviewed protected time and concrete named visits. Reconcile explicit transport with its corresponding leg without counting it twice; uncertain correspondence must be reported.

Do not count an explicit transport activity and its main-visit connection as two trips. The transport slot can describe the same leg and its reserved interval. Conversely, do not silently consume an occupied activity to enlarge the gap. Do not concatenate disjoint intervals around a fixed commitment.

Inter-day transitions are outside v1 route scoring, matching current per-day product binding and the absence of accommodation planning. Do not create a last-POI-to-next-day-first-POI leg. Consecutive visits at the same independently confirmed canonical venue are route N/A with a reason, not an observed zero-duration PASS; retain visit occurrences for other checks. Distinct IDs at the same address are not automatically the same venue.

## Departure and feasibility semantics

For a defined continuous interval [t_depart, t_deadline], independent provider duration d, frozen product reserve r (600 seconds for DRIVE; zero for WALK/TRANSIT), and zero additional evaluator buffer, record raw deficit max(0, t_depart + d + r - t_deadline). Under the accepted five-minute Routes tolerance, schedule feasibility passes when that deficit is <=300 seconds. Preserve a positive raw deficit even when it is within tolerance. Retain precision and the adopted duration basis; rounding for display must not alter the verdict.

For a simple A-ending/B-starting gap with no blockers or separately fixed departure, the proposed departure is A.end and the deadline is B.start. A valid explicit departure can narrow the available interval; it must not precede the source visit end or ignore protected occupancy. Transit/time-sensitive DRIVE evidence must correspond to the adopted departure semantics, not a city-wide representative departure. Provider time support and invalid temporal context follow evidence-time-contract.md; no silent date shifting or additional date tolerance is introduced.

Do not search arbitrary later departures until a feasible route appears. If a rule later permits waiting/departure search, its range, cost and accounting must be fixed before scoring. Preserve any provider-included waiting; do not blindly add waiting twice. If waiting is not represented or its semantics are unknown, do not invent it or certify a mismatched departure. A common snapshot is keyed by direction, endpoints, mode, departure context and settings, not just the unordered pair of venues.

## Evidence and result states

Separate structural evaluability, applicable-route evidence coverage and feasibility among adjudicable legs. Each UNKNOWN includes a specific reason, leg identifiers, mode/departure context and evidence references.

- Provider failure, missing/invalid status, invalid/negative/missing duration, malformed/missing matrix element, uncertain identity, ambiguous mode or unsupported temporal context do not become zero travel time or confirmed temporal conflicts.
- Accepted: an explicit no-route response is FAIL when the query succeeded and independently verified endpoints, direction, mode and departure context apply to the planned leg. Report a context-specific route violation, not universal physical impossibility. Do not manufacture duration/deficit seconds or switch modes to turn it into PASS. Service failure, timeout and incomplete data remain UNKNOWN with reasons. Include confirmed no-route cases in route-compliance outcomes; numerical duration-deficit reporting remains unavailable for those cases.
- Preserve fallbackInfo and staticDuration. Use a valid returned duration, including traffic-calculation fallback, under the accepted simplified evidence policy. Do not substitute staticDuration when duration is absent or invent a usable route from an error. No separate traffic-fidelity verdict is required.
- Partial coverage yields observed transfer-duration subtotal, observed maximum and explicit observed-leg count/denominator, not a complete daily travel burden. Never fill unknown legs with zero. Daily sums and medians must disclose evidence and mode basis.
- Record route deficits separately from overlap; they can describe the same underlying timing problem and must not be silently double-weighted in an auxiliary score.

## Accepted mode and buffer decisions

1. Accepted mode policy: assess the itinerary's explicitly stated mode for a leg, honoring the reviewed request restriction. V0 text can supply an unambiguous mode; structured V1-V3 fields are evidence of a claim, not automatically correct. Conflicts go to a documented clarification/adjudication path. If neither request nor itinerary fixes a usable mode, record UNKNOWN with a missing-mode reason rather than silently assuming WALK or choosing the fastest alternative. Exact extraction and cross-leg preference scope remain to be specified.
2. Accepted reserve policy (supersedes earlier exclusion of the product reserve): retain the product's 10-minute DRIVE access/pickup/drop-off allowance for every version; WALK and TRANSIT have no such allowance. Add no further evaluator buffer; the subsequently accepted five-minute tolerance is a separate classification allowance, not additional duration. Keep independent provider duration and product reserve separately reported. DRIVE's <=30-minute threshold applies to provider driving duration; interval occupancy uses provider duration plus 10 minutes. Do not double-count a reserve already reflected in the planner's displayed arrival time: compare the independently calculated duration-plus-reserve against the available interval once. This is product-rule compliance, not a claim that Google measured the reserve.

## Explanatory examples

A ends 10:00, B begins 10:20, independently observed WALK duration is 25 minutes: a raw five-minute deficit, which passes at the accepted tolerance boundary. A 20-minute duration exactly fits without using tolerance. Failed acquisition is UNKNOWN with its reason, not a 20-minute surplus.

A ends 10:00, B starts 11:00, a fixed commitment occupies 10:20-10:40: the two 20-minute gaps do not automatically provide one 40-minute continuous route slot. Commitment location and itinerary semantics must be resolved before claiming a 30-minute transfer fits.

These are documentation examples, not formal cases or provider observations.

## Future verification

Check directed endpoints, mode/departure mismatch, exact boundary and positive deficit, fractional duration precision, zero versus missing duration, successful empty status encoding, invalid/error/missing status, no-route condition, fallback/static basis, missing matrix elements, reversed estimates, blockers, explicit transport deduplication, same-venue and overnight applicability, snapshot replay and separation from V3 findings. No code, fixtures or tests were created or run.


## Corrected meaning of the user's route window

The user clarified that "window" means per-mode route distance/duration thresholds, not the continuous gap between activities. The earlier attribution of gap semantics to that user request was mistaken and is superseded here. Continuous travel availability remains a separate feasibility concept.

Checked current defaults in config/runtime.yaml and the shared initial_routes usable check:

| Mode | Product route threshold |
| --- | --- |
| WALK | Provider route distance <= 3 km AND provider duration <= 45 minutes |
| TRANSIT | Applicable provider total duration <= 45 minutes |
| DRIVE | Provider driving duration <= 30 minutes |

These are product transfer-burden/selection thresholds, not proof that a scheduled gap is sufficient. The user proposed using these values as the evaluation reference. Record exceedances against these independently applied thresholds separately from schedule deficit. Do not discard an over-threshold observed route from evidence coverage merely because it exceeds the product threshold. Explicit-mode queries remain the adopted policy; the thresholds do not authorize switching modes until a passing alternative is found.

The product uses drive_reserve_minutes=10; the user now accepts this reserve in Evaluation, with no additional evaluator buffer. walk_radius_km=2 and motor_radius_km=5 are discovery/no-route geographic filters, not observed route-distance limits. Transit and driving have no corresponding per-leg kilometre cap in the checked usable test. These are current defaults, not a frozen final configuration; capture the agreed evaluation values rather than reading a moving planner configuration during scoring.

Exact threshold-rate aggregation and auxiliary-score contribution remain OPEN. Sharing explicitly accepted product thresholds is distinct from reusing planner validation verdicts. The example of a 30-minute route in a 20-minute itinerary gap remains a 10-minute timing deficit even when that route is within its mode's product threshold.


Example under the accepted rule: provider DRIVE duration 20 minutes and an available 25-minute interval yield required occupancy 30 minutes and a raw five-minute deficit, classified as within the accepted schedule tolerance. Provider duration remains 20 minutes in observed-route totals; the 10-minute product allowance is separately labelled.


## Accepted five-minute route tolerance

The user accepts a tolerance of 300 seconds for BOTH product duration-cap compliance and scheduled-time feasibility, uniformly across versions. The two checks are separate; never add them into a ten-minute allowance.

Let d be independent provider duration, L the product mode duration cap, r the product reserve (600 seconds for DRIVE; zero for WALK/TRANSIT), and G the applicable continuous available interval at departure.

- Duration-cap compliance: d <= L + 300 seconds. WALK still also requires provider route distance <=3 km; there is no added distance tolerance. Effective time boundaries are WALK/TRANSIT 50 minutes and DRIVE 35 minutes, with nominal caps still reported as 45/45/30 minutes.
- Schedule feasibility: d + r <= G + 300 seconds. Record raw deficit max(0, d + r - G), even when it passes within tolerance.
- If a combined route-compliance result is later specified, both applicable checks must pass. Passing one does not waive the other. Exact combined aggregation remains OPEN.
- Preserve nominal limits, provider duration, product reserve, available time, raw threshold overrun, raw schedule deficit, tolerance and each verdict. Distinguish exact compliance from compliance within tolerance in report explanations.

Example: TRANSIT duration 49 minutes is four minutes beyond the nominal 45-minute cap and passes that check. If the itinerary allows 44 minutes, its raw five-minute deficit also passes. If it allows 43 minutes, its six-minute deficit fails even though the mode cap check passes. These allowances are evaluated separately, not summed.

This is a chosen evaluation allowance for observation-time variation, not a measured guarantee that provider error is bounded by five minutes. It does not change Opening's zero-grace rule, WALK's distance threshold, the DRIVE product reserve, or an explicit no-route FAIL. Missing/inapplicable evidence remains UNKNOWN, regardless of tolerance. No planner algorithm or runtime threshold is changed by this evaluation decision.


## Provider fallback clarification — official documentation checked

Google's FallbackInfo identifies a deviation from the requested routing preference, with actual fallback routingMode such as FALLBACK_TRAFFIC_UNAWARE or FALLBACK_TRAFFIC_AWARE and reasons including SERVER_ERROR or LATENCY_EXCEEDED. These describe traffic-calculation strategy, not automatic replacement of requested DRIVE with TRANSIT or WALK. A well-formed request with explicit travelMode/departure can therefore receive a fallback calculation; its occurrence/rate in this project's runs has not been established.

Source: [Google Routes FallbackInfo](https://developers.google.com/maps/documentation/routes/reference/rest/v2/FallbackInfo). Checked by reading public documentation, not invoking the route API. The user subsequently accepts using valid returned route durations, including traffic-calculation fallback; the earlier incompatible-traffic-context UNKNOWN proposal is superseded.

The latest user decision supersedes excluding generic no-POI activities from benchmark delivery: treat such items as free_time/transition-like for evaluation, without counting them as primary visits or inventing a venue. Preserve the original output role/text and record the evaluation classification. This does not erase explicit user-protected time or reclassify a concretely named but unresolved POI as free time. Ordinary no-POI placeholders alone do not disqualify a group.


## Returned-route evidence policy accepted — 2026-09-28

Accepted simplification: use the valid route duration returned by Google for the queried endpoints, direction and stated travel mode, including a fallback traffic-calculation result. Do not classify a valid result UNKNOWN solely because traffic awareness differs from the requested routing preference. Preserve requested/returned context and fallbackInfo for traceability, without adding a separate traffic-fidelity score or promising future road conditions. Do not silently switch endpoints, direction, travel mode or query date. Explicit no-route remains FAIL; provider failure, invalid status or no usable duration remains UNKNOWN. Existing duration thresholds, DRIVE product reserve and five-minute tolerances remain unchanged.

Per-element status/duration parsing and temporal context follow [evidence-time-contract.md](evidence-time-contract.md). Public documentation verification is separate from future parser tests and does not imply real API execution.


## Accepted default departure selection — 2026-10-02

The user chose waiting and the longest continuous free interval when the submitted
itinerary does not state an authoritative departure. Select the interval from independent
itinerary occupancy/protections before using route evidence; departure is its start.
Do not concatenate intervals, trial different provider departures until a route passes,
or switch modes. An explicitly stated departure is honored instead of choosing another
fragment. The former immediate A.end proposal is superseded for unstated departure.

Equal-longest ties use earliest UTC start. Unknown blockers or unresolved adjacency
remain uncertain. The Q2/Q3 decisions below subsequently resolved protected-boundary
tolerance and partial-evidence verdicts. This section records specification decisions;
the implementation checkpoint below records executable behavior.


## Accepted hard protection boundary — 2026-10-02

Applicable non-travel protections are hard boundaries with zero route grace. A selected
fragment ending at a scheduled_commitments protection or independently fixed commitment
must accommodate provider duration plus the DRIVE reserve before that boundary. No
300-second allowance crosses it. The separate 300-second schedule tolerance applies
only to the next scheduled visit deadline; mode duration-cap tolerance is unchanged.
primary_visits-only protection does not itself block traffic. This supersedes the
historical unqualified use of five-minute tolerance at every interval deadline.


## Accepted decisive failure and technical preflight closure — 2026-10-02

The user confirmed that distance or time beyond its applicable limit establishes FAIL,
even if another component is unavailable. Complete evidence and decisive outcome are
separate. Conditional compliance is P/(P+F), including such decisive FAIL; all required
components must pass for combined PASS, otherwise UNKNOWN. Applicable explicit no-route
retains FAIL without invented duration. Invalid/foreign context cannot prove a factual
component failure. These rules close the historical combined component/partial evidence
aggregation item for the Ticket 07 subset; auxiliary total remains Ticket 08.

The [preflight](ticket-07-preflight.md) defines longest-fragment deterministic selection
before route evidence, explicit departure authority, zero-grace hard boundaries,
source-linked request mode review, mode/provider/time applicability, exact raw precision,
public preparation/scorer/CLI proposals and separate coverage/burden measures. Historical
A.end default and universal interval-deadline tolerance are superseded by Q1/Q2. Existing
planner/RequirementSpec behavior is unchanged. At that preflight checkpoint the
specification was ready for scope approval; no implementation, live acquisition,
formal case or Git action had occurred. The user subsequently approved implementation.

## Executable offline route checkpoint — 2026-10-02

`prepare_routes`, `score_routes` and the local route CLI implement the approved subset;
see [acceptance](ticket-07-acceptance.md) for actual validation and review corrections,
and the [package guide](../../backend/evaluation/README.md#ticket-07-offline-same-day-routes)
for supplied review/coordinate wires and query defaults. Longest-fragment selection
precedes observations; explicit departure controls. V0 Activity/V1-V3 Transfer authority,
same-day occurrence scoring, source provenance and independent snapshot replay remain
binding. No real acquisition or planner policy change is introduced.

Fixed other occupancy and scheduled_commitments protection delimit zero-grace fragments.
All-known disjoint alternative occupancies are irrelevant to another route; a guaranteed
shared occupation at its deadline is a hard boundary. A merely possible boundary stays
UNKNOWN and cannot borrow 300 seconds. primary_visits-only protection does not block traffic.

Raw nanosecond duration, provider distance, single DRIVE reserve, nominal cap and separate
tolerances remain visible. Malformed or inapplicable evidence stays UNKNOWN; valid returned
fallback remains usable. Any independently proved component FAIL is decisive without
claiming all components known. No-route has null duration. Coverage and observed daily/trip
burden are separate, with missing and unresolved-population counts; no auxiliary total,
formal case/experiment, version comparison or freeze is included. Changes remain local,
uncommitted and unpublished at base 3427784b on feature/evaluation.
