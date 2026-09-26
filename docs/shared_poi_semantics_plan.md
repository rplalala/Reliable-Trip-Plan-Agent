# POI semantics, exploration and visit multiplicity implementation plan

Current status (2026-09-26): implemented with offline validation and bounded A/B live observations; C stopped at clarification and D remains unexecuted. See section 15.
The user separately approved implementation after this plan. Sections 1-11 preserve the accepted
design and planning chronology; section 12 records actual implementation and limitations.
Code baseline inspected: `feature/v3`, `7748f3e91500b8dd5a6db11bd04900145ab0b83b`.
Numeric defaults proposed below require implementation approval and offline sizing; they are
not measured optimums. Existing engineering checkpoints and historical live evidence remain intact.

## 1. Observed problem and ownership

The one-off London trace `cd6ffe0a-dcd8-44bd-8439-18e18a39c647` used London,
2026-10-01 through 2026-10-08, one traveler, AUD 3000 whole-trip and the exact preference:
`I like climbing mountain, I want to visit zoo, I also want to enjoy a rich trip.`
Artifacts: `logs/v3_london_preference_trace_20261001/`. That run used a separately hashed dirty
frontend tree; it is not represented solely by this plan's current baseline commit.

Google returned general attractions, but admission/Details ordering and final supply favored
linked preference buckets. All 16 supply positions were selected through the climbing/zoo buckets,
eight each; some also had default discovery provenance. Qualified comparison supply was 53.
Several restaurants carried preference discovery links, which are not semantic match evidence.
The output had 12 main visits, nine distinct identities and three repeated identities.
Repair was not called because there were no authorized targets with the three reviews disabled.
This did not literally reproduce an all-climbing/all-zoo itinerary, but localized lost exploration
opportunities and unnecessary repeats. It is development evidence, not a formal quality comparison.

Relevant current seams:

- `policies/acquisition_opportunities.py`: active user-intent buckets precede general filling.
- `services/candidate_details.py`: cached qualification plus a new-success target, without semantic
  primary-role qualification or continuation state owned by a semantic preparation cycle.
- `policies/planning_supply.py`: an active intent bucket can continue filling the entire supply.
- `schemas/interpreted_requirements.py`: sourced visit intentions support minimum counts and
  mandatory dates, not the full exact-count/distinct-date contract approved here.
- `versions/v3/wiring.py`: repetition scope is review-gated and currently requires multiple dates.
- `versions/v3/repair_targets.py`: repeat excess currently uses minimum visit counts.
- `schemas/product.py`: ProductPlanResult exposes minimum coverage, but not a general policy
  completion contract for unresolved multiplicity/qualification.

These are shared product/first-generation corrections plus V3 repair extensions. They are not
all V3-exclusive benefits. No global Semantic Evaluator or deterministic semantic classifier
will be introduced.

## 2. Accepted product semantics

LLMs interpret natural language, actual venue use, category relationships, themes and exceptions.
Programs enforce identity, provenance, typed authorization, deadlines, counts and evidence scope.
Neither name keywords nor a provider's broad type alone constitutes semantic adjudication.

- An unspecified-frequency one-off category goal normally needs one matching visit. Once met,
  reduce its selection priority and prefer suitable unrepresented experiences. This is not a
  blanket one-visit limit on a category or a rule that every soft preference has a mandatory quota.
- Explicit themed/exclusive trips, exact counts, minimum counts, dates and revisits take priority
  over ordinary diversification. Different zoos and repeat visits to one zoo are different goals.
- Ordinary restaurants, cafes, offices and professional-service venues are not main POIs. A
  source-grounded explicit request can authorize a bounded exception. A corporate public museum
  is a museum; a museum cafe remains a cafe when that is the actual visit object.
- For one requested Michelin dining experience, allow multiple matching candidate alternatives
  but at most one such main dining visit unless the request explicitly authorizes more. Do not
  schedule additional ordinary restaurants as main POIs after satisfying that exception.
  Explicit counts apply at the exception goal level, not independently to each candidate.
- There is no fixed last-day dining rule. Choose a suitable location/date/window and combine
  the exception with ordinary attractions as appropriate.
- Indoor climbing is not automatically mountain climbing; an aquarium is not automatically a
  zoo. Related alternatives may be suggested for soft preferences with an explicit substitution
  label. They do not prove the original goal satisfied. Unsupported hard requirements retain
  the existing clarification/unfulfilled boundary.
- Unrequested repeated main visits to the same canonical identity are product-policy violations,
  within one day or across dates. They trigger V3 repair by default, independently of optional
  quantity/overfull reviews. Transit endpoints, source references and Nearby listings are not
  separate main visits. Relabeling a visit cannot bypass counting.
- `total twice in different days` means exactly two visits on distinct dates. `at least twice`
  defines a lower bound and an explicit revisit need, not a permit for unlimited priority.
  Ordinary context/quality checks still apply; do not turn a lower bound into an invented maximum.
- Role-qualification UNKNOWN cannot count as established main coverage. A qualified attraction
  with unknown hours/prices/access facts is different: it remains selectable under existing
  evidence policies. UNKNOWN operating facts do not revoke a known semantic role.
- Non-main candidates remain in the identity ledger. They are not automatically exported as
  Nearby: existing Nearby discovery, allowed categories, locality and independent ledger apply.

## 3. Shared sourced requirement adaptation

Extend the existing one-pass interpreter draft/domain/mapping and strict prompt, rather than
adding another requirement interpretation call. Use source references and stable requirement IDs.
Add only the missing dimensions: goal versus continuing preference; ordinary versus explicitly
themed/exclusive scope; category versus named-place target; exact/minimum count; distinct-date
requirement; and explicit non-attraction experience exception. Reuse existing visit/time fields
instead of retaining two competing count authorities.

Named-place requirements bind through existing canonical resolution. Category goals bind through
candidate semantic assessments, not invented place IDs. General liking of food alone does not
authorize ordinary restaurants as primary activities. Michelin qualification cannot be inferred
from a restaurant name or model familiarity without supplied supporting evidence.

Historical absent fields remain unassessed. Do not migrate historical artifacts or interpret
absence as proof of no explicit revisit. New requests obtain assessed provenance; unresolved
related requirements block unsafe deletion, without freezing unrelated optional edits.
Version only changed prompt/wire/domain/projection contracts according to current conventions.

## 4. Shared candidate semantic assessment

Add a small shared service/DTO/prompt, provisionally:

- `schemas/poi_semantics.py`: bounded input/result contracts and requirement-match judgments.
- `services/poi_semantics.py`: batching, cache, strict validation and failure ownership.
- `services/poi_semantics_prompts.py`: instructions and few-shot examples.
- A dedicated adapter method in the structured LLM interface/Foundry implementation, with
  per-call output/timeout settings. Do not change shared client defaults or reuse Repair patch DTOs.

