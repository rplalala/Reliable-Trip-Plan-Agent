# Phase 6 Proposal: TripWorld Discovery into the Planning Candidate Funnel

Status: **Proposed; awaiting user approval. No Phase 6 implementation.**
Update (2026-09-18): **On hold for selector architecture review.** The user requested
analysis of a shared bounded LLM selector for both V1 and V2 before choosing this
QCGRE adaptation. See [the separate architecture review](poi_selector_architecture_review.md).
The proposal below is preserved for comparison; it is not accepted or authorized
for implementation, and its Q_rel recommendation is not a settled decision.
Repository inspection date: 2026-09-18. Phase 1-5 are Accepted and form the frozen
technical baseline; this is not a complete V2 freeze. V1 remains frozen. This proposal
is grounded in the current repository, not a generic RAG architecture or a formal
experiment plan. All new types, files, settings and behaviors below are proposals.

## 1. What exists and where integration belongs

`backend/app/versions/v1/graph.py` executes one typed requirement interpretation,
date validation, destination resolution, `acquire_candidate_funnel`, review-aware
selection, Weather, Routes, Official Web, itinerary generation and final date checks.
`V1EvidenceAcquisitionService.run_candidate_funnel()` in
`backend/app/services/evidence_acquisition.py` currently owns:

```text
build_place_search_intents
 -> search_candidate_observations
 -> merge_search_observations
 -> named-place resolution / exclusions
 -> select_pois(capacity=c_raw, require_details=False)
 -> select_pois(capacity=r_pool, require_details=False)
 -> current Details/rating for contenders
 -> select_pois(capacity=k_final, require_details=True)
 -> review-aware refinement in a later graph node
```

The exact proposed integration seam is **after ordinary Google observations exist,
before the merged pool is narrowed to C_raw** (currently immediately before the
`merged = merge_search_observations(observations)` statement). The implementation
would live in a **V2-owned funnel**, not a new branch inside V1's method. Named-place
resolution must first be computed from the existing Google observations/intents and
protected through union; RAG must not silently reinterpret unresolved explicit names.

```text
Same typed requirements and resolved destination
 -> existing explicit-name / Google interest discovery
 -> bounded TripWorld semantic discovery in parallel conceptually, ordered operationally
 -> on-demand current Google acquisition for needed RAG hits
 -> canonical union, preserving source histories and named-place constraints
 -> C_raw -> R_pool -> Details reuse/acquisition -> review-sensitive final selection
 -> existing selected-POI evidence and itinerary behavior
```

Do not append RAG POIs after final selection. Do not call the entire V1 planner again
on RAG failure: that repeats interpretation and potentially paid calls. Continue with
the already available Google-only observations, typed semantics, cache and budgets.

There is currently no `backend/app/versions/v2/` graph/runner or `scripts/run_v2.py`.
The shared `SystemVersion` already lists V2, but that enum does not implement it.
The product `PlanningService` currently delegates to V0; Phase 6 must not silently
switch the product API/frontend to V2. A separate V2 runner is the initial entry point.

## 2. Existing contracts and concrete incompatibilities

| Current component | Reuse / constraint |
| --- | --- |
| `TripIntentExtractionResult` in `schemas/trip_intent.py` | Reuse the single V1 LLM extraction and source-span validation unchanged |
| `PoiInterest`, `ExperiencePreferenceIntent`, `NamedPlaceIntent` | Semantic query inputs; no second parser or raw-text regex interpretation |
| `PlaceSearchIntent` / `SearchIntentKind` | Reuse stable intent identity/importance where applicable |
| `DestinationContext` in `evidence/models.py` | Already contains coordinates; has no country or radius |
| `RetrievalService` / `GeographicScope` | Existing ENRICHED query embedding, fixed production policy and exact retrieval |
| `GooglePlacesProvider`, request/response DTOs, normalization | Current identity/information acquisition; preserve fixed masks and reviews separation |
| `RequestCache`, `ToolBudget` | Reuse request-local semantics with explicit V2 additions described below |
| `QueryIntentHit` | Keep unchanged: it explicitly means one unfiltered Google search position |
| `PlaceSelectionInput` | Requires at least one Google hit; cannot represent RAG-only candidates as-is |
| `PlaceCandidate` | Requires nonnegative `provider_rank`, even for downstream evidence; needs an explicit compatibility solution |
| `merge_search_observations` | Chooses a canonical row using minimum Google rank; not a multi-source canonical merger |
| `select_pois` / review sensitivity | Hardwired to Google hits for Q, C and stable ties; cannot be reused blindly with fake hits |

