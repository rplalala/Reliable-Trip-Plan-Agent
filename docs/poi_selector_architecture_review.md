# Shared V1/V2 POI Selector Architecture Review

Status: **Architecture B approved in principle; revised requirement contract proposed,
awaiting approval. Design only.** Date: 2026-09-18.
No executable code, selector, Phase 6 integration or version reopen is implemented
by this report. No paid model/Google calls were made. Phase 1-5 history and artifacts
remain accepted. The prior Phase 6 Q_rel adaptation is on hold, not an approved design.

Revision authority: **Section 20 supersedes the earlier closed selector requirement
projection, exact final-count rule, and related migration assumptions.** Sections 1-19
remain as the original analysis, including historical sizing measurements. Approval in
principle does not authorize executable changes or a V1 reopen. The historical V1 freeze
remains intact. The revised principle is: **schema constrains structure, not the entire
space of possible semantics.**

## 1. Recommendation

Adopt **Architecture B: deterministic gates + one shared bounded two-stage LLM POI
selection service + deterministic output validation**, for both a deliberately
reopened V1 and the later V2. Keep the historical deterministic QCGRE version available
for reproducibility, but remove its weighted selection and counterfactual review
trigger from the new production path. Do not retain QCGRE as a hidden fallback.

This recommendation is architectural, not a measured assertion that the LLM selects
better POIs. The current code embeds Google rank in several contracts and selection
stages. A bounded combination decision over source-neutral canonical evidence avoids
inventing equivalence between Google rank and RAG cosine. This fits the project's
small candidate capacities and existing strict LLM/Profile boundaries. It introduces
real stochasticity, semantic-error risk and latency, so a new V1 freeze must depend
on development validation of those tradeoffs. Do not replace the frozen baseline
before that approval/validation sequence.

## 2. Actual current responsibilities

Inspected current files include `policies/poi_selection.py`, `poi_funnel.py`,
`poi_capacity.py`, `review_sensitivity.py`, `experience_selection.py`,
`services/evidence_acquisition.py`, `review_selection.py`, `evidence/selection_models.py`,
`experience_models.py`, the V1 graph/runner/prompts, runtime configuration, Foundry
client/DTOs and representative tests. Paths are under `backend/app/` unless stated.

| Current mechanism | Actual responsibility / coupling |
| --- | --- |
| `evaluate_poi_eligibility` | Exclusions, permanent closure, supported future-opening incompatibility, coordinate validity, required Details availability; temporary closure and unknown status remain date risks |
| `q_rel` | Max across genuine Google hits; rank normalized by unfiltered response length, weighted by explicit/preference/fallback importance |
| `c_cov` | Greedy marginal uncovered intent contribution; maximum 25 times intent weight, not a semantic match classifier |
| `g_geo` | Nearest already-selected candidate distance: initial 5, <=3 km 10, <=10 km 5, otherwise 0; not route feasibility |
| `r_rating` | Clipped Google rating signal in [-10,10], missing=0; no userRatingCount |
| `E_exp` | Review-supported profile interpreted into bounded preference score, with total constrained to [-15,10] |
| `select_pois` | Must-visit protection/conflicts, eligibility, repeated greedy Q+C+G+R+E, then best Google rank / Place ID ties |
| `run_candidate_funnel` | Uses this selector for C_raw, R_pool and no-review final; Details/rating are acquired only for R_pool |
| `find_review_sensitive_candidates` | Repeatedly changes hypothetical E values and reruns the same selector; fetches reviews when final membership might flip |
| `ReviewSelectionService` | Cached review acquisition, Profile LLM/validation, iterative sensitivity and final selection |

`QueryIntentHit` explicitly represents an original Google response position;
`PlaceSelectionInput.query_hits` must be nonempty, and `PlaceCandidate.provider_rank`
is mandatory. `merge_search_observations` also chooses a canonical observation using
Google rank. These source assumptions do not disappear by replacing only the last
call to `select_pois`. Likewise the existing review trigger cannot be retained by
calling an LLM for every hypothetical E value: that would be an expensive, unstable
simulation loop and would reintroduce QCGRE dependence.

### Actual current capacities

`k_final=min(16,2*days+2)`, `r_pool=max(10,k_final+2)`,
`c_raw=max(20,2*r_pool)`, `review_pool_cap=min(6,ceil(k_final/3))`.
Current normal limits are candidates=36, Details=18, final=16, reviews/Profile=6.
All these example algorithmic capacities fit the current normal limits:

| Days | C_raw | R_pool / Details upper bound | k_final | Review/Profile upper bound |
| --- | ---: | ---: | ---: | ---: |
| 1 | 20 | 10 | 4 | 2 |
| 3 | 20 | 10 | 8 | 3 |
| 5 | 28 | 14 | 12 | 4 |
| 7 | 36 | 18 | 16 | 6 |
| 10 | 36 | 18 | 16 | 6 |

C_raw is **not** an upper bound on all raw discovered observations. The inspected
Melbourne and Singapore traces contained 105 and 118 distinct Google IDs before
narrowing. The new design therefore needs an explicit bounded admission policy before
the LLM; it cannot quietly send every search result.

## 3. Proposed common pipeline

```text
Existing single Requirement LLM -> validated typed requirements
 -> explicit named-place resolution + source discovery
 -> current Google identity acquisition as required by each source
 -> canonical ID merge / immutable discovery sidecar
 -> deterministic known-fact gate + bounded C_raw admission
 -> Stage A: cheap typed LLM shortlist (R_pool) + bounded reserves/review nominations
 -> deterministic Stage A validator
 -> current Google Details for shortlist, cache reuse, bounded reserve replacement
 -> refreshed deterministic gate
 -> bounded review acquisition for eligible nominated contenders
 -> existing Review LLM -> validated ExperienceProfile
 -> Stage B: typed review-aware final LLM selection (k_final)
 -> deterministic Stage B validator
 -> selected canonical POIs
 -> existing Weather / Routes / Official Web -> itinerary LLM
```

The LLM judges semantic preference tradeoffs and candidate combinations **inside**
the admitted set. It has no tools and cannot acquire extra candidates, change provider
facts, enlarge budgets or declare a failed identity resolved. Stage A's gate is
provisional on cheap current Google observations; Stage B's gate requires current
Details. Calling the first pool "fully fact-verified" would overstate the evidence.

Keep R_pool as a **contender/Details pool**, not a pool in which every POI receives
reviews. Reviews still cover at most the much smaller review_pool_cap. RAG-only
candidates may already have full Details from resolution: reuse them, but suppress
rating/Profile from Stage A for all channels so early acquisition does not give one
source systematically richer preference evidence. Stage B exposes comparable current
Google fields for every contender; no historical TripWorld facts fill missing fields.

The initial implementation should execute Stage A/B sequentially. It may short-circuit
an LLM call when deterministic constraints leave only one possible set, recording
`forced_set` rather than claiming a model decision. No second requirements parser.

### Bounded pool admission without a hidden weighted selector

First reserve every resolved, currently admissible required ID. If required count
exceeds the pool/final capacity, report a conflict instead of discarding requirements.
Fill remaining C_raw slots by deterministic round-robin across normalized typed
POI-interest buckets, preserving importance tiers and deduplicating canonical IDs.
Use canonical ID ordering inside an admission bucket; unmatched fallback candidates
form a final bucket. A candidate present in several buckets consumes one slot.
Record dropped IDs/counts and bucket associations for diagnostics.

This is a mechanical capacity policy, not a claim of optimal relevance; ID-based
admission can omit better venues and needs development inspection. Google rank and
RAG rank may still prioritize bounded acquisition before admission, but do not become
cross-source weights or the final score. Use the same admission algorithm, capacities
and serialization for V1/V2. Source quota bonuses and source labels in model input are
not part of this recommendation.

## 4. One-stage versus two-stage

| Design | Benefits | Costs / limitation |
| --- | --- | --- |
| One final LLM after rich evidence for all C_raw | One selector call; can compare the complete admitted rich pool | Up to 20-36 Details calls instead of 10-18; reviewing all would exceed the 2-6 review cap. Using a cap still needs an independent review-allocation rule |
| Deterministic pre-narrowing to R_pool, capped reviews, one final LLM | One selector call; keeps provider budgets small | Deterministic preselection still determines which candidates can win; retaining QCGRE here preserves much of the original source problem |
| Recommended two-stage | Stage A provides semantic shortlisting before paid enrichment; Stage B considers bounded Profile evidence; all provider counts remain capped | Two sequential selector calls; Stage A omissions cannot be recovered freely; review allocation needs a replacement policy |

Two-stage is preferable for this repository because selective enrichment was an
intentional V1 design and the code already distinguishes C_raw, R_pool and final sets.
It is **not** inherently cheaper than current QCGRE: selector calls are new, and the
replacement review policy may consume more of the existing cap. A simpler one-stage
alternative remains viable if measured latency becomes unacceptable, but should be
a separately approved architecture, not two concurrent production defaults.

## 5. Common typed input and model-visible projection

**Superseded projection:** use section 20.8 for requirements, linked associations and
stage projections. Candidate factual authority described here still applies.

All proposed models use strict validated fields, immutable domain objects and
`extra=forbid`. Transport DTOs follow the existing Foundry pattern. Bounds below
are proposed contract limits; operational counts still come from configuration.
String/array bounds must be checked in application code even if the provider's strict
JSON Schema subset cannot express every bound.

### SelectorContext

| Field | Type / meaning |
| --- | --- |
| `contract_version`, `evidence_policy_version` | Application-owned version strings |
| `destination`, `start_date`, `end_date`, `trip_days`, `traveler_count` | Existing validated trip metadata; no raw request dump |
| `interests` | Up to 24 typed `{id, text<=160, importance}` from PoiInterest |
| `experience_preferences` | Up to 16 typed `{id, kind, importance}` using existing enum |
| `required_ids`, `excluded_ids` | Canonical Google IDs produced by deterministic identity handling |
| `selection_min`, `selection_max` | Application-computed bounds for the current stage |
| `review_limit` | Stage A nomination upper bound, at most current effective review cap |
| `unresolved_hard_constraints` | Read-only typed constraint/check IDs and statuses; not model waiver requests |

