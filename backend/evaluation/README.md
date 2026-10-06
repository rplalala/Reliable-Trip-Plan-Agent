# Independent evaluation package

Tickets 01-12 have offline implementations for explicitly submitted immutable material.
Ordinary scoring and Ticket 12 reporting consume saved outputs; the isolated
Ticket 11 command executes only frozen V3 post-primary cases. No formal corpus or
comparative research is constructed by these commands.
[Evaluation architecture](../../docs/0006-independent-evaluation.md) owns scope.
Ticket 11's [controlled replay contract](../../docs/contracts/0001-evaluation-artifacts.md#controlled-repair)
defines execution inputs, independent conditions and human supplementation.
Ticket 12's [contract](../../docs/contracts/0001-evaluation-artifacts.md#mechanism-official-audit)
defines separate mechanism/audit readers and explicit opt-in capture, disabled by default.
The [approved scope](../../docs/contracts/0001-evaluation-artifacts.md#ticket12-implementation-scope)
defines the local wrapper, reader/audit CLI and offline acceptance boundaries.

## Contract and module navigation

Current rules have one topic owner. Read the relevant contract before preparing inputs;
acceptance records and Issue comments preserve historical decisions, not alternate rules.

| Responsibility | Current contract | Implementation |
| --- | --- | --- |
| Batch/artifact wire and deferred tracks | [Artifacts](../../docs/contracts/0001-evaluation-artifacts.md) | [intake](intake.py), [records](records.py), [projection](projection.py) |
| Structural claims and occurrence association | [Intake/claims](../../docs/contracts/0002-intake-identity-usage.md#claims) | [preparation](preparation.py), [claims](_claims.py) |
| Independent identity judgment | [Identity](../../docs/contracts/0002-intake-identity-usage.md#identity) | [Version dispatch/API checks](identity_program.py), [target ownership](identity_targets.py), [V0 correspondence/historical LLM](identity_llm.py), [legacy replay](identity.py), [V0 material](identity_adoption.py) |
| Request planning and frozen replay | [Snapshots](../../docs/contracts/0002-intake-identity-usage.md#snapshots) | [snapshot](snapshot.py) |
| Opt-in usage and descriptive resources | [Usage](../../docs/contracts/0002-intake-identity-usage.md#usage) | [usage capture](../app/observability/usage_capture.py), [usage_report](usage_report.py) |
| Reviewed requirements, time and occupancy | [Requirement/schedule](../../docs/contracts/0003-requirement-schedule.md) | [requirement_schedule](requirement_schedule.py), [schedule_time](schedule_time.py), [occupancy](occupancy.py) |
| Opening and route compliance | [Opening/routes](../../docs/contracts/0004-opening-routes.md) | [opening](opening.py), [routes](routes.py), [route preparation](_route_preparation.py) |
| Final five-dimension auxiliary report | [Quality](../../docs/contracts/0005-quality-human-review.md#scores) | [quality_report](quality_report.py) |
| Anonymous packages, revisions and human reports | [Human](../../docs/contracts/0005-quality-human-review.md#human) | [human_tasks](human_tasks.py), [human_answers](human_answers.py), [human_report](human_report.py) |
| Frozen V3 execution and controlled outcomes | [Controlled Repair](../../docs/contracts/0001-evaluation-artifacts.md#controlled-repair) | [controlled CLI](controlled_cli.py), [replay](controlled_replay.py), [report](controlled_report.py) |

Development verification utilities live in `tools/` within this package. The V0
[route request tool](tools/route_requests.py) and its
[CLI](tools/route_requests_cli.py) prepare smoke inventories and budgets; neither
Product planning nor the final quality scorer calls them. Smoke is a development
activity, not a product runtime stage. Core identity, snapshot and scoring modules
and their CLIs remain at the package root. A CLI is not necessarily a smoke utility.

## Offline workflow and CLI

Run from the repository root with the existing Python environment. Names below represent
researcher-prepared files; commands do not generate missing independent evidence. For each
CLI, `--help` gives executable arguments. Default reports go to stdout; save them outside
source artifacts. Human output paths must be new. No command below acquires live evidence.

### Start with the synthetic usage packet

For a small development demonstration without authoring envelopes, run the subprocess
acceptance tests. They reuse existing synthetic fixtures and exercise the actual module
commands; they do not generate real trips. With the existing Python/npm environments,
run this in PowerShell 7 from the repository root:

```powershell
npm --prefix frontend run build:blind-review
New-Item -ItemType Directory -Path artifacts/evaluation-usage -Force | Out-Null
$env:EVALUATION_USAGE_RENDERER_DIR = (Resolve-Path frontend/dist-blind-review).Path
.venv/Scripts/python.exe -m pytest backend/tests/evaluation/test_usage_workflow.py -q --basetemp artifacts/evaluation-usage/demo-01 -o cache_dir=artifacts/evaluation-usage/cache
Remove-Item Env:EVALUATION_USAGE_RENDERER_DIR
```

Use a fresh `--basetemp` name each time: pytest clears that directory before use.
Generated inputs, snapshots, package and reports remain under that ignored directory.
Each test folder's `cli-output/` retains numbered `*-command.json` (argv/exit code),
`*-stdout.json` and `*-stderr.txt`. Command records contain local absolute paths;
replay them only while that packet remains in its original location. Tests verify that
pre-existing source bytes survive each CLI unchanged. External connections are guarded;
loopback remains available for the event loop's internal socket pair. Regression runs
use synthetic tokenization, as the parent suite does, and do not measure payload size.
Without `EVALUATION_USAGE_RENDERER_DIR`, the package test uses a minimal renderer fixture
so ordinary Python regression tests need no npm build. Set it as above for the real renderer.

| Example | What to inspect | Expected interpretation |
| --- | --- | --- |
| Four-version quality/resources | Quality `groups[].versions`; resource `metrics` | All V0-V3 retained; the synthetic V1 score is 50 with two opening UNKNOWNs; missing tokens stay null |
| V3 overlap retime | Pair `continuity`, `correspondence`, `deltas`, `visit_changes` | Confirmed overlap resolved using adopted lineage, zero removed visits; grounding delta is exactly 0/1; unresolved total delta stays null |
| Four controlled cases | `targets[].independent_outcome` or `control.outcome` | `resolved`, `valid_no_change`, `lawful_change`, `regressed`, respectively |
| Mechanism/audit | Mechanism `runs`; audit queue `units` and report `counts` | Complete simulated captures give three run-bound claim units, two occurrences each; missing captures leave the population count null |
| Anonymous package | `public/review.html`, private mapping, import/report stdout | Four labels A-D, one imported answer revision and one descriptive task; answers are synthetic |
| Invalid input | Intake `material_diagnostics`, command exit code | Missing file and changed-source hash mismatch exit 2 with the affected path |

The exclusive-addition example deliberately includes an independently reviewed quotation,
“Exactly one primary visit on this day.” Its planner interpretation misses that restriction.
V3's internal `ACCEPTED_COMPLETE` therefore coexists with the independent `regressed` verdict.
Without that restriction, the same independently feasible addition is `lawful_change`.
The audit verdicts and ranking answers only demonstrate file linkage and report processing;
they are not real human assessments or evidence that any venue fact is true.
Existing native browser acceptance remains separate from package generation/import checks.

For researcher-supplied material, follow the commands below and the relevant contract;
the demo does not collect missing independent evidence. Four-final scoring requires a
final-only snapshot, whereas V3 paired reporting requires a paired snapshot. Do not reuse
one snapshot across those scopes. Exit 0 means processing completed, including FAIL,
UNKNOWN or unavailable totals; inspect the report rather than treating it as an itinerary PASS.

Save stdout JSON as UTF-8 without BOM. In PowerShell 7, set
`$env:PYTHONIOENCODING = 'utf-8'` and pipe a stdout-only command to
`Set-Content -Encoding utf8NoBOM`; native CLI output options already write UTF-8.
Windows PowerShell 5.1 `>` uses UTF-16, so it cannot be used for these JSON artifacts.
The [dated usage record](../../docs/records/evaluation/2026-10-04-evaluation-usage.md)
retains the observed validation sequence and limits.

<a id="entry-points"></a>
<a id="manifest-and-envelope-vocabulary"></a>
<a id="independent-review-replay"></a>
<a id="identity-replay-ticket-03"></a>
<a id="validation"></a>
<a id="ticket-04-independent-snapshots"></a>
<a id="independent-preparation-formats"></a>

### Intake and identity

```powershell
.venv/Scripts/python.exe -m backend.evaluation manifest.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli identity-plan manifest.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli replay identity-snapshot --expected-plan identity-plan.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli identity-evidence identity-snapshot
.venv/Scripts/python.exe -m backend.evaluation.identity_cli manifest.json identity-evidence.json
.venv/Scripts/python.exe -m backend.evaluation.identity_cli manifest.json identity-evidence.json --prepare --model YOUR_JUDGMENT_MODEL
.venv/Scripts/python.exe -m backend.evaluation.identity_cli manifest.json identity-evidence.json --model-result identity-model-result.json
```

An acquisition caller separately uses `build_identity_plan`, injected async
`acquire_snapshot`, immutable `load_snapshot`, then `identity_evidence`.
There is no built-in live Google client or acquisition CLI. The caller owns credentials,
authorization and explicit send ceilings. Identity uses the
[version-specific policy](../../docs/contracts/0002-intake-identity-usage.md#version-specific-identity-requirement).
V1-V3 final/optional visits and their requirement targets use program rules over independent
API facts, with literal name/address equality and no model fallback. No model result is needed
for those references. No human confirmation or sampling is mandatory. `--prepare` prints a
V0-only frozen packet covering generated visits and user-requested requirement targets;
it does not execute a model. Target judgments belong to their own version, while
independent acquisition evidence can be shared. Import a
separately authorized saved response through the contract's model-result envelope. The
command has no built-in model execution client. Missing V0 results remain UNKNOWN;
API-backed references continue independently. V0 semantic judgments remain fallible. Intake exits 0 for
accepted material or 2 for correction. Identity exits 0 for packet preparation/completed
judgments (including confirmed failures), 3 for UNKNOWN/missing judgment, and 2 for
material/linkage errors. Incorrect submitted addresses and different venues are grounding
FAIL, even when the intended venue is recognizable. Their canonical ID stays null: candidate
facts cannot supply corrected route endpoints. Original outputs and denominators are retained.
Current reports use `versioned_api_identity_2`; V0 packets use
`v0_identity_correspondence_3`: citation paths are schema enums
shared with import. Address-presence schema alternatives bind short reference IDs;
every absent/null/blank address requires `not_supplied` and forbids `claim.location` citations.
A supplied address forbids `not_supplied`, including UNKNOWN/no-match decisions.
`candidate_correspondence` retains the validated match separately from original-claim
`grounding_verdict`; recognizing a candidate does not repair an erroneous occurrence.
Supported destination contradictions remain FAIL even without a supplied original address;
the response must cite original name/destination and independent candidate support.
Old policy-1 packets and rejected historical output cannot be normalized or relabeled for
current import. The frozen historical all-version schema remains explicitly replayable.

`--historical-program` explicitly replays the former `versioned_api_identity_1`
shared-target policy and `v0_identity_correspondence_2` packet. Its material cannot
pass current import. `--historical-llm` remains the older all-version replay.

For V0 correspondence within a verified material bundle:

```powershell
.venv/Scripts/python.exe -m backend.evaluation.identity_adoption_cli v0-identity-material.json --prepare --model YOUR_JUDGMENT_MODEL
.venv/Scripts/python.exe -m backend.evaluation.identity_adoption_cli v0-identity-material.json --model-result identity-model-result.json
```

The historical proposal response lacks the new address assessments and is not silently
converted. For exact historical replay use `--legacy` with the original audit/review inputs:

```powershell
.venv/Scripts/python.exe -m backend.evaluation.identity_cli manifest.json identity-evidence.json audit-plan.json --legacy --reviews identity-reviews.json
.venv/Scripts/python.exe -m backend.evaluation.identity_adoption_cli v0-identity-material.json --legacy
# Explicit replay of the superseded all-version LLM policy:
.venv/Scripts/python.exe -m backend.evaluation.identity_cli manifest.json identity-evidence.json --historical-llm --model-result historical-model-result.json
```

The [historical material contract](../../docs/contracts/0002-intake-identity-usage.md#v0-only-model-assisted-offline-adoption)
defines the V0 source bundle. Both policies retain the original files. Save stdout as UTF-8
without BOM. New consumers replay the complete source-bound model material; historical
consumers replay their frozen inputs. A copied or edited report cannot unlock preparation.
No planner version or production provider caller changes.

Offline regression coverage: `backend/tests/evaluation/test_identity_program.py` exercises
mixed-version resolver/CLI-to-quality and V3-pair flows with disabled model/network clients,
independent synthetic snapshots, strict field equality, FAIL/UNKNOWN preservation, unadopted
coordinates/endpoints and stale/forged/historical material rejection. Existing historical
policy tests explicitly select their replay path. Run these tests with the backend gates;
no paid acquisition or smoke execution is part of this validation.
`backend/tests/evaluation/test_identity_v0_contract.py` covers current schema alternatives,
supported/nonempty and rejected citations, complete owned decision coverage, exact provenance,
CLI import, preserved correspondence versus FAIL/UNKNOWN, quality fractions and null route
endpoints using synthetic local snapshots. SDK execution tests use MockTransport only.

### Prepared one-call identity development smoke

The [post-merge #82 refresh](../../docs/records/evaluation/intake-identity-usage.md#post-merge-v0-smoke-refresh-2026-10-06)
replaces the stale #77 execution proposal with a new offline manifest bound to the merged
implementation. Both historical material and failed attempts remain preserved. The fresh
directory was unconsumed at preparation; readiness and Issue publication grant no execution
authority. Its subsequently approved [one-call execution](../../docs/records/evaluation/intake-identity-usage.md#v0-identity-smoke-execution-2026-10-06)
imported eight V0 primary PASS while preserving a requirement-subject UNKNOWN. That
execution directory is now consumed; do not reuse it or infer route validation from identity.

The subsequent [#85 offline refresh](../../docs/records/evaluation/intake-identity-usage.md#v0-target-smoke-refresh-2026-10-06)
binds merged #83 source and all nine V0 visit/target references (fourteen candidate
appearances). Real cached-tokenizer sizing is 16,111 input tokens, or 17,135 with reserve,
exceeding the original 16,000 preparation ceiling. The guard rejected that preparation;
the preserved blocked draft is not an executable manifest and grants no live authority.
The user subsequently approved only the offline smoke-limit correction and re-preparation:
the tool now uses an 18,000 input ceiling / USD 0.0042 reference allowance. A compatible
new manifest required separate exact-plan live approval; historical approval was not reused.
Do not substitute the historical eight-visit request or trim candidate evidence to fit.

The subsequent [approved #85 execution](../../docs/records/evaluation/intake-identity-usage.md#v0-target-identity-smoke-execution-2026-10-06)
completed exactly one request with zero retries: eight visits and one V0-owned requirement
target are PASS, with zero FAIL/UNKNOWN. Offline import replay is exact; the target's
missing original address remains null with `not_supplied`. Original claims, V1-V3 records,
all protected evidence and implementation hashes are unchanged. The fresh execution
directory is now consumed. This identity-only result does not establish route feasibility,
score results or another request's authority.

`tools.validation.identity_judgment_smoke` is a separate development executor for a verified
V0 material bundle. Preparation is offline; execution requires explicit user approval of
the exact manifest digest and the [smoke execution handoff](../../docs/agents/smoke-tests.md).
Existing historical authorization is used only to verify source material. It grants no
new request authority. Preparation accepts `--endpoint` without loading credentials;
otherwise it reads existing V0 settings. Execution requires `AZURE_OPENAI_ENDPOINT`,
`AZURE_OPENAI_DEPLOYMENT` and `AZURE_OPENAI_API_KEY` through V0 settings; no credentials
are written to preparation. The request itself selects `gpt-6-luna`.

```powershell
.venv/Scripts/python.exe -m tools.validation.identity_judgment_smoke prepare --material v0-identity-material.json --directory artifacts/new-identity-smoke --endpoint https://YOUR_RESOURCE.openai.azure.com/openai/v1/
# Execute only after this exact preparation and its limits receive user approval:
.venv/Scripts/python.exe -m tools.validation.identity_judgment_smoke execute --preparation artifacts/new-identity-smoke/preparation.json --approved-manifest-sha256 APPROVED_DIGEST
```

Optional `--protected-hashes` reads a JSON `file_hashes` map to preserve additional original
files. The preparation binds verified source hashes, implementation hashes, the original
identity packet, exact wire request, endpoint, token/retail-reference limits and a single
execution directory. Schema `rtpeval_identity_smoke_preparation_2` recomputes V0 visit/target
references and candidate counts under the corrected output contract, excluding V1-V3
from the model request; V0 requirement targets are included. It writes `preparation.json`,
`pending-identity-report.json` and private `handoff.md`; append the reviewed source revision
and configuration prerequisites before any future dispatch. The pending report has no new
V0 model evidence. Implementation hashes cover evaluator modules, local reference/token
code and dependency declarations. Re-preparation over an existing directory is rejected. One approved
execution consumes its directory, even when it fails; reusing it cannot send again.
The SDK has zero retries, redirects are disabled, and the HTTP boundary checks the exact
POST/request and rechecks sources before its sole attempt. Changed source material after
the response prevents import. No planner or Google calls are included.

The fixed development limits are one request, low reasoning, no tools, `store=false`,
18,000 estimated input tokens including 1,024 reserve, 3,000 output tokens and a 60-second
HTTP deadline. The locally cached tokenizer is a surrogate preflight estimate. Excessive
reported usage stops import after receipt; these checks cannot guarantee the provider's
tokenizer or invoice ceiling. The fresh proposed live reference allowance is USD 0.0042; it
requires new exact-plan approval and does not inherit #73's consumed allowance. Official
OpenAI reference rates checked 2026-10-06 are USD 0.10 ordinary input, 0.01 cached input,
0.125 cache writes and 0.50 output per million tokens. At these caps the maximum standard
reference is USD 0.00375; a regional +10% scenario is USD 0.004125. Output already includes
reasoning. Receipts retain original usage, partition reported input categories, and label
missing categories as a conservative reference upper bound rather than observed zero.
Malformed or excessive category counts stop import. These standard/regional scenarios do
not establish a service tier, Azure SKU, taxes or a Foundry invoice ceiling. See the
[model price reference](https://developers.openai.com/api/docs/models/gpt-6-luna) and
[cache usage reference](https://developers.openai.com/api/docs/guides/prompt-caching).

`execution.json` records attempts, usage, reference cost, raw byte digest and terminal error
type without SDK exception text or headers. Received complete raw bytes stay in `response.bin`;
`model-result.json` is imported through the current source-bound policy. Only a valid complete
result produces `identity-report.json`. Execution exit 0 means valid processing, including
FAIL/UNKNOWN; exit 1 means a terminal execution/import error. Missing approval or changed
preparation raises before sending. Original claims stay intact; wrong addresses remain FAIL
with null canonical identity. No paid execution is implied by preparation or an offline test.

Fresh-clone tests use synthetic fixtures rather than requiring ignored live artifacts:

```powershell
New-Item -ItemType Directory -Path artifacts/evaluation-adoption -Force | Out-Null
.venv/Scripts/python.exe -m pytest backend/tests/evaluation/test_identity_llm.py backend/tests/evaluation/test_identity_adoption.py -q --basetemp artifacts/evaluation-adoption/test-01 -o cache_dir=artifacts/evaluation-adoption/cache
```

<a id="v0-route-requests"></a>

### Development-only V0 smoke route requests and budget

This tool is in `backend.evaluation.tools`, separate from ordinary evaluator scoring.
It consumes core evaluator preparations without becoming a required scoring step.
Use the new module path below; the former root-level tool modules are retired.
Historical records and frozen manifests retain the paths of their own revisions.

The [#86 offline refresh](../../docs/records/evaluation/routes.md#accepted-v0-identity-route-refresh-2026-10-07)
uses #85's accepted current report: all four original legs are identity-eligible and reuse
eight independent coordinates, requiring no Details. The dated KR profile retains three
blocked WALK requests and one conditional TRANSIT, zero ready Routes and four UNKNOWN
feasibility verdicts. Actual CLI replay returns 3 and matches the library; the request
package is complete preparation without live authority. No provider/price refresh or
acquisition occurred; hypothetical inventory estimates are not a paid allowance.

The later [free KR support and budget assessment](../../docs/records/evaluation/routes.md#kr-route-support-budget-2026-10-07)
identifies Kakao Map V2 WALK as a documentation candidate for three calls (30 KRW
published reference), with TMAP pedestrian as an alternative. This is an offline draft,
not a supported provider in these commands. Retention/use conditions, account costs and
an offline adapter remain unresolved. Kakao/ODsay general TRANSIT cannot establish the
original explicit departure; Google KR TRANSIT coverage remains unconfirmed. The saved
#86 package, zero-send preflight and all four UNKNOWN verdicts are preserved.

The [Sydney offline preparation](../../docs/records/evaluation/routes.md#sydney-offline-route-preparation-2026-10-07)
adds explicit `--region AU` / `region_code="AU"`. Australian WALK can become ready for
approval with complete independent identity/coordinates/window checks; it stays UNKNOWN
without route evidence. TRANSIT remains conditional and DRIVE is unsupported by this
acquisition path. The input must explicitly declare Australia. Default KR output/replay
is unchanged; region is never inferred or a live authorization. Unique requests determine
budgets, while repeated leg occurrences remain visible.

The new [Sydney source request](../../tools/validation/packets/sydney-v0-route-smoke/request.json)
is four days (October 14-17), two travelers and AUD 1600, with two primary visits per day
and required Sydney Opera House. It is a new generation input, not a generated output,
reviewed RequirementSpec or API snapshot. Its non-generation USD 0.3522 price scenario
includes unready routes and does not authorize their execution. The later bounded
generation-only smoke stopped after one requirements response because exact daily
cardinality is an unsupported hard semantic condition. It produced no itinerary or
evaluator bundle; the consumed plan cannot be reused. Original input and raw output
remain preserved, and actual billing is unknown. See the
[generation stop record](../../docs/records/v0-v3/development-pilots.md#sydney-v0-generation-smoke-2026-10-07).
The dated input needs trusted-day revalidation before later use.

Prepare from an exact current `versioned_api_identity_2` report without acquiring evidence:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
.venv/Scripts/python.exe -m backend.evaluation.tools.route_requests_cli v0-identity-material.json identity-report.json --context schedule-context.json --route-reviews route-reviews.json --prepared-at 2026-10-05T10:23:02Z | Set-Content -Encoding utf8NoBOM request-package.json
# Missing current report: derive a current pending report without any model result or send.
.venv/Scripts/python.exe -m backend.evaluation.tools.route_requests_cli v0-identity-material.json --context schedule-context.json --prepared-at 2026-10-05T10:23:02Z
# Historical identity reports require explicit replay; they never replace current evidence.
.venv/Scripts/python.exe -m backend.evaluation.tools.route_requests_cli v0-identity-material.json historical-identity.json --legacy --context schedule-context.json --prepared-at 2026-10-05T10:23:02Z
# Australian source material only; no Sydney V0 identity bundle has been acquired yet.
.venv/Scripts/python.exe -m backend.evaluation.tools.route_requests_cli sydney-identity-material.json identity-report.json --region AU --context schedule-context.json --prepared-at 2026-10-07T00:00:00Z
```

Schema `rtpeval_v0_route_requests_2` binds the selected identity policy and exact replay
inputs. Current reports require no human identity/audit gate; missing model evidence keeps
original legs visible with UNKNOWN endpoints. Rejected/stale reports or corrupt sources
return material diagnostics with no partial request inventory. A historical report supplied
without `--legacy` is rejected; historical saved packages are not rewritten or relabeled.
Each leg exposes original endpoint claims, candidate correspondence, grounding verdicts and
identity blockers separately from its route verdict. FAIL/UNKNOWN endpoints cannot acquire
canonical coordinates or substitute venues. Endpoint occurrence/unique-venue counts remain
distinct from deduplicated Details/Routes request counts.

Optional `--occupancy-reviews` retains reviewed occupancy; `--details-snapshot` consumes already supplied
independent Details with the package's exact `details_plan`. It sends nothing and never retries bad evidence.
Saved coordinates are reused only after source replay and ID/numeric validation. The current provider
preparation profile is KR, checked 2026-10-05. Original mode/timing/continuous windows and blocked legs stay visible.
WALK coverage and TRANSIT's unverified regional support can leave zero ready Routes.
Omit absent optional review flags; a supplied review file must contain its JSON object
envelope, not JSON null. Zero eligible venues is distinct from missing coordinates for
eligible venues. Zero ready requests is a complete preparation outcome; it cannot remove
actual identity blockers without separately accepted current evidence.

Exit 0 means complete preparation without pending applicable legs, 3 means a complete blocked/conditional
inventory, and 2 means invalid material. Save UTF-8 without BOM. Completion is not route feasibility or acquisition
approval. Masks, dated prices, source hashes, actual versus hypothetical budgets and stops are in the
[request contract](../../docs/contracts/0004-opening-routes.md#v0-route-request-package).

Library seams: `prepare_v0_route_requests` and `preflight_v0_route_requests` in [route_requests](tools/route_requests.py).
Preflight recomputes the frozen package before checking ledger/request limits and always returns
`live_authorized=false`. No provider or model client is present. Execution requires separate inventory/budget
approval and a current-session execution child configured `gpt-6.1-sol` / `medium`.

Fresh-clone fixtures are independently runnable:

```powershell
New-Item -ItemType Directory -Path artifacts/evaluation-route-requests -Force | Out-Null
.venv/Scripts/python.exe -m pytest backend/tests/evaluation/test_route_requests.py backend/tests/evaluation/test_route_requests_versioned.py -q --basetemp artifacts/evaluation-route-requests/test-01 -o cache_dir=artifacts/evaluation-route-requests/cache
```

<a id="offline-evaluation-preparation-and-metrics-tickets-01-06"></a>
<a id="ticket-05-offline-requirement-and-schedule-metrics"></a>
<a id="ticket-06-offline-opening-compliance"></a>
<a id="ticket-07-offline-same-day-routes"></a>
<a id="selection-and-scoring"></a>

### Independent schedule, opening and routes

```powershell
.venv/Scripts/python.exe -m backend.evaluation.requirement_schedule_cli manifest.json identity-report.json --context schedule-context.json --occupancy-reviews occupancy-reviews.json
.venv/Scripts/python.exe -m backend.evaluation.route_cli prepare manifest.json identity-report.json --context schedule-context.json --occupancy-reviews occupancy-reviews.json --route-reviews route-reviews.json --coordinates coordinates.json
.venv/Scripts/python.exe -m backend.evaluation.snapshot_cli evidence-plan manifest.json identity-report.json route-contexts.json
.venv/Scripts/python.exe -m backend.evaluation.opening_cli manifest.json identity-report.json evidence-snapshot --context schedule-context.json --expected-plan evidence-plan.json
.venv/Scripts/python.exe -m backend.evaluation.route_cli score manifest.json identity-report.json evidence-snapshot --context schedule-context.json --occupancy-reviews occupancy-reviews.json --route-reviews route-reviews.json --coordinates coordinates.json --expected-plan evidence-plan.json
```

Save prepared route contexts, build the evidence plan and acquire/replay its snapshot
through the separately authorized injected caller before scoring. Preparation does not
invent coordinates or transport restrictions. Missing optional context/review retains
UNKNOWN or applicability diagnostics. Route preparation exports `route_contexts` and its ready-made `evidence_plan`.

When the adopted identity report was resolved from an independent identity snapshot that
already contains coordinates, replace `--coordinates coordinates.json` with
`--identity-snapshot identity-snapshot` on route prepare/score or quality-report commands.
The library keyword is `identity_snapshot_directory`; direct inspection uses
`prepare_snapshot_coordinates` in [snapshot_coordinates](snapshot_coordinates.py).
Each replay verifies the snapshot and its exact identity linkage. Source-derived coordinate
records retain response hashes/pointers and retrieval times, without fabricated review fields.
Missing, invalid or conflicting coordinates stay diagnostic and do not trigger acquisition.
Select one coordinate source; the existing reviewed envelope and query options remain available.
The automatic path uses existing default query options and requires its own matching evidence
plan; previously prepared manual-coordinate query hashes are not interchangeable.
Use that plan directly, or put the context array under `{"contexts": [...]}` in
`route-contexts.json` for the snapshot planning CLI; the full preparation report is not
that CLI input. `--expected-plan` optionally enforces trusted full-plan equality.

Library seams: `score_requirement_schedule`, `prepare_routes`, `score_opening`, and
`score_routes`. These and identity/snapshot plan commands support `--paired` where
declared, selecting available V3 draft/final-primary projections; paired scope must
remain consistent across inputs. Ticket 10 combines these paired outputs below.
Scorers exit 0 for complete processing, including FAIL/UNKNOWN,
or 2 for material/replay correction. Snapshot commands exit 2 for invalid replay/input.

<a id="ticket-08-final-multimetric-report-and-auxiliary-scores"></a>

### Final report and resources

```powershell
.venv/Scripts/python.exe -m backend.evaluation.quality_report_cli manifest.json identity-report.json evidence-snapshot --context schedule-context.json --occupancy-reviews occupancy-reviews.json --route-reviews route-reviews.json --coordinates coordinates.json --expected-plan evidence-plan.json --generated-at 2026-10-03T00:00:00Z
.venv/Scripts/python.exe -m backend.evaluation.usage_report usage-v0.json usage-v1.json usage-v2.json usage-v3.json
```

`build_quality_report` combines the existing independent scorers and identity records.
It accepts final-only snapshots (`paired=False`); a paired snapshot reports
`unsupported_snapshot_scope`. It emits exact five-dimension scores/masks without resource,
human or mechanism penalties. Exit 0 means processing completed, not a passing itinerary
or available total; correction exits 2. `--generated-at` defaults to current UTC;
freeze it with the inputs for reproducible report content.

Current report schemas are `rtpeval_quality_report_2` and `rtpeval_v3_pair_report_2`.
Both use `rtpeval_daily_density_2` and the sole current
[approved table](../../docs/contracts/0005-quality-human-review.md#daily-density)
from [Issue #52](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/52).
Use `overall_total.score_0_100` for the density-adjusted score; `auxiliary_total`
remains the exact five-dimensional diagnostic. Both report commands accept
`--density-reviews density-reviews.json`. Review the complete original request once
per group, including dated count exceptions, and reuse that policy for final and paired
reports. A request containing nonempty `additional_preferences` needs this review to
establish density deductions; omitting it keeps the overall total unavailable.

Example preparation (replace all linkage and review fields with actual values):

```json
{
  "schema_version": "rtpeval_density_reviews_1",
  "batch_id": "submitted-batch",
  "batch_revision": "1",
  "groups": [{
    "group_id": "request-group",
    "input_sha256": "actual-input-file-sha256",
    "reviewer_ref": "independent-reviewer",
    "reviewed_at": "2026-10-04T00:00:00Z",
    "review_origin": "agent",
    "rationale": "Original request asks for relaxed pace without explicit daily counts.",
    "default": {
      "profile": "relaxed",
      "exact_count": null,
      "source_refs": [{
        "field_path": "additional_preferences",
        "quote": "Please keep the pace relaxed."
      }]
    },
    "days": []
  }]
}
```

The [density contract](../../docs/contracts/0005-quality-human-review.md#daily-density)
defines dated overrides, count exemptions/mismatches, penalty tables and UNKNOWN bounds.
Keep historical report files intact and write new replays to separate paths.

Usage envelopes come from opt-in [request-local capture](../app/observability/USAGE.md),
not automatic CLI/API collection. `compare_usage` keeps scopes/namespaces and missing
measurements explicit. Its CLI prints a descriptive report; invalid envelopes raise an
input error rather than partial comparisons. It adds no billing claim or quality penalty.

<a id="transport-responsibility-correction---2026-09-30"></a>
<a id="ticket-09-local-blinded-ranking-workflow"></a>

### Local blinded ranking

```powershell
npm --prefix frontend run build:blind-review
.venv/Scripts/python.exe -m backend.evaluation.human_cli prepare manifest.json selection.json --out preparation.json
.venv/Scripts/python.exe -m backend.evaluation.human_cli package manifest.json selection.json display-review.json --out public-review --private-out private-mapping.json --renderer-js frontend/dist-blind-review/review.js --renderer-css frontend/dist-blind-review/review.css
.venv/Scripts/python.exe -m backend.evaluation.human_cli import public-review/presentation.json private-mapping.json answers.json --out imported-revisions.json
.venv/Scripts/python.exe -m backend.evaluation.human_cli report public-review/presentation.json private-mapping.json answers.json --generated-at 2026-10-03T00:00:00Z --out human-report.json
```

Prepare and independently review display material before packaging. Deliver only
`review.html` and `presentation.json`; retain preparation, display review and private
mapping outside the public directory. Open `review.html` directly in a local browser.
The package needs no account, server, CDN or submission endpoint. Use synthetic material
for development; real assessment needs separate approval. Successful processing exits 0;
invalid material or output conflicts exit 2. Import/report can take multiple answer files.

The current renderer provides IANA zone selection and HH:mm clocks, labelled Inferred
arrival, drafts, submitted revision recovery, JSON download/import and confirmed Clear
answers. It hides Original timestamp controls and dedicated uncertainty/item/time-warning
hints; frozen material retains uncertainty. Clear only erases this package/rater's local
answer history. Download a backup first; researcher-held old revisions remain records.
The [human contract](../../docs/contracts/0005-quality-human-review.md#human) owns exact
answer, blinding and display semantics. Automated DOM checks do not prove native file://
storage behavior; the [acceptance record](../../docs/records/evaluation/blinded-ranking-record.md)
distinguishes automated checks from user-reported browser acceptance.

### V3 paired diagnostics

```powershell
$env:PYTHONIOENCODING = 'utf-8'
.venv/Scripts/python.exe -m backend.evaluation.v3_pair_cli prepare manifest.json identity-report.json | Set-Content -Encoding utf8NoBOM edit-provenance.json
.venv/Scripts/python.exe -m backend.evaluation.v3_pair_cli report manifest.json identity-report.json paired-evidence-snapshot --context schedule-context.json --route-reviews route-reviews.json --coordinates coordinates.json --expected-plan paired-evidence-plan.json --edit-provenance edit-provenance.json --generated-at 2026-10-03T00:00:00Z | Set-Content -Encoding utf8NoBOM v3-pair-report.json
```

Prepare the current identity replay and frozen evidence plan with `--paired`. Save
stdout JSON as UTF-8. The commands read the original selected V3 result bytes
automatically; `--edit-provenance`
is optional and, when supplied, is checked against a fresh source replay. Additional
report options are `--occupancy-reviews`, `--correspondence-reviews` and
`--identity-snapshot` (as an alternative to `--coordinates`). No provider/model/database
call or input modification occurs. The snapshot argument can be omitted when no group
has an available pair; supplied snapshots are still verified.

Library seams are `read_v3_result_sources`, `prepare_v3_correspondence` and
`build_v3_pair_report`. Original adopted edit/fragment sources establish occurrence
lineage, independent identities establish venue continuity, and the scorers establish
quality. The report retains local uncertainty, pair availability, exact signed deltas,
losses/replacements, route topology/context and independent conflict transitions.
Its pair mask/auxiliary totals remain separate from Ticket 08's four-final report.
Exit 0 means complete processing, including unavailable pairs and FAIL/UNKNOWN checks;
corrupt/stale material exits 2. See the [paired contract](../../docs/contracts/0005-quality-human-review.md#v3-pairs).

## Verification and status boundary

<a id="offline-cost-report"></a>

### Offline cost report

```powershell
.venv/Scripts/python.exe -m backend.evaluation.cost_report --usage saved-v0-usage.json --usage saved-v3-usage.json --snapshot saved-oracle-snapshot --prices prices.json --bills normalized-bills.json --annotations historical-annotations.json --output cost-report.json
```

`--usage` and `--snapshot` are repeatable; either one alone suffices. `--bills` and
`--annotations` are optional. All inputs are local, and original files remain unchanged.
The report is independent of quality scores and does not launch any model/API call.
Native snapshots must pass the existing raw/plan/attempt hash replay before normalization.
Their collection is shown in the oracle namespace, without artificial version attribution.

A minimal illustrative price file (synthetic rates, not a current provider quotation):

```json
{"schema_version":"rtpeval_prices_1","currency":"USD","rows":[
  {"price_id":"fixture-model","source":"synthetic worked example","as_of":"2026-10-05",
   "valid_from":"2026-10-01","valid_until":"2026-11-01",
   "match":{"kind":"model","provider":"fixture","operation":"chat","model":"test"},
   "rates":{"input_tokens":"2","cached_input_tokens":"0.5","output_tokens":"4"},
   "per":"1000000"}
]}
```

For 1,000 input tokens including 400 cached, and 200 output tokens, this yields
`0.0022` USD. Reasoning tokens are part of output, not another charge. Missing cache
counts do not imply zero; a deliberate no-discount assumption needs a source-linked
annotation, or the estimate stays unavailable. Each official price row must retain its
source/date/currency, billing unit and applicable context. Explicit proxy prices and SKU
scenarios must retain an `assumption`, rather than pretending unknown context is observed.

Normalize an existing invoice/export into rows according to its evidence:

```json
[
  {"bill_id":"invoice-line-1","scope":"event","currency":"USD","amount":"0.10",
   "source":"invoice.csv:1","usage_sha256":"<original usage file SHA-256>",
   "result_sha256":"<result hash from usage>","kind":"model","event_id":"<captured ID>"},
  {"bill_id":"resource-month","scope":"aggregate","currency":"KRW","amount":"12000",
   "source":"resource-month-export.csv:2"}
]
```

Those hash/ID placeholders must be replaced with genuine matching artifacts. A complete
run bill uses `scope: run`, artifact hashes and `complete: true` without kind/event ID.
Aggregate rows cannot bind events/runs, and no cross-currency conversion occurs.
Actual event charges override estimates; whole-run bills leave category/Repair allocation
unknown. Backing HTTP transport is not another model charge, and Repair is never added
to the run again. Missing costs remain null beside a partial observed subtotal.

The library seam is `build_cost_report(sources, prices, bills=..., annotations=...)`, where
each source has original `sha256` and `usage`. Annotation rows contain `usage_sha256`,
kind/event ID, `source`, `source_sha256`, `note` and `fields` (only missing billing context
or explicit cached-input assumptions). Import does not fetch cloud bills or query billing
warehouses. Do not attribute aggregate exports to individual runs without supporting data.

Relevant regression tests live in `backend/tests/evaluation/`
and the [blind-review frontend](../../frontend/src/features/blind-review/BlindReview.tsx).
Actual historical results are in [evaluation record index](../../docs/records/README.md)
and linked Issues. Synthetic checks do not establish real provider availability,
formal benchmark outcomes or a version freeze. Formal controlled-case construction/execution
and independent official-fact audit execution remain separately authorized.

## Mechanism and official-evidence audit workflow

```powershell
.venv/Scripts/python.exe -m backend.evaluation.mechanism_cli prepare --manifest manifest.json --observations linked-observations.json --output mechanism-preparation.json
.venv/Scripts/python.exe -m backend.evaluation.mechanism_cli prepare --selection controlled-preparation.json --output controlled-mechanism-preparation.json
.venv/Scripts/python.exe -m backend.evaluation.mechanism_cli report mechanism-preparation.json --output mechanism-report.json
.venv/Scripts/python.exe -m backend.evaluation.mechanism_cli audit-queue mechanism-preparation.json --output official-audit-queue.json
.venv/Scripts/python.exe -m backend.evaluation.mechanism_cli audit-report official-audit-queue.json --reviews official-audit-reviews.json --output official-audit-report.json
```

The two `prepare` examples are alternatives: an existing curated four-version manifest or
genuine saved Ticket 11 V3-only preparation. Optional observations and reviews may be omitted;
missing metadata is unavailable, not zero. Commands read local JSON without provider/model
calls, case replay or website checks. Reports retain internal mechanisms separately from
independent quality. Exit 2 identifies material corrections; valid missing observations,
unreviewed units and unavailable verdicts are retained in successful processing.

Library seams: `prepare_sources`, `read_batch_sources`, `report_mechanism`,
`build_audit_queue` and `report_audit`. The producer explicitly owns
`backend.app.observability.mechanism_capture.capture_attempt`: wrap its existing invocation,
supply original input/run identity and the exact saved-result serializer, and save the
emitted envelope through a synchronous local sink. No new planner run flag is required.
This capture is independent of enabled tracing/usage; custom injected adapters lacking the
submission observation remain partial. Sink/capacity/redaction failures preserve planning.

Official units require accepted typed claims and exact actual submission/rule occurrences.
Preparation-only and accepted-unused claims are excluded; submission does not prove model
attention or provider receipt. Queue/unit hashes bind independent reviews. Unreviewed and
unavailable units remain visible. Incomplete collection reports the observed unit count while
the full qualifying population remains null. See the
[wire contract](../../docs/contracts/0001-evaluation-artifacts.md#mechanism-audit-executable-wire)
and [offline acceptance](../../docs/records/evaluation/2026-10-04-mechanism-official-audit.md).

## Controlled V3 offline workflow

Run from the repository root with the existing Python environment. Commands emit JSON;
save artifacts as UTF-8 without BOM. Exit 0 means successful processing, including quality
FAIL/UNKNOWN outcomes; material/execution errors exit 2. Cases are supplied frozen
post-primary inputs, not ordinary planner captures automatically upgraded into runnable
cases. See the [case and review wire](../../docs/contracts/0001-evaluation-artifacts.md#controlled-executable-wire).
Use a dedicated offline process with an exclusive event loop and no other network work;
execute cases serially. The guard patches sockets and the loop clock. Do not embed this
executor in an active web-service event loop or run unrelated async tasks alongside it.

```text
python -m backend.evaluation.controlled_cli replay case.json
python -m backend.evaluation.controlled_cli prepare case.json execution.json requirements.json
python -m backend.evaluation.controlled_cli identity-references preparation.json
python -m backend.evaluation.controlled_cli identity-plan preparation.json
python -m backend.evaluation.controlled_cli identity preparation.json observations.json --prepare --model YOUR_JUDGMENT_MODEL
python -m backend.evaluation.controlled_cli identity preparation.json observations.json --model-result identity-model-result.json
python -m backend.evaluation.controlled_cli evidence-plan preparation.json identity.json --context context.json --route-reviews route-reviews.json --coordinates coordinates.json
python -m backend.evaluation.controlled_cli report case.json execution.json requirements.json expectations.json identity.json snapshot --context context.json --route-reviews route-reviews.json --coordinates coordinates.json --expected-plan plan.json --generated-at 2026-10-04T00:00:00Z
python -m backend.evaluation.controlled_cli batch controlled-batch.json --generated-at 2026-10-04T00:00:00Z
```

The evidence-plan command emits a route preparation containing `evidence_plan`; save that
plan separately for snapshot acquisition/verification. Collection remains the existing
injected-transport `acquire_snapshot` API and requires its own authorization if live.
The saved-snapshot replay and identity-evidence commands remain in `snapshot_cli`.
Use `identity-evidence DIRECTORY --historical` only to derive the original evidence wire
for historical policy replay. Current evidence keeps pagination metadata and uncertainty;
coordinate consumers select the derivation using the verified report's policy.
Independent identity observations, positive-count audit plan, schedule context, coordinates,
requirements and review material retain their existing schemas. No four-version manifest
is required for these controlled commands.

Both evidence preparation and reporting accept `--occupancy-reviews`. Reporting additionally
accepts `--correspondence-reviews` and `--factual-reviews` for separately linked human facts.
The raw Ticket 10 pair remains in `pair`; supplemental check outcomes remain in
`reviewed_checks`, with original scores/deltas untouched. A route fact may establish duration
compliance while a transfer commitment remains unknown; review occupancy through its own
source-backed channel rather than treating the route fact as a whole-itinerary PASS.

An expectations guard for an independently reviewed exact-one-visit requirement can be:

```json
{
  "goal_id": "one-visit-on-day",
  "basis": "explicit_requirement",
  "condition": {"kind": "daily_count", "date": "2026-09-26", "minimum": 1, "maximum": 1},
  "source": {"field": "additional_preferences", "quote": "Exactly one primary visit on this day."}
}
```

Place this in the reviewed expectations envelope's `guards` array and bind the envelope
to the emitted normalized `case_hash`. The quote must be present in that original request.
Such a guard is independent of the planner's interpreted requirements: a missed interpretation
can cause an internally adopted addition to be independently classified as regression.
Ordinary additions with supported new checks and preserved requirements are lawful changes.

Controlled batch manifests reference previously emitted reports with the standard relative
JSON artifact envelope (`path`, byte `sha256`, schema, media type and availability). Every
entry declares `case_id`, `role` and `expected_goal_ids`. Missing or invalid reports remain
unavailable inventory units. Counts describe submitted cases; no formal 32-case corpus,
live usage/cost measurement, version ranking or causal conclusion is produced.