The main issue is wider than changing `q_rel()`: Google-only assumptions also occur
in `c_cov`, `best_rank`, required-place ordering, the canonical merge, and
`find_review_sensitive_candidates()` (`min(hit.provider_rank ...)`). Review
counterfactuals call the same selector repeatedly. A new relevance rule must be used
consistently at C_raw, R_pool, no-review final, review sensitivity and final selection.

## 3. Query construction from existing semantics

Propose a small V2 `RagQueryPlan` with:

```text
query_id / query_builder_version / semantic_text
originating_intent_ids / intent_kind / source_spans
purpose: poi_interest | experience_discovery | generic_fallback
geographic_scope: latitude, longitude, radius_km, country?
fetch_k / max_fetch_k / deterministic_query_order
```

`DiscoveryIntent` today holds only semantic text; the new plan surrounds it with
provenance and bounds. It does not change the frozen corpus/embedding space.

Use the validated `PoiInterest.surface` and its importance to create one query per
distinct non-named interest, up to a configured maximum. Reuse the corresponding
Google `PlaceSearchIntent.intent_id` where the same interest exists; otherwise use
a stable source-independent ID derived from the normalized interest and importance.
Repeated RAG queries must not invent additional coverage rewards for the same interest.
Deduplicate exact normalized texts and execute in deterministic priority order.

Use a finite mapping of existing experience enums to positive discovery phrases, not
a new parser: e.g. AVOID_CROWDS -> quieter/less crowded places; PREFER_FAMILY_FRIENDLY
-> family-oriented attractions. PREFER_ACCESSIBLE may guide discovery but cannot
assert accessibility. Walking and visit-duration needs lack reliable corpus fields;
retain them for existing experience/routes handling, with no claimed hard retrieval
filter. Query wording is a heuristic to approve and version, not factual inference.

Prefer a small list of separate interest queries and at most bounded supplementary
experience queries over one very long concatenated request or every Cartesian
interest/preference combination. Experience-only queries carry provenance but do not
create new C_cov interest IDs. Where interests exist, they may be included as text
context, but do not turn every compound query into proof of matching every interest.
If no usable typed interests exist, reuse a bounded generic fallback concept and
fallback importance. Named-place queries remain exclusively in the existing explicit
path. Requested admission/hours questions belong to downstream official evidence,
not additional RAG queries. Do not embed dates, budgets, IDs or the raw full request.

Coordinates come from the existing `resolve_destination()` result. Radius is a
validated V2 runtime policy, not an inferred locality equality or a hardcoded Sydney
scope. Optional country stays null initially: current `DestinationContext` has no
country, and parsing a formatted address would invent an unreliable contract. A
future structured country extension needs a separate reviewed provider mapping.
No automatic unbounded radius expansion; any bounded retry scope must be explicit.

`RetrievalService` is currently synchronous, writes query checkpoints, uses build-sized
timeouts/configuration and expects a live DB connection. A V2 wrapper must provide
request deadlines, short DB statement/connection limits and bounded query tokens/
retries without changing offline Phase 5 behavior. Use a bounded worker-owned
connection and adapter timeout; an async timeout alone does not stop an underlying
thread/API request. Avoid sharing one psycopg connection across concurrent tasks.
For planning, prefer request-scoped query-vector reuse; keep existing disk checkpoints
for the standalone CLI rather than silently persisting every user's semantic query.
No new infrastructure, vector index, embedding model or corpus regeneration is needed.

## 4. Ranked-stream resolution and deterministic stopping

Each query yields an ordered stream. Within a stream order is cosine descending,
then entity ID (as in Phase 5). Across queries use deterministic importance-prioritized
round-robin, preserving within-stream order; raw cosine from different queries is
not a globally calibrated score. Keep every originating hit even when entity/Google
identity deduplication means acquisition occurs only once.

Proposed state machine:

