# Ticket 10: independent V3 before/after specification preflight

Date: 2026-10-02, Australia/Sydney.
Status: Specification preflight complete. Q1-Q3 and final shared understanding
Accepted by the user; source-driven correspondence revision approved on 2026-10-02.
Implementation is not authorized; not Implemented or Frozen.
Starting revision: `b3ceb0560eedb03767574c4f9c84efd73f77b883` on `feature/evaluation`.
The index/worktree was clean before this preflight. No implementation is claimed.
Revision starting point: `a0675d7775c699b8b54d5aa62def2cd3a50b713c`, clean worktree/index.

## Authorization and authority

The user approved Ticket 10 specification preflight in this conversation. It covers
current Issue/contracts/interface inspection and an English preflight document with
an implementation proposal, acceptance checks and unresolved decisions. It does not
authorize implementation, live tests, GitHub tracker mutation, formal case construction
or execution, push, branch changes, version progression or freeze.
The later approval authorizes revision of correspondence specifications and related
documentation/local commits only; it does not authorize implementing the reader or
changing planner ID allocation, transport binding or Repair behavior.

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
| project / records.source | Each occurrence retains declared date, raw activity values, original activity_id, exact artifact hash and JSON pointer. Derived source IDs also include projection context. | Source hashes/pointers locate observations; validated producer activity IDs and edit provenance can establish lineage without establishing venue correctness. |
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
These observations distinguish source lineage from venue continuity and quality.
Validated producer activity IDs and adopted edits can establish source correspondence;
an equal ID does not prove the same venue or a repaired conflict. Array positions,
internal target IDs and target disappearance do not supply an independent verdict.

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

The revision also inspected [Repair service](../../backend/app/versions/v3/repair_service.py),
[component adoption](../../backend/app/versions/v3/repair_components.py) and
[itinerary schema](../../backend/app/schemas/itinerary.py). Activity IDs are unique within
an itinerary. retime/move/replace preserve IDs; add allocates round/component-prefixed
IDs, delete removes them, and consume_windows records previous/root/fragment IDs.
Each round records input_itinerary and adopted. A round can contain rejected components;
accepted components can later be rolled_back. The cumulative summary's top-level patch
is not the entire edit history. Final wiring selects the adopted schedule, normalizes
activity ordering and place_name from its ledger, then presents transfers anew before
copying final_primary. Name normalization and transport refresh require explicit stage
reconciliation, not claims of a new venue or unexplained source changes.

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

## Accepted source-driven correspondence revision

The original Q2 used simple content/venue matching and manual review of complex edits.
The user challenged this because the actual program already links activities, transfers
and edits, then explicitly approved revising the specification. The current policy
below supersedes the blanket complex-edit-review and prohibition on reading edit lineage.
It preserves Q1's mask, Q3's valid aggregate availability and independent quality rules.

Separate three questions: which source activity was edited, whether its venue/role
remains the same, and whether it is now compliant. Source provenance may answer the
first while independent identity/checks answer the others. A known edit relation can
coexist with identity UNKNOWN. No planner resolved/PASS/acceptance judgment establishes
independent venue identity, requirement fulfillment or quality.

### First: validate producer IDs and actual adopted edit provenance

Maintain source occurrences for all roles, independent journey commitments and candidate
legs. Read the full selected result artifact as an optional correspondence source, with
its exact byte hash and group/run/input association validated against accepted intake.
Existing intake projections do not retain rounds/components/window lineage; the future
reader must explicitly extract them rather than pretend those fields are already available.
Do not alter intake's established output/hashes or require new planner instrumentation.

Use unique activity IDs within the same selected V3 run together with checked edit
provenance and stage snapshots. Never join different runs, raw array positions, repeated
venue names or arbitrary reused IDs. Validate the observable sequence:

1. Bind Repair original/first round input to draft; check ordered round input/adopted
   transitions, result original/final and cumulative final. Rejected/skipped attempts
   retain their input as adopted; accepted statuses alone cannot certify that adoption.
2. Derive edits from actual adopted state differences, corroborated by effective patches,
   component proposals and window adjustments where available. Exclude rejected, pending
   and rolled-back proposals. A partially accepted round does not adopt every patch edit.
   Do not treat the cumulative top-level parsed/effective_patch as a complete history.
3. Require unique IDs, valid source membership, collision-free additions, plausible
   supported operation fields and consistent before/after relations. retime/move retain
   source lineage; replace retains the edited slot but records identity change separately;
   delete removes an occurrence; add creates one. Content need not remain equal.
4. Compose actually adopted transitions across rounds. A replacement followed by another
   replacement remains traceable; retain intermediate edit provenance without scoring
   rounds or multiplying final visit-loss counts. Compare draft and final populations.
5. Reconcile the adopted result with final_primary by activity ID, accounting for the
   inspected producer's sorting, place-name normalization and transfer/diagnostic refresh.
   Check date, role, times, source-place claims and other activity changes rather than
   accepting arbitrary differences. A supported normalization is recorded with its
   source basis; unexplained changes remain provenance diagnostics.

