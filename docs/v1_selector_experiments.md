# POI selector experiments

> Cleanup status (2026-09-20): this is historical method/result documentation, not an executable
> tool guide. Retired QCGRE/B1/B2 implementations and dedicated tests/scripts are not preserved.
> The causal minimum-set study is retained at `artifacts/research/selection_objective`;
> actual historical model/provider call records remain in logs. Source recovery snapshots are gone.

Dated records below preserve original scope, status and evidence; they are not current runtime instructions. Current design is maintained separately. Proposed or unexecuted steps remain unexecuted unless a later explicitly identified record establishes otherwise.

<a id="causal-chain"></a>
## Causal chain and interpretation limits

QCGRE offered transparent scoring tied to Google rank and fixed experience vocabulary. RAG/open
semantics exposed extension problems, not proof that all deterministic selection was unsuitable.
B1 bounded two-stage direct LLM selection addressed semantic trade-offs, but payload/cardinality,
identity/evidence validation and latency created reliability costs. B2 separated model judgments
from deterministic set choice; successive contract and token revisions were actually implemented.

The saved offline study traced the two-POI result primarily to the minimum-set/cardinality policy:
excluded candidates could be added without worsening earlier objectives on that fixed pool.
Sparse semantic distinctions were secondary. This was not simply an LLM refusal to choose more.
Upstream unseen candidates were not evaluated. A supply-oriented counterfactual restored options
without proving itinerary quality. Evaluator-specific incremental value was not established for
that case: supported walking distinctions were recoverable from typed evidence, while nuanced
judgments were variable and weakly grounded. This is not a general finding that LLM selection fails.

The accepted replacement preserves open requirements, subjects and evidence with deterministic
planning supply, not byte-for-byte old QCGRE. Historical evaluator implementations and exclusive executable experiments have been deleted; current
acquisition helpers still have active dependencies. Full methods, observations and limits follow.

<a id="m-f504c20b22a6"></a>
## Flow 1: historical Google-only QCGRE

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._



<a id="m-149f6f808b1c"></a>
## Motivation and implementation

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Flow 1: historical Google-only QCGRE. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-149f6f808b1c-0"></a>

The original V1-A supplied Places, Weather and Routes evidence to an otherwise stable
LLM planner. Its 2026-09-12 freeze was followed by an explicitly approved rating/review
realignment. The revised 2026-09-14 V1-A protected resolved required identities, narrowed
cheap candidates before paid Details, and selectively acquired reviews when evidence
could change selection. It was a reasonable bounded Google-only design, not a mistake
that should be retroactively erased.

<a id="b-149f6f808b1c-1"></a>

```text
Typed requirements / named places -> Google search observations -> canonical merge
-> C_raw / R_pool greedy narrowing -> Details and rating -> no-review baseline
-> counterfactual review sensitivity -> Review LLM -> validated ExperienceProfile
-> greedy Q_rel + C_cov + G_geo + R_rating + E_exp -> downstream evidence -> itinerary
```

<a id="b-149f6f808b1c-2"></a>

| Component | Historical responsibility |
| --- | --- |
| Q_rel | Maximum genuine Google query-hit relevance; native rank normalized by original unfiltered response length and weighted by intent importance. |
| C_cov | Greedy marginal uncovered intent contribution, maximum 25 times intent importance. |
| G_geo | Nearest selected-point distance heuristic: initial 5, within 3km 10, within 10km 5, otherwise 0; not Routes feasibility. |
| R_rating | Clipped Google rating contribution in [-10,10], missing neutral; no userRatingCount. |
| E_exp | Registered review-backed experience preference contribution, bounded [-15,10]. |

<a id="b-149f6f808b1c-3"></a>

The selector recomputed marginal coverage/grouping after every greedy addition. Required
canonical IDs were protected, eligibility was separate, and original provider rank then
Place ID broke ties. Review sensitivity enumerated reachable hypothetical E values and
reran selection to decide where review evidence could flip membership. This kept review
cost bounded but tied acquisition policy to the exact scoring mechanism.

<a id="m-d983ec3a65b6"></a>
## Existing evidence and freeze history

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Flow 1: historical Google-only QCGRE. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-d983ec3a65b6-0"></a>

- Original V1-A frozen 2026-09-12; historical 158-test post-compression regression.
- Revised V1-A 2026-09-14: 507 backend tests and Ruff; identical Smoke A revalidation
  resolved Opera House after the earlier named-identity mismatch.
- Revised Smoke B: candidate search 9/12, 123 observations, 85 unique IDs; C=36,
  R=18, final=16, Review/Profile=6. Review evidence changed one final membership.
  Four 4x16 WALK matrices supplied 256 baseline elements. This tested development
  integration and budgets, not statistical ranking quality.
- Complete V1 frozen 2026-09-15: 605 backend tests, Ruff and diff checks; later Official
  Web integration, one-call typed semantics and V1 cost projection included. An initial
  Singapore range-cost mapping failure was corrected and the identical request rerun
  successfully. These later features were not retroactively part of the original freeze.
- Pre-redesign historical baseline is recoverable at Git commit
  `60902ac09a1331f6eebddba8963efd24f6e8e61a`.

<a id="m-ac7ed922138f"></a>
## Why adaptation was abandoned

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Flow 1: historical Google-only QCGRE. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ac7ed922138f-0"></a>

Q_rel relied on Google response position/length; TripWorld cosine/rank is not the same
quantity. Directly combining them would require a new arbitrary mapping or source bonus.
The engineered additive weights also offered a limited way to express nuanced set-level
and traveler-specific semantics. The paused Phase 6 proposal records that rejected
adaptation direction; it is not an implementation authorization.

<a id="b-ac7ed922138f-1"></a>

Useful survivors: canonical identity, factual eligibility, bounded staged acquisition,
actual rating, evidence-specific Profile, missing-state discipline, capacity formulas,
cache/budget, downstream evidence separation and independent V0. Source-native metadata
remains acquisition provenance, not final semantic preference.

<a id="m-0ed57281c9e1"></a>
## Flow 2: B1 direct two-stage LLM selection

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-6a092ab9bde7"></a>
## Hypothesis and approved redesign

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Flow 2: B1 direct two-stage LLM selection. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6a092ab9bde7-0"></a>

On 2026-09-18 V1 was explicitly reopened. B1 aimed to replace closed engineered scoring
with shared source-blind holistic selection suitable for Google-only V1 and future V2.
The requirement redesign established that schema constrains structure, not all possible
semantics. One interpreter retained operational fields and added bounded open
SemanticRequirements, source references, subject attribution, linked DiscoveryIntents and
ExperienceEvidenceRequests. Evidence dimensions did not become a universal preference
taxonomy. Unsupported HARD semantics required clarification before provider acquisition.

<a id="b-6a092ab9bde7-1"></a>

```text
One open Requirement LLM -> canonical facts / Hard Gate -> bounded admission
-> Stage A LLM shortlist/reserves/review nominations -> Details / selective Reviews
-> Review LLM / validated Profile -> Stage B LLM final IDs -> deterministic validator
-> Weather / Routes / Official Web -> itinerary
```

<a id="b-6a092ab9bde7-2"></a>

B1 could make nuanced holistic trade-offs directly, had a working end-to-end path and
preserved open preferences. The common interpreter, provenance, hard policy, evidence
projection and application aliases were valuable work retained in B2.

<a id="m-65a6aff2fc06"></a>
## Offline, compaction and live development sequence

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Flow 2: B1 direct two-stage LLM selection. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-65a6aff2fc06-0"></a>

1. Initial implementation: 688 passed, 9 skipped. Offline sizing found B=10,952 and
   long-name A/B=16,568/14,894 over then-current limits. Live work stopped for approval.
2. Approved payload compaction: canonical sidecars separated from compact model input,
   repeated associations interned, display-name prefix bounded to 160 code points,
   raw reviews/full Profile narratives omitted. Caps became provisional A14k/B11k,
   output4096, low reasoning, 90s and no transport retry. 695 passed, 9 skipped.
3. First bounded live matrix: five direct requirement scenarios; failed first smoke
   due to copied 'my mother' versus original 'My mother' (16.906s, zero Google calls).
4. Successful review-linked smoke: 96.078s, A underfilled six instead of ten and used
   one repair. Three Profile calls, one failed due to summary >240. B selected four
   within 1..8. Google: destination1, search3, Details10, Reviews3, Weather1, Routes1.
5. Frozen A raw counts 6,6,10,10,10; valid3/5, exact set agreement2/10 pairs, mean
   Jaccard0.7236. Frozen B valid5/5, exact set agreement3/10, mean Jaccard0.7900.
   Two structurally accepted B outputs confused LOW confidence on ACCESSIBLE with
   low walking intensity. These were small fixed-fixture observations, not benchmarks.
6. First matrix total: 25 model calls, 19 Google method invocations, one repair,
   no fallback/forced selection. Missing requested walking/crowding/family evidence
   and absent positive cache-hit observations limited conclusions.
7. Approved targeted fixes: exact-first unique Unicode-casefold source recovery;
   application A count normalization; explicit Profile value/confidence; requirement
   dimension links; diagnostic summary truncation. 128 focused tests; 720 passed,
   9 skipped overall. Representative A12,784/B9,895 used 14k/11k ceilings.
8. Targeted live smoke, local 2026-09-19: 63.187s, one source-case recovery, required
   Opera House retained. A10, B4; no repair/fallback. No experience requests were
   extracted, so zero Review/Profile calls. The generator revisited MCA on day three;
   four route elements were unavailable. This is not verified schedule quality.
9. Targeted frozen A: raw ten each, but two selected/reserve overlaps rejected.
   Old six-item responses replayed offline normalize to ten without new calls.
10. Targeted frozen B: no observed confidence/value confusion; two invalid dimension
    supports rejected. Three accepted outputs selected5,6,6. One accepted rationale
    implied short duration using only alias f. The extra fewer/deeper response selected
    three but was rejected for support linkage, so it was not a successful cardinality
    result. Targeted total15 model calls and16 Google method invocations; no repair.

<a id="b-65a6aff2fc06-1"></a>

The 63s and 96s runs had different evidence/repair paths and are not a controlled speed
comparison. Direct frozen matrices deliberately bypassed service repair/fallback; their
raw failure fractions are not production rates. Full tables, hashes, provider usage,
extraction examples and limitations remain in the dated [B1 validation record](v1_selector_experiments.md).

<a id="m-3e6e558cfe27"></a>
## What was fixed and what changed the decision

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Flow 2: B1 direct two-stage LLM selection. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-3e6e558cfe27-0"></a>

Count underfill, copied-case robustness, confidence presentation and summary overflow
received concrete fixes. Selected/reserve overlap, wrong requirement-dimension support,
unattributed prose claims, final-set variation and extra sequential model latency remained.
The recommendation initially was another narrow reliability pass; the user paused it
and approved a design comparison, then explicitly selected B2 and stopped B1 work.

<a id="b-3e6e558cfe27-1"></a>

The issue was responsibility: the LLM interpreted meaning and simultaneously performed
mechanical set execution. Increasing count/reserve/repair/validator machinery did not
establish semantic truth. B1 was retired as the active target, not portrayed as worthless.
Its historical results are retained; B1 was never re-frozen as the final V1 baseline.

<a id="m-4fab216c5669"></a>
## Flow 3: B2 semantic evaluation and deterministic selection

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-4fab216c5669-0"></a>

Approved 2026-09-19 for implementation, cleanup and offline validation only. B2 retains
the revised interpreter/evidence foundation, removes the Stage A LLM, allocates Reviews
deterministically, invokes one source-neutral evaluator and executes a deterministic
lexicographic policy over legal subsets. No model selects the final IDs.

<a id="b-4fab216c5669-1"></a>

Relations are ordinal alignment judgments, not numerical scores or factual truth.
Support aliases are application-owned. Requirement-local facet/redundancy groups model
bounded set relationships without an arbitrary O(N squared) pair output. Generic
operations retain open semantic text; unsupported relationships remain explicit.

<a id="b-4fab216c5669-2"></a>

The policy enumerates up to 2^18 subsets, prunes hard/count violations, processes strength
tiers and conflict/redundancy/subject-fairness/coverage objectives, applies flexible
cardinality, then geographic, comparable-rating and canonical-ID ties. It does not
restore weighted QCGRE. Current details belong solely in [POI selection](development_record.md).

<a id="m-b08891cabf72"></a>
## Design expectation versus observation

_Source context: POI Selection Evolution: QCGRE, B1, B2 / Flow 3: B2 semantic evaluation and deterministic selection. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-b08891cabf72-0"></a>

Expected: one fewer sequential selection call; reproducible final mapping for identical
facts and judgments; clearer failure attribution and shared V1/V2 source-neutral policy.
Not yet established: lower live latency/cost, better fresh-run membership stability,
better POI quality or itinerary feasibility. Evaluator output can be larger than B1.

<a id="b-b08891cabf72-1"></a>

Offline B2 observations and cleanup inventory are recorded in
[B2 implementation checkpoint](v1_selector_experiments.md). **There is no B2 live validation.**
No freeze, V2 runtime integration, V3, commit or push is authorized by these measurements.

<a id="b-b08891cabf72-2"></a>

Remaining risks: deterministic shortlist recall loss; model relation/evidence mistakes;
sparse evidence; operator limitations; abrupt lexicographic trade-offs; equal-subject
opportunity is an explicit policy default; semantic coverage may undersupply a multi-day
trip; token headroom and reasoning use; combinatorial CPU; no automatic evaluator repair;
downstream generation can still violate evidence. Deterministic does not mean verified.

<a id="m-36bea7cc71d7"></a>
## Documentation and code disposition

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-36bea7cc71d7-0"></a>

Current selection authority is poi_selection.md; chronology is this document. Dated B1
measurements remain a standalone historical report. Duplicate B1 architecture review
and B1/B2 comparison documents are consolidated, with their original proposal snapshots
preserved in the explicitly requested ignored development archive. Historical V1 freeze
records remain in v1_milestone.md; v1_design.md now describes the active reopened graph.

<a id="b-36bea7cc71d7-1"></a>

Dead QCGRE engines, review-sensitivity, old extraction bindings and direct B1 selection
are deleted, not hidden behind flags or commented legacy blocks. Historical QCGRE code
is recoverable from Git. B1 was uncommitted: do not falsely claim its complete code is
recoverable from a commit; its process, contracts and evidence are preserved in records.

<a id="m-b4c26fe9e023"></a>
## Historical requirement-contract audit (pre-reopen V1, 2026-09-18)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b4c26fe9e023-0"></a>

Paths below are relative to the repository root. The dated audit read then-current executable
files; it does not treat the earlier proposal as implemented behavior.

<a id="b-b4c26fe9e023-1"></a>

| Contract / source | Actual current fields and bounds | Meaning / consumer / classification |
| --- | --- | --- |
| `backend/app/schemas/request.py`: TravelRequirements | Optional destination (nonempty string), start/end dates with ordering validation, traveler_count >=1, budget Money (nonnegative Decimal amount, three uppercase currency characters); required_activities, excluded_activities, preferences, unresolved_fields are lists of strings without explicit count/text bounds | Destination/date drive acquisition and date validation. Count/budget remain meaningful structured planning inputs, but do not prove feasibility. Four lists are already open text, without per-item source provenance. They are not a complete machine-checkable preference contract |
| `schemas/trip_intent.py`: TripIntentExtractionResult | requirements; named_place_intents <=24; requested_place_information <=32; experience_preferences <=16; one nullable transport_preference; poi_interests <=24 | Immutable extra-forbid domain envelope. One V1 call, not one call per capability |
| `schemas/named_place_intent.py`: NamedPlaceIntent | place_text 1..160; inclusion REQUIRED or OPTIONAL; source_text 1..320; additional_source_texts defaults empty with no explicit length bound | Identity surface for search/reconciliation and must-visit handling. **There is no EXCLUDED value in this extraction enum today.** Additional sources are application-derived after merging |
| `schemas/trip_intent.py`: PoiInterest | surface 1..160; importance explicit_requirement or normal_preference (FALLBACK rejected); source_text 1..320 | **Open copied search surface, not a finite category taxonomy.** Current prompt requires a surface copied from user text. Used for candidate queries and Q/C intent weights; not sufficient to express arbitrary set relationships |
| ExperiencePreferenceIntent | preference enum of AVOID_CROWDS, PREFER_LESS_WALKING, PREFER_ACCESSIBLE, PREFER_FAMILY_FRIENDLY, PREFER_SHORT_VISIT, PREFER_LONG_VISIT; same two importance values; source_text 1..320 | Closed evidence-linked preference vocabulary. Drives fixed Profile dimensions and old E/review-sensitivity machinery. No local-feel, quietness, distinctiveness, traveler attribution or set-diversity semantics |
| TransportPreferenceIntent | one mode DRIVE/WALK/BICYCLE/TRANSIT; source_text 1..320 | Mechanical Routes mode decision; null uses existing WALK grouping default. No ranked/mixed modes, per-leg constraints or numeric walking limit contract |
| RequestedPlaceInformation | target_surface 1..160, target_source_text 1..320, source_text 1..400; exactly one requested_facet or operational_need; subject_scope plus optional scope_text <=160; temporal_scope; date_source_text <=100 and nullable start/end | Drives claim-scoped Official Web information gaps and acquisition. Scope/date invariants are validated; this is an information question, not automatically an inclusion requirement or hard constraint |
| RequestedFacet | general_admission_policy, admission_fee, ticket_requirement, advance_ticket_purchase_requirement, reservation_requirement | Deliberately finite evidence-acquisition vocabulary. Ticket possession, advance purchase, reservation and fee are distinct |
| Allowed operational_need in extraction | current_operational_status, date_specific_operational_exception, special_date_hours | Broader OfficialInformationNeed also has admission_ticket and reservation_requirement, but this extraction contract rejects those operational alternatives in favor of facets |
| Subject/temporal scopes | whole_venue, sub_area, exhibition, ticket_product (UNKNOWN forbidden for requests); GENERAL, CURRENT, TRIP_DATES, EXPLICIT_DATE | Necessary typed evidence targeting; explicit date source and dates required together, ordered and within trip. General/current status cannot stand for a dated exception |
| `evidence/experience_models.py`: ExperienceProfile | crowding, walking_intensity, accessibility, family_friendliness, visit_duration; allowed values per dimension; review refs, low/medium confidence, availability; draft summary <=240, <=5 reviews | Fixed review-evidence representation. Missing signals mean unknown. No quietness field, no official accessibility certification |

<a id="b-b4c26fe9e023-2"></a>

Current prompt and transport path:

<a id="b-b4c26fe9e023-3"></a>

1. `versions/v1/graph.py` calls `generate_structured(...TripIntentExtractionResult)`
   once with `V1_REQUIREMENT_EXTRACTION_SYSTEM_PROMPT`. Its input builder comes from
   V0 and includes original request and the fixed reference date.
2. `versions/v1/prompts.py` extends the V0 extraction instruction. It separates named
   places, supported current-information questions, six experience preferences,
   one transport mode and copied POI-interest surfaces. It prohibits discovery
   weights/tools and assigns fallback search to the application. It has no general
   open, provenance-linked semantic requirement array.
3. `llm/azure_foundry/dto.py` uses strict extra-forbid DTOs with Literal vocabularies.
   FoundryTripIntentExtractionDTO inherits flattened base requirement fields and
   named-place fields; it is not shaped exactly like the nested domain envelope.
   Most domain length/count limits are not present on the current transport DTOs.
4. `llm/azure_foundry/mapping.py:map_foundry_trip_intents` constructs the nested
   domain result, delegates base Money/date conversion and converts lists to tuples.
   `client.py:_FOUNDRY_BINDINGS` binds this response type separately from V0's
   TravelRequirements and from ExperienceProfileDraft.
5. The graph validates named intents, then other trip intents, checks required base
   fields, then trip dates. It stores the separate arrays in V1State and sends them
   to discovery, review acquisition, routing and Official Web respectively.

<a id="b-b4c26fe9e023-4"></a>

Source validation is real but limited:

<a id="b-b4c26fe9e023-5"></a>

- `policies/trip_intent.py` checks source_text as an exact nonempty substring of
  the original request. Normalized surfaces are checked using boundary regexes;
  information targets must match a named surface. Scope/date spans must occur
  inside the supporting source; explicit information dates must be within the trip.
- `policies/named_place_intent.py` rejects model-supplied additional_source_texts,
  checks copied spans/surfaces, rejects a finite set of generic category surfaces
  and action wrappers, merges equal normalized place surfaces, and preserves
  contradictory inclusion as a contract error. It does not solve arbitrary identity.
- These checks prove copying/link integrity, **not semantic entailment**. A valid
  quote can still be normalized incorrectly by the model. There are no offsets,
  traveler subjects or generic requirement IDs in the current extraction.
- Regex/keyword helpers still exist in `poi_funnel.py`, `experience_selection.py`
  and `transport.py`. The active V1 graph supplies typed arrays/mode, bypassing the
  legacy general preference/transport parsers. Exact-name exclusion remains active
  in `services/evidence_acquisition.py`: excluded_activities are compared with
  normalized candidate display names. It cannot implement a general category ban.
  Thus neither "there is no regex anywhere" nor "all exclusions are canonical" is
  accurate. The new path must not activate or extend these semantic fallback helpers.

<a id="b-b4c26fe9e023-6"></a>

Downstream audit:

<a id="b-b4c26fe9e023-7"></a>

- `policies/poi_funnel.py:build_place_search_intents` turns names and PoiInterest
  surfaces into destination queries. It truncates non-name terms to 80 characters,
  deduplicates equal normalized strings and adds generic fallback queries. Reusing
  this truncation for nuanced semantic queries would lose meaning.
- `services/evidence_acquisition.py` reconciles named identities, derives required
  IDs, combines supplied excluded IDs with exact displayed-name exclusions, and
  runs current QCGRE stages. No generic hard semantic predicate registry exists.
- `policies/experience_selection.py:experience_needs_from_intents` maps six enums
  to five dimensions, deduplicates by preference and removes conflicting short/long
  needs. It cannot preserve different travelers' opposing duration preferences.
  `services/review_selection.py` uses these needs and QCGRE counterfactual sensitivity.
- `policies/transport.py:select_transport_mode_from_intent` applies the typed mode.
  Existing route-observation thresholds (3 km / 45 min for WALK) are route policy,
  not user-derived "less walking" constraints and not a POI radius.
- V1 graph passes RequestedPlaceInformation to the Official Web path, then selected
  POIs to Weather/Routes/official evidence and generation. The itinerary prompt still
  receives original request plus base requirements; selector proposals do not.
  Review/Profile is not currently passed to itinerary generation.

<a id="b-b4c26fe9e023-8"></a>

Audit conclusions A-E: base string lists and PoiInterest.surface are already open;
experience preference values and acquisition vocabularies are fixed. Preserve
destination/date/count/Money, named identity intention, routing mode and information
facets/scopes for their real consumers. Do not elevate SearchIntentKind weights or
the six experience values into the universal language of user meaning. Money and
traveler_count are useful typed inputs even where no current hard verifier exists.
There is no current generic numeric-limit schema to claim as already supported.

<a id="m-ff59d8767b1c"></a>
## Subsequent B2 bounded live checkpoint: 2026-09-19

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ff59d8767b1c-0"></a>

After explicit approval, two Sydney three-day attempts and one near-maximum evaluator
transport call were performed; no B2 code/prompt/budget changes or repairs followed.
A reached ten enriched POIs and seven semantic needs but evaluator returned requirement
indices1..7 rather than0..6, rejected as invalid_requirement_rows. It also supplied no
groups for redundancy_control. B acquired three real Reviews/Profiles with legitimate
walking/crowding/family links, then returned candidate_coverage rows with facet/redundancy
groups, rejected as invalid_group_operation. Neither reached final selection or itinerary.
Their37.859s/44.149s times are time-to-failure, not evidence of speedup over successful B1.

<a id="b-ff59d8767b1c-1"></a>

The single near-max transport call used13,067 engineering/12,877 actual input tokens,
2,374 output including425 reasoning, but row15 contained19 relations for18 candidates.
Request/token transport worked; response validation did not. Ordinary evaluator usages
were2319input/1360output(620reasoning) and2242/1033(516reasoning). No cap increase or retry.
Eight model and32 Google method calls were used across the authorized matrix. A preceding
sandbox connection failure had no model response/usage and no Google invocation; it was
preserved separately before network-enabled execution.

<a id="b-ff59d8767b1c-2"></a>

Because neither scenario succeeded, the approved successful-scenario frozen fixture did
not exist. The five-call stability test and live deterministic replay were not run; relation,
support, group, final-set agreement, Jaccard and under-selection remain unmeasured. Existing
offline deterministic evidence is not recast as a live observation. Profile values/confidence
were separated in B, missing evidence stayed unknown, and invalid evaluator outputs were
prevented from becoming final actions. Name/type-based unusual/local/gimmicky judgments
remain questionable inference rather than verified evidence.

<a id="b-ff59d8767b1c-3"></a>

This checkpoint changes the expectation from ready-to-test usability to an observed output
contract blocker. The recommendation is a separately approved narrow evaluator index/matrix/
operator-contract reliability fix before another bounded validation, not automatic B2 redesign,
B1/QCGRE restoration or V1 re-freeze. Complete measurements and requests are recorded in the
[B2 implementation checkpoint](v1_selector_experiments.md).
No formal research conclusion or alteration of historical QCGRE/B1 acceptance is implied.

<a id="m-f3296c0f6565"></a>
## Narrow evaluator contract revision: offline capacity blocker

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f3296c0f6565-0"></a>

Following the failed initial B2 live checkpoint, the user approved an alias-only sparse
output contract without altering final-selection policy. The implemented version2 removes
semantic_1/numeric output identity ambiguity, exact dense row counting and redundant
operation-plus-group declarations. The application supplies r/c aliases, expands omissions
to unknown and derives internal policy data from self-describing structures. The original
invalid outputs remain historical evidence; they were not shifted, repaired or reclassified.

<a id="b-f3296c0f6565-1"></a>

Acquisition/Profile had worked in the preceding runs; the current change addresses model
bookkeeping rather than declaring B2 architecture invalid. New offline contract/policy tests
passed; full backend once644passed/9skipped, final focused99passed, Ruff/diff-check passed.
A focused repeat exposed an elapsed-time equality assumption in a regression test; only the
telemetry comparison was corrected, leaving the production selector unchanged.

<a id="b-f3296c0f6565-2"></a>

Sizing prevented the authorized targeted live re-validation: typical10 sparse matches took
215 visible tokens, but retaining all80 explicit relations took1405 (old dense287). At432
relations with bounded support/groups, valid visible output took10142..10682, above6144.
The maximum-subject multilingual input reached14360, above14000. A high-token diagnostic-label
sample reached11938 output tokens before reasoning. Sparse improved low-density output but
was materially larger at high density. No cap increase, silent reduction or paid test was used
to hide this constraint. A/B/near-max and five-call stability were not run under version2.

<a id="b-f3296c0f6565-3"></a>

The next decision is a narrow payload/capacity refinement followed by offline sizing, not
an automatic live retry or change to deterministic selection. V1 remains unfrozen, V2/V3
unchanged, and no empirical quality or latency benefit is claimed. See the existing
[B2 checkpoint](v1_selector_experiments.md)
for the exact schema, measurements and remaining limits.

<a id="m-8fe5dacfb1dc"></a>
## Grouped sparse serialization: maximum-density recovery, residual label headroom

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8fe5dacfb1dc-0"></a>

The next explicitly approved offline-only pass retained18 candidates/24 requirements and
all six canonical relations. Version3 replaces per-pair output with one requirement row and
five candidate-alias buckets. Unknown pairs/rows are omitted; explicit neutral is preserved.
The application rejects duplicate rows/members and restores the full canonical matrix.
No selection objectives or provider budgets changed.

