# Independent evaluation architecture

Status: Tickets 01-12 have offline implementations within their approved scopes.
This is a technical boundary, not a formal benchmark or results report.
[PROJECT.md](../PROJECT.md) and live Issues own current authorization and task state.

## Separation from planning and benchmark construction

The final-quality workflow consumes a deliberately submitted, curated, source-linked batch. It does
not run planners, choose replacement cases, monitor a growing case list or decide when
benchmark construction is complete. The producer/user owns batch selection and eligibility.
Planner caches, validator verdicts and repair-target disappearance are not independent
factual ground truth. Independent observations retain provider/time/query applicability.

Input identity and artifact hashes preserve exact provenance. Original result bytes are
not rewritten to improve scores. Version-neutral projection separates visits, protections,
references and transport, preserving uncertainty and source references. V0 transport comes
from model transport activities; V1-V3 transport comes from application transfers. Ignored
sources retain diagnostics but contribute no fallback transport occupancy.

## Implemented module boundaries

| Slice | Implemented responsibility | Detailed reference |
| --- | --- | --- |
| 01-04 | Intake/projection, opt-in usage reporting, identity/adjudication, injected snapshot acquisition and replay | [Intake/identity/usage](contracts/0002-intake-identity-usage.md) |
| 05 | Requirement and schedule metrics with independent time/occupancy review | [Requirement/schedule](contracts/0003-requirement-schedule.md) |
| 06-07 | Offline opening and route preparation/scoring | [Opening/routes](contracts/0004-opening-routes.md) |
| 08-09 | Quality report, anonymous review package, answer import and descriptive outcomes | [Quality/human review](contracts/0005-quality-human-review.md) |
| 10 | Source-driven V3 draft/final-primary preparation, paired masks/deltas and independent continuity | [V3 paired diagnostic](contracts/0005-quality-human-review.md#v3-pairs) |
| 11 | Isolated frozen real V3 post-primary execution and independently reviewed target/control outcomes | [Controlled Repair](contracts/0001-evaluation-artifacts.md#controlled-repair) |
| 12 | Selected-source mechanism reports, exact official-claim audit queue/reviews and default-off local submission/selection capture | [Mechanism/audit](contracts/0001-evaluation-artifacts.md#mechanism-official-audit) |

[Artifacts and evidence contracts](contracts/0001-evaluation-artifacts.md) define shared
material integrity, source roles and independent evidence/time semantics. The five topic
contracts state current rules continuously, including ordinary-output compatibility. Historical
proposals and approvals remain in linked records/Issues. Broad proposals do not imply that
unimplemented follow-up modules are available.

Snapshot acquisition accepts injected transport. The evaluator-owned
`evaluation_run.prepare_run / execute_run / replay_run` and
[formal CLI](../backend/evaluation/README.md#fresh-automatic-evaluation-cli) now compose
fresh Google acquisition, V0-only correspondence and all native automatic final-quality
consumers. Preparation freezes originals, contexts, limits, prices and code; execution
persists evidence/failures; replay sends nothing. Final-only scope explicitly excludes
optional V3 and human/controlled/official tracks. Processing, acquisition and unresolved
evidence are separate fields. Fresh execution requires a prepared, approved allowance.

The Sydney four-original automatic flow completed fresh execution and network-blocked
CLI replay on 2026-10-09. All originals and receipt-covered evidence verify; current-policy
FAIL/UNKNOWN outcomes and conservative semantic limits remain visible in the
[acceptance record](records/evaluation/intake-identity-usage.md#sydney-four-final-fresh-acceptance-2026-10-09).
This establishes an engineering execution path, not a formal version comparison or
all-facts-verified result.

Development smoke helpers are separate from ordinary evaluator consumers. The
[V0 route request preparer](../backend/evaluation/tools/route_requests.py) and its CLI
live under `backend/evaluation/tools/`; they prepare acquisition inventories and budgets
for explicitly approved development checks. They are not product runtime stages or
dependencies of final quality scoring. Core intake, independent identity, snapshot,
schedule/opening/route scorers and report CLIs stay in `backend/evaluation/`. Product
planning does not import this evaluation package. V3's internal validation/repair remains
part of planning and is distinct from independent evaluation.

Route preparation can extract coordinates offline from a verified identity-phase snapshot
whose evidence matches verified physical associations. This reuses saved independent
observations with separate coordinate provenance; it does not borrow planner coordinates or
acquire missing points. Missing, invalid or conflicting points retain local uncertainty and
route candidates. The existing reviewed-coordinate source remains supported; details and
acceptance are in the [opening/route contract](contracts/0004-opening-routes.md#accepted-snapshot-coordinate-extension-2026-10-03)
and [dated bridge record](records/evaluation/routes.md#snapshot-coordinate-bridge-2026-10-03).

## Scoring semantics and uncertainty

The user accepted a [version-specific evaluator requirement](contracts/0002-intake-identity-usage.md#version-specific-identity-requirement)
on 2026-10-06: V0 introduces an LLM primarily for generated-POI correspondence with
independent API candidates; V1-V3 evaluation uses API evidence and program rules without
an evaluator model or fallback, including user-named requirements. Original API-backed
name/address differences count as errors, without repair. [Parent #74](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/74)
owns the classified follow-ups. Version dispatch (#75) and the V0 citation/missing-address
response correction (#76) are implemented locally; fresh-smoke preparation, offline route integration and delivery
remain separate follow-ups. Historical evidence is not reclassified.

Implemented identity uses the [version-specific contract](contracts/0002-intake-identity-usage.md#version-specific-identity-requirement):
V1-V3 use ID-linked API Details and literal name/address equality. RequirementSpec
meaning and API acquisition evidence are shared, but target identities are version-owned
under [#83](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/83). V1-V3 targets
use independent Details bindings or complete search evidence with a unique strict matching
ID after filtering by name, destination and supplied address. V0-only packets match
generated claims and user-requested targets with their independent candidates.
Requirement checks compare IDs within the same version before counting visits or
evaluating dates/time conditions. Citation enums and address-presence alternatives
agree with import validation; absent addresses require `not_supplied` without claiming an error.
Candidate correspondence and original-claim correctness remain separate in verified reports.
Reports require exact source-bound replay. High-impact
references and sampling no longer require human identity confirmation. Address correctness
remains a separate assessment: recognizing a venue does not repair the delivered address
or establish opening/route feasibility. Both a recognizable venue with an incorrect submitted
address and an address identifying another venue produce grounding FAIL and prohibit canonical
claim adoption. Under `versioned_api_identity_3`, the separately verified physical
association may permit requirement occurrence matching and opening/routes despite claim
FAIL: V0 uses existing validated
correspondence, V1-V3 independently verify the original API ID. Untrusted associations
remain UNKNOWN. Original time, order, transport mode and reserved duration are unchanged;
physical PASS cannot cancel grounding FAIL. Requirement occurrence matching uses the
verified association against the target's version-owned adopted canonical identity;
the target's grounding FAIL and all count/date/time components remain independently
applicable. A physical association alone does not establish full requirement fulfillment.
Historical policy-2 reports retain canonical-only downstream eligibility through
explicit `--historical-association` replay. Insufficient evidence stays UNKNOWN.
Supported V0 destination conflicts also remain FAIL even when the original address is absent.
All versions use the same standard; evaluation does not hide baseline errors or presume a version must fail.
Explicit historical human and uniform LLM identity replay is retained.
Blinded preference review and other human supplements keep their separate responsibilities.

| Term | Meaning |
| --- | --- |
| Submitted group | One request and its source-linked selected version artifacts; inclusion is not proof of quality |
| Claim | A proposition represented in the submitted output or reviewed obligation |
| Independent observation | Separately sourced evidence with declared identity/query/time applicability |
| Physical association | Verified API venue usable for occurrence matching, hours and coordinates while preserving original grounding and version-owned requirement targets |
| Identity judgment | Version-scoped program checks or V0 model correspondence with independent API facts, preserving original claims and uncertainty |
| Historical adjudication | Human resolution in an explicitly replayed legacy identity report |
| Compliance | Outcome against an applicable criterion, distinct from evidence availability |
| Common mask | The explicitly shared comparison set; missing evidence must remain visible |
| UNKNOWN | An unresolved applicable fact/outcome, not a passing check or a zero-valued measurement |
| Blinded review | Human preference judgment without exposing version attribution or automatic scores |

Explicit obligations retain exact counts, dates and subjects. Same-scope overlapping protected
intervals share occupancy blocking while each original obligation is checked independently.
Protections are not additional non-overlap score units. Unstated named-visit counts do not
silently authorize repeated visits; explicit repetition permission has separate semantics.

Opening/route checks distinguish decisive independently supported FAIL from complete PASS
and unresolved evidence. Coverage, availability, denominators and burden remain visible.
Quality reports use exact shared-mask arithmetic; uncertainty must not disappear by shrinking
a denominator or treating unavailable dimensions as zero. Fees/access and absent facts are
not certified by structural schema acceptance.

Anonymous review is separate from automatic scoring. The researcher prepares source-linked
display material, holds the hidden mapping and imports revision-aware answers. The renderer
uses IANA time-zone selection and HH:mm, with confirmed clearing scoped to the active package
and rater. User-reported browser acceptance is distinct from automated test evidence.

<a id="proposed-follow-up-boundaries"></a>

## Paired, controlled and mechanism boundaries

Ticket 10's offline preparation/report uses validated existing activity/adopted-edit/split
lineage before content fallback and residual review. It preserves valid paired aggregate
scores despite unresolved local correspondence, while venue identity and quality remain
independent of producer decisions. Its two-stage mask is separate from the four-final mask.
See the [development acceptance](records/evaluation/v3-pair-report.md).
Controlled Repair is the isolated Ticket 11 execution boundary. Ticket 12 reads selected
saved sources and optionally captured actual observations. Internal acceptance, independent
quality and independent official-fact review remain separate. Capture adds no model/provider
calls or tokens by design; its local normalization/storage overhead is unmeasured. Missing
historical observations cannot be inferred from final outputs or current gate replay.
This document authorizes no formal run, comparison or final conclusion.

Ticket 11's [accepted controlled replay contract](contracts/0001-evaluation-artifacts.md#controlled-repair)
uses the real V3 Repair path with frozen capabilities and independently reviewed outcomes.
Controls permit lawful changes while checking preserved user obligations and newly introduced
problems; explicit one-visit restrictions override generic quantity recommendations. Human
supplements remain separate from planner inputs, and unresolved verdicts remain visible.
The offline implementation recomputes production permissions and uses strict frozen
external scripts, restored caches/semantic state and logical async timeouts. Raw paired
scores remain separate from supplemented check outcomes. Formal case construction,
live execution and Issue synchronization remain separately authorized; no formal cases
have been built. See the [executable wire](contracts/0001-evaluation-artifacts.md#controlled-executable-wire).

Task authority: [parent #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12),
[Ticket 10 #22](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22),
[Ticket 11 #23](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23), and
[Ticket 12 #24](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24).
Commands and exact implemented outputs belong to the
[evaluation package guide](../backend/evaluation/README.md).
See [ADR: evaluation independence](adr/0004-independent-evaluation.md).


## Batch and benchmark terminology

**Qualifying group**: One request and the four V0-V3 outputs whose respective workflow completion has been established by benchmark construction. Qualification is not a claim of itinerary quality.
_Avoid_: Correct group, evaluator-approved run

**Benchmark candidate list**: The collection of qualifying groups available for later user selection. Adding a candidate does not initiate evaluation.

**Evaluation batch**: The explicitly selected collection of groups handed over by the user for evaluation. Its size is not fixed by the evaluation module.
_Avoid_: Automatically evaluated candidate stream

**Requirement Specification**: Human-reviewed obligations derived independently from the original request. It is distinct from a planner's interpretation of that request.

**Evaluation snapshot**: Preserved independent external evidence used consistently to assess the submitted itineraries. It is an evidence basis, not absolute real-world truth.

## Requirement and schedule units

**Submitted place claim**: The scheduled place identified by the output's structured
place fields, independently checked against external evidence. A descriptive title does
not need to be synonymous with that name; the claim does not itself establish factual identity.

**Transport association**: The source-linked relation between a submitted journey and
a directed pair of scheduled visit occurrences. It does not establish route feasibility.

**Obligation check**: One outcome for one independently reviewed requirement, with
all of its explicit count, date and time conditions retained as components.

**Schedule commitment**: One distinct scheduled visit, journey or fixed activity whose
occupied time is assessed independently; uncertain timing does not erase the commitment.

**Daily density deduction**: A reviewed ordinary/relaxed/rich pace policy applied to
source-distinct primary visit counts on every requested date. Explicit matching daily
numbers override defaults. This deduction adjusts the overall score while preserving
the original five-dimensional auxiliary score; [the score contract](contracts/0005-quality-human-review.md#daily-density)
owns numeric penalties, review provenance and uncertainty rules.

**Protected blocker**: A reviewed interval restricting specified kinds of scheduled
commitments. Overlapping protections can share a blocked span while remaining separate
user obligations.

**Potential match**: A source-preserved occurrence whose unresolved role or identity
could affect a reviewed place obligation; it is not a confirmed visit to that place.


## Route evaluation concepts

**Route candidate leg**: A directed connection between consecutive scheduled primary
visit occurrences on one delivered day. It remains inventoried when route evidence is
missing or applicability is uncertain.

**Submitted departure**: The departure claimed by the itinerary's authoritative
transport representation. It is distinct from the departure used for an evidence query.

**Query departure**: The departure recorded in the independent route request; omission
is a distinct time basis rather than proof that the submitted departure was queried.

**Continuous travel interval**: One uninterrupted available span for a candidate journey.
Separate spans around an occupied commitment do not form one longer interval.

**Route cap**: An adopted per-mode provider duration or distance threshold. It is
separate from the available time between scheduled commitments.

**Hard route deadline**: An applicable non-travel protection or guaranteed fixed
occupation boundary that permits no schedule grace, including the DRIVE reserve.

**Decisive route verdict**: A combined outcome established by all required PASS components
or any independently proven FAIL. A partial decisive FAIL does not establish complete
component evidence; missing components remain separately visible.

## V3 before/after concepts

**V3 stage pair**: The selected V3 run's pre-repair draft and final primary itinerary,
evaluated independently under one compatible frozen snapshot. The draft is a V3 stage,
not an independently executed V2 itinerary.

**Paired dimension mask**: The common included score dimensions for a V3 stage pair;
a dimension is omitted only when neither stage has applicable or unresolved units.
It is separate from the four-version final report's mask.

**Edit provenance**: Source-linked evidence of transformations actually adopted between
V3 stages, including retained activity IDs and parent/fragment relations. It describes
editing history without establishing independent quality or venue identity.

**Occurrence correspondence**: A validated relation between activities in the two V3
stages, established first through edit provenance and then through source-content or
reviewed evidence where needed. Edit continuity is distinct from venue continuity.

**Correspondence review**: Source-linked human verification of an ambiguous or complex
cross-stage relation remaining after provenance validation and content fallback. Complexity
alone does not require review when validated sources establish the relation; independent
quality checks determine compliance.

## Blinded ranking concepts

**Anonymous plan label**: A public A/B/C/D identifier whose plan association remains
fixed across the three ranking dimensions within one assessment task.

**Private label mapping**: The researcher-only association between anonymous labels
and selected source versions, retained outside the rater package and answer export.

**Display preparation**: Researcher review of prospective anonymous content, including
source-linked removal of identity/provenance identifiers while preserving travel facts
and uncertainty. It is separate from the rater's assessment.

**Tie group**: A set of plan labels judged equally for one dimension. Ordered tie
groups in a submitted ranking partition all four labels exactly once.

**Unable-to-judge response**: A whole-dimension response indicating insufficient basis
to rank the plans. It does not mean the plans are tied or that the dimension is inapplicable.

**Not-applicable response**: A whole-dimension response indicating that the dimension
does not apply to this task. It does not supply an ordering.

**Effective answer revision**: The highest valid complete submitted revision for one
task/rater. Earlier revisions remain audit records; drafts are not effective answers.

**Inferred display arrival**: A separately labelled clock time computed from supplied
departure and duration when the itinerary omits arrival. It is not a submitted arrival
claim, independent evidence or an input to quality scoring.

**Hidden duplicate task**: A repeated source group presented under an independent
anonymous assignment, used for within-rater consistency and excluded from main counts.

**Comparable pair**: A version pair with a ranked outcome in both an original task and
its hidden duplicate for the same dimension. No comparable pairs means consistency
is unavailable, not perfect agreement.
