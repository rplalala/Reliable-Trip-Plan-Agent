# RTPEval evaluator research design

Shared terminology: [Evaluation glossary](evaluation_glossary.md).

Status: **ACCEPTED WITH SPECIFICATION ITEMS OPEN**

Decision recorded: 2026-09-24.

## 1. Authority, status, and authorization

This document records the research design accepted by the user after two code-informed
reviews. It is the accepted basis for a later RTPEval v1 Specification. The overall research
architecture is settled; remaining work concerns explicit specification items, not another
overall redesign.

This is **not Benchmark Frozen**, not a completed evaluation specification, and not
implementation authorization. V3 engineering closed on 2026-09-25; later shared and V0
changes are recorded in PROJECT.md. Acceptance of this design does not freeze V3 or any
earlier version, demonstrate a research result, or authorize formal
experiments or thesis writing.

[PROJECT.md](../PROJECT.md) remains the current project-level source of truth. This document
owns the accepted evaluation design and its open decisions. Current implementation must be
checked again at the final engineering checkpoint; historical proposals and development
captures do not override the actual code or current project context.

Separately requested specification design may proceed for opening,
routes, requirements, identity adjudication, run outcomes, controlled cases, human presentation,
and the analysis plan. Do not implement an evaluator, create formal benchmark cases, run
experiments, or modify planning algorithms to accommodate evaluation under this approval.

With V3 engineering closed, the first step is an **Evaluation Readiness Audit** against the
current actual checkpoint. The [2026-09-28 audit](evaluation_readiness_audit.md) begins that
work. Resolve the open items into a formal RTPEval v1 Specification, obtain
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
Present the final V3 system first and use the independent V0-V3 runs as incremental system
comparisons. Use the existing independently runnable V0-V3 paths; no additional strict
single-module ablation study is planned.

### 2.1 Supplementary comparison: V3 vs Codex + Travel Planning Skill

Status: **ACCEPTED WITH SPECIFICATION ITEMS OPEN**. Direction recorded: 2026-09-25.

Add **V3 vs Codex + Travel Planning Skill** as a supplementary comparison of how the two
systems perform travel-planning tasks. It complements the main V0-V3 study; it does not
replace that study or establish a pure causal effect of harness differences.

For now, only this comparison direction is accepted. Tool access, environment isolation,
sample size, and execution configuration remain open for later specification. This addition does
not freeze the benchmark or authorize skill/evaluator implementation or experiments.

## 3. Stable design principles

- No unique Gold itinerary: multiple choices of places and schedules can be valid.
- Fixed requests, independent evidence, independent rules, and multiple metrics replace
  reference-itinerary text matching.
- Independent judgement and independent evidence collection are required.
- Google is frozen external evidence, not absolute real-world truth.
- Human-reviewed benchmark requirements are evaluation inputs, not injected E2E planner inputs.
- Report multiple metrics; do not create a primary weighted composite score.
- Dimension subscores and an auxiliary reliability/constraint-compliance total may be designed for presentation;
  their normalization, weights, coverage gates and missingness rules must be fixed before
  held-out results are revealed. They do not replace the primary metric vector.
- Score only groups where all four versions completed their prescribed workflows; disclose all attempts and exclusions separately from benchmark scores.
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
| Batch Intake | Validate a user-submitted batch and its artifact integrity; consume benchmark-owned collection records without rerunning workflow eligibility |
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

## 6. Batch handoff and scope boundary

Each group delivers four separate complete result files: `v0_result.json`, `v1_result.json`, `v2_result.json`, and `v3_result.json`. Do not combine four results into one JSON file. The manifest references each file and hash; the adapter extracts its itinerary while isolating internal findings from quality scoring and human presentation.

RequirementSpec is prepared during benchmark construction from the original Input, with assistant drafting permitted and explicit user review required. Evaluation only consumes the reviewed artifact: it does not generate, infer, repair or silently complete obligations. Missing, unreviewed or structurally invalid specifications produce intake diagnostics for upstream correction; explicitly recorded unresolved semantics remain unresolved.

[Benchmark construction](benchmark_design.md) owns input design, planner execution,
workflow-completion admission, failure reasons and iteration recommendations. Only the user
can authorize planner iteration. Sample counts and construction policy are outside this module.

Evaluation starts after the user has curated and handed over a versioned batch of qualifying
groups; it is not triggered whenever one group qualifies. Each group supplies the original
input and four final itineraries. Human-reviewed requirements support independent checks;
optional usage and V3 draft artifacts support additional reports. The detailed contract is in
the [module specification](../.scratch/rtpeval/spec.md).

