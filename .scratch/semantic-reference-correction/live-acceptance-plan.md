# Minimal live revalidation plan for semantic reference correction

Status: Approved for tool adaptation, offline validation and three one-attempt live cases; live execution not yet started. Prepared on 2026-09-27 (Australia/Sydney) against
uncommitted work based on `339e7e4a4a9eac133f2bdff69217b8b35c6990b4`.
This is development acceptance of the existing V1-V3 citation correction, not a
formal version benchmark, version freeze, or authorization to make live calls.

## Scope and fixed inputs

Run only the three 2026-09-26 failures, in this order, once each in separate
processes: Sydney V1, Sydney V3, Melbourne V1. Use the original JSON bytes from:

- `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\live_smoke_20260926\sydney\input.json`
- `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\live_smoke_20260926\melbourne\input.json`

Both requests specify two travelers, AUD 3000 and the same one-sentence
landmarks/waterfront/local-food preference. Sydney spans 2026-09-28 through
2026-10-02; Melbourne spans 2026-09-28 through 2026-10-05. Preserve every JSON
field, including the dates. Record input SHA-256, Git HEAD, dirty-file list,
runtime-config SHA-256, prompt versions, run ID, start time and the actual
reference date for each case. Do not copy secrets or environment files into the
output.

At each case start, obtain the date in the configured `Australia/Sydney` zone
and pass it explicitly as `--reference-date`. The dates remain within the
shared 14-date/10-day policy if the reference date is 2026-09-27 or
2026-09-28. Stop before external calls if it is 2026-09-29 or later; do not
backdate the run or silently alter the original request. A date change across
cases must be visible in the manifests. Also stop before external calls if
the approved three-case input or runtime policy differs unexpectedly.

## Capture wiring to prepare offline before approval to execute

`tools/validation/poi_semantics_acceptance.py` already wraps the V1 runner's
client factory, and V3 delegates its CLI to that runner. Its
`CapturedSemantics` observer saves normalized `input`, `output`, and `outcome`
records with call IDs and `correction_of` links. However, the current tool
always calls V3, parses only `V3PlanningResult` on success, and its CLI does
not expose the `reference_date` argument already accepted by `run_case`.
Thus the existing CLI cannot provide equivalent independent V1/V3 evidence.

Before any live run, make only these development-tool changes:

1. Add an explicit `--version {v1,v3}` selector and select the independent
   `backend.app.versions.v1.runner.main` or V3 main accordingly. Keep V3 as
   the existing default for old callers. Record the version in the case
   manifest; reject V3-only Repair flags for V1.
2. Expose `--reference-date` on the acceptance CLI and forward it to
   `run_case`; retain the V3 `--rag-env-file` loading and pass no RAG setup
   to V1. Use one case/output directory per invocation.
3. Keep V3 Product serialization; on V1 success validate the V1 result type
   and save its normal CLI result without calling V3 presentation. Preserve
   the application's exit code independently of capture completeness.
4. Add offline, mocked V1/V3 CLI-path tests confirming version routing,
   reference-date forwarding, credential redaction, normalized three-stage
   capture, failed-first/corrected-second call linkage, first-call success,
   capture-size failure reporting, and no extra provider call from capture.
   Run the focused acceptance/capture tests and scoped lint before live use.

No production service, schema, prompt, policy, budget, or version entry point
changes are proposed. The adapter must not relax strict citation or other
semantic validation. Current `DevelopmentRequirementCapture` redacts known
client secrets; it is not a general personal-data anonymizer. Keep outputs
in ignored local directories with existing ACLs; inspect for accidental
secrets before sharing or committing any summary. Full rejected historical
Sydney outputs were not retained, so this is a new live observation, not a
replay of those exact responses.

## Live ceilings and execution policy requiring separate approval

Only after explicit approval of this concrete plan and successful offline
adapter checks, execute the three cases sequentially. Enable semantic and
requirement capture for each; enable Repair capture for Sydney V3 to locate
any downstream outcome if generation becomes reachable. Copy the current
runtime config only to set an isolated normalized trace directory. Keep raw
provider payload capture off. Do not raise any configured limits.

Per case, use the existing 600-second application development ceiling and a
660-second outer process kill. There is one process attempt per case and no
automatic network retry in this minimal plan. Record failures and continue
to the next case unless a global preflight/credential/date/budget/capture
safety stop applies. A semantic failure must not be bypassed to obtain a
partial itinerary. Each case uses the existing request-wide POI semantics
limit of six model calls, 120 cumulative seconds, 45 seconds/call, 32,000
input and 8,192 output tokens/call. The correction is at most one extra
assessment of the same batch and consumes those same limits. Main generation
remains at 252,000 input and 16,384 output tokens/call. V3 Repair remains at
five rounds/five model calls, 360 stage seconds, and 252,000 input/16,384
output tokens/call. The whole run is bounded by three cases, not by a
separate monetary cap; actual usage and provider sends must be reported.

