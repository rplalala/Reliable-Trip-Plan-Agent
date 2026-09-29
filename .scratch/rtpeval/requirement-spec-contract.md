# RequirementSpec contract — draft

Status: Responsibility split and semantic scope consolidated from accepted decisions; field draft pending precise rule and serialization contracts. Not frozen or implemented.
Date: 2026-09-28.
Source: shared request and interpreted-requirements schemas at checkpoint 8a435e2db0198e4fc8928b85e333b45b66c0c981. Documentation changes are uncommitted. This is an evaluator contract proposal, not a formal benchmark case.

## Ownership and authority

Benchmark preparation authors a separate requirement_spec.json for each original input. An assistant may draft from that input only; the user reviews it before delivery. The file is independent of all planner outputs and is never injected into their execution. Evaluation reads explicit reviewed fields and never invents requirements from prose. The original Input remains the rater's only request description; this specification is hidden during blind assessment.

The file describes user obligations, not Google facts or desired itineraries. EvidenceSnapshot owns opening and route evidence. Identity records own canonical adjudication. EvaluationRules owns product-default policy, tolerance and scoring formulas. A user obligation and a product default must not be silently conflated.

## Envelope field draft

| Field | Meaning |
| --- | --- |
| schema_version | Independent RequirementSpec version; not the planner interpreted_requirements version. |
| spec_id / revision / group_id | Stable linkage and correction history. |
| input_sha256 | Link to exact delivered original Input under the batch hashing convention, including preferences. |
| review | Explicit reviewed status, reviewer reference and review time; assistant authorship is separate from approval. |
| subjects | Named places referenced by obligations, retaining original wording and independent subject IDs. Optional reviewed canonical bindings reference identity records rather than planner IDs. |
| obligations | Explicit machine-readable user requirements with source references and semantic resolution state. |
| soft_preferences | Source-grounded preferences for descriptive context, not invented hard pass/fail targets. |
| unresolved_items | Ambiguous, conflicting or unsupported clauses and reviewed reasons; do not erase these clauses from the record. |

Every source reference identifies an original input field and, for text, a verbatim quote and occurrence/offsets. Structured dates or budget can refer directly to the field path. Do not cite planner-normalized wording as the source. Exact timestamp, hash serialization and source-offset encoding remain wire-contract details to finalize.

Review and semantic resolution are separate: a human-reviewed specification may explicitly acknowledge unresolved semantics. Review does not turn uncertainty into a hard obligation. Changing meaning creates a new revision and an affected-report record.

## Obligation field draft

Common fields: obligation_id, kind, source_refs, resolution (resolved/unresolved/unsupported), reason when not resolved, and subject_ref when applicable. Unresolved payloads must not contain invented executable values.

| Kind | Payload and interpretation |
| --- | --- |
| required_visit | subject_ref; count with mode minimum or exact and positive value; distinct_dates when specified; date_obligations. Each date obligation states its own minimum/exact count rather than implying a global exact count. |
| excluded_visit | subject_ref and explicit date scope (whole trip or specified dates). It concerns scheduled primary visits under the existing scope, not unscheduled Nearby references. |
| protected_time | Explicit dated full-day or clock interval in destination-local time, together with the reviewed meaning of what must not be scheduled. Current planner TimeProtection represents protected time, not arbitrary ticket/appointment execution guarantees. |
| fixed_visit_time | A named visit and explicit start/window/duration obligation only when actually supported by a separately defined evaluation rule. Keep unsupported variants recorded rather than treating them as implemented planner capability. |

Trip dates and destination originate in Input; do not hand-copy a competing set of base trip facts into this file. Date obligations must lie within the supplied trip scope or be recorded as a reviewed conflict. A combined exact count lower than the required per-date minimum is a specification conflict, not a planner failure. Any sum/count validation depends on whether visits must occur on distinct dates; do not infer duplicate semantics from raw appearance counts.

## Already accepted interpretation constraints

- Minimum and exact counts are distinct. Visits beyond a minimum do not automatically violate the user obligation; non-required repetition is reported separately under its own rule.
- Date obligations are explicit and not replaced by a global visit count.
- Nearby cannot satisfy required visits.
- Soft preferences and pace descriptions do not silently become hard daily-count or travel-minute thresholds.
- No verified budget obligation is activated in v1; preserve Input budget for presentation/descriptive reporting only.
- Missing identity evidence and unclear user meaning are different states. Canonical uncertainty belongs to identity adjudication; reviewed semantic uncertainty remains visible as structural unevaluability for dependent checks.
- Evaluator cannot substitute result.requirements or interpreted_requirements for this specification.

