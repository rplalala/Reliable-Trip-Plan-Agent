# Development Pilots

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="berlin-six-day-smoke-assessment"></a>

<a id="berlin-six-day-smoke-assessment--berlin-smoke-assessment"></a>

## Berlin smoke assessment

<a id="berlin-six-day-smoke-assessment--later-itinerary-only-blind-review-authorization-and-result---2026-09-28"></a>

### Later itinerary-only blind review authorization and result - 2026-09-28

After the original evidence-gated stop, the user explicitly instructed `smoke tests`
to evaluate itinerary quality and ignore budget for this blind review. Iteration 2
verified that user message and the executor's saved review/mapping. The executor used
one no-history reviewer with only the common input and four anonymous full itinerary
projections, saving the anonymous response before revealing the mapping.

The reported order A > C > B > D maps to V0 > V3 > V2 > V1. The simulated traveler
favored V0's variety and relaxed pacing; V3 offered richer content but more museums
and cross-district movement; V2's final two days were sparse; V1 repeated venues.
These are the reviewer's judgments, not verified geography, general traveler preferences
or causal conclusions. All costs and venue access remained unverified.

Evidence: `logs/berlin_six_day_20260928/blind_packet.md`, `blind_mapping.json`,
`blind_review.md` and the execution report addendum. The original manifest stays
`stopped_budget_evidence`, with its original `blind_review_eligible=false`; the later
review is separately authorized and does not repair that evidence gap. No rerun occurred.
The reviewed V0 itinerary predates the subsequent transport/Nearby prompt adjustment;
the ranking cannot be attributed to or validate that change. V1 repeats remain an
accepted version limitation, not a current implementation task.

<a id="berlin-six-day-smoke-assessment--subsequent-user-decision---2026-09-28"></a>

### Subsequent user decision - 2026-09-28

The user considers V1 repeats normal for the scope of that intermediate version;
they remain observed output limitations, not a current fix task or a new requirement
for V1. The proposed repeat investigation below is not proceeding.
The user selected a 10 MB (10,000,000-byte) runtime capture threshold instead of the
earlier proposed 8 MB. This configuration-only change is implemented for subsequent
runs; the frozen Berlin artifacts, cap and failed evidence gate are unchanged.
No new live execution or blind assessment was authorized by this adjustment.
Validation: observability, runtime configuration and V3 wiring tests passed (92 tests,
9.68s); `git diff --check` passed. Offline synthetic payloads with 6,041,655 and
9,999,000 data bytes were preserved, while 10,001,000 data bytes triggered truncation;
secret redaction passed in all three cases. No provider was called.

Date: 2026-09-28, Australia/Sydney. Status: Assessed; execution complete, evidence gate
failed. Revision: `e68d8e6a4297d50a98fcacb3241d392781dec022` plus the frozen development
launcher. Documentation-only working changes and older unrelated scratch work remain.
No production change, extra attempt, blind reviewer, commit, or freeze was authorized
or performed during this assessment.

<a id="berlin-six-day-smoke-assessment--verified-observations"></a>

### Verified observations

Iteration 2 checked the executor report against the batch manifest, all four result
files, V1-V3 run/budget records, and V3 original/final validation target counts.
The four independent applications each ran once and exited zero with six nonempty
ordered days. Scheduled activity counts are V0 16, V1 14, V2 14, V3 17.

- V0 policy completion is unassessed by design; successful generation is not policy
  or feasibility validation.
- V1 reports four unauthorized cross-day repeats and one below-target day. It failed
  that output policy despite structural completion. The executor's brief pause was
  corrected by referring to this batch's actual stop conditions; the original V2/V3
  allowance continued without changing the policy, budget, or input.
- V2 reports no repeat-policy failure but two below-target days. V2/V3 RAG ran and
  contributed scheduled places, with partial identity-resolution outcomes. Neither
  contribution nor the four independent stochastic outputs establishes causal benefit.
- V3 changed daily counts from 4/4/3/1/1/1 to 4/4/3/2/2/2 through one accepted Repair
  round. Original validation had three improvement targets; final validation has zero.
  Final findings still include 22 UNKNOWNs: opening 3, visitor suitability 17, budget
  1, semantic requirements 1. This supports targeted shortage repair in this case,
  not fully verified travel feasibility or universal reliability.
- All 61 scheduled cost fields are unknown; the shared EUR 3000 budget is unverified.

<a id="berlin-six-day-smoke-assessment--evidence-gate-and-bounded-diagnosis"></a>

### Evidence gate and bounded diagnosis