Record the applied provenance basis, raw result/source pointers and validation reasons.
Within a validated sequence, repeated visits, cross-day movement and explicit replacements
are automatically traceable; complexity alone does not require human review. A replace
operation and independently confirmed venue change are separate fields: replacing with
the same canonical venue is not automatically a lost visit. Same-ID replacement of
Museum A with Gallery B identifies an edit relation, not repaired Museum A opening hours.

For free-time splits, compose previous_fragment_id/root_activity_id/fragment_ids and
adopted window adjustments, including fragment deletion and actual occupied intervals.
Check parent/child existence, dates, intervals and stage membership. Preserve a source
one-to-many relation without inventing extra visits. No unsupported merge operation is
assumed; an unrecorded many-to-many transformation uses fallback/review.

### Then: content fallback and evidence-backed review

If provenance is absent, incomplete or locally inconsistent, retain a diagnostic and
use only the still-supported relations. Unique unchanged content or unique independently
confirmed venue matching remains a fallback, with its weaker basis labelled. Preserve
identity/role UNKNOWN and explicit date/time changes. Do not select by nearest time,
favorable verdict, array order or greedy leftover matching. A plausible unmatched
counterpart stays unresolved rather than automatically removed/added.

Review requests contain source refs, known lineage, candidate relations and specific
missing/contradictory evidence. A supplied review may establish unchanged/modified/moved/
replaced/split/merged/complex/added/removed relations with supporting evidence and rationale.
It cannot silently override contradictory validated provenance: resolve the contradiction
against source material and record the correction. No all-pairs solver, LLM matcher or
new semantic classifier is proposed.

The review envelope remains proposed rtpeval_v3_correspondence_1 with batch/revision,
group/run/result hash, stage/source refs, relation, reviewer/time/rationale and optional
supporting refs. Validate membership, disjoint occurrence participation, cardinality,
hash/revision linkage and review metadata. Source-driven relations retain distinct
operation/identity-change/quality fields; complex groups never invent one-to-one edges.

Missing optional lineage is not pair_unavailable and does not disable valid aggregate
scores. Incomplete/contradictory embedded lineage disables affected automatic lineage
claims with explicit diagnostics and fallback/review; it does not create itinerary FAIL.
Foreign/stale supplied result bytes or review material remain material-correction errors.
No new final-only intake, Ticket 08 or planner failure gate is introduced.

### Transport connections and changes

Within one stage, transfers bind by from_activity_id/to_activity_id. Across stages,
first establish endpoint activity lineage and then inspect the directed adjacency.
If a1 -> a2 becomes a1 -> a3 -> a2 after adding a3, deterministically record the removed
direct leg and added legs. Existing endpoint links explain the structural change without
requiring a reviewer or inventing a one-leg verdict from summed route results.

A persisted endpoint pair with a replaced venue still has connection lineage but a
changed route context. Changed venue/day/mode/departure requires applicable independent
snapshot records and new stage checks. Dangling/nonadjacent transfers retain existing
diagnostics; the evaluator does not retarget them or repair the submitted itinerary.

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
  leg into new legs; record a source-derived structural edit without summing leg verdicts
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

## Accepted partial availability: Q3 with source-driven preparation

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

The first clarified approach used automatic content matching followed by manual inspection
of source/edit records. The later approved revision moves validated ID/adopted-edit/window
reading into automatic preparation, ahead of content fallback and the remaining review
queue. This restores recorded connections instead of asking reviewers to reconstruct
ordinary recorded edits. Add no planner instrumentation or live acquisition. Full edit
metadata is not currently an intake projection; the proposed source reader does not import
internal quality verdicts or claim to implement the later mechanism reporter.

Only after available evidence and review still fail to establish a unique relation
does affected continuity remain unresolved. No method can recover an unrecorded unique
history from indistinguishable before/after occurrences alone. The user accepted local
unresolved tracking with preserved valid aggregate deltas after this review step.

## Proposed implementation seam and bounded acceptance

After specification confirmation and separate implementation approval, prefer a thin
`backend/evaluation/v3_pair_report.py` and matching CLI over the existing public scorers.
Proposed boundary: build_v3_pair_report(intake, identity_report, snapshot_directory,
schedule_context=None, occupancy_reviews=None, route_reviews=None,
coordinate_evidence=None, edit_provenance=None, correspondence_reviews=None, *, expected_plan=None,
generated_at=...). Return immutable rtpeval_v3_pair_report_1 data with schema/rule/source
hashes, deterministic content hash, per-group pair availability, stage metrics/mask,
exact deltas, independent correspondence and continuity records/diagnostics.

