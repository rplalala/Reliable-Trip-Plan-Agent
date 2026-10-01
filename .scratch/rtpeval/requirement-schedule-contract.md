# Ticket 05 requirement and schedule contract

Current follow-up, 2026-10-02: offline implementation and acceptance are complete.
The user subsequently authorized documentation/archive/Issue closeout and requested a
local commit, then approved one coherent feature grouping. [Ticket 05 #17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17)
is closed as completed; code and updated documents remain local and unpublished.
See [Ticket 05 acceptance](ticket-05-acceptance.md) for implementation, review corrections,
validation and closeout evidence. No live service or push is authorized. The following
2026-10-01 specification checkpoints retain their original authorization and history.

Date: 2026-10-01. Code checkpoint: `473600254023f7d41648eed02215b6ab84e4ff03`.
Status: Specification-ready after the user accepted Q1 and Q2 on 2026-10-01.
Implementation scope is proposed for separate approval. No scoring implementation
or implementation tests have been performed. Existing documentation changes remain
uncommitted.

## Authority and inputs

This contract specializes [RequirementSpec](requirement-spec-contract.md),
[metrics](metrics-contract.md), [scores](score-profile.md),
[projection](intake-projection-contract.md) and [time](evidence-time-contract.md)
for Ticket 05. It does not redesign the evaluator or change planner behavior.
Original Input, reviewed RequirementSpec, accepted Ticket 01 projections and
source-linked Ticket 03 identity decisions are the inputs. Frozen independent time
context and occupancy review may be supplied separately. Planner requirement
interpretation, validation, candidate membership and Repair findings are not verdict
inputs. Nearby and ignored transport sources never become scheduled main visits.

The public boundary will consume immutable preparation records and return a
source-linked offline metric report. It will not invoke a planner, provider, model
or database. Final projections are evaluated independently; optional V3 projections
can use the same metric function, but pre/post deltas remain Ticket 10 work.

## Current code facts and implementation seams

- `backend/evaluation/intake.py::_requirements` checks linkage, review, identifiers,
  array shape and source references. It does not validate executable counts,
  distinct dates, time operators or protection scopes. Its `protected_intervals`
  collection contains original obligations, not normalized blockers.
- `backend/evaluation/projection.py` preserves source times and declares uncertain
  roles. Invalid/missing times remain content diagnostics. Its journey
  `occupancy=[]` can mean incomplete/conflicting claims; it cannot certify absence.
- Version-selected transport is already implemented: V0 activities; V1-V3 transfers.
  Same-source duplication/alternatives and unbound claims remain visible.
- `backend/evaluation/identity.py::identity_references` currently includes resolved
  REQUIRED/EXCLUDED subjects only. The accepted fixed-time subjects
  need the same independent subject linkage and high-impact review protection.
- Source linkage is exact artifact hash plus pointer and batch/group/run context.
  Existing source references name top-level Input fields and use Unicode-code-point
  quote offsets. This slice does not introduce nested source-path syntax.

Add scorer-specific semantic validation after accepted intake rather than silently
changing Ticket 01's tolerant artifact reader. A malformed executable payload or
mechanically contradictory reviewed specification produces `needs_material_correction`
for the submitted batch; no partial cohort or quality FAIL is manufactured.
Content uncertainty produces check UNKNOWN or an explicit metric-availability reason.

## Obligation wire and checks

Keep the existing `rtpeval_requirements_1` envelope, identifiers, review and
source references. Executable fields below live directly on each obligation;
do not infer them from result prose. Unresolved/unsupported records retain reason
and source, without invented executable values. A resolved record with an unknown
operator is returned for specification correction instead of silently executing it.

| Kind | Executable fields |
| --- | --- |
| `required_visit` | `subject_ref`; `count={mode:minimum|exact,value:positive integer}`; optional `distinct_dates` boolean (omission means no extra distinct-date constraint); `date_obligations` array of `{date,count_mode:minimum|exact,count:positive integer}` (omission means none). |
| `excluded_visit` | `subject_ref`; `scope=whole_trip|specified_dates`; `dates` is required and nonempty for specified dates, absent for whole-trip scope. |
| `protected_time` | `date`; `interval={kind:full_day}` or `{kind:clock,start:HH:MM[:SS],end:HH:MM[:SS]}`; explicit `scope=primary_visits|scheduled_commitments`. Clock endpoints are same-day, strictly increasing; `24:00` is allowed only as the end. |
| `fixed_visit_time` | `subject_ref`, `date`, `match=single_visit|at_least_one` and nonempty `conditions`; the multiple-visit mode also requires `repeat_permission_refs` as defined below. |

Booleans are not integers. Counts must be finite positive integers; dates are ISO
calendar dates within inclusive Input trip dates. Duplicate date entries for one
obligation, invalid references, nonpositive durations and unsupported resolved scope
values are material diagnostics. Full-day protection expands to local midnight to
the following local midnight, not a presumed 86400 seconds on a DST date.

### Default visit cardinality — user correction, 2026-10-01

For an explicit named-place visit obligation without stated repeat/count meaning,
upstream preparation writes `count={mode:exact,value:1}` for the requested trip and
obtains review. This supersedes the earlier default minimum-one decision. Evaluation
reads the explicit reviewed count; it does not infer a default from request prose.
A second confirmed occurrence violates exact one; a potential second occurrence can
prevent PASS. This authoring rule applies to actual reviewed named-place obligations,
not every venue the planner selects or source-grounded soft interests.

Explicit two/three/repeated visits follow their reviewed count/date semantics. A
numeric exact count is never weakened into minimum one. Explicit minimum counts retain
minimum semantics; clearly allowed repetition enables the multiple-visit time mode
below. A vague numerical quota is not invented for a permission such as multiple
visits; retain unresolved count meaning if it cannot be represented independently.

For `required_visit`, global occurrence count and date counts are separate conditions.
`distinct_dates=true` requires the global count to be represented on at least
`count.value` distinct requested dates; exact count still constrains occurrences.
Per-date counts are evaluated on their named date; they do not imply global exactness.
All explicit components must hold, and they remain inside one parent check.
Known contradictions (for example global exact two with minimum two on each of two
different dates) require upstream correction. An unresolved apparent conflict remains
visible rather than being labelled a planner failure. Do not combine separate
obligations into a new quota or add tests for absent fields.

### Occurrence date scope

Whole-trip means inclusive original Input trip dates for both global REQUIRED counts
and whole-trip EXCLUDED checks. Use requested `declared_day` values for structural
count/date reporting when the submitted civil-date fields agree; an absent timezone
alone does not erase an explicitly declared calendar day. Extra declared output dates
with consistent outside-trip timestamps are diagnostic observations outside these
obligation counts and descriptive denominators. A visit after the trip cannot satisfy
a required visit within it. Do not add extra days to the requested denominator.

Where a supplied timestamp contradicts its declared day, or independently supported
zone/offset interpretation contradicts the required date, preserve the source occurrence
but do not assert a confirmed scoped count. It is a potential match for every requested
date/trip scope that the retained uncertainty could affect. This also applies to extra
declared days with contradictory potentially in-trip timestamps. Do not choose whichever
date helps PASS. Invalid/missing clocks need not erase a consistent declared calendar
count; precise fixed-time/occupancy checks still require valid temporal interpretation.
These are structural scheduled-visit counts, not proof of actual attendance.

### Identity uncertainty and count bounds

For each subject/date scope, compute confirmed matching occurrences `L` and an upper
bound `U=L+potential_matches`. Adopted canonical identity establishes matches and
nonmatches; occurrence source identity prevents repeated imports from counting twice.
Same-venue visits at different source occurrences remain distinct. An unresolved
identity can be a potential match; observed search `candidate_ids` are not exhaustive
and their absence does not prove a nonmatch. Unresolved role records that could be
primary visits remain potential matches, with their reasons and declared dates.
Unresolved subject identity prevents confirmed venue equality; do not compare only
planner supplied IDs or name strings. Missing identity does not erase a known visit.

| Count condition | PASS | FAIL | Otherwise |
| --- | --- | --- | --- |
| Minimum `k` | `L>=k` | `U<k` | UNKNOWN |
| Exact `k` | `L=U=k` | `L>k` or `U<k` | UNKNOWN |
| At least `k` distinct dates | At least `k` confirmed matching dates | Fewer than `k` potentially matching dates | UNKNOWN |
| Exclusion | No confirmed or potential scoped match | At least one confirmed scoped match | UNKNOWN |

A conjunction's proven failing component establishes parent FAIL; PASS requires all
components PASS, otherwise UNKNOWN. This allows two confirmed visits to satisfy
minimum two despite an additional unresolved visit, while exact two remains UNKNOWN.
Count bounds are conservative; if uncertainty coupling cannot establish a conclusion,
retain UNKNOWN rather than asserting a jointly possible assignment.

One original obligation ID contributes one requirement check, regardless of component
count. Recognized applicable kinds with unresolved semantics or unsupported operators
contribute one UNKNOWN, not an N/A success. Unclassified unresolved clauses whose
applicability cannot be established retain a separate structural availability count;
they cannot be silently deleted to declare a complete score. Unknown executable kinds
require correction. Reviewed soft preferences are outside the obligation denominator.
An explicitly reviewed empty obligation list gives N/A only when there is no
unlinked unresolved content that could represent an applicable obligation.

`obligations` is the only collection generating weighted obligation checks.
`unresolved_items` is a completeness/annotation collection, not a second set of
weighted checks. Each item has `item_id`, `source_refs` and `reason`, with optional
`obligation_ref` or explicit `classification=soft_preference`. A linked annotation
references an existing parent obligation and adds no check; multiple annotations do
not multiply its weight. An explicitly reviewed soft item adds no hard check.
An unlinked, unclassified item retains `requirement_completeness_unresolved`, including
when obligations is empty: the requirement dimension is unavailable, not true N/A.
Recognized unresolved/unsupported hard requirements should be represented as original
obligations upstream; Evaluation never manufactures that parent from an annotation.
Malformed source/parent linkage requires correction. A partial known-obligation report
may still be returned, but no complete denominator or score is asserted until this
unlinked content is resolved or explicitly classified upstream.

### Fixed-visit-time scope (Q2 corrected by user on 2026-10-01)

For an explicit date and subject, support a conjunction of any nonempty selection of:
`start_at=HH:MM[:SS]`, `within={start,end}` (whole visit containment),
and `duration={mode:minimum|exact,seconds:positive integer}`.
Wire: `kind=fixed_visit_time`, `subject_ref`, `date`, explicit
`match=single_visit|at_least_one`, and `conditions` containing those fields.
There is no hidden five-minute time/duration tolerance. End at window end is allowed.
Duration uses resolved instants, including elapsed-time DST effects.

Without explicit repetition/count meaning, preparation selects `match=single_visit`:
exactly one same-subject primary visit in the requested trip must occur on the named
date and satisfy the entire time conjunction. The parent check combines global exact
one with dated time compliance, without adding an inferred extra obligation/check.
Two confirmed occurrences make it FAIL even if one has the correct time. A possible
extra occurrence or uncertain time/date can make it UNKNOWN. PASS requires exact-one
certainty and a fully compliant confirmed visit.

Only explicit original-input permission/requirements for repeated visits enable
`match=at_least_one`. This mode requires nonempty `repeat_permission_refs` with original
Input source references verified using the existing quote/offset convention. It is not
a default, and an itinerary's repetition or a reviewer selecting a mode without source
permission cannot authorize it. Any explicit numeric/date quota remains in its reviewed
required_visit obligation, checked independently. Same-subject reviewed obligations
must be mutually consistent; do not combine a default exact-one parent with an explicit
multi-visit count. Absence of a count for a clearly stated permission does not invent
an exact or minimum number of repeated visits.

In multiple-visit mode, at least one scoped primary visit must satisfy the whole time
conjunction; different visits cannot each satisfy different components. PASS needs one
confirmed fully compliant matching visit. FAIL needs proof that no confirmed or
potential occurrence could satisfy it; otherwise UNKNOWN. Other occurrences do not
invalidate this time-only component, but exact/minimum/date quotas still apply.

All-occurrences conditions, ordinal selection, cross-midnight clock windows, relative
ordering, recurring daily constraints and unspecified afternoon/evening remain
unsupported/unresolved with original meaning preserved. An explicit all-occurrences
meaning remains unsupported rather than weakened to either supported selector.
The author reviews the selector and its cardinality/source basis before submission;
evaluator prose interpretation never supplies it. Mechanically impossible time
conjunctions or contradictory explicit quotas require correction.

Examples (documentation only): "Visit A on Wednesday at 10:00 for at least 60 minutes"
has one trip-wide A occurrence, on Wednesday, satisfying all time conditions. Two A
occurrences violate its single-visit rule. "Visit A twice, with a Wednesday visit at
10:00 for at least 60 minutes" retains exact two in the reviewed count obligation;
at least one Wednesday A must meet all the time conditions. Two visits with neither
meeting the conjunction do not satisfy the time obligation.

## Independent time and occupancy preparation

Preserve original strings. Follow evidence-time-contract.md for half-open intervals,
offsets, IANA zones, unique localization and DST folds/gaps. Never use host timezone,
planner timezone metadata or provider duration to repair submitted timestamps.
Aware endpoints can establish instant relations without localization when their
declared date context is consistent; local-clock requirements need a supported
destination zone. Clock/date mismatch, zone conflict or unsupported overnight activity
leaves dependent checks UNKNOWN. Date coverage can still use explicit declared days.

Offline time context uses `schema_version=rtpeval_schedule_context_1`, `batch_id`,
`revision`, and `groups`. Each group has `group_id`, exact `input_sha256`,
`timezone` (IANA), `source_ref` (independent evidence or reviewed factual context),
`reviewer_ref` and offset-aware `reviewed_at`. Source hashes/review revision are frozen
with the report. Missing context is permitted as uncertainty, not default localization.
Supplying a context is factual preparation, not another user obligation.

Occupancy decisions use a separate source-linked review envelope
`rtpeval_occupancy_reviews_1`, with batch/revision and records. A record links exact
activity source, review revision, reviewer/time and rationale, with
`occupancy=committed|uncommitted|unresolved` and optional `protected_obligation_refs`.
It never edits role, identity or timestamps. Frozen review decisions must be replayed;
stale source/hash, duplicate active decisions or contradictory links require correction.
Version/projection membership is preserved; one activity ID is not a global key.
This envelope decides activity flexibility and protection-placeholder correspondence
only. It does not point at transfers, select a winning transport alternative, merge
transport sources or invent endpoint associations. Existing Ticket 01 activity reviews
can resolve V0 endpoint/role ambiguity through a new source-linked projection. Unbound
V1-V3 transfers or conflicting journey alternatives remain UNKNOWN/denominator-unresolved
in this slice. Further transport-association adjudication is not silently introduced
as an occupancy review feature.

Automatic occupancy decisions are limited to established primary visits, selected
transport claims and clearly uncommitted placeholders. Named unresolved primary
visits remain commitments even when their canonical identity is unknown. Generic
locationless placeholders can be uncommitted under the accepted free-time rule;
notes stating a reservation/fixed rest/appointment or conflicting protection prevent
automatic flexibility. Remaining flexibility is unresolved and needs independent
review. No planner lineage or Repair permission supplies that review.

### Commitments and transport

A primary visit is one commitment; a separately reviewed fixed generic activity is
one commitment. Each source-selected logical journey is one commitment. Consistent
V0 segments preserve their disjoint intervals within that journey and one score unit;
the gaps between segments are not occupied automatically. Same-source duplicate
claims contribute sources, not additional commitments. Repeated actual journeys
between different occurrence pairs remain separate even when both are A-to-B.
Unbound source-selected claims remain visible commitments or uncertain association
groups; they are not silently discarded or reassigned. If duplicate-vs-distinct
association is unresolved, the commitment denominator is not established.

Missing/invalid times on an established commitment give a time-UNKNOWN unit. Mode
uncertainty alone does not invalidate otherwise explicit occupancy times; route mode
evaluation remains separate. Conflicting same-journey claims are alternatives, not
two simultaneous journeys. While their alternatives remain unresolved, occupancy is UNKNOWN; clear common
overlap may be reported as a lower bound only if every surviving alternative proves it.
Never turn incomplete `journey.occupancy` into an empty known schedule.

V1-V3 ignored transport activities and V0 ignored transfers contribute no occupancy,
mode or fallback. An absent transfer stays missing: do not generate its interval from
adjacent visits or independent route duration. Missing journey claims are reported
as transport-structure coverage; schedule non-overlap assesses submitted commitments
and does not certify the physical feasibility of an unrepresented journey.

### Protected blockers (Q1 accepted by user)

Normalize resolved protections by date and exact scope. Union overlapping/touching
same-scope intervals for occupancy checks, retaining every original obligation ID
and interval. Different scopes remain separate and are filtered by their explicit
meaning. Protections do not conflict with each other. `primary_visits` forbids primary
visits only; `scheduled_commitments` forbids primary visits, selected transport and
fixed generic commitments, while leaving genuine uncommitted free time available.
Do not guess a protection scope from its output placeholder or planner interpretation.

Protected blockers are not additional non-overlap score units. A forbidden commitment
overlapping a protection is FAIL in its non-overlap check; each affected original
protection obligation is also FAIL in the requirement dimension. This cross-dimension
relationship is explicit, as with existing correlated timing/route consequences.
Adding overlapping protection clauses cannot increase the activity denominator.

An output placeholder representing the same protection is not counted as a second
commitment. Equivalence needs source-linked independent review referencing the
original protection; simple temporal overlap or a shared word such as rest is not
enough. Keep an actually separate fixed appointment as its own commitment. Unknown
scope/time/placeholder correspondence retains dependent UNKNOWN or denominator
availability reasons. Unresolved protections are not unioned as guessed intervals.

## Non-overlap checks and duration reporting

One established distinct commitment contributes one check. A positive intersection
with another distinct commitment, or with an applicable protected blocker, yields
FAIL. Touching endpoints do not overlap. A commitment with known complete occupancy
and no possible unresolved conflict is PASS; if conflict cannot be excluded, UNKNOWN.
Confirmed conflict overrides unrelated uncertainty. Identity equality does not erase
an overlap between two separately scheduled same-venue visits.

`P/(P+F+U)` is the verified non-overlap fraction on an established commitment set.
Do not create O(n^2) passing pair checks. Unresolved role/flexibility or ambiguous
duplicate correspondence can leave unit applicability/count unknown: report known
units/states, candidate counts and `denominator_unresolved`; no full-scope percentage
is produced from a convenient smaller set. The later aggregate ticket must preserve
that availability diagnostic rather than treating it as group-wide N/A.

Report positive unordered commitment-pair conflicts once, separately from
commitment-to-protection conflicts. For each pair, union segment intersections;
do not multiply pairs by segment/source count. Sum-of-pair intersection time is not
union conflict time. Report per-day and request union of instants with at least two
distinct conflicting commitments, protection-conflict union, and their combined
conflict union. Protection-to-protection intersections do not add conflicts.
Report known durations with complete/lower-bound status and unknown record counts.
Do not round seconds before comparisons or treat an unknown interval as zero.

Scheduled occupied time is the union of submitted established commitments only.
Protected reservation union is separate; a combined occupancy/blocker view may be
exported for Ticket 07 but does not select departure or imply a continuous route gap.
Local-day slicing requires valid time context. Retain whole-request known instants
when only daily attribution is unresolved; DST days are not forced to 24 hours.

## Descriptive schedule metrics

- Date coverage uses inclusive Input requested days as denominator. Report declared
  day-present, any-submitted-activity, known-primary-covered and empty-primary-day
  counts. Possible-primary days have unknown coverage; raw submitted-activity counts
  are not assertions about evaluated occupancy. Missing requested days remain zero
  known visit days. Extra output dates are diagnostic, not extra denominator days.
- Density counts source-distinct primary occurrences on requested declared days,
  including empty days. Report known and possible counts, and `<2`, `2..5`, `>5`
  categories only when role uncertainty cannot change the category. These are
  descriptions, not quantity FAILs. Canonical uncertainty does not remove an otherwise
  established visit from density.
- Canonical repetition groups adopted identities only. For venue occurrences `n`
  across `d` declared requested dates, extra occurrences are `n-1`, within-day extras
  are `sum(max(0,n_day-1))`, and across-day extras are `d-1`; the two extra counts
  sum to `n-1`. Report repeated venue counts, occurrence counts and unresolved
  identities separately. Observed known-identity repetition is a lower bound when
  unknown identities could merge/add repetitions.
- Display reviewed minimum/exact/date revisit obligations alongside observed counts.
  Do not allocate duplicate obligations as additive authorization, guess which
  occurrence was necessary, or report an automatic non-required-repetition defect
  ratio. Minimum revisits and visits beyond a minimum are not automatic violations;
  explicit exact-count excess is already assessed in its parent requirement check.

## Report and implementation scope

Report schema: `rtpeval_requirement_schedule_report_1`. Include batch/group/run and
projection IDs; Input/spec/result, identity/review/context and rules hashes; check
IDs derived from stable parent obligations/commitments; sources; applicability;
PASS/FAIL/UNKNOWN/N/A; reasons; component states; count bounds; raw interval measures;
known/candidate unit counts; denominator availability; and descriptive coverage,
density/repetition fields. Null is missing, never NaN/Infinity or invented zero.
Repeated replay preserves all semantic fields; generated time is metadata.

Implementation proposal: add `backend/evaluation/requirement_schedule.py` for typed
validation, obligation checks and descriptive metrics; `schedule_time.py` for independent
time normalization; `occupancy.py` for commitment/blocker preparation; and
`requirement_schedule_cli.py` for explicit offline JSON input/output. Add focused
`backend/tests/evaluation/test_requirement_schedule.py`, `test_schedule_time.py`,
`test_occupancy.py` and CLI coverage, with package guide/acceptance updates. Names are
proposed module boundaries, not implemented commands.
Keep Ticket 01 intake behavior and immutable source records intact. The fixed-time subject
extension in `identity.py` must preserve Ticket 03 identity audit and replay.
The expected identity reference set is recomputed from the extended subject selection
and selected projections. Record its digest and
`subject_scope_version=required_excluded_fixed_time_1` in newly prepared identity output.
Scorer preflight validates this set, source links and policy scope; missing/new/stale
references require `identity_replay_required`, not silent adoption of a smaller old report.
Replay the existing offline resolver against frozen evidence/reviews/audit after the
subject extension, because the additional subject can move other visit candidates into
high-impact review. Previous automatic decisions do not bypass that recomputation even
when input/spec/result hashes are unchanged. Missing evidence on replay remains UNKNOWN;
no live lookup is required. Missing identity evidence differs from an omitted preparation
reference: only the latter is a stale/incomplete identity preparation diagnostic.
No new infrastructure, planner execution path or acquisition client is needed.
Opening (06), route verdicts/departure selection (07), five-dimension total/mask (08),
blind HTML (09) and Repair comparison (10) remain their own tasks.

### Future offline acceptance slices

1. Typed payloads, source linkage, empty reviewed obligations and contradictory specs;
   distinguish material correction from content UNKNOWN without shrinking the batch.
2. Minimum/exact/date/distinct-date conjunctions; confirmed and potential identity/role
   matches; wrong supplied ID with independently adopted identity; Nearby exclusion.
3. Accepted time operators and quantifier boundaries; exact endpoint,
   precision, missing zone, offset mismatch, DST fold/gap and full-day expansion.
4. Protected-scope unions, original obligation checks, placeholder correspondence and
   blocker exclusion from the non-overlap denominator; fixed generic commitments.
5. Touching intervals, triple overlaps, segments/duplicates/alternatives, unbound and
   missing/incomplete transport, wrong-version source exclusion and denominator uncertainty.
6. Empty/extra dates, density with role uncertainty, known-identity repetition lower
   bounds and authorized minimum revisits without an invented defect penalty.
7. Offline CLI replay/source immutability and invariance to planner internal finding,
   requirement-interpretation and mechanism metadata changes; network access guarded.

These are future engineering fixtures, not executed checks or formal benchmark cases.
Relevant existing evaluation regressions, broader backend checks if shared code changes,
Ruff and Standards/Spec review are required during the separately approved implementation.

## Documentation verification record

Read-only code/contract consistency review caught the initially assumed schema name;
it was corrected to the existing `rtpeval_requirements_1`. The review also identified
underspecified unresolved-item applicability, ordinary count date scoping, transport
review targets and fixed-time-only identity replay. These mappings were made explicit
above without changing the accepted Q1/Q2 semantics. Validation uses code reading,
local link/anchor checks, current-status consistency and diff whitespace only.
No backend tests, fixture execution, live service or scoring run belongs to this record.

Final checks passed: 44 new/changed local documentation links/anchors, implemented
schema-name and current-status consistency, explicit completeness/replay mappings,
English contract content and diff whitespace. Read-only follow-up review found no
remaining concrete contradiction blocking this specification. Existing runtime files
were unchanged; the earlier unrelated workspace documentation/AGENTS edits are preserved.

## Specification verification and authorization

On 2026-10-01 the user accepted both proposed semantic decisions: protections are
blockers rather than additional non-overlap units; explicit dated fixed-time checks
use the bounded operator set. The subsequent same-day user correction supersedes
the initial default at-least-one selector: unstated counts use a single visit, while
explicit repeat permission permits at-least-one time matching. The prior
transport and same-scope union decisions remain in force. Technical defaults here
are explicit field absence semantics, not inference from planner/request prose.

This contract closes Ticket 05's specification gate. It authorizes neither the
implementation nor a live smoke/experiment. The implementation proposal includes
TDD, focused/broader relevant regressions, Standards/Spec review, fixes and acceptance
documentation as one task. Git actions remain separately authorized. Existing
uncommitted documentation and AGENTS changes must be preserved.

## Cardinality correction verification scope — 2026-10-01

The user's correction supersedes default minimum-one visit authoring and default
at-least-one fixed-time matching. Supported time operators and protection scoring are
unchanged. Active contract/status summaries now describe exact-one/single-visit defaults
and source-gated multiple-visit time matching; historical checkpoints are marked as
superseded where needed. This is specification correction only; implementation approval
is still pending. Future tests must cover a second confirmed/potential occurrence,
explicit exact/minimum multiple quotas, absent repeat permission and selector/count
conflicts. No source artifact, planner behavior or scorer code was changed.

Cardinality-correction checks passed: 45 new/changed local document links/anchors,
single-visit/source-permission consistency and diff whitespace. No backend tests ran.
