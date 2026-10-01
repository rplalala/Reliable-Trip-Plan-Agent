# RTPEval evaluation module specification

Status: needs-info
Design state: Accepted module boundary; detailed scoring contracts OPEN. Not frozen or authorized for implementation.
Updated: 2026-09-28.

This specification synthesizes the accepted decisions. The remaining information is specific rule definition, not a request to redesign the research architecture. It is not labelled ready-for-agent implementation while those contracts remain open.

## Problem Statement

The researcher needs to evaluate a curated batch of travel requests and their corresponding V0-V3 itineraries fairly, without assuming a unique correct itinerary or reusing V3's judgments as ground truth. Automatic reliability measures, resource usage and blinded human preferences answer different questions and must remain distinguishable.

Benchmark construction already determines workflow completion and records failures. Evaluation must consume the batch the user eventually selects, rather than execute planners, continuously watch candidates or decide which failed systems should be changed.

## Solution

Provide a batch-oriented evaluation workflow: validate delivered materials, project outputs without rewriting them, resolve identities independently, collect and freeze common external evidence, score offline, prepare blinded human tasks, import judgments, and export reproducible reports. Automatic scoring and human assessment are separate tracks over the supplied batch; human tasks do not depend on automatic scores being available.

Benchmark construction and evaluation have separate design documents. Benchmark construction owns inputs, executions, admission, failure diagnosis and iteration recommendations. The user alone decides whether iteration happens and when a curated batch is handed over. Evaluation has no automatic admission-to-scoring trigger.

## User Stories

1. As the researcher, I want to submit a curated batch when I am ready, so that individual candidate admissions do not start evaluation.
2. As the researcher, I want arbitrary batch sizes, so that sample counts are not hard-coded into the module.
3. As the researcher, I want each request linked to exactly one selected final output per version, so that comparisons preserve pairing.
4. As the researcher, I want material errors reported before scoring, so that missing artifacts are not silently converted into poor scores.
5. As the researcher, I want externally certified workflow eligibility respected, so that the evaluator does not repeat benchmark screening.
6. As the researcher, I want independently reviewed request obligations, so that planner interpretation does not define its own correctness.
7. As the researcher, I want V0 names and V1-V3 IDs checked by an independent resolver, so that neither search rank nor a supplied ID is automatically ground truth.
8. As the researcher, I want ambiguity routed to adjudication, so that uncertainty is not disguised as a match.
9. As the researcher, I want common frozen evidence for every version in a group, so that internal evidence availability does not determine quality scores.
10. As the researcher, I want offline replay, so that repeated scoring does not recollect changing provider data.
11. As the researcher, I want counts, denominators, coverage and compliance together, so that UNKNOWN reductions do not imply improvement automatically.
12. As the researcher, I want transparent dimension scores and an auxiliary total, so that summaries remain subordinate to their measurable components.
13. As the researcher, I want actual usage separated from estimates and missing data, so that resource comparisons do not invent zero cost.
14. As the researcher, I want optional V3 before/after comparison, so that Repair changes are assessed independently when both outputs exist.
15. As the researcher, I want mechanism reports separated from scoring, so that acceptance and internal findings cannot determine independent quality.
16. As the rater, I want only the original request and anonymous plans, so that mechanisms and automatic judgments do not prime my assessment.
17. As the rater, I want separate rankings for preference match, pace and usefulness, allowing ties, so that different dimensions are not forced into a single judgment.
18. As the rater, I want unable-to-judge and N/A distinguished from ties, so that missing judgments are not counted as equal preference.
19. As the rater, I want answers saved and resumable, so that interrupted assessment does not lose completed work.
20. As the researcher, I want mapping-aware answer import and wins/ties/losses, so that anonymous results can be attributed without leaking the key to the rater.
21. As the researcher, I want hidden duplicate consistency checks excluded from main counts, so that they do not increase sample weight.
22. As the researcher, I want the independent Controlled Repair report kept separate, so that it does not inflate four-version E2E scores.
23. As the researcher, I want hashes and correction history, so that a report can be traced to its exact artifacts and rules.
24. As the researcher, I want a future external-system adapter, so that the supplementary Codex comparison does not require redesigning the scorer.

