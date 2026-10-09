# Intake Identity Usage

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="rtpeval-ticket-01-02-review"></a>

<a id="rtpeval-ticket-01-02-review--tickets-01-and-02-follow-up-review"></a>

## Tickets 01 and 02 follow-up review

Date: 2026-09-30.
Base: `364f91f05f01328266bfb00c5b75885242d93d7d`.
Scope: existing uncommitted Ticket 01/02 code, shared adapter changes, contracts and offline tests. Ticket 03 was excluded. User requested review only; implementation and tests were not edited.

<a id="rtpeval-ticket-01-02-review--standards"></a>

### Standards

Zero actionable findings. No explicit repository standard violation or concrete maintenance issue was identified in this review. Shared adapter instrumentation remains opt-in; prompts, budgets and planner decisions were not changed by the reviewed diff. This does not override the Spec findings below.

<a id="rtpeval-ticket-01-02-review--spec"></a>

### Spec

1. **P1 - Missing selected-run provenance/full-input validation.** `backend/evaluation/intake.py:288`. Artifact contract requires each selected run's provenance reference and complete input hash linkage. Intake validates RequirementSpec-to-input and usage-to-result, but never reads run provenance. A synthetic fixture with valid-hash provenance files declaring wrong input hash, wrong run and wrong version is still accepted; omitted provenance is also accepted. Group membership and completion attestation do not validate the provenance that is actually supplied. Require and validate the selected-run full-input association without rerunning planners. The implementation README's optional-provenance wording does not establish an approved relaxation of this requirement.
2. **P2 - Overlapping/equal-time visits lack required ambiguity diagnostics.** `backend/evaluation/projection.py:176-205`. Contract says equal/overlapping times remain conflicts/ambiguities. Two visits at 09:00-10:00 and 09:30-11:30 are accepted with `adjacency_status=ordered_candidates` and a negative gap (10:00 to 09:30); no overlap diagnostic is emitted. Equal-start visits are likewise ordered using tie-breakers without recording the ambiguity. Preserve sources/candidate pairs but expose the conflict instead of claiming unambiguous chronology.
3. **P2 - Unknown Repair tokens become zero.** `backend/evaluation/usage_report.py:71-80`. Contract requires missing token observations to remain unavailable. An actual offline `capture_attempt` with one Repair SDK call returning no usage produces null whole-run/observed token totals, but `repair_token_observed_subtotal=0`. No Repair token value was observed. Emit null when none of the Repair events have known usage, retaining partial subtotal semantics when some are observed.
4. **P2 - Missing event collections are reported as zero.** `backend/evaluation/usage_report.py:20-40`. With available/default-adapter coverage but absent model/provider/cache arrays, the report defaults them to empty lists and emits zero calls/tokens/sends/cache hits. The contract requires missing observations to remain unavailable. Validate required collections before calculating complete totals.
5. **P2 - Duplicate cache events are counted twice.** `backend/evaluation/usage_report.py:21-24,40`. Two cache-hit rows with the same event ID yield cache_hits=2 because only model/provider collections are checked for duplicate IDs. The contract explicitly rejects duplicate event IDs rather than double weighting. Include cache event identities in validation.

<a id="rtpeval-ticket-01-02-review--verification"></a>

### Verification

- Root reran `.venv/Scripts/python.exe -m pytest backend/tests/evaluation backend/tests/observability/test_usage_capture.py -q -rs`: **91 passed, 1 skipped**. Includes existing Ticket 03 tests; counts are not exclusive Ticket 01/02 coverage.
- Standards reviewer independently reran the capture suite: **13 passed**; these overlap with the above count.
- Additional synthetic temporary-artifact probes exercised real `load_batch` for provenance and chronology; a fixture SDK call inside real `capture_attempt` reproduced Repair missingness. Direct report probes demonstrated missing-array zero and duplicate cache counting. Probe outputs were inspected in-session, with no persistent raw logs.
- No correction or corrective retest was performed. Existing tests passing does not cover these counterexamples. Earlier acceptance records remain historical and their no-remaining-findings conclusions are qualified by this review.
- No real provider/model/database call, formal benchmark/experiment, commit/push or planner behavior change occurred. Existing workspace changes were preserved.

Final counts: Standards 0; Spec 5 (one P1, four P2). Recommended next step: correct these boundaries with offline regression tests before dependent evaluation work.


<a id="rtpeval-ticket-01-02-review--correction-disposition---2026-09-30"></a>

### Correction disposition - 2026-09-30

The user authorized all five fixes; they are now implemented and validated offline. Twenty-two regression cases cover the failure-before/fix-after sequence. Final evaluation/capture suite: **113 passed, 1 skipped** (existing Windows symlink privilege limit); Ruff check, format check and git diff whitespace check passed.

Standards follow-up: zero actionable findings. Spec follow-up initially found that overlap uncertainty also blocked independently reviewed transport endpoint binding. A failing public-intake regression was added, then corrected by restricting the adjacency filter to automatic positional matching. Final Spec review reports zero remaining findings, with an independent targeted rerun of nine provenance/overlap tests (overlapping coverage, not additional totals).

See ticket-01-acceptance.md and ticket-02-acceptance.md for the detailed sequence. Original findings above describe the pre-correction implementation and are no longer outstanding. No planner/capture adapter behavior changes, real services, formal benchmark/experiment, commit/push or freeze occurred. New provenance wire and conservative chronology/missingness rules are documented in the active contracts and package guide.

<a id="rtpeval-ticket-01-03-acceptance"></a>

<a id="rtpeval-ticket-01-03-acceptance--tickets-0103-ordinary-output-implementation-acceptance"></a>

## Tickets 01/03 ordinary-output implementation acceptance

