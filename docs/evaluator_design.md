# RTPEval evaluator research design

Status: **ACCEPTED WITH SPECIFICATION ITEMS OPEN**

Decision recorded: 2026-09-24.

## 1. Authority, status, and authorization

This document records the research design accepted by the user after two code-informed
reviews. It is the accepted basis for a later RTPEval v1 Specification. The overall research
architecture is settled; remaining work concerns explicit specification items, not another
overall redesign.

This is **not Benchmark Frozen**, not a completed evaluation specification, and not
implementation authorization. V3 engineering is still in progress. Acceptance of this design
does not freeze V3 or any earlier version, demonstrate a research result, or authorize formal
experiments or thesis writing.

[PROJECT.md](../PROJECT.md) remains the current project-level source of truth. This document
owns the accepted evaluation design and its open decisions. Current implementation must be
checked again at the final engineering checkpoint; historical proposals and development
captures do not override the actual code or current project context.

Before V3 finishes, separately requested specification design may proceed for opening,
routes, requirements, identity adjudication, run outcomes, controlled cases, human presentation,
and the analysis plan. Do not implement an evaluator, create formal benchmark cases, run
experiments, or modify planning algorithms to accommodate evaluation under this approval.

After V3 engineering finishes, the first step is an **Evaluation Readiness Audit** against the
final actual checkpoint. Resolve the open items into a formal RTPEval v1 Specification, obtain
approval for implementation and development dry runs, and freeze the resulting rules and
analysis plan before held-out execution. This design does not authorize those later steps.

## 2. Research question and version comparison

RTPEval asks whether successive mechanisms improve final itineraries' groundedness, explicit
requirement satisfaction, temporal consistency, opening consistency, route feasibility,
verifiable reliability, and practical quality, and what additional computation they require.

| Version | Mechanism being compared |
| --- | --- |
| V0 | LLM baseline without external travel-information tools; retains shared request/preference interpretation |
| V1 | External travel information, including Places, Routes, Weather, and existing evidence acquisition |
| V2 | V1 plus TripWorld RAG discovery |
| V3 | V2-style initial draft plus explicit validation, bounded multi-round targeted repair, re-validation, and Nearby attached to the final primary itinerary |

V1/V2 already have post-primary Nearby. V3's distinction is its placement after repair, not
the introduction of Nearby itself. V0 is not necessarily a single-model-call request: nonempty
preferences can invoke the shared interpreter before generation.

All versions must run at the same final shared source checkpoint. Shared correctness fixes,
including evidence normalization, requirements, dates, and resource lifecycle changes, are
not V3-exclusive contributions. Historical old V1/V2 outputs must not be compared with final
V3 outputs as the main benchmark result.

These are comparisons of the implemented version mechanisms under recorded conditions, not
proof that every observed difference is attributable to one isolated causal factor.

### 2.1 Supplementary comparison: V3 vs Codex + Travel Planning Skill

Status: **ACCEPTED WITH SPECIFICATION ITEMS OPEN**. Direction recorded: 2026-09-25.

Add **V3 vs Codex + Travel Planning Skill** as a supplementary comparison of how the two
systems perform travel-planning tasks. It complements the main V0-V3 study; it does not
replace that study or establish a pure causal effect of harness differences.

For now, only this comparison direction is accepted. Tool access, environment isolation,
sample size, and execution configuration remain open and will be determined after V3
engineering is complete, starting with the Evaluation Readiness Audit. This addition does
not freeze the benchmark or authorize skill/evaluator implementation or experiments.

## 3. Stable design principles

- No unique Gold itinerary: multiple choices of places and schedules can be valid.
- Fixed requests, independent evidence, independent rules, and multiple metrics replace
  reference-itinerary text matching.