```text
for hit in stable merged stream:
    attach any already-known discovery provenance
    if usable target reached: stop new acquisitions
    if entity/canonical ID already processed: reuse outcome; do not spend again
    if existing Google ID: obtain/reuse current Details
    else, or after failed ID acquisition: bounded name/location search
    uniquely reconcile fallback -> obtain/reuse current Details
    validate canonical ID, current coordinates and existing POI eligibility
    if unresolved/unusable: record reason; continue to next hit
    union by returned canonical Google ID
    count only a distinct usable RAG contribution toward target
```

Keep all local already-retrieved provenance even when acquisition stops early. Define
the target as **new distinct usable canonical candidates beyond the Google pool**;
an overlap adds discovery provenance but does not satisfy a target intended to improve
recall. Record both total RAG-resolved identities and net new identities. Overlap can
still cost a Details call if current information was not acquired already. Stop on
usable target, API/fallback budget, deadline, configured stream cap or exhaustion.

`usable` means current Google identity/coordinates and the existing structured
eligibility checks succeed; missing rating alone is allowed. Permanently closed,
invalid-coordinate, excluded or definitely-after-trip opening entities do not count.
V1 treats temporary closure/unknown status as risks, not unconditional exclusion;
preserve that behavior and allow existing evidence handling to address it.

Recommend configuration expressed in relation to existing effective capacities:
`usable_rag_target <= c_raw` and bounded by acquisition headroom; initial fetch K can
be `min(max_fetch_k, ceil(oversampling_factor * target_for_query))`. Numeric defaults
remain unapproved. Start with one acquisition at a time for deterministic spend and
stopping. Concurrency >1 requires ordered reservations, bounded in-flight work and
deterministic result commitment; it must not resolve the entire retrieved set eagerly.

Phase 5 exposes Top-K, not pagination. If a configured incremental fetch is approved,
reuse the same query vector with larger K through `PostgresSearch`, skip previously
seen IDs and stop at max K. Do not re-embed unchanged text or promise an unlimited
server cursor. Freeze the corpus/version for a run or abort RAG if its identity changes.

## 5. ID-first, fallback and FSQ-only acquisition

For an ID-backed hit use `PlaceDetailsRequest` with **the existing full
`PLACES_DETAILS_FIELD_MASK` and matching language**. This is the actual current-info
acquisition, not a small validation call followed by another identical Details call.
Reviews remain separate and selective. Store the normalized Details/rating result
and use returned Google ID/name/location as canonical metadata. Preserve the historical
TripWorld ID and any returned-ID redirect as resolution provenance.

A 200 response is not sufficient if identity/coordinates are unusable. Recheck the
Google coordinates against destination scope and plausibility relative to the source
entity. Do not reject ordinary renamed places solely on different spelling when an
ID succeeds; reject unresolved geographic contradictions. Matching thresholds and
handling of valid moved businesses require explicit configuration/approval.

For a failed/stale ID or FSQ-only entity, Text Search uses a bounded preferred-name
plus locality/destination query and source-coordinate bias, reusing the existing
request DTO and mask. Existing Google bias is a fixed **50 km circle** and is not a
hard radius filter. The resolver must apply its own Haversine checks to the results.
Use exact normalized preferred-name/known-alias evidence plus geographic consistency
for an initial conservative unique match. Do not accept the first search result
unconditionally, invent an LLM identity judge or resolve ambiguity by provider rank.
If multiple plausible matches remain, reject/replace. Exact matching sacrifices recall;
more permissive fuzzy matching needs separate justification and tests.

A selected fallback search result must obtain the full current Details mask before
RAG-only admission. Search success alone is not the full current-info contract. Search
rank for a name/location resolution query is **identity evidence**, not relevance to
the originating interest; never feed it into Q_rel. The existing provider does not
expose detailed HTTP status categories in its service outcome; initially treat a
sanitized acquisition failure as fallback-eligible under the bounded budget. A future
error-code extension could distinguish quota/auth outages from stale IDs, but is not
necessary to pretend those distinctions already exist. No global Google validation.

## 6. RequestCache and paid-call reuse

Actual current keys in `V1EvidenceAcquisitionService` are:

```text
Details: ("place_details", place_id, field_mask, language_code)
Search:  ("places_search", casefold(text_query), page_size, field_mask,
          include_future_opening_businesses, (lat, lon) or None, language_code)
Reviews: ("place_reviews", place_id, field_mask, language_code)
```