## Implementation Decisions

### Ownership and batch lifecycle

The benchmark producer owns runner invocation, attempt IDs, terminal outcomes, full result capture, completion certification, excluded-group records and recommendations for iteration. The user owns iteration approval and batch selection. Evaluation accepts a delivered batch, validates its materials and emits an intake result. Valid intake permits separate automatic and human workflows. Human results can be pending while automatic reports already exist; a report must explicitly state which tracks are complete.

The evaluator never replaces an input, invokes a planner, recommends iteration on behalf of benchmark construction, or turns a candidate into final batch membership. It does not use V3 stop states to reassess eligibility. A malformed batch returns actionable intake diagnostics; correction produces a new revision. No silent subset evaluation occurs. Missing optional artifacts only disable their dependent outputs.

### Input contract

Each group delivers four separate complete result files: `v0_result.json`, `v1_result.json`, `v2_result.json`, and `v3_result.json`. Do not combine four results into one JSON file. The manifest references each file and hash; the adapter extracts its itinerary while isolating internal findings from quality scoring and human presentation.

RequirementSpec is prepared during benchmark construction from the original Input, with assistant drafting permitted and explicit user review required. Evaluation only consumes the reviewed artifact: it does not generate, infer, repair or silently complete obligations. Missing, unreviewed or structurally invalid specifications produce intake diagnostics for upstream correction; explicitly recorded unresolved semantics remain unresolved.

| Artifact | Required content and missingness |
| --- | --- |
| Batch manifest | Batch ID and revision, selected group IDs, declared V0-V3 membership, supplied artifact references/hashes, producer completion attestation, and provenance references. Size is user-selected. Serialization is defined in artifact-contract.md; no artifacts have been generated. |
| Selected group | Original materialized Input including preferences and dates; exactly one identified final itinerary per V0-V3 version; selected run IDs; original activity correspondence; source/configuration provenance with explicit missing fields. |
| RequirementSpec | Human-reviewed version-independent obligations and applicability with review provenance: REQUIRED/EXCLUDED, minimum/exact/date obligations, fixed times and unresolved semantics. Not copied from planner interpretation or injected into planners. Detailed schema remains OPEN. |
| Per-version usage files | v0_usage.json through v3_usage.json, linked to selected results; measured timings, model usage and provider events with collection scope/status. Missing observations yield unavailable resource metrics, never inferred zero. |
| Optional V3 draft | Original pre-repair draft linked to the selected final run. Both artifacts are necessary for paired analysis; missing pair is unavailable, identical pair has delta zero. |
| Optional mechanism/official records | V3 audits and qualifying accepted-and-exposed/rule-used official facts, consumed only by separate reporters. Their absence does not block ordinary itinerary evaluation. |
| Evaluation configuration | Versioned rule profile, evidence policy, score profile when enabled, and human-task configuration. Unresolved rule profiles are not silently filled with invented defaults. |

Input integrity checks cover required artifacts, duplicate identifiers, version membership, matching request/run references, schema compatibility and hashes. They do not certify travel quality. Structurally parseable but semantically incomplete activities remain visible as structural unevaluability according to the applicable rule, rather than being silently removed.

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

### Automatic evaluation boundary

The public workflow consumes a batch plus configuration and produces intake diagnostics and reports. Inside it, a small pure quality seam consumes only an EvaluationItinerary, reviewed RequirementSpec, frozen EvidenceSnapshot and EvaluationRules. It returns an EvaluationReport deterministically without network, models, databases or V3 decision imports. Identity adjudication is persisted into the evaluation artifacts with provenance.

Adapters retain actual roles, dates, times, identities, transport claims, notes, amounts and uncertainty. V0 estimated transport is distinguishable from application-owned transfers. Nearby is an unscheduled reference and does not satisfy primary-visit obligations. No adapter silently repairs itinerary content.

Collect independent evidence over the union of selected final places, relevant requirements and available V3 drafts. Resolve IDs and names under one policy, inspect high-impact/ambiguous matches, and sample accepted matches for review. Query only necessary directed route legs. Store provider context, failures, retrieval intervals and planner-to-oracle lag. Evaluation cache is separate from planner RequestCache. Offline scoring never queries providers.

