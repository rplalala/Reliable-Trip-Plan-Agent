# Offline evaluation preparation and metrics (Tickets 01-06)

Ticket 01 prepares a user-curated batch; Ticket 03 replays independent identity observations; Ticket 05 scores requirements and submitted schedule occupancy; Ticket 06 scores opening from verified snapshots. The package does not run planners, acquire live evidence through a built-in client, calculate the auxiliary quality total, render blind tasks or call an external service from its offline commands. It imports no planner modules and uses the Python standard library plus the already installed `tzdata` for timezone provenance.

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

The module consumes previously recorded observations only. Ticket 04 acquires/persists evidence through separately authorized injected transport. An empty review queue means workflow completion, not that every place is grounded: reviewed unresolved identities remain UNKNOWN. Grounding fractions are verified coverage, not hallucination rates. Ticket 05 consumes these identities; opening, route, auxiliary-score and formal comparison work retain separate tickets.

## Validation

Tests generate disposable synthetic artifacts in pytest temporary directories. They are not formal benchmark cases. Run:

```powershell
.venv/Scripts/python.exe -m pytest backend/tests/evaluation -q -rs
.venv/Scripts/ruff.exe check backend/evaluation backend/tests/evaluation
```

No provider acquisition, real model call, database access or V0-V3 algorithm change is part of this module.


Ticket 03 follow-up (2026-09-30): the details-only shortcut recognizes only a matching numbered street component with a supported English street suffix. Generic country/admin/postcode components require competition search. Search/details name or full-address disagreement enters review even when IDs agree. Separate titles must equal the place name or `Visit <name>` for automatic acceptance; other prose is left for adjudication. These conservative recognizers can increase unresolved coverage for valid venues. Malformed optional IDs remain per-reference uncertainty without aborting the batch. See the contract for exact recognition limits.


Ticket 01/02 follow-up (2026-09-30): overlapping visit intervals produce source-linked `overlapping_visit_intervals` diagnostics and mark affected candidate adjacency unresolved; display sorting does not repair chronology. Available/partial usage envelopes require explicit model/provider/cache event arrays (empty is valid, absent is not). Duplicate cache IDs are rejected like model/provider duplicates. Repair token subtotal is null when no Repair token value was observed; a measured zero stays zero and partial known values remain an observed subtotal.


## Ticket 04: independent snapshots

The snapshot module provides offline request preparation, acquisition through an explicitly injected async transport, and immutable local replay. It has no built-in Google client, credentials, database, planner cache, or live CLI. See [snapshot contract](../../.scratch/rtpeval/snapshot-contract.md) for the exact wire and [acceptance](../../.scratch/rtpeval/ticket-04-acceptance.md) for verification.

```powershell
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli identity-plan C:/batch/manifest.json --paired
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli replay C:/snapshots/identity --expected-plan C:/batch/identity-plan.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli identity-evidence C:/snapshots/identity
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli evidence-plan C:/batch/manifest.json C:/batch/identity-report.json C:/batch/route-contexts.json --paired
```

Commands write JSON to stdout. Exit 0 means a valid plan/replay, not complete evidence or a quality PASS; exit 2 means material/snapshot correction is needed. An empty contexts array is valid and leaves candidate legs explicitly pending. Replay never performs acquisition.

Python API: `build_identity_plan`, `build_evidence_plan`, `acquire_snapshot`, `load_snapshot`, and `identity_evidence`. Acquisition requires `AcquisitionPolicy(max_sends=...)` and a caller-owned async callable receiving a detached request descriptor and returning `Response(status_code, body_bytes)`. Return exact raw bytes; raise `TransportFailure` with a supported safe category for a failed dispatch. Credentials and network serialization remain in the separately authorized transport integration. Programming errors/cancellation abort without publishing a manifest; interrupted directories cannot be reused or replayed automatically.

Workflow: prepare identity requests, acquire to a fresh directory with a separately authorized transport, replay to an identity envelope, run Ticket 03 adjudication/audit, then prepare canonical details and explicit route contexts. Available V3 draft/final_primary projections are included only when paired is requested. Unresolved references and unrequested legs remain inventoried. Identical requests share evidence without merging occurrences. One-cell route matrices avoid full union cross products. Current/regular hours, timezone, coordinates and unrounded duration strings remain in raw evidence for later offline scorers.