Assess all factual-gate-qualified candidates competing for main supply, not just candidates
programmatically labeled ambiguous. The factual gate retains canonical identity, explicit
exclusions and applicable confirmed conflicts; it does not decide venue semantics.

Each input row includes canonical ID, name, provider types, bounded available descriptions,
relevant existing evidence with reference IDs, linked sourced requirements and exception scope.
Use an allowlisted projection; no raw provider envelope, full route matrix or entire review corpus.
Discovery links are explicitly provenance, never evidence that a preference is satisfied.

Each output row identifies the actual visit object, primary-role decision (ordinary attraction,
explicit-exception-only, non-main, unresolved), compact reason and input evidence references.
Per-requirement judgments distinguish supported match, related alternative, mismatch and unresolved.
The LLM also supplies normalized experience categories for diversity; these are model judgments,
not official facts or an unrestricted scoring system. A place can satisfy multiple goals but counts
once toward identity capacity. Output exceptions must reference actual application-authorized
requirements; the model cannot mint an exception or claim verified opening/access facts.

Require exactly one result per submitted identity, valid reference membership and bounded fields.
Unknown/duplicate/missing IDs, invalid exception bindings, malformed output or failure to parse
are system contract failures, not user preference errors. Transport/provider/model timeout and
contract failures terminate planning without primary/Repair/Nearby continuation or automatic retry.
Cancellation propagates. A failed Repair-time assessment retains adopted history only as diagnostic
data; it does not silently return a successful fallback response.

Reuse a request-owned assessment cache keyed by canonical ID, relevant evidence fingerprint,
requirement/exception context and prompt/schema version. New evidence triggers reassessment only
if decision-relevant; round number and trace ID never invalidate it. Semantic batch attempts and
actual sends remain separate; success cache hits do not consume another send.

### Required few-shot cases

| Supplied context | Expected decision |
| --- | --- |
| Corporate museum with supplied exhibition description | Museum may be main; opening/access remain independently assessed |
| Museum cafe described as coffee and light meals | Non-main absent an explicit applicable exception |
| Mountain-named restaurant with restaurant facts | Not evidence of climbing; no lexical matching shortcut |
| Zoo query returned a restaurant | Retrieval origin alone does not establish zoo match |
| One Michelin meal requested, qualification supported | Eligible exception candidate, one scheduled exception visit |
| Michelin claim has no supporting supplied material | Do not declare the Michelin requirement satisfied |
| Zoo goal already met, suitable unrepresented history attraction available | Prefer new experience, without declaring all other zoos illegal |
| Same zoo requested exactly twice on different dates | Protect two distinct-date visits; third visit is unauthorized |
| Indoor climbing offered for mountain preference | Label related alternative; do not claim mountain climbing fulfilled |
| Museum role known but prices/hours missing | Role remains eligible; operating/price UNKNOWN remains visible |
| Venue role itself cannot be determined | Unresolved role; do not count it as proven minimum coverage |

Treat descriptions as untrusted data, not instructions. Include contradictory/insufficient input
examples and output ownership constraints. Do not use generated explanations as new evidence.

## 5. Exploration through admission, acquisition and supply

Preserve current capacities and a single canonical ledger. For an ordinary non-exclusive trip,
reserve `ceil(remaining_optional_capacity / 3)` exploration opportunities after explicit required
identities, bounded by available qualifying choices. Apply the same source-opportunity principle
to admission capacity, Details work allocation and final optional supply; do not simply reserve
slots at the final step after default candidates have already been lost.

Before assessment, lanes use request/default discovery provenance only to allocate processing
opportunity; they do not prove semantic match. After assessment, LLM categories/matches support
selection and diversify beyond already represented experiences. A mixed-source identity occupies
one position and cannot double-count both lane quotas. Prefer otherwise-unrepresented general
options when allocating exploration positions. Account for all explicit mandatory identities first;
report when they leave no discretionary capacity. A proven-empty lane can release capacity.

Do not copy the full raw preference into new discovery or run another interpretation. Reuse existing
Google/RAG capabilities and DiscoveryIntent. General discovery has a system-default purpose, not
a fabricated user demand. RAG default exploration may use a remaining existing query slot; it
does not silently increase query/embedding budgets. A clearly themed trip uses its interpreted
scope rather than a mandatory general-tourism quota.

Assessment follows normal Details and precedes final supply. Refactor Details preparation into
a resumable request-owned queue: retain cached results, attempted/failed IDs, cumulative sends,
original preparation deadline and success counts. `new_success_target` remains an initial
acquisition checkpoint, not proof of semantic adequacy. If semantic-qualified supply or exploration
opportunities remain insufficient, continue pending candidates within current admission/send/time
limits and the new semantic budget. Do not reset the two-pass queue or its deadline on continuation.

Stop when qualified supply is prepared, eligible queue exhausted, capacity/budget/deadline prevents
further useful work, or there is no display/selection opportunity. Do not acquire more merely to
consume unused budget. Unprocessed due to capacity is not unsuitable; model abstention is not a
confirmed exclusion. A factual restriction retains date/mode/target scope.

For a single approved non-main experience, propose at most two semantically qualified exception
alternatives in final supply (within K, not extra slots). This is a preparation reference, not a
guarantee of availability. Multiple explicit exception goals/counts share capacity; deduplicate
alternatives and report shortfall. Do not let exceptions monopolize discretionary supply.

## 6. First generation and shared output

Project assessments, explicit visit multiplicity, ordinary exploration opportunity and exception
limits into V1/V2/V3 primary input. Instruct the existing generator to satisfy sourced goals,
then prefer other suitable experiences and unused identities; provide few-shot counterexamples.
No requirement forces every selected place to match all preferences. Do not fill every supply slot.

An application-owned assessment ledger controls qualification and authorized exceptions, independent
of generated activity_kind. Reject semantic-authority claims outside that ledger. Compute goal
progress from scheduled identities and their scoped assessments; distinguish inferred match from
verified operations. No new model call is required merely to count visits or enforce exact dates.

V0 shares requirement/multiplicity instructions and observable output checks but remains tool-free.
It does not invoke the external-candidate assessment pipeline or fabricate canonical certainty.
Only confidently identifiable exact repeats are enforceable there; uncertain equivalence stays
unresolved. V1/V2 do not acquire V3 Repair. Their detectably noncompliant outputs must carry
incomplete status rather than falsely claim satisfaction.

## 7. V3 repair, rollback and failure