`_cached_provider_call_with_status()` checks cache before its factory consumes budget.
It caches `_ProviderResult` for successes **and provider failures**; budget rejection
is outside the provider catch and is not a successful cached result. `RequestCache`
itself does not cache raised exceptions and has no in-flight single-flight protection.

Propose a small public acquisition gateway delegating to existing cache/key logic,
with explicit charging context and typed acquisition outcome. Keep current private
methods as unchanged-default wrappers for V1. Both V2 Google discovery and RAG
resolution must share one gateway/cache instance. Do not directly inject a raw DTO
under a key whose existing value type is `_ProviderResult`, or create a second cache
namespace for the same successful Details request. Canonical redirects additionally
reuse the already obtained outcome by returned ID within the gateway, with provenance;
they must not require a second paid Details request just to populate that alias.

Match exact masks/language so later contender enrichment hits the cache. A minimal
sanity-check mask cannot satisfy full Details, and reviews cannot satisfy Details.
Failed IDs/attempted fallback keys are reused within the request; revisiting the same
failed hit must not spend again. For initial concurrency=1 existing cache semantics
are sufficient. Add V2-local keyed locks/single-flight only if concurrency is approved;
do not silently alter V1 scheduling or assume the current cache already guarantees it.

Early successful RAG Details remain in the cache/evidence sidecar. During C_raw/R_pool
scoring, project rating/details to the same stage-appropriate visibility as Google
search observations. Otherwise RAG would receive R_rating before Google gets it.
Only the selected contender stage exposes Details/rating symmetrically. Candidates
outside R_pool do not bypass its limit merely because their Details were preloaded.

## 7. ToolBudget: protect the baseline, expose incremental cost

Current normal limits are candidate searches **12**, Details **18**, candidates **36**,
final POIs **16**, and reviews/Profile **6**; hard search/Details ceilings are **12/20**.
Capacities are trip-dependent: `k_final=min(16,2*days+2)`, `r_pool=max(10,k_final+2)`,
`c_raw=max(20,2*r_pool)`, reduced by operating limits. R_pool is currently limited by
configured Details capacity, not by already-spent calls. Pre-resolving RAG from that
same unreserved budget can starve ordinary enrichment and break graceful degradation.

Existing PLACE_DETAIL_CALLS and CANDIDATE_SEARCH_CALLS describe the operation correctly,
but have no allocation ownership, reservation or RAG/fallback dimension. Recommend:

- Retain operation totals for every actual Google request, including failures.
- Add narrow V2 allocation counters for RAG resolution calls and fallback searches,
  plus query count/token/deadline bounds; do not repurpose review or destination counters.
- Reserve the baseline discovery and Google-only R_pool Details entitlement before
  permitting incremental RAG cache misses. Run explicit/ordinary Google searches first.
- Cache hits cost zero API units. A failed direct ID costs one Details unit; fallback
  search costs a search unit; a subsequent Details miss costs another Details unit.
  Every real HTTP attempt counts; the current Google transport has retries disabled.
- Use atomic reservation/checking across operation totals and RAG sublimits before
  calling the provider. No charge refunds for failed paid attempts. Blocked budget
  checks are logged separately and do not increment HTTP-attempt counts.

**Budget decision requiring approval:** keeping the existing 12/20 hard ceilings can
leave little or no incremental capacity (especially fallback searches and long trips).
The design must then clip RAG target to available reserved headroom, including zero.
To permit a useful positive target consistently, approve explicit **V2-only total
ceilings** and normal limits in centralized configuration while preserving V1's exact
12/20 ceilings and normal values. A new RAG bucket must not secretly bypass a claimed
global limit; the effective V2 total is baseline allocation plus approved incremental
allocation and must be shown in trace/cost reports. This proposal recommends that
explicit V2 envelope, but does not freeze its numerical values or modify any limits.

Candidate counters count distinct admitted C_raw IDs, not every raw SQL hit or every
failed resolution. FINAL_POIS is charged once, after review-aware selection. Review,
Weather, Routes and Web budgets are preserved. RAG outage must not spend their budgets.
No unbounded second pass or budget refund is used to conceal replacement costs.

## 8. Canonical merge and two kinds of provenance

