# Offline evaluation preparation (Tickets 01 and 03)

Ticket 01 prepares a user-curated batch; Ticket 03 replays independent identity observations against it. The package does not run planners, acquire live evidence, calculate the auxiliary quality total, render blind tasks or call an external service. It imports no planner modules and uses the Python standard library.

## Entry points

Run from the repository root:

```powershell
.venv/Scripts/python.exe -m backend.evaluation C:/batch/manifest.json
```

The command prints JSON to stdout, never writes the submitted package, and returns exit code 0 for accepted preparation or 2 for material correction. Do not redirect stdout over a submitted input artifact. Library entry: `backend.evaluation.intake.load_batch(path)`. It returns a frozen `IntakeResult`; `to_dict()` provides an independent serializable copy.

An accepted intake result is not an itinerary PASS or a claim that every metric is evaluable. Role, clock and correspondence diagnostics remain visible. A fatal material error returns no partial inventory. The five-dimension quality scorer is unimplemented.

## Manifest and envelope vocabulary

Concrete schema identifiers for this implementation:

- Manifest: `rtpeval_batch_1`.
- RequirementSpec: `rtpeval_requirements_1`.
- Usage envelope: `rtpeval_usage_1`.
- Optional independent projection reviews: `rtpeval_reviews_1`.
- Derived source IDs: `rtpeval_projection_1`.
- Original input: `planning_request_2`; itinerary: `itinerary_1` or `itinerary_2` (absent itinerary version is recorded as historical).

Manifest fields: schema_version, batch_id, revision, created_at, qualification_policy_ref, selected_group_ids and groups. Identity/revision fields are nonempty strings. Each group has group_id, completion_attested=true, input_ref, requirement_spec_ref and selected_runs containing exactly v0/v1/v2/v3. The group list follows selected_group_ids order. A selected run has globally unique run_id, result_ref and usage_ref.

Every reference has a relative path, exact-byte SHA-256, media_type=application/json and availability=available. Requirement/usage/review references additionally specify their schema_version. A result reference has no invented schema_version: the result identifies system_version and the itinerary identifies output_version. Original result files are kept intact and only allowlisted itinerary fields enter projection. Artifact paths are resolved inside the manifest directory, including link resolution.

RequirementSpec contains schema_version, spec_id, revision, group_id, input_sha256, review, subjects, obligations, soft_preferences and unresolved_items. review has status=reviewed, reviewer_ref and reviewed_at. Subjects use subject_id; obligations use unique obligation_id, kind, resolution and original-input source_refs. Named visit obligations link subject_ref. Top-level input field_path plus verbatim quote/occurrence and optional Unicode offsets supports source verification. An empty reviewed obligation list is valid. This intake validates delivery/linkage; operator execution and full metric-specific requirement semantics belong to Ticket 05.

A usage envelope is required even if collection is unavailable: schema_version, group_id, version, run_id, result_sha256 and collection_status (available/partial/unavailable). Additional measurement fields remain in the original artifact for Ticket 02; absence never becomes zero. Each selected run requires a hashed `provenance_ref` sidecar with `schema_version=rtpeval_provenance_1`, `group_id`, `run_id`, `version`, `input_sha256` and `result_sha256`. All five linkage fields must match the selected group/run and exact input/result bytes. Intake retains the provenance file hash in the run inventory. Additional configuration metadata is not promoted to quality evidence.

## Independent review replay

Optional projection_reviews_ref points to an envelope with schema_version, batch_id and records. Each record has group_id, run_id, artifact_sha256, pointer, reviewer_ref, reviewed_at, revision and rationale. The pointer addresses an activity under /itinerary, /v3/draft or /v3/final_primary. Stale/duplicate decisions are rejected.

Optional decisions: role (primary_visit/transport/transition/unresolved), mode (WALK/TRANSIT/DRIVE or null), paired from_activity_id/to_activity_id, and multi_poi=true for a confirmed delivery violation. These are human-reviewed evaluation preparation facts, not planner findings or preferences. A changed result hash requires a new reviewed association rather than automatic reuse.