The unchanged per-case external-service policy ceilings include Places
destination search 1, candidate search 12, ordinary Details 60 and review
Details 8; weather 2; baseline route matrix 7 requests/400 elements,
alternative route matrix 32 requests/64 elements; web evidence 8 tasks and
8 page fetches; Nearby references 3 requests. V3 additionally permits
TripWorld retrieval up to 4 queries/80 positions, 30 resolution Details
and 4 fallback calls. These are configured ceilings across distinct
subsystems, not an additive estimate of billable HTTP requests; record the
actual counters and provider errors. Existing RAG, route, web and Repair
deadlines can stop work earlier. Check credential availability without
printing values. If observed sends exceed configured bounds, an unexpected
external service is invoked, or output capture exposes a secret, stop the
batch and investigate before further live calls.

Save each case under a new unique ignored directory of the form
`D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\semantic_reference_revalidation_20260927\<case-id>\`.
Expected files are `request.json`, `manifest.json`, `runtime.yaml`,
`started.json`, `result.json`, `stderr.log`, `execution.json`, `trace/`,
`requirements/`, `semantics/`, and for V3 `repair/` if reached. Save a
batch-level `manifest.json` and English `report.md` in that root. Do not
overwrite or append to the 2026-09-26 smoke evidence. Semantic capture is
limited to 1 MiB per stage and 4 MiB per case; record `incomplete` on a
capture failure or limit. The trace policy caps an individual normalized
payload at 1,000,000 bytes and may truncate a large `run.json`; corroborate
with events and case captures. Never save raw provider envelopes.

## Acceptance and reporting

For each semantic batch, join normalized records by `call_id` and
`correction_of`, and compare to trace events. Report separately:

- First-call pass: the first semantic output is accepted and no correction
  was sent. This validates this run's path but does not demonstrate the new
  correction's efficacy.
- Corrected pass: the first output fails specifically on invalid/missing
  evidence references; one linked second call is sent with bounded feedback;
  its entire result passes identity, match, exception and citation checks.
  This is direct evidence of the bounded correction for that batch.
- Corrected but later failed: the semantic batch passes on the second call,
  but generation, route, validation or Repair subsequently fails. Do not
  mislabel the full itinerary as completed.
- Uncorrected failure: the second output fails, the correction cannot be
  sent within limits, or the failure is outside the citation class. Retain
  the terminal error and reason. A missing capture makes mechanism efficacy
  unverified even when a CLI result exists.

For each case also report application exit, requested-date coverage,
semantic calls/tokens/time, API counters, RAG status for V3, generation
reachability, V3 validation/Repair targets and accepted edits if reached,
and evidence completeness. A complete itinerary does not imply verified
activity costs, budget fit, route feasibility or general model reliability.
The three cases answer whether the current citation correction works on
fresh live outputs, not whether V1/V3 as a whole are complete.

The original failure evidence is in
`D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\live_smoke_20260926\report.md`
and sibling `traces/` directories. Implementation context is in
`PROJECT.md`, `.scratch/semantic-reference-correction/spec.md`, and
`docs/shared_poi_semantics_plan.md`. After execution, send the new report
and exact evidence locations to the same-project iteration task, distinguishing
observed facts, inference and unavailable evidence.

## Budget decision boundary

Do not tune budgets as part of these three runs. If a correction is blocked
by a measured call, time or token ceiling, report the exact counter,
deadline and presend stop. Compare an independently proposed modest limit
increase with another mechanism using expected extra spend, latency,
complexity, bounded validation and rollback criteria. A higher budget can
enable a call but cannot make an invalid citation valid or weaken evidence
checks. Any increase requires separate approval and a new run scope.


## Execution readiness handoff

The iteration conversation owns this plan, tool implementation and result assessment.
The smoke tests conversation only executes these prepared commands and reports evidence.
The acceptance adapter changes have been inspected by iteration; its focused tests passed
30 cases. Iteration removed an unvalidated launcher placeholder, blocked overlapping case
starts, and included launcher logs and JSONL events in the known-secret scan. Four mocked
launcher tests passed (ordering, no rerun, capture/secret stops and overlap prevention).
No external calls were made by these checks. The launcher and its tests remain ignored local
artifacts under `logs/semantic_reference_revalidation_20260927/`.

From the repository root, iteration prepares the batch once with:

```powershell
.venv\Scripts\python.exe -m logs.semantic_reference_revalidation_20260927.run_one prepare
```

After iteration confirms readiness, smoke tests runs these commands sequentially, checking
the batch manifest and stop conditions before each next command:

```powershell
.venv\Scripts\python.exe -m logs.semantic_reference_revalidation_20260927.run_one sydney_v1
.venv\Scripts\python.exe -m logs.semantic_reference_revalidation_20260927.run_one sydney_v3
.venv\Scripts\python.exe -m logs.semantic_reference_revalidation_20260927.run_one melbourne_v1
```

Never rerun prepare or any started case. Inspect the recorded counters and provider failures
between cases for the plan's global stop conditions; the local launcher is not a replacement
for that assessment. If a tooling blocker appears, stop and report it to iteration without
editing code or inventing an alternative execution path.
