# Independent opening and route compliance

Current implemented Tickets 06-07 contract, reconciled 2026-10-03. These are offline
preparation/parsing/scoring rules, not a live collection client or formal experiment.
Shared [artifact/time](0001-evaluation-artifacts.md), [identity/snapshot](0002-intake-identity-usage.md)
and [occupancy](0003-requirement-schedule.md#occupancy) contracts retain their ownership.
The evaluator applies its emitted frozen rules rather than reading moving planner thresholds.

<a id="rtpeval-opening-contract"></a>
<a id="rtpeval-opening-contract--opening-evaluator-contract"></a>
<a id="rtpeval-opening-contract--inputs-and-independence"></a>
<a id="rtpeval-opening-contract--code-informed-evidence-boundary"></a>
<a id="rtpeval-opening-contract--proposed-processing-order"></a>
<a id="rtpeval-opening-contract--interval-and-timezone-semantics"></a>
<a id="rtpeval-opening-contract--evidence-states-and-metrics"></a>
<a id="rtpeval-opening-contract--accepted-decisions"></a>
<a id="rtpeval-opening-contract--documentation-examples"></a>
<a id="rtpeval-opening-contract--future-checks"></a>
<a id="rtpeval-opening-contract--special-date-clarification-example"></a>
<a id="rtpeval-opening-contract--required-unknown-explanation"></a>
<a id="rtpeval-opening-contract--ticket-06-preflight-clarification--2026-10-02"></a>
<a id="rtpeval-opening-contract--ticket-06-offline-implementation-wire--2026-10-02"></a>
<a id="opening-routes"></a>
<a id="opening-evaluator-contract"></a>

<a id="opening"></a>

## Opening scope, evidence and verdicts

An independently resolved primary place visit and independently interpretable interval are
the units. Nearby and unresolved role populations retain their separate scope diagnostics.
RequirementSpec has no entry/exterior distinction: prose cannot create an opening exemption.
Planner-selected hours or V3 findings are not ground truth. Zero grace applies to full-visit
containment; touching closing time is allowed and a lunch closure is not bridged.

`--paired` includes available V3 draft
and final_primary projections independently, with the same paired snapshot scope.
No Repair delta or route verdict is calculated. Library entry:
`score_opening(intake, identity_report, snapshot_directory, schedule_context=None,
*, paired=False, expected_plan=None)` returns immutable `OpeningResult`.
Schema: `rtpeval_opening_report_1`; rules: `rtpeval_opening_rules_1`.

Exit 0 means complete processing, including visit FAIL/UNKNOWN; exit 2 means material
correction or identity replay. JSON is printed to stdout. Preparation file hashes,
canonical intake/identity/context/rule hashes, snapshot manifest hash and expected/
actual plan hashes remain auditable. Submitted bytes are never rewritten. Save the
report outside its source artifacts. CLI constructs no provider/model/database client.

Whole-batch source/policy validation precedes scoring. Source corruption, stale phase/
paired scope or incomplete request linkage returns no partial cohort. Identity policy,
references, review/audit metadata and source mismatch requires identity replay.
Valid but failed observations and missing/malformed hours produce visit UNKNOWN.
Mixed snapshots keep supplied route contexts and verify their linkage without choosing
routes. Optional trusted full-plan equality includes those routes; canonical opening
references/details are checked even without that optional plan.

One check is emitted per primary occurrence. Repeated canonical places remain repeated
checks; Nearby and requirement-subject-only records add no visit. Nonapplicable
activities and unresolved roles retain source/reason records. Applicable counts are
known occurrences; `applicable_denominator` is null while roles are unresolved.
Full-scope percentages, including conditional compliance, are then unavailable.
`counts` covers primary checks; nonapplicable records carry their own N/A/UNKNOWN states.
Empty applicable scope has state N/A and unavailable rates, never 100 percent.

Every check records original start/end, normalized UTC interval, declared date, source,
canonical identity, independent timezone/origin, provider timezone version when supplied,
actual installed zone-file hash/basis, selected details attempts/raw hashes, reasons and
explanation. Clock evaluability and identity availability are separate. Explicit offset/
date contradictions, naive DST folds/gaps and precision beyond six fractional digits
remain UNKNOWN. `allow_cross_date=True` is opening's explicit opt-in; Ticket 05's
same-date time behavior remains unchanged. Reversed same-date clocks are never repaired.

Opening uses original raw `currentOpeningHours` and `regularOpeningHours`. It retains
field presence, weekly/dated endpoint meaning and literal truncation. Optional endpoint
day/hour/minute require actual integer values; absence is not zero. Explicit applicable
`periods: []` means closed, while missing/null/invalid values remain unavailable.
Regular Sunday 00:00/no-close is the documented always-open sentinel; arbitrary current
missing-close periods do not imply continuous access. Split periods retain lunch gaps;
overnight and previous-day contributions and weekly rollover are supported.

Current applicability uses the selected attempt's place-local request date plus six
calendar dates. Post-trip current hours cannot become historical evidence. Applicable
current defects block regular substitution; eligible outside dates use weaker regular
fallback. Known special dates lacking usable applicable current evidence remain UNKNOWN
with the exceptional-hours explanation. Collection crossing local midnight retains
uncertainty, while consistent literal dated spans may still prove opening. A truncated
23:59 close does not invent closure or opening in the final minute. Each date segment
records `selected_basis` and factual `basis`; unusable evidence has basis unavailable.
A visit's factual basis is current, regular, mixed or unavailable.

Half-open containment has zero grace: ending at close can PASS; any positive known
closure overlap yields FAIL even with other unknown time. Partial valid spans may prove
PASS containment but cannot establish a closed complement without bounded completeness.
Verdict, complete/partial/missing evidence, clock/identity availability and basis counts
are separate. Conditional compliance is PASS/(PASS+FAIL), including partial FAIL;
complete-evidence coverage and verdict-decidable coverage use the applicable population.
Two PASS plus one partial FAIL gives compliance 2/3, complete coverage 2/3 and decisive
coverage 1 when the first two visits are complete.

`outside_seconds` is exact only when all time is known; otherwise null.
`confirmed_outside_lower_bound_seconds`, `known_open_seconds`, `unknown_seconds` and
open/closed/unknown segment intervals preserve what is established. Missing visit
magnitude stays null; known zero stays zero. Integer microsecond interval measurement
prevents floating subtraction from hiding a fractional conflict. Duration summaries
are labelled observed per-visit subtotals with observed/missing counts; they do not
claim complete full-batch magnitudes or a global-time union.

[Acceptance](../records/evaluation/opening.md#rtpeval-ticket-06-acceptance) records the actual development
failures, corrections, retests and review. [Preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18#issuecomment-5955697757)
retains the approved decisions and original inspection checkpoint. Opening fixtures are
offline/synthetic; separately authorized local database/native checks are recorded in
acceptance and acquire no provider evidence. No provider availability, future factual certainty or booking/access
claim follows from this implementation. V0-V3 planner paths remain unchanged.

<a id="rtpeval-route-contract"></a>
<a id="rtpeval-route-contract--leg-records-and-adjacency"></a>
<a id="rtpeval-route-contract--accepted-mode-and-buffer-decisions"></a>
<a id="rtpeval-route-contract--corrected-meaning-of-the-users-route-window"></a>
<a id="leg-records-and-adjacency"></a>
<a id="accepted-mode-and-buffer-decisions"></a>
<a id="corrected-meaning-of-the-users-route-window"></a>

<a id="route-wire"></a>

## Route preparation and wire

`prepare_routes(intake, identity_report, schedule_context=None, occupancy_reviews=None,
route_reviews=None, coordinate_evidence=None, *, paired=False)` returns immutable
`RoutePreparation`. `score_routes` additionally takes a snapshot directory and optional
`expected_plan`, returning immutable `RouteResult`. `to_dict()` exports independent copies.
Schemas are `rtpeval_route_preparation_1`, `rtpeval_route_report_1`; rules are
`rtpeval_route_rules_1`. Preparation selects sources/intervals before observing route results
and emits both `route_contexts` and a complete Ticket 04 evidence plan. No provider is called.

Reuse existing rtpeval_schedule_context_1 and rtpeval_occupancy_reviews_1 unchanged.
Source/obligation/occupancy validators were moved to private _schedule_preparation.py
without Ticket 05 policy changes. No new executable RequirementSpec kind was added.

rtpeval_route_reviews_1 requires batch_id, nonempty revision and groups. Each unique
group links group_id/input_sha256 with reviewer_ref and offset-aware reviewed_at:

- status unrestricted explicitly reviews the absence of hard mode constraints;
  no policies are supplied. Missing review is UNKNOWN, never guessed unrestricted.
- status restricted requires nonempty policies, each with unique policy_id, original
  Input source_refs, nonempty allowed_modes subset of WALK/TRANSIT/DRIVE, and scope
  whole_trip or specified_dates. The latter requires unique inclusive-request dates;
  whole_trip has no dates. Empty intersections require correction.
- status unresolved requires reason, with source_refs where available.

Optional stated_mode is `{"mode": "WALK", "source_refs": [...]}`: an independently
reviewed exact original-input mode, distinct from a soft preference or allowed set.
It supplies mode only if no usable itinerary mode fixes one and conflicting claims
are not hidden. Missing Transfer remains missing in claim coverage. Hard restrictions
need policy records; query defaults do not invent them. Source references reuse exact
field/quote/occurrence/Unicode-offset validation. Extraction/review is supplied external
preparation; the evaluator does not parse unrestricted prose or run an LLM.

rtpeval_route_coordinates_1 requires batch_id, nonempty revision and records. Each
unique adopted canonical place_id record has latitude/longitude (strict finite numeric
values in range), lowercase 64-hex evidence_sha256, independent source_ref, reviewer_ref
and offset-aware reviewed_at. Never borrow planner locations. This supplied review is
a trust boundary: the hash links evidence, but the evaluator does not certify coordinate
facts or acquire the referenced source. Exact coordinate/hash correspondence gates
query applicability. Missing coordinates retain pending contexts and UNKNOWN.

Optional mode_options maps modes to `{"time_basis": ..., "routing_options": {...}}`.
Defaults deliberately use time_independent WALK, time_independent DRIVE with explicit
TRAFFIC_UNAWARE, and explicit_departure TRANSIT. Explicit queries use the adopted
departure; time-independent queries use null departure and retain the estimate label
and acquisition timestamp, without claiming historical query support. Ticket 04 wire
validation and Ticket 07 provider/mode applicability are distinct: supported preferences,
modifiers/locales and exact departure are checked when interpreting frozen evidence.
Unsupported valid-wire context stays UNKNOWN without shifting dates or modes.

<a id="rtpeval-route-contract--route-evaluator-contract--draft"></a>
<a id="rtpeval-route-contract--purpose-and-inputs"></a>
<a id="rtpeval-route-contract--checked-repository-contracts"></a>
<a id="rtpeval-route-contract--departure-and-feasibility-semantics"></a>
<a id="rtpeval-route-contract--evidence-and-result-states"></a>
<a id="rtpeval-route-contract--explanatory-examples"></a>
<a id="rtpeval-route-contract--future-verification"></a>
<a id="rtpeval-route-contract--accepted-five-minute-route-tolerance"></a>
<a id="rtpeval-route-contract--provider-fallback-clarification--official-documentation-checked"></a>
<a id="rtpeval-route-contract--returned-route-evidence-policy-accepted--2026-09-28"></a>
<a id="rtpeval-route-contract--accepted-default-departure-selection--2026-10-02"></a>
<a id="rtpeval-route-contract--accepted-hard-protection-boundary--2026-10-02"></a>
<a id="rtpeval-route-contract--accepted-decisive-failure-and-technical-preflight-closure--2026-10-02"></a>
<a id="rtpeval-route-contract--executable-offline-route-checkpoint--2026-10-02"></a>
<a id="route-evaluator-contract"></a>
<a id="departure-and-feasibility-semantics"></a>
<a id="accepted-five-minute-route-tolerance"></a>
<a id="provider-fallback-clarification--official-documentation-checked"></a>
<a id="returned-route-evidence-policy-accepted--2026-09-28"></a>
<a id="accepted-default-departure-selection--2026-10-02"></a>
<a id="executable-offline-route-checkpoint--2026-10-02"></a>

<a id="route-verdicts"></a>

## Route selection, applicability and scoring

Keep consecutive primary occurrences within each delivered day; no inter-day routes.
Confirmed same-canonical legs are N/A; distinct venues at one address remain distinct.
V0 uses Activity claims, V1-V3 Transfers without ignored-Activity fallback. Duplicate
claims keep all sources but one leg. Conflicting Transfer or segmented/mixed Activity
journeys never become a favorable uninterrupted single-mode matrix claim.

Subtract applicable scheduled_commitments protections and fixed other occupancy from
the endpoint gap, excluding this leg's own transport. Preserve original obligation IDs
and scopes through blocker union. primary_visits-only protection does not block traffic.
Possibly overlapping unknown occupancy stays uncertain; known disjoint alternatives do
not contaminate unrelated routes. A guaranteed common occupation starting at the deadline
is a hard boundary; a merely possible deadline occupation stays UNKNOWN and cannot borrow
next-visit tolerance. Explicit departure controls and must fit one free span.
Otherwise choose the longest continuous fragment, tie earliest UTC start, before route
observations. Never concatenate spans, try a later fragment after failure or switch mode.

For provider duration d, reserve r and selected G, retain raw deficit max(0,d+r-G).
Hard protection/fixed-commitment deadlines require d+r <= G with zero grace; only the
next-visit deadline permits 300 seconds. DRIVE reserve is 600 seconds once, others zero.
Separate caps are WALK/TRANSIT 2700+300 seconds, DRIVE 1800+300 seconds, and WALK distance
<=3000 meters with no distance tolerance. Tolerances never sum. Exact and within-tolerance
PASS are labelled. Shared rule constants drive arithmetic and the emitted rules/hash.

Verify raw replay and full identity/occurrence/request reconstruction before scoring.
Corruption, foreign/unused linkage or wrong paired scope returns no partial cohort.
Valid wrong mode/departure/coordinates/options is inapplicable UNKNOWN evidence;
optional trusted plan additionally enforces exact acquisition-plan equality.
Historical non-TRANSIT explicit query is unsupported relative to acquisition; TRANSIT
and time-sensitive DRIVE need applicable explicit departure. No Compute Routes transit
horizon is copied into matrix policy. Query/itinerary clocks support six fractional
digits; provider durations preserve integer nanoseconds, without float rounding.

Parse raw status/condition independently of the available summary. Require a status
object: omitted code within it means default zero, malformed/error status stays UNKNOWN.
Successful ROUTE_NOT_FOUND FAILs with null duration/deficit; contradictory route fields
invalidate that observation. ROUTE_EXISTS uses nonnegative duration strings with up to
nine fractional digits, never staticDuration or rounded seconds. Missing WALK distance
or duration keeps its component UNKNOWN. Valid returned traffic fallback is accepted
and traced. Any independently proven component FAIL decides the leg; all required
components must PASS for combined PASS, otherwise UNKNOWN.

Report source claims/mode basis, selected fragment and deadline, component reasons and
classification, exact measurements, nominal caps/tolerances/reserve, expected/actual
query, raw attempts/hashes and preparation/source/rule/plan/manifest hashes. Structural,
applicable response, full-component, decisive and duration-available coverage differ.
No-route is decisive without duration; partial FAIL enters P/(P+F) without becoming
complete evidence. Unknown is null travel, never zero. Unresolved role/adjacency
populations and empty denominators suppress full-scope rates.

Daily/request sum, median and maximum are observed per-occurrence subtotals with missing
and unresolved counts; reserve is separate. Request deduplication never merges score
occurrences. Unknown potential legs prevent complete burden claims globally and on the
affected days. No route/overlap double weighting, auxiliary arithmetic, V3 repair delta
or formal comparison is calculated. Synthetic development tests do not establish real
provider availability, historical/future travel certainty or benchmark outcomes.



Nominal caps are independently applied product references, not planner verification verdicts.
The 300-second evaluation tolerance does not change planner thresholds or guarantee provider
error bounds. WALK's 2-km and motor 5-km geographic discovery filters are not provider route
distance caps. Only WALK has the 3-km observed-distance cap in this rule profile. A valid route
can exceed a cap and still count as observed evidence. Traffic fallback changes calculation
strategy, not the requested mode, and creates no independent traffic-fidelity score.

For example, TRANSIT duration 49 minutes passes the nominal 45+5 cap; in a 44-minute ordinary
next-visit gap it also passes the separate five-minute schedule tolerance, but in a 43-minute
gap schedule FAIL is decisive. A protection ending the same fragment permits no grace.
DRIVE duration 20 plus reserve 10 needs 30 minutes; the reserve is not added to provider burden.
These are rule illustrations, not measured provider outcomes or benchmark cases.

<a id="inputs-and-independence"></a>
<a id="code-informed-evidence-boundary"></a>
<a id="proposed-processing-order"></a>
<a id="interval-and-timezone-semantics"></a>
<a id="evidence-states-and-metrics"></a>
<a id="accepted-decisions"></a>
<a id="documentation-examples"></a>
<a id="future-checks"></a>
<a id="special-date-clarification-example"></a>
<a id="required-unknown-explanation"></a>
<a id="ticket-06-preflight-clarification--2026-10-02"></a>
<a id="ticket-06-offline-implementation-wire--2026-10-02"></a>
<a id="purpose-and-inputs"></a>
<a id="checked-repository-contracts"></a>
<a id="evidence-and-result-states"></a>
<a id="explanatory-examples"></a>
<a id="future-verification"></a>
<a id="accepted-hard-protection-boundary--2026-10-02"></a>
<a id="accepted-decisive-failure-and-technical-preflight-closure--2026-10-02"></a>

<a id="history"></a>

## Commands, code and decision history

Code owners: [opening](../../backend/evaluation/opening.py),
[routes](../../backend/evaluation/routes.py) and
[route preparation](../../backend/evaluation/_route_preparation.py).
[Package commands](../../backend/evaluation/README.md) own invocation/exit codes.
Opening [preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18#issuecomment-5955697757)
and [acceptance](../records/evaluation/opening.md#rtpeval-ticket-06-acceptance), route
[preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19#issuecomment-5955699412)
and [acceptance](../records/evaluation/routes.md#rtpeval-ticket-07-acceptance) preserve decisions,
failed checks, corrections and executed validation. Historical immediate-departure, universal
schedule grace and partial-verdict proposals are superseded by the current rules above.