Evaluation validates delivered materials and integrity, not execution eligibility. Missing or
invalid mandatory materials produce an intake diagnostic and require a corrected batch; the
module does not silently drop groups, run planners, fill missing results or select replacements.
Controlled Repair remains a separate V3-only evaluation track, outside the four-version gate.

## 7. Requests, identity, and common scoring semantics

### 7.1 Human-reviewed requirements

The evaluation specification must independently state relevant named identities, inclusion
rules, mandatory dates, visit counts, fixed unavailable intervals and supported transport requirements,
without distinguishing exterior viewing from venue entry. It must follow the actual request, not the planner's interpretation.
It is not injected into E2E planning.

Distinguish minimum count, exact count, and date obligations. Exceeding a minimum is not a
revisit violation. If exact-count or other semantics exceed the final product contract,
record that boundary rather than silently treating them as supported.

### 7.2 Identity adjudication

The [identity contract draft](../.scratch/rtpeval/identity-contract.md) specifies provider
capabilities, adjudication records and uncertainty propagation. An adjudicated named venue
may support downstream checks despite a conflicting supplied ID, but the ID error is
reported separately and the original output is not corrected. Uncertain identity remains UNKNOWN.

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

The [activity scope contract draft](../.scratch/rtpeval/activity-scope-contract.md) separates
visit counts from time occupancy and route legs. Uncommitted locationless free-time use and same-canonical route N/A are accepted.
Inter-day travel is outside v1 route scope; no planner role summary determines the independent denominators.

For each applicable metric retain raw counts, numerator, denominator, unknown/not-applicable
counts, and reason distributions. Do not turn UNKNOWN into an observed zero value, a FAIL or an empty-denominator
100 percent compliance. UNKNOWN earns no verified-success credit under the accepted score formula.

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

Benchmark construction owns planner execution and its balanced/randomized order. After the
user submits a curated batch, Evaluation constructs each group's union, acquires independent
evidence and scores offline. It does not run planners; preserve planner-to-oracle lag.

The union includes V0/V1/V2 finals, V3 final_primary, V3 pre-repair draft, and specification
identities needed for REQUIRED/EXCLUDED checks. Include round proposals/adopted outputs only
if independent round-level scoring is separately specified. Only admitted four-version
groups enter snapshot acquisition and comparative benchmark scoring.

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

The [opening contract draft](../.scratch/rtpeval/opening-contract.md) captures interval and
evidence semantics. Zero grace is accepted: ending exactly at closing is compliant,
and any positive overrun remains recorded. A known special-date exception without usable applicable hours yields UNKNOWN, with a
specific explanation and evidence references; regular hours cannot silently replace it.

Report current/date-specific evidence, regular weekly fallback, and unavailable/uninterpretable
evidence separately. Compliance means full scheduled-interval containment in adopted hours;
it does not establish ticket ownership, reservations, eligibility, or special-area access.

Do not use open_now for future visits. Missing periods are not closed, and explicitly closed
periods are not missing. Longer trips naturally extend beyond the current-hours window;
report evidence basis rather than treating regular fallback as equally date-specific.

Freeze rules for timezone/offset conflicts, multiple periods, overnight visits, special-date
fallback, missing/invalid/closed evidence, and boundary precision/tolerance.
Entry/exterior distinctions are outside v1; do not infer an opening exemption from access wording.
Public Activity currently has no general per-visit access-mode field, so evaluation assumptions
must be explicit and version-neutral rather than borrowed from V3 bindings.

### 9.2 Routes

Use valid Google-returned route durations even when traffic calculation falls back; retain
fallback metadata but do not introduce a separate traffic-fidelity UNKNOWN. This does not
permit wrong endpoints/modes or fabricated durations. No-route and service-failure rules,
product DRIVE reserve and the two five-minute tolerances remain unchanged.

Successful applicable evidence explicitly reporting no route is FAIL; provider failure,
timeout or incomplete evidence is UNKNOWN with reasons. No-route FAIL has no invented
numeric deficit. A five-minute Routes tolerance applies separately to both mode duration caps and schedule
deficits, never as a summed ten-minute allowance. Preserve raw values; it does not change
Opening's zero-grace rule, WALK distance limits or the product DRIVE reserve.