Reuse current validator, scopes, component dependencies, candidate authorization, material feedback
and latest-adopted state. Add same-day repetition scope and make unauthorized canonical repeats
an automatic product-policy target. Distinguish product-policy violation from a provider-confirmed
operating/route fact in finding reason/basis; do not relabel old review evidence retroactively.
Quantity and overfull review defaults remain unchanged. Retire the optional repetition gate for
this mandatory path without retaining a configuration switch that bypasses the invariant; document
the compatibility behavior of the old key explicitly.

Choose which occurrence to retain using the Repair model with requirements, actual windows and
routes; never always retain the first. Exact/date-bound authorized copies are protected. Repetition
can neither move to a different day nor change activity_kind to disappear from the count.

Repair reuses assessed candidates; new candidates require the same shared assessment before ADD/
REPLACE authorization. Requests beyond the semantic call/time budget stop new candidate preparation;
already assessed material may still support repair. No new per-round allowance is created.

Treat deduplication and directly necessary coverage compensation as one dependency group. Default
policy violations and resulting minimum-coverage needs precede optional review improvements.
The minimum-one rule and existing applicable conditional coverage floor remain distinct. Do not
silently replace the existing coverage floor with one simply to accept deletion.

Prefer one atomic combination in a round. If compensation spans rounds, maintain a bounded pending
branch for that dependency group, separate from the last publishable adopted state. Remaining targets
and IDs must be stable. Descendant edits depending on pending state belong to that group; do not allow
unrelated edits to depend on an uncommitted deletion. On completion recheck the combined group against
the current publishable state. On exhaustion discard that group and its dependent window/transfer
changes, retaining independently adopted improvements. Never restore the entire original draft just
because the final group failed. Pending/accepted/rejected status must be explicit in audit.

If repetition/coverage remains after rollback, expose the last adopted itinerary as incomplete with
the residual policy violations; it is not a compliant completed plan. Confirmed EXCLUDED/operating
removal retains its existing distinct safety and partial-compensation policy. Do not reintroduce a
prohibited place merely to restore coverage. New assessment model failure is terminal, as above,
and must not be swallowed by existing generic Repair fallback handlers.

Nearby executes once after final adopted primary only when normal allowed finalization is reached.
It never compensates main coverage or satisfies exception/revisit requirements. No Nearby after
terminal assessment failure, cancellation or exhausted request deadline.

## 8. Proposed configuration and execution accounting

Use `config/runtime.yaml` and its typed loader only. The following are proposed conservative
engineering starting values, not effective settings in this documentation-only change:

| New setting | Proposed initial value | Scope |
| --- | ---: | --- |
| Semantic assessment model calls | 6 | Whole request, initial and all Repair rounds share |
| Candidates per assessment batch | 32 | Distinct IDs; overflow splits within remaining call budget |
| Engineering input ceiling | 32,000 tokens | System + user + schema + framing for each assessment |
| Output ceiling | 8,192 tokens | Per assessment; no truncation recovery retry |
| Framing reserve | Reuse main-generation authoritative setting | Count once; no duplicate default |
| Assessment model timeout | 45 seconds | Dynamically shortened by remaining applicable deadlines |
| Cumulative assessment time | 120 seconds | Whole request; no additional request time granted |
| Ordinary exploration share | 1/3 | Optional opportunities at each bounded selection stage |
| Exception alternatives reference | 2 per requested exception visit | Within existing supply capacity |

One first batch of 32 and one later batch can assess the current 64 admitted identities; do not
assume all Details finish or all candidates qualify. Small continuation batches consume real calls.
Retain enough remaining time for the work that follows; do not dispatch a batch when the existing
phase's required downstream reserves cannot be honored. Repair assessment is inside its current
preparation/round/stage limits, not an extension of them. Initial work is inside the original request
deadline. Cache lookup does not spend another model call; actual failures are charged and terminal.
Pre-send capacity/deadline stops are preparation limits, not provider failures or user input errors.

Preserve existing primary/Repair 252k input, 16,384 output, K, admission, tool budgets, five Repair
rounds/calls, stage 360 seconds and explicit whole-request 600 seconds. New assessment calls are
separate from those five patch-generation calls and increase potential model usage; report both
categories and aggregate callback totals without double counting. Never reset tool failure history.

Validate positive limits, fractions in (0,1], batch/input/output relationships and required config
presence; zero is invalid for these mandatory-service settings, not silent bypass. No new CLI
override is proposed. Snapshot effective policy/version/hash once per request. Keep secrets in
existing environment settings. Update config/README only with implemented keys/values, not fake
active settings during this planning task.

## 9. Minimal implementation sequence and affected files

1. **Shared contracts and LLM service:** interpreted DTO/draft mapping, preference prompt, new
   `poi_semantics` DTO/service/prompt, `llm/client.py`, Foundry adapter, typed runtime config.
   Establish source ownership, few-shot, strict parsing, cache and terminal failures first.
2. **Supply pipeline:** `candidate_acquisition.py`, `candidate_details.py`,
   `planning_supply_pipeline.py`, `acquisition_opportunities.py`, `planning_supply.py`;
   request-owned continuation and lane accounting. Integrate V1/V2/V3 shared primary projection.
3. **Generation and completion contract:** version prompts, shared diagnostics/minimum coverage,
   itinerary output and request context propagation. Expose qualification and multiplicity outcomes;
   retain independent V0/V1/V2 paths. No hidden extra semantic generation pass.
4. **V3 integration:** `validation.py`, `repair_targets.py`, `wiring.py`, `repair_candidates.py`,
   `repair_models.py`, `repair_projection.py`, `repair_components.py`, `repair_acceptance.py`,
   `repair_service.py`. Default same-/cross-day dedup, exact repeat protection, assessed candidates,
   conditional-group pending/adopted separation and final comparisons.
5. **API/Product/UI:** `schemas/product.py`, existing planning response schemas, presentation
   service, streaming terminal mapping and React itinerary/status components. Display incomplete
   adopted results with residual issues; system assessment failures remain errors, never rewrite
   preference requests or a success-completion stream event. No second planner orchestration.
6. **Offline validation and documentation:** tests below, actual serializer sizing and targeted
   shared/version regression; document test chronology and migration. Stop before live.

This work changes existing first-generation semantic guidance intentionally; it does not change
travel provider limits, Weather, SQL, date windows, vector artifacts or model deployment.

## 10. Offline acceptance and sizing plan

- DTO/mapping: one-off versus continuing preference, category diversity versus same-place repeats,
  exact/minimum count, distinct dates, explicit theme, exception scope and historical missing fields.
- LLM boundary: correct/unknown/malformed batch, invented IDs/evidence/exception refs, duplicate or
  missing rows, timeout/cancellation, terminal failure and zero downstream work after failure.
- Few-shot fixtures: corporate museum, museum cafe, Mountain restaurant, zoo-query restaurant,
  unverified Michelin, indoor-climbing alternative, true themed trip and qualified-hour UNKNOWN.