<a id="b-8fe5dacfb1dc-1"></a>

The measured sequence matters: grouped relations alone reduced ordinary maximum multilingual
output10682->4803, but repeated alias enum definitions grew input to14699. Supports/groups
were then measured as about67% of the high-token-label output, justifying compact wire keys.
Shared schema alias definitions and lossless subject-set interning reduced final maximum
input14360->13363; ordinary maximum output became4467. Schema1596->998, prompt464->582;
prompt growth was not concealed. No name/meaning/subject/evidence truncation occurred.
All432 non-UNKNOWN judgments distributed across five buckets reconstruct exactly and fit
the ordinary representative output case. Typical explicit neutrals remain serialized.

<a id="b-8fe5dacfb1dc-2"></a>

The legal high-token-label cases still reach5723..5771 visible output, only421..373 below6144
before reasoning; therefore there remains a diagnostic headroom limitation, despite hard
serialized-size fit. The next decision concerns representation/headroom, not B2 rejection.
Focused116passed, full backend once650passed/9skipped, Ruff/diff-check passed. No live or paid
calls, embedding/database work, V1 freeze, V2/V3 implementation or commit/push followed.
The existing checkpoint records full component measurements and the unchanged historical
sequence: dense/index structural failures -> per-pair sparse capacity failure -> grouped
serialization with ordinary full-density fit and residual diagnostic-label stress risk.

<a id="m-04921cf9bd29"></a>
## Execution-budget recalibration and bounded live evidence (2026-09-19)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-04921cf9bd29-0"></a>

Accepted grouped-sparse representation retained. User explicitly superseded the old
14,000/6,144 provisional engineering ceilings with development32,000/16,384, low reasoning,
90s, no retries/repair. Actual Foundry model metadata identified gpt-5.6-luna-2026-07-09;
matching documented limits support the request. No capacity/prompt/selection-policy change.
Offline sample sizes remain13,363 input/5,771 visible output at the largest diagnostic;
headroom becomes18,637/10,613. Focused119 pass; full backend653 pass/9 skip; Ruff/diff pass.

<a id="b-04921cf9bd29-1"></a>

A once: failed Requirement extraction on five empty subject_refs; no evaluator/Google.
B once: successful63.031s, evaluator8.024s, selected required Opera House and Rocks museum.
Near-max once: valid16.085s,13,127 provider input/2,319 output including516 reasoning.
Five fresh identical-B-input evaluators:5/5 valid, three two-POI sets and two three-POI sets
adding Sydney Culture Walks. Pairwise exact selected-set agreement40%, mean Jaccard0.8.
Ten identical-canonical-result replays are deterministic excluding timing telemetry.

<a id="b-04921cf9bd29-2"></a>

Evidence dimensions stayed isolated, but local-culture judgments from names/types remain
inferences. Missing crowding remained unknown. Three-day output had limited unique POIs,
repeated visits and unsupported descriptive wording. Token room and structural success
do not resolve those quality issues.13 model calls and19 Google method calls; no retry,
policy tuning, V2/V3, re-freeze, commit/push or thesis archive changes. Recommend a narrow
Requirement DTO/domain subject alignment fix next, subject to approval. This supersedes
additional compression as the next action, while preserving all earlier checkpoint facts.

<a id="m-fec21aca0163"></a>
## Bounded offline candidate-supply decision (2026-09-19)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-fec21aca0163-0"></a>

Hypothesis: **minimal semantic coverage may have been incorrectly treated as adequate
planning candidate supply.** One saved B pool and its original plus five frozen evaluator
outputs were replayed without providers or production edits. Current selected-POI contract
is mixed/ambiguous: ordinary visits are not enforced, but planner input does not separately
project canonical required-vs-optional identities; Routes/Web treat every supplied point
as an evidence target. Weather depends on destination/date.

<a id="b-fec21aca0163-1"></a>

Funnel from saved traces:41 observations ->34 canonical ->20 admitted ->10 successful,
factually eligible enriched candidates ->2 selected. For original B, best sizes2..8 have
identical non-cardinality objectives; each omitted enriched candidate first loses on -size.
Five-output frontiers differ at sizes3..6 but coincide at7/8. One qualified-supply
counterfactual yields the same8-place pool for all six outputs, without sacrificing earlier
objectives. A declared small deterministic no-evaluator comparator overlaps7/8 members,
preserves known Profile distinctions, and trades slightly wider geography for another
stored primary type. This is not a travel-quality benchmark.

<a id="b-fec21aca0163-2"></a>

Full historical QCGRE replay was skipped: real ranks/hits exist, but old controlled
ExperiencePreferenceIntent inputs do not. No fabricated mappings or E=0 comparison.
Original raw method logs were overwritten by their capture harness; normalized enriched
facts/Profiles and event counts survive. Upstream omitted-candidate quality is unknown.

<a id="b-fec21aca0163-3"></a>

Recommendation is OPTION B: deterministic metric-led selection, preserving open requirement
and evidence infrastructure. The shortage is primarily a policy effect, but fixing it does
not establish sufficient unique evaluator value. This supersedes the earlier subject-only
fix as the recommended architecture decision, not the implemented runtime. Implementation
remains semantic_set_1/evaluator3 unchanged pending approval. No live calls, production
changes, V1 refreeze, V2/V3, commits/pushes or thesis-note writes occurred.

<a id="m-74fdef52eda9"></a>
## Accepted Option B: deterministic planning candidate supply (2026-09-19)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-74fdef52eda9-0"></a>

The user accepted the offline decision study and authorized implementation, offline checks
and exactly one new live B followed by one new live A. The stage responsibility changed
from minimum semantic covering set to bounded planning options. B2 is retired from the
active graph, while its evaluator/grouped contract/set policy code and tests remain.

<a id="b-74fdef52eda9-1"></a>

The earlier study remains unchanged: 41 observations ->34 canonical ->20 admitted ->10
eligible ->2 selected. Sizes 2..8 tied before -size; all eight omitted candidates could
individually be added without worsening earlier objectives. Five varied evaluator outputs
converged on the same eight-place supply counterfactual. The declared deterministic
baseline overlapped seven of eight. This supported removing the mandatory extra evaluator,
not a general conclusion that LLM evaluators have no value.

<a id="b-74fdef52eda9-2"></a>

The implementation now uses REQUIRED-first, typed subject/intent opportunity turns,
Profile conflict/alignment, conservative type variety, comparable rating, geographic tie
and canonical ID, filling to existing capacity. No new weights or semantic-purity gate.
Generic/UNKNOWN/neutral and soft-conflicting candidates remain usable options.
Required and optional canonical IDs are explicitly projected to the planner. Scheduled
POIs remain a separate itinerary outcome; no automatic repair was added.

<a id="b-74fdef52eda9-3"></a>

Inspection found a real direction gap in ExperienceEvidenceRequest: a dimension alone
cannot mean less walking rather than hiking. A narrow optional preferred/avoided value
extension uses the same Requirement LLM and existing dimension values. Old snapshots
remain UNKNOWN instead of using raw-text guesses. DTO subject refs now validate nonempty
bounded membership locally; the portable Foundry wire schema still avoids unsupported
minItems. Empty arrays are not filled silently.

<a id="b-74fdef52eda9-4"></a>

Offline: focused 193 passed; full backend once 673 passed, 9 skipped; Ruff/diff passed.
Saved B replay produced eight, indices {0,1,3,5,6,7,8,9}, without fabricated direction.
Justice museum outranked Rocks and Finger Wharf outranked Customs House on current rating
within their types; Artspace provides another known primary type. Exact differences and
limits are recorded in the current policy document. No scenario IDs are hard-coded.
No benchmark, V1 re-freeze, V2/V3, B2 deletion, database/embedding operation or commit/push.

<a id="m-84ec8e720f32"></a>
## B2 Historical Implementation and Development Checkpoints

_Source context: original document introduction/navigation. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-84ec8e720f32-0"></a>

Original checkpoint: implemented and offline-validated, before the later bounded live
checkpoints below. B2 is now retired from the active graph. Current policy: [POI selection](development_record.md).
Decision history: [evolution](development_record.md). Historical B1 evidence:
[dated checkpoints](v1_selector_experiments.md).

<a id="m-7099f6973152"></a>
## Retirement from the active path (2026-09-19)

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-7099f6973152-0"></a>

B2 is a completed, retired experimental stage in the V1 selection evolution. The user
accepted Option B after the saved offline causal study. Deterministic candidate supply
is now implemented and offline validated: 193 focused tests, full backend once 673 passed
and 9 skipped, Ruff/diff checks passed. Evaluator and subset enumeration active calls are
zero by construction and integration regression tests. B2 code and historical tests remain
for a separately approved cleanup; no fallback or environment flag returns to B2.

<a id="b-7099f6973152-1"></a>

This retirement does not rewrite the observations below. The confirmed size penalty
caused saved B under-selection; after supplying eight, repeated evaluator outputs did
not establish enough stable incremental value to justify the extra mandatory call.
This is engineering evidence, not a benchmark proving deterministic selection superior.
Current V1 remains reopened. Live results are appended to the current selection/evolution
records. No B2 code deletion, V0 change, V2/V3, database/embedding work, commit or push.

<a id="m-30078c945862"></a>
## Original B2 scope and result (historical)

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-30078c945862-0"></a>

Reopened V1 now has one active POI selection flow: one Requirement Interpreter,
canonical identities and factual gates, deterministic admission, bounded Details,
deterministic registered Review acquisition, validated Profile, one Semantic Evaluator,
and deterministic legal-set selection before existing downstream evidence/generation.
B1 direct selection and QCGRE scoring are removed. The open requirement foundation,
source/subject validation, unsupported-HARD handling, cache/budgets, current evidence
boundaries and V0 isolation are preserved. TripWorld Phases 1-5 are unchanged. No V2
RAG runtime or V3 implementation, live/paid call, embedding regeneration or database
rebuild was performed. No commit, push or branch switch was performed.

<a id="m-2660be8e924d"></a>
## Offline checks

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-2660be8e924d-0"></a>

- Focused B2/foundation validation: 262 passed in 5.17s.
- Complete backend suite, run once: 604 passed, 9 skipped in 11.35s. Optional database
  integration tests stayed skipped. Normal tests use fake providers/models.
- Final removal of unused candidate_limit argument and documentation of the retained
  historical transport fixture adapter: 20 relevant tests passed in 3.72s afterward.
- Ruff: passed. git diff --check: passed (only CRLF-to-LF normalization warnings).
- Current document links resolve; AST import audit found no deleted-module consumers.
- Protected V0/TripWorld Phases1-5/dependency files match the pre-task hash snapshot.

<a id="b-2660be8e924d-1"></a>

The lower suite count reflects removal of tests solely for retired B1/QCGRE behavior,
not a claim that fewer tests establish greater quality. New tests cover relation shapes,
indices, aliases and dimension isolation; source-neutral projection; HARD authority;
groups and cardinality; strength ordering, subject fairness and duplicate coverage;
required/excluded facts; geographic/rating ties and missing ratings; deterministic replay;
and bounded acquisition/integration. No normal test invokes a live model.

<a id="m-936f1d6bb0a2"></a>
## Reproducible engineering sizing

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-936f1d6bb0a2-0"></a>

Run the offline utility scripts/measure_b2_policy.py with the existing local tokenizer
vocabulary. It produces ignored logs/b2_offline_measurements.json. The utility makes no
provider call. Input count includes the prompt, strict transport schema and framing
allowance; it is an engineering estimate, not provider-reported usage. Names may use the
existing flagged display prefix; semantic requirements and candidates are not dropped.

<a id="b-936f1d6bb0a2-1"></a>

| Fixture | Input tokens | Visible output tokens | Input headroom | Output remainder |
| --- | ---: | ---: | ---: | ---: |
| typical | 3,013 | 287 | 10,987 | 5,857 |
| maximum_english | 5,991 | 3,330 | 8,009 | 2,814 |
| maximum_multilingual | 11,883 | 3,870 | 2,117 | 2,274 |
| maximum_subjects_multilingual | 13,067 | 3,870 | 933 | 2,274 |
| maximum_relation_output | 11,883 | 4,194 | 2,117 | 1,950 |

<a id="b-936f1d6bb0a2-2"></a>

Limits are provisional input14,000/output6,144. Maximum fixtures include 18 candidates,
24 requirements, rich Profiles, 48 support records, 12 groups/72 memberships,
multilingual names/text and maximum subjects. The largest input leaves only933 tokens
(6.7%): this is narrow headroom, not broad assurance. The largest visible output leaves
1,950 tokens for reasoning and any additional provider budget effects. Actual reasoning
usage is unmeasured; total generated-token fit cannot be certified offline. These are
bounded representative fixtures, not a proof of every possible Unicode serialization.
No measured representative input exceeded the cap. Live overflow must stop explicitly,
not truncate requirements, change models or trigger an uncontrolled retry.

<a id="m-d8548ae8295e"></a>
## Enumeration measurements

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-d8548ae8295e-0"></a>

| Fixture | Legal subsets | Wall time seconds | Selected count |
| --- | ---: | ---: | ---: |
| typical | 1,012 | 0.016 | 8 |
| maximum | 262,124 | 3.531 | 16 |
| required_pruned | 1,471 | 0.047 | 8 |
| dense_groups | 262,124 | 3.719 | 13 |

<a id="b-d8548ae8295e-1"></a>

At N18/K16 the 262,124 legal nonempty subsets exclude sizes17 and18. The pruned case
has four required identities and K8. Dense groups exercise bounded facet/redundancy
operations. Streaming masks avoid materializing all subset objects; only equally best
integer masks are retained (bounded by262,144). Selection runs in a worker thread to
avoid blocking the event loop, but Python CPU/GIL and concurrent-request throughput
remain limitations. Approximately3.5-3.7s is acceptable for this initial bounded planning
prototype; it is not a production-concurrency or subsecond latency result. No optimizer
was introduced.

<a id="b-d8548ae8295e-2"></a>

Separate tracemalloc fixture: N18/9 requirements, 262,124 legal subsets, peak traced
allocation109,264 bytes and64.234s with instrumentation. This is a representative Python
allocation observation, not peak process RSS or a universal memory bound. Instrumentation
heavily distorts runtime; do not compare64s against uninstrumented planner latency.

<a id="m-45685fabee9a"></a>
## Cleanup decisions

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-45685fabee9a-0"></a>

KEEP: open requirement contracts/interpreter/provenance/subjects; mechanical named and
transport/current-information contracts; canonical merge and factual date/status/coordinate
gates; Profile acquisition/validation; current evidence/caches/budgets; downstream
Weather/Routes/Web/generation; V0; all accepted TripWorld Phases1-5.

<a id="b-45685fabee9a-1"></a>

UPDATE: the retained selection/acquisition files now expose only shared factual primitives
and B2 orchestration. Foundry uses strict evaluator DTOs and no old selection result DTOs.
Runtime schema6 replaces selector with semantic_evaluator. Stage A/B input/output/timeout
settings and obsolete trace-allowlist entries are removed. Current evaluator defaults:
input14k/output6144, timeout90s, low reasoning, retries0. Result contract b2_1 carries
semantic_evaluation and set_selection instead of stage_a/stage_b. Snapshot and policy
hashes support deterministic replay without treating model interpretation as verification.

<a id="b-45685fabee9a-2"></a>

DELETE decisions by file (paths describe removed historical content, not live links):

<a id="b-45685fabee9a-3"></a>

| Removed file or group | Why obsolete / replacement |
| --- | --- |
| services/poi_selector.py; schemas/poi_selector.py; policies/selector_projection.py | B1 direct selected/reserve IDs, stage payloads, review nominations and repair logic have no active consumer; replaced by evaluator/projection/set policy. |
| policies/experience_selection.py; policies/review_sensitivity.py | QCGRE E scoring and counterfactual review-trigger engine no longer define selection or acquisition. |
| policies/trip_intent.py; policies/named_place_intent.py | Superseded extraction-envelope validators; canonical interpreted-requirement/source validation now owns these checks. Mechanical identity DTO remains. |
| tests/policies/test_experience_selection.py | Tested removed E scoring. |
| tests/policies/test_trip_intent.py; test_named_place_intent.py; test_semantic_intent_migration.py | Tested obsolete envelopes/adapters; relevant provenance/named/open-contract regressions are retained in current tests. |
| tests/services/test_v1_candidate_funnel.py | Tested retired QCGRE funnel behavior; current acquisition/integration tests replace it. |
| tests/versions/v1/test_selector_projection.py | B1-specific stage projection removed; B2 projection tests replace it. |
| scripts/measure_selector_payloads.py; scripts/selector_sizing_baseline.py | Retired A/B sizing fixtures; reproducible B2 fixtures/measurement replace them. |
| docs/poi_selector_architecture_review.md; docs/poi_selection_b1_b2_design_review.md | Unique audit/history preserved in evolution/current policy and ignored historical source snapshots; duplicated current design retired. |

<a id="b-45685fabee9a-4"></a>

Tests renamed and adapted: test_phase6_integration -> test_b2_integration;
test_open_semantic_selector -> test_interpreted_requirements; test_selector_live_fixes ->
test_provenance_profile_regressions. The last two preserve useful foundation regressions,
not B1 selection semantics. prepare_selector_tokenizer -> prepare_tokenizer preserves
the shared vocabulary utility; it was not run during this task.

<a id="b-45685fabee9a-5"></a>

Removed blocks in retained files:

<a id="b-45685fabee9a-6"></a>

- poi_selection: Score, Q/C/G/R/E scoring, greedy selection, score/covered-intent output;
  preserve factual eligibility and selected factual record.
- poi_funnel: old raw-request search construction, experience keyword markers and obsolete
  wrappers; preserve canonical dedupe/identity/date primitives.
- selection_models: engineered intent weight; retain acquisition provenance.
- evidence_acquisition: old CandidateFunnelResult, search_candidates/shortlist/enrich_places,
  run_candidate_funnel/run_review_aware_selection, unused reviews cache-key and unused
  candidate_limit argument; keep actual typed search/Details/current evidence.
- review_selection: old ReviewAttempt/ReviewAwareSelectionResult/run and counterfactual
  dependencies; keep bounded cached Reviews/Profile acquisition.
- trip_intent/named schema and Foundry DTO/mappings: obsolete PoiInterest, universal
  ExperiencePreferenceIntent and old extraction envelopes/bindings; keep mechanical
  RequestedPlaceInformation, TransportPreferenceIntent and named identity.
- test_poi_selection and legacy integration tests: remove greedy weights, old stage
  selected/reserve/repair assertions; preserve factual regression and rewrite integration.
- Historical B1 report: trim duplicate current architecture, retain dated raw findings,
  test counts, failure/fix chain, measured calls/latency and limitations.

<a id="b-45685fabee9a-7"></a>

Intentional narrow legacy retention: policies/transport.select_transport_mode is explicitly
marked historical test-only. Existing transport and route regression fixtures still call
it; no active V1/V2 path imports it. Production uses select_transport_mode_from_intent.
The shared transport module is retained because routing is a preserved foundation. There
is no retained QCGRE/B1 production selector or hidden legacy selection flag.

<a id="m-3cb233adf6d5"></a>
## Documentation and history

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-3cb233adf6d5-0"></a>

Current authority is docs/poi_selection.md; canonical chronology is
[poi_selection_evolution.md](development_record.md). PROJECT, V1 design and milestone
state B2 implemented/unfrozen. Historical B1 implementation report remains a dated report.
Phase6 proposal is marked superseded/paused and retains independent future retrieval
identity design; TripWorld Phases1-5 acceptance is unchanged. No old live findings are
presented as B2 results. Ignored V1-A source snapshots preserve uncommitted B1/B2 proposal
content that cannot truthfully be claimed recoverable from a historical Git commit.
V1A-18 records hypotheses, observations, decision changes and unresolved questions.
These are development-history notes, not formal benchmarks or final thesis conclusions.

<a id="m-68361dd224f9"></a>
## Remaining risks / next decision

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-68361dd224f9-0"></a>

- The evaluator remains stochastic and can misinterpret even structurally valid evidence.
  Deterministic membership is conditional on an identical factual/evaluation snapshot.
- Support records have two refs and unique candidate/requirement pairs. A need linked to
  more than two dimensions cannot earn complete evidence-supported coverage under this
  initial policy; it stays unresolved instead of silently dropping dimensions.
- Compact/default may yield too few POIs for a rich multi-day itinerary; broad can include
  similar candidates when no explicit redundancy group distinguishes them. No days-times-N
  minimum or invented diversity rule was added.
- Bounded operators cannot express every conditional interaction. Unsupported/downstream
  semantics remain explicit. Fairness and conflict-first ordering are policy choices.
- Deterministic shortlist is capacity management, not proof of optimal discovery recall.
- Input headroom is narrow; total output/real reasoning, fresh-run stability, provider
  latency and live quality are not measured. No empirical superiority over B1 is claimed.
- Geography is straight-line compactness, not travel-time feasibility. Downstream evidence
  does not start a new reselection loop; itinerary verification/repair remains future V3.

<a id="b-68361dd224f9-1"></a>

Recommendation: review these limitations, then authorize a small bounded B2 live development
checkpoint if acceptable. Start with representative ordinary requests plus one registered
Profile case and frozen-evaluation replay, not an unbounded matrix. Observe actual usage,
latency and evidence links; stop on token/contract failures. No live work starts automatically.

<a id="m-dcb7fb9d6c49"></a>
## Task-local file inventory

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-dcb7fb9d6c49-0"></a>

This inventory compares the pre-B2 workspace snapshot, not Git HEAD. HEAD status also
contains pre-existing uncommitted B1 foundation changes. Renames appear as add/remove.
Ignored logs and thesis snapshots are excluded from repository-file counts.

<a id="m-6eeee443e152"></a>
## Added

_Source context: B2 Historical Implementation and Development Checkpoints / Task-local file inventory. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-6eeee443e152-0"></a>

```text
backend/app/policies/semantic_evaluation.py
backend/app/policies/semantic_projection.py
backend/app/policies/semantic_set_selection.py
backend/app/schemas/semantic_evaluation.py
backend/app/services/semantic_evaluator.py
backend/tests/policies/test_semantic_evaluation.py
backend/tests/policies/test_semantic_set_selection.py
backend/tests/services/test_b2_acquisition.py
backend/tests/versions/v1/test_b2_integration.py
backend/tests/versions/v1/test_interpreted_requirements.py
backend/tests/versions/v1/test_provenance_profile_regressions.py
docs/b2_implementation.md
docs/poi_selection.md
docs/poi_selection_evolution.md
scripts/b2_development_fixtures.py
scripts/measure_b2_policy.py
scripts/prepare_tokenizer.py
```

<a id="m-ed1ac1d6009b"></a>
## Modified

_Source context: B2 Historical Implementation and Development Checkpoints / Task-local file inventory. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ed1ac1d6009b-0"></a>

```text
PROJECT.md
backend/app/evidence/selection_models.py
backend/app/llm/azure_foundry/client.py
backend/app/llm/azure_foundry/dto.py
backend/app/llm/azure_foundry/mapping.py
backend/app/observability/run_trace.py
backend/app/policies/poi_funnel.py
backend/app/policies/poi_selection.py
backend/app/policies/transport.py
backend/app/runtime/config_models.py
backend/app/runtime/token_counting.py
backend/app/schemas/named_place_intent.py
backend/app/schemas/revised_v1_result.py
backend/app/schemas/trip_intent.py
backend/app/services/evidence_acquisition.py
backend/app/services/review_selection.py
backend/app/services/semantic_poi_pipeline.py
backend/app/versions/v1/graph.py
backend/app/versions/v1/official_web.py
backend/app/versions/v1/runner.py
backend/tests/conftest.py
backend/tests/llm/azure_foundry/test_client.py
backend/tests/llm/azure_foundry/test_dto.py
backend/tests/llm/azure_foundry/test_open_contracts.py
backend/tests/policies/test_poi_funnel.py
backend/tests/policies/test_poi_selection.py
backend/tests/runtime/test_config.py
backend/tests/services/test_v1_review_selection.py
backend/tests/versions/v1/fakes.py
backend/tests/versions/v1/test_graph.py
backend/tests/versions/v1/test_named_place_extraction.py
backend/tests/versions/v1/test_places_contracts.py
backend/tests/versions/v1/test_runner.py
backend/tests/versions/v1/test_semantic_safety.py
config/runtime.yaml
docs/tripworld_phase6_proposal.md
docs/v1_design.md
docs/v1_milestone.md
docs/v1_selector_implementation.md
```

<a id="b-ed1ac1d6009b-1"></a>

The approved B1/B2 comparison document was also removed after consolidation; it was
created after the earlier snapshot and is therefore not in that snapshot removal list.

<a id="m-227ede168a32"></a>
## Deleted or renamed pre-task paths

_Source context: B2 Historical Implementation and Development Checkpoints / Task-local file inventory. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-227ede168a32-0"></a>

```text
backend/app/policies/experience_selection.py
backend/app/policies/named_place_intent.py
backend/app/policies/review_sensitivity.py
backend/app/policies/selector_projection.py
backend/app/policies/trip_intent.py
backend/app/schemas/poi_selector.py
backend/app/services/poi_selector.py
backend/tests/policies/test_experience_selection.py
backend/tests/policies/test_named_place_intent.py
backend/tests/policies/test_semantic_intent_migration.py
backend/tests/policies/test_trip_intent.py
backend/tests/services/test_v1_candidate_funnel.py
backend/tests/versions/v1/test_open_semantic_selector.py
backend/tests/versions/v1/test_phase6_integration.py
backend/tests/versions/v1/test_selector_live_fixes.py
backend/tests/versions/v1/test_selector_projection.py
docs/poi_selector_architecture_review.md
scripts/measure_selector_payloads.py
scripts/prepare_selector_tokenizer.py
scripts/selector_sizing_baseline.py
```

<a id="m-cefe57d03d4c"></a>
## Final Git state

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-cefe57d03d4c-0"></a>

Branch feature/v2; index empty, no commits/push. 41 tracked modified, 11 tracked deleted and 25 untracked paths remain. This includes pre-existing B1 foundation changes; it is not solely a B2 task diff. Ignored measurement logs and thesis notes remain ignored and unstaged.

<a id="m-10dbc14746ba"></a>
## B2 LIVE DEVELOPMENT VALIDATION

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-10dbc14746ba-0"></a>

Date: 2026-09-19. This section records the subsequent, explicitly authorized small live
checkpoint. Earlier statements of no live calls describe the preceding offline checkpoint.
Status: attempted, blocked by evaluator output-contract failures; **V1 is not re-frozen**.
No production code/configuration/prompt changed, no automatic repair or output normalization,
no budget/cap increase, no V2/V3/TripWorld change, no commit/push. Live execution has stopped.

<a id="m-9384ec05aa2e"></a>
## Authorized versus executed matrix

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-9384ec05aa2e-0"></a>

Two end-to-end attempts (A/B), one near-maximum transport call. Both scenarios stopped
before final selection. The required successful-scenario frozen fixture therefore does
not exist; the five fresh stability calls were NOT run. An unsuccessful snapshot was not
silently substituted. Relation/support/group agreement, five final sets, exact-set agreement,
Jaccard, inclusion frequency and successful-output replay are all **not measured**, not
zero or perfect agreement. No additional city, retry-until-success or prompt-tuning loop.

<a id="b-9384ec05aa2e-1"></a>

The initial sandbox A attempt failed to establish a connection at requirement extraction
(0.116s, no response/usage and zero Google calls). Its artifacts were preserved separately.
Execution outside the sandbox was then authorized by automatic review; A was executed
once against the reachable provider. No poor model output was retried. The network failure
is not included in model-output validity or provider-reported usage measurements.