- Independent judgement and independent evidence collection are required.
- Google is frozen external evidence, not absolute real-world truth.
- Human-reviewed benchmark requirements are evaluation inputs, not injected E2E planner inputs.
- Report multiple metrics; do not create a primary weighted composite score.
- Report all-run outcomes and quality conditional on an itinerary being produced.
- Use request-level paired comparison; visits and legs are nested observations.
- Combine E2E, controlled Repair, V3 pre/post, and complementary human evaluation.
- Separate development/regression from held-out evaluation.
- Use a matched shared checkpoint and preserve UNKNOWN, N/A, and missing outputs separately.
- Separate structural evaluability, evidence coverage, and evidence compliance.
- Acceptance, fewer UNKNOWN results, and fewer repetitions do not automatically mean improvement.
- Retain single-rater blinded human evaluation with its limitations disclosed.
- Audit only accepted official facts exposed to a model or used by a rule.
- Freeze evaluation rules and the formal analysis plan before held-out execution and before
  held-out version differences are revealed.

## 4. Product scope

In scope are dated/timed primary visits, requested dates, canonical identity, REQUIRED and
EXCLUDED places, visit date/count obligations, fixed unavailable time, opening, transitions,
overlap, repetition, density, pace/spatial burden, soft preferences, repair, and system cost.

Complete accommodation schedules, meal coverage, bookings, and full-day occupation are not
mandatory outputs. Nearby is an unscheduled reference: it does not count as a primary visit,
satisfy REQUIRED, fill a primary coverage deficit, or contribute a planned primary expense.

The input budget is a whole-trip budget. Verified travel-cost and budget evaluation is
**DEFERRED for RTPEval v1**. Planner-reported amounts and missing values may be described,
but are not independently verified prices or a verified subtotal. Do not establish verified
cost coverage or whole-trip budget PASS as v1 main metrics. A valid numeric amount, a range
midpoint, and a Places price level do not establish a comparable party-level ticket cost.

## 5. Independence and proposed architecture

### 5.1 Judgement independence

Independent quality scoring reads only planner outputs, the human-reviewed requirement
specification, and the evaluation snapshot, under the frozen evaluation rules/configuration.
It must not use V3 findings, ValidationReport, TargetProgress, repair status, acceptance
decisions, runtime scope, or RAG origins to select its answers or decide what to score.

Those internal records belong to a separate mechanism reporter. It may describe what the
system attempted, but cannot supply ground truth to the quality scorer. Runtime acceptance
is not independent repair success.

### 5.2 Collection and factual-source independence

The evaluator owns its provider requests, cache, limits, timestamps, failure records, and
snapshots. Planner RequestCache or retained planner evidence must not automatically become
external evaluation evidence. Planner evidence can support mechanism analysis and the
separately scoped official-fact audit.

Google may be used by both planner and evaluator. Consequently, automatic results mean
"consistent with the frozen external evidence used by the evaluator," not "objectively
correct in the real world." Full factual-source independence is not claimed.

### 5.3 Component responsibilities

| Component | Responsibility |
| --- | --- |
| Run Collector | Preserve full requests/results, outcomes, provenance, configuration, usage, timing, and failures without changing planning decisions |
| Evaluation Adapter | Map outputs to a common representation while retaining original roles, timestamps, identities, amounts, notes, and uncertainty |
| Requirement Specification | Independently reviewed request semantics, established during benchmark design rather than copied from the planner interpreter |
| Identity Resolver | Resolve place references, retain alternatives, and route ambiguous/high-impact items to adjudication |
| Evidence Collector | Acquire and persist independent Places/Routes evidence under a uniform policy |
| Offline Evaluator | Score output/specification/snapshot under frozen rules without network access |
| Reporter | Aggregate independent quality results; keep mechanism diagnostics and resource accounting distinguishable |

This is a responsibility model, not a requirement to introduce separate services or new
infrastructure. Requirement specifications exist before planner execution even though they
are consumed during later scoring.

### 5.4 Code-sharing boundary

Potentially reusable components include neutral PlanningRequest/Itinerary/Money DTOs,
Google request/response DTOs, HTTP transport, and mechanical coordinate/field conversions.
Basic normalization may be shared only after independent fixture verification.

Do not reuse V3 validation, repair acceptance, route/schedule/spatial decisions, finding
comparisons, or target progress as the evaluator implementation. A shared directory name
does not make a function neutral: current opening-hours functions already implement adopted
evidence selection and judgements used by V3.

