# Food preference and sparse-day offline diagnosis

## Archival status - 2026-09-28

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

## Acceptance synchronized first

The development record now owns the current three-case wire acceptance, 45-check budget audit,
1727-passed / 9-skipped final combined-tree regression and five local commits. PROJECT and the
index link it. Earlier failures, limited correction evidence and UNKNOWNs remain historical facts.

## Feedback loop and validation

From repository root:

```
.venv\Scripts\python.exe .scratch/food-sparse-diagnosis/replay.py --assert-no-sparse
.venv\Scripts\python.exe .scratch/food-sparse-diagnosis/replay.py
.venv\Scripts\python.exe .scratch/food-sparse-diagnosis/probes.py
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

## Observed facts

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

## Ranked hypotheses and checks

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

## Root cause versus specification

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

## Minimum next proposal and TDD points

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

## Budget comparison and missing evidence

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