The oracle ledger records sends, retry sends and requested matrix elements separately from planner usage. Snapshot deduplication is local to one plan; future reruns use a new directory. Collection times form an interval. Planner-to-oracle lag is explicitly unavailable until independent planner times exist. Provider applicability, operational storage/retention settings, live budgets and factual accuracy are not established by synthetic acceptance.


## Transport responsibility correction - 2026-09-30

Implemented in the current workspace: V0 retains model-estimated transport activities. V1-V3 share a primary generation schema excluding transport and an output acceptance check rejecting declared transport activities; both initial and Repair prompts explicitly reserve transport selection and transfer times to the application. Supplied route evidence can inform visit spacing. Existing Routes selection/binding and Repair operation permissions remain unchanged. A forbidden declared activity fails generation without adding a retry. Semantic transport disguised under another role cannot be comprehensively detected mechanically.

Independent evaluation now selects transport sources by planner version: V0 activities, V1-V3 transfers, including optional V3 projections. Ignored records retain source pointers and diagnostics but supply no evaluated transport occupancy/fallback; missing transfers stay missing. Source identity tuples are unchanged. `transport_source`, `ignored_transport` and activity `transport_applicable` expose this distinction for later scoring. Independent evidence remains the factual oracle. Same-source duplicate/conflict handling and distinct visit occurrences are preserved. This supersedes the historical equal-authority Activity/Transfer reconciliation checkpoint. Ticket 05 scoring and protected-time union were pending at this 2026-09-30 checkpoint; see the subsequent implementation below. No live calls, formal experiments, commit/push or freeze were included in that correction task.


Transport correction validation: final backend suite **1973 passed, 10 skipped (85.49s)**; nine opt-in database cases and one Windows symlink privilege case were skipped. New boundary tests first reproduced forbidden-source acceptance. DTO fixture mismatches and a test nesting error were corrected. Spec review caught a contradictory shared prompt instruction, removed while retaining V0's explicit transport instruction; follow-up reviews have zero remaining findings. The first full run stalled and was interrupted; its runtime retrieval file passed separately (16 tests). The next full run exposed five superseded V3 transport expectations; updated boundary tests passed (119), followed by the successful final full run. Ruff, compilation and diff checks passed. See the transport correction acceptance record under .scratch/rtpeval for the complete sequence and limitations.


Subsequent checkpoint (2026-09-30): the separately authorized planner smoke and
workspace commit closeout are recorded in [development acceptance](../../docs/transport_responsibility_smoke.md).
Earlier uncommitted/no-live statements describe their dated implementation scopes;
the planner smoke does not validate independent oracle acquisition or scoring.

## Ticket 05: offline requirement and schedule metrics

The [contract](../../.scratch/rtpeval/requirement-schedule-contract.md) defines the
reviewed executable payloads; [acceptance](../../.scratch/rtpeval/ticket-05-acceptance.md)
records implementation validation. Invoke from the repository root:

```powershell
.venv/Scripts/python.exe -m backend.evaluation.requirement_schedule_cli C:/batch/manifest.json C:/batch/identity-report.json --context C:/batch/schedule-context.json --occupancy-reviews C:/batch/occupancy-reviews.json
```

The optional flags may be omitted. `--paired` evaluates available V3 `draft` and
`final_primary` projections independently; it does not calculate Repair deltas.
Library entry: `score_requirement_schedule(intake, identity_report,
schedule_context=None, occupancy_reviews=None, paired=False)` returns an immutable
result. CLI output is JSON on stdout, with input file hashes; input files are never
rewritten. Exit 0 means a complete analysis, including content UNKNOWN or FAIL;
exit 2 means material correction or identity replay is required. Save output separately.

Report schema is `rtpeval_requirement_schedule_report_1`. Executable semantic
validation follows accepted intake without changing Ticket 01's tolerant reader.
Invalid operators/types/sources and detectable contradictory quotas return
`needs_material_correction` with no partial result cohort. A stale, incomplete or
previous-scope identity report returns `identity_replay_required`. Re-run the offline
identity resolver using retained evidence/reviews/audit: newly prepared reports include
`subject_scope_version=required_excluded_fixed_time_1` and `reference_set_digest`.
Fixed-time-only subjects use the same high-impact adjudication policy. An intact
`needs_adjudication` report is permitted; its unresolved identities remain uncertainty.