- London artifact replay: default candidates survive admission, Details and supply opportunities;
  origin links do not establish match; one dining goal cannot fill the final main supply with meals.
  Do not require specific landmark IDs to always win or modify historical artifacts.
- Continuation: enough raw Details but insufficient semantic supply; pending queue resumes without
  resetting deadlines, sends, failures or cache; no extra work without purpose/input opportunity.
- Multiplicity: same-day/cross-day duplicates, exact two distinct days, two different zoos,
  minimum counts without invented maxima, protected named visits and no role-switch escape.
- Repair: successful grouped dedup+fill; pending fill over rounds; terminal failure; exhausted
  compensation discards only dependent edits; previous independent fixes remain adopted.
- Integration: real supply/service/graph with mocked external boundaries, V0 tool-free, V1 no RAG,
  V2 no Repair, V3 mandatory dedup without quantity review; latest adopted summary and one Nearby.
- Product: incomplete result never labeled policy-complete; model failure never attributed to
  preference input; cancellation and owned resource cleanup; no rejected proposal in final UI.
- Sizing: actual DTO/prompt/schema/serializer/offline tokenizer for 1/16/32 candidates, 64 split
  candidates, many sourced goals/exceptions, long evidence and Repair delta batches. Include
  primary and Repair projection regressions. Preserve mandatory facts/protection and identity
  scope; bounded omission is visible, not a fabricated decision. Oversize before dispatch yields
  a capacity outcome, not an invalid PlanningRequest. Do not expand ceilings to force a pass.
- Run targeted tests, affected shared/V0-V3 regressions, Ruff, diff whitespace checks and relevant
  frontend checks if production UI changes. Record initial failures, fixes and retests in order.

At the original planning checkpoint no implementation tests or sizing had run. See section 12
for subsequent authorized offline results.

## 11. Later capacity-calibration backlog

After implementation and offline acceptance, propose separately authorized, fixed-input development
smokes for ordinary mixed interests, explicit theme, dining exception, revisit and long trips.
Measure candidate opportunities per lane, semantic abstentions, prefilter losses, call sizes,
latency, actual usage, queue stops and downstream Repair effects. Change only justified limits;
record exact configuration/hash and avoid combining changed-model/changed-input runs as controlled
comparisons. Multiple smokes are a backlog item, not current execution authorization.

Do not raise budgets merely because a run does not use all available calls. No promise that every
trip becomes full or semantically ideal; bounded judgments and provider uncertainty remain visible.

## 12. Implementation checkpoint — 2026-09-26

Status: **implemented + offline-validated**, with no new provider or live calls. This is an
authorized post-closeout change. It does not rewrite the London trace or earlier V3 evidence.

### Actual interfaces and ownership

- The existing single interpreter now uses `preference_prompt_14`, `preference_draft_10` and
  `interpreted_requirements_4`. `preference_input_2` is unchanged. `ExperienceGoal` carries sourced
  frequency, category/named-place target, theme and primary-exception intent. Named visits retain
  `VisitRequirement` as the executable count/date authority, with exact count and distinct dates.
  Old version-3 contracts remain readable; default-repeat enforcement does not reinterpret their
  absent assessment as permission or as proof of no revisit request.
- `schemas/poi_semantics.py`, `services/poi_semantics.py` and its prompt implement
  `poi_semantics_1`. The Foundry client has a dedicated strict output method. Domain validation
  additionally enforces exact submitted identity membership, input evidence references, supported
  exception references and application canonical bindings for named exceptions. This is not a
  provider-fact validator. Strict wire shape alone does not guarantee correct semantic judgment.
- One request-owned service is reused by initial acquisition and every Repair round. Fingerprints
  include projected facts, requirements and application named bindings. Call attempts, cache hits,
  elapsed model time, effective policy/hash, per-call input hash, results and reported usage are
  exposed in `semantic_assessment` and trace records. Actual HTTP sends remain provider telemetry;
  a logical model invocation is not proof that HTTP was sent. Usage is already included in outer
  callbacks when present and must not be added twice.
- `candidate_acquisition`, `candidate_details`, `planning_supply_pipeline`,
  `acquisition_opportunities` and `planning_supply` preserve required identities and diversify
  ordinary optional opportunities. Before judgment, discovery provenance allocates processing;
  after judgment, supported matches/categories guide supply. Neither is a global score or a
  fixed itinerary ratio. The same bounded Details queue continues when qualification or available
  exploration material is insufficient. Final smaller tails are assessed before supply selection.
- New Repair candidates get provisional preparation associations and must pass the final semantic
  batch before model input authorization. A test exercises real discovery preparation, projection,
  patch acceptance and the shared semantic ledger; merely being present in the ledger is not enough.
- `visit_multiplicity`, `poi_semantic_output` and generation diagnostics expose counted policy
  issues and sourced goal progress. Same-day/cross-day unauthorized repeats automatically produce
  CONFIRMED **product-policy** targets, independently of optional repetition review. Explicit
  minimum counts are not invented maxima; exact/distinct-date requirements remain protected.
  Known role and excess dining-allowance violations have scoped `primary_policy` findings and
  replacement/deletion authorization; facts such as access, opening and prices stay separate.
- `repair_pending` stores only otherwise valid deduplication dependency groups waiting for
  compensation. They are unpublished. The next input contains both the adopted itinerary and the
  pending proposal, and application-generated `effective_patch` combines pending edits with the
  new parsed patch before all checks. The model's raw parsed patch remains separately auditable.
  If compensation fails, only that pending group is discarded; unrelated accepted changes survive.
  This is not an unsafe coverage waiver and does not resurrect EXCLUDED visits.
- `ProductPlanResult.policy_completion/policy_reasons` and the React itinerary view distinguish
  incomplete adopted output. Missing minimum coverage is included. `complete` has this limited
  product-policy scope, not whole-trip feasibility or proof that every soft preference is fulfilled.
  Unknown roles and historical multiplicity cannot be presented as verified. Semantic-model failure
  is terminal system failure; no primary/Repair/Nearby continuation or preference rewrite fallback.

Shared changes affect V0 guidance and V1/V2/V3 supply; they are not V3-exclusive benefits. V0 is
still tool-free, V1 does not initialize RAG, V2 does not execute Repair, and V3 still runs Nearby
once after its actual adopted primary. No product default version was changed.

### Effective limits and remaining limitations

`runtime.yaml` owns the mandatory `poi_semantics` block: 6 request-wide model invocations,
32 IDs/batch, 32,000 engineering input, 8,192 output, 45 seconds/call, 120 cumulative model seconds,
1/3 ordinary exploration opportunities and 2 alternatives per requested exception visit. Framing
uses existing main-generation 2,048. Missing/zero/inconsistent settings fail configuration
validation; existing historical request DTOs remain a separate compatibility concern.

