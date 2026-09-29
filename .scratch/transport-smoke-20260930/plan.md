# Three-day transport responsibility live smoke

Date: 2026-09-30, Australia/Sydney. Status: Authorized preparation and one-shot execution.
User request in Evaluation implementation: run a three-day smoke. The user-facing
defaults were Berlin, October 3-5, two travelers, EUR 1500, the broad preference below,
V0-V3 once each. Iteration ownership was previously transferred to Iteration 2, which
owns this plan, tooling and assessment; `smoke tests` executes and reports only.
This authorizes bounded real service calls, not production fixes, Git writes, extra
runs, a blind review, formal evaluation or benchmark execution.

## Input and current tree

All versions use adjacent request.json byte-for-byte: Berlin, Germany; 2026-10-03
through 2026-10-05; two travelers; EUR 1500; preference
`We want to have an enjoyable trip in this city.` Real Sydney launch date is the
reference date. Never backdate or silently shift trip dates if they expire.

Inspected branch: feature/evaluation. HEAD: 1eb441f47cb0de65eb1c687eb56a45dba286aa86.
Existing uncommitted Ticket 04 and transport-correction code/tests/docs are preserved.
The current primary DTO prohibits declared transport for V1-V3; shared acceptance
rejects it without deletion/retry. V0 retains its own transport-capable DTO/prompt.
V3 Repair stays operation-only and reserves route binding to the application.
Evaluator traffic-source changes are present but this smoke does not run the evaluator,
Ticket 05 metrics or any independent oracle calls.

Source acceptance reports 1973 passed / 10 skipped and clear Standards/Spec reviews;
this plan treats those as reported offline evidence, not as a substitute for live results.
The new manifest hashes all backend Python (including dirty evaluation/tests), scripts,
validation tools, runtime YAML, dependency files, new packet files, local env files and
corpus manifests, plus relevant environment overrides. It records full HEAD and dirty
paths. No secret values are emitted. Unrelated concurrent edits must not be folded in.
Stop on hash drift rather than modifying/re-freezing an in-progress batch.

## Actual current allowance

The runtime was inspected on 2026-09-30. Its copy changes only trace directory and
normalized capture level; no product budget, prompt or retry value is changed here.
Full frozen runtime.yaml remains the authority for all fields not summarized below.

- Four fresh processes in order V0, V1, V2, V3, one attempt each. Outer cap 660 seconds
  per case, 2640 seconds across cases; V1-V3 have a 600-second shared request deadline.
  V0 has its current provider timeout and the outer limit, without an invented CLI flag.
- Current primary generation allowance: 252000 input / 16384 output tokens. V0 remains
  its independent plain-LLM path with interpretation and one generation; do not inject
  tools, nomination, RAG, validation or Repair into it.
- V1-V3 nomination: one call, 12 names, 8000 input/2000 output, 20 seconds, zero retry;
  supplementary searches at most 4 within the primary candidate-search limit of 12.
  Destination search 1; primary Details ceiling 60. Duration-dependent candidate/detail
  success/supply capacities retain current policy; effective limits must be read from
  each actual budget summary rather than treating YAML upper bounds as actual sends.
- Routes: baseline 7 sends/400 run elements (64 per request); alternative 32 directed
  pairs/32 sends/64 elements, with existing post-generation reserves 16/16/32;
  route work 120 seconds including a 30-second post-generation reserve; provider
  timeout 20 seconds. Existing ledger scopes and cache charging remain authoritative.
- Semantics: 6 calls/120 seconds shared across primary and Repair; 45 seconds per call,
  32000 input/8192 output. Existing bounded semantic correction is retained, not a
  discretionary permission to repeat the entire request.
- V2/V3 initial RAG: top_k 20; 4 queries/80 positions/2048 query tokens; canonical 30,
  Details 30/fallback 4; 360-second stage within request time; retries zero.
- V3 Repair: at most 5 rounds/5 model calls; stage/round/model 360/120/70 seconds within
  request remainder. Input/output 252000/16384 per call. Quantity review true, overfull
  false. Stage acquisition: Google 6 including fallback 1, embedding 1, retrieval 1,
  canonical 30, Details 30, route sends 24/elements 32, top_k 10. No new targets or
  forced Repair run. If Repair is not triggered, report that live path unexercised.
- Nearby: 3 requests/3 references, 10-second stage, 4-second request timeout, no retry.
  Weather, profile and web evidence use current frozen limits and current authority.
- Trace: enabled, normalized, raw provider payloads false, 10,000,000-byte payload
  threshold. Do not increase it or reconstruct a truncated result during this batch.