Requirements use explicit reviewed counts: exact/minimum, optional distinct dates and
dated quotas remain components of one parent check. Unstated named-visit cardinality
is authored upstream as exact one; evaluation never reads planner requirement prose.
`fixed_visit_time.match=single_visit` includes trip-wide exact one; `at_least_one`
requires verified original-input `repeat_permission_refs`. One visit must satisfy the
complete time conjunction. Unlinked/unclassified annotations or unresolved unknown
kinds make the requirement denominator unavailable; linked annotations and reviewed
soft preferences add no weighted checks. Empty reviewed hard requirements give N/A
only when completeness is established.

Time context uses `rtpeval_schedule_context_1`, nonempty string `batch_id`/`revision`
and `groups`. Each group provides exact `group_id`/`input_sha256`, IANA `timezone`,
nonempty string `source_ref`, `reviewer_ref` and offset-aware `reviewed_at`.
`source_ref` references independently collected or reviewed factual evidence; a
reference/hash establishes linkage, not authenticity. Missing groups are permitted
as missing context. No host/planner zone is inferred. Aware intervals retain instants
without a zone; local-clock checks need one. Naive DST folds/gaps and offset/date
conflicts remain UNKNOWN. Fractional timestamp precision up to six digits is retained;
greater precision is explicitly unsupported rather than truncated. Protection uses
local midnight to next local midnight, including 23/25-hour DST days.

Occupancy review schema is `rtpeval_occupancy_reviews_1`, with string `batch_id`/
`revision` and `records`. Each record supplies the exact activity `source` object
from intake, string `revision`, reviewer/time/rationale, `occupancy=committed|uncommitted|unresolved`,
and optional `protected_obligation_refs`. It decides flexibility/correspondence,
never roles, identities, transport endpoints or alternatives. Unknown/stale/duplicate
links and known contradictory correspondence require correction. Role-ambiguous
activities still require Ticket 01 role preparation. Named visits remain commitments;
unreviewed generic locationless placeholders are automatically flexible only when
notes supply no further commitment claim. Nonempty unclear notes conservatively need
review. A protection placeholder is excluded only through an exact reviewed link;
uncertain correspondence keeps applicability and the denominator unresolved.

Protection union preserves date and scope and never adds a score unit. Each primary
visit, reviewed fixed generic activity and source-selected logical journey supplies
one non-overlap check. V0 disjoint segments preserve gaps; duplicate sources share
one journey; V1-V3 use Transfers without model-activity fallback. Mode uncertainty
alone does not erase explicit occupancy. Same-journey conflicts are alternatives;
all alternatives may prove a conflict, while their common interval evidence remains
a lower bound. Unbound claims and unresolved roles/flexibility preserve candidate units
and prevent a full-scope rate. Missing journeys affect structure coverage, not an
invented occupancy interval. Non-overlap covers all submitted commitments, including
extra output dates; requirement counts and descriptive denominators use requested dates.

Reports distinguish positive unordered pair intersections, their summed seconds,
commitment-conflict union, protection-conflict union and combined conflict union.
Scheduled occupancy and protected reservations remain separate. Unknown duration is
null, never a fabricated zero. Daily attribution needs independent time context;
whole-request known instants remain available without it. Date coverage, density and
adopted-canonical repetition are descriptive; missing requested days remain zero known
visit days, extra dates are diagnostic, and unknown identities preserve repetition
lower bounds. Revisit quotas are displayed without an invented repetition penalty.
Opening/route feasibility, five-dimension totals, blind tasks and Repair comparison
remain separate tickets. V0-V3 planning behavior and execution paths are unchanged.


## Ticket 06: offline opening compliance

Invoke from the repository root using accepted intake and an independently replayed
identity report. The snapshot must be an evidence-phase snapshot matching both:

```powershell
.venv/Scripts/python.exe -m backend.evaluation.opening_cli C:/batch/manifest.json C:/batch/identity-report.json C:/batch/evidence-snapshot --context C:/batch/schedule-context.json --expected-plan C:/batch/trusted-plan.json
```

`--context` and `--expected-plan` are optional. `--paired` includes available V3 draft
and final_primary projections independently, with the same paired snapshot scope.
No Repair delta or route verdict is calculated. Library entry:
`score_opening(intake, identity_report, snapshot_directory, schedule_context=None,
*, paired=False, expected_plan=None)` returns immutable `OpeningResult`.
Schema: `rtpeval_opening_report_1`; rules: `rtpeval_opening_rules_1`.

