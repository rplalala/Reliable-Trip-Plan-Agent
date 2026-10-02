# Ticket 10: independent V3 before/after specification preflight

Date: 2026-10-02, Australia/Sydney.
Status: Specification preflight complete. Q1-Q3 and final shared understanding
Accepted by the user. Implementation is not authorized; not Implemented or Frozen.
Starting revision: `b3ceb0560eedb03767574c4f9c84efd73f77b883` on `feature/evaluation`.
The index/worktree was clean before this preflight. No implementation is claimed.

## Authorization and authority

The user approved Ticket 10 specification preflight in this conversation. It covers
current Issue/contracts/interface inspection and an English preflight document with
an implementation proposal, acceptance checks and unresolved decisions. It does not
authorize implementation, live tests, GitHub tracker mutation, formal case construction
or execution, push, branch changes, version progression or freeze.

[PROJECT](../../PROJECT.md) and [AGENTS](../../AGENTS.md) own current scope and workflow.
[Issue #22](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22) owns live
Ticket 10 state. On 2026-10-02 it was open, labelled needs-info/rtpeval, with no comments.
[Ticket 08 / #20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20) was
closed/completed. The statement in #22 that Ticket 08 is unfinished is an obsolete
migration snapshot, not a current dependency blocker. No Issue was edited.

The configured gh CLI could not authenticate (HTTP 401); a GitHub connector read
retrieved #22, its empty comment list and #20 successfully. No credential changes
were attempted. Initial gh flags were incompatible; the connector supplied the
required body/state/comments without relying on the retained local ticket snapshot.

Relevant contracts are [metrics](metrics-contract.md), [score profile](score-profile.md),
[artifact](artifact-contract.md), [intake projection](intake-projection-contract.md),
[snapshot](snapshot-contract.md) and [evaluator design](../../docs/evaluator_design.md).
Historical OPEN statements yield to their later accepted specializations. Ticket 08
acceptance is retained, not rerun or represented as validation of Ticket 10.

## Observed implementation facts

| Seam | Current behavior | Ticket 10 implication |
| --- | --- | --- |
| load_batch in intake.py | Four selected final results remain mandatory. V3 optional draft/final_primary projection failures retain diagnostics and set the affected projection to null. paired_available requires both. | Keep every selected group; missing optional pairs disable paired outputs, not final quality or cohort membership. |
| project / records.source | Each occurrence retains declared date, raw activity values, original activity_id, exact artifact hash and JSON pointer. Derived source IDs also include projection context. | IDs locate evidence; they do not establish cross-stage continuity. |
| identity_references / identity_ready | Available optional V3 visits have separate references and replay validation. Canonical identity comes from independent resolution/review. | Use the current replay, including UNKNOWN identities; do not substitute planner source_place_id. |
| snapshot plans | paired=True includes four finals plus available draft/final_primary and requirement subjects. Identical request descriptors share evidence while occurrences remain separate. | Require one compatible frozen paired evidence snapshot, with distinct route query contexts. No acquisition is part of this preflight. |
| requirement/schedule, opening and route scorers | paired=True emits rows for four finals and available V3 optional stages, keyed by group/version/run/projection. | Reuse these public scorers; verify complete expected row and hash linkage before selecting paired rows. |
| build_quality_report | Requires paired=False and exactly four final rows; rejects a paired snapshot as unsupported_snapshot_scope. | Do not call it unchanged for paired totals or silently broaden its current scope. |
| score arithmetic | Exact P/(P+F+U), equal weights, true no-check zero contribution inside a common mask, unresolved denominator/null total. | Reuse these arithmetic rules with an explicitly separate paired mask. |
| occupancy and route rows | Independent commitment sources, obligation IDs, conflict pairs/spans, canonical endpoints and route contexts are available. IDs depend on source projections. | Derive continuity from independent occurrence correspondence; never equate source-derived check IDs across stages. |

Source entry points: [intake](../../backend/evaluation/intake.py),
[projection](../../backend/evaluation/projection.py), [records](../../backend/evaluation/records.py),
[identity](../../backend/evaluation/identity.py), [snapshot](../../backend/evaluation/snapshot.py),
[quality report](../../backend/evaluation/quality_report.py),
[requirement/schedule](../../backend/evaluation/requirement_schedule.py),
[occupancy](../../backend/evaluation/occupancy.py), [opening](../../backend/evaluation/opening.py)
and [routes](../../backend/evaluation/routes.py).

The V3 producer retains activity_id when replacing a POI, while output acceptance can
reorder activities. Runtime free-time lineage can describe split fragments, but intake
does not expose that lineage as independent evaluation preparation. Internal Repair
outcomes can label old-conflict removal resolved; this is not an independent verdict.
These observations explain why equal activity IDs, array positions, internal target
IDs and target disappearance are insufficient evidence of correspondence or repair.

The independent interface audit located producer details in
[repair acceptance](../../backend/app/versions/v3/repair_acceptance.py),
[repair obligations](../../backend/app/versions/v3/repair_obligations.py),
[repair schedule](../../backend/app/versions/v3/repair_schedule.py),
[V3 wiring](../../backend/app/versions/v3/wiring.py) and
[output acceptance](../../backend/app/policies/itinerary_output.py).
Requirement check_id uses projection context plus obligation_id but not the projection
prefix, so it can be equal across this run's optional stages. Always index by
group/version/run/projection plus the semantic obligation; raw check_id alone is unsafe.
No extra Repair metadata requirement should disable an otherwise valid pair.

## Settled source and scoring boundaries

Compare only the selected run's `/v3/draft` with `/v3/final_primary`, labelled V3 draft
and V3 final primary. `/itinerary` remains the selected four-version final projection;
it is not a fallback for a missing optional after stage. Nearby is outside primary
visit scoring. No-repair, skipped or rejected Repair remains eligible when both
optional stages are valid. No selection on internally accepted improvements.

Use the same original Input, reviewed RequirementSpec/revision, identity policy,
independent preparation and frozen paired snapshot for both stages. The same snapshot
does not imply the same route response: changed endpoints, date, departure, mode,
coordinates or routing options require correctly linked distinct query records.
Missing context/evidence stays UNKNOWN; old route evidence is not repurposed.

Q1 Accepted by the user: use the draft/final_primary pair's common dimension mask.
In the fixed order requirements, grounding, non_overlap, opening, routes, exclude a
dimension only if both stages prove denominator zero. A null/unresolved denominator
retains the dimension. Included true no-check has null raw rates and a zero accounting
contribution; included unresolved denominator has null contribution and affected total.
No weight redistribution or fabricated UNKNOWN units. An empty mask has null totals.

This paired mask and its two totals are separately labelled diagnostics; they do not
change Ticket 08's four-final mask, totals or hashes. Totals from different masks must
not be presented as directly interchangeable. Use exact rational contributions and
unrounded means; export score changes in percentage points and exact fractions.
Signed deltas are after minus before. Defined identical outcomes give zero; null raw
rates, empty masks and unresolved denominators never acquire zero deltas by imputation.

## Accepted correspondence policy: Q2

Correspondence is an independent relation between source occurrences, not a claim that
a visit is correct. Maintain an inventory for all activity roles, plus independently
grouped journey commitments and same-day candidate legs. Preserve source refs, role,
declared date, normalized interval availability, canonical identity and raw claims.

Recommended automatic rules are deliberately narrow:

1. A unique unchanged content match can establish occurrence continuity, ignoring
   projection pointers and activity IDs. Preserve identity/role UNKNOWN even when
   source content is unchanged; source continuity cannot resolve semantic uncertainty.
2. A confirmed primary venue occurring exactly once in each stage may correspond by
   independently adopted canonical identity. Record changed date/time/role separately;
   date movement does not erase date-specific obligations or evidence applicability.
3. Changed repeated venues, competing matches, identity/role ambiguity, different-venue
   replacement and one-to-many/many-to-one changes require independent review. Do not
   resolve these by array position, nearest time, favorable verdict or greedy leftover
   matching. Unchanged uniquely identifiable repeated occurrences can still match.
4. A reviewed relation may be unchanged, modified, moved, replaced, split, merged,
   complex, added, removed or unresolved. Each source occurrence belongs to at most one
   disjoint relation; a complex relation lists all before/after refs without inventing
   one-to-one edges. Review cannot change independent identity or metric verdicts.

Proposed review envelope: schema_version=rtpeval_v3_correspondence_1, batch_id/revision,
preparation revision, records. Each record binds group_id/run_id/result_sha256, before
and after projection identifiers, source refs, relation, reviewer_ref, reviewed_at and
rationale. Validate exact projection/source membership, duplicate participation,
allowed cardinality, current result/preparation linkage and nonempty review metadata.
Foreign, stale or contradictory review material is material correction, not a smaller
cohort. Missing optional review leaves genuine ambiguity unresolved.

Clarification requested by the user on 2026-10-02: the initial Q2 wording was unclear.
Concrete proposal: a single Museum A in each stage, independently confirmed as the same
venue, moving from 10:00 to 14:00 can match automatically. Two Museum A occurrences in
each stage with changed times cannot be matched by list order. Activity a1 changing
from Museum A to Gallery B is replacement, not the same visit merely retimed.
After this clarification, the user accepted simple automatic correspondence plus
independent human review for complex changes. This concerns correspondence, not a
new quality verdict or authority to trust internal Repair resolution labels.

Unmatched sources are not automatically labelled removed or added: a plausible
unresolved counterpart or replacement remains a review candidate. Review requests
include affected source refs, candidate relations and ambiguity reasons so a reviewer
can inspect actual occurrences rather than infer lineage from scores.

Keep original activity IDs and runtime metadata only as provenance if supplied; do
not derive independent correspondence from internal target/patch/lineage decisions.
No all-pairs assignment solver, LLM matcher or semantic classifier is proposed.

## Independent obligation and conflict continuity

The following rules specialize existing independence and removal boundaries; they
do not create a Controlled Repair success rate or use internal target sets.

- Match reviewed obligations by obligation_id within the same exact RequirementSpec.
  One parent remains one score unit with its count/date/time components. A changed
  activity set cannot remove that obligation. Report PASS/FAIL/UNKNOWN transitions,
  supporting occurrences and component changes; requirement regressions stay visible.
- Track visit-specific opening/grounding checks using independently established visit
  correspondence and before/after facts. A deleted visit is removed, not a repaired
  occurrence. A venue replacement reports old removal and new independent results;
  a newly compliant venue does not verify the old venue's failed fact.
- Match an overlap conflict by its independently continued participants, not by raw
  commitment_id/check_id or exact conflict clock span. Protection conflicts also keep
  the original obligation_id/scope. If either participant disappears, report removal
  context rather than a retained commitment made conflict-free. Unknown relations stay
  unresolved. New participants/conflicts retain their own after-stage evidence.
  Only a confirmed before non-conflict for continued participants, or independently
  established new participants, supports introduced-conflict attribution. An ambiguous
  relation or UNKNOWN before outcome yields unresolved attribution/UNKNOWN-to-FAIL,
  not a claim that a previously absent conflict was introduced.
- Candidate leg continuity requires independently corresponded directed endpoint
  occurrences. Changed day/mode/departure/adjacency is explicit context change, not
  identical evidence applicability. An inserted middle visit changes the old direct
  leg into new legs; record a reviewed structural edit without summing leg verdicts
  into a fictional one-leg resolution. Many-to-many sets retain constituent outcomes.
- A retained compatible unit's independently confirmed FAIL-to-PASS transition may
  be labelled resolved for that check, with changed time/context exposed. FAIL-to-
  UNKNOWN is not verified resolution; PASS-to-UNKNOWN is lost verification. Deletion,
  replacement or unresolved mapping is not a substitute for this transition.

Many-to-many relations do not generate per-occurrence transition rates, new weighted
checks or success denominators. Record constituent P/F/U/N/A and losses/additions.
Independent obligation transitions remain meaningful across these structural edits.
Partial observed improvement requires the same independently continued check to remain
FAIL with a strictly reduced, comparable exact violation magnitude under the same
applicable rule. Unknown/lower-bound magnitudes do not support that comparison. Retain
raw states and measurements when no such metric exists; no generic partial-success
percentage or conversion between conflict types is proposed.

## Accepted review-first partial availability: Q3

Recommendation: correspondence uncertainty disables affected continuity statements,
not otherwise valid aggregate stage values/deltas. Separate pair source availability,
metric/denominator availability, evidence coverage and correspondence coverage.

Every selected group receives a paired record. An absent/invalid optional stage yields
pair_unavailable with original intake diagnostics and null pair deltas. Present stages
may retain standalone observations; no stage is synthesized. An entire source/replay/
snapshot corruption yields material/replay diagnostics without a silently reduced
cohort. A valid pair can have unresolved identity, partial evidence or an unavailable
full-scope dimension while retaining its other defined observations.

For valid stage metrics, export raw P/F/U/N/A counts, known-unit counts, each established
denominator and signed denominator change; null denominator changes remain null.
Keep before/after structural and evidence-adjudicable counts/rates, basis/reason changes,
observed-subtotal population counts and lower-bound/full-scope status. Do not describe
an observed travel subtotal or outside-opening lower bound as an exact total.

Report primary-visit counts, unique canonical venues with unresolved identity counts,
requested-day coverage and date-specific density/repetition. Distinguish known removed
and added visits from unresolved correspondence; a visit-count difference alone cannot
identify which visit was lost. Expose requirement regressions, retained/new confirmed
conflicts, lost verification and missing after evidence alongside any numeric gain.

Whole-plan metric deltas answer what changed in the two observed stage populations.
They do not establish why it changed, success for a matched target, absence of all
regression or a causal Repair effect. No overall Repair success classification is proposed.

Clarification requested by the user on 2026-10-02: the initial Q3 wording was unclear.
Illustrative arithmetic, not an executed result: four independently scored opening
checks change from 2 PASS/2 FAIL to 3 PASS/1 FAIL, giving scores 50 to 75. Repeated-visit
correspondence may remain unresolved even when both denominators and stage results
are established. The recommendation retains the aggregate +25 percentage-point delta
while withholding an assertion about which particular visit was repaired. This does
not permit numeric deltas for unresolved denominators or corrupt material. The user
then asked why correspondence could remain unknown and whether it could be confirmed.

The clarified approach, subsequently Accepted, attempts automatic correspondence,
then emits a source-linked review queue for ambiguity. A reviewer may inspect full
original outputs and available edit records as provenance clues, record an independently
checked relation with supporting source refs/rationale, and replay the report. Add no
planner instrumentation or live acquisition merely to resolve correspondence. Full
edit metadata is not an intake projection; manual inspection is distinct from trusting
an internal target verdict or replacing independent quality scoring.

Only after available evidence and review still fail to establish a unique relation
does affected continuity remain unresolved. No method can recover an unrecorded unique
history from indistinguishable before/after occurrences alone. The user accepted local
unresolved tracking with preserved valid aggregate deltas after this review step.

## Proposed implementation seam and bounded acceptance

After specification confirmation and separate implementation approval, prefer a thin
`backend/evaluation/v3_pair_report.py` and matching CLI over the existing public scorers.
Proposed boundary: build_v3_pair_report(intake, identity_report, snapshot_directory,
schedule_context=None, occupancy_reviews=None, route_reviews=None,
coordinate_evidence=None, correspondence_reviews=None, *, expected_plan=None,
generated_at=...). Return immutable rtpeval_v3_pair_report_1 data with schema/rule/source
hashes, deterministic content hash, per-group pair availability, stage metrics/mask,
exact deltas, independent correspondence and continuity records/diagnostics.

Validate row membership and hashes across all expected paired scorer outputs; then
select V3 draft/final_primary explicitly. Avoid caller-authored metric summaries or
rewriting prepared intake as synthetic runs. Missing-all-pairs should produce explicit
unavailable group records without demanding fictional paired evidence. Mixed batches
retain unavailable pairs while replaying valid pairs under the same source boundary.

Share a small internal score-arithmetic adapter only if needed, with equivalent
Ticket 08 behavior covered by regression tests. Preserve its final-only entry point,
rules profile, group mask, public wire and unsupported-paired diagnostic. No new planner
imports, third-party dependencies, provider client, database or frontend is proposed.
CLI inputs reuse current preparation JSON plus optional correspondence review; stdout
is deterministic JSON with optional explicit generated_at and exit/status conventions
consistent with existing offline report CLIs. Exact review file byte hashes remain
distinct from canonical preparation digests.

Future TDD acceptance scenarios, not fixtures created or tests run in this preflight:

1. Identical valid schedules: zero defined changes despite distinct projection refs;
   N/A/unavailable rates stay null. No-repair/skipped/rejected pairs remain included.
2. Missing/invalid draft or final_primary: unavailable row, no /itinerary fallback,
   no cohort deletion or fabricated zero.
3. Same activity_id with changed canonical venue; different IDs/pointers for an unchanged
   visit; sorted arrays; cross-day movement with preserved date obligations.
4. Repeated-venue ambiguity, unresolved identity/role and manual review replay; reviewed
   replacement, split/merge, added/removed visits; source inventory partition validation.
5. Conflict removed by deleting a visit versus conflict repaired while retaining it;
   FAIL-to-UNKNOWN, PASS-to-UNKNOWN, new overlap/protection/opening/route conflicts and
   requirement regressions after a replacement or movement.
6. Pair-union mask, true no-check contribution, unresolved denominators, empty masks,
   exact rational deltas and unchanged four-final scores/masks/wire.
7. Route endpoint insertion/direction/mode/day/departure changes, no old-query reuse;
   partial decisive FAIL, no-route without duration and observed-subtotal coverage.
8. Stale/foreign/duplicate reviews, corrupted snapshots, missing scorer rows and mismatched
   source/rule hashes fail atomically. Properly relinked internal-findings-only changes
   preserve independent numeric/correspondence results while provenance hashes change.
9. Public CLI replay determinism, read-only inputs, no network calls, time metadata
   excluded from content hash, missing optional review distinct from malformed review.

Relevant checks after implementation approval: targeted TDD at report/review/CLI seams,
current evaluation scorer and quality-report regressions, backend lint, and the full
relevant offline backend gate required by the implementation workflow. Commit implementation
and direct tests before independent Standards/Spec review; preserve separate fix commits.
Those are future checks, not authority to start them now. V0-V3 behavior/entry points,
formal Controlled Repair and mechanism work remain outside this task.

## Preflight validation and decision history

Observed: read-only Issue/contracts/source inspection and one independent interface-audit
subagent. No implementation tests, provider/model/database calls, formal cases or benchmark
results were produced. The initial documentation check passed for five documents and
193 existing local-link targets, with no CJK repository prose. Final content/diff/link
checks cover the completed decision record; no historical test counts are reused as new
Ticket 10 results. Local closeout groups preflight/current-status/index/glossary documentation
in one docs commit; the ignored research archive is excluded from staging.

- Q1: Accepted by user on 2026-10-02: two-stage common mask, separately labelled.
- Q2: Accepted after concrete examples: simple automatic correspondence plus independent
  human review for complex changes; a raw activity ID does not prove venue continuity.
- Q3: Accepted after further clarification: supplement review first; residual uncertainty
  affects local continuity, while valid independent aggregate deltas remain available.

The user subsequently confirmed the complete specification, explicitly without authorizing
implementation. Specification preflight is complete; the proposed report/CLI/TDD/review
scope remains the next separately approved task. No implementation has started.