Independent judgment does not import V3 validation or Repair policy decisions. Neutral schemas/provider protocols and mechanical normalization can be shared only with independent fixtures. A mechanism reporter may consume internal findings and round records but cannot overwrite quality reports.

### Human assessment boundary

Human assessment is part of Evaluation. Generate a simple HTML assessment from an explicitly selected subset of the delivered batch and a versioned presentation configuration. The earlier 12-case/three-duplicate plan is a planning reference; sample selection and final counts belong to later study design, not hard-coded module requirements.

Each task displays the original Input and uniformly rendered anonymous A/B/C/D itineraries. Preserve meaningful plan content and uncertainty without LLM rewriting. Hide version identity, source/implementation metadata, automatic scores, RequirementSpec, repair status and oracle evidence. Keep the version mapping outside both the rater-facing HTML and rater answer export. Freeze presentation details before use; exact rendering fields remain OPEN.

Labels stay consistent across the three dimensions within a group and are balanced/randomized across groups. Hidden duplicate tasks can reassign labels; the researcher-side mapping identifies underlying plans. The rater ranks preference match, pace and usefulness separately with ties. Ties, unable-to-judge and N/A are distinct responses. Use a single rater as currently accepted and disclose their project relationship; no inter-rater agreement claim.

Save/resume and export answers keyed by task, batch and presentation revision. Import validates identifiers and ranking consistency. Exact storage/export format and correction behavior remain OPEN; no hosting service or account infrastructure is assumed. Aggregate per-dimension version-pair wins/ties/losses, respecting within-request dependence. Duplicates assess intra-rater consistency only, never increase main counts. Human judgments do not feed the automatic total.

### Output contract

| Output | Meaning |
| --- | --- |
| IntakeReport | Material validity, artifact errors and optional-data availability; not workflow-completion screening. |
| EvaluationReport | Per-group/per-version observations, raw counts, denominators, structural evaluability, evidence coverage/compliance, UNKNOWN/N/A reasons, magnitudes and source/rule hashes. |
| ComparisonReport | Paired four-version metrics for the submitted cohort, with optional configured dimension scores and auxiliary reliability total. No total until its formula is approved. |
| ResourceReport | Measured/reported/estimated/missing usage distinguished; evaluation acquisition costs separate from planner costs. |
| HumanTaskPackage / HumanReport | Anonymous tasks and answer schema; researcher-only mapping; separate rankings and aggregated wins/ties/losses with consistency and missingness. |
| V3PairedReport / MechanismReport | Independent before/after changes distinct from internal trigger/acceptance/round diagnostics. |
| ControlledRepairReport | Separate V3-only independent outcomes for supplied controlled artifacts; never pooled into E2E scores. |

Report incomplete tracks explicitly. Version corrections rather than overwriting prior evidence or quietly mixing new and old results. Benchmark failure summaries remain external context and are not scored or assigned zero.

### Detailed accepted metric and reporting constraints

## Quality checks and scorecard

All-attempt outcomes and exclusions are disclosed outside benchmark scoring. Primary E2E results for admitted groups are a **multi-metric vector**, with raw counts and applicable denominators: date/primary-visit coverage; canonical grounding; REQUIRED/EXCLUDED and date/count obligations; fixed-time satisfaction; overlap; opening evaluability/coverage/compliance; route evaluability/coverage/feasibility and deficit; observed transfer burden; repetition; and density/occupied time. Main visits and directed legs are nested within a request, not independent requests.

The evaluator must distinguish confirmed evidence conflict from product-policy violations and optional guidance. Current V3 minimum-one-visit coverage and unauthorized repeat rules are product-policy checks; two-to-five density guidance and overfull review are not automatically hard defects. The scorer independently computes these categories. A source missing opening periods or route information yields UNKNOWN when the check applies, not PASS, FAIL or zero travel time.

