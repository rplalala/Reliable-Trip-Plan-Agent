# RTPEval specification review — 2026-09-28

Status: **REVIEW FINDINGS AND PROPOSALS; DECISIONS OPEN**.

Scope: current [module draft](spec.md), [research design](../../docs/evaluator_design.md), [readiness audit](../../docs/evaluation_readiness_audit.md), and current [project context](../../PROJECT.md). This review does not replace accepted decisions or authorize implementation, benchmark cases, or runs. It examines the existing draft while evaluation documentation changes remain uncommitted; it does not claim a new full code audit.

## Findings

### F1. Automatic reliability does not establish overall travel quality

The proposed automatic subscore groups mostly measure grounding, requirements and feasibility. Density and transfer burden describe behavior; they do not independently establish preference match or usefulness. The accepted human sample compares only V2 and V3, so it cannot substantiate subjective V1-over-V0 or V2-over-V1 claims.

Proposal: explicitly label the auxiliary total by the dimensions it includes, provisionally an automatic reliability/constraint score. Retain the current human scope unless separately expanded. Do not claim subjective superiority for unassessed version pairs.

### F2. Auxiliary total missingness and double counting are unresolved

Unknown evidence, inapplicable requirements, different visit sets and missing outputs make a single total difficult to compare. Averaging only known checks can reward low evidence coverage; treating UNKNOWN as failure contradicts the accepted semantics. Temporal, route and opening scores can also penalize one scheduling defect more than once without an explicit weighting rationale.

Proposal: preserve raw metrics and separate coverage; leave the total unavailable until its eligibility/missingness rule and dimension grouping are agreed. Consider displaying bounds when unknown checks materially affect the total. Freeze weights and sensitivity variants before held-out results; do not choose them to achieve a desired ordering.

### F3. Identity resolution has an asymmetric starting point

V1–V3 normally provide canonical IDs, while V0 requires name resolution. This is an output-capability difference, but resolver failure must not silently be attributed to a nonexistent place. Conversely, an ID does not establish a correct name-to-place association.

Proposal: use supplied IDs as candidate evidence, verify their association, and apply a common match acceptance standard. Use the same fallback/adjudication policy for ambiguous or conflicting outputs from any version. Report ambiguity/unresolved identity separately. A blinded name-only sensitivity sample is optional, not a replacement for the accepted main protocol.

### F4. Incremental version comparison is not automatically isolated ablation

V1 minus V0, V2 minus V1 and V3 minus V2 estimate final-system differences under matched conditions. Retrieval can change supply, tool work and later model context; separate runner paths and nondeterminism also matter. RAG-origin selection is exposure, not causal contribution. V3 draft-to-final is a within-run Repair analysis and is not an independent V2 comparison.

Proposal: call the main comparisons staged or incremental mechanism comparisons. Reserve isolated-ablation claims for separately specified controlled interventions. Report request-level quality deltas and resource deltas without forcing every added mechanism to improve every dimension.

### F5. Product-policy compliance and real-world evidence need separate labels

Minimum daily coverage and unauthorized repetition are product rules; opening/route conflicts depend on external evidence. Current code informs what the product implements but cannot itself approve the benchmark rule. The research design's historical Sparse/Duplicate classification and the newer module draft need an explicit specification reconciliation.

Proposal: keep evidence conflicts, independently approved product-policy violations, and improvement guidance distinguishable in checks and controlled cases. Preserve legitimate revisits, minimum-count semantics and exempt dates. Do not equate policy compliance with traveler usefulness.

### F6. Capture and usage are not yet an executable contract

The audit identifies V0 trace asymmetry, truncation, partial usage and outcome gaps. Required measured fields still need an exact mapping. A missing cost ledger should not discard an otherwise evaluable itinerary; missing itinerary and missing usage have different reporting consequences. Overlapping stage durations cannot be summed into end-to-end latency, and reasoning/cached token breakdowns must not be added twice to provider totals.