A separate orchestration context retains validated source spans, request identity,
budget/deadline, model/config hash and discovery metadata. Do not embed credentials,
request UUID, system_version or an instruction that this is V2 into the selector.
The same input evidence must produce identical model messages/schema/configuration
regardless of whether the caller is V1 or V2.

### CandidateForSelection

| Field | Type / authority |
| --- | --- |
| `place_id`, `name` | Canonical Google ID and current Google name, name capped at 160 |
| `types` | Normalized current Google primary type; adapter currently does not expose a complete type list, so do not invent it |
| `latitude`, `longitude` | Finite current Google coordinates |
| `distance_from_destination_km` | Deterministic Haversine calculation |
| `nearest_neighbors` | Up to three `{place_id,distance_km}` among this stage's candidates; not a route-time matrix |
| `rating`, `rating_state` | Stage A always null/not_acquired; Stage B current Google value or explicit missing state |
| `required` | Application-owned flag consistent with context |
| `business_status`, `risk_flags` | Current structured evidence and deterministic gate output |
| `interest_ids` | Deduplicated possible associations with user interests, not proofs of suitability |
| `evidence_refs` | Opaque IDs into the immutable current-evidence ledger |
| `experience_profile` | Stage A null; Stage B bounded projection described below, including explicit unavailable |

No Google rank, actual_result_count, RAG cosine/rank, numeric Q/C/G/R/E or source
names enter the default model-visible view. `discovery_provenance` and
`metadata_provenance` stay in a parallel typed application record keyed by place_id:
source/query/entity IDs, ranks, hashes and resolution history remain inspectable.
This is stronger than telling a model "do not favor TripWorld" while showing its label.

TripWorld semantic priors explain retrieval in that sidecar; do not send their enriched
descriptions to Stage B as extra factual evidence. A RAG-associated interest is still
a hypothesis, not an assertion of public access or accessibility. If future work
exposes priors to the selector, that is an extra V2 information mechanism requiring
an explicit comparison change, not merely the addition of discovery candidates.

For long or numerous associations, retain all IDs in the ledger and project a bounded
stable subset per candidate; preserve required associations first and disclose
truncation. Token limits are checked before calls, with deterministic compaction;
never truncate required IDs or hard-gate evidence to fit a prompt.

## 6. Stage A and Stage B outputs

### Stage A: ShortlistDecisionDraft

```text
selected_place_ids: unique ordered IDs, exact target min(R_pool, admitted count)
decisions: one DecisionRecord per selected ID
reserve_ids: disjoint ordered candidate IDs, bounded reserve_limit
review_requests: bounded {place_id, preference_id, dimension} records
```

The shortlist order is an acquisition priority, not itinerary order. A reserve_limit
of four is used only in the sizing example; choose its operating value at approval.
Reserve replacements stop at the existing total Details-attempt budget. R_pool
caps valid contenders; a failure does not authorize spending another full R_pool.
Required IDs are acquired first regardless of proposed order. Review requests are
nominations, not tool commands; the deterministic allocator validates and caps them.

### Stage B: SelectionDecisionDraft

```text
selected_place_ids: unique IDs, exact application-computed target
decisions: one DecisionRecord per selected ID
```

Common `DecisionRecord`:

```text
place_id: supplied canonical ID
requirement_ids: unique references to supplied requirement IDs
role: required | interest_anchor | complement | geographic_companion
evidence_refs: supplied evidence IDs belonging to this candidate or its distance edge
rationale: at most 120 characters, brief supplied-evidence explanation
```

No arbitrary scores, revised facts, opening hours, extra places or routing instructions
can appear. A rationale is a model explanation, not causal proof or accepted factual
evidence. Do not request chain of thought. It does not drive budgets or override gates,
and should not be passed as authoritative evidence to itinerary generation.

The application wraps validated drafts in `SelectionDecision` with
`stage`, `input_sha256`, `selector_version`, actual deployment/returned-model metadata,
`prompt/schema/config hashes`, attempt count, validation status and fallback/forced-set
status. **The model must not self-report its authoritative version or input hash.**
Unused/rejected-ID narratives add tokens without operational value and are omitted.
The application computes the unused set by subtraction.

## 7. Deterministic authority and count rules

**Revision:** section 20.6 specifies the operationalization ledger and unresolved-hard
policy; section 20.9 replaces the exact Stage B target with bounded flexible cardinality.

Keep canonical identity, current Google resolution, dedupe, required/excluded policy,
coordinate validation, permanent closure and supported impossible-date rules outside
the selector. Current `evaluate_poi_eligibility` should be extracted into a source-neutral
eligibility module, not deleted with the scoring functions. Preserve temporary-closure
and unknown-state risk distinctions unless a separately approved rule changes them.

`HardConstraintCheck` is an application record:
`{constraint_id, scope, status: pass|fail|unknown|unsupported, evidence_refs, rule_version}`.
Only registered deterministic predicates with appropriate evidence can yield pass/fail.
The present contracts do **not** implement arbitrary user hard constraints. For example,
PREFER_ACCESSIBLE is a preference, review accessibility is subjective, and total-trip
cost/route feasibility is not known from this POI pool. Do not claim the new gate can
certify them. Reuse typed existing meanings; a new candidate-level hard constraint
needs an explicit shared extraction/check contract in the existing single requirements
call, not keyword parsing or selector interpretation.

For a genuinely mandatory candidate-level predicate with unknown/unsupported evidence,
return an unresolved constraint/clarification or obtain already-authorized evidence;
do not label the candidate compliant by LLM judgment. Whole-itinerary constraints remain
generation inputs and explicit unresolved limitations until appropriate downstream
checks; this preselection gate is not V3's validator. A known individual admission cost
over the entire budget could support exclusion, but missing costs cannot prove feasibility.

Required unresolved, required+excluded conflicts, required infeasible, or required count
exceeding capacity return a deterministic `SelectionBlocked`/clarification result.
Do not fabricate IDs, silently relax the requirement, or ask an LLM to choose which
must-visit to drop. User approval of a partial plan is separate from selection validity.

For Stage B let E be eligible supported contenders and M feasible required IDs:
`target=min(k_final, |E|)`, `selection_min=selection_max=target` for the initial policy.
If M is not a subset of E or |M| exceeds k_final, block. If E is empty, preserve a
clear no-viable-candidates result. A reduced count due to scarcity is disclosed by
code, not invented by the selector. k_final is a POI-pool target, not a promise to
schedule each POI or prove daily feasibility. A later flexible count policy needs a
versioned rule, not an unbounded natural-language exception.

## 8. Validation, retry and explicit fallback

Validate both stages using the immutable input snapshot:

1. Schema/types/bounds; refusal, timeout, incomplete output and malformed JSON are failures.
2. Selected/reserve IDs exist in the appropriate pool; no duplicates or forbidden overlap.
3. All feasible required IDs remain; excluded/ineligible IDs are absent; counts meet bounds.
4. Decision records map exactly one-to-one to selected IDs; role and required flag agree.
5. Requirement and evidence references exist, belong to the referenced candidate/edge,
   and review dimensions correspond to genuine typed experience needs.
6. Hard-gate status has not changed; newly failed candidates are not silently retained.

Referential validation does not prove a rationale's semantic truth. Keep that distinction
explicit. Names and Profile summaries are untrusted data; prompts delimit them and deny
tool/instruction authority. Schema validation alone cannot prevent semantic hallucinations.

Recommend **one repair retry total per trip across both stages**, not an unbounded
per-candidate loop. Retry only invalid structured decisions using concise validator
error codes and the same evidence snapshot, when time/token budget remains. Do not
retry auth/outage errors blindly. The transport retains `max_retries=0`, avoiding
hidden multiplicative retries. Enforce at most three selector calls in a normal
two-stage run including that shared retry.

After Stage A failure: deterministic required-first, interest-bucket round-robin with
canonical-ID ties creates the bounded shortlist/reserves. Review acquisition still
uses validated existing preferences and its cap; do not trust failed nominations.
After Stage B failure: choose feasible required IDs first, then the same mechanical
interest-bucket/canonical-ID fallback among the rich eligible pool to target count.
Pass fallback output through the same validator. If constraints are unsatisfiable,
return SelectionBlocked, not a knowingly invalid itinerary.

Do not simply remove invented IDs from a bad response and call it successful selection;
that can lose required coverage or underfill counts. Record `decision_origin=fallback`
and disclose reduced semantic assurance. The fallback is a documented availability
path, not a second production QCGRE selector or a claimed semantic optimum.

## 9. Review evidence without counterfactual QCGRE

Retain `preprocess_reviews`, the bounded Review LLM prompt, `ExperienceProfileDraft`,
`validate_profile_draft`, confidence/ref handling and per-request review/Profile cache.
The existing profile has five dimensions: crowding, walking_intensity, accessibility,
family_friendliness and visit_duration. It has **no atmosphere/quietness field**;
do not invent one because TripWorld's library prior suggests quietness.

Stage A may nominate review contenders for supplied experience preferences. The
allocator requires that a nominee is a rich, hard-gate-valid contender, has an actual
relevant user preference, and lacks usable Profile evidence. Deduplicate by canonical
ID, check cache first, prioritize non-required alternatives whose membership remains
discretionary, then respect Stage A priority with stable ties. Required POIs do not
normally need reviews just to decide membership. Never request reviews for every
candidate automatically. If nominations are invalid/exhausted, use the bounded
deterministic allocator over remaining contenders; no extra selector call is needed.

No experience preferences -> no review calls solely for selection. Review failures
and unsupported signals remain unavailable/unknown; they do not imply a bad place.
Stage B sees at most five signals per acquired Profile, confidence, compact review
references and at most a 240-character summary. It sees no raw review text/URLs.
Reference IDs prove provenance linkage, not objective truth or official certification.

The clean separation is:

- Requirement LLM: what does the user want?
- Review LLM: what do these supplied reviews support?
- Selector LLM: which allowed combination fits those typed requirements?
- Deterministic code: identity, supported factual predicates, bounds and validity.

