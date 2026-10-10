# POI selection methods, failures and supply decision

Historical development, September 2026. QCGRE, B1 and B2 are retired; their dedicated
implementations/tests/harnesses and local recovery snapshots were deleted. QCGRE's prior
source is recoverable at `60902ac09a1331f6eebddba8963efd24f6e8e61a`; uncommitted B1
has no guaranteed complete Git recovery. Saved method/results remain here, with the
minimum-set study under `artifacts/research/selection_objective` and retained captures
listed below. Current rules belong to
[admission and deterministic supply](../../0002-requirements-evidence.md#admission-acquisition-and-deterministic-supply).

## QCGRE: bounded Google-based selection

The revised September 14 V1-A protected canonical required IDs, cheaply narrowed
`C_raw` / `R_pool`, obtained Details/rating, selected a no-review baseline, then acquired
reviews only where hypothetical experience values could flip membership. Validated
ExperienceProfile fed a greedy relevance/coverage/geography/rating/experience objective.

| Component | Historical responsibility |
| --- | --- |
| Q_rel | Maximum genuine Google query-hit relevance; native rank normalized by original unfiltered response length and weighted by intent importance. |
| C_cov | Greedy marginal uncovered intent contribution, maximum 25 times intent importance. |
| G_geo | Nearest selected-point distance heuristic: initial 5, within 3km 10, within 10km 5, otherwise 0; not Routes feasibility. |
| R_rating | Clipped Google rating contribution in [-10,10], missing neutral; no userRatingCount. |
| E_exp | Registered review-backed experience preference contribution, bounded [-15,10]. |

The selector recomputed marginal coverage/grouping after every greedy addition. Required
canonical IDs were protected, eligibility was separate, and original provider rank then
Place ID broke ties. Review sensitivity enumerated reachable hypothetical E values and
reran selection to decide where review evidence could flip membership. This kept review
cost bounded but tied acquisition policy to the exact scoring mechanism.

Original freeze September 12 had a **158-pass** post-compression regression; the revised
September 14 gate passed **507**. Identical Smoke A resolved Opera House after the earlier
named-identity mismatch. Revised Smoke B used search **9/12**, 123 observations/85 IDs,
C36/R18/final 16/Profile 6 and four 4×16 WALK matrices (**256 elements**); reviews changed
one membership. Complete V1 freeze September 15 had **605** backend passes, including
later official Web/typed semantics/cost projection. Singapore range-cost mapping failed
before correction and identical-input revalidation; those features were not original
V1-A capabilities.

QCGRE's Google position/length relevance could not directly consume TripWorld cosine/rank.
Additive fixed weights and finite experience vocabulary also limited open, subject-specific
set semantics. This motivated reopening, not proof all deterministic selection was invalid.
Canonical identity, factual eligibility, bounded acquisition, Profile evidence, missingness,
capacity/cache/budgets and downstream separation survived the replacement.

## Open requirements and B1 direct selection

The September 18 redesign preserved typed trip facts, named/mode/acquisition fields while
adding bounded open requirements, IDs, exact source/subject attribution and linked discovery/
evidence requests. Earlier open string lists still had six experience values/five Profile
dimensions and no general requirement IDs/offsets/subjects. Exact quote/name validation was
linkage, not semantic entailment; regex/display-name exclusions were not category bans.
Unsupported HARD meaning stopped acquisition through clarification.

B1 used one interpreter, admission, Stage A model shortlist/reserves/review nominations,
Details/selective Reviews/Profile, Stage B model final IDs and deterministic validation,
then downstream tools/generation. It preserved open semantic trade-offs, but mixed model
meaning interpretation with mechanical set execution.

| Development stage | Observed result and boundary |
| --- | --- |
| Initial sizing | **688 passed, 9 skipped**; B10952, long-name A/B16568/14894 exceeded then-limits. No live proceeded before approval. |
| Approved compaction | Sidecars/interning, 160-code-point display prefix, no raw review/full Profile narrative; A14000/B11000, output 4096, low effort, 90 seconds, zero transport retry. **695 passed, 9 skipped**. |
| First failed smoke | Copied `my mother` did not match original `My mother`; **16.906 seconds**, zero Google calls. |
| Successful initial smoke | **96.078 seconds**; A underfilled 6 instead of 10, one repair; 3 Profile calls, one summary>240 failure; B4 within 1..8. Google methods: destination 1/search 3/Details 10/Reviews 3/Weather 1/Routes 1. |
| Frozen initial A | Raw counts **6,6,10,10,10**, valid **3/5**, set agreement **2/10**, mean Jaccard **0.7236**. |
| Frozen initial B | Valid **5/5**, agreement **3/10**, Jaccard **0.7900**; two accepted outputs confused LOW confidence on ACCESSIBLE with low walking intensity. |
| Initial matrix total | **25 model, 19 Google method calls**, one repair; missing walking/crowding/family evidence and no positive cache-hit observations limited interpretation. |
| Targeted fixes | Exact-first unique Unicode-casefold source recovery, application A count normalization, explicit Profile value/confidence, dimension links, summary truncation; focused **128**, backend **720 passed, 9 skipped**; representative A12784/B9895. |
| Targeted smoke | **63.187 seconds**, one source-case recovery, required Opera House retained, A10/B4, no repair/fallback. No experience requests: zero Profile/Reviews. Generated MCA revisit and four unavailable route elements remained. |
| Targeted frozen outputs | A raw 10 each but two selected/reserve overlaps rejected; old six-item A inputs normalized offline. B rejected two dimension supports; accepted counts **5,6,6**, one unsupported short-duration rationale using alias f; fewer/deeper count 3 rejected for linkage. Total **15 model, 16 Google** methods. |

The 63/96-second runs differed in evidence/repair and were not controlled speed comparisons.
Frozen matrices bypassed service repair/fallback, so raw invalid fractions were not
production rates. Remaining overlap/support/prose errors, variation and sequential latency
led the user to stop B1 and select B2. B1 was useful open-semantics work, not a re-frozen
baseline or a worthless method.

## B2: model judgments, deterministic subsets and structural blockers

B2 removed Stage A, allocated Reviews deterministically and used one source-neutral
semantic evaluator before lexicographic legal-set enumeration. Ordinal alignment and
bounded requirement-local facet/redundancy groups were judgments, not factual truth or
weighted QCGRE scores. Up to 2^18 subsets handled hard/count constraints, strength tiers,
conflict/redundancy/subject fairness/coverage, flexible cardinality and geographic/rating/ID
ties. Initial acceptance was offline-only; reproducibility conditional on fixed judgments
did not prove live stability, latency, cost, quality or feasibility.

Two approved initial Sydney attempts failed: A returned indices 1..7 for required 0..6 and
no redundancy groups; B had legitimate walking/crowding/family Reviews but invalid group
operations. Times **37.859/44.149 seconds** measured failure, not speedup. A near-max call transported
**13067 engineering / 12877 actual input**, **2374 output incl 425 reasoning**, but row 15
had 19 relations for 18 candidates. Ordinary usage was **2319/1360 (620 reasoning)** and
**2242/1033 (516 reasoning)**. Matrix total **8 model / 32 Google methods**; no retry.
Because neither scenario completed, five-call successful-fixture stability and live replay
were not run; agreement/Jaccard/under-selection were unmeasured. Name/type-based semantic
claims remained questionable inference. An earlier no-response sandbox failure was separate.

### Serialization and capacity changes

| Revision | Measured change | Remaining limitation / offline gate |
| --- | --- | --- |
| Sparse alias-only version 2 | r/c aliases removed index ambiguity; omissions→unknown, application derives operations. Typical 10 matches **215** visible tokens; all 80 **1405** versus dense 287. Max 432 with support/groups **10142–10682**, label stress **11938**; max multilingual input **14360**. | Exceeded 14000/6144; no paid revalidation/stability run. Backend **644/9 skipped**, focused 99. |
| Grouped version 3 | Requirement rows/five relation buckets, no unknown pairs, explicit neutral kept; duplicate members rejected. Full 432 judgments reconstruct. Multilingual output **10682→4803** initially, but repeated enums raised input 14699. Support/groups were about 67% of label stress. | Shared aliases/interned subjects/compact keys reduced input **14360→13363**, ordinary max output 4467; schema **1596→998**, prompt **464→582**. No semantic/source truncation. |
| Final grouped headroom | Legal label stress **5723–5771** visible tokens, only **421–373** before 6144 and unmeasured reasoning. | Hard serialization fit did not ensure reasoning room. Focused 116/backend **650/9 skipped**, no live. |
| Approved execution recalibration | **32000/16384**, low effort, 90 seconds, zero retry/repair; returned model `gpt-5.6-luna-2026-07-09`. Largest 13363/5771 gained **18637/10613** headroom. | No representation/objective change; focused 119/backend **653/9 skipped**. |

The subsequent A failed on five empty subject references before evaluator/Google. B
completed **63.031 seconds**, evaluator **8.024 seconds**, selecting Opera House and Rocks museum.
Near-max was valid **16.085 seconds**, **13127 input / 2319 output incl 516 reasoning**.
Five fresh identical-B-input judgments were **5/5 valid**, three two-POI sets and two
three-POI sets adding Sydney Culture Walks: **40% exact agreement**, Jaccard **0.8**.
Ten identical-canonical-result replays were deterministic excluding telemetry. Total
**13 model / 19 Google methods**, no retries/repair. Missing crowding stayed unknown;
repetition and unsupported descriptive wording remained. Token fit did not fix quality.

## Minimum-set study and accepted planning-supply replacement

One fixed B pool and its original plus five saved judgments were replayed offline:
**41 observations → 34 canonical → 20 admitted → 10 eligible enriched → 2 selected**.
Original sizes 2..8 tied on all non-cardinality objectives; each of the eight omitted
candidates first lost on `-size`, despite individually adding without degrading earlier
objectives. Five-output frontiers differed at sizes 3..6 but agreed at 7/8. Minimal semantic
coverage was being treated as adequate multi-day planning supply; it was not simply a
model refusal to choose more. Sparse semantic distinctions were secondary on this pool.

A qualified-supply counterfactual gave the same eight-place pool for all six judgments;
a declared small no-evaluator baseline overlapped **7/8**, retained Profile distinctions
and traded geography for a stored primary type. Full QCGRE replay was not attempted:
old experience-intent inputs were absent, so no fabricated mapping/E=0 comparison was
used. Raw method logs had been overwritten; normalized facts/Profiles and event counts
survived. Unseen upstream candidates and itinerary quality were not evaluated.

The user accepted deterministic planning options, retiring the mandatory evaluator.
REQUIRED-first subject/intent opportunities, directional Profile alignment/conflict,
conservative type variety, comparable rating and geography/ID ties filled existing capacity.
Generic/UNKNOWN/neutral/soft-conflicting POIs stayed usable; required/optional identities
were separately projected, scheduled output remained another outcome. An evidence
request's dimension alone could not distinguish less walking from hiking: optional
preferred/avoided values added direction without another interpreter call. Old evidence
stayed UNKNOWN rather than guessed from raw text; nonempty DTO subject refs were checked
without unsupported portable wire `minItems`.

Focused **193**, backend **673 passed, 9 skipped**, Ruff/diff passed. Saved supply indices
were `{0,1,3,5,6,7,8,9}`. Justice museum/Rocks and Finger Wharf/Customs House differences
followed comparable rating within types; Artspace added a primary type. No scenario ID
was hardcoded. This established a bounded policy choice, not general evaluator uselessness,
travel diversity or superiority. The later approved B-then-A live scope was separate from
this initial offline implementation checkpoint.

## Evidence locations and replay conditions

Local paths below identify the retained historical captures; they are not dependencies
for understanding this record or running the current system. Retired harnesses and recovery
snapshots are no longer available. The original full record remains in Git history at
`149d3b4856b7ef73e13758cd921e7bee9265aeab`.

| Event | Historical evidence | Interpretation boundary |
| --- | --- | --- |
| B1 initial live matrix | `logs/selector_live_20260918/`, including `replay_manifest.json` | Five extraction scenarios, two end-to-end attempts, five direct A and five direct B calls, one compaction stress call; direct matrices bypassed repair/fallback |
| B1 targeted correction | `logs/selector_fix_20260919/` | One fresh smoke, five A calls on old bytes, five B calls on a migrated Profile snapshot and one fewer/deeper response |
| B2 initial failures | `logs/b2_live_20260919/` | Two failed end-to-end scenarios and one near-maximum call; successful-scenario stability/replay could not be run |
| B2 budget recalibration | `logs/b2_budget_live_20260919/` | One A, one B, one near-maximum call and fixed-input repetitions under the recorded revised caps |
| Minimum-set study | `artifacts/research/selection_objective/normalized_snapshot.json` and `report.json` | Original B plus five frozen judgments on the same ten eligible candidates; overwritten raw method logs were not recoverable |
| Offline sizing | `logs/b2_offline_measurements.json`, `logs/selector_compaction_sizing.json` | Engineering estimates include prompt/schema/framing; visible output excludes unmeasured reasoning |

B1 used deployment/returned model `gpt-5.6-luna`, `semantic_selector_2` and
`selector_projection_2`; the targeted pass used revision 3 of both. Initial local
reference date was 2026-09-18 with trips 2026-09-20..22; the targeted pass used
2026-09-19 with trips 2026-09-21..23. The same-wording targeted run had an earlier UTC
date because execution occurred after local midnight. A/B caps were 14,000/11,000 input,
4,096 output, low reasoning, 90 seconds and zero transport retries. These were dated
execution settings. Initial extraction token-detail dictionaries were redacted before
persistence; reasoning/cache counters are unavailable for those five calls. The observer
was corrected without repeating paid calls.

### Frozen B1/B2 input and output bindings

These SHA256 bindings distinguish the original and corrected inputs; they are not
interchangeable replay fixtures. B1 extraction cases A-E used the September 18 Sydney
request family, covering mixed family preferences, a non-negotiable stairs ban, named
require/exclude places, qualitative preferences and distinct traveler subjects.

| B1 extraction request | SHA256 |
| --- | --- |
| A | `5d51b643e2d76dbb3519ceba94ccd1fc905c9e09a25e4f1c9f732515d5fe65ce` |
| B | `0e87ae2921c339e6c477d032d3407e28f56bbbc8982d47df21cbf5bb8d277f38` |
| C | `58d12a664a966c9666043499e49895c6b4cdac4e1c7038eead92716c13b13e72` |
| D | `433080a66690708286822e675ba5caf0756a2524f8001bb069e7d67d7290e174` |
| E | `18bb9f15b1182d027bf357b6c8bf4bf5f0b416e7cadb044007f3820c23a771bd` |

Within `logs/selector_live_20260918/` and `logs/selector_fix_20260919/`,
the original Stage A bytes were reused while Stage B migrated to the revised Profile:

| Frozen model input | SHA256 |
| --- | --- |
| Original `smoke2_snapshot_A.json`; corrected `frozen_A.json` | `7c162c2ed624960abce176646d83e596fa27efd524cff69109f624c5084b911f` |
| Original `smoke2_snapshot_B.json` | `6fd5a4743fe3b4f2d6239d48dffe1ffb20c947e8489fc5e54806e148eb1fa3a8` |
| Corrected `frozen_B.json` | `3f870352f7c50f7325ec5157f6ca5fe940fc7f3f8217bb53d919603783f06e37` |
| Corrected `fewer_snapshot.json` | `f018fb66c65ba1b186c516a633babe3865a239243d603655da001afac16e513d` |
| Corrected `smoke1_snapshot_A.json` | `2f14f122cfd5d6d24abf227a02f7eb18b64e5170e4ec17543bc3de0a63c80d17` |
| Corrected `smoke1_snapshot_B.json` | `f8e2a496ce16ae09d952deb8e6503fc3b6edb21d0aeec5a55b0dcdeb7441e6c6` |

The B2 budget baseline and five repeats under `logs/b2_budget_live_20260919/`
shared exact evaluator input SHA256
`4bd1d8debc90f28f59713a9d131b1637e0fe0431edaefbb157b32a8a859b8ba8`.
Their distinct saved outputs bind the fixed-input stability and minimum-set observations:

| Output | SHA256 |
| --- | --- |
| B2 baseline output (`B_result.json`) | `d80491a678520dfaee0304ebdc87f5477fde4af4c970eef3e0356b85de4c291b` |
| B2 repeat 1 (`repeat_1_result.json`) | `0507c98c81715da5b88e3dac696b0af4038259790ef0285762f32c234878fc88` |
| B2 repeat 2 (`repeat_2_result.json`) | `18bfab29137132e78ca0927e007c7e106d6a919cbe4215d6e2166a6549a90ef7` |
| B2 repeat 3 (`repeat_3_result.json`) | `b85f2cb87da49022ce1b2cd73400cc31976958c0946f22728bc3c096e28ef71d` |
| B2 repeat 4 (`repeat_4_result.json`) | `32c0d501bbcb9987dea12db6ea241b935ff32b44ce053d876043ed7e31fc2766` |
| B2 repeat 5 (`repeat_5_result.json`) | `070d240698e5634d8cc67bf59c9eca3cf9d0b89498a18bf6c5d68099935b8983` |

B2 initial request bindings:

- A: 5,631 UTF-8 bytes, SHA256 `b5df872fa7d140384e91d30334b88045ea57c2b5138513d6a474071acb47cce5`.
- B: 5,264 UTF-8 bytes, SHA256 `a69f2789659b1699dafa8a4f2252dcf90be69fa103428a73466a2309e0f7ea2e`.
- Prompt: `28504a3911923187805b8dd28ad6f9e9816e97f892e1dc0a10341d12f3b14c79`.
- Transport schema: `00ff9091d43feb44359a110d89bdb5551bfa7f10cb89b157a71676bb7499dcca`.

The original dense B2 offline fixtures used 18 candidates, 24 requirements, 48 support
records and 12 groups/72 memberships under 14,000 input and 6,144 output ceilings:

| Fixture | Input estimate | Visible output |
| --- | ---: | ---: |
| Typical | 3,013 | 287 |
| Maximum English | 5,991 | 3,330 |
| Maximum multilingual | 11,883 | 3,870 |
| Maximum subjects/multilingual | 13,067 | 3,870 |
| Maximum relation output | 11,883 | 4,194 |

Separate September 19 enumeration measurements were: typical 1,012 legal subsets in
0.016s (eight selected); maximum 262,124 in 3.531s (16 selected); required-pruned
1,471 in 0.047s (eight selected); dense groups 262,124 in 3.719s (13 selected).
The N18/K16 maximum excludes subset sizes 17 and 18; the pruned case has four
required identities and K8. Streaming integer masks avoided materializing every
subset, retaining only equally best masks, bounded by 262,144. A worker thread kept
enumeration off the event loop, but Python CPU/GIL and concurrent throughput remained
limitations; these timings did not establish subsecond or production-concurrency performance.

A separate N18/nine-requirement `tracemalloc` run enumerated 262,124 legal subsets,
observing 109,264 bytes peak traced allocation and 64.234s elapsed. This measured
Python allocations, not process RSS or a universal memory bound. Instrumentation
heavily distorted runtime; its elapsed time is not comparable to the uninstrumented runs.

These bounded fixtures left as little as 933 input tokens. They did not prove that all
Unicode payloads or reasoning-inclusive responses fit. Later sparse/grouped revisions
and the changed execution ceilings are separate stages recorded above.

The study's supply counterfactual kept eligibility, required/excluded constraints and
capacity eight; it maximized the original non-cardinality semantic vector before
maximizing discovery-linked alternatives and applying unchanged geography/rating/ID ties.
All ten saved candidates were discovery-linked, an explicit diagnostic assumption.
All six evaluator outputs yielded indices `[1,2,3,4,5,7,8,9]`, compared with original
`[1,2]`. Added museum/landmark/gallery/attraction types were option rationales, not
proof of experience diversity, walking suitability, hours, route feasibility or schedule
fit. No newly acquired Profile evidence supported the additions. Unknown conflicts did
not become verified absence of conflicts.
