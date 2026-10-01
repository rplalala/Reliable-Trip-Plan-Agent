# RTPEval unified metrics contract — draft

Status: Consolidation of accepted decisions and explicit remaining specification items. Not frozen or implemented.
Date: 2026-09-28. Documentation-only; no evaluation results or experiments.

## Population, sources and units

Evaluate only the user-submitted batch of benchmark-qualified four-version groups. Benchmark construction owns screening, failed-attempt records and iteration recommendations; Evaluation does not select cases or rerun planners. Each primary visit in a qualifying group represents one POI with its own explicit interval. A multi-POI block sharing one interval is an input-contract diagnostic for upstream correction, not an invitation to split times or invent visits.

Sources: I = original Input; R = reviewed RequirementSpec; P = selected per-version result itinerary; E = independent identity records and frozen evaluation evidence; U = per-version usage file; M = optional mechanism records; H = blinded human answers. Independent quality checks read I/R/P/E and frozen rules, never M judgments. Original artifacts remain unchanged.

The request/group is the paired comparison unit. Visits, obligations and legs are nested observations, not independent requests. Compute per-request counts/rates and preserve those records for paired comparison. Exact cross-request aggregation, confidence intervals and multiplicity belong to the preregistered analysis plan; do not silently substitute pooled micro-rates for request-level comparisons.

## Common report contract

Each metric records its unit, scope, numerator/denominator when meaningful, applicable count, structurally evaluable count, evidence-adjudicable count, PASS/FAIL/UNKNOWN/N/A counts where applicable, raw magnitude, reason codes/explanations and source/rule hashes. Descriptive metrics need not be converted into PASS/FAIL.

- PASS: check is applicable, evaluable and meets its frozen rule; route tolerance passes are explicitly labelled.
- FAIL: applicable check has sufficient evidence to contradict the rule. Not every descriptive imperfection is a failure.
- UNKNOWN: applicability is established but structure, semantics or evidence cannot support judgment. Always retain the specific reason and relevant artifact/evidence references.
- N/A: check does not apply; do not turn it into a successful observation or zero travel time.
- Missing material: intake or optional-track availability diagnostic, not a quality score of zero.

Where a denominator cannot yet be established, report the unresolved structural count instead of inventing a rate. Empty denominators give unavailable/not-applicable rates, never 100 percent. Evidence coverage and evidence compliance are separate; report coverage with compliance rather than rewarding selective uncertainty. Artifact failures requiring batch correction must not be silently treated as a smaller evaluated cohort.

## A. Independent itinerary metrics