No K, provider budget, primary/Repair 252k/16,384, five patch-call allowance, 360-second Repair or
explicit 600-second whole-request allowance was raised. Local pre-send capacity stops leave
unassessed identities unauthorized; actual semantic failures consume an attempt and terminate.
Cancellation propagates. New semantic calls add possible cost and latency within existing deadlines.

The available PlaceEvidence contract has name, primary type, address and source, but no provider
editorial/exhibition-description field. The semantic projection therefore does **not** fabricate
one or perform new web acquisition. Complex corporate-museum/cafe cases can remain unresolved;
few-shot instructions are not live accuracy evidence. Michelin status without supplied support
cannot be asserted. All semantic fixture judgments are explicitly synthetic. This step proves
mechanical boundaries and integration, not that the real model always classifies a venue correctly.

The London minimal fixture retains 50 identities from the three historical Google discovery
responses plus source hashes and original selection reasons. It proves exploration survives
16/32/48-slot admission prefixes. It is not a replay of the complete merged Google/RAG judgment
pipeline, and search-origin membership is not retroactively labeled semantic suitability. The
original run's 53 qualified comparison candidates and failed diversity outcome remain unchanged.

### Actual offline sizing

`python -m tools.diagnostics.poi_semantics_payload` uses the current system prompts, DTO schemas,
serializers and offline tokenizer. These are engineering counts, not real model usage.

| Sample | Engineering tokens | Ceiling/outcome |
| --- | ---: | --- |
| Semantic 1 / 16 / 32 brief candidates | 2,980 / 3,325 / 3,693 | Below 32,000 |
| Semantic 32 candidates with long address evidence | 163,725 | Pre-send overflow |
| Repair 32-identity initial / pending feedback | 17,007 / 17,237 | Below 252,000 |
| Repair long requirements/evidence, initial / pending | 97,575 / 97,805 | Below 252,000 |
| Pure retiming, initial / pending | 4,688 / 4,918 | Below 252,000 |
| Protected-text Repair pressure | 284,592 | `repair_input_overflow` |

64 semantic identities are exercised as two cached batches in tests. Pending sizing is a bounded
synthetic proposal, not a claim to exhaust the maximum multi-group size. Protected information is
not removed to force a pass. Component token counters are not a disjoint sum of the complete
payload (semantic/pending fields also contribute); use `total_tokens` as authoritative.

### Validation chronology and corrections

Counts below are individual runs, not disjoint totals. No full-repository or live regression ran.

1. Initial semantic-service suite: 14 passed. A first shared test command referenced a nonexistent
   test file and collected nothing; the corrected file is `test_quality_first.py`.
2. Early V3 integration run exposed missing dedicated semantic methods in offline fake models and
   was interrupted before completion. Synthetic fake methods were added, not production fallbacks.
3. Focused B target run: 11 passed / 1 failed; authorized exact revisit now correctly has no target.
   Supply/strict/Gate run: 51 passed / 8 failed; historical wire fixtures needed explicit synthetic
   new fields. B/validation/multiround: 119 passed / 4 failed; old repeat/default and README assertions
   were migrated. Original raw historical artifacts were not altered.
4. Wiring/service run: 44 passed / 1 failed; a purported legal-add fixture had unintentionally
   repeated another identity on all dates. After distinct fixture IDs, the isolated test passed.
   Pending suite initially passed 5 tests. Combined semantic/B/multiround/Gate run: 101 passed /
   1 failed; duplicate-failed-patch stop is now a valid unchanged-input outcome.
5. New independent-retime/pending test initially failed (6 passed / 1 failed). Repetition magnitude
   was missing from severity comparison. It was corrected; independent accepted retiming survives
   pending-group rollback. This was an implementation correction, not just a fixture migration.
6. Shared DTO/Foundry/Gate/V1 batch: 274 passed / 21 failed. Follow-up batches: 87 passed / 4 failed,
   then 73 passed / 2 failed. Fixes were explicit wire migrations, fake semantic ports and SDK
   MockTransport ownership/usage expectations (9 captured calls, 360 fixture tokens instead of
   7/280). These figures describe deterministic harness responses, not real provider usage.
7. Quality/service/harness/pending run: 80 passed / 3 failed. Fixed missing projection fixture field,
   V1 fake delegate and a direct-selection fixture that bypassed assessment. Next five-suite
   integration run passed 142. New same-queue tail test initially failed (125 passed / 1 failed)
   because it omitted the caller's final small-tail assessment; corrected to exercise that step.
8. Shared/API/V0/V2 batch: 141 passed / 2 failed; new strict visit distinct-date fields were made
   explicit in synthetic mapping fixtures. V3/Repair/locality batch: 172 passed / 2 failed;
   tests were updated for mandatory new-contract repeat scope and unassessed historical contracts.
   Locality/pending rerun passed 13.
9. Primary-role replacement integration initially had an invalid synthetic patch without times
   (27 passed / 1 failed). After supplying both timestamps, role replacement plus real semantic
   discovery integration passed 9. The new-discovery path also exposed and fixed premature rejection
   of identities awaiting their final semantic batch; they must qualify before authorization.
10. Broad affected regression: 638 passed / 3 failed. Remaining failures were the new result key,
    one review fake missing the semantic adapter and deterministic comparison including elapsed
    telemetry. Corrected V1 runner/supply suites passed 13; no production fallback was added.
11. Qualification/completion targeted regression passed 55. London replay initially used an
    invalid assumption that a raw-Google general ID could not acquire a later RAG association;
    the assertion now distinguishes historical selection reasons from raw lanes. Semantic suite
    then passed 21. Final changed V3/quality/API/output regression passed 269.
12. Frontend Vite first failed before tests with EPERM writing its temporary config. The authorized
    offline rerun passed both suites, 30 tests. TypeScript build-info writes hit the same local
    restriction; direct no-emit checks for app/node configurations passed. Changed-file ESLint
    passed. Ruff initially found formatting/import issues; scoped fixes and final check passed.

13. Mandatory-config validation, semantic service, quality supply and SDK harness rerun passed
    120 tests. Final Ruff and `git diff --check` passed. Direct TypeScript no-emit and changed-file
    ESLint checks passed; no production frontend fix was required after the initial test changes.

No branch switch, stage, commit, push or historical log modification occurred.
`AGENTS.md` and `docs/agents/` changed independently during the task and were preserved, not authored
as part of this feature. Later fixed-input live calibration remains separately authorized backlog.


## 13. Approved Spec review fixes (2026-09-26)

