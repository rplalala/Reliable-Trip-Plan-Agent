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

Save local progress keyed by presentation/task; provide explicit JSON download/import so browser storage is not the only copy. No server, account system or remote submission is assumed. Import validates IDs, presentation revision, allowed labels, group completeness and duplicate submissions. Retain revisions and identify the effective submission reproducibly, not by an accidental last filesystem write. The accepted 2026-10-02 correction rule below supersedes the earlier manually selected final-submission proposal.

Researcher-side aggregation joins the private mapping after response validation. Derive six correlated pair outcomes from a complete four-plan ranking per dimension: earlier tie group wins; same group ties. Report wins/ties/losses and available denominators separately per dimension. Unassessable/N/A answers do not become ties. Duplicate consistency is descriptive agreement of each underlying pair's win/tie/loss between original and duplicate, with comparable pair count; no inter-rater statistic or extra main-result weight.

## Verification seams

Future offline checks cover source hashes and path integrity, missing optional usage, N/A contribution arithmetic, role/transfer projection, ranking partition validation, answer revisions, private-key absence from HTML/export and deterministic label replay. No schema code, HTML, benchmark artifact or tests were created by this design document.

## Projection specialization — 2026-09-29

[intake-projection-contract.md](intake-projection-contract.md) specifies Ticket 01's material diagnostics, tolerant wire reading, independent role review and transport correspondence. A required usage envelope may explicitly declare observations unavailable. Source identity is artifact hash plus JSON pointer within batch/group/run, not a potentially reused activity ID alone. No provider duration is silently converted into a claimed arrival during projection.

## Ticket 02 implementation specialization — 2026-09-29

[Usage capture contract](usage-capture-contract.md) and [capture guide](../../backend/app/observability/USAGE.md) define the implemented producer-owned sidecar. Distinct model/provider/cache event arrays and stage/Repair subsets retain provenance. Exact result-byte serialization supplies the hash. Collection can be partial even when timing is available; custom adapter coverage is not inferred. Resource comparison requires all four selected envelopes and never feeds quality scoring.


## Selected-run provenance wire - 2026-09-30

Every selected run requires an available `provenance_ref` using the normal relative-path, exact-byte SHA-256 and JSON media/schema checks. Its object has `schema_version=rtpeval_provenance_1`, `group_id`, `run_id`, `version`, `input_sha256` and `result_sha256`. These fields must exactly match the selected group/run/version and complete input/result file hashes. Missing or contradictory provenance is a batch material error. Additional configuration fields may remain explicit metadata. This validates producer-supplied linkage, not the truth of an unobserved execution or a recomputation of qualification. Legacy deliveries without this association must supply the sidecar; intake does not infer it from file names or itinerary content.

## Ticket 05 semantic wire specialization — 2026-10-01

[Requirement/schedule](requirement-schedule-contract.md) defines executable fields on
`rtpeval_requirements_1`, independent time-context and occupancy-review envelopes,
and `rtpeval_requirement_schedule_report_1`. Required source/review envelopes remain
unchanged; the current intake's accepted status is not typed scoring validation.
Scorer preflight must report malformed executable payloads/known contradictions as
material correction while retaining semantic/time/identity uncertainty in reports.
Independent schedule context is optional; absence does not infer a timezone.
No parser, metric report or CLI from this specialization is implemented yet.

## Ticket 08 proposed quality report specialization — 2026-10-02

[Specification preflight](ticket-08-preflight.md) defines the proposed aggregate wire;
no Ticket 08 report or CLI is implemented. Use schema_version=rtpeval_quality_report_1
consistently with current executable reports, specializing the earlier generic
report_schema_version field description. Include batch_id/batch_revision, generated_at,
rules_profile_id/hash, component schema/rule hashes, exact source-file hashes and
canonical replay/preparation digests, stage availability, group records and diagnostics.

Each group retains one ordered mask, included-dimension count and exactly four selected
final run records. Each dimension preserves P/F/U/N/A where the producer defines those
units, applicability/denominator availability, exact numerator/denominator pairs,
fractional rates, explicitly scaled 0-100 verified score and separate contribution.
Excluded activity/role/protection records retain their own typed population; they do not
become extra weighted units. Preserve original check/measurement/reason/evidence records.

Known zero applicability, unresolved denominator and absent/corrupt source material are
different states. True single-version no-check N/A has null raw rates and zero included
contribution. Unresolved full-scope denominator has null score/contribution/affected total;
all-four true N/A is excluded and an empty mask has null total plus diagnostic. Material
or replay correction yields empty groups rather than a silently reduced cohort.

The pure report boundary uses an explicit offset-aware generation timestamp; CLI may
generate UTC metadata or accept --generated-at. Stable content hashing excludes generation
metadata and the content hash itself. Fixed sources/rules/timestamp reproduce canonical
JSON; source/rule hashes are retained even when generation metadata is excluded.
Internal-findings-only source changes require properly relinked identity/snapshots; numeric
invariance does not imply identical provenance hashes or permission to reuse stale evidence.
No optional-track aggregation, paired V3 totals, live acquisition or formal analysis is
authorized by this specification specialization.

