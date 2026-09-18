# TripWorld Phase 5: persistent retrieval layer

Phase 4 and Phase 5 were explicitly accepted as complete. The user designated Phases
1-5 as the frozen technical baseline on 2026-09-18, except for concrete bug fixes.
Phase 5 implements an isolated global retrieval
layer; it does not modify V0/V1 runtime, Q+C+G+R+E, or itinerary generation. Phase 6
Google resolution and candidate integration remain unimplemented. This document
records completed full-corpus engineering validation on September 18, 2026. Phase 5
is implemented; this is not a complete V2 runtime milestone or complete V2 freeze.
The process record is in `thesis_notes/V2/README.md`; Phase 6 remains a design-only
proposal in `docs/tripworld_phase6_proposal.md`, awaiting approval.

## Reproducible local setup

Use Docker Desktop in Linux-container mode. The separate `compose.tripworld.yaml`
project pins `pgvector/pgvector:0.8.2-pg17` by image SHA-256, with PostgreSQL 17.10
and pgvector 0.8.2 verified in the running container. It exposes port 55432 only
on 127.0.0.1, has a `pg_isready` healthcheck, and uses the persistent named volume
`reliable-tripworld_tripworld_pgdata`. It does not require native Windows PostgreSQL.

Create an ignored `.env.tripworld` from the TripWorld variables in `.env.example`.
Set a nonempty database password locally; no real credentials belong in Git.
Set `OPENAI_API_KEY` in the process environment before paid embedding/query operations.
The CLI loads an environment file only when `--env-file` is supplied and does not
override existing process variables. OpenAI uses its own API endpoint, not Luna/Azure.

```powershell
uv sync --group retrieval
docker compose --env-file .env.tripworld -f compose.tripworld.yaml up -d --wait
uv run python scripts/tripworld_database.py --env-file .env.tripworld migrate
uv run python scripts/tripworld_database.py --env-file .env.tripworld ingest
uv run python scripts/tripworld_database.py --env-file .env.tripworld preflight
# Review the printed cost/resource preflight before the full embedding job.
uv run python scripts/tripworld_database.py --env-file .env.tripworld embed
uv run python scripts/tripworld_database.py --env-file .env.tripworld status
uv run python scripts/tripworld_database.py --env-file .env.tripworld validate
uv run python scripts/tripworld_database.py --env-file .env.tripworld audit
docker compose --env-file .env.tripworld -f compose.tripworld.yaml stop
# Start again with up -d --wait. Do not use down -v unless intentionally deleting data.
```

`validate` reuses Phase 4's existing 24-query vector checkpoint, without API calls.
It requires the completed production vector set and the Phase 4 sample/query artifacts.
The retrieval service itself does not depend on the Phase 4 sample.

## Five-ID sanity check

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

## Schema, provenance, and ingestion

`backend/app/tripworld/database/migrations/001_retrieval.sql` initializes the extension
and schema. The migration runner records filename/checksum and rejects edits to applied
migrations. Initialization is transactional and serialized with an advisory lock.
Subsequent changes belong in new numbered migration files.

- `corpus_builds`: source artifact hash, complete build manifest, row count and timestamp.
- `entities`: one row per RetrievalEntity, Google ID, normalized names, geographic and
  policy columns, exact ENRICHED text/hash, entity content hash, and complete typed
  entity metadata in JSONB. This preserves aliases, FSQ provenance, categories, semantic
  fields, locality/region/country sets, anomaly flags, and all corpus/text versions.
- `embedding_spaces`: immutable compatibility configuration, keyed by its fingerprint.
- `embeddings`: one normalized `vector(1536)` per exact text hash and embedding space,
  plus vector hash, generation metadata and timestamp.
- `entity_embeddings`: a view mapping every allowed entity to its compatible text vector.
  Multiple entities with byte-identical text can reuse one physical vector while
  retaining separate retrieval identities and slots.

RAW vectors are not imported. Old vectors with changed text cannot match updated
entities; unchanged text can reuse its vector even if non-text metadata changes.
Historical unreferenced vectors can remain as reusable cache; no destructive global
vector purge is part of normal ingestion.

Entity ingestion validates the Parquet SHA-256, builder/text versions and each row's
provenance against its manifest. COPY loads a temporary staging table, validates counts
and duplicate IDs, then performs a transactional content/version-aware upsert and
removes stale entity rows from that full snapshot. No per-row INSERT loop is used.
The ingestion/build locks prevent a corpus replacement during an embedding build.

The initial full COPY ingestion populated **647,057 rows in 100.57 seconds**.
An unchanged full-corpus rerun completed in **83.76 seconds**, with **zero changed
rows and zero removals**. Tests separately exercise changed-text invalidation and rollback.
Production source SHA-256 remains
`a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7`.
The original TripWorld revision and approved Phase 1-4 artifacts were not regenerated.