Independent manually checked fixtures should cover current/regular hours, missing and empty
periods, overnight and 24-hour schedules, DST, successful empty route status objects,
conditions, fallback, invalid/negative durations, and direction. Shared mapping errors must
not silently contaminate both planner and evaluator.

## 6. Benchmark composition and sampling

### 6.1 Development and city eligibility

Tokyo, Sydney, London, and Melbourne are development/regression cities. Use them for
evaluator dry runs, historical case studies, and mechanism diagnostics, not as the sole
generalization evidence.

Maintain city exposure categories such as mentioned, fixture-only, smoke, debugging, tuning,
and held-out eligible. A city name occurring in a unit fixture is not equivalent to
itinerary-level targeted tuning.

Final held-out cities remain OPEN. Selection should consider itinerary-level exposure,
basic Places/Routes operability, reasonable but not necessarily optimal TripWorld coverage,
geographic/timezone support, and geographic/urban diversity. Do not select cities using V3
scores. Do not silently require cross-city travel or choose only the richest RAG coverage.

### 6.2 E2E design target

The current design target is six cities with six request types each: **36 unique requests**.
The types are Basic, Soft Preference, REQUIRED, REQUIRED + EXCLUDED, Pace/Spatial, and Complex.
Basic still contains the mandatory structured budget. Complex must not always mean long trip.

Proposed length strata are 12 requests of 2-3 days, 18 of 4-5 days, and six of 7-10 days.
Cross length with query type rather than confounding the two.

Independent analysis tags may include REQUIRED dates/counts, explicit revisits, OPTIONAL,
EXCLUDED, exterior/venue-entry intent, fixed unavailable time, explicit transport preference,
relaxed/tight pacing, whole-party preferences, supported subgroup preferences, long trips,
and constrained budgets. Tags do not activate case-specific scoring rules.

Unsupported, contradictory, ambiguous, or demonstrably unsatisfiable requests require
explicit boundary-case semantics. Their inclusion and allocation remain specification items;
do not silently mix them into normal successful-itinerary expectations or require the planner
to act as a complete infeasibility solver.

### 6.3 Optional repeats: OPEN

One run of each version on each request gives **36 x 4 = 144 planner runs**. An optional
second run for 12 preselected requests adds 48, giving **192 planner runs**.

Do not currently prioritize repeats over additional unique requests. After V3 finishes,
use approved development observations of per-run cost, latency, provider usage, failure rate,
and actual run-to-run variation to decide the final 144/192 plan. Select repeat requests before
formal outcomes are known. Repeats are sensitivity observations, not new independent requests
and not double-weighted main results. Live-data repeats measure run-to-run sensitivity, not
pure model variance unless external inputs are also controlled.

## 7. Requests, identity, and common scoring semantics

### 7.1 Human-reviewed requirements

The evaluation specification must independently state relevant named identities, inclusion
rules, mandatory dates, visit counts, fixed unavailable intervals, transport requirements,
and exterior/entry intent. It must follow the actual request, not the planner's interpretation.
It is not injected into E2E planning.

Distinguish minimum count, exact count, and date obligations. Exceeding a minimum is not a
revisit violation. If exact-count or other semantics exceed the final product contract,
record that boundary rather than silently treating them as supported.

### 7.2 Identity adjudication

Independent evaluation may resolve V0's name-based places using Google. This does not give
V0 tools at planning time. Do not automatically accept the first search result, and do not
automatically treat ambiguity as hallucination.

Automatically handle evidence-sufficient matches. Send ambiguous matches, ID/name conflicts,
and high-impact REQUIRED/EXCLUDED identities through human adjudication. Preselect a sample
of automatic acceptances for manual checking. Retain candidate alternatives, decisions,
reasons, and identity mappings; deduplicate repeated identities to reduce work.

V1-V3 IDs remain subject to association checks. Hide version labels during adjudication
where practical. Unresolved items remain unresolved when the adjudication budget is exhausted.