<a id="m-b343d0bb3b9d"></a>
## Exact requests and interpreted semantics

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b343d0bb3b9d-0"></a>

**Scenario A:**

<a id="b-b343d0bb3b9d-1"></a>

> Plan a three-day Sydney trip from 2026-09-21 to 2026-09-23 for three adults: me, my mother and my father. Budget AUD 1800 total. I definitely want to visit the Sydney Opera House. My father likes architectural character; my mother likes cultural places with a local feel. I prefer distinctive places that are not gimmicky tourist attractions. Avoid choosing three museums that all feel the same. We prefer fewer places with deeper visits rather than rushing. We are willing to travel farther if a place is genuinely distinctive. Prefer public transport.

<a id="b-b343d0bb3b9d-2"></a>

Reference date2026-09-19; requested dates2026-09-21..23, inside the supported window.

<a id="b-b343d0bb3b9d-3"></a>

- semantic_1: Favor places with architectural character, according to the father. (medium; favor; individual_poi; subjects father).
- semantic_2: Favor cultural places with a local feel, according to the mother. (medium; favor; individual_poi; subjects mother).
- semantic_3: Favor distinctive places. (high; favor; individual_poi; subjects party).
- semantic_4: Avoid gimmicky tourist attractions. (high; avoid; individual_poi; subjects party).
- semantic_5: Avoid choosing three museums that all feel the same; museums should not be selected as a uniform set merely because they are museums. (high; avoid; selected_poi_set; subjects party).
- semantic_6: Prefer fewer places with deeper visits rather than rushing. (high; favor; itinerary_style; subjects party).
- semantic_7: Accept traveling farther only when a place is genuinely distinctive. (medium; favor; selected_poi_set; subjects party).

<a id="b-b343d0bb3b9d-4"></a>

**Scenario B:**

<a id="b-b343d0bb3b9d-5"></a>

> Plan a three-day Sydney trip from 2026-09-21 to 2026-09-23 for two adults and one child, budget AUD 1800 total. Include the Sydney Opera House as a required stop. We prefer less walking, would like to avoid crowds, and prefer family-friendly places. I also enjoy unusual local cultural places rather than gimmicky attractions. Prefer public transport.

<a id="b-b343d0bb3b9d-6"></a>

Reference date2026-09-19; requested dates2026-09-21..23, inside the supported window.

<a id="b-b343d0bb3b9d-7"></a>

- semantic_1: The party prefers places and an itinerary involving less walking. (medium; favor; itinerary_style; subjects party).
- semantic_2: The party would like to avoid crowded places and experiences. (medium; avoid; selected_poi_set; subjects party).
- semantic_3: The party prefers family-friendly places. (medium; favor; selected_poi_set; subjects party).
- semantic_4: The speaker prefers unusual local cultural places over gimmicky attractions. (medium; favor; selected_poi_set; subjects traveler_1).

<a id="b-b343d0bb3b9d-8"></a>

Both preserved REQUIRED Sydney Opera House, public-transport preference, three travelers
and AUD1800 budget. A retained father/mother/party attribution and seven semantic items;
no ExperienceEvidenceRequest was emitted, so zero Reviews/Profile calls. B emitted four
semantic items and registered walking_intensity, crowding and family_friendliness links.
No request was fabricated to force Reviews.

<a id="m-a21f2785cfb0"></a>
## Actual evaluator failures and semantic inspection

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-a21f2785cfb0-0"></a>

**A:** expected row indices0..6; returned1..7. The application rejected
invalid_requirement_rows. This is consistent with confusing semantic_1-style IDs with
zero-based output indexes, but the model's internal cause is not observable. No index
shift/repair was applied. In addition, its redundancy_control row supplied no groups;
that is another independent contract issue, not fixed by an index correction alone.
The compact record also used the one-based-looking requirement6.

<a id="b-a21f2785cfb0-1"></a>

For semantic inspection only, row positions/text make apparent intended judgments readable;
this does not make their numeric references valid:

<a id="b-a21f2785cfb0-2"></a>

- Father/architecture: Opera House and Customs House weak_match; most others unknown.
  Conservative and plausible inference, but limited factual features do not establish
  architectural merit. A potentially useful match can be missed by overly weak relations.
- Mother/local cultural feel: MCA, Rocks Market, history walks and Writers Walk weak_match;
  plausible but unverified. No evidence of actual local patronage was supplied.
- Distinctive/non-gimmicky: Runaway Gardens/Spiegeltent and BridgeClimb strong_match for
  distinctiveness; Spiegeltent conflict for gimmick avoidance. These are questionable
  name/type-based judgments, not supplied factual proof of quality or gimmickiness.
- Avoid three similar museums: redundancy_control without any group cannot execute.
- Farther-if-distinctive: conditional_contribution with all unknown. It did not turn the
  condition into an invented radius, but no usable contribution was delivered.

<a id="b-a21f2785cfb0-3"></a>

A's17 support records referenced existing candidate aliases, with no invented alias.
Their requirement indices remain misbound; valid alias spelling does not fix row identity.
Some cite name/type as support for distinctiveness or nongimmickiness. This is evidence
interpretation to inspect, not proof that those semantic properties are facts.

<a id="b-a21f2785cfb0-4"></a>

**B:** row indices0..3 and ten relations per row were correct, but all four operations
were candidate_coverage while the response supplied three facet groups and one redundancy
group. Validation rejected invalid_group_operation. One requirement simultaneously received
facet and redundancy groups; singleton facet groups also cannot meet the current diversity
operation's minimum two-facet semantics. Groups were not silently discarded.

<a id="b-a21f2785cfb0-5"></a>

B's concrete evidence-linked judgments were largely consistent with supplied signals:
Opera House HIGH walking intensity -> conflict with less walking; Luna Park LOW crowding
with low confidence -> match for crowd avoidance; acquired family-friendly values -> match.
Missing/unacquired walking/crowding/family signals stayed unknown, not conflict. No
accessibility-for-walking or crowding-for-quiet substitution was observed. The low crowding
value and low confidence are distinct fields; calling this match does not establish strong
certainty. The same caution applies to Opera House's low-confidence family signal.

<a id="b-a21f2785cfb0-6"></a>

B used primary_type aliases to support/contradict unusual local culture: museum/gallery
weak matches are plausible inference; amusement-park type alone does not prove gimmickiness,
and tourist_attraction type alone does not prove local cultural value. These are questionable
semantic judgments. No such judgment was accepted as a HARD pass or downstream official fact.
A/B schema-valid DTOs were therefore NOT treated as valid or semantically correct evaluations.

<a id="m-f2f263a61f03"></a>
## Scenario B Profile evidence and aliases

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f2f263a61f03-0"></a>

All three acquired Profiles were available; each used five retrieved review snippets.
The table lists every returned dimension. Missing dimensions remained absent/unknown.

<a id="b-f2f263a61f03-1"></a>

| Candidate | Dimension | Value | Confidence | Linked requirement / evaluator use |
| --- | --- | --- | --- | --- |
| Sydney Opera House (c1) | walking_intensity | HIGH | medium | semantic_1 / c1.walking_intensity / contradicts; relation conflict |
| Sydney Opera House (c1) | family_friendliness | FAMILY_FRIENDLY | low | semantic_3 / c1.family_friendliness / supports; relation match |
| Luna Park Sydney (c0) | crowding | LOW | low | semantic_2 / c0.crowding / supports; relation match |
| Luna Park Sydney (c0) | family_friendliness | FAMILY_FRIENDLY | medium | semantic_3 / c0.family_friendliness / supports; relation match |
| The Rocks Discovery Museum (c2) | visit_duration | SHORT | low | No registered visit_duration link; not cited by evaluator. Its primary_type was separately cited for open culture semantics. |

<a id="b-f2f263a61f03-2"></a>

For B's10 support records, independent read-only inspection found zero nonexistent aliases,
zero cross-candidate aliases and zero unlinked Profile-dimension references. This is one
rejected evaluation's component-level observation, not evidence of general reliability.
The overall evaluation failed before final policy, so no Profile signal became a final
requirement-satisfaction or verified status.

<a id="m-dc8de980f04c"></a>
## Cardinality, deterministic trace and replay limits

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-dc8de980f04c-0"></a>

| Observation | A | B |
| --- | ---: | ---: |
| Trip days | 3 | 3 |
| Feasible required IDs | 1 | 1 |
| Admitted candidates | 20 | 20 |
| Enriched/eligible candidates | 10 | 10 |
| Selection minimum / maximum | 1 / 8 | 1 / 8 |
| Excluded IDs | 0 | 0 |
| Interpreted cardinality intent | fewer/deeper | no explicit cardinality preference |
| Returned cardinality | compact, invalid requirement index | none |
| Final selected count / IDs | Not produced | Not produced |
| Final-policy subsets evaluated | 0: not reached | 0: not reached |
| Final-policy CPU/wall time | Not measured | Not measured |

<a id="b-dc8de980f04c-1"></a>

REQUIRED ID: ChIJ3S-JXmauEmsRUcIaWtf4MzE (Sydney Opera House).
No final comparison ran. Consequently no winning strength/conflict/fairness/coverage/facet
vector, redundancy exclusion, geography/rating/canonical-ID tie or final membership exists.
The decisive stopping comparisons are application row identity validation (A) and group
operation compatibility (B). Invalid judgments were never fed into an offline hypothetical
selection and reported as live results.

<a id="b-dc8de980f04c-2"></a>

Default/compact/broad behavior, under-selection, itinerary repetition and empty periods
cannot be assessed because neither itinerary was generated. There is no evidence here of
systematic under-selection and also no evidence resolving that risk. No days-times-N rule
or cardinality modification was introduced. Live deterministic replay was not possible
under the specified successful-evaluation prerequisite; previous offline replay evidence
remains separate and is not relabeled as a live result.

<a id="m-73ad9bd22945"></a>
## Factual authority and snapshots

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-73ad9bd22945-0"></a>

Actual A/B model-visible payloads were recursively checked: no provider/source labels,
provider rank, actual_result_count, future RAG rank/cosine, system_version, QCGRE scores or
raw reviews. Candidate names may name real Google-backed places; this is not a source bonus.
The evaluator schema has no write-back fields for identity, coordinates, business status,
rating, evidence values or HARD check_result. Code inspection confirms final evidence is
application-owned; both actual outputs were rejected before selection or generation.
This validates the observed fail-closed boundary, not every possible semantic interpretation.

<a id="b-73ad9bd22945-1"></a>

Exact serialized input strings were saved before each model call, with canonical sidecars,
configuration, hashes, deployment and output metadata in ignored logs/b2_live_20260919.
They contain synthetic user requests and public POI data, no credentials. A/B snapshots
are failed-scenario diagnostic artifacts, NOT the successful fixture required for stability.

<a id="b-73ad9bd22945-2"></a>

- A: 5631 UTF-8 bytes; SHA256 `b5df872fa7d140384e91d30334b88045ea57c2b5138513d6a474071acb47cce5`.
- B: 5264 UTF-8 bytes; SHA256 `a69f2789659b1699dafa8a4f2252dcf90be69fa103428a73466a2309e0f7ea2e`.

<a id="b-73ad9bd22945-3"></a>

Prompt SHA256 `28504a3911923187805b8dd28ad6f9e9816e97f892e1dc0a10341d12f3b14c79`.
Transport schema SHA256 `00ff9091d43feb44359a110d89bdb5551bfa7f10cb89b157a71676bb7499dcca`.
Evaluator semantic_evaluator_1; projection semantic_projection_1; policy semantic_set_1;
config schema6, input14k/output6144, low reasoning,90s, zero retries/repair. Returned model
identifier for every evaluator call: gpt-5.6-luna. No model/deployment swap occurred.

<a id="m-0eb42382d548"></a>
## Actual evaluator usage and latency

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-0eb42382d548-0"></a>

| Call | Engineering input | Provider input | Output (includes reasoning) | Reasoning subset | Total usage | Seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 2509 | 2319 | 1360 | 620 | 3679 | 12.915 |
| B | 2432 | 2242 | 1033 | 516 | 3275 | 9.828 |
| stress | 13067 | 12877 | 2374 | 425 | 15251 | 16.578 |

<a id="b-0eb42382d548-1"></a>

All three engineering estimates were190 tokens above provider input. Provider-reported
input_token_details.cache_read was0 for all; cache_creation was2316/2239/12874 respectively.
These are usage fields as returned, not independently calculated billing. No dollar cost
was inferred. Reasoning is a subset of output and was not added again to totals.

<a id="b-0eb42382d548-2"></a>

Evaluator latency across the three different inputs: mean13.107s, median12.915s,
range9.828..16.578s. This is descriptive, NOT a five-run identical-input stability sample.
The two ordinary calls alone average11.372s; neither produced a valid final evaluation.

<a id="m-4ff865263bea"></a>
## Near-maximum transport result

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-4ff865263bea-0"></a>

Exactly one synthetic18-candidate/24-requirement, maximum-subject multilingual call:
43,836 input bytes, engineering13,067, actual12,877 input tokens. Foundry accepted the
request/schema, returned a response with output2,374 including reasoning425, within6144.
No refusal, timeout or token overflow was observed. Actual input remained below14k.

<a id="b-4ff865263bea-1"></a>

Domain validation then failed because row15 contained19 relations for18 candidates:
rows.15.relations exceeded the maximum18. Thus transport/token acceptance succeeded but
response validity FAILED. No complete domain draft was saved because mapping failed;
usage metadata and the precise validation error were preserved. No second stress call,
cap increase or silent matrix trimming was performed. This is not a travel-quality test.

<a id="m-65b6a6788b8d"></a>
## End-to-end timing and calls

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-65b6a6788b8d-0"></a>

Times below are actual calls or noted lifecycle intervals. Total measures run_v1 invocation
to failure, excluding provider construction. Provider durations and model durations do not
cover all local serialization, tracing, graph or scheduling overhead. No residual time is
misreported as shortlist computation.

<a id="b-65b6a6788b8d-1"></a>

| Stage | A seconds | B seconds |
| --- | ---: | ---: |
| Requirement LLM | 13.762 | 10.567 |
| Destination search | 0.950 | 0.914 |
| Named-place search | 1.050 | 0.487 |
| Candidate searches, summed | 3.569 | 1.424 |
| Deterministic shortlist | Not isolated by current instrumentation | Not isolated by current instrumentation |
| Details, summed | 5.333 | 7.095 |
| Reviews provider, summed | 0 | 2.408 |
| Review/Profile LLM, summed | 0 | 11.132 |
| Semantic Evaluator model call | 12.915 | 9.828 |
| Final deterministic selection | Not reached | Not reached |
| Weather / Routes / Official Web / itinerary | Not reached | Not reached |
| Total to failure | 37.859 | 44.149 |

<a id="b-65b6a6788b8d-2"></a>

B Profile LLM calls individually3.853/4.521/2.758s. These failed runs must not be compared
with successful historical B1 approximately96s/63s as evidence of end-to-end speedup.
Successful B2 end-to-end latency remains unknown.

<a id="b-65b6a6788b8d-3"></a>

| Call category | A | B | Stress |
| --- | ---: | ---: | ---: |
| Requirement LLM | 1 | 1 | 0 |
| Semantic Evaluator | 1 | 1 | 1 |
| Review/Profile LLM | 0 | 3 | 0 |
| Itinerary LLM / Web Reasoner | 0 | 0 | 0 |
| Destination search | 1 | 1 | 0 |
| Named-place search | 1 | 1 | 0 |
| Candidate discovery searches | 3 | 2 | 0 |
| Details calls / cache hits | 10 / 0 | 10 / 0 | 0 / 0 |
| Reviews calls | 0 | 3 | 0 |
| Weather / Routes / Web / page calls | 0 | 0 | 0 |
| Stage A selector / Stage B direct selector | 0 / 0 | 0 / 0 | 0 / 0 |

<a id="b-65b6a6788b8d-4"></a>

Paid/live matrix actual totals:8 model invocations and32 Google provider-method invocations.
The separate sandbox connection attempt had no response or usage and is recorded separately.
Five stability calls were not spent. Existing request budgets were never increased.

<a id="m-9474ba547a6e"></a>
## Decision, limitations and checks

_Source context: B2 Historical Implementation and Development Checkpoints / B2 LIVE DEVELOPMENT VALIDATION. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-9474ba547a6e-0"></a>

Recommendation: **one narrow B2 evaluator-contract reliability fix, separately approved**,
not V1 re-freeze and not immediate architecture replacement on this small evidence.
Prioritize unambiguous application-supplied requirement indices, exact matrix bounds and
explicit operation/group consistency. Audit transport schema versus domain validation;
strict provider DTO parsing alone did not enforce all application invariants. Do not simply
shift IDs, discard groups, truncate rows or relax gates to make these outputs pass.
No fix or prompt tuning was implemented in this live task.

<a id="b-9474ba547a6e-1"></a>

The successful part is bounded acquisition, real Profile links, actual token headroom and
rejection of invalid outputs. The usability blocker is that neither ordinary request reached
final selection. Semantic quality/stability/cardinality/itinerary and successful replay
questions remain unanswered. This is development evidence, not a formal failure-rate estimate
or conclusion that B2 is superior/inferior to B1.

<a id="b-9474ba547a6e-2"></a>

Only ignored measurement harness/artifacts and the two requested documentation files changed.
No production implementation was changed, so the conditional code-fix focused/full tests and
Ruff rerun were not triggered. Documentation diff-check passed; no runtime files were edited.
The next task requires explicit approval. No automatic fix/live retry/freeze/commit/push follows.

<a id="m-6c070e1a2d2b"></a>
## Evaluator-contract reliability checkpoint: alias-only sparse judgments

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-6c070e1a2d2b-0"></a>

Date: 2026-09-19. Explicitly approved narrow contract change, implemented and offline-tested.
**Blocked before targeted live re-validation by measured token sizing.** No new live model,
Google or other paid calls were made in this checkpoint. No repair/retry, cap/budget increase,
policy tuning, V2/V3 work, TripWorld rebuild, embedding regeneration, commit or push.
V1 remains reopened/unfrozen. The preceding failed live observations remain unchanged.

<a id="m-1e73be26ee4d"></a>
## Root causes and design choice

_Source context: B2 Historical Implementation and Development Checkpoints / Evaluator-contract reliability checkpoint: alias-only sparse judgments. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-1e73be26ee4d-0"></a>

The actual previous Foundry DTO transmitted generic integer requirement identities and
unconstrained relation lists; strict schema parsing did not encode the runtime matrix shape.
The model also saw semantic_1-style identities, while output required zero-based numbers.
Scenario A's1..7 rows are consistent with confusing those representations; internal model
causality is not provable. A also supplied redundancy_control without groups. Scenario B
returned candidate_coverage plus incompatible separate groups. The stress response had19
relations in a row for18 candidates. Those were application-invalid outputs, not successes.

<a id="b-1e73be26ee4d-1"></a>

The new model contract uses only request-local r0..r23 and c0..c17 aliases. Existing aliases
are supplied explicitly in records, evidence links, assessments and required-candidate data.
Application side retains the canonical requirement/Google identity maps. Canonical IDs and
numeric row IDs are absent from model input/output identity fields. No index shifting or
repair of old outputs exists. The old live artifacts remain historical and are not converted
into successful examples.

<a id="b-1e73be26ee4d-2"></a>

Chosen design: sparse candidate-requirement records, omitted=unknown. The existing Foundry
adapter supports fixed strict DTOs cleanly; a runtime-generated exact dense object would
require per-request schema generation/binding/schema sizing and different integration paths.
No such infrastructure was introduced. Sparse removes exact-array bookkeeping, but repeated
field/alias serialization is expensive at high density: measurements below disprove the
assumption that sparse is always smaller. The choice remains blocked for maximum capacity;
this checkpoint is not a claim that live usability has been established.

<a id="m-c628cbfc70c3"></a>
## Exact model schema and bounds

_Source context: B2 Historical Implementation and Development Checkpoints / Evaluator-contract reliability checkpoint: alias-only sparse judgments. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-c628cbfc70c3-0"></a>

All eight top-level fields are required; unused structures are empty arrays. Extra fields
are forbidden. Candidate/requirement aliases use static bounded Literal vocabularies in
Foundry, followed by request-local membership checks in application code.

<a id="b-c628cbfc70c3-1"></a>

```json
{
  "semantic_relations": [
    {"candidate_ref": "c0", "requirement_ref": "r0", "relation": "match"}
  ],
  "supports": [],
  "facet_groups": [],
  "redundancy_groups": [],
  "cardinality_preferences": [],
  "conditional_contributions": [],
  "downstream_only_requirements": [],
  "not_operationalized_requirements": []
}
```

<a id="b-c628cbfc70c3-2"></a>

- semantic_relations: <=432 records. relation remains strong_match/match/weak_match/neutral/
  conflict/unknown. No score/probability. Duplicate pairs reject, including identical repeats.
- supports: <=48 unique candidate/requirement pairs; candidate_ref, requirement_ref,
  interpretation supports/contradicts/insufficient, support_alias_refs1..2. Aliases must exist
  on that candidate and Profile dimensions must be registered for that requirement.
- facet_groups: requirement_ref, member_candidate_refs1..18, label1..80 code points. At least
  two distinct facets are required to invoke the unchanged facet-coverage policy. No model
  tolerance field: application owns facet tolerance1.
- redundancy_groups: same fields plus allowed_before_penalty1..16 and <=selection_max.
- Both group arrays share <=12 total groups and <=72 total memberships. Empty/duplicate
  members, unknown aliases, duplicate membership groups and out-of-scope requirements reject.
  No group_ref is needed because no structure references groups; labels are never parsed.
- cardinality_preferences: <=2 requirement_ref/mode records, mode compact/broad. Repeated
  requirement rejects even with the same mode; compact+broad for one requirement rejects.
- conditional_contributions: <=24 unique requirement aliases. Its candidate contributions
  use the corresponding semantic_relations; no extra unsupported conditional rule is invented.
- downstream_only_requirements and not_operationalized_requirements: <=24 unique aliases
  each. They are mutually exclusive and incompatible with groups/cardinality/conditional
  structures for the same requirement. Diagnostic relations do not create policy coverage
  when one of these terminal statuses applies.

<a id="b-c628cbfc70c3-3"></a>

Candidate relations require no operation field and may coexist with redundancy or facets.
Facet plus redundancy is supported. Conditional plus redundancy is supported. Conditional
plus facet coverage for one requirement rejects because the unchanged policy has a single
coverage interpretation; implementing a new combined objective would exceed this task.
Cardinality remains exclusive of other special structures. Group requirements retain
selected_poi_set scope; cardinality retains the approved selected-set/whole-trip/style scopes.
A set requirement can be explicitly not_operationalized without invented groups. Absence
of groups supplies no facet reward, no redundancy claim, and no verification of diversity.

<a id="m-f16347562d48"></a>
## Canonicalization and unchanged policy

_Source context: B2 Historical Implementation and Development Checkpoints / Evaluator-contract reliability checkpoint: alias-only sparse judgments. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f16347562d48-0"></a>

The application validates the new domain output, resolves aliases by lookup (not parsing or
shifting numbers), rejects duplicate pairs, initializes every cell to unknown, writes the
accepted sparse judgments, canonicalizes support/group/member ordering, derives internal
operations from structural presence and validates evidence and scope invariants. Explicit
neutral stays neutral. Input record ordering cannot affect the expanded state.

<a id="b-f16347562d48-1"></a>

CanonicalSemanticEvaluation retains the complete internal matrix and application-owned
operation data required by the existing policy. It is not registered with Foundry and is
not accepted as model output. Internal shape checks are deliberately retained because they
protect policy invariants. Only SemanticEvaluationDraft with sparse fields is model-facing.
SemanticEvaluationResult stores raw_output separately from canonical draft for traceability;
evaluator version2 distinguishes this response from historical version1.

<a id="b-f16347562d48-2"></a>

The deterministic semantic_set_1 implementation file is byte-for-byte unchanged against
the task-start snapshot. Required/excluded rules, strength objectives, fairness, coverage,
cardinality, geography/rating/canonical ties and enumeration remain unchanged. No hidden
legacy flag or retry path exists. V0, acquisition/orchestration, dependencies and TripWorld
were also checked against the task-start snapshot and remain unchanged by this checkpoint.

<a id="m-ec061949773a"></a>
## Dead contract cleanup and current files

_Source context: B2 Historical Implementation and Development Checkpoints / Evaluator-contract reliability checkpoint: alias-only sparse judgments. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ec061949773a-0"></a>

Removed old FoundryRelationRowDTO, FoundrySemanticSupportDTO, FoundrySemanticGroupDTO and
FoundryCardinalityDTO. Their integer IDs, rows, operation and separate generic groups are
no longer model-output fields. The service no longer accepts the old dense model response;
old version1 evaluator configuration is rejected. Numeric values survive only in internal
canonical policy data, never as model identity. There was no need to delete entire files.

<a id="b-ec061949773a-1"></a>

Updated schema/DTO, projection, application canonicalizer, evaluator prompt/service,
evaluator version/config, fake-model integration responses, Foundry tests and relevant
contract tests. Existing policy tests retain their deterministic expectations. Updated
shared offline fixtures/sizing utility; added test_sparse_semantic_contract.py and
measure_b2_contract.py. No new architecture document was created.

<a id="m-bdc98dbc1306"></a>
## Offline sizing: before and after

_Source context: B2 Historical Implementation and Development Checkpoints / Evaluator-contract reliability checkpoint: alias-only sparse judgments. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-bdc98dbc1306-0"></a>

Previous dense checkpoint: typical input3013/output287; maximum English input5991;
maximum multilingual input11883; maximum subjects multilingual input13067; maximum visible
relation output4194. These are historical measurements, not rerun live calls.

<a id="b-bdc98dbc1306-1"></a>

New measurements use the exact new Foundry schema, prompt, alias input and serialized output.
Every output fixture passes canonicalization before sizing. The typical80-cell fixture
contains10 matches and70 explicit neutrals: dropping those neutrals would change them to
unknown, so the10-record sparse example is not advertised as lossless compression.

<a id="b-bdc98dbc1306-2"></a>

| New fixture | Relation records | Engineering input | Visible output | Output headroom vs6144 |
| --- | ---: | ---: | ---: | ---: |
| best_all_unknown | 0 | 4202 | 44 | 6100 |
| typical_positive_sparse | 10 | 4202 | 215 | 5929 |
| typical_explicit_neutral | 80 | 4202 | 1405 | 4739 |
| maximum_density_english | 432 | 7284 | 10142 | -3998 |
| maximum_density_multilingual | 432 | 13176 | 10682 | -4538 |
| maximum_subjects_multilingual | 432 | 14360 | 10682 | -4538 |
| worst_permitted_sample | 432 | 14360 | 11938 | -5794 |

<a id="b-bdc98dbc1306-3"></a>

Worst permitted sampled output includes432 judgments,48 support records with two refs,
12 groups/72 memberships, two cardinality records, conditional/downstream/not-operationalized
markers on disjoint requirements and80-code-point high-token diagnostic labels. The maximum
multilingual subject input includes8 explicit subjects plus party. The ordinary multilingual
maximum already exceeds output cap without extreme labels. This is a demonstrated valid
counterexample to cap adequacy, not a universal upper bound over all Unicode strings.

<a id="b-bdc98dbc1306-4"></a>

Caps remain input14,000/output6,144/timeout90s; automatic repair/retry0. Maximum input14,360
exceeds by360. Maximum-density ordinary visible output10,142..10,682 exceeds by3,998..4,538,
before reasoning. Worst sampled visible output11,938 exceeds by5,794. Reasoning is unmeasured
and cannot make this fit. No requirement/candidate/relation truncation, changed omission
semantics, relation-limit reduction or automatic cap increase was used to claim success.

<a id="b-bdc98dbc1306-5"></a>

