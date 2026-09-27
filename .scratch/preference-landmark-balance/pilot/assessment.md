# V3 preference and landmark pilot assessment

Date: 2026-09-28, Australia/Sydney. Base: `cc4d5a0` plus the frozen uncommitted
ticket 03 implementation and pilot adapter. No commit, freeze or formal comparison.
The user authorized preparation and three sequential single attempts through completion.
Iteration 2 owns this assessment; the `smoke tests` conversation owns execution/reporting.

## Evidence and preparation

The private evidence root is `logs/preference_landmark_pilot_20260928/`. Its manifest
hashes the actual dirty source, inputs, runtime and environment files; no credential
values are published. Each case preserves normalized requirements, nomination/resolution
lineage, supply, initial/final itinerary and validation, capture status and independent
trace `budget.json`. See that root's `report.md` for the execution audit and nominee tables.

Prior implementation regression: 1793 passed / 9 skipped. Pilot adapter and existing
acceptance-tool tests: 25 passed. Review found initialization/payload capture isolation,
actual byte accounting and local RAG readiness gaps. These were corrected before the
successful retest and final Standards/Spec reviews. No production change was made during
the live batch. New lineage capture has separate 1 MiB/artifact and 4 MiB/case limits;
the existing capture streams retain their own limits.

## Results

All three authorized cases completed once, sequentially, with exit 0 and complete
mandatory captures. Application elapsed time totals 275.265 seconds; this excludes
between-case review and is not batch wall-clock latency.

| Case | Seconds | Main visits by day | Nominees resolved / qualified / supplied / scheduled | Assessment |
| --- | ---: | --- | --- | --- |
| Sydney ordinary | 89.890 | 3 / 3 / 2 | 10 / 10 / 10 / 7 | Ordinary target 1 exercised; museums 1, architecture 3, gardens 1 supported scheduled matches; all three covered |
| Melbourne focus | 118.296 | 3 / 2 / 2 | 9 / 7 / 2 / 1 | Focus target 2 failed interpretation; architecture unassessed; gardens covered |
| Brisbane short | 67.079 | 3 | 7 / 7 / 7 / 2 | Four ordinary targets retained; gardens covered; historic architecture, museums and zoos unassessed |

Each nomination sent once and returned 12 names; each used four supplementary searches.
Primary candidate searches were 7/8/7 of 12; primary Details were 24/24/16 of 60.
RAG and Repair have separate ledgers and must not be folded into those primary ceilings.
RAG returned partial/partial/empty: Sydney recorded 1 query, 20 positions, 12 Details
and 4 fallback sends; Melbourne 3 queries, 60 positions, 26 Details and 4 fallback sends;
Brisbane 1 query with zero positions, Details or fallback sends. Each used one embedding
send. Semantic calls were 1/2/1 with no correction. Requirement and primary-generation
billed usage are unavailable; reported nomination/semantic usage is not a full cost total.
All three final itineraries equal their initial itineraries, with `repair=null` and
`reason=no_authorized_targets`. Repair effectiveness and nomination-failure fallback
were **not exercised**. Final validation retained respectively 13/9/5 UNKNOWN findings
and no CONFIRMED violations. Access/reservations, verified costs and open semantics
remain unknown; Sydney additionally has three missing structured-hours findings.

Brisbane schedules Old Windmill Observatory, City Botanic Gardens and Queensland Art
Gallery. The explicit maximum-three wording survives in `semantic_5` as an itinerary-style
preference, without an executable count goal. The observed output obeys the maximum,
but this run does not establish validator enforcement of that maximum. Product coverage
explicitly exposes three `unassessed` interests with zero supported scheduled matches;
these must not be relabeled as covered or as three confirmed unmet constraints.

Overall: execution and capture succeeded, but the **complete feature acceptance did
not pass**, because the required focus-target interpretation failed. Sydney provides
limited positive evidence for ordinary preferences coexisting with nominated landmarks.
Brisbane provides limited evidence for bounded output and truthful uncertainty reporting.

## Observed focus interpretation failure

Melbourne input explicitly says `This trip is mainly about museums.` This is also the
accepted specification's example requiring a sourced soft target of two. The actual
`interpreted_requirements.semantic_requirements` instead contains `semantic_1` with
`kind=goal`, `scope=whole_trip`, `experience_goal.trip_scope=themed` and `soft_coverage=null`. The final
Product coverage omits museums entirely. This is an **observed engineering acceptance
failure**, even though the application returned successfully and the itinerary has many
museum visits. Counting more than two museums cannot establish the missing target contract.

The observed selection trace repeatedly selects the museum discovery intent: seven
qualified nominated landmarks become only two supplied nominees and one scheduled nominee.
All seven final visits are museum/gallery-related locations, including Tribute Garden
(Immigration Museum); architecture remains `unassessed`, while gardens is reported covered.
This is a concrete planning concern, not evidence that all destinations behave this way.

Code inspection explains the compatible path: `soft_opportunity_limits` only applies to
eligible soft preferences (individual-POI or selected-set scope, excluding this whole-trip
classification), while acquisition and selection retain existing `themed` /
`exclusive` branches that bypass general exploration. The model's theme classification
therefore bypasses the intended soft saturation behavior. This is a code-supported
diagnosis, not a counterfactual experiment proving the sole cause of every chosen visit.
No fix, prompt tuning, source modification or live rerun was performed.

## Scope of conclusions

These are development pilot observations, not a V0-V3 comparison or a formal benchmark.
Landmark nomination is model knowledge, semantic coverage is model judgment, and neither
proves opening, access or price facts. Successful execution is separate from engineering
acceptance and from travel feasibility. Missing billed usage is not zero expenditure.
Additional fixes or live attempts require a separately agreed scope after this report.
