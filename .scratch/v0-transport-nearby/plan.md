# V0 transport and Nearby prompt revalidation

Date: 2026-09-28, Australia/Sydney. Status: Authorized by the user's instruction to
implement the proposed review -> one V0 live -> grouped commit workflow.
Iteration 2 prepares and assesses; `smoke tests` executes only this prepared case.

## Scope and review

Current changes: runtime capture threshold 10,000,000 bytes; V0 prompt explicitly
requests estimated transport activities and useful nearby model-knowledge references.
V1/V2 already have Nearby; V1 repeated visits are accepted as a version limitation,
not a current fix task. No planning/schema/tool/Repair addition is included.
Review baseline: e68d8e6a4297d50a98fcacb3241d392781dec022 plus the scoped working tree.
Parallel code-review axes: Standards zero findings; Spec zero findings. Both were
read-only and confirmed real prompt compliance still needed a live observation.

## One-shot execution contract

Use the adjacent request.json byte-for-byte, copied from the original Berlin request:
Berlin, Germany; October 3-8, 2026; two travelers; EUR 3000; preference
`We want to have an enjoyable trip in this city.` Do not change these inputs.
One V0 run only, current deployment, independent scripts/run_v0.py. The existing V0
path uses interpretation and one primary generation; no tool/RAG/Repair stages are
added. Maximum outer process time 660 seconds; V0 has no 600-second application flag.
Existing client timeout/retry settings remain unchanged, with no discretionary retry,
probe, regeneration, alternative input, or other version run. No new blind reviewer.

Preparation freezes HEAD, Python sources, runtime YAML, dependency files, input,
launcher and environment hashes into logs/v0_transport_nearby_20260928/manifest.json.
V0 still uses the source runtime; it has no injected trace. This run cannot validate
the 10 MB V3 trace cap: that configuration was checked offline separately.
Stop before launch on any mismatch, missing credential, expired/unsupported dates,
or an existing started/execution marker. Use the real Sydney reference date.
After launch, any timeout, provider failure, secret exposure or incomplete output
consumes this attempt; report it without rerunning or editing code. A pre-launch
permission denial does not consume an attempt. Obtain execution network permission
in the smoke conversation; do not try a restricted-network trial first.

Preparation is offline. Once dispatch confirms preparation, run exactly:

```powershell
.venv\Scripts\python.exe .scratch\v0-transport-nearby\run_once.py execute
```

Working directory: D:\Workspace\Capstone\Reliable-Trip-Plan-Agent.
Never run prepare again, clear markers, or reuse the original exhausted four-case
launcher. An execution record with zero exit still needs the output checks below.

## Acceptance and reporting

Preserve result.json, stderr.log, manifest.json, started.json, execution.json. Validate
the result using the existing PlanningResult schema and check system_version=v0,
all six dates present, and nonempty main sightseeing days. Report daily main visits
separately from transport/generic/free-time activities. Do not compare total activity
counts to the older V0 output as if added transport were added sightseeing.

Inspect each pair of consecutive different scheduled venue visits on each day:
transport should appear between them, name endpoints/mode, allocate estimated time
without overlapping visits, and state it is unverified. All source_place_ids must
remain null; no invented provider-backed transfer records or verified route claims.
Report missing legs or ambiguous roles instead of guessing they comply. Compare
actual main-visit counts and balance with the old output as observations, not causal
proof of whether the prompt displaced visits or improved quality.

Check one to three useful model-knowledge Nearby references linked to a planned
day/area, with unverified proximity/availability, no scheduled venue duplicates,
no reference times/costs/booking claims, and no false external identity. An empty
list is schema-valid when no suitable option exists, but does not demonstrate the
positive Nearby behavior sought here; report it for iteration assessment.

Do not require identical venues, exact old counts, invented recommendations, known
costs or real-world routing verification. All real-world estimates remain unverified.
This is a bounded prompt implementation check, not a benchmark or version freeze.
Write report.md and a faithful itinerary.md in the evidence directory. Send results,
limitations and paths back to iteration thread 01a0e29d-405e-7d82-b894-d95eb7f67632.
Only iteration assesses completion and handles the approved grouped commits.

## Offline verification before dispatch

Standards review: zero findings. Spec review: zero findings. Relevant combined tests:
176 passed in 11.27s, including observability/config/V3 wiring, V0, V1 references, V2,
Nearby/output roles/DTOs and the four launcher gates. Ruff passed. The first launcher
test run accidentally intercepted its Git HEAD subprocess with the fake planning
process; the test fixture was corrected to supply a fixed offline HEAD. All four
launcher tests then passed, followed by the combined selection. No production fix
or live retry resulted from this test-only correction. Preparation and a separate
preflight check passed without external requests.
