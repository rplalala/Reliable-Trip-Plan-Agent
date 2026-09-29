# RTPEval evaluation readiness audit

Status: **DESIGN AUDIT, NOT BENCHMARK FROZEN**. Audited 2026-09-28 against clean `HEAD` `8a435e2db0198e4fc8928b85e333b45b66c0c981`. This is a read-only code and contract review. No provider, model, database, or formal benchmark run was performed.

## Decision and scope

The current checkpoint is suitable for specifying an independent evaluation module. It is not yet ready for formal held-out execution. V3 engineering was closed in the [V3 closeout](v3_closeout.md), and subsequent shared/V0 work is recorded in [PROJECT.md](../PROJECT.md). No version or benchmark freeze follows from either record.

This audit covers the module's interfaces, source data, independence boundary, run capture, and changes since the [accepted research design](evaluator_design.md). It does not revisit the accepted overall research architecture or select benchmark cases.

## Readiness by boundary

| Boundary | Current evidence | Readiness decision |
| --- | --- | --- |
| Common input | [`PlanningRequest`](../backend/app/schemas/request.py) has a shared versioned request, typed trip fields, optional preferences, and optional request ID. Date validity also depends on the runtime reference date and product window. | **Usable.** The collector must retain the complete materialized JSON and reference date. `structured_hash()` excludes preference text and is insufficient as the benchmark fingerprint. |
| Common output | [`Itinerary`](../backend/app/schemas/itinerary.py) has dated activities, roles, optional place IDs, optional transfers, route diagnostics, and unscheduled references. All four runners return a `PlanningResult` subtype. | **Usable with an independent adapter.** Do not use planner diagnostics or transfer `validation_state` as evaluation answers. |
| V0 output | [`run_v0`](../backend/app/versions/v0/runner.py) returns the common itinerary, but lacks the V1–V3 tracer/result extensions. Current V0 can include estimated `transport` activities and optional unverified Nearby references. | **Partial capture.** A neutral outer collector is needed for run outcome, full output, elapsed time, model identity/configuration, and available usage. Model-estimated transport is not a Google-backed route fact. |
| V1–V3 capture | The shared [tools runner](../backend/app/versions/v1/runner.py) creates run IDs and a best-effort [`FileRunTracer`](../backend/app/observability/run_trace.py). Current trace configuration caps a serialized payload at 10 MB and excludes raw provider payloads. | **Partial capture.** A complete captured runner result must be authoritative for evaluation; trace events and summaries are supplemental. Test truncation/failure handling before any formal run. |
| V3 pre/post | [`V3Outcome`](../backend/app/versions/v3/state.py) retains `draft`, `final_primary`, original/final reports and repair metadata on successful returns. V3 trace can replace an oversized outcome with a truncation marker. | **Usable when both artifacts are captured.** Missing pairs remain unavailable. Reports, scope, target IDs, and acceptance stay in a mechanism-only channel. |
| External evidence | Neutral [`PlacesProvider` and `RoutesProvider`](../backend/app/integrations/protocols.py), request/response DTOs, and Google adapters exist. Place details include current/regular hours and time zone; route matrix responses retain status, condition, and fallback fields. | **Provider layer reusable; oracle absent.** Build evaluation-owned request policy, limits, cache, evidence persistence, timestamps, and failure records. Planner `RequestCache` and acquired evidence cannot be the oracle. |
| Independent quality scoring | No current evaluator module implements the accepted independent RTPEval rules. V3 validation, Repair, route policy, and opening adoption contain planner judgments. | **Specification and implementation required.** Quality scoring may read only captured planner output, independently reviewed requirement specification, and frozen evaluation snapshot. |
| Requirement and identity review | Current interpreted requirements and POI semantic assessments are planner-owned. V0 may name a place without a canonical ID. | **Specification required.** Independently review requirements; resolve identities with recorded alternatives, adjudication and an audit sample. Do not treat Google top result or planner interpretation as truth. |
| Usage and latency | V1–V3 budget/trace data are useful but best-effort and stage-specific; V0 has no symmetric trace. `budget.json` describes application counters and explicitly does not establish provider billing. | **Recording contract required.** Separate attempted calls, actual sends, cache hits, reported tokens, elapsed wall time, missing usage, and evaluation oracle cost. Preserve failure attempts. |
| Benchmark and analysis | The [design](evaluator_design.md) specifies the accepted structure but leaves opening/route semantics, outcomes, identity, controlled fixtures, exact analysis, and optional repeats open. | **Not frozen.** Resolve and version these contracts before held-out results are exposed. |