Define evaluation-relevant place-bearing activities before freeze. Preserve model-declared
roles, but do not let a concrete named visit evade checks solely because it is labelled
generic_activity or unknown. Do not invent POI roles through unvalidated keyword rules.

### 7.3 Denominators and missingness

For each applicable metric retain raw counts, numerator, denominator, unknown/not-applicable
counts, and reason distributions. Do not turn UNKNOWN into zero or an empty denominator into
100 percent compliance.

- Structural evaluability: can the relevant visit/transition/check be defined from the output?
- Evidence coverage: is usable independent evidence available for that defined check?
- Evidence compliance: does the check satisfy the rule where evidence permits judgement?
- UNKNOWN: the check applies, but available semantics or evidence do not permit judgement.
- N/A: the check does not apply.
- Missing output: no evaluable planner artifact exists; this is a run outcome, not an
  ordinary unknown fact within a successful itinerary.

Do not hide structurally unclear transitions by dropping them before reporting coverage.
Grounding's verified proportion may retain unresolved visits in its denominator without
claiming those unresolved visits are false places.

## 8. Independent evidence snapshots

For each matched request block, run all four versions under a prebalanced or randomized
execution order, collect their outputs, construct the evaluation union, acquire independent
evidence, and then score offline. Do not always run V0, V1, V2, V3 in that order.

The union includes V0/V1/V2 finals, V3 final_primary, V3 pre-repair draft, and specification
identities needed for REQUIRED/EXCLUDED checks. Include round proposals/adopted outputs only
if independent round-level scoring is separately specified. Failed runs do not prevent
scoring available outputs from the other versions.

Deduplicate Places by canonical identity. Route request keys must distinguish direction,
mode, departure/time context, endpoint coordinates/version, and routing options. Preserve
returned calculation context/fallback as response provenance; do not collapse distinct
applicability contexts into one pair-level duration.

Record provider, query key, request/retrieval times, applicable dates/times, response/evidence
status, failures, and artifact hashes. A snapshot is a documented collection interval, not
one instantaneous state of the world. Record planner-to-oracle lag and keep blocks short,
including awareness of local-midnight changes. Collection failures and retries need one
predefined version-neutral policy.

Acquire only necessary directed legs rather than a full union N x N matrix. Batch only
compatible queries, count actual requested matrix elements, and keep evaluation acquisition
cost separate from planner cost. Evaluation cache is independent of planner RequestCache.

Future live reruns use new snapshots. Do not silently rescore old results with new real-world
facts. Explicit evidence-time sensitivity analyses are separate outputs.

## 9. Opening and route contracts: OPEN specification work

### 9.1 Opening

Report current/date-specific evidence, regular weekly fallback, and unavailable/uninterpretable
evidence separately. Compliance means full scheduled-interval containment in adopted hours;
it does not establish ticket ownership, reservations, eligibility, or special-area access.

Do not use open_now for future visits. Missing periods are not closed, and explicitly closed
periods are not missing. Longer trips naturally extend beyond the current-hours window;
report evidence basis rather than treating regular fallback as equally date-specific.

Freeze rules for timezone/offset conflicts, multiple periods, overnight visits, special-date
fallback, missing/invalid/closed evidence, exterior intent, and boundary precision/tolerance.
Public Activity currently has no general per-visit access-mode field, so evaluation assumptions
must be explicit and version-neutral rather than borrowed from V3 bindings.

### 9.2 Routes

Compare usable provider duration with an applicable continuous travel interval. Do not sum
disjoint free intervals across fixed commitments. Freeze departure and waiting semantics,
especially for TRANSIT and traffic-sensitive DRIVE.

Also freeze default mode and explicit overrides; intermediate real activities; elastic
free_time versus protected rest; explicit transport activities; unknown-location activities;
route-not-found versus provider failure, invalid status and fallback; same canonical versus
same-address places; overnight transitions; and any evaluator transfer buffer.

