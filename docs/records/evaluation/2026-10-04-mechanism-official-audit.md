# Ticket 12 mechanism and official-evidence audit — 2026-10-04

Status: Implemented, offline validated and fixed-base dual-axis review completed.
Source contract: [mechanism/audit](../../contracts/0001-evaluation-artifacts.md#mechanism-official-audit)
and [executable wire](../../contracts/0001-evaluation-artifacts.md#mechanism-audit-executable-wire).
Tracker: [Ticket 12 / #24](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24).

The user approved the complete concrete scope before implementation. Starting fixed point
was `21986f542cd5ec72ec519709c5882477c80c7413`, with a clean tracked worktree/index.
Implementation and direct tests were committed before review:
`8e945fd45b1b0e26ec55a71e748e13f8ccf8660d`
(`feat: add mechanism reports and opt-in official evidence audit`). No branch switch,
push, Issue mutation, PR, merge, live run, formal audit or version freeze was authorized.

## Delivered behavior

Preparation reuses the four-version batch or saved genuine V3-only Ticket 11 sources.
Exact result bytes and original input/run identity are verified; optional channels retain
local material diagnostics. Repair trigger is nonempty original authorized scope. Original
versus related targets, attempts, rounds, components and internal progress have separate
units. Cumulative parent summaries and matching trace copies are not added to child counts.
Missing metadata/denominators remain null, with observed cells and coverage retained.

Default-off caller-owned capture observes Gate-accepted claim catalogs, exact primary/Repair
structured projections, actual default-adapter submission, and actual V3 opening-rule
selections. Recording adds no prompt/schema/provider/budget changes. Injected unobserved
clients remain partial. Returns, failed calls and cancellations retain their original
behavior. Capacity and secret-bearing observations produce partial diagnostics; sink
failure logs its error type without replacing planning.

Audit units bind exact accepted source/claim revisions and all qualifying occurrences.
Preparation-only, rejected/search-only and accepted-unused claims do not qualify.
Independent human reviews bind exact queue/unit hashes and preserve reviewer, time,
rationale, supporting sources and unavailable verdicts. Observed qualifying units and
review/verifiable coverage remain visible when the complete population is unknown.
Independent Ticket 10/11 outcomes and usage remain separate attachments; internal Repair
acceptance is not an independently verified resolution or truth score.

## Validation sequence

1. Public capture, report, audit and CLI slices first failed with absent implementation
   modules, then passed after implementation. Subsequent boundary checks cover real runner/
   adapter prompts and call counts, result/adoption parity, usage-off rule selection,
   budget aborts, failure/cancellation, exact hashes, duplicate/conflicting identities,
   related targets, pending components and review missingness.
2. One real-graph fixture failed because empty preference input correctly skipped
   interpretation while the fixture queued an extra response. The explicit intended
   request corrected the fixture. Budget abort uses actual `input_tokens` and the named
   resource error. Retest passed. A rule-selection fixture initially used the historical
   `official:` alias; using actual Gate `official_web:` identity corrected the fixture.
3. Focused evaluator/observability/official integration/multiround/V3 validation/default
   adapter regression: **978 passed, 1 skipped**. Later dedicated Ticket 12 gate:
   **40 passed**. Full backend gate: **2477 passed, 10 skipped** in 318.11 seconds.
   Skips are existing environment/opt-in cases, not missing newly required acceptance tests.
4. Ruff and compile checks passed. Format initially found mixed line endings in three
   hook files; the formatter corrected them and all fourteen intended Python files passed.
   No configured/installed mypy or pyright was available; no type-check result is claimed.

These are synthetic/offline development checks. They do not establish provider receipt,
model attention, causal influence, real capture overhead, a formal truth rate, corpus
coverage or version ranking. Official rule observation is scoped to actual V3 operating/
opening selections, not verified admission or whole-trip affordability. Existing trace
fragments cannot establish complete historical denominators.

## Dual-axis review and corrections

The code-review skill used two independent read-only agents on
`21986f5...8e945fd`, reviewing the committed implementation against repository standards
and the originating fixed-point accepted contract. Standards: **0 findings**.
Spec: **2 P2 findings**, both report integrity/missingness errors:

- Matching trace rounds only compared status, accepting contradictory continuation,
  cumulative counters or usage. The fix compares these shared source fields while preserving
  valid saved-result mechanism counts and marking only the trace channel invalid.
- Truncated capture counted a catalog claim without its lost qualifying occurrence as
  accepted-unused. The fix leaves confirmed unused/population counts unavailable for
  partial capture and retains explicitly named observed counts/catalog remainder.

Four regression cases first failed (three trace cells and one real bounded-capture
producer/consumer flow), then passed after correction. The combined affected report/audit
test selection passed **29 tests**. The evaluator-wide correction gate passed
**640 tests, 1 skipped**, in 100.09 seconds. Fix commit:
`877dc89` (`fix: preserve trace integrity and partial audit uncertainty`). The earlier
full backend gate is not being described as validation of this later report-only correction.
No runtime hooks, planner budgets, prompts or score wires changed in the correction.

Committed correction recheck completed on both axes: Standards **0 new findings**;
Spec **both findings closed, no new concrete findings**. The Spec reviewer independently
reran the four new regression cases and all passed. Final contract/package/PROJECT and
record-index updates preserve the distinction between the full implementation gate and
the later evaluator-wide correction gate. No further implementation issue is outstanding
within this approved scope. Real capture overhead, live/formal execution, publication,
tracker synchronization and any version freeze remain outside this acceptance.

## Engineering publication and tracker closeout — 2026-10-04

After local preflight, the user explicitly authorized a normal push of the current
feature/evaluation branch, publication verification, acceptance updates and completed
closure of #22-#24, then parent #12. The worktree/index were clean at the starting
delivery revision `bab0d5315f9a6dcaecb8327c1017bfe94269f2c1`.

The push advanced the remote from `fc9996803b05b9b444583f0985274bee75c4ed0f`
through all 56 prepared local commits, including Tickets 05-12, related corrections
and documentation migration. Remote branch identity and exact Git blob parity for
seven linked contract/acceptance/navigation files were verified before Issue updates.
No force push, rebase, squash, PR, merge or branch change occurred.

The live Issue bodies/comments were refreshed and matched the preflight source
snapshots. Active acceptance checklists and current summaries were updated while
preserving original wording, unrelated content and imported historical checklists.
Obsolete readiness labels were removed; existing classification labels remain.
Each saved body, acceptance comment, label change and completed closure was re-read:

- [Ticket 10 / #22 acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22#issuecomment-5973113398).
- [Ticket 11 / #23 acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23#issuecomment-5973121380).
- [Ticket 12 / #24 acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24#issuecomment-5973124658).
- [Parent #12 acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12#issuecomment-5973135724),
  published only after all #13-#24 child states were verified closed/completed.

Preflight documentation checks passed for 58 Markdown files and 499 local tracked
links/anchors, with zero errors. Four historical/reachable Ticket 10 revision pairs
have identical Git trees, preserving the meaning of prior validation and review.
Eight prepared Issue drafts preserved unrelated source content; their 24 intended
published file links were checked locally before actual publication verification.
The final PROJECT/tracker/record corrections form a separate documentation closeout.
Existing code test and dual-axis review results above were reused; no new code suite,
live provider/model/database call, formal case/audit, comparison, analysis or freeze
was performed. Engineering plan closure does not establish a formal research result.

The GitHub CLI token was invalid, so Issue operations used the connected GitHub tools.
Sandboxed SSH initially could not read known_hosts and surfaced host-key failure;
an authorized read-only check outside the sandbox succeeded and matched both verified
branch tips. Normal push used that available connection. No credentials, host keys,
Git/SSH configuration or provider budgets were changed.

## Pre-implementation inspection and approved scope

Historical event: 2026-10-04. The sections below were relocated from the current artifact
contract during the 2026-10-04 design-consistency audit at revision
`16cf98ca91fb1c6daac60bbe84c52202dc10e21d` (initial worktree clean; documentation edits
uncommitted during relocation). They preserve the original inspection, setup failure/retest
and approval sequence. Preflight gaps, future-tense delivery names and Issue status describe
their stated checkpoints; they are not current implementation or tracker claims.
The source contract retains its old anchors and links here. Current technical rules remain
in that contract, and the later validation/publication sections above retain their own scope.

**Status: implemented, offline validated and fixed-base review completed.**
After the read-only preflight, the user accepted reuse of existing records plus the
minimum opt-in local capture on 2026-10-04. This accepts the observation units,
denominators, audit linkage and delivery scope below; it does not activate capture or
authorize implementation, live collection, formal audit execution, publication or Issue
mutation by itself. The user subsequently approved the complete implementation scope below.
At preflight inspection, Issue #24 was open/needs-info; tracker synchronization
remains separate. Missing optional artifacts must not invalidate independent quality
material. Inspection checkpoint: `7c9783bdeb1b57b7fe6fdfc258dec47cc5c3dcf7`.

#### Preflight interfaces and gaps before implementation

| Required observation | Current source | Technical conclusion |
| --- | --- | --- |
| Initial findings, improvement targets and authorized scope | `V3Outcome.original_report` and `scope` in [V3 state](../../../backend/app/versions/v3/state.py) | Complete saved outcomes already support mechanism-only trigger/authorization observations. Internal findings do not establish independent truth. |
| Rounds, model attempts, components, target links, adoption and stopping | `RepairResult.rounds`, `RepairRoundRecord.target_links`, per-round result and continuation reason in [repair models](../../../backend/app/versions/v3/repair_models.py) | Use the real records. The top-level result is a cumulative summary, not an additional round. |
| Accepted official claims and resolved representations | `OfficialWebIntegrationResult.accepted_evidence`, [official planner projection](../../../backend/app/versions/v1/official_planner.py), `EffectiveFact.source_refs` | Typed claims and provenance exist in memory; the ordinary final result does not preserve a complete official-claim catalog. |
| Primary model evidence | `official_planner_evidence_prepared` and the primary generation code in [V1 graph](../../../backend/app/versions/v1/graph.py) | Preparation precedes input-budget checks and model invocation. Prepared evidence alone does not prove input submission. Raw request capture is optional. V2/V3 share this primary graph. |
| Repair model evidence | `effective_evidence` and selected hours in [repair input](../../../backend/app/versions/v3/repair_projection.py), followed by [repair invocation](../../../backend/app/versions/v3/repair_service.py) | The actual projection exists, but ordinary mechanism traces chiefly retain sizing/fingerprints rather than a complete per-call official-fact submission record. |
| Rule-selected operating evidence | `Finding.adopted_evidence.selected_hours` and evidence refs from [opening assessment](../../../backend/app/evidence/opening_hours.py) | Selected evidence can be traced where complete validation reports survive. All effective evidence in context, or conditions merely reported as unverified, are not automatically rule-used facts. |
| Trace and resource availability | [run tracer](../../../backend/app/observability/run_trace.py), [usage capture](../../../backend/app/observability/usage_capture.py) and [usage report](../../../backend/evaluation/usage_report.py) | Tracing is best-effort and may be disabled/truncated. Numeric usage already has run/result linkage and missingness; no duplicate resource collector is needed. |

The observed gap is capture provenance, not missing itinerary/transport correspondence
or a need to rerun validation. The accepted reader design consumes saved observations; it must
not replay a rule and label newly reconstructed evidence as historically used.

## Preflight validation and approval

Existing offline interface checks passed 77 tests across official integration, multiround
Repair, tracing, budget summaries and usage reporting. The initial run had 63 passes and
14 setup errors because the task-local temporary parent directory had not been created;
after directory setup, the same test selection passed. No production/test source changed,
new Ticket 12 implementation fixture, live service or formal audit was executed.
The user selected the minimum capture extension together with the readers/reports,
rather than a saved-material-only delivery. No specification decision remains pending
from that preflight. Its next gate was explicit implementation-scope approval under
AGENTS.md. The user then approved that scope; actual implementation/validation is
recorded below. The earlier design approval alone did not authorize execution.

#### Implementation approval proposal — 2026-10-04

**Status: approved by the user and implemented on 2026-10-04.** The accepted design above
is the specification. The prepared scope at `21986f5` was explicitly approved in this
conversation before implementation. Preparation checkpoint: `8acb361`; Issue #24 and
its comment were reread without mutation. Approval includes implementation, offline
validation, local commits, dual-axis review, in-scope corrections and documentation.

| Delivery | Expected implementation location | Included behavior |
| --- | --- | --- |
| Selected-source preparation and mechanism report | New `backend/evaluation/mechanism_preparation.py`, `mechanism_report.py` and narrowly needed schema/helpers | Read explicitly selected saved results and optional linked observations; report trigger/authorization, original and related targets, rounds, model attempts, component adoption and internal progress with separate units/coverage. |
| Official audit queue and reviewed report | New `backend/evaluation/official_audit.py` and narrowly needed schema/helpers | Join accepted claims to actual submission/rule-selection occurrences; preserve claim/source revisions, exclusions and missingness; import independently supplied exact-unit reviews and emit descriptive audit coverage/verdicts. |
| Researcher commands | New `backend/evaluation/mechanism_cli.py` | Prepare selected sources, emit mechanism report, export audit queue and build reviewed audit report. Commands read local artifacts and emit versioned JSON; they do not invoke planners or acquire sources. |
| Opt-in local capture | New `backend/app/observability/mechanism_capture.py` with a small internal observation helper if needed | Caller-owned async attempt wrapper with original-input/run identity, exact result serializer and local sink, independent of enabled usage/tracing; default-disabled recording and explicit partial/unavailable coverage. |
| Minimal shared hooks | Existing `backend/app/versions/v1/graph.py`, `backend/app/versions/v3/repair_service.py`, `backend/app/llm/azure_foundry/client.py` and the V3 assessment/selected-hours seam | Register the accepted official catalog and exact structured projections; observe actual primary/Repair invocation and actual selected official operating/hour evidence. Hooks do not change evidence, prompts, schemas, permissions or budgets. |
| Public-seam verification and documentation | `backend/tests/evaluation/`, `backend/tests/observability/`, relevant existing version/LLM tests; current contracts/package/PROJECT and dated acceptance under `docs/records/evaluation/` | Offline TDD and regressions, local implementation/test commits, fixed-base Standards/Spec review, separate review corrections and final acceptance. |

The capture interface is an explicit producer wrapper around an existing runner, analogous
to the existing usage attempt wrapper. It accepts invocation, linkage, serializer and sink;
no new always-on runtime feature, YAML budget/configuration, planning API field or altered
V0-V3 entry script is required. An enabled wrapper receives bounded normalized observations;
its sink work follows invocation/result serialization. Failed writes, serialization failure,
capacity truncation, cancellation and failed calls preserve the planner return/exception
and retain recording coverage where possible. Capture failures never replace planning errors.

Observation covers the existing default primary/Repair model adapter and actual V3 official
operating/hour rule selections. A prepared projection is not qualified until the invocation
seam observes submission. Arbitrary injected clients without that observation do not inherit
claimed complete coverage. Rule records come from the actual assessment and selected refs,
including their precise activity/date/representation; neither replayed validation nor all
effective evidence in context supplies historical rule-use proof. No generic rule engine,
all-adapter discovery system or new fact extractor is included.

Preparation supports the delivered four-version selection and actual selected V3-only
sources already available through Ticket 11 preparation, with the existing source/hash
contracts reused. It never invents V0-V2 results or reruns controlled cases. Optional source
references supply capture, current recognized trace records, existing usage and independent
Ticket 10/11 reports. Missing optional channels stay unavailable; complete saved V3 outcomes
can support mechanism observations without a capture. Only explicitly surviving trace
cells are read, with no generic historical-log reconstruction. Exact duplicates deduplicate;
conflicting identities and foreign/stale hashes are material diagnostics in that channel.
Quality/identity readers and Ticket 08/10/11 score wires remain unchanged.

Planned artifact families: `rtpeval_mechanism_capture_1`,
`rtpeval_mechanism_preparation_1`, `rtpeval_mechanism_report_1`,
`rtpeval_official_audit_queue_1`, `rtpeval_official_audit_reviews_1` and
`rtpeval_official_audit_report_1`. Their detailed fields follow the accepted units/linkage
and are implemented at public seams; internal helper names/grouping may follow the code's
natural responsibilities without changing this scope. No raw prompt/provider-body dump
is required. Source-bound claim excerpts remain local observation material, not Git assets.

The offline acceptance tests must cover:

- Real unchanged prompts, model/provider call counts, itinerary/results and policy/budget
  settings with capture off/on; recording failure/cancellation and independent usage-off
  operation; no observed official fact submission on an input-budget abort.
- Original versus round-local/related targets, skipped/rejected/partial/complete adoption,
  cumulative summary exclusion, duplicate/conflicting round records and missing trace.
- Rejected, accepted-unused and preparation-only claims excluded from the qualifying set;
  exposed-only, rule-selected-only and both-qualified claims; repeat occurrences counted
  once per exact audit unit with occurrence links retained.
- Exact input/result/source/review hashes, date/subject/representation linkage, absent and
  foreign reviews, contradictory material, unavailable verdicts and review coverage.
- Separate usage attachment without summing per-round and cumulative tokens; independently
  linked outcomes remain separate from internal success and cannot change quality/identity.
- Public CLI workflow through preparation/report/queue/reviewed report using synthetic
  artifacts only; four-version and genuine V3-only selection; existing evaluator regressions.

Run focused TDD checks, relevant evaluator/official/LLM/V3/observability regressions, Ruff,
format/compile checks, documentation link checks and one full relevant backend gate for the
shared hooks. Use an existing configured type checker if available; do not install tooling
or claim a missing type-check result. Record the implementation starting commit as the review
base, commit implementation/direct tests before the two review axes, and preserve separate
fix and final-documentation commits under AGENTS.md.

This proposal includes no live execution, extra model/provider calls, model token/budget
increase, formal case construction/audit/rates/comparison, automatic website checks, frontend,
new provider/database infrastructure, unrelated refactor, version freeze, branch switch,
push, PR, merge or Issue mutation. Local capture introduces bounded serialization/storage
work; its actual overhead is not yet measured. Full Ticket 12 implementation, relevant
validation/review corrections and documentation are the single approved scope.