The [route contract draft](../.scratch/rtpeval/route-contract.md) records checked adapter
capabilities and continuous interval/evidence semantics. Stated-mode evaluation and zero
extra evaluator buffer are accepted. Reconstruct the two-POI window independently, using
the single unblocked interval at the actual departure rather than summing fragments.

Compare usable provider duration with an applicable continuous travel interval. Do not sum
disjoint free intervals across fixed commitments. Freeze departure and waiting semantics,
especially for TRANSIT and traffic-sensitive DRIVE.

Also freeze default mode and explicit overrides; intermediate real activities; elastic
free_time versus protected rest; explicit transport activities; unknown-location activities;
route-not-found versus provider failure, invalid status and fallback; same canonical versus
same-address places; overnight transitions; and any evaluator transfer buffer.

Apply only explicitly accepted, frozen product thresholds independently across all versions.
Include the product DRIVE reserve of 10 minutes, with zero additional evaluator buffer;
report it separately from provider duration. Do not reuse V3 verdicts as ground truth.
If mode is an evaluation assumption rather than an output claim, label the resulting metric
as feasibility under that assumption. Missing routes never contribute zero minutes.

With partial route evidence, report observed transfer subtotal and observed maximum, not a
complete trip burden. Exact adjacency, eligibility, batching, departure applicability, and
evidence conflict rules remain OPEN.

## 10. Controlled Repair

This retained V3-only mechanism study is separate from the four-version E2E benchmark.
It does not require four-version-complete groups and does not contribute to their scores.

The accepted composition is **24 target cases + 8 control cases**, subject to final
capability verification. Eight target families with three examples each are sparse day,
duplicate visits, overfull day, overlap, opening conflict, route conflict, REQUIRED omission,
and EXCLUDED inclusion.

Separate confirmed-conflict targets from review/improvement targets. Sparse, Duplicate,
and Overfull are not automatically confirmed defects. Three examples per family support
mechanism diagnosis, not a precise family-level success estimate.

Controls cover no authorized modification, explicit revisits, legitimate relaxed low density,
reasonable high density, opening-boundary cases, missing opening evidence, missing route evidence,
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

Every V3 attempt is retained in the execution ledger. Within admitted E2E groups, only
runs with both valid before and after artifacts enter paired analysis. Identical outputs have delta zero; missing pairs are
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

### Automatic checks and human judgment

Programs perform explicit, reproducible checks; raters judge preference fit, pace appropriateness and practical usefulness. The Evaluation module supports both tracks, but does not replace the rater's subjective judgment with an inferred numerical proxy.

| Area | Automatic responsibility | Human responsibility |
| --- | --- | --- |
| Explicit requirements | Reviewed required/excluded visits, dates, minimum/exact counts and supported explicit time constraints | No routine recounting or compliance audit requested from the rater |
| Schedule and evidence | Overlap, date coverage, independently resolved identity, opening and route checks under frozen rules; preserve UNKNOWN where evidence is insufficient | No external fact lookup or route arithmetic required |
| Pace and preference | Descriptive POIs/day, occupied time, observed transfers and supported categories; no inferred preference PASS | Judge preference match and whether the plan's pace fits the original request |
| Practical usefulness | Report relevant observations without equating compliance with usefulness | Holistic usefulness ranking from original input and anonymous plans |
| Resources | Aggregate reported tokens, measured latency and provider usage; retain missingness | Not part of the rater's task |
| Ambiguity | Identify unresolved evidence/identity and retain audit records | Separate adjudication may resolve ambiguous identities or review requirements; this is not the blinded preference task |

A numerical description is not automatically a quality score. For example, fewer POIs, fewer transfers or fewer repeats need not be better. Do not translate "relaxed" into an invented daily cap or "distinctive architecture" into a fabricated deterministic label. Explicit quantitative constraints can be checked only when reviewed and supported by a specified rule. Rule applicability, evidence coverage and compliance remain separate.

Blind presentation withholds the automatic scores and RequirementSpec. Rankings use preference match, pace and usefulness with ties; unable-to-judge and N/A remain distinct. Human answers never supply missing opening/route facts or feed the auxiliary automatic total.


### Illustrative division of work

Example request: "Plan three days in Paris. I must visit the Louvre, do not include Versailles, and prefer a relaxed trip."

| Program checks | Rater judgments |
| --- | --- |
| Requested date coverage; whether the Louvre is scheduled and Versailles is excluded | How well the itinerary matches the stated preferences |
| Activity overlap, opening compliance and route feasibility against the frozen evidence | Whether the itinerary feels appropriately relaxed |
| Recorded tokens, elapsed time and tool usage | Which plan would be more useful to follow |

