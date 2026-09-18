# TripWorld Phase 4: global retrieval foundation and OpenAI spike

Status: development spike completed on 2026-09-18 and explicitly accepted as complete.
This is implementation validation, not a formal benchmark, research conclusion, or V2 freeze.
Phase 1-3 artifacts were reused. V0/V1 runtime paths and selection logic were not changed.
No global embeddings, PostgreSQL, pgvector, Google resolution, candidate merge, or V2 integration were implemented.

## Global entities and identity limitations

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

## API model and dimensionality decision

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

## Exact token estimates, API usage, and storage

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

## Representative destinations and geographic filtering

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

## RAW versus ENRICHED results

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

## Eligibility, duplicates, and Top-K

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

## Mapping gaps and next-stage recommendations

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

Recommended next stage, subject to approval:

1. Use PostgreSQL + pgvector for the global corpus, starting with one chosen text variant
   and `vector(1536)`. Keep an entity table keyed by retrieval entity ID, nullable Google
   ID, name/aliases, latitude/longitude, country/localities/regions, categories,
   eligibility, anomaly flags, source FSQ provenance, and text/content versions. Store
   embeddings separately by entity/content hash/model/dimension/text variant; keep a
   corpus-build manifest with source revision and checksums. Do not mix vector spaces.
2. Begin with indexed geographic candidate selection and exact cosine ranking inside
   that pool. Tokyo's 48,014 candidates require roughly 281 MiB of vector payload per
   scan; the current 384-candidate timing does not establish database p95 latency.
   Measure actual SQL plans, cold/warm reads, radius sizes, and concurrency before
   deciding on HNSW. There is no measured need for ANN yet, and no evidence that exact
   search meets all future latency targets. Avoid global ANN followed by a small
   geographic filter, which can underfill results without further design.
3. Retain explicit eligibility/anomaly handling and review negative semantic text,
   merged indoor/outdoor contexts, and taxonomy gaps before freezing corpus text.
   A full global embedding run should follow that text/dimension decision, with empty
   text exclusions, bounded scheduling, per-batch checkpoints, and a larger explicitly
   approved budget. The current CLI intentionally limits the spike to 2,500 entities.
4. Later resolve source Google IDs with current Google evidence and check identity
   consistency. FSQ-only discovery needs name/alias plus geographic resolution and
   ambiguity handling. A TripWorld-first result enters candidates only after successful
   Google resolution; Google-first candidates must continue without a TripWorld match.
5. Complement semantics with lexical proper-name/alias matching and later deterministic
   deduplication. Similarity is a discovery signal, not a replacement for Q+C+G+R+E.
   Define geographic scope resolution, query-intent contracts, budgets, and provenance
   before connecting to the V2 candidate funnel. Optional live Google comparison was
   deferred; no Google calls or V1 modifications were needed for this spike.

## Reproduction and checks

Implementation lives in `backend/app/tripworld/retrieval/`; the isolated entry point is
`scripts/tripworld_retrieval.py`. Configuration and queries are in
`data/tripworld/embedding_model.v1.json` and `retrieval_queries.v1.json`.

```powershell
uv sync --group retrieval
uv run --group retrieval python scripts/tripworld_retrieval.py entities
uv run --group retrieval python scripts/tripworld_retrieval.py sample
uv run --group retrieval python scripts/tripworld_retrieval.py estimate
# Live step: OPENAI_API_KEY must already exist in the process environment.
uv run --group retrieval python scripts/tripworld_retrieval.py spike
uv run --group retrieval python scripts/tripworld_retrieval.py query --semantic-query "quiet indoor places" --latitude -37.812659 --longitude 144.965733 --radius-km 15 --country AU --top-k 10 --variant enriched --exclude-ineligible
uv run pytest -q
uv run ruff check .
```

Only the OpenAI endpoint is used; no implicit Luna/Azure/base-URL fallback and no
implicit `.env` loading. The adapter sanitizes API errors. Transient connection,
408/409/429/5xx errors have bounded backoff; authentication/quota failures stop.
Each completed batch is atomically checkpointed and checked by input/vector hash.
The same input/configuration/batch partition reuses completed vectors. A lost response
before a durable checkpoint can be billed again: no API-level exactly-once guarantee
is claimed. Do not delete checkpoints or change batch partition mid-resume.
Changing operational configuration also changes checkpoint fingerprints. Concurrent
writers to the same artifact directory are not supported by this development CLI.

The tokenizer cache, raw/projected data, entity/vector artifacts, checkpoints, and
generated reports are gitignored. Only code, tiny fixtures, configuration/manifests,
and this report are intended for version control. The full backend regression suite
passed **644 tests**, including **39 TripWorld tests**; Ruff passed. Tests use fake
embedding providers/HTTP responses and do not require API credentials or downloads.
They cover deterministic grouping/rebuilds, geo boundaries, normalized exact ranking,
artifact corruption/version mismatch, retry and failure behavior, preflight budgets,
and interruption/resume. Existing Phase 1-3 work remains uncommitted and preserved.
No commit, push, database setup, global embedding, or V2 runtime work was performed.
