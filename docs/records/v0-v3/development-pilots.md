# Development Pilots

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

## Berlin six-day smoke assessment — 2026-09-28

The four independent applications each ran once at revision
`e68d8e6a4297d50a98fcacb3241d392781dec022` with the frozen development launcher.
All exited zero with six ordered, nonempty days, but the batch's evidence gate failed.

| Version | Scheduled activities | Observed boundary |
| --- | ---: | --- |
| V0 | 16 | Policy completion unassessed; generation success does not verify feasibility. |
| V1 | 14 | Four unauthorized cross-day repeats and one below-target day. |
| V2 | 14 | No repeat-policy failure; two below-target days. |
| V3 | 17 | One accepted Repair changed counts from 4/4/3/1/1/1 to 4/4/3/2/2/2 and improvement targets from three to zero. |

V2/V3 RAG contributed scheduled places with partial identity resolution. This is not
causal evidence of benefit. V3 retained 22 UNKNOWNs: opening 3, visitor suitability
17, budget 1 and semantic requirements 1. All 61 scheduled costs were unknown;
the shared EUR 3000 budget remained unverified.

V3's standalone `budget.json` was complete and its recorded counters stayed within
limits. Its `run.json` recorded `truncated=true`, `original_bytes=6041655` against
the frozen 1,000,000-byte trace cap. The oversized-payload preview explains the
missing full trace, not application failure or excessive spending. The manifest's
`stopped_budget_evidence` and `blind_review_eligible=false` remain unchanged.

The assessment proposed an 8 MB capture cap and an offline V1 repeat investigation.
The user instead selected 10 MB (10,000,000 bytes) for subsequent runs and declined
repeat investigation: repeats remain an intermediate-version limitation. Offline
validation passed 92 tests in 9.68 seconds. Synthetic 6,041,655- and 9,999,000-byte payloads
were preserved; 10,001,000 bytes triggered truncation, with redaction passing in
all three cases. This did not recover the frozen trace or authorize a retry.

A later, separately authorized itinerary-only blind review ignored budget. One
reviewer without history saw the common input and four anonymous full itinerary
projections before the mapping was revealed. A > C > B > D mapped to V0 > V3 > V2 >
V1: the simulated traveler favored V0's variety/pacing, found V3 richer but more
museum-heavy and dispersed, V2 sparse late in the trip, and V1 repetitive. These
are reviewer judgments, not verified geography or general traveler preferences.
The original failed evidence gate was not repaired. The reviewed V0 predates its
subsequent transport/Nearby change, which this ranking cannot validate.

Evidence identifiers: `logs/berlin_six_day_20260928/{report.md,manifest.json,itineraries.md}`,
`v*/result.json`, `blind_packet.md`, `blind_mapping.json` and `blind_review.md`.
The published observations above do not depend on access to those private files.
This was development smoke evidence, not a formal benchmark or thesis conclusion.

## Food preference and sparse-day offline diagnosis

### Scope and replay

Diagnosed on 2026-09-27 at `8f5e9b3`; improvement options remained Proposed and
were deferred on September 28. No production fix or stochastic regeneration was
performed. Saved outputs were replayed through the actual `observe_generation`.
The explicit `--assert-no-sparse` observation failed on four below-target dates;
this was not a hard-quota assertion or evidence of an implementation regression.
Ordinary replay matched captured counts. A one-date probe counted one main identity,
remained one after adding a generic activity, and became two after a distinct main
identity. These counting counterfactuals establish no route/time feasibility.
Twelve existing diagnostics/supply tests passed; there is no red-to-green quality claim.

Replay source: `tools/validation/packets/food-sparse-diagnosis/{replay.py,probes.py}`.
Its output, `logs/food_sparse_diagnosis_20260927/replay-result.json`, describes the
historical contracts, not validation under subsequent policy.

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
current contract navigation:
[requirements/evidence](../../0002-requirements-evidence.md) and
[itinerary/transport](../../0003-itinerary-transport.md).

