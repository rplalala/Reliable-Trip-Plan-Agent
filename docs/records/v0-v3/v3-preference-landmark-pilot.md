# Preference Landmark Pilot

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="preference-landmark-balance-pilot-assessment"></a>

<a id="preference-landmark-balance-pilot-assessment--v3-preference-and-landmark-pilot-assessment"></a>

## V3 preference and landmark pilot assessment

Date: 2026-09-28, Australia/Sydney. Base: `cc4d5a0` plus the frozen uncommitted
ticket 03 implementation and pilot adapter. No commit, freeze or formal comparison.
The user authorized preparation and three sequential single attempts through completion.
Iteration 2 owns this assessment; the `smoke tests` conversation owns execution/reporting.

<a id="preference-landmark-balance-pilot-assessment--evidence-and-preparation"></a>

### Evidence and preparation

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

<a id="preference-landmark-balance-pilot-assessment--results"></a>

### Results

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

<a id="preference-landmark-balance-pilot-assessment--observed-focus-interpretation-failure"></a>

### Observed focus interpretation failure

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

<a id="preference-landmark-balance-pilot-assessment--scope-of-conclusions"></a>

### Scope of conclusions

These are development pilot observations, not a V0-V3 comparison or a formal benchmark.
Landmark nomination is model knowledge, semantic coverage is model judgment, and neither
proves opening, access or price facts. Successful execution is separate from engineering
acceptance and from travel feasibility. Missing billed usage is not zero expenditure.
Additional fixes or live attempts require a separately agreed scope after this report.

<a id="preference-landmark-balance-pilot-focus-revalidation-assessment"></a>

<a id="preference-landmark-balance-pilot-focus-revalidation-assessment--melbourne-v3-focus-revalidation-assessment"></a>

## Melbourne V3 focus revalidation assessment

Date: 2026-09-28 Australia/Sydney. Status: bounded case engineering acceptance passed;
not a general quality claim or freeze. Base cc4d5a0 plus frozen uncommitted ticket03,
focus convergence and follow-up tooling. User authorized exactly one new attempt, using
the unchanged original Melbourne input and existing budgets. No retry or production edit.

<a id="preference-landmark-balance-pilot-focus-revalidation-assessment--observed-outcome"></a>

### Observed outcome

Application exit0 in99.781 seconds; no outer timeout. Requirement, semantic, Repair-path,
lineage and trace capture completed with no recorded errors. The interpreted museum
requirement uses selected_poi_set scope and soft target2/current_trip_focus, grounded in
the exact original quote `This trip is mainly about museums.` (offsets0..34). Architecture
and gardens have ordinary target1. Final Product coverage reports museums2/2,
architecture2/1 and gardens1/1, all covered through supported distinct scheduled matches.
Variety/comfortable pace remain uncounted itinerary-style requirements.

Nomination returned12 names in one3.235s call;8 resolved,8 qualified,8 supplied,6 scheduled.
Four supplements reached their own cap while primary candidate searches were7/12; primary
Details24/60. Primary supply contained12 POIs. Additional same-category visits are allowed
for independent value; target2 is not a maximum. Final main visits total8, daily3/3/2:

- Oct3: Melbourne Museum; Hellenic Museum; Melbourne Laneways & Arcades Self-Guided Walking Tour.
- Oct4: National Gallery of Victoria; Shrine of Remembrance; Royal Botanic Gardens Victoria - Melbourne Gardens.
- Oct5: Royal Exhibition Building; Melbourne Skydeck.

The six scheduled nominees are Melbourne Museum, NGV, Shrine of Remembrance, Royal Botanic
Gardens, Royal Exhibition Building and Melbourne Skydeck. This supplies bounded evidence
that focused preference coverage can coexist with independent nominated landmarks. The
different outcome from the earlier run is descriptive, not a controlled causal comparison.

<a id="preference-landmark-balance-pilot-focus-revalidation-assessment--budgets-validation-and-limitations"></a>

### Budgets, validation and limitations

No recorded primary used/limit exceeded its limit. Semantics used one call. Initial RAG
used one embedding, one query,20 returned positions,8 Details and4 fallback sends; these
are separate from primary acquisition counters. Nearby sent3 requests. Nomination reported
225 input/293 output tokens; full requirement/generation billed usage remains unavailable.
Application/outer600/660s bounds were respected. No monetary cost total is inferred.

Initial and final itineraries are equal; reason=no_authorized_targets and repair=null.
No Repair action or post-edit revalidation was exercised. Final findings have no confirmed
violations and11 UNKNOWNs:8 access/reservation/special-area,1 structured-hours missing,
1 budget,1 open semantics. Route PASS and covered preferences do not certify admission,
prices, operational access or overall feasibility. No universal focus-classification or
landmark-quality reliability is established by a single sample.

<a id="preference-landmark-balance-pilot-focus-revalidation-assessment--evidence-and-preparation-checks"></a>

### Evidence and preparation checks

Evidence root: logs/focus_revalidation_20260928/; manifest captures current dirty source,
runtime and input hashes. The smoke execution report,12-row lineage.csv and Markdown
final_itinerary.md supplement per-case result/Product and independent budget artifacts.
The prior three-case pilot remains unchanged. The follow-up launcher has a separate
single-case output and child entry; its test initially intercepted Git with a process
stub, then passed after test-only correction. Launcher/capture suite11 passed, Ruff passed;
prior full production suite1807 passed/9 skipped. No commit or new version freeze.