Exit 0 means complete processing, including visit FAIL/UNKNOWN; exit 2 means material
correction or identity replay. JSON is printed to stdout. Preparation file hashes,
canonical intake/identity/context/rule hashes, snapshot manifest hash and expected/
actual plan hashes remain auditable. Submitted bytes are never rewritten. Save the
report outside its source artifacts. CLI constructs no provider/model/database client.

Whole-batch source/policy validation precedes scoring. Source corruption, stale phase/
paired scope or incomplete request linkage returns no partial cohort. Identity policy,
references, review/audit metadata and source mismatch requires identity replay.
Valid but failed observations and missing/malformed hours produce visit UNKNOWN.
Mixed snapshots keep supplied route contexts and verify their linkage without choosing
routes. Optional trusted full-plan equality includes those routes; canonical opening
references/details are checked even without that optional plan.

One check is emitted per primary occurrence. Repeated canonical places remain repeated
checks; Nearby and requirement-subject-only records add no visit. Nonapplicable
activities and unresolved roles retain source/reason records. Applicable counts are
known occurrences; `applicable_denominator` is null while roles are unresolved.
Full-scope percentages, including conditional compliance, are then unavailable.
`counts` covers primary checks; nonapplicable records carry their own N/A/UNKNOWN states.
Empty applicable scope has state N/A and unavailable rates, never 100 percent.

Every check records original start/end, normalized UTC interval, declared date, source,
canonical identity, independent timezone/origin, provider timezone version when supplied,
actual installed zone-file hash/basis, selected details attempts/raw hashes, reasons and
explanation. Clock evaluability and identity availability are separate. Explicit offset/
date contradictions, naive DST folds/gaps and precision beyond six fractional digits
remain UNKNOWN. `allow_cross_date=True` is opening's explicit opt-in; Ticket 05's
same-date time behavior remains unchanged. Reversed same-date clocks are never repaired.

Opening uses original raw `currentOpeningHours` and `regularOpeningHours`. It retains
field presence, weekly/dated endpoint meaning and literal truncation. Optional endpoint
day/hour/minute require actual integer values; absence is not zero. Explicit applicable
`periods: []` means closed, while missing/null/invalid values remain unavailable.
Regular Sunday 00:00/no-close is the documented always-open sentinel; arbitrary current
missing-close periods do not imply continuous access. Split periods retain lunch gaps;
overnight and previous-day contributions and weekly rollover are supported.

Current applicability uses the selected attempt's place-local request date plus six
calendar dates. Post-trip current hours cannot become historical evidence. Applicable
current defects block regular substitution; eligible outside dates use weaker regular
fallback. Known special dates lacking usable applicable current evidence remain UNKNOWN
with the exceptional-hours explanation. Collection crossing local midnight retains
uncertainty, while consistent literal dated spans may still prove opening. A truncated
23:59 close does not invent closure or opening in the final minute. Each date segment
records `selected_basis` and factual `basis`; unusable evidence has basis unavailable.
A visit's factual basis is current, regular, mixed or unavailable.

Half-open containment has zero grace: ending at close can PASS; any positive known
closure overlap yields FAIL even with other unknown time. Partial valid spans may prove
PASS containment but cannot establish a closed complement without bounded completeness.
Verdict, complete/partial/missing evidence, clock/identity availability and basis counts
are separate. Conditional compliance is PASS/(PASS+FAIL), including partial FAIL;
complete-evidence coverage and verdict-decidable coverage use the applicable population.
Two PASS plus one partial FAIL gives compliance 2/3, complete coverage 2/3 and decisive
coverage 1 when the first two visits are complete.

`outside_seconds` is exact only when all time is known; otherwise null.
`confirmed_outside_lower_bound_seconds`, `known_open_seconds`, `unknown_seconds` and
open/closed/unknown segment intervals preserve what is established. Missing visit
magnitude stays null; known zero stays zero. Integer microsecond interval measurement
prevents floating subtraction from hiding a fractional conflict. Duration summaries
are labelled observed per-visit subtotals with observed/missing counts; they do not
claim complete full-batch magnitudes or a global-time union.

[Acceptance](../../.scratch/rtpeval/ticket-06-acceptance.md) records the actual development
failures, corrections, retests and review. [Preflight](../../.scratch/rtpeval/ticket-06-preflight.md)
retains the approved decisions and original inspection checkpoint. Opening fixtures are
offline/synthetic; separately authorized local database/native checks are recorded in
acceptance and acquire no provider evidence. No provider availability, future factual certainty or booking/access
claim follows from this implementation. V0-V3 planner paths remain unchanged.