**Live gate failed.** The approved condition forbids live calls before sizing passes;
therefore targeted A/B/near-max were not run, and no valid new snapshot exists for the five
stability calls. Structural live validity is unmeasured (0 calls), not0% or100%. New final
sets, deterministic live traces, live CPU time, evaluator latency/usage, successful end-to-end
latency and agreement/Jaccard/inclusion statistics are all unavailable. Prior failed live
results remain previous-version evidence. New semantic quality cannot be inferred from
unit tests. No paid calls were spent on a known oversize contract.

<a id="m-cb56b1f1445a"></a>
## Offline validation

_Source context: B2 Historical Implementation and Development Checkpoints / Evaluator-contract reliability checkpoint: alias-only sparse judgments. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-cb56b1f1445a-0"></a>

- Initial focused contract/policy/integration checks:92 passed in4.61s.
- Complete backend suite, run once:644 passed,9 skipped in12.16s.
- Subsequent focused run exposed an existing integration-test timing assumption: it compared
  full planning results including set_selection.elapsed_seconds. Wall time is not a
  deterministic semantic result. Only that assertion was changed to exclude elapsed telemetry.
  No production clock or policy was changed to satisfy the test.
- Final focused contract/policy/integration/Foundry checks:99 passed in4.06s.
- Ruff: passed. Final git diff --check: passed.

<a id="b-cb56b1f1445a-1"></a>

Tests cover all six relations, omitted unknown versus explicit neutral, aliases and obsolete
identity rejection, same/conflicting duplicate pairs, maximum432 records, support ownership/
registered dimensions, inference-only coverage, group scopes/members/count bounds, compatible
relations+redundancy, label independence, compact/broad duplication, statuses/conflicts,
canonical ordering, unchanged policy expectations, source blindness and single-call behavior.
No tests call live providers; optional database integrations remain skipped.

<a id="m-056f304b066a"></a>
## Recommendation and stop

_Source context: B2 Historical Implementation and Development Checkpoints / Evaluator-contract reliability checkpoint: alias-only sparse judgments. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-056f304b066a-0"></a>

Recommendation: one further narrow evaluator payload/capacity decision before re-validation,
not B2 reconsideration or V1 re-freeze. A promising direction is more compact sparse judgment
encoding that preserves one alias identity system, omitted=unknown and all approved judgments;
measure its worst case before adopting it. Do not simply raise output cap, omit explicit
neutral judgments, reduce supported record count or change selection objectives without
review. A new representation must remain simpler than the bookkeeping contract it replaces.

<a id="b-056f304b066a-1"></a>

This task stops with a tested but maximum-capacity-blocked development contract. Current
authority in PROJECT, V1 design and POI selection was updated; historical B2 failures and
QCGRE/B1 findings were preserved. No implementation/live continuation is automatic.

<a id="m-cea18f9188d5"></a>
## Grouped sparse serialization checkpoint (offline only)

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-cea18f9188d5-0"></a>

Date: 2026-09-19. Authorized narrow representation optimization; implemented and tested.
No live Foundry/OpenAI/Google or other paid calls. No cap increase, relation/candidate/
requirement/evidence reduction, further name truncation, deterministic-policy changes,
TripWorld rebuild, embeddings, V2/V3, freeze, commit or push.

<a id="m-380c3cb38f84"></a>
## Exact grouped contract

_Source context: B2 Historical Implementation and Development Checkpoints / Grouped sparse serialization checkpoint (offline only). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-380c3cb38f84-0"></a>

The evaluator is semantic_evaluator_3; model projection is semantic_projection_3. The old
per-pair semantic_relations field is removed. The only relation-output representation is:

<a id="b-380c3cb38f84-1"></a>

```json
{
  "requirement_relations": [
    {
      "requirement_ref": "r0",
      "strong_match": ["c1", "c3"],
      "match": ["c4"],
      "weak_match": ["c5", "c7"],
      "neutral": ["c8"],
      "conflict": ["c9"]
    }
  ],
  "supports": [],
  "facet_groups": [],
  "redundancy_groups": [],
  "cardinality_preferences": [],
  "conditional_contributions": [],
  "downstream_only_requirements": [],
  "not_operationalized_requirements": []
}
```

<a id="b-380c3cb38f84-2"></a>

At most24 unique requirement rows,18 distinct candidate memberships per row,432 explicit
non-UNKNOWN judgments. Five bucket fields are required by the static strict DTO; arrays
may be empty. No unknown bucket exists or is accepted. Entirely unknown rows may be omitted;
an explicit empty row is also equivalent to all unknown and supplies no positive judgment.
The model is never required to enumerate the matrix or classify every pair.

<a id="b-380c3cb38f84-3"></a>

UNKNOWN means insufficient basis to judge and is represented by omission. NEUTRAL means
sufficient basis to judge neither meaningful alignment nor conflict and is explicitly
serialized. No neutral judgment is dropped to claim compression. Application initializes
all canonical cells to unknown, resolves each unique r alias, validates every c alias,
rejects repeated candidates within or across buckets, then writes each explicit judgment
into the canonical row. Duplicate rows reject even if identical. No precedence/merging/
repair chooses between conflicting buckets. Canonical ordering is application-owned.

<a id="b-380c3cb38f84-4"></a>

All original self-describing support/group/cardinality/conditional/status semantics and
bounds remain. Existing compatibility/scope/evidence checks remain. Semantic relations do
not become HARD passes, current official facts or Profile evidence. Support does not create
a positive relation automatically. Normalization yields the same CanonicalSemanticEvaluation
and unchanged semantic_set_1 policy. The selector file is byte-identical to the task baseline.

<a id="m-0623a7016a92"></a>
## Measured sequence and representation-only compaction

_Source context: B2 Historical Implementation and Development Checkpoints / Grouped sparse serialization checkpoint (offline only). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-0623a7016a92-0"></a>

Before modification, baseline schema1596 tokens, prompt464, maximum input14360 and maximum
ordinary multilingual visible output10682 were captured offline, alongside file hashes.
Grouped rows were measured BEFORE other representation changes:

<a id="b-0623a7016a92-1"></a>

- Schema1887, prompt512, input JSON12172 plus128 framing: input14699.
- Ordinary maximum multilingual visible output4803; high-token labels6059.
- In the6059 sample, supports1730 and facet groups2319 tokens together represented about67%
  of serialized output. This justified the explicitly conditional support/group compaction.

<a id="b-0623a7016a92-2"></a>

The grouped schema initially grew because the same candidate Literal enum was inlined in
five buckets and other structures. Shared named TypeAliasType definitions now emit one
CandidateRef and RequirementRef definition via $defs/$ref; there is no runtime schema builder.

<a id="b-0623a7016a92-3"></a>

Only after the measurements above, support/group repeated wire keys were shortened:

<a id="b-0623a7016a92-4"></a>

| Wire structure | Exact keys and lossless domain interpretation |
| --- | --- |
| supports | c=candidate_ref, r=requirement_ref, i=interpretation, e=support_alias_refs |
| facet_groups | r=requirement_ref, m=member_candidate_refs, l=label |
| redundancy_groups | r=requirement_ref, m=member_candidate_refs, l=label, t=allowed_before_penalty |

<a id="b-0623a7016a92-5"></a>

Alias values, complete label strings, members, interpretations and evidence refs are
unchanged. Domain fields remain descriptive; Foundry mapping restores them. Tests compare
round-tripped structured values and canonical state. No group label is omitted or shortened.
Cardinality/conditional/status serialization was left alone because it was not dominant.

<a id="b-0623a7016a92-6"></a>

After shared schema definitions and shorter wire keys: schema998/prompt568, maximum input
13866; ordinary maximum output4467, high-token-label output5723. To improve the134-token
input headroom losslessly, repeated subject-reference lists were interned once:

<a id="b-0623a7016a92-7"></a>

requirement.subject_set_ref -> requirement_subject_sets -> original subject_refs list.

<a id="b-0623a7016a92-8"></a>

This retains every subject, subject order, label and normalized requirement text. No candidate
facts, Profile dimensions/values/confidences or evidence alias strings were removed. Final
prompt582 includes the compact key/subject-table instructions; input JSON11655. Prompt tokens
increased relative to the per-pair contract, while schema and redundant input serialization
fell. No claim that every component shrank is made.

<a id="m-41dacde707cd"></a>
## Before/after sizing and remaining headroom

_Source context: B2 Historical Implementation and Development Checkpoints / Grouped sparse serialization checkpoint (offline only). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-41dacde707cd-0"></a>

Engineering input uses the actual strict DTO schema, exact system prompt/input JSON and128
framing allowance. Output is the actual compact wire encoding (by_alias=True), not the more
verbose domain/debug serialization. Fixtures are validated before measurement. Token counts
remain local engineering estimates; no provider/reasoning usage was measured in this task.

<a id="b-41dacde707cd-1"></a>

| Component at maximum subjects/multilingual | Per-pair | Final grouped |
| --- | ---: | ---: |
| Output schema | 1596 | 998 |
| System prompt | 464 | 582 |
| Input JSON | 12172 | 11655 |
| Framing allowance | 128 | 128 |
| Total engineering input | 14360 | 13363 |
| Ordinary maximum visible output | 10682 | 4467 |
| Previous high-token-label sample visible output | 11938 | 5723 |

<a id="b-41dacde707cd-2"></a>

Final input breakdown: global requirement context7300, candidate facts3332, Profile/evidence
aliases1034. These standalone fragments have slightly different JSON boundary tokens, so
sum the actual input JSON11655 rather than adding fragment counts as exact independent parts.
Group instructions account for211 of the582 prompt tokens; they are a subset, not an extra.

<a id="b-41dacde707cd-3"></a>

| Final fixture | Explicit judgments | Input | Visible output | Input headroom | Output headroom |
| --- | ---: | ---: | ---: | ---: | ---: |
| best_all_unknown | 0 | 3741 | 45 | 10259 | 6099 |
| typical_positive_sparse | 10 | 3741 | 276 | 10259 | 5868 |
| typical_explicit_neutral | 80 | 3741 | 486 | 10259 | 5658 |
| maximum_density_english | 432 | 6839 | 3927 | 7161 | 2217 |
| maximum_density_multilingual | 432 | 12731 | 4467 | 1269 | 1677 |
| maximum_subjects_multilingual | 432 | 13363 | 4467 | 637 | 1677 |
| full_density_distributed | 432 | 13363 | 4467 | 637 | 1677 |
| worst_permitted_sample | 432 | 13363 | 5723 | 637 | 421 |
| maximum_mixed_groups | 432 | 13363 | 5748 | 637 | 396 |
| maximum_redundancy_groups | 432 | 13363 | 5771 | 637 | 373 |

<a id="b-41dacde707cd-4"></a>

The full_density_distributed case distributes all432 non-UNKNOWN judgments across all five
buckets and reconstructs every cell exactly. It is not a mostly-unknown success case.
Maximum subjects include8 explicit subjects plus party. Normal maximum support/group fixtures
include48 support records/two refs each,12 groups/72 memberships and two cardinality records.
Additional high-token label cases exercise all facet, mixed facet/redundancy and all redundancy
structures, plus compatible conditional/downstream/not-operationalized markers. These are
legal representative stress cases, not a mathematical tokenizer upper bound over all Unicode.

<a id="b-41dacde707cd-5"></a>

Output component counts (standalone values; root keys/framing account for the remainder):

<a id="b-41dacde707cd-6"></a>

| Component | Ordinary maximum multilingual | High-token all-redundancy sample |
| --- | ---: | ---: |
| requirement_relations | 1898 | 1898 |
| supports | 1442 | 1442 |
| nonempty group array | 1063 | 2318 |
| cardinality | 25 | 25 |
| conditional/downstream/not-operationalized arrays | 1/1/1 | 16/16/19 |

<a id="b-41dacde707cd-7"></a>

All sampled visible serializations fit the6144 hard cap; maximum input leaves637 tokens
(4.55%). Ordinary maximum visible output4467 meets the approximately4500 diagnostic target
and leaves1677 for reasoning. HOWEVER the high-token label cases reach5723..5771, leaving
only421..373. This materially misses the diagnostic target and is not a comfortable or
proven reasoning budget. The problem has narrowed to diagnostic-label-heavy outputs plus
remaining support overhead, not loss of432-judgment capacity. No label loss, output truncation
or cap increase was used to declare success. Total generated-token fit remains unproven.

<a id="b-41dacde707cd-8"></a>

Typical10-positive output grew215->276 due to five bucket keys; full80-judgment typical output
fell1405->486 with explicit neutrals preserved. Grouping is a high-density improvement, not
a claim that every sparse payload is smaller. Empty output44->45 is also recorded honestly.

<a id="m-84476d83cc7b"></a>
## Cleanup and offline verification

_Source context: B2 Historical Implementation and Development Checkpoints / Grouped sparse serialization checkpoint (offline only). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-84476d83cc7b-0"></a>

Removed SparseRelation, FoundrySparseRelationDTO, semantic_relations per-pair output and its
normalization loop. No compatibility flag or legacy model-output adapter remains. Updated
fixtures emit grouped rows; previous sizing data is retained only as ignored measurements
and dated history. The retired test_sparse_semantic_contract.py was replaced by
 test_grouped_semantic_contract.py, migrating its evidence/group/status invariants and adding
bucket-specific tests. Current design docs no longer advertise the per-pair format.

<a id="b-84476d83cc7b-1"></a>

Focused grouped/evaluator/policy/acquisition/integration/Foundry tests:116 passed in4.30s.
Complete backend suite, run once:650 passed,9 skipped in9.02s. Ruff passed; final diff-check
passed. Optional database integration remains skipped. No providers were invoked by tests.

<a id="b-84476d83cc7b-2"></a>

Tests prove: all five explicit relation buckets; omitted pair/row -> unknown; explicit
neutral preserved; explicit unknown array forbidden; duplicate rows/in-bucket/cross-bucket
members rejected; unknown/noncanonical/numeric aliases rejected; full18x24 reconstruction;
shuffled rows and bucket membership yield identical canonical state and deterministic selected
set; support does not manufacture relations; evidence ownership and dimension isolation;
unchanged group/cardinality/status policy; lossless compact-wire and subject-set roundtrips;
source blindness; one-call boundary and no old-output repair.

<a id="m-f7db267390be"></a>
## Stop and recommendation

_Source context: B2 Historical Implementation and Development Checkpoints / Grouped sparse serialization checkpoint (offline only). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f7db267390be-0"></a>

No live calls were authorized in this pass, regardless of sizing results; none were made.
Input and ordinary full-density output blockers are resolved without reducing semantic
capacity. The remaining high-token-label diagnostic output lacks comfortable reasoning
headroom. Recommendation: one further representation-only headroom optimization/review
before broadly claiming readiness for targeted maximum-capacity live validation. Do not
reduce label/evidence/semantic capacity or raise caps automatically. This is not evidence
that the deterministic selector or B2 architecture should be reconsidered.

<a id="b-f7db267390be-1"></a>

Current caps remain14000 input/6144 total generated/90s; retries0. Historical dense/index live
failures and per-pair offline sizing failures remain intact. V1 is not re-frozen, TripWorld
Phases1-5 and V0 are unchanged, V2/V3 were not started, and no commits/push were performed.

<a id="m-e834107125d3"></a>
## Development budget recalibration and bounded live checkpoint (2026-09-19)

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-e834107125d3-0"></a>

This checkpoint supersedes the preceding recommendation to compress the representation
again. The grouped-sparse contract is accepted unchanged. Earlier 14,000 input / 6,144
combined generated-token ceilings were provisional engineering values, not research or
architectural requirements. The bounded task demonstrated legitimate output needs,
including reasoning. The approved response is additional execution headroom, not an
increasingly opaque contract or weaker validation.

<a id="m-46c121a7371c"></a>
## Deployment verification and execution settings

