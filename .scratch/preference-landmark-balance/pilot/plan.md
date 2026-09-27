# Preference and landmark pilot: phase A execution plan

Prepared: 2026-09-28, Australia/Sydney.
Status: Authorized by the user on 2026-09-28 through live completion, subject to the
three-case single-attempt limits and stop rules below. No further user approval is required.
Outcome: all three attempts completed; Melbourne failed focus-target interpretation.
See [assessment](assessment.md). The plan below preserves the executed allowance;
it does not authorize retries or further cases.
Base: cc4d5a003412002b99e5f4bb6549631eea287782 plus the validated uncommitted ticket 03 tree.
No commit is required to run; the exact dirty source state must be hashed before execution.

## Objective and ownership

Check real-model behavior through interpretation, nomination, exact resolution, admission,
qualified supply, initial itinerary, validation, targeted Repair and final scheduling.
The primary question is whether the current V3 output follows the accepted preference/landmark
policy. Initial/final differences identify which stage changed the observed result; they do
not establish a controlled causal comparison. This is a small implementation pilot, not a formal
benchmark, version ranking or freeze. Iteration 2 owns preparation, tool adaptation, offline
checks and assessment. The existing same-project `smoke tests` conversation executes prepared,
authorized cases and reports blockers; it must not modify code, tune prompts or design fixes.
Results return to iteration 2, thread 01a0e29d-405e-7d82-b894-d95eb7f67632.

## Approved cases

All use V3, two travelers, the currently configured model/deployment and dates beginning
2026-10-03. The three adjacent JSON files are the full reviewable inputs. Budgets are user
trip budgets, not API spending limits; unknown costs must not be represented as verified.

| Order / ID | Destination / dates | Trip budget | Principal observation |
| --- | --- | --- | --- |
| 1 ordinary_sydney_v3 | Sydney, Australia; Oct 3-5 | AUD 1800 | Especially liking museums stays ordinary target 1; gardens/architecture are separate soft interests |
| 2 focus_melbourne_v3 | Melbourne, Australia; Oct 3-5 | AUD 1800 | Explicit museum trip focus has sourced target 2; other ordinary interests remain 1 |
| 3 short_brisbane_v3 | Brisbane, Australia; Oct 3 only | AUD 600 | Four interests, relaxed pace and explicit maximum 3 main visits; gaps must be truthful |

Distinct destinations exercise portability; outcomes are not causal A/B comparisons.
No fixed list of must-include landmarks, category percentage or mandatory soft-goal success
is imposed. Unavailable or infeasible options may remain unused.

## Approved execution allowance

- Exactly three sequential fresh-process case attempts, one per input. No parallel calls
  across cases, reruns, network probes, alternative prompts or extra cases.
- 600-second application deadline and 660-second outer process limit per case, at most
  1980 seconds (33 minutes) total process allowance. These are ceilings, not latency forecasts.
- Existing config/runtime.yaml stays authoritative. Only trace output location and normalized
  capture settings may change in a frozen runtime copy. Raw provider envelopes stay disabled.
- Per V3 case: at most one interpretation, one nomination and one primary generation call.
  Nomination: 12 names, 8000 input / 2000 output tokens, 20 seconds within request deadline,
  zero retry/correction. Three cases therefore allow at most three nomination sends.
- Candidate search: 12 per case including at most 4 nomination supplements (36 / 12 batch
  maxima) for primary candidate search; destination search is separate, at most 1 per case.
  Primary acquisition Details ceiling is 60 per case. RAG and Repair have separately named
  stage allowances below; do not report 12 searches or 60 Details as the whole V3 total.
- Semantics retains 6 calls / 120 seconds total / 45 seconds per call, including existing
  bounded correction behavior. Existing Profile, Web, Weather, Routes and Nearby budgets
  remain in force. The total model calls are NOT limited to interpretation+nomination+generation.
- C/G/K remain duration-dependent: 3-day cases C48/G24/K12, 1-day case C48/G16/K8.
  G is the normal Details new-success target, not an independent total send ceiling.
- RAG is enabled through the existing V3 path and `.env.tripworld`. Per case, initial RAG
  limits remain 4 queries / 80 positions / 2048 total query tokens, top_k 20, at most 30
  resolution entities / 30 Details calls / 4 fallback calls, and a 360-second stage deadline
  subject to remaining request time. Existing cache and shared-budget charging apply; these
  stage bounds are not permission to add budgets together or increase an effective ceiling.
- V3 Repair retains quantity_review_enabled=true and overfull_review_enabled=false. At most
  5 rounds / 5 model calls per case (15 Repair model calls across three cases), only for
  existing authorized targets. The 360-second stage / 120-second round / 70-second model
  limits are shortened by request remainder and existing preparation/recheck/Nearby reserves.
  At most 252000 input / 16384 output tokens per Repair call. No minimum number of rounds
  or successful repairs is promised; do not trigger Repair just to exercise it.
