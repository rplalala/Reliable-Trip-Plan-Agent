# Ticket 09 blinded ranking specification preflight

Date: 2026-10-02, Australia/Sydney. Inspected code revision:
`33903d0bc914f7b10c889d80ff19159f863cb88b`, branch `feature/evaluation`.
Initial worktree/index: clean. Status: specification preflight complete; implementation
scope approval pending. This record is a specification proposal, not implemented assessment.

## Authority and scope

[PROJECT](../../PROJECT.md) is current authority; [AGENTS](../../AGENTS.md) owns approval,
language, local Git and research boundaries. [Issue #21](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21)
owns Ticket 09 state; [parent #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12)
remains open. The live Issue and its empty comment list were read. Its predecessor is
completed Ticket 01, not the automatic scoring tickets. Ticket 08 is completed separately.
The historical [local ticket](issues/09-blinded-ranking.md) is not a second live tracker.

The user authorized specification preflight only. This includes relevant current code/
contract inspection, existing offline seam checks, clarification, related documentation/
archive/tracker records. It does not authorize new backend/frontend implementation,
renderer prototypes, browser package builds, real rater sessions, study sampling,
formal comparisons/inference, live/model/provider/database/native supplements, push,
version freeze or another ticket. Implementation needs separate explicit scope approval.

Matt routing uses grill-with-docs with grilling/domain vocabulary, adapting to the
existing evaluator documentation. No new study, fixed sample quota or statistical
analysis plan is introduced. One factual projection/UI audit was delegated read-only
as requested by grilling; user decisions stay in this conversation.

## Already established requirements

[Artifact/human-answer contract](artifact-contract.md), [module specification](spec.md),
[projection contract](intake-projection-contract.md) and the human sections of
[evaluator design](../../docs/evaluator_design.md) already establish:

- Explicit selection from an accepted batch; four selected final v0-v3 plans per task.
  No dependence on identity adjudication, automatic scores, oracle snapshots or complete
  resource observations. Intake's four linked usage envelopes remain required, but
  collection may be unavailable. Do not relax the intake contract for this ticket.
- One original Input and uniform anonymous A/B/C/D plans. Labels remain fixed across
  preference match, pace and practical usefulness within a task. Assignments are
  randomized/balanced and frozen privately; counts/selections come from supplied config.
- Hide source/version/implementation metadata, canonical IDs, raw result filenames,
  internal findings/Repair status, scores, RequirementSpec, independent oracle evidence
  and Nearby. Do not LLM-rewrite plans, improve itineraries or remove meaningful uncertainty.
- Ordered tie groups partition all four labels exactly once for a submitted ranking.
  Whole-dimension unable_to_judge and not_applicable remain distinct from ties. A partial
  label ordering is a draft, not a submitted three-plan ranking or an automatic tie.
- Local save/resume plus explicit JSON export/import, with exact presentation linkage
  and retained revisions. The private version mapping never enters public HTML or answers.
- Six underlying-version pair outcomes per assessable dimension, with per-pair available
  denominators and separate missingness. These six observations are correlated within
  a request. No total ranking score, inferential comparison or inter-rater statistic.
- Hidden duplicates have new task IDs/assignments, spaced in supplied task ordering.
  They contribute only intra-rater consistency, never main-result weight. Real assessment,
  rater recruitment and final sample/duplicate counts remain separately authorized work.

## Observed executable seams and gaps

`load_batch` validates byte hashes, selected runs, source links and reviewed requirements,
then exposes the original Input, source-preserving final projections and private context.
Those objects contain IDs, sources, planner_version, role/review metadata and diagnostics;
they cannot be serialized wholesale to a browser. A strict public display DTO is required.

Current projection Activity fields retain title/place/location/clocks/cost/notes. Transfer
fields retain endpoint IDs, mode, departure/arrival, duration/distance/reserve; they omit
raw Transfer unknowns and calculation_basis. Some of that omitted text expresses meaningful
uncertainty. A blind display adapter must inspect exact linked original material through
the existing material boundary, not invent certainty from an incomplete projection or
copy whole provider/internal records. Its proposal accepts the manifest path, not arbitrary
caller-authored display summaries. No shared projection/scorer policy change is proposed.

Latest transport source selection is authoritative: V0 transport Activities; V1-V3
application Transfers, with ignored transport Activities retained only privately. Never
use an ignored Activity as fallback when a Transfer is missing. Unbound/ambiguous/dangling
authoritative claims must stay visible with a neutral association-uncertainty notice.
Do not insert only transfers matching to_activity_id and thereby silently hide leftovers.

Journey occupancy deduplicates timing tuples, not all display content. Consistent duplicate
claims may have distinct notes/cost/distance/reserve content; display keeps those distinct
meaningful fields once, traceable to all originals privately. Conflicting alternatives
remain distinct supplied claims; sequential segments remain segments. Missing clocks/
arrivals and malformed-but-preserved text stay explicit, without invented source timestamps
or a favorable fictional merged journey. Q2 below separately permits labelled display-only
arrival arithmetic; it never changes source claims. No opening/route verdict is shown.

Product ItineraryView is unsuitable for direct reuse: it displays attribution, internal
validation/coverage, weather and Nearby; insertion by endpoint can omit unbound claims,
and its HH:mm extraction hides offset/cross-date information. An independent React
component should consume the anonymous DTO. Existing product/developer UI behavior remains
unchanged. Display original dates and clocks with available offset/cross-date context;
do not infer a zone or move/split an activity. Missing times keep declared-day/source
order with a neutral notice rather than being silently deleted.

Input display allowlist: destination, start_date, end_date, traveler_count, original
whole-trip budget amount/currency and additional_preferences. Version/request metadata
and reviewed interpretation are withheld. Activity allowlist: title, displayed place/
location, original start/end, notes and original displayed cost. Transfer display uses
plain mode, supplied clocks/duration/distance/reserve and necessary neutral uncertainty.
No provider badge, schema/activity/canonical ID or derived evaluator verdict is exposed.

## User clarification frontier

### Q1: explicit identity/provenance text leakage — Accepted

The user adopted the recommendation and asked whether the researcher prepares the page
before the rater receives it. Yes: the researcher reviews the prospective display content,
then supplies source-linked manual redaction for explicit version/provider/internal-review
identifiers. Ordinary content remains verbatim; travel facts and uncertainty are preserved.
Original files are unchanged. Original text, exact source/field/hash linkage, reviewed
display text, reviewer, timestamp and reason remain in the private preparation record.
No LLM rewrite or automatic factual repair. Unsafe unresolved leakage blocks package
delivery rather than quietly dropping text/tasks or exposing the private mapping.

The source-linked review/approval applies to the complete prospective presentation.
Lexical checks can flag likely leakage but cannot certify free text safe; a genuine
place name resembling a version code must not be blindly erased. HTML escaping and
script/data separation are also required; markup in source text is inert display text.
This is preparation of anonymous material; the rater independently supplies rankings.

### Q2: missing claimed arrival — Accepted, explicitly labelled display inference

After a concrete example, the user chose to show source departure/duration and additionally
compute a clearly labelled inferred arrival: source 10:00 departure plus 30 minutes gives
"Inferred arrival: 10:30; arrival not supplied by the itinerary". This is a display-only
specialization, not a submitted arrival claim, independent evidence or factual correction.
Keep the source arrival field absent and never feed the computed display value to scorers.
Use only the selected source's valid, unambiguous departure and duration. No new provider
query, route evidence, inferred timezone or hidden reserve is used in this arithmetic.
Preserve supplied estimate/unknown wording, explicit offsets and cross-date rollover.
If either operand is missing/ambiguous/invalid, show the supplied fields and unavailable
inference reason instead of inventing a clock time. A supplied arrival is displayed as
supplied; no inferred value overwrites it. These boundaries preserve the projection
contract's prohibition on manufacturing a claimed arrival. No extension is implemented yet.

### Q3: correction after submission — Accepted, latest submitted revision is effective

The user permits corrections and specifies that the new revision supersedes the old
answer. This specializes the earlier manual final-selection proposal: for each task/rater,
the highest valid complete submitted answer_revision is effective automatically. Keep
older revisions only for audit, never as additional counted answers. Draft saving does
not supersede a submitted answer. Revision ordering is explicit, not file modification
time, import order or a browser clock. Exact replay is idempotent; different content at
the same revision is a conflict requiring correction rather than arbitrary overwrite.
The report identifies the effective revision and content hash so selection is reproducible.

## Proposed interfaces after clarification and implementation approval

Prefer three offline public seams, with explicit versioned config and generation metadata:

1. Delivered manifest + selection/presentation config + source-linked projection/display
   reviews -> public HumanTaskPackage, separate private mapping/preparation record.
2. Exported answer bundles + frozen presentation/mapping -> validated retained drafts/
   submitted revisions and material diagnostics, without silent record replacement.
3. Validated revisions + latest-submitted-revision policy -> separate HumanReport with
   underlying pair outcomes, missingness and duplicate consistency, without automatic totals.

Potential files: backend/evaluation/human_tasks.py, human_answers.py, human_report.py and
human_cli.py, related public-boundary tests; independent frontend/src/features/blind-review/
components/state/tests and a separate assessment build entry/config. File names/interfaces
are proposals, not implemented modules. No FastAPI endpoint, account system, hosting,
database persistence, email delivery or external client is proposed.

Use existing React/Vite dependencies for an offline static bundle. A proposed isolated
classic/IIFE bundle with inline assets avoids needing a dev server/module import/CDN
at task consumption time. Installed Vite types expose library formats, CSS split and
sourcemap controls; actual file:// loading/storage/export behavior still needs future
implementation/browser verification. No build/browser prototype was run in this preflight.
Public package generation must reject a bundle with external asset dependencies or
source maps/private source data. Existing product build configuration remains intact.

Proposed presentation config explicitly supplies selected unique main groups, duplicate
references/order/separation, seed, policy/revision and one opaque rater slot. No default
12-case/three-duplicate study quota. Private deterministic assignment policy and actual
frozen mappings are recorded; the seed/mapping never enters public HTML or answer files.
The proposed engineering profile balances version-to-label positions across all shown
tasks, including hidden duplicates: for each version, maximum minus minimum position
count is at most one. Main-only, duplicate-only and combined counts remain private
diagnostics; only main tasks contribute preference outcomes. Randomization and spacing
are independent of response outcomes. A supplied ordering/config that cannot meet the
declared constraints is rejected, not silently reduced. No formal sampling decision is
inferred. Actual algorithm feasibility/replay checks belong to approved implementation.

Use opaque public task/presentation IDs; source group/run/version/file references and
duplicate markers remain in the private mapping. Public batch/revision identifiers must
not themselves leak source labels: validate safe identifiers or record a private source-
to-public alias. Exact source-byte hashes remain private, not disguised as browser IDs.
Package regeneration changes the frozen presentation revision/hash rather than allowing
old answers to attach to a new ordering. Config/private/public linkage is checked on import.

Public answer records preserve the artifact contract's answer_schema_version, linked
batch/presentation/task identity, opaque rater_ref, answer_revision, aware updated_at,
submission state and exactly three dimension responses. Export bundles contain public
answers only. Draft incomplete groups are preserved but cannot create pair outcomes.
Submitted ranked groups are nonempty and partition A/B/C/D; unsupported labels, repeated/
missing labels, unknown tasks, stale revisions and same-key conflicts are diagnostics.
Browser storage is best-effort; failed storage must be visibly disclosed, with JSON
download/import as portable backup. No save acknowledgement without successful persistence.

The effective answer is the highest valid complete submitted revision per task/rater;
its revision and content hash are recorded explicitly. Older imported revisions cannot
replace it; same-revision conflicts block reporting until corrected.
Pair outcomes use six fixed unordered version pairs with an oriented win/tie/loss convention.
Unable-to-judge/N/A/draft/unselected/missing counts remain separate; no artificial ties.
Duplicate consistency compares the selected original and duplicate by underlying version
pair, separately per dimension, with agreeing/comparable pairs and unassessable reasons.
Zero comparable pairs gives null agreement, never 100%. Missing duplicate/original does
not remove a main task. No optional automatic score/report integration is proposed.

## Planned implementation acceptance checks

- Synthetic manifest -> frozen package -> exported/imported revisions -> researcher
  outcomes. Preserve source bytes, require strict path/hash/config/presentation linkage.
- Uniform rendering/three-dimension labels; deterministic seed replay and balance;
  independently reassigned/spaced duplicates with no main-count inflation.
- Whole public HTML/JSON/assets/export leakage inspection, including script strings,
  IDs, filenames, free-text metadata, private mappings and duplicate/source flags.
  Hostile source markup cannot execute or create external requests.
- Source-selected transport, duplicates/segments/alternatives/unbound claims, unavailable
  arrivals, explicitly labelled display-only arithmetic, preserved cost/note/uncertainty
  and meaningful cross-date/offset display; no computed value enters source/scorer data.
- Ties/all-tied partitions, unable-to-judge/N/A, drafts, revision conflicts, latest valid
  submitted revision selection, idempotence, stale imports, storage failure and backup.
- Six exact mapped pair outcomes per dimension; missingness and duplicate agreement with
  null empty denominators, separately from quality/resource/mechanism reports.
- React interaction tests and isolated offline build, then actual local browser visual
  inspection of synthetic desktop/narrow examples and file:// persistence/export/import.
  No real rater, real study case or formal comparison is part of these development tests.
- Relevant intake/backend/frontend regressions, Ruff/type/build/document checks, one final
  full relevant offline gate, then pre-review local implementation commit and Standards/
  Spec review/correction commits under AGENTS. Implementation approval remains required.

## Actual preflight verification

Existing intake/source-projection regression: **56 passed, 1 skipped in 3.23s**, repository
Python 3.12.14, no cacheprovider, TRIPWORLD_TEST_DATABASE=0, task-local pytest root.
The skip is the existing Windows symlink privilege case; no supplement was run. Initial
run passed with no failure/correction/retest cycle. No new Ticket 09 test, HTML package,
React component, questionnaire result or implementation exists. The Ticket 08 full
2273/10-skipped gate remains prior history, not a Ticket 09 run.

Q1-Q3 are accepted. The preflight resolves display preparation, optional inferred arrival
and answer correction semantics. The interfaces and bounded synthetic validation above
are the concrete proposed implementation scope. User confirmation/approval of that
consolidated scope remains required; do not begin implementation from preflight alone.

## Documentation and tracker closeout

[Tracker synchronization](ticket-09-tracker-update.md) records successful updates and
exact independent body readback for Issue #21/parent #12. Both remain open with their
existing labels and unchecked Ticket 09 implementation acceptance. Historical published
links remain unchanged; the new detailed documents are local/unpublished.

English/content and local-target checks passed for eight related documents, including
the ignored archive: 170 local Markdown targets. Diff whitespace checks passed. The
completed test's temporary root was removed only after verifying its exact absolute
workspace target and absence of reparse points. Only seven intended documentation files
are selected for a local docs commit; the ignored historical archive is not force-added.
No implementation review is claimed for this documentation-only preflight. Implementation
approval would activate TDD, bounded synthetic checks, commit-before-dual-review and
separate correction commits; it would not authorize push or actual rater assessment.
