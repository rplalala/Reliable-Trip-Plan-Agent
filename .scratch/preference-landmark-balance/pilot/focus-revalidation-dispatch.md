# Authorized Melbourne V3 focus revalidation

Date: 2026-09-28 Australia/Sydney. The user explicitly approved one bounded Melbourne
V3 live revalidation after the focus convergence implementation. Iteration 2 owns this
plan/tooling/assessment; the existing smoke tests conversation executes and reports only.

## Frozen scope

Exactly one fresh-process attempt of `focus_melbourne_v3.json` in this directory: original
Melbourne Oct3-5, two travelers, AUD1800, unchanged preference text. Use the real Sydney
date, never backdate; stop if dates are invalid. Current code is cc4d5a0 plus uncommitted
ticket03, focus correction and tooling. Production full regression1807 passed/9 skipped;
follow-up launcher/capture tests11 passed, Ruff passed. Initial launcher test failed because
its process stub also intercepted Git; the test stub was corrected and retested offline.

The original plan.md's per-case budgets, exclusions, evidence and stop rules apply unchanged:
600s application/660s outer; one interpretation, one nomination (12 names/20s), one primary
generation; candidate searches12 including supplements4, primary Details60; semantic6 calls/
120s shared with Repair; initial RAG4 queries/80 positions/30 Details/4 fallback; Repair at
most5 rounds/calls with existing360s stage inside the same600s request. Existing runtime
route/weather/Nearby and all other limits remain authoritative. No increases, retries,
connectivity probes, extra cases, new soft-gap Repair triggers or production edits.

Preparation is complete at logs/focus_revalidation_20260928/manifest.json, with current
source/input/runtime/environment-file hashes. Do not prepare again or modify hashed files.
The adapter reuses existing normalized bounded captures and one-shot/deadline guards; its
child module preserves the single-case configuration. Old exhausted pilot artifacts stay intact.

## Execute once from repository root

Use authorized network access from the outset, escalating for the live process if necessary.
Do not test connectivity first. Do not call child directly or reset markers.

```powershell
.venv/Scripts/python.exe -B -m tools.validation.focus_revalidation execute --case focus_melbourne_v3
```

Stop and report any terminal failure, capture loss, source drift, budget breach or confirmed
identity/restriction violation. A failed attempt is consumed. Do not repair or rerun.

## Assess and return

The key acceptance is a sourced museum soft target2 (not goal/themed/null), architecture
and gardens ordinary target1, no inferred ratio/large count, independent landmarks retaining
candidate opportunity after saturation. Count supported final distinct POIs, not candidates.
Targets are not category maxima; additional same-category landmarks are permitted. A soft
gap or UNKNOWN alone is not a hard failure. Record nominated/resolved/qualified/supplied/
initially/finally scheduled IDs, actual stage budgets, timing, available usage and missing
usage. Compare initial/final and any recorded Repair actions; don't infer repair efficacy
if skipped. Historical Melbourne is context, not a controlled causal comparison.

Write English report.md, lineage.csv and final_itinerary.md (Markdown dates/times/places,
preserve original notes and uncertainty) under logs/focus_revalidation_20260928/. Send a
Chinese handoff with facts, failures, missing evidence and paths to iteration2 thread
01a0e29d-405e-7d82-b894-d95eb7f67632. No commit, production change or further live call.