The program may describe "three POIs per day and 50 observed transfer minutes," but those numbers alone do not establish that the plan is relaxed. The rater makes that judgment from the original request and anonymously presented itinerary. Unavailable external evidence remains UNKNOWN; the rater is not asked to look it up. This is a documentation example, not a benchmark case, collected observation or evaluation result.

The 2026-09-28 decision expands human evaluation to **V0-V3**, superseding the V2/V3-only
pairwise design. Use one rater and support hidden duplicate tasks for intra-rater consistency.
The earlier 12-case/three-duplicate proposal is a sampling reference, not a module quota. This is complementary exploratory subjective
evidence, not population-level user preference evidence. Report the rater's relationship to
the project and the limits of single-rater assessment. Do not report inter-rater agreement.

Preselect cases using stated strata. Choose the compared run deterministically in advance
rather than selecting the best repeat. Human assessment consumes the same submitted batch as automatic evaluation (Section 6),
then applies an explicitly supplied sampling policy without independently selecting successful runs.
All four versions must complete their prescribed workflows. Normal V3 stopping can remain
eligible despite unresolved quality problems; cap-truncated pending Repair cannot.
Report attempted, excluded and retained counts separately from benchmark scores. Human and
automatic conclusions both concern the selected complete-group cohort. Internal workflow
completion determines admission, not independent quality judgments.

Anonymous labels and display order must be reassigned across cases
and hidden duplicates; freeze a balanced/randomized assignment procedure. Space duplicate tasks
apart and never count them twice toward results. Compare consistency by underlying plan identity.

The rater receives only the original request and uniformly presented anonymous itineraries;
do not reveal version mechanisms, hypotheses, automatic scores, oracle evidence or internal
RequirementSpec. Use a fixed complete presentation of dates, times, places, notes, and displayed amounts.
Hide version labels, canonical IDs, provider metadata, findings, repair status, and Nearby.
Do not rewrite with an LLM, remove meaningful uncertainty, fix false claims, or omit dates.
Blinding reduces label bias but cannot guarantee that style/content never reveals a version.

Ask which plan better matches preferences, requested pace/travel style, and practical usefulness.
The accepted response format is a simple HTML questionnaire. Each request forms one group
of four anonymously labelled itineraries A/B/C/D. The rater ranks all four separately for
preference match, pace, and practical usefulness, allowing ties (for example A = C > B > D).
Keep the labels consistent across the three dimensions within a group and reassign them
across groups. Keep the version mapping outside the rater-facing HTML and exported answers.
Preserve ties, unable-to-judge responses and N/A as distinct states. Derive per-version-pair
wins/ties/losses separately for each dimension, stating evaluable denominators. Do not turn
unable-to-judge or N/A into ties. Multiple pair comparisons from one group are correlated,
not independent request samples. Hidden duplicates contribute only to consistency checks.
Report unique-case counts and raw duplicate consistency, which is not proof of validity.
Answer persistence and export details remain specification items.

Development failures may guide later authorized planner changes. A request used to diagnose
or tune a planner becomes development-exposed; it cannot retain untouched held-out status.
If formal runs expose a genuine bug, record the checkpoint and affected slice under Section 17,
retain original outcomes, and distinguish reruns. Do not mix old/new checkpoints or tune on
excluded test cases and present only the subsequent successes as original held-out evidence.

The user's example of 20 inputs means 20 groups and 80 itineraries, not 80 independent
request samples. This is a scale illustration, not a replacement of the current 12-case
earlier sample proposals. Final counts and selection are supplied by later benchmark design.
HTML implementation and participant assessment are not authorized by this design decision.

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

A separate [score profile proposal](../.scratch/rtpeval/score-profile.md) describes candidate
five accepted equal-weight dimensions and accepted PASS/(PASS+FAIL+UNKNOWN) verified
credit. Unknown rate is UNKNOWN/N; verification coverage is (PASS+FAIL)/N. Group-wide N/A removes a dimension jointly; single-version no-check N/A contributes zero
under the shared weights, without becoming FAIL; no total is implemented or retrospectively fitted to results.

The [unified metrics contract](../.scratch/rtpeval/metrics-contract.md) expands this overview
with sources, units, denominators, states and accepted tolerances. It records OPEN aggregation
and score formulas rather than inventing them. Qualified primary visits have one POI and an
explicit time interval; multi-POI blocks are intake diagnostics, not automatically split visits.

