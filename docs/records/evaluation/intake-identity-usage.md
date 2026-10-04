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
| V3 draft | 95 | 95 | 2, 2, 1, 2 | 5 |
| V3 final-primary | 100 | 100 | 2, 2, 2, 2 | 0 |

The paired adjusted delta remains exactly 5 percentage points (1/20). Final V1-V3
auxiliary scores remain 100. All dimension populations/counts, daily density counts
and deductions, schedule measures and occupancy are unchanged. Substantive primary
metrics also compare equal after excluding only derived `observation_id`/`evidence_hash`
fields; identity resolution, adopted venue and reason records have zero differences.
Policy versions, source/preparation/snapshot hashes and observation references changed,
so report bytes differ from old reports; this is not new independent factual evidence.

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