Use returned current **Google Place ID** as the canonical key. Source RetrievalEntity
IDs/FSQ IDs remain provenance. Union genuine Google interest hits and RAG discovery
hits separately; deduplicate repeated hit records by stable source/query/entity IDs.
Keep current Details once per canonical ID, preserve opening-date conflicts and
explicit exclusions, and never overwrite current Google facts with historical data.

| Case | discovery_sources | metadata_sources |
| --- | --- | --- |
| Google discovery plus optional local metadata | GOOGLE_PLACES | GOOGLE_PLACES, TRIPWORLD |
| RAG discovery then Google identity/current-info acquisition | TRIPWORLD_RAG | TRIPWORLD, GOOGLE_PLACES |
| Independent Google and RAG discovery | GOOGLE_PLACES, TRIPWORLD_RAG | GOOGLE_PLACES, TRIPWORLD |
| Explicit named-place path | USER_EXPLICIT (plus genuinely independent channels only) | GOOGLE_PLACES, optionally TRIPWORLD |

Google calls performed solely to resolve a RAG hit do not create GOOGLE_PLACES
discovery provenance. Likewise local metadata enrichment is not RAG discovery.
Store Google operation role (discovery vs resolution), original intent, raw search
position/count, RAG rank/cosine, corpus/space/hash versions, resolution path/attempts,
cache outcomes and stop reason. Actual run trace can later support source attribution;
this phase does not implement a formal V1-vs-V2 evaluation.

Google-first optional enrichment uses a batched indexed lookup on
`tripworld.entities.google_place_id`, which already has a unique nonnull index.
No extra Google request or embedding is needed. Missing rows/DB failures leave the
Google candidate untouched. Even locally excluded/anomalous metadata must not veto a
valid Google-first candidate: the TripWorld production policy governs its discovery
channel, not Google's independent path. Keep flags informational and priors out of
current facts/Profile. Lookup results also are not independent semantic interest hits.

Keep original Google observations immutable alongside the canonical union. If no
usable RAG contribution survives, run the original Google-only normalization and
selection projection, including its search-coordinate behavior. Do not let a failed
RAG attempt's cached Details silently change that baseline projection; this makes
the promised outage-equivalence test precise.

## 9. Q_rel alternatives and recommendation

Current `policies/poi_selection.py` computes, for each real Google hit:

```text
w = 1.0 explicit_requirement, 0.8 normal_preference, 0.4 fallback
q(hit) = 30*w                                  if raw_count == 1
         30*w*(raw_count-1-zero_based_rank)/(raw_count-1) otherwise
Q_rel = max(q(hit)), default 0
```

`actual_result_count` is the **raw response length**, even when invalid DTO rows are
filtered. It is not post-dedupe count or usable Google resolution count. Example:
Google normal-preference rank 0 of 20 contributes 24; rank 19 contributes 0. A lone
name-fallback result would wrongly contribute 24 if misrepresented as interest search.
RAG is 1-based Top-K rank with a truncated caller-chosen K, cosine has no shared
calibration, and resolution failures must not rerank the survivors to increase Q.

| Alternative | V1 compatibility / determinism | Interpretability and source comparability | Complexity / experimental implication |
| --- | --- | --- | --- |
| A. Conservative Google-evidence Q; RAG-only Q=0 | Exact V1 Q formula retained for genuine Google hits; deterministic | Zero means no Google ranking evidence, not semantic irrelevance; makes no rank equivalence claim | Smallest new scoring policy; biases against RAG-only places and may underestimate its potential contribution |
| B. Explicit source-aware ordinal RAG relevance, e.g. bounded rank decay combined by max | V1 unchanged if opt-in only; deterministic with fixed query policy | Transparent new heuristic, but RAG score scale and Google scale still uncalibrated; not a relabeling of rank | More parameters, multi-query effects and ablations needed later; changing fetch K must not inflate scores |
| C. V2-wide common rank fusion such as weighted reciprocal rank | V1 binary can stay unchanged; V2 Google-only ranking can change | Common ordinal rule is explicit, but assumes comparable source weights rather than proving relevance equivalence | Changes selection even beyond added discovery, confounding future mechanism comparisons |
| D. Obtain new Google interest-query evidence for each RAG candidate | Can use a real Google hit if actually returned, never an invented rank | Restores provider evidence but cannot force Google to rank a desired candidate | Extra quota, possible exclusion of exactly the long-tail candidates RAG should add |
| E. Learned/calibrated or LLM relevance | V1 can remain separate, but new model/evaluation dependence | Calibration needs labels; LLM adds uncertain scoring behavior | Outside this phase and project scope; reject for initial integration |