Date: 2026-10-03, Australia/Sydney. Specification accepted 2026-10-02.
Review fixed point: e1b89ae38958c6ea573e50cb555e697d738a7964 on feature/evaluation.
The starting working tree was clean. The user approved offline implementation of the
[specification](../../contracts/0002-intake-identity-usage.md#rtpeval-ticket-01-03-simplification), tests, local commits, dual-axis review,
necessary corrections and related documentation. No live run or publication is authorized.

<a id="rtpeval-ticket-01-03-acceptance--scope-and-behavior"></a>

### Scope and behavior

V0 explicit transport endpoints can associate with a uniquely containing same-day
occurrence gap. Direction, complete normalized endpoint labels, supported title/notes
clauses and chronology must agree. Repeated labels do not alone require review.
V1-V3 retain directed application-transfer references and existing source authority.

Structured place/role claims survive ordinary descriptive titles, including Walking tour
of Museum A. Bounded explicit visit/list/movement conflicts remain reviewable. No general
semantic model, title-equivalence whitelist or new LLM invocation is introduced.

The independent snapshot identity bridge retains optional address_components from raw
addressComponents. Typed locality supports combined city/state/postcode formatting;
street components support output locations, and complete agreeing typed street addresses
can reconcile search/details format differences. Conflicts and malformed components retain
diagnostics. Missing components use legacy fallback; no request or backfill is added.

Projection policy and identity association policy are recorded separately from immutable
source references. Existing source IDs remain stable. Older derived identity reports
require offline replay; snapshot raw bytes are not rewritten. Branch competition,
high-impact review and predeclared audit selection remain active.

<a id="rtpeval-ticket-01-03-acceptance--development-validation-sequence"></a>

### Development validation sequence

1. Initial pytest setup failed because the default system temporary directory was
   inaccessible. Task-local temporary directories enabled the actual regression loop.
2. Explicit V0 endpoint tests failed twice, then passed after bounded association.
3. Walking-tour role reproduction failed, then all three descriptive-role cases passed.
4. Six name-only/supplied-ID descriptive-title cases failed, then the identity file
   passed 47 tests after removing blanket title-equivalence gating.
5. Combined locality formatting failed, then passed with typed locality evidence.
   Four search/details/location cases failed, then the identity file passed 52 tests.
6. Snapshot bridge tests failed for available/malformed components; raw component
   forwarding fixed them. One test incorrectly expected a null success reason instead
   of the existing strict_association reason; its expectation was corrected.
7. A stale-policy report was initially accepted; the regression passed after policy
   validation. A structured street contradiction also reproduced a false acceptance;
   typed street precedence fixed it, with 53 identity tests passing at that checkpoint.
8. An old review-replay fixture used endpoint wording now automatically supported.
   It was changed to unsupported between wording to continue testing manual replay.
   Direction, competing notes, complete labels, repeated occurrences, wrong locality,
   malformed components and snapshot-policy rejection received further regressions.
9. Evaluation suite: 500 passed, 1 skipped in 73.72 seconds. Ruff passed. The skip is
   the existing Windows symlink privilege case. Network guards remained enabled.

Full backend gate: 2329 passed, 10 skipped in 210.52 seconds. Skips: nine opt-in
PostgreSQL cases and one Windows symlink privilege case. No cases were deselected.
Implementation commit: 898b3bc (fix: accept structural evaluation claims and typed addresses),
created after validation and before Standards/Spec review. The specification's earlier eight probes remain development history,
not extra passing tests or a formal benchmark. No external API, model or database result
is inferred from offline fixtures.

<a id="rtpeval-ticket-01-03-acceptance--dual-axis-review-and-correction"></a>

### Dual-axis review and correction

Standards: no explicit project-standard violation. Two maintainability suggestions identified
duplicated normalization and endpoint-marker detection; both now use shared helpers.

Spec: two P2 findings. Conflict recognizers dropped parsed claims from public audit output;
formatted-address fallback could also accept an output city contradicting typed locality.
Public-boundary regressions reproduced both: 10 failed, 4 passed (eight failures were
existing parametrized title cases extended with parsed-evidence assertions). The correction
retains source, field, original and parsed claim in projection/identity output and the
identity review queue. Typed locality prevents unsupported legacy location fallback.
Missing street components with available locality can therefore require review.

After correction: relevant intake/identity tests 124 passed, 1 skipped; complete evaluator
regression 502 passed, 1 skipped in 55.34 seconds. Ruff and diff whitespace checks passed.
The earlier full backend result remains the pre-review gate; the correction was confined
to evaluator code and validated with its complete suite, not another full backend run.
Correction commit: b32e997 (fix: preserve conflict evidence and typed locality precedence).
Both independent review axes rechecked this commit and closed all four findings/suggestions;
neither reported a remaining concrete issue. No commits were amended or squashed.

Current-state documentation and the historical research archive were updated after review.
Documentation validation checks English content, relative Markdown targets and whitespace.
All nine documentation/archive files and 221 local targets passed these checks.
An initial multi-file documentation patch was rejected for an unmatched heading; inspection
confirmed no partial change, and a corrected patch succeeded before final validation.

<a id="rtpeval-ticket-01-03-acceptance--operational-boundary"></a>

### Operational boundary

No planner runtime, prompt, budget, provider field mask or production API changed.
The evaluator still has no built-in operational Google acquisition client. Future authorized
acquisition can request address components within an already required name/address request;
this implementation only consumes supplied independent evidence. Old missing evidence is
not automatically enriched. Geographic aliases, unsupported prose and incomplete addresses
retain documented review/coverage limits.

Live Issues #13 and #15 and their comments were read before implementation. They describe
the earlier completed scopes. This local extension does not mutate their state/comments,
push code, create a PR, freeze a version or start Ticket 10.

<a id="rtpeval-ticket-01-03-simplification"></a>

<a id="rtpeval-ticket-01-03-simplification--tickets-0103-structural-claims-and-ordinary-output-compatibility"></a>

## Tickets 01/03: structural claims and ordinary-output compatibility

Current status, 2026-10-03: subsequently approved, implemented and validated offline;
see [implementation acceptance](intake-identity-usage.md#rtpeval-ticket-01-03-acceptance). The approval boundary below
records the original specification-only checkpoint.

Date: 2026-10-02, Australia/Sydney.
Status: User decisions accepted; specification revision only. Implementation requires
separate approval. Inspected revision: 186fd2488f3c196e4898ab6e2c8d341e6aeeaeb3;
the working tree was clean before this documentation task.

<a id="rtpeval-ticket-01-03-simplification--authority-and-scope"></a>

### Authority and scope

[PROJECT](../../../PROJECT.md) owns project status. This revision specializes the
[projection contract](../../contracts/0002-intake-identity-usage.md#rtpeval-intake-projection-contract) and
[identity contract](../../contracts/0002-intake-identity-usage.md#rtpeval-identity-implementation-contract). Earlier acceptance records
describe the implemented conservative rules, not implementation of this revision.
GitHub Tickets 01/03 remain their existing work records; no Issue state, body or comment
is changed by this local documentation task.

The user approved specification and acceptance revision after the Tickets 01-09 audit.
The user then accepted structural fields as the primary identity/role claims because
interpreting arbitrary title semantics is unreliable, and accepted a narrow independent
address-component extension with no additional requests or automatic old-data backfill.
No planner, evaluator code, fixture, live acquisition or formal evaluation is authorized
by this specification approval. Ticket 10 implementation remains separately authorized
work; the Ticket 04-to-07 coordinate bridge remains a candidate outside this revision.

<a id="rtpeval-ticket-01-03-simplification--observed-facts-and-limits"></a>

### Observed facts and limits

- V0 prompts require origin/destination/mode in transport title or notes. The current
  projector instead excludes endpoint prose from automatic positional association.
- V1-V3 output validation checks supplied IDs and normalizes place_name from the candidate
  ledger. It does not normalize title or guarantee agreement between all free-text fields.
- The projector currently treats main_poi titles beginning with walking as role conflicts.
  Identity accepts separate titles automatically only as the name or Visit plus the name.
- Identity currently uses exact comma/semicolon address components and complete formatted
  address equality. The snapshot identity bridge and identity candidate reader omit typed
  address components. Raw snapshots can retain them, but their presence is not guaranteed.
- The original request destination is free text, not a canonical city or geographic boundary.

Source seams: backend/app/versions/v0/prompts.py, backend/app/policies/itinerary_output.py,
backend/evaluation/projection.py, backend/evaluation/identity.py,
backend/evaluation/snapshot.py and backend/app/schemas/request.py.

The preceding audit ran eight synthetic function probes without changing files: four
title cases passed the product output validator; plain Visit Museum A passed strict
identity association, Morning at Museum A required identity review, Walking tour of
Museum A required role and identity review, and Visit Different Museum required identity
review. Two address variants differed only in address representation and produced strict
association versus destination_unverified. Two V0 transport variants produced one bound
claim for Walking versus one unbound claim for Walking from Museum A to Museum B despite
one candidate gap. These are development reproductions, not full planner runs or measured
production frequencies. No corrected behavior has been executed.

<a id="rtpeval-ticket-01-03-simplification--1-v0-occurrence-association"></a>

### 1. V0 occurrence association

Use existing day, interval, activity occurrence and explicit endpoint claims before
requesting review. A supported explicit directed phrase such as Walking from Museum A
to Museum B may associate automatically when its normalized names identify the scheduled
endpoints and exactly one same-day candidate gap fully contains the transport interval.
Require resolved chronology and no conflicting endpoint claim in the supported title/notes
fields. A model-estimate disclaimer does not negate a movement mode.

Comparison uses NFC, case folding and whitespace normalization, retaining source pointers.
The bounded endpoint recognizer must match complete scheduled labels, not substrings,
provider IDs invented from prose, or approximate venue names. It does not interpret
arbitrary narrative. Unsupported endpoint syntax keeps the existing review route.
The implementation must publish its finite supported syntax and cover it through the
public projection boundary. No LLM extraction is introduced.

Repeated venue labels alone do not force review if the complete interval and endpoint
conditions select exactly one occurrence pair. Multiple surviving pairs, reversed or
contradictory endpoints, overlaps, an intervening unresolved visit or invalid clocks retain
review/uncertainty. Do not pick the nearest pair or replace an explicit conflicting endpoint
with a convenient positional match. Existing independently reviewed endpoints can still
establish association despite a separate timing conflict.

V1-V3 continue to associate application transfers by directed activity IDs. Association
identifies the submitted journey; independent identity and route evidence determine its
factual endpoints and feasibility. Source selection, occupancy units and scoring stay intact.

<a id="rtpeval-ticket-01-03-simplification--2-structural-role-and-place-claims"></a>

### 2. Structural role and place claims

For an explicitly declared main_poi with a usable place_name, those fields define the
submitted visit and place claim. source_place_id remains a claimed identity subject to
independent evidence. Ordinary title wording does not independently veto either claim.
Morning at Museum A, Walking tour of Museum A and A relaxing morning therefore need no
title-equivalence review when the structural visit is Museum A.

Retain original title/notes for display and audit. Do not build an expanding whitelist of
acceptable descriptive titles or attempt to prove every title semantically equivalent to
the place name. Automatic structural interpretation is not certification that all prose
is accurate. This deliberately accepts incomplete detection of implicit prose conflicts.

Keep review for contradictory structural declarations and concretely recognized competing
claims: for example main_poi Museum A paired with an explicit Visit Museum B claim or a
supported directed movement from Museum A to Museum B. Recognizers must expose the exact
source and parsed competing claim, rather than flagging a movement keyword alone. An
independently supplied review can record other semantic contradictions. No general entity
recognizer or multilingual semantic classifier is promised.

Without usable place_name, the existing name-only/title evidence path remains available;
the revision does not manufacture a place from generic prose. Ambiguous structured roles,
multi-POI blocks and genuine identity conflicts retain their existing handling. Apply the
same output-field interpretation across versions, without importing a planner verdict or
candidate ledger as independent factual proof. Independent details/search, branch checks,
high-impact review and the predeclared audit sample remain required as applicable.

<a id="rtpeval-ticket-01-03-simplification--3-independent-structured-address-evidence"></a>

### 3. Independent structured address evidence

Extend only the evaluator's independent observation bridge/candidate representation to
retain typed address components when present in linked independent responses. Preserve
original formatted address, component types/text and observation hashes. The existing
planner DTO/cache is not the independent source. This is a required narrow future interface
change, not a capability already present in Ticket 03 or the snapshot bridge.

For a city destination such as Sydney, an independently returned locality component with
the same normalized name can establish the city association even when formattedAddress
contains Sydney NSW 2000 as one segment. Match components by type, never array position.
Country/state/postcode/street occurrences of the same word do not substitute for locality.
Explicit destination qualifiers must also agree; unsupported composite wording, aliases
and metropolitan-area interpretations remain reviewable rather than silently simplified.

Apply the new evidence consistently at all three affected checks: destination association,
output location association and search/details address agreement. A street location can
match the independently supplied street-number/route component combination, including
provider-supplied short forms. Generic locality agreement cannot activate the existing
numbered-street branch-search shortcut.

For search/details with the same ID and compatible name, differing formatted strings may
be equivalent when their complete usable typed address evidence agrees. Require agreement
on street number, route, locality and country for this street-address path; administrative
and postal components, when present, must agree on both sides as well. Missing or conflicting
components do not prove equivalence. Different street numbers, routes or localities retain
review even if the ID is equal. This narrow path does not promise normalization of every
address type; exact legacy address agreement remains usable when components are absent.

No substring-only city test, inferred geocoding, silent alias translation or fabricated
component is allowed. Missing components retain the existing strict fallback or review.
Do not rewrite old snapshots. Malformed supplied components must be diagnosed rather than
silently converted to favorable evidence. New rule/observation revisions must participate
in report and review linkage: replay old evidence under the selected new rules, reject stale
derived reports, and preserve historical acceptance records without new network requests.

<a id="rtpeval-ticket-01-03-simplification--4-accepted-cost-boundary"></a>

### 4. Accepted cost boundary

There is no new request, retry, reverse-geocoding call or LLM call for this extension.
Future authorized independent acquisition may add addressComponents to an already required
Places request that retrieves displayName/formattedAddress. Missing fields or old snapshots
never trigger automatic follow-up acquisition. Planner budgets and field masks are outside
this specification change. Local payload storage/parsing increases slightly; no size or
latency measurement is claimed.

Official documentation checked 2026-10-02: addressComponents is Place Details Essentials
and Text Search Pro; displayName is Place Details Pro and Text Search Pro. Requests are
billed at their highest requested SKU. Thus adding this field to the described existing
requests does not raise their SKU under the checked policy. Future live integration must
verify its actual field mask and the then-current policy; this is not a blanket statement
that a separate request or an IDs-only query upgrade is free.

Sources: [Place data fields](https://developers.google.com/maps/documentation/places/web-service/data-fields),
[billing rules](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing),
and [address component wire](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places#AddressComponent).
Public documentation reads made no authenticated Places calls.

<a id="rtpeval-ticket-01-03-simplification--5-acceptance-examples-for-later-implementation"></a>

### 5. Acceptance examples for later implementation

Automatic in this table means eligible without the removed ambiguity trigger; independent
identity requirements and audit/high-impact review can still apply.

| Input and evidence | Required result |
| --- | --- |
| V0 A ends 10:00, Walking from A to B occupies 10:00-10:20, B starts 10:30; one matching gap | Associate with that directed occurrence pair; retain estimated mode/time claims. |
| The same names occur later but only one gap contains this transport interval | Select the unique occurrence pair; no name-only ambiguity. |
| Transport explicitly says B to A while the available gap is A to B | Review; no positional override. |
| Several candidate pairs remain or chronology is unresolved | Review/uncertainty; no favorable selection. |
| main_poi Museum A with Morning at Museum A, Walking tour of Museum A or A relaxing morning | Keep primary visit and Museum A claim; no keyword/title-whitelist rejection. |
| Museum A fields with a concretely recognized Visit Museum B or A-to-B movement claim | Retain an explicit conflict and review its interpretation. |
| Generic text with no usable structured place | Preserve existing role/name-only handling; no invented identity. |
| Sydney destination; formatted city segment Sydney NSW 2000; independent locality Sydney | Accept city association, subject to the remaining identity checks. |
| Melbourne locality and Sydney Road street | Do not accept Sydney destination. |
| Same ID/name and equal complete typed street address, differently formatted search/details strings | Accept address equivalence without rewriting originals. |
| Same ID but conflicting street number or locality | Review; ID equality cannot erase the conflict. |
| Old snapshot lacks address components | Exact legacy fallback or review; zero automatic backfill requests. |

Later TDD must cover public intake/projection and snapshot-to-identity replay, including
the new ordinary-output cases and the retained conflicting cases. Verify source pointers,
rule/evidence revisions, stale-review rejection, V0/V1-V3 source selection, unchanged
branch/audit requirements and downstream requirement/opening/route/report regressions.
Use synthetic offline evidence and a network guard; request-plan counts and model-call
counts must not increase because of this feature. Test old snapshots without backfill.

The future implementation scope is projection.py, identity.py, the narrow snapshot identity
bridge and affected replay-policy validation, directly related tests and documentation.
No planner behavior change or new operational provider client is proposed. Record a starting
commit, run TDD, commit implementation/tests before Standards and Spec review, then commit
any review fixes and final acceptance documents under the repository Git policy.

<a id="rtpeval-ticket-01-03-simplification--documentation-validation"></a>

### Documentation validation

This record captures accepted decisions and future acceptance criteria. The current task
runs English-content, local Markdown target and diff checks only. Implementation test
results, production coverage and corrected-output claims must be added only after the
separately authorized implementation occurs.

Completed checks: nine documentation/archive files, 213 local Markdown targets, zero
English-content or missing-target errors; diff whitespace checks passed. Inspection found
and removed duplicated introductory notes left by a partial patch application, and applied
the missing package-guide notice before validation. No source or test file changed.

<a id="rtpeval-ticket-01-03-simplification--subsequent-implementation-approval-and-checkpoint"></a>

### Subsequent implementation approval and checkpoint

The user subsequently approved the bounded offline implementation. The earlier specification-
only statements preserve the original authorization checkpoint. [Implementation acceptance](intake-identity-usage.md#rtpeval-ticket-01-03-acceptance)
records TDD, actual regressions, commits, review and remaining limits. Runtime planner changes,
extra acquisition, backfill, formal work, publication and Ticket 10 remain outside this approval.

<a id="rtpeval-ticket-01-acceptance"></a>

<a id="rtpeval-ticket-01-acceptance--ticket-01-offline-acceptance"></a>

## Ticket 01 offline acceptance

Date: 2026-09-29.
Base revision: 364f91f05f01328266bfb00c5b75885242d93d7d.
Working tree: earlier specification-closure edits plus new independent evaluation package/tests; uncommitted. The user approved Ticket 01 implementation and offline acceptance only.
Status: Implemented and validated offline within stated limitations. Not benchmark/version frozen.

<a id="rtpeval-ticket-01-acceptance--delivered-behavior"></a>

### Delivered behavior

- Immutable, source-linked batch inventory from a user-curated manifest and separate per-version files.
- Fatal integrity/linkage/wire errors return needs_material_correction with no partial cohort. Date/content uncertainty remains diagnostic; no live planning-date validation or workflow requalification.
- Independent activity roles, review replay and within-day candidate adjacency. No canonical ID truth claim.
- Structured Transfer and text-based transport claims coexist; confirmed duplicates share occupancy, segments are retained, contradictions remain alternatives, and missing arrivals are not synthesized.
- Allowlisted quality data excludes planner requirements, RAG origin, route verdicts and V3 findings. Optional V3 projections and unavailable usage are explicitly tracked.
- Read-only local CLI and Python API; package guide documents envelope vocabulary and review preparation.

<a id="rtpeval-ticket-01-acceptance--verification-sequence"></a>

### Verification sequence

1. Initial test collection failed due to an unclosed bracket in the new test file; corrected before execution. Ruff reported formatting/line-length issues and two zip strictness findings; formatting and explicit strict=False resolved them. An intermediate edit used the Windows default GBK reader and failed on UTF-8 source; explicit UTF-8 resolved that tooling issue.
2. Initial behavior suite passed 20 tests. Review added structural, numeric, source-quote, stale-review, day-boundary, role uncertainty and filesystem-boundary cases.
3. Code review found that a general negation filter would mistake 'not live verified' for mode negation. Restricted negation to mode statements, added regression coverage, and restricted automatic positional binding for rich endpoint prose.
4. Final evaluation suite: **38 passed, 1 skipped**. The skipped real symlink test requires host privileges unavailable here. Literal traversal and a simulated resolved-link escape test pass; native link/junction behavior is not claimed validated by that simulation.
5. Ruff check and format check pass; CLI --help succeeds. Document/link and diff checks are run at closeout. No shared application code changed, so the unrelated planner suite was not rerun.

Tests use synthetic local temporary artifacts, with network guards. An import-boundary check restricts this package to standard-library and relative imports. Finding-mutation testing compares semantic projections while permitting correct artifact-hash/source-ID changes. This is not a formal experiment or proof of future provider coverage.

<a id="rtpeval-ticket-01-acceptance--remaining-limits"></a>

### Remaining limits

- Rich/ambiguous natural-language roles/endpoints require independent review; no model-based classifier is implemented.
- Timezone resolution, canonical resolution, oracle acquisition, metric scoring, usage collection, renderer and Repair reporting belong to subsequent tickets.
- Intake checks RequirementSpec structure/provenance and basic referential integrity; full obligation operator semantics belong to Ticket 05.
- No actual benchmark package, live API/model/database call, native junction test, thesis analysis, Git commit or version freeze occurred.

<a id="rtpeval-ticket-01-acceptance--references"></a>

### References

- [Implementation guide](../../../backend/evaluation/README.md)
- [Ticket](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/13)
- [Contract](../../contracts/0002-intake-identity-usage.md#rtpeval-intake-projection-contract)
- [Tests](../../../backend/tests/evaluation/test_intake.py)


<a id="rtpeval-ticket-01-acceptance--authorized-follow-up-corrections---2026-09-30"></a>

### Authorized follow-up corrections - 2026-09-30

The later review found full-input provenance and overlapping-visit gaps in the earlier implementation. The user authorized correction; previous acceptance remains historical. Selected runs now require `rtpeval_provenance_1` with exact group/run/version/full-input/result association, using the existing file hash/path/schema reader. Its hash is retained in inventory. Overlapping/equal-start visits retain source records and candidate legs but produce explicit diagnostics and unresolved affected adjacency.

TDD sequence: all six missing/mismatched provenance cases initially failed, then passed after validation and explicit fixture sidecars were added. Existing evaluation suite then passed 84 tests with one skip. Both overlapping-time cases initially failed, then passed after projection correction. No planner validation or chronology repair was added. Final combined evaluation/capture suite: **113 passed, 1 skipped**; the skip remains native Windows symlink privileges. Ruff check/format check pass. Final review disposition is recorded in ticket-01-02-review.md. No live calls, benchmark/experiment, commit/push or freeze. Legacy synthetic/material deliveries missing provenance need an explicit producer sidecar; this is not an automatic attestation of actual execution.

Follow-up Spec review caught an interaction: the new unresolved adjacency also excluded explicitly reviewed transport endpoints. A public intake regression first failed with no associated claim; filtering was moved to automatic positional matching only. The regression then passed, preserving unique reviewed association alongside unresolved chronology. The final 113-test pass above includes this correction.

<a id="rtpeval-ticket-02-acceptance"></a>

<a id="rtpeval-ticket-02-acceptance--ticket-02-implementation-and-offline-acceptance"></a>

## Ticket 02 implementation and offline acceptance

Date: 2026-09-29.
Base revision: 364f91f05f01328266bfb00c5b75885242d93d7d.
Working-tree context: uncommitted Ticket 01 code/specification and Ticket 02 observation hooks, report, tests and documentation. No commit was created.
Status: Implemented and validated offline. Not benchmark frozen or formally evaluated.

<a id="rtpeval-ticket-02-acceptance--scope-and-implementation"></a>

### Scope and implementation

The user authorized closure through implementation/testing without repeated approvals, except unresolved consequential decisions. No such new scoring decision was needed. The [contract](../../contracts/0002-intake-identity-usage.md#rtpeval-usage-capture-contract) fixes the invocation/cleanup clock, provider-reported versus derived/missing usage, actual dispatch-attempt versus billing distinction, cache reuse versus lookup, Repair subsets and research-report semantics.

- [Capture guide](../../../backend/app/observability/USAGE.md): benchmark-owned opt-in invocation with caller-owned sink and exact-byte serializer.
- [Neutral event ledger](../../../backend/app/observability/usage.py): request-local model/provider/cache/stage observations; scoped HTTP hook installation/removal supports concurrent shared clients.
- [Attempt capture](../../../backend/app/observability/usage_capture.py): LangChain callbacks, failure/cancellation/cleanup preservation, result linkage and explicit coverage declarations.
- [Resource report](../../../backend/evaluation/usage_report.py): selected four-version groups, per-request differences/ratios and descriptive medians with availability counts. Single-attempt summaries remain usable by the upstream attempt ledger.

Shared adapters expose observation seams for Foundry structured/semantic/nomination/Repair, direct official search/reasoning, retrieval embedding, JSON/page HTTP, cache and existing stage wrappers. Prompts, models, budgets, retries and planning decisions were not changed. V3 final resource cleanup occurs inside the producer's selected invocation; the returned result is not rewritten. The quality scorer/reader does not run planners.

<a id="rtpeval-ticket-02-acceptance--actual-verification-sequence"></a>

### Actual verification sequence

1. Initial capture suite: 10 tests passed. Targeted existing paths plus evaluation: 139 passed, one pre-existing Ticket 01 native symlink test skipped.
2. Initial broad relevant regression: 4 failed, 937 passed, 1 skipped. All four failures were existing requirement-harness assertions that client HTTP hooks must be empty after cleanup. No failing assertion established a changed itinerary result.
3. Corrected ownership: inactive capture installs no hooks; active capture attaches lazily and removes only its own callbacks. Shared clients retain hooks until all concurrent capture owners finish. Added concurrency/cleanup regression coverage rather than weakening existing tests.
4. Focused cleanup/requirement-harness retest: 37 passed. Further usage tests cover explicit retry after SDK failure and coexistence with existing usage callbacks. Final capture suite: 13 passed.
5. Repeated broad relevant regression: **944 passed, 1 skipped** across observability/runtime, Foundry, integrations, retrieval runtime, planner runtime, V0-V3 and evaluation. Duration about 103 seconds. During this run, a resource-report-only guard was tightened for four-version membership/unavailable envelopes; the latest targeted usage/evaluation rerun passed **51 tests, 1 skipped**, covering that final change.
6. Ruff passed on all changed Python paths; usage-report CLI help succeeded. Final whitespace and document-link checks are recorded at closeout. Test counts overlap and must not be added as independent evidence.

The skipped test is the Ticket 01 native Windows symlink creation check: host privileges do not allow creating it. Literal traversal and simulated resolved-link escape coverage pass. No real provider/model/database calls or formal benchmark executions were performed; mocks and synthetic local artifacts exercise actual callback and transport seams.

<a id="rtpeval-ticket-02-acceptance--review-findings-and-corrections"></a>

### Review findings and corrections

Local Standards/Spec review checked observation-only integration, callback noninterference, scoped cleanup, failure and cancellation propagation, distinct source/missingness labels, no prompt/URL/credential retention, and request-level comparisons. HTTP hooks are not physical-delivery or billing proof. Cleanup failure does not replace a primary failure/cancellation; usage sink failure leaves the planner result intact and appears on the supplied ledger diagnostics.

No-record does not imply zero: unverified adapters yield observed subtotals and unavailable complete counts. Failed model calls without returned usage prevent a complete token total. Zero baselines give no ratio. Namespace/outcome/timing mismatch blocks the applicable comparison. Comparison groups require four usage envelopes; availability inside envelopes can still be partial/unavailable. No efficiency score or quality-score contribution is introduced.

<a id="rtpeval-ticket-02-acceptance--remaining-limits-and-next-boundary"></a>

### Remaining limits and next boundary

- Capture must be explicitly enabled by benchmark producer invocation. Existing ordinary CLI runs do not automatically save usage. A producer must confirm artifact persistence and matching result bytes.
- default_adapters is a declared, checked integration configuration; arbitrary injected/new clients are not inferred covered. No live completeness claim was established here.
- Unobserved stages remain unattributed. Internal provider web-search actions and model reasoning are not reconstructed from HTTP counts. A request with no response retains incomplete outcome, not a guessed status.
- Stage latency is inclusive/non-additive. Cache lookups do not prove reused results or saved API requests. Observed route-matrix cardinality is not billable usage.
- Resource reporting is for researcher analysis and future thesis/presentation discussion, separate from blind human review and quality totals. No actual thesis analysis was performed.
- Ticket 03 identity closure remains a separate next task. No formal cases, shared checkpoint freeze, commit or push occurred.


<a id="rtpeval-ticket-02-acceptance--authorized-follow-up-corrections---2026-09-30"></a>

### Authorized follow-up corrections - 2026-09-30

The user authorized the three report-boundary corrections identified in the follow-up review. Available/partial usage requires explicit event arrays; unavailable envelopes may omit them. Repair tokens with no observed values now stay null, while observed zero and partial known subtotals are preserved. Cache duplicate event IDs are rejected like model/provider duplicates. Capture hooks and planner paths were not changed.

TDD sequence: six missing/null array cases failed before correction, then passed along with unavailable-envelope compatibility. Repair subtotal tests initially had one failure and two passes, then all three passed. Duplicate-event tests initially had one cache failure and two existing model/provider passes, then all three passed. Final combined evaluation/capture suite: **113 passed, 1 skipped** (the existing native Windows symlink privilege case). Ruff check/format check pass. These counts overlap Ticket 01 validation and include Ticket 03; do not add them as independent evidence. No need to rerun unrelated planner suites because this correction pass only changed evaluator readers/reporting and fixtures. Final review disposition is in ticket-01-02-review.md. No live service, formal benchmark/experiment, commit/push or freeze.

<a id="rtpeval-ticket-03-acceptance"></a>

<a id="rtpeval-ticket-03-acceptance--ticket-03-offline-implementation-and-acceptance"></a>

## Ticket 03 offline implementation and acceptance

Date: 2026-09-29.
Base revision: 364f91f05f01328266bfb00c5b75885242d93d7d.
Working tree: Tickets 01/02 and prior specification changes remain uncommitted; Ticket 03 adds only independent evaluation files, one Ticket 01 import-boundary test allowlist entry, and related documentation. No commit or push.
Status: Implemented and validated offline within the limits below. Not a formal benchmark, live evidence run or version freeze.

<a id="rtpeval-ticket-03-acceptance--delivered-behavior"></a>

### Delivered behavior

- Read accepted Ticket 01 visit/role/source projections and independently reviewed named requirement subjects without importing planner judgments.
- Apply the user-approved strict supplied-ID details and no-ID name-search association paths, with explicit city/address and observable competition checks. Provider rank and mere ID retrieval do not establish a match.
- Queue aliases, branches, wrong-city/malformed/missing evidence, ID/name conflicts and potential REQUIRED/EXCLUDED matches for factual adjudication. Keep unresolved reasons and avoid calling missing candidates hallucinations.
- Require a versioned, predeclared audit seed/count. Select strict automatic proposals deterministically by a semantic key; sampled references remain pending until reviewed. The queue hides version labels.
- Replay consecutive versioned review decisions bound to source/evidence hashes. A reviewed named venue can resolve for downstream identity while a wrong supplied ID remains an explicit conflict.
- Report each final and available V3 optional projection's applicable/resolved/unresolved visit counts, grounding fraction, claimed-ID consistency and unresolved-role count. No obligation/opening/route/auxiliary total is produced.
- Expose a Python API and read-only local CLI for offline replay. Input evidence/reviews remain separate files; result artifacts are never rewritten.

<a id="rtpeval-ticket-03-acceptance--verification-sequence"></a>

### Verification sequence

1. Initial identity suite found two test-fixture mistakes: the altered V1 result had not been saved back to the synthetic batch, making the supposed supplied ID absent. The fixture writer was corrected; no production identity rule changed for that failure.
2. Initial Ruff findings were import-fixture naming and formatting issues. The test fixture was shared through the existing pytest module plugin, and code was formatted.
3. The first combined evaluation suite found one failure in Ticket 01's standard-library import allowlist after Ticket 03 introduced `unicodedata`. The allowlist was updated; its network/import boundary was not relaxed.
4. Review tightened branch handling: supplied-ID details with only name/city and no specific output location now require an independent full-page name-search competition check. Added a direct details/branch fixture and retained the specific-address path.
5. Final offline evaluation suite: **58 passed, 1 skipped**. The skip is the existing Ticket 01 native Windows symlink creation test; host privileges prevent creating that link. Its traversal/resolved-path alternatives remain tested. Ruff check and format check pass on the evaluation package/tests; identity CLI help and fixture-driven no-network replay pass. `git diff --check` reports no whitespace errors.

The tests use synthetic files and observations only. They include name-only and supplied-ID acceptance, alias, branch, wrong city, malformed response, provider failure, wrong ID/right name, closed business, distinct colocated IDs, high-impact subjects, review revision/stale hash, audit determinism, V3-finding mutation and network blocking. The V3-only internal-finding file change alters source hashes as expected but leaves semantic audit keys and grounding summaries unchanged.

<a id="rtpeval-ticket-03-acceptance--review-and-limitations"></a>

### Review and limitations

Local Standards/Spec review checked source isolation, same V0-V3 policy, strict association, separate claimed-ID conflict, UNKNOWN propagation, pending audit behavior, review replay and no planner/network imports. No remaining finding required a code change after the final suite.

The evidence envelope is a Ticket 04 handoff; no acquisition client, provider budget, retry policy, cache or raw Google snapshot was implemented. Declaring an independent source in a fixture is not proof of real acquisition. A full-page response cannot prove global name uniqueness because the current adapter has no pagination/alias guarantee. Strict rules can leave real places unresolved. The module can replay a persisted reviewer JSON file but does not provide a reviewer UI or verify human factual accuracy. Benchmark preparation must prove the audit plan was frozen before result inspection. Formal cases, live services, scoring downstream of identity and V0-V3 behavior changes are outside this acceptance.

<a id="rtpeval-ticket-03-acceptance--references"></a>

### References

- [Implementation contract](../../contracts/0002-intake-identity-usage.md#rtpeval-identity-implementation-contract)
- [Ticket](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/15)
- [Package guide](../../../backend/evaluation/README.md)
- [Implementation](../../../backend/evaluation/identity.py)
- [Offline tests](../../../backend/tests/evaluation/test_identity.py)


<a id="rtpeval-ticket-03-acceptance--follow-up-corrections-and-revalidation--2026-09-30"></a>

### Follow-up corrections and revalidation — 2026-09-30

Status: The four findings in [follow-up review](intake-identity-usage.md#rtpeval-ticket-03-review) are corrected and validated offline. This supersedes the review's corrections-pending state while preserving both earlier records. Base remains `364f91f05f01328266bfb00c5b75885242d93d7d`; all work is uncommitted.

- Generic country/admin/postcode matches no longer activate the details-only branch shortcut. Only a matching recognized numbered street component can do so; unsupported forms need competition search or review.
- Search/details candidates with matching IDs but contradictory normalized names or full formatted addresses enter review.
- Separate title claims must equal the name or `Visit <name>` to pass automatically. Other prose enters adjudication rather than being interpreted as consistent. Original title now participates in the semantic audit key.
- Dictionary/list claimed IDs no longer raise during high-impact matching. The affected reference remains unresolved while unrelated valid records are reported normally.

Validation sequence used the public intake/resolver path, one defect at a time. Generic-location regressions initially failed in all three cases, then passed after correction (including the existing specific-street positive case). Search/details regressions initially failed in all three cases, then passed. Title tests initially had eight failures and four valid-title passes across V0-V3, then all twelve passed. Dictionary/list ID tests initially both raised TypeError, then both passed and retained six resolved unaffected visits with one audit-pending visit. These are 20 additional synthetic test cases, not a benchmark.

The combined suite passed **78 tests with 1 skip** before final formatting. Initial Ruff check reported eight long lines in the added tests; formatting corrected them. Final rerun: **78 passed, 1 skipped**, Ruff check and format check passed; `git diff --check` had no whitespace errors (only existing CRLF normalization warnings). The skip remains the Windows symlink privilege case. The evaluation suite includes offline CLI replay with network access blocked. Standards and Spec follow-up reviews each found zero actionable issues in these corrections.

Only evaluator code/tests and related records changed in this correction pass. Existing Ticket 01/02 work and V0-V3 planner paths remain intact. No real Google/model/database calls, formal cases/experiments, commit/push or freeze occurred. Conservative English street/title recognition and strict full-address equality can increase adjudication workload; they do not establish worldwide semantic parsing or live evidence coverage. Ticket 04 still requires separately authorized scope.

<a id="rtpeval-ticket-03-review"></a>

<a id="rtpeval-ticket-03-review--ticket-03-follow-up-implementation-review"></a>

## Ticket 03 follow-up implementation review

Date: 2026-09-30.
Base revision: `364f91f05f01328266bfb00c5b75885242d93d7d`.
Scope: uncommitted Ticket 03 implementation, tests and accepted identity contracts. Existing Ticket 01/02 changes were preserved. This was a review, not a correction pass.

<a id="rtpeval-ticket-03-review--findings"></a>

### Findings

<a id="rtpeval-ticket-03-review--standards-axis"></a>

#### Standards axis

No explicit repository coding-standard violation was found. One correctness issue was identified on this axis:

- **P1: Generic address components bypass branch checks** (`backend/evaluation/identity.py:298-302`). A supplied ID with `location="Country"`, destination `Example City`, and details address `10 Main St, Example City, Country` qualifies as a specific location. With no independent search, this bypasses competition checking. An accepted synthetic eight-reference batch produced seven `resolved` results and one sampled `audit_pending` result. A country/admin component does not establish a specific branch. Restrict this shortcut to sufficiently specific location evidence; otherwise require search or adjudication.

<a id="rtpeval-ticket-03-review--spec-axis"></a>

#### Spec axis

- **P1: Search/details contradictions are ignored** (`identity.py:314-318`). Details can match the claimed name/city while search returns the same ID with a different name and city. The code compares candidate IDs/counts but ignores those material contradictory fields. An accepted synthetic batch produced seven automatic resolutions and one audit-pending result. The implementation contract explicitly requires contradictory search evidence to block automatic acceptance.
- **P2: Material title/name contradictions are ignored** (`identity.py:101-105`). A reference titled `Visit National Aviation Museum` with `place_name="Museum A"` is evaluated exclusively as Museum A. Exact independent search evidence for Museum A produces automatic acceptance despite the different named venue in the title. The accepted synthetic batch produced seven automatic resolutions and one audit-pending result. Preserve ordinary descriptive titles, but route materially conflicting venue claims to review under the no-material-contradiction contract.
- **P2: Malformed claimed IDs can abort the batch** (`identity.py:266`). Intake accepts an optional `source_place_id` represented as a dictionary. With an unrelated requirement subject and non-overlapping observed candidate IDs, set membership raises `TypeError: unhashable type: 'dict'` before the malformed-ID guard runs. The CLI consequently reports a batch evidence-correction failure instead of reference-level uncertainty. Validate the optional ID before membership checks and retain per-reference handling.

<a id="rtpeval-ticket-03-review--evidence-and-limitations"></a>

### Evidence and limitations

- Re-ran `.venv/Scripts/python.exe -m pytest backend/tests/evaluation -q -rs`: **58 passed, 1 skipped**. The skip is the existing Windows symlink privilege case.
- Executed additional synthetic probes from stdin using temporary artifact files and the actual `load_batch`/identity resolver path. The four findings above are observed behavior, not inferred from code alone. Probe output was inspected in the review session; no persistent raw probe log was created.
- The passing suite does not cover these counterexamples. No fixes or corrective retests were performed in this review.
- No Google, model or database calls; no formal benchmark or experiment; no commit/push. No V0-V3 planner behavior was changed.
- The earlier acceptance record remains historical evidence of its stated checks. Its conclusion that no findings remained is superseded by this follow-up review. Correct these issues and add focused regression coverage before continuing downstream identity-dependent work.

Final actionable counts: Standards axis **1 correctness finding** (zero explicit coding-standard violations); Spec axis **3 findings**.


<a id="rtpeval-ticket-03-review--correction-disposition--2026-09-30"></a>

### Correction disposition — 2026-09-30

All four findings above were corrected after explicit user approval. Twenty new synthetic regression cases demonstrate the failure-before/fix-after sequence. Final evaluation suite: 78 passed, one existing Windows symlink skip; Ruff and format checks pass. Standards and Spec follow-up reviews each report zero actionable findings. See [acceptance follow-up](intake-identity-usage.md#rtpeval-ticket-03-acceptance) for the full sequence and conservative recognition limits. Original findings remain historical evidence, not outstanding defects.

<a id="rtpeval-ticket-04-acceptance"></a>

<a id="rtpeval-ticket-04-acceptance--ticket-04-offline-snapshot-acceptance"></a>

## Ticket 04 offline snapshot acceptance

Date: 2026-09-30. Base revision: `1eb441f` on `feature/evaluation`.
Working tree: Ticket 04 implementation/tests/contracts and documentation are uncommitted. Previously committed Tickets 01-03 are preserved; the only existing-test change adds asyncio to the standard-library import allowlist.
Status: Implemented and validated for the approved injected-transport/offline scope. Not live-ready Google integration, formal evaluation, benchmark freeze or version freeze.

<a id="rtpeval-ticket-04-acceptance--delivered"></a>

### Delivered

- Two-stage request planning: independent Search/Details observations feed Ticket 03; source-checked adopted identities feed canonical details union and explicit route-context plans.
- Deduplicate identical request descriptors while retaining every original reference and candidate leg. Optional available V3 draft/final_primary is included when paired is requested; missing optional projections, unresolved identities and missing route contexts remain explicit.
- Route requests preserve direction, identities, coordinates/evidence hashes, mode, departure basis and routing options. Only necessary one-cell matrices are requested; Ticket 07 still owns departure/applicability choices.
- Acquisition uses an injected async transport, explicit send/attempt/time bounds, safe transport-failure categories and bounded retry. Raw response bytes, hashes, request/retrieval times and every failed attempt remain stored. The oracle ledger is separate from planner usage.
- Fresh directories only; manifest published last. Replay checks request coverage, plan/hash linkage, safe paths, response hashes, derived summaries, ledger and UTC time order. It does not acquire data or recompute scoring verdicts.
- Offline CLI prepares plans, replays snapshots and exports identity evidence. No live acquisition command/client, credential loading or database dependency is installed.

<a id="rtpeval-ticket-04-acceptance--actual-validation-sequence"></a>

### Actual validation sequence

1. Implemented public seams one slice at a time. Initial plan/acquisition/bridge/union/CLI tests failed because the respective interfaces did not yet exist, then passed after each slice. Route-context test initially failed at the deliberately unsupported context boundary, then passed after explicit context validation/keying was implemented.
2. Retry regressions first failed for the absent typed-failure path; HTTP, timeout and transport retry/budget cases then passed. Permanent HTTP failures and malformed successful responses do not retry.
3. The first network guard also blocked Windows asyncio's local socket pair. The fixture was corrected to allow loopback socket construction while rejecting external socket connections. This was a test-harness issue, not a provider connection.
4. Corruption tests passed raw hash/path/coverage/summary cases but initially failed ledger and missing-attempt cases. Replay now recomputes ledger totals and validates unrequested-record states; all passed.
5. Parameter allowlisting regression initially failed because an extra authorization field could reach persistence. Operation-specific input fields and reference/operation linkage are now checked before directory creation/transport invocation. No credential value was real.
6. Initial combined evaluation run: 1 failed, 126 passed, 1 skipped. The failure was the existing import allowlist lacking asyncio. Added only that standard-library module, retaining the no-planner/no-network-client boundary.
7. Standards and Spec reviews both found the same P2: missing acquisition timestamps were accepted at replay and broke the identity bridge later. Four timestamp regressions (missing, naive, reversed, outside collection interval) failed first, then passed after UTC/time-order validation. Final reviewers report zero remaining actionable findings on their respective axes.
8. Further targeted coverage checks supplied-ID/name-only handoff, malformed optional location, stale identity source hashes, reverse legs, context distinctions, optional drafts, matrix precision/missing/duplicate elements and CLI error reporting. Final snapshot suite: **35 passed**.
9. Ruff initially found import ordering, line length and ambiguous short variables. Corrected imports/names and formatted files; final Ruff check/format check and compileall pass. No separate static typechecker is configured in pyproject.toml.
10. Final full backend suite: **1957 passed, 10 skipped in 83.84 seconds**. Nine database integration tests remain opt-in and were skipped; one native Windows symlink test lacks privileges. The interim evaluation/capture suite of 145 passed / one skip and reviewer targeted runs overlap this final result and must not be added as independent evidence. CLI help and git diff whitespace checks pass.

<a id="rtpeval-ticket-04-acceptance--limits-and-next-step"></a>

### Limits and next step

Evidence is synthetic and temporary. No actual Google/model/database call, formal case, benchmark, experiment, commit/push or freeze occurred. The transport contract is executable but does not serialize live Google requests; provider applicability and storage/retention settings require a separately authorized operational integration. Request timeout/send limits are development engineering defaults, not an approved live budget.

The declared independent coordinate/source context must be prepared and reviewed externally; hashes and source links establish consistency with supplied material, not factual authenticity. Planner-to-oracle lag is null because no reliable planner timestamps were supplied. Snapshot integrity is verified against its manifest and optional trusted plan; callers requiring external tamper evidence must retain a trusted manifest hash. A programming error or cancellation leaves an unpublished directory, not an automatically resumed snapshot. API/CLI successful replay does not imply complete evidence or a quality PASS.

Recommended next step: inspect Ticket 05's supported obligation/time-operator boundaries, or separately scope a live transport integration if explicitly desired. Ticket 06 can consume frozen raw opening evidence once its implementation is authorized. No dependent ticket starts automatically.

<a id="rtpeval-transport-correction-acceptance"></a>

<a id="rtpeval-transport-correction-acceptance--transport-responsibility-correction-acceptance"></a>

## Transport responsibility correction acceptance

Date: 2026-09-30. Base commit: 1eb441f47cb0de65eb1c687eb56a45dba286aa86.
Branch: feature/evaluation. Existing uncommitted Ticket 04 work preserved.
Status: Implemented and validated offline; not frozen.

<a id="rtpeval-transport-correction-acceptance--scope"></a>

### Scope

- V0 retains its explicit model-estimated transport instructions and DTO.
- V1-V3 share a primary DTO excluding transport and output acceptance rejecting declared model transport before route binding. Initial and Repair prompts prohibit transport authoring; the shared policy no longer advertises the forbidden transport role. Application route selection, budgets and transfer construction are unchanged.
- V3 Repair retains its existing operation-only patch permissions; transport role/mode injection is rejected.
- Evaluator final and optional V3 projections select activities for V0 and transfers for V1-V3. Ignored-source records and diagnostics retain provenance without occupancy/fallback. Repeated actual journeys stay occurrence-specific.
- Ticket 05 metrics and protected-time union implementation remain pending.

<a id="rtpeval-transport-correction-acceptance--verification-history"></a>

### Verification history

Acceptance and DTO tests first failed on the missing version boundary, then passed after implementation. Six evaluator cases reproduced use of the forbidden activity source. They now pass with explicit version selection. Existing duplicate/conflict tests now compare authoritative transfers with each other. DTO construction fixtures were updated to the primary day schema; cost behavior is unchanged. A new optional-projection test initially used the wrong result nesting and was corrected to run.optional.

Related combined tests: 190 passed, 1 skipped. Intake/mixed Routes/V0 prompt checks after occurrence coverage: 78 passed, 1 skipped.

Standards review: zero findings. Spec review identified a P2 contradiction in the appended shared role vocabulary. A failing composed-prompt regression reproduced it; removing that shared transport suggestion while retaining V0's explicit instruction fixed it. V0/V1/shared-policy retest: 22 passed. Spec follow-up: zero remaining findings. Ruff and compilation passed; no static typechecker is configured.

First full-suite attempt stalled without reporting a failure around the retrieval tests and was interrupted. Exact test/cause was not established from a stack. The runtime retrieval file passed separately (16 tests). A final full rerun enabled faulthandler timeout diagnostics.

<a id="rtpeval-transport-correction-acceptance--limitations"></a>

### Limitations

All checks use local artifacts or fake dependencies, with no real Google/model/database calls or formal experiments. Declared forbidden transport fails generation without an extra retry. Prompt instructions cannot establish comprehensive detection of transport prose hidden under another role; evaluator ambiguity remains reviewable. Independent evidence remains necessary to assess factual route feasibility. No commit, push, benchmark or freeze.


The next full run completed with 5 failed, 1968 passed and 10 skipped in 83.54s. All five failures were old V3 fixtures expecting declared model transport to pass output acceptance into schedule/semantic/coverage validation. Updated those cases to assert the newly required rejection at the shared boundary, retaining non-transport assertions. The four affected files passed 119 tests; Spec follow-up found no remaining issue. The application rejects this invalid generated input, whereas independent evaluation can still intake historical delivered outputs and preserve/ignore their transport source records. A final full run verifies these updated expectations.


Final full backend regression: **1973 passed, 10 skipped in 85.49s**. The ten skips are nine opt-in database cases and the existing native Windows symlink privilege case. Ruff, compilation and diff whitespace checks passed. Standards and Spec have zero remaining actionable findings. No live service was called, no files were staged or committed, and no version was frozen.

<a id="structured-role-title-correction-2026-10-04"></a>

## Structured role and title correction - 2026-10-04

Status: Implemented, validated offline and reviewed; not frozen.
Review fixed point: `300ee039b3e2a2116a0b21f93eb09c9da2ade126` on
`feature/evaluation`; the starting working tree was clean. The user requested avoiding
title-regex semantic overreach following the approved density-table work. This correction
is limited to evaluator role classification, relevant regressions and current contracts.

Observed failure: the movement recognizer accepts `Walk to Museum A and explore its
exhibitions`, interpreting all text after `to` as a destination. The old role classifier
then changed a declared `main_poi` into `unresolved`. This was reproduced with synthetic
intake fixtures; it is not an observed real-provider failure rate. The previously preserved
Seoul replay had no unresolved-role/possible-count cases in the four finals or V3 stages.

The classifier no longer uses movement/visit title patterns to veto declared roles.
Existing place/placeholder guards, independent role overrides, source preservation,
transport authority, explicit endpoint association and genuine date/role uncertainty remain.
Competing-title metadata and the separate factual identity checks are retained; establishing
a visit role does not establish that its venue is real or correctly identified. Projection
policy advances to `structural_claims_directed_occurrences_3`; immutable source-reference
version remains `rtpeval_projection_1`. Derived material affected by classification must be
replayed from preserved sources. The density table remains `rtpeval_daily_density_2`.

Validation sequence: the first pytest invocation could not access the default Windows
temporary/cache directories, before exercising assertions. Using a fresh ignored workspace
`--basetemp` and disabling pytest cache fixed the execution environment. The intake RED run
then reproduced four expected role assertion failures, with three existing cases passing.
Removing the veto made intake pass (70 passed, 1 skipped). Transport-title and four-version
quality/density regressions then passed (102 passed, 1 skipped), including known count 2,
possible count 0 and ordinary density penalty 0. The genuine unknown-role fixture still
keeps its denominator unavailable. Ruff initially detected mixed line endings introduced by
editing; formatting corrected them, and lint/format/whitespace checks passed.

The full backend suite passed: **2532 passed, 10 skipped in 322.19s**. Implementation
and directly related tests were committed before review as `9039466`
(`fix: preserve structured activity roles across title wording`).
Parallel Standards and Spec reviews of that commit against the recorded fixed point each
reported zero findings. No implementation correction commit was needed; current contract
and acceptance updates are committed separately after review.

Evidence identifiers: local test directories `artifacts/title-role-red`,
`artifacts/title-role-intake-green`, `artifacts/title-role-report-green` and
`artifacts/title-role-full`; these are ignored execution material, not published dependencies.
No original Seoul artifacts or report files were rewritten. No planner/provider/model run,
formal experiment, publication or version freeze is part of this correction.

The subsequent [Issue #53](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/53)
explicitly associates implementation `9039466` and documentation `55ab8fc` with the
broader free-text correction history. Their commits are preserved without rewriting.

<a id="free-text-scoring-corrections-2026-10-04"></a>

## Free-text scoring corrections - 2026-10-04

Status at the local acceptance checkpoint: Implemented, offline validated and reviewed;
publication was pending. The subsequent publication/replay section below owns closeout.
Specification and live task state:
[Issue #53](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/53).
Starting/review revision: `55ab8fc59243be4f4fb583fc7284dabeecb907a4`; the starting
tree was clean. The user authorized all four confirmed problems, local implementation,
tests, commits, review and documentation. Publication was separately limited to earlier
revisions through `300ee039`, delivered in PR #54; these corrections remain local.

### Reproduced behavior and correction

- Structured Museum A claims with agreeing independent evidence were blocked solely by
  benign `Visit Museum A in the morning`, gardens or walking titles. Identity title
  diagnostics no longer veto automatic proposals. Actual candidate/ID/name/address,
  destination, high-impact and predeclared audit gates remain.
- A `free_time` Coffee break became a possible visit, turning a known two-visit day
  into count bounds 2..3 and an unavailable ordinary penalty. Declared free time is
  non-POI regardless of title/place text; primary roles are no longer erased by generic
  placeholder titles. Independent occupancy review remains separate and can retain a
  named rest interval as a fixed commitment.
- Walking transport became mode UNKNOWN after unrelated conditional/bus notes. V0
  reads independent mode review or a bounded first-title-clause declaration; conflicting
  recognized title modes and unsupported/missing mode declarations stay unknown. Notes
  are preserved, not mined for mode keywords or narrative negation.
- A generic estimate note prevented otherwise supported transport binding. Remove that
  note whitelist and incidental endpoint-keyword veto. Complete supported endpoint
  declarations still require agreement, exact delivered labels, chronology and a unique
  containing same-day occurrence gap. Generic prose supplies no endpoint declaration;
  unsupported titles, genuine recognized conflicts and ambiguous gaps retain review.

Projection policy is `structural_claims_directed_occurrences_4`; identity association
policy is `structural_claims_typed_addresses_3`. Source-reference version stays
`rtpeval_projection_1`; wire shapes and `rtpeval_daily_density_2` remain unchanged.
Older identity/preparation reports require offline replay because the association
policy changed. Original evidence and historical reports are preserved.

### Development validation sequence

Public seams: batch intake, independent identity resolution, final quality report,
V3 paired report and occupancy preparation. Identity RED reproduced 20 failures with
4 controls passing; the full identity file then passed 69 tests. Role RED reproduced
7 failures with 1 control passing; related intake/report/occupancy checks then passed
120 tests with 1 skipped. Mode RED reproduced 6 failures with 3 controls passing;
its explicit-conflicting-title follow-up reproduced 1 failure and then passed all
10 mode cases. Binding RED reproduced 5 failures with 5 controls passing; the full
intake file then passed 93 tests with 1 skipped.

The integrated five-file run initially had 229 passing, 1 skipped and one test error:
the new occupancy assertion used `guaranteed_intervals` instead of the existing
serialized `intervals` field. Correcting only that test made the occupancy file pass
11 tests. Final/V3 checks cover title-invariant density, generic-note-invariant V0
scores and preserved independent rest occupancy. Ruff lint/format and whitespace
checks passed before the full backend run.

The complete backend suite passed: **2574 passed, 10 skipped in 255.42s** using
`python -m pytest backend/tests -q --basetemp artifacts/semantic-full-backend
-p no:cacheprovider --tb=short`. The same complete worktree was validated before
splitting its implementation and directly related tests into local commits:
`a694c21` (`fix: keep identity association independent of title prose (#53)`) and
`4e12ab4` (`fix: respect structured roles and explicit transport claims (#53)`).
Validation covers their combined code state, rather than a separate full-suite run
of the intermediate first commit. The committed review uses the starting revision
above through `4e12ab4df7e2e0fa33a3c72b7d7de21157885f22`.

The initial committed reviews reported Standards 0 findings and Spec 1 P2 finding:
`Walking; Estimated travel time` associated while `Walking ; Estimated travel time`
did not. The association path had not stripped the first title clause, unlike the mode
path. A public intake regression reproduced 1 failure with 1 control passing. Removing
clause boundary whitespace then passed the five-file suite (232 passed, 1 skipped,
23.52s). Ruff first reported mixed line endings introduced by editing; formatting
corrected them and lint/format/whitespace checks passed. The separate correction commit
is `62c7586` (`fix: normalize transport title clause spacing (#53)`); earlier commits
are preserved rather than amended. Standards and Spec independently rechecked the
correction, confirmed the P2 resolved and reported zero remaining findings over the
combined starting revision through `62c75867704107cc4193bf0980c59f4919686edd`.
The Spec reviewer also independently reproduced successful binding for both title
forms. The final full backend run after correction passed **2576 tests, 10 skipped
in 247.11s**, using the same command with
`--basetemp artifacts/semantic-review-full-backend`. No code changed after this run.
Ruff lint/format and committed/working diff whitespace checks passed. Final current
contracts, project status and this acceptance record are a separate documentation
commit after review. Local acceptance is complete; Issue #53 remains open only for
its separately authorized correction publication criterion. The historical
`main_poi` commits `9039466`/`55ab8fc` and all new correction commits remain excluded
from PR #54; no new live execution or planner/density changes were made.

Evidence identifiers are ignored local fixture directories `artifacts/semantic-*`
and the executed pytest results. No original Seoul sources or output reports were
rewritten or rerun. All observations here are synthetic implementation diagnostics,
not measured live failure frequencies or formal evaluation conclusions. These changes
add no LLM/provider calls, planner behavior, version freeze, or general semantic model.

<a id="prose-publication-and-seoul-replay-2026-10-05"></a>

## Prose publication and Seoul offline replay - 2026-10-05

Status: Published, merged and offline replay validated. This remains engineering
acceptance, not a formal benchmark, version freeze or research conclusion.

### Publication and review correction

The user authorized delivery of the seven local commits through `31f5137`, including
the preceding `main_poi` correction, followed by offline replay of existing Seoul
evidence. The clean `feature/evaluation` branch was pushed without rewriting history.
[PR #55](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/55) used exact base
`69197cdc5a99c96ab94e15fa8b9313b11b1127c9`. Independent Standards review found one
P2 documentation issue: PROJECT.md still described a 2477-pass gate as latest.
Spec found zero issues. Separate commit `96e4f6d` updated that current summary to
the actual final 2576-pass/10-skip result and linked this existing owner; both reviewers
rechecked through `96e4f6de4f67def4b3bb9110700a26a81b679491` with zero remaining
findings. Code was unchanged, so the existing full-suite/Ruff evidence was reused;
release whitespace checks passed. No CI checks or configured mypy/pyright gate exist.

The [review comment](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/55#issuecomment-5980448177)
was published and re-read before head-matched merge. Observed merge revision:
`a4b7ba361a1b24a5740cfb9eade300e68d8d15a4`. PR state MERGED and Issue #53 state
CLOSED were verified, with all nine criteria checked and a self-contained publication
acceptance appended. Local main was safely fast-forwarded without switching branches.
The earlier local-only statements in this record describe historical checkpoints.

### Offline replay and linkage corrections

Replay used delivered evaluator revision `96e4f6d` (the same backend code in the
merge above). The working tree remained clean through execution; only the ignored
replay helper and generated artifacts were created. Original input/results, independent
raw responses, context, predeclared audit, route/density reviews and historical agent
adjudications were retained. No new evidence, adjudication, model or provider call was made.

The new intake policy changes plan hashes. New snapshots were derived in separate
directories only after proving every original request, reference, leg and other plan
field unchanged: identity differed only in `intake_hash`; final/paired plans only in
`intake_hash` and `identity_report_hash`. Raw bytes, original collection times, attempts,
response status and ledgers were preserved; those ledgers describe historical sends.
Separate replay-provenance files record that new network sends are zero.

The first local helper attempt stopped at its evidence-equality assertion because
`observation_id` includes the derived snapshot hash. The corrected adapter proves
observations identical except that identifier, then rebinds the historical review
evidence hashes in new files; decisions, candidates, reviewer, rationale and original
review times remain unchanged, with an explicit old/new binding provenance. A second
attempt completed final quality but the paired report correctly rejected the stale
original edit provenance. Regenerating that preparation through the native `prepare`
entry point from original V3 result bytes and the new identity report fixed the linkage.
Neither attempt required evaluator code changes or rewriting original artifacts.

The final sequence rebuilt intake, identity evidence/report, final and paired route
preparations/plans/snapshot bindings, V3 edit provenance, final quality and V3 pair.
All applicable CLI results were complete. Two full offline passes produced identical
bytes for intake, identity report, both route preparations, edit provenance, quality
and pair. Socket/DNS access was forbidden with zero attempted calls. SHA-256 inventories
confirmed all 313 original source files and 5 earlier density-baseline files unchanged.

### Observed report differences and limits

| Scope | Before | After | Primary visits by day | Mean daily deduction |
| --- | ---: | ---: | --- | ---: |
| V0 final | Unavailable | Unavailable | 2, 2, 2, 2 | 0 |
| V1 final | 85 | 85 | 2, 1, 1, 1 | 15 |
| V2 final | 90 | 90 | 2, 2, 1, 1 | 10 |
| V3 final | 100 | 100 | 2, 2, 2, 2 | 0 |
| V3 draft | 95 | 95 | 2, 2, 2, 1 | 5 |
| V3 final-primary | 100 | 100 | 2, 2, 2, 2 | 0 |

The paired adjusted delta remains exactly 5 percentage points (1/20). Final V1-V3
auxiliary scores remain 100. All dimension populations/counts, daily density counts
and deductions, schedule measures and occupancy are unchanged. Substantive primary
metrics also compare equal after excluding only derived `observation_id`/`evidence_hash`
fields; identity resolution, adopted venue and reason records have zero differences.
Policy versions, source/preparation/snapshot hashes and observation references changed,
so report bytes differ from old reports; this is not new independent factual evidence.

Independent documentation review caught the draft table's last two day counts in
the wrong order. The native report and comparison were correct throughout; the
documentation and local readable summary were corrected to `2, 2, 2, 1`. Every
table row was then checked against the saved comparison. Scores/deductions were
unchanged and no evaluator replay or code correction was needed.

V0 still has 8 known commitments and 4 unresolved candidate commitments, leaving the
non-overlap denominator unavailable. Its four route occurrences retain unresolved
occupancy/mode, one also unresolved identity; grounding remains 7 PASS and 1 UNKNOWN.
The unchanged scores establish regression compatibility for this saved case only.
The preceding synthetic regressions exercise the four corrected failures; no live
frequency estimate, version ranking or claim that every itinerary fact is known follows.

Ignored local evidence identifiers: `artifacts/seoul-prose-replay/replay.py`,
`complete-first/`, `complete-repeat/`, `comparison.json`, `semantic-comparison.json`,
`acceptance.json` and `summary.md`. Failed first/second preparations remain separate
for historical diagnosis. Raw artifacts are not committed or required published assets.

<a id="v0-structured-transport-2026-10-05"></a>

## Structured V0 transport declarations - 2026-10-05

Status: Implemented, offline-validated and reviewed locally.
This is offline engineering validation, not a live result, formal comparison or freeze.
[Issue #57](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/57) owns the task.
Starting fixed point: `37eae16c59bf94ec2c130a80f9992ca3bab1cfe0`; final code revision:
`72ff58f5c197641fc358bdd533b8c18b8261edb8`. Implementation began from a clean
`feature/evaluation` branch. Tests initially ran against the combined uncommitted
implementation, then both implementation commits were reviewed. Only related tracked
documentation remained uncommitted when this record was written.

### Decision and observed behavior

The preceding Seoul replay preserved four V0 journeys with unresolved mode/association.
Their producer supplied prose without structured endpoints. Adding more title grammar
would not make that language reliable. The approved solution supplies declarations at
generation: a V0-only provider activity DTO mapped to optional shared Activity data.
Missing/null objects are omitted on shared serialization to retain historical/V1-V3
wire compatibility. The provider schemas for V1-V3 remain unchanged.

Public fixture tests observe directed ID binding independent of narrative titles/notes,
including contradictory prose. Null/unsupported modes remain unknown; self, reversed,
dangling, malformed, nonadjacent, cross-day, overlapping and invalid-clock associations
do not obtain a favorable legacy fallback. Independent mode and endpoint reviews override
their corresponding fields separately. Review identified an ambiguous sentence in the
Issue brief; the body and a clarification comment now distinguish automatic gap checks
from the accepted endpoint-review exception that can associate despite time conflict.
The conflict remains available to scoring; no implementation exception was added.

Report fixtures retain two primary visits and zero density penalty. Correct IDs and
clocks establish three non-overlap units even with mode null; route state then stays
UNKNOWN. Invalid IDs leave the non-overlap denominator unresolved. Supported WALK plus
independent synthetic route evidence passes the route check, while opening evidence
still has two UNKNOWN results. Declaration acceptance does not supply provider facts.
The [output contract](../../0003-itinerary-transport.md#transport-ownership) and
[intake contract](../../contracts/0002-intake-identity-usage.md#claims) own current rules.

### Failure, correction and retest sequence

Public seams were Activity/PlanningResult schema and wire output, Foundry generation
and mapping, mocked `run_v0`, batch intake and the frozen-evidence quality report.
Schema RED reproduced 3 failures with 8 controls passing, then all 11 passed. Provider
schema RED reproduced 1 failure with 9 controls passing; mapping/prompt RED reproduced
5 failures with 12 passing. Structured intake RED reproduced 27 failures with 104
passing and 1 skipped. The combined focused suite then passed 356 with 1 skipped.

A run using the default pytest temporary root produced 76 setup permission errors
with 149 tests passing. Fresh repository-local `--basetemp` directories and
`-p no:cacheprovider` resolved that environmental problem; the existing intake file
passed 95 tests with 1 skipped. A new report assertion initially assumed null mode
also made the occupancy denominator unavailable. Reading the existing occupancy
contract corrected that assertion: known endpoints/clocks and unknown mode are
separate. The three report cases then passed without changing any scoring rule.

The first full backend run had 2627 passing, 10 skipped and four failing fixtures:
two reused the now-V0 provider helper as V1 input without omitting `transport`; two
new V0 cases queued an interpretation response despite empty preferences, which
correctly skip interpretation. Correcting those fixtures passed the related 41 tests.
The second complete run passed **2631 tests, 10 skipped in 309.14s**. Ruff initially
reported long lines; wrapping and formatting resolved them, and lint/format/whitespace
checks passed before committing the combined validated code in two logical groups:

- `dc0d381` - `feat: declare V0 transport modes and activity endpoints (#57)`.
- `1bb6a3b` - `feat: project structured V0 transport claims (#57)`.

Both committed review axes reported zero implementation findings. An additional root
probe of `PlanningResult.model_json_schema(mode="serialization")` then found the
wrap serializer's `dict` return annotation replaced Activity's output schema with a
generic object lacking properties. A public regression reproduced 1 failure with
11 passing. Removing that annotation retained typed output properties, required fields
and the extra-field restriction, without changing serialized values. Schema/API checks
passed **85 tests in 4.92s**. The separate correction commit is `72ff58f` -
`fix: preserve activity serialization schema (#57)`; both axes rechecked the complete
fixed-point diff with zero remaining findings. Spec also independently passed its
54-case focused probe and the corrected 12-test schema file. No history was rewritten.

Final full backend command:

```powershell
uv run pytest backend/tests -q -p no:cacheprovider --basetemp artifacts/v0-transport-schema-final-backend --tb=short
```

It passed
**2632 tests, 10 skipped in 238.61s** after the schema correction. Final Ruff lint,
format and whitespace checks passed. No configured mypy/pyright gate exists.

### Evidence and limitations

Ignored fixture roots `artifacts/v0-transport-*` and the executed pytest outputs are
local evidence identifiers, not published dependencies or raw provider material.
Original Seoul sources and historical reports were not rewritten. This task did not
replay Seoul or call live LLM/Google services. V0's two-node, tool-free path and V1-V3
independent execution remain covered by tests; the unchanged density/identity rules
are not a newly approved research policy. No measured live improvement, failure frequency,
formal ranking or version freeze is claimed. Local commits are complete; code publication
and a new live check require separate authorization. Current task acceptance remains
tracked in Issue #57.

<a id="v0-structured-transport-live-2026-10-05"></a>

## Structured V0 transport live smoke - 2026-10-05

Status: Validated for one bounded development smoke. Not a formal benchmark,
version comparison, independent route-feasibility assessment or version freeze.
The user explicitly approved the prepared scope and budget after PR #58 delivery:
one V0 workflow, at most two model calls, a 600-second request deadline and no retry.
Execution used clean `feature/evaluation` revision
`c368f1cef9f54d365e50a6e4eeabb2334dcf57e5`, whose tree is identical to merged PR #58
revision `f9d788087417d95c9a04cdfa3ed9b20ad6a5ec57`.
No production/configuration change was made. This record and its PROJECT.md pointer
were added after execution; the tracked working tree was clean throughout the run.

### Scope, dispatch failure and actual execution

The unchanged Seoul request specifies 2026-10-07 through 2026-10-10, two travelers,
KRW 1,200,000, one Gyeongbokgung visit and relaxed history/neighborhood/food interests.
Input SHA-256: `07be92a51cc1db24d925e04ab16d15c15f2e501cecfd24a151ea9ee6cb6debfa`.
Reference date was 2026-10-05; no previous live allowance was reused.

The `smoke tests` conversation verified the prepared files and code, then automatic
approval review rejected two delegated launch requests before process creation.
It did not recognize cross-conversation human approval as trusted live authorization.
No launch marker or model send existed at that checkpoint. The owning conversation
then launched the same verified entry point using the user's direct approval there.
The smoke executor inspected and reported the saved artifacts without launching again.
This is an execution-coordination deviation, not a model retry or a budget extension.
The rejection history remains in the local execution report.

The single actual workflow completed with exit code 0. Launch and completion were
2026-10-04T15:53:38.100781Z and 2026-10-04T15:54:08.991526Z, respectively
(2026-10-05 locally). Usage capture measured **30.516 seconds** including cleanup.
It recorded two successful `gpt-6-luna` model invocations and two instrumented Foundry
HTTP sends, both status 200: preference interpretation and structured generation.
There were no retries, V1-V3 runs, Google/Web/Weather/RAG/database calls or independent
factual-evidence acquisition. Reported tokens total **18,286**: 12,675 input and
5,611 output. These are observed provider/message usage, not independently measured
billing; actual charged cost remains unknown. Inclusive stage summaries overlap
and include duplicate stage labels; they must not be added to obtain total elapsed time.

### Observed declarations and native projection

The result contains four days, each with two declared `main_poi` activities and one
estimated transport activity. All four transport activities preserve a nested
declaration; non-transport activities serialize without one. There are no
application-owned transfers.

| Day | Directed activity endpoints | Mode | Model-estimated interval |
| --- | --- | --- | --- |
| 2026-10-07 | `day1-gyeongbokgung` to `day1-contemporary-history-museum` | WALK | 12:00-12:20 +09:00 |
| 2026-10-08 | `day2-bukchon` to `day2-insadong` | WALK | 12:00-12:25 +09:00 |
| 2026-10-09 | `day3-seoul-museum-history` to `day3-gwangjang-market` | TRANSIT | 12:00-12:35 +09:00 |
| 2026-10-10 | `day4-changdeokgung` to `day4-jongmyo` | WALK | 12:00-12:20 +09:00 |

Unmodified native projection policy `structural_claims_directed_occurrences_5`
uniquely binds **4/4** claims, with **0 unbound claims and 0 projection diagnostics**.
No endpoint/mode review, title rewriting or evidence substitution was supplied.
This live sample has only supported modes and valid bindings; it does not exercise
null modes or invalid endpoints, which remain covered by the prior offline regressions.
For example, the title "Travel toward Gwangjang Market" does not name its origin
or mode; its structured endpoints and TRANSIT declaration supply that representation.
This is observed successful production of the new contract in this one run, not a
claim that free-text parsing became reliable or all future outputs will be complete.

### Checks, evidence and limits

Offline preparation validated input dates, credential presence without printing
secrets, clean code/tree equality, current 600-second runtime configuration and
protected original-source hashes. Initial helper lint found import-placement and
lambda-assignment violations; local helper corrections passed Ruff lint/format
before live approval and did not modify production code. A network-forbidden check
also projected historical V0 material without rewriting it.

After the actual run, shared PlanningResult validation and an exact independent
replay of the saved projection passed. Input/result hash linkage across the attempt,
provenance, usage and mechanism artifacts passed, as did all four protected original
Seoul hashes (input, V0 result, manifest and packet). The prepared plan/launcher hashes
still matched authorization. The saved result SHA-256 is
`b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`.
The full backend gate was not repeated: no production code changed after the existing
2632-pass/10-skip gate; this task adds actual bounded execution and source checks.

Local evidence identifier: `artifacts/v0-transport-live-20261005/` contains the
plan, authorization, launcher, preflight, launch marker, copied input, result,
attempt, provenance, usage, mechanism, projection, inspection, execution report
and completion audit. These ignored files are retained local evidence, not published
dependencies or raw payloads committed to Git.

Mechanism capture links the correct input/result and reports no collection error,
but its `prepared_calls`, `occurrences` and `catalog` arrays are empty for this V0
path; that envelope does not independently prove model submission contents or attention.
The usage ledger supplies the observed invocation/send counts. The provenance file
also retains preflight-only `network_calls_performed: 0` and
`status: ready_for_budget_confirmation` fields copied from preparation; these describe
preflight, not the completed live attempt. Use `attempt.json` and `usage.json` for
actual completion and calls, rather than treating those inherited fields as live totals.
No new identity,
opening, price or route facts were independently checked. A valid model-estimated
duration and correct binding do not imply route PASS. Historical Seoul V0-V3 sources,
reports and scores remain unchanged; no paired score delta or general quality ranking
is inferred from this new sample. Future factual verification or another live attempt
requires its own approved scope and budget.

<a id="offline-cost-acceptance-2026-10-05"></a>

## Offline cost accounting and Seoul replay — 2026-10-05

Status: **Implemented, offline validated and reviewed; local commits only.**
[Issue #59](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/59) supplements
closed usage [#14](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/14).
The user approved TDD, implementation/testing/review/corrections, local commits, Issue
updates and offline replay. No paid provider call, account billing query, push/PR/merge,
planner rerun, formal experiment or version freeze is included. The separate new-V0
[route plan](routes.md#new-v0-route-plan-2026-10-05) remains preparation only.

Review fixed point: `ff2085f6e6dafffa2b02f9b14bb10c89e49b3be8` on `feature/evaluation`,
with a clean initial tracked tree. Existing prior V0 smoke documentation commits are
outside this diff. Runtime reports, prices, normalized sources/annotations and checks
remain ignored local evidence under `artifacts/seoul-cost-20261005/`; no raw provider
payload, runtime log or price assumption artifact is committed.

### Implementation and price basis

The existing opt-in ledger now retains optional cache/reasoning token details, bounded
Google billing request context and separately observed SDK search-tool counts. Reasoning
remains part of output. Uniquely observed active model invocations supply exact backing
HTTP bindings; ambiguous capture remains unlinked. The stdlib-only cost library/CLI
accept saved usage and verified native snapshots, explicit dated price rows, normalized
event/run/aggregate bills and source-linked historical annotations. Decimal money,
unknowns, Repair subsets, namespaces and lineage are separate from quality scoring.
Output cannot overwrite imported usage/price/bill/snapshot material.

No actual bill was supplied, so **actual charges remain unavailable**. Microsoft pricing
research did not yield a usable deployment-specific numeric rate. The user then explicitly
selected OpenAI official GPT-6 Luna prices: Standard short context, per million tokens
**input $0.10, cached input $0.01, output $0.50**, checked 2026-10-05 at the
[official model page](https://developers.openai.com/api/docs/models/gpt-6-luna).
Historical missing cache counts use an explicit, source-linked **no-discount assumption**;
cache writes, regional premium and service-tier differences are excluded rather than
claimed observed. Each call is below the 272,000-token long-context threshold. These are
current-price retrospective estimates and not Foundry invoice amounts.

Google prices use the Global first paid tier before credits/free caps/tax/volume discounts,
checked 2026-10-05. The preserved historical oracle adapter's exact Text Search/Details
mask includes opening hours/website fields, supplying an annotated Enterprise basis:
$35/1,000 searches and $20/1,000 Details. The frozen TRANSIT matrix requests use no
advanced options and one element each: Essentials $5/1,000 elements.
Sources: [prices](https://developers.google.com/maps/billing-and-pricing/pricing),
[field/SKU rules](https://developers.google.com/maps/billing-and-pricing/sku-details),
[route billing](https://developers.google.com/maps/documentation/routes/usage-and-billing).
Annotations retain exact original source hashes and reconstruction explanations.

### Observed offline results

| Saved attempt | Observed input/output tokens | OpenAI model estimate USD |
| --- | --- | --- |
| Original Seoul V0 | 12,562 / 5,815 | 0.0041637 |
| Original Seoul V1 | 64,151 / 8,195 | 0.0105126 |
| Original Seoul V2 | 65,406 / 10,806 | 0.0119436 |
| Original Seoul V3 | 95,078 / 14,696 | 0.0168558 |
| New structured-transport V0 | 12,675 / 5,611 | 0.004073 |

V3 Repair's model estimate is **$0.003523**, already included in V3. This is a subset,
not an extra amount to add. Model-backed HTTP is not another model fee, but these older
envelopes lack exact backing links; that uncertainty prevents complete run totals.
Historical planner API events also lack field-mask/mode/SKU context, so the primary
report leaves those components unpriced. Open-Meteo account charging and unobserved
services are not inferred; absent embedding events do not establish a universal zero bill.

Two explicitly assumed unit-rate scenarios supplement the primary report. They price
every historical search/Details/matrix event at the stated official rate regardless of
the unknown actual SKU. They are **not a confirmed range or bill**:

| Scenario | Per 1,000 search / Details / matrix-element rates | V1 observed subtotal USD | V2 observed subtotal USD | V3 observed subtotal USD | V3 Repair subset USD |
| --- | --- | --- | --- | --- | --- |
| Pro / Enterprise / Essentials | $32 / $20 / $5 | 2.0565126 | 2.0679436 | 2.0988558 | 0.093523 |
| Highest field tiers | $40 / $25 / $15 | 4.4405126 | 4.4719436 | 4.6668558 | 0.273523 |

These subtotals include the model estimate. Weather and unlinked/uncertain sends remain
unavailable; neither scenario supplies a complete actual/estimated run total. The Repair
API scenarios correspond to 18 requested route elements, not another whole-run charge.

Independent oracle accounting remains shared and separate:

| Frozen oracle snapshot | Actual recorded sends | Requested matrix elements | Retail estimate USD |
| --- | --- | --- | --- |
| Identity | 36: 23 searches + 13 Details | 0 | 1.065 |
| Final evidence | 23: 16 Details + 7 matrix | 7 | 0.355 |
| Paired evidence | 23: 16 Details + 7 matrix | 7 | 0.355 |
| Observed oracle subtotal | 82 | 14 | **1.775** |

The final/paired acquisitions have different timestamps/manifest hashes and separately
recorded sends, so both are counted; duplicate artifacts/captured attempts are rejected.
They are not allocated to V0-V3. These rows do not assert charges after account allowances
or establish formal efficiency/quality comparisons.

The final CLI replay completed after review corrections. All eight original usage and
snapshot manifest hashes remained byte-identical; native raw observations passed existing
replay/hash checks. The new V0 result also retained SHA-256
`b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`.
Old Seoul sources/reports and V0 planning decisions were not modified.

### Validation, commits and independent review

TDD first reproduced absent cache details, absent Google billing context, absent SDK tool
counts and missing cost/snapshot interfaces. Each slice passed after implementation.
Worked examples cover exact cache partition/output amounts, requests/elements/embeddings,
tool fees, actual event override, whole-run allocation limits, aggregate retention,
bad/foreign/duplicate bindings, absent data, expired/ambiguous prices, adapter coverage,
source-bound annotations, CLI no-socket operation and immutable/corrupt snapshots.
An initial subtotal assertion was corrected to include its matrix component; Ruff
formatting/import findings were corrected before the gate.

1. Before implementation commits, focused checks passed **73 tests**, Ruff/diff checks
   passed, and the full unfiltered backend gate passed **2655 tests, 10 skipped in
   323.62s**. No configured static typechecker exists. Existing skip conditions remain.
2. Implementation commits: `0a68380` (`feat: capture optional billing usage details (#59)`)
   and `f3d4621` (`feat: account saved usage and imported bills offline (#59)`). These were
   committed before independent Standards/Spec review against the fixed point.
3. Standards found optional `tools=None`/SDK omission metadata could turn a successful
   SDK response into TypeError. Spec found broad model-HTTP suppression hid failed,
   unlinked or foreign sends. Regression tests reproduced both before correction.
   A real mocked HTTP/SDK seam also reproduced the missing invocation link.
4. Separate correction commits preserve history: `6e74c11` (`fix: preserve SDK outcomes
   and bind model transport (#59)`) and `0f6a247` (`fix: retain uncertainty for unlinked
   model sends (#59)`). Corrected focused checks passed **80**; affected Foundry,
   integration, retrieval, runtime, intake and planner-runtime checks passed **288,
   1 skipped**. The full gate was not repeated after these bounded corrections.
5. Standards and Spec rechecks each reported **zero remaining actionable findings**.
   Reviewers also checked the pending cost contract/guide and route preparation boundary.
   Narrow reviewer checks passed 6 capture and 23 calculator tests respectively; these
   overlap other checks and must not be added into an independent total.

The final documentation commit records acceptance, current interfaces and the route plan.
Issue checklist completion reflects local validation, not publication or bill retrieval.
No version milestone/freeze or formal research conclusion follows.

### Git delivery review correction — 2026-10-05

Publication was separately authorized for this scope: push, PR review, merge after
acceptance and closure of Issue #59. [PR #60](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/60)
reviews the complete published scope against `f9d7880`; the first published head was
`9be9e1b`. Synchronizing main introduced no file changes, preserving earlier test evidence.
The original baseline and implementation/correction commits above remain in history.

The delivery Spec review found no actionable findings and independently passed 30
focused tests. Standards found two issues: SDK tool billing observations inflated the
existing physical HTTP metrics, and PROJECT.md still called Issue #57's gate the latest.
The HTTP regression first failed for both zero and one actual mocked dispatch (reporting
one and two respectively). Correction `941bd9d` excludes only the explicit
`sdk_output_tool_calls` observations from HTTP metrics, retaining their cost units,
duplicate-event validation, model tokens and actual transport events. PROJECT.md now
points to the later Issue #59 full gate and distinguishes subsequent bounded checks.

The first broader correction run passed 79 tests but had 16 fixture setup errors because
the default Windows pytest temporary directory was inaccessible. Using a fresh workspace
temporary directory and disabling pytest cache resolved this environment issue: all **95
observability/resource/cost tests passed in 3.89s**. Ruff lint/format and diff checks passed.
The local log is `artifacts/seoul-cost-20261005/delivery-correction-tests.txt`; it is
ignored evidence, not a published dependency. No source artifacts, invoices, paid calls,
planner behavior or route execution changed. Final delivery review and merge status are
recorded on PR #60 and Issue #59.

<a id="uniform-llm-identity-2026-10-05"></a>

## Uniform LLM identity judgment — 2026-10-05

The user approved replacing mandatory human place-identity confirmation with LLM judgments
under [Issue #72](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/72). The decision
applies to evaluator V0-V3, relevant requirement subjects and optional V3 projections;
individual names in a live smoke are evidence, not design rules or fixed test cases.
Implementation baseline: `b158c916148d92d0f73907054aa492f12062004f`; implementation/test
commit: `9f1cd71`. The unrelated pre-existing `.gitignore` change remains outside the task.
Git publication and fresh live model/Places/Routes calls were not authorized.

The [current contract](../../contracts/0002-intake-identity-usage.md#uniform-llm-identity)
prepares immutable packets with original claims, independent candidate observations and
short references. Every adopted identity comes from supplied model judgments; high-impact
and sampling no longer impose human gates. Model output explicitly assesses address and
destination compatibility. An identified venue can coexist with an incorrect original
address; the original claim is retained. Unknown/no-supported-match and contradictions
keep unresolved identities, denominator coverage and downstream uncertainty. Exact
request/response/report replay checks integrity, not semantic correctness or human accuracy.
Explicit legacy entry points reproduce frozen native/V0 human-policy reports.

Public-boundary TDD first failed on the missing packet module, then missing model adoption,
downstream replay and CLI preparation. Later tests exposed acceptance of malformed cited
address components, a malformed-record marker scan and a controlled CLI replay mismatch.
The controlled mismatch came from JSON field order changing a serialized request string;
canonical request serialization fixed it without changing source bytes. A source-linked
synthetic high-impact fixture also needed its declared required-visit count to enter route
preparation; the fixture now supplies an exact count of one. A final malformed model-content
regression reproduced an AttributeError and now rejects that material as a ValueError.
Synthetic evidence covers all versions, optional projections, protected subjects, unknown
and no-match outputs, wrong claimed IDs, address states, packet/response/report tampering,
three CLIs, coordinates and V0 route-request preparation with a network guard.

The first full backend gate passed **2804 tests with 10 skips in 353.61s**. Final focused
coverage after the extra malformed-content regression passed **28 tests in 5.44s**; Ruff
passed. Standards and Spec each found one issue during independent review. Standards found stale
PROJECT.md validation metadata, corrected in the pending documentation. Spec found that cited
address components lacked optional `shortText` type validation. The synthetic regression first
reproduced acceptance of `shortText: 42`; correction `e8a7293` rejects the complete import and
consumer replay while keeping valid repeated provider types available to the model. Both
review rechecks have **zero remaining actionable findings**. Correction retests passed **301
identity/snapshot/schedule/request tests in 38.57s** and **30 LLM tests in 5.24s**.

The follow-up full run passed 2804 with 10 skips but failed one existing retrieval test,
`test_sql_timeout_and_caller_cancellation_are_distinct[True]`, in 342.20s. It configures a
20ms SQL timeout and distinguishes cancellation after an asyncio event. The complete
retrieval test file independently passed **16 tests in 7.77s**. Timing interference while
another focused test run was active is an inference, not a confirmed production defect.
No retrieval code or timeout test was changed. The final serial full backend gate after
correction passed **2807 tests with 10 skips in 328.32s**, without another test run active.
The final code revision is `e8a7293`; implementation and correction remain separate commits.
Ruff, tracked-link checks, preserved historical anchors and protected-file hashes pass.
Status: locally implemented, offline validated and independently reviewed; Git publication
and fresh paid judgment collection remain pending separate authorization.
No mypy/pyright configuration is present. Local logs are ignored evidence identifiers:
`.scratch/issue72/full-backend.log`, `full-backend-final.log`, `full-backend-serial.log`,
`review-retest.log`, `review-focused.log` and `retrieval-recheck.log` under that directory.

Offline replay of saved smoke material verified all **61 protected file hashes unchanged**.
The new derived packet covers nine references (one requirement subject and eight visits),
has zero human gates and produced zero new model/provider sends or incremental charges.
Its explicit model is inherited from the saved material solely to prepare the request.
The prior response lacks the new address assessments; it was not fabricated or reinterpreted
as a current-policy response. Derived local evidence identifiers are
`artifacts/llm-identity-policy-20261005/packet.json`, `pending-report.json` and
`offline-acceptance.json`. New-policy acceptance for that smoke awaits separately authorized
fresh model judgment; its original six-adoption report and all four UNKNOWN route verdicts
remain historical evidence. No planner rerun, score change, formal benchmark, version freeze
or research conclusion is claimed. Blinded preference work and other human supplements are
outside this place-identity change.

<a id="address-failure-no-repair-2026-10-05"></a>

### Delivered-address failure clarification - 2026-10-05 to 2026-10-06

After the uniform-policy local acceptance, the user clarified that both a recognizable
intended venue with a wrong submitted address and an address denoting another venue must
count as errors. Evaluation must preserve baseline mistakes rather than repair V0. The
same evidence standard applies to every version; an expectation that V0 can err is not
permission to manufacture failures. This is an in-scope correction under #72, with fixed
review base `adaf2888b78f9d6cacddd41510f0077720cbe7e3`. The pre-existing unrelated
`.gitignore` change is excluded; no live sends or Git publication are authorized.
Implementation/test commit: `1c43007`.

Policy `llm_identity_judgment_2` marks supported `incorrect_claim` and `different_place`
assessments as grounding FAIL and refuses canonical adoption. The chosen candidate remains
diagnostic model material, including claimed-ID conflicts, but cannot supply corrected
addresses, coordinates or route endpoints for that occurrence. UNKNOWN remains for
insufficient evidence. Confirmed failures complete their judgments rather than entering
an automatic repair/retry queue. The quality consumer uses replayed per-occurrence verdicts;
existing score arithmetic, denominators, planner behavior and legacy classifications remain
unchanged. Prior policy packets/reports cannot authorize current downstream preparation.

TDD reproduced incorrect-address adoption and missing explicit verdicts in eight address
cases. After blocking adoption, eight four-version report cases exposed confirmed errors
being downgraded to UNKNOWN; consuming the explicit verdict corrected them. The twelve
report cases passed (two error assessments and evidence uncertainty across four versions).
Two further red tests showed unsupported failure assessments being accepted; address failures
now require original name/destination/location and independent candidate citations. The
identity/report files then passed 84 tests. Initial test invocations encountered missing
pytest in system Python and inaccessible default temporary/cache directories; validation
uses repository `.venv`, new workspace basetemp directories and disabled pytest cache.

The first coordinate regression incorrectly expected the shared venue coordinates to
disappear globally and failed three cases. Source inspection showed valid references in
other versions independently retain those coordinates. The corrected public-boundary
assertion preserves their evidence while proving V0's bad occurrence has a null endpoint,
no expected route context, zero identity-eligible acquisition legs and zero sends. All
three error/uncertainty cases passed. This is fixture correction, not suppression of a
provider/planner error. No internal implementation mocking or actual provider send was used.

The first full gate passed **2824 tests, 10 skipped in 361.36s**. A final legacy-compatibility
regression initially stopped at stale snapshot linkage; rebuilding its matching synthetic
snapshot exposed the real defect: an added same-name legacy metadata field supplied new FAIL
classification. The quality consumer now reads the explicit verdict only from a source-bound
model record, whose markers require exact LLM replay. Legacy reports keep their original
classification. Identity and quality files passed **88 tests in 19.29s**, and Ruff passed.
The final serial full backend gate completed on 2026-10-06 and passed **2825 tests,
10 skipped in 339.67s**. Independent
Standards and Spec review of `adaf288...1c43007` and pending current/dated documentation
reported **zero actionable findings on each axis**; no review correction commit was needed.
Checks passed for Ruff, diff whitespace, 201 tracked local documentation links, preserved
explicit historical anchors and English additions. There is no configured mypy/pyright gate.
Ignored log identifiers are `.scratch/issue72/address-full-backend.log` and
`.scratch/issue72/address-full-backend-final.log`. The implementation is locally complete;
Git publication remains separately authorized.

Protected-source replay verified all 61 prior hashes unchanged. New ignored evidence
identifiers are `artifacts/llm-identity-address-fail-20261005/packet.json`,
`pending-report.json` and `offline-acceptance.json`. The packet covers the same nine
references and prepares the inherited model name only. No fresh result is supplied, so
all nine current-policy verdicts remain UNKNOWN; no old response is rewritten or used
to invent smoke failures. Fresh paid judgment remains separately authorized. No formal
benchmark, version comparison, freeze or research conclusion is claimed.

<a id="identity-smoke-preparation-2026-10-06"></a>

### Frozen one-call V0 identity smoke preparation (2026-10-06)

[Issue #73](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/73) approved preparation, offline checks, local commits, review and documentation only.
The development executor freezes the existing material through the policy-2 judgment packet;
its new model response remains absent. Default preparation has no network transport. Execution
requires explicit approval of the exact manifest digest and consumes one bound directory.
The model is gpt-6-luna, low reasoning, no tools, store=false, one POST, zero retries,
20,000 estimated input tokens including 1,024 reserve, 4,000 output tokens and a 60-second
HTTP deadline. Reported usage above the allowance stops import after receipt; the surrogate
input-token estimate is a preflight guard, not an exact provider tokenizer or invoice ceiling.
Standard retail reference prices checked on 2026-10-06 are USD 0.10/M input and 0.50/M
output. The maximum reference estimate is USD 0.004 against a USD 0.005 allowance;
cache-write/regional/provider adjustments and an actual Foundry invoice remain unavailable.
No Google acquisition, planner generation, route execution or V1-V3 live expansion is included.

The initial public-seam red gate could not import the missing executor. The first implementation
revealed frozen material must be thawed before the identity interface accepts it; that adaptation
was corrected. The first isolated executor gate passed 13 tests. Terminal coverage was then
extended to tool output, incomplete/partial decisions and source mutation during a call;
executor plus identity policy passed 52 tests. Ruff caught an approval-digest variable in the
wrong test scope; it was moved and lint passed. The full backend gate passed **2842 tests, 10 skipped in 397.57s**. A redundant identical
source check was removed without behavior change during that gate; the final executor
retest passed **17 tests in 9.60s**. Ruff and syntax checks passed. Both Standards and
Spec reviewed committed implementation `abc2663` against fixed base
`f29d8a2a110b7577fe0d320b7ba8c82e7a7cf902` and returned zero findings.
The pre-existing unrelated `.gitignore` change was preserved and excluded.

A completed execution receipt means valid processing, including FAIL/UNKNOWN judgments,
not that all venues passed. Address failures have null canonical identity, no candidate-based
repair and no new coordinates/route endpoints. The old 61-file evidence remains byte-identical.
Source-bound raw bytes, usage, model envelope and accepted report are separate evidence;
malformed returns cannot create an accepted report. Any failure stops permanently for that
execution directory; unknown billing stays null. A future live child must receive the exact
revision, hashes, command, limits, stopping criteria and user approval before dispatch.

The actual preparation at local evidence identifier
`artifacts/llm-identity-smoke-20261006/preparation.json` contains nine references and
**16,498 estimated input tokens including reserve**. Its manifest digest is
`6387cb507b7e2fdbf1a44badbd977c0fa2c7a5962c913ade01fc3afabc054e02`;
wire-request digest is
`8a7740e37a384b0803345b95a92f0bdde21fcbf1776c2a14f7436c3349aeb7e0`.
All 61 additional protected originals and 69 total frozen source files verified unchanged.
Implementation hashes are separately bound. The execution directory does not yet exist:
actual new model/Places/Routes sends and incremental charges are zero. No fresh judgments
or route facts are available; the current-policy pending verdicts remain UNKNOWN. The
previous six historical adoptions and four UNKNOWN routes are preserved as historical
results, not silently upgraded. No particular new PASS/FAIL count is an acceptance target.

The private handoff supplies the exact future command and final local revision. Public
operational instructions are in the [evaluation README](../../../backend/evaluation/README.md#prepared-one-call-identity-development-smoke).
This is a validated preparation and local implementation, pending Git publication and
separate live-plan approval. Neither is a formal benchmark, version freeze or research
conclusion. The request is a single uniform judgment over saved V0 claims and independent
facts; all V0-V3 planner behavior and score formulas remain unchanged.

#### Exact-plan approval and prelaunch automatic review block (2026-10-06)

The user subsequently approved the exact frozen single-call plan in the current chat.
The parent saved local evidence identifier
`artifacts/llm-identity-smoke-20261006/live-authorization.json` and delegated execution
only to a current-session `gpt-6.1-sol` child at medium reasoning with no history fork,
as required by the [smoke policy](../../agents/smoke-tests.md). The approved model under
test remained `gpt-6-luna` at low reasoning. Source revision was
`c9965bdd5f651efc6f8c5f2a05b9c7c7f099b149`; only the known unrelated `.gitignore` edit
was present. The request, manifest, source files, endpoint and limits were unchanged.

The child verified 61/61 protected originals, 69/69 source files and 2/2 implementation
hashes both before and after the blocked dispatch, plus exact manifest/wire digests,
HEAD and branch. Automatic approval review rejected the exact execution command before
it launched. Its stated reasons were insufficient explicit trusted authorization for
the locally derived identity payload to the specific Azure destination, and a perceived
model configuration mismatch with smoke policy. This is a reviewer block, not an observed
provider failure or a measured policy deviation. The documented child/model-under-test
separation was unchanged. The child stopped and did not retry.

Actual model/Google/planner sends and incremental charges are **zero**. No process exit,
HTTP status, duration, provider usage, response, identity verdict or provider invoice
was observed. The bound execution directory remains absent. All nine current-policy
pending verdicts remain UNKNOWN; source evidence was not edited. The parent independently
rechecked the same hashes and inspected the frozen wire schema/destination without
network work. The payload consists of the nine supplied claims, independent candidates,
provider observations and source associations, plus judgment instructions/output schema.
The configured destination and full data scope are being presented to the user to address
the automatic review's request for explicit external-send approval. No new attempt is
made by this record; the one-call allowance remains unconsumed.

Local evidence identifiers are `blocked-execution.json` next to the preparation and the
updated private handoff. No code or tests changed, so the prior 2842-pass full backend
and 17-pass executor gates remain the engineering checks; documentation links/diffs and
remote tracker readback are checked for this record. This blocked development smoke is
not a benchmark, a version freeze or a semantic judgment on any real venue.

<a id="identity-smoke-execution-2026-10-06"></a>

### Approved single-call V0 identity execution and rejected import (2026-10-06)

After the prelaunch block above, the parent displayed the exact configured Azure destination,
nine-reference data scope and model-under-test configuration. The human explicitly approved
that external send and repeated approval after an interrupted turn. A read-only preflight
confirmed no matching live process or execution directory, no consumed request, and unchanged
manifest, wire and implementation/source hashes. Only documentation differed from c9965bd;
execution revision was **ffb2db3da6e76b80f9a3fd90b38394b8fb4c7b77**, on feature/evaluation,
with the unrelated pre-existing `.gitignore` edit preserved. The parent recorded local
`explicit-send-authorization.json` and updated the private handoff. A current-session
`gpt-6.1-sol`/medium child used a bounded five-turn history fork, permitted by smoke policy,
to retain direct human consent context. The model under test stayed `gpt-6-luna`/low.

Automatic review allowed the exact command this time. The unchanged manifest digest was
`6387cb507b7e2fdbf1a44badbd977c0fa2c7a5962c913ade01fc3afabc054e02` and the wire digest
`8a7740e37a384b0803345b95a92f0bdde21fcbf1776c2a14f7436c3349aeb7e0`. The one real POST
returned **HTTP 200**, response status completed, in **7.175079 seconds**. Request/response
UTC timestamps were `2026-10-05T14:57:13.015153+00:00` and
`2026-10-05T14:57:20.190232+00:00`: **2026-10-06 01:57:13-01:57:20 AEDT** in the client
calendar. Process exit was **1**, execution receipt stopped with ValueError, and no
accepted `identity-report.json` was generated. There were no retries, alternate execution
methods, new Google acquisition, planner reruns or V1-V3 live expansion.

Observed usage was **14,403 input / 967 output / 15,370 total**, cached input 0, reasoning
0 and cache-write input **14,400**. The executor's frozen base retail calculation recorded
**USD 0.0019238**. Its declared calculation omits cache-write premiums. Using the
[official model rates](https://developers.openai.com/api/docs/models/gpt-6-luna) checked
2026-10-06 (USD 0.10/M ordinary input, 0.125/M cache writes and 0.50/M output), the parent
separately calculated an adjusted standard retail reference of **USD 0.0022838**:
three ordinary input tokens, 14,400 cache-write tokens and 967 output tokens. Both
references are below the USD 0.005 allowance; neither is an Azure invoice. Provider/regional
adjustments and child/session billing remain outside this model-test reference calculation.
Original execution usage/cost evidence was not rewritten to absorb the derived estimate.

The raw byte digest was
`d6f747af929131e4cbd6667e709cb4bb9a42deaacc2ee26f0daf3272b2d262c9`.
The child preserved `execution.json`, `response.bin` and `model-result.json` under local
identifier `artifacts/llm-identity-smoke-20261006/execution/`. The parent independently
verified raw-byte/envelope hashes, exact packet binding, nine unique owned references and
all **61/61 protected originals, 69/69 sources and 2/2 implementation hashes**. All original
V0 claims and old smoke evidence remain byte-identical. A read-only public-interface replay
reproduced **Unsupported identity judgment citation**; no response was edited or repaired.

All nine raw decisions said match/different_precision/consistent. However, each cited
`case.candidates.display_name` and `case.candidates.formatted_address`; the importer accepts
`candidate.display_name` and `candidate.formatted_address`, while `case.candidates` alone
is a separate supported whole-set citation. The protected subject additionally cited a
null `claim.location` and assessed it as different_precision instead of the required
not_supplied. The first unsupported citation rejects the complete batch. The parent and
child inspection of the other malformed fields is diagnostic, not an accepted semantic
judgment or a human identity gate. Raw matches cannot be counted as PASS, adopted identities,
new canonical coordinates or route endpoints. Current pending verdicts remain **nine UNKNOWN**;
this rejected evaluator response is not evidence of nine V0 address failures. Genuine planner
mistakes remain possible and must not be manufactured or repaired.

The parent saved local `live-assessment.json` and a readable `results.md` beside the preparation,
containing original claims, independent selected candidate facts, raw rationales/citations,
rejection diagnostics and distinct usage/cost evidence. These are ignored diagnostic
artifacts, not current contracts or accepted reports. The consumed execution directory cannot
be reused. The private handoff records the terminal outcome. No code/tests changed; the
prior 2842-pass/10-skip full backend and 17-pass executor gates remain the engineering
checks, and this failed live integration plus exact offline rejection is recorded separately.
Tracked link/diff checks and remote tracker readback cover the documentation update.

The bounded execution and assessment are complete; the smoke acceptance is **not passed**.
The proposed next correction is to constrain supported evidence_fields in the model schema
and clarify/guard missing-address output. It is not implemented here, and no further paid
request is authorized. Original provider/model evidence must stay intact through any later
correction. Git publication remains separately unauthorized. This is development smoke
failure evidence, not a benchmark, version freeze, formal comparison or research conclusion.

<a id="version-specific-evaluator-backlog-2026-10-06"></a>

### Version-specific evaluator decision and classified backlog (2026-10-06)

The user clarified that evaluator V0 introduces an LLM primarily to correspond
model-generated POI claims with independent API candidates, while V1-V3 evaluation
introduces no model, including for user-named requirements. API-backed name/address
differences remain errors; intended-venue recognition cannot repair an original wrong
address. The earlier all-version LLM design is superseded as a requirement, without
changing current code or relabeling historical evidence. Independently missing/failed
evidence remains UNKNOWN; no V0 failure is presumed or manufactured.

The user explicitly requested backlog organization, classification and Issue publication.
At this specification-only checkpoint, source revision is local unpublished
`1a3e17f05e49b0f6f9e36661d13b32b0fda3f27f` on feature/evaluation, with the pre-existing
unrelated `.gitignore` modification preserved. Current resolver behavior remains the
uniform `llm_identity_judgment_2` policy. No implementation or test pass for the new
requirement is claimed, and publication is not implementation approval.

[Parent #74](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/74) owns the
accepted specification and five OPEN, ready-for-agent children:

| Category | Ticket | Immediate blocker |
| --- | --- | --- |
| Enhancement: deterministic V1-V3 evaluation and V0 dispatch | [#75](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/75) | None; implementation approval still required |
| Bug: V0 correspondence/citation/missing-address contract | [#76](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/76) | #75 |
| Enhancement: fresh V0 smoke preparation | [#77](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/77) | #76 |
| Enhancement: revised offline V0 route preparation | [#78](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/78) | #76 |
| Enhancement: reviewed Git delivery and historical reconciliation | [#79](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/79) | #77 and #78 |

All five native parent/child relationships and five native blocking edges were
created and read back. New bodies, exact titles, OPEN state and category/readiness/group
labels were verified against their drafts. Existing #72/#73/#70 gained current-follow-up
notes and enhancement categories while retaining their titles, historical bodies and
OPEN state. No Issue was closed. #67 remains the historical parent; its human identity
and audit gates are not requirements for this iteration. GitHub owns live state;
local draft scripts/material are ignored publishing aids, not another tracker.

The source-bound correction/report path is tested inside each implementation ticket;
there is no separate horizontal testing ticket. Smoke preparation and route preparation
can proceed independently after #76. An accepted real identity report is still a data
gate for real route readiness, so preparing a smoke alone cannot unlock queries. The
consumed #73 allowance and rejected raw response remain intact. #79 does not require a
paid smoke to deliver offline-validated code with accurately documented limitations.

Current project status and the identity contract distinguish the accepted requirement
from implemented behavior. Remote content/state/label/relationship readback passed;
128 tracked local link targets across four updated documents, preserved historical
anchors, new anchors, English content and diff checks passed. No code tests or live
calls are run. Prior engineering gates remain historical. No planner output, raw provider
artifact, score formula, model/Google request, Git push/PR/merge, formal benchmark or
version freeze is introduced by publishing this backlog.

<a id="evaluator-checkpoint-delivery-2026-10-06"></a>

### Authorized existing evaluator checkpoint delivery (2026-10-06)

After requesting delivery of the existing local commits, the human explicitly chose
full delivery: push, create a PR, review and merge after successful checks. This
authorization covers the existing checkpoint before #75 implementation, not the
pending version-specific evaluator or a fresh live request. The final four consecutive
documentation commits had previously been consolidated at the user's explicit request
into `b2bbf75`, with an identical tree and preserved `.gitignore` bytes; the original
documentation objects remain in a local backup ref for historical receipts.

[PR #80](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/80) publishes the
ten existing commits from `f011a29` through `b2bbf75`. Review base is
`5d21d6b4685c7793f27954d7c175bed9524b3803` (main at dispatch), merge base
`56cae0c96c618a6c03ce25a29277132b08589b9d`, and reviewed head
`b2bbf75fbf3d5f110955da035ef857604efc96d6`, on feature/evaluation.
The pre-existing unrelated `.gitignore` edit remains unstaged and excluded; ignored
raw/scratch artifacts are not published. This delivery-state documentation is a
separate follow-up commit, without implementation changes.

Independent Standards and Spec agents each found **zero actionable findings** across
the combined release diff. They checked current policies/contracts, source-bound
identity replay and no-repair FAIL propagation, CLI/consumer integration, offline route
readiness, one-attempt execution and truthful historical/current status. The accepted
V0-only model / deterministic V1-V3 replacement is explicitly unimplemented. No code
correction was needed. The final documentation delta is separately checked before
merge; the pre-merge PR comment records its final head, both axes and validation scope.

The reused serial backend gate is **2842 passed, 10 skipped in 397.57s**; final executor
17 and executor/identity 52 also remain valid prior evidence. No code/test file changed
after `abc2663`; a new full run is not claimed. Initial delivery checks passed 281 tracked
local targets across 14 changed documents and base-to-head whitespace. No mypy/pyright
gate or CI check is configured. The absence of CI is not a passed CI result.

Historical #70/#72 scopes can close after verified merge, and #67 after delivery of its
two original offline slices (#69 and #70). #73 can close as frozen preparation and
execution-evidence delivery complete: **its live import failed, nine verdicts remain
UNKNOWN, no accepted report exists, the allowance is consumed and no retry is
authorized**. The response correction belongs to #76 and fresh-plan preparation to #77.
Four route verdicts remain UNKNOWN with zero executable requests. #74-#79 remain OPEN;
this delivery does not implement or close their subsequent scopes. Actual merge and
Issue outcomes are recorded in the accessible PR/tracker, rather than anticipated here.

No new model, Google or planner call, original-output repair, score-formula change,
formal benchmark, version comparison or freeze occurs in this delivery. Source hashes
in historical execution manifests are not rewritten to absorb Git history consolidation.

<a id="version-specific-identity-implementation-2026-10-06"></a>

### Version-specific identity implementation (#75, 2026-10-06)

The human authorized #75 implementation, offline tests, local commits and Standards/Spec
review, then resumed work with the implement skill after a waiting/handoff interval.
Fixed review base is `819f0c3c5956c43f6c799feb128fb5a74bb4f2f5`; implementation/tests are
committed as `ffa36a4d96cbf87ad3557dab44b5665495221d2c`. At this validation checkpoint,
current documentation is an unstaged draft and the unrelated `.gitignore` change remains
unstaged. No branch switch, push, PR, merge, tracker mutation or paid execution is included.

The current public resolver produces `versioned_api_identity_1`: V1-V3 primary visits
use independent ID-linked Details and literal original/API name/address comparisons.
Missing output-contract fields are FAIL; unavailable or unlinked independent evidence
is UNKNOWN. Shared named requirements use independent verification of retained bindings
or unique deterministic search. V0 correspondence packets contain only V0 primary visits;
foreign/historical packets and modified reports cannot supply current verdicts. Exact
consumer replay retains original claims, FAIL/UNKNOWN and null canonical endpoints.
Opening/route reports retain identity verdicts separately from their own unavailable facts.
Old uniform LLM and human/audit policies remain explicitly replayable, with original
artifacts untouched. Generation behavior, score formulas and population rules are unchanged.

Public-interface TDD first showed exact V1/API matches staying UNKNOWN without model
results; the program path made these PASS and exact address mismatches FAIL. A second
slice exposed missing requirement-binding support, then verified independent Details
without admitting shared subjects into model packets. Consumer tests exposed absent
endpoint/coordinate failure metadata and verified its preservation without adopting
corrected endpoints. Missing structured names/addresses initially stayed UNKNOWN when
Details were absent; proven contract omissions now remain FAIL independently of availability.

The broader evaluator/executor gate initially reported **957 passed, 1 skipped, 1 failed**
in 175.75s. The executor prepared a scoped V0 packet but still imported through the old
uniform resolver, yielding a stopped offline SDK receipt. Its import was routed through
the public version dispatcher, and the test expectation now scopes model UNKNOWN to V0.
No citation/schema repair from #76 was introduced. The correction and final program
regressions passed **37 tests** in 8.34s, using synthetic local evidence and MockTransport.

Before review corrections, the serial full backend gate at `ffa36a4` passed
**2862 tests, 10 skipped in 273.87s**:
`.venv/Scripts/python.exe -m pytest backend/tests -q -p no:cacheprovider
--basetemp=.scratch/pytest-75-full --tb=short --show-capture=no`.
The local `.scratch/pytest-75-full.txt` is an ignored evidence identifier, not a published
dependency. Global `ruff check backend tools --no-cache` passed; formatting checks passed
all 18 changed Python files. A broader format check reported 61 pre-existing unrelated
files, which were preserved. No configured mypy/pyright or CI result is claimed.
Initial tracked documentation link checks passed 216 repository-relative targets.
The final documentation check passed 217 targets against the Git index; whitespace
checks also passed. Current contracts, navigation and this dated record are committed
as a separate documentation group after the correction review.

Independent Standards review found no hard documented-standard violations and one P3
terminology issue: the programmatic replay branch still used `model_policy` and a
model-assisted diagnostic, and the V0 material docstring described uniform LLM behavior.
Independent Spec review found one P2: malformed/conflicting typed destination components
in an unbound requirement search escaped as `ValueError`, aborting the complete CLI batch
instead of producing local UNKNOWN. Both findings were corrected in the separate commit
`a53aa8110d06f52777fabe7b9a3cd31709c19a30`, preserving the original implementation commit.

Six public CLI regression cases initially produced **3 failed, 3 passed**: null, non-array
and conflicting components reproduced the batch abort, while exact, ambiguous and wrong-query
cases already behaved correctly. The correction catches the typed-destination exception
locally; all six preserve valid V1 PASS records. The broader correction gate passed
**246 tests in 33.48s** across program/historical identity, V0 adoption, snapshots,
coordinates, quality and V3-pair consumers; its ignored evidence identifier is
`.scratch/pytest-75-review-green.txt`. Global Ruff lint and changed-file formatting passed
again. The full suite was not repeated for this bounded correction; its earlier result is
not presented as a post-correction full run. Both review axes rechecked `a53aa81` and the
final documentation drafts with **zero unresolved findings**.

The V0 response correction (#76),
fresh smoke plan (#77), revised offline route integration (#78) and publication (#79)
remain separate scopes. No accepted real current-policy V0 identity report, new route
fact, billing result, formal benchmark, version comparison or freeze is established here.

<a id="v0-correspondence-contract-correction-2026-10-06"></a>

### V0 correspondence contract correction (#76, 2026-10-06)

The human explicitly authorized implementation of #76 after local #75 completion.
Fixed review base is `1bd405768dfe8bb01088845efdecb2ae5933fba3`, on feature/evaluation.
The unrelated pre-existing `.gitignore` edit remains unstaged and outside this task.
Implementation/tests are committed as `0e5aba66682e24958102089d3eb53b5f4ba69856`.
This is a local implementation and offline validation event, not a live smoke, formal
benchmark, research conclusion, version freeze or GitHub publication.

Public-interface TDD reproduced missing citation enums at preparation and missing-address
decisions incorrectly accepting `unknown`, `different_precision` or `equivalent` without
a supplied address. The current packet now shares citation paths with import, and uses
address-presence alternatives bound to owned short reference IDs. Missing addresses require
`not_supplied` for all decisions and exclude `claim.location`; supplied addresses forbid
`not_supplied`. Model instructions agree with both schema and import. The V0 policy changes
to `v0_identity_correspondence_2`, creating new packet/request provenance. The original
historical all-version schema/instructions remain unchanged. Old or rejected envelopes
are not normalized, repaired or relabeled; #73 raw response/consumed execution files were
not edited, and no paid model, Places or Routes request was made.

A downstream regression first exposed absent correspondence metadata, then a missing V0
identity verdict on route legs. Current records now retain `candidate_correspondence`
separately from original-claim `grounding_verdict`; coordinate/opening/route consumers
preserve V0 verdict metadata as well as programmatic verdicts. Recognized wrong addresses
and different venues remain FAIL with null canonical IDs and no corrected endpoints.
Insufficient correctness evidence stays UNKNOWN. Quality and requirement descriptors
retain the original identity records; score formulas, denominators and generation are
unchanged. Synthetic snapshot tests check these behaviors through public consumers.

The regression harness was corrected for required acquisition ceilings, the existing
coordinate status (`complete`), the quality report's `primary_metrics` location and the
identity CLI's decisive-FAIL exit code (`0`). These were test assumptions, not production
contract changes. After the citation/address/import and consumer corrections, the related
identity/program/historical/offline-SDK gate passed **111 tests in 14.22s**. The pre-review V0
contract gate passed **40 tests in 4.33s**. No live POI names were added as reusable fixtures.
Global Ruff lint (`backend tools scripts`), six changed-file format checks and changed-module
Python compilation passed. No configured mypy/pyright or remote CI result is claimed.

The first serial full backend gate reported **2907 passed, 10 skipped, 1 failed in 275.48s**.
The evaluator architecture guard rejected the new `copy` import, which is outside its
standard-library allowlist. Schema cloning now uses the existing JSON roundtrip, without
relaxing that guard or touching provider/model material. The intake/identity/program/
historical/offline-SDK correction gate then passed **249 tests, 1 skipped in 24.05s**.
Ignored local evidence identifiers are `.scratch/pytest-76-full.txt`,
`.scratch/pytest-76-full-corrected.txt` and `.scratch/pytest-76-full-final.txt`; none is a
published dependency. The intermediate corrected full run was stopped without a complete
result when review found a behavior requiring another code change; it is not a passing gate.

Independent Standards review found zero hard violations and one P3 possible duplication:
current match rows checked address presence twice. Independent Spec review found one P2:
supported destination contradictions still produced UNKNOWN, particularly when missing
addresses required `not_supplied`. Three synthetic no-address cases first reproduced
UNKNOWN for match/unknown/no-supported-match decisions. Correction commit
`4c98f56e235de6d4d96de7ce0c24052be7149c78` makes supported current V0 destination conflicts
FAIL, requires original name/destination plus independent candidate support, and preserves
historical behavior. Missing evidence rejects import rather than certifying a failure.
The late historical address guard no longer repeats the current-path check.
Additional negative citation tests briefly had a misplaced test body (three NameErrors);
restoring its public quality/route assertions resolved the harness error. The final affected
gate passed **254 tests, 1 skipped in 22.15s**, covering intake's architecture guard,
current/historical identity, program dispatch and offline SDK execution. Ruff and changed-file
format checks passed again. Both axes rechecked the committed correction with zero unresolved
code findings. A duplicated destination-conflict paragraph in the contract draft was removed.

The final serial full backend gate at `4c98f56` passed **2913 tests, 10 skipped in 276.95s**:
`.venv/Scripts/python.exe -m pytest backend/tests -q -p no:cacheprovider
--basetemp=.scratch/pytest-76-full-final --tb=short --show-capture=no`.
Global Ruff lint, six changed Python format checks and whitespace checks passed. Final
documentation checks passed 189 tracked local link targets and the new record anchor.
Both independent axes reviewed the final documentation drafts with **zero unresolved findings**.
Current contract, project status, CLI usage guide and this dated acceptance record form a
separate final documentation commit after implementation and review corrections. The only
remaining worktree edit is the unrelated pre-existing `.gitignore` change.
#77/#78/#79 remain separate scopes with their original approval gates.

<a id="fresh-v0-smoke-preparation-2026-10-06"></a>

### Fresh V0 identity smoke preparation (#77, 2026-10-06)

The user explicitly authorized #77 implementation with offline preparation only and zero
paid calls. Fixed review base is `f53c2b13922f8a6c7fad71f77bf00e9ad15b9490`, following #76,
on `feature/evaluation`. Implementation and public-interface tests are committed as
`5f0e1b4e3370c1900439bb2758d91f04d164b5d6`. The unrelated pre-existing `.gitignore` edit
remains excluded. This event prepares a reviewable request; it establishes no new live
model/Places/Routes evidence, score comparison, formal benchmark, freeze or Git publication.

The verified original bundle is the ignored local historical identifier
`artifacts/v0-identity-adoption-20261005/material.json`. Current policy recomputes **eight
V0 primary references and nine independent API candidates**, rather than assuming the old
nine-reference model population. Shared requirement subjects and V1-V3 stay on program
verification and are absent from the request. All eight originals have supplied addresses;
the missing-address contract is rehearsed separately with synthetic null-address fixtures.
The real current pending report retains **eight V0 UNKNOWN** results and zero non-V0
model judgments. No rejected historical response is imported or repaired.

The fresh private preparation identifier is `artifacts/v0-identity-smoke-77-20261006`.
Its manifest, pending report, complete destination/data handoff and offline audit bind
**73 source hashes and 68 implementation/dependency hashes**. The 69 original source
hashes remain unchanged; the additional protected files are the old #73 preparation and
its three consumed execution files. The original #73 execution directory remains present
and untouched; the newly bound execution directory does not exist. Token sizing uses the
already cached, hash-checked local o200k vocabulary, with **12,652 tokens including 1,024
reserve**. No tokenizer download or model client is allowed during actual preparation.
Raw claims, candidate payloads, private endpoint and secrets are excluded from tracked docs.
These local identifiers are evidence references, not dependencies for public instructions.

The concrete frozen preparation has manifest SHA-256
`14304cf36f3e138011e3a1b3ae5f79b002026cc874d66148d12eb233786ce096`
and wire-request SHA-256
`ffc53c919ddc9b51a59b720a019f0197d1058222fd71263ef8a57a042d584d56`.
The private handoff names source revision `5f0e1b4`, configured HTTPS Responses destination,
original/candidate data scope, exact command/digest, credentials prerequisites, output
paths, stops and the request-local reference map. Request proposal: **one `gpt-6-luna`
call with low reasoning**, `store=false`, no tools, 16,000 input/3,000 output caps,
60-second HTTP timeout and zero retries. Google, planner and Routes request counts are zero.
This is a fresh proposal, not reuse of #73's consumed approval.

[Official model pricing](https://developers.openai.com/api/docs/models/gpt-6-luna) and
[cache usage](https://developers.openai.com/api/docs/guides/prompt-caching) were checked
2026-10-06. Standard reference rates per million tokens are USD 0.10 ordinary input,
0.01 cached input, 0.125 cache writes and 0.50 output; output already contains reasoning.
Maximum uncached reference at the proposed caps is USD 0.0031, maximum standard input
category reference is USD 0.0035, and a regional +10% scenario is USD 0.00385. The new
proposed allowance is **USD 0.004**. This proxy cannot guarantee a Foundry invoice ceiling;
provider SKU, tier, credits and tax are unverified. Execution preserves raw usage and
prices supplied cache categories separately. Missing category counts produce an explicit
conservative reference upper bound, not invented zero usage; invalid/overlapping category
counts stop import. Provider invoice remains unavailable.

Public-interface TDD first reproduced absent preparation metadata, then old token limits,
ignored cache categories and invalid category acceptance (seven failing pricing cases).
The relative-material-root regression reproduced resolving source files against the process
directory instead of the bundle directory. Credential-free CLI preparation first rejected
the new explicit endpoint argument. Corrections now emit schema version 2, a pending report
and handoff, apply the new proposal/categories, resolve relative roots correctly and avoid
credential loading for explicit offline destinations. The first preservation test briefly
failed because its new `Path` import was missing; adding it corrected the harness.

The default Windows sandbox hung creating an asyncio loopback socketpair before synthetic
fixture setup. A faulthandler stack identified that restriction; the incomplete runs were
stopped and are not passes. Offline pytest was then run outside that shell restriction,
with repository external-network guards and injected HTTP transports still active. No
paid invocation occurred. Actual preparation additionally prohibited DNS, socket connection
and model-client creation. The executor gate passed **29 tests** before the final CLI slice;
the related executor/current/program/historical/adoption gate passed **138 in 29.98s**.
It covers successful matching, confirmed FAIL, legitimate UNKNOWN, invalid citations,
null addresses, changed sources, raw evidence preservation and terminal attempt consumption.
Global Ruff lint, two changed-file format checks and whitespace checks passed.

Independent Standards review of the committed implementation and concrete handoff found
zero findings. Independent Spec review found one P3 private-handoff navigation typo:
the supplemental pointer used `reference_map` instead of the actual `reference_maps`.
The pointer and private handoff audit hash were corrected; manifest/wire/source hashes
remain unchanged. The private correction receipt preserves the previous/new handoff hashes.
No tracked implementation correction was needed. The final serial full backend gate at
`5f0e1b4` passed **2926 tests, 10 skipped in 283.85s**:
`.venv/Scripts/python.exe -m pytest backend/tests -q -p no:cacheprovider
--basetemp .scratch/pytest-77-full --tb=short --show-capture=no`.
Its ignored local evidence identifier is `.scratch/pytest-77-full.txt`; it is not a public
dependency. Global Ruff, two changed Python format checks and whitespace checks passed
again. Documentation validation passed **174 tracked local link targets/anchors** and
English-only added text. All 73 source and 68 implementation hashes still match; the new
execution directory remains absent. Both independent axes reviewed the final documentation
and corrected handoff with **zero unresolved findings**. Current contract, operational
guide, project state and this dated record are saved in a separate final documentation
commit. The unrelated `.gitignore` edit remains the only intended unstaged worktree change.

Actual preparation sends and incremental charges are **zero**. Any subsequent live test
requires explicit approval of this new exact manifest/limits and a current-session execution
child configured `gpt-6.1-sol` / `medium`. HTTP success must be reported separately from
accepted import; raw/usage/error evidence and failed directories must remain preserved.
FAIL/UNKNOWN are valid results, without an all-match/PASS target. The old #73 failure and
UNKNOWN evidence remain until genuinely new accepted evidence exists. #78 route integration
and #79 publication remain separate scopes; no full planner rerun or version expansion is
authorized here. The Issue remains a tracker-owned lifecycle item; this local record does
not claim closure or authorize a send.

<a id="evaluator-iteration-delivery-preparation-2026-10-06"></a>

### Evaluator iteration delivery preparation (#79, 2026-10-06)

The human authorized local delivery material only, with zero paid calls and explicitly
deferred push, PR creation and merge. This scope includes read-only remote inspection,
commit/diff inventory, independent combined review, PR/Issue reconciliation drafts,
current-state documentation and local commits. No branch switch, Issue mutation,
implementation change, new smoke freeze or paid execution is included. Starting local
head is `92f92fe85c48a501c08dba16858a60947fd43563` on feature/evaluation; the only
pre-existing worktree change is the unrelated `.gitignore` edit, excluded and preserved.

#### Actual delivery range and corrected historical assumptions

Read-only GitHub checks verify `main` at
`a983f350f9d3f1e943b4f2acf63af641ab676f85` and remote feature/evaluation at
`819f0c3c5956c43f6c799feb128fb5a74bb4f2f5`, matching the local remote references.
[PR #80](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/80) is MERGED at
that main commit (2026-10-05T17:10:26Z); no open PR exists for feature/evaluation.
Historical #67/#70/#72/#73 are already CLOSED. Thus the ticket's instruction to include
earlier unpublished work is resolved from actual state: those historical changes are
already published, not new outgoing changes and not reasons to reopen their Issues.

The fixed combined-review command is
`git diff a983f350f9d3f1e943b4f2acf63af641ab676f85...92f92fe85c48a501c08dba16858a60947fd43563`;
its merge-base is `819f0c3`. The completed-slice range has **ten commits, 32 changed
files, 2718 insertions and 168 deletions** before this preparation documentation:

| Commit | Slice and purpose |
| --- | --- |
| `ffa36a4` | #75 version dispatch, independent API evaluation, consumers and tests |
| `a53aa81` | #75 separate review correction for local malformed requirement evidence |
| `1bd4057` | #75 current contracts and acceptance |
| `0e5aba6` | #76 supported V0 citations and absent-address output/import contract |
| `4c98f56` | #76 separate supported destination-conflict correction |
| `f53c2b1` | #76 correction and validation record |
| `5f0e1b4` | #77 fresh offline V0-only smoke preparation and rehearsal |
| `769a066` | #77 preparation evidence and approval boundary |
| `571ed95` | #78 current-policy route readiness and public-interface tests |
| `92f92fe` | #78 current route contract and real blocked-package evidence |

The proposed normal publication would push the existing feature/evaluation branch,
then, if separately authorized, create a new PR targeting main. Merge is a further
explicit action; current authorization stops at local preparation. Final preparation
documentation is a separate local commit appended to this inventory, without rewriting,
amending or squashing prior implementation/correction commits. Exact final head is
recorded in the local delivery manifest and chat closeout after the documentation commit.

#### Validation, reviews and limitations

The root inspected the complete changed-file inventory, implementation/consumer diff,
contracts and dated records; independent Standards and Spec reviewers each inspected
the full fixed 32-file diff and all ten commits. **Standards: zero actionable findings.
Spec: zero findings.** No implementation correction is needed. The earlier #75/#76
review findings remain in their original dated sections with separate correction commits;
combined delivery review does not erase those failures or replace their validation sequence.

The serial full backend result at `571ed95` is reused: **2945 passed, 10 skipped in
414.43s**; the related identity/route/coordinate gate passed **178**. These counts
overlap. No Python, planner, dependency or configuration file changed after that tested
state; no new full run is claimed. Delivery checks pass global Ruff and formatting for
all **24 changed Python files**. No configured mypy/pyright or new PR CI result is claimed.
Initial document verification caught a newly drafted route-contract anchor that did not
exist. The link was corrected to the existing contract anchor without changing runtime
behavior; repeat checks pass **257 tracked local Markdown targets/anchors**, English
added content and whitespace. The **81 protected source hashes** remain unchanged.
Independent final preparation-material reviews also report **Standards: zero actionable
findings; Spec: zero findings**, covering current-state documentation, PR draft, Issue
map and manifest/audit material. No code correction or further backend test run is needed.
Excluded-path/content inspection and a credential-shape scan find no secrets or ignored
raw/scratch files in the proposed diff; the heuristic scan is not a proof of all secret absence.

The [current identity contract](../../contracts/0002-intake-identity-usage.md#version-specific-identity-requirement)
and [route contract](../../contracts/0004-opening-routes.md#route-preparation-and-wire)
represent deterministic V1-V3 checks, V0-only correspondence, exact replay and
no-repair FAIL/UNKNOWN propagation. Generation and scoring arithmetic are unchanged.
The [#78 record](routes.md#versioned-v0-route-readiness-2026-10-06) remains the actual
real-package evidence: **four UNKNOWN/blocked original legs, zero eligible endpoints,
Details/Routes requests and proposed acquisition budget; 81 protected file hashes unchanged**.
Synthetic tests demonstrate policy behavior, not actual venue/route accuracy.

#73's HTTP-success/import-failure, nine UNKNOWN verdicts, raw response and consumed
allowance remain preserved. No fresh accepted real current-policy V0 model report exists.
#77's original offline preparation checkpoint contains eight V0 references and nine
independent candidates, but #78 changed two frozen implementation files. Its preserved
manifest is stale for execution. No refreeze occurs here; a future smoke needs a fresh
exact freeze, separate approval and the required current-session execution child.
Paid smoke is not required to publish offline-validated implementation/preparation.

#### Prepared materials and pending tracker actions

Ignored `.scratch/delivery-79/` contains `manifest.json`, `commits.txt`, the full proposed
diff, a self-contained English PR title/body draft and an Issue reconciliation draft.
These paths are private preparation identifiers, not published document dependencies
or an alternative live specification. The manifest binds the actual local head, base,
commit list, code blobs, diff digest and reused test state. No raw provider/model payload,
endpoint credential or runtime artifact is promoted into it or tracked documentation.

Read-only Issue snapshots observe #74-#79 OPEN. The local map proposes evidence-based
acceptance reconciliation only after authorized publication/readback; no automatic closing
references are added. Historical #67/#70/#72/#73 closures remain intact. Any #77 closure
must state completed historical offline preparation without claiming current executability.
#79's publication/readback/reconciliation criteria remain pending, so neither it nor
parent #74 is described as fully complete. Stale parent implementation statements are
listed for later authorized synchronization, not silently updated in the tracker now.

Before any approved publication, refresh remote main/source heads, local head and existing
PR state; reassess changed scope before pushing. PR creation requires its own approval
and attachment/readback; merging and Issue reconciliation require their applicable explicit
authorization. This local preparation has **zero new model/Google/planner sends, zero
incremental charges and zero remote mutations**. It establishes no version freeze,
formal benchmark/comparison, thesis result or research conclusion.

<a id="evaluator-iteration-publication-2026-10-06"></a>

#### Authorized publication and pre-merge checkpoint (2026-10-06)

After the local preparation above, the human explicitly authorized normal push, PR
creation, review followed by a published comment and merge, plus closure of associated
Issues only if all acceptance conditions are met. Zero paid calls remains binding.
This supersedes the preparation-only Git boundary; it does not approve a live smoke,
force push, history rewrite, branch deletion or branch switch.

Normal push published `3f2143b7a58e46cf6597cd5cf400ff5bfa737531` to feature/evaluation.
Remote readback confirmed the exact head. Newly created
[PR #81](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/81), attached to the task,
targets main at `a983f350f9d3f1e943b4f2acf63af641ab676f85`. Its initial readback confirms
the prepared **11 commits / 32 files**, a non-draft, mergeable/CLEAN PR and an empty
check rollup. No new configured CI outcome exists; absence of checks is not a passed CI.
The repository permits merge commits, which retain the implementation/correction history.

This authorization/current-state documentation is an additional local documentation
commit, published into the same PR before final review/comment/merge. The actual final
head and independent Standards/Spec outcomes are recorded in the pre-merge PR comment;
the fixed base and implementation content retain the earlier full combined-review scope.
No Python, planner, dependency or configuration change follows the tested `571ed95` state.
The reused **2945 passed / 10 skipped** full backend and **178** related gate remain valid;
fresh backend or live validation is not claimed. Final document/exclusion/hash checks cover
this additional documentation delta, with the unrelated `.gitignore` bytes preserved.

The original #73 rejected response/consumed allowance and all 81 protected file hashes
remain unchanged. The real current route package still has four UNKNOWN/blocked legs and
zero eligible endpoints, acquisition requests or proposed budget. #77 remains historical
offline preparation with a stale execution manifest, requiring a fresh exact freeze and
separate approval for any future send. Its completion never certifies current executability.

At this pre-merge checkpoint, #74-#79 are OPEN. After verified merge, authorized
reconciliation checks existing acceptance wording, preserves historical decisions and
adds self-contained evidence before closing only fully met scopes. #67/#70/#72/#73 stay
closed without repeated mutations. Actual merge and final lifecycle outcomes belong to
the linked PR/Issues; this pre-merge record does not anticipate their success. No paid
call, new original-output repair, scoring change, formal evaluation or freeze occurs.

<a id="post-merge-v0-smoke-refresh-2026-10-06"></a>

### Post-merge V0 smoke refresh (#82, 2026-10-06)

The user explicitly authorized a follow-up Issue and refreshed offline plan, with zero
paid calls and no execution. [Issue #82](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/82)
owns this preparation and a separately gated future execution slice. Completed #74-#79
remain historical acceptance; #77's preserved plan is stale after #78 changed
`route_requests.py` and `route_requests_cli.py`. It is not silently updated or retried.

Fixed review/source base is `e6cd6e5eb38cf02fb12316a50d9cf4e439f22381` on
`feature/evaluation`. Merged main `e2ff2a722f03eaddeb0ff3655768e30c6da4990a` has the same
tree `74d90ef5d127c1eb92d7ecde96a465f1b0f7b606`. These are the resulting refs after the
user-authorized compression of three docs commits and remote main history update;
PR #81's historical merge receipt retains `eae5411` and its original published head.
This refresh makes no new Git publication or history change. Only current/dated
documentation changes are tracked; the unrelated `.gitignore` edit remains excluded.
No runtime, dependency, generation flow, V0-V3 behavior or scoring formula changes.

The new private preparation identifier is `artifacts/v0-identity-smoke-82-20261006`.
Its manifest, pending identity report, handoff and offline acceptance receipt bind
**91 source hashes and 68 implementation/dependency hashes**. The expanded source guard
includes original material, #73 consumed failure evidence, the stale #77 preparation,
and #70/#78 route material. All protected bytes remain unchanged. The new execution
directory is absent; preparation blocks DNS, socket connections and model-client creation.
The exact configured HTTPS Responses destination and configuration prerequisites stay
in the private handoff, alongside source revisions, command/digest and output paths.
The reference map is `packet.reference_maps`; cases are in `wire_request.input` JSON.
Private raw claims/candidates, destination and secrets are excluded from tracked material.
Local identifiers here are evidence references, not public navigation dependencies.

Current scope is **eight V0 primary references and nine independent API candidates**,
all eight original addresses supplied. Shared requirement subjects and V1-V3 remain
programmatically verified outside the model request. The eight pending V0 UNKNOWN
verdicts are byte-identical to #77's pending report; no fresh accepted real model result
exists. The four preserved route legs remain UNKNOWN/blocked with zero acquisition
requests. Raw output is not repaired, and all-PASS is not an acceptance target.

New canonical manifest SHA-256:
`c3f59f878c0e060d3c4fd3248d1f75d5e78ccf669f307f2de3bd78f6b39f9e20`.
Wire-request SHA-256:
`ffc53c919ddc9b51a59b720a019f0197d1058222fd71263ef8a57a042d584d56`.
The wire is intentionally unchanged: #78 changed the implementation inventory, not
the V0 request/schema. The new manifest binds current hashes, expanded preservation
and a fresh directory; an unchanged wire never renews the old approval.

Proposed request: **one `gpt-6-luna` call, low reasoning, `store=false`, no tools**;
16,000 input/3,000 output token caps, 1,024 input reserve, 60-second HTTP timeout and
zero retries. Offline sizing remains **12,652 tokens including reserve**, using the
cached tokenizer with networking prohibited. Google, planner and Routes proposals are zero.
[Official model prices](https://developers.openai.com/api/docs/models/gpt-6-luna) and
[cache categories](https://developers.openai.com/api/docs/guides/prompt-caching) were
rechecked 2026-10-06: per million tokens USD 0.10 ordinary input, 0.01 cached input,
0.125 cache writes and 0.50 output. Input categories partition the input total; output
already includes reasoning. The standard maximum reference is USD 0.0035, regional
+10% scenario USD 0.00385, and proposed fresh reference allowance USD 0.004. These
are retail references, not an established Foundry service tier or invoice ceiling.
Actual incremental preparation charges are USD 0; provider invoice remains unavailable.

Fresh offline executor/current-contract/route tests passed **100 in 46.65s** using
synthetic fixtures and injected transports. They cover preparation without credentials,
V0-only routing, complete owned decisions, citations, missing original addresses,
successful correspondence, confirmed FAIL, legitimate UNKNOWN, source changes, usage
categories and terminal attempt consumption. Test attempts use separate synthetic
directories, never the actual new execution directory. The first scratch launcher used
an unsupported relative Python module name and exited before preparation; the corrected
`runpy.run_path` launch prepared successfully. No code correction or new test was needed.
The ignored local test receipt is `.scratch/pytest-82-offline.txt`. The earlier full
backend **2945 passed / 10 skipped** at `571ed95` still covers unchanged runtime code;
it is reused evidence, not a fresh full-suite or CI result. No new live evidence exists.

Only separate approval of this exact new manifest/destination/data scope/limits may
authorize a future send, after hash revalidation. Dispatch must then use a current-session
`gpt-6.1-sol` / `medium` execution child; none is dispatched now. One attempt consumes
its directory even on error. Preserve raw bytes, usage and failures; distinguish HTTP
success from accepted import. Invalid/partial/foreign/citation/usage/source results stop;
legitimate FAIL/UNKNOWN remain valid imports with original claims and null canonical
endpoints. #73's consumed allowance remains consumed. Issue #82 stays open for the
unapproved future slice; no paid send, push, PR, merge, formal run or freeze is authorized.

<a id="v0-identity-smoke-execution-2026-10-06"></a>

### Approved V0 identity smoke execution (#82, 2026-10-06)

After the offline refresh and parameter explanation, the user explicitly approved the
V0 identity smoke in the current session. This supersedes the preparation-only boundary
for exactly one frozen attempt, not any further request or Git publication. The
[approval receipt](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/82#issuecomment-6007810684)
binds canonical manifest
`c3f59f878c0e060d3c4fd3248d1f75d5e78ccf669f307f2de3bd78f6b39f9e20`, private destination,
eight primary V0 references/nine independent supplied candidates and the existing
token/time/zero-retry/USD 0.004 retail-reference limits. Current source and documentation
review base are `1220da6720ac65f7289a53c45b881515ed5673bf` on `feature/evaluation`;
no runtime changes follow the frozen `e6cd6e5` implementation. The unrelated `.gitignore`
edit remains excluded. All 91 source and 68 implementation/dependency hashes matched
before dispatch; credentials were present, destination/deployment matched and the
bound execution directory was absent. No secrets or private endpoint are recorded here.

Only the current-session `gpt-6.1-sol` / `medium` execution child ran the exact approved
`identity_judgment_smoke execute` command, once. The provider request itself used
`gpt-6-luna` / `low`, with `store=false` and no tools. Process exit was **0**; the
request started at **2026-10-06T02:04:58.521275+00:00** and the complete raw response
was retrieved at **2026-10-06T02:05:04.486105+00:00**. HTTP was **200**, provider status
`completed`, with no reported error/incomplete code. Actual sends were **one model,
zero retries, zero Places/Google, zero Routes and zero planner**. No additional request
was dispatched, and there was no configured-limit or scope deviation.

HTTP success is distinct from accepted import. The complete source-bound response
imported successfully through `versioned_api_identity_1`: all **eight V0 primary
references are PASS**, with `match` correspondence; none are FAIL/UNKNOWN in this
particular response. A separate requirement subject was excluded from the model
request and remains **UNKNOWN**. Consequently the overall identity report is still
**`needs_evidence`**. These are observed outcomes, not an all-PASS requirement or a
claim that every user requirement has independent verification.

Reported usage: **10,842 input tokens**, partitioned into **10,839 cache-write,
zero cached and three ordinary input tokens**; **808 output tokens**, including
**zero reported reasoning tokens**; **11,650 total tokens**. Zero reported reasoning
tokens do not change the requested `low` setting or establish an absence of internal
reasoning. At the frozen retail-reference rates, standard cost is **USD 0.001759175**;
the regional +10% reference scenario is **USD 0.0019350925**, both below USD 0.004.
The receipt basis is `reported_categories`, not a missing-category estimate. These
reference calculations are not actual Foundry billing: invoice, SKU/tier, credits
and tax remain unavailable. No model fee of zero is claimed for this live request.

The consumed private execution identifier is
`artifacts/v0-identity-smoke-82-20261006/execution`. It retains `response.bin`,
`execution.json`, `model-result.json` and `identity-report.json`. Raw response SHA-256:
`dbf3ff340a86ee7a7b771736ab26759b8c29c103b8751bb1be1bac8e4180fe7d`.
The immutable original #73 failure/consumed allowance, #77 stale preparation and
#70/#78 route material remain intact. Old pending reports are not overwritten by
the new accepted report; their UNKNOWN verdicts retain their historical meaning.

Parent assessment was entirely offline, with DNS/socket connection prohibited. It
verified all protected/source implementation hashes, receipt/raw/model-result digests,
and exact replay of the accepted identity report against original material. All
original claims and all non-V0 records are unchanged. FAIL/UNKNOWN canonical-null
invariants remain checked without repairing output. The private assessment identifier
is `artifacts/v0-identity-smoke-82-20261006/execution-assessment.json`; it is local
evidence, not a public document dependency. No runtime correction or new test was
required; the preceding **100 passed** fixture gate and unchanged-code full backend
gate are reused, not new test/CI runs or repeated live validation.

This is bounded development smoke evidence, not a formal benchmark, human review,
version comparison, freeze, scoring run or route feasibility result. Preserved
route packages retain their original blocked outcomes; no route package or score
was regenerated. Any route preparation/acquisition or further identity attempt
requires its own approved scope. The one-call directory and allowance are consumed;
do not delete/regenerate them to retry. Issue #82 owns final acceptance and lifecycle;
local documentation does not anticipate remote closure or authorize push/PR/merge.

<a id="version-owned-requirement-targets-2026-10-06"></a>

### Version-owned requirement targets (#83, 2026-10-06)

The user approved a follow-up Issue, offline implementation, local commits and independent
Standards/Spec review. [Issue #83](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/83)
owns the self-contained scope. Review fixed base is
`2bfe17cc12cde0f5b4dd5b8be04ae54e57f68af9` on `feature/evaluation`. The pre-existing
`.gitignore` edit remains excluded. This approval authorizes no model/provider execution,
paid request, push, PR, merge, branch switch, formal comparison or version freeze.

The original shared program target was inconsistent with the approved V0 correspondence
path. The new design shares reviewed RequirementSpec meaning and independent acquisition
evidence, while keeping target identity judgments owned by each submitted version. V0
primary visits and requirement targets use V0-only supplied-candidate correspondence;
V1-V3 use independent program checks with no model dependency or fallback. Each version's
required/excluded/fixed-time checks compare its adopted visit and target IDs before
counting dates, times or visits. Final/optional projections of one version share that
version's target. Current report/packet policies are `versioned_api_identity_2` and
`v0_identity_correspondence_3`; old packets cannot establish new judgments. Generation,
scoring arithmetic, original output and route FAIL/UNKNOWN populations are unchanged.

For unbound V1-V3 targets, complete provenance-linked search evidence is strictly filtered
by original literal name, destination and supplied address before adopting one distinct
ID. Zero/multiple surviving IDs, a saturated page, retained pagination, incomplete or
malformed evidence remain UNKNOWN. Duplicate-ID facts must agree. Typed sublocality levels
are separate; explicit locality/administrative-region and country values can support the
original destination without translation, fuzzy matching, rank selection or inference.
Proven errors remain FAIL, and no canonical ID is adopted for FAIL/UNKNOWN.

Implementation and directly related regressions were committed before review as
`0fe87c9` (`fix: scope requirement target identity by version for #83`). Public-seam
TDD first reproduced shared target ownership, premature multi-hit rejection, typed
address handling, borrowed requirement results, missing provenance and conflicting
duplicate-ID acceptance. Fixes made the targeted cases pass. An existing smoke fixture
still expected two references after the V0 target was added; its scope assertion was
updated. The intermediate relevant gate reached **150 passed / 1 failed**, followed
by **58 passed** for the new target tests and smoke preparation tests.

Independent initial review found **one Standards P2** and **two Spec P2s**. New regression
tests reproduced historical paginated coordinate replay failure (one failure), falsey
malformed pagination acceptance (six failures), and city components masking explicit
region/district destinations (two failures). Separate correction commit `904e318`
(`fix: preserve historical evidence and strict target checks for #83`) keeps original
evidence derivation on replay-verified historical reports/material/CLI/route paths,
preserves pagination on current reports, rejects malformed pagination and supports the
explicit region values. The snapshot CLI now exposes historical wire derivation
explicitly. Both reviewers rechecked all committed changes against the fixed base:
**zero remaining Standards findings; zero remaining Spec findings**. No review correction
was amended into the implementation commit.

The final focused gate passed **87 tests**, including the current target contract,
historical paginated coordinates and V0 route material, and offline smoke-tool tests.
Ruff, evaluator compile checks and whitespace checks passed. The first full backend run
completed with **2971 passed / 10 skipped / 2 failed**. One failure was a stale route-test
policy assertion, corrected in `904e318` and passing the focused gate. The other is the
untouched V3 whole-request 0.1-second timeout test: isolated rerun reached a different
pre-primary failure boundary, and an extracted fixed-base Git snapshot reproduced
`runtime.closes == 0` versus expected one. No planner/runtime/test-version files differ
from that baseline. This is an existing environment-sensitive test limitation, not a
green full-backend result; changing generation or expanding into V3 is outside this
Issue. Early Windows sandbox/temp-path failures were rerun with fresh task-local pytest
directories and the normal external-socket prohibition; asyncio internal loopback was
allowed. No external provider connection was made.

The complete evaluator rerun passed **1053 tests / 1 skipped** after the corrections
(329.35 seconds). Its snapshot-CLI pagination test was also exercised by the final
87-test gate after the CLI change. Private test receipts are
`artifacts/identity-83/full-01.txt`, `evaluation-final-02.txt` and `review-green-02.txt`
in that directory. These document separate actual runs, not a recomputed all-green
full-backend result. No further broad rerun was needed after the passing relevant gates.

Final DNS/socket-blocked assessment verified all **91 original source hashes**, all
**four #82 execution files** and exact historical report replay. The new offline-only
packet has **nine V0 references: eight primary visits and one requirement target**, with
**14 candidate appearances**. Exact regeneration matches its saved packet. Its local
evidence identifiers are `artifacts/identity-83/offline-v0-packet.json` and
`artifacts/identity-83/final-offline-assessment.json`; these are private aids, not public
document dependencies. Actual model/Places/Routes/planner sends are **zero**, incremental
paid calls **zero**. No new live result, execution manifest or allowance is claimed.
The eight old PASS visits and historical requirement UNKNOWN remain unchanged under
their original policy. A future complete nine-reference result requires separately
approved preparation/execution and cannot reuse the consumed #82 allowance.

The user subsequently approved offline diagnosis and correction of the recorded V3
baseline failure. The separately owned
[V3 deadline-phase record](../v0-v3/v3-development.md#deadline-phase-regression-2026-10-06)
documents the phase-selection test assumption and stronger public-entry regressions,
without production code or generation changes. Its fresh full backend run passed
**2983 tests / 10 skipped / zero failures**. This resolves the baseline limitation for
the current offline gate while preserving the original failure/retest account above;
it adds no live evidence or Git publication authorization.

<a id="requirement-target-delivery-2026-10-06"></a>

### Authorized requirement-target delivery (#83, 2026-10-06)

After all offline acceptance items passed, the user explicitly authorized push, PR
creation, published review, conditional merge and closure of #83. The source branch
`feature/evaluation` was fast-forward pushed from `e6cd6e5` to `42fce73`; no force push,
history rewrite, branch switch or branch deletion occurred. It carried seven local
commits: the #82 preparation/execution records, #83 implementation and separate review
correction/acceptance, and the V3 deadline-phase correction/acceptance. The unrelated
`.gitignore` edit remains excluded. [PR #84](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/84)
was created against `main` at `e2ff2a722f03eaddeb0ff3655768e30c6da4990a`.

The complete combined release is reviewed from that fixed main baseline through the
actual published PR head. The fresh **2983 passed / 10 skipped / zero failures** backend
gate is valid for its unchanged code, configuration and dependencies; later delivery
documentation is checked separately. Ruff, compile and tracked-document checks passed.
The repository has no CI workflow, configured mypy/pyright gate, branch protection or
ruleset at this checkpoint; absent checks are not reported as CI passes. Normal merge
is selected to retain implementation and correction history. Published Standards/Spec
conclusions and final merge/Issue lifecycle are owned by PR #84 and Issue #83; creation
does not anticipate a successful merge before review completes.

This approval supersedes the preceding no-publication checkpoints only for this Git
delivery. It authorizes zero new model, Places, Routes, planner, database or embedding
service calls, zero paid execution and no smoke, formal evaluation or version freeze.
The prepared nine-reference packet and consumed historical #82 allowance remain unchanged.

<a id="v0-target-smoke-refresh-2026-10-06"></a>

### V0 visit/target smoke refresh and input-limit block (#85, 2026-10-06)

Status: offline preparation and bounded sizing validated; executable preparation blocked.
The user authorized follow-up Issue creation and offline plan refresh, with zero paid
calls. [Issue #85](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/85) owns
the live follow-up state. The source baseline is the completed #83/#84 merge
`5dee3b97df79d0267a8c6d0bb2205d68106a2bdf`; preparation HEAD
`2da623932b5e07accc67103738103e2e2e8fcaa3` has the same tracked tree. The branch remains
`feature/evaluation`, and the unrelated unstaged `.gitignore` edit is preserved and
excluded. No production code, tests, configuration, dependencies, generation flow,
score formula or V1-V3 behavior changes in this refresh.

The current `v0_identity_correspondence_3` packet replays exactly from preserved material:
**nine V0 references = eight primary visits + one V0 requirement target**, with
**fourteen candidate appearances**. The target now belongs to V0's correspondence path;
V1-V3 retain program identity checks and receive no model evidence or fallback. Original
claims and all supplied factual candidates remain intact. The old #82 report replays
under its original policy; its eight PASS and shared-target UNKNOWN are historical
results, not current-policy results. No new correspondence verdict or route feasibility
is observed here, and FAIL/UNKNOWN must remain intact in any future assessment.

#### Observed preparation failure and proposed next scope

The scratch launcher first needed the repository import path (`PYTHONPATH=.`); after
that local invocation correction, the real public preparation function rejected the
request with `Estimated input exceeds smoke allowance`. DNS, socket connects and live
SDK construction were blocked throughout actual preparation. Independent sizing with
the checksummed, locally cached o200k tokenizer measured **16,111 input tokens**, or
**17,135 including the existing 1,024 reserve**. This exceeds the unchanged 16,000
limit by 1,135. The guard runs before directory creation or any send; it behaved as
intended. This is an input-capacity finding, not an API/model failure. No vocabulary
download, credential probe, execution child, provider request or paid retry occurred.

The revised handoff is explicitly blocked; it does not include an executable dispatch
command or a `preparation.json` accepted by the executor. Approval of the blocked draft
alone cannot make the unchanged executor accept this request. The proposed next scope
is a separately authorized offline correction to the smoke-only limits and regression
coverage, followed by a fresh compatible manifest and another one-use directory:

| Limit | Current unchanged executor | Unapproved next proposal |
| --- | --- | --- |
| Input tokens, including 1,024 reserve | 16,000 | 18,000 |
| Output tokens | 3,000 | 3,000 |
| Requests / retries / HTTP timeout | 1 / 0 / 60 seconds | 1 / 0 / 60 seconds |
| Standard reference maximum | USD 0.0035 | USD 0.00375 |
| Regional +10% reference maximum | USD 0.00385 | USD 0.004125 |
| Reference allowance | USD 0.004 | USD 0.0042 |

The proposed input ceiling leaves 865 surrogate tokens beyond this reserved estimate.
The model remains `gpt-6-luna`, reasoning `low`, `store=false`, without tools. The prices
are reused from the tool's documented 2026-10-06 reference basis, without a new pricing
network request: USD 0.10 ordinary input, 0.01 cached input, 0.125 cache writes and 0.50
output per million tokens. The maximum assumes all input billed as cache writes and
counts output/reasoning once. The proposal increases the regional reference maximum
by USD 0.000275; it is not a Foundry invoice or provider-tokenizer guarantee. No budget
change is implemented or authorized for execution. Candidate truncation, a different
eight-visit scope, additional requests and repairs are not used to bypass the guard.

#### Frozen offline evidence and boundaries

The private evidence identifier is `artifacts/v0-identity-smoke-85-20261006`, containing
`blocked-preparation.json`, `pending-identity-report.json`, `handoff.md`,
`offline-acceptance.json` and subsequent offline check receipts. This is a local evidence
identifier, not a published dependency. The blocked draft binds the merged revision,
exact packet/wire request, private destination, **102 protected source/file hashes**
and **69 current implementation/dependency hashes**, current limits and the unapproved
proposal. All **91 historical source hashes**, **four #82 execution outputs** and
**ten existing #82 preparation/execution files** remain byte-identical; the #83 offline
packet is also protected. Old #82 implementation hashes are historical, not asserted
to match the deliberately changed #83 implementation.

Blocked draft SHA-256:
`f693b1d5c9e852c6ccd74f870400c3c25c37f9d240117fbbd643d69cafc3897f`.
Wire request SHA-256:
`f829b61a0b912c035f21c00033c6bb474de4ecd7d62fce46466c4e4bcd6fdc17`.
No compatible executable manifest or execution directory exists. #73 and #82 allowances
remain consumed, and their original attempts/results cannot be deleted or regenerated
for a retry. A future live request requires the compatible new manifest, separate exact
user approval and a newly dispatched current-session `gpt-6.1-sol` / `medium` child under
the [smoke policy](../../agents/smoke-tests.md). Credential prerequisites belong in the
private handoff; no credentials or private provider destination are tracked.

The unchanged-code full backend gate remains **2983 passed / 10 skipped** from the
[V3 deadline-phase correction](../v0-v3/v3-development.md#deadline-phase-regression-2026-10-06).
Fresh focused synthetic smoke tests passed **30 tests / zero failures** in 18.22 seconds,
using mock transports and the backend external-network guard. No implementation or
synthetic test needed correction. The separate real-packet capacity check reproduced
the intended pre-send rejection; fixture test success is not real-packet readiness.
Document/hash checks verify tracked links, anchors, English additions, exclusion of the
private destination, exact packet/pending-report replay and absence of runtime changes.
This preparation adds no live evidence, formal benchmark, score comparison,
route validation, version freeze or Git publication authorization. Issue #85 remains
open for the blocked prerequisite and separately approved future execution/assessment.

<a id="v0-smoke-capacity-correction-2026-10-06"></a>

#### Approved offline capacity correction and re-preparation (2026-10-06)

The user then explicitly approved only the proposed **18,000 input tokens / USD 0.0042
reference allowance**, regression coverage and offline re-preparation. Review fixed
point: `435cccfee77c0149e3c82d5e1b02d77a34031a17`. Implementation/test commit:
`ae196e2cd8de11a511f273f91943cd8028af4ddf` (`fix: raise V0 identity smoke capacity for #85`).
It changes exactly two smoke-tool constants and the directly related tests/operational
README. Reserve 1,024, output 3,000, model `gpt-6-luna` / `low`, one send, zero retries,
60-second HTTP timeout, no tools and `store=false` stay as specified. Production
V0-V3 generation budgets, identity rules, score formulas and dependencies are unchanged.
The unrelated unstaged `.gitignore` edit remains byte-identical and excluded.

The updated allowance regression first failed against the original 16,000 cap, then
passed after the two-constant correction. Five new parameterized cases verify an intact
original claim sized between the old/new input ceilings, pre-directory rejection above
the new ceiling, valid reported 18,000 input / 3,000 output at the most expensive input
category, rejection at 18,001 input or 3,001 output, preserved raw mock responses and
non-reusable consumed attempts. The focused smoke gate passed **35 tests in 13.29s**.
The preparation tests forbid live SDK construction; SDK execution tests use only
`httpx.MockTransport` and the backend external-network guard. Ruff and compilation pass.

One fresh full backend run completed with **2948 passed, 40 failed, 10 skipped in
305.95s**. It is a failed full gate, not a pass or reuse of the earlier green gate.
All failures occur in unchanged identity/route-request tests that fix preparation at
`2026-10-06T10:00:00Z` while their synthetic snapshot acquisition uses the real clock.
The first isolated reproduction returned `needs_material_correction`, diagnostic
`artifact_integrity_error` at `snapshot/time`, explanation `Identity evidence is later
than preparation`; its saved synthetic snapshot finished at
`2026-10-06T11:24:49.380188+00:00`. Restoring the original smoke constants in an isolated
process reproduces that failure (**1 failed**). Fixing only the snapshot clock to
09:00 UTC in a temporary diagnostic process makes every full-run failure pass
(**40 passed in 13.92s**). Both diagnostic processes report one pytest import-rewrite
warning; neither changes tracked code or tests. These controlled observations support
a pre-existing fixture-clock limitation, not a smoke capacity regression. The separate
route-test correction is outside the smoke-only authorization and remains unimplemented.

Local evidence identifiers are `artifacts/smoke-85-limit-validation/red-01.txt`,
`green-01.txt`, `focused-01.txt`, `full-01.txt`, `probe-01.txt`, `baseline-old-01.txt` and
`baseline-clock-01.txt` under the same directory. The prior green full gate and earlier
blocked preparation remain historical evidence; they do not erase this failure.

The new one-use preparation identifier is
`artifacts/v0-identity-smoke-85-refreshed-20261006`. Its compatible
`rtpeval_identity_smoke_preparation_2` manifest and private handoff bind implementation
`ae196e2`, the merged identity baseline and **108 protected source/file hashes plus
69 implementation/dependency hashes**. The additional six protected files preserve
the entire meaningful blocked #85 preparation/check record. Historical 91 sources,
four #82 execution outputs and ten #82 preparation/execution files remain unchanged.
The packet and exact wire are identical to the blocked nine-reference
draft, preserving all fourteen candidate appearances and the original pending report.

New manifest SHA-256:
`425a0684faeaee51763d9dc9a00467557c266df29d5c049d41e361580a4a1993`.
Wire request SHA-256 remains
`f829b61a0b912c035f21c00033c6bb474de4ecd7d62fce46466c4e4bcd6fdc17`.
The real cached-tokenizer estimate remains **17,135 including reserve**, leaving 865
surrogate tokens below the new input ceiling. At the same documented reference prices,
maximum standard reference is **USD 0.00375**, regional +10% **USD 0.004125**, within
the new USD 0.0042 reference allowance. These are offline sizing/reference scenarios,
not actual usage, a provider-tokenizer guarantee or a Foundry invoice ceiling.

The execution directory remains absent; no execution child, credential probe, planner,
Places/Google, Routes or model call occurs. Actual sends and incremental charges are
**zero**. Offline re-preparation does not approve live execution, publication, repair,
all-PASS outcomes, a formal benchmark or a version freeze. Issue #85 stays open for a
separately approved exact-plan execution and assessment; the fixture-clock limitation
must remain explicit in any subsequent delivery decision.

Independent Standards and Spec reviews of fixed base `435cccf` through implementation
`ae196e2` each report **zero findings**. The Spec reviewer separately verified all
108 source hashes, 69 implementation hashes, packet/wire/pending replay and absent
execution directory. No review correction is needed. Final documentation is checked
separately and committed after review; private raw files remain ignored.

<a id="route-fixture-clock-baseline-2026-10-06"></a>

#### Approved offline route-fixture clock correction (2026-10-06)

Status: validated offline. The user subsequently authorized fixing the fixture-clock
baseline, superseding the earlier smoke-only task boundary for these tests. Review
fixed point: `14ffd588eddd9a0a847cc473622943735f89911f`. Implementation/test commit:
`f4499f22fab74f8bd99f91d93f79794a2d19b5dd`
(`test: pin synthetic snapshot clocks before route preparation`). Only the adoption
fixture and current-policy route test module change. Production code, provider/time
validation, generation, V0-V3 identity rules, score formulas and budgets are unchanged.
The unrelated `.gitignore` edit remains excluded and byte-identical.

The feedback loop uses the public route preparation boundary under current and explicit
historical policy. Six cases test evidence one second after preparation, equal to it,
and one second before it. Before the fix, the two intended rejections passed while the
four expected valid cases failed with `artifact_integrity_error` at `snapshot/time`.
The `adoption_case` fixture now depends on a scoped `snapshot_clock` fixture, which
replaces only the synthetic acquisition module's wall clock with 09:00 UTC on the
fixture date. It remains active for that test's supplied Details acquisitions and is
restored by pytest teardown. Other snapshot tests and process/system clocks are not
globally frozen; asyncio and monotonic deadline clocks remain active.

All six initial cases then passed. Four additional cases advance the same controlled
clock for Details evidence at the 10:00 preparation boundary or one second after it,
under both current and historical policies. Equal timestamps remain valid; future
Identity or Details evidence still produces `needs_material_correction` with no partial
legs/requests. The correction stabilizes synthetic evidence construction rather than
relaxing the production rule or rewriting saved evidence.

The related adoption, identity model-contract, current/historical route-request and
smoke-tool gate passed **172 tests in 32.24s**. A fresh full backend gate passed
**2998 tests / 10 skipped / zero failures in 304.32s**. All forty original failures
are resolved in the actual tracked fixture implementation, without the prior temporary
diagnostic launcher. Ruff, formatting, compilation and whitespace checks pass. Tests
use synthetic injected transports and the backend external-network guard; no paid
provider/model/planner/Places/Routes calls or live smoke execution occur.

Local evidence identifiers are `artifacts/route-clock-baseline/red-01.txt`,
`green-01.txt`, `focused-01.txt`, `full-01.txt`, `protected-before.json` and the final
`offline-assessment.json` under that same directory. The earlier failed full run and
controlled-clock diagnosis remain unchanged historical evidence. This new green run
supersedes the unresolved fixture limitation for current offline readiness.

Offline source preservation checks confirm **113 protected file hashes** and
**69 implementation/dependency hashes** unchanged, including the fresh #85 manifest,
handoff, pending report, acceptance/check receipts and all previously protected sources.
The manifest recomputes identically with SHA-256
`425a0684faeaee51763d9dc9a00467557c266df29d5c049d41e361580a4a1993`.
Its execution directory remains absent, and no execution child is created. A separate
local handoff addendum records this resolved test limitation; the original private
smoke preparation and its earlier limitation account are preserved byte-for-byte.
This test-only change does not require a new request freeze or grant live authority.
Actual live sends and incremental charges are zero. Issue #85 remains open for separately
authorized exact-plan execution/assessment; no push, PR, merge or version freeze occurs.

Independent Standards and Spec reviews from `14ffd58` through test commit `f4499f2`
each report **zero findings**. The Spec reviewer independently verifies all 113
protected hashes and 69 implementation/dependency hashes. No correction commit is
needed; final source-preservation and tracked-document checks pass, and the current
status/evidence documentation is committed separately after review.

<a id="v0-target-identity-smoke-execution-2026-10-06"></a>

#### Approved V0 visit and requirement-target identity smoke (2026-10-06)

Status: executed and assessed. After the capacity and clock corrections above, the user
explicitly approved actual smoke for the exact prepared manifest. Execution source HEAD:
`eac3b6215bc3ef1653f0b3fc79d60845456cd960`, including reviewed smoke implementation
`ae196e2cd8de11a511f273f91943cd8028af4ddf` and reviewed fixture correction
`f4499f22fab74f8bd99f91d93f79794a2d19b5dd`. The unrelated unstaged `.gitignore` change
remains byte-identical and excluded. No production implementation changes occur in this
event; documentation is committed separately after the offline assessment.

The parent verified all 108 source hashes, 69 implementation/dependency hashes and
113 protected original/source/preparation/receipt files before dispatch. Offline preflight
blocked sockets and live SDK construction, checked saved configuration without printing
secrets, confirmed the unused execution directory and recorded a new current-session
exact-plan authorization. No credential probe or old allowance reuse occurred. The
mandatory new execution child used `gpt-6.1-sol` / `medium`; the actual API request used
`gpt-6-luna` / `low`, not the execution child's model settings.

Manifest SHA-256:
`425a0684faeaee51763d9dc9a00467557c266df29d5c049d41e361580a4a1993`.
Wire request SHA-256:
`f829b61a0b912c035f21c00033c6bb474de4ecd7d62fce46466c4e4bcd6fdc17`.
The complete nine-reference packet retains eight primary visits, one V0-owned requirement
target and fourteen candidate appearances. Limits were 18,000 input including the 1,024
estimation reserve, 3,000 output, USD 0.0042 reference allowance, one send, zero retries,
60-second HTTP timeout, no tools and `store=false`. Nothing was trimmed or repaired.

The approved CLI ran once, exited zero and recorded `completed`. Request timestamp:
`2026-10-06T12:14:24.083973+00:00`; retrieval timestamp:
`2026-10-06T12:14:31.619827+00:00` (23:14:24 to 23:14:31 AEDT on the same date).
HTTP status was 200 and provider status was completed. Actual model sends: **one**;
retries: **zero**. There were no planner/generation, Places/Google, Routes, embedding,
database or additional model requests. Both directory and allowance are consumed,
including their original raw outputs; no rerun is authorized.

Provider-reported input was **14,917 tokens**: 3 ordinary, 14,914 cache-write and zero
cached. Output was **1,064**, including **203 reasoning** tokens; total was **15,981**.
Reasoning is already part of output and is not billed twice. Standard retail reference
was **USD 0.00239655**, regional +10% **USD 0.002636205**, using reported categories and
the prepared documented price basis. Both are below the reference allowance. The actual
Foundry invoice is unavailable; these references are not an actual billed charge.

Import under `versioned_api_identity_2` / `v0_identity_correspondence_3` produced
`complete`: **8 primary_visit PASS and 1 requirement_subject PASS; 0 FAIL, 0 UNKNOWN**.
All nine correspondence decisions were `match` with `model_match` grounding reasons;
review and judgment queues were empty. The V0 requirement target resolves to an API
candidate through V0 model correspondence. Its original address remains null and its
address assessment is `not_supplied`; the model did not supply or repair the original
claim. This result is specific to the current V0-owned target and does not reinterpret
#82's historical shared-target UNKNOWN.

Parent assessment blocked networking and live SDK construction, replayed the saved
response through the public identity resolver and obtained the exact saved report.
Original claims and every non-V0 record match the pending report. All **108 source
hashes, 69 implementation/dependency hashes and 113 protected historical/preparation
files** remain unchanged. V1-V3 receive no model judgments; no downstream route or score
run is inferred from their unchanged records. FAIL/UNKNOWN remain legitimate retained
outcomes under the contract, although this particular run has none. No human adjudication
or formal benchmark was performed.

Raw response SHA-256:
`8225a4cb6623d2606f0e9f36c4871c714fcf6294fe0ac985542699b85a0c0d4f`.
Local-only evidence identifier: `artifacts/v0-identity-smoke-85-refreshed-20261006`.
It preserves `live-authorization.json`, `execution/response.bin`, `execution/execution.json`,
`execution/model-result.json`, `execution/identity-report.json` and the parent's separate
`execution-assessment.json`; all four execution output hashes are recorded in that
assessment. Raw provider payloads, private handoffs, endpoint and credentials remain
untracked. The child reported a process deviation: a private handoff was emitted into
its tool output during the initial read, without credential values; no raw provider body
was printed. A local default-encoding read failed and was corrected to explicit UTF-8,
without another model request. These do not change the single-send receipt.

The prior full backend gate **2998 passed / 10 skipped / zero failures** and independent
Standards/Spec **zero findings each** remain valid for the unchanged implementation.
This event adds exact offline replay and documentation/link/hash checks, rather than
repeating the unchanged full suite. #85's execution/assessment acceptance is satisfied;
GitHub owns its reconciled lifecycle. No Git push, PR, merge, formal comparison, score
conclusion, route validation or version freeze is included. Any further live acquisition
or model request needs its own approved scope and budget.

<a id="sydney-v0-identity-smoke-2026-10-07"></a>

#### Sydney natural-input V0 identity execution and assessment (2026-10-07)

Status: executed and assessed as an identity-only development smoke. The user approved
the next step after natural-input generation and had authorized prepared bounded smoke
execution without another prompt. Source HEAD was
`961eb750ed827016ec9d5cab83661671faad2672`. The unrelated `.gitignore` addition remained
byte-identical and excluded. No tracked planner/evaluator implementation changed.

The original natural input/result retain SHA-256
`1b3c50ad9ce9c58a4caf047388f3c4131faa0cddb0ffff2467dd8b2f1593d6ba` and
`d8ca6c8ac44aa2438f2efe65534b57488be81dbed217bc7d66626801f78431c7`.
An explicitly labelled single-source library view reuses current projection and identity
modules. It is not qualified four-version batch intake or final quality scoring; no missing
versions were fabricated. Parent agent source review covers only the named Opera House
obligation and retained natural soft preferences, not full requirements or human acceptance.
The target address remains null and is independent of the generated visit's address.
Seven original primary visits and one required target produce eight searches. Two optional
recommendations are listed separately, unverified and excluded from primary counts.

The one-use private adapter froze 134 acquisition dependencies and 153 model dependencies.
Acquisition digest:
`c71005079bd782ff212690d2c5783635b66fc22be6e33ccd6117657982ea7724`.
Model preparation digest:
`c8009011cf4201818f153f80ea6cead5935b1e4168325dd62c42de4d42310bb8`.
SDK-wire offline interception passed, retaining all eight cases and thirteen candidate
appearances. Input estimate including the 1,024 reserve was 15,827, below 18,000.
Mock empty results remained pending UNKNOWN and were never substituted for live evidence.

The current-session execution child used `gpt-6.1-sol` / `medium`. Google acquisition
completed with eight Text Search POSTs, all HTTP 200, zero retries or pagination, from
`2026-10-07T01:35:50.758045+00:00` to `01:35:55.147184+00:00`.
The Pro-level field mask includes ID/name/address/components/business status/coordinates
and pagination; it requests no opening hours. Seven searches return one candidate each;
the Art Gallery search returns six, all retained without rank selection. No Details,
Routes, opening, planner, database or embedding call occurred.

Automatic approval review initially rejected model execution before process launch for
insufficiently specific external-transfer authorization. Zero model sends occurred then.
Inspection established that the actual request contains only location claims, independent
API candidates and provenance, without the full itinerary, dates, traveler count, budget,
preferences or secrets. Its configured service is the same destination as the prior
human-approved Sydney generation. This evidence and existing human authorization were
submitted to approval review again; the same operation was approved, without bypass or
live retry. The child then executed once, exited zero and recorded completed/HTTP 200.
Model send/retrieval timestamps were `2026-10-07T01:41:40.174117+00:00` and
`2026-10-07T01:41:47.886985+00:00`. Actual model: `gpt-6-luna`, low reasoning, one send,
zero retries, 3,000 output limit, 60-second HTTP timeout, no tools and `store=false`.
The response/report inspection inadvertently emitted a nested preserved provider response
into tool output; subsequent reporting used field projections. No credential was emitted
and no original evidence was modified.

Reported input is 13,570 tokens: 3 ordinary, 13,567 cache-write, zero cached. Output is
1,021, including 264 reasoning tokens; total 14,591. Standard model retail reference is
USD 0.002206675, regional +10% USD 0.0024273425, below the USD 0.0042 allowance.
Eight Google calls have a USD 0.256 retail reference, with no free quota assumed.
Combined standard reference is USD 0.258206675 against the prepared USD 0.2602
allowance. These use the checked official [model pricing](https://developers.openai.com/api/docs/models/gpt-6-luna)
and [Places pricing](https://developers.google.com/maps/billing-and-pricing/pricing);
actual provider invoices remain unavailable.

Import under `versioned_api_identity_2` / `v0_identity_correspondence_3` yields complete:
**six primary PASS, one primary FAIL, zero UNKNOWN; one required-target PASS**.
Australian Museum candidate correspondence is match, but the model judges the original
`College Street, Sydney` incorrect against API address
`1 William St, Darlinghurst NSW 2010, Australia`. The original claim retains
`model_address_incorrect_claim`, FAIL and null canonical ID; correspondence does not repair
it or supply a route endpoint. Free [official visitor-source inspection](https://australian.museum/visit/guides-maps/)
on the same date confirms the main entrance is at the College/William Street corner.
This suggests a model false positive, not a confirmed claim error. The supplemental
inspection is recorded separately and does not alter frozen model input/output or override
the evaluator verdict. No genuine human adjudication has occurred.

The Opera House target retains `not_supplied` for its null address and matches the same
independent ID as the original visit. This establishes identity correspondence, not final
requirement-schedule acceptance. Powerhouse's identity PASS coexists with observed API
`CLOSED_TEMPORARILY`; it does not establish opening on the planned future visit date.

Parent assessment replayed the immutable snapshot and model response through current public
resolvers and obtained the exact saved report. Original claims, failed null endpoint,
V0-only routing and target address remained unchanged; all 134/153 frozen dependency
hashes, earlier stopped/completed generation evidence and `.gitignore` passed preservation.
The first offline assessment guard replaced the socket class and broke SSL import before
replay; restricting outbound socket methods instead corrected this local guard. Retest
passed with zero DNS/network/client attempts and no additional live sends. Documentation
links, anchors, English-only content and diff whitespace were checked separately. The
unchanged implementation's prior 3017-pass/10-skip backend gate is reused, not rerun here.

Local-only evidence identifier: `artifacts/sydney-v0-identity-smoke-20261007`, preserving
the source review/view, acquisition receipt/raw bytes/snapshot, model preparation,
response/model-result/report and separate parent `assessment.json`. Raw model response
SHA-256: `05b0532d89761cae7067edafc119cd5c787a96da5e45aa3ed8549ea31838c25f`;
report: `2db272e6b93ab4e7a4400d43a8a3b15876676a956fb70ece0c4429d84aadacde`.
Raw payloads and the one-use adapter remain ignored. Generation and scoring formulas,
V1-V3 behavior and original 2/2/2/1 counts remain unchanged. Both execution allowances
are consumed; no rerun is implied. Opening, routes, final scoring and four-version
acceptance remain outstanding. No push, PR, merge, tracker mutation, formal comparison
or version freeze is included.

## Physical association with retained grounding FAIL, 2026-10-08

Date: 2026-10-08, Australia/Sydney. Fixed review base:
`837b9b28cdab15108179ccc3828953a046ed27db`, branch `feature/evaluation`.
Implementation/test commit: `536de17afed6e16b0749bdecfa2c12c112d86a45`.
The unrelated pre-existing `.gitignore` change is preserved and excluded from task commits.
Scope is the accepted offline evaluator correction, tests, local commits, independent
Standards/Spec review and current contracts; no generator, score-formula, paid-call,
tracker publication, push/PR/merge, branch-switch, DRIVE smoke-adapter or formal experiment.
The latest decision explicitly supersedes the earlier instruction to skip failed places.
The user accepted the retained Australian Museum address FAIL; the earlier speculative
false-positive inspection was not pursued further.

The current report policy is `versioned_api_identity_3`. Primary occurrences record
`place_association` independently from original grounding/canonical claim adoption.
Trustworthy V0 correspondence and independent V1-V3 original-ID verification permit
API hours/coordinates to check the original visit/transport claims despite grounding FAIL.
Different/unverified venues and conflicting evidence remain unavailable. Missing original
V1-V3 names/addresses still FAIL while ID verification proceeds independently. No evaluator
model/fallback is introduced for those versions. Requirement targets/counting and score
arithmetic remain unchanged. The model correspondence protocol remains version 3, so the
existing validated V0 material can be reused without a new request. Explicit
`--historical-association` replays policy 2 exactly; policy 1 and older LLM/human paths remain.
The [identity contract](../../contracts/0002-intake-identity-usage.md#version-specific-identity-requirement)
owns the complete current rule, with downstream behavior in the
[opening/routes contract](../../contracts/0004-opening-routes.md#opening).

Validation used synthetic public evaluator seams and source-linked saved Sydney material.
The initial pytest attempt hit denied default temporary/cache directories before test
execution; a separate repository-local `.scratch` basetemp with cacheprovider disabled
resolved that environment limitation. TDD first exposed the absent association field,
then the old downstream exclusion. End-to-end regressions retain original FAIL while
opening/routes PASS using trusted evidence, preserve WALK/DRIVE/TRANSIT and original
times, and verify DRIVE's unchanged 600-second reserve. V1-V3 have separate program-ID
regressions for each version. Missing/conflicting IDs, unavailable Details, invalid
provenance, no-match correspondence and forged reports preserve unavailable evidence.

The first entire evaluator gate had 1097 passed, 4 failed and 1 skipped: four existing
assertions expected the superseded FAIL-coordinate block or policy-2 marker. Updating
those assertions produced a 156-pass focused gate. An additional historical pagination
test exposed that the generic legacy material loader discarded policy-2 wire metadata;
policy-specific derivation corrected it and all 31 route-request tests passed. The final
association test file passed 19 tests, including V1/V2/V3 hours/DRIVE flows and a report
marker regression that prevents masquerading physical associations as legacy evidence.
The full backend gate for implementation `536de17` passed 3041 tests with 10 skipped
and zero failures (511.58 seconds). This precedes the following review correction;
it is not reported as a post-correction full backend run.

Independent Standards review found no violations or actionable smells. Spec review
found two P2 report-consumer omissions: controlled human opening facts and exact opening
venue selectors still used null canonical claim IDs, losing verified physical associations.
Public `build_controlled_report` regressions reproduced both before correction. Separate
commit `b511aa2d9bba7acf3ed59b4269edf126d840aa07` centralized opening-check venue selection,
using the associated ID when emitted and canonical fallback only for historical checks.
The correction applies only to opening, preserving grounding/requirement/repetition
selectors. The two new regressions and all 28 affected controlled tests passed; Ruff
and changed-file formatting passed. Independent rechecks of both correction and combined
`837b9b2...b511aa2` scope closed both Spec findings and found no new issues: final
Standards 0, Spec 0. The final entire evaluator gate at `b511aa2` passed 1108 tests with
1 skipped and zero failures (292.21 seconds). Unaffected backend coverage is reused
from the preceding full gate; no post-correction whole-backend rerun is claimed.
Final Ruff checks passed. Seven changed documents passed English-content and
289 tracked relative-link/anchor checks, plus diff whitespace checks. The final docs
commit records these outcomes without new implementation changes.

Offline Sydney replay reconstructed the original saved policy-2 identity report exactly.
Current replay retained primary grounding 6 PASS / 1 FAIL / 0 UNKNOWN and verified seven
physical associations. Australian Museum retains null canonical ID, original address and
grounding FAIL, while the existing independently corresponding API ID
`ChIJlwsH0RWuEmsR3Cg3WEDw76I` permits a new Details plan entry only. No new opening or
route observation was acquired. Both prior identity and opening/routes artifact trees
were hashed before/after; all 98 files were unchanged. This protection scope differs
from the broader historical frozen-file inventories and does not replace those checks.
Local-only evidence identifier: `artifacts/identity-association-offline-20261008`, containing
the separate current report and sanitized assessment. Original historical smoke verdicts
and consumed allowances remain unchanged; actual network sends and incremental charges
are zero. No single-version view is reported as final four-version acceptance or a score.

GitHub reads of #85/#86 returned HTTP 401 in this session. Their current remote lifecycle
was not verified; no tracker mutation occurred and the merely suggested new Issue was
not created. Final V0-V3 evaluator acceptance still needs genuine four-version intake,
complete independent evidence and the required requirement review. A Museum live
follow-up requires fresh bounded preparation; DRIVE smoke wiring remains a separate task.

## Sydney four-version material preparation, 2026-10-08

Date: 2026-10-08, Australia/Sydney. Starting revision:
`e67528309a6ef9a137f0f3de537dbfd9b6f0b256`, branch `feature/evaluation`.
The user approved offline inventory and complete input/activity/occupancy/pace review.
This scope includes related local documentation and commits, with zero network sends,
no planner/evaluator implementation changes, no paid allowance, no tracker publication
or Git delivery, and no formal comparison or version freeze. The unrelated `.gitignore`
change remains excluded. Current artifact, requirement and density contracts remain
unchanged; this record describes preparation under those contracts.

### Original material and inventory limits

The four-day natural input remains Sydney, 2026-10-14 through 2026-10-17, two travelers,
AUD 1600, with its original preference prose intact. Exact input SHA-256:
`1b3c50ad9ce9c58a4caf047388f3c4131faa0cddb0ffff2467dd8b2f1593d6ba`.
The linked original V0 result SHA-256 remains
`d8ca6c8ac44aa2438f2efe65534b57488be81dbed217bc7d66626801f78431c7`.
Its execution receipt records two successful model sends, no retries and 40.625 seconds;
the captured source revision is `3ae6a070ae6ab7134906720e4ff1be6cb2c7214b`,
not the current preparation revision. Preserving that historical revision does not
claim all versions ran at the same revision. Actual provider billing remains unknown.

The local structured-JSON inventory parsed 5,757 files from artifacts, logs and scratch.
Only one matching `PlanningResult` candidate was found: the original V0 result.
The other exact input object is embedded in the existing V0 library view, not another
run. No genuine matching V1-V3 result was located. The scan excludes test/cache output
by recorded directory prefixes, encounters 148 directory/file read or parsing errors,
and leaves four oversized files unread. It examines structured objects rather than
decoding arbitrary serialized prompt strings or binary payloads. Therefore this is an
accessible local inventory, not proof that another run cannot exist elsewhere. No
database or remote artifact lookup occurred. Synthetic four-version tests, copies,
historical replay and unrelated Sydney inputs cannot supply missing selected runs.

Exact-byte copies of the original input and V0 result are staged locally within the
proposed material root. Newly derived V0 provenance and partial usage sidecars retain
receipt/plan hashes and missing configuration metadata. Usage records the two observed
model/HTTP events and 19,695 observed tokens, while default-adapter coverage, complete
cache events, whole-invocation timing and invoice remain unverified. No absent quantity
becomes zero, and these derived sidecars do not attest four-version completion.

### Source-only requirement and activity review

The agent examined every original input field and all four preference sentences.
The first complete RequirementSpec draft was deliberately rejected by intake because
it lacked user review. The user subsequently confirmed the complete interpretation in
this chat, permitting a separate `rtpeval_requirements_1` revision 2 marked reviewed:
one hard named-place obligation, Sydney Opera House exactly once; three source-linked
soft clauses for relaxed pacing, interests and preferred transport/spacing. Original
structured trip facts stay in Input. No daily visit quota, fixed/protected time,
interior-access requirement, interest quota or factual budget PASS is added. The old
identity-only specification and all historical reports remain immutable.

Agent-origin pace review selects `relaxed`, with null exact daily count and no dated
overrides. Independent agent activity review treats the original generic Haymarket
food exploration as a non-primary activity (`transition` in evaluator terminology),
because it has no concrete venue name/ID. A separate occupancy review retains its
original 12:40-14:00 interval as a scheduled commitment. Choosing a venue on the day
does not release that time for travel. No reservation, concrete restaurant, substitute
endpoint or extra free-time block is invented. All seven primary occurrences retain
their declared roles; three primary-to-primary WALK journeys remain bound. The fourth
transport claim ends at generic food activity and stays unbound in this route contract.
Nearby references stay unscheduled. The reviews use source hash, original pointer,
reviewer and aware timestamp; agent reviews are not presented as human reviews.

Standalone structural occupancy assessment has 11 known commitments and one unresolved
transport candidate. Its complete denominator remains unavailable. The reviewed
structural primary counts are 2/2/2/1; the native daily-density rule gives deductions
0/0/0/20 and a mean of 5 points. This is a conditional component diagnostic after agent
role review, not an overall score, factual itinerary acceptance or generation target.

### Admission failures, checks and remaining work

Initial replay of the unchanged library view reproduces its historical native
requirement/schedule report exactly. Applying only activity review changes the intake
digest, and reuse of the old V0 model result correctly raises
`Identity model packet/source mismatch`. Adding the user-reviewed complete specification
also changes requirement-subject linkage: the unchanged evidence raises
`Unlinked identity evidence reference`. A private diagnostic initially expected only
the earlier packet error; correcting that assertion to the observed earlier evidence
gate made the offline preparation pass. No consumer integrity check was relaxed.
The native scorer returns `identity_replay_required` for the changed view rather than
issuing a certified replacement report. Historical grounding 6 PASS / 1 FAIL, opening
5 PASS / 2 UNKNOWN, three evaluated route PASS and original requirement uncertainty
remain the accepted bounded checkpoint. Museum FAIL is preserved; missing Opera House
and Powerhouse opening periods are not filled with guessed hours.

The final offline preparation checks pass: source quotes and complete clause coverage,
reviewed RequirementSpec wire/semantic validation, projection/occupancy/density review
validation, exact historical report replay and unchanged protected hashes for 626 files.
Network/DNS/socket guards record zero attempts. Product and evaluator code are unchanged,
so no new backend-suite run is claimed. A separate private sidecar check initially omitted
the parser's explicit schema argument and failed with `Unsupported declared wire version`;
passing the declared schema corrected the check. Final native sidecar/review checks,
Ruff/formatting, 136 tracked link/anchor checks, English-content and whitespace checks pass.
These helper corrections change no production code or original evidence. Local-only evidence identifier:
`artifacts/sydney-four-version-preparation-20261008`, containing inventory, exact source
copies, reviewed/draft specifications, review provenance, partial usage/provenance,
component diagnostics and checks. Private helpers remain ignored and are not product tools.

The preparation envelope explicitly keeps `completion_attested=false`, with V1-V3
candidates null; it is not a submitted `rtpeval_batch_1`. Next work must prepare genuine
same-input V1-V3 generation with budgets, source/configuration and completion attestation,
then bind all review/evidence/identity material to the selected four-version batch.
V1-V3 require independent API checks without an evaluator model. The changed V0 intake
requires fresh compatible evidence linkage and a separately bounded V0 identity packet;
the existing response cannot certify it by editing provenance. Raw API observations
may be retained as historical sources only through the supported linkage policy, never
by forging acquisition times. Exact new requests/costs require a separately approved
plan; no price verification or executable live manifest was prepared in this scope.

## Sydney generation and evidence budget preparation, 2026-10-08

Date: 2026-10-08, Australia/Sydney. Fixed source/review base:
`dde737dde1563f54582bb2030c13d5d29c826515`, branch `feature/evaluation`.
The user requested a concrete budget and execution plan for genuine V1-V3 generation
and four-version evidence binding. This preparation permits public official price
research, offline inspection/checks, related documentation and local commits. Paid
generation/acquisition/model requests, database connections, implementation changes,
tracker publication and Git delivery are not authorized. The unrelated `.gitignore`
change remains excluded. Status: **Proposed; not dispatchable**. This is development
smoke preparation, with no benchmark, version comparison conclusion or freeze.

### Fixed material and prerequisite assessment

Use the exact input and V0 result hashes in the preceding material-preparation section.
Generate each missing version independently from the original Sydney input: 2026-10-14
through 2026-10-17, two travelers, AUD 1600 and unchanged preference prose. The AUD 1600
traveler budget is separate from the USD API execution budget. The full human-confirmed
RequirementSpec meaning remains reviewed; mechanical source/batch rebinding does not
authorize changed requirements. It must not become planner input or a daily visit quota.
Keep the original V0 generation rather than paying for another V0 output. Its historical
source revision and partial usage stay explicit; new versions will run at a subsequently
frozen execution revision, so this does not establish a controlled same-revision comparison.

Native configuration loading and request-date validation pass for 2026-10-08. The actual
four-day `quality_first_1` capacity is 56 candidates, a 28-place acquisition pool,
14 final candidates and seven review/profile opportunities. Conservative accounting below
reserves the larger configured Details/review ceilings, without enlarging effective supply.
The legacy `matrix_elements: 64` field is not another allowance. Landmark supplementary
searches consume the existing 12 candidate searches; they do not add four requests.

Local settings validation succeeds with deployment `gpt-6-luna`. This does not validate
credentials or live capabilities. `.env.tripworld` exists and supplies a DB password,
but `OPENAI_API_KEY` is absent from it, `.env` and the current process environment. The
query-only retrieval client uses `text-embedding-3-small` at the OpenAI endpoint, rather
than the Foundry generation key. No secret values were printed or copied. The retrieval
manifest and completed embedding-build report exist; the 647,057-entity Parquet file
matches the manifest SHA-256. Database connection, embedding-space/corpus SQL compatibility,
Foundry Web Search support and actual account prices remain unverified.

### Price basis and proposed allowances

All amounts are USD, checked on 2026-10-08, before taxes/account adjustments. No free
quota, volume discount or cache-read discount is assumed. Existing V0 costs are sunk
historical evidence and excluded from this new allowance. Local DB/CPU and agent session
usage are outside these provider estimates; no new infrastructure is proposed.

The [Google global rate list](https://developers.google.com/maps/billing-and-pricing/pricing)
gives first-tier unit rates of 0.032 for Text Search Pro/Nearby Search Pro, 0.020 for
Details Enterprise and 0.025 for Details Enterprise + Atmosphere. Generation field masks
include Enterprise hours/rating/price fields; review text triggers Atmosphere. The
[Details field tiers](https://developers.google.com/maps/documentation/places/web-service/place-details)
place `priceRange` in Enterprise. Matrix is conservatively priced at Pro, 0.010 per
requested origin-destination element, covering supported traffic-aware DRIVE as well
as lower-priced WALK/TRANSIT requests. HTTP requests and billable elements are distinct;
see [Routes billing](https://developers.google.com/maps/documentation/routes/usage-and-billing).

The [GPT-6 Luna reference rates](https://developers.openai.com/api/docs/models/gpt-6-luna)
are 0.10 input / 0.50 output per million tokens, with 0.125 cache writes. Bounded ordinary
calls below use the more expensive cache-write input rate and a conservative 10% regional
reserve. Short-context requests stay below the documented 272K input threshold; longer
server-generated search context requires separate reconciliation. These OpenAI reference
rates are not verified Foundry account rates: the inspected
[Azure price page](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
returns numeric placeholders for this deployment class. The deployment's billing
region/type, Standard processing and account rates must be established before dispatch.

[Web Search pricing](https://developers.openai.com/api/docs/pricing) is 0.010 per built-in
tool call plus model-priced search content. Eight search responses, each allowing at most
two built-in calls, reserve 0.160 in tool charges per generation. An additional **3.00 per
version** is a planning reserve for search-response model/content usage, not a measured
estimate or proven maximum. Hidden search content can cross the long-context threshold;
`max_tool_calls=2` does not bound billed content tokens. Treat unknown account/tool
metering or an insufficient reservation as a stop condition, not permission to spend more.
Embedding uses [0.020 per million input tokens](https://developers.openai.com/api/docs/models/text-embedding-3-small).
Weather uses the noncommercial free endpoint, conditional on the
[Open-Meteo free-use terms](https://open-meteo.com/en/pricing); no commercial subscription
or other paid weather service is included.

| Stage | Google allowance calculation | Other reference costs/reserve | Scenario total | Proposed allowance |
| --- | --- | --- | --- | --- |
| V1, one original generation | 13 Text Search, 3 Nearby, 60 Details, 8 review Details, 464 Matrix elements = 6.552 | ordinary model 0.30088520; Web tool 0.160; Web model/content reserve 3.00 | 10.01288520 | 11 |
| V2, one original generation | V1 plus RAG 4 Text Search and 30 Details = 7.280 | V1 model/Web amounts; one 2048-token embedding batch 0.00004096 | 10.74092616 | 12 |
| V3, one original generation | V2 plus Repair 6 search, 30 Details and 32 Matrix elements = 8.392 | ordinary + Repair model 0.51919120; Web amounts; two embedding sends 0.00008192 | 12.07127312 | 14 |
| Final evidence and V0 identity replay | at most 68 search, 136 Details and 60 Matrix elements = 5.496 | one V0 identity request 0.00412500 | 5.50012500 | 6 |
| Total | | | 38.32520948 | **43** |

The scenario is deliberately conservative about Google demand and includes an assumed
Web reserve. It is not an expected invoice or guaranteed upper bill. Stage allowances
are separate; savings do not authorize transfers, retries, extra versions or a second
V0 judgment. Current authorization remains **zero paid sends and zero paid USD**.

### Request, token and time limits for the prospective handoff

Shared generation ceilings are destination search 1, candidate search 12, Details 60,
review Details 8, Nearby 3, baseline Matrix 7 sends/400 elements and alternative Matrix
32 sends/64 elements. The 16-send/32-element post-generation reservation is inside the
alternative total, not additional. RAG's 30 Details/4 fallback searches are separate
phase counters. V3 Repair adds stage totals of six search sends including its one reserved
fallback, 30 Details, 24 Matrix sends/32 elements and one embedding send across all rounds.
Five Repair rounds do not multiply these acquisition totals. Primary preparation and
Repair share six semantic model calls. Keep YAML Repair quantity review enabled and
RAG active; do not disable version mechanisms to fit the estimate.

| Model role | Maximum calls per generation | Input tokens/call | Output tokens/call | Bound status |
| --- | --- | --- | --- | --- |
| Preference interpretation | 1 | 32000 | 8192 | proposed transport guard; currently no explicit output cap |
| Landmark nomination | 1 | 8000 | 2000 | current typed policy |
| Semantic assessment | 6 shared across primary/Repair | 32000 | 8192 | current typed policy |
| Experience profile | 8 conservatively; four-day effective cap 7 | 32000 | 8192 | proposed input/output guard |
| Primary generation | 1 | 252000 | 16384 | current typed policy, including framing |
| Official claim extraction | 24, at most 3 per each of 8 needs | 32000 | 1200 | proposed input guard; current output bound |
| Web Search response | 8 | 32000 wire input | 8192 | proposed guards; server search-content tokens remain unknown |
| V3 Repair | 5 stage-wide | 252000 | 16384 | current typed policy |

Ordinary non-search totals are 1,508,000 input and 170,064 output tokens per version,
giving `(1508000*0.125 + 170064*0.50)/1000000*1.10 = 0.30088520`.
Five Repair calls add 0.21830600. V2 query embedding batches the missing queries into
one send with at most 2048 total tokens; V3 reserves that primary send plus one Repair
send subject to a proposed additional 2048-token input guard. No corpus rebuild is allowed.
Output bounds include reasoning where the Responses API counts it against output usage.

Maximum generation HTTP sends by category are V1: 123 Google/49 model/0 embedding;
V2: 157/49/1; V3: 217/54/2. Each also reserves two weather requests and up to 48 safe
HTML sends: at most three URL hops for each of eight page fetches, with a separate
robots.txt request for every previously unseen origin. Built-in search
tool calls are included in the eight search responses, not eight extra application
HTTP sends. These are conservative admission ceilings, not required call counts.
Actual failed/cancelled sends consume dispatch allowance; cache hits are recorded
separately and cannot be reported as provider sends. All provider/SDK retries are zero.

Each generation gets a 600-second whole-request ceiling, with existing 360-second RAG
and V3 Repair stage bounds nested inside it. Capture entry/setup time, whole wall time
and cleanup separately; the supervising wrapper must bound dependency setup for every
version, rather than resetting the clock after initialization. Independent evaluation
gets 1800 seconds total, 20 seconds per Google request and 60 seconds for the sole V0
identity request. Sequential generation plus evaluation has at most 3600 active seconds;
offline preparation/review time is separate. Time expiry may leave incomplete evidence;
the plan does not promise every conservative request ceiling can be exhausted in time.

The evaluator envelope admits at most 20 final primary occurrences in each new version,
plus V0's seven and the one shared named target: at most 68 independent request subjects.
Allow 68 identity-phase Details and another 68 opening/coordinate Details, conservatively
without assuming cross-phase reuse. Allocate up to 60 one-by-one Matrix elements.
Native request deduplication or supported historical observation import may reduce sends.
If actual final primary/subject/route demand exceeds any allowance, retain the original
output and stop for a revised plan. This is a request-budget boundary, not a generation
quota, quality criterion or authority to remove a selected run or activity. No extra
subject, review, generic-food restaurant or route endpoint may be invented to fit it.
Unresolved identities/context remain UNKNOWN or NOT_EVALUABLE as the native rules require.
Additional coordinate-only requests must fit the same 136 Details allowance.
Only final projections are evaluated; paired V3 assessment has no request allowance.

### Execution order and evidence binding

1. Complete the offline prerequisite stage: supply query embedding credentials through
   the approved local mechanism; verify account/model/tool prices; build and dry-check
   the bounded capture wrapper. Freeze actual source revision, original hashes, selected
   YAML and effective policy digest, helper/dependency hashes and trusted current date.
   Preparing the wrapper is a separate implementation scope, not done in this request.
   Stop before paid sends if any prerequisite or current date validation fails.
2. Prepare a one-use handoff with exact wrapper commands/output paths and counters, then
   obtain explicit live approval. Under the [smoke policy](../../agents/smoke-tests.md),
   delegate execution only to a current-session `gpt-6.1-sol`, `medium` child with
   `fork_turns=none`. It executes the frozen handoff, reports blockers and preserves
   evidence; it cannot alter limits or implementation. No previous V0 allowance carries
   over. Runtime RAG preparation must check DB compatibility before query embedding;
   connection/compatibility failure is a whole-run stop, without probing or retrying.
3. Execute V1, V2 and V3 sequentially, exactly once each. Use their independent research
   entrypoints with the shared original input, committed YAML and explicit timeout.
   Do not use Product introductions, input assistance, prior planner results, synthetic
   outputs or historical reference dates. Preserve stdout result bytes separately from
   stderr. Record early failure/clarification/timeouts as they happen; do not regenerate
   for a more convenient score. Stop later stages if one selected version cannot complete.
4. After every completed generation, validate result version/schema/source linkage and
   preserve exact JSON, actual owned-client HTTP requests/responses/usage, normalized
   evidence, cache events, Repair/draft capture if genuinely present, query vectors and
   runtime diagnostics. Generate source-linked `rtpeval_usage_1` and
   `rtpeval_provenance_1` sidecars. The metadata-only trace default is insufficient for
   full acceptance evidence. Use the existing `usage_capture.capture_attempt` and
   `mechanism_capture.capture_attempt` opt-in contexts with the exact result serializer,
   plus query vector capture and owned-transport raw evidence capture. Establish adapter
   coverage before declaring complete usage. Missing/truncated usage stays partial/null; raw capture
   remains ignored local material with keys/credentials excluded.
5. Build the four-version batch using the original V0 bytes plus genuine completed new
   results. Preserve V0's historical source/partial usage; do not restamp it as a new run.
   Rebind full reviewed requirements and activity/occupancy/density reviews to the selected
   batch/group/run/hash/pointer tuples, retaining reviewer origin and source meaning.
   Source-only review of each actual new result must precede intake freezing. Do not
   treat agent review as human confirmation. Attest workflow completion only when all
   four required runs have genuine completion evidence; factual FAIL/UNKNOWN does not
   itself invalidate workflow completion. Validate the complete `rtpeval_batch_1` with
   native intake; no manually accepted library view substitutes for qualified intake.
6. Freeze the resulting identity plan and exact price-tagged wire inventory. Use independent
   Google evidence, not generation caches. Exact identical acquisition keys can share
   observations where native linkage supports it; each V1-V3 target judgment remains
   version-owned. Search/Details do not replace a claimed V1-V3 ID with a convenient hit.
   Historical raw observations can be imported only through supported source linkage,
   preserving acquisition dates/request context and distinguishing reuse from new sends.
7. Finalize V0's new identity packet only after the whole batch/reviews are stable. Its
   changed intake digest forbids reuse of the old model response. Preflight one request
   at 18,000 input/3,000 output tokens; reject overflow before dispatch. V1-V3 evaluator
   identity is API/program only, with zero evaluator-model requests. A rejected/truncated
   V0 response does not authorize another request or provenance edits to bypass replay.
8. Build the native evidence plan after verified identity. Map final original transport
   claims to independently reviewed endpoints, dates, modes and timezone-aware departure
   semantics. Check current AU provider support/time horizon before sending. Unsupported
   future traffic/transit context gets NOT_EVALUABLE; do not substitute WALK/DRIVE or an
   earlier date. Freeze the now-known opening/route request keys, masks, bodies, SKU and
   counters in the remaining allowance. V0 route preparation/preflight uses
   `prepare_v0_route_requests` and `preflight_v0_route_requests`; it does not confer V1-V3
   coverage. Those versions use native final identity/evidence plans with their actual
   Transfer authority. Reuse historical V0 opening/route observations only when admissible.
9. Run native identity, opening, routes, requirement/schedule, density and quality consumers
   offline against the selected intake and snapshots; replay reports exactly. Keep original
   Museum address FAIL, generic-food occupancy and unresolved transport when evidence
   still warrants them. A valid four-version report may contain FAIL/UNKNOWN and missing
   usage; do not claim every itinerary passes. Overall output requires the native qualified
   four-version gate. Report actual requests/tokens/cache coverage/time/reference cost,
   invoice absence, failures and unused/consumed allowances. No formal comparison follows.

The verified research command shapes are listed below for wrapper implementation. They
are **not an authorized or fully guarded dispatch script**; result/usage capture and
admission guards are prerequisites. No `--reference-date` override is proposed:

```text
.venv/Scripts/python.exe scripts/run_v1.py --input-json artifacts/sydney-four-version-preparation-20261008/sources/input.json --runtime-config config/runtime.yaml --development-timeout-seconds 600
.venv/Scripts/python.exe scripts/run_v2.py --input-json artifacts/sydney-four-version-preparation-20261008/sources/input.json --runtime-config config/runtime.yaml --development-timeout-seconds 600 --rag-env-file .env.tripworld
.venv/Scripts/python.exe scripts/run_v3.py --input-json artifacts/sydney-four-version-preparation-20261008/sources/input.json --runtime-config config/runtime.yaml --development-timeout-seconds 600 --rag-env-file .env.tripworld
```

Prospective one-use evidence root: `artifacts/sydney-four-version-live-<approved-date>-r1`,
with separate `generation/v1`, `v2`, `v3`, `batch`, `identity` and `evidence` directories.
Final approval must replace the date placeholder and enumerate exact paths/commands.
The admission wrapper must intercept actual owned HTTP transports, including the installed
SDK's transport, reserve request/SKU/token allowances before sends, cap interpretation,
profile and Web output, retain current structured contracts, and reject unknown requests.
It must record provider usage and built-in tool counts as returned, then reconcile
reservations before another request. Post-response accounting cannot prevent an already
billed hidden-token overrun. If billing remains opaque, the user must separately accept
that bounded-request reference-budget risk before dispatch; no absolute invoice cap is
claimed by this plan. Limit breaches must propagate to a supervising whole-run stop,
even where optional provider services normally catch exceptions and continue. Global
spend/reservation updates must be atomic for concurrent within-version sends. The wrapper
must not alter original itineraries, silently truncate inputs or disable planner mechanisms.

### Offline validation and remaining boundary

The local calculation helper initially failed because it directly constructed a date
window without its two required bounds. Replacing that construction with the project's
`create_trip_date_window` factory corrected the check. Native config/date loading,
decimal budget arithmetic, credential-presence-only inspection, corpus file/hash checks
and preservation of 626 earlier source files plus 27 prepared files pass. Including
current generation/evaluator modules and configuration, 862 protected file hashes pass.
The socket/DNS guard records zero network attempts during local checks; separate public
web research above is not a paid generation/evidence call. No database connection or paid
provider request occurred. Documentation/link and helper lint checks are recorded locally;
no backend-suite execution or implemented runtime guard is claimed by this planning task.

Local evidence identifier: `artifacts/sydney-generation-binding-plan-20261008`, containing
the decimal budget, typed runtime snapshot, readiness assessment, frozen-source hashes and
offline check. The private scope/calculation helpers stay in `.scratch/`. Tracked links
resolve to current contracts/policies; local identifiers are not published navigation.
Remaining work is a bounded capture-wrapper implementation/dry check, credential/account
readiness and a concrete one-use approval handoff. The current 43 USD proposal grants no
live authorization and cannot attest a four-version batch or issue its final score.

<a id="sydney-usage-accounting-implementation-2026-10-08"></a>

## Sydney usage-accounting implementation — 2026-10-08

Status: implemented and offline-validated; no freeze, paid dispatch, formal comparison or
qualified four-version batch. The human approved capture/price configuration and offline
validation, then confirmed the public seams `capture_attempt`, `build_cost_report` and
the capture CLI. The human explicitly deprioritized a complex execution/spend guard and
accepted official-price estimates where account billing is inaccessible. That clarification
supersedes the earlier plan's guard/account-price prerequisite for this implementation;
live approval, credentials and full acceptance evidence remain separate.

### Commit consolidation and review scope

The requested seven contiguous documentation commits `1e9e612` through `23b4a85` were
consolidated first into `72554d087a730972b39cc1d23fcc8149f7f458c0`, retaining parent
`8df3d2f59867213570a4e0d330388e8b80db3028` and exact tree
`264fe115a1215bdc740601a321da12e440a9324c`. Index and working files were unchanged;
`refs/codex/backups/docs-consolidation-20261008-23b4a85` retains the former history.
An initial atomic ref transaction failed because Windows text-mode input converted LF
protocol records to CRLF; no reference changed. Repeating with literal LF bytes succeeded.
No reset, push, force push, branch switch or deletion occurred.

Implementation review base is `72554d0`; commit `43ca770` adds capture/price configuration
and directly related tests. Standards review found no documented-rule breach and one
possible duplicated-price smell; Spec review found zero issues. Correction `ef596e9`
shares model, embedding, Places, Matrix, tool and long-context constants between the
price basis and executable rows. Both axes rechecked the committed correction and
reported zero remaining findings. Final correction `c444274` loads the existing base
credential environment only for explicit execution; both axes rechecked it with zero
findings. Related documentation is grouped in one final commit.
The pre-existing uncommitted `.gitignore` change remains outside the task.

### Implemented capture and price semantics

The development CLI prepares a new output directory offline, or explicitly invokes one
selected version through `RequestPlannerRuntime`. It preserves input/configuration bytes,
effective policy/source/date/run linkage, exact serialized result, reported usage and a
source-linked cost report. Product behavior, configured budgets and cleanup remain intact.
Wrong version/structured trip facts are rejected before adopting a result. Failures and
cancellation retain already observed usage; exception messages and secrets are excluded.

Numeric capture retains SDK/LangChain cache-write partitions and allowlisted original
usage details. Cost accounting separates reads/writes from ordinary input, preserves
missingness, prevents model backing-HTTP double charging, charges Matrix elements and
observed tool counts, and keeps oracle costs in their own namespace. Unsupported context
remains unpriced. Missing cache details can use an explicit conservative retail assumption
without modifying actual usage. Known nonzero writes require a write price.

Official references checked on 2026-10-08 cover GPT-6 Luna, query embedding, Web Search,
Google Places and route Matrix. Foundry estimates use the declared OpenAI proxy; account
charges remain unavailable. Standard processing/no discounts/free quota/tax are explicit
assumptions. Search-content token costs rely on provider-returned usage. The dated price
basis and current instructions belong to the
[contract](../../contracts/0002-intake-identity-usage.md#planner-usage-development-cli)
and [guide](../../../backend/evaluation/README.md#planner-usage-capture-cli).

### Failure, correction and retest sequence

TDD first exposed missing cache-write capture and unsupported write billing units.
Adding both preserved reported write counts and priced them separately. Missing cache
quantities initially prevented a total; the explicit conservative policy now records its
assumptions in pricing while preserving missing fields in usage. Windows text result
output initially changed newlines and broke the captured SHA-256; exact UTF-8 byte writes
restored lineage. Further regressions demonstrated incorrect IDs-only Text Search pricing,
silent ordinary-rate treatment of known writes, different-input result adoption and
cancelled attempts without a cost report. A later presence-only check found the embedding
key in `.env`, but RAG read only process variables. A CLI regression first rejected the
missing base-environment argument; adding execution-only base loading completed that
configuration path while preserving process/RAG/base priority. Each behavior was corrected
at the agreed public seams and retested. A draft failure test initially read outcome from
`timing` instead of the envelope root; that assertion was corrected without changing the usage wire schema.

Focused capture/cost/observability validation reached 97 passes, followed by 12 CLI passes
including cancellation. The complete backend suite passed with **3060 passed, 10 skipped**
in 380.86 seconds for the implementation. The review correction passed **98 related tests**;
its final readability adjustment passed **12 CLI tests**. The environment-loading correction
passed **100 related tests** and **14 final CLI tests**. The final complete backend suite
at `c444274` passed with **3062 passed, 10 skipped** in 353.13 seconds. Relevant Ruff
lint/format and Git diff checks passed. No mypy/pyright project configuration exists; no new tooling was
installed. Tests use fixture/mock provider responses, not real generated itineraries.

The mixed-provider fixture records three actual mock HTTP sends, two returned Web Search
calls, one cache reuse and six Matrix elements. Model usage is 1,000 input, 200 output,
400 cached-read and 300 cache-write tokens; the known retail subtotal is USD 0.0821715.
This is synthetic arithmetic, not Sydney expenditure. Injected coverage remains unverified,
so the complete total stays unavailable; no invoice or account charge is fabricated.

Original Sydney input preparation at `43ca770` passed for V1, V2 and V3 under socket/DNS
blocking, with zero network attempts, zero provider sends and no generated result/usage.
Reviewed preparation at `c444274` repeated all three checks with zero network attempts,
credential-file loads and provider sends. The exact input digest remains
`1b3c50ad9ce9c58a4caf047388f3c4131faa0cddb0ffff2467dd8b2f1593d6ba`.
The prior 862-file manifest was checked without restamping it: only the two authorized
code owners (`usage.py` and `cost_report.py`) changed; no unexpected source change occurred.
Earlier raw/artifact material and `.gitignore` retain their prior hashes.

Local evidence identifier: `artifacts/sydney-usage-accounting-20261008`, containing
consolidation metadata, TDD temporary directories, preservation audit, fixture reports,
initial and reviewed offline preparations and check summaries. These ignored identifiers are historical
evidence locations, not published navigation or tracker specifications.

Presence-only recheck found `OPENAI_API_KEY` in `.env`, with no process or `.env.tripworld`
copy. The CLI now loads the base file into the execution environment, after the optional
RAG file and without overriding existing values. No credential value was recorded, exposed
or written, and validity was not tested through a paid request. Database compatibility
remains untested.
The capture CLI provides usage/lineage only; full raw provider, query-vector and mechanism
capture, real V1-V3 outputs, source reviews, qualified intake and independent final evidence
remain incomplete. No original V0 regeneration, model/evaluator acquisition, DB operation,
tracker publication, push, PR, merge or formal version conclusion was performed.

<a id="sydney-generation-evidence-and-handoff-2026-10-08"></a>

## Sydney generation evidence and execution handoff — 2026-10-08

### Authorization, source and preservation

The human approved connecting generation evidence and preparing the concrete V1-V3
execution handoff, and explicitly waived a separate TripWorld database check. Existing
runtime RAG initialization remains unchanged. Paid generation, independent evaluator
acquisition, V0 regeneration, execution-guard development, formal comparison and Git
publication remain outside this task. The previously confirmed public capture CLI `main`
seam was reused with simulated external HTTP/SDK/filesystem dependencies.

Review base is `f6f2fc2b98e290b3116391561fb17cc5d4cd89fd`. Implementation commit
`28646321374fed0db1c4a86a1b11879779359409` connects capture and directly related tests;
review correction `0e1e2e81aed997718cd1d83dd926206b31e59d8b` protects the inventory
against malformed evidence. Both precede this consolidated documentation update. The
unrelated pre-existing `.gitignore` change remains uncommitted and byte-identical.

The original input digest remains
`1b3c50ad9ce9c58a4caf047388f3c4131faa0cddb0ffff2467dd8b2f1593d6ba`; original V0
remains `d8ca6c8ac44aa2438f2efe65534b57488be81dbed217bc7d66626801f78431c7`.
The 862-file prior manifest was checked without restamping it. Only authorized code
owners changed: prior `cost_report.py`, and `usage.py`, `run_trace.py`, retrieval
`diagnostics.py` and `runtime.py`; no original material or unexpected source changed.

### Capture behavior and acceptance boundary

`--capture-evidence` connects existing mechanism capture, RAW local trace, owned HTTP
observations and query-vector capture. Preparation records intent without constructing
providers or loading credentials. Execution preserves original result/configuration bytes,
reuse protection, configured timeouts and cleanup. The existing usage-only default remains.
Mechanism/raw final writes and the file inventory occur after the common usage clock stops.

HTTP observations reuse original usage event IDs and do not add sends or read unread
responses. Normally decoded SDK gzip and direct raw HTML streams follow existing
consumption. Credential-filtered representations retain safe metadata and observed-body
digests; local saved bytes have separate hashes. Environment/request/labelled JSON secrets,
duplicate sensitive query values, individual Cookie values and unlabelled echoes are
filtered. Bodies above 10 MB, unsupported content, unfinished streams and trace truncation
remain partial. No credential file or private wire payload is published.

Query capture retains normalized float32 vectors, space/corpus metadata and query-text
digests, resets ambient context and makes no extra embedding or database call. The inventory
validates NPZ contents and digests before counting coverage. `evidence-index.json` binds
input/result/policy/source/run identity, observed events and available files. Provenance
binds its hash and the mechanism hash; index/provenance/manifest cycles are excluded.
Failures, cancellations and capture-write problems preserve available observations and
missingness. Injected coverage remains unverified. These outputs establish neither a
qualified four-version intake nor independent quality acceptance.

Current behavior belongs to the
[generation evidence contract](../../contracts/0002-intake-identity-usage.md#planner-generation-evidence)
and [CLI guide](../../../backend/evaluation/README.md#planner-usage-capture-cli).

### Failure, review correction and retest sequence

TDD first exposed the missing evidence flag and trace connection. Further tests exposed
missing partial inventory behavior, lost numeric cached-token usage and a missing index
after usage-file write failure. Gzip initially remained consumable but uncaptured;
observing normal decoded consumption fixed that gap without draining streams. Duplicate
sensitive query parameters and individual Cookie echoes then exposed incomplete filtering;
collecting each value corrected both cases. Each behavior was retested through the public
CLI. An initial pytest basetemp parent error required only directory preparation.

The initial full backend run passed **3071 tests, 10 skipped in 393.47 seconds**. After
compression/filtering refinements, the committed implementation passed **3072 tests,
10 skipped in 392.81 seconds**, with **99 related tests** and relevant Ruff checks passing.

Standards review found zero hard policy breaches or separate Fowler smells, but two P2
engineering issues: unprotected JSON reads and counting partial NPZ files. Spec review
found the NPZ issue and a P1 normal-list trace issue. Existing graph capture legitimately
writes `selected_place_evidence` as a list; treating every trace payload as a dictionary
would interrupt final inventory after successful planning. A broken JSON write similarly
would replace optional missingness with a CLI exception.

Public CLI regressions reproduced all three error classes. Long Windows test-output paths
initially prevented trace payload creation and masked two regressions; shorter ignored
temporary paths reproduced the actual `AttributeError`/JSON decode failures. The correction
accepts valid non-object JSON payloads, records broken/unreadable evidence as partial, keeps
readable damaged-file hashes, and validates vector bundles before counting them. A partial
NPZ created before simulated filesystem failure no longer satisfies query-vector coverage.
The correction passed **103 related tests in 15.50 seconds**, including the four added
cases; Ruff and Git diff checks passed. The complete suite result above precedes this
local inventory correction; it is not represented as a post-correction full-suite run.
Both axes rechecked the committed correction and reported zero remaining Standards
or Spec findings; no reviewer changed files or performed live/DB operations.

### One-use preparation and remaining live work

Network/DNS-blocked preparation checked V1, V2 and V3 with zero network attempts, zero
execution credential loads, zero provider sends and no generated results. A presence-only
audit finds all required Foundry, Google, embedding and TripWorld variables. Its initial
case-sensitive dotenv lookup misreported the lowercase Google key; matching existing
Windows/settings case-insensitive semantics corrected the audit, without changing credentials.
Live credential validity and database compatibility remain untested.

The one-use handoff records exact commands, unused output directories, original input,
the existing `sydney-natural` group, preserved V0 provenance, source/dependency hashes,
capture acceptance and stopping/reporting rules. Its final source revision is recorded in
the local package after the documentation commit. Prospective execution is serial V1,
inspection, V2, inspection, V3, inspection, using the required current-session
`gpt-6.1-sol`/`medium` execution child only after explicit exact-plan live approval.

Generation-only proposed retail allowances are **USD 11/12/14, USD 37 total**. The earlier
USD 6 independent evaluation proposal is excluded. Official retail references were rechecked
on 2026-10-08; Foundry uses the declared OpenAI proxy. Prior scenario send counts and
unenforced preference/profile/extraction token assumptions are labelled planning thresholds,
not newly implemented request guards or guaranteed account ceilings. Actual sends and
reported usage determine later estimates; unsupported quantities remain unknown.

Existing runtime deadlines remain 600 seconds per invocation through cleanup, with local
capture IO afterward, zero operator retries, existing main-generation token admission and
existing V3 repair/acquisition limits. Stop before another stage on failed/cancelled runs,
capture/lineage failure, reference threshold exceedance or changed source/date. No automatic
retry, RAG DB bypass, budget/policy adjustment or extra acquisition is authorized.
Real V1-V3 outputs, producer completion, final-source reviews, changed-intake V0 independent
identity and the exact independent final-evidence plan remain pending.

Ignored local evidence identifiers: `artifacts/sydney-generation-evidence-20261008` and
`artifacts/sydney-generation-evidence-handoff-20261008`; short review test outputs also use
`.scratch/ge-*`. These identifiers are historical local locations, not published navigation,
tracker state or shared dependencies. No paid planner/embedding/evaluator call, separate DB
operation, push, PR, merge, branch switch or version freeze occurred.

Subsequent explicit approval consumed the V1 and V2 invocations of this package.
V1 completed; V2 produced an original result after its RAG connection suboperation
timed out before retrieval/embedding. The parent stopped before V3, retaining both
outputs and all observed evidence. Combined retail/proxy estimate: USD 4.388204290;
actual account billing remains unavailable. See the complete
[generation execution and stop record](../v0-v3/development-pilots.md#sydney-v1-v3-generation-execution-2026-10-08).
This later execution does not alter the historical zero-send preparation snapshot or
establish qualified four-version intake, independent quality acceptance or a freeze.

The expressly authorized host resumption subsequently completed genuine V2/V3 retrieval
and generation, retaining V0/V1 and the degraded V2 attempt. Original outputs for all
four versions are now hash-bound in a local generation-only snapshot. Its new retail/proxy
subtotal is USD 4.787736595; the workflow subtotal including the earlier attempt is
USD 9.175940885, with actual account billing unavailable. See the complete
[host generation resumption record](../v0-v3/development-pilots.md#sydney-generation-host-resumption-2026-10-08).
Producer/final-source review bindings, changed-intake V0 independent identity and exact
independent final-evidence planning remain pending; no independent evaluator call occurred.

<a id="sydney-four-version-offline-evaluator-intake-2026-10-08"></a>

## Sydney four-version offline evaluator intake, 2026-10-08

Date: 2026-10-08, Australia/Sydney. Source/review base:
`f730108382ab0e38bbcc0fc24ccec8e3d1f82e62`, branch `feature/evaluation`.
The unrelated pre-existing `.gitignore` edit remains unchanged. Scope is the user-approved
offline intake, existing independent-observation reuse, native scoring and engineering
assessment of the four selected originals. No planner/evaluator implementation, original
output, policy formula or runtime configuration changed. New paid acquisition, formal
benchmark/comparison, thesis conclusions, freezes and remote Git delivery are excluded.
The preceding generation event remains owned by the
[host resumption record](../v0-v3/development-pilots.md#sydney-generation-host-resumption-2026-10-08).

### Actual selected materials and preparation

The selected `sydney-natural` group retains the original input SHA-256
`1b3c50ad9ce9c58a4caf047388f3c4131faa0cddb0ffff2467dd8b2f1593d6ba`:
Sydney, 2026-10-14 through 2026-10-17, two travelers, AUD 1600 and relaxed pace.
The complete human-reviewed RequirementSpec is copied byte-for-byte: Sydney Opera House
exactly once is the sole named hard obligation; interests, transport preference and spacing
remain soft. No daily quota, fixed slot or indoor visit requirement is added.

| Version | Selected original run | Result SHA-256 |
| --- | --- | --- |
| V0 | `sydney-natural-v0-20261007` | `d8ca6c8ac44aa2438f2efe65534b57488be81dbed217bc7d66626801f78431c7` |
| V1 | `sydney-v1-20261008-r1` | `e9046d62d719eeca95247a46873ce1cd475d89fa33775281a76ec9d5ab5f63b1` |
| V2 | `sydney-v2-20261008-r2` | `b261eeba55abafc258e1b87dd0871cf42d8c1abe3aa1caeabdcfb1044da2476d` |
| V3 | `sydney-v3-20261008-r2` | `a86d1335f197dea1cd23c4de02a4a483921ee1c630dd04ef2825f6000e1e7fe6` |

Original result/provenance/usage bytes are copied inside the new batch root. The retained
degraded V2 run is not selected. Agent source-only review inventories every final activity
and original Transfer declaration; native completion receipts attest all four generation
workflows completed. This is producer completion, not human factual review or independent
quality acceptance. The earlier generation-only binding remains unchanged.

Native `rtpeval_batch_1` intake accepts revision 2 of
`sydney-natural-identity-development`; no manually accepted library view substitutes for
this gate. Retaining the batch ID preserves exact V0 activity/occupancy source IDs.
The generic Haymarket food block remains a committed non-primary activity, not free time.
Existing source-linked activity, occupancy, timezone and mode reviews are reused only
against identical input/run/hash/pointer bindings. A new agent density review of the same
complete input binds revision 2 and retains relaxed pace without an exact count.
V3 optional projections are available but excluded from final-only scoring.

### Independent observation reuse and missing identity coverage

Three evaluator-owned historical snapshots pass native manifest, raw-byte hash, request,
attempt-time, derived-payload and historical-ledger validation. They contain eight identity
searches, the earlier eight opening/route captures, and two Museum follow-up captures.
No planner wire, internal validator, RAG result, generation cache or Repair decision is
admitted as independent quality evidence.

The current native identity plan contains 33 distinct keys: 21 Search and 12 Details.
Eleven exact keys reuse historical observations, preserving raw bytes, request context and
actual acquisition times. Twenty-two keys have no matching saved capture. Three reused
Details captures have opening-only masks, so absent names/addresses are not manufactured.
Consequently all 12 unique claimed-ID Details keys need identity-field acquisition or
refresh. Thirteen missing Search keys remain in the full native plan; V1-V3 deterministic
claimed-ID checks do not require those searches as substitutes for Details.

Independent Opera House search resolves the three version-owned V1-V3 requirement targets
with PASS. Their primary visits remain UNKNOWN because original claimed-ID Details lack
identity fields. V0 has seven primary occurrences plus one requirement target awaiting a
new correspondence judgment. Its new `v0_identity_correspondence_3` packet is frozen for
`gpt-6-luna`, but no model is invoked. The changed intake/evidence digests prohibit reuse
or relabeling of the old model response. The historical Museum address FAIL and its
separate saved assessment remain intact; missing current judgment is UNKNOWN.

### Native scoring and assessment

All final scorers execute over the accepted four-version intake. The current evidence plan
contains one Details key for the independently identified Opera House requirement target;
unresolved primary identities leave their opening/route acquisition references pending.
A derived replay view imports that exact historical Details record, with explicit source
manifest/plan/record hashes and preserved capture times. Its native ledger counts one
historical capture; this offline execution sends zero requests. No unrequested snapshot
record or artificial budget exhaustion is invented to force scoring.

| Version | Primary grounding UNKNOWN | Opening UNKNOWN | Routes UNKNOWN | Decidable non-overlap PASS |
| --- | ---: | ---: | ---: | ---: |
| V0 | 7 | 7 | 3 | 11 |
| V1 | 10 | 10 | 6 | 16 |
| V2 | 8 | 8 | 4 | 12 |
| V3 | 9 | 9 | 5 | 14 |

All four exact-once requirement checks remain UNKNOWN because their primary occurrence
identities are unresolved. Known commitment intersections total zero seconds. V0 retains
one ambiguous final-day transport association and an unresolved occupied-time population;
its non-overlap applicability denominator and total therefore remain unavailable despite
11 decidable checks passing. A complete processing status does not assert complete
evidence or every itinerary passing.

Source-distinct daily counts are V0 `2/2/2/1`, V1 `3/2/3/2`, V2 `3/2/2/1` and
V3 `3/2/2/2`. The existing relaxed-pace formula yields mean daily deductions of 5, 20,
15 and 10 points respectively. These are operational formula checks, not invented hard
requirements or comparative research findings. Native V1-V3 auxiliary values are 20,
driven solely by verified non-overlap with UNKNOWN contributing zero in the other four
dimensions; resulting totals are retained locally. They must not be interpreted as
complete factual quality measurements or version rankings.

### Verification, preservation and next acquisition boundary

The first local helper reached valid intake and identity replay, then failed while writing
an `IdentityJudgmentPacket` directly as JSON. The local correction uses its public
`to_dict()` conversion and a fresh revision-2 directory; failed revision-1 materials remain
preserved. No original artifact or provider request was affected.
The compact-summary aid also initially assumed every metric exposed `state`; selecting
only fields present in the native metric schema corrects that local `KeyError`. Subsequent
summary, preservation and document checks pass without changing any scorer output.

The corrected preparation passes native intake, current identity-report replay, occupancy
source matching, requirement/schedule and route preparation. Six public CLI consumers
(intake, identity, requirement/schedule, opening, routes, quality) each reproduce identical
JSON and return codes in a second offline invocation. Identity returns 3 for expected
missing evidence; the other five return 0. Network/DNS/socket guards record zero attempts.
All 56 directly referenced original files and the earlier 541-file preservation inventory
remain unchanged. The 286 frozen generation/source/configuration files also remain
unchanged. This task changes only tracked engineering documentation; full product tests
are not rerun for local artifact preparation.

Usage intake retains V0's partial capture and V1-V3's native coverage rather than promoting
unknown account billing or coverage to zero. New evaluator provider sends, model sends
and acquisition expenditure are all zero. Historical snapshot ledger entries are not
added to this execution's costs.

Ignored local evidence identifier: `artifacts/sydney-four-version-evaluator-20261008-r2`.
It contains the native manifest/intake, source-only and completion attestations, exact
original copies, independent reuse provenance, pending V0 packet, identity/schedule/
density/opening/routes/quality reports, CLI replay receipts and preservation assessment.
Revision 1 identifies the preserved local serialization failure. These paths are historical
local identifiers, not shared documentation dependencies or additional task authorities.

The next concrete identity acquisition inventory is 12 distinct Details field refreshes
and one new V0 correspondence request. It is not an executable authorization: field masks,
wire bodies, measured token preflight, exact cost allowance and live execution child still
require a prepared, approved package. After identity replay, freeze actual opening/route
keys against independently reviewed endpoints, modes and departure semantics; then acquire
only supported missing evidence and rerun the native scorers. Retain actual FAIL/UNKNOWN,
the generic-food occupancy and unresolved transport. No final independent quality
acceptance, freeze or formal version comparison is established by this offline stage.

<a id="formal-four-final-execution-2026-10-09"></a>

## Formal four-final execution implementation — 2026-10-09

Status: implemented, offline validated and independently reviewed; fresh Sydney execution
and final acceptance remain pending. Issue [#87](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/87)
owns the task. Starting review point was `2e7f3e6a482a3a4f5ecc6224750e6f02bca3ac0e`.
Local implementation commits are `affc639` (complete V0 case-set binding), `cdd2fa3`
(timed unbound V0 occupancy), `276358c` (formal execution/replay) and separate review
correction `7fe0c52`. Documentation was still uncommitted at this validation checkpoint;
the unrelated existing `.gitignore` modification was preserved. No push/PR/merge or
version freeze is included.

### Decisions and observed implementation

The user approved offline development and confirmed public seams `prepare_run`,
`execute_run`, `replay_run`, actual CLI, `resolve_versioned_identities` and
`score_requirement_schedule`. The formal evaluator client composes fresh independent
Google search/Details, one V0 correspondence request, version-owned API/program identity,
snapshot-derived coordinates, hours/directed routes and native requirement/schedule,
opening, route, density and quality consumers. The original outputs are not regenerated
or repaired. Final-only scope identifies optional V3 stages and human/controlled/official
tracks as outside the run.

The binding unit is the complete current-policy V0 case set, with original source
occurrences, claims, ordered candidates, capture/raw provenance and related RequirementSpec
meaning. Batch wrapper changes can remap unchanged cases; relevant changes reject import.
The original packet/response/times remain preserved, and result-1/historical contracts
retain exact old matching. This fixes applicability without certifying freshness or
backfilling this acceptance run from old evidence.

A declared V0 transport activity keeps occupancy from its own clock when its primary
route endpoints cannot bind, including generic food/free-time endpoints. Invalid clocks
remain UNKNOWN and established intersections remain FAIL. Route identity and mode
uncertainty are preserved. Schedule and route rule versions advance to 2; historical
reports require their original rule/code revision for exact reproduction.

### Failure, correction and validation sequence

Public-boundary red tests first exposed absent execution/binding support and the V0
occupancy denominator gap. During incremental implementation, native route preparation
used `evidence_plan`, not the initially assumed `snapshot_plan`; malformed lookup was
corrected. A model connection error initially escaped without a final receipt; catching
the native `TransportFailure` fixed stopped-report preservation. A replay test then showed
that changed HTTP response bytes with recomputed file hashes could detach model material
from the actual response; replay now verifies request/response/times/usage and regenerates
the route plan before comparing final reports. Stopped-attempt cost tests added null
actual billing and unpriced failure accounting instead of discarding already sent requests.

The first complete evaluator regression had 1156 passed, one skipped and two failures.
One was the old import guard's inability to distinguish the new execution boundary from
offline scorers; a narrow module/import allowlist retained the planner-free core rule.
The other expected a null occupancy denominator for a known-time V0 activity with reversed
endpoints; the approved occupancy change establishes three schedule units while its route
remains UNKNOWN. Affected tests then passed 202 cases with one skipped. New binding,
execution and occupancy boundaries passed 22 cases. The full backend gate subsequently
passed **3098 tests, 10 skipped**, in 291.37 seconds, with external network blocked.

Independent Standards review found two issues: a tokenizer `RuntimeError` after Google
sends could bypass final receipts, and usage events retained full request wire despite the
metadata-only contract. Spec review found two more: density UNKNOWNs were omitted from
the inventory, and identity UNKNOWNs did not link the source-owned HTTP failure cause.
Review regressions reproduced the missing density/failure linkage and escaped runtime
error. Correction `7fe0c52` adds offline tokenizer preflight and runtime-error capture,
allowlisted usage projection, density UNKNOWN units and acquisition links, including shared
version-owned requirement evidence and directed route prerequisites. Full wire stays in
the independent HTTP journal. All **23** affected public-boundary tests passed afterward;
both review axes rechecked their findings as resolved with no material new regression.
The full backend gate predates this correction; its affected execution/binding/occupancy
tests were rerun, and Ruff plus whitespace checks pass. No live request was used to test
these corrections.

Mocked actual CLI preparation/execution/replay and a separate replay subprocess complete
the native flow. HTTP tests preserve WALK time independence, DRIVE `TRAFFIC_UNAWARE` and
original TRANSIT departure/direction, with one shared request retaining four source/version
verdicts. Failed HTTP, connection, runtime dependency, reference-cost exhaustion, source
drift, whole-run deadline, consumed-directory refusal and detached response bytes are
covered. Synthetic tokenization tests structure and limits, not real payload measurements.

### Preserved originals and proposed fresh package

The original Sydney input hash remains
`1b3c50ad9ce9c58a4caf047388f3c4131faa0cddb0ffff2467dd8b2f1593d6ba`;
reviewed RequirementSpec remains
`76682ad7b594daf6bef437a755d96194b3ece9f1c103e8fd7bf6013933d13eaf`.
Its sole hard visit obligation remains Sydney Opera House exactly once; soft pace/food/
architecture/museum/harbour/walk/transit preferences introduce no daily quotas or tour rule.
The four selected original output hashes match Issue #87 exactly; V2 uses successful r2.
The unrelated `.gitignore` bytes retain SHA-256
`fdc63780f304bde2f8ac48b7e520330bc45254e8799cb4323cfe645c82a3ae02`.

The actual formal CLI prepares the accepted originals and reviewed contexts offline with
exit 0. New local evidence identifier:
`artifacts/sydney-fresh-evaluation-preparation-20261009-r1`.
Preparation digest is
`2debadce52a9278e7efad68cfe0fda955a7fac8ec9abbe33a6420269232a19fa`.
This is a proposed unconsumed package, not execution authorization or an evaluation result.
It freezes code at `7fe0c52`, 21 distinct original Search keys, 12 supplied-ID Details keys
and 35 acquisition references. Second-phase identity/route keys are derived only from fresh
evidence, with conservative ceilings of 35 Details and 18 directed matrix elements.

Proposed limits: 86 Google sends across both phases, one `gpt-6-luna` V0 model request,
18000 input-token sizing allowance, 3000 maximum output tokens, 120-second request timeout,
900-second total timeout, zero retries and USD 2 reference allowance. The published retail
scenario is at most USD **1.705750**: 21 Search at 0.032, 47 total Details at 0.020,
18 matrix elements at 0.005 and conservative model cache-write/output exposure of 0.003750.
The price basis was checked on 2026-10-09 against the
[Google global table](https://developers.google.com/maps/billing-and-pricing/pricing) and
[OpenAI GPT-6 Luna rates](https://developers.openai.com/api/docs/models/gpt-6-luna).
OpenAI rates proxy inaccessible Foundry billing; tax, account discounts, free tiers and
credits are excluded. The price book's validity interval is explicit. These figures are
planning estimates, not observed charges or an invoice cap.

Offline vocabulary validation succeeds. The initial case-sensitive presence check incorrectly
reported a missing Google key. A user-prompted recheck finds a nonempty `Google_Maps_API_Key`
in the project `.env`; the actual CLI's `load_dotenv` followed by uppercase `os.environ`
lookup succeeds on Windows. This was a presence-check error, not a sandbox access failure.
The Foundry key and deployment are also present. No credential value is recorded and no
request has verified live credential validity. Explicit approval of this exact prepared
scope remains the live prerequisite. New evaluator/model/provider sends and expenditure in this implementation
task are zero. Old acquisitions remain historical evidence. Issue #87 cannot close until
fresh evidence, saved-evidence replay, original preservation and final report acceptance
are completed. This record establishes no benchmark, ranking or research conclusion.


<a id="sydney-four-final-fresh-acceptance-2026-10-09"></a>

## Sydney four-original fresh evaluation acceptance — 2026-10-09

Status: the full final-only automatic workflow is accepted under the current evaluator
policy, with explicit unresolved facts and semantic limits. This is bounded engineering
acceptance for Issue [#87](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/87),
not a formal benchmark, version ranking, human review or freeze. All four original
outputs and the reviewed Input/RequirementSpec remain unchanged.

### Authorization, revision and actual execution

The user explicitly approved the exact prepared package and requested fresh independent
acquisition, full evaluator execution, saved-evidence zero-network replay, source
preservation and item-by-item FAIL/UNKNOWN assessment. Approved ceilings were 86 Google
sends, one V0 `gpt-6-luna` model send, zero retries, USD 2 reference allowance, 18000 input
sizing tokens, 3000 output tokens, 120-second request and 900-second total timeouts.
The preparation digest remains
`2debadce52a9278e7efad68cfe0fda955a7fac8ec9abbe33a6420269232a19fa`.
Source HEAD was `925bd0a19899ed7b16a6669db6a925e91b9b045a`; operational code was frozen
at `7fe0c52`. The only unrelated working-tree change was the existing `.gitignore`,
whose previously recorded SHA-256 was preserved before and after execution.

A current-session execution child used `gpt-6.1-sol` with `medium` reasoning and ran the
formal `evaluation_run_cli execute` command once, loading `.env` without exposing values.
No connectivity probe, retry, bespoke acquisition runner, planner regeneration, Repair,
mode substitution, date shift or V1-V3 evaluator model call occurred. Historical API/model
evidence was not substituted. Original reviewed authoring contexts remained source-bound.

Execution ran 02:03:06.080827 through 02:03:34.221506 Australia/Sydney, lasting
28.140679 seconds. Exit code was 0 and stderr empty. Actual sends were **64 Google**:
21 Search, 28 Details and 15 one-cell directed matrices, plus **one V0 model request**.
All 65 HTTP receipts were 200/completed. The initial identity phase used 33 Google sends;
the freshly derived second phase used 16 Details and 15 matrices. Shared requests retained
separate source/version judgments. Retry count was zero; the maximum observed request
was 6.936869 seconds. All approved bounds were respected.

The model reported 12411 input tokens, 979 output, 13390 total, zero cached input and
12408 cache-write input. Observed sends and reported usage produce a retail reference
estimate of **USD 1.3090408**: Search 0.672, Details 0.560, matrices 0.075 and model
0.0020408. Actual account billing is unavailable/null; these estimates are not invoice
charges and exclude credits, free tiers, discounts and taxes. The dated price book and
its previously checked official sources remain bound to the report.

Local evidence identifiers (not published dependencies):
`artifacts/sydney-fresh-evaluation-preparation-20261009-r1/run/execution` contains
`report.json`, `receipt.json`, `usage.json`, raw HTTP journal, both new snapshots,
V0 material and native component reports. The parent directory retains command stdout/
stderr, authorization, replay checks and `acceptance.json`/`acceptance.md`. Final report
SHA-256 is `09272f235cadc20aeb94f4c6a4f5945f35a77faaf89637611beb422695e0b459`.

### Saved-evidence verification and native outcomes

A separate process invoked the actual `replay` CLI with DNS/socket connection entry points
blocked. Exit code was 0; network attempt count was **0**, and the reconstructed final
report matched the saved report exactly. Replay checked all **205 receipt-covered files**,
raw response hashes, V0 HTTP/model/timing/usage linkage, identity decisions and newly derived
route preparation before recomposing native quality. The post-run native source/code check
and direct original-output hash checks passed. Original Input and RequirementSpec hashes
remain those in the preceding preparation record. No execution artifact was edited to
obtain a match. No implementation change required another backend test run.

Processing and acquisition are `complete`, with no acquisition failures. Evidence is
`unresolved`; a completed process does not certify every fact. Identity's aggregate
`needs_evidence` status is retained, including the two unadopted address-FAIL cases;
it is not a missing-command or absent-snapshot status. Native quality totals are available
for all four finals. Counts below are **PASS / FAIL / UNKNOWN**; density is an auxiliary
soft-profile adjustment, not an added hard requirement.

| Version | Requirements | Grounding | Non-overlap | Opening | Routes | Mean density penalty | Overall score |
| --- | --- | --- | --- | --- | --- | ---: | ---: |
| V0 | 1 / 0 / 0 | 7 / 0 / 0 | 12 / 0 / 0 | 5 / 0 / 2 | 3 / 0 / 0 | 5 | 89.2857 |
| V1 | 0 / 0 / 1 | 8 / 2 / 0 | 16 / 0 / 0 | 6 / 0 / 4 | 6 / 0 / 0 | 20 | 48.0000 |
| V2 | 1 / 0 / 0 | 8 / 0 / 0 | 12 / 0 / 0 | 4 / 0 / 4 | 4 / 0 / 0 | 15 | 75.0000 |
| V3 | 1 / 0 / 0 | 9 / 0 / 0 | 14 / 0 / 0 | 5 / 0 / 4 | 5 / 0 / 0 | 10 | 81.1111 |

These are current-policy outputs for one engineering case; they support no version-level
ranking or research conclusion. The optional V3 `draft`/`final_primary` projections and
human, controlled-Repair and official-audit tracks are explicitly outside this run.

### Every retained UNKNOWN

All fourteen opening UNKNOWNs were individually checked against the newly captured raw
Details bytes. Each requested both current and regular hours; HTTP 200 omitted both fields.
None resulted from a failed request, old snapshot, model binding rejection or unexecuted
stage. Public-space access and exterior-only intent were not inferred from names.

| Item | Version | Date/scope | Original venue or obligation | Retained cause |
| --- | --- | --- | --- | --- |
| 1 | V1 | Whole trip | Sydney Opera House exactly once | `count`: bounds 1..3; one confirmed and two unadopted potential visits |
| 2 | V0 | 2026-10-14 | Sydney Opera House | `hours_missing` |
| 3 | V0 | 2026-10-17 | Powerhouse Museum | `hours_missing`; API also reports `CLOSED_TEMPORARILY` |
| 4 | V1 | 2026-10-14 | Sydney Opera House | `hours_missing` |
| 5 | V1 | 2026-10-14 | Sydney Harbour Bridge | `hours_missing` |
| 6 | V1 | 2026-10-15 | Darling Harbour | `hours_missing` |
| 7 | V1 | 2026-10-17 | Bondi Beach | `hours_missing` |
| 8 | V2 | 2026-10-14 | Sydney Opera House | `hours_missing` |
| 9 | V2 | 2026-10-14 | Sydney Harbour Bridge | `hours_missing` |
| 10 | V2 | 2026-10-14 | The Rocks | `hours_missing` |
| 11 | V2 | 2026-10-16 | Darling Harbour | `hours_missing` |
| 12 | V3 | 2026-10-14 | Sydney Opera House | `hours_missing` |
| 13 | V3 | 2026-10-14 | Sydney Harbour Bridge | `hours_missing` |
| 14 | V3 | 2026-10-14 | The Rocks | `hours_missing` |
| 15 | V3 | 2026-10-17 | Bondi Beach | `hours_missing` |

Item 1 follows the existing conservative count contract: the two V1 address-FAIL visits
have verified API associations with Harbour Bridge and Maritime Museum, but no adopted
canonical identity. The requirement counter therefore leaves both as potential Opera House
matches despite those distinct associations. The bounds are policy-induced uncertainty,
not independent evidence of three Opera House visits. This semantic limitation is retained
explicitly rather than turned into PASS or hidden as an API failure.

Powerhouse's raw `businessStatus=CLOSED_TEMPORARILY` is preserved. The hours scorer does
not convert that current, undated status into closure for the planned 2026-10-17 visit.
Its UNKNOWN is not proof of feasibility. Considering business status or external/exterior
access would require an explicit policy change; no such reinterpretation occurred here.

### Every retained FAIL and interpretation limits

Two grounding FAILs are the current literal `api_address_mismatch` rule:

| Version / original venue | Submitted address | New API formatted address |
| --- | --- | --- |
| V1 / Sydney Harbour Bridge | Sydney Harbour Bridge, Sydney NSW, Australia | Sydney Hbr Brg, Sydney NSW, Australia |
| V1 / Australian National Maritime Museum | 2 Murray St, Darling Harbour, Sydney NSW 2000, Australia | 2 Murray St, Darling Hbr, Sydney NSW 2000, Australia |

The differences are abbreviations, not independent proof of different physical locations.
Both original claims and native FAILs remain unchanged. No normalization, model fallback
or post-hoc correction was applied to improve the result.

Six daily-density FAILs retain the configured relaxed-profile soft penalties:

| Version | Date | Primary visit count | Daily penalty |
| --- | --- | ---: | ---: |
| V0 | 2026-10-17 | 1 | 20 |
| V1 | 2026-10-14 | 3 | 40 |
| V1 | 2026-10-16 | 3 | 40 |
| V2 | 2026-10-14 | 3 | 40 |
| V2 | 2026-10-17 | 1 | 20 |
| V3 | 2026-10-14 | 3 | 40 |

There are no native requirements, non-overlap, opening or route FAILs in this run.
The sole hard user obligation remains Opera House exactly once; these density outcomes
add no hard daily quota. All FAIL/UNKNOWN sources and reasons remain in the full report
and parent acceptance inventory. The engineering end-to-end objective is fulfilled;
address equivalence, verified-association count semantics, business-status treatment and
public-space access remain explicit policy limitations, not silently resolved facts.

<a id="requirement-physical-association-correction-2026-10-09"></a>

## Requirement physical-association correction — 2026-10-09

Status: implemented and offline validated under
[#88](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/88). Fixed review base:
`ee0f4947edb32fe2f7a07f5b4fd7c1ee98fd6531`; implementation/test commit: `2f9dd6f`.
An unrelated pre-existing `.gitignore` edit was excluded. No planner output, identity
grounding verdict, opening policy, route policy or original execution receipt was edited.

The fresh #87 evidence already verified the two V1 address-FAIL occurrences as Harbour
Bridge and Maritime Museum. Canonical-only requirement matching nevertheless treated
them as possible Opera House occurrences. This widened the exact-once bounds to 1..3.
Requirement/schedule rules version 3 consumes the verified physical occurrence association
only after complete source-bound identity replay. Targets remain version-owned adopted
canonical identities; their failing grounding components, occurrence roles, dates and
time uncertainty are preserved. Historical identity policies retain canonical-only matching.
The new `requirement_identity` diagnostics expose the physical and grounding provenance.

### Failure, correction and validation

The first attempted red test lacked its local parent test directory; creating that
directory allowed the actual regression to run. It failed as intended: the public scorer
returned UNKNOWN instead of PASS for a verified different venue with address FAIL.
The minimal implementation passed that regression. Expanded tests initially reported
45 passes and three failures because a fixture selected a requirement subject instead
of a primary visit with the same name. Restricting fixture selection to `primary_visit`
corrected the test setup; the suite passed 48, then 50 after duplicate-venue and V0 cases.

Public scorer and actual CLI coverage includes counts, dates, exclusions, fixed times,
target FAIL preservation, same/different venues, V0 validated correspondence, missing or
conflicting evidence, forged association/source/version rejection and historical rules.
The full backend gate passed **3112 tests, 10 skipped**, in 310.40 seconds. Ruff and
`git diff --check` passed. Independent Standards and Spec reviews of the committed
implementation each reported zero findings; no review correction commit was needed.

### Separate offline recalculation and original replay

The actual requirement and quality CLI entry points recalculated from the original
fresh evidence with DNS/socket access blocked: exit codes 0/0, zero network attempts.
All 205 protected receipt files and four original outputs passed unchanged-file checks.
V1's exact-once bounds became **1..1**, requirement PASS, with overall score **68.0000**
instead of 48.0000. Its grounding remains 8 PASS / 2 FAIL. Fourteen opening UNKNOWNs
remain; all opening, route, non-overlap, grounding and density results are unchanged.
Other overall scores remain V0 89.2857, V2 75.0000 and V3 81.1111. These values describe
one engineering correction and do not support a formal version comparison.

Local evidence identifiers, not published dependencies:

- Original execution: `artifacts/sydney-fresh-evaluation-preparation-20261009-r1/run`.
- Separate corrected output: `artifacts/sydney-requirement-association-recalculation-20261009-r1`;
  `requirements.json`, `quality.json` and `recalculation-check.json`.
- Original-rule replay: `original-rules-replay.stdout.json` and
  `original-rules-replay-check.json` in that separate directory.

| Material | SHA-256 |
| --- | --- |
| Original preparation | `2debadce52a9278e7efad68cfe0fda955a7fac8ec9abbe33a6420269232a19fa` |
| Original report, unchanged | `09272f235cadc20aeb94f4c6a4f5945f35a77faaf89637611beb422695e0b459` |
| Original receipt, unchanged | `ca5852385f6fcdeb1279afbb25ddfdc8da8d11a64514836b88bf824406bae0e1` |
| Corrected requirements | `e7011d0697813bc1d564b905a453112121d552135eef16ad887e00eed1377ebc` |
| Corrected quality | `664479d3fc9a4e8af6b6c09fd03815038f967ea42ce77e503be920f5a10f700a` |
| Current requirement scorer | `a4b12481969d8a156e26fa7111232e70d37a1d245e09bdef6f8490d656a83d6b` |

In an isolated process, the trusted scorer source from the fixed base was loaded without
checking out or editing the repository. The formal `evaluation_run_cli replay` then
reproduced the original rules-2 report exactly: exit 0 and zero network attempts.
Current rules-3 recalculation remains a separate result; it is not a fresh acquisition
or a replacement execution receipt. No additional Google/model calls or cost were incurred.

The remaining opening issues need explicit access, evidence-applicability and closure
semantics. The [opening proposal](opening.md#opening-access-boundary-proposal-2026-10-09)
records advice only; it does not alter current scoring or authorize collection.

<a id="google-address-equivalence-acceptance-2026-10-09"></a>

## Google-supported address equivalence acceptance (2026-10-09)

Status: implemented and offline-validated under
[#92](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/92). The user approved
binary address comparison, public resolver/CLI TDD seams and Issue publication. The
fixed review base is `35499b65fabebdfe1cb572123d7fb9bdeabfcd15`; implementation is
`c77fbed`, with review correction `590ac9d`. Shared regression also includes the
separate [V3 pace scope](../v0-v3/v3-development.md#soft-pace-repair-acceptance-2026-10-09)
through `0a4a96b`. The unrelated pre-existing `.gitignore` edit was excluded. No live
request, original-output rewrite, Git publication or formal comparison was authorized.

Policy `versioned_api_identity_4` uses the same independent Google observation's
long/short address component pairs, after provenance and ID/name checks, to explain
the complete original address. Exact/format equivalence and supported aliases PASS;
unexplained differences and conflicting aliases FAIL. Missing independent observations
remain identity uncertainty, rather than fabricated address judgments. V0 correspondence
and historical policies 1-3 retain their original replay paths.

### Test and review sequence

Initial public-boundary tests reproduced supported aliases failing under literal rules.
Implementation then passed alias, number/city, missing/conflicting component, original
immutability, real CLI and historical-reconstruction checks. Negative provenance tests
also caught misleading comparison PASS records on unverified observations; comparison
auditing was restricted to verified attempted comparisons before the implementation commit.
Two early test assumptions were corrected: whole-batch CLI exit includes unresolved
other versions, and assertions about a historical address case must target that version.

Independent Spec review found two P2 defects: a cross-linked long/short endpoint could
excuse another street, and an unbound requirement's unique candidate could lose its
address FAIL in a search UNKNOWN. Failing public tests reproduced both. The first
subject test accidentally supplied the search helper with the wrong shape; a corrected
fixture independently reproduced UNKNOWN instead of FAIL before the fix. The correction
rejects conflicts on either alias endpoint and retains candidate-level binary comparisons.
A unique eligible mismatch is FAIL; multiple candidate identities remain independently
uncertain. Tests cover unique FAIL, multiple FAIL comparisons, a surviving PASS alongside
FAIL, and source-bound report reconstruction. Standards review's separate P3 V3 duplication
was corrected in `0a4a96b`; both axes then reported zero remaining findings.

An early broad run failed 22 tests (3161 passed, 10 skipped): the pure numeric helper's
import allowlist, current policy/wire/prompt assertions, synthetic optional-field fixtures,
and a tuple/list construction in a new date-override test required correction. A separate
overlapping wire/preparation run observed a source-binding mismatch while implementation
files changed. After correcting the tests and freezing production sources, the full backend passed **3195 / 10 skipped** in
464.36 seconds at `32be42d`. After the review corrections, the address/public-CLI and
complete V3 gate passed **483** in 30.28 seconds at `0a4a96b`. Ruff and whitespace checks
passed. Because the correction adds candidate audit fields, the complete evaluator suite
then passed **1248 / 1 skipped** in 425.16 seconds at the same revision, covering downstream
scoring, source binding and replay. Local gate identifiers are
`artifacts/address-pace-tests/full-stable.log`, `review-green.log` and
`evaluation-review-final.log`; these are evidence identifiers, not published dependencies.

### Retained evidence recalculation

With DNS and sockets prohibited, public `resolve_versioned_identities` first reconstructed
the accepted policy-3 identity report exactly, then separately applied policy 4. Only two
grounding/canonical outcomes changed, both V1 FAIL to PASS:

| Original venue | Google-supported pair | Result |
| --- | --- | --- |
| Sydney Harbour Bridge | `Sydney Harbour Bridge` / `Sydney Hbr Brg` | PASS |
| Australian National Maritime Museum | `Darling Harbour` / `Darling Hbr` | PASS |

All other address words/numbers remain matched. The local receipt identifier is
`artifacts/address-pace-tests/retained-address-check.json`. The accepted #91 full report
SHA-256 remains `8992422ca3953fd1d90f059674da68e1f18e1730f5816157a876a8b7d7c1c83b`;
its receipt remains `5ea846bccf2ededed1275bbc3690b36659c46c2a262a32b7fbabb165a42e5c7c`.
All four original output hashes remain unchanged. Google/model sends and additional cost
are zero. This is an identity-only engineering recalculation, not a newly bound four-version
quality report. New implementation bindings and any additional live judgments require
separate preparation and authorization; the old report/receipt are never relabeled.

<a id="complete-v0-identity-coverage-acceptance-2026-10-09"></a>

## Complete V0 identity coverage and same-output evaluator (2026-10-09)

Status: implementation, independent live evaluation and complete native/quality CLI
acceptance validated. Residual itinerary judgments remain visible.
The human authorized strengthening complete identity coverage and
direct evaluator execution, with current execution approvals defaulted. Review fixed
point is `a452aa5089d4e79781ede289d8a07434bbf3deb6`; implementation is
`779dc8aaef8f88c6801e0391344fc639cce2a586`. The unrelated pre-existing `.gitignore`
change remains excluded. No planner regeneration, scoring-rule change, automatic retry,
remote Git delivery, formal comparison or version freeze belongs to this task.

### Failure, correction and offline checks

The preceding completed model response judged one of eight required V0 cases and
omitted all seven visits. Strict import stopped rather than accepting incomplete
coverage. The original generation, both stopped reports and raw responses remain
historical evidence; this correction does not edit or relabel them. Their full account
is retained in the [source-protected execution record](../v0-v3/v3-development.md#source-protected-v3-cli-execution-2026-10-09).

An actual CLI regression first failed because the request allowed an arbitrary-length
array instead of requiring every case. The request now uses a strict `decisions` object
with all owned short IDs required. Shared address-presence definitions avoid repeating
all judgment properties for every reference. Exact count/IDs, visit and subject coverage,
key/value identity agreement and explicit UNKNOWN on insufficient evidence are stated
before dispatch. Import rejects incomplete/foreign/duplicate coverage, old arrays and
foreign candidates, while retaining original citation/address/destination validation.
Only a validated object is converted to internal rows; provider bytes stay unchanged.
Historical uniform/legacy V0 array requests retain their original branches.

The red CLI test passed after the minimal fix. Final affected validation passed
**204 tests in 136.27 seconds**, including synthetic provider responses, success and
six invalid-response CLI cases, source binding, historical paths, opening integration
and exact zero-network stopped/successful replay. Ruff and diff checks pass.
An earlier full run was stopped after the legacy compatibility correction so the
complete gate would test the final implementation. Independent Standards and Spec
implementation reviews report zero findings. The final full backend passed
**3231 tests, 10 skipped, in 672.12 seconds**. No frontend test is implied.

### Frozen execution package

Original V0-V2, reviewed Input/RequirementSpec and the source-protected V3 remain
unchanged. V3 result SHA256 is
`ecd6d368b4467fc3a49995dc925d983475fa14cf08beb9cdd4870e7d69ea7e6f`.
The separate package preserves batch revision 4 and source-linked role/occupancy,
route and density reviews. Offline preview against retained candidate facts measures
**15,606** complete request tokens including framing, below the 24,000 allowance;
those preview facts will not be used as new independent execution evidence.
The prepared implementation and digest match, and native credential presence checks
pass without exposing keys or sending provider requests.

Preparation SHA256 is
`2979edd919a3ac0572d33385a47c83ace4768bd8fb7d3d918ad12989fa771da3`.
Limits are **86 Google**, **one gpt-6-luna identity call**, medium, 24,000 input /
3,000 output tokens, 120-second request / 900-second overall and **USD 2.76** reference
allowance, with zero retries. A separate eligible missing-hours assessment may use
zero Google, one medium model call, 32,000 input / 8,000 output tokens and USD 0.05.
These are reference-price reservations, not account billing caps. Current-session
execution children must use `gpt-6.1-sol` / medium and only their frozen handoff.

Local evidence identifier:
`artifacts/sydney-v3-identity-coverage-evaluator-20261009-r1`.
It is ignored evidence, not a published dependency.

### Output-budget stop and separate correction

The one-use initial execution exited 2 in **34.326 seconds**. It acquired 35 Google
requests and made one model call, without retries. The provider returned `incomplete`
with `max_output_tokens`: **15,132 input / 3,000 output**, including **2,346 reasoning
tokens** within output. Strict import rejected the incomplete response. No identity,
route or quality report was completed; omission coverage cannot be inferred from this
truncated material. Reference usage was **USD 0.967391425**, actual billing unavailable.
The stopped receipt is
`d71e8f9621dad7fe91f690070cf80f4bbc984283a13ee7ffb19bf9bbf3f3f2e8`.

The parent prepared a separate corrected package under the current default approval,
raising only the output allowance to **8,000**. Medium reasoning, the 24,000 input
limit, original sources, source reviews, code, scoring rules and time limits remain
unchanged. Fresh independent acquisition is required; the consumed package is not
resumed or overwritten. Previewing the just-acquired packet measures **17,564** input
tokens including framing. Conservative reservation is **USD 2.759** for at most 86 Google
and one model, within the unchanged USD 2.76 allowance. Including the first stop, the
current step's bound is 121 Google and **USD 3.727391425**, below USD 5.50. It contains
two separate prepared identity attempts, with zero automatic transport retries.
New preparation SHA256 is
`a0a86549b778aba37c576d59536d0742fbc77fd5e3123bae93d38eb37e510774`.
The corrected execution exited zero in **42.969 seconds**. The response is `completed`
and supplies all **eight** owned decisions exactly once. Actual usage is **67 Google**,
one model, **12,635 input / 2,640 output** tokens, including 1,552 reasoning tokens
within output, and **USD 1.3818993** reference cost. Processing and acquisition complete;
there are no acquisition failures. The native report retains 13 missing-hours checks
before supplemental access assessment. Its receipt is
`bb21c07cd07c3d8d6fb0d9592c653d5d6e739530ec7c590040dfeb9a4d423040`.

### Missing-hours assessment and final acceptance

Opening preparation initially rejected the inherited identity-only `reasoning_effort`
options field, without a provider send or execution directory. Removing that field
retained the opening workflow's fixed medium policy; no production change was needed.
The rejected options are preserved separately. The valid packet freezes 13 cases,
16,638 complete input tokens including framing and USD 0.008 maximum price reservation.
Preparation SHA256 is
`959445ff374d1cd0da96e5d77baa30b8e9844a281d89bb6cf7156c47c8da44db`.

One opening model call, zero Google and zero retries completed in **25.468 seconds**.
Actual usage is 14,905 input / 2,364 output tokens, with 807 reasoning tokens already included
in output, and **USD 0.00304505** incremental reference cost. Twelve judgments PASS for
ordinary public-landmark or outdoor viewing under the existing common policy; these
are `llm_access_reasonableness` judgments, not API-certified opening hours. V0 Powerhouse
indoor admission remains UNKNOWN. Neither missing hours nor undated temporary closure
was converted into confirmed future opening or closure.

With credentials removed and DNS/TCP blocked, actual `replay`, `replay-opening` and
manifest-based quality CLI all exit zero and reproduce the same source-bound component
reports and totals. Repeated quality CLI JSON is byte-identical. All three stopped
attempts also retain their expected exit 2 reports and unchanged closed receipts.
All **832** generation/preparation/execution files checked before and after replay are
unchanged. Original Input, V0-V2, prior/current V3 and `.gitignore` hashes match.
Opening receipt is
`76e09abfa9d95b93e4b9bf4e04280295d42dfb087a9751ef07a9f6c89dca2ce2`;
final native report is
`b45d2b5af5d817a73420a9bf06f44b589bb68ee69976a794177c911acbe5df7d`.

| Version | Overall score | Grounding FAIL | Opening UNKNOWN | Mean soft pace deduction |
| --- | ---: | ---: | ---: | ---: |
| V0 | 89.2857 | 1 | 1 | 5 |
| V1 | 80.0000 | 0 | 0 | 20 |
| V2 | 85.0000 | 0 | 0 | 15 |
| V3 | 100.0000 | 0 | 0 | 0 |

All four Opera House exact-once requirements PASS. V1-V3 have no factual FAIL/UNKNOWN
under the current rules. V0's address FAIL is the model's `incorrect_claim` assessment
of Australian Museum's original `College Street, Sydney` against the independent
candidate's William Street address; recognizing the venue does not repair that claim.
V0 `day4_powerhouse`, 2026-10-17 10:00-12:15 Sydney time, remains UNKNOWN because
`Explore the Powerhouse Museum` implies indoor admission and neither applicable hours
nor admission evidence is supplied. Its reasons are `hours_missing` and
`llm_access_reasonableness_unknown`; HTTP acquisition itself succeeded.
Five auxiliary daily pace deductions remain: V0 Oct 17 (count 1, 20 points), V1 Oct 14/16
(count 3, 40 points each), V2 Oct 14 (count 3, 40 points) and Oct 17 (count 1, 20 points).
Daily means produce the table's final deductions; they are distinct from factual failures.
The unchanged new V3 already has zero initial/final pace deduction and no Repair round;
this acceptance does not demonstrate a new Repair improvement or a formal quality ranking.

This evaluator task used **102 Google**, **three model calls** (initial truncated identity,
corrected identity and opening), **zero automatic retries**, and **USD 2.352335775**
reference cost. Combined saved executions since source-protected V3 generation,
including the two prior stopped evaluator packages, total **USD 6.634772835**.
Actual account billing remains unavailable. Evidence identifiers are the package's
`evaluator/run`, `evaluator/run-output8k`, `opening/execution` and
`final-acceptance/acceptance.json`, `quality-cli-report.json`, `factual-failures.json`,
`unknowns.json`, `soft-pace-deductions.json` and closed receipts. They are local artifacts,
not published assets. Documentation publication, further official evidence acquisition
and formal comparisons remain separate scopes.

### Authorized Git delivery and operational-documentation correction

The human subsequently requested delivery of the accepted work. The published
[delivery PR #103](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/103) targets
`main` at `5dee3b97df79d0267a8c6d0bb2205d68106a2bdf`; its initial reviewed head is
`18233eaa3cf2f39e7392100dfaccbf4813f8751b`. The complete three-dot scope contains
53 commits and 117 changed files, including the previously accepted #85-#94 work.
Those ten Issues were already closed. The separate open unified-CLI/material-handoff
Issues #95-#102 are excluded; native evaluator acceptance does not implement that
additional task interface. No raw runtime artifacts or unrelated `.gitignore` change
is published.

Delivery reuses the final 3,231-pass/10-skip backend gate because production code
is unchanged. Lint across all 97 changed Python files found one 101-character test
assertion; test-only commit `18233ea` wraps it without semantic change. Its actual
opening CLI gate passes seven tests in 49.29 seconds, formatting passes and all
97 files pass lint. No mypy/pyright project configuration or GitHub Actions workflow
exists; no new frontend validation, live request or paid execution occurred.

Full PR Spec review reports zero findings. Initial Standards review finds one P2
operational-documentation inconsistency: the evaluation README calls identity policy
3 current and says grounding FAIL prevents coordinates, contrary to current policy 4
and verified physical association. The correction updates both current-policy references
and explains that verified association permits independent route facts while original
grounding FAIL remains visible; unresolved association still blocks acquisition.
Historical policy-3 material retains explicit legacy replay. This is a documentation
correction, with no change to scoring, eligibility or retained reports.

The PR owns the final head, correction recheck, published pre-merge review and merge
state. Related Issues receive pinned published acceptance links, preserving their
earlier local-only descriptions as historical checkpoints. Further evidence acquisition,
formal research and version freezes remain outside this delivery.

<a id="installed-rtpeval-validation-acceptance-2026-10-09"></a>

## Installed RTPEval validation acceptance (#96, 2026-10-09)

The human authorized implementation of
[#96](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/96), including TDD,
offline checks, local commits, Standards/Spec review, corrections and documentation.
One initial branch creation/switch was explicitly confirmed; the branch was subsequently
renamed at the human's request to `rtpeval/cli-96`. Fixed review base is
`70e367de0e970225488b0cbeb4b8e2b6842c727f`. Implementation commit is `e418d94`;
the separate review correction is `b8291fe`. The unrelated pre-existing `.gitignore`
change is excluded and its SHA256 remains
`fdc63780f304bde2f8ac48b7e520330bc45254e8799cb4323cfe645c82a3ae02`.
No paid execution, push, PR, tracker publication, formal comparison or version freeze
is authorized or performed by this task.

### Implementation and test sequence

The repository now uses the bundled compatible `uv_build` backend for editable
installation and exposes the `rtpeval` console script. The lockfile changes only this
project's source from virtual to editable; dependency versions are unchanged.
The lazy dispatcher lives in `backend/cli/`, outside the evaluator's preparation-bound
Python file set. It delegates validation to the existing native command without
duplicating intake, scoring or acquisition logic. No evaluator/planner Python file,
schema or V0-V3 behavior changes.

The first installed-entry test failed because the command did not exist. After adding
packaging and the top-level entry, native accepted-inventory parity failed because the
initial dispatcher emitted no report. Delegating to the native intake command made
both public-interface slices pass. Expanded characterization initially used the wrong
diagnostic key (`diagnostics` instead of `material_diagnostics`) and an incorrect
expectation for argparse's missing-command priority; correcting these test expectations
preserved the native behavior. The resulting initial CLI gate passed 15 tests.

Default sandbox cache writes and a new empty offline cache could not complete setup.
Using the existing uv cache outside the restricted sandbox resolved and installed
the local editable project offline. Windows' installed uv trampoline could not resolve
its script path inside the sandbox; the normal host invocation succeeded. Default
pytest temporary-directory ACLs also blocked setup. Tests use fresh destinations under
the ignored workspace `artifacts/rtpeval-96/` directory instead. These were environment
failures, not provider sends or changes to production behavior. Editable metadata,
offline lock checking and actual `uv run --offline --locked --no-sync rtpeval` help
commands were verified.

The affected gate passed **188 tests, 1 skipped in 177.51 seconds**, covering installed
CLI behavior, native intake, legacy subprocess workflows and native evaluation
preparation/execution/replay with synthetic transport. The new tests compare exact
accepted/correction stdout and exit codes and preserve source bytes. Guarded child
processes reject and record DNS/socket operations, credential-file/environment reads
and online-runtime imports. Top-level help additionally forbids evaluator imports.
Five deliberate negative controls verify that caught DNS/TCP, credential or runtime
attempts still fail the harness; none sends a request or reads a credential value.

### Review correction

Independent Standards review of `70e367d...e418d94` found zero issues. Spec review
found one P2: the native leaf help and argument errors advertised
`rtpeval [-h] manifest`, omitting the required `validate` subcommand. A new public
help assertion reproduced that failure. Correction `b8291fe` temporarily supplies
`rtpeval validate` as the native parser's program name and restores it in `finally`,
including help/error exits. It does not edit the native parser or prepared hashes.
The final CLI gate passes **20 tests in 12.66 seconds**, including corrected help/error
usage, unchanged native JSON and old-module behavior. Ruff lint and format checks pass.
Both independent correction rechecks report **zero remaining Standards and Spec
findings**; the operation documents were also checked against this bounded slice.

The full backend gate passed **3,251 tests, 10 skipped in 538.75 seconds**. Collection
started at implementation `e418d94`, before the help-only correction; installed-command
subprocesses ran against the editable source. The separate final 20-test gate verifies
the strengthened help/error assertions at `b8291fe`. The correction changes only
displayed usage and leaves the rest of the full gate's behavior unchanged. No second
full run was needed. Compile checks, lock validation and whitespace checks pass;
the project has no configured mypy/pyright gate.

The operational guide now states editable installation, current commands, offline
behavior, JSON output and exit meanings. Only `validate` is exposed through the new
interface. Intake acceptance is not quality PASS or formal benchmark qualification.
Standalone distribution is untested and not required. No frontend gate or real
Planner/provider/model execution was run. Local evidence identifiers are
`artifacts/rtpeval-96/affected-r1`, `help-red`, `help-green.xml` and `full-r1.xml`;
they are ignored test artifacts, not published dependencies. Remote #96 remains open
because tracker publication is excluded. Subsequent #97-#102 implementation needs
its own approved scope.

<a id="one-step-rtpeval-evaluation-acceptance-2026-10-09"></a>

## One-step RTPEval evaluation acceptance (#97, 2026-10-09)

The human authorized advancement of
[#97](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/97) after local #96
acceptance, with implementation, TDD, local commits, Standards/Spec review, corrections
and related documentation. Fixed review base is
`05bda8658c5ab5980d3ac64ba4849d5451e4c290`; implementation commit is `4044dab`.
Work remains on `rtpeval/cli-96`, without another branch switch. The pre-existing
`.gitignore` change is excluded and retains its SHA256 recorded in the preceding #96
event. No paid/live run, push, PR, tracker write, formal comparison or version freeze
is performed. Remote #97 remains open; this record is local engineering acceptance.

### Implementation and test sequence

`backend/cli/evaluate.py` adds the installed evaluate group. Manifest execution accepts
explicit options, prices, optional reviewed contexts and a fresh directory. It invokes
native preparation, transfers the integrity digest internally and invokes native execution;
stdout contains the native report without a separate quality command. Offline prepare and
replay and the exact-digest prepared-directory execution route remain available. Mode
selectors are mutually exclusive; legacy execution rejects preparation options.

No native evaluator/planner Python file, dependency version or scoring rule changes.
The adapter stays outside the native preparation-bound file set, preserving implementation
and source hashes, version-specific identity/reasoning policies, usage and failure receipts.
The internal digest does not establish independent authorization. A started package remains
consumed on failure; no retry, resume, recovery, extra probe or opening supplement is added.

The first evaluate-help tracer failed with an invalid top-level command choice. Adding the
lazy group made it pass alongside the existing validation tests. The next one-step tracer
failed because the root public entry did not accept the native injected HTTP client. Passing
that existing test seam through the dispatcher and composing preparation/execution produced
the automatic native report and exact replay. An empty-directory regression then exposed
truthiness-based mode selection; the adapter now rejects an empty selector before loading
the evaluator. Offline guard setup initially rejected legitimate transitive configuration
type imports through the tokenizer. The harness now distinguishes module import from
initialization and directly blocks HTTP clients, runtime settings and dotenv loading, while
retaining credential-file/environment and DNS/socket guards. These were test-harness errors,
not credential reads or provider sends by the command.

The expanded public tests exercise one-step and legacy execution with native fixtures and
MockTransport: complete acquisition, partial Google acquisition, model connection failure,
cost reservation refusal and total deadline stops. Native reports, hashes and receipts are
preserved; comparisons do not replace meaningful hash/status/receipt differences. Both
routes replay through guarded installed and legacy commands with exactly equal reports and
exit codes. Tests also cover all reviewed-context flags, missing tokenizer, malformed local
material, incomplete versions, explicit credential-file ordering, missing credentials,
source drift before/during/after execution, preparation/report tampering and consumed-directory
refusal. Reviewed density reaches native scoring. Successful processing retains observed
FAIL, UNKNOWN, unresolved evidence and unavailable totals. The six-send representative case
has five Google requests and one V0 model request with explicit medium reasoning, zero retries
and no supplemental opening assessment.

The affected gate passes **1,327 tests, 1 skipped in 658.34 seconds**, covering the installed
validation/evaluation entry and the native evaluation suite, including 42 new evaluation CLI
tests. Earlier one-step/outcome slices passed 2 and then 34 tests; the affected gate includes
the final expanded assertions. Three
negative controls demonstrate that caught HTTP-client, runtime-settings and dotenv initialization
attempts still fail the offline harness. Synthetic tokenization validates structure and limits,
not real payload sizes. Ruff lint/format, compile and whitespace checks pass; the project has
no configured mypy/pyright gate. Actual `uv run --offline --locked --no-sync rtpeval evaluate`
group and execute help were verified on the installed console entry.

### Final gates and review

The full backend gate passes **3,293 tests, 10 skipped in 820.87 seconds**. It collected
the final 42 evaluation CLI tests and final implementation/test source, committed unchanged
as `4044dab` while the gate ran. No implementation change followed collection or review;
final documentation remains a separate group. Standards and Spec implementation reviews
against `05bda865...4044dab` each report zero findings, so no implementation correction
commit is needed. Documentation Standards review found one low-priority omission: the
development guide abbreviated the execute example without the runnable `uv run rtpeval`
prefix. The final documentation group supplies the complete command. Documentation Spec
review found zero issues. Both final document rechecks report zero remaining findings,
verifying completed gate numbers, the command correction, current state and remaining
authorization boundaries.
Local evidence identifiers are `artifacts/rtpeval-97/affected.xml`, `full.xml`, `offline-red`,
`offline-green2` and `outcomes`; these are ignored diagnostic artifacts, not published
dependencies. Documentation records runnable modes, reviewed contexts, credentials,
native budgets and separate status/exit meanings. No frontend or standalone distribution
validation is claimed. Material collection/finalization, generation registration, remaining
command groups and integrated acceptance (#98-#102) remain separate pending scopes.

### Delivery authorization and evidence reuse (2026-10-09)

After implementation acceptance, the human authorized delivery of #96 and #97 together:
rename the current branch to `rtpeval/xxx-96-97`, push, create a PR, merge after successful
verification, check evidence-backed Acceptance criteria and close fully resolved Issues.
The branch rename is complete; no branch switch or history rewrite occurred. The original
`.gitignore` change remains excluded with its recorded SHA256 unchanged. This delivery
authorization supersedes the earlier publication exclusion for these two tickets only.

The human explicitly requested no repeated PR code-review. Delivery reuses #96's corrected
Standards/Spec acceptance and #97's zero-finding implementation and final documentation
reviews. Source head before this documentation update is `88ab39e`; remote `main` is
`e757a3a457469818f395088e103d2f2a0e3764c6`. The latter's complete tree equals original
review base `70e367de0e970225488b0cbeb4b8e2b6842c727f`, so the combined published diff
contains only the two approved CLI slices and their documentation. Existing five task
commits are preserved, including #96's separate help correction. No implementation or
dependency changes invalidate the final 3,293-pass backend checkpoint.

All seven #96 and nine #97 Acceptance criteria are supported by the public-interface
tests and acceptance events above. Delivery checks the actual PR base/head/diff, remote
check status and published review conclusion before merging. Checkbox updates preserve
the original Issue wording; final merge and closure outcomes are recorded on the delivery
PR and Issues, which remain the lifecycle authority. No new live/paid run, formal benchmark,
version freeze or implementation of #98-#102 is authorized by this delivery.


## Unified RTPEval material workflow acceptance (2026-10-09)

### Scope and revisions

Status: implemented and validated at child/public synthetic seams and the final full
backend gate, with zero findings on both independent review axes. The human approved #98–#102
implementation, tests, local commits, review/corrections, coherent documentation and
full Git delivery under parent #95. [PR #105](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/105)
owns publication and merge; GitHub Issues own acceptance checkboxes and closure. Paid/live
execution, actual external RequirementSpec sessions, formal research and freezes are
excluded. V0–V3 retain independent runners and native behavior.

The combined review fixed base is `93ab3ba24049dd5321fea1c755e354f054c0625e`.
Collection `ef51e39`, tool adapters `52dddb2`, reviewed finalization `57ce384` and
selected registration `2aadf2d` retain their original implementation commits, integration
history and separate corrections. #102 starts at integrated `4919591`; public acceptance
tests are committed as `c268859`, followed by coherent operational documentation in
`c1280a1`. That documentation was the only task-local uncommitted context at the earlier
child-summary checkpoint. Final review and complete tests cover committed `c1280a1`;
the final acceptance update changes only this record and `PROJECT.md`. The unrelated primary `.gitignore`
change remains excluded, with SHA256
`FDC63780F304BDE2F8AC48B7E520330BC45254E8799CB4323CFE645C82A3AE02` unchanged.
No evaluator hash-bound implementation or original version runner changes in #102.

### Substantive failure, correction and retest sequence

Collection's first public tracer failed because `batch` was unknown. Subsequent red
slices exposed missing selection/hash/path associations, completion qualification,
recursive bound evidence copying and staging reconstruction. The implementation now
retains explicit missing/blocked attempts and checks original and copied sources.
The final child collection/intake gate passed **187 tests, 1 skipped in 38.68s**;
its post-integration focused collector gate passed **36 in 17.90s**.

Finalization initially lacked the public attachment operation. Later red slices showed
that exact configuration equality discarded actual additional options, author and
reviewer outputs incorrectly shared a final hash, and generic transcripts could be
reused after envelope edits. The corrected flow preserves an authored pending draft,
reviewer input and final reviewed output with exact execution/transcript bindings.
A separate `74a8d23` correction retains transcript subdirectory layout while interpreting
its embedded snapshot refs against the verified execution artifact. Stable child
finalization/core CLI validation passed **71 tests in 88.32s**. Synthetic transcripts
prove recorded lineage behavior; they do not authenticate a real external session or
semantic review quality.

Selected generation's red slices exposed missing public delegation/registration,
invalid V3 final-primary linkage, rebased selection refs and policy ambiguity. Actual
returned Planner observations now qualify required workflow completion under fixed
`selected_workflow_1`, while the operator's policy remains unchanged. Source selection
snapshots stay at their original root; native captured input/configuration refs are
explicit. Normal V3 partial/rejected/skipped outcomes can qualify; interrupted execution,
failed required retrieval and failed new usage capture remain blocked. A separate
`4919591` correction reports malformed selection maps as registration failure without
losing successful Planner status. The broader merged child gate passed **167 tests in
99.97s** before that localized correction; its final generation gate passed **33 in
15.46s**. These are distinct source checkpoints, not one combined final result.

Tool-adapter parity tests initially used incorrect native wire names and an unfixed
quality-report clock. Corrections use native output names and a fixed generated time,
without normalizing source/status/hash differences. The explicit tools-offline guard
preserves SDK class types while rejecting runtime construction and credential access;
it permits only Windows asyncio's local socketpair connection. External DNS/socket
attempts remain recorded even when caught, and strict default guard behavior is retained.
The post-integration tool/core/collector gate passed **111 tests in 124.34s**; prior
representative new/legacy parity, group/leaf help and explicit mocked incremental opening
acceptance remain evidence for those unchanged paths.

#102's documentation tracer first failed because the root guide omitted generation and
material handoff. Appending `--help` to a registration execution example then hit the
intentional registration/help boundary; the checker now reads leaf help and verifies
actual documented options. The integrated tracer initially asserted a run ID in the
native inventory, which exposes projected material rather than that field; it now reads
selected IDs from the accepted manifest and verifies the native four-version inventory.
These were acceptance-harness corrections, not production defects. The corrected public
suite passed **3 tests in 26.12s**. The integrated/native intake/evaluation-run/planner-usage
gate then passed **176 tests, 1 skipped in 60.17s**. Adding direct exact-byte assertions for
author draft, reviewed final, execution and transcript files was followed by the final
public suite: **3 passed in 25.64s** on the source committed as `c268859`.

### Public integration observations and documentation

Installed public commands collect explicit existing sources into `pending_review`, attach
synthetic external reviewed material, finalize through native intake and validate the
accepted four-version manifest. MockTransport one-step evaluation emits the native report,
with **five Google sends, one V0 model send and zero retries**. No implicit supplemental
opening request occurs. Processing and acquisition complete while evidence remains
unresolved, FAIL/UNKNOWN and unavailable totals remain visible, and explicit unavailable
producer usage stays unavailable. Preparation/report/receipt digests agree. Guarded offline
installed replay returns the complete saved report and preserves all execution files.
Original source/config/handoff bytes and copied author/draft/review/transcript lineage are
unchanged. The selected V3 injected generation case preserves normal partial Repair,
qualifies its required workflow, registers without RequirementSpec, and re-collects the
exact capture through the installed public command while missing versions remain visible.

The root README now gives a concise command/network/output table, shortest accepted
manifest execute/replay route, selected generation and existing-material handoff examples.
Detailed operational schemas and parameters remain in `backend/evaluation/README.md`;
durable producer/review lineage rules belong to the current intake contract. Development
smoke and historical module commands retain their owners, anchors and original meaning.
No CLI dispatch of external author/reviewer is implied. Completion, quality/PASS, staging,
registration, invocation, unavailable usage and processing exit codes remain distinct.

Ruff lint/format and whitespace checks pass for the new test. Documentation verification
checked six current owners, **15 new local links**, **eight parseable JSON templates**,
and preservation of every baseline heading/explicit anchor; public help checks cover the
actual root/material workflow flags. Local historical evidence identifiers are
`artifacts/rtpeval-95/102-native-gate.xml`, `102-stable-public.xml` and `doccheck-102.py`.
They are ignored diagnostics, not published dependencies. Exhaustive child red/green
commands and durations remain local handoff aids; the event summary above is the public
engineering account. No full backend or frontend gate was run by #102.

### Combined review and final backend acceptance

The merger retained every implementation, child integration and separate correction
commit. Primary integration checks passed **98 in 105.74s** for collection/core/evaluation,
**133 in 183.49s** for tools/collection/evaluation, **87 in 71.13s** for collection/finalization,
**81 in 28.19s** for generation/native usage/evidence/core CLI, and **3 in 24.38s** for the
final public workflow. These overlapping scopes are not added together. Initial primary
collection setup needed an existing basetemp parent; Windows sandbox `uv` console-launcher
canonicalization failures were resolved by host execution, without source changes.

Two independent read-only agents reviewed the complete 19-file fixed-base diff and all
eleven outgoing commits from `93ab3ba24049dd5321fea1c755e354f054c0625e` through
`c1280a1d3bde034809d2cb813975c5a571d2354d`. **Standards: zero findings. Spec: zero findings.**
No review correction was required. The combined conclusion is reused for PR delivery;
no second PR-wide code review is performed. All thirteen changed Python files passed
Ruff lint and format checks; fixed-base whitespace checks passed. Mypy and pyright are
not configured. No frontend gate is claimed because the frontend and application API
are unchanged. The final documentation check also verifies each new local link with
the Git index: sixteen tracked destinations, eight JSON templates and retained anchors.

The first complete backend invocation incorrectly used `D:/Workspace/Capstone` as its
working directory. It finished **52 failed, 3418 passed, 11 skipped, 2 warnings in 662.22s**.
JUnit and tracebacks identify 46 missing relative `config/runtime.yaml` paths, four
relative version-runner paths, one relative PowerShell script and one `Path.cwd()`-relative
implementation inventory. The wrong-script output also caused two GBK reader warnings.
This invocation error is retained as a failed gate, not reported as a source defect or
as successful validation. The additional skip was an absent parent-relative historical
artifact; its existing offline test runs from the proper repository root.

Without changing source, tests or dependencies, the corrected complete command ran from
`D:/Workspace/Capstone/Reliable-Trip-Plan-Agent` using the primary editable environment:

```powershell
.venv/Scripts/python.exe -m pytest backend/tests -q -p no:cacheprovider --basetemp D:/Workspace/Capstone/artifacts/rtpeval-95/final-root --junitxml D:/Workspace/Capstone/artifacts/rtpeval-95/final-root.xml
```

Final result on unchanged `c1280a1`: **3471 passed, 10 skipped in 673.89s**, with no failures
or warnings reported. The skips are nine opt-in isolated PostgreSQL cases and the existing
host symlink-creation privilege case. Local JUnit identifiers are
`D:/Workspace/Capstone/artifacts/rtpeval-95/final-95.xml` and `final-root.xml`; they are
ignored diagnostic evidence, not published navigation dependencies. The complete rerun
was required to replace the invalid-cwd gate. Earlier #97 full-suite evidence keeps its
original scope and is not substituted for this final result.

Only final acceptance documentation follows this tested code state. Git delivery uses
the existing PR, publishes the combined review/check conclusion, and checks existing
child Acceptance criteria against these results before closure. No actual external
author/reviewer session, paid/live provider request, formal benchmark or version freeze
is established by this synthetic/offline acceptance.
