# TripWorld embedding and persistent exact retrieval

## Space and offline/runtime boundary

OpenAI text-embedding-3-small, 1536 dimensions, float32, L2 normalization and cosine remain the
established ENRICHED space. dimensions is omitted and no query/document prefixes are added.
API model names are not immutable downloadable weight revisions: saved vectors, returned model,
content/request hashes and checkpoint metadata preserve actual results. Fresh regeneration need
not be bit-identical. Corpus embedding is an explicit offline job; runtime embeds bounded queries
only. Offline batch/retry/cost settings are not runtime query budgets.

## Persistence and exact search

Existing PostgreSQL/pgvector stores entity metadata, policy/corpus/space identity and compatible
vectors. Compose pins pgvector:0.8.2-pg17 by digest; the recorded setup verified PostgreSQL17.10
and pgvector0.8.2. Production eligibility precedes geographic-filtered exact cosine ranking with
stable entity ties and Top-K. No ANN or arbitrary early truncation is substituted. Compatibility
preflight validates corpus/space/policy, vector shape/normalization and integrity. Coordinates,
not locality strings, define the circle. No shadow table, vector copy or maintenance is implicit.

## Diagnostics and opt-in capture

RuntimeRetrieval observes connection/prepare, execute, fetch/decode and domain construction.
SQLSTATE is recorded if present, otherwise unknown. SQL suboperation timeout, server timeout,
outer phase deadline, provider errors and user cancellation remain distinct. Cleanup is awaited;
no background result mutation or hidden retry. Development vector capture is opt-in and records
actual vectors with text/vector hashes and space integrity. Production logs do not save raw user
vectors/text by default. Embedding SDK usage and owned-client HTTP attempts are independent,
deduplicated observations; unknown historical sends remain unknown.

The bounded diagnostic utility reuses runtime compatibility/SQL and distinguishes SELECT/EXPLAIN
from maintenance. A new connection is not cold cache; shared buffer reads are not a unique disk
I/O count. TOAST observations, variable timings and the paused inline shadow-table proposal are
in [V2 development](v2_development.md), not evidence of a completed optimization. [V2 design](v2_design.md)
owns runtime work budgets and resolution; [guide](development_guide.md) owns setup and backups.

## Schema, ingestion and resumability

corpus_builds records artifact hash, complete manifest, row count and timestamp. entities stores
Google ID, normalized names, geography/policy fields, exact ENRICHED text/hash, entity content hash
and typed JSONB metadata (aliases, FSQ provenance, categories, locality sets and anomaly flags).
embedding_spaces is keyed by immutable configuration fingerprint. embeddings stores one normalized
vector(1536) per exact text hash/space, plus vector hash and generation metadata. entity_embeddings
maps each eligible entity to its compatible text vector: text dedup saves physical storage without
merging distinct entity result identities or Top-K slots. RAW vectors are not imported.

Migration filenames/checksums are recorded; applied files cannot be edited. Initial migration
is transactional and advisory-locked. Ingestion validates Parquet hash, builder/text versions and
row provenance, COPY-loads staging, validates counts/duplicates, then performs transactional
content/version-aware upsert and removes stale entities for a full snapshot. Build locks prevent
corpus replacement during embedding. Changed text cannot reuse an old vector; unchanged text can
reuse vectors despite metadata changes. Unreferenced vectors are not destructively purged.

Production policy tripworld-production-policy-v1 excludes ineligible, empty-text, invalid-coordinate,
country-conflict and strictly-over-10-km spread entities. Unknown eligibility remains available;
excluded metadata is retained. Remaining 1-10-km spread flags are visible, not repaired identities.
The reason ordering above is the exclusion priority. Historical counts and cost/storage estimates
are in V2 development with their measurement conditions.

The offline builder processes missing distinct text hashes, content-addressed checkpoints and
binary COPY-upserts successful batches. Existing compatible vectors are skipped. A failed DB batch
rolls back only that batch; completed checkpoints remain recoverable. Recover pending batches before
changing batch partitioning. A lost paid response before durable checkpoint cannot guarantee exactly-once
billing. Runtime queries never execute ingestion, migration or this global embedding job.


## Clean-environment reproducibility audit (2026-09-20)

Scope: static current code and saved reports; no database query, API call or build was performed.
The existing foundation was already committed in 4d3d557, 7cdc182 and 4a744b3. The current worktree
relocates offline tooling and adds runtime integration; it is not a new global embedding build.
At the original audit, relocated code was still uncommitted. The approved repository checkpoint
subsequently saved that code in dc0b871 and the runtime integration in 255b1ec; this source-distribution
gap is now closed. No build or database restoration was executed during Git organization.

### Source, deterministic corpus and entity identity

