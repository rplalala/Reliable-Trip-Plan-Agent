# V0 transport and Nearby acceptance

Date: 2026-09-28, Australia/Sydney. Status: Passed for this bounded implementation check.
Frozen live base: e68d8e6a4297d50a98fcacb3241d392781dec022 plus the source hashes in
logs/v0_transport_nearby_20260928/manifest.json. No extra attempt is authorized.

## Observed result

The single V0 process/application returned exit zero, no outer timeout and no secret
exposure marker. Iteration 2 independently parsed the saved result as PlanningResult
and checked six dated outputs, roles, timing and reference content.

- Main visits by day: 4/3/3/2/3/2, totaling 17.
- Transport activities: 3/2/2/1/2/1, totaling 11 (nine walking, two public transit).
  Each consecutive different venue pair has a named connecting leg. Transport times
  fit between visits without overlaps. Every leg explicitly labels its route and
  duration as model estimates, not live-verified facts.
- All activity provider IDs are null; no application-owned transfers were fabricated.
  Diagnostics count 17 main visits separately from 11 transport activities.
- One optional reference, Markthalle Neun, is associated with October 5 and Kreuzberg
  near the planned Gorlitzer Park visit. It has a contextual reason and explicit
  unverified proximity/availability, no external source ID and no scheduled duplicate.

These observations meet this run's positive transport/Nearby goals. The old V0 output
had 16 activities and no transport/reference items; the new total 28 includes 11
transport activities. This is not 28 sightseeing visits or proof of causal quality
improvement. V1/V2 Nearby behavior remains unchanged.
The original 16 activities were 15 main visits and one generic activity, as confirmed
by the executor's role-aware comparison. All 28 new scheduled costs remain unknown.
The executor's report.md and faithful itinerary.md are saved in the evidence directory;
the final handoff confirmed no retry, code edit, other-version run or commit there.

## Checks and limits

Standards: zero findings. Spec: zero findings. Combined relevant regression: 176 passed
in 11.27s; Ruff passed. Earlier prompt-fixture and launcher-mock issues were test-only,
corrected and retested as documented in the shared output record and plan. No production
fixes were needed after review or live execution.

This is one prompt adherence check, not verified venue access, travel duration,
proximity, cost, enjoyment, a benchmark, or a freeze. V0 has no injected trace or usage
capture. The 10 MB capture change has offline validation; this V0 case does not exercise
V3 trace serialization. The old four-version batch and its separately authorized blind
review remain historical and unchanged.

The user authorized two logical local commits: capture threshold with documentation;
V0 prompt/output-preservation test, revalidation tooling/input and direct documentation.
Exclude unrelated dirty files, secrets, ignored evidence and archives. No push or merge.
