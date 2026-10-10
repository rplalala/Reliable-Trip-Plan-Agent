# V2 development record

> Repository cleanup (2026-09-20): source/document/config recovery snapshots, including
> `D:/Workspace/Capstone/phase6_source_snapshots`, have been permanently deleted by user approval.
> Snapshot paths in dated entries describe historical actions, not available recovery locations.
> Retired selector implementations are no longer executable. Historical methods/results remain.

Historical checkpoints retain their recorded scope and status. Current contracts are in
[the design index](../../README.md); later implementation does not validate earlier runs.

<a id="m-e7b06f4ead1b"></a>

## TripWorld Phase 4: global retrieval foundation and OpenAI spike

Status: development spike completed on 2026-09-18 and explicitly accepted as complete.
This is implementation validation, not a formal benchmark, research conclusion, or V2 freeze.
Phase 1-3 artifacts were reused. V0/V1 runtime paths and selection logic were not changed.
No global embeddings, PostgreSQL, pgvector, Google resolution, candidate merge, or V2 integration were implemented.

### Global entities and identity limitations

| Measure | Count |
| --- | ---: |
| Source rows | 687,173 |
| RetrievalEntities | 647,057 |
| Google-ID-backed entities | 526,682 |
| FSQ-only entities | 120,375 |
| Google IDs with multiple FSQ rows | 30,633 |
| Excess source rows removed from retrieval slots | 40,116 |
| Largest group | 43 |
| Entities with empty retrieval text | 3 |
| Entities without valid coordinates | 9 |
| Eligible / ineligible / unknown | 285,927 / 63,789 / 297,341 |

Google-backed means a source Google Place ID exists; it does not mean that Google has
currently resolved or validated that place. Group by nonblank Google ID, otherwise by FSQ ID.
Preferred names use deterministic normalized Google-name frequency, then FSQ names;
ties, aliases, categories, semantics, and provenance have stable ordering. Both texts are
rebuilt at entity level. Unicode/case normalization removes duplicate aliases/categories.
Coordinates use an actual observed medoid, not an averaged invented point. The entity
retains all contributing FSQ IDs and country/region/locality values.

Within merged groups, maximum pairwise coordinate spreads are:

| Spread | Groups |
| --- | ---: |
| Up to 100 m | 16,314 |
| 100 m-1 km | 7,725 |
| 1-10 km | 3,747 |
| 10-100 km | 1,455 |
| Over 100 km | 1,392 |

There are 6,594 groups over 1 km, 2,847 over 10 km, and 449 country conflicts.
These categories overlap. A deterministic medoid does not repair a wrong upstream
Google match. Such entities need later identity review/Google validation; the spike
preserves and reports their flags rather than silently treating them as reliable.
Different Google IDs and FSQ-only records can still represent the same real place.

The global artifact is `data/tripworld/artifacts/retrieval_entities.parquet` (177,556,609 bytes).
Its SHA-256 is `a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7`.
Source corpus SHA-256 is `27230ecb110503dd3b9390e70709eefdab843f6f28ce0b908efd3b36054f6e9b`.
TripWorld revision remains `421bc1dc63068bb398055b1ce987265fe22415db`.
Versions: `tripworld-retrieval-entity-v1`, `tripworld-entity-text-v1`,
and `tripworld-category-semantics-v1`.

### API model and dimensionality decision

Use OpenAI `text-embedding-3-small`, default **1536 dimensions**, float32,
L2-normalized vectors, and cosine similarity. The request omits `dimensions` and uses
no query/document prefixes. RAW and ENRICHED use the same model and query vectors.
Local embedding model evaluation was superseded by the user's API strategy: the
unfinished local weight download was removed, with no local vectors generated.
There are no PyTorch, transformers, sentence-transformers, or CUDA dependencies.