| Metric | Source and unit | Calculation / denominator | State and interpretation |
| --- | --- | --- | --- |
| Date coverage | I, P; requested calendar day | Days containing >=1 main visit / inclusive requested days; separately day-present, any-activity and empty-main-day counts | Descriptive. Empty is not automatically FAIL; any supported product minimum/exemption check must be explicitly separate. |
| Main visits and density | P, independent role record; visit/day | Visit occurrences per requested day; counts below 2, within 2-5, above 5; requested days include empty days | Descriptive guidance, not <2 or >5 hard failure. Count visits and unique canonical venues separately. |
| Canonical grounding | P, E; main visit | Independently resolved main visits / applicable main visits, retaining identity-UNKNOWN visits in the latter | Verified fraction, not a hallucination rate. Ambiguity or failed lookup does not prove fabrication. Uncertain role counts remain visible. |
| Claimed-ID consistency | P, E; visit with supplied ID | Consistent/conflicting/unverifiable association counts among supplied-ID visits; absent-ID count separately | V0 absent IDs are not errors. Confidently adjudicated named venue can support downstream checks while supplied-ID error remains recorded. No extra auxiliary penalty is currently included; retain raw consistency counts. |
| REQUIRED fulfillment | R, P, E; reviewed obligation | PASS / (PASS+FAIL) among decidable obligations, plus decided/applicable coverage and all raw states | Minimum/exact/date conditions determine outcome; do not count individual subconditions as extra independent obligations. Relevant unresolved identities can prevent definitive omission/count judgments. Unstated named-visit counts use explicit exact one upstream under the 2026-10-01 correction; stated count/date semantics remain binding. |
| EXCLUDED violation | R, P, E; reviewed prohibition | FAIL / (PASS+FAIL), with obligation coverage and raw states | Confirmed scheduled match violates; unresolved potential matches can prevent a clean PASS. Nearby does not satisfy or violate main-visit obligations under accepted scope. |
| Protected/fixed-time compliance | R, P; supported reviewed time obligation | PASS / decidable applicable obligations; conflicting intervals/duration separately | Explicit time constraints only. Unresolved meanings/unsupported operators retain availability reasons. Exact role/boundary logic remains OPEN; no inferred clock range for vague afternoon. |
| Activity overlap | P, independent occupancy; timed commitment pair/day/request | Positive intersection pair count, affected requests and union duration where >=2 distinct commitments overlap | Touching endpoints do not overlap. Deduplicate transport activity/Transfer representations; union minutes are not the sum of overlapping pairs. Occupancy role details remain OPEN. |
| Scheduled occupied time | P, independent occupancy; day | Union of applicable scheduled commitment intervals, in minutes/hours | Descriptive; avoid double-counting overlaps or transport representations. Flexible free_time is distinguished from fixed occupancy. Final inclusion rules OPEN. |
| Opening structural evaluability | P, R, E; applicable main visit | Structurally evaluable visits / applicable visits, with reasons for excluded or unclear scope | Distinguish identity/clock/role uncertainty from absence of provider hours. |
| Opening evidence coverage | E, P; applicable main visit | Complete-evidence visits / applicable visits; separately verdict-decidable coverage and structural breakdown | Separate current/date-specific basis, regular fallback and unavailable basis; partial decisive FAIL does not become complete evidence. |
| Opening compliance | P, E; verdict-decidable visit | PASS / (PASS + FAIL), including partial decisive FAIL under the 2026-10-02 clarification | Positive overlap with a known closed span yields FAIL; zero grace and departure exactly at close are retained. Missing evidence without containment/conflict proof stays UNKNOWN. |
| Opening conflicts and outside minutes | P, E; visit/time | Confirmed conflicts and visit duration outside union of adopted open intervals | Includes early arrival and within-visit closure. Partial evidence can support labelled lower bounds, not invented closed minutes; exact partial aggregation OPEN. |
| Route structural evaluability | P, R, E; same-day candidate leg | Defined/evaluable legs / applicable candidate legs, with structural unknowns | Exclude inter-day travel and confirmed same-venue connections as N/A. Unresolved endpoints/mode/occupancy remain visible. Do not silently skip unknown intermediate locations. |
| Route evidence coverage | P, E; applicable same-day leg | Applicable independently adjudicable responses / applicable legs; expose duration-available count separately | Successful applicable explicit no-route is adjudicable evidence, not a provider outage, although it has no usable duration. |
| Route availability/compliance | P, E; leg | Context-specific no-route FAIL counts; time/cap compliance reported separately below | No route under valid endpoints/mode/departure is FAIL. Provider failure, timeout, malformed/incomplete response is UNKNOWN. Do not switch mode to force PASS. |
| Mode-threshold compliance | P, E, frozen product rules; cap-adjudicable leg | PASS / (PASS+FAIL), with full-evidence and decisive coverage separately; raw nominal overruns retained | WALK <=3 km and nominal45+5 minutes; TRANSIT nominal45+5; DRIVE nominal30+5. No distance tolerance. Any independently proven component failure establishes FAIL, including missing other components; all required components must pass for PASS, otherwise UNKNOWN. |
| Scheduled route feasibility | P, R, E; time-adjudicable leg | Compare duration + reserve to one selected continuous interval; zero grace at a hard boundary, otherwise +300 seconds at the next-visit deadline | Without explicit departure select the longest known free fragment before route evidence; valid explicit departure controls. DRIVE reserve600 seconds, others0; no extra buffer or crossing protected non-travel time. Preserve raw deficit even for tolerance PASS. Explicit no-route is a separate route FAIL, not a fabricated numerical deficit. |
| Transfer deficit | P, E, R; duration-supported leg | max(0, provider_duration + product_reserve - available_interval), in seconds | Report raw value and tolerance-based verdict separately. Do not add cap tolerance to schedule tolerance to obtain ten minutes. |
| Observed transfer burden | E, P; observed leg/day | Provider-duration subtotal, median and maximum with observed/applicable counts; product reserve separately | Partial evidence yields observed subtotal/maximum, not full-trip travel burden. Unknown is not zero. |
| Canonical repetition | P, E, R; visit/day | Within/across-day canonical counts and repeated occurrences; authorized obligations shown alongside | Descriptive repetition is not automatically a defect. Extra visits beyond a minimum are not automatically violations. Exact non-required ratio denominator and authorization attribution remain OPEN. |

