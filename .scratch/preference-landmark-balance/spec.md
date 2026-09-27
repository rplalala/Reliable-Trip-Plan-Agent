# Preference coverage and local landmark balance

Status: ready-for-agent
Date: 2026-09-27
Design status: Accepted decisions; specification published; implementation pending
Baseline revision: 8f5e9b3cdb60c4c7f3fbb55f68ebb8a24dd7ac86

## Problem Statement

Travelers with ordinary positive interests can receive a trip dominated by those
interests while representative local sights are absent. Existing preference
discovery and selection can continue rewarding the same interests throughout the
candidate pool. General attraction discovery is currently conditional on how many
other discovery intents already exist. General exploration does not establish that
a place is a representative landmark.

A six-day Paris development smoke motivated this discussion: an isolated reviewer
preferred the visible V0 itinerary over the grounded versions, particularly its
landmark and museum coverage. This single itinerary-only assessment does not prove
that V0 is generally more reliable or that any particular mechanism caused the
difference. The requested improvement is a general planning policy, not a Paris
exception or a benchmark optimization.

Travelers need a recognizable destination experience that accommodates their
interests without turning every ordinary preference into a trip-wide theme. They
also need truthful treatment of missing evidence and preferences that could not be
accommodated.

## Solution

Treat each independently interpretable, POI-based positive preference as a soft
coverage objective for the final itinerary. Its default target is one distinct
qualifying POI. Raise that target to two only when the user's original wording
explicitly identifies the interest as a focus of this particular trip. Meeting the
target ends its additional preference priority; it does not prohibit more POIs of
that kind. A supported POI can satisfy several preferences simultaneously.

After accommodating these soft objectives where feasible, prioritize local
representative landmarks while considering practical schedules, geography and
variety. A landmark can also satisfy a preference. Explicit user quantities,
exclusions and restrictions retain precedence. Limited time can leave some soft
objectives uncovered; show the remaining gaps without calling them confirmed
violations or pretending the whole trip is verified.

V0 expresses these principles through its existing prompts. V1–V3 additionally use
one bounded model nomination of destination landmarks before candidate discovery,
resolve nominations through existing place identity boundaries, and merge them into
the shared candidate pipeline. Nomination supports planning priority only; it does
not prove opening hours, admission, route feasibility or cost.

## User Stories

1. As a traveler, I want an ordinary interest to receive meaningful coverage, so that it is represented without dominating my trip.
2. As a traveler, I want an explicitly stated trip focus to receive a soft target of two POIs, so that my emphasis has a concrete effect.
3. As a traveler, I want emotional wording such as "I especially like museums" to retain the ordinary target, so that the system does not invent a trip theme.
4. As a traveler, I want the system to retain the original wording supporting a trip-focus decision, so that the interpretation can be checked.
5. As a traveler, I want each independent POI-based preference considered, so that several interests are not collapsed into a single generic goal.
6. As a traveler, I want one relevant POI to cover multiple interests when supported, so that the itinerary uses my time efficiently.
7. As a traveler, I want additional museums or parks to remain possible after my preference target is met, so that important landmarks are not excluded by an artificial category cap.
8. As a traveler, I want explicitly requested quantities preserved, so that a default target does not overwrite what I asked for.
9. As a traveler, I want explicit maximum quantities preserved, so that a soft saturation threshold does not weaken an actual limit.
10. As a traveler, I want exclusions and exclusive scopes respected, so that landmark priority does not send me to places I ruled out.
11. As a traveler, I want enjoyment, pace and similar whole-trip goals treated across the itinerary, so that one stop is not falsely declared to satisfy them.
12. As a traveler, I want coverage assessed from scheduled visits, so that a matching candidate that was never arranged does not count as fulfillment.
13. As a traveler, I want feasible alternatives available for an interest, so that one closed or unsuitable candidate does not consume the only opportunity.
14. As a traveler, I want classic sights considered even when I list several interests, so that preference queries do not eliminate general destination discovery.
15. As a traveler, I want a classic museum to retain its destination value after my museum target is met, so that preference saturation does not demote the landmark itself.
16. As a traveler, I want representative landmark nominations based on the destination, so that my positive preferences do not bias every discovery source in the same way.
17. As a traveler, I want nominated names resolved to supported place identities, so that a model suggestion is not presented as a verified location without evidence.
18. As a traveler, I want ambiguous nominations left unresolved, so that the system does not silently substitute a similarly named place or an adjacent attraction.
19. As a traveler, I want user-named places handled before optional nominated landmarks, so that an auxiliary feature does not displace an explicit request.
20. As a traveler, I want practical routing and date compatibility to affect landmark selection, so that nomination rank does not dictate an infeasible trip.
21. As a traveler, I want varied experiences and geographic coherence, so that many individually famous places still make a useful combined itinerary.
22. As a traveler, I want suspected overlapping experiences treated cautiously, so that different place IDs do not automatically imply independent highlights or justify unsupported deletion.
23. As a traveler, I want my explicit request for separate related visits retained, so that diversity guidance does not erase my intent.
24. As a traveler, I want reasonable planning to continue when nomination is unavailable, so that a failed auxiliary call does not unnecessarily terminate my request.
25. As a traveler, I want uncovered soft preferences disclosed, so that a completed output does not overstate what was arranged.
26. As a traveler, I want time constraints to take precedence over filling every soft target, so that many preferences do not force an overcrowded itinerary.
27. As a project maintainer, I want V0 to remain LLM plus prompts, so that its independent mechanism boundary is preserved.
28. As a project maintainer, I want V1–V3 to share this baseline improvement, so that ordinary planning quality is not reserved for V3.
29. As a project maintainer, I want nomination calls and search sends explicitly bounded and reported, so that their cost and time are visible.
30. As a project maintainer, I want unused search allocations reusable within the same total, so that reservations do not waste available capacity.
31. As a project maintainer, I want evidence-backed tuning after bounded tests, so that configurable limits can improve without silently exceeding an approved run budget.
32. As a project maintainer, I want soft targets distinguished from hard requirements and verified facts, so that V3 does not manufacture confirmed violations from ordinary preferences.

