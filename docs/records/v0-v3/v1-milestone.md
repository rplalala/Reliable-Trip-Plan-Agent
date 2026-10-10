# V1 milestone and reopening decisions

These dated checkpoints distinguish accepted historical freezes from later reopening.
They do not freeze current files or extend old validation to later prompts. Current
behavior is in [the design index](../../README.md); detailed development observations
remain in [V1 development](v1-development.md) and [selector experiments](v1-selector-experiments.md).

## Freeze stages and changed responsibility

| Date | Accepted stage | Boundary |
| --- | --- | --- |
| 2026-09-12 | Original V1-A explicitly frozen | Places/Weather/Routes, plain-LLM generation with supplied facts; no reviews, official Web, RAG or general validation/Repair |
| 2026-09-14 | Revised V1-A explicitly re-frozen | Google rating/review enrichment, separate ExperienceProfile and deterministic POI selection; conservative exact identity |
| 2026-09-15 | Complete V1 explicitly frozen | V1-B official/current Web evidence plus graph/planner integration, semantic and cross-country development checks; V2 had not started |
| 2026-09-19 | V1 reopened | B1, then B2, then deterministic planning supply; initial B2 acceptance offline-only, without re-freeze |

The revised V1-A folded former V1-C's review responsibilities into selection. Reddit/
TripAdvisor acquisition was excluded. Rating stayed separate from Profile, and the revised
mask did not request `userRatingCount`; old masks describe their original stage.
V1-B supplemented selected POIs. Phase 1/2 subsystem and Phase 3 planner/graph integration
were separate delivered checkpoints, not an initial capability. Frontend review display
was still unimplemented at those stages.

## Named intent, search capacity and evidence-following observations

Smoke A initially selected Sydney Opera House while the required identity remained
unresolved. Typed named intent/exact Place-ID reconciliation and identical-input live
revalidation resolved one ID, set `must_visit=true` and cleared that conflict.

Initial Smoke B's three-call candidate-search budget omitted six explicit interests.
Revalidation used destination search **1/1**, candidate search **9/12**, executed all nine
supported intents, and retained 123 raw observations / 85 unique IDs. Pools were
`C_raw=36/36`, `R_pool=18/18`, final **16/16**, Profile **6/6**; review evidence changed
one selected membership. Four 4×16 WALK chunks supplied **256 elements**. The revised
V1-A gate passed **507 backend tests** with standalone V0/V1-B compatibility and Ruff.
These checks supported the September 14 re-freeze, not universal evidence-following.

Earlier live fixes normalized Google timezone objects, requested then filtered Weather's
ten-day horizon, and redacted credential-bearing HTTP URLs. Routes evolved from WALK
only through directed alternatives to logical-pair collapse, stable TRANSIT direction
and labelled reverse estimates. Central YAML replaced scattered environment budgets.

Generation exposed wrong route-number attribution and visits before supplied opening.
Prompt corrections required exact pair IDs and full-visit hours, but did not enforce
feasibility deterministically. Sydney still reserved about **15 minutes** against
matching WALK evidence of about **28 minutes**. Places relevance also admitted lodging
and professional-service architecture candidates. No general validation/reselection/
Repair was added to V1.

Web reasoning could truncate structured JSON under `max_output_tokens`, failing that
source safely while others continued. Conservative subject/scope binding and inaccessible
pages retained UNKNOWN. The cause of historical `unsupported_price_field` rejection
was unrecoverable; a later free-admission claim resolved fee 0 without Gate relaxation.
Aliases such as `MCA` were not broadly expanded.

The original complete live flow preceded prompt-only follow-ups; the later **158-pass**
backend regression, Ruff/diff checks did not supply another full live flow. Final
September 15 freeze followed subsequent semantic/cross-country checks rather than being
implied by that earlier Phase 3 result.

## Shared baseline developments after freeze

### Latest accepted boundary - 2026-09-20

V1 quality-first planning had **24 ordinary successes, 24 compared, 12 supplied and
8 scheduled**, with independent Nearby. The [paired V2 checkpoint](v2-milestone.md#earlier-quality-first-pair---2026-09-20)
locates configuration and uncovered live paths; this did not re-freeze either version.

### Later shared first-draft checkpoint - 2026-09-20

The shared extension's failed full-suite and targeted correction remain distinct in the
[dated V2 summary](v2-milestone.md#later-shared-first-draft-checkpoint---2026-09-20).
It did not establish V2 feasibility or a V3 validation benefit at that date.

### Compatible transfer output update (2026-09-25)

V1 participated in optional-transfer compatibility with its independent execution path
preserved. [Shared output/presentation evidence](v1-development.md#compatible-transfer-output-update-2026-09-25)
locates the implementation and checks.

### Shared first-generation mixed transport (current offline checkpoint)

The 2026-09-25 [mixed-transport event](v1-development.md#2026-09-25---shared-first-generation-mixed-transport)
supplied a shared V1/V2/V3 baseline; only V3 added Repair. It was offline-only and did
not extend earlier live acceptance. Current rules belong to the
[transport contract](../../0003-itinerary-transport.md). The
[shared milestone notice](v3-closeout.md#shared-milestone-notice-2026-09-25)
locates Product/version-isolation/recovery boundaries at that date.

## Persistent limitations

Search relevance and selection do not guarantee visitor suitability or scheduling of
non-required POIs. Weather/Routes inform scheduling rather than reselecting places.
TRANSIT is a representative departure-duration estimate, not fare/station/service proof;
a mirrored reverse estimate is not an observed reverse journey. Web facts may remain
UNKNOWN. Development live integration and explicit historical freezes establish neither
statistical reliability nor formal benchmark conclusions.