The [official embedding guide](https://developers.openai.com/api/docs/guides/embeddings)
documents the default size, shortened dimensions, normalization, and tokenizer.
The [API contract](https://developers.openai.com/api/reference/resources/embeddings/methods/create)
allows up to 8,192 tokens/input, 2,048 inputs/request, and 300,000 tokens/request.
This implementation deliberately uses 8,191 tokens/input, 64 inputs/batch,
20,000 tokens/batch, at most three attempts, and a US$0.10 spike retry-exposure budget.
Both document variants and query tokens are included in the spike preflight budget.

1536 is the recommended initial production decision because no shortened-dimension
quality comparison has been performed. 768 halves vector storage and arithmetic,
but does not reduce input-token charges; quality may change. Shortening requires an
explicit later decision and a separate artifact contract. No global run was started.

The API exposes the model name rather than a downloadable immutable model revision.
Do not describe this as a pinned weight snapshot. Saved vector hashes, returned model
names, request IDs, timestamps, software versions, source/content hashes, and versioned
configuration preserve the actual run. Future fresh API regeneration is not guaranteed
to be bit-identical; checkpoint reuse preserves the vectors actually received.

### Exact token estimates, API usage, and storage

Full-corpus tokenization uses `cl100k_base` over actual entity texts, not sampling.
The [official model price](https://developers.openai.com/api/docs/models/text-embedding-3-small)
checked on 2026-09-18 is US$0.02 per million input tokens (standard API).

| Variant | Global tokens | Standard cost | Max tokens/document | Sample API tokens | Sample encode time |
| --- | ---: | ---: | ---: | ---: | ---: |
| RAW | 39,160,088 | $0.78320 | 1,431 | 114,901 | 48.329 s |
| ENRICHED | 49,605,198 | $0.99210 | 1,515 | 155,687 | 40.760 s |

Global variants together: 88,765,286 tokens, approximately **$1.77531** before
retries/taxes. Each has three empty texts and no overlong documents. A future global
job must explicitly exclude empty texts and record exclusions; this spike rejects
empty input rather than submitting it to OpenAI.

The sample embedded 2,118 entities per variant plus 24 queries. There were **69
successful requests**, no retries, **270,778 usage tokens**, and an estimated standard
charge of **$0.00541556**. This is usage multiplied by published price, not a billing
invoice. Query encoding took 0.574 s; document encode/checkpoint throughput was
43.82 RAW and 51.96 ENRICHED documents/s. The serial sample extrapolates to about
4.10 and 3.46 hours globally (7.56 hours for both), not a service commitment.
Account limits, future batching, network latency, and document lengths can change this.

Each sample `.npy` is 13,013,120 bytes (12.41 MiB); both are 24.82 MiB.
Global 1536 float32 payload is 3,975,518,208 bytes (3.70 GiB) per variant,
7.41 GiB for both. At 768 dimensions it is 1.85 GiB per variant.
These conservative counts include the three empty entities. Checkpoints and final
arrays coexist locally, so sample disk use includes a second vector copy plus reports.

For one production vector/entity, the [pgvector storage formula](https://github.com/pgvector/pgvector#vector-type)
is `4 * dimensions + 8` bytes. At 1536 dimensions, vector payload alone is
3,980,694,664 bytes. A planning estimate for one table is **5.18-9.26 GiB**, assuming
1-4 KiB/entity of metadata plus 20-50% heap/TOAST/index headroom. This is not measured
PostgreSQL size and excludes HNSW, WAL, backups, replicas, and a second vector variant.

### Representative destinations and geographic filtering

Sampling uses occupied 0.25-degree global grid cells, two coverage strata selections
per tier, six distinct countries, and corpus-derived median coordinate centers.
High means at least 3,000 entities, medium 300-2,999, low 40-299, checked for both
seed cell and radius. Labels come from observed localities, not city geocoding.
Within each 15 km circle, deterministic SHA-256 identity sampling caps entities at 384.
No category preference is used during sampling.

| Destination label | Country | Tier | Full 15 km pool | Embedded sample |
| --- | --- | --- | ---: | ---: |
| Tokyo | JP | High | 48,014 | 384 |
| Kuala Lumpur | MY | High | 15,524 | 384 |
| Santiago | CL | Medium | 2,737 | 384 |
| Antalya | TR | Medium | 2,913 | 384 |
| Melbourne | AU | Low | 292 | 292 |
| Kansas City | US | Low | 290 | 290 |

Tokyo's sample covers only 0.8% of its pool; missing museums or libraries in a sampled
pool is not evidence that the full destination lacks them. Low/high describes this
TripWorld snapshot, not a city's real POI population. This is not a population-weighted
global quality estimate. Sydney does not drive the architecture or sample selection.

Generic geographic filtering is optional country consistency, bounding box, then
Haversine distance before vector ranking. Missing country metadata remains available;
known contradictory country values are excluded when a country is supplied. Missing
coordinates are excluded. Tests cover poles, the dateline, radius boundaries, and
bounding-box corner false positives. No locality-equals-city assumption is used.

Scanning the global coordinate arrays took approximately 114-119 ms per selected
scope. Sample searches used 290-384 geographically filtered candidates; exact ranking
median was 0.69-0.78 ms and p95 0.89-1.18 ms, excluding API/query encoding, serialization,
and artifact load. All retrieved representatives were within their radius; this does
not validate every source coordinate within an anomalous merged entity.

### RAW versus ENRICHED results

The 12 intents each have English and Chinese queries. Six destinations, two variants,
and two eligibility settings produce **576 cases**, each reporting Top-5/10/20.
All full results, scores, categories, entity metadata, location flags, and overlap
diagnostics are in the ignored `data/tripworld/reports/phase4_spike.json`.
The following inspected examples use eligibility filtering and the English query
unless stated otherwise. Scores are cosine values, not calibrated quality scores.

| Observation | RAW | ENRICHED | Interpretation |
| --- | --- | --- | --- |
| Melbourne, quiet indoor | Time Out Fed Square first (0.290); State Library third (0.266) | RMIT Swanston Library first (0.323), La Trobe Reading Room second (0.310), State Library third (0.309) | Useful library prior; access and actual quietness remain unverified |
| Kuala Lumpur, gardens | TWG Tea at The Gardens first (0.371), Town Park second (0.350) | Town Park first (0.396), tea shop second (0.371), Taman Tasik third (0.355) | Better category alignment; name-based contamination persists |
| Kansas City, gardens | Green Lady Lounge second (0.276), between parks | Three parks first; lounge fourth (0.289) | Better park ordering despite a higher irrelevant lounge score |
| Santiago, gardens | Parque Balmaceda first (0.335), other parks mixed with plazas | Five park-category results at the top, Balmaceda first (0.375) | Helpful outdoor category expansion |
| Antalya, gardens | Botanical-garden-category entity first; park and unrelated venue mixed | University botanical garden enters fourth (0.338) | Useful category recall; public access is unknown |
| Tokyo, Chinese nightlife | BOOK AND BED TOKYO first (0.323) | A bar first (0.325), Craft Beer Moon Light second (0.310) | More nightlife-aligned ordering in the sparse sample |

Enrichment is promising for category/experience alignment, but is not uniformly better:

- For quiet indoor queries, Kuala Lumpur's outdoor Town Park remains first and its
  score increases from 0.307 to 0.329. Antalya's botanical-garden-category entity
  increases from 0.281 to 0.318. Relaxing outdoor priors can conflict with indoor intent.
- Melbourne's State Library entity merges the library and lawn: its categories include
  Park/Plaza and its aliases include State Library Lawn. Enrichment increases its garden
  score from 0.365 to 0.416. A single Google identity can contain distinct visit contexts.
- Quiet indoor search in Tokyo still returns a restaurant and a smoking-area label.
  Santiago returns furniture retail and outdoor plazas. More text cannot create a
  relevant missing candidate or enforce a hard indoor constraint.
- "Less touristy" still returns Melbourne Skydeck and other tourist-attraction-category
  results. Neither text variant contains reliable crowding/popularity evidence.
- Enrichment for private/office categories currently contains negative travel language
  such as "generally unsuitable for travel discovery". Embeddings do not enforce that
  negation; eligibility must remain explicit metadata. Review this text in a future
  mapping/template version rather than changing approved Phase 1-3 artifacts now.

Average RAW/ENRICHED ID overlap is 78.61% at Top-5, 79.62% at Top-10, and 81.91% at
Top-20 across all paired cases. This measures ranking change, not accuracy. English/
Chinese Top-5 overlap after eligibility filtering is 57.78% RAW and 61.39% ENRICHED.
Both languages produce plausible museum/nightlife examples, but paraphrase rankings
are not invariant. No relevance labels, precision/recall score, or formal benchmark
claim is made.

### Eligibility, duplicates, and Top-K

Counts below are retrieved slots across 144 unfiltered cases per variant, not unique POIs.

| K | Slots | RAW ineligible | ENRICHED ineligible |
| --- | ---: | ---: | ---: |
| 5 | 720 | 41 (5.69%) | 38 (5.28%) |
| 10 | 1,440 | 87 (6.04%) | 97 (6.74%) |
| 20 | 2,880 | 187 (6.49%) | 232 (8.06%) |

Ineligible examples include office-category Wisma Chuang and residential Warisan
Cityview. Excluding ineligible removes all such labeled slots by construction but
keeps unknown, including some irrelevant stores or services. At filtered Top-20,
unknown accounts for 1,013 RAW and 784 ENRICHED slots. This is not a measured residual
contamination rate: unknown is not synonymous with unsuitable.

There were zero duplicate entity IDs and zero representative-coordinate radius
violations in every Top-K. Location-anomalous entities still appeared in three RAW
and two ENRICHED filtered Top-20 slots. Duplicate suppression covers source Google-ID
groups, not all real-world identity ambiguity.

Increasing K widens the candidate pool and admits more weak/off-intent results.
No production K, similarity threshold, or score-to-Q_rel mapping is selected.
Do not universally exclude cafes, hotels, stations, libraries, markets, or nightlife;
their suitability depends on intent and later validation.

### Mapping gaps and next-stage recommendations

352,875 entities match at least one existing semantic rule. High-frequency unmatched
travel-relevant categories include Buddhist Temple (1,088 hierarchical FSQ occurrences;
921 Google-category occurrences), Ramen Restaurant (5,694), Sake Bar (3,983), Bakery
(2,178 hierarchical FSQ occurrences), Fish Market (151 hierarchical FSQ occurrences),
Fresh food market (520 Google occurrences), and Hiking area (112 Google occurrences).
Counts overlap across sources and hierarchical/leaf forms; they must not be added.
The unmatched list also includes many convenience stores, roads, residences, and
services. Do not target 100% mapping coverage. A small future extension could prioritize
Buddhist temples, food subtypes, public food markets, and hiking categories, while
preserving access uncertainty. No mapping change or source-corpus regeneration was made.

The spike recommended one production text/vector space, explicit eligibility/anomaly
metadata, geography before exact cosine ranking and later demand-driven Google
canonicalization. It did not select production K/threshold/score fusion or prove that
384-candidate timings applied to Tokyo's48014 pool (~281 MiB vector payload).
ANN remained a measured-needs decision; global ANN followed by geography could underfill.
A full build needed frozen text/dimension choices and bounded checkpointed scheduling.
These recommendations became the separate Phase 5/6 decisions, not spike implementation.

### Phase 4 reproducibility and checks

The isolated retrieval CLI was `scripts/tripworld_retrieval.py`; model/query inputs were
`data/tripworld/embedding_model.v1.json` and `retrieval_queries.v1.json`. Phase 4 outputs
and query/sample hashes bind the reported observations. Current setup and restore commands
are in [the development guide](../../guides/development.md); paid regeneration cannot
reproduce provider vectors byte for byte merely by using the same model name.

The isolated adapter used explicit OpenAI configuration with bounded transient retry,
atomic input/vector-hash checkpoints and no implicit provider/env fallback. Lost paid
responses before durable checkpoint could be billed again; alias model names did not
pin immutable weights. Current setup/recovery is authoritative in the guide.
Generated data/vectors/checkpoints/reports remained private, with tiny fixtures and
versioned manifests published.

The full backend regression suite
passed **644 tests**, including **39 TripWorld tests**; Ruff passed. Tests use fake
embedding providers/HTTP responses and do not require API credentials or downloads.
They cover deterministic grouping/rebuilds, geo boundaries, normalized exact ranking,
artifact corruption/version mismatch, retry and failure behavior, preflight budgets,
and interruption/resume. The gate included the existing Phase 1–3 implementation context.
No commit, push, database setup, global embedding, or V2 runtime work was performed.

<a id="m-0045d5920358"></a>
## TripWorld Phase 5: persistent retrieval layer

Phase 4 and Phase 5 were explicitly accepted as complete. The user designated Phases
1-5 as the frozen technical baseline on 2026-09-18, except for concrete bug fixes.
Phase 5 implements an isolated global retrieval
layer; it does not modify V0/V1 runtime, Q+C+G+R+E, or itinerary generation. Phase 6
Google resolution and candidate integration were not yet implemented at this checkpoint. This document
records completed full-corpus engineering validation on September 18, 2026. Phase 5
is implemented; this is not a complete V2 runtime milestone or complete V2 freeze.
Phase 6 was still a design-only proposal at the Phase 5 acceptance date; its later
integration and validation are recorded below.

### Phase 5 local environment

The development environment used Docker Desktop Linux containers, pinned
`pgvector/pgvector:0.8.2-pg17`, PostgreSQL 17.10/pgvector 0.8.2, loopback port 55432 and
volume `reliable-tripworld_tripworld_pgdata`. Current reproducible setup is maintained in
[the development guide](../../guides/development.md); this record preserves observations
from that environment rather than a second command guide.

`validate` reuses Phase 4's existing 24-query vector checkpoint, without API calls.
It requires the completed production vector set and the Phase 4 sample/query artifacts.
The retrieval service itself does not depend on the Phase 4 sample.

### Five-ID sanity check

Exactly five primary Google Places ID lookups used the existing `GooglePlacesProvider`
with field mask `id,displayName,location` and no retries. All succeeded; no fallback
lookups were made. The names and returned coordinates were inspected with no obvious
identity mismatch. This is technical validation of the lookup flow, not a validity-rate
estimate for TripWorld.

| TripWorld name | Google returned name | Latitude | Longitude |
| --- | --- | ---: | ---: |
| Aqua City Odaiba Shrine | Aqua City Odaiba Shrine | 35.6279735 | 139.7738151 |
| Taman Tasik Sri Rampai | Tasik Sri Rampai | 3.1942631 | 101.7285624 |
| Violeta Parra Museum | Violeta Parra Museum | -33.4387945 | -70.6353190 |
| Nabız Live | Nabız Live | 36.8489159 | 30.7536748 |
| State Library Victoria | State Library Victoria | -37.8097255 | 144.9654504 |

The exact entity/Google IDs and Unicode names are retained in the ignored
`data/tripworld/reports/phase5_google_sanity.json`. No per-entity global validation state
was added, no corpus refresh took place, and no reusable Google resolution bridge was built.

### Schema, provenance, and ingestion

The persistent layer separated corpus manifests/entities, immutable vector spaces and
content-addressed embeddings; a view preserved one retrieval slot/entity despite shared
text vectors. Transactional/checksum-locked migrations and COPY ingestion protected
snapshot consistency; unchanged text reused vectors, changed text invalidated association.
ENRICHED alone entered production. Detailed storage/compatibility rules are in
[candidate supply](../../0004-retrieval-persistence%28v2v3%29.md); source/provenance survived ingestion.

The initial full COPY ingestion populated **647,057 rows in 100.57 seconds**.
An unchanged full-corpus rerun completed in **83.76 seconds**, with **zero changed
rows and zero removals**. Tests separately exercise changed-text invalidation and rollback.
Production source SHA-256 remains
`a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7`.
The original TripWorld revision and approved Phase 1-4 artifacts were not regenerated.

### Explicit production policy and preflight

Policy `tripworld-production-policy-v1` excludes ineligible entities, empty text,
invalid/missing coordinates, country conflicts, and coordinate spread **strictly
greater than 10 km**. Unknown remains available. Metadata for every excluded entity
stays in PostgreSQL. The 1-10 km spread flag remains visible on otherwise allowed
entities; the policy is conservative screening, not identity repair or Google validation.

| Exclusion | Overlapping reason count | Mutually exclusive first reason |
| --- | ---: | ---: |
| Ineligible | 63,789 | 63,789 |
| Empty text | 3 | 3 |
| Invalid coordinates | 9 | 6 |
| Country conflict | 449 | 397 |
| Spread over 10 km | 2,847 | 2,067 |

The first-reason priority is the order above. Total excluded is **66,262**;
**580,795 entities** remain, representing **577,011 distinct ENRICHED texts**.
Their texts contain 44,095,604 tokens per entity, or **43,805,323 unique-text tokens**.
Maximum input is 1,515 tokens; no truncation is needed.

At the [published standard model rate](https://developers.openai.com/api/docs/models/text-embedding-3-small)
of US$0.02/million input tokens, the conservative new-vector cost is **US$0.87611**
before existing-vector reuse. Three-attempt exposure is approximately **US$2.62832**.
The preflight requires standard cost <= US$2, retry exposure <= US$5, input <=8,191
tokens, and at least 25 GiB free workspace disk. It runs before paid generation.
Observed workspace free space was approximately 242 GiB, host C: approximately 337 GiB,
and the Docker VM filesystem reported approximately 945 GiB available.

Per-entity vector payload upper bound is 3,568,404,480 bytes (3.32 GiB). Physical text
deduplication reduces this slightly. The rough DB estimate is 4.73-8.69 GiB, excluding
WAL/backups/Docker overhead; checkpoints occupy additional local disk space. The Phase 4
serial-throughput extrapolation was 11,104 seconds (3.08 hours); actual global timings
are reported below rather than inferred from that sample.

### Embedding generation and recovery

The vector space is fixed: OpenAI `text-embedding-3-small`, default 1536 dimensions,
cosine, float32 and L2 normalization, with no prefixes/custom dimensions. ENRICHED is
the only production representation. OpenAI's alias is recorded as such, not presented
as an immutable model-weight revision.

The existing adapter now uses base64 transport to reduce decimal-JSON response size;
the decoded float32 vectors and compatibility contract are unchanged. A mocked test
verifies decoding. Initial 256-text requests had poor observed throughput; a measured
64-text persistent-client probe took 1.70 seconds followed by 0.66 seconds. The build
therefore uses **64 inputs/batch, at most 20,000 tokens/batch, up to sixteen workers**,
with one reused HTTP client per worker. Initial requests are paced at 900,000 tokens/minute,
below the observed account response-header limit of 1,000,000 tokens/minute (3,000
requests/minute). Retries still have bounded backoff; concurrent unrelated account usage
can cause rate-limit responses. These settings are not a promise
of model latency. Model/token cost is independent of batch partitioning.

The build seeds **1,880 eligible ENRICHED sample vectors**, selects only missing distinct
text hashes, writes durable content-addressed checkpoints, and COPY-upserts each
successful batch to PostgreSQL using binary COPY. Repeated runs skip DB vectors with unchanged text.
Database errors roll back the current batch; previously committed batches remain.
Do not delete checkpoints during recovery. Changing batch settings mid-run can change
checkpoint partitions; preserve/recover pending completed batches before changing them.
No exactly-once billing guarantee is possible if a process loses a paid response before
it is durably checkpointed. Tests cover partial failure, resume, and zero new calls on
the third unchanged build. Operational tuning recovered 1,792 pending vectors without
additional API calls.

The completed database contains **577,011 physical vectors**, covering all **580,795
production RetrievalEntities** through `entity_embeddings`. There are zero missing
entity vectors and zero invalid dimensions/norms. Text deduplication preserves one
logical retrieval slot per entity; it does not merge separate entities.

The saved-response audit records **8,577 successful production requests / 8,577
attempts**, **43,669,473 API tokens**, and an estimated **US$0.87338946**. This includes
production timing probes and recovered checkpoints, and excludes the 1,880 reused
Phase 4 vectors. No retries appear in those saved responses. Operator interruptions
and a Windows progress-report file-lock failure occurred during tuning; completed
vector batches were preserved. Progress-report writes now retry and cannot abort a
paid build merely because telemetry is temporarily locked. Another 448 pending
vectors were recovered from checkpoints during a later resume.

The first-to-last saved production response window was **4,065.77 seconds (67.76
minutes)**, from 06:50:15 to 07:58:01 UTC. It includes pauses and tuning but excludes
startup before the first saved response; it is not an exact uninterrupted job runtime.
The final uninterrupted segment took **2,752.63 seconds (45.88 minutes)**. Interrupted
requests whose responses were lost may have been billed and cannot be reconstructed;
the saved-response ledger is an observed cost estimate, not a complete billing invoice.

At completion, PostgreSQL measured **7,260,591,795 bytes (6.76 GiB)**. The entities
table and indexes occupied **1,615,937,536 bytes (1.50 GiB)**; the embeddings table,
TOAST and indexes occupied **5,635,112,960 bytes (5.25 GiB)**. Logical vector datum
size was **3,547,463,628 bytes (3.30 GiB)** including pgvector datum overhead. Docker,
WAL, backups and local checkpoints are additional. These are completion snapshots;
normal database maintenance and reruns can change physical allocation.

Generation reports and checkpoints stay under ignored `data/tripworld/reports/` and
`data/tripworld/artifacts/phase5/`. Secrets are never included. Request IDs and response
model/timestamp/usage data support auditing. API usage costs are estimates, not invoices.

### Retrieval service and indexes

The retrieval service separated query embedding and exact Postgres search, with
read-only compatibility rejection before a paid provider. Geographic/policy filtering,
cosine ranking and stable ID ties preceded final payload lookup. B-tree/GIN exact
identity/geography/alias indexes were used; no ANN, PostGIS, fuzzy fusion was implemented.
Current command examples are in the development guide rather than duplicated here.

### Validation and next-stage boundary

Offline tests used fake providers and a separate opt-in `tripworld_test` database,
with an explicit production-reset refusal. Default tests made no live OpenAI calls.

The final full backend regression suite, including real PostgreSQL integration,
passed **662 tests**. Ruff and `git diff --check` passed. Coverage includes migration
checksums, COPY rollback/idempotence, text changes, vector compatibility/reuse, resume,
policy versions, dateline/pole/radius handling, cosine ties, aliases, sanitized DB
errors, missing-space rejection before paid API calls, and read-only retrieval.

Full-corpus validation passed **144 cases** (24 English/Chinese queries across six
destinations), checking all 2,880 returned slots for entity-ID uniqueness within each
query, geographic correctness, and eligibility/anomaly policy. An independent NumPy
calculation over the complete Santiago 15 km candidate pool matched PostgreSQL's
Top-20 order. Queries used existing Phase 4 vectors with zero API calls. Two additional
end-to-end service smoke queries used the live OpenAI adapter: 2 requests, 16 tokens,
estimated US$0.00000032, accounted separately from the document build.

Among the 2,880 slots, 2,317 were eligible and 563 unknown; none were ineligible.
Eleven retained the 1-10 km coordinate-spread flag. Geography verifies the entity's
representative coordinates, not every merged source coordinate or current Google
location. Different IDs may still refer to the same real place; identity deduplication
at the later Google canonicalization stage remains necessary.

### Exact-search measurements

All measurements use the populated global database, Top-K 10, a single client,
two query intents (English culture and Chinese quiet-indoor), and five warm repeats
per intent. Each table p50/p95 pools those ten SQL execution samples. They exclude
query embedding, network round trips and future Google resolution. First-touch values
show both intents; caches were not flushed and overlapping scopes can warm later
measurements. These small-sample percentiles are diagnostics, not a concurrency SLA
or formal retrieval-quality benchmark. Sydney is not a benchmark destination.

| Destination | Radius km | Geographic rows | After policy | Warm p50 ms | Warm p95 ms | First-touch ms (EN / ZH) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tokyo | 5 | 15,447 | 14,726 | 322.2 | 326.9 | 433.0 / 319.4 |
| Tokyo | 15 | 48,014 | 46,020 | 940.5 | 1013.0 | 1092.4 / 922.4 |
| Tokyo | 30 | 70,870 | 67,797 | 1380.2 | 1501.4 | 1485.4 / 1368.4 |
| Kuala Lumpur | 5 | 3,094 | 2,512 | 32.4 | 34.3 | 72.9 / 33.0 |
| Kuala Lumpur | 15 | 15,524 | 12,873 | 275.8 | 284.1 | 352.1 / 277.3 |
| Kuala Lumpur | 30 | 23,375 | 19,301 | 399.4 | 408.8 | 468.8 / 392.7 |
| Santiago | 5 | 1,903 | 1,617 | 19.9 | 21.0 | 42.4 / 20.4 |
| Santiago | 15 | 2,737 | 2,300 | 25.2 | 27.7 | 38.2 / 26.5 |
| Santiago | 30 | 2,861 | 2,406 | 27.5 | 29.8 | 30.7 / 29.8 |
| Antalya | 5 | 1,807 | 1,488 | 17.6 | 25.7 | 41.3 / 19.5 |
| Antalya | 15 | 2,913 | 2,372 | 27.1 | 30.9 | 42.5 / 29.3 |
| Antalya | 30 | 3,071 | 2,512 | 30.7 | 32.7 | 33.5 / 30.5 |
| Melbourne | 5 | 292 | 284 | 2.8 | 3.4 | 7.1 / 3.3 |
| Melbourne | 15 | 292 | 284 | 2.8 | 3.2 | 3.3 / 2.9 |
| Melbourne | 30 | 292 | 284 | 2.7 | 3.4 | 4.4 / 3.5 |
| Kansas City | 5 | 261 | 247 | 2.5 | 3.0 | 5.5 / 3.7 |
| Kansas City | 15 | 290 | 270 | 2.7 | 3.1 | 3.9 / 3.2 |
| Kansas City | 30 | 290 | 270 | 3.1 | 3.4 | 3.1 / 2.9 |

Tokyo's 15 km first-touch EXPLAIN used bitmap latitude/longitude/country indexes,
produced 48,102 allowed bounding-box rows, reduced them to 46,020 radius-qualified
rows, and performed 46,020 embedding primary-key lookups before cosine sorting and
the final ten metadata lookups. Execution took 1,092.37 ms, with 257,098 shared block
hits and 197,070 reads. Vector access and ranking dominate this dense case; there is
no global 577k-vector scan or ANN approximation. Full JSON plans and client timings
are retained in the ignored validation report.

**Decision: retain exact search for the initial interactive planner.** Medium/low
density scopes take milliseconds to a few hundred milliseconds, while Tokyo 30 km
has warm p95 around 1.50 seconds for SQL alone. This is workable for a small number
of retrieval intents in the current staged planner, but it does not establish a
sub-500 ms or high-concurrency service. If a later measured latency/concurrency budget
cannot tolerate dense-scope cost, separately evaluate filtered ANN against this exact
baseline, checking geographic/policy recall and sufficient results after filtering.
HNSW is not currently implemented or recommended solely due to global corpus size;
any implementation requires separate approval.

### Representative multilingual and lexical results

Both languages can retrieve category-relevant venues, but rankings differ and are
not guaranteed translations of one another. For the culture intent, top results
at the configured 15 km destination scope were:

| Destination | English culture Top-3 | Chinese culture Top-3 |
| --- | --- | --- |
| Tokyo | ESP MUSEUM; WHAT MUSEUM; Bunkamura THE MUSEUM | Bunka Gakuen Costume Museum; National Institutes for Cultural Heritage; Fujifilm Photo History Museum |
| Kuala Lumpur | The National Museum of Malaysia; Muzium Telekom; National Textiles Museum | Lost In Chinatown; BNM Museum and Art Gallery - Museum Cafè; Bank Negara Malaysia Museum and Art Gallery |
| Santiago | Museo de Arte Contemporáneo; Museo de Arte Contemporáneo (MAC); MUI | Museo de Arte Contemporáneo; La Moneda Cultural Center; National Museum of Fine Arts |
| Antalya | Antalya Archaeology Museum; Antalya Culture and Arts; Ataturk House & Museum | Antalya Culture and Arts; Kültür; Antalya Archaeology Museum |
| Melbourne | Immigration Museum; Melbourne Museum; National Gallery of Victoria | Immigration Museum; Melbourne Museum; Royal Exhibition Building |
| Kansas City | American Jazz Museum; Kemper Museum of Contemporary Art; The Nelson-Atkins Museum of Art | Negro Leagues Baseball Museum; National WWI Museum and Memorial; Hallmark Visitors Center |

The Chinese culture query is the `culture.zh` entry in
`data/tripworld/retrieval_queries.v1.json`; the English text is "museums and cultural
attractions". Cross-language results are useful discovery signals, not proof of
travel suitability: the Kuala Lumpur Chinese Top-3 includes a museum cafe, and
Tokyo includes a cultural institution. Sparse Melbourne/Kansas City coverage limits
recall even when SQL is fast. Broader production results need not match the small
Phase 4 sample; the NumPy comparison controls for the same full candidate pool.

Normalized exact lexical lookup maps **State Library Lawn** to **State Library
Victoria** and retrieves **Aqua City Odaiba Shrine** by preferred name, with no
embedding or Google API call. It is intentionally not fuzzy search or score fusion.

### Phase 5 evidence and Phase 6 design boundary

The Phase 5 checkpoint added the PostgreSQL/pgvector service, Docker configuration,
CLI and offline tests without integrating the V0/V1 runtime or candidate funnel.
Local detailed evidence is under `data/tripworld/reports/`: `phase5_google_sanity.json`,
`phase5_ingestion.json`, `phase5_reingestion.json`, `phase5_preflight.json`,
`phase5_embedding_run.json`, `phase5_audit.json`, `phase5_validation.json`,
`phase5_lexical.json` and `phase5_service_smoke.json`. Published aggregate results,
versions, manifests, hashes and tiny fixtures provide context without raw data,
generated vectors or credentials.

At this checkpoint Phase 6 was proposed, not implemented. The intended bridge would
resolve ranked candidates on demand, try Google IDs before name/location fallback,
discard unresolved candidates and continue within a per-trip attempt budget, retaining
provenance and request-scoped reuse. Google-first candidates would not require a
TripWorld match. Cosine similarity remained a discovery signal; neither global-corpus
prevalidation nor direct conversion into Q_rel was approved. Pool size, concurrency,
exact budgets and any score fusion required a separate integration decision. The
later implementation and its bounded evidence are recorded below.

## Implementation checkpoint - 2026-09-19

The user approved Current A-K with a counting correction: scan at most 20 returned
positions, union all valid origins, and charge the six-entity limit only to independent
entities needing new resolution. Existing Google/request-resolved canonical IDs do not
consume that limit or trigger validation Details. Failure consumes an attempted entity;
this is not a six-success target. No source quota, adaptive K or extra retrieval pass.

### Integration and ownership decision

V2 selected its own version/CLI while reusing shared V1 graph/runner functions;
V1 stayed independently Google-only and rejected hidden retrieval injection.
TripWorld discovery entered after named-identity/conflict handling and before factual
admission, preserving final `itinerary_2` and adding separate RAG diagnostics.
The approved counting correction scanned≤20 positions and charged six only to NEW
resolution attempts, including failures; existing canonical observations were free.
No source quota, adaptive K or extra pass was introduced.

The bridge preserved nullable Google rank, source-neutral intent links and canonical
origin union through Details. Compatible early Details shared request-cache results;
budget/dependency/cancellation omissions were not cached as Google identity failures.
Unresolved retrieval degraded independently while original Google planning continued.
Runtime reads verified manifest/artifact/policy/vector-space compatibility, never
migrated or regenerated vectors. Caller cancellation propagated and owned work closed.
Current detailed rules belong in [candidate supply](../../0004-retrieval-persistence%28v2v3%29.md)
and [requirements/evidence](../../0002-requirements-evidence.md).

Historical defaults were 2 queries, K 10,20 positions, 6 new resolutions, 8 Details,
2 fallback searches, 15 km scope/1 km identity tolerance, one embedding batch, 30 seconds phase,
8/3/2/4 seconds embedding/SQL/connect/Google with no retries. Worst-case main+RAG Details 26,
candidate/fallback searches 14 plus destination 1/Nearby 3 were workload ceilings, not prices.
Windows used SelectorEventLoop for psycopg; Proactor-host incompatibility degraded RAG
without a replacement thread/database. This constraint remains operationally relevant.

### Historical recovery baseline (subsequently deleted)

The approved September 20 deletion removed
`D:/Workspace/Capstone/phase6_source_snapshots/20260919T113719Z` and its manifest
SHA256 `c4b0f98cddcd7fa04e8f0571957fb703d1ad6122d44d7e5a6ceae0d64061b257`.
At creation it verified 306 whitelisted source/config files and 11 tracked migration
omissions, excluding secrets/datasets/vectors. The uncommitted intermediate overlay
is no longer recoverable from that snapshot; Git/current artifacts must not be
presented as restoring those exact states.

### Integration verification and incomplete full gate

The full backend invocation stopped during collection with one module-name collision;
no test execution completed, so it was not a full pass. Corrected runner checks passed
14 and refined discovery/graph checks 29. The earlier 91 focused checks and historical
829/9/8 failure checkpoint cannot replace this incomplete full gate.

One authorized read-only PostgreSQL check returned ten Melbourne results within 15 km,
using a hash/model/dimension-verified saved vector. It performed no embedding send,
data write, migration or rebuild. This validates adapter execution, not relevance or
new corpus coverage. No second full backend invocation was made.

Local records: artifacts/validation/rag_integration/{backend_full.txt,runner_affected.txt,
discovery_affected.txt,local_db_readonly.json}. No real Google, embedding or generation
model calls. Unit network safeguards and MockTransport/fake DB/providers were used.

At the September 19 checkpoint, full-backend acceptance remained incomplete despite
the collection correction and passing affected tests. The separately approved September 20
regression below closed that verification gap, without declaring V2 frozen or generally
correct. Remaining technical limits included conservative alias/geography misses, sparse coverage,
no guaranteed net-new/scheduled RAG contribution and possibly paid Details later discarded
by common admission. Nearby does not fix sparse primary itineraries or date coverage.

## Conditional regression and bounded V2 live checkpoint - 2026-09-20

Status: **Full standard backend regression passed; Google-only degradation exercised;
normal RAG integration is NOT live-validated. Not Frozen.**

This checkpoint supplied the full regression and first bounded live evidence missing
from the September 19 checkpoint above. The earlier collection failure remains a failed collection
attempt, not a retrospective green run. No implementation, prompt, configuration,
budget or algorithm changed in this checkpoint. No retry, replacement sample or third run.

### Regression and preflight

One standard `python -m pytest backend/tests -ra --tb=short` execution (with JUnit output):
869 collected, 860 passed, 9 skipped, 0 failed, 0 errors, exit 0, 21.11 seconds.
External network remained blocked by the normal test fixture; TRIPWORLD_TEST_DATABASE=0.
Ruff (`backend scripts`) and git diff --check passed. No repeated full suite.
Nine local PostgreSQL-writing integration tests remained skipped because
`TRIPWORLD_TEST_DATABASE=0`; the normal network-blocking fixture stayed active.
They covered migrations, ingestion/invalidation, exact geo/alias/ties, incompatible
space/stale policy, read-only rejection, rollback, geo boundaries and build resume.

AcceptanceSession capture/resource readiness and RuntimeRetrieval.prepare passed before
paid dispatch. Local compatibility check took 0.043 seconds, with no paid probe, corpus
scan, migration or DB write. Live used the existing AcceptanceSession, real run_v2 and
Windows SelectorEventLoop; product/default engine stayed unchanged. Source/config hashes
were unchanged after both runs. UTC artifact timestamps on September 19 correspond to
September 20 in Australia/Sydney.

### Frozen inputs and identity

Reference date: 2026-09-20. Both requests: planning_request_2, 2026-09-21 through
2026-09-23, three travelers, total-trip budget; final output contract itinerary_2.
Tokyo: Tokyo, Japan; 180000 JPY; exact preferences:
`I definitely want to visit Meiji Jingu. I prefer small museums and places with distinctive local architecture.`
Melbourne: Melbourne, Australia; 1800 AUD; exact preferences:
`I definitely want to visit Queen Victoria Market.`
Both requested V2 and dispatched backend.app.versions.v2.runner.run_v2 once.

- Tokyo request SHA-256: `9c73e491a640eaa3c48723b38ffa3725d18e4dc7572963979e8e28b16e095442`.
- Melbourne request SHA-256: `bfbbdf82910465e38ee833972b0b0265a637b17cd25bd2763f781fd057280928`.
- implementation_hash: `8eefe6c680d11a75e892b9d140ecd417ef858d964126976b7312673dd0d5f368`.
- runtime_config_hash: `20c788ff6457bf7c96bbf7ba68b2508fe833c734ae917a5dd087a6263eb63af8`.
- prompt_files_hash: `86de03ed6f948b87ff55c5899215c365cd86464a96b64b0208c002ae4fb39b5e`.
- schema_files_hash: `4ee5ce9029edeaf73895dc9358c006c146d9f5f7bb18086f1c215066f7f5cbc5`.
- schema_hash: `383b8672557dc3084608ae08b0ef031b2a60d08443caf9a85f995a734e9232c6`.
- Corpus artifact: `a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7`.
- Space: `afa5ba967bb4dbf2978e5a8e99b1f9dca25a4e1e23a4c51f8cfe8572113259ec`; text-embedding-3-small, 1536 dimensions, ENRICHED, normalized cosine.
- Policy: tripworld-production-policy-v1; runtime: tripworld_runtime_1.

### Actual RAG funnel and failure boundaries

Tokyo interpreter produced discovery_1 `places with distinctive local architecture`
(semantic_2) then discovery_2 `small museums` (semantic_1). Both are user-derived queries;
no default or invented preference. Scope: (35.6764225, 139.650027), 15 km, no country filter.
One query embedding batch succeeded (7 prompt/total tokens, 3.088 seconds). Read-only
runtime prepare took 0.030 seconds. The FIRST exact SQL search timed out after 3.001 seconds;
the second was not dispatched. No SQL result set was returned: this is NOT a successful
zero-row query or a measurement of Tokyo corpus coverage. RAG phase took 6.205 seconds.
The existing diagnostic says deadline_limited / TimeoutError; the observed cause is the
3-second SQL suboperation bound, NOT exhaustion of the 30-second phase deadline.

Returned positions, unique entities, cheap entity scan, resolution attempts, incremental
Details/fallback, overlap, new/mixed canonical IDs and every RAG downstream fate count
were zero. Google observations survived unchanged. Its funnel had 41 raw observations,
40 merged identities, 20 admitted, 10 Details-enriched, 8 supplied (1 REQUIRED + 7 OPTIONAL),
7 scheduled. All supply/scheduled identities are Google-only discovery. Extinct Media
Museum was supplied but not scheduled. No RAG-only/mixed admission, enrichment, supply,
scheduled or Nearby-only contribution can be claimed.

Melbourne preference interpretation succeeded, with a REQUIRED Queen Victoria Market and
no DiscoveryIntent. Google performed destination, named-place and two normal default
searches (top attractions/local food). Exact display-name matches included both the market
ChIJsVeQNzRd1moRUNQyBXZWBA8 and transit station ChIJlXQB4zVd1moRA3CXTTHAfB0.
Existing unique-exact-name resolution therefore raised ClarificationRequired:
unresolved_named_identity, before the RAG extension. This was NOT an empty Google response,
a missing REQUIRED preference, or a RAG failure. No RAG query plan, embedding, SQL, supply,
generation or Nearby executed. The intended RAG default branch remains uncovered; no
replacement request or forced resolution was used. No Melbourne itinerary exists.

### Actual Tokyo itinerary and independent references

Times below are actual model output in Tokyo local time (+09:00). No activities were added
by the reviewer. Each main identity is Google-only discovery and belongs to main supply.

| Date | Time | Actual main place | Canonical ID |
| --- | --- | --- | --- |
| 2026-09-21 | 09:00-11:00 | Meiji Jingu | ChIJ5SZMmreMGGARcz8QSTiJyo8 |
| 2026-09-21 | 13:00-15:00 | Samurai Museum TOKYO Shinjuku | ChIJA5gBoXeNGGARJqJqceqLJiQ |
| 2026-09-22 | 10:00-12:00 | Former Prince Asaka Imperial Family Residence | ChIJ41V6qRuLGGAR3hfLAFHax1A |
| 2026-09-22 | 12:10-13:30 | Tokyo Metropolitan Teien Art Museum - Japanese Garden | ChIJ2zLblLSLGGARkGjOdSu0RWY |
| 2026-09-22 | 16:00-17:30 | Japan Traditional Crafts Aoyama Square | ChIJ91khboGMGGARBo42MbnQzg8 |
| 2026-09-23 | 11:00-12:30 | Shinkenchiku-sha Co.,Ltd. Aoyama House | ChIJNZIv-5yMGGARFvzvvuyxaQg |
| 2026-09-23 | 14:00-15:30 | Shinjuku Gyoen Museum | ChIJ5RR13yiNGGART-NAUWZQ2bE |

REQUIRED Meiji Jingu was scheduled. Seven unique linked IDs, zero unlinked activities,
zero repeated canonical visits, no empty day, one unused supplied ID. All seven costs
are null: budget feasibility is not proven. Opening-hour baselines are explicitly qualified
as not proving date-specific exceptions. Weather returned HTTP 404 and was unavailable.
Claims such as small/compact museum suitability remain semantic judgments, not validated
size facts; the wording "measured transfer interval" should not be treated as a verified
route for every transfer. Structural success does not prove all free text or feasibility.

Three actual Nearby searches returned ten results each; three final references, all outside
main supply, not counted as scheduled visits, costs or REQUIRED satisfaction:

| Reference | Scheduled anchor/date | Type | Straight-line distance |
| --- | --- | --- | --- |
| Treasure Hall Lawn | Meiji Jingu / 2026-09-21 | park | approximately 337 m |
| Bikkuri Donkey | Samurai Museum TOKYO Shinjuku / 2026-09-21 | restaurant | approximately 0 m |
| Tokyo Metropolitan Teien Art Museum | Former Prince Asaka Imperial Family Residence / 2026-09-22 | museum | approximately 42 m |

These reasons were application templates from actual Nearby evidence. Source refs in the
raw final artifact are google_places_nearby:<actual-call-id>:<index>. Zero metres is rounded
coordinate distance, not proof of identical identity or zero walking. The museum/reference
and scheduled residence/garden may overlap as a visitor experience despite different IDs;
canonical deduplication does not prove distinct attractions. No live correction was made.
All reasons retain unverified availability/prices/accessibility and straight-line-not-route
uncertainty. IDs/names/addresses came from Google evidence, not model-created sources.

Nearby used the approved 3 requests, 10 candidates/request, 800 m, DISTANCE, mixed four
types, 300 m non-transitive anchor reuse, 10-second phase/4-second request limits, no retry.
The garden reused the residence region. Crafts Aoyama, Aoyama House and Shinjuku Gyoen
Museum anchors were uncovered by the three-region limit. No extra discovery for coverage.
Nearby status completed, 2.5 seconds, three references. Main itinerary fields (including
all dates/times/order/identities/notes/costs) matched the pre-Nearby snapshot exactly:
`a1158e7ead86ea2893e311a44507c572c02df56a7cc04fbe7271a1cda4473c79` before and after (excluding references).

### Calls, usage, capture and uncovered paths

| Work | Tokyo | Melbourne |
| --- | ---: | ---: |
| Requirement HTTP sends / mapped responses | 1 / 1 | 1 / 1 |
| Itinerary HTTP sends / mapped responses | 1 / 1 | 0 |
| Query embedding SDK batch | 1 | 0 |
| SQL retrieval attempts / completed result sets | 1 / 0 | 0 / 0 |
| Google destination / candidate searches | 1 / 3 | 1 / 3 |
| Main Details / Reviews | 10 / 0 | 0 / 0 |
| RAG incremental Details / fallback | 0 / 0 | 0 / 0 |
| Weather sends | 1 (404) | 0 |
| Routes requests / requested matrix elements | 4 / 72 | 0 / 0 |
| Nearby sends / cache hits | 3 / 0 | 0 / 0 |
| Profile / evaluator / Official Web reasoning / Web/page | 0 | 0 |

Routes comprised baseline 64 elements and eight alternative elements over three additional
requests. Provider workload is not an invoice. No second interpreter, repaired generation,
planner rerun, hidden harness retry, or reference model call was introduced.

| Model task (gpt-5.6-luna) | Input | Output (includes reasoning) | Reasoning | Cached input | Cache write | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tokyo requirement | 3939 | 652 | 324 | 0 | 3936 | 4591 |
| Tokyo itinerary | 20323 | 1920 | 516 | 0 | 20320 | 22243 |
| Melbourne requirement | 3928 | 145 | 46 | 3807 | 118 | 4073 |

Embedding usage is separately 7 prompt/total tokens; do not add reasoning/cache again.
Provider-reported model durations: 6, 14 and 2 seconds respectively (integer timestamps).
Tokyo main completion: 44.316 seconds; RAG included therein: 6.205; Nearby: 2.5;
total: 46.836. Melbourne total: 5.455 seconds, failed before generation.

Model SDK/HTTP/domain and Google transport captures were preserved with unique call/attempt
IDs. Session closed its owned client once; capture_errors empty; both file tracers healthy.
A measurement limitation remains: the scoped generic HTTP observer did not intercept the
embedding client's transport. Its successful single SDK batch, usage, timing and configured
zero retries are captured, but independent embedding HTTP-send count is UNKNOWN, not a
claimed measured one. This gap does not justify repeating the paid operation.

Observed request caches had no hits; RAG Details reuse/overlap/free merge/negative-cache
boundaries were not live exercised. Offline tests, not these samples, cover them. SQL timeout
returned control with no subsequent SQL dispatch; user cancellation was not exercised.
Normal SQL completion, identity fallback, RAG source union, admission field parity with
RAG Details, RAG supply/scheduled contribution, default RAG query, and reference failure
isolation remain unexercised by this live pair. No live faults were injected.

At this checkpoint only Google-only degradation had end-to-end live evidence;
normal RAG remained unvalidated. The later SQL and identity investigations below
were separate from this failed normal-path coverage, not replacement samples.

Artifacts are ignored under logs/phase6_acceptance_20260920: manifest, regression/JUnit,
preflight, per-case results, raw session calls/events, traces and analysis.json. The original
external source snapshot was unchanged during that checkpoint; it was subsequently deleted
by user authorization and is not a current recovery entry. No corpus/vector/DB write, frontend/default
change, B2 cleanup, stage/commit/push, re-freeze or V3 work. This is development evidence,
not a formal V1/V2 comparison or complete correctness proof.

## Runtime observations and storage decision - 2026-09-20

Status: Local observation repair implemented and offline checked. Decision **B**: proceed
only with a separately approved storage-layout experiment; no production SQL/performance
change, timeout increase or normal V2 live acceptance is claimed.

### Preserved baseline and implemented observations

The original Tokyo vectors are still missing. The museums/cultural checkpoint remains a
compatible performance control, not exact semantic replay. Earlier observations include
1.130-second completion and 15-second timeouts at execute; fetch/decode was negligible
when reached, and the original 30-second phase was not exhausted. Melbourne remains a
pre-RAG named-identity clarification. The prior 860-pass/9-skip full suite remains historical
and was not repeated in this telemetry task.

RuntimeRetrieval now records metadata-only timings for prepare, connection, compatibility,
embedding, SQL, execute and fetch/decode. Errors retain exception type and PostgreSQL
SQLSTATE when exposed; absent SQLSTATE stays unknown. The existing SQL timeout context
is retained at the same location/value; its expired() value is observed after exit.
TripWorldDiscovery retains existing status/degradation behavior and adds timeout_scope and
phase_deadline_expired. Caller cancellation is recorded and immediately re-raised; no retry,
replacement query, negative-cache or background-task behavior was added. This touched the
execution/cancellation call sites for measurement, so adapter, service cancellation and V2
runner tests were included; it is not hidden as an unrelated logging-only change.

Embedding request/response hooks attach to the actual owned SDK HTTP client, including the
installed httpx2 path. Hooks record unique attempt IDs, status and request IDs, without
headers, credentials or raw inputs. No global send/close replacement. Hooks are removed
before normal owned-client closure. embedding_sends continues to count SDK batch attempts;
embedding_http_attempts records real HTTP attempts separately. SDK usage is captured once
before subsequent domain validation; status/request metadata survives malformed JSON or
model mismatch. Usage is not reconstructed from HTTP layers or counted twice. Historical
HTTP-send counts remain UNKNOWN, not retroactively repaired.

Full query vectors are saved ONLY when a development caller explicitly passes
`capture_directory=Path("logs/<development-session>/query_vectors")` to RuntimeRetrieval,
for example through the existing V2 retrieval_factory injection. Default is None; no runtime
configuration/prompt/CLI default was changed. Each opt-in NPZ includes float32 normalized
vectors, shape/dtype, corpus artifact, full space/space ID, per-input text SHA-256 and vector
SHA-256. Raw query text is not written by this capture; text hashes link to separately
approved input capture. Capture failure records a diagnostic and does not fail a successful
embedding result. Capture success is not permission to commit vectors or private artifacts.

### Actual local structure and resource evidence

New bounded read-only catalog checks used the current local PostgreSQL and existing adapter.
Artifacts: artifacts/diagnostics/retrieval_storage/{structure,storage_details,decision}.json.
No vector search, EXPLAIN ANALYZE, provider/model call, schema write or maintenance occurred.
Existing executed plans from the preceding eight-query diagnosis were reused.

| Item | Observation |
|---|---|
| PostgreSQL / pgvector | 17.10 / 0.8.2 |
| embedding storage | attstorage=e (EXTERNAL); sampled pg_stats avg_width=18 |
| Embeddings main heap | 673,808,384 bytes |
| Embeddings ordinary indexes | 180,748,288 bytes |
| Embeddings TOAST heap / TOAST index | 4,726,874,112 / 52,142,080 bytes |
| Embeddings total relation | 5,635,112,960 bytes |
| Entities main heap / total | 1,064,026,112 / 1,615,937,536 bytes |
| shared_buffers / work_mem | 128 MiB / 4 MiB |
| track_io_timing | off; no per-read physical latency attribution available |
| Statistics | embedding analyze 2026-09-18 07:59 UTC; entities 08:08 UTC; not refreshed |

The embeddings table also carries space/text/vector hashes and generation metadata
(avg_width 885); the 18-byte vector width and 4.73 GB TOAST heap support widespread out-of-line
vectors. EXTERNAL policy alone would not prove every row is out-of-line. TOAST size contains
actual vector data, not 4.73 GB of pure overhead. Cumulative table I/O counters were captured,
but are not this query's deltas. Shared reads can hit OS cache. Parent/child EXPLAIN buffers
are not summed. The existing Tokyo plan performs 44,440 vector lookups and only ten final
entity payload fetches, with cardinality underestimation and 706 temporary blocks written.

Read-only Docker inspection:
container reliable-tripworld-postgres-1, pgvector/pgvector:0.8.2-pg17. HostConfig Memory and
MemorySwap are 0; cgroup memory.max and swap.max are max (no container-specific limit).
Docker stats reported 153.7 MiB / 11.68 GiB; an independent cgroup snapshot reported
171,991,040 memory bytes and ZERO current swap bytes. Container-visible MemTotal was
12,249,312 kB and MemAvailable 11,182,668 kB. These are snapshots, not per-query synchronized
measurements or host physical memory assumptions. They do not demonstrate current memory
pressure. Data uses Docker named volume reliable-tripworld_tripworld_pgdata at
/var/lib/docker/volumes/reliable-tripworld_tripworld_pgdata/_data, mounted on
/var/lib/postgresql/data; it is NOT a Windows-path bind mount. Docker's backing-disk physical
read latency is not established by these observations.

### Candidate selection and bounded experiment stop

The authorized early-stop condition was used: no SQL/session-only candidate had evidence
that it would remove the dominant per-vector out-of-line access. Increasing work_mem could
remove a roughly 5.5 MiB CTE spill, but would leave 44,440 embedding lookups and TOAST reads.
The query already defers full entity metadata until Top-K. Removing materialization without
a demonstrated plan benefit could introduce recomputation instead. No arbitrary rewrite or
work_mem/parallel/cache combination was tested just to fill the query allowance.

| New experiment category | Executions | Result/equivalence |
|---|---:|---|
| A original normal SELECT | 0 | Not executed this task |
| B alternative normal SELECT | 0 | No supported SQL/session candidate selected |
| EXPLAIN ANALYZE | 0 | Prior actual plans reused |
| Ordered-ID/score comparison | 0 | No new real-data equivalence or speedup claim |

This is not an A-B-B-A result, not evidence that a tested rewrite failed, and not a p95/SLA
measurement. It is the explicitly allowed evidence-based decision to stop before an
unjustified low-risk rewrite. The new task used 0 of 4 normal and 0 of 2 analyzed searches;
no prior eight executions were relabeled as new comparisons. No production timeout change:
15 seconds per query would not leave adequate time for two queries plus embedding and
Google resolution inside 30 seconds, and prior 15-second failures remain unexplained in
full detail. Larger timeout alone is not a completed performance repair.

### Decision B: one preferred approval item, inline-vector shadow storage

Prefer a controlled storage-layout experiment before an ANN semantic change or resource
expansion. Its SINGLE primary variable is embedding inline versus current EXTERNAL storage.
Create a separately named shadow copy of the embeddings table with vector(1536) PLAIN
storage set BEFORE copying; retain the same columns, key/index definitions, space and
existing vector bytes. Only the diagnostic query's relation name changes between copies.
No embedding regeneration, dimension change, candidate truncation or new index algorithm.

Why this target: inline vectors can remove separate TOAST lookup/chunk access for each
exact comparison. This directly addresses observed work, unlike raising timeout or only
removing CTE spill. It may increase main-heap pages and cache pressure, so improvement is a
hypothesis, NOT established. Row-size compatibility and treatment of other variable-width
columns must be checked during construction; preserve their values and integrity.

Costs and recovery: this requires a full copy/write of approximately 577k existing vector
rows, ordinary duplicate indexes and WAL; it is NOT a metadata-only ALTER. Merely changing
SET STORAGE on the existing column would not retroactively inline the stored vectors.
Budget roughly 5-6 GB for the shadow plus WAL/temporary headroom; require at least 12 GB free
before starting as an engineering guard, then monitor actual growth and stop at an approved
space bound. This estimate is not a measured final table size. No Docker/PostgreSQL restart
is inherent. Original table, IDs, corpus manifests, query SQL and runtime remain untouched
as the recoverable baseline; do not cut over or drop originals during the experiment.

The proposed experiment was not executed or promoted. Its gate required copied
text/vector/eligibility integrity, same vector/Tokyo/K/cosine/tie order, bounded
A-B-B-A plus one plan/layout (≤15 seconds each), ordered-ID/score equivalence within
1e-6, reduced vector-fetch I/O and repeat benefit. Four timings would not establish SLA.
Production cutover/rollback and any later live acceptance remained separate decisions.

Melbourne's market/station ambiguity remains an independent shared identity limitation.
No named-role field, Requirement prompt change, rank shortcut or REQUIRED bypass was made.
No HNSW/IVFFlat, index build, table copy, SET STORAGE, global setting, memory expansion,
restart, maintenance ANALYZE/VACUUM, cache flush or full-corpus warmup was performed.

### Validation and changed files

Telemetry changed runtime/diagnostics and additive discovery report wiring, with
adapter, cancellation, capture and V2/AcceptanceSession coverage. It added no retry
or selection/source-policy change.

Initial affected runtime/diagnostic/service/V2-runner/AcceptanceSession set: 57 passed.
Additional real-stack tests initially yielded 10 passed/1 failed because malformed-JSON
fixture omitted application/json and the SDK legitimately returned text. Correcting the
fixture (not production parsing policy) yielded 11 passed. Subsequent embedding cancellation
and phase assertions: 29 passed across runtime/service; final SQL-vs-phase test brought the
service module to 17 passed. These are overlapping checks, not additive full-suite counts.
Ruff and git diff --check passed. No full backend repeat; earlier full regression stands.

Coverage includes owned httpx2 sends, zero SDK retries on 429, malformed response metadata,
usage before domain validation, capture off/on same input/result, integrity hashes, capture
write failure isolation, SQL timeout versus caller cancellation, embedding timeout/cancel,
phase expiration, unchanged Google degradation and resource closure. No actual embedding
was obtained. No source-policy, selection, generation, frontend, default engine, B2, database,
commit/push, re-freeze or V3 change. Normal RAG live remains unvalidated.

### Evidence and reproducibility limits

Used logs/phase6_acceptance_20260920/{manifest,session_events,session_calls,tokyo_result,
melbourne_result,analysis}.json and both original trace directories. The Tokyo plan,
query texts, embedding usage and runtime errors exist; the embedding response vectors
were NOT saved. Runtime RequestCache was in memory and is no longer available. Therefore
none of these measurements is an exact replay of either Tokyo semantic query.

Substitute: the previously saved Phase 5 query `museums and cultural attractions`, checkpoint
d5d9797ff9d60b621f77122755339422df25db54a7bb97089f9b195b401602d2.npz.
phase5_service_smoke.json links that text/checkpoint/space. Validated finite float32 shape
(1,1536), unit norm, response model text-embedding-3-small and vector-byte SHA-256
97988b6ac1c3a4c0e9055f331729491c9464843803f49ea3ef94935f99d2402b.
Runtime.prepare checked the actual artifact, manifest, production policy and embedding space.
No new embedding request. Source/parameter/checksum manifest is saved in
artifacts/diagnostics/retrieval_execution/diagnostic_manifest.json.

Tokyo used the captured center (35.6764225,139.650027), 15 km, K=10, country=null.
Melbourne component control used (-37.8136276,144.96305759999998), same radius/K/vector/space.
It did not bypass REQUIRED to run the planner and is not Melbourne end-to-end success.
All connections were read-only and loopback; no corpus export, maintenance, schema/index
change, cache flush, service restart or resource change. Original live artifacts remain intact.

### Exact timing boundary and observed cancellation

Runtime.prepare has separate connection (2 seconds) and compatibility SQL (3 seconds)
bounds. The connection is autocommit with default_transaction_read_only=on and a server
statement_timeout. Runtime.search wraps BOTH `await conn.execute` and `await cursor.fetchall`
in the client SQL timeout. Query construction/vector validation happens before that wrapper;
artifact checking and ranked domain dictionaries happen after it. execute includes server
execution and libpq result receipt; fetchall performs row decoding. It is not correct to
label all execute time as CPU, or to infer the original live fetch stage from its old trace.

All diagnostic timeouts occurred before execute returned; fetchall/domain mapping did not
start. Completed Tokyo normal fetch/decode was 0.000219 seconds; Melbourne 0.000307 seconds.
Compatibility/connection succeeded separately. Client exception chains on attempts 1/6/8
were TimeoutError -> CancelledError, with no surfaced PostgreSQL SQLSTATE. Attempt 2 surfaced
psycopg QueryCanceled, SQLSTATE 57014, consistent with the configured 15-second server limit
winning the race. 57014 alone does not identify every possible cancellation cause; the script
saved structured types/code, not server diagnostic message_primary. The original live did
not capture that code or cancellation detail, so its exact server/client race remains unknown.

After every executed search, transaction status was IDLE, a SELECT 1 probe succeeded, and
the owned connection closed normally. No background search or retry was scheduled. User
cancellation was not injected. Monitors were read-only and canceled/awaited in cleanup.
The live RAG elapsed 6.205 seconds remains a SQL-suboperation timeout, not an exhausted
30-second phase. Its current deadline_limited status conflates these two cases.

### Eight-search execution ledger

No more retrieval executions were performed after number 8. Plain EXPLAIN, settings/index/
statistics reads and bounded pg_stat_activity samples were not retrieval executions. Each row
used a new connection, NOT a claimed cold cache. Earlier partial/failed reads can warm later
runs; EXPLAIN ANALYZE overhead and omitted result transfer differ from ordinary queries.

| # | Center | Operation | Client/server bound | Client seconds | Outcome |
|---|---|---|---|---:|---|
| 1 | Tokyo | Actual RuntimeRetrieval.search | 3 s / 3 s | 3.024 | client TimeoutError, execute unfinished |
| 2 | Tokyo | Same SELECT | 15 s / 15 s | 14.961 | QueryCanceled, SQLSTATE 57014 |
| 3 | Tokyo | EXPLAIN ANALYZE BUFFERS | 15 s / 15 s | 3.325 | completed; server execution 3327.875 ms |
| 4 | Tokyo | Same SELECT, repeated | 15 s / 15 s | 1.130 | 10 rows; fetch/decode 0.000219 s |
| 5 | Melbourne | Actual RuntimeRetrieval.search | 3 s / 3 s | 0.0176 | 10 rows |
| 6 | Tokyo | Actual RuntimeRetrieval.search, repeated | 3 s / 3 s | 2.994 | client TimeoutError |
| 7 | Melbourne | EXPLAIN ANALYZE BUFFERS | 15 s / 15 s | 0.1128 | completed; server execution 106.363 ms |
| 8 | Tokyo | EXPLAIN ANALYZE BUFFERS, repeated | 15 s / 15 s | 15.005 | client TimeoutError |

Small overrun beyond a timeout includes cancellation/cleanup scheduling, not another search.
No consistent cold/warm latency claim or percentile estimate is justified. In particular,
number 4 does not establish reliable sub-three-second Tokyo execution.

### SQL and plan findings; historical comparison

The exact parameterized SQL is saved with each measurement. Its execution structure is:

1. Materialized geographic CTE: discovery_allowed plus latitude/longitude bounding box;
   runtime also applies exact production policy_version and artifact_hash.
2. Great-circle radius <=15 km +1e-9; join embeddings by text_hash AND space_id.
3. Exact `1 - (embedding <=> query_vector)` per eligible entity; descending similarity,
   entity ID COLLATE C tie-break, LIMIT 10 in materialized ranked CTE.
4. Fetch entity metadata by primary key for ONLY the ten winners; final stable sort.

There is no pre-Top-K loading of full entity metadata in the SQL projection. The physical
entity heap still occupies many pages; projection alone does not make those pages narrow.
Existing indexes include latitude/longitude B-trees, entities primary key and embeddings
(space_id,text_hash) primary key. No ANN/PostGIS was used or proposed as this diagnosis.

Completed Tokyo plan: bitmap intersection -> entities heap -> materialized geographic ->
44,440 embedding primary-key probes/cosine evaluations -> top-N heapsort -> 10 entity lookups.
Geographic eligible rectangle: 47,185 actual vs 6,711 estimated rows; circle leaves 44,440
vs 2,237 estimated. Geographic heap stage took 334.665 ms; ranked input completed around
3310.355 ms. Top-N sort used 26 kB. Final payload lookup loops=10, not 44,440.
Root totals: 249,662 shared hits, 189,498 shared reads, 706 temp blocks written, zero temp
blocks read. Do not add cumulative child counters to these totals. Shared reads are
PostgreSQL buffer misses and may still hit OS cache; they do NOT prove physical disk reads.
The geographic CTE spilled approximately 5.5 MiB at the observed 4 MiB work_mem.
Shared buffers were 128 MiB. Existing statistics were present, not refreshed by this task.

Completed Melbourne plan: 284 geographic/circle rows (estimate 1), no temp spill; 2,118 shared
hits and 800 reads. This independently confirms that the runtime adapter can return ten
results from a lower-density scope with the saved vector.

Wait samples: number 4 saw six IO/DataFileRead and four active/no-wait samples; number 6 saw
25 DataFileRead and three active/no-wait; number 8 saw 116 DataFileRead, six DataFilePrefetch,
14 active/no-wait and one ClientRead sample. All sampled blocker lists were empty. Early
attempts 1-3 were not sampled. This supports I/O-sensitive high-density exact retrieval,
not demonstrated lock contention, result decoding, or a phase deadline failure. It does not
pin the original live stall to a specific host/Docker/disk event or prove no transient lock
could ever have occurred. Underestimation and CTE spill are secondary efficiency concerns;
this evidence does not prove fixing either alone removes the latency variation.

Phase 5 and runtime call the SAME search_query builder. Runtime adds only the policy/artifact
predicates, bounded async execution and post-fetch compatibility/rank construction; no new
join or early payload projection. Applying identical data conditions to the historical
builder produces byte-identical SQL (verified offline and hashed). Removing these conditions
would change the eligible universe, so no misleading unrestricted-old-vs-restricted-new
latency comparison was run. Prior historical Melbourne latency is not a Tokyo baseline.
No alternative SQL rewrite was executed: current evidence does not justify selecting one
as a proven repair within the eight-execution cap. Same-query successful repetitions are
performance observations, not a claim that original Tokyo vector identities were replayed.

### Melbourne identity evidence and replay

Original named intent is REQUIRED with place_text Queen Victoria Market and a valid source
span. NamedRequirementDraft/NamedRequirement and the bridged NamedPlaceIntent have no target
role/type constraint. The source text is only the proper name, not an explicit market-vs-
station clarification. No role can be mechanically recovered by matching words in that name.

| Candidate | Actual primaryType | Coordinates | Source / rank (one-based) |
| --- | --- | --- | --- |
| ChIJsVeQNzRd1moRUNQyBXZWBA8 | market | -37.8075798,144.956785 | named search / 1 |
| ChIJlXQB4zVd1moRA3CXTTHAfB0 | transit_station | -37.8094414,144.955869 | same named search / 8 |

Both names are exactly Queen Victoria Market and both statuses OPERATIONAL. Market address
is Queen St, Melbourne VIC 3000; station address Melbourne VIC 3000. Neither exact-name
candidate appeared in the saved default top-attractions/local-food responses. Thus these
sources do not provide independent corroboration selecting one identity. Provider rank is
not an identity guarantee; both positions are plausible within the same destination.

Offline replay of the exact-name subset through current merge/resolver produced
ambiguous_exact_name with both IDs. Type, coordinates and QueryIntentHit provenance survived
merge; they were NOT lost by mapping. Resolver builds a normalized-name -> ID-set and
accepts exactly one ID. It does not use types/position/rank to break this ambiguity. This
is conservative behavior, not automatically a bug: provider types distinguish the objects,
but the current user contract does not tell code which role to require.

The recommended minimal future extension was a nullable source-grounded
`expected_primary_type`, interpreted only from explicit user role wording. Market
versus station could then filter known incompatible types; two plausible markets,
missing competing types or no explicit role would still clarify. No provider rank,
proper-name suffix, model world knowledge or REQUIRED bypass could manufacture
uniqueness. This extension was Proposed, not implemented by this diagnosis.

### Embedding observer diagnosis and proposed local fix

The installed default AsyncOpenAI client is AsyncHttpxClientWrapper whose send method is
httpx2._client.AsyncClient.send. The live observer patched httpx.AsyncClient.send, so it
captured Google but not that default embedding transport. Existing AcceptanceSession
explicitly owns its model client and its own hooks, explaining why model HTTP counts worked.
SDK batch success and usage remain valid; historical independent embedding HTTP count stays
UNKNOWN. Do not rewrite it to zero or an inferred one.

The proposed scoped hooks on the actual owned SDK client were later implemented in
the telemetry stage above. Offline MockTransport demonstrated httpx 2 observation
where the generic httpx patch missed sends. Historical independent embedding HTTP
counts remain UNKNOWN; later instrumentation cannot reconstruct them.

<a id="m-6d53b29b6f5c"></a>
## Development waiting override and conditional normal RAG live - 2026-09-20

Status: **Normal V2 RAG discovery/resolution/supply/scheduling has bounded development-live
 evidence under the explicit 60/180-second override. Not a production SLA or re-freeze.**

The user deferred inline/PLAIN shadow tables and storage copying to prioritize functional
validation of the original tables and exact SQL. Historical 3/30-second failures, 1.13-second
success/15-second timeout variation, and EXTERNAL/TOAST findings remain valid. This task
changed waiting budgets only for explicitly opted-in V2 development calls. It did not
perform a database performance optimization or establish production latency guarantees.

### Minimal override and effective timeout stack

config/v2_development_override.json contains ONLY sql_timeout=60 and deadline_seconds=180.
versions/v2/config.py now permits those upper bounds while defaults remain SQL=3/phase=30.
load_development_override(path, base) rejects other keys and validates against RAGConfig;
it returns a new config without mutating shared runtime defaults. Existing run_v2 rag_config
and retrieval_factory injection are used. No destination-name condition, parallel config
framework, V0/V1 override or offline corpus-build configuration change was introduced.

The opt-in override used existing V2 injection rather than changing CLI/default behavior.

| Boundary | Historical/default | This development validation |
| --- | ---: | ---: |
| PostgreSQL session statement_timeout | 3000 ms | 60000 ms (SHOW returned 1min) |
| Application SQL execute/fetch | 3 seconds | 60 seconds |
| Entire RAG phase | 30 seconds | 180 seconds |
| Development whole-run bound | no AcceptanceSession global bound | explicit 360 seconds |
| Embedding / connect / Google suboperations | 8 / 2 / 4 seconds | unchanged |

The enclosing phase clipped SQL to remaining time and canceled/awaited work and cleanup.
Per-connection server settings and embedding/connect/Google bounds stayed unchanged.
Work ceilings stayed two queries, one embedding batch, K=10,20 returned positions,
six new-resolution attempts (including failures), eight incremental Details, two fallback
searches and zero retries. SQL, corpus, geographic/identity/selection policies and prompts
were unchanged; this was waiting-budget validation rather than performance optimization.

### Offline gate and two local SELECTs

Affected configuration/runtime/deadline/service/V2-runner/AcceptanceSession tests:
**94 passed in 15.53 seconds**, exit 0. Ruff and diff checks passed. Tests confirm effective
60000 ms session timeout, immutable defaults/work ceilings, actual V2 config dispatch,
phase/caller cancellation, ownership, cache and failure distinctions. Unit tests did not wait
60/180 seconds. No new failures or fixes between the gate and paid execution; no full suite
repeat. The prior full 860 passed/9 skipped remains separate historical evidence.

Both local requests used actual RuntimeRetrieval, original SQL, fresh RequestCache, the
previously validated museums/cultural vector and Tokyo (35.6764225,139.650027), 15 km, K=10.
Original Tokyo vectors are still absent; these two SELECTs are compatibility/performance
controls, not an exact replay of the old semantic request. Each independently had 180-second
outer boundary, SQL=60, read_only=on and cache_hit=false. No database/OS cache flush or warmup.

| Local execution | Execute | Fetch/decode | Query total | Whole local check | Result |
|---|---:|---:|---:|---:|---|
| First | 23.914363 s | 0.000227 s | 23.914825 s | 23.971042 s | 10 valid rows |
| Repeat | 0.962450 s | 0.000223 s | 0.962881 s | 1.008015 s | 10 valid rows |

Entity schemas/artifact/coordinates/scores passed integrity checks. Ordered IDs matched
exactly, scores matched with rtol=0/atol=1e-6; complete IDs/scores are in local_results.json.
Both transactions ended IDLE and connections closed; neither timed out or reported SQLSTATE.
These are first/repeated observations, not controlled cold/warm measurements. Exactly two
local retrieval executions, no third or extra EXPLAIN. Both gates passed, authorizing the
single fresh Tokyo live without another approval prompt.

### Frozen fresh Tokyo dispatch

Actual runner backend.app.versions.v2.runner.run_v2; existing AcceptanceSession and Windows
SelectorEventLoop. input=planning_request_2, output=itinerary_2. Trusted reference date
2026-09-20; trip 2026-09-21 through 2026-09-23, Tokyo, Japan, three travelers, total 180000 JPY.
Exact additional_preferences:
`I definitely want to visit Meiji Jingu. I prefer small museums and places with distinctive local architecture.`

- request_hash: `9c73e491a640eaa3c48723b38ffa3725d18e4dc7572963979e8e28b16e095442`.
- implementation_hash: `6a20a9fc859117d497c8434ae45c7a4e9273ca5d682b711051b33dadb66797bb`.
- runtime_config_hash: `34f05980dba254106e47dc70b3b0c7e7b2f55b0005cc5566602b7de00bc39fd8`.
- prompt_files_hash: `86de03ed6f948b87ff55c5899215c365cd86464a96b64b0208c002ae4fb39b5e`.
- schema_files_hash: `4ee5ce9029edeaf73895dc9358c006c146d9f5f7bb18086f1c215066f7f5cbc5`.
- corpus_manifest_hash: `ac9d7cc8c0b28cbc3ad3913ed6921f67342fbe662f08a768098745e9dd30b349`.
- artifact_hash: `a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7`.

Effective configuration and old/new values are frozen in effective_config.json/live_manifest.json.
No source/config changed between freezing and completion. Query vectors came from this
fresh interpretation and real embedding call, NOT the diagnostic vector. One opt-in NPZ
contains both actual 1536-dimensional normalized vectors; vector checksum, text hashes in
actual query order, space and shape were verified offline. The earlier missing capture is
not rewritten as available. Credentials were not added to captures or documents.

### Actual query-to-itinerary funnel

Both queries were user-derived: discovery_1 `places with distinctive local architecture`
linked to semantic_1, and discovery_2 `small museums` linked to semantic_2. One embedding
batch/one observed HTTP attempt (200), seven prompt/total tokens. Runtime prepare 0.056743 s;
embedding 2.592 s. SQL 1 execute/fetch: 23.297610 / 0.000238 s; SQL 2: 0.884878 / 0.000352 s.
Two successful result sets, ten positions each, 20 distinct entities, no Google overlap.

Six direct-ID resolution attempts all succeeded, six incremental Details HTTP sends, zero
fallback, zero RAG cache hits. Fourteen remaining entities were marked entity_budget, not
invalid/failed/attempted. Status partial therefore records bounded processing, not failed SQL
or Google-only degradation. Canonical union added six net-new Google-backed identities;
Google used for identity resolution does not make them Google-discovered.

| New RAG-only candidate | Admission / subsequent outcome |
|---|---|
| Beni Museum | admitted; normal enrichment reused cached Details; supplied and scheduled |
| Min-on Music Museum | admitted; normal enrichment capacity not attempted |
| Wakayama Domain Kii Family Mansion Remains | admitted; normal enrichment capacity not attempted |
| Remains of Kirishitan Yashiki | admission capacity omission |
| Fushimi-yagura | admission capacity omission |
| The National Museum of the Imperial Collections, Sannomaru Shozokan | admission capacity omission |

All six had resolution Details, but only ONE reached the normal enrichment stage under its
existing bounded processing order; these are different stage counts. RAG fate: 3 admitted,
1 normally enriched, 1 supplied, 1 scheduled, zero mixed identities. One compatible Details
cache hit avoided re-fetching Beni Museum. Mixed-source overlap and fallback remain live
uncovered; no source boost or guaranteed RAG quota was used.

Main supply: 8 identities (1 REQUIRED +7 OPTIONAL), comprising 7 Google-only and 1 RAG-only.
Scheduled: 5 unique canonical IDs (4 Google-only, 1 RAG-only, 0 mixed). REQUIRED Meiji Jingu
scheduled; zero unlinked activities, zero unscheduled REQUIRED. The three supplied-but-not-
scheduled Google-only places were Aoyama House, Japan Traditional Crafts Aoyama Square and
Shinjuku Gyoen Museum. No comparison to prior itinerary length is a formal quality result.

### Actual generated itinerary and application references

Times are actual Tokyo local (+09:00) output. No activity was added by the reviewer.

| Date | Time | Main place | Discovery source |
| --- | --- | --- | --- |
| 2026-09-21 | 09:30-12:00 | Meiji Jingu | Google-only |
| 2026-09-22 | 10:30-12:30 | Former Prince Asaka Imperial Family Residence | Google-only |
| 2026-09-22 | 13:00-14:30 | Tokyo Metropolitan Teien Art Museum - Japanese Garden | Google-only |
| 2026-09-23 | 10:30-12:00 | Beni Museum | RAG-only |
| 2026-09-23 | 15:00-17:00 | Extinct Media Museum | Google-only |

Main notes retain unknown date-specific opening exceptions and required-visit access.
The garden transfer references supplied 107 m/85-second matched route evidence. Beni to
Extinct Media Museum lacks a usable transit alternative measurement and requires flexible
transport/feasibility confirmation. All five costs are null; budget feasibility is unproven.
The first day contains one main visit, not a filled whole day. No activity-density repair or
new validator was introduced. Weather again returned HTTP 404; that separate issue persists.

Nearby separately made three successful searches and appended three references:
Treasure Hall Lawn near Meiji Jingu (September 21, park, approximately 337 m straight-line);
Tokyo Metropolitan Teien Art Museum near Former Prince Asaka Residence (September 22,
museum, approximately 42 m); and restaurant ChIJczW5NmSLGGARJZLLuwItUyI near Beni Museum
(September 23, approximately 26 m; original Japanese display name retained in raw output).
All are outside the main supply and backed by actual Nearby source refs. None counts as
scheduled, budget expenditure or RAG main-candidate contribution. Application reasons retain
unverified availability/prices/accessibility and straight-line-not-walking uncertainty.
Canonical deduplication does not establish separate visitor experiences for residence/garden/
museum identities. Main business fields before/after Nearby compared equal.

### Calls, usage, elapsed time and acceptance limits

| Actual work | Count |
| --- | ---: |
| Requirement model / itinerary model HTTP | 1 / 1 |
| Query embedding SDK batch / actual HTTP | 1 / 1 |
| SQL attempts / completed sets | 2 / 2 |
| Main destination / candidate searches | 1 / 3 |
| RAG incremental Details / fallback | 6 / 0 |
| Main Details HTTP / compatible cache hit | 9 / 1 |
| Total Details HTTP | 15 |
| Reviews / Profile / evaluator | 0 / 0 / 0 |
| Weather | 1 (404) |
| Routes requests / matrix elements | 4 / 72 (64 baseline +8 alternative) |
| Nearby HTTP / cache hit | 3 / 0 |
| Official Web / page / reasoning | 0 / 0 / 0 |

Longer waiting did not add work ceilings or retries, but six RAG identity Details calls now
actually occurred. This is not zero incremental Google cost. The one cached re-use means
normal enrichment attempted ten places while issuing nine new Details sends. Counts are
actual workload, not invoices. One fresh planner and one interpretation; no paid replacement.

| Model task (gpt-5.6-luna) | Input | Output | Included reasoning | Cached input | Cache write | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Requirement | 3939 | 856 | 513 | 0 | 3936 | 4795 |
| Itinerary | 20183 | 1735 | 741 | 0 | 20180 | 21918 |

Embedding seven tokens is separate. Reasoning/cache are not added again to reported totals.
RAG phase: 30.619 s (embedding 2.592, retrieval 24.184, resolution 3.693).
Main itinerary completion: 68.185 s; Nearby: 2.844 s; total fresh request: 71.052 s.
The 60/180/360 limits are development ceilings, not measured target latency or production SLA.
No SQL/phase timeout occurred. Actual reads continue to show large first/repeat variation;
TOAST/storage diagnosis is not invalidated and no performance optimization was performed.

Session capture_errors empty, tracer healthy, owned model client closed once, runtime DB
connection closed; vectors verified and sources unchanged. No retry, supplemental search,
second live, Melbourne run or post-hoc output editing. Failure branches were not injected;
new default/mixed/fallback destinations and broad correctness remain outside this smoke.

Functional conclusion: the original exact SQL/tables can support normal bounded V2 retrieval,
Google-backed canonical integration and a scheduled RAG-only POI under a reasonable explicit
development waiting allowance. This is stronger than the prior Google-only fallback evidence,
but only one fresh live and not a formal benchmark or complete version freeze.

The normal-path checkpoint left latency unresolved and kept 60/180 explicitly opt-in.
Inline/PLAIN storage work was deferred, not rejected. Melbourne identity ambiguity
remained separate. Evidence: `logs/phase6_development_window_20260920`.

## Historical RAG design boundary

Stable retrieval was intended to supply destination/POI priors, not replace current
opening, disruption, weather, route or ticket verification. TP-RAG was a possible
China-specific supplement, not an implemented second corpus. Phases 1–5 were accepted
and designated the frozen technical baseline on September 18 except concrete bugs;
this was not a complete V2 runtime freeze. Phase 6 was then Proposed and later
implemented/validated separately. Google resolution remained demand-driven and
Google-first supply did not require a TripWorld match.

## Later shared changes (2026-09-20..25)

The [V2 milestone](v2-milestone.md) records the quality-first and first-draft acceptance
boundaries. A London run exhausted its 2-second connection allowance before SQL/embedding. The
approved connection-only change was 2 to 10 seconds, retaining that execution's SQL 60,
RAG 360 and explicit outer 600-second limits. Mocked checks verified timeout dispatch;
no live retry, SQL optimization or connectivity improvement was claimed.
Shared coverage/role diagnostics and the optional transfer DTO were later extended.
The [mixed-transport event](v1-development.md#2026-09-25---shared-first-generation-mixed-transport)
records the shared implementation, failures, retests and sizing. V2 still has no V3 Repair;
these offline changes do not validate prior live outputs or create a new freeze.