## Implementation Decisions

### Preference semantics and coverage

- Use an application-owned soft coverage target of one per independent POI-based
  positive preference. Use two only for an explicit statement of the current trip's
  focus, such as "This trip is mainly about museums." "I especially like museums"
  alone remains one. The focus classification must retain exact user-source
  provenance. Ambiguous wording falls back to the ordinary soft target.
- Keep inferred product-policy targets distinct from user-authored exact/minimum/
  maximum quantities. Existing explicit-count fields must not be populated with
  inferred one/two values. Represent target origin and focus provenance separately
  in the existing interpreted-requirements/policy boundary as needed.
- Count distinct qualifying scheduled POIs, not candidates, references or repeated
  visits to the same canonical identity. A POI may cover multiple requirements only
  through supported matches. Preserve the existing role and exception boundaries.
- Whole-trip goals such as enjoyment, relaxation and low travel burden do not
  acquire a POI-count fulfillment claim.
- Ordinary and trip-focus targets are soft. Explicit quantities and restrictions
  preserve their existing semantics; exclusive scope does not authorize the model
  to infer an unspecified count or category ratio.
- Saturation removes additional priority from the satisfied preference only. It
  does not remove a POI's independent landmark value or its support for a different
  uncovered preference. Explicit maxima remain enforceable limits.
- The one/two rule applies to final itinerary coverage. Candidate selection must
  retain reasonable alternatives; one matching selected candidate is not evidence
  of final fulfillment. Avoid candidate buckets that continue consuming all
  opportunities solely because the same preference remains a discovery source.
- When soft goals compete with a feasible, varied itinerary, prefer places that
  jointly cover interests and destination value. Permit unresolved soft gaps and
  expose them through existing progress/presentation mechanisms. A soft gap alone
  must not become a CONFIRMED violation or a new automatic Repair target.

### Destination landmark nomination

- Add a focused nomination service and strict structured model response through
  the existing LLM client abstraction. Keep provider calls outside graph nodes.
  Use the configured model/deployment unless separately approved otherwise.
- Run nomination after the request has passed existing input/Gate checks and before
  candidate discovery. Use destination identity/context; do not condition the
  positive nomination list on personal interests or ask the model to extract new
  preferences during this call.
- Return an ordered, bounded list of representative place names. Preserve model
  origin and rank as planning metadata. Nominations are not user-named REQUIRED
  places and do not modify the user's requirement contract.
- Rank supplies a soft classic-landmark preference. Existing exclusions, identity,
  factual eligibility, primary-role and feasibility checks remain authoritative.
  Landmark status is not an operating, admission, reservation or cost fact.
- Deduplicate canonical identities after reliable resolution. Retain each
  candidate's landmark and preference relationships independently; a landmark is
  not required to be unmatched to preferences to qualify for general priority.
- Reuse already acquired search results before issuing supplementary name queries.
  Apply the existing identity-resolution boundary. An unresolved or ambiguous name
  remains unresolved; do not take the first search hit, infer an alias, or equate a
  museum with its pyramid, courtyard or nearby monument without supported identity.