Do not copy V3's spatial reserves or acceptance thresholds as independent quality truth.
If mode is an evaluation assumption rather than an output claim, label the resulting metric
as feasibility under that assumption. Missing routes never contribute zero minutes.

With partial route evidence, report observed transfer subtotal and observed maximum, not a
complete trip burden. Exact adjacency, eligibility, batching, departure applicability, and
evidence conflict rules remain OPEN.

## 10. Controlled Repair

The accepted composition is **24 target cases + 8 control cases**, subject to final
capability verification. Eight target families with three examples each are sparse day,
duplicate visits, overfull day, overlap, opening conflict, route conflict, REQUIRED omission,
and EXCLUDED inclusion.

Separate confirmed-conflict targets from review/improvement targets. Sparse, Duplicate,
and Overfull are not automatically confirmed defects. Three examples per family support
mechanism diagnosis, not a precise family-level success estimate.

Controls cover no authorized modification, explicit revisits, legitimate relaxed low density,
reasonable high density, exterior visits, missing opening evidence, missing route evidence,
and protected content. Specify expected invariants for each control; do not universally
equate any modification with failure. Missing evidence cannot justify fabricated certainty,
but it does not prohibit every otherwise authorized edit.

### 10.1 Real V3 path with frozen external conditions

Freeze candidate pools, identities, provider responses, evidence, and one uniform capability
configuration. Preserve the real V3 validator, target selection, scope construction, candidate
preparation, repair, acceptance, and re-validation. Do not inject hand-selected targets/scopes
to replace the tested capability. Runtime candidate authorization still comes from V3.

The independent case definition specifies target facts and allowed invariants. A target that
V3 does not detect remains in the benchmark, not removed from the resolution denominator.
If any separately approved test injects targets/scopes, label it as a narrower component test.

The capability configuration may uniformly enable implemented review capabilities; do not
change settings per case. Default E2E uses the final approved product configuration. Capability
results must not be presented as default E2E behavior.

Frozen provider conditions must support the intended permitted edits or explicitly return
unavailable evidence. A new place outside snapshot coverage is not a successful repair merely
because it cannot be checked. Exact fixture/provider coverage remains a specification item.

## 11. Independent Repair and V3 pre/post outcomes

Compare V3 pre-repair draft with final_primary under the same evaluation snapshot. Do not
call the draft an independent V2 run. Do not include Nearby as a repaired primary visit.

Every V3 attempt enters run-outcome reporting. Only runs with both valid before and after
artifacts enter paired analysis. Identical outputs have delta zero; missing pairs are
unavailable, not zero. No-repair, skipped, and rejected cases remain eligible when both
artifacts exist. Do not select only accepted improvements.

Track independent outcomes using dates, canonical identities, requirement obligations,
activity correspondence, and before/after facts, not disappearing internal target IDs.
Distinguish resolved, partial, unresolved, unchanged, new confirmed conflict, evaluable-to-
UNKNOWN changes, visit loss, requirement regression, and independently specified scope or
protected-content violations. Do not use runtime scope to define independent quality truth.

Interpret metric changes together with denominators, evidence coverage, visit loss, and new
conflicts. Removing a visit or replacing it with an unresolvable place cannot automatically
count as complete success. Comparing compliance rates with changing visit sets requires
their underlying counts. Undefined metrics do not acquire numeric deltas by imputation.

## 12. Human evaluation

Retain **12 unique held-out cases**, comparing V2 and V3, with one rater and **three hidden
duplicate tasks** for intra-rater consistency. This is complementary exploratory subjective
evidence, not population-level user preference evidence. Report the rater's relationship to
the project and the limits of single-rater assessment. Do not report inter-rater agreement.

Preselect cases using stated strata. Choose the compared run deterministically in advance
rather than selecting the best repeat. Missing pairs remain reported; do not silently replace
them with successful cases. Duplicates reverse A/B presentation where specified, are spaced
apart, and never count twice toward win rates. Compare consistency in underlying plan identity.