### Deferred improvement options

No mandatory fix was justified by these samples. The proposed minimum was shared
first-generation guidance exposing unsupported continuing preferences and asking
for supported reasons for sparse output. Generic food stops would remain optional,
unverified and outside primary coverage; V1/V2 would gain no Repair. Evidence-backed
named restaurants would need a separate non-main support role/ledger rather than
admission as primary attractions. These options were deferred, not implemented or
shown to improve stochastic generation. Offline tests could verify retained
permissions and projection, but not live efficacy.

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

## V0 transport and Nearby acceptance

Date: 2026-09-28, Australia/Sydney. Status: Passed for this bounded implementation check.
Frozen live base: e68d8e6a4297d50a98fcacb3241d392781dec022 plus the source hashes in
logs/v0_transport_nearby_20260928/manifest.json. No extra attempt is authorized.

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
no live retry or other-version run followed.

### Checks and limits

This is one prompt adherence check, not verified venue access, travel duration,
proximity, cost, enjoyment, a benchmark, or a freeze. V0 has no injected trace or usage
capture. The 10 MB capture change has offline validation; this V0 case does not exercise
V3 trace serialization. The old four-version batch and its separately authorized blind
review remain historical and unchanged.

Preparation validation passed 176 combined tests in 11.27 seconds, covering
observability/config/V3 wiring, V0, V1 references, V2, Nearby/roles/DTOs and four
launcher gates; Ruff and both independent reviews passed. These are preparation
checks, distinct from this one live prompt-adherence observation.