For presentation, group checks into transparent **dimension subscores** (proposed groups: request fulfillment, grounding, temporal feasibility, opening, and routes) and an **auxiliary reliability/constraint-compliance total**. Primary evaluation results remain individual metrics; benchmark-owned attempt outcomes are contextual records, not evaluator admission decisions. Practicality/density, subjective preference and system cost remain visible separately unless an explicit future score profile defines a justified role for them. Resource consumption is reported alongside quality and is not silently folded into that total. The accepted score profile defines equal weighting and PASS/(PASS+FAIL+UNKNOWN), joint removal of group-wide N/A dimensions and zero contribution for a single-version no-check dimension. Preserve raw states and the common mask. Scores are not yet implemented or frozen; exact technical applicability rules still require completion. The [OECD/JRC composite-indicator handbook](https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html) motivates documenting these choices and testing robustness to weighting and missing-data assumptions.

The Official Evidence Audit reads qualifying planner-side facts only when Evidence Gate accepted them and they were exposed to a model or used by a rule. Its independent recheck and outcomes are reported separately from Google-based itinerary scoring. Search results, rejected facts and unused records do not enter its denominator, and model exposure is not a causal-use claim. Exact extraction and recheck contracts remain **OPEN**.

## Resource metrics

### Accepted usage handoff and collection gap

Each group supplies `v0_usage.json`, `v1_usage.json`, `v2_usage.json` and `v3_usage.json` separately from the corresponding full result files. Benchmark execution owns collection and file production; Evaluation validates associations and aggregates the supplied observations. Uniform collection is required engineering preparation, not implemented behavior. This decision does not authorize collector implementation or runs.

Each record identifies its group, version and selected run, schema version, collection status and measurement scope. Record measured end-to-end duration and available stage durations; model calls and provider-reported input/output/total tokens by model; actual provider sends, failures, cache hits and Routes matrix elements; and V3 Repair rounds plus its tokens/calls/duration as subsets of the total. Keep engineering estimates separate from reported observations. Do not add Repair totals again or assume overlapping stage durations sum to wall time. Record missing fields and reasons explicitly; missing is never zero. Evaluation's own provider usage has a separate ledger.

The intended handoff includes all four usage files, even where some observations are unavailable. Historical or incomplete packages with absent usage retain an explicit resource-availability diagnostic; absence does not become an itinerary quality failure or a new workflow-eligibility gate. Result/trace metadata can provide source evidence, but must not be double-counted as additional usage.

Before resource comparisons, close the known gaps: symmetric V0-V3 capture, a common outer timing boundary, source-linked model/provider accounting, retry/cache semantics, complete result retention and missingness reporting. Exact wire fields and transport hooks remain to be specified. Verification must cover actual zero versus missing, provider failures/retries, stage/Repair attribution and identical run linkage across result and usage files.


Per attempt, record measured end-to-end elapsed time and terminal status. Where observable, retain stage times for interpretation, primary generation, semantics/landmark work, RAG, Repair and Nearby. Record model calls and reported input/output/total tokens by invocation and model; keep engineering token estimates separate. Record actual Places/Routes/Weather/Web/embedding sends and requested route matrix elements where the transport hook supports them. Count cache hits and provider failures separately. Report resource usage for supplied selected runs. Any supplied all-attempt resource ledger remains separately labelled benchmark-construction context, not part of selected-group quality scores.

V0 currently has no symmetric run trace, and V1–V3 tracing is best-effort and size-bounded. The outer collector's complete attempt/result capture is therefore a prerequisite for formal runs. Where model or provider metadata cannot be obtained reliably, report `missing` and the collection scope rather than estimating a false zero. Monetary model/API cost may be a dated derived estimate, never a billing fact. Independent oracle calls belong to a separate ledger.

## Repair and controlled cases

The accepted controlled composition stays **24 targets + 8 controls**. Case metadata must distinguish confirmed evidence conflicts, confirmed product-policy violations, and review/improvement opportunities. A Duplicate case is not universally an improvement case under the current product policy; explicit authorized revisits and exact/minimum obligations must be checked. Sparse cases distinguish the confirmed zero-main minimum, exemptions/UNKNOWN, and optional one-to-two quantity guidance. Overfull stays an optional review unless another independently specified obligation applies.

Freeze the candidate pool, provider responses, evidence and uniform capability configuration. Execute the real V3 validator, target selection, scope, candidate preparation, Repair, acceptance and re-validation. Independent outcomes follow canonical identity, date, requirement obligation, activity correspondence and before/after facts. Internal target disappearance or patch acceptance is not ground truth. Include target-detection failures in denominators and record new conflicts, visit loss, and evidence-coverage changes.