This checkpoint follows section 12 without rewriting its historical validation claims.
The user approved four Spec fixes with TDD, excluded the existing P3 pending-reason
heuristic, and prohibited live execution and commits.

### Implemented behavior

- Canonically assessed eligible visits count even when generation labels them
  `generic_activity`, `unknown`, or `free_time`. Transport endpoints remain excluded.
  Diagnostics, duplicate targets, repair acceptance and conditional coverage use the
  same visit rule; unlinked placeholders gain no identity from their title.
- Explicit category `exact` goals require equality; `minimum` goals retain no upper
  bound. Shortfalls and excesses produce incomplete output and scoped repair targets.
  Candidate additions must support the goal, and excess can decrease across rounds.
  Distinct identities and dates are counted separately: date shortfalls move existing
  visits without silently adding beyond an exact limit.
- Sourced named-place count/date obligations flow into shared completion diagnostics
  and Product presentation. A failed repair preserves incomplete output. A REQUIRED
  identity used only as a transport endpoint does not satisfy a visit obligation.
- Supply selection retains enough supported category identities for explicit
  exact/minimum goals before ordinary diversification, within the existing capacity.
  This does not guarantee feasibility or sufficient supply when capacity is exhausted.

### Offline validation and remaining limitation

Regression tests were added before the corresponding implementation changes. Initial
failures reproduced role-label evasion, exact-count overflow, multi-round excess,
named-count false completion and category supply loss. Additional failing boundary
cases covered supported additions, unassessed V0 output, distinct-date accounting,
adjacent movement, atomic compensation and REQUIRED transport-only presence.
The compensation implementation briefly failed on a missing helper import; that was
corrected before its successful rerun. The final two focused suites passed 49 tests.

The full backend suite completed with **1590 passed, 9 skipped, 1 failed**.
`test_later_rejected_deletion_does_not_pollute_earlier_adopted_loss` expects an overfull
review edit to be adopted before a repeat target. The current confirmed repeat target
makes that first edit unauthorized. Loading the saved pre-fix production modules in
an isolated process reproduced the same assertion failure, establishing that it
predates these four fixes. At that checkpoint the test was not changed or suppressed, and the full suite was
not green. The subsequently approved fixture correction is recorded below.

Scoped Ruff, formatting and Python compilation checks passed; `git diff --check`
passed. No Python static type checker is configured in the project. Both final review
axes found no remaining actionable issue in this repair delta. Existing V0/V1/V2/V3
entry points were preserved and included in the backend suite's offline coverage.

The existing P3 remains deferred. No live calls, staging, commits, branch switches,
historical log changes or thesis archive changes were performed.


### Approved target-priority fixture correction (2026-09-26)

Diagnosis reproduced the isolated failure and reduced it to a first-round deletion.
The current specification prioritizes CONFIRMED targets and forbids borrowing permissions
from deferred reviews. The old fixture proposed deleting an unrelated overfull visit
while a confirmed repeat remained, so rejection at operation authorization was correct.
Changing only the repeated identity to a distinct one in an in-memory control restored
that deletion's authorization. Existing locality/priority tests passed (6 tests).

With explicit approval, the second-day `g` visit became `f2` at canonical place `f` in
`test_later_rejected_deletion_does_not_pollute_earlier_adopted_loss`. Both proposed
deletions now address confirmed repeats. The first removes `f` while preserving coverage;
the later deletion of `a2` is rejected for uncompensated coverage loss. Every original
assertion remains intact, including adopted loss, final itinerary and coverage-regression
isolation. No production priority or acceptance logic changed.

The correction and locality suites passed 14 tests. Scoped Ruff and formatting passed.
The full offline backend suite then passed: **1591 passed, 9 skipped, 0 failed**.
This supersedes the earlier failing-suite status without removing that chronology.
The change is test-fixture and documentation only; V0-V3 production paths are unchanged.
No live execution, P3 work, staging or commits occurred.


## 14. Live acceptance attempt stopped at dependency boundary (2026-09-26)

After explicit authorization, A-C dates were corrected to 2026-10-05 through
2026-10-07 and case D was added for London, 2026-10-01 through 2026-10-08,
one traveler, AUD 3000, with mountain-climbing, zoo and rich-trip preferences.
Only A started. The requirement interpreter returned `requirement_provider_failed`
with `transport_failure` before POI semantics, supply, generation or Repair.
The process exited with code 1 after approximately 1.17 seconds. Resource cleanup
was recorded; retrieval initialization was not attempted. Underlying transport
cause and provider usage were not captured and remain unknown.

The approved stop condition was followed: no retries, and B/C/D remain unexecuted.
This is a failed live attempt, not live validation of the semantic extension or
of the original London issue. Existing offline validation is unchanged.
Inputs, policy/source fingerprints and the detailed report are in
`artifacts/poi_semantics_acceptance/20260925T154533Z/`; runtime traces are in
`logs/poi_semantics_acceptance/20260925T154533Z/A/`.
No production changes, P3 work, staging or commits were performed.


## 15. Network-enabled bounded acceptance (2026-09-26)

After separate network authorization, the batch used unchanged production code,
limits and fixed inputs. A completed in 152.31 seconds: eight distinct main POIs,
no canonical repeat, complete Product policy status, and one route-deficit Repair
round. Duplicate repair was not triggered. B completed in 118.44 seconds: exact
two different museums on different dates and minimum two different parks were
preserved and satisfied in diagnostics and Product. Supply retained three supported
museum alternatives and two park identities. A/B each used two semantic calls;
no count Repair or minimum-above-two branch was observed.

C received HTTP 200, then stopped after 10.03 seconds with
`clarification_required / unsupported_hard_requirements`, referring to `semantic_1`.
No itinerary was generated. The hard semantic gate is identifiable, but the full
failed interpretation was not persisted, so model classification root cause remains
unconfirmed. Per the stop rule, D was not run and C was not retried.

D is the user's eight-day London climbing-mountain/zoo/rich-trip scenario,
2026-10-01 through 2026-10-08, one traveler, AUD 3000. Its original problem is
not yet live-validated. No full four-case acceptance, formal benchmark or freeze
is claimed. P3 remains deferred; no production edits or commits were made.

Detailed inputs, fingerprints, checks and report:
`artifacts/poi_semantics_acceptance/20260925T155503Z/`.
Trace evidence: `logs/poi_semantics_acceptance/20260925T155503Z/{A,B,C}/`.
A's trace run summary is truncated by the configured cap; the separate result JSON
is complete. Missing usage and failed-draft evidence must not be invented.


## 16. Named-visit prompt routing and acceptance capture (2026-09-26)

Approved scope: strengthen representation precedence/examples, preserve the hard
semantic gate, add opt-in failure evidence to a thin one-case V3 acceptance entry,
and validate offline. No live run or automatic commit is authorized by this work.