Historical execution specification: [Issue #39](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/39).

<a id="sydney-v0-generation-smoke-2026-10-07"></a>

## Sydney V0 generation smoke stop - 2026-10-07

Date: 2026-10-07, Australia/Sydney. Outcome: stopped, not passed. Source revision:
`c2750d57b7b2f8e8c3ee6641bb7cd81edf3755c9`. Production code was unchanged; an
ignored one-use execution helper applied transport/token limits to the existing V0
runner.
The user authorized prepared smoke execution without another approval. The parent
prepared and assessed this run; a current-session execution child used
`gpt-6.1-sol` with `medium` effort and executed only the frozen handoff.

The source input is the existing four-day Sydney request (October 14-17, two
travelers, AUD 1600, required Sydney Opera House). The generation-only plan allowed
at most two Responses POSTs, zero retries, 32,000 input tokens per send, 8,192 output
tokens per send, 120 seconds per HTTP request and 250 seconds total. The input
surrogate counted the entire SDK JSON body plus a 2,048-token reserve; the first
body measured 9,851 tokens before that reserve. Offline interception captured the
actual SDK body before dispatch. Seven guard cases passed: valid wire, rejected
model mismatch, missing output cap, streaming, tools, priority tier and exceeded
send count. The private worst-case retail references were USD 0.016192 standard
and USD 0.01781120 regional, below the USD 0.020000 reference allowance. These
references did not guarantee a Foundry invoice ceiling or authorize API acquisition.

Execution made exactly one POST, with HTTP 200 and provider status `completed`,
using `gpt-6-luna`. The request did not explicitly set reasoning effort; the original
response reports `medium`. Elapsed time was 24.860 seconds. The unchanged runner
then raised `ClarificationRequired`; the itinerary node was never invoked. There
was no retry, fallback, output repair, other-version run or independent API call.

Offline replay of the saved domain draft through `interpret_preferences`, with
DNS/socket connections blocked, reproduces code `unsupported_hard_requirements`
for `semantic_1`. Its text is `Plan exactly two primary sightseeing visits per day.`
with strength `hard`, scope `itinerary_style`, capability `semantic_only`, result
`unknown` and disposition `clarify`. The exact quote is grounded in the original
input. Shared requirements policy currently has no registered predicate to certify
this daily cardinality. The required Opera House visit is represented separately
as an executable named visit obligation. This stop is consistent with the current
[shared requirements boundary](../../0002-requirements-evidence.md#input-gate-and-provenance-contract);
it is not a route timeout or an independent evaluator verdict. The same shared
hard-semantic gate precedes V1-V3 generation; those versions were not run here.

Reported usage: 9,074 input tokens (3 ordinary, 9,071 cache-write, 0 cached), 3,349
output tokens, 12,423 total. The 1,915 reasoning tokens are included in output.
Using the frozen [official Luna retail reference](https://developers.openai.com/api/docs/models/gpt-6-luna),
rates per million were USD 0.10 ordinary input, 0.125 cache-write, 0.01 cached input
and 0.50 output. Recomputed standard reference is USD 0.002808675; regional +10%
is USD 0.00308954250. The executor's preliminary references, USD 0.00280875 and
0.003089625, were corrected by this explicit partition calculation. Actual Azure/
Foundry billing remains unknown; these are not observed invoice charges.

Evidence identifiers (private historical paths, not published dependencies):
`artifacts/sydney-v0-generation-smoke-20261007/{plan.json,first-wire.json,assessment.json}`
and `execution/{execution.json,request-1.json,response-1.bin,capture/}`. Original raw
response SHA256: `cdc2e2b18bd7312a011cf8c121ed6971b4602d2ec1f24dc4b62b7ec4f64266b5`.
The assessment verified all 206 frozen source/input files, the helper/first-wire/input
hashes, 146 protected original files and seven earlier frozen Sydney preparation
files. Neither offline replay nor assessment changed the original receipts or provider bytes.

No `result.json`, accepted itinerary, identity snapshot, route evidence, final score
or four-version acceptance result exists. No production fix was made; the prior
3,017-pass/10-skip backend gate belongs to the unchanged tool-boundary implementation,
not this live result. The consumed execution directory remains one-use. The parent's
initial suggestion to soften the daily count or add hard-count support was superseded
by the user's boundary clarification below; it grants no implementation authority.

### User clarification: density scoring is not a generation quota

The user subsequently clarified that no exact daily count was requested for V0-V2.
The parent had added `exactly two primary sightseeing visits per day` to the smoke
input. This confounded natural planning requirements with a count favored by the
independent scoring table. The model faithfully extracting that hard wording does
not justify a shared-input feature fix or reinterpret it as the user's requirement.
The preparation error is separate from the observed, contract-consistent gate stop.

The correction removed the added daily count from the separately prepared natural
input below, keeping the relaxed-pace preference without a suggested count. The
consumed counted input, response and receipt were preserved; evaluator scores were
not used to select a replacement output. The clarification itself involved no new
input execution or paid call.

Current code already shares a soft first-generation target of 2-5 main POIs; it is
explicitly not an unconditional quota or hard user requirement. V3 alone has internal
quantity validation/repair (`quantity_review_enabled: true` in current runtime
configuration, with a 2-5 reference range and applicability/permission checks).
Independent evaluator density deductions remain post-output scoring. This correction
changes neither those existing policies nor score formulas and does not establish
an uncontaminated benchmark or authorize formal comparison.

<a id="sydney-v0-natural-generation-smoke-2026-10-07"></a>

## Sydney V0 natural-input generation smoke - 2026-10-07

Date: 2026-10-07, Australia/Sydney. Generation completed; independent evaluator
acceptance had not yet occurred at this checkpoint. The user approved the corrected
preparation/execution after clarifying that daily density scoring must not supply
generation quotas. Input preparation commit: `3ae6a070ae6ab7134906720e4ff1be6cb2c7214b`.
Only the new [natural request](../../../tools/validation/packets/sydney-v0-route-smoke/request-natural.json)
and evaluator usage documentation changed at that revision. Production V0-V3,
prompts, shared requirements policy, Repair and score formulas were unchanged.

The new input removes only `with exactly two primary sightseeing visits per day`
from the earlier preference text. Four days, dates October 14-17, two travelers,
AUD 1600, relaxed pace, required Sydney Opera House once, natural interests and
walking/public-transport preferences remain identical. No suggested daily count
replaces the deleted condition. The old counted input and all original stop evidence
remain unchanged; this is a separately approved case, not a retry or repaired result.

### Offline preparation and execution boundary

Schema and current trusted-day validation passed against October 7. Exact input
comparison confirmed only the unwanted daily hint was removed. The parent captured
the actual SDK body using MockTransport and stopped before HTTP dispatch. Eight
guard cases passed: valid body and rejection of model mismatch, streaming, tools,
priority tier, missing output cap, exceeded send count and exceeded input bound.
The first JSON-body surrogate was 9,843 tokens; with the 2,048 reserve it was 11,891.
All 206 source/input hashes, 15 original-run files and 153 earlier evidence files
(146 originals plus seven preparation files) passed verification before execution.

The plan used the unchanged two-node V0 runner with a private bounded transport:
at most two Responses POSTs, zero retries, 32,000 input tokens per send, 8,192 output
tokens per send, 120 seconds per request and 250 seconds total. Its worst retail
references were USD 0.016192 standard / 0.01781120 regional against a USD 0.020000
reference allowance. Actual Foundry billing was not guaranteed by that allowance.
There was no daily output-count success condition, independent API acquisition,
model fallback or output repair. The execution child used `gpt-6.1-sol` / `medium`
in the current session, following the frozen source/input/helper/wire handoff.

### Observed result and faithful offline replay

The child executed the helper exactly once. Exit code 0, status `completed`, two
model sends, zero retries, 40.625 seconds. Both responses were HTTP 200, provider
`completed`, model `gpt-6-luna`, service tier `default`. Requests did not override
reasoning effort; both original responses report `medium` / `standard`.
Twelve capture JSON files retain six stages for each call, with no reported capture
errors. Source HEAD and all protected hashes were unchanged after execution.

The original PlanningResult has seven model-declared main POIs across four days:
2/2/2/1. It also has four WALK transport activities, one generic Haymarket food
activity and two optional unscheduled references. The generic activity and references
are not counted as main visits. Day four remains below the existing soft generation
target; it was neither rejected nor filled to improve density scoring. Sydney Opera
House appears once as a named model claim. The requirements draft has no hard
semantic conditions; its named Opera House visit obligation retains exact count one.

All seven main claims have supplied location text and null provider IDs, consistent
with plain V0 output. No independent name/address correctness, operating access or
route duration is established by those fields. One declared WALK terminates at the
generic food activity; no canonical venue endpoint is invented for it. Independent
projection/evidence preparation must preserve unresolved applicability and endpoints.
No automatic score, independent identity verdict or factual route verdict was emitted.

The parent replayed the two saved provider responses through the existing DTO mapping
and unchanged `run_v0`, with DNS/socket connections blocked. The reconstructed
PlanningResult equals the original result field-for-field, including diagnostics.
This assessment made zero network requests and did not modify original raw bytes.
Validation here is input/schema/wire/limit/hash checking and saved-response replay;
the earlier 3,017-pass/10-skip suite remains evidence for unchanged production code,
not a new test run or proof of factual itinerary quality.

### Usage, evidence and remaining scope

| Request | Ordinary input | Cache-write | Cached input | Output | Included reasoning |
| --- | ---: | ---: | ---: | ---: | ---: |
| Requirements | 3 | 145 | 8,918 | 2,047 | 1,266 |
| Itinerary | 3 | 3,823 | 0 | 4,756 | 2,070 |
| Total | 6 | 3,968 | 8,918 | 6,803 | 3,336 |

Total input is 12,892 tokens; total input plus output is 19,695. Reasoning is already
included in output. Actual second-wire surrogate was 4,204 tokens before reserve.
Using the [official Luna retail rates](https://developers.openai.com/api/docs/models/gpt-6-luna)
rechecked October 7, references are USD 0.001131105 for requirements and 0.002856175
for itinerary, totaling USD 0.003987280 standard / 0.004386008 regional +10%.
The actual Azure/Foundry invoice remains unknown.

Private historical evidence identifiers, not published dependencies:
`artifacts/sydney-v0-natural-generation-smoke-20261007/{plan.json,input.json,first-wire.json,offline-check.json,original-run-hashes.json,assessment.json}`
and `execution/{execution.json,request-1.json,request-2.json,response-1.bin,response-2.bin,result.json,capture/}`.
Frozen input SHA256: `1b3c50ad9ce9c58a4caf047388f3c4131faa0cddb0ffff2467dd8b2f1593d6ba`.
Response hashes: `580ec34e5ae57b19d6e93938de2827a47fcc9cc2317a18aee75e3c6c2d31c89d`
and `0d6504a20e57c59ac2b58a599e3a968b2d11d248480982523137360ad2d56575`.
Result hash: `d8ca6c8ac44aa2438f2efe65534b57488be81dbed217bc7d66626801f78431c7`.

This one-use execution plan is consumed. Independent identity candidate acquisition,
opening/route evidence, applicable reviewed RequirementSpec and final scoring still
need preparation against this actual original output. The earlier eight-venue/four-leg
scenario is not a source of replacement output or permission to drop difficult claims.
No independent API sends or V1-V3 live execution occurred in this case.

<a id="sydney-v1-v3-generation-execution-2026-10-08"></a>

## Sydney V1-V3 generation execution stop - 2026-10-08

Date: 2026-10-08, Australia/Sydney. Status: V1 and V2 original generation completed;
execution stopped after a V2 RAG connection timeout, before V3. Source revision:
`12a56de7b9f7d0bd4c24951f7273016ac62aa845`. No production code, configuration, prompts or limits changed.

### Approved execution and admission

The human explicitly approved the prepared one-use generation package. Its original
preparation snapshot remains unchanged and records its earlier unauthorised state;
the separate current-session authorization receipt binds that exact package hash.
The approved scope was one invocation each of V1, V2 and V3, serially with parent
assessment between versions, subject to the package stops. Retail-reference allowances
were USD 11/12/14, USD 37 total, with zero operator retries. Independent evaluator
acquisition, V0 regeneration, separate DB probing and policy/budget changes were excluded.
Normal V2 RAG database preparation remained part of the selected runtime.

Admission verified all 285 frozen source/input files, six dependency versions, exact
source revision, current Sydney date, credential presence and unused output directories,
without a provider request or DB probe. The required current-session execution child
used `gpt-6.1-sol` with `medium` reasoning effort and executed each dispatched argv once.
V1 completion and fresh source/date/dependency checks admitted V2; V3 was never dispatched.

Both generations used the exact original natural input: Sydney, October 14-17, two
travelers, AUD 1600 and Sydney Opera House once, without an added daily visit quota.
Input SHA256 remained
`1b3c50ad9ce9c58a4caf047388f3c4131faa0cddb0ffff2467dd8b2f1593d6ba`.
The original V0 result and provenance were preserved; V0 result SHA256 remained
`d8ca6c8ac44aa2438f2efe65534b57488be81dbed217bc7d66626801f78431c7`.

### Observed generation and usage

| Observation | V1 | V2 |
| --- | ---: | ---: |
| CLI exit code / planner outcome | 0 / completed | 0 / completed |
| Runtime through cleanup, seconds | 107.219 | 130.656 |
| Process wall time, seconds | 115.838 | 136.967 |
| Model calls / model HTTP sends | 4 / 4 | 5 / 5 |
| Google HTTP sends | 62 | 76 |
| Weather HTTP sends | 1 | 1 |
| Total observed HTTP sends | 67 | 82 |
| Embedding / safe HTML / Repair model sends | 0 / 0 / 0 | 0 / 0 / 0 |
| Reported input tokens | 50,344 | 52,902 |
| Reported output tokens | 9,216 | 12,478 |
| Included cached input tokens | 0 | 4,669 |
| Application cache hits / trace lookups | 0 / 60 | 0 / 74 |
| Estimated retail/proxy USD | 2.078895275 | 2.309309015 |
| Unpriced events | 0 | 0 |

Google observations were V1 search/details/matrix 14/28/20 and V2 11/44/21. Model
cache tokens are distinct from application cache hits. Token totals were 59,560 and
65,380 respectively; reasoning, where reported, is already included in output.
Both stages stayed below their request thresholds, reference allowances and 600-second
whole-run deadline. The estimates use the frozen October 8 retail basis and declared
Foundry/OpenAI proxy assumption. The combined estimate is **USD 4.388204290**, not an
observed invoice. Actual account charges, discounts, free quotas and taxes are unavailable.
V3 incurred no dispatched generation request; the unspent allowance is not a charge.

Original result SHA256 values:

- V1, `sydney-v1-20261008-r1`:
  `e9046d62d719eeca95247a46873ce1cd475d89fa33775281a76ec9d5ab5f63b1`.
- V2, `sydney-v2-20261008-r1`:
  `197520b9de70a7c0e6b4bd4c317282489779f89c9eaf855ec6f6b88f9111b209`.

### Evidence assessment and RAG stop

Each exact result digest agrees across manifest, usage, mechanism, evidence index,
provenance and cost report. Original input and the five structured trip facts match.
Parent checks verified 216 V1 and 260 V2 indexed file hashes, plus three provenance
references per run. All 149 original HTTP IDs are unique within their runs and agree
between usage and index; every observed response was HTTP 200 and both captured bodies
were complete. Usage, mechanism and index report available capture. Trace has 165/178
rows respectively and terminal `run_completed` events. Capture availability describes
preserved observations; it does not attest successful execution of every mechanism.

V2 RAG discovery reports `deadline_limited` with `TimeoutError`. Its configured
10-second connection suboperation failed before SQL retrieval or embedding. Prepare
and connection diagnostics describe the same failure at nested stages, not two extra
operator attempts. RAG elapsed time was 10.097 seconds; its phase deadline did not
expire, and the whole planner remained within 600 seconds. Retrieval queries, returned
positions/entities, embedding sends and RAG fallback sends were all zero. No NPZ was
produced, so vector digest validation is inapplicable; no successful retrieval or
vector evidence is attested. The captured exception type does not establish the
underlying connectivity cause.

The existing runtime continued to produce a selected V2 result with degraded RAG.
That CLI success does not satisfy the intended genuine retrieval evidence. The parent
applied the package's timeout stop before V3 and retained this original V2 output.
No retry, extra embedding, replacement result, connection probe or timeout increase
was performed. The V3 output directory remains absent. Restoring RAG prerequisites,
refreshing the execution package and any new paid attempt require a separate approved
scope; the consumed V2 invocation cannot be silently reused.

No backend suite was rerun for this execution-only task; prior implementation
validation remains scoped to its recorded revision, rather than being a new live gate.

Private historical evidence identifiers, not published dependencies:
`artifacts/sydney-four-version-live-20261008-r1/{v1,v2}` and
`artifacts/sydney-generation-evidence-handoff-20261008`, containing the immutable
authorization receipt, original consoles/process receipts, child assessments, parent
assessments and `parent-live-summary.json`. Each version retains original result,
usage, RAW trace, credential-filtered HTTP, mechanism, cost report, index and provenance.

This stopped package was bounded generation development evidence. V2 genuine retrieval
and V3 generation had not completed; producer completion, final-source review bindings,
changed-intake V0 independent identity and independent final-evidence planning were pending.
No independent evaluator request, total score or qualified four-version intake followed this stopped package.

### Subsequent host connectivity diagnosis

The human requested a connection recheck and supplied a Docker Desktop screenshot
showing the PostgreSQL container running with `55432:5432`. At documentation revision
`a70317f`, a single sandboxed connection check still timed out after 10.016 seconds,
before its read-only `SELECT 1`. A sandbox listener inventory had returned no matching
port; the parent's inference that the host database was unavailable was too strong.

A host-environment Docker inspection then confirmed the container healthy, with
`127.0.0.1:55432` published. Its current start timestamp was 12:08:07 UTC (23:08:07
Sydney), after the earlier V2 generation. The same connection script, dotenv paths and
10-second bound passed outside the sandbox in 0.031 seconds; `SELECT 1` returned one.
The current host connection is usable, while the sandbox check did not establish host
service absence. These later observations do not identify the historical V2 connection
failure's sole cause or retroactively supply RAG retrieval evidence.

Both checks made one connection attempt each, zero retries and zero model/embedding
calls. No corpus compatibility query, service/configuration change or V2/V3 rerun was
performed. Private historical receipts are
`.scratch/tripworld-connection-recheck-20261008-r1.json` and
`.scratch/tripworld-connection-recheck-20261008-r2-host.json`. Any refreshed live package
must account for the execution environment's ability to reach the host database.

<a id="sydney-generation-host-resumption-2026-10-08"></a>

### Authorized host generation resumption

Date: 2026-10-08, Australia/Sydney. Source revision:
`043cae393344d41f8e0dfe3e420b238c95682497`. The human explicitly instructed continuation
after the host connectivity diagnosis. The refreshed one-use package authorized one
new V2 invocation, assessment, then one V3 invocation on the host. V0, completed V1
and the earlier degraded V2 remained unchanged; the new V2 was explicitly authorized
after the stop, rather than an automatic retry. Production code, configuration,
prompts and limits were unchanged.

The package froze 286 files, checked six dependency versions and the actual Sydney
date, and recorded hashes for 541 prior original files. Offline V2/V3 CLI preparation
made zero network attempts, execution credential loads or provider sends. A separately
prepared read-only `RuntimeRetrieval.prepare` check then passed on the host in 0.047
seconds: connection, vector-space configuration, corpus manifest/count and policy
compatibility matched. It made no embedding or planner call and changed no DB data.
The existing required `gpt-6.1-sol` / `medium` child executed the exact V2 and V3 argv
once each with host access; parent assessment admitted V3 only after V2 passed.

V2/V3 retained their USD 12/14 reference allowances, 600-second invocation deadlines,
existing token/request/Repair limits and zero automatic operator retries. The earlier
USD 4.388204290 estimate remained included in the USD 37 workflow reference allowance;
the refresh did not expand that total. No independent evaluator call was authorized.

| Observed item | V2 host resumption | V3 host generation |
| --- | ---: | ---: |
| Exit code / planner outcome | 0 / completed | 0 / completed |
| Runtime through cleanup, seconds | 134.234 | 143.156 |
| Process wall time, seconds | 140.649 | 150.976 |
| Chat calls / embedding calls | 5 / 1 | 6 / 1 |
| Google HTTP sends | 76 | 90 |
| Weather HTTP sends | 1 | 1 |
| Total observed HTTP sends | 83 | 98 |
| Reported input token subtotal, including embedding | 53,809 | 83,297 |
| Reported chat output tokens | 12,152 | 13,303 |
| Included chat cached input tokens | 4,669 | 13,732 |
| Cache ledger hits / framework metric | 13 / 0 | 10 / 0 |
| RAG retrieval queries / returned positions | 1 / 20 | 1 / 20 |
| Captured query-vector bundles | 1 | 1 |
| Repair rounds / Repair chat calls | 0 / 0 | 1 / 1 |
| Estimated retail/proxy USD | 2.37225918 | 2.415477415 |
| Unpriced events | 0 | 0 |

Both embedding batches reported two input tokens; embedding output/cache fields were
not reported and were not relabelled as observed zero. Chat token totals and embedding
input are distinct observations. Cache-ledger hits and the framework metric remain
separate instrumentation scopes.

RAG runtime connection, compatibility, embedding, capture and SQL stages all completed.
Both discovery reports were `partial` because bounded candidate identity resolution
retained omissions, rather than because retrieval failed. V2 recorded 13 resolved,
six existing Google observations and one `fallback_not_unique`. V3 recorded 11 resolved,
four Google observations, two `fallback_not_unique` and three `fallback_budget` omissions.
These unresolved candidates were preserved in diagnostics; no extra lookup was added
to eliminate them. No RAG runtime timeout or failed SQL/embedding stage was observed.

V3 exercised one normal Repair round, with one chat call and 16 route HTTP sends.
Its reported input/output were 30,539/1,142 tokens, 31,681 total; the stage took 15.922
seconds, including 10.219 seconds for the model. Its internal decision was
`ACCEPTED_COMPLETE`; that is a planner decision, not an independent evaluator verdict.
The Repair retail subset was USD 0.0843883, already included in the V3 subtotal.
There were no safe HTML requests or additional operator retries in either invocation.

The two new retail estimates total **USD 4.787736595**. The V1-V3 workflow estimate,
including completed V1 and the earlier degraded V2, is **USD 9.175940885**, below its
USD 37 reference allowance. The frozen October 8 price basis and declared Foundry proxy
remain assumptions; actual account billing, discounts, quotas and taxes are unavailable.

Parent assessment checked all 263/306 indexed file hashes plus three provenance
references per run. All 181 original HTTP IDs agree with usage, are unique within each
run, and have HTTP 200 with complete request/response capture. Result digests agree
across six envelopes; original input and the five structured trip facts match. Usage,
mechanism and index capture are available; trace contains 179/194 rows and completion
markers. Each NPZ contains finite, normalized `float32 [1,1536]` vectors with valid
metadata/digests and the approved corpus artifact hash. The parent also reconstructed
normalized vectors from the captured embedding HTTP responses and matched their exact
values and request-text hashes to the NPZ. Fresh date/source/dependency checks and all
541 original-file preservation checks passed before final documentation changes.

The generation-only binding now references these exact original outputs:

| Version | Run ID | Result SHA256 |
| --- | --- | --- |
| V0, retained | `sydney-natural-v0-20261007` | `d8ca6c8ac44aa2438f2efe65534b57488be81dbed217bc7d66626801f78431c7` |
| V1, retained | `sydney-v1-20261008-r1` | `e9046d62d719eeca95247a46873ce1cd475d89fa33775281a76ec9d5ab5f63b1` |
| V2, new host run | `sydney-v2-20261008-r2` | `b261eeba55abafc258e1b87dd0871cf42d8c1abe3aa1caeabdcfb1044da2476d` |
| V3, new host run | `sydney-v3-20261008-r2` | `a86d1335f197dea1cd23c4de02a4a483921ee1c630dd04ef2825f6000e1e7fe6` |

The earlier degraded V2 remains a separate preserved attempt, not a rewritten output
or a removed cost. Selection follows the explicitly authorized mechanism restoration;
no independent score was used to choose a replacement. Legacy V0 provenance/usage are
retained as legacy observations, without fabricating a new native generation index.

Private historical evidence identifiers: `artifacts/sydney-four-version-live-20261008-r2`
and `artifacts/sydney-generation-evidence-handoff-20261008-r2`, including read-only
compatibility, immutable authorization, preserved-original inventory, child/parent
assessments, `four-version-generation-binding.json` and `parent-live-summary.json`.
Raw provider/model data and credentials remain untracked. No production code changed,
so no new backend suite is claimed; checks covered runtime compatibility, actual
execution, evidence lineage, vector/wire consistency and documentation.

At this checkpoint, all four versions had linked original generation material. The
binding alone did not qualify an evaluator intake, attest producer/final-source review
completion, supply changed-intake V0 independent identity or establish a final score.
Subsequent material qualification and evaluation are documented in the
[Sydney evaluation history](../evaluation/intake-identity-usage.md#sydney-material-qualification-and-four-final-evaluation);
those later results do not turn this generation binding into an evaluation receipt.