`data/tripworld/manifest.json` pins CRUISEResearchGroup/TripWorld revision
`421bc1dc63068bb398055b1ce987265fe22415db`, metadata/metadata_all.parquet, 155531767 bytes,
687173 rows, SHA-256 `bd94d73c8443a18b5c7d31c0bd0b855cd141763b63841ee90646be1d73f9345e`.
Download validation checks size/hash/schema/row count. Projection retains only the eleven fields:
fsq_place_id, fsq_name, fsq_latitude, fsq_longitude, fsq_locality, fsq_region, fsq_country,
fsq_category_labels, google_name, google_categories, google_place_id. Coordinates are float64,
categories list-of-string, remaining fields string. Reviews/behaviors/attributes are not inputs.

`tools/data/tripworld/{preprocessing,corpus,semantics,entity_builder}.py` perform deterministic
projection, normalization, category/alias handling and identity grouping. ENRICHED text uses the
versioned category_semantics.v1.json mapping, not new model-generated enrichment. IDs and coordinates
remain metadata, not embedding text. The saved entity artifact contains 647057 entities; production
policy allows 580795, representing 577011 unique embedding texts. Entity identity is not text-hash
identity: shared text can reuse a vector without collapsing distinct entities.
Saved entity artifact hash: a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7.

### Embeddings and persistence

Accepted space: text-embedding-3-small, ENRICHED, 1536 dimensions, float32, normalized, cosine;
space ID afa5ba967bb4dbf2978e5a8e99b1f9dca25a4e1e23a4c51f8cfe8572113259ec.
Corpus build uses production_config: batches <=64 inputs/20000 tokens, per-input <=8191 tokens,
up to three attempts, 60-second provider timeout, checkpoint reuse and bounded production pacing.
This OFFLINE build policy is distinct from runtime's one embedding batch and retry=0. Existing
compatible Phase 4 vectors may be reused if locally present; a clean build need not have them.
Embeddings are external model outputs: a model name and dimension do not guarantee byte-identical
regeneration. Saved vector hashes/checkpoints are required for exact values.

Migration `tools/data/tripworld/migrations/001_retrieval.sql` creates the vector extension and
tripworld corpus_builds, entities, embedding_spaces, embeddings and entity_embeddings view.
Entities have a primary ID, coordinate checks, production eligibility/policy and artifact FK;
Google IDs have a partial unique index. Embeddings have (space_id,text_hash) primary key,
vector(1536), vector hash and generation metadata. B-tree geographic/country indexes and GIN
normalized-name support exist; there is no ANN index. Migration versions/checksums prevent silent
migration drift. Ingestion stages/upserts the entity snapshot; vector construction fills compatible
missing text hashes. Runtime validates corpus/space/policy compatibility.

Exact SQL in backend/app/tripworld/database/search.py bounds geography, applies the actual circle
and production conditions, joins space-compatible vectors, sorts cosine then entity ID COLLATE C,
limits Top-K and then joins entity payload. No shadow/PLAIN table or ANN has been applied. Docker
uses the named tripworld_pgdata volume, not a Git dataset directory.

### Actual command sequence (documentation only)

Run from the repository root AFTER saving this worktree. Commands are not executed by this audit.
Set private environment variables or local ignored .env.tripworld first. Docker Compose reads
that file for DB variables; Python commands explicitly load it where shown. Embedding/query steps
can spend money; schema/ingestion/embed steps write the database and need separate authorization.

```powershell
uv sync --locked --group retrieval
uv run python tools/data/prepare_tripworld.py download
uv run python tools/data/prepare_tripworld.py preprocess
uv run python tools/data/prepare_tripworld.py profile
uv run python tools/data/prepare_tripworld.py corpus
uv run python tools/data/tripworld_retrieval.py entities
docker compose --env-file .env.tripworld -f compose.tripworld.yaml up -d
uv run python tools/data/tripworld_database.py --env-file .env.tripworld migrate
uv run python tools/data/tripworld_database.py --env-file .env.tripworld ingest
uv run python tools/data/tripworld_database.py --env-file .env.tripworld preflight
uv run python tools/data/tripworld_database.py --env-file .env.tripworld embed
uv run python tools/data/tripworld_database.py --env-file .env.tripworld status
uv run python tools/data/tripworld_database.py --env-file .env.tripworld audit
uv run python tools/data/tripworld_database.py --env-file .env.tripworld query "museums and cultural places" --latitude 35.6762 --longitude 139.6503 --radius-km 15 --country JP --top-k 10
```