## Ticket 08 executable wire — 2026-10-02

The approved report/CLI now implements `rtpeval_quality_report_1`; see
[acceptance](ticket-08-acceptance.md) and the [package guide](../../backend/evaluation/README.md).
`QualityReportResult` is immutable; `build_quality_report` requires an explicit aware
`generated_at`, and the CLI supports UTC metadata or `--generated-at`. Root component
metadata preserve emitted schema/rules/hash provenance; original row source hashes
remain in each version's `component_source_hashes`. `source_hashes.artifacts` retains
intake's exact-file hash map; preparation object digests and CLI file-byte hashes are
distinct. The CLI recalculates `content_hash` after adding `preparation_file_sha256`.
Each group exports `included_dimensions`, rational `dimension_weights`, four `versions`
and `all_totals_available`. Each version retains `primary_metrics`, normalized
`dimensions`, descriptive/schedule/occupancy records and `auxiliary_total`. Raw N/A,
unresolved population and material failure remain distinct. Complete replay uses exit 0
even with FAIL/UNKNOWN or null totals; material/replay correction uses exit 2 and empty
groups. A valid paired snapshot is unsupported scope, not corruption. Resource/human/
mechanism report availability remains separate from source usage/optional projection
metadata. Earlier proposed/not-implemented statements retain their historical dates.

## Ticket 09 preflight decisions — 2026-10-02

[Preflight](ticket-09-preflight.md) records source/UI inspection and accepted decisions;
no human package, answer importer or report has been implemented. The researcher reviews
prospective display content before delivery. Explicit version/provider/internal-review
text requires source-linked manual redaction that preserves travel facts and uncertainty;
original bytes and private original/display/reviewer linkage remain intact. Unsafe
unresolved leakage blocks delivery. The rater receives anonymous content and independently
ranks it. Structural allowlists and escaping do not replace free-text review.

The user accepts answer corrections: a new complete submitted revision supersedes the
previous effective answer. Use the highest valid submitted answer_revision per task/rater,
retain earlier revisions for audit only, and record the effective revision/content hash.
Drafts do not replace submitted answers. Identical imports are idempotent; differing
content with the same revision is a conflict, not a last-import-wins rule.

For a missing source arrival, the user accepts an additional explicitly labelled inferred
display time from the selected source's valid unambiguous departure plus duration. Retain
the original departure/duration and missing-arrival notice; preserve estimate/unknown
wording, offsets and cross-date rollover. Missing/ambiguous operands give an unavailable
inference notice. No new route evidence/provider call, timezone assumption or hidden
reserve is added. The source arrival remains absent, and the computed display value
never becomes a planner claim or scorer input. A supplied arrival is never overwritten.
This specializes blind display only; it does not relax quality projection rules.

## Ticket 09 executable wire — 2026-10-02

The approved offline seams now implement `rtpeval_human_preparation_1`,
`rtpeval_human_config_1`, `rtpeval_human_display_reviews_1`, `rtpeval_human_package_1`,
`rtpeval_human_mapping_1`, `rtpeval_human_answer_1`, `rtpeval_human_answers_1`,
`rtpeval_human_import_1` and `rtpeval_human_report_1`. Answer records retain
answer_schema_version; bundle/package/report roots use schema_version. Public batch
identifiers are opaque aliases and presentation_hash links exact frozen public content.
The private mapping retains source hashes, prospective preparation, complete display
review, actual label assignments and duplicate references. New complete submitted
answer_revision supersedes old effective answers while draft/history records remain
separate. Import conflicts reject the whole requested material rather than reducing it.
Mapped pair counters/missingness and duplicate consistency remain descriptive outputs.
Use explicit aware generated_at for pure report replay; CLI may generate UTC metadata.
[Package usage](../../backend/evaluation/README.md#ticket-09-local-blinded-ranking-workflow)
documents executable fields/commands. [Acceptance](ticket-09-acceptance.md) owns actual
validation/review/browser status; implementation does not authorize real assessment.

## Ticket 09 approved time-zone display extension — 2026-10-02

The user approved an independent renderer dropdown, default UTC, converting supplied
offset-aware activity/transport/inferred timestamps with local browser Intl into
selected IANA-zone dates and 24-hour HH-mm clocks. Source days remain original groups,
source timestamps remain inspectable, missing zones are never guessed and invalid
values retain explicit uncertainty. Date-only/free-text values remain unchanged.
Public/mapping/answer schema versions, original source bytes and presentation hashes
are unchanged; display choice is not added to answer records or scoring input.
[Scope and acceptance](ticket-09-timezone-display.md) owns actual extension evidence.

## Subsequent user display cleanup — 2026-10-02

The user removed the optional Original timestamp UI requirement and corrected current
clocks to 24-hour HH:mm. The dropdown/converted dates/source day grouping remain.
Original timestamp strings are retained in frozen artifacts, while missing/invalid
times and source uncertainty/inferred-arrival notices retain their explicit evidence.
No source, public/private schema, presentation hash, answer or scorer change is made.
[Cleanup acceptance](ticket-09-display-cleanup.md) records the superseding UI rules and
actual validation; earlier inspectable-control/HH-mm records remain historical.