V3's standalone `budget.json` is complete, and the recorded counters reported by the
executor stayed within limits. However, `run.json` explicitly records `truncated=true`
and `original_bytes=6041655`. The frozen `trace.max_payload_bytes` was 1000000.
`backend/app/observability/run_trace.py` wraps an oversized serialized payload in a
truncated preview at that threshold. This directly explains the missing full run
record; it is not evidence of application failure or excessive provider spending.

The frozen launcher therefore correctly recorded `stopped_budget_evidence` and
`blind_review_eligible=false`. The state name includes budget evidence because the
gate inspects both run and budget records; the budget summary itself is not truncated.
Do not rename this as a successful batch, reconstruct missing trace content, relax
the gate after observing results, or present a winner. No blind review was performed.
The full final itineraries remain readable in the executor's `itineraries.md`.

<a id="berlin-six-day-smoke-assessment--recommended-next-scope-proposed-not-implemented"></a>

### Recommended next scope (proposed, not implemented)

First address evidence capture offline. Compare a bounded capture-only increase from
1,000,000 to 8,000,000 bytes against reducing duplicated nested run data. The observed
6,041,655-byte record fits the former with headroom, making it a simpler candidate
before adding new trace mechanisms. This changes local serialization/storage limits,
not LLM tokens, API call allowances, or acceptance requirements. Expected API cost
increase is zero; local I/O, memory, and retained diagnostic volume may increase.
It is not a guarantee that all future records fit, nor permission to enable raw data.

Any approved implementation should use offline synthetic payloads around both limits,
preserve truncation and secret-redaction behavior, and keep the hard cap. Reject or
revert the increase if it causes unacceptable local resource use or capture safety
regression. Do not silently change this frozen batch or use a new cap to claim the
missing old trace was captured. A new live attempt requires a separate bounded scope.

Separately, investigate V1's repeat-policy failure offline with the saved request,
supply and output before proposing changes. V0/V1/V2 version boundaries remain intact;
do not add V3 validation/Repair to earlier versions just to make this case pass.

<a id="berlin-six-day-smoke-assessment--evidence"></a>

### Evidence

- `logs/berlin_six_day_20260928/report.md`: execution process, budgets and limitations.
- `logs/berlin_six_day_20260928/manifest.json`: attempts, freeze and failed evidence gate.
- `logs/berlin_six_day_20260928/v*/result.json`: saved outputs and available diagnostics.
- `logs/berlin_six_day_20260928/itineraries.md`: faithful user-readable projections.

This is development smoke assessment, not a formal benchmark or thesis conclusion.

<a id="food-sparse-diagnosis-diagnosis"></a>

<a id="food-sparse-diagnosis-diagnosis--food-preference-and-sparse-day-offline-diagnosis"></a>

## Food preference and sparse-day offline diagnosis

<a id="food-sparse-diagnosis-diagnosis--archival-status---2026-09-28"></a>

### Archival status - 2026-09-28

The user deferred this investigation after the checkpoint below; it is not an active
implementation task. This record and its scripts describe the 8f5e9b3 contracts and
saved local evidence. Do not treat the historical commands as current-policy validation.
Workspace cleanup only normalized script formatting and preserved the generated replay
output at `logs/food_sparse_diagnosis_20260927/replay-result.json` (ignored local evidence).
The historical data was not regenerated or rewritten under newer policy. The user's
2026-09-28 workspace-wide commit authorization permits archiving these source records;
the older no-commit/no-implementation statement below records its original authorization.

Date: 2026-09-27. Status: Diagnosed; improvement options Proposed, not implemented.
Base revision: `8f5e9b3`; this task changes documentation and local diagnostic artifacts only.
User authorization: update acceptance documents, then diagnose offline. No production edits,
network calls, budget adjustments, commits or new smoke execution.

<a id="food-sparse-diagnosis-diagnosis--acceptance-synchronized-first"></a>

### Acceptance synchronized first

The development record now owns the current three-case wire acceptance, 45-check budget audit,
1727-passed / 9-skipped final combined-tree regression and five local commits. PROJECT and the
index link it. Earlier failures, limited correction evidence and UNKNOWNs remain historical facts.

<a id="food-sparse-diagnosis-diagnosis--feedback-loop-and-validation"></a>

### Feedback loop and validation

From repository root:

```
.venv\Scripts\python.exe tools/validation/packets/food-sparse-diagnosis/replay.py --assert-no-sparse
.venv\Scripts\python.exe tools/validation/packets/food-sparse-diagnosis/replay.py
.venv\Scripts\python.exe tools/validation/packets/food-sparse-diagnosis/probes.py
.venv\Scripts\python.exe -m pytest backend/tests/policies/test_generation_diagnostics.py backend/tests/services/test_planning_supply_pipeline.py -q
```

