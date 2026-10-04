> Archived source snapshot, relocated 2026-10-03 from `docs/benchmark_design.md`.
> Current design is indexed in [docs/README.md](../../README.md).
> Original Current/Next statements and historical defaults below are dated evidence,
> not current system authority or renewed execution permission.

# Benchmark construction design — draft

Shared terminology: [Evaluation glossary](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/evaluation_glossary.md).

Status: Accepted responsibility boundary; detailed benchmark design deferred. No run, planner iteration, benchmark freeze or implementation authorization.

## Purpose and ownership

Benchmark construction designs inputs, runs V0-V3, collects complete results and available usage/provenance, and determines whether each group completed all four prescribed workflows. It owns the attempt ledger, excluded-group reasons and recommendations for related system iteration. Only the user decides whether iteration happens; recommendations never trigger changes or reruns automatically.

Qualifying groups enter a candidate list. They are not sent individually to Evaluation. The user will curate an explicitly identified batch of an as-yet-undetermined size and hand that batch to Evaluation. There is no automatic evaluation trigger on admission. Candidate membership is distinct from final user-selected batch membership.

## Completion and exclusions

The latest user decision supersedes excluding generic no-POI activities from benchmark delivery: treat such items as free_time/transition-like for evaluation, without counting them as primary visits or inventing a venue. Preserve the original output role/text and record the evaluation classification. This does not erase explicit user-protected time or reclassify a concretely named but unresolved POI as free time. Ordinary no-POI placeholders alone do not disqualify a group.

Qualified itineraries represent each primary visit as one POI with an explicit time interval; a multi-POI block sharing one interval does not meet the accepted delivery contract. Evaluation does not invent a split if malformed material is submitted.

All four versions must produce itineraries through their own complete workflows. V3 pending further Repair cut short by a limit is ineligible. A numeric cap alone does not prove truncation. Normal stops due to no candidates, no improvement opportunities or rejected repairs are eligible without execution failure or resource truncation. Repetition, sparse days, residual conflicts and UNKNOWN evidence alone do not establish workflow failure.

Record attempted input/group, version, outcome, evidence for the failure reason, checkpoint and any iteration recommendation, distinguishing observations from hypotheses. Preserve the user's decision separately. Do not delete failures when a later run succeeds. Exact stop-reason mapping and construction tooling remain future benchmark design work.

## Batch handoff to Evaluation

Each group delivers four separate complete result files: `v0_result.json`, `v1_result.json`, `v2_result.json`, and `v3_result.json`. Do not combine four results into one JSON file. The manifest references each file and hash; the adapter extracts its itinerary while isolating internal findings from quality scoring and human presentation.

RequirementSpec is prepared during benchmark construction from the original Input, with assistant drafting permitted and explicit user review required. Evaluation only consumes the reviewed artifact: it does not generate, infer, repair or silently complete obligations. Missing, unreviewed or structurally invalid specifications produce intake diagnostics for upstream correction; explicitly recorded unresolved semantics remain unresolved.

Deliver a versioned manifest and the selected groups, each containing the original materialized input, exactly one identified final itinerary for each V0-V3 version, and independently reviewed RequirementSpec. Include source/configuration provenance and artifact hashes. Additional usage records, V3 pre-repair draft, mechanism records and qualifying official-fact records support optional evaluation outputs. Missing optional records do not retroactively disqualify a group; the corresponding evaluation is unavailable.