READY means the current contract provides a usable basis, **not** that an evaluator exists.
OPEN requires specification and/or recording work. DEFER excludes a verified v1 result until
separately authorized. REMOVE means excluded as a primary RTPEval v1 metric.

| Metric group | Status | Data and interpretation |
| --- | --- | --- |
| Run outcomes | EXTERNAL INPUT | Benchmark-owned ledger; produced, clarification, invalid input, timeout, model/provider/schema/internal failure, cancellation; degradation is an additional attribute, not double-counted completion |
| Date coverage and raw activity counts | READY | Request/output; distinguish day present, any activity, main visits, and empty day; empty is not automatic failure |
| Canonical grounding | OFFLINE IMPLEMENTED | Ticket 03 independent identity replay reports verified, unresolved and supplied-ID conflict counts; live evidence acquisition remains Ticket 04 |
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
| Human four-version blind assessment | OPEN | V0-V3; HTML groups A/B/C/D with per-dimension rankings allowing ties; per-pair wins/ties/losses accepted; presentation details and sample selection remain open |
| Official evidence audit | OPEN | Accepted-and-exposed or rule-used fact provenance and independent audit |
| Verified travel cost/budget | DEFER | No verified coverage, subtotal, or whole-trip PASS as v1 main metrics; model amounts may be descriptive |
| Small factual claim audit | DEFER | Optional exploratory human work, not required v1 scope |
| Automated False Certainty/public access accuracy | REMOVE | No adequate common assertion/access contract; do not add fictional fields |
| Auxiliary reliability/constraint subscores and total | DESIGN ACCEPTED | Five equal-weight verified-compliance scores, shared N/A mask and individual N/A zero contribution; implementation/technical applicability and analysis plan not frozen |
| Whole-trip budget PASS | REMOVE | Not a primary metric |

Any future factual claim audit must distinguish supported, unsupported by evaluation evidence,
contradicted, and evidence conflict. Unsupported does not mean false.

Do not collapse verification coverage across unrelated checks into a single quality score.
Opening, routes, identities, and requirements have different units and applicability.

## 15. Resource accounting and observability

The accepted handoff contains separate `v0_usage.json` through `v3_usage.json` alongside
results. Benchmark execution must supply uniform collection; this remains an engineering
gap, not implemented functionality. Evaluation reads and aggregates records, distinguishing
missing observations from zero and Repair subsets from totals. The detailed delivery and
collection requirements are in the module specification and benchmark design. Missing usage
is a resource diagnostic, not a new planner-completion or itinerary-quality decision.

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

The request is the paired comparison unit. Selected primary runs are declared in the supplied
batch manifest; optional repeats, if specified, are a separate sensitivity analysis. Visits and
legs may contribute descriptive micro-counts but are not independent experimental samples.

Report benchmark quality only for admitted four-version-complete groups. Separately disclose
all attempted groups and exclusions, without scoring excluded outputs or treating them as zero.
For paired quality differences, state available pairs and missingness within the admitted
cohort. Selection limits all quality claims to that cohort; it does not establish all-request superiority.

Use city, length, and query type for stratified descriptions. Account for repeated requests
and city clustering in the chosen uncertainty method, without claiming precise generalization
from six cities. Exact statistical tests, primary comparisons, aggregation, confidence intervals,
and any multiplicity treatment remain OPEN, but must be specified before held-out results
are revealed. Development data and predefined applicability rules may inform that choice.
Post-result additions are exploratory, not retrospectively preregistered.

Planned reporting groups are run outcomes, E2E quality, computational cost, repair mechanism
and independent outcomes, V3 pre/post, four-version human blind assessment, and qualifying official-fact audit.
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

## 18. Open-item register and next step — 2026-09-28 checkpoint

