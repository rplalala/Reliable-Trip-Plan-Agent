# Ticket 07 route specification and interface preflight

Date: 2026-10-02 (Australia/Sydney).
Revision: 3427784b87d5864aba25dcba8b48430ec4de9dac, feature/evaluation.
The tracked working tree was clean at entry. Status: factual interface audit complete;
Q1/Q2/Q3 accepted; specification/interface proposal subsequently approved for implementation. This document preserves the preflight checkpoint, not an
implemented or frozen route specification.

## Authority and authorization

The user requested Ticket 07 specification preflight after Ticket 06 local closeout.
[PROJECT](../../PROJECT.md) remains authority; [Issue #19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19)
owns live status. Issue #19 was open, needs-info, with no comments when inspected.
Its predecessor Ticket 04 completed the approved injected-transport/offline scope.
[Route](route-contract.md), [activity scope](activity-scope-contract.md),
[projection](intake-projection-contract.md), [snapshot](snapshot-contract.md),
[requirement/schedule](requirement-schedule-contract.md) and
[evidence/time](evidence-time-contract.md) retain their current responsibilities.

Authorized: current-code/primary-document inspection, bounded existing offline seam
regressions, proposed contracts and related documentation/archive/Issue updates.
Not authorized: route-scoring implementation, new formal cases, real API/model/database
runs, formal experiments, commits/push, branch switches or version freezes.

## Observed current interfaces

| Seam | Observed behavior | Ticket 07 consequence |
| --- | --- | --- |
| projection.mode_claim | Independent review or finite WALK/TRANSIT/DRIVE title/notes extraction; negated/conditional/multiple modes stay unresolved | Reuse claims; do not let a query context invent the submitted mode |
| Version-selected transport | V0 Activity claims; V1-V3 Transfer claims; ignored alternate sources have no fallback | Preserve source authority and missing-transfer uncertainty |
| Projection legs | Same delivered-day consecutive primary occurrences in a sorted view, source pointers retained; unresolved role/overlap can make adjacency unresolved | Keep occurrences, uncertainty and inter-day exclusion; no planner cache/validation truth |
| Transfer binding | Exact directed activity-ID pair; dangling/reversed/nonadjacent/cross-day claims remain diagnostics | Do not retarget a claim to a convenient candidate leg |
| occupancy.prepare_occupancy | Independent commitments, scoped merged protections, alternatives, unresolved candidates and coverage | Reuse time evidence, not route mode or verdicts; its complete occupancy may have mode=None |
| schedule_time.normalize_interval | Offset/independent-IANA UTC interpretation, half-open spans, microsecond clock precision, DST/date errors explicit | No host zone, date shifting or invented overnight end |
| snapshot.build_evidence_plan | Inventories every leg and canonical identity, missing contexts pending, context request keys directed and fully parameterized | Ticket 07 must determine mode/departure applicability before a route context is adopted |
| snapshot.load_snapshot | Raw paths/hashes, attempts/timestamps/coverage/ledger/summary replay and optional trusted-plan equality | Corruption is whole-material correction, not shrinking coverage |
| Route summary available | One JSON (0,0) element; status/condition/duration are preserved, not semantically validated | Parse raw element independently; available is not route PASS |
| opening mixed-plan validation | Rebuilds full evidence plan from supplied leg contexts and checks exact equality | Reuse the neutral invariant after approval; do not import opening verdict policy |

Evidence: backend/evaluation/projection.py:55,173,251,288,406,415;
occupancy.py:297,327,379; schedule_time.py:71,87,127;
snapshot.py:147,211,328,467,507,532,559; opening.py:47.
Line references identify this inspection revision, not future guaranteed positions.

The route snapshot context has leg_id plus source_kind=independent_evaluation_context,
mode, departure, time_basis, origin, destination and routing_options. Modes are
WALK/TRANSIT/DRIVE. explicit_departure is offset-aware; time_independent has null
query departure. Endpoints retain adopted canonical ID, coordinates and evidence hash.
The raw ISO departure is preserved, so applicability compares instants while retaining
original serialization. Options currently have a restricted key set but only broad
str/bool value checks; Ticket 07 still needs per-key and mode-specific interpretation.
An endpoint hash establishes linkage only, not factual coordinate authenticity.

## Accepted boundaries carried forward

- Same confirmed canonical venue is N/A, not a zero-duration observed PASS. Same-address
  different venues are not automatically identical. Do not create inter-day routes.
- Nearby does not add scheduled endpoints. Named unresolved visits remain candidates;
  locationless flexible time is slack only under existing independent occupancy rules.
- WALK nominal duration cap 2700 seconds and distance cap 3000 meters; TRANSIT duration
  cap 2700 seconds; DRIVE provider-duration cap 1800 seconds.
- Duration-cap tolerance is 300 seconds. Schedule-feasibility tolerance is separately
  300 seconds. DRIVE has exactly 600 seconds of product reserve; WALK/TRANSIT zero.
  Do not sum tolerances, enlarge WALK distance, add waiting twice or double-count reserve.
- Successful applicable explicit no-route is FAIL with no fabricated duration/deficit.
  Provider error/incomplete or inapplicable evidence remains UNKNOWN. Returned traffic
  fallback is accepted without switching modes or inventing duration from staticDuration.
- Frozen independent raw evidence determines verdicts. Planner validation_state,
  reserve_seconds, provider estimates and V3 findings are claims or diagnostics only.

## Historical first frontier: before Q1/Q2/Q3 answers

At this checkpoint all entries were Proposed. The user requested a clearer example for
Q1; no selection had yet been accepted and Q2/Q3 were unanswered. The accepted answers
and consolidated proposal below supersede this historical readiness gate.

| Decision | Proposed recommendation | Alternative and consequence |
| --- | --- | --- |
| Q1 default departure and continuous interval | Use explicit valid submitted departure, else A.end; inspect only its containing free fragment, no later search | With no explicit departure, deterministically select the longest fragment and depart at its start; this can pass a leg that fails immediate departure |
| Q2 tolerance at protected boundary | scheduled_commitments protections/fixed commitments stay hard; apply 300 seconds only at the next visit deadline | Apply 300 seconds at every selected interval deadline, potentially tolerating travel across a protected boundary |
| Q3 combined route result with partial evidence | Any independently proven component failure establishes FAIL; PASS requires all necessary components PASS; otherwise UNKNOWN | Require complete component evidence before a combined FAIL, turning some proven failures into UNKNOWN |

Q1 illustration: A ends 10:00, B starts 11:00, travel takes 30 minutes and protected
non-travel time is 10:10-10:20. Immediate departure has a ten-minute continuous fragment;
waiting until 10:20 supplies forty minutes. An explicit 10:00 departure is honored
under both proposals. These are synthetic explanatory times, not an acquired route,
formal case or benchmark result. The waiting proposal selects from itinerary intervals,
not by trying provider responses until one passes; tie behavior would need definition.

## Historical technical closure checklist

1. Separate submitted departure from provider query departure. A missing arrival does
   not manufacture an arrival or prove no route; each needed temporal field is assessed
   independently. Multiple distinct same-mode V0 segments are not automatically one
   uninterrupted route; mixed-mode segments cannot be scored as a single-mode matrix
   leg without pretending the original claim changed.
2. Honor protection scope: primary_visits-only does not itself block traffic. Fixed
   generic commitments and scheduled_commitments protections can restrict it. Unknown
   occupancy/protections/adjacency remain structural uncertainty; never sum fragments.
3. Assess a query mode against the authoritative claim and separately sourced request
   restrictions. Current Ticket 05 executable RequirementSpec handles only required,
   excluded, protected and fixed-visit obligations; no route-mode restriction wire is
   already implemented. Define independent, source-linked route policy metadata rather
   than silently changing Ticket 05 or parsing unrestricted prose while scoring.
4. Define explicit_departure applicability by adopted UTC instant and recorded local
   day; define deliberately time-independent WALK/basic DRIVE evidence separately.
   TRANSIT/time-sensitive DRIVE cannot silently borrow another departure. Unsupported
   historical context stays UNKNOWN and never shifts a date.
5. Validate routing_preference values and applicability, preserve allowed modifiers and
   requested/returned context. Unsupported combinations cannot be accepted merely
   because Ticket 04 allowed their broad value types.
6. Define raw status/condition/no-route parsing, Decimal nanosecond duration arithmetic,
   WALK distance completeness, component outcomes, and duration-available versus
   decisive/complete evidence coverage. Never ceil provider duration into a verdict.
7. Define candidate population, N/A counts, unresolved-population suppression, P/(P+F)
   conditional rates and observed daily/per-request transfer subtotals. Auxiliary total
   and cross-request comparisons remain Ticket 08/formal work, not this ticket.

## Primary provider documentation inspected

Checked on 2026-10-02 without a provider API call:

- [Compute Route Matrix reference](https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRouteMatrix):
  requested field mask must include status; status and route condition are distinct.
  ROUTE_NOT_FOUND has no duration/distance; durations preserve up to nine fractional
  digits. Omitted query departure uses request time; past explicit departure is allowed
  only for TRANSIT. routingPreference is restricted to DRIVE/TWO_WHEELER.
- [ProtoJSON](https://protobuf.dev/programming-guides/json/): absent implicit-presence
  scalar defaults differ from missing message presence; duration string parsing retains
  nanosecond precision. Existing snapshot extraction intentionally requires an explicit
  status object and strict (0,0) indices; preserve that boundary in this offline ticket.
- [Transit matrix guide](https://developers.google.com/maps/documentation/routes/transit-rm):
  confirms the matrix endpoint supports TRANSIT. The separate Compute Routes transit
  guide's day window was not transferred into a matrix rule without matrix-specific proof.

This audit verifies documented semantics, not actual availability or future travel
conditions. Complete HTTP serialization/acquisition stays in a separately approved
integration, not LangGraph nodes or this offline scorer.

## Existing-seam development validation

Command: pytest backend/tests/evaluation/test_snapshot.py
backend/tests/evaluation/test_occupancy.py backend/tests/evaluation/test_schedule_time.py
-q -p no:cacheprovider --basetemp .scratch/ticket07-preflight-testtmp --tb=short,
with TRIPWORLD_TEST_DATABASE=0.

Observed: 59 passed in 3.66s, no failures/skips. Tests are existing synthetic seam
regressions; no Ticket 07 parser/scorer/CLI or new fixture was implemented. Temporary
files are removed after recording results. This does not validate a route metric,
constitute a formal benchmark or freeze any version.

## Historical resume boundary before user answers

Resolve the first frontier and any downstream policy/interface decisions, then record
which are Accepted versus Proposed. Confirm shared understanding before claiming
specification closure. Issue #19 stays open/needs-info until that closure. Implementation
needs a separate approved scope; no commit/push or Ticket 08 execution follows.


Initial factual-check checkpoint: five intended documentation files only; 134 local
Markdown targets exist; English and diff checks passed. Index is empty, HEAD remains
3427784b87d5864aba25dcba8b48430ec4de9dac and the generated preflight test root is absent.
Issue #19 read-back confirms open/needs-info with this preflight disclosed as local and
unpublished. First-frontier answers remain pending; no ready/implementation claim follows.


## Q1 user decision — 2026-10-02

Status: Accepted. When no authoritative explicit departure is stated, allow waiting and
choose the longest continuous available travel fragment. For the 10:00/11:00 example
with non-travel protection 10:10-10:20, choose 10:20-11:00; a thirty-minute route can
fit. This supersedes the proposed immediate A.end default, which was not selected.
An explicit submitted departure remains controlling and is not replaced by a longer
or more favorable later fragment. Selection uses itinerary intervals only, before
observing provider duration or trying alternate route results.

Proposed deterministic tie handling: for equal longest durations choose the earliest
start, then stable source order. Do not compare resulting route durations to break ties.
Uncertain blockers must not be erased to construct a longer interval. Q2 tolerance at
a protected boundary and Q3 decisive partial-evidence combined FAIL remain pending;
Q1 acceptance alone does not resolve them or authorize implementation.


## Q2 user decision — 2026-10-02

Status: Accepted. Do not cross applicable protected non-travel time, even by two minutes.
For the selected continuous interval, distinguish a hard protection/commitment boundary
from the next-visit deadline. The former receives zero grace; the latter retains the
accepted 300-second schedule classification tolerance. Provider duration plus the
single DRIVE reserve must fit before a hard boundary. Duration-cap tolerance remains
separate. primary_visits-only protection does not itself restrict transport.

This refines the formerly broad wording of schedule tolerance without changing any
planner threshold or Ticket 05 zero-grace occupancy rule. A two-minute hard-boundary
overrun is FAIL; a two-minute deficit only relative to the next visit can remain within
route schedule tolerance. Q3 remains pending; no route implementation is authorized.


## Q3 user decision — 2026-10-02

Status: Accepted. Distance or time over its applicable limit establishes FAIL even if
another component is UNKNOWN. A sixty-minute WALK response with missing distance fails
the effective fifty-minute duration cap, while distance remains UNKNOWN and complete
evidence coverage is not claimed. For context-applicable evidence, mode-policy, caps,
hard-boundary/schedule checks and explicit no-route compose as follows: any independently
proven FAIL yields combined FAIL; all required components PASS yields combined PASS;
otherwise UNKNOWN. Structural/context uncertainty is not itself a proved failure.

## Consolidated deterministic interval and claim rules

These technical rules implement the three accepted meanings within prior boundaries;
they do not introduce a departure optimization, alternate mode search or new provider.

1. Retain the current same-day candidate inventory and source-stable leg IDs. Confirmed
   same-canonical pairs are N/A; no inter-day or Nearby connection is manufactured.
   Unresolved roles/order/identity/clock do not erase candidate records or yield PASS.
2. Normalize A.end/B.start independently. Subtract only applicable scheduled_commitments
   protections and independently fixed generic/other occupied commitments from that
   gap. Exclude this leg's own source-selected transport claim from blockers so it does
   not block itself. primary_visits-only protection is not a traffic blocker. Preserve
   original obligation IDs, scopes and source refs, even when blocker spans are unioned.
3. Unknown potentially overlapping occupancy/protection remains interval uncertainty;
   it cannot be assumed absent to choose a longest fragment. Known disjoint uncertainty
   does not contaminate an unrelated leg. Never concatenate disjoint free fragments.
4. Collapse exact duplicate authoritative claims. A unique, interpretable stated mode
   and departure are used; distinct incompatible Transfer alternatives or unresolved
   association do not justify choosing the favorable claim. V0 sequential mixed-mode or
   disjoint transport segments remain an unsupported/uncertain one-matrix association,
   not a fabricated uninterrupted single-mode journey.
5. A valid explicit departure controls and must fall within the endpoint gap and the
   selected continuous free fragment. Do not silently replace an invalid explicit
   departure with a default. Missing claimed arrival/duration does not manufacture an
   arrival; provider duration independently supplies the route measurement. The route
   field dependency is assessed separately from projection occupancy completeness.
6. With no authoritative explicit departure, rank known free fragments by descending
   exact elapsed length, then earliest UTC start, then stable source order. Select once
   before consulting provider results. If the longest fragment's selected route fails,
   do not try another fragment. The proposed tie break makes equal lengths deterministic
   without comparing traffic outcomes; it is an implementation choice, not an extra
   allowance. No known fragment or an uncertain selection yields a specific reason.
7. For duration d, reserve r, chosen gap G: raw deficit is max(0,d+r-G). If the selected
   fragment ends at hard protection/fixed occupancy, require d+r <= G with zero grace;
   otherwise require d+r <= G+300 seconds against the next-visit deadline. Equality
   passes. Record the deadline kind, effective tolerance, raw deficit and nominal caps.
8. Date/time support and endpoint/mode correspondence gate factual provider components.
   Malformed input delivery/foreign preparation/corrupt snapshot requires whole-material
   correction. Valid unavailable evidence or unresolved interpretation yields component
   UNKNOWN, not corruption or a synthetic no-route.

## Source-linked request mode policy

The existing finite mode extractor and independently reviewed claims remain the normal
itinerary mode source. An explicitly fixed original-input mode may supply the mode when
no usable itinerary claim fixes one, following the accepted request-or-itinerary policy;
this is not an inference from soft preferences or from an arbitrary query's mode.
A restriction's allowed set alone is not fabricated as a submitted Transfer. Missing
V1-V3 Transfer records remain missing in source/claim coverage, even if an independent
explicit request supplies a mode for a candidate feasibility check.

Use a new independent review envelope, not a new Ticket 05 executable obligation:
rtpeval_route_reviews_1 with batch_id, revision and group records. Each group record
links group_id/input_sha256, reviewer_ref, reviewed_at and source-backed policies:

- status unrestricted: explicit reviewed absence of hard mode restrictions; no guessed
  unrestricted status when review metadata is missing.
- status restricted: ordered constraint records with policy_id, scope whole_trip or
  specified_dates (inclusive Input dates), nonempty allowed_modes subset of WALK/TRANSIT/
  DRIVE, and source_refs using existing original-input field/quote/occurrence provenance.
- status unresolved: reason and source_refs where available; only affected policy
  components remain UNKNOWN. Unsupported or ambiguous mode meanings are not invented.
- Optional stated_mode: WALK/TRANSIT/DRIVE plus original-input source_refs establishing
  that exact mode, distinct from an allowed set or soft preference. Conflicting scopes
  or an impossible empty intersection require material review/correction.

Missing envelope/group record yields request_mode_policy_unavailable, not a reduced
population or an automatic PASS. An authoritative claimed mode outside a known allowed
set proves policy FAIL; it is retained as the query mode rather than switched to make
compliance pass. Unclear mode remains structural UNKNOWN; query metadata cannot settle
it. Input restriction extraction/review remains preparation work without an LLM call.
This preserves the current RequirementSpec and Ticket 05 default behavior.

## Provider applicability and raw interpretation

- The selected submitted/evaluation departure and provider query departure are separate
  fields. explicit_departure must match the adopted UTC instant exactly; retain original
  strings and offset/local-day diagnostics. No 300-second query-time matching tolerance.
- Deliberate time_independent contexts are allowed for WALK and explicitly
  TRAFFIC_UNAWARE basic DRIVE only. Keep null provider departure, acquisition time and
  this estimate label; it is not a claim to have queried the historical visit date.
  TRANSIT and time-sensitive DRIVE require applicable explicit departure. An accepted
  returned traffic fallback does not repair a wrong requested date/mode/endpoints.
- Compare supported explicit departure to the stored acquisition attempt timestamp;
  past non-TRANSIT query contexts are unsupported. A provider failure/unsupported-context
  signal remains UNKNOWN; do not transplant Compute Routes-specific transit horizons
  into this matrix implementation or shift dates to evade provider limitations.
- routing_preference is a documented DRIVE enum; do not send it for WALK/TRANSIT.
  avoid_tolls/highways/ferries must be boolean and applicable to DRIVE; language/region
  must be nonempty strings. Unsupported options require recorded applicability reasons.
  Capture parameters in hashes; future HTTP serialization is a separate integration.
- Rebuild the complete identity/source-linked evidence plan, including all supplied
  legs/details/request keys and paired scope. Optional trusted expected-plan equality
  strengthens linkage. Verify raw replay before inspecting the unique (0,0) element.
- Explicit object status with absent code means default zero under the frozen boundary;
  integer nonzero/error status cannot prove no-route. Missing/null/malformed status,
  invalid indices/condition, or contradictory route-information/no-route fields are
  UNKNOWN. Do not trust matrix summary available as a verdict.
- Successful applicable ROUTE_NOT_FOUND gives availability/combined FAIL and null
  duration/deficit. Successful ROUTE_EXISTS requires a finite nonnegative duration
  string with up to nine fractional digits; no staticDuration substitution. WALK
  distance must be a nonnegative strict integer for distance-cap PASS. Missing/invalid
  distance leaves that component UNKNOWN without erasing independently proved failure.
- Preserve raw duration and exact integer nanoseconds/decimal text; use no binary-float
  arithmetic, flooring or ceiling at a verdict boundary. Existing itinerary instants
  remain independently validated microsecond clocks; represent their lengths exactly
  at nanosecond scale for comparison. Schema can expose duration_nanoseconds and
  duration_seconds_exact text, with display formatting separate from classification.

## Public seams proposed for approved implementation

- prepare_routes(intake, identity_report, schedule_context=None, occupancy_reviews=None,
  route_reviews=None, coordinate_evidence=None, *, paired=False) -> immutable
  RoutePreparation. Inventory, claim/policy, selected interval/departure and unresolved
  reasons remain visible. Independent coordinate records link adopted canonical IDs,
  finite coordinates, raw evidence references/hashes; missing coordinates leave a
  context pending rather than borrowing planner locations. Emit Ticket 04-compatible
  route_contexts only where complete. No acquisition or provider request serialization.
- score_routes(intake, identity_report, snapshot_directory, schedule_context=None,
  occupancy_reviews=None, route_reviews=None, coordinate_evidence=None, *, paired=False,
  expected_plan=None) -> immutable RouteResult. Recompute preparation, verify snapshot
  request-context equality and linkage, then emit rtpeval_route_report_1 with frozen
  rtpeval_route_rules_1. Prepared query metadata does not become authoritative claims.
- Local preparation/scoring CLI: source batch and independent identity plus supplied
  preparation files; scoring adds the frozen snapshot. Stdout deterministic JSON;
  status complete exits 0 even with leg FAIL/UNKNOWN; material correction or identity
  replay exits 2. No socket/provider/model/database client or input rewrite.

Report per-occurrence leg sources, N/A/structural reasons, claim present/absent and mode
basis, candidate/selected fragments, deadline kind/tolerance, policy/cap/schedule/no-route
components, requested/returned/raw observation refs, exact d/r/G/overruns/deficits and
rule/source/preparation/plan/snapshot hashes. The scorer does not compute a V3 Repair
delta or five-dimension total. Name choices are proposed wire contracts, not an existing
import/API implementation.

## Coverage and aggregation closure

Keep structural evaluability, applicable response coverage, complete component evidence,
decisive combined coverage and duration-available counts separate. Successful no-route
is decisive response evidence with no duration. Partial decisive FAIL enters conditional
P/(P+F) but does not become full evidence. UNKNOWN never turns into zero travel time.
Known same-canonical N/A is excluded with its reason. Unresolved role/adjacency population
suppresses full-scope percentages; unresolved known candidate mode/identity remains in
that candidate denominator. Empty denominators return unavailable, not fabricated rates.

Daily/request provider-duration sum, observed maximum and median include only genuinely
observed context-applicable legs and retain observed/applicable/missing counts. Reserve
is separate from provider duration. No-route and UNKNOWN have null numerical duration;
no complete daily burden is claimed with missing legs. Repeated occurrences stay repeated;
deduplicated snapshot requests do not deduplicate score units. Route deficits and Ticket
05 overlaps may describe one problem and are not automatically double-weighted. Auxiliary
mask/total and formal cross-request analysis remain outside Ticket 07.

## Implementation approval proposal

Create backend/evaluation/routes.py, route_cli.py and private route preparation/raw
parsing helpers as needed; add route scorer/CLI tests. Reuse or extract only neutral
source/context, reviewed occupancy/protection validation, time and full-plan integrity
helpers while preserving Ticket 05/06 behavior. Do not import planner route_options,
initial_routes/validation findings as truth or change provider/runtime/planner behavior.

Drive TDD through public preparation/scorer/CLI seams. Required synthetic checks:
longest fragment/tie selection independent of provider response; explicit departure;
non-travel hard boundary versus visit deadline; scope/free-time/fixed/missing occupancy;
V0/V1-V3 source authority, absent/duplicate/conflicting/mixed claims; exact Input mode
policy provenance; same venue/inter-day/unresolved population; aware/naive/DST clocks;
exact query/coordinate/context/identity/paired linkage; raw status/condition/no-route,
missing distance/duration, precision/tolerance/reserve boundaries and accepted fallback;
partial FAIL versus full evidence; deterministic no-network/source-unchanged CLI replay.

Run relevant evaluation regressions after each affected slice, broader/full relevant
backend gate after neutral/shared changes, Ruff/compilation and Standards/Spec code
review with corrections. Update acceptance/contracts/current docs/archive and #19
within the approved implementation. No live smoke, formal case/experiment, commit/push,
freeze, total report or later ticket is included. Implementation has not started.

## Final specification checkpoint — 2026-10-02

All three human result-meaning decisions are Accepted. Remaining deterministic
validation/wire choices above are a concrete technical proposal aligned with existing
contracts. Preflight is specification-ready for review and implementation scope approval;
no code/API or test fixture has been created. Earlier pending states remain dated history.
Current files are local/uncommitted and unpublished; original 59-test seam result is
unchanged. Final approval should confirm the consolidated technical scope; it does not
need to repeat the three answered result-meaning questions.

Issue #19 was updated and read back as open/ready-for-agent, with the three accepted
decisions, concrete proposal, original validation scope and implementation approval
pending stated explicitly. The prior preflight and migration records are preserved as
history; implementation acceptance checkboxes remain unchecked. The metrics contract
was aligned with hard-boundary grace and partial decisive failure. Readiness does not
authorize implementation or imply that unpublished local documents are on GitHub.

Final documentation checks: six intended tracked/untracked documentation changes plus
the ignored archive; 142 local Markdown targets exist; English and diff checks pass.
Index is empty, HEAD remains 3427784b87d5864aba25dcba8b48430ec4de9dac and the generated
test root is absent. No tests were repeated for subsequent documentation-only changes.

## Subsequent implementation authorization — 2026-10-02

The user approved the concrete offline implementation scope summarized after this
preflight. prepare_routes/score_routes/local CLI, synthetic TDD, relevant/full offline
regressions, Standards/Spec review/corrections and related documentation/archive/Issue
updates are now authorized. Earlier implementation-pending statements are historical
checkpoints. No real provider/model/database call, formal case/experiment, Git write,
version freeze, auxiliary total or later ticket is included. Acceptance is recorded
separately after implementation and verification; readiness is not a version freeze.

## Subsequent implementation record

The [offline acceptance](ticket-07-acceptance.md) now records public preparation/scoring,
local CLI, actual synthetic TDD and regression results, review findings and corrections.
The earlier inspection and pending approval statements remain historical. Implementation
does not authorize live acquisition, Git actions, formal evaluation or Ticket 08 work.
