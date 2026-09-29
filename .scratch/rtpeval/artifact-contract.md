# Evaluation artifact and human-answer contract

Status: Technical design under the accepted module scope; not implemented or frozen.
Date: 2026-09-28.

## Batch layout and integrity

A delivered local batch has a manifest plus a directory per group. Each group contains input.json, requirement_spec.json, v0_result.json through v3_result.json, and v0_usage.json through v3_usage.json. This describes future delivery, not directories or benchmark cases created by this task. Optional artifacts are referenced explicitly rather than discovered by guessing filenames.

Manifest fields: schema_version, batch_id, revision, created_at, selected_group_ids, qualification_policy_ref, groups, provenance. Each group lists group_id, input_ref, requirement_spec_ref, and exactly four selected_runs keyed by v0-v3. Each selected run records run_id, result_ref, usage_ref and provenance_ref. Each artifact reference carries relative path, SHA-256, media type, schema version where known, and availability. Producer qualification is attested, not recomputed by Evaluation.

Hash exact UTF-8 file bytes. Use input_sha256 to link the complete original input including preference text; do not substitute structured_hash. Reformatting produces a new artifact hash/revision. Do not rewrite provider or planner JSON to make a hash match. Generated report values may use canonical JSON serialization but must cite exact source-byte hashes. Relative artifact paths resolve inside the submitted batch; reject escape paths, duplicate group/run IDs, missing required files, mismatched version labels and unknown major contract versions.

Existing product result JSON remains unchanged. The adapter extracts top-level itinerary; V3 draft/final_primary are optional additional projections linked to the same selected run. Mechanism fields are accessible only to their reporter. No secrets/raw credentials are part of provenance. Missing provenance values are explicit, not inferred from filenames.

## RequirementSpec wire shape

Envelope fields follow requirement-spec-contract.md: schema_version, spec_id, revision, group_id, input_sha256, review, subjects, obligations, soft_preferences and unresolved_items. review contains status, reviewer_ref and reviewed_at, with draft_author_ref optional. A reviewed empty obligations list is valid. Missing review or input linkage is an intake error.

Each source reference uses field_path, quote and occurrence (zero based); offset_start/offset_end, when included, count Unicode code points in the original decoded field and use a half-open range. Validate the quote against the source; never rewrite wording to fit it. Structured input references may omit quote/offsets. Review identifiers need not expose personal names in public reports.

Obligations have stable obligation_id, kind, resolution, source_refs, reason when unresolved, and typed payload. required_visit uses subject_ref, count.mode (minimum/exact), count.value, distinct_dates when explicitly reviewed and date_obligations. Each date obligation has date, count_mode and count. excluded_visit has subject_ref and scope (whole_trip/specified_dates). protected_time has explicit local date interval and reviewed scope. Unsupported fixed-time operators remain recorded, not executed as guessed constraints. No entry/exterior field is introduced.

Subject identity and interpretation are separate. Subject records retain the reviewed place wording and source refs, with optional identity_record_ref after independent adjudication. A planner's interpreted_requirements is never substituted. Review changes produce a new specification revision and affected-report record.

## Usage file shape and ownership

Each usage file contains schema_version, group_id, version, run_id, result_sha256, collection_status, timing, model_calls, provider_events, stage_summaries, repair_summary, and missing_fields. Each observation identifies source_ref and status (reported/measured/estimated/missing as appropriate). Zero is stored only for a measured/reported zero; unavailable values use null with a reason.

Timing declares scope, started_at, finished_at and elapsed_seconds measured using a monotonic clock. A common outer boundary starts immediately before the selected version invocation and ends after its complete result/final resource cleanup or error. File preparation, evaluator work and human assessment are outside planner elapsed time. Stage timings can overlap and do not replace outer elapsed time. This is a collector requirement; current capture is not claimed compliant.

A model call records call_id, provider/model identity when available, stage, optional round_id, outcome, usage provenance and input/output/total tokens. Reported totals remain reported; a sum derived from complete reported components is labelled derived, never billed usage. Missing component usage remains missing. Retries are distinct calls; repeated snapshots of one call are not additional consumption.

A provider event records event_id, provider/operation, stage, outcome, transport send status and requested element_count where applicable. Count actual sends separately from cache hits and logical processing attempts. Record failures and retries. Stage and Repair totals reference underlying event IDs and are subsets, not extra charges. Oracle acquisition uses its own ledger.

A usage file can explicitly declare unavailable collection while preserving run linkage. Missing resource observations never become a planner-quality failure; malformed linkage is a material diagnostic. Benchmark-side instrumentation is a prerequisite for usable cost comparisons and requires its own approved implementation.

## Reports and numeric serialization