- Repair acquisition limits are stage totals across all rounds: Google 6 including reserved
  fallback 1, embedding 1, retrieval 1, canonical attempts 30, Details 30, route sends 24 /
  elements 32, top_k 10. They retain existing ledgers and request ceilings. Semantics' six
  calls and 120 seconds are shared by primary preparation and Repair, never reset per round.
- RAG and Repair consume the same 600-second request allowance; no extra 360 seconds is
  added to it. There is still one nomination and one primary generation, not one per round.
  Soft preference gaps alone and nomination rank do not authorize new Repair actions.
- Input Polish and destination autocomplete are not invoked. Use the current deployment
  and configured embedding/retrieval resources; no database rebuild, reindex or service
  repair is included. Missing RAG dependencies are blockers, not permission to run as V1.
- This is a call/time/token-bound authorization proposal, not a dollar cap. Report actual
  available usage; unavailable billed usage and monetary costs remain missing.

Use the real Australia/Sydney execution date. All trips must still be future and inside the
current date window. Stop before calls on Oct 3 or later; never backdate or silently shift
inputs. If delayed, iteration must revise dates and obtain approval for the updated inputs.

## Tool readiness and execution gate

Existing tools.validation.poi_semantics_acceptance supports V3 with --version v3,
--rag-env-file .env.tripworld, --capture-requirements, --capture-semantics and --capture-repair,
plus Product/result output and trace/budget evidence. The preference_gate_smoke
tool only runs interpretation and is insufficient for this end-to-end pilot. Historical
Paris/semantic launchers illustrate one-shot process control but must not be executed or
copied unchanged: they freeze different cases, dates and earlier code.

Before live dispatch, iteration must finish and offline-validate a small development-only adapter:

1. Capture bounded normalized nomination input/output/outcome (including all nominated
   names/ranks) and exact resolution outcomes, plus admission/supply IDs. Existing compact
   budget events contain aggregate counts and cannot alone explain lost nominees.
2. Preserve production behavior, cancellation and client ownership. Never modify returned
   nominations, retry, resolve aliases or obtain extra evidence. Reuse normalized redaction
   and capture caps (1 MiB per stage / 4 MiB per case); no credentials/raw provider envelopes.
3. Freeze source hashes for backend/app, scripts, relevant validation tools, dependencies,
   case inputs, runtime and launcher, including untracked source files; HEAD alone is
   insufficient for this dirty tree. Refuse mismatches before any client construction.
4. Verify one-shot markers, order, real-date checks, timeout and capture failure behavior
   with fake collaborators. Do not contact providers during preparation.
5. Persist the normalized initial itinerary and its validation/coverage report independently
   of Repair invocation, then retain final itinerary/report, per-round proposed changes,
   acceptance/rejection and stop reasons. Existing before_repair_stage capture is useful
   when reached but does not replace initial capture on no-target/deadline/early-stop paths.
   If generation never completes, mark initial/final evidence not reached. If an initial
   itinerary exists and Repair is skipped, record why and whether final equals initial.
6. Validate local RAG configuration without exposing credentials or making connectivity
   probes. Actual embedding/database operations occur only within the approved case attempt.
7. Produce manifest/runtime copy and exact launcher commands. This plan alone is not an
   executable dispatch packet; the smoke conversation must not fill the tooling gaps.

The user subsequently authorized completion of preparation and these three live attempts
without further approval. Stage B remains excluded; dispatch uses the ready packet only.

## Acceptance and evidence

Save fresh evidence under logs/preference_landmark_pilot_20260928/<case_id>/, never overwrite
an existing attempt. Keep batch manifest, input/runtime/source hashes, execution status,
normalized requirement/nomination/semantic captures, RAG diagnostics, initial itinerary and
validation/coverage report, Repair snapshots and round outcomes, trace, independent budget.json,
final result/Product output and a per-case assessment. Logs remain ignored/private; reports contain
no credentials or raw provider envelopes. Missing mandatory evidence means inconclusive,
not an inferred pass. Preserve failure artifacts as carefully as successful runs.

For each case, construct a small lineage table: nominated name/rank -> exact canonical ID
or unresolved reason -> admitted -> Details/role-qualified -> supplied -> initially scheduled -> finally scheduled.
Separate supported preference relationships from discovery associations, model landmark
knowledge and operating facts. Trace truncation must not be repaired by inventing evidence.

Compare initial and final states for scheduled landmark IDs/ranks, distinct supported
preference coverage/gaps, main visits per day, explicit restrictions, and validation findings.
Attribute changes to recorded accepted Repair actions only; report rejection, no-target,
resource exhaustion and unavailable evidence separately. Repair may improve quantity while
leaving soft gaps or UNKNOWNs. Do not equate model output or completed status with verified
feasibility. Loss of a preference/landmark is an observation requiring context, not by itself
an unauthorized Repair finding.