The producer attests that groups satisfy its completion policy. Evaluation checks artifact integrity and schema compatibility, not planner workflow completion. It does not invoke planners, select replacement inputs, decide iteration or monitor the growing candidate list. Its input/output contract is specified in the [evaluation module specification](../../contracts/0001-evaluation-artifacts.md#rtpeval-spec).

If failures inform tuning, record development exposure and checkpoint changes. A candidate is not automatically held-out. Matched checkpoint and final sampling decisions must be resolved for the eventual study; old and new outputs must not be silently mixed.

### Accepted usage handoff and collection gap

Each group supplies `v0_usage.json`, `v1_usage.json`, `v2_usage.json` and `v3_usage.json` separately from the corresponding full result files. Benchmark execution owns collection and file production; Evaluation validates associations and aggregates the supplied observations. Uniform collection is required engineering preparation, not implemented behavior. This decision does not authorize collector implementation or runs.

Each record identifies its group, version and selected run, schema version, collection status and measurement scope. Record measured end-to-end duration and available stage durations; model calls and provider-reported input/output/total tokens by model; actual provider sends, failures, cache hits and Routes matrix elements; and V3 Repair rounds plus its tokens/calls/duration as subsets of the total. Keep engineering estimates separate from reported observations. Do not add Repair totals again or assume overlapping stage durations sum to wall time. Record missing fields and reasons explicitly; missing is never zero. Evaluation's own provider usage has a separate ledger.

The intended handoff includes all four usage files, even where some observations are unavailable. Historical or incomplete packages with absent usage retain an explicit resource-availability diagnostic; absence does not become an itinerary quality failure or a new workflow-eligibility gate. Result/trace metadata can provide source evidence, but must not be double-counted as additional usage.

Before resource comparisons, close the known gaps: symmetric V0-V3 capture, a common outer timing boundary, source-linked model/provider accounting, retry/cache semantics, complete result retention and missingness reporting. Exact wire fields and transport hooks remain to be specified. Verification must cover actual zero versus missing, provider failures/retries, stage/Repair attribution and identical run linkage across result and usage files.

## Requirement preparation boundary

Prepare and human-review requirement_spec.json before handoff using the [field contract](../../contracts/0003-requirement-schedule.md#rtpeval-requirement-spec-contract). Explicit supported obligations, qualitative preferences and unresolved/unsupported clauses remain separate. Do not derive obligations from the four outputs, translate relaxed pacing into an invented threshold, or omit an explicit clause because it is difficult to check. Reviewed empty obligations are valid when the input contains none. The evaluator does not author or complete the specification.

## Separate mechanism study

Controlled Repair remains a separate V3-only study with 24 target and 8 control cases as the accepted design basis. It does not require four-version groups and is not pooled into E2E scores. Construction/execution of controlled fixtures is separately authorized; independent outcome reporting belongs to Evaluation.

## Earlier planning references — not frozen requirements

The following earlier proposals are retained for later benchmark design, not imposed on the evaluator or approved for execution. They do not fix the final batch size, replacements, stopping rules or iteration policy.

### Earlier composition discussion

Scope clarification (2026-09-28): benchmark construction is deferred to a separate design
session. The numbers and sampling proposals below are planning references, not module
requirements or frozen sample targets. The evaluator must not hard-code 36 groups or a
144/192-run quota. Input design, admission-list construction, replacement, stopping rules,
and final sample sizes belong to that later benchmark design.

The provisional workflow is to design inputs and run matched four-version groups one at
a time: qualifying groups enter a benchmark candidate list; nonqualifying groups retain
failure summaries for deciding whether later system iteration is needed. This is not
experiment or iteration authorization. Benchmark construction owns admission and attempt records; Evaluation scores a later user-selected batch. If failures inform system tuning,
record development exposure and checkpoint changes; candidate-list inclusion does not by
itself establish held-out status or permit mixing checkpoints in final comparisons.

### 6.1 Development and city eligibility

Tokyo, Sydney, London, Melbourne, and Berlin are development/regression cities. Use them for
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

The earlier provisional design target is six cities with six request types each: **36 unique requests**.
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

### 6.4 Benchmark admission

Benchmark construction applies the four-version completion gate before groups become candidates for the later automatic and human evaluation batch. Admit a request group only when V0-V3 each
produced an itinerary through their complete prescribed workflow. Excluded groups receive
no benchmark quality scores, including otherwise available outputs from individual versions.

V3 is ineligible when intended further Repair is stopped by a round/call/time/resource cap.
Reaching a numeric cap alone does not prove truncation. Normal stopping because there are
no candidates, no further improvement opportunities, or rejected repairs is eligible when
there is no execution failure or resource truncation. Residual defects and UNKNOWN evidence
alone do not disqualify an output. V1/V2 repetitions and sparse days remain quality observations.
The exact code-level mapping of stop reasons and pending work remains OPEN.

Keep an attempt/exclusion ledger outside benchmark scoring, with version, reason, checkpoint,
resource records where available, and retained group counts. Results describe the selected
four-version-complete cohort, not unconditional performance on all requests. Do not silently
replace excluded groups or retry until success; replenishment and the distinction between
attempted and retained sample-size targets must be specified before formal execution.
Controlled Repair is retained as a separate V3-only mechanism study. The four-version
completion gate does not apply to it; its results are reported separately and are not pooled
into four-version E2E benchmark scores.

## Documentation checkpoint — 2026-09-28

The evaluation work plan has been approved and published, but detailed benchmark construction remains separate and deferred. The user will eventually select a batch of qualifying groups; candidate admission does not invoke Evaluation. Benchmark construction owns attempt/failure records and recommendations; the user alone authorizes iteration. No formal inputs, sample size, cities, repeated-run policy, admission implementation or benchmark freeze were established by ticket publication.

A historical record is retained under thesis_notes/benchmark. It is not a current source of truth or an experiment result. The next planned task after the user's break is Evaluation Ticket 01 specification closure, not benchmark creation.