For REQUIRED and EXCLUDED, adjudicable-obligation rates are conditional and must never appear without coverage and UNKNOWN counts. Underlying minimum/exact/date components remain auditable. Numerical formatting and final exported field names are still wire-contract items.

## B. Resource metrics

| Metric | Source / denominator | Reporting rule |
| --- | --- | --- |
| End-to-end latency | U; selected run | Measured duration under a common capture boundary; missing/partial scope explicit. |
| Stage latency | U; stage/run | Record available stages; overlapping stage times are not blindly summed as wall time. |
| Model calls and tokens | U; call/model/stage/run | Reported input/output/total tokens separate from engineering estimates; preserve call provenance and missingness. |
| Provider usage | U; provider/run | Actual sends, failures/retries, cache hits and requested Routes elements separately; no budget limits masquerading as consumption. |
| Repair use | U and M; V3 selected run | Rounds, calls, tokens and time as subsets of totals; never count them twice. |
| Oracle usage | Evaluation acquisition ledger | Separate from planner usage. It does not alter planner cost comparisons. |

No universal efficiency score or conversion of resource usage into itinerary quality is adopted. Uniform usage capture is outstanding engineering preparation, not currently implemented by these documents.

## C. Human and independent Repair reporting

| Track | Source / unit | Report |
| --- | --- | --- |
| Blinded ranking | H; request and preference/pace/usefulness dimension | A/B/C/D ranking with ties; per-version-pair wins/ties/losses, valid comparison counts, unable-to-judge and N/A. Six pairs from one group are correlated. |
| Intra-rater consistency | H and private task mapping; hidden duplicate | Compare underlying plans, not display letters; exclude duplicate tasks from main result weight. Exact consistency summary OPEN. |
| V3 pre/post | P draft/final, R, common E; paired run | Independent before/after counts and defined deltas, denominators, evidence coverage, visit loss and new conflicts. Missing pair unavailable; identical valid pair gives zero changes where metrics are defined. |
| Controlled Repair | Supplied controlled artifacts, R, E; independent case | Target resolution/improvement, residuals, regressions and control invariants; do not infer success from target-ID disappearance. Kept separate from four-version E2E. Exact rates/denominators await controlled definitions. |
| Mechanism reporter | M, U; version/run/round | Trigger, parsed/accepted patches, stop reasons and RAG exposure; these do not decide quality outcomes or establish causal use. Exact event denominators OPEN. |
| Official Evidence Audit | Qualifying accepted-and-exposed/rule-used facts, independent recheck | Eligible/audited counts and supported/contradicted/scope-mismatch/unavailable outcomes; not general web-source accuracy or LLM causal-use evidence. |

The rater judges preference, pace and usefulness rather than performing external fact lookup or arithmetic. Behavioral counts are descriptive support, not automatic proxies for subjective quality; blinded tasks withhold automatic scores and RequirementSpec.

## D. Subscores and auxiliary total

The [score profile](score-profile.md) is authoritative for accepted score arithmetic: five equally weighted dimensions, each using PASS/(PASS+FAIL+UNKNOWN), with grounding expressed as verified visits/all applicable visits. Conditional compliance rates in the metric table remain diagnostic rates, not the auxiliary subscore formula.

Group-wide true N/A removes the dimension jointly; a single-version no-check dimension retains common weight with zero contribution and raw status/rates N/A, never fabricated FAIL. UNKNOWN is an applicable undecidable check, including insufficient structure/semantics as well as missing evidence. Display raw counts, verification coverage, unknown rate and the group's dimension mask beside the numeric total.

A leg contributes only one route verdict even if both duration cap and schedule fail. ID-conflict counts, density, repetition, coverage and resource/human outputs remain visible rather than silently creating extra score penalties. No additional weights or post-result optimization are permitted.

## E. Remaining decisions and technical work

This table makes the accepted rules inspectable but does not close timezone/DST semantics, role/occupancy ambiguity, departure/fallback provider semantics, repeated-visit attribution, exact controlled-case definitions, score aggregation or wire schemas. Freeze these before dependent implementation and held-out analysis. No new benchmark cases, test fixtures, code or experiments are authorized here.