Add a narrowly scoped offline edit-provenance preparation reader if needed, such as
`backend/evaluation/v3_correspondence.py`. It consumes exact-linked full result material,
extracts only adopted source transformations and produces a reproducible proposed
rtpeval_v3_edit_provenance_1 envelope. Keep source file-byte hashes and projection IDs
separate from canonical preparation digests. Its pure interface validates supplied
observations/links and returns provenance records/diagnostics, not quality judgments.
CLI obtains full selected result bytes from manifest artifact refs through the existing
safe artifact-reading rules; do not discover files by name or use arbitrary caller-authored
edit summaries. Report replay verifies envelope/source/rule linkage and consistency with
the available stage observations. An internally generated envelope is still evidence
preparation, not trusted truth: recompute or validate its observable adopted-chain claims
against linked original material before using them. Existing intake schema/output stays unchanged.

Validate row membership and hashes across all expected paired scorer outputs; then
select V3 draft/final_primary explicitly. Avoid caller-authored metric summaries or
rewriting prepared intake as synthetic runs. Missing-all-pairs should produce explicit
unavailable group records without demanding fictional paired evidence. Mixed batches
retain unavailable pairs while replaying valid pairs under the same source boundary.

Share a small internal score-arithmetic adapter only if needed, with equivalent
Ticket 08 behavior covered by regression tests. Preserve its final-only entry point,
rules profile, group mask, public wire and unsupported-paired diagnostic. No new planner
imports, third-party dependencies, provider client, database or frontend is proposed.
CLI inputs reuse current preparation JSON plus optional prepared edit provenance and
correspondence review; stdout is deterministic JSON with optional explicit generated_at
and exit/status conventions consistent with existing offline report CLIs. Exact review file byte hashes remain
distinct from canonical preparation digests.

Future TDD acceptance scenarios, not fixtures created or tests run in this preflight:

1. Identical valid schedules: zero defined changes despite distinct projection refs;
   N/A/unavailable rates stay null. No-repair/skipped/rejected pairs remain included.
2. Missing/invalid draft or final_primary: unavailable row, no /itinerary fallback,
   no cohort deletion or fabricated zero.
3. Valid repeated visits with distinct retained IDs match without manual review; retime,
   cross-day move and same-ID replacement are traced through adopted edits. Sorting and
   supported place-name/transfer normalization do not break lineage or prove venue identity.
4. Multi-round edits, partially accepted components, rejected/pending/rolled-back proposals,
   allocated-ID collisions and inconsistent adopted chains. Only observed adopted changes
   enter final correspondence; a summary patch cannot replace full provenance.
5. Source-linked free-time split fragments and multi-round root composition; explicit
   deletion/addition, replacement with the same or different canonical venue, missing
   lineage content fallback, unresolved identity and manual contradiction review. IDs or
   operation labels never resolve independent identity/quality UNKNOWN.
6. Conflict removed by deleting a visit versus conflict repaired while retaining it;
   FAIL-to-UNKNOWN, PASS-to-UNKNOWN, new overlap/protection/opening/route conflicts and
   requirement regressions after a replacement or movement.
7. Pair-union mask, true no-check contribution, unresolved denominators, empty masks,
   exact rational deltas and unchanged four-final scores/masks/wire.
8. Route endpoint insertion/direction/mode/day/departure changes, automatic old/new leg
   topology, dangling connections and no old-query reuse;
   partial decisive FAIL, no-route without duration and observed-subtotal coverage.
9. Stale/foreign/duplicate supplied provenance or reviews, corrupted snapshots, missing scorer
   rows and mismatched source/rule hashes fail atomically. Incomplete/contradictory embedded
   edit metadata instead disables its automatic lineage path with fallback diagnostics.
   Properly relinked internal-findings-only changes
   preserve independent numeric/correspondence results while provenance hashes change.
10. Public preparation/CLI replay determinism, read-only inputs, no network calls, time metadata
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
  human review for complex changes. Superseded by the later approved source-driven revision;
  a raw activity ID still does not prove venue continuity or compliance.
- Q3: Accepted after further clarification: supplement review first; residual uncertainty
  affects local continuity, while valid independent aggregate deltas remain available.
  Validated edit-source reading now precedes the remaining review queue.
- Revision: user challenged whether existing activity/transport connections could solve
  matching directly; inspection confirmed IDs, adopted round/component snapshots and split
  records. User approved revising specifications to prioritize validated edit provenance,
  separate it from quality truth and use content/review only for residual material gaps.

Revision validation: documentation checks passed for six files and 209 existing local-link
targets, with no CJK repository prose and no superseded active correspondence prohibition.
Diff/content inspection covers only the four intended tracked documentation files; archive
and its index remain ignored. No implementation or lineage replay test was run. The original
a0675d7 documentation commit remains intact; this revision uses a separate docs commit.

The user subsequently confirmed the complete specification, explicitly without authorizing
implementation, then approved the source-driven documentation revision only. Specification
preflight is complete; the proposed preparation/report/CLI/TDD/review
scope remains the next separately approved task. No implementation has started.