Implemented `preference_prompt_15` examples route British Museum exact-two visits
on distinct dates into REQUIRED named identity plus VisitRequirement. A queue-free
guarantee remains independently hard. Category exact/minimum goals remain separate
and no named identities are invented. Only prompt identity changed; wire draft 10
and canonical contract 4 remain unchanged. Version identity is synchronized in the
adapter, acceptance fingerprint and existing alignment checks.

The new `tools/validation/poi_semantics_acceptance.py` reuses the existing V3 CLI,
Product projection and DevelopmentRequirementCapture. It captures normalized draft
and canonicalization outcome before a failed run can discard them, with shared call
IDs, prompt revision and fingerprints. The wrapper is opt-in, preserves application
exit status, uses no second interpretation call and never reruns an existing case
folder. Capture write failures and missing file traces are separately observable.
Production gate, candidate supply, Repair and Product logic are unchanged.

### Offline validation chronology

1. New SDK/MockTransport-to-V3 rejection capture test first failed because the tool
   did not exist; after implementation it passed and retained a hard duplicate plus
   the valid visit fields and rejection IDs from a single HTTP send.
2. Capture write-failure, disabled-capture and repeat-folder protection checks passed.
   Prompt-revision capture first failed with a missing key; recording the adapter's
   actual revision plus the synchronized prompt 15 identity fixed it. The combined
   tool/prompt-alignment run passed 30 tests.
3. The independent hard-condition regression initially used a list expectation for
   an in-memory tuple. Correcting that assertion preserved the existing gate behavior.
4. A new logging lifecycle test exposed a CLI handler bound to a closed case file;
   case-scoped cleanup fixed it. The combined requirement/semantic/Repair run passed
   66 tests. Secret-redaction coverage then passed with the tool suite.
5. Spec review found an unconditional file-tracer directory access. Two new tests
   reproduced failures for disabled and unavailable file trace. The wrapper now
   records their different statuses, preserves the business exit code and marks
   missing requested evidence incomplete. All 11 new tool/SDK tests passed.

Standards and final Spec review report no remaining findings in this change.
Ruff, Python compilation and the no-I/O CLI help check passed. The project does not
configure a Python static type checker. The full offline backend suite passed:
**1602 passed, 9 skipped, 0 failed**. Final scoped `git diff --check` passed.

These tests verify real service/SDK handling of controlled outputs and capture
behavior; they do not demonstrate that the real model follows the new prompt.
C needs a separately approved captured live rerun; D remains unexecuted. No P3,
production policy loosening, staging, commit or live execution occurred in this task.

## 17. Captured C live retest (2026-09-26)

Following separate approval, C ran once with the unchanged October 5-7 input and
budgets in the network-enabled environment. It exited 0 after 131.094 seconds.
The prompt-15 normalized draft and successful canonicalization share a call ID:
REQUIRED British Museum, executable minimum/exact two visits, distinct dates true,
and no duplicate hard semantic requirement. The separately sourced request for
other attractions remains medium-strength. Capture is complete with no errors;
raw provider payload capture remains disabled.

Final itinerary verification by canonical identity found British Museum exactly
twice on October 5 and 6. Eight main visits cover seven identities, with daily
counts 3/2/3. Product and diagnostics are complete with no policy issues. Final
validation has 13 PASS and 11 UNKNOWN findings, no confirmed violations, no
improvement targets and no Repair. POI semantics used 3/6 calls and 54.545/120
seconds; recorded tool counters remained within unchanged limits. Retrieval
resources were closed. UNKNOWN real-world facts remain unresolved.

This validates the observed successful path only; it does not establish prompt
reliability or reconstruct the earlier failed interpretation. The earlier C
failure is preserved in section 15. D remains unexecuted, and no count Repair path
was exercised. No production edits, P3 work, retries, staging or commits occurred.
Inputs, fingerprints, normalized captures, result, Product, trace, checks and report:
`artifacts/poi_semantics_acceptance/20260926T022409_C_retest/`.

## 18. Captured D acceptance blocked at preference input (2026-09-26)

After separate approval, the original eight-day London case ran once with unchanged
input and configured budgets: October 1-8, one traveler, AUD 3000, mountain climbing,
zoo and rich-trip preferences. The model returned HTTP 200, but the captured draft
classified `I also want to enjoy a rich trip` as `semantic_ambiguity`, with
`CLARIFICATION_REQUIRED` input and `CLEAR` safety. Canonicalization returned
`preference_input_blocked`; application exit 2 after 12.0 seconds. No retry occurred.

Mountain climbing was separately drafted as a continuing medium preference, and zoo
visiting as a one-off medium goal, both ordinary scope without primary exceptions.
The gate blocked before these could be used for planning. All recorded travel-tool
counters are zero; there is no itinerary, Product result, semantic assessment or
Repair. Resource release is recorded. This is not an observed Google dependency
failure, and it does not validate the original mountain/zoo/diversity improvements.

Normalized draft and canonicalization rejection capture is complete, with linked
call ID, prompt revision and fingerprints. Trace is available; raw provider payloads
remain disabled. Evidence and report: `artifacts/poi_semantics_acceptance/20260926_D_captured/`.
The next proposed step is a separately approved offline diagnosis of the soft
quality preference classification. No production edits, P3 work, staging, commits,
formal evaluation or freeze occurred. Historical checkpoints above remain unchanged.

## 19. Soft-quality input boundary correction (2026-09-26)

After offline diagnosis and explicit approval, prompt 16 adds an ordinary quality/style
boundary and the exact D positive example. Broad rich/varied/enjoyable/memorable wishes
remain sourced soft semantics without invented quotas, exclusive themes, luxury spending
or feasibility guarantees. D retains the ordinary continuing mountain preference and
one-off zoo goal alongside rich-trip style semantics. A mixed request with a missing
mandatory reference still clarifies that reference; soft wishes never override genuine
input, scope, hard-conflict or safety issues.

Prompt identity is synchronized in adapter and acceptance metadata. The shared V0-V3
prompt changes; gate, schemas, interpretation call count, budgets, supply, Repair and
independent entry points do not. No phrase allowlist or automatic issue removal was added.

### Validation and limitations

The new instruction-boundary test failed first against prompt 15, then passed after the
prompt change. Nine new tests use instruction checks and the real SDK over MockTransport
into interpret_preferences: historical D still blocks, synthetic D and two paraphrases
retain meaning and structured facts, mixed true ambiguity/contradiction/unsupported scope
still block, and fabricated provenance remains a contract error. The historical fixture
contains only the normalized draft/request, source fingerprint and provenance label;
it is not raw provider text and has not been rewritten as a successful response.

