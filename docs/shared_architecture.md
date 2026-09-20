# Shared architecture

## Version and responsibility boundaries

V0 is plain LLM planning without external travel acquisition. V1 adds tools and current evidence.
V2 adds TripWorld main-candidate discovery before shared admission. V3 targeted validation/repair
is not implemented. The implemented versions have independent runners; product/developer APIs
currently dispatch only V0. React, FastAPI and backend orchestration remain a modular monolith.

```text
PlanningRequest -> optional shared interpretation -> canonical context
V0 -> plain generation -> itinerary_2
V1 -> Google discovery ---------------------------------------+
V2 -> Google discovery + TripWorld / Google resolution --------+-> canonical union
   -> admission -> Details/selective Reviews -> deterministic supply
   -> Weather/Routes/Official Web -> primary generation/validation -> Nearby -> itinerary_2
```

Application code owns form facts, identity, provenance, mechanical rules, budgets and validation.
The Requirement LLM interprets language once; the itinerary LLM uses bounded supplied context.
Discovery source, factual provider and budget owner are different dimensions. TripWorld enrichment
is a retrieval prior, not current evidence. Google resolution does not imply Google discovery.
Review signals and official claims retain their separate evidence and uncertainty boundaries.
UNKNOWN is not verified satisfaction. Provider responses are normalized behind services/adapters.

Detailed owners: [requirements](shared_requirements.md), [supply](shared_poi_supply.md),
[output](shared_itinerary_output.md), [V0](v0_design.md), [V1](v1_development.md), [V2](v2_design.md).
Shared changes preserve version mechanisms. Passing checks never automatically freezes a version.


## Evaluation checkpoint and future validation boundary

V2 current implementation checkpoint accepted: this closes primary implementation/smoke work,
not shared-code correctness maintenance. A formal-evaluation baseline checkpoint binds code,
configuration, contracts, prompts, corpus/space and deployment state to intended mechanism
comparisons. Shared correctness fixes apply to every dependent version; record checkpoint changes
and assess affected evaluations rather than fixing ordinary shared bugs only in a later version.

Future V3 adds explicit post-generation validation, structured violations, targeted repair and
re-validation. It is not another POI selector. The [current issue triage](known_issues.md#current-checkpoint-triage-2026-09-20)
separates missing evidence from repairable plan contradictions. Neither V3 nor acceptance makes
UNKNOWN facts verified. No formal evaluation or V3 implementation is started by this record.