## Presentation of mechanism comparisons

Present V3 as the final system, then describe the existing V0-V3 runs as incremental system comparisons examining the addition of external evidence, RAG, and validation/Repair. No additional strict single-module ablation study is planned. The recorded methods identify the actual independent runner and shared checkpoint for each run.


## Testing Decisions

Use the highest external seams: delivered batch plus fixture snapshot to report, and human-task generation/answer import to human report. Avoid tests that merely mirror internal methods. Existing provider normalization, schema and V3 fixture-based tests provide patterns, not ground-truth verdicts.

- Verify malformed batch diagnostics, request/version mismatch and missing required artifacts; no runner or eligibility validator invocation.
- Verify missing usage and missing draft disable only dependent outputs; preserve semantically incomplete activities and meaningful denominators.
- Independently authored opening/route fixtures cover timezone/DST, multiple/overnight periods, closed/missing/invalid evidence, route direction/status/fallback/departure and interval occupancy after contracts are settled.
- Verify REQUIRED/EXCLUDED identity and obligation semantics, ambiguity and adjudication provenance without importing V3 decisions.
- Identical versioned inputs and snapshots produce identical offline quality reports; any network access during scoring fails the test.
- Changing a V3 finding alone leaves independent quality unchanged; changing relevant independent evidence can change it.
- Verify resource provenance and avoid cumulative/round double counting.
- Inspect generated human artifacts for hidden version mappings and metadata leaks, consistent task labels, answer save/resume/export, ties versus missingness, mapping-aware import, and duplicate exclusion from main counts.
- Verify automatic and human tracks can complete separately without inventing missing results.

These are proposed acceptance checks, not tests executed in this documentation task. Exact fixtures await the OPEN contracts; implementation approval remains separate.

## Out of Scope

Input construction, city/sample-count selection, candidate admission, planner execution and completion diagnosis; failure-driven planner iteration; automatic per-candidate evaluation; formal experiment execution; additional strict single-module ablation; Codex harness/skill implementation; evaluator implementation or HTML implementation in this task; thesis writing and research conclusions.

Verified budget/cost coverage, whole-trip budget PASS, false certainty and public-access accuracy remain deferred. Planner amounts can be descriptive. There is no primary composite score.

## Further Notes

Technical contracts now describe RequirementSpec/artifact serialization, human answer storage, provider states and time interpretation. Remaining dependent work includes validated identity acceptance/audit criteria, transport correspondence, usage hook mapping, official-audit extraction and Controlled Repair correspondence/invariants. Independent acceptance fixtures are still required. Benchmark composition and final analysis sampling remain in their separate design process.

The implementation readiness label remains needs-info because these scoring contracts are not complete. The accepted architectural boundary can be used to finish the specification; it does not authorize implementation, provider calls, development dry runs or formal experiments.

## Comments

2026-09-28: User confirmed separate benchmark/evaluation documents and a curated batch handoff after collecting a user-chosen number of qualifying groups. This supersedes prior evaluator-owned admission and any automatic admission-to-evaluation flow. Benchmark construction records failure causes and iteration recommendations; actual iteration requires the user's decision. Automatic and blinded human assessment both remain Evaluation responsibilities.


### Input contract review checkpoint — 2026-09-28

The [field mapping review](input-contract-review.md) records checked schema facts and separates pending delivery/authorship proposals from accepted decisions. Current structured_hash omits preference text, request_id is optional, and result requirements do not preserve the original request. Batch identity must therefore include a distinct complete-input fingerprint. V3 draft/final_primary and the shared final itinerary are separate supported artifact sources; activity IDs are scoped, not guaranteed cross-Repair identity. Do not revalidate historical input against the current live planning date window during batch intake. Accepted delivery uses four separate full-result JSON files per group. RequirementSpec is independently drafted and user-reviewed upstream; Evaluation never authors it.


### RequirementSpec field proposal — 2026-09-28