Proposal: require complete attempt identity/outcome records; track quality and resource capture availability separately. Define wall time, stage time, reported versus estimated tokens and unique invocation IDs. The draft heading about verification before implementation approval should distinguish pre-implementation acceptance-test design from tests executable only after implementation exists.

## Decision frontier at review time

1. Should the auxiliary automatic total be explicitly limited to reliability/constraint compliance, leaving subjective overall usefulness to human evaluation? Recommended: yes.
2. For the existing V2/V3-only human sample, should subjective V1/V0 and V2/V1 claims remain outside v1, or should the human study be expanded? Recommended: retain current scope and restrict claims.
3. Should existing staged V0–V3 comparisons be labelled incremental system comparisons, with any strict isolated ablation requiring separate design? Recommended: yes.

Detailed total-score missingness, role adjudication and policy definitions follow these decisions. No recommendations above are recorded as user acceptance by this review.

## User decisions — 2026-09-28

1. Accepted: limit the auxiliary automatic total to reliability/constraint compliance; overall usefulness remains a human assessment.
2. Modified recommendation: expand human assessment to V0-V3. The rater receives only original input and anonymous itinerary outputs, without mechanism or evaluation information. Existing 12 unique cases, single rater and three hidden duplicates remain; response format and aggregation must be specified for four versions.
3. Accepted: use incremental system comparison terminology. Strict isolated-module ablation requires separate design.

These decisions supersede the corresponding proposals above. Next open decision: human response format; ranking, rating and pairwise designs have different workload and aggregation implications.

## Subsequent user clarification — 2026-09-28

- Use the existing V0-V3 versions; no additional strict single-module ablation study is planned. This supersedes the earlier suggestion to leave such a study for separate design.
- Human response format is accepted: a simple HTML questionnaire with original input and anonymous A/B/C/D itineraries in each group, ranked separately for preference match, pace and usefulness, with ties permitted.
- Twenty inputs and eighty itineraries were given as an example, not a frozen sample-size change. Sample size, aggregation, persistence/export and incomplete-group handling remain open. Do not implement HTML under this design-only scope.

## Human ranking protocol: next decision round

Status: proposals only; not yet accepted.

1. Missing outputs: if at least two itineraries are available, assess those outputs and record unavailable versions separately in all-run outcomes. Do not automatically rank a missing artifact last or discard the whole request. Report each version pair's available-case denominator and the complete-four subset separately. With fewer than two available outputs, no comparative human result exists for that request.
2. Aggregation: preserve rankings with ties, then derive wins/ties/losses for each version pair separately for preference match, pace and usefulness. These are correlated within-request observations, not six independent samples per four-plan group. Keep dimensions separate; do not invent one weighted human total. Duplicate tasks remain consistency checks only.
3. Unassessable judgments: distinguish a meaningful tie from inability to judge. Permit N/A for a dimension not specified by the request and an explicit unable-to-judge response; record both separately from ties. Never coerce missing judgments into ranks or wins.

Final sample count and workload remain open. Automatic opening/route/identity rules, auxiliary-score missingness and resource-capture contracts also remain open; accepting the human workflow will not resolve those separate specification items.

## User decisions on eligibility and reporting — 2026-09-28

- The user rejected partial-group assessment: all four versions must produce itineraries through their prescribed complete workflows to enter human assessment. V3 is excluded when intended Repair remains but a limit forces stopping. V1/V2 repeated places or sparse days alone remain eligible quality observations.
- Accepted: per-dimension, per-version-pair wins/ties/losses; preserve request-level dependence and exclude hidden duplicates from main results.
- Accepted: ties, unable-to-judge and N/A are distinct.
- The user permits development iteration informed by failures. This design decision does not execute code changes or runs. Cases used for tuning become development-exposed; held-out bug handling must retain outcomes and distinguish checkpoints/reruns.