A main_poi declaration or structured named venue supports a visit candidate, not identity confirmation. Generic placeholder labels are recognized conservatively; unclear prose goes to role review rather than an LLM. Place names occurring only in prose may require review. Automatic positional transport binding is limited to simple movement labels with no endpoint-bearing prose and a unique containing gap. Rich descriptions, aliases or conflicting content require independent review. Multiple unresolved roles conservatively make that day's candidate adjacency unresolved. These limitations remain observable and are not hidden denominator reductions.

Transport associations preserve all claims. Matching mode/start/end representations share occupancy sources; sequential activity segments remain separate intervals; competing Transfer/activity intervals become alternatives. No arrival is invented from provider duration. Protected requirements remain separate from transition placeholders, keyed by obligation ID, for later occupancy scoring. Unknown timezone/time context is preserved; there is no machine-local conversion.

Nearby is a separate unscheduled source inventory. The future renderer must hide it as specified, and must strip private mapping/source identifiers. This package emits researcher preparation data, not a rater-ready artifact.

## Identity replay (Ticket 03)

```powershell
.venv/Scripts/python.exe -m backend.evaluation.identity_cli C:/batch/manifest.json C:/batch/identity-evidence.json C:/batch/identity-audit.json --reviews C:/batch/identity-reviews.json
```

`--reviews` is optional; the evidence and audit-plan files are required. Exit 0 means the review queue is empty, 3 means adjudication is pending, and 2 means intake/evidence correction is needed. Output goes to stdout and includes original source references, per-visit/subject records, a reviewer queue and per-version grounding/claimed-ID counts. Save it separately from submitted inputs. Python entry points are `identity_references(intake)` and `resolve_identities(intake, evidence, reviews, audit_plan)` in `backend.evaluation.identity`.

The [Ticket 03 contract](../../.scratch/rtpeval/identity-implementation-contract.md) defines `rtpeval_identity_evidence_1`, `rtpeval_identity_audit_1` and `rtpeval_identity_reviews_1`. V0 name-only claims can resolve through strict independent name search; supplied IDs require independent details association. Missing/ambiguous evidence, aliases, competing candidates, ID/name conflicts and high-impact requirement matches go to factual review. The preselected audit sample also stays pending until reviewed. The reviewer queue hides version labels; researcher records retain source linkage. A reviewed intended place can resolve while its incorrect supplied ID remains a separate conflict. No provider rank or V3 finding decides identity.

The module consumes previously recorded observations only. Ticket 04 must acquire/persist real evidence under its own authorization and connect it to this handoff. An empty review queue means workflow completion, not that every place is grounded: reviewed unresolved identities remain UNKNOWN. Grounding fractions are verified coverage, not hallucination rates. Requirement, opening, route, auxiliary-score and formal comparison work belong to later tickets.

## Validation

Tests generate disposable synthetic artifacts in pytest temporary directories. They are not formal benchmark cases. Run:

```powershell
.venv/Scripts/python.exe -m pytest backend/tests/evaluation -q -rs
.venv/Scripts/ruff.exe check backend/evaluation backend/tests/evaluation
```

No provider acquisition, real model call, database access or V0-V3 algorithm change is part of this module.


Ticket 03 follow-up (2026-09-30): the details-only shortcut recognizes only a matching numbered street component with a supported English street suffix. Generic country/admin/postcode components require competition search. Search/details name or full-address disagreement enters review even when IDs agree. Separate titles must equal the place name or `Visit <name>` for automatic acceptance; other prose is left for adjudication. These conservative recognizers can increase unresolved coverage for valid venues. Malformed optional IDs remain per-reference uncertainty without aborting the batch. See the contract for exact recognition limits.


Ticket 01/02 follow-up (2026-09-30): overlapping visit intervals produce source-linked `overlapping_visit_intervals` diagnostics and mark affected candidate adjacency unresolved; display sorting does not repair chronology. Available/partial usage envelopes require explicit model/provider/cache event arrays (empty is valid, absent is not). Duplicate cache IDs are rejected like model/provider duplicates. Repair token subtotal is null when no Repair token value was observed; a measured zero stays zero and partial known values remain an observed subtotal.
