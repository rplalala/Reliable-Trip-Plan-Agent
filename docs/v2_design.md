# V2 main-candidate RAG integration

Current shared/V3 engineering checkpoint (2026-09-25): see [closeout](v3_closeout.md)
for current configuration, shared ownership and artifact-verified evidence. Earlier dated
implementation/live statements below retain their original scope. V0 remains tool-free;
V1/V2 do not run Repair; the product default remains V0. Provider recovery UI is offline-only.


V2 adds discovery before shared admission, not RAG references after the itinerary.

## Query construction and bounded work

<a id="b-cde410ef021f-0"></a>

The existing interpreted DiscoveryIntent supplies query text and positive requirement links.
Normalize/deduplicate text and preserve merged intent/requirement provenance. Ordering follows
requirement strength and stable intent identity. No second language parser or raw-preference
keyword rules are introduced. Empty preferences, only named intentions, or no usable discovery
intent produce the versioned `top attractions` system-default query, never a user preference.
Dates, money, traveler count and internal IDs are not embedded as a whole request.

<a id="b-cde410ef021f-1"></a>

Under default quality_first_1: at most four query texts, one embedding batch,
20 results each, 80 result positions scanned across queries, 16 new resolution entity attempts,
20 incremental Details sends and four fallback searches. Failure counts toward attempts.
Each query is at most 200 characters/512 tokens; total query tokens at most 2048.
The destination circle remains 15 km and identity tolerance 1 km. All runtime retries remain zero.

## Resolution, merge and evidence

<a id="b-6e22a34753f8-0"></a>

Known Google IDs reuse compatible evidence or request required current Details. Missing/failed
IDs may use bounded name/location fallback (one fallback per entity, up to three results).
Unresolved ordinary RAG candidates are recorded and skipped; unresolved REQUIRED identity keeps
the shared clarification boundary. No corpus-wide Google validation occurs.

<a id="b-6e22a34753f8-1"></a>

Canonical Google ID determines one shared candidate. Preserve all real discovery origins and
intent references without duplicate rewards. Google resolution of a RAG place is not itself
Google discovery. Do not invent Google rank or equate cosine with rank. Early RAG Details can
be reused in shared acquisition, while cheap admission fields remain stage-aligned. Static
categories/enrichment cannot become current opening, price or Review/Profile facts.

<a id="b-6e22a34753f8-2"></a>

RAG failure retains acquired Google and resolved RAG evidence and continues the same request;
it does not rerun V1, interpretation or paid work. V1 has no retrieval extension. Nearby remains
post-primary and uses actual scheduled anchors with unchanged independent budgets.

## Runtime ownership, timeouts and failure handling

Default quality_first_1 has SQL60s and RAG360s, embedding/connect/Google8/10/4s, zero retries;
SQL time is constrained by remaining phase time. Historical SQL3/RAG30 and60/180 are preserved in development records and explicit test fixtures;
they are not separate active configuration files. Deadlines stop new work; cleanup is awaited and user
cancellation propagates. Ordinary failures retain Google and already resolved RAG results in
the same request without rerunning V1, interpretation or paid acquisition. Failed attempts count.

versions/v2/runner.py injects discovery; policies/tripworld_query_plan.py builds queries;
services/tripworld_discovery.py resolves/merges; tripworld/retrieval/runtime.py owns DB execution.
[Supply](shared_poi_supply.md), [output](shared_itinerary_output.md) and [V1 tool/Nearby design](v1_development.md)
are reused. Space and persistence are in [retrieval](v2_tripworld_retrieval.md); historical SQL
failures and measured waiting allowances belong to [V2 development](v2_development.md).

## Shared first-draft checkpoint

Shared generation guidance, explicit activity roles and observational daily diagnostics
apply before Nearby. Long-trip supply is K18/K20 for nine/ten days; acquisition is still
bounded at C64/G32/send40/P8. Full baseline Routes support 400 directed elements in at
most seven requests. Alternatives and all discovery/enrichment budgets are unchanged.
This does not guarantee daily coverage or introduce post-generation refill/repair.
See [shared output](shared_itinerary_output.md#first-generation-roles-and-diagnostics)
and [shared supply](shared_poi_supply.md) for the single detailed contract.


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