Interpretation limitation: this human cohort is selected using outcomes and a stricter V3 completion condition. Exclusion counts and reasons must be visible, and human conclusions conditional on that cohort. The rule does not remove attempts from all-run reporting or discard otherwise evaluable outputs from automatic E2E evaluation. The V3 stop-reason/pending-work eligibility mapping and any sample replenishment policy remain open.


## Superseding benchmark admission decision — 2026-09-28

The user extends the four-version completion gate to the entire comparative benchmark, not only human assessment. This supersedes the earlier provision to score available outputs from excluded groups. Automatic scoring and E2E pre/post require an admitted four-version-complete group. Excluded groups receive no benchmark scores; keep a separate transparent attempt/exclusion and resource ledger. Quality conclusions are conditional on this selected cohort.

Accepted: normal V3 stopping due to no candidates, no further improvement opportunities or rejected repair is eligible without execution failure or resource truncation. Intended Repair cut short by a cap is ineligible; the cap value alone is not sufficient. Unresolved quality problems alone do not imply incomplete execution.

Still OPEN: code-level completion mapping, replenishment and attempted/retained sample counts. The V3-only Controlled Repair study cannot satisfy a four-version gate as currently defined; confirm whether it remains a separate mechanism study before freezing that scope.


## Controlled Repair scope accepted — 2026-09-28

The user retains Controlled Repair as a separate V3-only mechanism study with the existing 24 target cases and 8 control cases design. The four-version completion gate applies to comparative E2E and its associated human/pre-post evaluation, not this separate study. Controlled Repair results are reported independently and are not pooled into four-version benchmark scores. This resolves the preceding scope question; case definitions and execution contracts remain specification items, not implementation or experiment authorization.


## Benchmark construction deferred — 2026-09-28

The user places sample-count and benchmark construction decisions outside the current evaluator-module design. The prior question about 36 attempted versus 36 admitted groups is deferred, not resolved in favor of either. Provisional direction: design inputs sequentially, run four-version groups, retain qualifying groups in a benchmark candidate list, summarize failures and consider whether system iteration is needed. Module design retains admission, exclusion/provenance records and scoring contracts. No fixed sample quota, automatic tuning, input creation or live execution is authorized. Exposure and checkpoint records remain necessary for later benchmark claims.


## Batch handoff and documentation split — 2026-09-28

Accepted: benchmark construction owns workflow eligibility, failed-group reasons and iteration recommendations; only the user authorizes iteration. Evaluation receives a later user-curated batch, not a stream triggered by each admitted candidate. Documents are split into benchmark construction and evaluator design. The module specification is synthesized in the to-spec structure, retaining automatic and human assessment, independent evidence, resources, optional pre/post and separate controlled outcomes. Input integrity validation is not workflow re-screening. Detailed rule contracts remain OPEN; needs-info honestly reflects implementation readiness rather than implying a frozen spec or implementation authorization.


## Input contract facts and pending decisions — 2026-09-28

Read-only schema/runner inspection confirms shared final itineraries, distinct V3 draft/final_primary, preference-excluding structured hashes and asymmetric trace/resource capture. The input-contract review records these findings. Full-result delivery and independently assisted human-reviewed RequirementSpec preparation remain proposals for user confirmation. No code, fixtures, provider calls or test runs were introduced.


## Input packaging and RequirementSpec ownership accepted — 2026-09-28

The user requires a separate result JSON per version within each group (v0_result.json through v3_result.json), rather than one combined four-version JSON. Full results remain the source for itinerary extraction. The user accepts assistant-drafted, human-reviewed RequirementSpec preparation during benchmark construction. Evaluation consumes it without generating or inferring obligations. These decisions resolve the preceding packaging/authorship frontier; detailed field schemas and scoring rules remain open.


## Usage delivery accepted; collection outstanding — 2026-09-28

The user accepts four separate per-version usage files and explicitly notes that collection must be completed. Benchmark-side capture is an engineering prerequisite; Evaluation consumes and aggregates supplied measurements. Record actual/estimated/missing distinctly, consistent latency scope, provider calls and Repair subsets without double counting. No collector implementation or execution is authorized in this design turn.