The first command exited 1 on the observed four-day target gap. It is an explicit quality
observation assertion, NOT a claim that every day must meet a hard quota. Typed saved outputs
are passed through actual `observe_generation`; current counts must equal captured counts.
The ordinary replay succeeded and saved `replay-result.json` (now retained at the local
path above); it does not invoke an LLM or
reproduce a stochastic generation decision. The minimal one-date/one-activity probe reproduced
count 1; adding a generic activity left 1; adding a distinct main identity yielded 2. Those
counterfactuals test counting only, with no assertion of temporal/route feasibility. The 12
existing diagnostics/supply-pipeline tests passed. No production fix was applied, so there is
no red-to-green claim for the observed quality gap. Phases involving a fix are deferred under
the user's diagnosis-only authorization.

<a id="food-sparse-diagnosis-diagnosis--observed-facts"></a>

### Observed facts

| Case | Main counts | Eligible / selected | Scheduled IDs / unused selected | Food-supported semantic candidates | Generic food activities |
| --- | --- | --- | --- | --- | --- |
| Sydney V1 | 2/2/2/2/1 | 21 / 16 | 9 / 7 | 10, all non_main | 0 |
| Melbourne V1 | 2/2/1/2/1/1/2/2 | 19 / 16 | 13 / 3 | 11, all non_main | 2 |
| Sydney V3 | 2/3/3/2/3 | 27 / 16 | 13 / 3 | 12, all non_main | 1 |

Food mappings are manually identified from each captured normalized requirement, not a proposed
runtime keyword classifier: Sydney semantic_3; Melbourne semantic_2. All are sourced medium
favor preferences, category/continuing, no explicit primary exception. Relaxed pace is retained.
Food discovery intents exist. All supported food candidates are absent from selected and
scheduled IDs. Each saved selected-place evidence artifact has 16 rows. Generic food notes
explicitly say that specific venues/prices are not established in supplied planning evidence.

Sparse dates: Sydney October 2; Melbourne September 30, October 2 and October 3. Their lone
main visits occupy 2h, 1.5h, 1.25h and 1.5h respectively; Melbourne October 2 also contains a
1h generic meal. There are no empty dates. `policy_completion=complete`, goal_progress empty.

Unused Sydney attractions: Martin Place amphitheatre, Hermitage Foreshore Walk, Sydney Tower
Eye, Shelly Beach Walking Track, Cremorne Reserve, Cremorne Point Garden And Walk, The Coast
Track. Unused Melbourne attractions: Docklands Sunset Point, Galatea Point, Webb Trail.
Their existence disproves a raw selected-count shortage; it does not prove compatibility with
any specific sparse date. No candidate-specific insertion feasibility replay was performed.

<a id="food-sparse-diagnosis-diagnosis--ranked-hypotheses-and-checks"></a>

### Ranked hypotheses and checks

1. Role-policy exclusion blocks named food choices. Prediction: supported food judgments exist,
   but are non_main, excluded before primary selection/projection. Confirmed by capture and code.
2. Generation chooses a sparse subset despite available main supply, potentially due to pace
   or evidence constraints. Prediction: K is full and unused selected candidates exist, while
   counts remain sparse. Confirmed observation; the model's causal rationale is NOT established.
3. Completion/Review covers narrower obligations than every preference and default count.
   Prediction: continuing goals are omitted from goal_progress and 1-main days satisfy minimum
   coverage; V1 does not run Repair. Confirmed by actual diagnostic replay and policy code.
4. Interpretation loss or exhausted acquisition is the primary cause. Prediction: food missing
   from normalized requirements or no adequate selected capacity. Contradicted for loss and
   raw count capacity. Specific date/route/opening limitations remain possible.

<a id="food-sparse-diagnosis-diagnosis--root-cause-versus-specification"></a>

### Root cause versus specification

Food's deterministic path is supported match -> non_main -> excluded primary candidate -> no
named food venue in generator supply. `POISemanticAssessment.main_eligible` accepts attractions
and authorized exceptions only; `PlanningSupplyPipeline._select` applies that gate and exports
only selected judgments. `planner_supply_projection` still passes semantic preferences, so the
model can respond with generic activities, but ordinary food support has no named scheduled
support path. Prompt 5 explicitly forbids turning continuing food interest into a main exception.
This is a capability/design limitation under the existing contract, not a bad evidence-reference
mapping, failed API, lost input, or demonstrated selector implementation error.

Sparse output originates in the generator's chosen itinerary, not diagnostic undercounting:
generic meals correctly do not inflate main counts. The shared generation policy targets 2-5
normally while respecting pace, rest and evidence; V1 remains single generation + diagnostics.
`goal_progress` deliberately skips continuing preferences. `policy_completion` covers primary
roles, multiplicity and minimum coverage, not every soft preference or the 2-5 target. Sydney V3
repaired its own single coverage target; that is not a controlled comparison with Sydney V1.