The [RequirementSpec contract draft](requirement-spec-contract.md) separates input/review linkage, subjects, explicit obligations, soft preferences and unresolved clauses. It preserves the accepted upstream authorship boundary. Current rule (user correction, 2026-10-01): benchmark preparation writes unqualified named required visits as explicit exact-one obligations for user review, superseding the earlier minimum-one default. RequirementSpec v1 omits entry/exterior distinctions; scoring does not infer access intent or use it to exempt visits from opening checks. Detailed field structure and time semantics are not frozen.


### Identity contract draft — 2026-09-28

The [identity contract](identity-contract.md) records current provider capabilities, independent resolution/adjudication records and downstream uncertainty propagation. It distinguishes Google entity existence from association with the itinerary's description. Accepted: when independent adjudication clearly identifies the named venue despite a conflicting supplied ID, use that venue for downstream checks while retaining a separate supplied-ID conflict. Otherwise preserve UNKNOWN. Do not modify planner artifacts or treat this as a clean original binding. Automatic thresholds and score aggregation remain OPEN; implementation is not authorized.


### Opening contract draft — 2026-09-28

The [opening contract](opening-contract.md) records full-interval containment, evidence-basis separation, timezone and provider-encoding gaps, and outside-opening duration semantics. Zero grace is accepted (ending exactly at closing is compliant); an indicated special-date exception with no usable applicable schedule yields UNKNOWN with a specific reason and evidence references, without silently substituting regular hours; no scoring implementation or provider calls are authorized.


### Route contract draft — 2026-09-28

The [route contract](route-contract.md) records current request/result capabilities, continuous interval semantics, directed/departure-specific evidence and explicit UNKNOWN reasons. Stated-mode evaluation with UNKNOWN when no usable mode is specified, and zero extra evaluator buffer, are accepted. The user clarified that the referenced route window means per-mode product thresholds: WALK <=3 km and <=45 minutes, TRANSIT <=45 minutes, DRIVE <=30 minutes at the checked defaults. Keep threshold exceedance separate from schedule-window feasibility; the accepted product DRIVE reserve of 10 minutes is included for all versions, with no additional evaluator buffer. Provider duration and product reserve are reported separately. The earlier attribution of continuous-window semantics to this request is superseded. Adjacency, provider temporal/fallback semantics and special applicability cases remain OPEN. No implementation or live acquisition is authorized.


### Route outcome and requested tolerance update — 2026-09-28

Accepted: successful, applicable explicit no-route evidence is a route FAIL, without invented duration deficit; provider failure/timeout/incomplete evidence is UNKNOWN with reasons. The user requests five-minute Routes tolerance; scope is accepted for both product duration caps and scheduled-time deficit, each with <=300 seconds allowed independently (never summed to ten minutes). Preserve raw overruns/deficits; DRIVE reserve stays 600 seconds and WALK distance stays <=3 km. Opening remains zero grace. Preserve raw values and apply any accepted tolerance uniformly across versions.


### Activity scope and adjacency draft — 2026-09-28

The [activity scope contract](activity-scope-contract.md) establishes a shared inventory for visits, occupancy and route connections without importing planner role summaries or lineage. Uncommitted locationless free time as travel slack is accepted; protected commitments cannot be consumed. Same canonical venue as route N/A is accepted. Checked product routing is per-day; inter-day travel is outside the v1 route scoring scope, including the previously proposed explicit-overnight extension. Other structural and denominator details remain OPEN.


### Unified metrics contract — 2026-09-28

The [metrics table](metrics-contract.md) consolidates source boundaries, units, denominators, states, accepted tolerances and remaining formula items. Each primary visit in delivered qualifying itineraries is one POI with an explicit interval; unexpected multi-POI blocks return an input-contract diagnostic without invented splitting. The table is a draft specification, not implemented scores, frozen weights or formal results.


### Score profile proposal — 2026-09-28

The [score profile](score-profile.md) records accepted five equal-weight dimensions. The user requires a numeric total for each group/version without rewarding missing evidence, superseding the earlier incomplete-evidence suppression proposal. The PASS/(PASS+FAIL+UNKNOWN) verified-compliance score is accepted; common-N/A exclusion and single-version no-check zero contribution are accepted. Raw N/A remains distinct from FAIL/UNKNOWN. UNKNOWN is not relabelled FAIL. Primary metrics and coverage remain visible.