**Recommend A as an explicit, conservative Phase 6 starting policy**, subject to user
approval. Preserve all genuine Google hits and compute Q from them. For RAG-only
candidates set Q=0 with `relevance_evidence=google_rank_unavailable`; cosine/rank
control discovery resolution order and remain trace metadata, not a final score.
An overlapping candidate keeps its existing Google Q unchanged. No source-count bonus.
Do not claim this makes sources equally competitive: a RAG-only venue can lose to a
Google top hit solely because only the latter has Q evidence. If that tradeoff is
unacceptable, choose B explicitly before implementation; do not silently compensate
with a hidden quota, cosine threshold or positive constant.

C_cov retains the formula `max(25*intent_weight for uncovered interest IDs)`, default
zero. Introduce a source-independent **InterestCoverageHit** separate from Google
QueryIntentHit. A RAG result from a POI-interest query contributes that same normalized
interest ID/importance after successful canonical resolution; this is discovery
association, not verified factual suitability. Identical interests from two channels
count once. Pure experience queries do not add coverage IDs or manufacture E evidence.
Coverage for interest queries remains a retrieval heuristic just as provider hits
were, so this extension must be explicit in later comparisons.

Stable V2 ties: descending total, then the best genuine Google rank if present,
then canonical Google ID; missing Google rank sorts after finite ranks. This retains
the existing ordering for Google-only inputs and leaves RAG-only ties deterministic
without mixing rank spaces. RAG rank remains acquisition priority only under A.
Required named places keep priority and existing relative ordering. Review-sensitive
ties must use the same key, not `min()` over an empty Google-hit list.

## 10. Selection contracts, reuse and unchanged C/G/R/E

Propose `V2PlaceSelectionInput` with canonical candidate, a possibly empty list of
real `google_query_hits`, separate coverage hits, RAG hits/provenance, and the existing
structured evidence/rating/opening-date/coordinate state fields. Retain V1's strict
nonempty `PlaceSelectionInput.query_hits` invariant. Do not loosen QueryIntentHit or
populate it with synthetic rows.

One narrowly scoped shared extension is needed for downstream `PlaceCandidate`:
allow `provider_rank: int | None` with null representing **no Google discovery rank**,
while V1 normalization still always supplies the same integer. Preserve V1's serialized
values and output path. V2 source query/category come from real originating semantic
intent; provenance lives in a V2 sidecar rather than unbounded fields in itinerary DTOs.
Audit every consumer before implementation: legacy `shortlist()` sorts provider_rank
and must never receive V2/null-rank inputs. This schema extension and its compatibility
tests require approval; an alternative separate canonical candidate type would require
more downstream projection/generalization, not justify a fabricated rank=0.

Use V2-owned selection/merge orchestration and a source-aware selector policy. Reuse
unchanged pure eligibility, distance, rating and E scoring via a narrow structural
candidate view/protocol where needed; do not pass arbitrary duck-typed dictionaries.
Factor only the common pure greedy loop if practical, with V1's existing Q/coverage/
tie functions as unchanged defaults and V2's policy explicit. Differential tests must
prove the default V1 path exactly equivalent, including conflicts and review sensitivity.
Do not create a giant shared graph full of version conditionals.

Review selection must use that same V2 selector in its counterfactual tests. Reuse
the existing Reviews acquisition, preprocessing, bounded Profile prompt/validation
and `score_experience` semantics. A narrowly injected selection/coverage/tie policy
with V1 defaults is preferable to copying the entire review pipeline. V2 funnel and
review input interfaces should expose the existing capacities, must/excluded IDs,
conflicts and evidence while adding the new provenance. The exact type seam is a
reviewable refactor prerequisite, not an assertion the present classes already support it.

- **C_cov:** same 25*weight uncovered-interest formula; source-independent association
  extension documented above. No additional reward for multiple retrieval variants.
