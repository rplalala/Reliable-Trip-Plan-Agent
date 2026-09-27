# Iteration 2 assessment: Paris six-day development smoke

Date: 2026-09-27 (Australia/Sydney). Code revision:
`8f5e9b3cdb60c4c7f3fbb55f68ebb8a24dd7ac86` on `feature/v3`.
The initial working tree had uncommitted `PROJECT.md`, `docs/README.md`,
`docs/development_record.md`, `docs/known_issues.md`, and local
`.scratch/food-sparse-diagnosis/` and `.scratch/iteration2-handoff/` records.
This smoke added only local plan/evidence/assessment files; it changed no
production code or configuration. Status: bounded development validation,
not a formal benchmark, global quality validation, or version freeze.

## Assessment

The authorized four-case batch met its structural execution objective:
one attempt per independent V0–V3 entry point, process and application exit 0,
all six requested dates present, no outer timeout, and no recorded primary-tool
limit overrun. V1/V3 requirement and semantic captures are complete; V2/V3 RAG
participated and reported complete. V3 validation ran and found no authorized
improvement target, so `repair=null`. This batch does not verify the live Repair
path. See `logs/paris_six_day_20260927/report.md` for the exact sequence,
counts, capture status and evidence locations.

The isolated itinerary-only reviewer, using no project or version context,
ranked anonymous C > B > A > D; the post-review mapping is C=V0, B=V1,
A=V2, D=V3. The stated preference for V0 was its major Paris landmark and
museum coverage with two stops per day. This is one qualitative judgment on
visible stop lists. It cannot establish which version is more reliable or
attribute differences to tools, RAG, validation, or Repair. Addresses, source
evidence, route diagnostics and validation findings were deliberately absent
from the blind input.

Selected-place evidence localizes a visible part of the landmark gap: the
final V1/V2/V3 selected sets contain neither Louvre Museum nor Musée d'Orsay.
V3 selected Louvre Pyramid but did not schedule it; that place is not the
museum. The selected sets have 16 identities each; V1 scheduled all 16 and
V2/V3 scheduled 15 each. Earlier candidate-pool membership, rejection causes,
date feasibility and model choice rationale were not established by this
assessment. Broad enjoyment wording imposed no named-place requirement, so
these omissions do not by themselves prove a hard Spec violation. V3's
`policy_completion=complete` covers its defined counted/role/coverage contract,
not city-icon coverage or factual feasibility.

All 58 scheduled activities have `estimated_cost=null`. The EUR 3000 whole-trip
budget therefore remains unverified; an unknown value is not a zero cost or a
budget PASS. V3 retained visitor-suitability UNKNOWN 15, opening UNKNOWN 2,
budget UNKNOWN 1 and semantic-requirements UNKNOWN 1. No hard date or
structured-output failure was observed. The vague preference, missing
date-specific operating evidence, unknown travel cost, and one-case sample
prevent a general travel-quality conclusion.

## Boundary and follow-up

The task is complete as a bounded live smoke and requested blind review.
There is no evidence-backed mandatory production correction from this batch.
If the user wants to investigate the landmark coverage difference, first
inspect saved acquisition/selection evidence offline to distinguish discovery,
admission, selection and generation decisions before proposing a general
change. Do not tune specifically for Paris or silently change version policy.
Any new live run, implementation, budget adjustment, formal evaluation or
commit needs its own authorization.

Evidence: `logs/paris_six_day_20260927/{request.json,manifest.json,report.md,
itineraries.md,blind_input.md}`; each `v*/result.json` and `execution.json`;
V1/V3 normalized captures and V1–V3 traces/budget summaries. Governing
scope: `.scratch/paris-six-day-smoke/spec.md`.