## Ticket 05 specification closure — 2026-10-01

[Requirement/schedule](requirement-schedule-contract.md) supersedes the OPEN time-operator,
occupancy inclusion, non-overlap units and repetition-attribution details above for
Ticket 05. It closes typed minimum/exact/date checks, supported explicit dated time
operators, protected scopes and blocker union, conservative uncertainty, pair/union
conflict measurements and descriptive schedule/repetition definitions. It retains one
obligation or logical commitment per score unit and reports unresolved denominator
availability explicitly. No non-required repetition defect ratio is adopted.
Opening and route provider rules, total/mask export, human and Controlled Repair work
retain their own contracts/tickets. No metric implementation or experiment occurred.

## Ticket 06 preflight metric clarification — 2026-10-02

[Ticket 06 preflight](ticket-06-preflight.md) identifies an ambiguity in the historical
phrase "fully adjudicable": complete evidence coverage and a decisive visit verdict are
different when partial evidence proves FAIL. The user confirmed that any known closure
inside the scheduled interval yields FAIL, including incomplete evidence. Conditional
compliance includes that decisive FAIL: PASS / (PASS + FAIL). Full evidence coverage,
verdict-decidable coverage, raw states, exact duration and confirmed lower bounds remain
separate. Unknown spans do not become closed time. Established half-open/zero-grace
boundaries remain unchanged. Auxiliary total arithmetic remains Ticket 08, outside this task.


## Ticket 06 executable measurements — 2026-10-02

[Acceptance](ticket-06-acceptance.md) and the
[package wire](../../backend/evaluation/README.md#ticket-06-offline-opening-compliance)
record the implemented opening subset. Complete-evidence and verdict-decidable coverage
are separate; partial decisive FAIL contributes to PASS/(PASS+FAIL). Unknown portions
stay unknown. Exact outside duration is null when incomplete, with confirmed lower-bound
and unknown seconds retained. Aggregation is an observed per-visit subtotal with counts,
not global-time union or formal cross-request analysis. Unresolved role populations and
empty denominators suppress percentages. Auxiliary total/masks remain Ticket 08.

## Ticket 07 specification preflight closure — 2026-10-02

The user accepted longest continuous free-fragment selection for unstated departure,
zero grace at applicable protected non-travel boundaries, and decisive FAIL whenever
an independently proven distance/time component exceeds its limit. The
[route contract](route-contract.md) and [preflight](ticket-07-preflight.md) supersede
historical OPEN aggregation and unqualified schedule-tolerance wording for Ticket 07.
Explicit departure remains controlling; selection is independent of provider outcomes.
Provider duration and the single DRIVE reserve are assessed against the selected
fragment, never the sum of disjoint gaps. The separate duration-cap tolerance remains.

Partial decisive FAIL enters conditional P/(P+F) without becoming complete evidence.
Keep structural, applicable response, full component, decisive and duration-available
coverage separate; no-route is decisive with null duration. Observed transfer sum,
median and maximum retain missing counts and reserve separately. Unknown travel is
not zero, repeated occurrences remain separate units and unresolved populations/empty
denominators suppress full-scope percentages. Auxiliary arithmetic stays Ticket 08.
At the preflight checkpoint the concrete proposal awaited implementation-scope approval;
that inspection did not implement metrics or run formal cases/experiments. The user
subsequently approved the offline implementation described below.

## Ticket 07 executable route measurements — 2026-10-02

[Acceptance](ticket-07-acceptance.md) records the implemented public preparation/scorer/CLI
and its actual failure/correction/retest sequence. Separate component, structural,
applicable-response, full-component, decisive and duration-available coverage is executable.
Partial component FAIL enters P/(P+F) without establishing full-component completeness;
explicit no-route FAILs with null duration. Unknown or inapplicable evidence cannot prove
a factual over-limit component. An occurrence contributes one combined route verdict.

Raw deficit is max(0, provider duration + one DRIVE reserve - selected continuous time).
Hard deadlines have zero grace; only next-visit deadlines use 300 seconds. Duration-cap
tolerance remains independent. Observed duration sum/median/max retain missing counts and
reserve separately. Unresolved potential leg populations suppress complete burden globally
and on affected dates, while preserving observed subtotals. Empty/unknown denominators
produce null rates. This does not implement auxiliary total/masks, V3 deltas, formal
cross-request analysis or comparative conclusions; those retain their own tickets.