## Ticket 07: offline same-day routes

Public seams are `prepare_routes(intake, identity_report, schedule_context=None,
occupancy_reviews=None, route_reviews=None, coordinate_evidence=None, *, paired=False)`
and `score_routes(intake, identity_report, snapshot_directory, schedule_context=None,
occupancy_reviews=None, route_reviews=None, coordinate_evidence=None, *, paired=False,
expected_plan=None)`. Immutable RoutePreparation/RouteResult serialize independent
copies with `to_dict()`. Schemas are rtpeval_route_preparation_1/rtpeval_route_report_1;
rules rtpeval_route_rules_1. Preparation never reads route observations. It returns
source-preserved candidate legs, selected intervals, reasons, route_contexts and a
complete Ticket 04 evidence_plan. Acquisition still needs a caller's injected transport.

From the repository root:

```powershell
.venv/Scripts/python.exe -m backend.evaluation.route_cli prepare C:/batch/manifest.json C:/batch/identity.json --context C:/batch/context.json --route-reviews C:/batch/route-reviews.json --coordinates C:/batch/coordinates.json
.venv/Scripts/python.exe -m backend.evaluation.route_cli score C:/batch/manifest.json C:/batch/identity.json C:/batch/snapshot --context C:/batch/context.json --route-reviews C:/batch/route-reviews.json --coordinates C:/batch/coordinates.json --expected-plan C:/batch/trusted-plan.json
```

Optional flags are --context, --occupancy-reviews, --route-reviews, --coordinates and
--paired; score also supports --expected-plan. Deterministic JSON goes to stdout.
Exit 0 means complete processing including quality FAIL/UNKNOWN; exit 2 means whole
material correction or identity replay. No supplied file is rewritten. Save reports
outside source artifacts. Snapshot CLI uses `{"contexts": preparation["route_contexts"]}`
as its context wrapper. Neither new CLI command acquires evidence or creates sockets,
provider/model/database clients, repair deltas or auxiliary totals.

### Independent preparation formats

Reuse existing rtpeval_schedule_context_1 and rtpeval_occupancy_reviews_1 unchanged.
Source/obligation/occupancy validators were moved to private _schedule_preparation.py
without Ticket 05 policy changes. No new executable RequirementSpec kind was added.

rtpeval_route_reviews_1 requires batch_id, nonempty revision and groups. Each unique
group links group_id/input_sha256 with reviewer_ref and offset-aware reviewed_at:

- status unrestricted explicitly reviews the absence of hard mode constraints;
  no policies are supplied. Missing review is UNKNOWN, never guessed unrestricted.
- status restricted requires nonempty policies, each with unique policy_id, original
  Input source_refs, nonempty allowed_modes subset of WALK/TRANSIT/DRIVE, and scope
  whole_trip or specified_dates. The latter requires unique inclusive-request dates;
  whole_trip has no dates. Empty intersections require correction.
- status unresolved requires reason, with source_refs where available.

Optional stated_mode is `{"mode": "WALK", "source_refs": [...]}`: an independently
reviewed exact original-input mode, distinct from a soft preference or allowed set.
It supplies mode only if no usable itinerary mode fixes one and conflicting claims
are not hidden. Missing Transfer remains missing in claim coverage. Hard restrictions
need policy records; query defaults do not invent them. Source references reuse exact
field/quote/occurrence/Unicode-offset validation. Extraction/review is supplied external
preparation; the evaluator does not parse unrestricted prose or run an LLM.

rtpeval_route_coordinates_1 requires batch_id, nonempty revision and records. Each
unique adopted canonical place_id record has latitude/longitude (strict finite numeric
values in range), lowercase 64-hex evidence_sha256, independent source_ref, reviewer_ref
and offset-aware reviewed_at. Never borrow planner locations. This supplied review is
a trust boundary: the hash links evidence, but the evaluator does not certify coordinate
facts or acquire the referenced source. Exact coordinate/hash correspondence gates
query applicability. Missing coordinates retain pending contexts and UNKNOWN.

Optional mode_options maps modes to `{"time_basis": ..., "routing_options": {...}}`.
Defaults deliberately use time_independent WALK, time_independent DRIVE with explicit
TRAFFIC_UNAWARE, and explicit_departure TRANSIT. Explicit queries use the adopted
departure; time-independent queries use null departure and retain the estimate label
and acquisition timestamp, without claiming historical query support. Ticket 04 wire
validation and Ticket 07 provider/mode applicability are distinct: supported preferences,
modifiers/locales and exact departure are checked when interpreting frozen evidence.
Unsupported valid-wire context stays UNKNOWN without shifting dates or modes.