### Specification closeout audit — 2026-09-28

The [closeout audit](closeout-audit.md) distinguishes accepted score arithmetic from remaining semantics and engineering preparation. N/A rules are now recorded; earlier incomplete-total suppression and score-formula-OPEN notes are superseded. The module is not implementation-ready as a whole. Contract-first ticket planning can be undertaken if requested, without authorizing coding or benchmark execution.


### Undefined activities and fallback clarification — 2026-09-28

Generic activities without a concrete POI are treated as free-time/transition-like, preserving original text and role. They do not disqualify delivery. Explicit protected time remains occupied; a concretely named unresolved POI remains a visit with uncertain identity. Google fallback documentation concerns routing preference/traffic computation, not automatic travel-mode switching; the latest accepted policy uses valid returned Google duration even with traffic-calculation fallback, retaining provenance.


### Superseding generic-activity decision — 2026-09-28

The latest user decision supersedes excluding generic no-POI activities from benchmark delivery: treat such items as free_time/transition-like for evaluation, without counting them as primary visits or inventing a venue. Preserve the original output role/text and record the evaluation classification. This does not erase explicit user-protected time or reclassify a concretely named but unresolved POI as free time. Ordinary no-POI placeholders alone do not disqualify a group.


### Google route-result simplification accepted — 2026-09-28

Accepted simplification: use the valid route duration returned by Google for the queried endpoints, direction and stated travel mode, including a fallback traffic-calculation result. Do not classify a valid result UNKNOWN solely because traffic awareness differs from the requested routing preference. Preserve requested/returned context and fallbackInfo for traceability, without adding a separate traffic-fidelity score or promising future road conditions. Do not silently switch endpoints, direction, travel mode or query date. Explicit no-route remains FAIL; provider failure, invalid status or no usable duration remains UNKNOWN. Existing duration thresholds, DRIVE product reserve and five-minute tolerances remain unchanged.

## Technical contract checkpoint — 2026-09-28

- [Artifact and human-answer contract](artifact-contract.md): batch references/hashes, reviewed requirement linkage, usage envelope, report missingness, blinded ranking export/import and private mappings.
- [Evidence and time contract](evidence-time-contract.md): timezone interpretation, opening-period precedence/completeness and per-leg Routes truth tables, with official provider references.

These drafts support contract-first task decomposition. They do not establish implemented collectors, tested parsers, frozen identity thresholds or complete Controlled Repair reporting. No new user decision is required for the already accepted route fallback and generic-activity boundaries. Dependent tasks must resolve the specific remaining technical definitions before being marked implementation-ready.

## Ticket 05 specification specialization — 2026-10-01

[Requirement/schedule](requirement-schedule-contract.md) now closes Ticket 05's executable
obligations, supported explicit time operators, commitment/protection units, uncertainty
and descriptive schedule metrics. It supersedes general pending RequirementSpec/time
wording for this slice only. User-reviewed single-visit fixed-time defaults, source-backed
at-least-one matching for explicit repetition, and protection-as-boundary scoring are accepted. Opening/routes and later report/mechanism
contracts remain separate. Ticket 05 is specification-ready, with implementation
approval pending; the overall module is not implemented/frozen by this update.

## Ticket 05 implementation follow-up — 2026-10-02

The subsequent user approval covers offline implementation, tests, review/corrections
and acceptance without real services or Git actions. Requirement and submitted-schedule
metrics are implemented in the uncommitted workspace; see
[Ticket 05 acceptance](ticket-05-acceptance.md) and the
[package guide](../../backend/evaluation/README.md). This follow-up supersedes the
pending implementation status for this slice only. Opening/routes, aggregate scores,
blind rating and Repair comparison retain their separate tickets and authorization.

## Ticket 05 closeout follow-up — 2026-10-02

After offline acceptance, the user separately authorized documentation/archive/Issue
closeout and approved one local feature commit grouping. Ticket 05 #17 is
closed as completed and parent #12 reflects Tickets 01-05 complete. The
[acceptance record](ticket-05-acceptance.md) links the self-contained online completion
comment. Implementation and current documents are local and unpublished; no push,
live service or later-ticket implementation is included. Migration snapshots and
earlier authorization statements retain their historical meaning.