Use a fixed complete presentation of dates, times, places, notes, and displayed amounts.
Hide version labels, canonical IDs, provider metadata, findings, repair status, and Nearby.
Do not rewrite with an LLM, remove meaningful uncertainty, fix false claims, or omit dates.
Blinding reduces label bias but cannot guarantee that style/content never reveals a version.

Ask which plan better matches preferences, requested pace/travel style, and practical usefulness.
Use A/Tie/B, with N/A where a dimension is not meaningfully applicable. Report unique case
counts, V2 wins, ties, V3 wins, unavailable/N/A counts, and raw duplicate consistency. Consistency
is not proof of validity. Exact presentation and sample allocation remain specification work.

## 13. Official Evidence Audit

Trigger audit only when **Evidence Gate accepted** a fact and it was either:

- `exposed_to_model`: actually supplied to a generation or repair model; or
- `used_by_rule`: actually adopted by a deterministic rule.

These are observable adoption/exposure states, not proof of causal LLM use. Searches,
retrievals, rejected facts, and unused log entries alone do not trigger audit. No random
official-website cross-check is planned.

Audit the fact, not an entire trip. Preserve identity, source URL/domain, claim, applicable
time and subject scope, planner observation time, supporting excerpt/snapshot where available,
and exposure/rule-use location. Rechecking is independent; the planner's accepted label does
not establish the audit answer.

Report qualifying fact count, audited count, supported, contradicted, scope mismatch, and
unavailable-to-recheck outcomes. Preserve planner_observed_at and evaluation_recheck_at.
A later unavailable or changed page does not establish that the earlier observation was false.

Keep this audit separate from the main Google opening denominator. Report supported official
evidence disagreements with Google without silently substituting evidence for one version.
This audit does not measure the overall accuracy of Google or completeness of unused sources.

## 14. Metrics register

READY means the current contract provides a usable basis, **not** that an evaluator exists.
OPEN requires specification and/or recording work. DEFER excludes a verified v1 result until
separately authorized. REMOVE means excluded as a primary RTPEval v1 metric.

| Metric group | Status | Data and interpretation |
| --- | --- | --- |
| Run outcomes | OPEN | Collector; produced, clarification, invalid input, timeout, model/provider/schema/internal failure, cancellation; degradation is an additional attribute, not double-counted completion |
| Date coverage and raw activity counts | READY | Request/output; distinguish day present, any activity, main visits, and empty day; empty is not automatic failure |
| Canonical grounding | OPEN | Independent identity mapping; verified, ambiguous, unresolved, wrong association; role/adjudication rules pending |
| REQUIRED/EXCLUDED and date/count obligations | OPEN | Independent requirement specification and identity; no runtime interpreter ground truth |
| Fixed-time satisfaction | OPEN | Specification intervals and activity semantics |
| Overlap | OPEN | Independent interval calculation; report affected requests, pairs, and union conflict duration rather than summed pairwise minutes as actual elapsed overlap |
| Opening coverage/compliance | OPEN | Independent snapshot and frozen interval policy; separate current/date-specific and regular basis |
| Route evaluability/coverage/feasibility | OPEN | Independent directed evidence and explicit mode/departure/occupancy contract |
| Transfer burden | OPEN | Observed durations, deficit, median/max/subtotal with coverage; no zero for missing legs |
| Density and occupied time | READY | Distinct visits/day and interval-union occupied time; 2-5 is guidance, not hard validity; role details remain open |
| Canonical repetition | OPEN | Independent identity and visit obligations; describe within/across-day repetition without equating it to error |
| Repair attempts/rounds/acceptance/stops | READY | Mechanism metadata only; denominators distinguish eligibility, attempted calls, and parsed/adopted proposals |
| Independent repair outcomes | OPEN | Independent before/after facts, target definitions, correspondence and invariants |
| V3 pre/post artifacts | READY | Successful result retains draft/final_primary; collector must preserve both and record unavailable pairs |
| RAG exposure | READY | Initialization, embedding/retrieval status, degradation, candidate fates; distinguish RAG-only and mixed-source identities, not causal contribution |
| Calls/tokens/provider elements/latency | OPEN | Unified actual-call accounting; missing usage is not zero; avoid round/aggregate double counting |
| Human pairwise | READY | Accepted single-rater design; exact presentation and sampling pending |
| Official evidence audit | OPEN | Accepted-and-exposed or rule-used fact provenance and independent audit |
| Verified travel cost/budget | DEFER | No verified coverage, subtotal, or whole-trip PASS as v1 main metrics; model amounts may be descriptive |
| Small factual claim audit | DEFER | Optional exploratory human work, not required v1 scope |
| Automated False Certainty/public access accuracy | REMOVE | No adequate common assertion/access contract; do not add fictional fields |
| Whole-trip budget PASS/composite score | REMOVE | Not primary metrics |