_Source context: B2 Historical Implementation and Development Checkpoints / Development budget recalibration and bounded live checkpoint (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-46c121a7371c-0"></a>

Before editing configuration, a read-only GET to the configured Foundry v1 model endpoint
returned HTTP 200, status succeeded, inference enabled, and model identity
`gpt-5.6-luna-2026-07-09`. The first sandbox attempt had a connection error; one network-enabled
metadata query succeeded. Neither request generated model content. The response identifies
the deployed model but does not itself advertise numeric context/output limits.

<a id="b-46c121a7371c-1"></a>

The exact model/version is documented by
[Microsoft Foundry model capabilities](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)
with 1,050,000 combined context, 922,000 input and 128,000 maximum output. The
[OpenAI model documentation](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
also specifies low reasoning support. Earlier actual project responses already used low
reasoning; this checkpoint subsequently confirmed request acceptance with the new output
ceiling. This is deployed-identity-plus-version-documentation verification, not an account
quota audit or a claim that a maximum-context request was empirically tested.

<a id="b-46c121a7371c-2"></a>

Development settings: input 32,000; generated output 16,384 (including provider-counted
reasoning); low reasoning; 90-second timeout; transport retries 0; automatic repair 0.
Combined proposed capacity is 48,384, within documented model capacity. These are safety
ceilings, not desired token usage or frozen production defaults. Prompt and schema are
unchanged. Genuine input overflow still rejects explicitly; no semantic truncation,
candidate dropping, or silent output recovery is introduced.

<a id="b-46c121a7371c-3"></a>

Only evaluator YAML/config validation changes; Requirement, Profile, itinerary and Official
Web task settings are unchanged. Capacities remain 18 candidates, 24 requirements, 432
judgments, 48 supports, 2 aliases/support, 12 groups, 72 memberships and 2 cardinality
records. Details/Reviews budgets, gates, unsupported-HARD treatment, and semantic_set_1
are unchanged. Runtime call count and problem size did not increase because of the cap.

<a id="m-362a2f2d2d41"></a>
## Offline sizing

_Source context: B2 Historical Implementation and Development Checkpoints / Development budget recalibration and bounded live checkpoint (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-362a2f2d2d41-0"></a>

Same fixtures, prompt, schema and text as the accepted grouped checkpoint. Measurements
are identical before/after; only headroom changes. HEALTHY here is a judgment based on
absolute practical margins, not a new runtime percentage threshold. No 4,500-token target
is imposed. All representative fixtures below are HEALTHY under the new development
budget. The largest sampled valid serialization is not a universal tokenizer upper bound.

<a id="b-362a2f2d2d41-1"></a>

| Fixture | Input | Visible output | Old input margin | Old output margin | New input margin | New output margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| best_all_unknown | 3741 | 45 | 10259 | 6099 | 28259 | 16339 |
| typical_positive_sparse | 3741 | 276 | 10259 | 5868 | 28259 | 16108 |
| typical_explicit_neutral | 3741 | 486 | 10259 | 5658 | 28259 | 15898 |
| maximum_density_english | 6839 | 3927 | 7161 | 2217 | 25161 | 12457 |
| maximum_density_multilingual | 12731 | 4467 | 1269 | 1677 | 19269 | 11917 |
| maximum_subjects_multilingual | 13363 | 4467 | 637 | 1677 | 18637 | 11917 |
| full_density_distributed | 13363 | 4467 | 637 | 1677 | 18637 | 11917 |
| worst_permitted_sample | 13363 | 5723 | 637 | 421 | 18637 | 10661 |
| maximum_mixed_groups | 13363 | 5748 | 637 | 396 | 18637 | 10636 |
| maximum_redundancy_groups | 13363 | 5771 | 637 | 373 | 18637 | 10613 |

<a id="b-362a2f2d2d41-2"></a>

Largest input: prompt582 + schema998 + JSON11655 + framing128 =13363. Remaining input18637.
Global context7300, candidate facts3332, Profile/aliases1034 are standalone fragment
measurements; their sum need not equal JSON tokens because token boundaries differ.
The 211 group-instruction tokens are included in the582 prompt tokens.
Largest output5771 leaves10613 for reasoning/additional provider framing under16384.
Output fragments: relations1898; supports1442; redundancy groups2318; empty facets1;
cardinality25; conditional16; downstream16; not-operationalized19. Root keys/framing
account for the remainder. Full mixed-five-bucket offline fixtures preserve all432 judgments.

<a id="b-362a2f2d2d41-3"></a>

Affected tests:119 passed in4.39s after correcting the overflow test from14001 to32001.
Initial focused run:118 passed/1 failed because that test still used the old boundary;
no runtime protection defect was discovered. Full backend suite run once:653 passed,
9 skipped in8.16s. Ruff and diff checks passed. No embeddings or database rebuilds.

<a id="m-bd45cbd10408"></a>
## Live scenarios and evidence

_Source context: B2 Historical Implementation and Development Checkpoints / Development budget recalibration and bounded live checkpoint (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-bd45cbd10408-0"></a>

Ignored artifact root: `logs/b2_budget_live_20260919/`. One A, one B, one near-max call,
then exactly five fresh evaluator calls against the successful B snapshot. All responses,
including A's invalid interpretation, were preserved. No model retry or repair.

<a id="b-bd45cbd10408-1"></a>

A: the approved three-adult Sydney/Opera House/architecture/local culture/distinctiveness/
anti-gimmick/redundancy/fewer-deeper/conditional-distance/public-transit request failed at
Requirement interpretation. Five semantic items had empty subject_refs; domain validation
requires at least one. FoundryInterpretationDTO currently exposes list[str] without that
minimum, while the domain has min_length=1. No Google or evaluator calls followed.
Requirement latency12.410s; run_v1 duration12.608s. This is an upstream contract-alignment
failure, not evaluator token exhaustion. Multi-traveler/facet/cardinality/conditional live
behavior is therefore not established by this run. No implementation fix was applied live.

<a id="b-bd45cbd10408-2"></a>

B: three-day Sydney/two-adult-one-child/required Opera House/less walking/avoid crowds/
family-friendly/unusual local culture/public-transit request completed in63.031s.
20 admitted,10 Details candidates,3 Reviews/Profile acquisitions; no failed Details.
Selected Sydney Opera House (`ChIJ3S-JXmauEmsRUcIaWtf4MzE`) and The Rocks Discovery Museum
(`ChIJ47iDxkKuEmsR_bma_SA7k1E`). Default cardinality;502 legal subsets; semantic_policy
origin; selection timer0.016s. Covers semantic_1 walking,semantic_3 family,semantic_4 local
culture; semantic_2 crowding unresolved. Required Opera House conflicts with walking and
remains selected; adding a lower-walking museum does not erase that conflict. No fallback.

<a id="b-bd45cbd10408-3"></a>

Decision trace: zero high/low-tier conflicts; medium tier has one conflicting requirement
and one conflict incidence (required Opera House), zero redundancy penalty, party positive
coverage3/3 active goals, one strong refinement and final size2. Full objective:
`[0,0,0,(),0,0,-1,-1,0,(Fraction(1,1),),3,0,0,0,0,(),0,0,0,1,0,-2]`.
The missing crowding evidence is not a positive match or proof of an uncrowded visit.

<a id="b-bd45cbd10408-4"></a>

Profiles: Opera House walking HIGH/medium confidence, family-friendly/low confidence;
Rocks museum walking LIGHT/medium and visit_duration SHORT/low; Artspace partial with no
usable signals. All crowding data missing. Walking support references only walking;
family support references only family. No duration/accessibility substitution for walking,
no missing Profile treated as negative, and no missing crowding treated as verified pass.
Open local-culture judgments rely on name/type and remain semantic inferences, not current
factual verification. A name/type support reference establishes traceability, not proof of
local authenticity/non-gimmickiness. Empty inference_only_requirement_ids in the current
trace must not be presented as proof that these semantic claims are factually verified.

<a id="b-bd45cbd10408-5"></a>

B end-to-end stages: Requirement8.755s; Profile3.670+2.493+3.504=9.667s;
evaluator8.024s; selection0.016s; itinerary19.387s. Google method durations plus
orchestration account for the remaining time. These are run_v1 timings, excluding process
startup; event clocks start earlier. This is not a controlled B1/B2 speed comparison.

<a id="b-bd45cbd10408-6"></a>

Generated itinerary is structurally successful but qualitatively limited: only two unique
POIs across three days, repeated visits, much flexible downtime, and an unsupported
family-friendly description of Rocks museum. Profile evidence was not passed to the
itinerary as factual family evidence. No V3 validation/repair or policy tuning was added.

<a id="b-bd45cbd10408-7"></a>

Near-max:18 candidates/24 requirements/maximum subjects/multilingual, engineering13363,
provider input13127, output2319 including reasoning516, completed in16.085s. Valid grouped
output with22 requirement rows/396 explicit judgments, no supports/groups. Missing rows
remain unknown. This validates actual transport and structure, not travel quality or live
emission of every maximum-density support/group combination. Offline fixtures cover432.

<a id="b-bd45cbd10408-8"></a>

All7 evaluator calls (B+near-max+five repeats) were completed and structurally/domain-valid,
with no incomplete/truncated responses. A had no evaluator call and is not in that denominator.

<a id="m-7962e13a119b"></a>
## Provider-reported evaluator usage

_Source context: B2 Historical Implementation and Development Checkpoints / Development budget recalibration and bounded live checkpoint (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-7962e13a119b-0"></a>

Visible output below is derived as total output minus reported reasoning, not a separate
provider visible-token field. Returned model for every evaluator call: gpt-5.6-luna.

<a id="b-7962e13a119b-1"></a>

| Call | Engineering input | Provider input | Visible derived | Reasoning | Output total | Total usage | Cache create/read | Seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| B | 3093 | 2857 | 333 | 509 | 842 | 3699 | 2854/0 | 8.024 |
| stress | 13363 | 13127 | 1803 | 516 | 2319 | 15446 | 11659/1465 | 16.085 |
| repeat_1 | 3093 | 2857 | 246 | 504 | 750 | 3607 | 0/2854 | 8.479 |
| repeat_2 | 3093 | 2857 | 198 | 516 | 714 | 3571 | 0/2854 | 7.699 |
| repeat_3 | 3093 | 2857 | 300 | 359 | 659 | 3516 | 0/2854 | 6.636 |
| repeat_4 | 3093 | 2857 | 287 | 516 | 803 | 3660 | 0/2854 | 8.264 |
| repeat_5 | 3093 | 2857 | 394 | 494 | 888 | 3745 | 0/2854 | 8.200 |

<a id="b-7962e13a119b-2"></a>

Actual calls stayed far below the new ceiling; a larger cap does not imply larger usage or
higher latency. Five repeat inputs exactly match B hash
`4bd1d8debc90f28f59713a9d131b1637e0fe0431edaefbb157b32a8a859b8ba8`.
No Google, Details or Reviews were repeated for stability.

<a id="m-f1f011e9b8c2"></a>
## Fixed-input stability and deterministic replay

_Source context: B2 Historical Implementation and Development Checkpoints / Development budget recalibration and bounded live checkpoint (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f1f011e9b8c2-0"></a>

Five fresh evaluator calls:5/5 structurally valid. Selected sets:
1. Opera House + Rocks museum.
2. Opera House + Rocks museum.
3. Opera House + Rocks museum + Sydney Culture Walks.
4. Opera House + Rocks museum + Sydney Culture Walks.
5. Opera House + Rocks museum.

<a id="b-f1f011e9b8c2-1"></a>

All40 candidate/requirement cells (including UNKNOWN) have mean pairwise agreement85.5%.
Restricting each pair to cells where either run is non-UNKNOWN, mean agreement is27.44%:
shared unknowns otherwise inflate apparent consistency. Support-record-set mean Jaccard
is64.39%, using exact requirement/candidate/interpretation/sorted-alias tuples. Group and
cardinality outputs are identical empty arrays5/5, which does not validate non-empty-group
stability. Status differs: not_operationalized r1/r3 in repeat2, r1 in repeat5, none otherwise.

<a id="b-f1f011e9b8c2-2"></a>

Selected-set pairwise exact agreement4/10 (40%); modal set3/5; original B set reproduced3/5.
Mean pairwise Jaccard0.8 (range2/3..1). Inclusion: Opera House5/5, Rocks museum5/5,
Sydney Culture Walks2/5, all seven other candidates0/5. The same facts yield family
weak_match vs match and open-culture weak/match/strong/unknown variations; those relation
changes cross the deterministic policy's existing coverage boundary. No policy was tuned.

<a id="b-f1f011e9b8c2-3"></a>

One identical canonical B evaluation replayed10 times gives identical semantic result,
selected IDs, objective and snapshot hash, excluding elapsed-time telemetry. Per replay
wall time3.12-3.68ms. Process CPU timer resolution is coarse on Windows: aggregate31.25ms
for10 calls (about3.125ms/call); individual0 readings do not mean zero work. Live policy
elapsed times0-16ms are wall timers, not precise per-call CPU measurements.

<a id="m-522aa6a0a7cb"></a>
## Calls, scope, recommendation

_Source context: B2 Historical Implementation and Development Checkpoints / Development budget recalibration and bounded live checkpoint (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-522aa6a0a7cb-0"></a>

13 model calls total:2 Requirement,3 Profile,7 evaluator,1 itinerary. Google19 provider
method calls:4 text searches (destination+named/discovery),10 Details,3 Reviews,1 Weather,
1 route matrix. No Official Web search/page/reasoner calls were required. These are
instrumented provider-method counts, not a packet-level HTTP audit. Metadata: one successful
read-only lookup plus the initial sandbox connection failure; no generation charge.

<a id="b-522aa6a0a7cb-1"></a>

No live implementation fixes; only pre-live budget/config/tests/sizing updates. No prompt,
projection, evaluator schema, deterministic selection, acquisition, V0 or TripWorld changes.
No V2/V3, re-freeze, commits, pushes, embeddings, DB rebuilds or thesis-note writes.

<a id="b-522aa6a0a7cb-2"></a>

Recommendation: **needs one narrow fix**, beginning with Requirement transport/domain
subject attribution alignment and focused offline tests. Do not infer missing subjects from
keywords or automatically repair the failed run. B2 need not be discarded based on this
checkpoint, but V1 is not ready to re-freeze. Semantic-label variability, name/type evidence
limitations and three-day itinerary under-selection/repetition remain explicit review items;
they are not authorized implementation changes. Development ceilings remain provisional
until later production-budget review. Stop here; no further model calls or next-phase work.

<a id="m-e278491d273d"></a>
## Bounded offline candidate-supply decision study (2026-09-19)

_Source context: B2 Historical Implementation and Development Checkpoints. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-e278491d273d-0"></a>

Hypothesis: **minimal semantic coverage may have been incorrectly treated as adequate
planning candidate supply.** This study changes no production policy, prompt, schema,
acquisition, runtime budget, or version behavior. Only the saved successful Scenario B
and its five frozen-input outputs are used. No providers, model calls, embeddings or
DB operations. This is an engineering decision check, not a benchmark or thesis conclusion.

<a id="m-8da69326cd7c"></a>
## Frozen evidence and limitations

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-8da69326cd7c-0"></a>

`B_projection.pkl` contains the interpreted contract, all10 canonical enriched candidates,
normalized Details, three Profiles, RequirementAssessments, evidence ledger, required/
excluded IDs, acquisition order and selection maximum8. Original evaluation/selection and
five repeat results contain canonical judgments and objective traces. B_started stores the
actual evaluator execution config; current policy is semantic_set_1. A derived readable
snapshot is in ignored `artifacts/research/selection_objective/normalized_snapshot.json`; its provenance
is the original pickle hash, not reconstructed facts. Results and complete manifest are
in ignored `artifacts/research/selection_objective/report.json`.

<a id="b-8da69326cd7c-1"></a>

Important missing raw artifacts: the old capture harness overwrote tool payload files with
the same method name. Only the last raw Search, Details and Profile payload files survive.
Normalized evidence for all10 enriched candidates and all3 Profiles is preserved in the
pickle, and event counters preserve the funnel. All41 raw search observations and full
normalized records for the24 non-enriched unique POIs are not available. Counts below are
trace-reported, not recomputed from a complete raw response archive. This prevents claims
about the quality of upstream omissions, but does not block the10-candidate decision study.
Raw tool files have sensitive request headers; their contents are not copied into this
report or the derived snapshot. Only hashes are recorded. No original artifacts were edited.

<a id="b-8da69326cd7c-2"></a>

Exact source paths and SHA-256:

<a id="b-8da69326cd7c-3"></a>

| Absolute path | SHA-256 |
| --- | --- |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_projection.pkl` | `9ba0763514fae547951ecc25c571a8e465743ae32a9578fe22366a6d406c1c9a` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_result.json` | `d80491a678520dfaee0304ebdc87f5477fde4af4c970eef3e0356b85de4c291b` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_evaluation.json` | `7aa540908e07c34d54eee21296daf2e3d07e44669b5f2c775d059e7e9709c7b8` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_events.json` | `4e77c9fed5ecdf454982ca18a4385aee4ea9b6ea8f9fc8b6d3a93d6568a3340c` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_selection.json` | `88ef095ea4b2a3d0f9d1b9d51b49ec92901e1e7c4d938e23fe605e653b2715f1` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_started.json` | `3cd593b6ae5e67418b9e45180667a795a5939b3d665023357d514c2411da4983` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_snapshot_metadata.json` | `9a41f400796b13c59fc3e0baebdab9d7d29a5b502e341f83d3c5c7a3c6eb8f09` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_exact_evaluator_input.json` | `4bd1d8debc90f28f59713a9d131b1637e0fe0431edaefbb157b32a8a859b8ba8` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_projection_context.json` | `5fa9b0c4177355c8f2b6bcd9ca0093d0aa824fcdf623811af78404c6412a752e` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_model_calls.json` | `4a9f3082056863334f576253a3d98e92cd5e00bb2293f34e39560f12617c9550` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_tools_google_places_details.json` | `512908cbff387d3a7e1069101ad0f7c334b5e7fbd038e6b2ac96b4ca03786d22` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_tools_google_places_search_text.json` | `9b84d32192166bcd799afdbd0c9880aa1d7a4c4c384cae496b61c1164986789d` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\B_evidence_v1_experience_profile.json` | `491eb319819e5d4509cb3c152cee77f7a691f841e521555e66beb92cb687ce28` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_1_result.json` | `0507c98c81715da5b88e3dac696b0af4038259790ef0285762f32c234878fc88` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_2_result.json` | `18bfab29137132e78ca0927e007c7e106d6a919cbe4215d6e2166a6549a90ef7` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_3_result.json` | `b85f2cb87da49022ce1b2cd73400cc31976958c0946f22728bc3c096e28ef71d` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_4_result.json` | `32c0d501bbcb9987dea12db6ea241b935ff32b44ce053d876043ed7e31fc2766` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_5_result.json` | `070d240698e5634d8cc67bf59c9eca3cf9d0b89498a18bf6c5d68099935b8983` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_1_exact_evaluator_input.json` | `4bd1d8debc90f28f59713a9d131b1637e0fe0431edaefbb157b32a8a859b8ba8` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_2_exact_evaluator_input.json` | `4bd1d8debc90f28f59713a9d131b1637e0fe0431edaefbb157b32a8a859b8ba8` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_3_exact_evaluator_input.json` | `4bd1d8debc90f28f59713a9d131b1637e0fe0431edaefbb157b32a8a859b8ba8` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_4_exact_evaluator_input.json` | `4bd1d8debc90f28f59713a9d131b1637e0fe0431edaefbb157b32a8a859b8ba8` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\logs\b2_budget_live_20260919\repeat_5_exact_evaluator_input.json` | `4bd1d8debc90f28f59713a9d131b1637e0fe0431edaefbb157b32a8a859b8ba8` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\backend\app\policies\semantic_set_selection.py` | `8381296546c9dba65f38d9e4f7d7aaabd8c7cd4a2e85f6d93a0adc1a38a1675d` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\config\runtime.yaml` | `b007a0f41150ea7e43b430d77904cb5877f6f74f5d90f4a4a005b3653893a662` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\backend\app\versions\v1\graph.py` | `22da931f2b74e47f7141bc1e0fe02d3b3b31c543136ccb335d8859633a5c0732` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\backend\app\versions\v1\prompts.py` | `9db6b71c40e53734117dbd9deef901c9aa41dd519b074170ed1e22c845bd9a29` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\backend\app\services\evidence_acquisition.py` | `2440f89ebd65f68b4c97fd7cbc1eda717395dfdf05fd13bb530c652e9f20c1ec` |
| `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent\backend\app\versions\v1\official_web.py` | `2cc6f7e9c5409283cdfe19958ff4853ce13166323a7c6b117ea38e572f856ea8` |

<a id="m-d0aa7ea609c4"></a>
## Actual downstream contract: C, mixed / ambiguous

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-d0aa7ea609c4-0"></a>

The selector and Official Web preserve required canonical IDs separately, but the itinerary
prompt receives only TravelRequirements, original user text and undifferentiated Place
facts. In this B snapshot TravelRequirements.required_activities is empty; the REQUIRED
Opera House is present in interpreted named_places and selection metadata, but that typed
ledger is not separately projected into the generation prompt. The original request still
instructs the model to visit it. No structured output rule verifies required-ID coverage.

<a id="b-d0aa7ea609c4-1"></a>

No current prompt or output schema requires all selected POIs to appear. Ordinary POIs may
be omitted without violating a declared all-selected-visit rule. However, there is also no
explicit optional-pool contract; naming such as 'final selected POIs' and undifferentiated
place evidence is ambiguous. Activity has place_name/location but no canonical place_id;
output validation checks dates/times/IDs, not supplied-candidate inclusion or mandatory
visits. Therefore this is neither a clean mandatory set nor a fully specified optional pool.

<a id="b-d0aa7ea609c4-2"></a>

Sources: versions/v1/graph.py::generate_evidence_informed_itinerary;
versions/v1/prompts.py::build_itinerary_generation_prompt and system prompt;
schemas/itinerary.py; versions/v1/official_web.py::project_official_web_inputs.

<a id="b-d0aa7ea609c4-3"></a>

Routes takes every selected place with usable coordinates and requests the full directed
N by N grid, including diagonals. Current2 points requested4 elements. An8-point pool
would request64 elements:16x the elements, still one request at current64/request and
256/run limits, assuming all coordinates/timezone inputs remain usable. This is a request
shape estimate, not a new route observation or priced invoice. WALK alternatives are
separately bounded; B uses explicit TRANSIT. Official Web gap planning inspects each
selected POI but only acquires tasks for actual gaps/needs; required/named IDs affect
priority. More inspected POIs does not mean8 paid searches. Existing caps6 tasks/6 page
fetches remain; exact extra tasks are not asserted. Weather uses destination and dates,
not POI count. More candidates also enlarge planner evidence and tokens.

<a id="b-d0aa7ea609c4-4"></a>

Minimum future contract clarification: expose required_canonical_ids separately from
optional planning candidate IDs and say explicitly that ordinary candidates may be omitted,
whereas required visits must be honored or their inability disclosed. The existing itinerary
schema permits omission already; no shared V0 schema change is necessary for that freedom.
A V1-only canonical activity reference would improve traceability if separately approved;
this study does not add enforcement, scheduling validation or V3 repair. Retain bounded
all-pairs Routes initially rather than inventing a second scheduling/model pass; explicitly
accept its element cost. Official Web retains need-driven acquisition and required priority.

<a id="m-0d02b280ec3e"></a>
## Funnel and candidate identities

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-0d02b280ec3e-0"></a>

41 Google POI observations (named1 + discovery20 + default20; destination lookup excluded)
->34 unique canonical POIs ->20 admitted ->10 Details attempts ->10 successful normalized
Details ->10 factual-gate-eligible enriched POIs ->10 evaluator candidates ->2 selected.
14 canonical candidates missed admission;10 admitted candidates were outside the enrichment
target. Neither group is proven unusable. The enriched10 are all eligible; zero identity,
Details, provider-budget or factual-gate failures occurred among these10.

<a id="b-0d02b280ec3e-1"></a>

| Index | Canonical ID | Name | Type | Rating |
| ---: | --- | --- | --- | ---: |
| 0 | `ChIJ13oNdG2uEmsR4KSealVEbxs` | Artspace | association_or_organization | 4.5 |
| 1 | `ChIJ3S-JXmauEmsRUcIaWtf4MzE` | Sydney Opera House | performing_arts_theater | 4.8 |
| 2 | `ChIJ47iDxkKuEmsR_bma_SA7k1E` | The Rocks Discovery Museum | museum | 4.4 |
| 3 | `ChIJ68aBlEKuEmsRHUA9oME5Zh0` | Museum of Contemporary Art Australia | art_museum | 4.3 |
| 4 | `ChIJCZ5rATyuEmsRcAjUsjLzbGU` | Customs House | historical_landmark | 4.5 |
| 5 | `ChIJFRY_smmuEmsR_KsiZoS75Gw` | Justice and Police Museum | museum | 4.5 |
| 6 | `ChIJG_XjmW2uEmsRQFRYqzt9KYs` | Finger Wharf | historical_landmark | 4.6 |
| 7 | `ChIJPVqlfGyuEmsRHPcnCX1X1OE` | Art Gallery of New South Wales | art_gallery | 4.7 |
| 8 | `ChIJSytgJF2uEmsRC6q8BDZh5qA` | BridgeClimb Sydney | tourist_attraction | 4.7 |
| 9 | `ChIJWYOIy-ivEmsR5u1M18ce9pw` | Sydney Culture Walks | tourist_attraction | 5.0 |

<a id="b-0d02b280ec3e-2"></a>

Only1 (Opera House) is REQUIRED. All10 have genuine discovery_1 QueryIntentHit associations
with the extracted query 'Unusual local cultural places in Sydney'; this is acquisition
relevance, not verified local/non-gimmicky experience. Stored ranks/result counts are used
as provenance only by the two study alternatives.

<a id="m-447a981ce39c"></a>
## Method and self-checks

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-447a981ce39c-0"></a>

One script: scripts/analyze_b2_decision.py. A Python line trace observes each legal mask's
objective inside the unchanged production function; it does not monkeypatch or edit it.
All six original production outputs are replayed exactly, excluding elapsed telemetry.
An independent tie implementation reproduces all six winners. Each output has502 legal
sets. Within each fixed size remove the last cardinality objective, preserving all other
lexicographic components, geography, conditional rating and ID ties. Assertions restrict
this observer to the actual default/non-fallback case; it is not a general replacement
selector.48 frontier rows satisfy size, required/excluded and eligibility checks. Each
supply pool preserves the original optimum non-cardinality objective. Comparator legal
masks are independently enumerated without evaluator data and match the factual legal set.

<a id="b-447a981ce39c-1"></a>

Focused checks are embedded in the one analysis script. Ruff passes after fixing loop
closure bindings and explicit zip strictness; no production fixes. No full backend suite
was run. Source hashes are checked unchanged after execution.

<a id="m-2eb8a0761433"></a>
## Original fixed-size frontier

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-2eb8a0761433-0"></a>

Indices refer to the canonical table above. All HIGH/LOW-tier conflict/redundancy/coverage
values are0 with empty subject vectors. All rows below retain one MEDIUM conflicting
requirement and one conflict incidence (Opera House/walking), zero redundancy and zero
facets. Only party is present; no multi-traveler fairness evidence exists in B.

<a id="b-2eb8a0761433-1"></a>

| Size | Best set | Party fairness | Positive requirements | Raw strong/match/weak pairs | Unknown pairs | Max pair / sum-center metres | Semantic ties before geography |
| ---: | --- | --- | ---: | --- | ---: | --- | ---: |
| 1 | [1] | ['1/3'] | 1 | 0/1/0 | 2 | 0/929 | 1 |
| 2 | [1, 2] | ['1'] | 3 | 1/2/0 | 4 | 646/1342 | 1 |
| 3 | [1, 2, 5] | ['1'] | 3 | 1/2/1 | 7 | 660/1767 | 8 |
| 4 | [1, 2, 3, 5] | ['1'] | 3 | 1/2/1 | 11 | 677/2053 | 28 |
| 5 | [1, 2, 3, 4, 5] | ['1'] | 3 | 1/2/2 | 14 | 687/2358 | 56 |
| 6 | [1, 2, 3, 4, 5, 8] | ['1'] | 3 | 1/2/2 | 18 | 698/2893 | 70 |
| 7 | [1, 2, 3, 4, 5, 8, 9] | ['1'] | 3 | 1/3/2 | 21 | 1344/3547 | 56 |
| 8 | [1, 2, 3, 4, 5, 7, 8, 9] | ['1'] | 3 | 1/3/2 | 25 | 1546/4704 | 28 |

<a id="b-2eb8a0761433-2"></a>

Raw relation-pair counts are not additive policy reward: one requirement covered several
times counts once; weak/unknown earn no positive coverage. Every size2..8 has the identical
21-component pre-cardinality objective, including one strong-match refinement. Size1 loses
at party fairness/coverage. Sizes3..8 lose only at component22 (zero-based21), -size; they
never reach the cross-size geography/rating tie. Within each fixed size geography leaves
exactly one winner; rating is technically eligible but never changes a winner here.

<a id="b-2eb8a0761433-3"></a>

For EACH excluded enriched candidate0,3,4,5,6,7,8,9, adding it to the original two keeps all
pre-size objectives equal. The first loss is component22. Primary loss reason for all8:
cardinality/minimum-set preference. Missing new coverage/facets explains why there is no
earlier reward; it is not factual ineligibility. No semantic conflict, redundancy,
subject-fairness or rating loss caused their original exclusion. At an8-point supply cap,
0 Artspace and6 Finger Wharf lose the geography tie; that is a separate later decision.

<a id="m-d845811f0c28"></a>
## Five-output fixed-size frontiers and semantic variation

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-d845811f0c28-0"></a>

| Size | Repeat1 | Repeat2 | Repeat3 | Repeat4 | Repeat5 | Mean pairwise Jaccard |
| ---: | --- | --- | --- | --- | --- | ---: |
| 1 | [1] | [1] | [1] | [1] | [1] | 1.0000 |
| 2 | [1, 2] | [1, 2] | [1, 2] | [1, 2] | [1, 2] | 1.0000 |
| 3 | [1, 2, 5] | [1, 2, 5] | [1, 2, 9] | [1, 2, 9] | [1, 2, 5] | 0.7000 |
| 4 | [1, 2, 3, 5] | [1, 2, 3, 5] | [1, 2, 3, 9] | [1, 2, 3, 9] | [1, 2, 3, 5] | 0.7600 |
| 5 | [1, 2, 3, 4, 5] | [1, 2, 3, 4, 5] | [1, 2, 3, 4, 9] | [1, 2, 3, 4, 9] | [1, 2, 3, 4, 5] | 0.8000 |
| 6 | [1, 2, 3, 4, 5, 8] | [1, 2, 3, 4, 5, 8] | [1, 2, 3, 4, 5, 9] | [1, 2, 3, 4, 5, 9] | [1, 2, 3, 4, 5, 8] | 0.8286 |
| 7 | [1, 2, 3, 4, 5, 8, 9] | [1, 2, 3, 4, 5, 8, 9] | [1, 2, 3, 4, 5, 8, 9] | [1, 2, 3, 4, 5, 8, 9] | [1, 2, 3, 4, 5, 8, 9] | 1.0000 |
| 8 | [1, 2, 3, 4, 5, 7, 8, 9] | [1, 2, 3, 4, 5, 7, 8, 9] | [1, 2, 3, 4, 5, 7, 8, 9] | [1, 2, 3, 4, 5, 7, 8, 9] | [1, 2, 3, 4, 5, 7, 8, 9] | 1.0000 |

<a id="b-d845811f0c28-1"></a>

Inclusion frequencies per size (omitted indices are0/5):

<a id="b-d845811f0c28-2"></a>

- Size1: 1=5/5.
- Size2: 1=5/5, 2=5/5.
- Size3: 1=5/5, 2=5/5, 5=3/5, 9=2/5.
- Size4: 1=5/5, 2=5/5, 3=5/5, 5=3/5, 9=2/5.
- Size5: 1=5/5, 2=5/5, 3=5/5, 4=5/5, 5=3/5, 9=2/5.
- Size6: 1=5/5, 2=5/5, 3=5/5, 4=5/5, 5=5/5, 8=3/5, 9=2/5.
- Size7: 1=5/5, 2=5/5, 3=5/5, 4=5/5, 5=5/5, 8=5/5, 9=5/5.
- Size8: 1=5/5, 2=5/5, 3=5/5, 4=5/5, 5=5/5, 7=5/5, 8=5/5, 9=5/5.

<a id="b-d845811f0c28-3"></a>

All outputs have one conflict requirement/incidence and zero redundancy/facets at every
size. Party fairness / positive coverage by sizes1..8:

<a id="b-d845811f0c28-4"></a>

| Output | Fairness vector (one party ratio per size) | Positive coverage by size |
| --- | --- | --- |
| original | 1/3, 1, 1, 1, 1, 1, 1, 1 | 1, 3, 3, 3, 3, 3, 3, 3 |
| repeat_1 | 0, 1/3, 1/3, 1/3, 1/3, 1/3, 1/3, 1/3 | 0, 1, 1, 1, 1, 1, 1, 1 |
| repeat_2 | 0, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2 | 0, 1, 1, 1, 1, 1, 1, 1 |
| repeat_3 | 1/3, 2/3, 1, 1, 1, 1, 1, 1 | 1, 2, 3, 3, 3, 3, 3, 3 |
| repeat_4 | 0, 2/3, 2/3, 2/3, 2/3, 2/3, 2/3, 2/3 | 0, 2, 2, 2, 2, 2, 2, 2 |
| repeat_5 | 1/3, 2/3, 2/3, 2/3, 2/3, 2/3, 2/3, 2/3 | 1, 2, 2, 2, 2, 2, 2, 2 |

<a id="b-d845811f0c28-5"></a>

Repeat3's size2 loses to size3 on fairness/positive coverage; repeat4's size2 loses to size3
on the strong-match refinement. Their sizes4..8 then tie their3-point optima on every
non-size objective and lose on -size. Repeat1/2/5 reproduce the minimum-size mechanism.
Evaluator variation therefore affects coverage/status denominators, match strength and
small-set inclusion; it does not change redundancy (always empty). At sizes7 and8,
all five frontiers coincide. Not-operationalized local-culture in repeat2 changes the
fairness denominator; cross-output fractions are not directly comparable satisfaction scores.

<a id="m-b227a2bbdb56"></a>
## Exactly one supply-oriented counterfactual

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b227a2bbdb56-0"></a>

Definition, offline only: eligible/required/excluded constraints unchanged, capacity8 from
the saved configuration. Admit optional members only with a stored link to a positive
DiscoveryIntent; that is a defensible search-based option rationale, not certified semantic
satisfaction. Maximize the existing full non-cardinality semantic vector FIRST. Among tied
optima maximize the number of these qualified alternative identities, then use unchanged
geography/rating/ID ties. Do not add unrelated POIs merely to reach8. Adding a candidate
that worsens any earlier objective is rejected even if capacity is unfilled. In this
snapshot all10 are discovery-linked, so supply count is the operative tie-break; this is
an explicit diagnostic assumption, not proof that every search hit is useful.

<a id="b-b227a2bbdb56-1"></a>

All six outputs produce [1,2,3,4,5,7,8,9]. No higher-priority semantic tradeoff is required;
all preserve their own current non-cardinality optimum. Their claimed coverage differs
substantially despite identical8-point pools. All pool members have normalized usable
Details, valid coordinates, acceptable business/date state and no exclusion; eligibility
is not a guarantee of every requested experience or schedule feasibility.

<a id="b-b227a2bbdb56-2"></a>

Additional members relative to original [1,2]:

<a id="b-b227a2bbdb56-3"></a>

| Index | Stored additional rationale | Evaluator contribution in original | Limit/risk |
| ---: | --- | --- | --- |
| 3 MCA | discovery_1 hit; art_museum; rating4.3; geographic tie | UNKNOWN, no extra goal | Museum type is not proof of different experience |
| 4 Customs House | discovery hit; historical_landmark; rating4.5; geographic tie | local-culture weak_match; no coverage reward | Name/type inference; no authenticity proof |
| 5 Justice and Police Museum | discovery hit; museum; rating4.5; geographic tie | local-culture weak_match; no coverage reward | May overlap museum experience; no redundancy evidence |
| 7 Art Gallery NSW | discovery hit; art_gallery; rating4.7; geographic tie | UNKNOWN, no extra goal | Different provider type is not proven semantic diversity |
| 8 BridgeClimb | discovery hit; tourist_attraction; rating4.7; geographic tie | UNKNOWN, no extra goal | No walking Profile; less-walking fit remains unknown |
| 9 Sydney Culture Walks | discovery hit; tourist_attraction; rating5.0; geographic tie | local-culture match, already covered by2 | Name/type inference; walking/crowding remain unknown |

<a id="b-b227a2bbdb56-4"></a>

No added member creates a recorded conflict/redundancy penalty. Missing evidence is not
proof of absence of conflict or repetition. None of these additions has newly acquired
Profile support. No opening-hour advantage, indoor/outdoor claim, route feasibility,
local popularity, or schedule fit is asserted. Ratings are stored but did not decide
these frontier ties. The counterfactual supplies alternatives, not mandatory visits.

<a id="m-05db5d43bdda"></a>
## Evaluator incremental value, separately from quantity

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-05db5d43bdda-0"></a>

- Walking conflict at1 and positive at2: useful distinction, category E (already in typed
  Profile facts), not unique to an extra evaluator. All five maintain conflict at1 and
  match/strong at2. A simple registered mapping of LIGHT/HIGH to the already structured
  less-walking request preserves this distinction; it needs no raw-text NLP.
- Family at1: legitimate low-confidence Profile evidence, but weak in repeats1/2/4 and
  match in3/5. Category C (unstable), with E (fact already provided). Threshold crossing
  changes reported coverage although REQUIRED ensures1 is always retained.
- Crowding: absent in all Profiles. Category E for preserving unknown, with C for toggling
  normal unknown vs not_operationalized in2/5. No positive no-crowd evidence is invented.
- Local culture: category B (plausible semantic association), C (unstable) and D if treated
  as verified authenticity/non-gimmickiness. Candidate9 ranges from weak, omitted/not-
  operationalized, match, strong, weak. Candidate2's local-cultural relation also changes.
  The judgments distinguish the small sets but add no membership distinction at size8.
  A name/type citation is not factual support for unusual/local/non-gimmicky claims.
- Traveler-specific distinctions, redundancy/facet groups and conditional contribution:
  not exercised in this B snapshot. No category-A uniquely useful evaluator distinction
  is established here; this does not prove those capabilities can never be useful.

<a id="b-05db5d43bdda-1"></a>

Removing the evaluator loses its open-culture interpretation, match-strength refinements
and operationalization labels. It does not lose Google facts, typed Profiles, discovery
associations or the structured original semantic requirements. The simple comparison still
uses the previously saved Requirement/Profile LLM results: 'non-LLM' here means no extra
Semantic Evaluator, not an entirely model-free pipeline.

<a id="m-38d931e1301f"></a>
## Small deterministic comparison (not QCGRE restoration)

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-38d931e1301f-0"></a>

One fixed definition from the same pool: same factual constraints and discovery-linked
option eligibility; minimize typed walking HIGH conflict count; maximize distinct supported
walking LIGHT / family-friendly dimensions for this snapshot's registered requests; retain
qualified alternatives up to8; maximize distinct non-null provider primaryTypes; apply
same geography/rating/ID tie. No raw text parsing, invented ranks, category-to-experience
inference, learned weights or new preference fields. Profile confidence remains available;
using a supported dimension does not promote it to verified satisfaction. These mappings
are diagnostic for the stored typed walking/family requests, not an implemented general
operationalization registry. Crowding stays unknown.

<a id="b-38d931e1301f-1"></a>

Result [0,1,2,3,4,5,7,9]: Opera House, Rocks museum, Artspace, MCA, Customs House, Justice
and Police Museum, Art Gallery NSW, Sydney Culture Walks. Seven members overlap with B2's
supply8; Jaccard7/9=0.7778. Artspace replaces BridgeClimb because type diversity precedes
geography. This supplies7 distinct stored primaryTypes versus6 in B2; provider categories
are a coarse diversity proxy, not proof of seven unique experiences. Both retain the same
known walking/family evidence and the same unavoidable required walking conflict; neither
verifies crowding or local authenticity. Counterfactual geography max1626m/sum5598m versus
B2 max1546m/sum4704m: an explicit small diversification/geography tradeoff, not routed distance.
The result supports similar factual candidate supply without evaluator judgments; it does
not establish equal itinerary quality or superior user satisfaction.

<a id="b-38d931e1301f-2"></a>

Historical full QCGRE replay skipped. Genuine provider_rank/actual_result_count/QueryIntentHit
and ratings/Profiles DO exist for these10, so missing ranks is not the reason. Historical
experience_selection.py requires controlled ExperiencePreferenceIntent/preference/importance
inputs, which are absent from this open-contract snapshot. Reconstructing them would insert
new semantic mappings and would not be a faithful full QCGRE replay. No E=0 fallback or
invented old preferences were used. The simple declared comparator is sufficient here.

<a id="m-201beea27fe2"></a>
## Causal conclusion and decision

_Source context: B2 Historical Implementation and Development Checkpoints / Bounded offline candidate-supply decision study (2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-201beea27fe2-0"></a>

Q1: primarily A (minimum-set/cardinality policy), with C as a secondary limitation (sparse
incremental semantic distinctions). Exact original replay proves all8 excluded candidates
can be added without worsening pre-size objectives. B is not the cause of the original
2-point result. D remains unassessed outside the preserved10, not an explanation established
by this study. Upstream truncation exists but is not needed to explain the observed2.

<a id="b-201beea27fe2-1"></a>

Q2: evaluator-specific incremental value is not established for this saved case. Its robust
walking distinctions are recoverable from typed evidence; nuanced local-cultural judgments
are variable and weakly grounded; the richer supply sets converge without requiring those
judgment differences. The simple deterministic comparison preserves similar evidence and
candidate supply. This is an engineering recommendation with one-case limitations, not a
claim that LLM semantic selection generally fails.

<a id="b-201beea27fe2-2"></a>

**Recommendation: OPTION B -- return to deterministic metric-led POI selection**, preserving
open requirements, source/subject identity, canonical facts, registered Profile evidence and
budgets. Do not restore old QCGRE byte-for-byte. Merely changing B2's size preference would
fix the measured shortage but has not justified the evaluator's additional role/cost.

<a id="b-201beea27fe2-3"></a>

Smallest next production direction, only after approval: a bounded deterministic supply
selector over the existing enriched pool; explicit required-vs-optional planner projection;
retain uncertainty and bounded acquisition; remove mandatory evaluator dependence from
that main path. Before implementation approve the finite evidence mappings and supply
policy rather than automatically shipping this diagnostic comparator. No broad operator
or scoring-framework redesign. The earlier subject_refs DTO/domain issue remains separate.

<a id="b-201beea27fe2-4"></a>

One bounded next validation plan for approval: frozen B replay plus a small fake-evidence
suite covering required/excluded, missing Profile, walking conflict, distinct types vs
redundancy, insufficient eligible supply, and budget/required-optional projection. No model
calls or new scenarios in this task. Any later live confirmation needs separate explicit
authorization. No day-filling, POIs/day, itinerary-density score, V3 repair or refreeze.

<a id="m-8cf001d14449"></a>
## B1 Development Validation Record (2026-09-18 to 2026-09-19)

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8cf001d14449-0"></a>

Historical development evidence, not current runtime authority or formal benchmark.
B1 has been retired from the active V1 path by the approved B2 migration. Earlier
recommendations to continue B1 fixes below are dated decisions, superseded by B2.
Current architecture: [POI selection](development_record.md). Chronology and decision rationale:
[POI selection evolution](development_record.md).

<a id="b-8cf001d14449-1"></a>

The original implementation sections are consolidated into the evolution record and
current contract. The following offline/live measurements, attempted fixes, failures,
limitations and original dated decisions are retained without presenting them as B2 results.
Historical file names in these sections refer to the B1 working tree, not live interfaces.

<a id="m-5cf981b07b18"></a>
## Historical pre-compaction offline validation and live stop

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-5cf981b07b18-0"></a>

- Full backend: **688 passed, 9 skipped** (6.46 seconds in the final recorded run).
- Ruff: passed. `git diff --check`: passed (Git also reports ordinary CRLF/LF notices).
- Fake-model tests cover open meanings, subject attribution, source occurrence/Unicode,
  exact dedup and links, HARD preflight, REQUIRED/EXCLUDED identity, stage projections,
  rank/source-independent serialization, invalid IDs/citations/review links, flexible
  count, unique-set bypass, shared repair/fallback, no active QCGRE, reserves inside the
  Details budget, downstream evidence flow, and V0/date regressions.
- Unit tokenization is mocked so a clean checkout needs no network/download. Actual
  sizing below runs separately with the checksum-verified real offline vocabulary.
- No live extraction examples, live choice-quality findings, measured live latency,
  reasoning usage, stability/Jaccard, clarification rate, or paid cost are available.
  Offline fakes are not evidence of natural-language extraction quality.

<a id="b-5cf981b07b18-1"></a>

The historical tokenizer preparation utility (now `scripts/prepare_tokenizer.py`) downloaded once for the public, SHA-256-verified
o200k vocabulary in ignored `.cache/tokenizer`. This preparatory download is not
a model API call. Runtime token counting cannot silently download missing assets.
The retired B1 payload sizing utility produced the following historical engineering measurements. The historical B2 sizing tool has been retired.

<a id="b-5cf981b07b18-2"></a>

Final sizing (system prompt + input JSON + domain output schema + 128-token framing
allowance; engineering estimates, not provider billing or a certified model tokenizer):

<a id="b-5cf981b07b18-3"></a>

| Fixture | Stage A / 12,000 | Stage B / 10,000 |
| --- | ---: | ---: |
| No semantic requirements | 4,497 | 2,787 |
| Four typical semantic requirements, six rich Profiles | 5,764 | 6,872 |
| 24 requirements / 6,000 semantic code points | 8,684 | **10,952** |
| Same with 256-character English names | 9,476 | **11,348** |
| Same with 256-character multilingual names | **16,568** | **14,894** |

<a id="b-5cf981b07b18-4"></a>

Fixtures include 36 Stage A candidates, 18 Stage B candidates, eight subjects where
applicable, linked discovery/evidence requests, assessments and up to six five-dimension
Profiles. A large bounded output fixture uses 3,022 tokens; this is not proof that all
valid outputs fit. These failing inputs do not even exhaust all named-place/information/
evidence-link bounds. Therefore the approved valid-input space demonstrably exceeds
the provisional input ceilings. No claims of complete worst-case coverage are made.

<a id="b-5cf981b07b18-5"></a>

**The approved instruction requires stopping before live validation at this blocker.**
No OpenAI/Foundry/Google paid or live provider calls were made, and no cap was increased
or semantic meaning silently removed. Small live extraction/selection/stability/end-to-end
validation remains pending. Existing TripWorld data, embeddings and database are untouched.

<a id="m-82c70fe9f519"></a>
## Historical pre-compaction recommendations

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-82c70fe9f519-0"></a>

Do not re-freeze V1 yet. First approve a revised prompt projection/size policy. Prefer
removing repeated evidence/reference metadata from model-visible projections while
retaining full provenance outside the prompt; separately decide an explicit display-name
bound/representation for long multilingual names. If the complete approved semantic
contract still cannot fit, approve explicit larger stage caps or a smaller admission
policy with acknowledged recall implications. Do not solve this by dropping preferences.

<a id="b-82c70fe9f519-1"></a>

After that decision: re-size, run affected offline checks, then authorize a concrete
bounded live matrix (fixed snapshots for repeated selector calls; no repeated Google
acquisition for stability runs). Selection quality, latency, stochastic stability,
clarification burden and possible underfilling remain unvalidated. There is no formal
V0/V1/V2 comparison, no V2-specific selector branch, and no re-freeze recommendation yet.

<a id="m-2e8ef6b1ed8c"></a>
## File impact

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2e8ef6b1ed8c-0"></a>

- New contracts: `schemas/interpreted_requirements.py`, `schemas/poi_selector.py`,
  `schemas/revised_v1_result.py`.
- New policy/services: `policies/interpreted_requirements.py`,
  `services/poi_selector.py`, `services/semantic_poi_pipeline.py`.
- New offline tokenizer/setup/sizing: `runtime/token_counting.py`,
  `scripts/prepare_tokenizer.py`, the retired B1 payload sizing utility.
- Adapted: Foundry client/DTO, V1 graph/state/prompts/runner/official-Web projection,
  review Profile acquisition method, historical acquisition docstrings, runtime config,
  numeric usage redaction, dependency manifest/lock.
- Tests: new open-contract/selector/safety cases; migrated V1 graph, identity, integration,
  runner and trace fixtures; strict DTO tests; offline-only tokenizer fixture.
- Documentation: PROJECT, V1 design/milestone, architecture review and this report;
  explicitly requested ignored V1A-14 development-history note. No ignored note was staged.

<a id="b-2e8ef6b1ed8c-1"></a>

All implementation changes are uncommitted; new source/test/script/report files remain
untracked until a separately authorized commit. Generated logs/vocabulary remain ignored.

<a id="m-7c9cf6c49aca"></a>
## Approved payload compaction checkpoint - 2026-09-18

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7c9cf6c49aca-0"></a>

**Current status:** compaction implemented and offline validated; awaiting user review
and separate live authorization. The earlier size blocker and 688-test checkpoint above
are historical. The user additionally authorized modest token-cap increases. V1 remains
unfrozen; Architecture B, HARD clarification policy, one interpreter, two selector stages,
one shared repair, V0 behavior, TripWorld baseline and paused V2 integration are unchanged.

<a id="m-22cf8d60e66b"></a>
## Canonical state versus model projection

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Approved payload compaction checkpoint - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-22cf8d60e66b-0"></a>

`policies/selector_projection.py` owns `SelectorProjection`. Only its `context` goes to
the model. `SemanticSelection` retains both projection sidecars, canonical requirement
objects, candidate facts/query provenance, full Profiles, full assessment snapshots and
the candidate-local evidence ledger. No canonical name, ID, source span or Profile is
rewritten. These are in-memory application records, not a new persistent database.

<a id="b-22cf8d60e66b-1"></a>

Both stages preserve every semantic item, complete normalized_text, kind, polarity,
strength, scope and subject_refs. No semantic shortening, keyword interpretation,
merging across travelers or dropping of low-priority meanings was introduced.

<a id="b-22cf8d60e66b-2"></a>

| Model field / previous repetition | Current projection | Full application owner |
| --- | --- | --- |
| Source quotes, occurrence, offsets, request hash | Not serialized | Canonical requirement contract |
| Assessment capability, predicate/version, scope, verbose evidence refs | requirement_id -> [evidence_state, disposition, check_result] | Full RequirementAssessment snapshot |
| Repeated candidate association arrays | Exact repeated sets interned in association_groups; candidate references group alias; unique sets remain inline | Original links/canonical requirements; lossless group expansion |
| Repeated subject information | One global ledger, original labels and stable subject IDs | Canonical subjects with source spans |
| Stage A per-candidate rating state/value and Profile null/state | Omitted; globally not_acquired | Canonical candidate/Details and Profiles if supplied |
| Stage B rating state/value | [state,value] | PlaceSelectionInput |
| Full Profile, summary, review references/count, duplicate place ID | experience.state and dimension -> [value,confidence] | Original ExperienceProfile, including summary and all refs |
| Verbose candidate evidence reference lists | Candidate-local f or a present dimension name in output citations | evidence_ledger[place_id][alias] |
| Latitude/longitude keys | One ordered coordinates pair, unchanged numeric values | Original candidate/Details facts |
| Null not_visitable_before | Omitted if absent; retained when known | Eligibility result |
| Provider rank, query source and other discovery provenance | Never model-visible | Candidate/query history and application pool |
| Requested current-information acquisition records | Not in selector view; remain available to the existing Web subsystem | Canonical requested_place_information |
| Empty legacy preferences/activity arrays, empty unresolved_fields, null trip fields | Omitted from trip view | Original TravelRequirements |

<a id="b-22cf8d60e66b-3"></a>

The factual gate still owns eligibility. A compact assessment never grants model authority
to verify a condition. `check_result=unknown` remains unknown after Review support arrives.
Missing dimensions and unacquired Profiles remain unknown, not negative evidence. Stage A
cannot see rich evidence even if passed rich objects. Stage B does not receive raw reviews.
Profile summary is omitted because the existing evidence contract exposes five bounded
review dimensions; this may lose incidental narrative nuance and needs live evaluation.
Unsupported open semantics still survive in requirements, without invented evidence.

<a id="b-22cf8d60e66b-4"></a>

Citation aliases are scoped by the decision's canonical place_id. `f` refers to supplied
observed facts; a dimension alias is valid only when that candidate has that signal.
Validation rejects borrowed candidate references and absent dimension citations. The full
review-reference chain remains inspectable outside the prompt. Citation validation checks
reference ownership, not entailment of a model rationale.

<a id="b-22cf8d60e66b-5"></a>

Coordinates retain geographic position and conditional distance tradeoffs remain in
semantic text. There were no pairwise-distance/neighborhood duplicates to remove; no
radius, walking threshold, routing promise or new geographic policy was invented.

<a id="m-9975a0ab13f0"></a>
## Display names, caps and output bounds

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Approved payload compaction checkpoint - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-9975a0ab13f0-0"></a>

Canonical names and IDs remain complete. Only display_name is a Unicode-code-point prefix
of at most 160 characters, with name_truncated explicitly true/false. Unicode grapheme
clusters may still cross the boundary. Identical prefixes never merge candidates. The
prompt tells the selector a prefix is incomplete; lost suffix cues are a known tradeoff.

<a id="b-9975a0ab13f0-1"></a>

The largest measured combined subject/link fixture gives:

<a id="b-9975a0ab13f0-2"></a>

| Display-name limit | Stage A tokens | A headroom at 14,000 | Stage B tokens | B headroom at 11,000 |
| --- | ---: | ---: | ---: | ---: |
| None | 15,475 | -10.5% | 10,812 | 1.7% |
| 160 | 12,415 | 11.3% | 9,282 | 15.6% |
| 128 | 11,407 | 18.5% | 8,778 | 20.2% |
| 96 | 10,363 | 26.0% | 8,256 | 24.9% |

<a id="b-9975a0ab13f0-3"></a>

160 is the least aggressive tested bound meeting the approximately 10% diagnostic margin
at the modest chosen ceilings. Stage A increases 12,000 -> 14,000 (+16.7%); Stage B
10,000 -> 11,000 (+10%). Config validation maxima match these ceilings. Output stays
4,096; reasoning stays low; timeout stays 90 seconds; provider retries stay zero.
Two normal selector calls and one request-shared repair remain the maximum call pattern.
Candidate admission, shortlist, final selection and acquisition budgets are unchanged.
Raising a ceiling does not pad normal prompts or add API calls; no paid cost was measured.

<a id="b-9975a0ab13f0-4"></a>

Output diagnostic records are sparse: at most six selected-candidate records, four linked
requirements and two local citations each, and 80-character English rationale. Previously
these were 18 records, 24 requirement refs, five refs and 120 characters. Selection and
reserve ID bounds remain 18, review nominations six, requirement considerations 24.
This reduces explanation duplication, not the requirements visible to the selector or
the permitted selected set. No explanations for rejected candidates are requested.

<a id="m-b3205b41da51"></a>
## Reproducible measurements

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Approved payload compaction checkpoint - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-b3205b41da51-0"></a>

The retired B1 payload sizing utility uses the existing checksum-verified cached
o200k vocabulary without networking. the retired frozen B1 sizing fixture freezes the
old projection/prompt/schema for comparisons; it is never imported by application code.
Generated JSON is in ignored `logs/selector_compaction_sizing.json` and is reproducible.
Counts include system prompt, input JSON, domain output schema and 128 framing tokens.
They are engineering estimates, not actual Foundry wire/billing/reasoning usage.

<a id="b-b3205b41da51-1"></a>

Fixtures use 36 Stage A candidates, 18 Stage B candidates, up to six full five-dimensional
Profiles with summary and five references per signal, 24 requirements totaling 6,000
semantic characters, eight subjects, and 256-character English/multilingual names.
maximum_links uses eight discovery intents totaling 1,200 characters, 120 evidence links,
and all 24 candidate associations. combined_representative_max adds synthetic 27-character
canonical IDs; maximum_subject_links also uses 100-character labels and all nine subject
references per semantic item. Source text is synthetic sizing data, not extraction evidence.

<a id="b-b3205b41da51-2"></a>

| Fixture | Stage | Before | After (160) | New-cap headroom |
| --- | --- | ---: | ---: | ---: |
| empty | A | 4,497 | 3,460 | 75.3% |
| empty | B | 2,787 | 2,780 | 74.7% |
| typical | A | 5,764 | 4,039 | 71.2% |
| typical | B | 6,872 | 3,579 | 67.5% |
| maximum_semantics | A | 8,684 | 5,979 | 57.3% |
| maximum_semantics | B | 10,952 | 5,479 | 50.2% |
| long_names | A | 9,476 | 6,339 | 54.7% |
| long_names | B | 11,348 | 5,659 | 48.6% |
| multilingual_long_names | A | 16,568 | 10,803 | 22.8% |
| multilingual_long_names | B | 14,894 | 7,891 | 28.3% |
| maximum_links | A | 12,836 | 6,371 | 54.5% |
| maximum_links | B | 18,992 | 5,871 | 46.6% |
| combined_representative_max | A | 21,576 | 11,623 | 17.0% |
| combined_representative_max | B | 35,584 | 8,490 | 22.8% |
| maximum_subject_links | A | 22,368 | 12,415 | 11.3% |
| maximum_subject_links | B | 36,376 | 9,282 | 15.6% |

<a id="b-b3205b41da51-3"></a>

Component breakdown for maximum_subject_links (other fixtures and all name alternatives
are in the reproducible JSON):

<a id="b-b3205b41da51-4"></a>

| Component | A before | A after | B before | B after |
| --- | ---: | ---: | ---: | ---: |
| system_prompt | 243 | 445 | 243 | 445 |
| schema | 540 | 540 | 540 | 540 |
| global_context | 5836 | 3849 | 21676 | 3805 |
| candidate_core | 15186 | 7451 | 8862 | 3864 |
| profile_increment | 432 | 0 | 4924 | 498 |
| framing_allowance | 128 | 128 | 128 | 128 |
| json_bpe_boundary_delta | 3 | 2 | 3 | 2 |
| total | 22368 | 12415 | 36376 | 9282 |
| per_candidate_core_mean | 421.8 | 207.0 | 492.3 | 214.7 |

<a id="b-b3205b41da51-5"></a>

Candidate core is the whole candidate array excluding Profile fields; profile_increment
is the difference with those fields restored. BPE boundary delta reconciles separately
counted fragments with actual concatenation. Global context now contains shared alias
sets and evidence-request groups; its growth can accompany a larger candidate reduction.

<a id="b-b3205b41da51-6"></a>

| Large valid output fixture | Tokens | Headroom at 4,096 |
| --- | ---: | ---: |
| A / english | 1,531 | 62.6% |
| A / multilingual | 1,897 | 53.7% |
| B / english | 1,005 | 75.5% |
| B / multilingual | 1,371 | 66.5% |

<a id="b-b3205b41da51-7"></a>

Output fixtures cover maximum stage selection/reserve/nomination counts, six rationale
records, four requirement links each, candidate-valid citations and 24 considerations.
English and multilingual 80-character rationales are measured; English remains requested.
These measurements are not proof over the entire permissible output space: unusually
long canonical IDs or high-token-density text may exceed the cap. Provider reasoning
also shares output resources differently from these serialized-output estimates.

<a id="m-417e793633af"></a>
## Validation, scope and remaining limits

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Approved payload compaction checkpoint - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-417e793633af-0"></a>

- Focused selector/safety tests: 31 passed; new projection tests: seven passed.
- Full backend suite run exactly once for this compaction pass: **695 passed, 9 skipped**
  (7.65 seconds). Skipped tests require the optional live database environment.
- Ruff passed; final whitespace/diff check recorded after documentation updates.
- Added checks for exact preservation of semantics/subjects, 120 linked dimensions,
  hidden provenance, retained full Profiles/assessments, Stage A isolation, candidate-local
  citations, Unicode name/identity safety, unchanged coordinates, deterministic association
  interning and unchanged selection bounds despite smaller diagnostic output.
- No live model/provider calls, vocabulary downloads, embedding regeneration, database
  rebuilds, paid operations, commits, pushes or branch switches during this pass.
- No V0 implementation changes, V2 runtime integration, V3 work, thesis archive updates,
  candidate-cap reductions, HARD policy changes, extra parser or scoring fallback.

<a id="b-417e793633af-1"></a>

Changed by this pass: selector_projection.py; semantic_poi_pipeline.py; poi_selector.py
schema/service; runtime config/model; sizing script and frozen baseline; projection,
open-selector and semantic-safety tests; this report and current-status/projection notes
in PROJECT, V1 design/milestone and the architecture review. Earlier dirty implementation
files remain part of the preceding approved reopen, not newly introduced by compaction.

<a id="b-417e793633af-2"></a>

All requested representative input fixtures now retain at least approximately 10% margin.
This does not guarantee every schema-valid request fits: maximum named-place records,
many long IDs, token-dense non-English semantic text, or arbitrary label combinations can
still overflow. Runtime rejects overflow explicitly; it never drops semantic requirements
to squeeze a request in. The input gate's framing estimate is not an exact transport bound.

<a id="b-417e793633af-3"></a>

Recommendation: review these measurements, then separately authorize a small bounded live
validation covering deployment acceptance, alias comprehension, truncated names, Profile
nuance, output/reasoning budget and choice stability. Passing offline sizing does not
establish selection quality, cost or live readiness and does not automatically authorize
that next step. Stop here; do not re-freeze V1.

<a id="m-a992ba62c554"></a>
## LIVE DEVELOPMENT VALIDATION - 2026-09-18

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a992ba62c554-0"></a>

**Development validation only; not a formal benchmark, thesis result, or V1 re-freeze.**
The authorized matrix is complete. Recommendation: **focused fixes before re-freeze**.
One of two end-to-end attempts completed. No extra scenarios or manual retries were run.

<a id="m-d5bc86224dc5"></a>
## Matrix, configuration and evidence location

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-d5bc86224dc5-0"></a>

- Five direct Requirement LLM calls: cases A-E below.
- Two fresh end-to-end attempts: the open-semantics family request (A) and review-linked
  family request. Each ran once; the first failure was not replaced.
- Five fresh Stage A and five fresh Stage B calls on smoke2 frozen inputs, without
  Google, acquisition, selector-result caching or repair prompts. Direct calls use the
  same existing Foundry binding and deterministic validator. Invalid outputs remain
  invalid observations; they do not trigger additional calls. Repair/fallback behavior
  was observed separately through the normal smoke graph.
- One Stage B compaction stress call with four requirements, eight subjects, repeated
  association aliases, 18 distinct synthetic IDs and multilingual 256-character names
  projected to 160 code points. No quality inference is drawn from this synthetic case.
- Actual reference date: 2026-09-18, Australia/Sydney. Trip dates: 2026-09-20 to 2026-09-22.
- Live interval begins 2026-09-18 13:46 UTC; all recorded calls completed that day.
  Per-call UTC timestamps and response identifiers remain in ignored artifacts.
- Configured deployment and every returned model identifier: `gpt-5.6-luna`.
- Selector policy `semantic_selector_2`, projection `selector_projection_2`, requirement
  contract `interpreted_requirements_1`; strict Foundry DTO via Responses API.
- Provisional development-only selector caps: input A 14,000 / B 11,000 engineering tokens,
  output 4,096, reasoning low, timeout 90 seconds, transport retries zero. No configuration
  values were changed by this validation; these are not frozen production policy.
- Ignored artifact root: `logs/selector_live_20260918/`. It contains the one-off harness,
  normalized results, exact selector input strings, configuration, prompt/schema hashes,
  traces, per-call metadata and analysis. No secrets or authorization headers are included.
  `replay_manifest.json` also retains the actual Foundry transport schema and options.

<a id="b-d5bc86224dc5-1"></a>

The five initial extraction records preserve input/output/total usage, but the generic
redactor removed nested token-detail dictionaries before persistence. Their reasoning
and cache breakdowns are therefore unavailable in retained evidence, not zero. The
one-off observer was corrected to flatten numeric reasoning/cache counters before later
calls. No paid calls were repeated to repair this measurement loss. Application code
was not changed. These counters are available for every subsequent model call.

<a id="m-75c40f8e2e6b"></a>
## Direct extraction cases and manual semantic review

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-75c40f8e2e6b-0"></a>

The exact requests, canonical objects, source offsets, subjects, strengths, scopes,
discovery/evidence links, issues and hashes are in `extractions.json`. All five canonical
source-span checks passed. Manual review is separate from schema validation.

<a id="m-56578e4845bc"></a>
## Extraction A

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18 / Direct extraction cases and manual semantic review. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-56578e4845bc-0"></a>

Request: Plan a Sydney trip from 2026-09-20 to 2026-09-22 for four people. This is a family trip. We definitely want to visit Sydney Opera House. My mother prefers quiet places; my father likes architecture. We prefer places that feel local rather than touristy, and unusual experiences but not gimmicky attractions. Avoid choosing several museums that all feel the same. We would rather visit fewer places in depth than rush. We are willing to travel farther only for something genuinely distinctive. We mainly use public transport.

<a id="b-56578e4845bc-1"></a>

Request SHA-256: `5d51b643e2d76dbb3519ceba94ccd1fc905c9e09a25e4f1c9f732515d5fe65ce`.

<a id="b-56578e4845bc-2"></a>

Named operational records: Sydney Opera House -> REQUIRED (named_1).

<a id="b-56578e4845bc-3"></a>

Subjects: mother=mother, father=father.

<a id="b-56578e4845bc-4"></a>

| ID | Canonical normalized text | Kind / polarity / strength / scope | Subject | Exact source [start,end) |
| --- | --- | --- | --- | --- |
| semantic_1 | The trip is for a family. | constraint / favor / medium / whole_trip | party | This is a family trip. [66,88) |
| semantic_2 | My mother prefers quiet places. | preference / favor / high / individual_poi | mother | My mother prefers quiet places; [137,168) |
| semantic_3 | My father likes architecture. | preference / favor / medium / individual_poi | father | my father likes architecture. [169,198) |
| semantic_4 | Prefer places that feel local rather than touristy. | preference / favor / high / selected_poi_set | party | We prefer places that feel local rather than touristy, [199,253) |
| semantic_5 | Prefer unusual experiences. | preference / favor / medium / individual_poi | party | unusual experiences [258,277) |
| semantic_6 | Avoid gimmicky attractions. | preference / avoid / high / individual_poi | party | not gimmicky attractions. [282,307) |
| semantic_7 | Avoid choosing several museums that all feel the same. | constraint / avoid / high / selected_poi_set | party | Avoid choosing several museums that all feel the same. [308,362) |
| semantic_8 | Prefer visiting fewer places in depth rather than rushing. | preference / favor / high / itinerary_style | party | We would rather visit fewer places in depth than rush. [363,417) |
| semantic_9 | Travel farther only for something genuinely distinctive. | constraint / favor / high / itinerary_style | party | We are willing to travel farther only for something genuinely distinctive. [418,492) |

<a id="b-56578e4845bc-5"></a>

Discovery intents: discovery_1: Local, unusual Sydney experiences that do not feel touristy or gimmicky (semantic_4, semantic_5, semantic_6); discovery_2: Sydney architecture experiences and architecturally significant places (semantic_3); discovery_3: Genuinely distinctive Sydney experiences worth travelling farther for (semantic_9).

<a id="b-56578e4845bc-6"></a>

Experience evidence requests: none. Extraction issues: [].

<a id="m-c443a5436eac"></a>
## Extraction B

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18 / Direct extraction cases and manual semantic review. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-c443a5436eac-0"></a>

Request: Plan a Sydney trip from 2026-09-20 to 2026-09-22 for four people. Absolutely no stairs. This is non-negotiable. We mainly use public transport.

<a id="b-c443a5436eac-1"></a>

Request SHA-256: `0e87ae2921c339e6c477d032d3407e28f56bbbc8982d47df21cbf5bb8d277f38`.

<a id="b-c443a5436eac-2"></a>

Subjects: implicit party only.

<a id="b-c443a5436eac-3"></a>

| ID | Canonical normalized text | Kind / polarity / strength / scope | Subject | Exact source [start,end) |
| --- | --- | --- | --- | --- |
| semantic_1 | The party must avoid all stairs; this is non-negotiable. | constraint / avoid / hard / whole_trip | party | Absolutely no stairs. This is non-negotiable. [66,111) |
| semantic_2 | The party mainly uses public transport. | preference / favor / medium / transport | party | We mainly use public transport. [112,143) |

<a id="b-c443a5436eac-4"></a>

Discovery intents: none.

<a id="b-c443a5436eac-5"></a>

Experience evidence requests: none. Extraction issues: [].

<a id="m-359713640eea"></a>
## Extraction C

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18 / Direct extraction cases and manual semantic review. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-359713640eea-0"></a>

Request: Plan a Sydney trip from 2026-09-20 to 2026-09-22 for four people. We definitely want to visit Sydney Opera House, and we do not want to visit Taronga Zoo. We mainly use public transport.

<a id="b-359713640eea-1"></a>

Request SHA-256: `58d12a664a966c9666043499e49895c6b4cdac4e1c7038eead92716c13b13e72`.

<a id="b-359713640eea-2"></a>

Named operational records: Sydney Opera House -> REQUIRED (named_1); Taronga Zoo -> EXCLUDED (named_2).

<a id="b-359713640eea-3"></a>

Subjects: implicit party only.

<a id="b-359713640eea-4"></a>

No SemanticRequirements; named meanings are not duplicated as preferences.

<a id="b-359713640eea-5"></a>

Discovery intents: none.

<a id="b-359713640eea-6"></a>

Experience evidence requests: none. Extraction issues: [].

<a id="m-85d5cbc6fa04"></a>
## Extraction D

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18 / Direct extraction cases and manual semantic review. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-85d5cbc6fa04-0"></a>

Request: Plan a Sydney trip from 2026-09-20 to 2026-09-22 for four people. We prefer unusual places but not gimmicky attractions, and places with historical character but not typical tourist traps. We are willing to travel farther only for something genuinely distinctive.

<a id="b-85d5cbc6fa04-1"></a>

Request SHA-256: `433080a66690708286822e675ba5caf0756a2524f8001bb069e7d67d7290e174`.

<a id="b-85d5cbc6fa04-2"></a>

Subjects: implicit party only.

<a id="b-85d5cbc6fa04-3"></a>

| ID | Canonical normalized text | Kind / polarity / strength / scope | Subject | Exact source [start,end) |
| --- | --- | --- | --- | --- |
| semantic_1 | Favor unusual places for the party. | preference / favor / medium / selected_poi_set | party | prefer unusual places [69,90) |
| semantic_2 | Avoid gimmicky attractions for the party. | preference / avoid / medium / selected_poi_set | party | not gimmicky attractions [95,119) |
| semantic_3 | Favor places with historical character for the party. | preference / favor / medium / selected_poi_set | party | places with historical character [125,157) |
| semantic_4 | Avoid typical tourist traps for the party. | preference / avoid / medium / selected_poi_set | party | not typical tourist traps [162,187) |
| semantic_5 | The party is willing to travel farther only for something genuinely distinctive; do not treat farther travel as independently preferred. | constraint / favor / high / itinerary_style | party | We are willing to travel farther only for something genuinely distinctive. [189,263) |

<a id="b-85d5cbc6fa04-4"></a>

Discovery intents: discovery_1: Unusual places in Sydney with historical character (semantic_1, semantic_3).

<a id="b-85d5cbc6fa04-5"></a>

Experience evidence requests: none. Extraction issues: [].

<a id="m-33a9f2333d14"></a>
## Extraction E

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18 / Direct extraction cases and manual semantic review. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-33a9f2333d14-0"></a>

Request: Plan a Sydney trip from 2026-09-20 to 2026-09-22 for four people. My mother prefers quiet places, my father likes architecture, and my sister prefers lively markets. These are preferences, not absolute requirements.

<a id="b-33a9f2333d14-1"></a>

Request SHA-256: `18bb9f15b1182d027bf357b6c8bf4bf5f0b416e7cadb044007f3820c23a771bd`.

<a id="b-33a9f2333d14-2"></a>

Subjects: mother=Mother, father=Father, sister=Sister.

<a id="b-33a9f2333d14-3"></a>

| ID | Canonical normalized text | Kind / polarity / strength / scope | Subject | Exact source [start,end) |
| --- | --- | --- | --- | --- |
| semantic_1 | The mother favors quiet places; this is a preference rather than an absolute requirement. | preference / favor / medium / selected_poi_set | mother | My mother prefers quiet places [66,96) |
| semantic_2 | The father favors places with notable architecture; this is a preference rather than an absolute requirement. | preference / favor / medium / selected_poi_set | father | my father likes architecture [98,126) |
| semantic_3 | The sister favors lively markets; this is a preference rather than an absolute requirement. | preference / favor / medium / selected_poi_set | sister | my sister prefers lively markets [132,164) |

<a id="b-33a9f2333d14-4"></a>

Discovery intents: discovery_1: Quiet places and peaceful attractions in Sydney (semantic_1); discovery_2: Architecturally notable places and buildings in Sydney (semantic_2); discovery_3: Lively markets in Sydney (semantic_3).

<a id="b-33a9f2333d14-5"></a>

Experience evidence requests: none. Extraction issues: [].

<a id="b-33a9f2333d14-6"></a>

Manual findings:

<a id="b-33a9f2333d14-7"></a>

- A retains family context, mother's quiet preference, father's architecture interest,
  local/non-touristy and unusual/non-gimmicky meanings, museum redundancy, fewer/deeper
  visits and the conditional distance tradeoff. No named-place duplicate reward or lost
  negation was observed. Strength normalization is not perfectly grounded: mother=high
  and father=medium despite no explicit relative priority. The distance condition remains
  intact, although an additional discovery query links it despite the prompt's usual
  selector-only guidance. Neither creates a mechanical radius.
- B retains the genuinely non-negotiable stairs constraint as hard. Assessment capability
  remains semantic_only, evidence not_acquired, result unknown, disposition clarify;
  there is no registered verifier. It also duplicates public transport into a semantic
  record and typed transport field. This is duplicate exposure, not a numeric double
  reward (there is no scoring), and merits a focused extraction-contract follow-up.
- C correctly separates Opera House REQUIRED from Taronga Zoo EXCLUDED; no semantics are
  duplicated. This direct check does not prove live Google identity resolution/exclusion,
  because no discovery was performed for C.
- D preserves both negatives and the conditional distance relationship. E keeps mother,
  father and sister distinct; no cross-person merge was observed. 'Notable architecture'
  in E is a slight interpretation of 'likes architecture', not new evidence about venues.
- No other missing preference, invented activity or suspicious HARD classification was
  observed in these five direct outputs. This small manual inspection is not a quality rate.

<a id="b-33a9f2333d14-8"></a>

For B, the already acquired live draft was replayed into the actual V1 graph with counting
fail-fast provider guards. It returned `ClarificationRequired: unsupported_hard_requirements`
at extraction/preflight. **Google/provider invocations: 0**. This replay adds no live LLM
call or trip scenario and demonstrates the boundary using a real interpreted result.
UNKNOWN was not promoted to PASS; accessibility was not used to certify no stairs.

<a id="m-e22a00efc59b"></a>
## Two end-to-end attempts

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e22a00efc59b-0"></a>

Smoke1 used exactly extraction A's request, but a fresh normal Requirement call. It stopped
in 16.906 seconds with `ClarificationRequired: invalid_source_occurrence`. The model quoted
`my mother prefers quiet places` and `my mother` while the source starts `My mother`.
Semantic content was largely preserved, but provenance was invalid. There was no Google,
selector, Review, Weather, Routes, Web or generation call. The strict source rule was not
relaxed and this failed run was not retried. Required-place retention and the richer
multi-person end-to-end scenario therefore remain unvalidated live.

<a id="b-e22a00efc59b-1"></a>

Smoke2 request:

<a id="b-e22a00efc59b-2"></a>

Plan a Sydney trip from 2026-09-20 to 2026-09-22 for four people. We are two adults and two children. We prefer avoiding crowds, less walking, and family-friendly places. We would like a relaxed mix of cultural and outdoor experiences, using mainly public transport. These are preferences, not non-negotiable requirements.

<a id="b-e22a00efc59b-3"></a>

It completed in 96.078 seconds. Four canonical semantic requirements cover avoiding crowds,
less walking, family friendliness and a relaxed cultural/outdoor mix. The first three
link respectively to crowding, walking_intensity and family_friendliness. No HARD or
required named POI is present. Twenty candidates entered Stage A; selection_min=max=10.
The first response chose six, failed `invalid_selection_count`, and used the single shared
repair. The repair chose ten and validated; no repair remained for Stage B. Ten usable
Details records were acquired, with no reserve attempt or duplicate Details fetch.

<a id="b-e22a00efc59b-4"></a>

Stage B received ten candidates, selection_min=1, selection_max=8. It chose four, with no
repair/fallback/forced-set bypass. The final IDs are marked below. A refers to repaired
Stage A shortlist order; R is reserve order. Review requests refer to smoke2 semantic IDs.

<a id="b-e22a00efc59b-5"></a>

| Canonical Place ID | Display name | Stage A / reserve | Review nomination | Stage B selected |
| --- | --- | --- | --- | --- |
| `ChIJ1y1QGkquEmsR3z6AOYKCxG4` | Pirrama Park | A1 | semantic_1 / crowding | yes |
| `ChIJ47iDxkKuEmsR_bma_SA7k1E` | The Rocks Discovery Museum | A2 | semantic_2 / walking_intensity | yes |
| `ChIJ68aBlEKuEmsRHUA9oME5Zh0` | Museum of Contemporary Art Australia | A3 | - | yes |
| `ChIJE06LRQeyEmsR2d4ZLoUE5Q8` | The Ian Potter Children’s Wild Play Garden | A4 | semantic_3 / family_friendliness | no |
| `ChIJFTfQPjuuEmsREP3x-Wh9AQ8` | Chinese Garden of Friendship | A5 | - | yes |
| `ChIJPVqlfGyuEmsRHPcnCX1X1OE` | Art Gallery of New South Wales | A6 | - | no |
| `ChIJWaTdYGuuEmsRoOfx-Wh9AQ8` | Royal Botanic Garden Sydney | A7 | - | no |
| `ChIJXZiB72uuEmsRVR6p6XmuVUk` | The Calyx | A8 | - | no |
| `ChIJYQHJQf6uEmsRENvx-Wh9AQ8` | Berry Island Reserve | A9 | - | no |
| `ChIJZ6DWeEOuEmsRYO_x-Wh9AQ8` | Observatory Hill Park | A10 | - | no |
| `ChIJ5V-W-dFJDWsRlJLQsGf4hN8` | Glenworth Valley Wilderness Adventures | R1 | - | no |
| `ChIJDcRr3A6vEmsRN3dKYsaQawI` | The Oriana Sydney | R2 | - | no |
| `ChIJDflB7BWuEmsRYPbx-Wh9AQ8` | Hyde Park | R3 | - | no |
| `ChIJE3lj4JevEmsRUltUxWzrPQo` | Runaway Gardens - Magic Mirrors Spiegeltent | R4 | - | no |
| `ChIJGyHH_mGuEmsRcWCxuY5YYAc` | Mary Booth Lookout Reserve | R5 | - | no |
| `ChIJQ3Mw5kqvEmsRvMv_rFfOZpY` | Writers Walk | R6 | - | no |
| `ChIJSytgJF2uEmsRC6q8BDZh5qA` | BridgeClimb Sydney | R7 | - | no |
| `ChIJTbZpk4qvEmsRHJRpFvlrbrU` | Digipark Sydney - Immersive Entertainment, 7D Cinema, Indoor Activities Sydney, Things to do in Sydney | R8 | - | no |
| `ChIJXdh5zWmuEmsRXi8KW8VhQmM` | Martin Place | R9 | - | no |
| `ChIJY94tt4SvEmsRxqcD7psP3Rk` | Phoenix Central Park | R10 | - | no |

<a id="b-e22a00efc59b-6"></a>

Flexible count: four is below the maximum eight, so this is genuine discretion, not a
forced set. Rationales cite outdoor/cultural variety and the museum's short-visit signal;
all three evidence-linked preferences are marked insufficient_evidence in the smoke.
However, the generated itinerary fills the first two days with these four POIs and gives
the third day only a 10:00-15:00 'Flexible family downtime and weather buffer'. This is
an under-selection/usefulness warning, even though the user asked for a relaxed trip.
No deterministic count heuristic or refill loop was introduced.

<a id="b-e22a00efc59b-7"></a>

Weather acquisition succeeded. One TRANSIT baseline matrix returned 16 elements with
partial availability and four provider route-not-found elements; no alternatives were
triggered. The Official Web policy executed but generated zero search/page/reasoner tasks.
The generator returned a valid three-day itinerary, and existing date checks passed.
This does not certify opening hours, route feasibility or satisfactory day coverage.

<a id="m-d81ac33c2934"></a>
## Profile compaction and semantic evidence boundaries

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-d81ac33c2934-0"></a>

Three Review requests and three Profile LLM calls processed five reviews per POI:

<a id="b-d81ac33c2934-1"></a>

| POI | Profile state | Model-visible signals |
| --- | --- | --- |
| Pirrama Park | available | accessibility = ACCESSIBLE, confidence low |
| The Rocks Discovery Museum | available | visit_duration = SHORT, confidence low |
| Ian Potter Children's Wild Play Garden | unavailable | no signals; Profile summary exceeded 240 characters |

<a id="b-d81ac33c2934-2"></a>

Seven other Stage B candidates are not_acquired. No acquired Profile supplies the requested
crowding, walking_intensity or family_friendliness signal. Therefore the sample contains
some positive support and missing/unavailable states, but **does not cover a genuine
observed negative signal**. No extra call was made to manufacture that coverage.

<a id="b-d81ac33c2934-3"></a>

Smoke2 and three of five Stage B repetitions preserve uncertainty about less walking.
The other two repetitions expose a correctness issue despite passing structural validation:

<a id="b-d81ac33c2934-4"></a>

- B4: 'Outdoor option with an available low-intensity accessibility signal.'
- B5: 'Outdoor option with an accessibility signal and low walking intensity.'

<a id="b-d81ac33c2934-5"></a>

Both mark less-walking semantic_2 addressed although the supplied signal is ACCESSIBLE
with **low confidence**, not LIGHT walking_intensity. This is an unsupported semantic
inference, plausibly confused by the compact tuple, not an application verification.
The validator verifies reference ownership but cannot establish rationale entailment.
Application check_result remains unknown and rationales do not become planner evidence;
nevertheless the selector's reasoning is unreliable here and needs focused correction.

<a id="b-d81ac33c2934-6"></a>

Unacquired MCA/garden candidates are repeatedly selected, so missing evidence is not
uniformly rejected. The unavailable playground is never selected; this sample cannot
prove that its omission is independent of missing evidence. No full-summary restoration
was made. The observed bug does not establish that summary is necessary: explicitly
separating confidence from evidence value is a more focused candidate for review.

<a id="m-11395d3fc6d9"></a>
## Frozen snapshots and source blindness

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-11395d3fc6d9-0"></a>

Exact serialized model input hashes:

<a id="b-11395d3fc6d9-1"></a>

- `smoke2_snapshot_A.json`: `7c162c2ed624960abce176646d83e596fa27efd524cff69109f624c5084b911f` (7771 UTF-8 bytes).
- `smoke2_snapshot_B.json`: `6fd5a4743fe3b4f2d6239d48dffe1ffb20c947e8489fc5e54806e148eb1fa3a8` (5922 UTF-8 bytes).

<a id="b-11395d3fc6d9-2"></a>

Each repetition used the same bytes, prompt, schema, deployment, low reasoning and config;
transport retry zero. Actual serialized payloads were inspected: no system_version,
GOOGLE_PLACES source label, provider_rank, actual_result_count, historical Q/C/G/R/E
scores or RAG/source-similarity fields are present. Canonical IDs and venue names remain.
Provider-side cached input tokens are reported below; they are not selector-result cache
hits. All ten calls received fresh model outputs without any repeated Google work.

<a id="b-11395d3fc6d9-3"></a>

The stress request was accepted by Foundry and returned a valid in-pool `place_00`, with
valid semantic references and local `f` citation. Output usage was 335 tokens (including
180 reasoning), below 4,096. No ID corruption or invented ID occurred. Because it chose
one of several indistinguishable synthetic prefixes, this only supports transport/reference
compatibility, not robust identity distinction or alias comprehension quality.

<a id="m-7de8bd47157b"></a>
## Stability on identical inputs

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7de8bd47157b-0"></a>

Pairwise metrics use all ten unordered pairs of the five **raw model responses**, before
any application presentation sorting. Stage A includes its two invalid six-item responses
in the primary statistics; the valid-only result is given separately, not substituted.

<a id="b-7de8bd47157b-1"></a>

| Metric | Stage A | Stage B |
| --- | ---: | ---: |
| Valid outputs | 3 | 5 |
| Invalid outputs | 2 | 0 |
| Exact selected-set agreement (pairs / 10) | 2 | 3 |
| Ordered selected-list agreement (pairs / 10) | 2 | 3 |
| Ordered reserve agreement (pairs / 10) | 0 | 10 |
| Reserve-set agreement (pairs / 10) | 1 | 10 |
| Ordered review-nomination agreement (pairs / 10) | 0 | 10 |
| Mean pairwise Jaccard | 0.7236 | 0.7900 |

<a id="b-7de8bd47157b-2"></a>

Stage B reserve/nomination agreement is trivial because both arrays must be empty.
Stage A counts: six twice (invalid), ten three times. Among its three valid responses,
exact sets agree in 1/3 pairs and mean Jaccard is 0.8788. Stage B counts: five four times,
four once, all within 1..8. Neither stage's canonical ID ordering is treated as evidence
of membership stability. This tiny matrix is descriptive, not a research reliability estimate.

<a id="b-7de8bd47157b-3"></a>

| Place ID | Name | Stage A inclusion / 5 | Stage B inclusion / 5 |
| --- | --- | ---: | ---: |
| `ChIJ1y1QGkquEmsR3z6AOYKCxG4` | Pirrama Park | 5 | 5 |
| `ChIJ47iDxkKuEmsR_bma_SA7k1E` | The Rocks Discovery Museum | 5 | 5 |
| `ChIJ5V-W-dFJDWsRlJLQsGf4hN8` | Glenworth Valley Wilderness Adventures | 0 | 0 |
| `ChIJ68aBlEKuEmsRHUA9oME5Zh0` | Museum of Contemporary Art Australia | 3 | 4 |
| `ChIJDcRr3A6vEmsRN3dKYsaQawI` | The Oriana Sydney | 0 | 0 |
| `ChIJDflB7BWuEmsRYPbx-Wh9AQ8` | Hyde Park | 3 | 0 |
| `ChIJE06LRQeyEmsR2d4ZLoUE5Q8` | The Ian Potter Children’s Wild Play Garden | 5 | 0 |
| `ChIJE3lj4JevEmsRUltUxWzrPQo` | Runaway Gardens - Magic Mirrors Spiegeltent | 0 | 0 |
| `ChIJFTfQPjuuEmsREP3x-Wh9AQ8` | Chinese Garden of Friendship | 5 | 5 |
| `ChIJGyHH_mGuEmsRcWCxuY5YYAc` | Mary Booth Lookout Reserve | 0 | 0 |
| `ChIJPVqlfGyuEmsRHPcnCX1X1OE` | Art Gallery of New South Wales | 5 | 1 |
| `ChIJQ3Mw5kqvEmsRvMv_rFfOZpY` | Writers Walk | 0 | 0 |
| `ChIJSytgJF2uEmsRC6q8BDZh5qA` | BridgeClimb Sydney | 0 | 0 |
| `ChIJTbZpk4qvEmsRHJRpFvlrbrU` | Digipark Sydney - Immersive Entertainment, 7D Cinema, Indoor Activities Sydney, Things to do in Sydney | 0 | 0 |
| `ChIJWaTdYGuuEmsRoOfx-Wh9AQ8` | Royal Botanic Garden Sydney | 5 | 4 |
| `ChIJXZiB72uuEmsRVR6p6XmuVUk` | The Calyx | 3 | 0 |
| `ChIJXdh5zWmuEmsRXi8KW8VhQmM` | Martin Place | 0 | 0 |
| `ChIJY94tt4SvEmsRxqcD7psP3Rk` | Phoenix Central Park | 0 | 0 |
| `ChIJYQHJQf6uEmsRENvx-Wh9AQ8` | Berry Island Reserve | 1 | 0 |
| `ChIJZ6DWeEOuEmsRYO_x-Wh9AQ8` | Observatory Hill Park | 2 | 0 |

<a id="b-7de8bd47157b-4"></a>

Stage B requirement-consideration variation:

<a id="b-7de8bd47157b-5"></a>

- semantic_1: insufficient_evidence 5/5.
- semantic_2: insufficient_evidence 3/5, addressed 2/5.
- semantic_3: insufficient_evidence 4/5, tradeoff 1/5.
- semantic_4: tradeoff 1/5, addressed 4/5.

<a id="b-7de8bd47157b-6"></a>

Across the entire matrix: three invalid selector outputs (smoke A initial plus two A
repetitions), one invalid canonical requirement extraction (smoke1), one invalid Profile
summary, one application repair call, **zero fallback and zero forced_set decisions**.
All requests were accepted by transport; no unsupported parameter, refusal, incomplete
response, timeout, invalid Place ID or invalid reference was observed. Two structurally
valid B rationales additionally made the unsupported walking inference described above.

<a id="m-e99a448d418f"></a>
## Per-call latency and provider usage

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e99a448d418f-0"></a>

All rows below are actual provider metadata; output includes reasoning where reported.
Cached input is part of input usage, and reasoning is part of output, not added again.
N/A for initial direct extraction reasoning/cache reflects the observer redaction loss.
Wall time includes transport, parsing and mapping. No currency cost is inferred.

<a id="b-e99a448d418f-1"></a>

| Call | Task/stage | Seconds | Input | Output | Reasoning | Cached input | Total | Engineering selector estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| extract_A/1 | InterpretationDraft | 18.516 | 2904 | 1973 | N/A | N/A | 4877 | - |
| extract_B/1 | InterpretationDraft | 5.656 | 2836 | 500 | N/A | N/A | 3336 | - |
| extract_C/1 | InterpretationDraft | 4.046 | 2845 | 323 | N/A | N/A | 3168 | - |
| extract_D/1 | InterpretationDraft | 8.875 | 2852 | 939 | N/A | N/A | 3791 | - |
| extract_E/1 | InterpretationDraft | 7.078 | 2845 | 788 | N/A | N/A | 3633 | - |
| smoke1/1 | InterpretationDraft | 16.703 | 2904 | 1888 | 1034 | 2901 | 4792 | - |
| smoke2/1 | InterpretationDraft | 14.062 | 2868 | 1641 | 956 | 2765 | 4509 | - |
| smoke2/2 | SelectorDraft A | 9.078 | 3031 | 1113 | 233 | 0 | 4144 | 3292 |
| smoke2/3 | SelectorDraft A | 8.406 | 3038 | 1121 | 143 | 0 | 4159 | 3299 |
| smoke2/4 | ExperienceProfileDraft | 5.625 | 884 | 450 | 321 | 0 | 1334 | - |
| smoke2/5 | ExperienceProfileDraft | 3.843 | 1017 | 262 | 150 | 0 | 1279 | - |
| smoke2/6 | ExperienceProfileDraft | 7.109 | 1133 | 677 | 492 | 0 | 1810 | - |
| smoke2/7 | SelectorDraft B | 9.265 | 2429 | 812 | 421 | 0 | 3241 | 2690 |
| smoke2/8 | V1Itinerary | 25.516 | 8212 | 2624 | 1341 | 0 | 10836 | - |
| stability_A_1/1 | SelectorDraft A | 10.234 | 3031 | 1202 | 326 | 3028 | 4233 | 3292 |
| stability_A_2/1 | SelectorDraft A | 9.875 | 3031 | 1210 | 384 | 3028 | 4241 | 3292 |
| stability_A_3/1 | SelectorDraft A | 8.516 | 3031 | 1168 | 241 | 3028 | 4199 | 3292 |
| stability_A_4/1 | SelectorDraft A | 9.015 | 3031 | 1216 | 287 | 3028 | 4247 | 3292 |
| stability_A_5/1 | SelectorDraft A | 7.406 | 3031 | 1080 | 170 | 3028 | 4111 | 3292 |
| stability_B_1/1 | SelectorDraft B | 6.328 | 2429 | 727 | 210 | 2426 | 3156 | 2690 |
| stability_B_2/1 | SelectorDraft B | 7.625 | 2429 | 824 | 365 | 2426 | 3253 | 2690 |
| stability_B_3/1 | SelectorDraft B | 6.281 | 2429 | 696 | 225 | 2426 | 3125 | 2690 |
| stability_B_4/1 | SelectorDraft B | 6.438 | 2429 | 740 | 270 | 2426 | 3169 | 2690 |
| stability_B_5/1 | SelectorDraft B | 5.687 | 2429 | 608 | 197 | 2426 | 3037 | 2690 |
| stress/1 | SelectorDraft B | 5.109 | 5730 | 335 | 180 | 0 | 6065 | 5991 |

<a id="b-e99a448d418f-2"></a>

Selector engineering input estimates exceed reported input by 261 tokens in these
requests: A 3,292 vs 3,031, A repair 3,299 vs 3,038, B 2,690 vs 2,429, stress 5,991 vs
5,730. Different schema/framing accounting makes these separate measurements; the
observed difference is not a universal correction factor. All selector output/reasoning
usage stayed below the provisional output cap. Requirement/Profile/generator use their
existing settings, not newly imposed selector settings. No Web Reasoner model call occurred.

<a id="m-3d5130e26c0e"></a>
## Provider, cache and budget accounting

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-3d5130e26c0e-0"></a>

| Actual call / observation | Smoke1 | Smoke2 |
| --- | ---: | ---: |
| Requirement LLM | 1 | 1 |
| Destination search | 0 | 1 |
| Candidate searches | 0 | 3 |
| Details | 0 | 10 |
| Details cache hits | 0 | 0 |
| Reserve Details | 0 | 0 |
| Review retrieval | 0 | 3 |
| Profile LLM | 0 | 3 (one invalid) |
| Stage A selector | 0 | 2 (one initial + one repair) |
| Stage B selector | 0 | 1 |
| Repair calls (included above) | 0 | 1 |
| Weather | 0 | 1 |
| Routes matrix | 0 | 1 (16 elements) |
| Native Web search / page retrieval / Official Reasoner | 0 | 0 / 0 / 0 |
| Itinerary generation | 0 | 1 |

<a id="b-3d5130e26c0e-1"></a>

Whole matrix: 25 model calls (7 Requirement, 3 Profile, 14 Selector, 1 itinerary),
19 Google provider method invocations, zero Web/page calls. Stability and stress account
for eleven of the selector calls and no Google invocations. No hidden manual retries.
Details are ten unique IDs with no validation-then-enrichment duplicate pattern. Separate
Review retrieval uses its distinct field mask and budget; it is not duplicate Details
validation. All acquired review candidates were nominated in Stage A. Effective three-day
caps are shortlist ten and reviews three, within global Details 18 and Review/Profile six.

<a id="b-3d5130e26c0e-2"></a>

Observed RequestCache hits are zero; stability reuses captured data rather than exercising
RequestCache. Thus this live sample does not empirically test the positive cache-hit budget
path. Code inspection confirms budget consumption stays inside the cache-miss loader; the
existing offline cache tests remain the evidence for hit behavior. Selector has no provider
handles/tools, and the trace shows one shared repair used only once. No live cap violation.

<a id="m-05f0e2d445a1"></a>
## Fixes, checks, limitations and next decision

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / LIVE DEVELOPMENT VALIDATION - 2026-09-18. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-05f0e2d445a1-0"></a>

No executable application, prompt, schema or configuration fix was made. The ignored
observer alone was corrected to retain numeric reasoning/cache metadata and serialize
application dataclasses. This does not change model inputs or runtime decisions. Therefore
no live-fix regression pass/full backend rerun was required; the preceding 695 passed /
9 skipped result remains historical, not a newly executed live-task test result. The
harness compiled before live execution. Final `ruff check backend scripts`, `git diff --check`,
and the untracked report whitespace check passed. Live artifacts were confirmed ignored.

<a id="b-05f0e2d445a1-1"></a>

Tracked documentation updated in this task: this report and stale current-status notes
in PROJECT.md, docs/poi_selection_evolution.md, docs/v1_design.md and
docs/v1_milestone.md. Ignored live artifacts remain untracked/ignored. Earlier dirty
implementation work is preserved. No commits, pushes, branch changes, embedding/database
work, TripWorld changes, V2/V3 implementation or thesis-note updates occurred.

<a id="b-05f0e2d445a1-2"></a>

Recommendation: focused fixes before explicit re-freeze, with a separately approved
revalidation budget. Prioritize exact source copying and useful clarification diagnostics;
Stage A cardinality compliance (the six-record rationale cap must not be mistaken for a
six-candidate shortlist); explicit separation of confidence from evidence values; and
Profile summary-bound compliance. Inspect the three-day under-selection outcome before
changing count policy. These are proposed next tasks, not implemented changes. No evidence
currently requires replacing Architecture B or restoring QCGRE.

<a id="b-05f0e2d445a1-3"></a>

Remaining gaps: only one successful complete trip; no successful live required-place
end-to-end case; no observed negative Profile dimension; sparse evidence for requested
experience preferences; zero positive RequestCache-hit observations; no Web-task/Reasoner
coverage; initial extraction reasoning/cache data lost; small nonrepresentative stability
sample; strict structured validation cannot prove semantic entailment or itinerary quality.
**STOP: do not re-freeze, add scenarios, begin V2, commit or push without further approval.**

<a id="m-ed27841c4705"></a>
## Targeted fixes and bounded re-validation - 2026-09-19

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19). Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ed27841c4705-0"></a>

**Development validation only. Architecture B retained; V1 is not re-frozen.**
This pass implements the four approved fixes and completes only the targeted live matrix.
Recommendation: **one more narrow reliability pass before re-freeze**, not a redesign.
The prior 2026-09-18 observations remain historical; no failed sample was erased/replaced.

<a id="m-caa131c298fc"></a>
## Implemented source-reference policy

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-caa131c298fc-0"></a>

`locate_source` first performs the original exact, case-sensitive occurrence lookup.
Only when the quote has no exact occurrence and occurrence=0 may it try Unicode casefold
comparison. It builds a mapping from folded positions to original code-point boundaries,
accepts exactly one whole-boundary match, and stores the original substring and offsets.
Canonical SourceReference adds `match_mode=exact|casefold_equivalent` (default exact).
Occurrence remains zero for unique fallback; request SHA-256 stays in the canonical
contract. Multiple folded matches, invalid exact occurrence indices, partial matches
inside expanded characters, punctuation changes, whitespace changes and paraphrases fail.
Even an apparent nonzero occurrence in the fallback domain is conservatively rejected;
it is not silently reinterpreted as an index in a different match domain.

<a id="b-caa131c298fc-1"></a>

No fuzzy matching, normalization of punctuation/whitespace, keyword NLP or embedding
lookup was added. The Requirement prompt now explicitly requires original casing and
punctuation. Existing legacy requested-information/transport source-string contracts
are unchanged; tolerance applies to SourceQuote-based semantic/named/subject references.

<a id="b-caa131c298fc-2"></a>

The previously failed captured live draft now canonicalizes offline: 11 references,
two casefold recoveries. The fresh targeted live smoke also succeeds and records one
actual recovery: original quote `My mother`, offsets [137,146), occurrence 0,
match_mode casefold_equivalent. It does not store the model's `my mother` casing.
See `previous_source_offline_replay.json` and `smoke_canonical.json` in the artifact root.

<a id="m-75edf828394b"></a>
## Application-owned Stage A cardinality

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-75edf828394b-0"></a>

Stage A's raw selected array is now bounded by the admitted-pool maximum 36 instead of
18, allowing safe over-target priority input; normalized acquisition still uses R_pool.
Stage B still validates against its existing contextual min/max (global final cap 16).
This does not raise candidate, Details, reserve or review capacity.

<a id="b-75edf828394b-1"></a>

1. Validate all raw IDs, uniqueness across selected/reserves, required/excluded IDs,
   citations, nominations and requirement references. Missing required IDs remain errors.
2. Preserve model priority; reserve slots for all required IDs even if they occur after
   the ordinary truncation boundary. Trim optional surplus while preserving retained order.
3. Promote model reserves in order until the target is filled.
4. Fill any remainder with the existing admission/fallback order, then remaining canonical
   IDs deterministically if that order is incomplete. No provider rank or score is used.
5. Keep bounded surplus as reserves; omit explanations/nominations for trimmed candidates.
   Validate the normalized result before acquisition.

<a id="b-75edf828394b-2"></a>

Contexts already cap R_pool by eligible candidate count. Pure count adjustment does not
use the shared repair allowance. Invalid IDs, duplicates and invalid links remain failures.
`SelectorResult` records raw_model_selected_count, normalized_shortlist_count,
stage_a_cardinality_adjustment, promoted_reserve_ids, deterministic_top_up_ids and
trimmed_ids. Actual adjustments use decision_origin=model_normalized. Stage A trace
also preserves the raw ordered selected/reserve IDs. Stage B receives no such normalization.

<a id="m-60ae4561ae42"></a>
## Explicit Profile values, confidence and linked support

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-60ae4561ae42-0"></a>

The canonical review dimensions, values, confidence derivation and refs remain intact.
Only selector projection changes to:

<a id="b-60ae4561ae42-1"></a>

```json
{
  "experience": {
    "state": "available",
    "signals": {
      "accessibility": {"value": "ACCESSIBLE", "confidence": "LOW_CONFIDENCE"}
    }
  }
}
```

<a id="b-60ae4561ae42-2"></a>

The prompt explicitly separates certainty from value, prohibits accessibility -> walking
and crowding -> quietness substitution, and distinguishes unavailable/not_acquired from
negative evidence. Missing walking_intensity is not manufactured from accessibility.

<a id="b-60ae4561ae42-3"></a>

A decision's Profile citation must be registered in ExperienceEvidenceRequest for every
requirement_ref in that decision. Mixed unrelated refs require narrower decisions.
Each RequirementConsideration also has bounded `review_support` entries (maximum two),
with place_id and dimension, for explicit review-backed support. The validator checks
selected candidate ownership, signal presence and that requirement's registered dimension.
Semantic-only decisions/considerations can leave support empty. Status addressed is still
a semantic judgment, not a factual verification. Free-text claims without a Profile
citation cannot be proven by this structural validator; this remains a known limitation.
Foundry transport DTOs explicitly carry the new support field.

<a id="m-f09272b74b36"></a>
## Non-authoritative Profile summary

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f09272b74b36-0"></a>

ExperienceProfileDraft applies a deterministic before-validator: a summary longer than
240 Unicode code points is sliced to 240 and sets summary_truncated=true. This flag is
carried into the canonical Profile as an additive diagnostic; dimensions, values,
confidence derivation, refs and availability policy are unchanged. Invalid dimensions
or refs still fail normally. No extra LLM call shortens the summary. Astral Unicode
characters are preserved; grapheme clusters and sentence endings may be cut.
A fake 300-code-point summary with a valid walking signal becomes an available Profile
with the same LIGHT value/ref and a 240-code-point summary. No paid Profile regression
call was made. Profiles and their summaries remain application-side except supported
explicit signal projections.

<a id="m-77153036e95f"></a>
## Stage B cardinality: unchanged rule, additional observation

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-77153036e95f-0"></a>

The min remains max(1, required_count); max remains min(k_final, eligible_count).
No days-times-N formula or lower-bound heuristic was added. The prompt asks for enough
planning candidates for trip duration without filler, and fewer only when justified.
`fewer_deeper_requirement_ids` is a bounded selector-output diagnostic, not a new user
preference enum or extraction flag. It references existing canonical semantics, is
validated for reference integrity, and has no effect on counts or scores. It remains a
model judgment, not a mechanically proven classification; no raw-text keyword scan exists.

<a id="b-77153036e95f-1"></a>

Stage B trace records trip_days, required_count, eligible_count, min/max, selected_count,
explicit_fewer_deeper_model_observation, linked requirement IDs and existing bounded
rationales/considerations. Mechanical fallback records the semantic observation as unknown.

<a id="m-697c2e6de836"></a>
## Offline validation and sizing

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-697c2e6de836-0"></a>

- Focused contract/selector/projection/Foundry suite: **128 passed**.
- Full backend suite run once after the fixes: **720 passed, 9 skipped**, 9.92 seconds.
  Optional database integration tests remain skipped; no database work was performed.
- Ruff passed. `git diff --check` passed (ordinary CRLF/LF notices only).
- Tests cover exact/unique-casefold/ambiguous/repeated/Unicode spans and paraphrase
  rejection; exact/underfilled/reserve-promoted/mechanically-filled/overfilled Stage A;
  required retention, invalid/duplicate ID rejection, no repair for pure count changes;
  explicit confidence, missing dimensions, wrong/correct requirement links, semantic-only
  outputs, long-summary preservation and unchanged flexible Stage B bounds. Existing
  graph/acquisition tests retain their Details-capacity assertions.
- Offline replay of all five old Stage A live outputs gives raw 6,6,10,10,10 -> normalized
  10,10,10,10,10. This is replay evidence, not five new live successes.
- Updated worst representative 160-character sizing: A 12,784 / 14,000 (8.7% margin),
  B 9,895 / 11,000 (10.0%). Explicit support/schema instructions consume more space;
  A no longer has the prior approximately 10% diagnostic margin in that stress fixture.
  The ceiling is unchanged and the runtime overflow gate remains. Actual targeted live
  inputs are much smaller. No input meaning or capacity was removed to recover headroom.

<a id="m-c92256167ab3"></a>
## Exact targeted live matrix and configuration

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-c92256167ab3-0"></a>

Artifact root: `logs/selector_fix_20260919/` (ignored). Fresh deployment and returned model:
`gpt-5.6-luna`. Local reference date 2026-09-19 in Australia/Sydney; provider timestamps
are 2026-09-18 UTC because the local run occurred after midnight. Smoke dates advance
within the supported window to 2026-09-21 through 2026-09-23; request wording otherwise
matches the previously failed family/mother/father/Opera House scenario.

<a id="b-c92256167ab3-1"></a>

Policy semantic_selector_3, projection selector_projection_3; input 14k/11k, output 4096,
reasoning low, timeout 90 seconds, provider retries zero. Caps remain provisional.
No further application changes were made after offline tests or in response to live errors.

<a id="b-c92256167ab3-2"></a>

- One fresh full smoke, once, no manual retry.
- Stage A: five fresh direct responses on the exact old serialized input bytes.
- Stage B: five fresh direct responses on one migrated fixed snapshot; only Profile
  representation/policy metadata changed, retaining actual evidence and missing dimensions.
- One additional fewer/deeper B response. The ordinary comparison reuses B1; no second
  extra call or Google work was made for cardinality observation.
- No extra city, stress case, extraction matrix, database, embedding or broad validation.

<a id="b-c92256167ab3-3"></a>

Each fixed-input call uses the current provider DTO, prompt, config and the application
validator/normalizer. Repairs/fallbacks are deliberately not invoked for this raw-response
matrix: each repetition has one fresh model output and any failure remains recorded.
The normal smoke exercises the service's shared budget. No manual repair or substitute run.

<a id="m-44e4ad70738f"></a>
## Stage A raw versus accepted results

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-44e4ad70738f-0"></a>

| Call | Raw selected | Accepted shortlist | Adjustment / additions / trims | Result |
| --- | ---: | ---: | --- | --- |
| A1 | 10 | 10 | none; no IDs added/promoted/trimmed | valid |
| A2 | 10 | - | not applied: structural rejection | duplicate_selection_ids |
| A3 | 10 | 10 | none; no IDs added/promoted/trimmed | valid |
| A4 | 10 | 10 | none; no IDs added/promoted/trimmed | valid |
| A5 | 10 | - | not applied: structural rejection | duplicate_selection_ids |

<a id="b-44e4ad70738f-1"></a>

A2 duplicates `ChIJ1y1QGkquEmsR3z6AOYKCxG4` across selected/reserves; A5 duplicates
`ChIJFTfQPjuuEmsREP3x-Wh9AQ8`. These are genuine structural failures, not count underfill,
and were not silently deduplicated. All five raw ordered shortlists/reserves are retained
in `fix_A_N_result.json`. Accepted cardinalities are 10, rejected, 10, 10, rejected.
Live top-up/trim ID lists are empty for the three valid responses; rejected responses have
no accepted result. Repair=0, fallback=0. No evidence-acquisition calls were made here.

<a id="b-44e4ad70738f-2"></a>

Historical-output replay demonstrates the actual count fix. Both old six-ID outputs
promote four model reserves without mechanical fill or repair. Exact promoted IDs:

<a id="b-44e4ad70738f-3"></a>

- Old A1: `ChIJ68aBlEKuEmsRHUA9oME5Zh0`, `ChIJDflB7BWuEmsRYPbx-Wh9AQ8`, `ChIJZ6DWeEOuEmsRYO_x-Wh9AQ8`, `ChIJYQHJQf6uEmsRENvx-Wh9AQ8`.
- Old A2: `ChIJZ6DWeEOuEmsRYO_x-Wh9AQ8`, `ChIJYQHJQf6uEmsRENvx-Wh9AQ8`, `ChIJGyHH_mGuEmsRcWCxuY5YYAc`, `ChIJXZiB72uuEmsRVR6p6XmuVUk`.

<a id="m-fa6b93206c25"></a>
## Stage B evidence-semantics results

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-fa6b93206c25-0"></a>

| Call | Raw count | Accepted count | Confidence/value confusion | Validator |
| --- | ---: | ---: | --- | --- |
| B1 | 5 | 5 | not observed | valid |
| B2 | 6 | - | not observed | unlinked_review_dimension |
| B3 | 5 | - | not observed | unlinked_review_dimension |
| B4 | 6 | 6 | not observed | valid |
| B5 | 6 | 6 | not observed | valid |

<a id="b-fa6b93206c25-1"></a>

Across these five calls: **zero observed confidence/value confusions; two wrong-dimension
support outputs rejected** (B2/B3). Both cite visit_duration for semantic_4 (relaxed cultural/
outdoor mix), and B3 additionally semantic_3 (family-friendly). Neither requirement is
registered for visit_duration; semantic_3 is linked to family_friendliness. This is an
invalid structural support relation even though a SHORT signal exists for that POI.
There were no accessibility -> walking citations or claims. Less-walking and crowding
remain insufficient_evidence in all five. One raw family consideration is tradeoff.

<a id="b-fa6b93206c25-2"></a>

Three outputs pass all structural validation. Unacquired candidates are included, so
missing evidence is not uniformly treated as negative. There is no observed negative
walking signal in this fixture, so the result does not cover every uncertainty state.
B5 says 'Short cultural visit' while citing only f: prose may still borrow a Profile fact
without declaring review support. Explicit link validation cannot detect every implied
or uncited claim without semantic interpretation. Do not equate accepted with factually
verified. No additional LLM validator or dimension-inference rule was added.

<a id="m-c8ae7e403bf9"></a>
## Source-reference smoke and downstream outcome

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-c8ae7e403bf9-0"></a>

The single smoke succeeds in **63.187 seconds**, with one exact-case recovery described
above. Required Sydney Opera House is resolved and retained. Stage A raw/accepted=10,
no normalization adjustment, one A call; Stage B chooses four from 1..8 with one call.
Both decision origins are model; repair/fallback/forced_set counts are zero.

<a id="b-c8ae7e403bf9-1"></a>

Final canonical IDs:

<a id="b-c8ae7e403bf9-2"></a>

- `ChIJ3S-JXmauEmsRUcIaWtf4MzE`: Sydney Opera House.
- `ChIJ68aBlEKuEmsRHUA9oME5Zh0`: Museum of Contemporary Art Australia.
- `ChIJCZ5rATyuEmsRcAjUsjLzbGU`: Customs House.
- `ChIJXZiB72uuEmsRVR6p6XmuVUk`: The Calyx.

<a id="b-c8ae7e403bf9-3"></a>

There are eight open semantic requirements, no linked experience requests in this fresh
interpretation, and therefore no Reviews/Profile calls. This smoke cannot validate live
summary truncation; the approved offline regression and captured B evidence cover those
separate concerns. Weather is available. Routes are partial: one 16-element TRANSIT matrix,
four provider route-not-found elements. Official Web ran its gap policy with zero tasks.
The generator returns a date-valid three-day itinerary: four distinct POIs over days one/
two, then a deeper MCA return visit on day three. This may fit fewer/deeper intent but is
not proof of itinerary quality or feasibility. For example 'quiet' in a generated activity
title is not supported by acquired quietness evidence; no V3 checks were introduced.

<a id="m-c0c421dcc1d2"></a>
## Cardinality observations (no new rule)

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-c0c421dcc1d2-0"></a>

| Observation | Trip days | Required / eligible | Min / max | Raw count | Accepted count | Fewer/deeper |
| --- | ---: | --- | --- | ---: | --- | --- |
| Ordinary fixed B1 (reused from five calls) | 3 | 0 / 10 | 1 / 8 | 5 | 5 | no |
| One additional fewer/deeper fixed input | 3 | 0 / 10 | 1 / 8 | 3 | rejected | semantic_5 |

<a id="b-c0c421dcc1d2-1"></a>

The added semantic_5 is the previously extracted exact meaning 'Prefer visiting fewer
places in depth rather than rushing', copied from the historical canonical record, with
its provenance retained outside the model snapshot. No new parser or acquisition ran.
The fewer output cites visit_duration for family/fewer requirements without registered
links and is rejected (`unlinked_review_dimension`). Its raw count suggests fewer choices,
but it is **not an accepted comparison result**. It contributes one further wrong-dimension
rejection beyond the five-call B matrix, for three total this pass.

<a id="b-c0c421dcc1d2-2"></a>

Separately, the live smoke records three days, required=1, eligible=10, min/max=1/8,
selected=4, fewer/deeper semantic_7=true. These sparse results do not establish systematic
under-selection, and no hard/preferred minimum was implemented. Five B repetitions have
raw counts 5,6,5,6,6; only 5,6,6 are accepted. Model-observed fewer/deeper IDs are traceable
but do not prove correct semantic classification by application code.

<a id="m-57dadcbd9075"></a>
## Actual model usage and latency

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-57dadcbd9075-0"></a>

Total **15 model calls**: one Requirement, thirteen Selector (two smoke + ten frozen +
one fewer), one itinerary. No Profile or Official Web model call this pass. Every provider
response is completed; no transport/schema rejection, refusal, timeout or manual retry.
Output counts include reported reasoning; cached input is part of input usage. Input
engineering estimates and provider usage are distinct measurements, not billing equals.

<a id="b-57dadcbd9075-1"></a>

| Call | Task | Seconds | Input | Output | Reasoning | Cached input | Total | Engineering estimate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fewer/1 | SelectorDraft B | 7.782 | 2865 | 709 | 332 | 1202 | 3574 | 3138 |
| fix_A_1/1 | SelectorDraft A | 12.672 | 3388 | 1418 | 465 | 1202 | 4806 | 3661 |
| fix_A_2/1 | SelectorDraft A | 8.187 | 3388 | 1066 | 184 | 3385 | 4454 | 3661 |
| fix_A_3/1 | SelectorDraft A | 8.766 | 3388 | 1132 | 204 | 3385 | 4520 | 3661 |
| fix_A_4/1 | SelectorDraft A | 9.031 | 3388 | 1171 | 220 | 3385 | 4559 | 3661 |
| fix_A_5/1 | SelectorDraft A | 9.171 | 3388 | 1180 | 247 | 3385 | 4568 | 3661 |
| fix_B_1/1 | SelectorDraft B | 9.468 | 2804 | 843 | 365 | 1202 | 3647 | 3077 |
| fix_B_2/1 | SelectorDraft B | 8.094 | 2804 | 893 | 341 | 2801 | 3697 | 3077 |
| fix_B_3/1 | SelectorDraft B | 5.516 | 2804 | 640 | 154 | 2801 | 3444 | 3077 |
| fix_B_4/1 | SelectorDraft B | 8.063 | 2804 | 889 | 346 | 2801 | 3693 | 3077 |
| fix_B_5/1 | SelectorDraft B | 9.313 | 2804 | 1015 | 479 | 2801 | 3819 | 3077 |
| smoke1/1 | InterpretationDraft | 12.265 | 2912 | 1354 | 498 | 0 | 4266 | - |
| smoke1/2 | SelectorDraft A | 9.781 | 3593 | 1175 | 298 | 0 | 4768 | 3866 |
| smoke1/3 | SelectorDraft B | 7.719 | 3027 | 761 | 270 | 1202 | 3788 | 3300 |
| smoke1/4 | V1Itinerary | 20.5 | 8354 | 2212 | 1077 | 1248 | 10566 | - |

<a id="b-57dadcbd9075-2"></a>

Every selector call remained below the 4096 output cap. Successful transport is recorded
separately from application validity. Direct comparison with the old 96-second review-linked
smoke would be misleading: this request has no Profile calls and different evidence.
No universal latency improvement or currency cost claim is made.

<a id="m-086a9658f8f8"></a>
## Provider/capacity/cache/source checks

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-086a9658f8f8-0"></a>

Only the smoke makes Google calls: destination search 1, candidate search 3, Details 10
(unique IDs), Reviews 0, Weather 1, Routes 1 = **16 provider method invocations**. Reserve
Details=0; Details cache hits=0; Web search/pages/reasoner=0. Details remain inside global
18 and effective shortlist 10; review budgets unchanged. No validation-then-enrichment
duplicate Details pattern. Frozen calls perform zero Google work; provider input-token
cache reads are not selector-result cache hits. Positive RequestCache-hit behavior was
not newly exercised. Shared repair capacity remains one, but none was used in this smoke.

<a id="b-086a9658f8f8-1"></a>

Actual serialized payloads were checked for forbidden source/version/rank/score fields;
none were present. Stage A frozen bytes are identical to the previous checkpoint. Hashes:

<a id="b-086a9658f8f8-2"></a>

- `frozen_A.json`: `7c162c2ed624960abce176646d83e596fa27efd524cff69109f624c5084b911f`.
- `frozen_B.json`: `3f870352f7c50f7325ec5157f6ca5fe940fc7f3f8217bb53d919603783f06e37`.
- `fewer_snapshot.json`: `f018fb66c65ba1b186c516a633babe3865a239243d603655da001afac16e513d`.
- `smoke1_snapshot_A.json`: `2f14f122cfd5d6d24abf227a02f7eb18b64e5170e4ec17543bc3de0a63c80d17`.
- `smoke1_snapshot_B.json`: `f8e2a496ce16ae09d952deb8e6503fc3b6edb21d0aeec5a55b0dcdeb7441e6c6`.

<a id="m-2ffa5c3efe55"></a>
## File impact and remaining decision

_Source context: B1 Development Validation Record (2026-09-18 to 2026-09-19) / Targeted fixes and bounded re-validation - 2026-09-19. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2ffa5c3efe55-0"></a>

Application changes:

<a id="b-2ffa5c3efe55-1"></a>

- `schemas/interpreted_requirements.py`, `policies/interpreted_requirements.py`,
  `versions/v1/prompts.py`: provenance match_mode, conservative resolver and exact-copy prompt.
- `schemas/poi_selector.py`, `llm/azure_foundry/dto.py`, `services/poi_selector.py`:
  priority normalization/diagnostics, bounded explicit support and cardinality observations,
  validation and semantic instructions. Stage A raw array bound 36 supports admitted-pool
  priority, without increasing actual shortlist/final/acquisition budgets.
- `policies/selector_projection.py`: explicit value/confidence view, projection version 3.
- `evidence/experience_models.py`, `policies/experience_profile.py`: diagnostic summary
  truncation and flag propagation; structured evidence rules remain intact.
- `runtime/config_models.py`, `config/runtime.yaml`: selector policy version 3 only;
  caps/reasoning/timeouts/retries unchanged.
- Tests: new `versions/v1/test_selector_live_fixes.py`; adapted
  `versions/v1/test_selector_projection.py` and `llm/azure_foundry/test_open_contracts.py`.
- Documentation: this checkpoint and current-status notes in PROJECT, V1 design/milestone
  and selector architecture review. Ignored one-off harness/snapshots/results are preserved
  outside Git; no secrets, raw datasets, embeddings or thesis notes were added.

<a id="b-2ffa5c3efe55-2"></a>

No executable V0 changes, no QCGRE restoration, no architectural replacement, no V2/V3,
no Phase 6, no embedding/database work, no commit/push/branch change, and no re-freeze.
Previous working-tree changes remain intact.

<a id="b-2ffa5c3efe55-3"></a>

Recommendation: **one more narrow reliability pass**, subject to user approval. The four
approved fixes work at their deterministic boundaries, and the end-to-end source failure
is resolved. Remaining raw duplicate-ID errors and repeated unregistered Profile citations
still cause material rejection rates. Investigate generation of disjoint ID lists and
explicit per-requirement evidence support without weakening validators or adding automatic
NLP repair. Uncited prose can still imply unsupported evidence. Frozen matrix failures
were deliberately not retried; normal service repair/fallback frequency under those failures
was therefore not measured here. No further tuning/live calls were run after observing them.

<a id="b-2ffa5c3efe55-4"></a>

The A stress sizing margin is 8.7%, fewer/deeper comparison has one rejected result,
Profile-negative evidence coverage is incomplete, and under-selection remains unresolved.
None of these observations authorizes a new cardinality formula or establishes formal
research results. STOP and wait for review before any further fix, live run or re-freeze.