- Merge supported nomination candidates through the shared discovery, admission,
  Details, semantic assessment and selection flow. Give classic discovery explicit
  opportunity even when preference-intent count is high. Retain its opportunity
  through bounded merging and selection, not merely as a discarded search result.
- Failure, invalid output, timeout, exhausted allowance or zero resolved nominations
  degrades to the available qualified pool. Record the degraded nomination/coverage
  state. Preserve normal cancellation and existing hard input/provider failures;
  the fallback applies to this auxiliary nomination capability.

### Resource policy

| Resource | Initial bound |
| --- | --- |
| Nomination model sends | At most 1 per planning request; no retry or corrective model call |
| Nominated places | At most 12 |
| Nomination input | 8,000 tokens including applicable prompt/schema/framing accounting |
| Nomination output | 2,000 tokens |
| Nomination call time | At most 20 seconds, shortened by remaining request allowance |
| Candidate search sends | Existing request-wide total of 12 |
| Supplementary nomination name searches | At most 4, charged to the same 12-send pool |

- The new model call has its own explicit accounting; it does not consume or enlarge
  the semantic-assessment allowance. It uses the current request deadline without
  resetting it. Existing caller-specific deadline behavior remains intact.
- User-named places have first claim on search opportunities. Plan a general
  destination-attraction search opportunity alongside preference discovery;
  nomination supplements cannot displace user-named processing. If higher-priority
  work exhausts the total, record skipped classic discovery rather than overrun.
- Four supplementary searches are a ceiling, not an entitlement or four additional
  sends. Allocate within the remaining shared pool, reusing cache/search matches
  and reallocating unused opportunities to remaining discovery work.
- Existing candidate, Details, final-supply, RAG, semantic, routing and Repair limits
  remain unchanged by this feature. Nomination count is not a guaranteed resolved,
  admitted, selected or scheduled count. No fixed final classic-versus-preference
  ratio is introduced.
- Bounds are configurable. The user permits considering increases based on test
  evidence. Record measured bottlenecks, expected benefit, costs, validation scope
  and rollback criteria before tuning; a run's approved budget remains binding.
- Capture nomination outcome, actual calls/sends, timing, available usage, resolved
  and unresolved counts, and search-allocation stops using current observability
  conventions. Missing billed usage remains missing. Raw provider capture and
  secret handling retain existing restrictions.

### Diversity and version boundaries

- Use nomination and generation guidance, together with existing semantic admission,
  to discourage repetitive experiences and fragmented visits to related sites.
  Uncertain overlap is a soft planning consideration, not a new hard prohibition.
  Explicit requests for separate related visits retain precedence.
- This iteration does not introduce a parent-site graph, inferred canonical
  equivalence, structural site grouping or hard category quotas. It cannot promise
  detection of every overlapping experience across distinct IDs.
- V0 receives prompt-level expression of the same planning principles through its
  existing LLM flow. It receives no nomination call, external resolver, candidate
  service or new enforcement pipeline. Its name-based observations do not become
  canonical or evidence-backed fulfillment claims.
- V1–V3 share nomination, preference-aware supply and generation changes. V1/V2
  remain without Repair. V3 retains its existing validation and Repair authority;
  soft target saturation does not expand that authority.
- Preserve all independent version entry points and existing structured input
  fields. Any compatible progress/schema additions must distinguish soft coverage,
  model knowledge and verified evidence and remain compatible with saved outputs.

## Testing Decisions

Use existing high-level planning runner/service boundaries with injected fake model,
place, route and retrieval collaborators as the main acceptance seam. Assert visible
outcomes, requirement/progress contracts, scheduled identities and real collaborator
send counts. Avoid asserting private helper order or merely reproducing the selector
algorithm in a test. A small additional adapter seam is justified for the nomination
wire schema, bounded tokens, timeout and usage propagation.

The user explicitly accepted these testing seams during specification synthesis:
existing planning entry points with injected fake model/place services, plus bounded
wire-schema and timeout checks for the new nomination adapter.

Prior art includes existing planning-supply policy/pipeline tests, request-wide
preference and taxonomy tests, structured semantic adapter tests, and independently
injected V0–V3 runner/graph tests. Reuse those fixtures and ownership patterns.

Required observable scenarios:

1. Ordinary preference has soft target one; current-trip focus with exact source
   text has two; emotional intensity alone and ambiguous focus retain one.
2. Explicit counts, maxima, exclusions and exclusive scopes retain precedence.
   The inferred soft target never appears as an explicit user quantity.
3. One supported scheduled POI covers two independent interests; unresolved or
   unsupported matches do not. Repeated canonical visits and optional references
   do not inflate distinct coverage.
4. Meeting a soft target removes further preference priority without banning a
   third same-category landmark or suppressing another uncovered preference.