## Current-code changes affecting the specification

1. The V0 prompt now requests estimated same-day transport activities and optional Nearby suggestions. Treat transport activities as planner claims; compute independent route feasibility from the applicable place visits and oracle evidence. References remain unscheduled and outside primary quality denominators.
2. Shared primary-visit semantics now distinguish valid POI roles, `minimum`/`exact` visit counts, dates, source-grounded category goals, and incomplete adopted outputs. The independent requirement specification must model supported obligations without copying the runtime interpreter's conclusions. Planner `policy_completion` is a product diagnostic, not the evaluator result.
3. One qualifying main visit per non-exempt day is a confirmed **product-policy** minimum in V3, while two-to-five visits remains guidance. Current V3 also identifies unauthorized same-day/cross-day repeats as confirmed product-policy targets; optional repetition review remains distinct. Controlled Sparse and Duplicate families must therefore label each case by its actual rule and authorization. Overfull review alone is not a confirmed defect.
4. Berlin is now a development-exposed city because of the four-version smoke and subsequent V0 revalidation. Those outputs preceded the latest V0 prompt on the original four-version block, so they are development evidence, not matched main-study results. Historical logs also retain their original trace limits.
5. The supplementary **V3 vs Codex + Travel Planning Skill** comparison currently needs only an adapter-compatible output slot in the module design. Its Codex environment, skill, tools and execution protocol remain separate open specification work.

## Proposed module boundary for the next specification

Use a version-neutral `RunArtifact` captured outside the planners. Normalize only the fields required for independent checks into an `EvaluationItinerary`; preserve the original serialized result and provenance. A separately reviewed `RequirementSpec` and evaluation-owned `EvidenceSnapshot` complete the quality scorer's input. The scorer produces per-check outcomes with numerator, denominator, structural evaluability, evidence coverage, evidence compliance, `UNKNOWN`, `N/A`, and reasons. A separate mechanism reporter can consume V3 reports, Repair rounds, RAG and resource traces; it cannot alter the quality score.

Collect the four outputs of a matched request block before collecting the union of independent Places and directed route evidence. Persist that snapshot and score offline. This is a data-flow contract, not authorization to call services now. Design the adapters so a future Codex result can enter through the same common itinerary boundary without giving it access to V3 internals.

## Open decisions before a buildable RTPEval v1 module specification

- Exact `RunArtifact` terminal outcome taxonomy and required capture fields, including failures before a runner creates its own run ID.
- Formal definition of evaluable place-bearing activities, especially V0 estimated transport, generic/unknown roles, and explicit transport activities.
- Opening interval and route interval semantics, including partial/failed provider evidence and time zones.
- Human-reviewed `RequirementSpec`, identity resolution confidence/adjudication record, and review budget.
- Controlled target/control cases against the current confirmed product-policy versus improvement distinction.
- Dimension subscores and an auxiliary reliability/constraint-compliance total are accepted as secondary presentation measures. Normalization, weights, missingness, coverage gates and sensitivity rules remain OPEN and must be frozen before use; the primary results stay multi-metric.
- Analysis plan, held-out eligibility, complete artifact/cost capture gate, and optional 144/192-run decision. Development evidence, not held-out results, should inform the latter.

The next deliverable is a draft module specification with explicit interfaces, failure behavior and acceptance checks. It remains a draft until the open evaluation rules and analysis plan are resolved and approved. The readiness audit neither authorizes implementation nor starts formal evaluation.