### Selection and scoring

Keep consecutive primary occurrences within each delivered day; no inter-day routes.
Confirmed same-canonical legs are N/A; distinct venues at one address remain distinct.
V0 uses Activity claims, V1-V3 Transfers without ignored-Activity fallback. Duplicate
claims keep all sources but one leg. Conflicting Transfer or segmented/mixed Activity
journeys never become a favorable uninterrupted single-mode matrix claim.

Subtract applicable scheduled_commitments protections and fixed other occupancy from
the endpoint gap, excluding this leg's own transport. Preserve original obligation IDs
and scopes through blocker union. primary_visits-only protection does not block traffic.
Possibly overlapping unknown occupancy stays uncertain; known disjoint alternatives do
not contaminate unrelated routes. A guaranteed common occupation starting at the deadline
is a hard boundary; a merely possible deadline occupation stays UNKNOWN and cannot borrow
next-visit tolerance. Explicit departure controls and must fit one free span.
Otherwise choose the longest continuous fragment, tie earliest UTC start, before route
observations. Never concatenate spans, try a later fragment after failure or switch mode.

For provider duration d, reserve r and selected G, retain raw deficit max(0,d+r-G).
Hard protection/fixed-commitment deadlines require d+r <= G with zero grace; only the
next-visit deadline permits 300 seconds. DRIVE reserve is 600 seconds once, others zero.
Separate caps are WALK/TRANSIT 2700+300 seconds, DRIVE 1800+300 seconds, and WALK distance
<=3000 meters with no distance tolerance. Tolerances never sum. Exact and within-tolerance
PASS are labelled. Shared rule constants drive arithmetic and the emitted rules/hash.

Verify raw replay and full identity/occurrence/request reconstruction before scoring.
Corruption, foreign/unused linkage or wrong paired scope returns no partial cohort.
Valid wrong mode/departure/coordinates/options is inapplicable UNKNOWN evidence;
optional trusted plan additionally enforces exact acquisition-plan equality.
Historical non-TRANSIT explicit query is unsupported relative to acquisition; TRANSIT
and time-sensitive DRIVE need applicable explicit departure. No Compute Routes transit
horizon is copied into matrix policy. Query/itinerary clocks support six fractional
digits; provider durations preserve integer nanoseconds, without float rounding.

Parse raw status/condition independently of the available summary. Require a status
object: omitted code within it means default zero, malformed/error status stays UNKNOWN.
Successful ROUTE_NOT_FOUND FAILs with null duration/deficit; contradictory route fields
invalidate that observation. ROUTE_EXISTS uses nonnegative duration strings with up to
nine fractional digits, never staticDuration or rounded seconds. Missing WALK distance
or duration keeps its component UNKNOWN. Valid returned traffic fallback is accepted
and traced. Any independently proven component FAIL decides the leg; all required
components must PASS for combined PASS, otherwise UNKNOWN.

Report source claims/mode basis, selected fragment and deadline, component reasons and
classification, exact measurements, nominal caps/tolerances/reserve, expected/actual
query, raw attempts/hashes and preparation/source/rule/plan/manifest hashes. Structural,
applicable response, full-component, decisive and duration-available coverage differ.
No-route is decisive without duration; partial FAIL enters P/(P+F) without becoming
complete evidence. Unknown is null travel, never zero. Unresolved role/adjacency
populations and empty denominators suppress full-scope rates.

Daily/request sum, median and maximum are observed per-occurrence subtotals with missing
and unresolved counts; reserve is separate. Request deduplication never merges score
occurrences. Unknown potential legs prevent complete burden claims globally and on the
affected days. No route/overlap double weighting, auxiliary arithmetic, V3 repair delta
or formal comparison is calculated. Synthetic development tests do not establish real
provider availability, historical/future travel certainty or benchmark outcomes.

[Ticket 07 acceptance](../../.scratch/rtpeval/ticket-07-acceptance.md) records actual TDD,
review findings/corrections and regression results. The
[preflight](../../.scratch/rtpeval/ticket-07-preflight.md) preserves the original proposals,
accepted user decisions and subsequent explicit implementation authorization.