## RequirementSpec count and access scope — 2026-09-28

Accepted: an unqualified required visit is explicitly minimum one in the benchmark-authored, user-reviewed specification; Evaluation does not infer the default. The user rejects entry/exterior differentiation because itineraries do not express it reliably. RequirementSpec v1 omits access-mode fields and scoring branches; preserved input wording is not an automatic opening exemption. Earlier exterior-specific control suggestions are superseded by an opening-boundary control direction, with exact control definitions still OPEN.


## Program/rater split and RequirementSpec consolidation — 2026-09-28

The user authorizes direct documentation consolidation of the responsibility split and RequirementSpec without re-interviewing settled principles. Programs perform explicit reproducible checks and resource aggregation; the rater judges preference, pace and usefulness. Descriptive behavioral metrics are not automatic subjective scores. RequirementSpec keeps executable obligations, soft preferences and unresolved/unsupported content distinct; reviewed empty obligations are valid, missing approval is an intake issue, and ambiguous clock language is never silently normalized. Detailed metric applicability and wire serialization remain OPEN. No implementation, benchmark creation or experiments were performed.


## Independent identity contract draft — 2026-09-28

Read-only provider/schema inspection informs the identity contract: rank is not confidence, location bias is not a hard boundary, candidate filtering differs from a true empty response, and requested/returned detail IDs require comparison. Keep independent resolution and supplied-ID consistency distinct. Existing independence and high-impact adjudication principles remain accepted; downstream scoring after a confirmed ID/name conflict is a proposal awaiting user decision. No external queries or implementation occurred.


## ID/name-conflict handling accepted — 2026-09-28

The user accepts downstream checking against a confidently adjudicated named venue while separately retaining the supplied-ID error. Uncertain identity remains UNKNOWN. Original result artifacts and planner route claims are not corrected by this evaluation mapping. Exact automatic matching thresholds, conflict-rate denominator and auxiliary-score contribution remain specification items.


## Opening boundary decision — 2026-09-28

The user accepts no grace period for opening compliance. Exact closing-time departure is permitted; positive overruns are retained. Special-date fallback remains unaccepted pending an explanatory example; no inferred approval.


## Special-date opening uncertainty accepted — 2026-09-28

The user accepts UNKNOWN for an indicated special-date exception without usable applicable hours, provided the reason accompanies it. Reports retain a specific explanation, visit/date and evidence references; they do not silently fall back to regular hours or assert closure. Other opening timezone/provider-encoding details remain OPEN.


## Route contract drafted — 2026-09-28

Read-only route/schema inspection establishes raw status/condition, per-leg completeness, directional and departure context requirements. A continuous-interval check cannot reuse planner reserve/validation as ground truth. Stated-mode selection with UNKNOWN when unspecified and zero extra evaluator buffer are proposals awaiting confirmation. No-route classification, detailed occupancy and provider temporal/fallback applicability remain OPEN. No APIs, tests or implementation were run.


## Route mode, buffer and window decisions — 2026-09-28

The user accepts stated-mode lookup (missing usable mode remains UNKNOWN with reason) and no extra evaluator buffer. The requested existing two-POI window was checked: available_intervals subtracts fixed commitments from the inter-activity gap, and transfer_time_check uses the remainder at actual departure. Evaluation preserves this meaning through independent reconstruction, not planner verdicts, lineage or reserves. Generic/free-time classification and timezone details remain OPEN. No execution or implementation occurred.


## Correction: per-mode route thresholds — 2026-09-28

The user clarified that their route window refers to kilometres/minutes thresholds. The previous interpretation as an activity gap is superseded. Checked defaults: WALK <=3 km and <=45 minutes, TRANSIT <=45 minutes, DRIVE <=30 minutes. The separate 10-minute planner DRIVE reserve is not added by Evaluation. Discovery radii 2/5 km are not route-distance limits. Threshold exceedance and scheduled-time deficit remain separate, and exact aggregation is OPEN.