## Deterministic requirements versus subjective preferences

RequirementSpec contains reviewed executable obligations, descriptive preferences and explicit unresolved/unsupported items in separate collections. The distinction follows the original request's meaning, not the ease of producing a score. Evaluation never rewrites prose into new constraints.

- A clear must-visit maps to minimum one unless an explicit count/date obligation says otherwise; the benchmark author writes this before review.
- An explicit dated clock interval or full day that must remain unscheduled is suitable for a protected_time check. Exact activity-role inclusion, boundaries and timezone interpretation belong to the time rule, not hidden defaults in this file.
- "Wednesday afternoon" does not by itself specify clock boundaries. Unless an independently justified interpretation is reviewed upstream, retain the time ambiguity; the evaluator must not silently define afternoon as 14:00-17:00.
- "Relaxed", "interesting architecture" and "small museums" remain source-grounded preferences for human judgment. Descriptive densities, categories and transfers may be reported but do not automatically prove preference satisfaction.
- An explicit measurable constraint is not converted to a soft preference merely because its evaluator is unimplemented. Mark unsupported rule coverage honestly and retain the original clause.
- A resolved user meaning with unavailable external evidence remains different from unresolved user meaning. The former can lead to evidence UNKNOWN; the latter cannot acquire a PASS just because evidence exists.

The human reviewer prepares this file from Input. The blinded rater sees Input and itineraries only; they are not asked to author this file, verify external facts or calculate compliance.

## Completeness and unresolved-content handling

Each relevant explicit clause is represented by a supported obligation or an unresolved/unsupported item with its source and reason. A request with no named obligations can have an explicitly reviewed empty obligations list. An empty list is not a missing file. Human preparation is responsible for semantic completeness; Evaluation validates structure/linkage, not whether a language model can discover additional obligations.

Missing approval, missing required structure or a mismatched input fingerprint is an intake diagnostic. A reviewed unresolved clause does not itself make the package malformed: expose its dependent-check unavailability and preserve it in reporting. A mechanically detectable contradictory executable payload is returned for upstream correction, not counted as an itinerary violation. Do not silently drop unresolved clauses or manufacture a denominator from them; metric-specific structural evaluability and denominator rules must state how they are represented.

No numeric threshold, opening exemption, identity binding or tolerance may be inferred from a subjective phrase. Explicit settings must cite the reviewed obligation or versioned EvaluationRules, and the report must retain that distinction.

## Code-informed boundaries

PlanningRequest contains structured dates and free-text additional_preferences. Its structured_hash omits those preferences. Planner VisitRequirement supports minimum_visits, exact_visits, dates, distinct_dates and nullable access_mode (venue_entry/exterior). These are vocabulary evidence, not evaluator ground truth or a reusable scoring validator. The planner access_mode field is deliberately not adopted by RequirementSpec v1.

Planner TimeProtection supports full-day or same-day local intervals with fixed/unresolved status. It does not establish that every natural-language arrival, appointment, daily-pacing or overnight restriction has a supported executable contract. The independent specification must retain unsupported semantics without claiming capability that the current output cannot demonstrate.

## Accepted simplifications — 2026-09-28

1. An explicit unqualified must-visit statement is authored as an explicit minimum-one obligation during benchmark preparation and reviewed by the user. Evaluation does not supply this default. Ambiguous count language remains unresolved.
2. RequirementSpec v1 does not distinguish venue entry from exterior viewing. Do not add access_intent/access_mode, separate satisfaction rules, or infer the distinction from itinerary prose or V3 bindings. The delivered itinerary does not reliably express this distinction. Original request wording is preserved for provenance and blind presentation, but independent scoring assesses the scheduled place visit without claiming verified interior access.
3. Opening applicability is defined uniformly in the separate opening contract. No exemption or additional penalty is inferred solely from entry/exterior phrasing. Explicit access-mode-specific evaluation is outside v1.

## Future acceptance checks

Check exact versus minimum, multiple date duties, contradictory total/date counts, source linkage, missing approval, unresolved semantics, unsupported time constraints, and independent namespace for subject/obligation IDs. Verify evaluator does not generate a new obligation when the corresponding reviewed field is absent. Also check reviewed empty obligations, missing versus unresolved content, ambiguous afternoon wording, and that qualitative preferences never create automatic hard thresholds. These checks have not been implemented or run.