Record two separate judgments:

- Engineering acceptance: valid source-backed target 1/2 interpretation; explicit maximum
  retained; no candidate-only or reference-only final satisfaction; exclusions/identity/role
  rules intact; nomination/search/call/deadline bounds respected; no extra primary generation,
  repeated nomination or unauthorized Repair; complete evidence and valid output dates/contracts.
- Planning observation: representative options reach supply; independent same-category
  landmarks remain possible; actual selection balances interests with routes/time/variety;
  overlap and sparse days are explained where evidence permits. A soft gap or unused landmark
  alone is not a confirmed violation. A returned itinerary alone is not acceptance.

Classify mechanisms as exercised-pass, observed-failure, not-exercised or evidence-missing.
Zero resolved nominations can demonstrate correct fallback but cannot demonstrate successful
landmark balancing. A supported multi-interest POI may satisfy several interests; four
interests and maximum three visits does not logically require a gap. If a gap exists, check
its disclosure rather than forcing an expected count. Never manufacture failures to exercise
fallback, correction or overlap branches.

Inspect results between cases. Stop the batch for a runtime/code/input mismatch, invalid
date, credential failure, unexpected provider use, exceeded budget, lost mandatory capture,
secret exposure or a confirmed identity/restriction boundary failure. Preserve and report.
An isolated auxiliary nomination failure may continue if its fallback and evidence are sound.
Other terminal application failures stop for iteration diagnosis; no automatic retry.

Smoke tests returns an English report.md and concise Chinese handoff with process, outcomes,
actual calls/time/available usage, observed facts versus inferences, Spec deviations, missing
evidence, blockers and paths. Iteration decides acceptance and next steps.

## After phase A

Only after reviewing these V3 cases, consider separately approved V0 prompt checks or V2
integration checks if a concrete remaining question warrants them. Use V1 only to isolate a
specific observed shared acquisition/initial-generation problem; prepare the exact case and
budget first. No automatic V1 rerun or four-version matrix is included. Diagnose reproducible
failures before implementation changes; do not compare cross-version superiority.
Commit timing remains the user's decision; no commit, push or freeze is included.

## Preparation validation

All three proposed JSON inputs passed the current PlanningRequest schema and actual
Australia/Sydney date-window checks on 2026-09-28. Current nomination/search/
request-deadline defaults match this proposal. This validation performed no model/provider
calls. The development-only capture/one-shot adapter remains a readiness prerequisite.

## Approved planning change - 2026-09-28

The user agreed to replace all three proposed V1 cases with V3 to inspect the final V3
outcome directly, retaining initial-versus-final evidence for diagnosis. Case content,
dates and trip budgets are unchanged; filenames now end in _v3. This approves the plan
revision, not live dispatch. The previous V1-first proposal is superseded. RAG/Repair can
increase actual cost within the same proposed request deadline; no dollar estimate is claimed.
The initial-result and nomination-lineage capture adapters remain unimplemented readiness
work. No live call, commit or dispatch has occurred.

Revision validation: all three renamed V3 case files passed schema and real-date checks
on 2026-09-28. RAG query, Repair call/review flags, shared semantic calls and
request timeout were checked against config/runtime.yaml. No provider was constructed
or contacted; production code/configuration and test results were not changed.

## Execution authorization and tooling checkpoint - 2026-09-28

After approving the V3-first revision, the user explicitly authorized proceeding through
live completion without another approval. `tools/validation/landmark_pilot.py` is the new
development-only launcher/observer; it reuses the current V3 acceptance tool. Source/runtime/
input drift, repeated attempts and case reordering fail before providers. The initial snapshot
is written at post-primary entry and initial validation at its first assessment; successful
final results retain both reports and Repair outcomes. Nomination and resolution observations
are isolated from planning failures. Independent budget.json is required.

The new lineage stream has a 1 MiB per-artifact and 4 MiB per-case ceiling; existing requirement,
semantic and Repair capture streams retain their own existing caps (not a new combined 4 MiB
cap over every historical capture channel). Missing/overflowed mandatory evidence stops the
batch. No raw provider envelopes are enabled. Only hashes of credential files are frozen;
credential values are not written into the manifest or chat.

Targeted tooling checks: 21 tests passed before final readiness checks; Ruff passed. Tests
cover drift/order/attempt consumption, failed child/outer timeout, actual V3 with fake model
and providers, redaction/size bounds and capture write failure isolation. Initial test mocks
also intercepted git subprocesses; narrowing that mock corrected two test-only failures.
No production source or resource policy was changed for this tooling.

Final readiness: 25 targeted tests passed; both reviews found no remaining blockers.
Batch prepared offline; exact commands and between-case gates are in dispatch.md. No
production source changes are permitted while this frozen three-case execution is active.