- **G_geo:** same initial 5, within 3 km 10, within 10 km 5, otherwise 0; use canonical
  Google coordinates. Current V1 normalization retains its search candidate even
  after Details; V2 must explicitly project current Details coordinates into its
  canonical candidate before final scoring/routes, leaving V1 untouched. Before
  Details, Google search coordinates are still current provider observations.
- **R_rating:** unchanged bounded Google-rating function, missing=0, no historical
  TripWorld rating. Keep stage visibility symmetric despite early RAG Details.
- **E_exp:** unchanged review-supported Profile -> deterministic score, no category
  priors or RAG similarity accepted as Profile evidence. Unknown remains unknown.

The shared total stays Q+C+G+R+E. Candidate membership and hence review sensitivity,
coverage and geography can change in V2; unchanged formulas do not imply unchanged
selected sets. Current V1's general feasibility limitations are not repaired here.

## 11. Graceful degradation and consistency

| Condition | Required behavior |
| --- | --- |
| Zero RAG hits | Continue Google observations; record empty retrieval |
| OpenAI query embedding error/timeout | End affected RAG work within deadline; no second requirements call; use Google path |
| PostgreSQL outage/configuration/version mismatch | Mark RAG unavailable; no corpus mutation/rebuild at runtime; use Google path |
| Historical Google ID fails | Attempt configured bounded name/location fallback; preserve failure provenance |
| Fallback ambiguous/fails | Reject this hit, continue stream; no fabricated identity |
| FSQ-only cannot resolve | Same rejection/replacement rule |
| Google RAG allocation exhausted | Stop new misses; retain successful candidates and baseline budget entitlement |
| All RAG hits fail | Google-only staged selection with existing cache/results; no repeat discovery or interpretation |
| RAG hit overlaps Google | Merge provenance/intent association, reuse cached current info, one canonical candidate |
| Optional Google-first metadata lookup fails | Continue unchanged Google candidate |
| RAG produces excluded/invalid current POI | Do not admit; continue under the same budget |

Do not swallow baseline errors: if Google itself has no viable candidates, preserve
the existing clear failure behavior; RAG cannot guarantee generation without successful
current resolution. With identical successful Google responses and no usable RAG
contribution, the Google-only selection result should match V1. A service outage must
not alter Q, candidate capacities, named-place requirements or planner prompt semantics.
Returned output identifies V2 even if its RAG channel degraded; trace states the fallback.

## 12. Proposed implementation files and scope

Nothing in this list is created as executable Phase 6 code by this design task.

| Proposed area | Responsibility |
| --- | --- |
| `backend/app/versions/v2/{graph,state,runner,config}.py`, `scripts/run_v2.py` | Separate version orchestration, same typed extraction/date/output semantics |
| `backend/app/tripworld/integration/{models,queries,retrieval,resolution,merge}.py` | Typed query/provenance contracts, bounded synchronous-service adapter, ranked resolver, canonical union |
| `backend/app/services/v2_candidate_funnel.py` | Source union before C_raw and cache-aware staged enrichment |
| `backend/app/policies/v2_selection.py` | Approved Q policy, coverage projection, stable ties |
| Small public facade in `services/evidence_acquisition.py` | Existing identical request keys/outcomes plus explicit V2 acquisition charging, V1 defaults preserved |
| Narrow policy seam in `poi_selection.py`, `review_sensitivity.py`, `review_selection.py` | Common pure selection/review loop with unchanged V1 defaults; V2 policy explicitly injected |
| `evidence/models.py` and minimal read-only selection input protocol | Nullable absent Google rank and shared evidence view, without fake provider hits |
| `runtime/{budget_limits,budget,config_models,config_loader}.py`, `config/runtime.yaml` | Explicit V2 allocations/ceilings/settings with backward-compatible V1 defaults; no hidden constants |
| V2-focused tests under `backend/tests/versions/v2/`, `backend/tests/tripworld/` | Fake-provider integration, policy and degradation checks |

Existing Phase 5 migrations/corpus/vector-space files remain unchanged. Batch local
Google-ID metadata lookup can live in the integration repository adapter and use the
existing index. No HNSW, IVFFlat, extra DB service, corpus refresh, reranker, new LLM
parser, frontend rollout or V3 validation/repair is in scope.

V2 settings should be one versioned optional section of the centralized runtime
configuration, validated only as appropriate, with old V1 values unchanged. Do not
make V1 startup require OpenAI embedding credentials or PostgreSQL. A V2 run with
unavailable RAG dependencies should log that channel's failure and use its Google
path; malformed policy values should still fail configuration validation.