Any future factual claim audit must distinguish supported, unsupported by evaluation evidence,
contradicted, and evidence conflict. Unsupported does not mean false.

Do not collapse verification coverage across unrelated checks into a single quality score.
Opening, routes, identities, and requirements have different units and applicability.

## 15. Resource accounting and observability

Keep planner and evaluator costs separate. Record interpretation, primary generation,
Reviews/ExperienceProfile, Web/reasoning, embedding, repair, and Nearby work where applicable.
Distinguish model calls, actual provider sends, cache hits, processing attempts, and requested
route matrix elements. Missing usage must remain missing. Monetary estimates, if later added,
need a dated pricing basis and must not be called billing facts.

Measure actual elapsed total/primary/repair/Nearby times rather than deriving latency from
deadlines or remaining budgets. Define treatment of failures and timeouts; do not report only
successful-run cost. Cumulative and per-round usage require explicit deduplication.

Current implementation risks to resolve through the readiness audit include:

1. V0 recording is not symmetric with V1-V3; its shared result does not retain the full
   interpreted contract or equivalent trace by default.
2. FileRunTracer is best-effort and bounded; metadata defaults and payload truncation can
   remove required artifacts. Persist and verify complete results outside summaries.
3. V3 has draft/final and round records, but failure paths may not have complete pairs;
   timing fields are not a universal measured-latency contract.
4. Official fact projection records exposure, not causal LLM influence; retain source-to-fact
   links independently of summary counts.
5. Source changes, effective CLI configuration, model identity, and actual vector corpus
   state need complete provenance; an upstream dataset manifest is not a database backup.

Use approved outer collection, passive client observation, and explicit artifact extraction
to close gaps without changing planning algorithms. Do not infer unobservable semantics or
causal effects from added logs. Missing provider metadata remains unavailable.

## 16. Analysis plan and result reporting

The request is the paired comparison unit. The 36 requests' first run per version constitute
the proposed main analysis; optional repeats are a separate sensitivity analysis. Visits and
legs may contribute descriptive micro-counts but are not independent experimental samples.

Report all-run outcomes alongside conditional itinerary quality. For paired quality differences,
state which pairs are available and how missingness affects interpretation; do not hide a
version's failures by presenting only the common successful subset.

Use city, length, and query type for stratified descriptions. Account for repeated requests
and city clustering in the chosen uncertainty method, without claiming precise generalization
from six cities. Exact statistical tests, primary comparisons, aggregation, confidence intervals,
and any multiplicity treatment remain OPEN, but must be specified before held-out results
are revealed. Development data and predefined applicability rules may inform that choice.
Post-result additions are exploratory, not retrospectively preregistered.

Planned reporting groups are run outcomes, E2E quality, computational cost, repair mechanism
and independent outcomes, V3 pre/post, human pairwise, and qualifying official-fact audit.
Do not include a verified travel-budget table as a v1 main result. Preserve raw denominators
and reason distributions alongside aggregated rates, medians/IQRs, or means where meaningful.

## 17. Matched checkpoint, freeze, and change control

Record the complete source commit/tree hash, dependency lock, model deployment/available
actual identity, inference settings, prompt/schema hashes, effective configuration and CLI
overrides, full materialized requests, TripWorld corpus/vector state, embedding identity,
tool configuration, budgets, deadlines, retries, environment, concurrency, execution order,
and cold/warm assumptions.