## Product DRIVE reserve accepted — 2026-09-28

The user accepts retaining the existing 10-minute product DRIVE reserve while adding no further evaluator buffer. This supersedes the earlier zero-reserve interpretation. All versions use the same rule. Keep provider duration and product allowance separate, apply DRIVE's 30-minute threshold to driving duration only, and compare duration plus reserve against available time without double-counting.


## No-route verdict and five-minute tolerance request — 2026-09-28

Accepted: applicable successful no-route evidence is FAIL, whereas provider failure/timeout/incomplete data is UNKNOWN with a reason. The user requests five-minute Routes tolerance for observation-time variation. Its scope (product duration caps, available-time deficit, or both) remains pending clarification. No claim of an empirically established five-minute provider error bound is made; Opening remains zero grace.


## Five-minute tolerance scope accepted — 2026-09-28

The user selects both duration-cap and schedule-feasibility tolerance. Apply <=300 seconds independently to each check, never add them into ten minutes. Preserve raw overruns and deficits; keep WALK distance unchanged and DRIVE reserve at 600 seconds. Explicit no-route remains FAIL, unavailable evidence UNKNOWN and Opening zero grace. This changes evaluation rules only, not planner configuration.


## Activity scope and adjacency draft — 2026-09-28

Read-only inspection confirms that OutputRoleSummary counts scheduled IDs without a primary-role filter and planner free-time lineage uses generation provenance; neither is independent quality ground truth. A common inventory draft separates visits, occupancy and routes. Free-time slack, no implicit overnight legs and same-canonical route N/A are proposals awaiting user decisions. Only documentation changed.


## Free-time decision — 2026-09-28

The user accepts using uncommitted locationless free_time for travel without consuming protected rest or other commitments. Cross-day and same-canonical proposals remain pending explanation, not accepted.


## Same-place accepted; day scope verified — 2026-09-28

The user accepts same-canonical adjacent visits as route N/A and asks whether current code supports inter-day travel. Inspection confirms same-day V0 prompting and per-day pairing in shared initial transfer binding, V3 repair bindings and final diagnostics. Inter-day lodging/travel is outside v1 evaluation route scope; the earlier proposed explicit-overnight extension is withdrawn. Candidate matrix pairs are not proof of an adopted inter-day transition. No code or live behavior was changed.


## Unified metrics consolidation — 2026-09-28

The user authorizes the next documentation step. The unified metrics contract consolidates all accepted dimensions, source isolation, nested units, coverage/compliance, UNKNOWN reasons, route tolerances and reporting boundaries. It preserves OPEN numerical aggregation and auxiliary-score formulas. The accepted one-POI-per-primary-activity qualification is recorded; malformed multi-POI blocks trigger material diagnostics rather than guessed splitting. No implementation or experiments were performed.


## Auxiliary score proposal — 2026-09-28

Five dimension formulas and an equal-weight auxiliary mean are proposed, together with a complete-adjudicability/common-applicability gate. Partial evidence would retain conditional subscores and main metrics rather than produce a misleading single total. The user has not accepted this profile. Resource/human reports remain separate, and no sampling changes or implementation are authorized.


## Numeric total and missing evidence — 2026-09-28

Five dimensions/equal weighting were accepted. The user now requires numerical results for each group/version without missing evidence creating an advantage. This supersedes the proposed suppression of incomplete totals. Proposed response: verified credit PASS/(PASS+FAIL+UNKNOWN), with UNKNOWN retained separately and no conditional-compliance substitution. For fixed applicability, evidence removal cannot improve this score; differing visit sets and zero-opportunity/N/A cases still need explicit rules. No claim that unknown facts are false or that this measures unconditional itinerary quality.


## Verified-compliance formula accepted — 2026-09-28

The user accepts PASS/(PASS+FAIL+UNKNOWN). Clarified terminology: UNKNOWN/N is unknown rate, its complement (PASS+FAIL)/N is verification coverage, and PASS/N is verified compliance/reliability credit. Confirmed failures are verified judgments. N/A and zero-check scoring remain unresolved; no implementation or execution.