## 13. Focused implementation test plan (future, no live paid calls)

Use fake Google/OpenAI providers, fixed request date, a tiny entity fixture and isolated
test DB where SQL integration is necessary. Assert calls, keys, scores and trace
provenance as well as final IDs:

1. TripWorld-only discovery resolves to a canonical Google POI; real Google hits remain
   empty, Q=0 under A, legitimate interest coverage present.
2. Google-only discovery reproduces V1 score vectors, ties, conflicts and final IDs.
3. Independent dual discovery produces one canonical candidate with two discovery
   sources; repeated RAG hits do not duplicate acquisition, score bonuses or capacity.
4. Google-first local metadata enrichment adds TRIPWORLD metadata only; missing or
   ineligible local records never reject or relabel Google discovery.
5. ID Details success is reused by contender enrichment with exactly one paid call.
6. Stale ID -> unique name/location fallback -> Details; count all three misses.
7. Failed/ambiguous fallback -> next ranked hit, including FSQ-only success/failure.
8. Name equality at distant coordinates and nearby homonyms are rejected; returned-ID
   redirects preserve alias provenance and avoid a second Details call.
9. Usable target stops acquisition; overlaps do not falsely satisfy net-new target;
   exhausted lists, configured max K, call/fallback budgets and deadlines all terminate.
10. Cache hits spend zero; failed outcomes are reused; mask/language mismatch is a
    distinct request; no DTO/result-type cache collision or duplicated in-flight call.
11. RAG budget use cannot consume reserved baseline Details/search/review capacity;
    current hard-limit clipping and any approved V2 total envelope are enforced.
12. USER_EXPLICIT required/optional/excluded identities remain authoritative across
    union, and RAG does not promote an unresolved name to a silently resolved must-visit.
13. OpenAI/DB outage, zero hits and all-resolution-failed cases reproduce Google-only
selection with one interpreter invocation, no repeated paid discovery, same dates.
14. Changing category priors cannot populate ExperienceProfile/E_exp; only actual
    review-derived validated evidence changes E. Review counterfactuals use V2 Q/ties.
15. Current Google coordinates drive G/routes; TripWorld coordinates remain provenance;
    early RAG rating cannot influence pre-Details narrowing asymmetrically.
16. Q alternatives have explicit unit expectations: no fake rank/count, no cosine Q,
    no fallback-name-query Q, no post-filter rank renormalization, shared-interest C
    counted once, optional missing Google rank never crashes a legacy consumer.
17. Stable output under shuffled input order, duplicate query hits and (if enabled)
    variable completion timing; no source-order-dependent canonical metadata choice.
18. V0/V1 full regression remains green; V1 startup works with RAG dependencies absent;
    V2 entry point works independently; product default does not switch accidentally.

Run focused tests during implementation, then full backend regression and Ruff.
No live smoke, formal relevance benchmark or V1/V2 outcome comparison is authorized
by this design-only task. A later user-approved small integration smoke may confirm
provider wiring after offline checks.

## 14. Decisions requested before implementation

1. Approve conservative Q option A (genuine Google Q, RAG-only zero) or choose explicit
   source-aware option B for a separate parameterized relevance proposal.
2. Approve V2-only query/provenance/coverage contracts, nullable absent Google rank,
   and the minimal shared acquisition/selection/review seams with strict V1 parity.
3. Choose incremental V2 Google spend envelope versus strict existing-ceiling headroom;
   then set usable target, oversampling/max K, query cap and fallback cap together.
4. Approve conservative unique name/alias plus geographic matching; choose radius,
   identity-distance tolerance and timeout values through small development fixtures,
   without freezing arbitrary constants here.
5. Start sequentially; any later concurrency increase requires single-flight and
   deterministic budget reservations. Preserve exact pgvector retrieval for now.

Main risks: Q=0 under-rewards RAG-only candidates; name matching can miss aliases;
historical identity merges mix contexts; paid resolution may dominate latency/cost;
too little reserved headroom disables useful retrieval; coverage remains uneven;
shared-policy seams can accidentally change V1 if not differentially tested.
The boundary is explicit: this document is a proposal, not approval to implement it.