## Explicit production policy and preflight

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

## Embedding generation and recovery

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

## Retrieval service and indexes

`RetrievalService` separates query embedding from `PostgresSearch`. It accepts a
semantic intent, generic coordinates/radius, optional country and Top-K, and returns
ranked typed entity metadata, cosine similarity and distance. Query construction is
not the raw trip request and does not modify the V1 interpreter. Normal discovery
always applies the fixed policy; callers cannot silently include ineligible entities.
Search validates an existing embedding space without creating or updating it, and the
service rejects a missing/incompatible space before constructing a paid API provider.
Lexical lookup and geographic counts do not require populated vector storage.

The exact SQL pipeline is bounding box (including antimeridian splits), optional
country consistency, Haversine radius, structured policy, compatible vector join,
cosine ordering, and deterministic entity-ID tie-breaking. Missing country metadata
remains available. Locality equality is never the geographic filter. Top-K is a caller
parameter (1-1000), not a final V2 selection policy.

B-tree indexes cover entity identity, non-null Google ID uniqueness, latitude,
longitude, country and allowed text hashes; a GIN array index supports normalized
exact preferred-name/alias lookup. Vector storage has a composite space/text-hash
primary key. There is **no HNSW, IVFFlat, PostGIS, fuzzy lexical ranking or score fusion**.

```powershell
uv run python scripts/tripworld_database.py --env-file .env.tripworld query "quiet indoor places" --latitude -37.812659 --longitude 144.965733 --radius-km 15 --country AU --top-k 10
uv run python scripts/tripworld_database.py --env-file .env.tripworld query "State Library Lawn" --latitude -37.812659 --longitude 144.965733 --radius-km 15 --country AU --lexical
```

## Validation and next-stage boundary

Automated tests use mocked OpenAI responses and an optional separate `tripworld_test`
database. The test fixture refuses to reset the production database. Enable real DB
tests with `TRIPWORLD_TEST_DATABASE=1` and the local DB credentials; create the separate
test database first. Default tests skip these integration tests when not configured.
No normal test makes a live OpenAI call.

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

### Working-tree and evidence status

Phase 5 adds `compose.tripworld.yaml`, `backend/app/tripworld/database/`,
`scripts/tripworld_database.py`, database tests and this report. It extends the
existing OpenAI adapter/checkpoint support, dependency groups/lockfile, environment
example and project status. Existing Phase 1-4 uncommitted files are preserved.
Tracked modifications are `.env.example`, `.gitignore`, `PROJECT.md`, `pyproject.toml`
and `uv.lock`; TripWorld code/tests/scripts/configuration/docs remain untracked pending
an explicitly requested commit. No V0/V1 runtime or selection files changed. No commit,
push, Google bridge, candidate funnel, Q_rel mapping or itinerary change was made.

Raw data, generated Parquet/NumPy/checkpoint artifacts, validation reports and real
credentials remain ignored. Reproducible code/configuration, manifests, versions,
hashes, tiny fixtures and this aggregate report remain reviewable in the repository.
Local detailed evidence is under `data/tripworld/reports/`: `phase5_google_sanity.json`,
`phase5_ingestion.json`, `phase5_reingestion.json`, `phase5_preflight.json`,
`phase5_embedding_run.json`, `phase5_audit.json`, `phase5_validation.json`,
`phase5_lexical.json` and `phase5_service_smoke.json`.

Phase 6 recommendations (not implemented): resolve only the ranked candidates actually
needed. Try an existing Google ID first, fall back to name/location on failure; FSQ-only
candidates begin with name/location search. Discard unresolved candidates and continue
until the required usable pool or request budget is reached. Preserve discovery and
resolution provenance, deduplicate by canonical Google ID, reuse request-scoped cache,
and retain Google-first candidates without a TripWorld match. Do not prevalidate the
global corpus, and do not turn cosine similarity directly into Q_rel without a separate
integration design. Existing Q+C+G+R+E remains unchanged.

For that design, keep cosine score and retrieval rank as discovery provenance, then
compute the existing Q_rel from the resolved canonical POI using its current contract.
Any future score fusion needs an explicit definition and separate approval. Give
resolution a per-trip call/attempt budget (including failed lookups and fallbacks),
reuse the existing RequestCache for repeated IDs/searches, and stop on either a usable
pool target or budget exhaustion. Candidate replacement should continue down the RAG
ranking after a failed resolution without blocking Google-first discovery. Exact
budget, pool size and concurrency settings remain Phase 6 decisions.