| Open item | Required resolution |
| --- | --- |
| Final engineering checkpoint | Readiness audit after V3 completion; no current version freeze implied |
| E2E/default and controlled capability configuration | Final supported operations, review flags, limits and deadlines |
| Opening contract | Timezone, periods, overnight, exceptions, precision and unknown states |
| Route contract | Mode, occupancy, continuous intervals, departure/waiting, statuses, fallback, buffers and partial evidence |
| Requirement specification | Independent format, exact/minimum/date obligations and unsupported semantics |
| Place-bearing roles and identity | Eligibility, resolution, adjudication budget, automatic-match audit and correspondence |
| Run outcomes | Mutually understandable terminal categories, degraded attributes and missing-artifact handling |
| Controlled targets/controls | Actual V3 entry boundary, fixtures, permitted invariants and evidence coverage |
| Benchmark construction | External responsibility; see the separate benchmark design |
| Batch membership | Supplied by the user; no evaluator sample-size quota or automatic replenishment |
| Evidence acquisition | Snapshot budget, batching, retries, time lag, failure records and persistence |
| Official audit | Accepted-and-exposed/rule-used extraction, provenance and independent audit workflow |
| Human presentation | Exact renderer/storage and supplied sampling configuration; benchmark design owns final counts |
| Analysis plan | Main paired comparisons, aggregation, missingness, city/repeat handling and uncertainty methods |
| Observability | Complete artifacts, actual usage/timing, provider metadata and integrity checks |
| Date batch and hashes | Materialization, validity window, artifact identities and reproducibility manifest |

At this checkpoint, the intended task was to complete the RTPEval v1 module specification
and resolve its explicitly OPEN contracts. Later Ticket 01-03 offline implementation states
are recorded in Sections 22-25; formal runs still require separate authorization.

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
At this design checkpoint, their existence did not mean RTPEval had been implemented or validated.

## 20. Technical contract checkpoint — 2026-09-28

[Artifact and human-answer contract](../.scratch/rtpeval/artifact-contract.md) defines batch integrity, per-version result/usage linkage, RequirementSpec serialization, report states and blinded ranking persistence. [Evidence and time contract](../.scratch/rtpeval/evidence-time-contract.md) defines timezone/period parsing and independent route-response classification with provider references.

Use valid returned Google route durations, including traffic-calculation fallback, with the accepted product caps/reserve and tolerances. Generic no-POI activities are free-time/transition-like; protected time and concretely named unresolved visits retain their separate meaning. No additional quality dimension is introduced.

Core contracts can now support task decomposition. Usage instrumentation, identity acceptance/audit validation, transport correspondence, mechanism extraction and Controlled Repair invariants remain dependent work. No evaluator, renderer, fixtures, benchmark or experiments were implemented by this documentation pass; the specification is not frozen.

## 21. Published work plan and pause checkpoint — 2026-09-28

The user approved the [12-ticket work plan](../.scratch/rtpeval/ticket-breakdown.md); individual issues are published. Nine retain needs-info; 06, 08 and 09 have specification-ready status but unresolved predecessor dependencies. Neither status nor publication authorizes implementation.

Before each implementation, resolve its technical information gaps using current code and accepted contracts. Ask the user only for decisions that affect result meaning and cannot be derived from existing agreements. Common definitions must be settled before dependent modules diverge; dependency waiting alone belongs in Blocked by. No broad redesign or repeated interview is required.

Resource reports supply objective measurements and descriptive comparisons for the researcher's later thesis/presentation analysis. They are not a new non-blind human rating stage, an efficiency PASS threshold or part of the itinerary quality total. The rater sees only original Input and anonymous plans; formal analysis and thesis writing remain separately authorized work.

The user requested a pause after documentation updates. Next intended work is specification closure for Ticket 01; it has not started. No evaluator implementation, formal cases, live acquisition, experiments or freeze occurred. Historical design records are preserved separately under thesis_notes/evaluation and thesis_notes/benchmark; current authority remains PROJECT.md and the active design/specification documents.

## 22. Ticket 01 specification closure — 2026-09-29

The user authorized closing the batch intake/projection specification. The [contract](../.scratch/rtpeval/intake-projection-contract.md) defines material errors versus content uncertainty, versioned source-preserving reading, role-review records and same-day transport association. V0 text-based transport and application-owned Transfer are supported without granting either privileged truth. Clearly corresponding duplicate journeys count once; segments and conflicting claims retain their meaning and provenance. Unclear roles/associations remain reviewable or unresolved rather than silently dropped.

Ticket 01 is now specification-ready. This supersedes the earlier pause for specification work only; no implementation or tests were performed, and the overall RTPEval specification is still not frozen. Remaining scoring/identity/usage/Repair contracts retain their own readiness gates.

## 23. Ticket 01 offline implementation — 2026-09-29

The user separately approved Ticket 01 implementation. [Offline intake and projection](../backend/evaluation/README.md) now reads a curated batch, validates material linkage, preserves immutable source references and projects independent roles/transport claims. It does not import planner judgments or run any planner/provider. Independent review handles ambiguous prose; this is not automatic semantic understanding of every itinerary.