The focused new suite passed 9 tests. Final full backend suite: **1611 passed, 9 skipped,
0 failed**, in 72.30 seconds. Scoped Ruff and Python compilation passed. There is no
configured Python static type checker. Independent Standards and Spec reviews against
the pre-change working-copy snapshot reported zero findings. Existing unrelated working
changes were excluded from this review.

These checks establish prompt delivery and application handling of controlled model
outputs; they do not establish actual model compliance. The old captured draft must
continue to fail because a prompt-only correction cannot change frozen output. D remains
blocked in historical live evidence; another captured live run requires separate approval.
No live execution, P3 changes, staging, commit, formal evaluation or freeze occurred.

## 20. Prompt-16 D retest: input passed, semantic evidence failed (2026-09-26)

After separate approval, D ran once with its original input and unchanged budgets.
Prompt 16 produced VALID/CLEAR, retaining sourced continuing mountain preference,
one-off zoo goal and rich-trip soft meaning. Canonicalization passed, giving bounded
live evidence for the prior input correction. Complete normalized requirement capture
and trace are retained; no raw downstream semantic response was captured.

The run then exited 1 after 95.312 seconds with `SemanticAssessmentError` and CLI
message `Invalid match evidence references`. The first POI semantic call received
HTTP 200, used 31.677 seconds, and recorded 3531 input / 7780 output tokens. This is
an observed evidence-reference validation failure, not proof of a Google outage or
a known exact malformed reference. Ordinary details had 53 qualified candidates.
Recorded tool limits were respected and retrieval resources closed.

No itinerary, Product or Repair result was produced, so D's mountain substitution,
zoo fulfillment, richness and repeat behavior remain unvalidated. No retries,
production edits, P3 work, staging or commits occurred. The proposed next step is
offline diagnosis of this new reference-validation boundary using available evidence.
Report and evidence: `artifacts/poi_semantics_acceptance/20260926_D_prompt16_retest/`.

## 21. Semantic reference instructions and failure evidence (2026-09-26)

Following diagnosis and approval, `poi_semantics_prompt_2` explicitly requires exact
same-candidate source_ref values at assessment and match levels, with valid and invalid
examples. It forbids requirement IDs, other candidates, invented suffixes and explanations
as evidence references. Supported matches still need evidence; copying a valid reference
does not establish semantic support. Data contract poi_semantics_1 and requirement prompt
16 are unchanged. Semantic call records/snapshots include prompt revision/fingerprint,
and cache keys include prompt text.

Invalid match-reference exceptions now expose bounded place/requirement/relation and
allowed/offending references. The existing terminal failure and no-retry policy remain.
The development acceptance entry adds default-off `--capture-semantics`, independent
of requirement capture. It records normalized input, schema-valid output before membership
validation and outcome, linked by call ID, batch and hashes. It does not save raw provider
envelopes or recover malformed SDK responses. Existing secret redaction is reused.
Artifacts are capped at 1 MiB each and 4 MiB per case; partially failed writes conservatively
consume their attempted maximum so residual files cannot bypass the cap. Capture failures
mark evidence incomplete without changing business exit status or causing another send.

These changes affect the shared semantic service used by V1-V3; V0 remains tool-free.
Independent version entry points, travel budgets, supply decisions and Repair are unchanged.
The historical D output remains unavailable and is not reconstructed by synthetic fixtures.

### Validation chronology

- A new test first failed for missing structured error details. Implementation then retained
  the pre-validation output and correlated failure while refusing invalid membership.
- The capture test initially failed to import the missing opt-in wrapper. After implementation,
  controlled real-SDK/MockTransport tests covered exact/cross-candidate/requirement-ID/suffix
  references, empty supported versus unresolved, redaction, default-off, initialization and
  write failures, bounded details, prompt delivery and cache invalidation.
- Spec review found partial writes could bypass the total cap. A real partial-write simulation
  reproduced 5,400,732 residual bytes above 4 MiB. Conservative failed-write accounting fixed
  it; the 14 new tests passed. Standards review had zero findings and Spec re-review cleared
  the cap issue.
- The first full suite stopped making progress in the existing retrieval segment and was
  interrupted without a diagnosis of that stall. A repeat with timeout stack diagnostics
  completed: 1624 passed, 9 skipped, one assertion failed. The failure compared random new
  call IDs across two equivalent planning runs. Adding only call_id to that test's existing
  nondeterministic telemetry exclusion preserved all business comparisons; isolated retest
  passed. Final full-suite retest: **1625 passed, 9 skipped, 0 failed**, in 73.59 seconds.
  Scoped Ruff, formatting, compilation, CLI help and diff whitespace checks passed.
  No Python static type checker is configured. Final Standards/Spec reviews have no
  remaining findings.

No live, P3, staging or commits occurred. Offline tests verify controlled response handling;
real model compliance and D's final itinerary remain unvalidated. A separately approved D
retest should enable both requirement and semantic capture, retaining the same stop rule.

## 22. D dual-capture completion with quality limitations (2026-09-26)

Following separate approval, D executed once with unchanged input and budgets, exiting
0 in 133.797 seconds. Prompt-16 interpretation passed VALID/CLEAR, preserving mountain,
one-off zoo and rich-trip soft meaning. Both prompt-2 semantic batches passed, using
2/6 calls and 33.129/120 seconds. Requirement capture has two linked artifacts; semantic
capture has six across two input/output/outcome groups, totaling 80,941 bytes. Both
captures are complete; hashes and same-candidate reference membership were checked offline.

The itinerary has 14 distinct canonical main visits, no cross-day repetition, and varied
museum/gallery/landmark/outdoor/zoo/activity venues. Battersea Park Children's Zoo on
October 3 satisfies the one-off zoo goal. VauxWall East on October 6 and Aldgate City
Bouldering on October 8 are explicitly labeled indoor related alternatives, not mountain
climbing fulfillment. Actual mountain climbing remains unfulfilled.

Daily main counts are 3/3/2/1/2/1/1/1. October 4, 6, 7 and 8 each have one main visit:
minimum coverage is satisfied, but four quantity observations remain NEEDS_REVIEW.
The unchanged quantity-review policy is disabled, giving no authorized Repair targets.
No Repair ran. Product complete and no confirmed violations do not establish richness
or real-world feasibility; final validation also has 16 PASS and 20 UNKNOWN findings.

Verdict: observed improvement with remaining quality limitations, not unconditional
rich-trip acceptance, model reliability evidence or formal comparison. Recorded budgets
were respected and retrieval resources closed. No retries, production edits, P3 work,
staging or commits. A proposed next step is offline diagnosis of sparse-day generation
and supply/review boundaries, requiring separate approval before changes.
Evidence and report: `artifacts/poi_semantics_acceptance/20260926_D_semantic_capture_retest/`.