## Specification consistency audit — 2026-09-28

Recorded the accepted joint-N/A removal and individual-N/A zero contribution, distinguished observational N/A from score accounting, and reconciled outdated formula/availability statements. Added closeout-audit.md with two scoring-semantic frontiers, technical-contract work and outstanding usage capture. Arithmetic examples, local links and whitespace checked; no evaluator tests, API calls or experiments. Full implementation readiness is not claimed.


## Fallback meaning and undefined-activity delivery boundary — 2026-09-28

Official Google FallbackInfo documents routing-preference/traffic calculation fallback, not travelMode substitution. Corrected the earlier ambiguous explanation; no actual API calls or failure-frequency claims. The user excludes ambiguous POIs/undefined-location fixed activities from benchmark delivery. Current V0/V1 prompt and nullable schema allowances do not guarantee that rule, so enforcement remains upstream preparation rather than a reported implemented fix. Legitimate non-venue transport/free_time and explicit user time protections remain distinct.


## Generic no-POI handling supersedes exclusion — 2026-09-28

The latest user decision supersedes excluding generic no-POI activities from benchmark delivery: treat such items as free_time/transition-like for evaluation, without counting them as primary visits or inventing a venue. Preserve the original output role/text and record the evaluation classification. This does not erase explicit user-protected time or reclassify a concretely named but unresolved POI as free time. Ordinary no-POI placeholders alone do not disqualify a group.


## Valid returned Google routes accepted — 2026-09-28

Accepted simplification: use the valid route duration returned by Google for the queried endpoints, direction and stated travel mode, including a fallback traffic-calculation result. Do not classify a valid result UNKNOWN solely because traffic awareness differs from the requested routing preference. Preserve requested/returned context and fallbackInfo for traceability, without adding a separate traffic-fidelity score or promising future road conditions. Do not silently switch endpoints, direction, travel mode or query date. Explicit no-route remains FAIL; provider failure, invalid status or no usable duration remains UNKNOWN. Existing duration thresholds, DRIVE product reserve and five-minute tolerances remain unchanged.

## Technical contract documentation — 2026-09-28

Drafted artifact-contract.md and evidence-time-contract.md; linked current specifications and corrected stale generic-activity exclusion text. Preserved the accepted valid-Google-return policy and existing scoring arithmetic. This pass specifies future serialization/parser/answer-storage behavior; it does not implement or validate those capabilities. Public provider documentation is cited in the evidence contract. Remaining technical dependencies are named in closeout-audit.md; no new broad research-design interview is required.

## Ticket 01 closure — 2026-09-29

User authorized specification closure only. Inspected current public schemas, prompts, shared route binding and schedule/output policies at 364f91f. Added intake-projection-contract.md and updated Ticket 01 to specification-ready. Initial policy-path lookup failed; file discovery corrected the path before inspection. No planner/helper was executed. No new user decision was needed: independent review/unresolved paths apply existing uncertainty rules. No code, live calls, benchmark cases, commits or tests were authorized by this closure.

## Ticket 01 implementation review — 2026-09-29

Performed local Standards/Spec review without delegated agents. Confirmed no shared planner changes or application imports; checked source-boundary isolation, duplicate transport treatment, missing optional artifacts and uncertainty handling. Corrected mode-negation and rich-prose positional-binding risks and added regression checks. Final offline results and known limits are recorded in ticket-01-acceptance.md. No commit or subsequent ticket execution is authorized.

## Ticket 02 closure and implementation — 2026-09-29

User authorized end-to-end Ticket 02 work without repeated routine approvals. Closed technical seams, implemented opt-in event capture and descriptive reports, and ran offline regressions. Four initial requirement-harness failures exposed persistent HTTP hooks; fixed with scoped removal/concurrent ownership without altering the existing tests. Final verification and limits are in ticket-02-acceptance.md. No research decision was silently changed and no live experiment ran.
