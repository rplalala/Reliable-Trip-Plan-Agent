# Shared architecture

Current semantic extension (2026-09-26): shared candidate judgments and V3 automatic deduplication
are implemented with offline evidence only; see the [checkpoint](shared_poi_semantics_plan.md#12-implementation-checkpoint--2026-09-26).
Earlier shared/V3 engineering checkpoint (2026-09-25): see [closeout](v3_closeout.md)
for current configuration, shared ownership and artifact-verified evidence. Earlier dated
implementation/live statements below retain their original scope. V0 remains tool-free;
V1/V2 do not run Repair; the product default remains V0. Provider recovery UI is offline-only.


## Version and responsibility boundaries

V0 is plain LLM planning without external travel acquisition. V1 adds tools and current evidence.
V2 adds TripWorld main-candidate discovery before shared admission. V3 adds implemented targeted
validation, bounded multi-round Repair and revalidation before final Nearby. Independent V0-V3
runners remain available; the product default remains V0. React, FastAPI and backend orchestration
remain a modular monolith. Historical proposal sections below do not override this current flow.

```text
PlanningRequest -> optional shared interpretation -> canonical context
V0 -> plain generation -> itinerary_2
V1 -> Google discovery ---------------------------------------+
V2 -> Google discovery + TripWorld / Google resolution --------+-> canonical union
   -> admission -> Details + semantic assessment / selective Reviews -> bounded supply
   -> Weather/Routes/Official Web -> primary generation / shared checks
   -> V1/V2: final primary; V3: validation / targeted Repair / revalidation
   -> one final Nearby stage -> itinerary_2
```

Application code owns form facts, identity, provenance, mechanical rules, budgets and validation.
The Requirement LLM interprets language once; a request-owned candidate LLM judges actual visit
objects and scoped requirement matches. The itinerary LLM uses bounded supplied context. V3's
Repair LLM proposes authorized edits; application checks decide adoption. Candidate semantic
failures terminate, while pre-send preparation limits leave unassessed candidates unauthorized.
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

## First-draft baseline extension

All V0/V1/V2 use shared first-generation coverage guidance and model-declared activity
roles. V0 observes normalized name proxies after generation/date checks; V1/V2 observe
validated supply IDs before independent Nearby discovery. Diagnostics never call tools,
change activities or trigger generation. Long-trip supply can now reach K20 while
ordinary acquisition remains C64/G32/send40/P8. See the responsibility-owned
[output contract](shared_itinerary_output.md#first-generation-roles-and-diagnostics)
and [supply policy](shared_poi_supply.md). This changes the shared evaluation checkpoint;
prior smoke outputs remain historical evidence, not validation of this new prompt.


## Compatible transfer output update (2026-09-25)

The shared itinerary DTO now accepts optional `transfers` (missing defaults empty).
Current V3 binds and presents verified/unknown per-leg route estimates and separate
application reserves; V0-V2 do not fabricate transfers or acquire additional routes for
this field. Primary model DTO/prompt, K, existing version entry points and product default
are unchanged. The frontend can render this optional data when supplied; this does not
implement the deferred Product V3/API selection or the whole frontend backlog.
See [V3 design](v3_design.md#shared-output-and-frontend) and the
[development verification record](v3_development.md#mixed-transport-and-joint-components-2026-09-25).
This is shared output compatibility, not evidence of a V3-only quality gain or a re-freeze.


## Shared first-generation mixed transport (current offline checkpoint)

V1/V2/V3 now use shared baseline routing, bounded pre-generation mixed-mode options,
one primary generation, and actual-adjacency/time transfer binding before the version's
post-primary step. V1/V2 report conflicts and UNKNOWN without repairing activities.
V3 reuses the same evidence and adopted transfers in its existing validator and Repair.
V0 remains tool-free. This is a shared baseline upgrade, not V3-exclusive mechanism value.

The normal planning supply is unchanged: this does not rediscover omitted POIs, increase K,
or add a second discovery pass. Default WALK preference permits evidence-supported TRANSIT
and DRIVE alternatives; explicit supported requirements remain restrictive. Representative
TRANSIT never inherits final-time PASS. Provider duration and DRIVE application reserve are
separate. The primary projection retains all directed baseline facts in a compact catalogue;
it drops redundant wrappers, not inconvenient facts. No selective fact omission is performed.
Unbound actual adjacencies remain in application-owned `route_diagnostics`, including
per-mode facts and unresolved alternatives; absent transfers do not erase obligations.

Primary input is 252000, output 16384. Supplementary totals are 32 directed pairs / 32 sends /
64 requested elements; post-generation reservations are 16 / 16 / 32 within those totals.
Baseline remains 7 / 400 / 64. Cumulative route-work wall time is 120 seconds with 30 seconds
reserved for post-generation, always inside the original request deadline. Other acquisition,
Repair and Nearby limits are unchanged. Common transport policy now belongs to `transport`
in runtime.yaml; Repair-only authority and added-burden policy remain version-specific.

Implementation and tests are recorded in `docs/v1_development.md`. This checkpoint has only
offline evidence; historical development live records are unchanged and do not validate it.
No new live, evaluation, freeze, commit or push is implied.


## Shared preference input gate checkpoint (2026-09-25)

Implemented + offline-validated only. All V0-V3 entries reuse the existing single preference
interpretation call to assess request-level input issues before travel acquisition. Application
policy checks exact provenance and returns rewrite/clarification or dedicated safety outcomes;
VALID does not certify feasibility or override hard-requirement/capability checks. Empty input
still skips interpretation. Model contract/provider failures remain system failures. Product
engine selection and travel budgets are unchanged. Historical live runs were not retroactively
validated with this feature. See [shared preference input checkpoint](shared_preference_input.md)
for contracts, compatibility, API/UI behavior, actual test chronology and serializer limits.


### Minimum daily coverage update (2026-09-25)

Shared output now reports the one-primary-visit minimum independently of 2-5 review
quantity guidance. V0-V2 remain diagnostic-only; V3 prioritizes confirmed minimum gaps
below hard protections and above optional reviews. Explicit source-linked full-day time
protections support exemptions; uncertain applicability remains unknown. Product output
includes coverage status without research metadata or source quotations. The primary
prompt, default engine and budgets are unchanged. See [shared minimum coverage](shared_minimum_daily_coverage.md)
for counting, compatibility, exemption and partial-result boundaries, and the V3 development
checkpoint for offline and live evidence. This does not retroactively validate historical runs.


Preference Gate contract-alignment checkpoint: prompt11/wire9/input2 reserves operational
conflict links structurally to structured issues and retains domain fail-closed enforcement.
The historical first smoke remains BLOCKED; see docs/shared_preference_input.md for offline
results and the separately authorized new interpreter-only smoke. No travel budget changes.


New Preference Gate smoke `9c8eb048-1e8c-47bd-b17f-9578a7c7c6f8` stopped before any model
send due to a capture-harness UnboundLocalError. All10 cases NOT_ATTEMPTED; SDK resources
closed. Alignment remains offline-validated; Step1 live remains BLOCKED. No rerun performed.