[Acceptance](../.scratch/rtpeval/ticket-01-acceptance.md): 38 tests passed, one native Windows symlink test skipped because creation privileges are unavailable; traversal/resolved-path guard checks passed. Ruff and CLI checks passed. Ticket 01 is resolved. No quality scoring, oracle acquisition, usage instrumentation, blind HTML, formal cases or experiment was implemented. Subsequent tickets and benchmark freeze remain separately authorized.

## 24. Usage capture and resource reports — 2026-09-29

Ticket 02 is implemented under separate authorization. The [producer capture guide](../backend/app/observability/USAGE.md) provides one opt-in invocation/cleanup boundary across versions, exact-byte result linkage, request-local model/provider/cache events and Repair subsets. Tokens are provider-reported or explicitly derived; missing usage is not zero. Client hooks are active only during capture and restore existing client state after the last capture owner ends.

Researcher reports compare the four selected envelopes per request with differences, ratios and descriptive medians. Missing/zero baselines and incompatible scope remain explicit; usage does not affect quality scores or blind rankings. Ordinary scripts do not automatically create sidecars; benchmark construction must enable capture and verify saved artifacts.

[Offline acceptance](../.scratch/rtpeval/ticket-02-acceptance.md): initial four hook-cleanup regression failures were corrected. Broad retest passed 944 with one Ticket 01 native symlink skip; latest usage/evaluation subset passed 51 with the same skip. No provider/model/database service was used and no benchmark was frozen. Arbitrary injected client coverage and live completeness remain unverified.

## 25. Ticket 03 offline identity implementation — 2026-09-29

The user approved strict, version-neutral identity association: supplied IDs require independent details checking of returned ID, name and destination; name-only references use independent search with exact name, sufficient destination/address evidence and no observed competition. Alias/translation, branches, ID/name conflicts, insufficient evidence and potential REQUIRED/EXCLUDED matches require factual review. A predeclared audit plan selects automatic proposals for manual checking. The [implementation contract](../.scratch/rtpeval/identity-implementation-contract.md) records conservative search scope, review replay and report semantics.

Ticket 03 now replays offline independent observation files against Ticket 01 source-linked primary visits and reviewed requirement subjects. It separates grounding from supplied-ID consistency, keeps sampled automatic proposals pending until review, and reports UNKNOWN with reasons. A human-confirmed named venue may be used downstream while the wrong planner ID remains a reported conflict; original output is unchanged. No V0-V3 planning code was modified. [Acceptance](../.scratch/rtpeval/ticket-03-acceptance.md): 58 evaluation tests passed, one existing native Windows symlink test skipped for host privileges; Ruff and local CLI checks passed. This does not establish live Google coverage or human-review accuracy. Ticket 04 still owns acquisition/snapshot persistence; Ticket 05 owns requirement outcomes. No formal case, experiment, version freeze, commit or push occurred.


## 26. Ticket 04 offline snapshot implementation - 2026-09-30

The approved snapshot slice now plans independent identity acquisition, exports Ticket 03 evidence, and prepares canonical Places union plus explicit directed route contexts. Its injected transport records bounded attempts and raw bytes in fresh versioned local snapshots; replay validates plan/source links, hashes, paths, coverage, UTC times and ledger consistency without networking. Unresolved occurrences, missing contexts and partial provider observations remain visible. No planner cache, verdicts or rounded route DTOs are adopted.

[Acceptance](../.scratch/rtpeval/ticket-04-acceptance.md): 35 snapshot tests; final full backend 1957 passed / 10 skipped; Standards/Spec timestamp finding corrected and final reviews clear. The slice includes no Google network serializer/client or live CLI. Live provider applicability/retention checks, budgets and execution remain separately authorized; Ticket 07 owns departure selection and Ticket 06 opening verdicts. The snapshot is a collection interval and independent-context declaration, not proof of instantaneous global truth. Work remains uncommitted and is not a benchmark/version freeze.


## Transport responsibility correction - 2026-09-30

Implemented in the current workspace: V0 retains model-estimated transport activities. V1-V3 share a primary generation schema excluding transport and an output acceptance check rejecting declared transport activities; both initial and Repair prompts explicitly reserve transport selection and transfer times to the application. Supplied route evidence can inform visit spacing. Existing Routes selection/binding and Repair operation permissions remain unchanged. A forbidden declared activity fails generation without adding a retry. Semantic transport disguised under another role cannot be comprehensively detected mechanically.