Every report includes report_schema_version, batch_id/revision, rules_profile_id/hash, source hashes, generated_at, stage availability and group records. A check records check_id, metric_id, unit_refs, applicability, status, reason_code, explanation, evidence_refs and raw measurements. A dimension records P/F/U counts, N/A counts, raw rate, coverage, unknown rate, verified score, contribution and common-mask membership.

Serialize absent raw values as null, never NaN/Infinity. Keep seconds internally with decimal precision; display rounding does not change boundary checks. For N>0 compute scores from unrounded counts, and round displayed percentages only. Individual N/A dimensions have null raw ratios and zero numeric contribution when included in the common mask. Group-wide N/A is excluded jointly. Record total_included_dimensions; do not silently compare different masks.

Diagnostics are material errors, adjudication requests or report availability reasons, not automatic cohort deletion. A corrected material package or adjudication creates a versioned revision; prior reports remain reproducible.

## Human presentation and answers

Generate a static local HTML package from an explicitly supplied group selection and recorded label assignment seed. Within a task, anonymous A/B/C/D remain fixed across preference/pace/usefulness. Across tasks use a balanced randomized permutation schedule, with actual assignments frozen in a researcher-only mapping. Duplicates get independent task IDs/assignments and remain outside main counts. The HTML and answer export contain no version labels, mapping key, raw result filenames, canonical IDs or automatic scores.

Render the original request fields and the same dated activity fields for all versions: title, displayed place, start/end, notes and displayed amounts when present. Nearby is hidden under the existing agreed presentation. Preserve uncertainty and meaningful content without an LLM rewrite. Use the same visual template and chronological ordering. Uniformly display transport from structured transfers or transport activities without creating duplicate journeys; no provider badges or internal validation status. Exact transfer correspondence must be independently traceable; ambiguous presentation is flagged rather than fabricated. Blinding cannot guarantee that itinerary content never suggests a version.

Answers are JSON with answer_schema_version, batch_id/revision, presentation_id, task_id, rater_ref, answer_revision, updated_at and one response per dimension. A ranked response uses ordered tie_groups (for example [[A,C],[B],[D]]); every label occurs exactly once. Alternative states are unable_to_judge or not_applicable with optional reason and no fabricated ordering. Support pending/incomplete drafts separately from submitted complete answers.

Save local progress keyed by presentation/task; provide explicit JSON download/import so browser storage is not the only copy. No server, account system or remote submission is assumed. Import validates IDs, presentation revision, allowed labels, group completeness and duplicate submissions. Retain revisions and select an explicitly identified final submission, not an accidental last filesystem write.

Researcher-side aggregation joins the private mapping after response validation. Derive six correlated pair outcomes from a complete four-plan ranking per dimension: earlier tie group wins; same group ties. Report wins/ties/losses and available denominators separately per dimension. Unassessable/N/A answers do not become ties. Duplicate consistency is descriptive agreement of each underlying pair's win/tie/loss between original and duplicate, with comparable pair count; no inter-rater statistic or extra main-result weight.

## Verification seams

Future offline checks cover source hashes and path integrity, missing optional usage, N/A contribution arithmetic, role/transfer projection, ranking partition validation, answer revisions, private-key absence from HTML/export and deterministic label replay. No schema code, HTML, benchmark artifact or tests were created by this design document.

## Projection specialization — 2026-09-29

[intake-projection-contract.md](intake-projection-contract.md) specifies Ticket 01's material diagnostics, tolerant wire reading, independent role review and transport correspondence. A required usage envelope may explicitly declare observations unavailable. Source identity is artifact hash plus JSON pointer within batch/group/run, not a potentially reused activity ID alone. No provider duration is silently converted into a claimed arrival during projection.

## Ticket 02 implementation specialization — 2026-09-29

[Usage capture contract](usage-capture-contract.md) and [capture guide](../../backend/app/observability/USAGE.md) define the implemented producer-owned sidecar. Distinct model/provider/cache event arrays and stage/Repair subsets retain provenance. Exact result-byte serialization supplies the hash. Collection can be partial even when timing is available; custom adapter coverage is not inferred. Resource comparison requires all four selected envelopes and never feeds quality scoring.


## Selected-run provenance wire - 2026-09-30

Every selected run requires an available `provenance_ref` using the normal relative-path, exact-byte SHA-256 and JSON media/schema checks. Its object has `schema_version=rtpeval_provenance_1`, `group_id`, `run_id`, `version`, `input_sha256` and `result_sha256`. These fields must exactly match the selected group/run/version and complete input/result file hashes. Missing or contradictory provenance is a batch material error. Additional configuration fields may remain explicit metadata. This validates producer-supplied linkage, not the truth of an unobserved execution or a recomputation of qualification. Legacy deliveries without this association must supply the sidecar; intake does not infer it from file names or itinerary content.
