# Shared POI acquisition and deterministic supply

## Default quality_first_1 capacities

<a id="b-03703c8677d9-0"></a>

The default policy is a shared V1/V2 acquisition change, not just larger budget numbers.
For trip duration D, let A = min(16, max(8, 2D + 6)). Final normal supply
K = max(A, 2D), while acquisition stays C = max(48, 4A), G = 2A,
ordinary Details sends = G + 8 and P = min(8, ceil(A / 2)). K is a supply
capacity, not an obligation to schedule all candidates or a feasibility guarantee.

<a id="b-03703c8677d9-1"></a>

| Days | Admission C | New success target G | Ordinary sends | Supply K | Profile cap P |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 48 | 16 | 24 | 8 | 4 |
| 2 | 48 | 20 | 28 | 10 | 5 |
| 3 | 48 | 24 | 32 | 12 | 6 |
| 4 | 56 | 28 | 36 | 14 | 7 |
| 5-8 | 64 | 32 | 40 | 16 | 8 |
| 9 | 64 | 32 | 40 | 18 | 8 |
| 10 | 64 | 32 | 40 | 20 | 8 |

<a id="b-03703c8677d9-2"></a>

Reliably resolved feasible REQUIRED places occupy shared capacity. Up to 16 REQUIRED may
expand the acquisition basis to max(A, REQUIRED count), and K to max(normal K, REQUIRED count).
C/G/send/P derive from that acquisition basis, never from the new 2D supply floor.
More than 16 REQUIRED remains an explicit capacity conflict even though final supply can hold 20. Ordinary shortfall does not invent places or demand
clarification just to fill a target. Configuration and absolute safety ceilings remain distinct.
These values now load from the single runtime.yaml. Historical conservative policy remains
only as an explicitly constructed compatibility/test case, not a second active config file.

## Admission and two-pass Details

<a id="b-91b3673077d0-0"></a>

Google and resolved RAG candidates share one canonical union and C, not separate allocations.
REQUIRED leads acquisition opportunities, followed by strength, subject and linked-intent
round-robin, cheap category/geographic facts and final canonical-ID ties. Early rating, cached
status, Google rank and cosine do not purchase admission priority.

<a id="b-91b3673077d0-1"></a>

First inspect compatible successful Details for every admitted candidate. Compatibility includes
identity, field mask and language; normalized facts must pass the existing common gate. Eligible
cache results participate in comparison without consuming G or new sends. The old r_pool
truncation no longer discards later valid cache entries under this policy.

<a id="b-91b3673077d0-2"></a>

Then acquire missing Details until G new independent qualified successes, send cap, C, queue
exhaustion or deadline. Failed/invalid responses consume sends but not successes. Request-level
attempt/incomplete state prevents silently repeating failed/cancelled work. Existing Details
only grant comparison opportunity, not selection reward. Separate requests do not share a
free cache merely because their destinations match.

## Deterministic final supply

<a id="b-b278dbe5081b-0"></a>

`select_planning_supply` starts with REQUIRED and excludes explicitly excluded identities.
Linked subject/intent opportunities rotate. Within the current cohort it prefers fewer distinct
requirement conflicts, more distinct supported alignments, then less repeated primary types.
One requirement cannot receive multiple rewards from several evidence dimensions. UNKNOWN
Profile evidence abstains. Rating breaks a tie only when every member has a rating; destination
distance and canonical ID finish the tie. Remaining valid candidates fill the bounded supply.
No RAG quota, provider-rank reward, cosine reward or model subset search is used.

<a id="b-b278dbe5081b-1"></a>

Selective Reviews/Profile remain bounded and evidence-request-driven, not mandatory for every
candidate. The final generator may schedule fewer than K and must preserve REQUIRED semantics.
Unscheduled supply is not automatically converted into reference recommendations.

## Accounting and implementation

<a id="b-12daf1778bd7-0"></a>

Record admission, cache-qualified comparison, ordinary new successes, actual sends, Profile use,
supply and scheduled identities separately. Discovery source, Google factual source and budget
owner are independent. Nearby references have their own accounting and do not inflate supply.

<a id="b-12daf1778bd7-1"></a>

Active files: `backend/app/policies/poi_capacity.py`, `acquisition_opportunities.py`,
`planning_supply.py`; `backend/app/services/planning_supply_pipeline.py`,
`candidate_acquisition.py`, `evidence_acquisition.py`; `backend/app/runtime/cache.py`.
CandidateAcquisition owns active acquisition; no retired semantic-selector framework is imported.

<a id="b-12daf1778bd7-2"></a>

Accepted sample evidence and exact test history live once in the
[Phase 6 recovery record](development_record.md#m-e07748f66be8).
Uncovered paths and quality limits belong to [known issues](known_issues.md).

## Independent work ceilings

Under default quality_first_1, ordinary Details has a120-second phase deadline with each request
bounded by20 seconds and remaining time. Candidate Text Search remains at most12 calls with20
results each; no pagination or extra queries are added just to reach C/G. Profile remains selective,
with P limiting places rather than requiring calls. Source-independent acquisition opportunities
use no early cached rating advantage. RAG has its separate increments in v2_design; these do not
replace or silently consume ordinary acquisition accounting. Cache hits, successful new candidates,
failed sends, unattempted work and shortfall retain distinct counters.

## Runtime ownership

`services/candidate_acquisition.py` owns Google/named discovery, optional V2 extension invocation,
canonical admission, Details and evidence-linked review acquisition. The current supply service
calls it through composition and supplies the existing capacity/order/final-selection policies.
`candidate_details.py` retains cache-first and new-success/send-budget semantics.
`policies/planning_supply.py` retains the deterministic final supply algorithm.
There is no runtime inheritance from or import of Semantic Evaluator/subset-selection experiments.
Zero evaluator/subset counters remain in existing result diagnostics; they do not instantiate code.
