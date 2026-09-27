# Paris six-day V0–V3 development smoke plan

Archived execution plan: this batch is complete and its one-shot allowance is exhausted.
The commands and hashes below document the original run, not permission to run again.
See assessment.md for the recorded result; workspace-wide commit authorization on
2026-09-28 allows preserving these documents without additional live execution.

Date: 2026-09-27, Australia/Sydney. The user authorized one live run of each V0,
V1, V2, and V3 and approved the identical preference text below. The user also
requested a blind comparison of all four complete itineraries if all four finish.
This is development smoke testing, not a formal benchmark or version freeze.

## Fixed input and revision

Use `logs/paris_six_day_20260927/request.json` byte-for-byte for every version:
Paris, France; October 3–8, 2026 inclusive; two travelers; EUR 3000 whole-trip
budget; preference `We want to have an enjoyable trip in this city.` Dates,
traveler count, and budget are neutral development-scenario choices made because
the user supplied only the city, duration, and preference. Do not silently alter
them. The actual Sydney calendar date at each start is the reference date; the
launcher refuses an expired start or an unsupported 14-day request window.

Pinned preparation revision: `8f5e9b3cdb60c4c7f3fbb55f68ebb8a24dd7ac86` on
`feature/v3`. The source `config/runtime.yaml` SHA-256 is
`36b70a2eb79c09ea56ae459bf4474a6b0a4177eda005e31e54653c6d21423f2f`.
The prepared manifest records exact request and runtime-copy hashes plus the
initial dirty-file list. Only the trace directory and capture level are changed
in the copied runtime: normalized capture, raw provider payloads disabled.
No production policy, budget, prompt, or version behavior changes.

## Execution authority and limits

The `smoke tests` conversation alone executes the prepared cases, one independent
process and one attempt each, strictly V0, V1, V2, V3. Run from the repository root:

```powershell
.venv\Scripts\python.exe -m logs.paris_six_day_20260927.run_one v0
.venv\Scripts\python.exe -m logs.paris_six_day_20260927.run_one v1
.venv\Scripts\python.exe -m logs.paris_six_day_20260927.run_one v2
.venv\Scripts\python.exe -m logs.paris_six_day_20260927.run_one v3
```

Preparation has already run offline. Do not run `prepare` again, reset the
manifest, delete a case directory, change the input, or rerun a failed case.
The executor must request needed network permissions directly in its own chat
before the first launch. Use the existing Foundry, Google, Open-Meteo and
TripWorld dependencies only; do not run separate live connectivity probes.
No network or model retry is authorized for this batch. A sandbox permission
failure before launch is not a live attempt and should be resolved without a
restricted-network trial. A runtime network failure is an attempted case:
report it and do not retry. No commits, pushes, code fixes, or budget changes.

V1/V2/V3 use the copied runtime's existing 600-second development request
allowance; the wrapper imposes a 660-second outer process limit on every case,
including V0. V0 has no development-timeout flag. Existing per-tool and
per-model limits are unchanged, including six request-wide semantic calls,
120 total semantic seconds, 45 seconds per semantic call, and at most five
V3 Repair model calls. At most four live planning attempts are authorized.

Stop before another case if the request/revision/runtime hash changes, dates
expire, credentials are unavailable, the outer timeout fires, required captures
are missing, a secret appears in artifacts, a configured budget is exceeded,
or an unexpected provider is used. An ordinary application failure is reported
and may be followed by the next distinct version; it is never retried.
Stop on an ambiguous infrastructure state until Iteration 2 assesses it.

## Capture and checks

Preserve `manifest.json`, the copied `runtime.yaml`, per-case `result.json`,
`execution.json`, stderr and launcher logs, and available trace/budget summaries.
V1/V3 also preserve normalized requirement and semantic captures; V3 preserves
Repair capture if reached. V2 uses its independent CLI and trace; V0 uses its
independent tool-free CLI. The launcher records whether a zero-exit result
covers all six requested dates. After each case, inspect actual process status,
application status, capture status, usage against configured limits, version,
dates, and obvious missing/duplicate day or activity evidence. Separate
observed facts, inference, and missing evidence. A completed itinerary is not
proof of factual accuracy, confirmed cost, opening hours, route feasibility,
or satisfaction of a vague preference.

Write the execution report in English in the batch evidence directory and
send a concise Chinese report with exact paths to Iteration 2
`01a0e29d-405e-7d82-b894-d95eb7f67632`. Iteration 2 owns diagnosis and
acceptance judgment. If all four results have zero application exit and complete
six-date itineraries, prepare four anonymous itinerary-only artifacts without
version labels, project context, internal diagnostics, or generation history.
Only then spawn the user-requested isolated subagent with no conversation history
to compare all four by trip quality using the same request. Keep the mapping
private until the blind assessment is returned. The blind assessment is a
qualitative development check, not a formal benchmark or ground-truth audit.
