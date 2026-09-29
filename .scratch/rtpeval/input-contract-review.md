# Evaluation input contract: code-informed review

Status: Facts checked; separate per-version result files and upstream reviewed RequirementSpec accepted. Detailed schema remains OPEN.
Date: 2026-09-28.
Source checkpoint: 8a435e2db0198e4fc8928b85e333b45b66c0c981, with uncommitted evaluation documentation. Read-only code inspection; no execution, tests or provider calls.

## Confirmed field mapping

| Needed input | Current source | Contract implication |
| --- | --- | --- |
| Original request | PlanningRequest: input_version, destination, start_date, end_date, traveler_count, budget, additional_preferences, optional request_id | Preserve the materialized input; result.requirements is not an exact substitute. |
| Request fingerprint | PlanningRequest.structured_hash derives structured trip fields only | Add a separately named evaluation fingerprint covering preferences and the entire materialized request; do not repurpose the existing hash or assume request_id is present. |
| Selected final | PlanningResult.system_version and itinerary, inherited by V1-V3 results | One neutral final-output adapter can start from the shared itinerary field; provenance is a separate envelope. |
| Activity correspondence | Itinerary.days[].activities[].activity_id | IDs are unique within an itinerary, not necessarily persistent across Repair; qualify by group/run/artifact. |
| Place reference | activity_kind, title, place_name, source_place_id, location | Preserve missing IDs and roles. Resolve externally; IDs are not automatically identity ground truth. |
| Times and amounts | start_time/end_time, estimated_cost, notes | Preserve original time strings/offsets and uncertainty. No mandatory destination IANA timezone exists in the itinerary; timezone resolution requires a separate explicit contract. Null cost is not zero. |
| Transport | Itinerary.transfers plus activities with transport role | Keep model-generated transport distinct from application-owned transfer claims. validation_state and provider durations are planner claims, not independent oracle verdicts. |
| Optional V3 pair | V3PlanningResult.v3.draft and v3.final_primary | Use these linked fields for Repair before/after when present; final top-level itinerary additionally carries Nearby attachments. Missing draft cannot be reconstructed from final. |
| Requirements | TravelRequirements; V1-V3 interpreted_requirements | These are planner-produced and must not become independent RequirementSpec. Current VisitRequirement has minimum/exact/date/access semantics useful as a vocabulary reference only. |

## Intake versus scoring

Batch material integrity is not workflow completion or itinerary quality. Do not re-run live request validity checks using the evaluation date: a historically valid trip can already be in the past at batch handoff. Preserve original schema/version and execution provenance. Missing optional usage/draft only makes the dependent report unavailable.

Do not blindly use every current product-model validator as the evaluation intake filter. Some validators reject schedule/reference inconsistencies that evaluation may need to describe. The eventual adapter must distinguish unreadable/missing structure from represented but inconsistent travel content; exact tolerant parsing policy remains OPEN. Preserve raw bytes and do not silently correct data.

## Accepted packaging and authorship

Each group delivers four separate complete result files: `v0_result.json`, `v1_result.json`, `v2_result.json`, and `v3_result.json`. Do not combine four results into one JSON file. The manifest references each file and hash; the adapter extracts its itinerary while isolating internal findings from quality scoring and human presentation.

RequirementSpec is prepared during benchmark construction from the original Input, with assistant drafting permitted and explicit user review required. Evaluation only consumes the reviewed artifact: it does not generate, infer, repair or silently complete obligations. Missing, unreviewed or structurally invalid specifications produce intake diagnostics for upstream correction; explicitly recorded unresolved semantics remain unresolved.

## Source references

- Shared request: backend/app/schemas/request.py.
- Shared output and activities/transfers: backend/app/schemas/planning.py and itinerary.py.
- Additional supply/RAG fields: backend/app/schemas/planning_supply_result.py and backend/app/versions/v2/state.py.
- V3 pair and final Nearby boundary: backend/app/versions/v3/state.py and wiring.py.
- Planner obligation vocabulary: backend/app/schemas/interpreted_requirements.py.


## Runner and capture findings

The CLI scripts delegate to version runners; results are printed as complete serialized result JSON, not automatically saved to a standardized result file. Benchmark-side collection must retain this output (or the full returned object) and assign artifact names/hashes. V0 returns the shared result without a symmetric trace, run ID or usage record. Group/run identifiers in the handoff envelope must therefore be producer-assigned and distinct from optional native trace IDs.

V1-V3 tracing is best-effort and size-bounded; a successful result does not guarantee a trace. Oversized trace payloads can become truncated previews. V3 adds request_resources after shared planner finalization and retrieval shutdown, so the earlier trace final_outcome is not a replacement for the returned result. Trace timing begins after some input/configuration work and cannot be labelled complete attempt latency. Preserve measured scope for every duration; absent actual usage is missing, not zero.

Source anchors: V0 runner serialization and main; V1 shared runner serialization/main and run_tools_planner; V3 runner finalization at lines 130-138. The shared trace format exposes system_version; its legacy system_stage label must not be used to identify the evaluated version. No capture behavior was executed in this review.