5. Candidate-only coverage is not final fulfillment; closed/unavailable candidates
   leave alternatives usable and unresolved final gaps visible.
6. Many competing preferences can remain partly uncovered under limited time;
   broad enjoyment and pace wording do not become POI-count satisfaction claims.
7. Multiple preference intents do not remove the general attraction discovery
   opportunity when budget remains. Landmark metadata survives admission/selection
   and is independent of preference support.
8. Nominations do not receive personal-interest conditioning, become user REQUIRED
   places, bypass explicit exclusions or acquire factual authority from rank.
9. Successful exact identity reuse avoids a supplementary send; ambiguous names,
   alias-only matches and neighboring attractions remain unresolved under the
   existing identity policy.
10. User-named processing takes priority; supplementary nomination sends are at
    most four; all candidate searches together remain at most twelve. Cover cache
    reuse, fewer than four needed, exhausted higher-priority work, and reuse of
    unspent opportunities.
11. Nomination sends at most once, including malformed schema and timeout cases;
    enforce input/output/list bounds and remaining deadline. No fallback model call
    or hidden retry is permitted.
12. Auxiliary nomination failure preserves usable existing planning paths and
    truthful degraded diagnostics. Cancellation is propagated and resources close.
13. Nominated candidates still fail ordinary identity, role or factual-admission
    checks when appropriate. Candidate/Details/final-supply budgets stay unchanged.
14. Prompt fixtures express variety and caution about overlapping site experiences
    without introducing unsupported identity merging or hard category limits.
15. V0 creates no new nomination/provider calls. V1/V2 never invoke Repair. V3
    retains existing target authorization and does not treat soft gaps as confirmed
    violations. All four independent entry paths retain valid output contracts.
16. Observability records actual budgets and missing usage correctly, and compatible
    schema consumers distinguish one/two soft targets from explicit counts.

Run focused tests while implementing. Shared contract and planning changes require
the full relevant backend regression suite and applicable lint/format checks before
delivery. Include affected presentation tests only if progress output changes.
Deterministic fixtures verify mechanics, not model nomination quality. Any later live
pilot needs a prepared case list, attempt/network policy, capture paths and approved
budget; delegate its execution to the established smoke-test conversation. No live
pilot or formal evaluation is authorized merely by publishing this specification.

## Out of Scope

- Formal benchmark design, formal cross-version comparison, thesis conclusions or
  claims that this feature reproduces the Paris blind-review preference.
- Paris-specific lists, scoring exceptions or prompt tuning.
- V0 tool integration, additional V0 model stages, or new V0 enforcement mechanisms.
- A new itinerary generation pass, V1/V2 Repair, or new V3 Repair authority for soft
  preference gaps.
- Named non-main dining support, expanded reference ledgers, or resuming the paused
  food/sparse-day capability investigation.
- Parent-site identity graphs, alias/fuzzy identity resolution, site deduplication
  infrastructure and hard category/landmark ratios.
- New operating-fact guarantees, verified trip-budget coverage or conversion of
  UNKNOWN findings into PASS.
- Raising existing search, Details, candidate, semantic, RAG, route or Repair
  ceilings; nomination has only the separately specified new bounded call.
- Live execution, commits, pushes, branch changes or version freezes as part of
  this specification-authoring task.

## Further Notes

The user accepted the design decisions through the grilling discussion and then
requested specification publication. This request authorizes this document; the
ready-for-agent status describes specification readiness, not completed
implementation or a live execution allowance. Current project documents remain the
source of truth for implemented behavior until implementation and documentation
synchronization occur.

Current-code facts relevant to implementation: continuing preferences presently do
not have the proposed saturated soft-coverage behavior; selected intent buckets can
continue rewarding the same preference; general discovery is conditionally appended;
there is no dedicated classic-landmark rank; the named resolver uses normalized exact
provider display-name matching. Existing exploration opportunities are not proof of
landmark coverage. Preserve the distinction between those facts and this proposed
behavior.

For the six-day baseline, the effective candidate policy was C64/G32/K16. A read-only
inspection also found that a documented ordinary Details ceiling of G+8 should not be
assumed to be an independently enforced gate: the observed implementation relies on
the global Details allowance and stage deadline. Verify effective limits when wiring
the feature; do not silently fix or expand unrelated budgets to make nomination fit.

The initial nomination limits are engineering estimates inspired by existing bounded
calls. Nomination token use, average latency, resolve success and monetary cost have
not yet been measured. Future tuning should distinguish model-call cost, provider
query competition, evidence quality and final itinerary quality.

Existing uncommitted project documentation, local smoke/validation evidence and paused
diagnostic records must be preserved. This specification records future work without
rewriting those historical results.