Relevant sources: `backend/app/services/planning_supply_pipeline.py`,
`backend/app/schemas/poi_semantics.py`, `backend/app/services/poi_semantics_prompts.py`,
`backend/app/versions/v1/prompts.py`, `backend/app/policies/generation_policy.py`,
`backend/app/policies/generation_diagnostics.py`, `backend/app/policies/poi_semantic_output.py`;
contracts: `docs/shared_poi_semantics_plan.md`, `docs/shared_itinerary_output.md`.

<a id="food-sparse-diagnosis-diagnosis--minimum-next-proposal-and-tdd-points"></a>

### Minimum next proposal and TDD points

No mandatory production correction is justified solely by these samples. Prefer a small shared
first-generation guidance/projection improvement, subject to a new approved Spec:

- Expose uncovered continuing preference evidence as a factual limitation, without counting it
  as a mandatory visit, declaring it satisfied, or conflating it with policy_completion.
- Clarify that an expressed food interest may receive a transparent generic self-directed stop
  when named support is unavailable; it remains optional, does not count toward main coverage,
  and must not invent venues, prices or proof of fulfillment.
- Ask the existing first generation to consider unused eligible candidates across sparse dates
  and state supported reasons for shortfalls. Keep relaxed pace and feasibility authoritative.
  No extra model call, automatic V1 Repair, case/date hardcoding or new restaurant exception.

This can improve transparency and model guidance, not guarantee richer output. If the product
requires evidence-linked named restaurants, define a separate non-main support role/ledger and
its routing, costs and output semantics first; simply admitting restaurants as main POIs would
violate the current rule. That larger option is not implementation-authorized here.

TDD for an approved small change: use synthetic mixed-interest contracts (not city strings) to
verify supported-but-ineligible food remains excluded and its limitation survives projection;
continuing preferences never become mandatory counts; generic stops cannot clear quantity or
claim verified food fulfillment; supplied unused candidates and explicit pace/uncertainty reach
the prompt; V0-V3 keep their existing independent execution and V1/V2 gain no Repair call.
Offline contract tests cannot prove the new prompt improves actual stochastic selection.

<a id="food-sparse-diagnosis-diagnosis--budget-comparison-and-missing-evidence"></a>

### Budget comparison and missing evidence

Keep current budgets. Existing V1 Details were 32/60; final K=16 was full and left 7/3 unused
candidates. Raising Details or K has no demonstrated benefit to these observed omissions and
adds potential latency/cost. Adding another generation call or V1 Repair would also expand
version behavior without isolating the issue. A later date-specific compatibility check could
show an actual usable-supply bottleneck; only then compare a measured budget increase.

Missing: a controlled prompt replay against the model (not authorized), exact causal rationale
for each omitted candidate, and per-date insertion feasibility for unused supply. Generic food
stops are not verified venues; all 38 activity costs remain null. No formal benchmark, comparative
quality result, automatic version freeze or budget compliance claim beyond recorded evidence.

Evidence: `logs/semantic_short_reference_revalidation_20260927/{sydney_v1,melbourne_v1,sydney_v3}/result.json`,
selected-place evidence in each trace, the original report and runtime configuration. The
original capture files are not modified; local replay output contains only selected diagnostics.

<a id="v0-transport-nearby-assessment"></a>

<a id="v0-transport-nearby-assessment--v0-transport-and-nearby-acceptance"></a>

## V0 transport and Nearby acceptance

Date: 2026-09-28, Australia/Sydney. Status: Passed for this bounded implementation check.
Frozen live base: e68d8e6a4297d50a98fcacb3241d392781dec022 plus the source hashes in
logs/v0_transport_nearby_20260928/manifest.json. No extra attempt is authorized.

<a id="v0-transport-nearby-assessment--observed-result"></a>

### Observed result

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

<a id="v0-transport-nearby-assessment--checks-and-limits"></a>

### Checks and limits

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

### Preparation validation chronology

Standards review: zero findings. Spec review: zero findings. Relevant combined tests:
176 passed in 11.27s, including observability/config/V3 wiring, V0, V1 references, V2,
Nearby/output roles/DTOs and the four launcher gates. Ruff passed. The first launcher
test run accidentally intercepted its Git HEAD subprocess with the fake planning
process; the test fixture was corrected to supply a fixed offline HEAD. All four
launcher tests then passed, followed by the combined selection. No production fix
or live retry resulted from this test-only correction. Preparation and a separate
preflight check passed without external requests.

Historical execution specification: [Issue #39](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/39).