- Trip budget EUR 1500 is not an API spending cap. Capture actual available counters
  and billed usage; missing values remain unknown. No cost claim from missing usage.

## Network, attempts and stop rules

Execute only after the executor obtains needed network permission for the existing
configured Foundry, Google, weather, evidence and TripWorld dependencies. No external
connectivity probes, corpus rebuilds, service repairs, new dependencies or subscriptions.
Preparation checks local settings/manifests only; it does not prove network/DB health.
A pre-launch permission denial does not spend a live attempt. Once started, any runtime
network failure or application rejection spends that case's one attempt. No rerun.

Stop before starting another case on source/input/runtime/environment drift, expired
dates, missing credentials, ambiguous infrastructure, timeout, missing/truncated
required evidence, secret exposure, actual budget overrun or unexpected provider.
Record ordinary generation rejection as a case failure. If execution/capture evidence
is sufficient and no structural stop occurred, proceed to the next distinct version.
Do not stop solely on sparse days, repeats, UNKNOWNs or absent Repair. These may be
quality observations, not permission to change the plan or add attempts.

The launcher records unique attempt locks before invocation and all process output.
Do not clear them, retry prepare, reset the manifest or reuse historical six-day paths.
Launch V0, inspect its evidence, then V1, V2, V3 separately. Do not unconditional-chain.

```powershell
.venv\Scripts\python.exe .scratch\transport-smoke-20260930\run_one.py v0
.venv\Scripts\python.exe .scratch\transport-smoke-20260930\run_one.py v1
.venv\Scripts\python.exe .scratch\transport-smoke-20260930\run_one.py v2
.venv\Scripts\python.exe .scratch\transport-smoke-20260930\run_one.py v3
```

Working directory: D:\Workspace\Capstone\Reliable-Trip-Plan-Agent.
Evidence root: logs/transport_responsibility_20260930/. Preparation is owned by iteration;
dispatch confirms when it is frozen. A launcher process exit is not application success;
inspect manifest and case execution.json. Any stopped_* state forbids further cases.

## Acceptance and report

For each output, check application status, matching version, all three ordered dates,
activity roles, schema and capture integrity. If no result is delivered, save the
generation-rejection/error stage and available evidence rather than inventing transfers.
V1/V3 capture normalized requirements/semantics, V3 Repair when reached. V2 uses its
own CLI trace; V0 has no injected tracer. Do not assert equal diagnostic coverage.

Run inspect_result.py against a successful result as a read-only aid. It reports actual
chronological occurrence pairs, transfer counts/identity/time matches, diagnostics,
unlocatable adjacencies, orphan transfers and model transport roles. Its findings are
structural observations, not a factual travel oracle or formal evaluation. A diagnostic
PASS without a transfer is not a completed binding; zero pairs does not prove a route
path was exercised. Check full context manually, including generic/unlocated activities.

- V0: model transport Activity is permitted and expected for different same-day venue
  visits, with named endpoints, mode and explicitly estimated duration/route. No
  fabricated canonical identities or provider-backed transfers. Report omissions,
  overlaps and unmarked estimates. Optional Nearby content is an observation only.
- V1-V3: zero declared model transport Activity. Manually inspect generic/free-time
  titles/notes for disguised transport; current mechanical checks do not prove absence
  of all transport prose. Actual same-day cross-place adjacent occurrences should have
  application-owned transfers tied to the right activity IDs, direction and interval,
  with available Routes evidence and diagnostics. Missing/invalid transfers are not
  passing transport coverage. Keep absence, UNKNOWN and real contradictions distinct.
- V3: inspect original/final roles, route bindings, validation and Repair records.
  If rejected proposals or transport-related rejection exist, report them and whether
  a delivered final result remains valid. Never add an attempt to force this branch.

Report per-version structural completion, source-boundary adherence and route-binding
coverage separately. Even complete bindings do not independently verify real-world
openings, pricing or travel feasibility. Inspect primary used/limit pairs plus stage
semantics/nomination/RAG/Repair/Nearby counters. Unknown usage is not zero.
Preserve English report.md, concise faithful itineraries.md and per-pair observations
under the evidence root; send results/blockers with paths to Iteration 2
01a0e29d-405e-7d82-b894-d95eb7f67632. No blind agent, Git write or production fix.

## Offline readiness

Ten mocked tests passed: four-case ordering and no-blind gate, source drift, timeout,
incomplete-day observation, budget stop, independent CLI dispatch, missing transfer
despite a PASS diagnostic, valid binding, duplicate/wrong-identity binding, and forbidden
model transport role. No real provider was called. Initial formatting/lint issues were
corrected; final static checks must pass before freezing.