Equal tool-call counts are not required: added mechanisms incur added costs. Do not grant
case-specific budgets or selective reruns after observing results. Full request fingerprints
must include preference text; the existing structured request hash alone is insufficient.

Freeze dates in two layers: first request templates and the materialization rule, then the
actual dated batch with hashes immediately before execution. Respect the actual product
date window and maximum trip duration. If the valid window is missed, create a new batch;
do not silently edit dated requests while retaining their old identity.

Approved development dry runs occur before final held-out freeze. They validate evaluator
semantics, identity handling, snapshots, accounting, and reports. Any planner tuning using
those cases preserves their development status.

Version and hash requests, specification/protocol, evaluation configuration, analysis plan,
evaluator implementation, identity/adjudication records, outputs, and snapshots as appropriate.
Exact artifact names and serialization conventions remain specification items.

After formal execution begins:

- Evaluator bug: retain old/new evaluator versions and rescore valid existing artifacts
  offline across the affected slice.
- Planner bug: record checkpoint changes and rerun affected versions/cases determined by
  impact, not by whether a result was poor.
- Oracle acquisition bug: version the correction, restore matched evidence consistency,
  and document temporal limitations of recollection; never silently change one version's facts.

## 18. Open-item register and next step

| Open item | Required resolution |
| --- | --- |
| Final engineering checkpoint | Readiness audit after V3 completion; no current version freeze implied |
| E2E/default and controlled capability configuration | Final supported operations, review flags, limits and deadlines |
| Opening contract | Timezone, periods, overnight, exceptions, exterior, precision and unknown states |
| Route contract | Mode, occupancy, continuous intervals, departure/waiting, statuses, fallback, buffers and partial evidence |
| Requirement specification | Independent format, exact/minimum/date obligations and unsupported semantics |
| Place-bearing roles and identity | Eligibility, resolution, adjudication budget, automatic-match audit and correspondence |
| Run outcomes | Mutually understandable terminal categories, degraded attributes and missing-artifact handling |
| Controlled targets/controls | Actual V3 entry boundary, fixtures, permitted invariants and evidence coverage |
| Held-out cities and requests | Exposure/coverage eligibility, request/length/tag allocation and boundary-case policy |
| Optional repeats | Development-based choice of 144 or 192 runs; no current priority over more unique cases |
| Evidence acquisition | Snapshot budget, batching, retries, time lag, failure records and persistence |
| Official audit | Accepted-and-exposed/rule-used extraction, provenance and independent audit workflow |
| Human presentation | Exact renderer, preselected 12 cases/run choice, three duplicates and unavailable/N/A handling |
| Analysis plan | Main paired comparisons, aggregation, missingness, city/repeat handling and uncertainty methods |
| Observability | Complete artifacts, actual usage/timing, provider metadata and integrity checks |
| Date batch and hashes | Materialization, validity window, artifact identities and reproducibility manifest |

The next post-engineering task is **Evaluation Readiness Audit**, followed by an approved
RTPEval v1 Specification. Implementation and development dry runs require subsequent approval.

## 19. Relevant current repository references

- [Project context](../PROJECT.md)
- [Shared itinerary output](shared_itinerary_output.md)
- [Shared requirements](shared_requirements.md)
- [V3 design and chronological checkpoints](v3_design.md)
- [Public itinerary schema](../backend/app/schemas/itinerary.py)
- [Interpreted requirement schema](../backend/app/schemas/interpreted_requirements.py)
- [V3 pre/post result](../backend/app/versions/v3/state.py)
- [Repair and round records](../backend/app/versions/v3/repair_models.py)
- [Official model-input projection](../backend/app/versions/v1/official_planner.py)
- [Official fact provenance](../backend/app/evidence/official_models.py)
- [Request-local cache](../backend/app/runtime/cache.py)
- [Run tracing](../backend/app/observability/run_trace.py)
- [Runtime configuration](../config/runtime.yaml)

These references describe implementation evidence, not independent evaluation ground truth.
Their existence does not mean RTPEval has been implemented or validated.
