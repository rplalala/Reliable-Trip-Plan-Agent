# Ticket 08 multimetric report specification preflight

Date: 2026-10-02, Australia/Sydney. Inspected code revision:
30960c67a7cf0f88093e5a0d47632112408d7404 on feature/evaluation.
The initial working tree/index were clean. Status: specification/interface inspection
complete; the concrete offline implementation proposal below requires separate approval.
Nothing in this record claims implemented Ticket 08 scores, a new benchmark or a freeze.

Current follow-up: the user subsequently approved this concrete implementation scope
and local commits without push. [Ticket 08 acceptance](ticket-08-acceptance.md) owns the
actual implementation, validation, review and Git follow-up. Pending-approval statements
below preserve the original preflight checkpoint rather than current authorization.

## Authority, task and authorization

[PROJECT](../../PROJECT.md) owns current scope; [AGENTS](../../AGENTS.md) owns approval,
language, Git and archive boundaries. GitHub [Issue #20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20)
owns Ticket 08 task state, not the historical [local snapshot](issues/08-quality-report-scores.md).
The Issue body and its empty comment list were read. Tickets 05, 06 and 07 are closed/
completed; their actual interfaces and current local contracts supersede migration-era
wording that those predecessors were unfinished. Ticket 08 remains open/unimplemented.

The user authorized specification preflight only, explicitly excluding implementation.
This covers relevant current inspection, existing offline regression checks, this record,
related current documentation/archive and tracker synchronization. It does not authorize
new backend/test modules, planner changes, live services, database/native supplements,
formal evaluation/inference, Git writes, push, freezes or Ticket 09+ work.

Accepted arithmetic comes from [score profile](score-profile.md), not the conditional
compliance fields already exported by individual scorers. Current [metrics](metrics-contract.md),
[artifact](artifact-contract.md), [requirement/schedule](requirement-schedule-contract.md),
[opening](opening-contract.md) and [route](route-contract.md) contracts define source units
and uncertainty. The [package guide](../../backend/evaluation/README.md) documents executable
Ticket 01-07 seams; historical OPEN/not-implemented statements retain their dated scope.

## Existing executable seams and adaptation

| Dimension | Current source | Report adaptation, without changing its policy |
| --- | --- | --- |
| Explicit requirements | score_requirement_schedule: requirements.checks/counts, denominator and denominator_unresolved | One parent obligation per unit; preserve kind/component records and unclassified completeness diagnostics. |
| Canonical grounding | Validated identity replay records indexed by reference_id plus primary_visit projection occurrences | Resolved primary visit = verified PASS; unresolved identity = UNKNOWN; no inferred fabrication FAIL. Supplied-ID conflicts remain separate. Do not trust a caller-edited identity summary as counts. |
| Schedule non-overlap | score_requirement_schedule: non_overlap.checks/counts, denominator and candidate_unit_count | One logical timed commitment per unit, not one pair; protected intervals are not extra score units. |
| Opening compliance | score_opening: opening.checks/counts and applicable_denominator | One primary visit per unit. Decisive partial FAIL enters F while evidence completeness remains separate. |
| Route compliance | score_routes: routes.checks/counts and applicable_denominator | One applicable same-day leg per unit; use the combined verdict, not separate extra weights for cap, distance or timing. Preserve same-venue N/A and unresolved populations. |

Current identity_ready accepts complete or needs_adjudication replay with exact source/
reference/policy linkage; unresolved identities are valid report observations, not grounds
for dropping a version. Pending identity review may therefore leave known units UNKNOWN.
Missing/stale/invalid replay is identity_replay_required, not four zero quality scores.

The grounding producer currently exports grounding_fraction among confirmed primary visits
and separately unresolved_role_activities. The aggregate must not present that partial
fraction as a full-scope score when roles are unresolved. Derive primary-visit identities
from validated records and preserve the unresolved-role count as denominator availability.
Requirement subject references are not visits and cannot add grounding units.

The other producers already suppress full-scope rates for unresolved requirement
completeness, commitment grouping, visit roles or leg populations. Preserve that behavior;
do not convert an unresolved population record into one invented UNKNOWN check.

## User clarification and existing-contract reconciliation

The initial preflight question used an example of three confirmed visits plus an activity
whose role was unresolved, asking whether an unavailable dimension should suppress a total
or contribute an accounting zero. The user asked what role uncertainty meant and then
correctly identified main_poi paired with a title such as Walk to Museum A as a labeling
error. That is a declaration/content conflict, not an ordinary failed place lookup.

Existing projection.classify explicitly retains such conflicts as role_review_required;
independent role review or upstream correction can resolve them. This preflight does not
change that classifier, silently repair source fields, introduce a new label-error penalty,
or claim the user approved either offered scoring alternative.

The proposed zero contribution for unresolved denominators is not adopted. Existing
Ticket 05 unit rules already prohibit a complete score until unresolved applicability/
grouping is resolved. Follow that boundary: keep partial checks, counts and reasons;
the affected full-scope dimension has null rates/verified score/contribution, and a total
requiring it is unavailable. This is distinct from the already accepted zero contribution
for a proven N/A/no-check dimension inside a common mask. It preserves the earlier goal
of numeric scores for packages whose applicable units are established, without guessing
units in unresolved packages. Corrected/reviewed material is replayed as a new revision.

## Fixed score and mask rules

Use the fixed dimension order: requirements, grounding, non_overlap, opening, routes.
For an established denominator N = P + F + U > 0:

- Verified score = 100 * P/N; this is the auxiliary input.
- Verification coverage = (P+F)/N, unknown rate = U/N, confirmed violation rate = F/N.
- Conditional compliance = P/(P+F), or null when P+F is zero; it is diagnostic only.
- Keep applicable, known-unit, structural, evidence and unresolved-population counts
  separate. UNKNOWN receives no verified-success credit but is never relabeled FAIL.
- Grounding uses resolved/P and unresolved/U primary visits; its F count is zero under
  the accepted identity-coverage definition. Claimed-ID contradictions retain raw counts.

Producer measurements retain their original unit/scales. Export normalized fractions in
the range 0-1 and explicitly named 0-100 score fields. Preserve exact numerator/denominator
pairs; compute means from unrounded rational values before converting for JSON display.
Never average producer-rounded percentages. Numerical display precision changes no rule.

Determine one included-dimension mask for the entire selected four-version group:

1. Exclude a dimension only when all four prove true no-check applicability, with no
   unresolved denominator. An empty reviewed obligation list is true N/A only when
   there is no unlinked unclassified requirement content.
2. If any version has applicable units or unresolved applicability, retain the dimension
   for all four. Unknown populations are not evidence of common N/A.
3. For an included dimension with proven N=0 in one version, keep raw state/rates/score
   N/A/null and P/F/U unchanged; set its separate contribution to zero with no-checks.
4. For an included dimension with unresolved denominator, keep contribution null and
   that version's total null with denominator_unresolved. Keep the common mask unchanged.
   Other versions whose denominators are established may retain their own numeric totals;
   expose that not all four totals are available. Never renormalize the affected version.
5. For an empty common mask, every total is null with no_scorable_dimensions. No invented
   zero/100, denominator one, or partial mask. This remains an upstream reconciliation
   diagnostic, not an ordinary itinerary-quality failure.

For m included dimensions, weights are 1/m and total = mean of their contributions.
Record exact total fraction, total_included_dimensions, mask and each zero/unavailable
reason. Do not assert totals with different masks measure the same content. No pooled
cross-request total, confidence interval, hypothesis test or version ranking is proposed.

Check-unit N/A counts retain producer meaning. Opening excluded activity records, identity
role diagnostics and protected boundaries are not manufactured into weighted visits or
commitments; preserve them as separately typed records rather than forcing uniform counts.

Arithmetic examples (specification examples, not executed results):

- P=2, F=0, U=8: verified score20, coverage0.2, conditional compliance1, unknown rate0.8.
- P=0, F=0, U=10: verified score0, coverage0, conditional compliance null; no ten FAILs.
- Four active dimensions each score80 and one included true no-check dimension:
  contribution0 yields total64; that dimension's raw rate remains N/A.
- The same known four scores plus an unresolved fifth denominator: affected total null,
  not64/80; the fifth dimension remains in the shared mask.

## Proposed public report and CLI seam (not implemented)

Prefer a thin backend/evaluation/quality_report.py boundary with immutable QualityReportResult
and build_quality_report(intake, identity_report, snapshot_directory, schedule_context=None,
occupancy_reviews=None, route_reviews=None, coordinate_evidence=None, *, expected_plan=None,
generated_at=...). Validate an explicit offset-aware generated_at in the pure boundary.
Reuse existing public scorers with paired=False and the same reviewed preparation/snapshot.
No caller-supplied arbitrary metric reports, producer payload adaptation, or provider client
construction is needed. No planner graph/client imports or new dependency is proposed.

Validate accepted intake and replay, then run the three component scorers. Verify exact
group/version/run/final-projection keys, no duplicates/missing/foreign records, matching
input/RequirementSpec/result hashes, one expected final projection for each v0-v3 and
compatible shared snapshot/plan hashes. Join by explicit keys, never list position.
This proposal requires a final-only evidence-phase snapshot with paired=False, matching
the existing scorer default. A paired=True snapshot requires an explicit unsupported-scope
diagnostic rather than silently discarding its linkage. Supporting paired evidence as an
aggregate input remains a later extension, not a claim that such a snapshot is corrupt.
Derive grounding from source occurrences/validated identity records after linkage checks.
No group or version is silently deleted. Preserve producer rules and source hashes exactly
as emitted; do not replace a component digest with a differently serialized digest.

The report uses schema_version=rtpeval_quality_report_1, batch_id/batch_revision,
generated_at, rules_profile_id/hash, component schema/rule provenance, source_hashes,
stage_availability, content_hash, groups and diagnostics. Use schema_version consistently with executable
reports; this specializes the generic historical report_schema_version field description.
Each group records its common mask, included count, four selected run IDs and total
availability. Each version retains primary metric/check records, normalized dimensions,
descriptive metrics and auxiliary total. Preserve checks, magnitudes, reasons, basis,
partial-evidence flags and observed-only burden; report complete does not mean quality PASS.

Source provenance includes exact manifest/input/spec/result/provenance/usage hashes from
intake; canonical prepared/replay digests; identity evidence/review/audit/reference hashes;
snapshot manifest/plan digests; preparation/expected-plan hashes; and component rule hashes.
CLI-read identity/context/review/coordinate/expected-plan files retain exact-byte SHA-256
separately from object digests. Temporal basis and underlying precision remain in component
measurements. Rules-profile hash covers formula, ordered dimensions, mask/availability
rules and report profile version; it is not a file hash of this narrative document.

Missing/unavailable provider observations inside a valid snapshot become original UNKNOWN
units. A missing/corrupt/stale snapshot or invalid source/review is a material/replay
diagnostic, not successful aggregation of a reduced cohort. Any component material failure
returns empty groups with its reason; do not export partial four-version totals.
Per-dimension denominator unavailability is different: a valid report retains all groups
and partial checks, with explicit null affected scores/totals.

Proposed quality_report_cli.py accepts manifest, identity report, snapshot directory and
the existing --context, --occupancy-reviews, --route-reviews, --coordinates, --expected-plan
options plus --generated-at. No --paired option or extra metric-file upload is proposed.
CLI may obtain UTC creation time when no timestamp is supplied; an explicit timestamp
supports byte-for-byte reproducibility. Report content/hash calculations exclude generated_at
and content_hash itself, but retain source and rule hashes. Identical frozen inputs,
rules and explicit timestamp yield identical canonical JSON. CLI emits structured JSON,
returns 0 for a completed replay even with FAIL/UNKNOWN/unavailable totals, and 2 for
material/replay correction. Serialize null, never NaN/Infinity; do not mutate source files.

## Optional tracks and later-ticket boundaries

The quality report does not require a resource comparison, human answers or mechanism
analysis. Intake already requires four linked usage envelopes; unavailable collection is
allowed. Preserve usage_hash and usage_available as source-envelope metadata, not proof
of complete resources. Keep resource reporting separate (existing Ticket 02 reporter).
Missing/not-integrated resource/human/mechanism reports have explicit availability and
no quality contribution; do not label an available usage envelope as an available analysis.
Do not add event aggregation, rankings, blinded UI or mechanism audit to this ticket.

Only final v0-v3 projections enter the group total. Optional V3 draft/final_primary data
retain intake availability but receive no paired total/delta here; that belongs to Ticket
10. No controlled Repair, official evidence audit, benchmark case generation, planner
rerun or formal comparison is included. Local fixtures only establish implementation.

## Proposed implementation checks after approval

Implementation would add quality_report.py/quality_report_cli.py and directly related
test_quality_report.py/test_quality_report_cli.py; update only related contracts/package/
project/index/acceptance/archive/tracker records. Existing scorers and V0-V3 entry points
keep their contracts and behavior. Reuse records/preparation utilities; avoid broad refactors.

Acceptance slices:

1. Exact P/F/U and companion arithmetic; all-UNKNOWN, mixed FAIL/UNKNOWN, grounding and
   commitment/obligation units; no conditional-rate substitution or double route penalty.
2. Shared all-N/A exclusion, single-version no-check zero, known-zero versus unresolved
   populations, empty mask and asymmetric total availability without weight redistribution.
3. Full per-request/four-version joins; invalid/foreign/stale preparation/snapshots, duplicate
   keys, source/rule/hash provenance and material failures with no smaller cohort.
4. One existing-fixture frozen evidence snapshot driving all five dimensions, no network/
   source mutation, stable explicit generated_at and exact serialization without nonfinite
   numbers. CLI diagnostics and exit behavior use actual public boundaries.
5. A findings-only V3 source change leaves metric counts/masks/scores unchanged after
   correct relinking/replay of source-hashed artifacts. Source/report hashes may change;
   stale identity/snapshot reuse must still fail. Do not demand whole JSON equality when
   provenance legitimately changes, or weaken evidence hashes to satisfy this invariant.
6. Optional-track absence cannot change quality scores; descriptive density/repetition,
   resource/human outputs and V3 internal findings cannot add score penalties.

Use TDD within the eventual approved implementation, relevant evaluation regressions,
backend Ruff/compilation and one final full offline backend gate, followed by Standards/
Spec review and necessary corrections. No live/database/native supplement or commit is
part of that proposal unless separately authorized. It is not formal benchmark execution.

## Actual preflight validation and closeout

Existing identity, requirement/schedule, opening, route and opening/route CLI tests passed:
**275 passed in 29.02s**, using no:cacheprovider and repository-local
.scratch/ticket08-preflight-check. TRIPWORLD_TEST_DATABASE=0; the selected modules contain
no opt-in database/native test. No Ticket 08 test or total/CLI implementation exists yet.
No failure/correction/retest cycle occurred in this preflight regression; initial run passed.
The earlier 2234/10-skipped full gate is Ticket 07 history, not rerun here.

The implementation proposal remains subject to explicit scope approval. A ready Issue,
completed predecessor, this inspection or the earlier Git approval does not authorize
implementation, commits/push or another ticket.

Final static checks passed for English/whitespace and **167 existing local Markdown
targets across six current documents**. Diff checks passed; backend/scripts/config have
zero content diff, the index is empty and HEAD remains 30960c67 on feature/evaluation.
The generated pytest root was removed after process completion. Issue #20 and parent
#12 were updated/read back with matching preflight bodies; both remain open, without
assignment/label/implementation-state changes. Current six documentation files remain
local/uncommitted; ignored research records are not project authority or staged assets.