Independent evaluation now selects transport sources by planner version: V0 activities, V1-V3 transfers, including optional V3 projections. Ignored records retain source pointers and diagnostics but supply no evaluated transport occupancy/fallback; missing transfers stay missing. Source identity tuples are unchanged. `transport_source`, `ignored_transport` and activity `transport_applicable` expose this distinction for later scoring. Independent evidence remains the factual oracle. Same-source duplicate/conflict handling and distinct visit occurrences are preserved. This supersedes the historical equal-authority Activity/Transfer reconciliation checkpoint. Ticket 05 scoring and protected-time union implementation remain pending. No live calls, formal experiments, commit/push or freeze are included.


Transport correction validation: final backend suite **1973 passed, 10 skipped (85.49s)**; nine opt-in database cases and one Windows symlink privilege case were skipped. New boundary tests first reproduced forbidden-source acceptance. DTO fixture mismatches and a test nesting error were corrected. Spec review caught a contradictory shared prompt instruction, removed while retaining V0's explicit transport instruction; follow-up reviews have zero remaining findings. The first full run stalled and was interrupted; its runtime retrieval file passed separately (16 tests). The next full run exposed five superseded V3 transport expectations; updated boundary tests passed (119), followed by the successful final full run. Ruff, compilation and diff checks passed. See the transport correction acceptance record under .scratch/rtpeval for the complete sequence and limitations.


Subsequent checkpoint (2026-09-30): the separately authorized planner smoke and
workspace commit closeout are recorded in [development acceptance](transport_responsibility_smoke.md).
Earlier uncommitted/no-live statements describe their dated implementation scopes;
the planner smoke does not validate independent oracle acquisition or scoring.

## Ticket 05 specification closure — 2026-10-01

The user authorized specification closure; the [requirement/schedule contract](../.scratch/rtpeval/requirement-schedule-contract.md)
now defines the executable count/date/time wire, source-linked conservative matching,
commitment units, protected blockers and descriptive schedule/repetition reporting.
One reviewed obligation retains one weight. Protections union only within identical
scope, retain original checks, and do not inflate the non-overlap activity denominator.
Fixed-time checks support explicit dated exact starts, full-window containment and
minimum/exact durations, with zero grace. Under the subsequent user correction,
unspecified named-visit counts mean exactly one for the trip; fixed-time-only checks
use the same single-visit rule. At-least-one time matching is allowed only with sourced
explicit repetition, and does not weaken an explicit total/date quota. Unsupported quantifiers/overnight/vague constraints retain
UNKNOWN/unresolved reasons. Unknown applicability/counts never become guessed rates.

Current intake does not yet validate executable payloads; transport occupancy can be
incomplete despite an empty projected interval list; fixed-time-only subjects need the
existing independent identity review path. These are explicit implementation seams.
Ticket 05 is ready-for-agent with implementation approval pending. No scoring, planner
change, backend test, live call, formal case, experiment or Git action occurred in this
specification task. Later opening, route, aggregate and Repair tickets retain their scope.

## Ticket 05 offline implementation — 2026-10-02

The user subsequently approved offline implementation and acceptance. The workspace
now implements reviewed count/date/exclusion and bounded fixed-time checks, independent
IANA time normalization, source-selected commitments, scope-preserving protected unions,
per-commitment non-overlap checks and descriptive coverage/density/repetition. Protection
does not increase the activity denominator. Content uncertainty and incomplete unit
applicability preserve UNKNOWN or metric unavailability; invalid executable material
returns the whole batch for correction. Identity preparation includes fixed-time-only
subjects and requires replay when source/reference/policy scope is stale.

The offline JSON CLI consumes existing preparation only. It produces raw pair/union
duration measures and hashes without running planners or acquiring evidence. See the
[guide](../backend/evaluation/README.md) and
[acceptance](../.scratch/rtpeval/ticket-05-acceptance.md) for actual test/review evidence
and limitations. Earlier pending-status statements describe their dated checkpoints.
This task does not implement opening/routes, the auxiliary total, blind tasks or Repair
comparison; it includes no live service, formal experiment, commit/push or version freeze.

Subsequent closeout, 2026-10-02: the user authorized current documentation, local thesis
archive and Issue updates, then approved one local feature commit grouping.
[Ticket 05 #17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17) is closed
as completed; parent #12 reflects Tickets 01-05 complete. The acceptance record
preserves implementation failures/corrections, review results and closeout checks.
Current code/documents remain local and unpublished; no push or later-ticket
implementation is authorized. This closeout changes status, not evaluation semantics.