Review ordering may not match the old sensitivity policy, and review use may rise
within the same cap. This is an intentional common V1/V2 redesign that must be
recorded at re-freeze; do not claim the exact old acquisition behavior survives.

## 10. Model/provider recommendation and actual configuration

The current `.env.example` and locally inspected deployment-name value identify
`gpt-5.6-luna`. V1 inherits V0 Foundry settings; the same injected structured client
serves requirements, Profiles and generation. The adapter uses `ChatOpenAI` against
a Microsoft Foundry v1 endpoint, Responses API, strict `json_schema`, explicit
DTO-to-domain bindings and `max_retries=0`. It currently sets no explicit temperature,
reasoning effort, selector output cap or selector-specific timeout, and rejects domain
schemas missing from `_FOUNDRY_BINDINGS`.

Recommend the **same Luna deployment family with a separate bounded selector task
configuration shared identically by V1/V2**, rather than altering other LLM tasks or
introducing an untested new model. Its bounded structured judgment role and existing
provider plumbing justify this choice; mere availability does not establish quality.
The public model page lists Structured Outputs and configurable reasoning support.
[OpenAI model reference](https://developers.openai.com/api/docs/models/gpt-5.6-luna).

Proposed initial validation configuration: reasoning effort `low`, no tools, no
conversation history, explicit per-stage timeout and output cap. Do not assume
temperature=0 or seed is supported/deterministic; only set supported controls after
the actual deployment capability check. Resolve/log the deployed model version when
available; a deployment name alone is not an immutable weight snapshot. Use the same
model, effort, schemas, prompts, serialization and guards for both versions, with no
per-version override. No training or fine-tuning.

Strict schemas improve format adherence, not truth or preference quality; handle
incomplete/refused responses and validate domain invariants in code.
[Structured Outputs documentation](https://developers.openai.com/api/docs/guides/structured-outputs).

## 11. Local serialized token-size experiment

**Historical measurement:** these fixtures predate the open semantic contract. They
are not measurements of the revised payload. See section 20.13 for re-sizing requirements.

This task measured actual serialized **design fixtures**, without creating executable
selector code or invoking a model. Two fixture families were used:

- Existing `_candidate` / `FakePlacesProvider` DTO shape from
  `backend/tests/versions/v1/fakes.py`, expanded to the actual configured capacities.
- The same fixture with ID/name strings replaced by actual Google observations from
  local V1 Melbourne run `9418b692-5291-4c2d-b3ff-5864ee0acf2d`, preserving realistic
  identifier/name lengths. The trace contains 105 distinct IDs. Its SHA-256 is
  `0ad526578d624143440ffe66554bafd707b22157c9c289ef2c7b2df3ef98d30c`.

**Only IDs/names are observed facts in the second family. Coordinates, 4.5 ratings,
interest associations, Profiles and example selection outputs are sizing fixtures,
not asserted current facts about those named venues and not LLM decisions.** Current
traces use metadata capture and do not retain full provider/Profile payloads, so exact
live prompt reconstruction is unavailable. This limitation is preferable to inventing
missing evidence. Fixtures omit discovery labels and provider-native ranks.

Used compact UTF-8 JSON with sorted keys; `o200k_base` (the installed tokenizer's GPT-5
family mapping) is a local proxy, not authoritative Foundry billed usage. Each input
includes the draft system prompt (166 tokens) and draft output schema (A=229/B=150).
Transport chat framing, stricter final DTO descriptions and hidden reasoning are not
included. JSON schemas here are size prototypes; full validation is described above.
Three-nearest-neighbor features are bounded; no O(C_raw squared) textual distance matrix.

| Days | A candidates | B candidates | Profile fixtures | Stage A input | Stage B input | A visible output example | B visible output example |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20 | 10 | 2 | 4,791 | 2,918 | 1,031 | 355 |
| 3 | 20 | 10 | 3 | 4,791 | 3,022 | 1,067 | 701 |
| 5 | 28 | 14 | 4 | 6,494 | 4,035 | 1,455 | 1,047 |
| 7 | 36 | 18 | 6 | 8,177 | 5,151 | 1,870 | 1,399 |
| 10 | 36 | 18 | 6 | 8,177 | 5,151 | 1,870 | 1,399 |

The short-ID repository-only fixtures measured A=3,558-5,942 and B=2,326-4,038,
showing why counting abstract rows alone underestimates realistic identifiers and
neighbor references. A stress fixture with six fuller five-dimension Profiles and
long summaries raised the 7-day B input to **5,817 tokens**. These are bounded examples,
not maximum-token proofs; 24 verbose interests/multilingual names can cost more.

For implementation testing, propose input ceilings including prompt/schema/feedback
of A=12k, B=10k, with deterministic compaction/fallback if exceeded. Propose a 4,096
generated-token cap per call, **including reasoning**; validate sufficient headroom
before re-freeze rather than assuming the model always completes. No huge context
window is needed. All exact fixture texts, prototype schemas and measurements are
saved in ignored `data/tripworld/reports/selector_design/prompt_size_measurement.json`.
No reusable production script was added.

## 12. Cost and latency: measured facts versus estimates

The public OpenAI Luna rate consulted for this analysis is **US$0.20/M input** and
**US$1.20/M output** tokens. This is a reference price, **not verification of this
Azure/Foundry deployment's region, billing tier, discount or mapped model version**.
Use actual Azure rates before approving a monetary runtime budget.
[Model pricing](https://developers.openai.com/api/docs/models/gpt-5.6-luna).

At those reference rates, excluding reasoning/retries/caching:

| Days | Two-stage visible-token estimate, USD |
| --- | ---: |
| 1 | 0.003205 |
| 3 | 0.003684 |
| 5 | 0.005108 |
| 7-10 | 0.006588 |

Formula: `(A_input+B_input)*input_rate/1e6 + (A_output+B_output)*output_rate/1e6`.
An illustrative extra 1,000-4,000 reasoning tokens across the calls adds US$0.0012-
0.0048. Reasoning tokens are charged as output and share the generated-token limit;
the examples do not measure their actual count.
[Reasoning usage and limits](https://developers.openai.com/api/docs/guides/reasoning).

With the proposed 12k/10k input and 4,096 output caps, two selector calls cost at most
about **US$0.01423 at the reference rates**, assuming those are complete billed-token
bounds. One shared retry makes at most three calls, about **US$0.02155** in the
A-retry worst case. Provider framing must be included in enforced limits; these are
budget scenarios, not current bills. No cache discount is assumed.

Normal semantic model calls per trip are 1 requirements + 2 selector + r Profile +
1 itinerary = **4+r**, excluding unchanged Official Web Reasoner calls. With maximum
r=2/3/4/6 by trip length, this is 6/7/8/10 calls. Zero experience needs gives r=0;
forced-set short circuits can lower selector calls. A repair adds at most one. Existing
Profile costs, Google calls, RAG query embedding and downstream generation are **not**
included in the selector-only dollar table.

The new selector has **no measured latency yet**. The two inspected historical V1
traces provide eight Review-LLM-start to review-attempt-end intervals: 3.29-5.29 s,
median 4.16 s. They include Profile mapping/validation and are small-output semantic
tasks, not selector timings. One requirements extraction took about 9.81 s; its
different prompt/output is not a throughput calibration for the proposed selector.

For capacity planning only, assume combined A/B startup/reasoning overhead 4-10 s
and visible generation 40-100 tokens/s. The measured example outputs (1,386-3,269
tokens total) imply roughly **18-92 seconds of added selector latency**, before
extra stalls/retries. Those throughput assumptions are not observed guarantees.
Short bounded rationales or output DTO compaction could reduce this, but cannot be
advertised as a measured improvement. A suggested initial maximum stage deadline is
45 s with a shared trip selector deadline; truncation/timeouts take the documented
fallback. Budget and timeout values remain proposed.

Provider work remains bounded: ordinarily 10-18 shortlist Details attempts and 2-6
review attempts, not reviews for all 20-36 candidates. Failed Details and reserves
consume the same per-trip cap; RAG resolution incurs additional acquisition as already
identified in Phase 6 and must have an explicit envelope without starving baseline
Google work. An always-rich one-stage alternative would need up to 36 Details calls,
above the current hard ceiling of 20. Two-stage is financially plausible; **interactive
latency and fallback frequency are the primary unvalidated feasibility risks**.

## 13. Stability and reproducibility controls

Freeze one selector configuration for both versions: model/deployment revision where
possible, low reasoning setting, stage prompt versions, transport/domain schemas,
normalization, token bounds, validator/fallback versions and candidate admission policy.
Sort candidates by canonical ID, sort set-like associations and evidence refs, use
stable Decimal/date/coordinate serialization, and hash the actual model-visible payload.
Do not include timestamps, random IDs or unrelated trace data in the prompt/hash.
Profile acquisition timestamps remain in the evidence ledger; use a stable explicit
freshness projection if needed rather than incidental run-time noise.

Canonicalize the final selected **set** for downstream presentation (required IDs first,
then canonical ID), so incidental JSON list order does not change Routes pair ordering
or the itinerary prompt. Do not call this an optimized travel route. Stage A acquisition
priority remains a meaningful model output, so record and assess its variation.

Request-scoped selector-result caching keys on input/config/schema hash and stage,
not just destination. A failed schema response is not a valid cached decision. For
development repeatability measurements, bypass selector-result cache so repeated runs
actually sample the model; retain separately replayable validated outputs for debugging.

Run Trace should record counts, versions/hashes, actual returned model identifier,
attempts, validation codes, fallback state, elapsed time and input/output/reasoning
usage. The present `StructuredLLMClient` returns only a parsed domain object; extend
its adapter observability or an envelope to retain usage/refusal/incomplete metadata.
Do not claim current traces already provide token accounting. Existing sanitizer
matches keys containing `token`; review safe usage-field serialization so counters
are not accidentally redacted. Keep credentials protected. Full normalized input/output
capture remains opt-in, bounded and ignored; trace-write failure remains best-effort.

Proposed small development stability check, after separate approval: a few fixed
Google-only, mixed-source, sparse, tied, required-place and conflicting-experience
fixtures, e.g. five fresh runs each. Record pairwise Jaccard/exact-set agreement,
per-ID selection frequency, Stage A shortlist/priority agreement, required/excluded/
capacity violations, invalid-output/retry/fallback frequency, latency and usage.
Record raw draft validity separately from accepted-output validity. Final canonical
ordering is deterministic; it must not be used to conceal varying membership.
No perfect determinism or formal multilingual quality claim; this is a development
check, not an authorized formal benchmark, and no repetitions were run in this task.

## 14. Direct architecture comparison

| Dimension | A: provider-agnostic deterministic QCGRE | B: gates + bounded shared LLM selector + validator |
| --- | --- | --- |
| Conceptual cleanliness | Needs explicit Q evidence scaling and source-aware contracts | Direct typed candidate-combination judgment; no numeric rank equivalence |
| V1/V2 comparability | Good if both use the same revised policy; conservative original proposal leaves RAG underweighted | Good if both are re-baselined to exactly the same selector/input view |
| Semantic preferences | Limited to engineered features, enums and weights | Can consider combinations/context; may misunderstand or over-infer |
| Google/RAG comparability | Calibration/ordinal assumptions remain explicit work | Removes final score normalization; residual discovery/evidence biases remain |
| Reliability | Exact mechanical behavior and inspectable score decomposition | Mechanical guarantees after validation, but semantic correctness unproven |
| Reproducibility | Deterministic with frozen inputs | Replay possible; fresh API responses can vary |
| Stability | Stable ties/ranks by construction | Stable preparation/guards, stochastic set membership |
| Explainability | Faithful arithmetic and clear eligibility reasons | Bounded reasons and evidence references; rationales are not proof of causal reasoning |
| Complexity | More cross-source relevance engineering; mature existing code | Simpler final preference rule, more schema/validator/retry/config/evidence controls |
| Google API usage | Existing selective Details and membership-flip reviews | Same caps possible, different review allocation; RAG resolution cost persists |
| LLM cost | Requirements/Profile/generation only | Adds up to two normal selector calls; low reference dollar estimate |
| Latency | Local arithmetic is negligible | New sequential model latency; not yet measured |
| Review acquisition | Counterfactual E sensitivity tightly tied to QCGRE | Typed nominations plus deterministic limited allocator |
| Testing | Exact expected rankings and policy invariants | Exact guards/call limits plus fake model tests and separate live stability checks |
| Research clarity | Fully specified heuristic baseline | Shared semantic selector isolates added discovery if both versions use it; stochasticity must be reported |
| Maintainability | New semantic needs may add features/weights/calibration | Prompt/schema/version maintenance and provider drift replace some weight maintenance |

The main architectural advantage of B is real but narrow: final preference selection
no longer requires source-native numeric comparability. It does **not** eliminate
candidate admission bias, identity errors, incomplete evidence, model priors or
unavailable venues. Retain deterministic gates and do not sell the LLM as a factual
validator. I recommend B for the main revised V1/V2 system, with latency/stability
acceptance required before a new V1 freeze.

## 15. What remains of QCGRE

Choose option **A for the new active scoring path, plus C for history**: retire the
additive Q+C+G+R+E final/preselection score and its review-sensitivity trigger. Preserve
the underlying information as typed facts/associations, not five synthetic numbers.
Mechanical interest-bucket admission and geographical feature computation remain,
but do not compute a disguised weighted QCGRE score. Diagnostics may display measured
coverage/distances/rating/Profile availability without using them as an additive rank.

Keep the historical selector through repository history or an explicitly named offline
legacy module/fixture replay when justified. Do not expose two normal production
selector switches indefinitely. No new baseline implementation or formal evaluation
is authorized now. Later approved same-candidate/evidence evaluation could compare
preference alignment, stability, constraints, diversity, latency and cost; an end-to-end
comparison must separately account for changed review acquisition and candidate pools.

## 16. Reopen and exact version difference

The existing V1 freeze on 2026-09-15 remains historical truth. This task is **not**
approval to reopen it. Proposed sequence:

1. User approves this architecture and an explicit V1 reopen scope/budgets.
2. Preserve a recoverable historical checkpoint and configuration/evidence manifests;
   commits/tags require separate explicit authorization, not automatic Git operations.
3. Implement the common selector in revised V1, with its old discovery sources only.
4. Complete offline guards/regression, then separately authorized bounded live wiring,
   latency and stability checks. Update documentation to actual results, including failures.
5. User explicitly re-freezes revised V1; record a new checkpoint, not a rewrite of the old one.
6. Revise/approve Phase 6 around that same selector and then add RAG discovery in V2.

```text
Revised V1:
typed requirements -> explicit + Google -> canonical gate/admission
 -> shared Stage A -> capped Details/Reviews/Profile -> shared Stage B + validator
 -> same downstream evidence/generation

V2:
typed requirements -> explicit + Google + TripWorld RAG (on-demand Google resolution)
 -> same canonical gate/admission
 -> same Stage A -> same capped Details/Reviews/Profile -> same Stage B + validator
 -> same downstream evidence/generation
```

The selector never receives system_version or a RAG bonus. Given identical canonical
evidence and requirements, V1/V2 produce byte-identical model requests, although
separate fresh model responses need not be identical. Different candidate membership
can change which reviews are acquired under the common rule; that is a downstream
effect of discovery, not a special V2 selector. Keep shared budgets/policies identical
where possible and report incremental RAG resolution cost/coverage limits explicitly.
No V2-only enriched descriptions or privileged profile filling in the selection prompt.

**V3 stays separate:** its mechanism evaluates a generated itinerary's temporal,
route, budget and other feasibility violations, performs targeted repair and revalidates.
Candidate/selector validity is pre-generation and cannot certify the resulting schedule.
A single bounded invalid-JSON/ID retry is not V3 itinerary repair. V0 remains unchanged.

If approved later, update `PROJECT.md`, `docs/v1_design.md`, `docs/v1_milestone.md`,
the Phase 6 proposal and V1/V2 archive indexes with dated new events. Preserve the
old freeze/events and Phase 1-5 TripWorld records. This task does not change those
historical records or mark V1 reopened.

## 17. File impact and migration boundaries

| Current / proposed path | Likely treatment if approved |
| --- | --- |
| `policies/poi_selection.py` | Extract eligibility/date-risk checks; retire weighted greedy selection from active pipeline; preserve legacy behavior in history |
| `policies/poi_capacity.py` | Reuse formulas initially; document new stage interpretation and operational bounds |
| `policies/poi_funnel.py` | Reuse intent construction/named-place reconciliation; replace rank-selected canonical merge/admission where necessary |
| `evidence/selection_models.py`, `evidence/models.py` | Separate Google discovery hits from source-neutral canonical candidate; remove mandatory fake rank requirement for RAG-only candidates via new candidate contract/projection |
| `policies/review_sensitivity.py` | Retire from active path; no LLM counterfactual score loop |
| `policies/experience_selection.py` | Retain typed experience-need extraction where useful; numeric E scoring becomes legacy/optional diagnostic, not active selection |
| `policies/experience_profile.py`, `evidence/experience_models.py` | Reuse review preprocessing/validation and supported dimensions unchanged |
| `services/review_selection.py` | Separate reusable cached Review/Profile acquisition from old sensitivity/selection orchestration |
| `services/evidence_acquisition.py` | Preserve provider/cache/normalization; refactor funnel stages and public acquisition seam; no repeated validation-then-Details |
| New `schemas/poi_selector.py`, `policies/poi_eligibility.py`, `policies/selector_validation.py` | Stage/context/decision contracts, hard gate, ID/evidence/count validation and mechanical fallback |
| New `services/poi_selection.py`, `services/selector_prompts.py` | Shared two-stage orchestration and versioned prompts; names subject to repository naming review |
| `llm/azure_foundry/{client,dto,mapping}.py` | Add strict selector DTO bindings, task-scoped caps/effort/deadlines, usage observability; existing task defaults preserved |
| `versions/v1/{graph,state,runner}.py` | Approved reopened V1 uses shared selector and new result projection; no obsolete Score assumptions in trace/output |
| Future `versions/v2/` + `scripts/run_v2.py` | Same selector dependency/config, only added discovery/resolution; not created now |
| `versions/v1/{prompts,official_web,official_planner}.py` | Preserve itinerary/official prompt semantics; update typed projections if old funnel/result signatures require it; no selector rationale as authoritative evidence |
| `runtime/{budget_limits,budget,config_models,config_loader}.py`, `config/runtime.yaml` | Explicit selector calls/tokens/deadline/retry policy and review allocation; same V1/V2 values |
| `observability/run_trace.py` and adapter tracing | Reuse best-effort tracing; add safe selector usage/result metadata and optional normalized capture |
| V0 graph/prompts/runner, Google/Weather/Routes clients, official grounding, TripWorld Phase 1-5 | Reuse unchanged except a concrete separately identified compatibility bug |
| Tests for funnel/reviews/graphs/Foundry/config | Replace active score assertions with new contracts; keep explicit legacy tests if retained |

Implementation order after approval: extract/test gates and source-neutral contracts;
build fake-client selector/validator/fallback; refactor review acquisition; integrate
revised V1; prove V0 unaffected and bound every new call; validate/re-freeze V1; only
then adapt Phase 6 discovery/merge. Do not attempt V1 selector redesign and V2 RAG
integration in one unreviewable change. No model training, new database layer, ANN,
frontend version switch or V3 mechanism belongs in this refactor.

## 18. Proposed tests and acceptance evidence

Normal automated tests use fake model/provider outputs; no live paid calls:

- Gate: permanent closure, definite opening-date incompatibility, invalid coordinates,
  explicit exclusions, ambiguous/unresolved required identity, hard unknowns and capacities.
- Stage A: required preservation, exact shortlist bounds, disjoint reserves, validated
  review nominations, cap enforcement and budgeted failed-Details replacement.
- Stage B: invented/duplicate/excluded IDs rejected; referenced requirements/evidence
  must exist; required feasible IDs retained; partial/empty pools handled by policy.
- Reviews: no experience needs means zero review calls; only capped eligible contenders;
  validated Profile with confidence/refs, missing evidence remains unknown; no raw
  reviews or TripWorld priors enter final selection or recreate E evidence.
- Failures: malformed output, refusal, truncation, timeout and provider outage; at most
  one shared repair retry; deterministic fallback revalidated and explicitly traced;
  no silently repaired fake IDs or ignored must-visits.
- Cache/budget: identical current Details/Profile reused, failures charged, hits free,
  no hidden retries, selector counters obey limits, trace failure does not alter results.
- Comparability: same canonical set/requirements/evidence with permuted discovery order
  produces identical messages/schema/config/hash; change sidecar sources/ranks only and
  model input stays identical. Mixed-source V2 and Google-only V1 share the service.
- Factual authority: changed current Google facts trigger re-gating; model explanations
  cannot override them; prior categories do not create accessibility/quietness facts.
- Projections: selected IDs map to aligned current PlaceEvidence; Official Web/Routes/
  itinerary receive no raw reviews, selection scores or invented provider ranks.
- Stability: deterministic preparation/fallback unit tests; separately authorized
  repeated fresh-model development runs assess membership variation as described above.
- Regression: V0 semantics/date contract unchanged; revised V1 independently runnable;
  future V2 imports same selector; V3 remains unimplemented/post-generation in scope.

A passing fake test suite cannot establish semantic quality or real latency. Re-freeze
requires explicit user review of measured behavior; thresholds for acceptable fallback
frequency, selected-set stability and latency must be agreed before that live check.

## 19. Risks and decisions for approval

**Historical decision list:** Architecture B now has approval in principle only. The
current approval boundary and remaining decisions are in section 20.15.

1. Approve Architecture B and intentional V1 reopen, rather than the old Phase 6 Q_rel
   adaptation. This is a larger baseline change, not a transparent bug fix.
2. Accept two stages and retire counterfactual E sensitivity; approve the capped
   nomination/allocation replacement and reserve policy.
3. Approve source-blind factual selector projection and shared configuration, with
   provenance/semantic priors confined to the sidecar by default.
4. Set selector runtime token/time/call limits and operational acceptance thresholds;
   verify actual Foundry model/version/rates before interpreting the cost table as billing.
5. Confirm required-conflict/unknown-hard-constraint behavior: no silent waiver, explicit
   blocked/clarification status when requirements cannot be supported.

Open risks include Stage A recall loss, admission bias, insufficient category semantics
without historical descriptions, model world-knowledge intrusion, Profile evidence
sparsity, stochastic selection, deployment drift and new sequential latency. Typed
guards control mechanical validity; they cannot guarantee preference-optimal choices.
The recommendation remains B because it cleanly separates those responsibilities
without inventing cross-provider Q scales, provided the common revised V1 is validated
and explicitly re-frozen before V2 integration proceeds.

## 20. Open-ended Semantic Requirement Contract — proposed revision

### 20.1 Decision and supersession map

Retain Architecture B. Its input must preserve open user meanings rather than require
an enum addition for each new preference. The single Requirement LLM interprets user
language once, before discovery. Application code validates structure, provenance,
links and registered operational meanings. Neither the gate nor the selector is an
additional natural-language requirements parser.

| Earlier assumption | Revised proposal |
| --- | --- |
| Section 5: interests plus six experience preferences describe selector needs | Operational requirements plus bounded, open SemanticRequirements; evidence requests are linked projections |
| PoiInterest is a universal semantic abstraction | Its surface is already free text, but its role is discovery; replace its independent importance/identity in the revised path with linked discovery intents |
| ExperiencePreferenceIntent represents user experience language generally | Existing fixed vocabulary is evidence-specific compatibility vocabulary, not universal user semantics |
| Sections 3/8: interest buckets implicitly represent all goals | Only discovery-purpose requirements create admission buckets; set diversity/style goals remain selector inputs without artificial search buckets |
| Section 7: exact final count | Stage B may select within application bounds to respect fewer/deeper experiences; Stage A enrichment capacity stays bounded |
| Section 9: review nominations cite independent preference IDs | Cite canonical requirement IDs plus supported evidence dimensions; nominations cannot grant evidence authority |
| Section 16/17: implement selector first with existing requirements | Explicit reopen, revised interpreter contract, shared selector, offline checks, bounded live development checks, STOP, explicit re-freeze, then future V2 |
| Sections 11/12: old measured prompt sizes approximate the proposed inputs | Preserve measurements as historical; re-size revised semantic payload before implementation acceptance |

This is an architectural proposal, not implemented behavior, a benchmark, or a new
version freeze. No model/provider call is needed for this revision.

### 20.2 Exact current requirement audit

Paths below are relative to the repository root. The audit reads current executable
files; it does not treat the earlier proposal as implemented behavior.

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

Current prompt and transport path:

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

Source validation is real but limited:

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

Downstream audit:

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

Audit conclusions A-E: base string lists and PoiInterest.surface are already open;
experience preference values and acquisition vocabularies are fixed. Preserve
destination/date/count/Money, named identity intention, routing mode and information
facets/scopes for their real consumers. Do not elevate SearchIntentKind weights or
the six experience values into the universal language of user meaning. Money and
traveler_count are useful typed inputs even where no current hard verifier exists.
There is no current generic numeric-limit schema to claim as already supported.

### 20.3 Proposed canonical contract and field meanings

Use a new versioned `InterpretedTripRequirements` envelope for the revised V1 and
future V2. Preserve the shared TravelRequirements class for V0. In the revised
interpreter, extract operational scalars and canonical intent records once; generate
any legacy base string-list view by projection rather than independently asking the
LLM for duplicate semantic interpretations.

The accepted envelope has operational trip fields, named-place requirements,
information requests, transport requirements, `semantic_requirements`, linked
evidence/discovery intents, source references and extraction issues. All are bounded.
The source request is retained outside the selector for provenance. This is a new
semantic contract version, not a promise of byte-compatible old V1 model outputs.

Proposed `SemanticRequirement`:

| Field | Meaning and ownership |
| --- | --- |
| requirement_id | Application-assigned opaque request-local ID after validation; shared reference across all projections |
| normalized_text | Open-ended English text preserving negation, conditions, comparisons, traveler attribution and tradeoffs; no predefined semantic taxonomy |
| kind | preference / constraint / goal. Describes user intent, not operational capability. A constraint describes a boundary; a goal an outcome; preference a comparative desire |
| polarity | favor / avoid. Direction toward the described subject; hard is represented separately. No redundant `require` polarity |
| strength | low / medium / high / hard. Semantic commitment, not numeric reward or evidence certainty. Default medium when unstated; hard only for a genuinely non-negotiable source-supported meaning |
| scope | individual_poi / selected_poi_set / whole_trip / itinerary_style / transport. One primary scope; nuanced relationships remain in text. Ambiguity is an extraction issue rather than an invented scope |
| subject_refs | party by default, or bounded traveler/group references explicitly grounded in the request; no inferred age, disability, gender or medical condition |
| source_refs | One to three exact source spans in the provenance ledger; obligatory, including enough context for negation/condition/subject |

Avoid redundant combinations such as constraint+require+hard where three fields
repeat one decision. `kind` does not grant enforcement; even hard+constraint can be
unsupported. Use `polarity=avoid` with a normalized phrase such as "Gimmicky places
whose appeal is mainly staged photo opportunities", rather than double-negating
"Avoid non-gimmicky places". The prose and structural direction must agree by
instruction and testing; code cannot generally prove that agreement.

Example accepted semantic record (illustrative, not executable):

```json
{
  "requirement_id": "req_003",
  "normalized_text": "Prefer distinctive places with a local feel over heavily tourist-oriented attractions",
  "kind": "preference",
  "polarity": "favor",
  "strength": "high",
  "scope": "selected_poi_set",
  "subject_refs": ["party"],
  "source_refs": ["span_004"]
}
```

Conditional tradeoffs should normally remain one item: "Travel farther only when a
place offers a distinctive experience" must not become two independent rewards for
distance and novelty. Distinct mother/father preferences remain separate records
with separate subject_refs. A small subject ledger (<=8, label <=80 characters,
source-backed) enables this without creating a traveler-personality taxonomy.

Operational records use the same ID namespace. A named place has source-backed
surface plus REQUIRED/OPTIONAL/EXCLUDED intention; Google ID comes only from later
resolution. This adds EXCLUDED in the new contract, not to the frozen V0 path.
Requested information remains a separate question with optional link to the relevant
requirement; asking admission price does not imply a hard budget or a required visit.
An explicit supported transport mode remains a typed routing instruction. Richer
conditional transport wishes remain semantic unless a registered policy supports them.

### 20.4 Bounds, provenance, IDs and consolidation

Proposed initial limits, identical for revised V1/V2 and checked in application code:

| Item | Bound / behavior |
| --- | --- |
| Semantic requirements | <=24; normalized_text 1..320 Unicode code points each; <=6,000 total normalized-text code points |
| Sources per semantic item | 1..3 exact contiguous spans; each 1..320 code points; <=12,000 total copied code points across semantic source references |
| Operational arrays | Retain <=24 named places and <=32 information requests; one supported transport mode; no generic arbitrary numeric-key dictionary |
| Linked evidence requests | <=16 distinct (requirement_id, dimension) pairs; at most five dimensions per requirement; no independent strength |
| Discovery intents | <=8; query_text 1..200 code points, <=1,200 total; 1..4 linked requirement IDs; no provider/version fields |
| Subject ledger | <=8 explicit subjects/groups, plus party; each requirement refers to <=8 subjects |
| Extraction issues | <=8, each reason code plus <=160-character explanation and <=3 source refs; overflow flag must remain visible |
| Revised interpreter raw input | Proposed 24,000 code-point and 8,000 input-token limits, both enforced; exceeds => request simplification, never silent raw-request truncation; V0 unchanged |
| Model-visible semantic sources | Only IDs by default; quoted original spans stay in the ledger, avoiding repeated large prompts |

Counts/character limits alone do not bound multilingual tokens. Validate complete
serialized input/schema against stage token limits too. These values are proposed
engineering budgets, not experimentally established optimal settings.

The Requirement LLM returns exact source_text plus a bounded occurrence index for
repeated identical text, not trusted character offsets or provenance hashes. The
application locates that exact occurrence in the immutable original request, checks
nonempty/length/bounds, and stores start/end as half-open Unicode code-point offsets,
quote, input hash and extraction/prompt/schema version. Recheck request[start:end]
equals quote. No Unicode normalization of quotes before this integrity check.
Nested quote matches and overlapping spans are allowed for compound requirements.
Names may use existing conservative surface normalization for identity comparison;
that is not permission to infer meanings from raw words.

The model uses temporary unique keys to link its output. After source validation,
application sorts records by first source offset, record family and stable full
serialized content to assign req_001 etc.; remap every dependent reference. This is
deterministic for an identical validated extraction. Do not include GOOGLE/RAG/V1/V2,
candidate IDs or discovery order in requirement identity. Same request, reference
date, interpreter/config and a replayed extraction give the same contract in both
versions. **Separate fresh LLM extractions can differ**: shared configuration cannot
guarantee identical semantics. Use a common interpreted snapshot for paired development
checks; do not introduce a persistent cache or claim model determinism.

Consolidation rules:

1. In the single interpretation call, merge genuinely synonymous statements only
   when subject, polarity, strength, scope and conditions are compatible. Preserve
   all supporting spans within bounds. "Not tourist traps" and "locals go there"
   are not necessarily equivalent; keeping them separate is valid.
2. Application collapses only exact duplicate normalized records with matching
   structural fields (union sources), never semantic similarity via keywords or
   embeddings. Repetition does not multiply strength. It must not merge differing
   travelers, conditions or contrary instructions. Conflicts remain visible issues.
3. Canonical meaning appears once; operational/evidence/discovery projections link
   to that record rather than create independent preference instances. Model-visible
   requirements have no additive rewards and no multiplicity weight.
4. The model consolidates to the limits in its original response. If preserving the
   request needs more items/text/sources, set overflow/clarification issue. Code must
   reject an oversized/ambiguous accepted contract, not truncate or summarize it.
   No extra semantic-compaction LLM is added. Never silently drop a hard/negative item.
5. Prompt compaction removes duplicate JSON material, raw spans, optional profile
   prose and optional geographic neighbors in that order. Keep all canonical meanings,
   operational requirements, strengths, unknown states and gate facts. If the minimum
   payload still does not fit, return an explicit size/clarification result, not a
   meaning-dropping fallback. Count limits are not permission to lose user intent.

An exact source quote is necessary but not sufficient to prove faithful normalization
or complete extraction. Strict DTOs, counterexample fixtures and later small live
development checks mitigate this; deterministic code cannot certify arbitrary meaning.

### 20.5 One meaning, several operational projections

| User meaning | Canonical owner | Linked projections; double-counting rule |
| --- | --- | --- |
| Definitely visit the Opera House | Named-place REQUIRED record | Identity search -> canonical required ID. No separate generic "Opera House preference" reward; canonical name requirement appears once |
| Exclude a named casino | Named-place EXCLUDED record | Resolve identity, exclude canonical ID; do not rely on arbitrary displayed-name substrings |
| Prefer less walking | One SemanticRequirement | Optional evidence request for walking_intensity references the same ID; no second preference weight, no invented radius |
| No casinos (category) | Open semantic constraint | Not a named place; no generic ban parser. A future approved typed category-exclusion binding may operationalize it, but current primary-type evidence/ontology does not prove all non-casino candidates compliant |
| Prefer architecture | One SemanticRequirement | A discovery intent can reference it; association is possible relevance, not verified architectural quality |
| Use public transport | Typed transport requirement | Routes mode consumes it; selector sees one operational record. A distinct wish such as scenic journeys may be its own linked semantic item |
| Rest somewhere other than a cafe | One conditional semantic goal, or linked distinct requirements if needed | Preserve the exclusion and rest objective together; no category heuristic makes a park a verified rest opportunity |

Base required_activities/excluded_activities/preferences can be generated as a
compatibility view for downstream generation, but revised selection reads only the
canonical ledger. Each projected string retains an internal originating requirement
ID; do not feed the projection and canonical items as independent priorities.
Unmapped legacy data is not promoted by a string parser. For old replay fixtures,
retain the old contract or require an explicit versioned adapter fixture.

Multiple IDs can express distinct related needs, but a decision cites each at most
once; association count never acts as a relevance score. This prevents structural
double counting, not all possible psychological emphasis in an LLM. Prompt wording
must tell the selector that linked evidence and repeated sources add information,
not additional votes.

### 20.6 Strength versus application-owned operationalization

Use separate axes instead of one status enum that mixes capability, evidence and
outcome. Proposed application-owned `RequirementAssessment`:

```text
requirement_id
capability: registered_predicate | evidence_assessment | semantic_only | unsupported
predicate_id/version: nullable; registered application identifiers only
evaluation_scope: candidate ID | candidate set | trip
evidence_refs: immutable references
evidence_state: available | partial | missing | conflicting | not_acquired
check_result: pass | fail | unknown | not_applicable
disposition: enforce | advise | acquire_then_recheck | clarification_required
```

Only a registered predicate with sufficient applicable typed evidence can produce
pass/fail. The predicate's scope, date applicability, allowed evidence and missing-data
policy are versioned. A capability exists independently of whether the current
candidate has evidence. EVIDENCE_SUPPORTED is therefore not a synonym for VERIFIED.

The Requirement LLM can emit a typed operational binding from the small approved
registry, with source links; the application validates the binding and decides whether
the evidence satisfies that predicate. It cannot emit authoritative assessments or
register arbitrary expressions. Initial registry covers named canonical membership/
exclusion and existing supported operational facts. No universal expression evaluator,
natural-language predicate compiler, quietness test or generic category-certification
engine is proposed. Model interpretation of the original language remains fallible.

Examples:

- "Absolutely no stairs" can be hard, even though the registry has no complete
  step-free POI/entrance/path/transport verifier. Capability unsupported, result
  unknown, disposition clarification_required. A review saying accessible does not
  prove this requirement, even with medium confidence.
- "Prefer less walking" is soft. A walking_intensity Profile can support a limited
  experience assessment; geographic distances are facts but not actual total walking.
  Keep advice and evidence limits, not a deterministic pass.
- A confirmed excluded canonical ID has a membership predicate independent of
  crowd opinions. A required ID known permanently closed produces a conflict, not
  permission to waive either rule.
- Unknown business status is an operational risk under existing policy, not a
  fabricated closure. It also cannot prove a separate hard requirement of guaranteed
  operation on a specific date.

**Initial unresolved-HARD policy comparison and recommendation:**

| Policy | Usability | Reliability / implementation consequence |
| --- | --- | --- |
| A: block/clarify unverifiable hard requirements | More friction for absolute subjective language | Honors non-negotiability without having to guess which user values are serious |
| B: proceed with UNVERIFIED marker | Lowest friction | Can deliver an unacceptable plan despite explicit hard intent; a warning is not user permission to relax it |
| C: only safety/feasibility-critical hard items block | Attractive compromise | Needs a trustworthy criticality classification and acquisition rules absent from current contracts; subtle mobility or sensory needs can be misclassified |
| D: explicit user-authorized best effort for particular hard IDs | A plus a negotiated escape | Sound later interaction extension; requires carrying an actual user decision, not elapsed time or inferred consent |

**Recommend A initially, with D available only after explicit user clarification.**
For a truly hard requirement, final selection cannot be released as an acceptable
planning result unless applicable registered checks support it. Acquire already
authorized evidence if it can actually resolve the condition; otherwise return a
typed clarification result identifying the original requirement and verification gap.
Do not ask the selector to downgrade hard to high. A user may explicitly change it
to a best-effort preference; preserve the original and the subsequent authorization.
Do not add a speculative safety classifier to choose which hard wishes matter.

This is deliberately stricter than silently proceeding with warnings. High/medium/low
preferences proceed with missing evidence and explicit uncertainty. Exaggerated wording
does not automatically mean hard: interpretation is the Requirement LLM's semantic
task, with ambiguity surfaced for clarification rather than keyword strength rules.
If the user really means "only places locals go to", unsupported verification blocks
under this policy. This limitation should be explained in one concrete clarification.

Apply the release policy across scopes: calling a hard requirement whole_trip does
not waive it. Without an appropriate trip-level verifier, a hard total walking/strict
total budget/no-stairs guarantee cannot be certified in V1. A provisional internal
shortlist can support authorized acquisition, but it is not an accepted final result.
This does not implement V3: it explicitly stops where V1 lacks verification. Requested
information questions and ordinary point budgets are not automatically hard guarantees.
Current V1 exception-only handling needs a typed clarification outcome on reopen;
UI interaction is not assumed to exist already.

### 20.7 Exact authority boundaries

Hard Gate and application policies may:

- Resolve/reconcile supported identity outcomes, merge identical canonical IDs,
  reject excluded IDs and preserve feasible required IDs.
- Reject invalid coordinates, confirmed permanent closure and supported definite
  date incompatibility. Preserve unknown and temporary-status risks as such.
- Enforce counts, acquisition budgets, canonical links, registered typed predicates,
  evidence applicability and the unresolved-hard release policy.
- Report conflicts, unknowns and unsupported requirements. A gate result certifies
  only evaluated predicates on supplied evidence, not current-world completeness.

They may not interpret raw request words, normalized semantic prose or categories
into new hard rules. There is no "quiet -> library", "touristy -> famous-place ban",
"less walking -> 3 km" or "family friendly -> playground -> verified" conversion.
Literal span matching, ID lookup, exact duplicates and typed enum dispatch remain
valid structural operations; they are not semantic reinterpretation.

The selector may judge preference alignment, diversity, redundancy, stated traveler
tradeoffs and whether distinction justifies distance inside the admitted set. It may
use available name/type facts as weak context for semantic judgment, but not invent
venue properties. It cannot resolve identities, acquire evidence, enlarge budgets,
change gates, declare a hard requirement verified, certify current truth or validate
an itinerary. A plausible local-feel guess remains a guess, not a sourced assertion.

TripWorld retrieval enrichment is still an offline semantic prior. A library/quiet
association never creates ExperienceProfile.quiet or a factual gate input. No new
Profile field is proposed. No model-world-knowledge statement becomes official evidence.
Input and output evidence links constrain references, not entailment; rationales stay
untrusted and do not become itinerary factual material.

### 20.8 Revised SelectorContext and two-stage projections

```text
SelectorContext
  contract_version, evidence_policy_version
  trip: destination, dates, days, traveler_count, point budget when supplied
  operational_requirements: bounded canonical ID-linked records
  required_ids, excluded_ids
  semantic_requirements: all normalized records with IDs/structure/subjects
  subjects: bounded source-backed labels, no raw personal narrative
  assessments: application-owned operationalization/evidence/check summaries
  selection_min, selection_max, review_limit, reserve_limit

CandidateForSelection
  canonical current Google identity, name, primary type, coordinates
  deterministic geographic facts and operational risks
  stage-appropriate current rating and supported ExperienceProfile
  semantic_associations: <=8 distinct requirement IDs, basis=discovery_context
  evidence_refs, explicit availability states
```

Associations are source-neutral possible relevance hints, never assertions that a
requirement is met. Limit them deterministically by canonical requirement order;
retain full association provenance outside the model and disclose omitted count.
An associated candidate does not receive a second reward. All requirements remain
visible even if candidate associations are absent/truncated. Do not add associations
for set/style goals merely to manufacture coverage. Operational hard checks are
separate and cannot be hidden by an association limit.

Stage A sees **all** canonical semantic requirements, including set/trip/style
preferences. It receives the same texts/strengths/subjects as Stage B. Requirements
outside POI selection are marked advisory/outside-selection scope, not omitted or
claimed satisfied. Stage A has cheap name/type/coordinates/status evidence; rating
and Profile are not_acquired for every source. It can shortlist potential matches
and nominate relevant supported review dimensions, with explicit uncertainty.

Stage B sees the same requirements plus current Details and selectively acquired,
validated Profile. Evidence states distinguish not_acquired, unavailable, partial,
conflicting and observed signals. Missing crowding is not high crowding; no reviews
is not bad experience; reviewed candidates are not automatically preferable. A
positive subjective review signal is not hard verification. Current Google rating
does not prove local feel, architecture, quietness or family suitability.

The input separates USER_REQUIREMENTS, OBSERVED_EVIDENCE, DERIVED_GEOGRAPHY and
POSSIBLE_ASSOCIATIONS. Profile is explicitly attributed to review evidence with its
confidence and supported dimension. No raw request, raw reviews, provider ranks,
TripWorld enrichment prose or V1/V2 label enters the selector prompt.

The outputs from section 6 retain ID/record validation. Change review nominations
to `{place_id, requirement_id, dimension}`. Add a bounded requirement assessment list
(<=24 entries) with `requirement_id`, `consideration=addressed|tradeoff|insufficient_evidence|outside_selection`,
optional selected IDs (<=selection_max) and <=120-character explanation. These are
**model judgments**, not pass/fail/verified fields. They make set-level considerations
inspectable without turning them into an additive score or authoritative evidence.
Application-owned assessments and selection status remain outside model control.
Output size budgets must include these additions; no hidden chain-of-thought required.

### 20.9 Flexible final count and failure behavior

The user's fewer/deeper example exposes a flaw in the previous exact-count rule.
Keep capacity formulas as upper bounds initially, not obligatory numbers to fill.
Stage A still targets min(R_pool, admitted count) to maintain options within Details
budgets; this is not a requirement to schedule all contenders.

For Stage B, with nonempty eligible E and feasible required M:

```text
selection_min = max(1, |M|)
selection_max = min(k_final, |E|)
```

Reject min>max, missing/infeasible required IDs and an empty pool. Select useful
coverage for the requested trip, avoiding redundant filler; fewer selections must
be explained against the stated goals, not an arbitrary invented day/pace formula.
This flexibility applies uniformly to both versions, without keyword detection of
"fewer". The model can still choose poorly; counts validate bounds, not quality.
The result remains a candidate set, not a guaranteed daily schedule.

There is no current typed user POI-count limit. If one is implemented later, it must
be a separately registered typed numeric constraint with an explicit unit/scope and
source evidence. Do not assume "not three similar museums" means max_POIs=2 or ban
all museums. That is a semantic redundancy preference unless the source states a
literal supported numeric rule.

The one shared selector repair retry and provider/call caps remain. Deterministic
fallback uses canonical required-first/discovery buckets and must pass the same
mechanical validator and unresolved-hard policy. Its count may use the documented
upper bound as a reproducible degraded default, but it cannot claim to have honored
open preferences or fewer/deeper intent. Return `degraded_selection` with semantic
alignment unevaluated, distinct from an ordinary accepted model decision. If hard
items remain unknown, block; fallback cannot waive them. Prompts too large to preserve
all meanings produce an explicit size error, not this fallback.

### 20.10 Experience evidence after the redesign

The clean model is **fixed evidence-linked dimensions + open semantic requirements**.
ExperienceProfile's five dimensions and review validation remain unchanged. Remove
the six preference values as an independent selector input or general user ontology.
They can remain in legacy fixtures/adapters for historical QCGRE; new evidence requests
should use `ExperienceEvidenceRequest(requirement_id, dimension)` instead.

The same Requirement LLM may identify which supported evidence dimension could inform
a meaning. The application accepts only registered dimensions/references and caps;
this does not declare satisfaction. Stage A chooses eligible candidate nominations
within that request set, and the deterministic allocator controls actual calls.
No corresponding evidence request => no new review acquisition for that meaning.

"Less walking" can request walking_intensity; "avoid crowds" can request crowding.
"Quiet" must not automatically become crowding: a sparse venue may be noisy. "No
stairs" may motivate an accessibility evidence request but the broader dimension
cannot certify the narrower hard condition. Different traveler needs share acquisition
where useful but retain distinct canonical IDs; no global short/long conflict drop.
Local feel, romantic atmosphere and non-gimmicky distinction survive as semantics
even when no Profile dimension represents them. No new enums are needed to preserve
these wishes, and no automatic Web/review fan-out is authorized for them.

### 20.11 Future V2 retrieval relationship (design only)

Replace independent PoiInterest records in the revised path with bounded
`DiscoveryIntent` records produced **inside the same Requirement LLM call**:

```text
local_key -> application intent_id
requirement_refs: 1..4 canonical requirement references
purpose: activity_or_category | semantic_discovery
query_text: <=200 characters, meaning-preserving open text
```

An empty discovery list is valid. Named identities use the existing separate identity
resolution path. Query intents describe positive discovery opportunities, not all
user requirements. The interpreter is source-independent; V1/V2 receive the same
contract. Provider execution policy later renders these intents for Google search
and, in V2 only, TripWorld retrieval. No provider name, RAG-only preference or source
rank is embedded in the requirement identity.

Examples: unusual local cultural places -> semantic_discovery; architecture ->
activity_or_category; avoid three similar museums -> selector-only; farther if unique
-> preserve the tradeoff in selection, optionally discover distinctive places but
never enlarge geographic scope from that wording; no casinos -> an exclusion, not a
positive casino search. Negative retrieval wording is not an enforcement mechanism.
An interpreter can propose a positive opportunity from a compound goal only while
retaining the complete goal in the semantic ledger.

Application validates text bounds, links, purpose enum and budget; it does not scan
raw/normalized words to decide query relevance. Schedule within existing approved
search limits using canonical requirement strength tiers/source order and intent IDs;
dedupe only exact query duplicates with merged refs. Hard unsupported requirements
do not gain enforcement through a search query. Admission buckets follow canonical
linked requirements, not number of paraphrased queries. Generic fallback queries
remain application defaults with no fabricated user requirement IDs.

Future Phase 6 must separately approve geographic scope, query rendering, Top-K,
incremental resolution budgets and source merge. Nothing here implements them or
reopens accepted TripWorld Phases 1-5. Retrieval hits still need current Google
resolution before formal candidate admission. Google-first paths need no TripWorld
match. This revision adds no second parser, embedding model or database change.

### 20.12 Migration and version isolation

All file impacts below are **future, after explicit approval and V1 reopen**.

| File / area | Intended treatment |
| --- | --- |
| `schemas/request.py`, V0 prompts/graph/runner and FoundryTravelRequirementsDTO/binding | Keep V0 behavior, base Money/date schema and old DTO mapping unchanged; no new V0 input limits or semantics |
| New `schemas/interpreted_requirements.py` (proposed name) | Versioned operational/open semantic envelope, source ledger, linked discovery/evidence requests, subjects and issues |
| `schemas/trip_intent.py`, `schemas/named_place_intent.py` | Preserve historical contracts for replay if needed; new revised named intent supports EXCLUDED and canonical references; retire old PoiInterest/experience arrays as universal selector language |
| `policies/trip_intent.py`, `policies/named_place_intent.py` | Add version-specific span occurrence/offset validation, links, exact dedup and limits; preserve old validation for old records; do not extend generic-category/keyword rules into a new NLP engine |
| New requirement projection/operationalization policies | Application IDs, legacy base view, registered predicate/evidence assessments and explicit clarification outcomes; no free-text inference |
| `versions/v1/prompts.py` | Replace only reopened V1 extraction extension with single open-semantic/operational/linking instructions; update selector input and generator projection to consume the same normalized meanings |
| `llm/azure_foundry/{dto,mapping,client}.py` | New strict DTO/binding for revised envelope; temporary refs -> domain validation -> app IDs; transport cannot set enforcement result. Existing V0 and Profile bindings unchanged |
| `versions/v1/{state,graph,runner}.py` | Carry canonical envelope/assessment ledger; expose typed clarification/degraded outcomes; only one extraction call; source-independent selector wiring |
| `policies/poi_funnel.py`, `services/evidence_acquisition.py` | Use linked discovery intents; do not truncate semantic queries at 80 characters; resolve excluded names explicitly; stop interpreting base preference lists in revised path |
| `services/review_selection.py`, `policies/experience_selection.py` | Acquire reviews from linked dimension requests/nominations; remove active QCGRE E and counterfactual triggers. Keep old enum adapter only for explicit legacy replay |
| `evidence/experience_models.py`, Profile prompt/validation | Reuse five evidence dimensions and supported refs/confidence; no open user text becomes Profile fact |
| `policies/transport.py`, Google Routes integration | Reuse mode execution; consume linked typed projection without raw-text fallback. Complex unsupported wishes remain visible semantics |
| Official Web planning/projection | Preserve current facets/scopes/acquisition limits; accept linked requirement refs; do not treat arbitrary open semantics as supported Web tasks |
| Shared selector schemas/prompts/services/validator | Use revised sections 20.8-20.10; flexible count, requirement-level judgments, hard release policy; same V1/V2 prompt/config |
| V1 itinerary prompt/projection | Convey normalized requirements and application-owned uncertainty/clarification state. Avoid duplicate independent preference lists. Never pass selector rationales as verified evidence; preserve existing current-evidence authority |
| Runtime/observability | Bounds, schema/prompt/registry hashes, source IDs, clarification/degraded reason codes; raw requests/spans remain controlled trace payloads; no model-billed usage invention |
| Tests | Revise trip-intent/semantic-migration/named-extraction/Foundry/funnel/review/graph fixtures and add selector contract tests; retain V0 regression and date checks |

Backward compatibility is appropriate at external provider/operational evidence and
V0 boundaries. Keeping the same old independent preference arrays as competing
authorities would preserve a bad abstraction, so use a versioned new envelope.
Do not mutate the shared V0 base prompt to implement the new semantics. Current V1
generation may keep original request for context, but canonical interpreted requirements
are its normalized planning instructions; it must not override operational checks by
re-reading prose. General itinerary compliance remains outside the selector's guarantee.

Historical V1 remains frozen until explicitly reopened. The intended revised V1 differs
from historical V1 in requirement interpretation and selection; future comparisons must
identify that checkpoint honestly. Future V2 shares the revised interpreter/selector,
adding discovery only. No V2 execution path or Phase 6 code is created in this task.

### 20.13 Development testing and revised sizing plan

Fake-model tests assert supplied interpreted meanings survive mapping and projections;
they cannot prove a live model understands language. No paid calls are needed for
normal tests. Proposed examples:

| Source example | Expected contract and key assertions |
| --- | --- |
| I want historical places but not typical tourist traps. | Open historical-interest and avoid-tourist-trap meaning, or faithful compound item; exact sources; no historical/touristy enum addition and no famous-place gate |
| I prefer somewhere unusual but not gimmicky. | Preserve distinction plus negative qualification; no forced category and no independent positive gimmick query |
| I don't want three similar museums. | selected_poi_set redundancy meaning; not max_total_POIs=2, not blanket museum exclusion, normally no retrieval query |
| I am willing to travel farther for something unique. | Conditional tradeoff retained; same Stage A/B text; no radius/route limit mutation |
| My mother prefers quiet places, my father likes architecture. | Two subject-linked needs; no inferred crowding/medical fact; architecture may create a discovery intent, quiet may remain evidence-unsupported |
| Absolutely no stairs. | hard semantic constraint; absent registered applicable verifier => unknown and clarification; accessible review never passes it |
| I prefer less walking. | One canonical requirement, one linked walking_intensity request; no double importance and no 3 km gate |
| I want places locals actually visit. | Open local-use preference with source; no fabricated visitor-demographic evidence. Hard variant "only" is tested separately for clarification |
| I definitely want the Opera House. | Named REQUIRED, no duplicated semantic reward; unresolved/ambiguous identity blocks, canonical feasible ID retained |
| I do not want casinos. | Semantic category exclusion, not named-place identity. Hard interpretation cannot be verified by name/category guess; a soft interpretation stays advice. Test genuine ambiguity and no silent downgrade |

Also test:

- Invalid/missing/altered spans, repeated identical quotes with occurrence index,
  Unicode offsets, out-of-range references, fake model-supplied enforcement fields,
  unknown registry keys, invalid structural combinations and oversized arrays/text.
- A valid quote with an invented normalized preference demonstrates the validator's
  entailment limitation; do not write a test claiming code can detect all such errors.
- Same-subject exact duplicates merge sources without extra strength; similar but
  distinct local/tourist-trap statements remain separate. Different travelers and
  contradictory short/long needs must not collapse under the old enum dedup rule.
- All canonical meanings and strengths survive Stage A/B projections; only evidence
  availability changes. Unknown Profile is not negative; no reviews is not a penalty.
- Canonical required/excluded conflicts, hard unknown/fail, supported hard pass,
  all scopes, bounds, flexible final cardinality and explicit user-authorized relaxation.
- No call from the revised graph to legacy raw-text preference/transport helpers;
  fake wrappers raise if invoked. Code review checks no new keyword/regex semantic
  inference. Structural exact span/ID validation is intentionally still permitted.
- Requirement IDs and serialized selector inputs match on shared interpreted snapshots
  across V1/V2, reordered discovery and changed source sidecars; fresh model variability
  is not tested as impossible. Discovery multiplicity does not multiply preference.
- Evidence requests share acquisition but not traveler meanings; dimensions outside
  the fixed evidence contract rejected; no quiet Profile field added by open semantics.
- Selector drafts cannot self-verify requirements or override app assessments; invented
  IDs/refs rejected; rationale citations do not automatically become accepted facts.
- Overflow/compaction preserves hard/negative/conditional text or blocks explicitly;
  no second compaction/parser call; fallback is marked degraded and cannot waive hard
  conditions. Empty/one-candidate/count-conflict cases remain bounded.
- V0 prompts/DTO results and date behavior unchanged; V1 retains independent runner,
  tool limits/cache behavior, Official Web authority and downstream generation boundaries.

Before implementation acceptance, re-run offline prompt sizing for 0/typical/24 semantic
items, long names, multilingual source input, eight subjects, complete assessments,
both candidate stages and the new bounded outputs. Existing section 11 measurements
remain valid only for their earlier fixtures. The provisional 12k Stage A / 10k Stage B
input and 4,096 output token limits may cause explicit overflow; they are not proof
that maximum new payloads fit. Do not raise caps or drop meanings silently. Select
final caps and concise projections after this sizing work is separately authorized.

No new token/cost/latency measurement was performed in this documentation revision.
The new contract still uses one interpreter plus two selector calls, not a new parser.
Larger payloads and output judgments invalidate treating old example costs as current
forecasts. Preserve section 12's assumptions/history and measure revised payloads before
claiming costs. Later bounded live development checks inspect extraction fidelity,
clarification burden, semantic choice, latency and stability; they are not formal
thesis evaluations, and V1 re-freeze still requires an explicit decision.

### 20.14 Risks and open questions

1. Source integrity does not establish semantic faithfulness or completeness. Open
   text preserves expressiveness but can still normalize away an important condition.
2. Initial A hard policy can block common absolute language. This is an explicit
   reliability/usability tradeoff; an actual clarification/relaxation contract is
   preferable to introducing an untested safety classifier or silently weakening hard.
3. Cheap Stage A facts often cannot support local feel or unusual-but-not-gimmicky
   judgments. Open requirements remove a vocabulary bottleneck, not an evidence gap.
   Model priors and early recall loss remain limitations.
4. Flexible Stage B count can underfill useful trip options. Test representative short/
   long trips and explain chosen size; do not substitute arbitrary word-derived counts.
5. Admission and deterministic fallback cannot optimize arbitrary set semantics.
   Explicit degraded status is essential, and hard constraints still govern release.
6. More expressive subjects/conditions and linked arrays increase extraction error
   and token pressure. Start with bounded records, not a general logical language.
7. A casino-category ban is not solved by exact identity exclusion. Approving a future
   category predicate requires specifying provider type completeness and unknown rules,
   not adding a keyword. Likewise no-stairs needs more than the current Profile.
8. Application operationalization only validates registered semantics/evidence. It
   cannot prove the Requirement LLM chose the right predicate from the user's wording.
9. Clarification/degraded outcomes need explicit API/runner representation during
   reopen. No existing frontend dialogue or resumable clarification flow is assumed.
10. Earlier proposal evidence/cost assumptions remain historical. The contract limits,
    revised sizing, flexible cardinality and unresolved-hard policy need approval
    before executable changes; no live thresholds have been established here.

### 20.15 Final recommendation, approval boundary and document diff

Architecture B is still recommended. This revision improves its input boundary:
mechanical fields drive mechanical subsystems; open text preserves arbitrary meanings;
fixed evidence dimensions describe what can actually be observed; application-owned
assessments determine what can be enforced. The selector judges tradeoffs without
claiming unavailable evidence or enforcing a closed preference taxonomy.

Decisions requested for the revised design: the canonical linked requirement contract
and bounds; policy A with explicit user-authorized relaxation only; flexible Stage B
count; evidence-dimension-only review requests; same-call linked discovery plan; and
the versioned migration that leaves V0 untouched. Approval of this design alone does
not silently reopen V1: executable work still needs the explicit reopen instruction.

Required sequence: approve revised design -> explicit V1 reopen -> implement revised
interpreter -> shared selector -> offline checks -> separately bounded live development
validation -> STOP -> explicit user re-freeze decision -> future V2 RAG integration.

Documentation changes in this revision: updated status to in-principle approval;
added supersession notices without deleting sections 1-19; added this audited contract,
operationalization policy, revised stage projections/counts, evidence/discovery links,
migration/tests/risks; marked old prompt-size results as historical. The old Phase 6
proposal remains paused. No executable files, PROJECT.md, historical milestone/archive
files, data preparation, embedding artifacts or Git commits are changed by this task.
