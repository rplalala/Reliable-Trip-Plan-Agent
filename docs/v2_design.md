# V2 main-candidate RAG integration

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