| Step | Input -> output / expected evidence |
| --- | --- |
| download | Fixed manifest -> raw/metadata_all.parquet; verified bytes/schema/hash |
| preprocess/profile | Raw -> processed/tripworld_selected.parquet and reports; 687173 source/projected rows |
| corpus | Selected fields + category mapping -> artifacts/retrieval_corpus.parquet and its manifest |
| entities | Corpus -> artifacts/retrieval_entities.parquet and manifest; saved baseline 647057 rows |
| migrate/ingest | Pinned Docker image + SQL migration + entity artifact -> schema/rows, reports/phase5_ingestion.json |
| preflight/embed | Policy-eligible text hashes -> 577011 physical baseline vectors, checkpoints and reports/phase5_embedding_run.json |
| status/audit | DB and saved checkpoint metadata -> versions/counts/integrity and reports/phase5_audit.json; no new embeddings |
| query | Semantic text + scope -> optional paid query embedding, then exact ranked entity IDs/scores/distances/metadata |

The existing `validate` subcommand is NOT the minimal clean-room validation step: it requires
artifacts/phase4/checkpoints and destinations.json, deliberately refuses new missing query vectors,
and executes maintenance ANALYZE before its broader SQL matrix. Do not advertise it as a generic
read-only command or assume those ignored historical inputs exist in a clean clone. A portable
small verification fixture/bundle is a remaining tooling need, not implemented here.

### Environment, scale and integrity checklist

Python >=3.12,<3.13; uv.lock pins packages; install retrieval dependencies (numpy, psycopg,
pgvector). Docker with persistent volume support is needed. compose.tripworld.yaml pins
pgvector/pgvector:0.8.2-pg17@sha256:feb68f4f15446397d8cac7f4fe48fe4586de83160d1fc48b46283312d1a33966.
DB variables: TRIPWORLD_DB_HOST (default 127.0.0.1), PORT (55432), NAME (tripworld), USER and
PASSWORD. Compose requires user/password. OPENAI_API_KEY is needed for new embeddings, not for
local DB audits; no Foundry/Google key is needed to build this corpus. Never commit credentials.
The embedding tokenizer may require its public vocabulary/cache on first setup; planner payload
counting has a separate explicit `uv run python tools/data/prepare_tokenizer.py` preparation step.
It is not a corpus embedding command.

Historical phase5_audit.json: DB 7260591795 bytes, zero missing production entity vectors and
zero invalid dimension/norm vectors. Generation window 4065.767 seconds includes pauses, excludes
work before the first saved response and reused Phase 4 vectors; it is not a clean-room build SLA.
Ingestion report: 100.574 seconds; repeated ingestion changed zero rows. Build preflight requires
25 GiB free workspace; allow additional Docker volume/WAL/checkpoints/source space. Reliable minimum
RAM and fresh-machine total build time are UNKNOWN; do not infer Docker memory from host RAM.
Historical observed tokens/cost estimates do not establish a current invoice or pricing guarantee.

Minimum verification: source size/SHA/schema/count; projection/corpus manifest versions/counts;
entity artifact/text hashes and policy; schema migration checksum and space config; eligible entity
count versus distinct text/vector count; no missing/invalid/nonfinite vectors; dimension and norm;
then a separately authorized bounded semantic query checking scope, rank, stable IDs and score
format. Existing ingestion/runtime checks, vector decoding and audit cover different parts, not
one universal verification command. Historical expected counts apply only to the fixed artifact.

### Reproducibility judgment and distribution boundary

Classification **B for functionally equivalent reconstruction**, with the current source now committed;
**C for exact historical vector/database contents from a clean clone alone**. Level 1 has an
implemented, repository-supported rebuild path plus the instructions above (not freshly executed here). Level 2 has local
hashes/checkpoint validation but not a complete immutable downloadable artifact bundle. Level 3
is not currently distributed: same model name does not recreate exact vector values, and the named
Docker volume is local-only. The repository checkpoint contains the relocated build/database entry points;
this closes the prior source gap without distributing the ignored data or exact historical vectors.

Keep source manifests/revision/checksum, mapping, small fixtures, SQL migration, Docker pin, tools,
lockfile and these instructions in Git. Keep raw/processed data, full corpus, vectors, DB volume,
logs and large reports out. The public fixed dataset is an upstream dependency; availability and
redistribution/license terms must be verified before publishing derived bundles.

Preferred next reproducibility step: an immutable corpus + vectors + metadata/hash bundle with a
small compatible query fixture and documented import verification, held outside ordinary Git.
That is more portable/auditable than a Docker volume image. A logical pg_dump can preserve schema
and exact values for faster restoration, at the cost of extension/version and artifact-size
coupling; it still needs checksum/version/restore verification and secret review. Neither release
nor dump exists as an audited recovery guarantee in this task. Do not create a new snapshot here.

## Connection establishment tolerance checkpoint

The approved connection timeout is now 10 seconds (previously 2); SQL remains 60 seconds
and the RAG phase 360 seconds. London stopped at connection establishment near two
seconds before embedding or SQL. This motivates a bounded tolerance change, not proof
of the underlying cause or that ten seconds will succeed. No SQL, storage, schema,
vector or retry change accompanies it. The outer 600-second development bound remains
explicit. Existing cancellation, awaited cleanup and Google-only degradation apply.
