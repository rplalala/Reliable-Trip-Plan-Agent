> Archived source snapshot, relocated 2026-10-03 from `docs/v2_development.md`.
> Current design is indexed in [docs/README.md](../../README.md).
> Original Current/Next statements and historical defaults below are dated evidence,
> not current system authority or renewed execution permission.

# V2 development record

> Repository cleanup (2026-09-20): source/document/config recovery snapshots, including
> `D:/Workspace/Capstone/phase6_source_snapshots`, have been permanently deleted by user approval.
> Snapshot paths in dated entries describe historical actions, not available recovery locations.
> Retired selector implementations are no longer executable. Historical methods/results remain.

Dated records below preserve original scope, status and evidence; they are not current runtime instructions. Current design is maintained separately. Proposed or unexecuted steps remain unexecuted unless a later explicitly identified record establishes otherwise.

<a id="m-6d53b29b6f5c"></a>
## Development waiting override and conditional normal RAG live - 2026-09-20

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-6d53b29b6f5c-0"></a>

Status: **Normal V2 RAG discovery/resolution/supply/scheduling has bounded development-live
 evidence under the explicit 60/180-second override. Not a production SLA or re-freeze.**

<a id="b-6d53b29b6f5c-1"></a>

The user deferred inline/PLAIN shadow tables and storage copying to prioritize functional
validation of the original tables and exact SQL. Historical 3/30-second failures, 1.13-second
success/15-second timeout variation, and EXTERNAL/TOAST findings remain valid. This task
changed waiting budgets only for explicitly opted-in V2 development calls. It did not
perform a database performance optimization or establish production latency guarantees.

<a id="m-54c83799ba98"></a>
## Minimal override and effective timeout stack

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Development waiting override and conditional normal RAG live - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-54c83799ba98-0"></a>

config/v2_development_override.json contains ONLY sql_timeout=60 and deadline_seconds=180.
versions/v2/config.py now permits those upper bounds while defaults remain SQL=3/phase=30.
load_development_override(path, base) rejects other keys and validates against RAGConfig;
it returns a new config without mutating shared runtime defaults. Existing run_v2 rag_config
and retrieval_factory injection are used. No destination-name condition, parallel config
framework, V0/V1 override or offline corpus-build configuration change was introduced.

<a id="b-54c83799ba98-1"></a>

To opt in from development orchestration, load that file against
load_runtime_config().tripworld_discovery and pass the resulting config to run_v2(rag_config=...).
If supplying retrieval_factory for explicit vector capture, construct RuntimeRetrieval with
that SAME effective config and capture_directory under ignored logs. No automatic default
engine or CLI behavior changed.

<a id="b-54c83799ba98-2"></a>

| Boundary | Historical/default | This development validation |
|---|---:|---:|
| PostgreSQL session statement_timeout | 3000 ms | 60000 ms (SHOW returned 1min) |
| Application SQL execute/fetch | 3 seconds | 60 seconds |
| Entire RAG phase | 30 seconds | 180 seconds |
| Development whole-run bound | no AcceptanceSession global bound | explicit 360 seconds |
| Embedding / connect / Google suboperations | 8 / 2 / 4 seconds | unchanged |

<a id="b-54c83799ba98-3"></a>

The existing enclosing RAG timer limits any SQL to min(60 seconds, remaining phase time);
expiration cancels/awaits the in-flight work and resource cleanup, rather than leaving a
background query. Server settings are per connection, never global. Runtime prepare uses
its existing SQL timeout field for compatibility reads, now the explicit development value;
connection timeout remains two seconds. AcceptanceSession/shared runner have no hidden
shorter whole-run wait. The 360-second development wrapper did not change per-model/provider
timeouts. No timeout fired in this live.

<a id="b-54c83799ba98-4"></a>

Work ceilings remain two queries, one embedding batch, Top-K 10, 20 returned positions,
six new-resolution attempts (failures count), eight incremental Details, two fallback
searches, zero retries. Main supply and Nearby budgets are unchanged. SQL builder, corpus,
space, policy, geographic bounds, tie order, identity policy and generation prompts unchanged.

<a id="m-4f9837cedc76"></a>
## Offline gate and two local SELECTs

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Development waiting override and conditional normal RAG live - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-4f9837cedc76-0"></a>

Affected configuration/runtime/deadline/service/V2-runner/AcceptanceSession tests:
**94 passed in 15.53 seconds**, exit 0. Ruff and diff checks passed. Tests confirm effective
60000 ms session timeout, immutable defaults/work ceilings, actual V2 config dispatch,
phase/caller cancellation, ownership, cache and failure distinctions. Unit tests did not wait
60/180 seconds. No new failures or fixes between the gate and paid execution; no full suite
repeat. The prior full 860 passed/9 skipped remains separate historical evidence.

<a id="b-4f9837cedc76-1"></a>

Both local requests used actual RuntimeRetrieval, original SQL, fresh RequestCache, the
previously validated museums/cultural vector and Tokyo (35.6764225,139.650027), 15 km, K=10.
Original Tokyo vectors are still absent; these two SELECTs are compatibility/performance
controls, not an exact replay of the old semantic request. Each independently had 180-second
outer boundary, SQL=60, read_only=on and cache_hit=false. No database/OS cache flush or warmup.

<a id="b-4f9837cedc76-2"></a>

| Local execution | Execute | Fetch/decode | Query total | Whole local check | Result |
|---|---:|---:|---:|---:|---|
| First | 23.914363 s | 0.000227 s | 23.914825 s | 23.971042 s | 10 valid rows |
| Repeat | 0.962450 s | 0.000223 s | 0.962881 s | 1.008015 s | 10 valid rows |

<a id="b-4f9837cedc76-3"></a>

Entity schemas/artifact/coordinates/scores passed integrity checks. Ordered IDs matched
exactly, scores matched with rtol=0/atol=1e-6; complete IDs/scores are in local_results.json.
Both transactions ended IDLE and connections closed; neither timed out or reported SQLSTATE.
These are first/repeated observations, not controlled cold/warm measurements. Exactly two
local retrieval executions, no third or extra EXPLAIN. Both gates passed, authorizing the
single fresh Tokyo live without another approval prompt.

<a id="m-8c05c0738bde"></a>
## Frozen fresh Tokyo dispatch

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Development waiting override and conditional normal RAG live - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-8c05c0738bde-0"></a>

Actual runner backend.app.versions.v2.runner.run_v2; existing AcceptanceSession and Windows
SelectorEventLoop. input=planning_request_2, output=itinerary_2. Trusted reference date
2026-09-20; trip 2026-09-21 through 2026-09-23, Tokyo, Japan, three travelers, total 180000 JPY.
Exact additional_preferences:
`I definitely want to visit Meiji Jingu. I prefer small museums and places with distinctive local architecture.`

<a id="b-8c05c0738bde-1"></a>

- request_hash: `9c73e491a640eaa3c48723b38ffa3725d18e4dc7572963979e8e28b16e095442`.
- implementation_hash: `6a20a9fc859117d497c8434ae45c7a4e9273ca5d682b711051b33dadb66797bb`.
- runtime_config_hash: `34f05980dba254106e47dc70b3b0c7e7b2f55b0005cc5566602b7de00bc39fd8`.
- prompt_files_hash: `86de03ed6f948b87ff55c5899215c365cd86464a96b64b0208c002ae4fb39b5e`.
- schema_files_hash: `4ee5ce9029edeaf73895dc9358c006c146d9f5f7bb18086f1c215066f7f5cbc5`.
- corpus_manifest_hash: `ac9d7cc8c0b28cbc3ad3913ed6921f67342fbe662f08a768098745e9dd30b349`.
- artifact_hash: `a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7`.

<a id="b-8c05c0738bde-2"></a>

Effective configuration and old/new values are frozen in effective_config.json/live_manifest.json.
No source/config changed between freezing and completion. Query vectors came from this
fresh interpretation and real embedding call, NOT the diagnostic vector. One opt-in NPZ
contains both actual 1536-dimensional normalized vectors; vector checksum, text hashes in
actual query order, space and shape were verified offline. The earlier missing capture is
not rewritten as available. Credentials were not added to captures or documents.

<a id="m-d77e3b5493b5"></a>
## Actual query-to-itinerary funnel

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Development waiting override and conditional normal RAG live - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-d77e3b5493b5-0"></a>

Both queries were user-derived: discovery_1 `places with distinctive local architecture`
linked to semantic_1, and discovery_2 `small museums` linked to semantic_2. One embedding
batch/one observed HTTP attempt (200), seven prompt/total tokens. Runtime prepare 0.056743 s;
embedding 2.592 s. SQL 1 execute/fetch: 23.297610 / 0.000238 s; SQL 2: 0.884878 / 0.000352 s.
Two successful result sets, ten positions each, 20 distinct entities, no Google overlap.

<a id="b-d77e3b5493b5-1"></a>

Six direct-ID resolution attempts all succeeded, six incremental Details HTTP sends, zero
fallback, zero RAG cache hits. Fourteen remaining entities were marked entity_budget, not
invalid/failed/attempted. Status partial therefore records bounded processing, not failed SQL
or Google-only degradation. Canonical union added six net-new Google-backed identities;
Google used for identity resolution does not make them Google-discovered.

<a id="b-d77e3b5493b5-2"></a>

| New RAG-only candidate | Admission / subsequent outcome |
|---|---|
| Beni Museum | admitted; normal enrichment reused cached Details; supplied and scheduled |
| Min-on Music Museum | admitted; normal enrichment capacity not attempted |
| Wakayama Domain Kii Family Mansion Remains | admitted; normal enrichment capacity not attempted |
| Remains of Kirishitan Yashiki | admission capacity omission |
| Fushimi-yagura | admission capacity omission |
| The National Museum of the Imperial Collections, Sannomaru Shozokan | admission capacity omission |

<a id="b-d77e3b5493b5-3"></a>

All six had resolution Details, but only ONE reached the normal enrichment stage under its
existing bounded processing order; these are different stage counts. RAG fate: 3 admitted,
1 normally enriched, 1 supplied, 1 scheduled, zero mixed identities. One compatible Details
cache hit avoided re-fetching Beni Museum. Mixed-source overlap and fallback remain live
uncovered; no source boost or guaranteed RAG quota was used.

<a id="b-d77e3b5493b5-4"></a>

Main supply: 8 identities (1 REQUIRED +7 OPTIONAL), comprising 7 Google-only and 1 RAG-only.
Scheduled: 5 unique canonical IDs (4 Google-only, 1 RAG-only, 0 mixed). REQUIRED Meiji Jingu
scheduled; zero unlinked activities, zero unscheduled REQUIRED. The three supplied-but-not-
scheduled Google-only places were Aoyama House, Japan Traditional Crafts Aoyama Square and
Shinjuku Gyoen Museum. No comparison to prior itinerary length is a formal quality result.

<a id="m-a3cf735b5804"></a>
## Actual generated itinerary and application references

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Development waiting override and conditional normal RAG live - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-a3cf735b5804-0"></a>

Times are actual Tokyo local (+09:00) output. No activity was added by the reviewer.

<a id="b-a3cf735b5804-1"></a>

| Date | Time | Main place | Discovery source |
|---|---|---|---|
| 2026-09-21 | 09:30-12:00 | Meiji Jingu | Google-only |
| 2026-09-22 | 10:30-12:30 | Former Prince Asaka Imperial Family Residence | Google-only |
| 2026-09-22 | 13:00-14:30 | Tokyo Metropolitan Teien Art Museum - Japanese Garden | Google-only |
| 2026-09-23 | 10:30-12:00 | Beni Museum | RAG-only |
| 2026-09-23 | 15:00-17:00 | Extinct Media Museum | Google-only |

<a id="b-a3cf735b5804-2"></a>

Main notes retain unknown date-specific opening exceptions and required-visit access.
The garden transfer references supplied 107 m/85-second matched route evidence. Beni to
Extinct Media Museum lacks a usable transit alternative measurement and requires flexible
transport/feasibility confirmation. All five costs are null; budget feasibility is unproven.
The first day contains one main visit, not a filled whole day. No activity-density repair or
new validator was introduced. Weather again returned HTTP 404; that separate issue persists.

<a id="b-a3cf735b5804-3"></a>

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

<a id="m-fa51618295ed"></a>
## Calls, usage, elapsed time and acceptance limits

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Development waiting override and conditional normal RAG live - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-fa51618295ed-0"></a>

| Actual work | Count |
|---|---:|
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

<a id="b-fa51618295ed-1"></a>

Longer waiting did not add work ceilings or retries, but six RAG identity Details calls now
actually occurred. This is not zero incremental Google cost. The one cached re-use means
normal enrichment attempted ten places while issuing nine new Details sends. Counts are
actual workload, not invoices. One fresh planner and one interpretation; no paid replacement.

<a id="b-fa51618295ed-2"></a>

| Model task (gpt-5.6-luna) | Input | Output | Included reasoning | Cached input | Cache write | Total |
|---|---:|---:|---:|---:|---:|---:|
| Requirement | 3939 | 856 | 513 | 0 | 3936 | 4795 |
| Itinerary | 20183 | 1735 | 741 | 0 | 20180 | 21918 |

<a id="b-fa51618295ed-3"></a>

Embedding seven tokens is separate. Reasoning/cache are not added again to reported totals.
RAG phase: 30.619 s (embedding 2.592, retrieval 24.184, resolution 3.693).
Main itinerary completion: 68.185 s; Nearby: 2.844 s; total fresh request: 71.052 s.
The 60/180/360 limits are development ceilings, not measured target latency or production SLA.
No SQL/phase timeout occurred. Actual reads continue to show large first/repeat variation;
TOAST/storage diagnosis is not invalidated and no performance optimization was performed.

<a id="b-fa51618295ed-4"></a>

Session capture_errors empty, tracer healthy, owned model client closed once, runtime DB
connection closed; vectors verified and sources unchanged. No retry, supplemental search,
second live, Melbourne run or post-hoc output editing. Failure branches were not injected;
new default/mixed/fallback destinations and broad correctness remain outside this smoke.

<a id="b-fa51618295ed-5"></a>

Functional conclusion: the original exact SQL/tables can support normal bounded V2 retrieval,
Google-backed canonical integration and a scheduled RAG-only POI under a reasonable explicit
development waiting allowance. This is stronger than the prior Google-only fallback evidence,
but only one fresh live and not a formal benchmark or complete version freeze.

<a id="b-fa51618295ed-6"></a>

Next recommendation: accept this normal-path functional checkpoint and keep the 60/180 file
explicitly opt-in. Record latency as unresolved; do not automatically adopt it as production
policy, start shadow storage, or expand live scenarios. Inline/PLAIN work is deferred, not
rejected. Melbourne named-role ambiguity remains unchanged. Any further performance work or
production timeout decision requires separate approval.

<a id="b-fa51618295ed-7"></a>

Changed implementation scope: versions/v2/config.py bounds/loader, the two-key development
JSON, and three relevant test files. Existing SQL, runtime adapter, prompts, common config,
frontend/default, B2 and database are unchanged this task. Existing records updated in place;
artifacts remain ignored under logs/phase6_development_window_20260920. No stage/commit/push,
re-freeze, corpus/vector rebuild or V3 work.

<a id="m-e3e3a7dac846"></a>
## Runtime observations and storage decision - 2026-09-20

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-e3e3a7dac846-0"></a>

Status: Local observation repair implemented and offline checked. Decision **B**: proceed
only with a separately approved storage-layout experiment; no production SQL/performance
change, timeout increase or normal V2 live acceptance is claimed.

<a id="m-801def8f67cc"></a>
## Preserved baseline and implemented observations

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Runtime observations and storage decision - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-801def8f67cc-0"></a>

The original Tokyo vectors are still missing. The museums/cultural checkpoint remains a
compatible performance control, not exact semantic replay. Earlier observations include
1.130-second completion and 15-second timeouts at execute; fetch/decode was negligible
when reached, and the original 30-second phase was not exhausted. Melbourne remains a
pre-RAG named-identity clarification. The prior 860-pass/9-skip full suite remains historical
and was not repeated in this telemetry task.

<a id="b-801def8f67cc-1"></a>

RuntimeRetrieval now records metadata-only timings for prepare, connection, compatibility,
embedding, SQL, execute and fetch/decode. Errors retain exception type and PostgreSQL
SQLSTATE when exposed; absent SQLSTATE stays unknown. The existing SQL timeout context
is retained at the same location/value; its expired() value is observed after exit.
TripWorldDiscovery retains existing status/degradation behavior and adds timeout_scope and
phase_deadline_expired. Caller cancellation is recorded and immediately re-raised; no retry,
replacement query, negative-cache or background-task behavior was added. This touched the
execution/cancellation call sites for measurement, so adapter, service cancellation and V2
runner tests were included; it is not hidden as an unrelated logging-only change.

<a id="b-801def8f67cc-2"></a>

Embedding request/response hooks attach to the actual owned SDK HTTP client, including the
installed httpx2 path. Hooks record unique attempt IDs, status and request IDs, without
headers, credentials or raw inputs. No global send/close replacement. Hooks are removed
before normal owned-client closure. embedding_sends continues to count SDK batch attempts;
embedding_http_attempts records real HTTP attempts separately. SDK usage is captured once
before subsequent domain validation; status/request metadata survives malformed JSON or
model mismatch. Usage is not reconstructed from HTTP layers or counted twice. Historical
HTTP-send counts remain UNKNOWN, not retroactively repaired.

<a id="b-801def8f67cc-3"></a>

Full query vectors are saved ONLY when a development caller explicitly passes
`capture_directory=Path("logs/<development-session>/query_vectors")` to RuntimeRetrieval,
for example through the existing V2 retrieval_factory injection. Default is None; no runtime
configuration/prompt/CLI default was changed. Each opt-in NPZ includes float32 normalized
vectors, shape/dtype, corpus artifact, full space/space ID, per-input text SHA-256 and vector
SHA-256. Raw query text is not written by this capture; text hashes link to separately
approved input capture. Capture failure records a diagnostic and does not fail a successful
embedding result. Capture success is not permission to commit vectors or private artifacts.

<a id="m-0678608edc7b"></a>
## Actual local structure and resource evidence

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Runtime observations and storage decision - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-0678608edc7b-0"></a>

New bounded read-only catalog checks used the current local PostgreSQL and existing adapter.
Artifacts: artifacts/diagnostics/retrieval_storage/{structure,storage_details,decision}.json.
No vector search, EXPLAIN ANALYZE, provider/model call, schema write or maintenance occurred.
Existing executed plans from the preceding eight-query diagnosis were reused.

<a id="b-0678608edc7b-1"></a>

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

<a id="b-0678608edc7b-2"></a>

The embeddings table also carries space/text/vector hashes and generation metadata
(avg_width 885); the 18-byte vector width and 4.73 GB TOAST heap support widespread out-of-line
vectors. EXTERNAL policy alone would not prove every row is out-of-line. TOAST size contains
actual vector data, not 4.73 GB of pure overhead. Cumulative table I/O counters were captured,
but are not this query's deltas. Shared reads can hit OS cache. Parent/child EXPLAIN buffers
are not summed. The existing Tokyo plan performs 44,440 vector lookups and only ten final
entity payload fetches, with cardinality underestimation and 706 temporary blocks written.

<a id="b-0678608edc7b-3"></a>

Read-only Docker inspection (initial sandbox pipe denial resolved by authorized read access):
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

<a id="m-b40ae23328d7"></a>
## Candidate selection and bounded experiment stop

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Runtime observations and storage decision - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b40ae23328d7-0"></a>

The authorized early-stop condition was used: no SQL/session-only candidate had evidence
that it would remove the dominant per-vector out-of-line access. Increasing work_mem could
remove a roughly 5.5 MiB CTE spill, but would leave 44,440 embedding lookups and TOAST reads.
The query already defers full entity metadata until Top-K. Removing materialization without
a demonstrated plan benefit could introduce recomputation instead. No arbitrary rewrite or
work_mem/parallel/cache combination was tested just to fill the query allowance.

<a id="b-b40ae23328d7-1"></a>

| New experiment category | Executions | Result/equivalence |
|---|---:|---|
| A original normal SELECT | 0 | Not executed this task |
| B alternative normal SELECT | 0 | No supported SQL/session candidate selected |
| EXPLAIN ANALYZE | 0 | Prior actual plans reused |
| Ordered-ID/score comparison | 0 | No new real-data equivalence or speedup claim |

<a id="b-b40ae23328d7-2"></a>

This is not an A-B-B-A result, not evidence that a tested rewrite failed, and not a p95/SLA
measurement. It is the explicitly allowed evidence-based decision to stop before an
unjustified low-risk rewrite. The new task used 0 of 4 normal and 0 of 2 analyzed searches;
no prior eight executions were relabeled as new comparisons. No production timeout change:
15 seconds per query would not leave adequate time for two queries plus embedding and
Google resolution inside 30 seconds, and prior 15-second failures remain unexplained in
full detail. Larger timeout alone is not a completed performance repair.

<a id="m-00dcc4666093"></a>
## Decision B: one preferred approval item, inline-vector shadow storage

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Runtime observations and storage decision - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-00dcc4666093-0"></a>

Prefer a controlled storage-layout experiment before an ANN semantic change or resource
expansion. Its SINGLE primary variable is embedding inline versus current EXTERNAL storage.
Create a separately named shadow copy of the embeddings table with vector(1536) PLAIN
storage set BEFORE copying; retain the same columns, key/index definitions, space and
existing vector bytes. Only the diagnostic query's relation name changes between copies.
No embedding regeneration, dimension change, candidate truncation or new index algorithm.

<a id="b-00dcc4666093-1"></a>

Why this target: inline vectors can remove separate TOAST lookup/chunk access for each
exact comparison. This directly addresses observed work, unlike raising timeout or only
removing CTE spill. It may increase main-heap pages and cache pressure, so improvement is a
hypothesis, NOT established. Row-size compatibility and treatment of other variable-width
columns must be checked during construction; preserve their values and integrity.

<a id="b-00dcc4666093-2"></a>

Costs and recovery: this requires a full copy/write of approximately 577k existing vector
rows, ordinary duplicate indexes and WAL; it is NOT a metadata-only ALTER. Merely changing
SET STORAGE on the existing column would not retroactively inline the stored vectors.
Budget roughly 5-6 GB for the shadow plus WAL/temporary headroom; require at least 12 GB free
before starting as an engineering guard, then monitor actual growth and stop at an approved
space bound. This estimate is not a measured final table size. No Docker/PostgreSQL restart
is inherent. Original table, IDs, corpus manifests, query SQL and runtime remain untouched
as the recoverable baseline; do not cut over or drop originals during the experiment.

<a id="b-00dcc4666093-3"></a>

Approval scope for that future package:

<a id="b-00dcc4666093-4"></a>

1. Approve isolated shadow construction and its bounded disk usage explicitly (not done now).
   Record source corpus/space/count/hash identities and snapshot references; verify copied
   text/vector hashes and eligibility identities before querying. Existing saved vectors only.
2. Reuse diagnose_tripworld_sql.py for one layout comparison, same vector/Tokyo scope/K/
   cosine/policy/tie. At most A-B-B-A plus one plan for each layout, each <=15 seconds.
   Compare successful ordered entity IDs and scores (absolute tolerance 1e-6); incomplete
   runs cannot prove equivalence. Capture per-run page/TOAST work without cumulative double
   counting; no active cache warmup, resource change or concurrent settings tuning.
3. Promotion gate: real-data equivalence, materially reduced vector-fetch I/O, and repeated
   normal-query benefit; a lone faster run is insufficient. Four timings do not establish
   production SLA. If supported, submit the smallest production migration/cutover and rollback
   patch for another approval; otherwise preserve the current production layout and report
   this specific hypothesis unsupported. No production cutover is authorized by this proposal.
4. Offline adapter/cancellation/capture tests first. Only after a justified production change,
   request separate permission for at most one necessary Tokyo V2 live to test normal RAG
   resolution/source union/fate. No Tokyo/Melbourne full live in the current task.

<a id="b-00dcc4666093-5"></a>

Melbourne's market/station ambiguity remains an independent shared identity limitation.
No named-role field, Requirement prompt change, rank shortcut or REQUIRED bypass was made.
No HNSW/IVFFlat, index build, table copy, SET STORAGE, global setting, memory expansion,
restart, maintenance ANALYZE/VACUUM, cache flush or full-corpus warmup was performed.

<a id="m-3d3d7127ea59"></a>
## Validation and changed files

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Runtime observations and storage decision - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-3d3d7127ea59-0"></a>

Runtime/helper changes: tripworld/retrieval/runtime.py and diagnostics.py; additive report
wiring in services/tripworld_discovery.py. Tests: test_runtime_retrieval.py and
services/test_tripworld_discovery.py. Existing diagnostic script/tests were reused for
regression coverage, not replaced by a benchmark framework.

<a id="b-3d3d7127ea59-1"></a>

Initial affected runtime/diagnostic/service/V2-runner/AcceptanceSession set: 57 passed.
Additional real-stack tests initially yielded 10 passed/1 failed because malformed-JSON
fixture omitted application/json and the SDK legitimately returned text. Correcting the
fixture (not production parsing policy) yielded 11 passed. Subsequent embedding cancellation
and phase assertions: 29 passed across runtime/service; final SQL-vs-phase test brought the
service module to 17 passed. These are overlapping checks, not additive full-suite counts.
Ruff and git diff --check passed. No full backend repeat; earlier full regression stands.

<a id="b-3d3d7127ea59-2"></a>

Coverage includes owned httpx2 sends, zero SDK retries on 429, malformed response metadata,
usage before domain validation, capture off/on same input/result, integrity hashes, capture
write failure isolation, SQL timeout versus caller cancellation, embedding timeout/cancel,
phase expiration, unchanged Google degradation and resource closure. No actual embedding
was obtained. No source-policy, selection, generation, frontend, default engine, B2, database,
commit/push, re-freeze or V3 change. Normal RAG live remains unvalidated.

<a id="m-c25267e4e4c9"></a>
## Bounded read-only diagnosis - 2026-09-20 (no paid calls; fixes pending approval)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._



<a id="m-56364cb891bb"></a>
## Evidence and reproducibility limits

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Bounded read-only diagnosis - 2026-09-20 (no paid calls; fixes pending approval). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-56364cb891bb-0"></a>

Used logs/phase6_acceptance_20260920/{manifest,session_events,session_calls,tokyo_result,
melbourne_result,analysis}.json and both original trace directories. The Tokyo plan,
query texts, embedding usage and runtime errors exist; the embedding response vectors
were NOT saved. Runtime RequestCache was in memory and is no longer available. Therefore
none of these measurements is an exact replay of either Tokyo semantic query.

<a id="b-56364cb891bb-1"></a>

Substitute: the previously saved Phase 5 query `museums and cultural attractions`, checkpoint
d5d9797ff9d60b621f77122755339422df25db54a7bb97089f9b195b401602d2.npz.
phase5_service_smoke.json links that text/checkpoint/space. Validated finite float32 shape
(1,1536), unit norm, response model text-embedding-3-small and vector-byte SHA-256
97988b6ac1c3a4c0e9055f331729491c9464843803f49ea3ef94935f99d2402b.
Runtime.prepare checked the actual artifact, manifest, production policy and embedding space.
No new embedding request. Source/parameter/checksum manifest is saved in
artifacts/diagnostics/retrieval_execution/diagnostic_manifest.json.

<a id="b-56364cb891bb-2"></a>

Tokyo used the captured center (35.6764225,139.650027), 15 km, K=10, country=null.
Melbourne component control used (-37.8136276,144.96305759999998), same radius/K/vector/space.
It did not bypass REQUIRED to run the planner and is not Melbourne end-to-end success.
All connections were read-only and loopback; no corpus export, maintenance, schema/index
change, cache flush, service restart or resource change. Original live artifacts remain intact.

<a id="m-fb1051eb8202"></a>
## Exact timing boundary and observed cancellation

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Bounded read-only diagnosis - 2026-09-20 (no paid calls; fixes pending approval). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-fb1051eb8202-0"></a>

Runtime.prepare has separate connection (2 seconds) and compatibility SQL (3 seconds)
bounds. The connection is autocommit with default_transaction_read_only=on and a server
statement_timeout. Runtime.search wraps BOTH `await conn.execute` and `await cursor.fetchall`
in the client SQL timeout. Query construction/vector validation happens before that wrapper;
artifact checking and ranked domain dictionaries happen after it. execute includes server
execution and libpq result receipt; fetchall performs row decoding. It is not correct to
label all execute time as CPU, or to infer the original live fetch stage from its old trace.

<a id="b-fb1051eb8202-1"></a>

All diagnostic timeouts occurred before execute returned; fetchall/domain mapping did not
start. Completed Tokyo normal fetch/decode was 0.000219 seconds; Melbourne 0.000307 seconds.
Compatibility/connection succeeded separately. Client exception chains on attempts 1/6/8
were TimeoutError -> CancelledError, with no surfaced PostgreSQL SQLSTATE. Attempt 2 surfaced
psycopg QueryCanceled, SQLSTATE 57014, consistent with the configured 15-second server limit
winning the race. 57014 alone does not identify every possible cancellation cause; the script
saved structured types/code, not server diagnostic message_primary. The original live did
not capture that code or cancellation detail, so its exact server/client race remains unknown.

<a id="b-fb1051eb8202-2"></a>

After every executed search, transaction status was IDLE, a SELECT 1 probe succeeded, and
the owned connection closed normally. No background search or retry was scheduled. User
cancellation was not injected. Monitors were read-only and canceled/awaited in cleanup.
The live RAG elapsed 6.205 seconds remains a SQL-suboperation timeout, not an exhausted
30-second phase. Its current deadline_limited status conflates these two cases.

<a id="m-906f3e3f8bd4"></a>
## Eight-search execution ledger

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Bounded read-only diagnosis - 2026-09-20 (no paid calls; fixes pending approval). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-906f3e3f8bd4-0"></a>

No more retrieval executions were performed after number 8. Plain EXPLAIN, settings/index/
statistics reads and bounded pg_stat_activity samples were not retrieval executions. A
mistyped checkpoint path failed before connecting; it did not consume a search. Each row
used a new connection, NOT a claimed cold cache. Earlier partial/failed reads can warm later
runs; EXPLAIN ANALYZE overhead and omitted result transfer differ from ordinary queries.

<a id="b-906f3e3f8bd4-1"></a>

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

<a id="b-906f3e3f8bd4-2"></a>

Small overrun beyond a timeout includes cancellation/cleanup scheduling, not another search.
No consistent cold/warm latency claim or percentile estimate is justified. In particular,
number 4 does not establish reliable sub-three-second Tokyo execution.

<a id="m-b87e3393d3ad"></a>
## SQL and plan findings; historical comparison

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Bounded read-only diagnosis - 2026-09-20 (no paid calls; fixes pending approval). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b87e3393d3ad-0"></a>

The exact parameterized SQL is saved with each measurement. Its execution structure is:

<a id="b-b87e3393d3ad-1"></a>

1. Materialized geographic CTE: discovery_allowed plus latitude/longitude bounding box;
   runtime also applies exact production policy_version and artifact_hash.
2. Great-circle radius <=15 km +1e-9; join embeddings by text_hash AND space_id.
3. Exact `1 - (embedding <=> query_vector)` per eligible entity; descending similarity,
   entity ID COLLATE C tie-break, LIMIT 10 in materialized ranked CTE.
4. Fetch entity metadata by primary key for ONLY the ten winners; final stable sort.

<a id="b-b87e3393d3ad-2"></a>

There is no pre-Top-K loading of full entity metadata in the SQL projection. The physical
entity heap still occupies many pages; projection alone does not make those pages narrow.
Existing indexes include latitude/longitude B-trees, entities primary key and embeddings
(space_id,text_hash) primary key. No ANN/PostGIS was used or proposed as this diagnosis.

<a id="b-b87e3393d3ad-3"></a>

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

<a id="b-b87e3393d3ad-4"></a>

Completed Melbourne plan: 284 geographic/circle rows (estimate 1), no temp spill; 2,118 shared
hits and 800 reads. This independently confirms that the runtime adapter can return ten
results from a lower-density scope with the saved vector.

<a id="b-b87e3393d3ad-5"></a>

Wait samples: number 4 saw six IO/DataFileRead and four active/no-wait samples; number 6 saw
25 DataFileRead and three active/no-wait; number 8 saw 116 DataFileRead, six DataFilePrefetch,
14 active/no-wait and one ClientRead sample. All sampled blocker lists were empty. Early
attempts 1-3 were not sampled. This supports I/O-sensitive high-density exact retrieval,
not demonstrated lock contention, result decoding, or a phase deadline failure. It does not
pin the original live stall to a specific host/Docker/disk event or prove no transient lock
could ever have occurred. Underestimation and CTE spill are secondary efficiency concerns;
this evidence does not prove fixing either alone removes the latency variation.

<a id="b-b87e3393d3ad-6"></a>

Phase 5 and runtime call the SAME search_query builder. Runtime adds only the policy/artifact
predicates, bounded async execution and post-fetch compatibility/rank construction; no new
join or early payload projection. Applying identical data conditions to the historical
builder produces byte-identical SQL (verified offline and hashed). Removing these conditions
would change the eligible universe, so no misleading unrestricted-old-vs-restricted-new
latency comparison was run. Prior historical Melbourne latency is not a Tokyo baseline.
No alternative SQL rewrite was executed: current evidence does not justify selecting one
as a proven repair within the eight-execution cap. Same-query successful repetitions are
performance observations, not a claim that original Tokyo vector identities were replayed.

<a id="m-1ce7e7a29498"></a>
## Melbourne identity evidence and replay

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Bounded read-only diagnosis - 2026-09-20 (no paid calls; fixes pending approval). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-1ce7e7a29498-0"></a>

Original named intent is REQUIRED with place_text Queen Victoria Market and a valid source
span. NamedRequirementDraft/NamedRequirement and the bridged NamedPlaceIntent have no target
role/type constraint. The source text is only the proper name, not an explicit market-vs-
station clarification. No role can be mechanically recovered by matching words in that name.

<a id="b-1ce7e7a29498-1"></a>

| Candidate | Actual primaryType | Coordinates | Source / rank (one-based) |
|---|---|---|---|
| ChIJsVeQNzRd1moRUNQyBXZWBA8 | market | -37.8075798,144.956785 | named search / 1 |
| ChIJlXQB4zVd1moRA3CXTTHAfB0 | transit_station | -37.8094414,144.955869 | same named search / 8 |

<a id="b-1ce7e7a29498-2"></a>

Both names are exactly Queen Victoria Market and both statuses OPERATIONAL. Market address
is Queen St, Melbourne VIC 3000; station address Melbourne VIC 3000. Neither exact-name
candidate appeared in the saved default top-attractions/local-food responses. Thus these
sources do not provide independent corroboration selecting one identity. Provider rank is
not an identity guarantee; both positions are plausible within the same destination.

<a id="b-1ce7e7a29498-3"></a>

Offline replay of the exact-name subset through current merge/resolver produced
ambiguous_exact_name with both IDs. Type, coordinates and QueryIntentHit provenance survived
merge; they were NOT lost by mapping. Resolver builds a normalized-name -> ID-set and
accepts exactly one ID. It does not use types/position/rank to break this ambiguity. This
is conservative behavior, not automatically a bug: provider types distinguish the objects,
but the current user contract does not tell code which role to require.

<a id="b-1ce7e7a29498-4"></a>

Recommended initial decision: keep clarification for this saved request. An optional future
minimal extension, separately approved, is a nullable registered expected_primary_type on a
named requirement with source provenance, populated by the existing interpreter only from
explicit user role wording (not a proper-name suffix or model world knowledge). No second
LLM and no universal preference taxonomy. A deterministic identity filter may reject a
known incompatible type only when that typed requirement exists. A missing candidate type
remains unresolved, not rejected to manufacture uniqueness.

<a id="b-1ce7e7a29498-5"></a>

| Counterexample | Proposed behavior if extension approved |
|---|---|
| Explicitly visit the market | market target plus known market/station types can select the sole compatible market |
| Explicitly visit the station | station target can select that station; no global transit exclusion |
| Two plausible same-name markets | clarify; type does not uniquely identify |
| Type missing on a competing identity | clarify; UNKNOWN is not evidence of incompatibility |
| No explicit role or sufficient identity/location evidence | clarify; retain REQUIRED |

<a id="b-1ce7e7a29498-6"></a>

Extending this contract would require named schema/DTO/prompt/mapping/bridge/resolver tests;
it is NOT implemented here and is not prerequisite to component SQL diagnosis.

<a id="m-19e6ab2619d3"></a>
## Embedding observer diagnosis and proposed local fix

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Bounded read-only diagnosis - 2026-09-20 (no paid calls; fixes pending approval). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-19e6ab2619d3-0"></a>

The installed default AsyncOpenAI client is AsyncHttpxClientWrapper whose send method is
httpx2._client.AsyncClient.send. The live observer patched httpx.AsyncClient.send, so it
captured Google but not that default embedding transport. Existing AcceptanceSession
explicitly owns its model client and its own hooks, explaining why model HTTP counts worked.
SDK batch success and usage remain valid; historical independent embedding HTTP count stays
UNKNOWN. Do not rewrite it to zero or an inferred one.

<a id="b-19e6ab2619d3-1"></a>

Proposed repair: attach request/response hooks to the actually owned embedding HTTP client
(or inject a scoped DefaultAsyncHttpxClient with hooks through the existing factory), with
unique attempt IDs and no credential logging. Preserve max_retries=0, timeouts and ownership;
remove hooks/close once. No new global monkeypatch or replacement harness. The new offline
MockTransport test demonstrates default httpx2 hooks observe one send even while patched
httpx.AsyncClient.send would raise. This is proof of the local observation mechanism, not a
production telemetry change or a paid test. Follow-up tests should cover 429/error/no retry,
SDK mapping failure, cancellation and separation of SDK-call vs HTTP-attempt counters.

<a id="m-8ea3e07f972f"></a>
## Conditional regression and bounded V2 live checkpoint - 2026-09-20

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-4a1077481a18-0"></a>

Status: **Full standard backend regression passed; Google-only degradation exercised;
normal RAG integration is NOT live-validated. Not Frozen.**

<a id="b-4a1077481a18-1"></a>

This checkpoint supersedes current incomplete-regression/no-live status, not the dated
2026-09-19 history below. The earlier collection failure remains a failed collection
attempt, not a retrospective green run. No implementation, prompt, configuration,
budget or algorithm changed in this checkpoint. No retry, replacement sample or third run.

<a id="m-41e18abe8455"></a>
## Regression and preflight

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Conditional regression and bounded V2 live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-41e18abe8455-0"></a>

One standard `python -m pytest backend/tests -ra --tb=short` execution (with JUnit output):
869 collected, 860 passed, 9 skipped, 0 failed, 0 errors, exit 0, 21.11 seconds.
External network remained blocked by the normal test fixture; TRIPWORLD_TEST_DATABASE=0.
Ruff (`backend scripts`) and git diff --check passed. No repeated full suite.
Each following existing skip requires explicit TRIPWORLD_TEST_DATABASE=1 for isolated local
PostgreSQL tests; these database-writing opt-in tests were not enabled:

<a id="b-41e18abe8455-1"></a>

- `test_real_migrations_extension_and_checksum`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.
- `test_real_ingestion_idempotence_text_change_and_vector_invalidation`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.
- `test_real_exact_geo_alias_policy_and_ties`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.
- `test_real_incompatible_space_rejected`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.
- `test_real_stale_policy_rejected`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.
- `test_real_readonly_search_and_missing_space_before_api`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.
- `test_real_bad_snapshot_rolls_back_without_losing_entities`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.
- `test_real_geo_pole_and_box_corner`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.
- `test_real_build_resume_and_no_api_for_unchanged_text`: Set TRIPWORLD_TEST_DATABASE=1 for isolated local PostgreSQL tests.

<a id="b-41e18abe8455-2"></a>

AcceptanceSession capture/resource readiness and RuntimeRetrieval.prepare passed before
paid dispatch. Local compatibility check took 0.043 seconds, with no paid probe, corpus
scan, migration or DB write. Live used the existing AcceptanceSession, real run_v2 and
Windows SelectorEventLoop; product/default engine stayed unchanged. Source/config hashes
were unchanged after both runs. UTC artifact timestamps on September 19 correspond to
September 20 in Australia/Sydney.

<a id="m-d972f22b9c15"></a>
## Frozen inputs and identity

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Conditional regression and bounded V2 live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-d972f22b9c15-0"></a>

Reference date: 2026-09-20. Both requests: planning_request_2, 2026-09-21 through
2026-09-23, three travelers, total-trip budget; final output contract itinerary_2.
Tokyo: Tokyo, Japan; 180000 JPY; exact preferences:
`I definitely want to visit Meiji Jingu. I prefer small museums and places with distinctive local architecture.`
Melbourne: Melbourne, Australia; 1800 AUD; exact preferences:
`I definitely want to visit Queen Victoria Market.`
Both requested V2 and dispatched backend.app.versions.v2.runner.run_v2 once.

<a id="b-d972f22b9c15-1"></a>

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

<a id="m-9befcde032b4"></a>
## Actual RAG funnel and failure boundaries

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Conditional regression and bounded V2 live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-9befcde032b4-0"></a>

Tokyo interpreter produced discovery_1 `places with distinctive local architecture`
(semantic_2) then discovery_2 `small museums` (semantic_1). Both are user-derived queries;
no default or invented preference. Scope: (35.6764225, 139.650027), 15 km, no country filter.
One query embedding batch succeeded (7 prompt/total tokens, 3.088 seconds). Read-only
runtime prepare took 0.030 seconds. The FIRST exact SQL search timed out after 3.001 seconds;
the second was not dispatched. No SQL result set was returned: this is NOT a successful
zero-row query or a measurement of Tokyo corpus coverage. RAG phase took 6.205 seconds.
The existing diagnostic says deadline_limited / TimeoutError; the observed cause is the
3-second SQL suboperation bound, NOT exhaustion of the 30-second phase deadline.

<a id="b-9befcde032b4-1"></a>

Returned positions, unique entities, cheap entity scan, resolution attempts, incremental
Details/fallback, overlap, new/mixed canonical IDs and every RAG downstream fate count
were zero. Google observations survived unchanged. Its funnel had 41 raw observations,
40 merged identities, 20 admitted, 10 Details-enriched, 8 supplied (1 REQUIRED + 7 OPTIONAL),
7 scheduled. All supply/scheduled identities are Google-only discovery. Extinct Media
Museum was supplied but not scheduled. No RAG-only/mixed admission, enrichment, supply,
scheduled or Nearby-only contribution can be claimed.

<a id="b-9befcde032b4-2"></a>

Melbourne preference interpretation succeeded, with a REQUIRED Queen Victoria Market and
no DiscoveryIntent. Google performed destination, named-place and two normal default
searches (top attractions/local food). Exact display-name matches included both the market
ChIJsVeQNzRd1moRUNQyBXZWBA8 and transit station ChIJlXQB4zVd1moRA3CXTTHAfB0.
Existing unique-exact-name resolution therefore raised ClarificationRequired:
unresolved_named_identity, before the RAG extension. This was NOT an empty Google response,
a missing REQUIRED preference, or a RAG failure. No RAG query plan, embedding, SQL, supply,
generation or Nearby executed. The intended RAG default branch remains uncovered; no
replacement request or forced resolution was used. No Melbourne itinerary exists.

<a id="m-5a464369a181"></a>
## Actual Tokyo itinerary and independent references

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Conditional regression and bounded V2 live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-5a464369a181-0"></a>

Times below are actual model output in Tokyo local time (+09:00). No activities were added
by the reviewer. Each main identity is Google-only discovery and belongs to main supply.

<a id="b-5a464369a181-1"></a>

| Date | Time | Actual main place | Canonical ID |
|---|---|---|---|
| 2026-09-21 | 09:00-11:00 | Meiji Jingu | ChIJ5SZMmreMGGARcz8QSTiJyo8 |
| 2026-09-21 | 13:00-15:00 | Samurai Museum TOKYO Shinjuku | ChIJA5gBoXeNGGARJqJqceqLJiQ |
| 2026-09-22 | 10:00-12:00 | Former Prince Asaka Imperial Family Residence | ChIJ41V6qRuLGGAR3hfLAFHax1A |
| 2026-09-22 | 12:10-13:30 | Tokyo Metropolitan Teien Art Museum - Japanese Garden | ChIJ2zLblLSLGGARkGjOdSu0RWY |
| 2026-09-22 | 16:00-17:30 | Japan Traditional Crafts Aoyama Square | ChIJ91khboGMGGARBo42MbnQzg8 |
| 2026-09-23 | 11:00-12:30 | Shinkenchiku-sha Co.,Ltd. Aoyama House | ChIJNZIv-5yMGGARFvzvvuyxaQg |
| 2026-09-23 | 14:00-15:30 | Shinjuku Gyoen Museum | ChIJ5RR13yiNGGART-NAUWZQ2bE |

<a id="b-5a464369a181-2"></a>

REQUIRED Meiji Jingu was scheduled. Seven unique linked IDs, zero unlinked activities,
zero repeated canonical visits, no empty day, one unused supplied ID. All seven costs
are null: budget feasibility is not proven. Opening-hour baselines are explicitly qualified
as not proving date-specific exceptions. Weather returned HTTP 404 and was unavailable.
Claims such as small/compact museum suitability remain semantic judgments, not validated
size facts; the wording "measured transfer interval" should not be treated as a verified
route for every transfer. Structural success does not prove all free text or feasibility.

<a id="b-5a464369a181-3"></a>

Three actual Nearby searches returned ten results each; three final references, all outside
main supply, not counted as scheduled visits, costs or REQUIRED satisfaction:

<a id="b-5a464369a181-4"></a>

| Reference | Scheduled anchor/date | Type | Straight-line distance |
|---|---|---|---|
| Treasure Hall Lawn | Meiji Jingu / 2026-09-21 | park | approximately 337 m |
| Bikkuri Donkey | Samurai Museum TOKYO Shinjuku / 2026-09-21 | restaurant | approximately 0 m |
| Tokyo Metropolitan Teien Art Museum | Former Prince Asaka Imperial Family Residence / 2026-09-22 | museum | approximately 42 m |

<a id="b-5a464369a181-5"></a>

These reasons were application templates from actual Nearby evidence. Source refs in the
raw final artifact are google_places_nearby:<actual-call-id>:<index>. Zero metres is rounded
coordinate distance, not proof of identical identity or zero walking. The museum/reference
and scheduled residence/garden may overlap as a visitor experience despite different IDs;
canonical deduplication does not prove distinct attractions. No live correction was made.
All reasons retain unverified availability/prices/accessibility and straight-line-not-route
uncertainty. IDs/names/addresses came from Google evidence, not model-created sources.

<a id="b-5a464369a181-6"></a>

Nearby used the approved 3 requests, 10 candidates/request, 800 m, DISTANCE, mixed four
types, 300 m non-transitive anchor reuse, 10-second phase/4-second request limits, no retry.
The garden reused the residence region. Crafts Aoyama, Aoyama House and Shinjuku Gyoen
Museum anchors were uncovered by the three-region limit. No extra discovery for coverage.
Nearby status completed, 2.5 seconds, three references. Main itinerary fields (including
all dates/times/order/identities/notes/costs) matched the pre-Nearby snapshot exactly:
`a1158e7ead86ea2893e311a44507c572c02df56a7cc04fbe7271a1cda4473c79` before and after (excluding references).

<a id="m-7ade772df530"></a>
## Calls, usage, capture and uncovered paths

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Conditional regression and bounded V2 live checkpoint - 2026-09-20. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-7ade772df530-0"></a>

| Work | Tokyo | Melbourne |
|---|---:|---:|
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

<a id="b-7ade772df530-1"></a>

Routes comprised baseline 64 elements and eight alternative elements over three additional
requests. Provider workload is not an invoice. No second interpreter, repaired generation,
planner rerun, hidden harness retry, or reference model call was introduced.

<a id="b-7ade772df530-2"></a>

| Model task (gpt-5.6-luna) | Input | Output (includes reasoning) | Reasoning | Cached input | Cache write | Total |
|---|---:|---:|---:|---:|---:|---:|
| Tokyo requirement | 3939 | 652 | 324 | 0 | 3936 | 4591 |
| Tokyo itinerary | 20323 | 1920 | 516 | 0 | 20320 | 22243 |
| Melbourne requirement | 3928 | 145 | 46 | 3807 | 118 | 4073 |

<a id="b-7ade772df530-3"></a>

Embedding usage is separately 7 prompt/total tokens; do not add reasoning/cache again.
Provider-reported model durations: 6, 14 and 2 seconds respectively (integer timestamps).
Tokyo main completion: 44.316 seconds; RAG included therein: 6.205; Nearby: 2.5;
total: 46.836. Melbourne total: 5.455 seconds, failed before generation.

<a id="b-7ade772df530-4"></a>

Model SDK/HTTP/domain and Google transport captures were preserved with unique call/attempt
IDs. Session closed its owned client once; capture_errors empty; both file tracers healthy.
A measurement limitation remains: the scoped generic HTTP observer did not intercept the
embedding client's transport. Its successful single SDK batch, usage, timing and configured
zero retries are captured, but independent embedding HTTP-send count is UNKNOWN, not a
claimed measured one. This gap does not justify repeating the paid operation.

<a id="b-7ade772df530-5"></a>

Observed request caches had no hits; RAG Details reuse/overlap/free merge/negative-cache
boundaries were not live exercised. Offline tests, not these samples, cover them. SQL timeout
returned control with no subsequent SQL dispatch; user cancellation was not exercised.
Normal SQL completion, identity fallback, RAG source union, admission field parity with
RAG Details, RAG supply/scheduled contribution, default RAG query, and reference failure
isolation remain unexercised by this live pair. No live faults were injected.

<a id="b-7ade772df530-6"></a>

Recommendation: **only Google-only degradation has successful end-to-end live evidence;
normal RAG is still unvalidated.** A separately approved narrow investigation should inspect
the exact geographic SQL execution under the existing three-second bound and the inherited
market/station identity ambiguity; do not assume a larger timeout or looser identity rule is
the solution. No new architecture, tuning, paid run or implementation fix is authorized here.

<a id="b-7ade772df530-7"></a>

Artifacts are ignored under logs/phase6_acceptance_20260920: manifest, regression/JUnit,
preflight, per-case results, raw session calls/events, traces and analysis.json. The original
external source snapshot was unchanged during that checkpoint; it was subsequently deleted
by user authorization and is not a current recovery entry. No corpus/vector/DB write, frontend/default
change, B2 cleanup, stage/commit/push, re-freeze or V3 work. This is development evidence,
not a formal V1/V2 comparison or complete correctness proof.

<a id="m-5cdc4c5e28e5"></a>
## Implementation checkpoint - 2026-09-19

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-5cdc4c5e28e5-0"></a>

The user approved Current A-K with a counting correction: scan at most 20 returned
positions, union all valid origins, and charge the six-entity limit only to independent
entities needing new resolution. Existing Google/request-resolved canonical IDs do not
consume that limit or trigger validation Details. Failure consumes an attempted entity;
this is not a six-success target. No source quota, adaptive K or extra retrieval pass.

<a id="m-44c018d06535"></a>
## Implemented wiring and ownership

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Implementation checkpoint - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-44c018d06535-0"></a>

`run_v2` / `scripts/run_v2.py` explicitly select SystemVersion.V2. The existing tools
runner and graph construction now expose shared functions; V1 remains an independent
Google-only wrapper. V2 injects TripWorldDiscovery into PlanningCandidateSupplyPipeline
only after original named identity/conflict handling and before factual admission.
No full graph copy or restored evaluator. Product/API default and frontend are unchanged.

<a id="b-44c018d06535-1"></a>

The shared builder remains in versions/v1/graph.py as build_tools_graph; the shared
runner remains in versions/v1/runner.py as run_tools_planner. Small explicit V2 wrappers
reuse them, avoiding a larger directory migration. The canonical origin union lives in
services/tripworld_discovery.py; the original Google merge is unchanged. V2 result adds
rag_discovery diagnostics in versions/v2/state.py, while final itinerary_2 is unchanged.
Existing acceptance_session is runner-agnostic and needs no new harness or modification.

<a id="b-44c018d06535-2"></a>

Shared changes are limited to nullable absent Google rank, validated TripWorld origins,
source-neutral intent links, origin preservation through Details, a read-only cache lookup,
explicit extension injection, version-aware CLI dispatch and independent runtime config.
New code lives in schemas/tripworld_discovery.py, policies/tripworld_query_plan.py,
services/tripworld_discovery.py, tripworld/retrieval/{runtime,query_tokens}.py,
versions/v2/{config,graph,runner,state}.py and scripts/run_v2.py. V1 rejects hidden runtime
retrieval injection. Supply algorithm, interpreter/generation prompts and Nearby policy
are unchanged; historical B2 files are retained.

<a id="b-44c018d06535-3"></a>

RuntimeRetrieval uses AsyncOpenAI with zero retries and psycopg async read-only connections.
It reads existing complete-build/manifest metadata, checks the DB space/build/current
sample policy, and restricts retrieval SQL to the expected artifact/policy. It never
migrates, regenerates corpus vectors or writes checkpoints. Compatibility checks are
bounded reads, not a full-corpus integrity audit. Query tokenization uses verified local
cl100k_base assets and never downloads missing vocabulary at runtime. Missing assets or
credentials cause explicit RAG degradation without affecting the independent Google path.

<a id="b-44c018d06535-4"></a>

V2 CLI supports `--rag-env-file` for explicitly supplied local DB/embedding settings.
Install the existing retrieval dependency group. On Windows the V2 CLI uses a selector
event loop for psycopg; callers embedding run_v2 in another host must provide a compatible
async loop. A Proactor-host incompatibility degrades RAG, rather than creating a background
thread or starting a replacement database. V1 event-loop defaults remain unchanged.

<a id="b-44c018d06535-5"></a>

Approved runtime defaults are in config/runtime.yaml: <=2 queries, Top-K 10, <=20 slots,
<=6 NEW-resolution entities, <=8 incremental Details, <=2 fallback searches, 15 km scope,
1 km identity tolerance, one embedding batch, 30-second phase, 8/3/2/4-second embedding/
SQL/connect/Google bounds and retry=0. Main C/R/K and Nearby limits are unchanged.
Details worst-case is 18+8=26; candidate/fallback search is 12+2=14, plus destination<=1
and Nearby<=3. These are maximum workloads, not prices or expected bills.

<a id="b-44c018d06535-6"></a>

Compatible early Details use the SAME RequestCache keys and _ProviderResult values as
normal enrichment. Rating/full evidence remains hidden from admission. Actual provider
errors may be negatively cached; budget refusal, stage interruption, cancellation and
RAG dependency failure are never stored as a Google identity failure. Interrupted I/O
is cancelled/awaited, and user cancellation propagates. Unknown or invalid queries are
recorded; the original Google request can continue without a second interpreter.

<a id="b-44c018d06535-7"></a>

Diagnostics record query sources/refs/scope, returned slots, unique entities, Google overlap,
resolution attempts, actual provider invocation counts/cache hits, stops, new versus mixed
canonical IDs and origins. Admission and final fate distinguish ineligible/capacity,
enrichment not attempted or failed, enriched-but-not-supplied, supplied-but-not-scheduled,
scheduled, and separately Nearby-only identities. Provenance alone is not improved quality.

<a id="m-ff5224c4e5a6"></a>
## Historical recovery baseline (subsequently deleted)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Implementation checkpoint - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ff5224c4e5a6-0"></a>

Historical snapshot (permanently deleted on 2026-09-20; not a recovery entry): `D:/Workspace/Capstone/phase6_source_snapshots/20260919T113719Z`.
The then-created manifest contained HEAD, status, 306 whitelisted files with SHA-256 and 11 tracked missing
migration files. Manifest SHA-256:
`c4b0f98cddcd7fa04e8f0571957fb703d1ad6122d44d7e5a6ceae0d64061b257`.
The whitelist includes the tracked tiny Parquet fixture and four unchanged TripWorld JSON
configuration/manifests; production datasets/vectors are excluded. All snapshot hashes
were verified at creation. Recovery then required the recorded HEAD, source overlay and listed
migration deletions. The later authorized deletion removed the overlay and manifest; those
uncommitted intermediate states can no longer be restored from this snapshot. It had preserved
the then-active semantic_poi_pipeline.py and retained B2 sources. Env/credentials,
environments, production datasets, DB files, private captures and thesis archives were not
copied. Ignored thesis_notes and logs stay at their original repository-local locations.
No Git staging/commit or re-freeze occurred.

<a id="m-cd6710c05821"></a>
## Validation record (do not rewrite the failed full attempt)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Implementation checkpoint - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-cd6710c05821-0"></a>

- Focused shared/V2/reference/config checks: **91 passed** before the full attempt.
- The ONE full backend invocation stopped during collection with **1 error**, caused by
  a test_runner module-name collision between the new V2 test and V0. No test execution
  completed in that invocation; it is not a full-suite pass.
- Renamed the new module to test_v2_runner.py. Affected V0/V1/V2 runner tests: **14 passed**.
- After refining admission/final-fate diagnostics, affected discovery and V1/V2 graph
  modules: **29 passed**. No second full backend run was made.
- Ruff and git diff --check passed. Earlier historical 829/9/8 and 53-test results remain
  historical, not evidence that this new full attempt passed.
- One authorized local PostgreSQL integration check passed: transaction_read_only=on,
  async compatibility checks plus one Melbourne 15-km exact query returned ten results.
  It reused a saved query vector with model/dimension/hash verification. Embedding sends=0;
  no data writes, migrations or rebuilds. This is adapter execution evidence, not relevance
  validation or a fresh corpus coverage measurement.

<a id="b-cd6710c05821-1"></a>

Local records: artifacts/validation/rag_integration/{backend_full.txt,runner_affected.txt,
discovery_affected.txt,local_db_readonly.json}. No real Google, embedding or generation
model calls. Unit network safeguards and MockTransport/fake DB/providers were used.

<a id="b-cd6710c05821-2"></a>

Full-backend regression acceptance remains incomplete despite the corrected collection
issue and passing affected tests. Recommend explicit authorization for one fresh complete
regression check before any V2 paid/live acceptance; do not declare V2 frozen or generally
correct. Further limits include conservative alias/geography misses, sparse coverage,
no guaranteed net-new/scheduled RAG contribution and possibly paid Details later discarded
by common admission. Nearby does not fix sparse primary itineraries or date coverage.

<a id="m-5ebd49a38905"></a>
## Phase 6 normal-path development validation - 2026-09-20

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-cb0e66f7464f-0"></a>

The user deferred inline/PLAIN copying and approved an explicit V2-only waiting override:
SQL 60 seconds, phase 180, with all existing work ceilings/retries unchanged. Defaults remain
3/30; config/v2_development_override.json is explicitly loaded per development call. This is
functional waiting allowance, not a database optimization or production SLA.

<a id="b-cb0e66f7464f-1"></a>

94 affected offline tests passed, then exactly two actual local original-SQL checks returned
10 valid, identically ordered results (23.915 s and 0.963 s). Compatible saved diagnostic
vector only; no claim of exact replay of missing historical Tokyo vectors. These gates
triggered the single authorized fresh Tokyo run_v2. It completed in 71.052 s; both real SQL
queries completed, six new identities resolved, three RAG-only candidates admitted and Beni
Museum reached normal supply and the actual itinerary. No mixed overlap in this sample.

<a id="b-cb0e66f7464f-2"></a>

RAG elapsed 30.619 s; partial means 14 entities unattempted under the six-resolution cap,
not SQL failure. Actual main output: four Google-only +one RAG-only POIs and three separate
Nearby references. Actual query vectors and HTTP attempts are now captured/verified. One
Details cache hit preserved reuse. Weather 404, unknown costs, execution variance and
Melbourne ambiguity remain. Normal RAG now has bounded development-live evidence; no
re-freeze, production default change, storage migration or further live is implied.

<a id="b-cb0e66f7464f-3"></a>

Full inputs/hashes, funnel, actual itinerary, tokens and limits are in the existing Phase 6
proposal. Original 3/30 failures, 1.13-to-15-second history, TOAST diagnosis and deferred shadow
proposal are preserved. No commit/push, frontend change, B2 cleanup or V3.

<a id="m-743413ccdd10"></a>
## Phase 6 telemetry repair and storage decision - 2026-09-20

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-743413ccdd10-0"></a>

Local runtime diagnostics now distinguish SQL/phase timeout, execute/fetch, SQLSTATE and
caller cancellation. Embedding hooks observe the actual owned httpx2 client. Explicit opt-in
development capture saves query vectors with space/text/vector hashes, without raw query
text; default capture remains off. Affected offline tests passed; no full-suite repetition.

<a id="b-743413ccdd10-1"></a>

Read-only storage/resource checks support Decision B: vectors are EXTERNAL with a 4.73 GB
TOAST heap, while the current exact query compares about 44k Tokyo entities. No justified
SQL/session-only change was selected; the approved early stop was used (zero new retrieval
executions, no speedup/equivalence claim). Propose separately approving one inline-vector
shadow-table experiment, using existing vectors and preserving the original table/runtime.
It requires copy/WAL/disk space, but no embedding regeneration or inherent restart.
Full evidence and approval gates are in the existing Phase 6 proposal. No production SQL,
timeout, named-role contract, storage, index or Docker setting changed. No paid/live calls,
commit/push/re-freeze. Normal RAG live remains pending; Melbourne clarification is unchanged.

<a id="m-6f93e42c41c3"></a>
## Phase 6 targeted diagnosis - 2026-09-20

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6f93e42c41c3-0"></a>

Eight bounded local read-only retrieval executions and no paid/external calls. Original live
query vectors were absent; the compatible saved Phase 5 vector is a performance control,
not exact Tokyo replay. Tokyo execute-stage timeouts and plans show high-density exact
search with substantial page reads, row-count underestimation and geographic CTE spill;
latency varied from 1.130 seconds to beyond 15 seconds. Fetch/decode was negligible when
completed, sampled blockers were empty, cancellation returned IDLE and connections closed.
Melbourne component retrieval completed in 0.0176 seconds; this does not resolve REQUIRED.

<a id="b-6f93e42c41c3-1"></a>

Same-name market/station types and provenance survive merge. Current named intent has no
explicit target role, so conservative clarification remains appropriate. SDK HTTP count gap
was traced to the default OpenAI httpx2 client versus an httpx observer. Five diagnostic tests
passed, including fake-transport hooks; production hashes/configuration remain unchanged.
See the existing Phase 6 proposal for the bounded measurement table and separately approvable
telemetry/performance/optional identity-contract work. No production timeout increase or
SQL rewrite is justified as a proven fix yet. Normal RAG live acceptance remains pending.

<a id="m-8bb3c5c63a25"></a>
## Phase 6 conditional acceptance - 2026-09-20

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8bb3c5c63a25-0"></a>

Full standard backend suite: 869 collected, 860 passed, 9 existing opt-in PostgreSQL skips,
zero failures/errors, exit 0; Ruff/diff passed. The dated collection failure below remains
historical. Production code/configuration were unchanged. Actual run_v2 dispatched Tokyo
and Melbourne once each through existing AcceptanceSession; no replacement runs.

<a id="b-8bb3c5c63a25-1"></a>

Tokyo: embedding succeeded; first exact SQL timed out at its 3-second suboperation bound
(RAG elapsed 6.205 seconds, not the 30-second total deadline). Google-only degradation
completed: eight supplied, seven scheduled including REQUIRED Meiji Jingu, three independent
Nearby references; main unchanged. No RAG candidate contribution. Weather HTTP 404.
Melbourne: REQUIRED Queen Victoria Market had same-name market/transit identities and
stopped with unresolved_named_identity before RAG/generation; no itinerary exists.

<a id="b-8bb3c5c63a25-2"></a>

Normal RAG is NOT development-live-validated. Only Google-only degradation has successful
end-to-end evidence. Successful SQL/resolution/merge, RAG contribution and default query
remain uncovered. Embedding SDK usage was captured, but independent embedding HTTP count
was not; capture limitation is retained, not filled by inference. No tuning or fix was made.
Full results, exact inputs/hashes, actual itinerary, calls and limitations are recorded in
[Phase 6 proposal](v2-development.md). Artifacts: logs/phase6_acceptance_20260920.
No commit/push/re-freeze, rebuild, B2 cleanup or V3. Next work requires separate approval.

<a id="m-25a0adbf1fc0"></a>
## Phase 6 runtime integration - 2026-09-19 (Implemented; limited offline evidence)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-25a0adbf1fc0-0"></a>

The user approved the existing Phase 6 Current A-K design, correcting the six-entity
count: known Google/request-resolved canonical IDs merge provenance without consuming
NEW-resolution attempts. At most 20 returned slots, six such attempts, eight incremental
Details and two fallback searches; no success quota or adaptive retrieval. An external
306-file baseline preserves active source and B2 history before migration, excluding
production data, credentials and ignored archives.

<a id="b-25a0adbf1fc0-1"></a>

V2 now has explicit runner/CLI dispatch and injects bounded TripWorld main discovery before
common admission. Existing Google merge/named resolution, deterministic supply, selective
Reviews/Profile, primary generation and post-itinerary Nearby remain shared. Static origins
stay distinct from current evidence; early Details reuse the existing request cache at the
normal stage. Query defaults do not masquerade as user intent. B2 is neither deleted nor used.

<a id="b-25a0adbf1fc0-2"></a>

Offline evidence: 91 focused passes. The sole full backend attempt stopped with one collection
error because V2 test_runner collided with V0; it did not execute the suite. Renaming to
test_v2_runner resolved that issue, with 14 affected runner tests passing. Later diagnostic
refinement passed 29 affected tests. Full-suite acceptance remains incomplete; no second
full invocation was made. One authorized local read-only PostgreSQL check passed using a
saved query vector, ten returned rows and zero embedding calls. Ruff and diff checks passed.

<a id="b-25a0adbf1fc0-3"></a>

No real generation/embedding/Google calls, V2 live, rebuilds, B2 cleanup, frontend change,
stage/commit/push or re-freeze. Tokyo positive-discovery and Melbourne named-only requests
are proposals for later bounded live approval, not executed experiments. A fresh complete
regression check should be separately approved before live acceptance. The original proposal
and older Q_rel/B2 histories below remain historically accurate for their dates.

<a id="m-0a2db7988bbf"></a>
## V2 TripWorld integration - 2026-09-19 (implemented; no V2 live)

_Source context: Current V1/V2 POI Planning Candidate Supply. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ff970e716b21-0"></a>

V1 keeps Google discovery. V2 now reuses the same tools graph and deterministic supply,
injecting bounded TripWorld discovery after Google merge and REQUIRED/EXCLUDED resolution,
before factual eligibility/admission. run_v2 is independent; the product default is unchanged.
V0 remains tool-free. Old evaluator/subset-selection code remains inactive and retained.

<a id="b-ff970e716b21-1"></a>

Use at most two existing positive DiscoveryIntent queries or one explicit system-default
top-attractions query. No second interpreter or raw-text NLP. Exact geographic retrieval
uses existing ENRICHED text-embedding-3-small / 1536 vectors in pgvector, with 15 km scope.
At most 20 result slots are scanned, with all origins merged; known canonical identities
do not consume the six NEW-resolution-entity attempts. Details<=8 and fallback searches<=2
are incremental budgets, separate from main planning and Nearby. Phase deadline is 30 s.

<a id="b-ff970e716b21-2"></a>

Google query hits retain genuine rank/count semantics. RAG origins carry static corpus,
query and resolution provenance; a RAG-only candidate has no invented Google rank. Shared
admission receives cheap fields; compatible early Details stay cached until normal
enrichment. No corpus prior becomes current factual evidence, Profile or verified satisfaction.
Same canonical ID means one candidate; intent/requirement links are deduplicated.

<a id="b-ff970e716b21-3"></a>

Main C/R/K, selective Reviews, REQUIRED/OPTIONAL, supply policy, generation prompts and
post-itinerary Nearby are unchanged. Nearby anchors still come only from scheduled places.
No guaranteed RAG admission or scheduled count. RAG failures preserve Google work and
validated partial results, without restarting interpretation or planning. Cancellation
propagates, while local budget/time stops do not poison the shared Details negative cache.

<a id="b-ff970e716b21-4"></a>

Trace exposes query/overlap/resolution accounting plus admitted/enriched/supplied/scheduled
and Nearby-only RAG identities. Mixed provenance is distinct from net-new candidates and
is not itself evidence of improved quality.

<a id="b-ff970e716b21-5"></a>

Validation record: 91 focused passes; one full-suite collection error (new V2/V0 module-name
collision), then 14 passing affected runner tests after renaming; 29 affected passes after
diagnostic refinement. No second full suite, so full regression acceptance is incomplete.
One local async PostgreSQL read-only check passed using a saved vector, no embedding API.
No V2 live or re-freeze. See the existing Phase 6 proposal for implementation and next steps.

<a id="m-e7b06f4ead1b"></a>
## TripWorld Phase 4: global retrieval foundation and OpenAI spike

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e7b06f4ead1b-0"></a>

Status: development spike completed on 2026-09-18 and explicitly accepted as complete.
This is implementation validation, not a formal benchmark, research conclusion, or V2 freeze.
Phase 1-3 artifacts were reused. V0/V1 runtime paths and selection logic were not changed.
No global embeddings, PostgreSQL, pgvector, Google resolution, candidate merge, or V2 integration were implemented.

<a id="m-2a0a577f0b99"></a>
## Global entities and identity limitations

_Source context: TripWorld Phase 4: global retrieval foundation and OpenAI spike. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2a0a577f0b99-0"></a>

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

<a id="b-2a0a577f0b99-1"></a>

Google-backed means a source Google Place ID exists; it does not mean that Google has
currently resolved or validated that place. Group by nonblank Google ID, otherwise by FSQ ID.
Preferred names use deterministic normalized Google-name frequency, then FSQ names;
ties, aliases, categories, semantics, and provenance have stable ordering. Both texts are
rebuilt at entity level. Unicode/case normalization removes duplicate aliases/categories.
Coordinates use an actual observed medoid, not an averaged invented point. The entity
retains all contributing FSQ IDs and country/region/locality values.

<a id="b-2a0a577f0b99-2"></a>

Within merged groups, maximum pairwise coordinate spreads are:

<a id="b-2a0a577f0b99-3"></a>

| Spread | Groups |
| --- | ---: |
| Up to 100 m | 16,314 |
| 100 m-1 km | 7,725 |
| 1-10 km | 3,747 |
| 10-100 km | 1,455 |
| Over 100 km | 1,392 |

<a id="b-2a0a577f0b99-4"></a>

There are 6,594 groups over 1 km, 2,847 over 10 km, and 449 country conflicts.
These categories overlap. A deterministic medoid does not repair a wrong upstream
Google match. Such entities need later identity review/Google validation; the spike
preserves and reports their flags rather than silently treating them as reliable.
Different Google IDs and FSQ-only records can still represent the same real place.

<a id="b-2a0a577f0b99-5"></a>

The global artifact is `data/tripworld/artifacts/retrieval_entities.parquet` (177,556,609 bytes).
Its SHA-256 is `a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7`.
Source corpus SHA-256 is `27230ecb110503dd3b9390e70709eefdab843f6f28ce0b908efd3b36054f6e9b`.
TripWorld revision remains `421bc1dc63068bb398055b1ce987265fe22415db`.
Versions: `tripworld-retrieval-entity-v1`, `tripworld-entity-text-v1`,
and `tripworld-category-semantics-v1`.

<a id="m-aa6aaf7cfbc8"></a>
## API model and dimensionality decision

_Source context: TripWorld Phase 4: global retrieval foundation and OpenAI spike. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-aa6aaf7cfbc8-0"></a>

Use OpenAI `text-embedding-3-small`, default **1536 dimensions**, float32,
L2-normalized vectors, and cosine similarity. The request omits `dimensions` and uses
no query/document prefixes. RAW and ENRICHED use the same model and query vectors.
Local embedding model evaluation was superseded by the user's API strategy: the
unfinished local weight download was removed, with no local vectors generated.
There are no PyTorch, transformers, sentence-transformers, or CUDA dependencies.

<a id="b-aa6aaf7cfbc8-1"></a>

The [official embedding guide](https://developers.openai.com/api/docs/guides/embeddings)
documents the default size, shortened dimensions, normalization, and tokenizer.
The [API contract](https://developers.openai.com/api/reference/resources/embeddings/methods/create)
allows up to 8,192 tokens/input, 2,048 inputs/request, and 300,000 tokens/request.
This implementation deliberately uses 8,191 tokens/input, 64 inputs/batch,
20,000 tokens/batch, at most three attempts, and a US$0.10 spike retry-exposure budget.
Both document variants and query tokens are included in the spike preflight budget.

<a id="b-aa6aaf7cfbc8-2"></a>

1536 is the recommended initial production decision because no shortened-dimension
quality comparison has been performed. 768 halves vector storage and arithmetic,
but does not reduce input-token charges; quality may change. Shortening requires an
explicit later decision and a separate artifact contract. No global run was started.

<a id="b-aa6aaf7cfbc8-3"></a>

The API exposes the model name rather than a downloadable immutable model revision.
Do not describe this as a pinned weight snapshot. Saved vector hashes, returned model
names, request IDs, timestamps, software versions, source/content hashes, and versioned
configuration preserve the actual run. Future fresh API regeneration is not guaranteed
to be bit-identical; checkpoint reuse preserves the vectors actually received.

<a id="m-7f1ad6dbc3d9"></a>
## Exact token estimates, API usage, and storage

_Source context: TripWorld Phase 4: global retrieval foundation and OpenAI spike. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7f1ad6dbc3d9-0"></a>

Full-corpus tokenization uses `cl100k_base` over actual entity texts, not sampling.
The [official model price](https://developers.openai.com/api/docs/models/text-embedding-3-small)
checked on 2026-09-18 is US$0.02 per million input tokens (standard API).

<a id="b-7f1ad6dbc3d9-1"></a>

| Variant | Global tokens | Standard cost | Max tokens/document | Sample API tokens | Sample encode time |
| --- | ---: | ---: | ---: | ---: | ---: |
| RAW | 39,160,088 | $0.78320 | 1,431 | 114,901 | 48.329 s |
| ENRICHED | 49,605,198 | $0.99210 | 1,515 | 155,687 | 40.760 s |

<a id="b-7f1ad6dbc3d9-2"></a>

Global variants together: 88,765,286 tokens, approximately **$1.77531** before
retries/taxes. Each has three empty texts and no overlong documents. A future global
job must explicitly exclude empty texts and record exclusions; this spike rejects
empty input rather than submitting it to OpenAI.

<a id="b-7f1ad6dbc3d9-3"></a>

The sample embedded 2,118 entities per variant plus 24 queries. There were **69
successful requests**, no retries, **270,778 usage tokens**, and an estimated standard
charge of **$0.00541556**. This is usage multiplied by published price, not a billing
invoice. Query encoding took 0.574 s; document encode/checkpoint throughput was
43.82 RAW and 51.96 ENRICHED documents/s. The serial sample extrapolates to about
4.10 and 3.46 hours globally (7.56 hours for both), not a service commitment.
Account limits, future batching, network latency, and document lengths can change this.

<a id="b-7f1ad6dbc3d9-4"></a>

Each sample `.npy` is 13,013,120 bytes (12.41 MiB); both are 24.82 MiB.
Global 1536 float32 payload is 3,975,518,208 bytes (3.70 GiB) per variant,
7.41 GiB for both. At 768 dimensions it is 1.85 GiB per variant.
These conservative counts include the three empty entities. Checkpoints and final
arrays coexist locally, so sample disk use includes a second vector copy plus reports.

<a id="b-7f1ad6dbc3d9-5"></a>

For one production vector/entity, the [pgvector storage formula](https://github.com/pgvector/pgvector#vector-type)
is `4 * dimensions + 8` bytes. At 1536 dimensions, vector payload alone is
3,980,694,664 bytes. A planning estimate for one table is **5.18-9.26 GiB**, assuming
1-4 KiB/entity of metadata plus 20-50% heap/TOAST/index headroom. This is not measured
PostgreSQL size and excludes HNSW, WAL, backups, replicas, and a second vector variant.

<a id="m-ee30ccc7153d"></a>
## Representative destinations and geographic filtering

_Source context: TripWorld Phase 4: global retrieval foundation and OpenAI spike. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ee30ccc7153d-0"></a>

Sampling uses occupied 0.25-degree global grid cells, two coverage strata selections
per tier, six distinct countries, and corpus-derived median coordinate centers.
High means at least 3,000 entities, medium 300-2,999, low 40-299, checked for both
seed cell and radius. Labels come from observed localities, not city geocoding.
Within each 15 km circle, deterministic SHA-256 identity sampling caps entities at 384.
No category preference is used during sampling.

<a id="b-ee30ccc7153d-1"></a>

| Destination label | Country | Tier | Full 15 km pool | Embedded sample |
| --- | --- | --- | ---: | ---: |
| Tokyo | JP | High | 48,014 | 384 |
| Kuala Lumpur | MY | High | 15,524 | 384 |
| Santiago | CL | Medium | 2,737 | 384 |
| Antalya | TR | Medium | 2,913 | 384 |
| Melbourne | AU | Low | 292 | 292 |
| Kansas City | US | Low | 290 | 290 |

<a id="b-ee30ccc7153d-2"></a>

Tokyo's sample covers only 0.8% of its pool; missing museums or libraries in a sampled
pool is not evidence that the full destination lacks them. Low/high describes this
TripWorld snapshot, not a city's real POI population. This is not a population-weighted
global quality estimate. Sydney does not drive the architecture or sample selection.

<a id="b-ee30ccc7153d-3"></a>

Generic geographic filtering is optional country consistency, bounding box, then
Haversine distance before vector ranking. Missing country metadata remains available;
known contradictory country values are excluded when a country is supplied. Missing
coordinates are excluded. Tests cover poles, the dateline, radius boundaries, and
bounding-box corner false positives. No locality-equals-city assumption is used.

<a id="b-ee30ccc7153d-4"></a>

Scanning the global coordinate arrays took approximately 114-119 ms per selected
scope. Sample searches used 290-384 geographically filtered candidates; exact ranking
median was 0.69-0.78 ms and p95 0.89-1.18 ms, excluding API/query encoding, serialization,
and artifact load. All retrieved representatives were within their radius; this does
not validate every source coordinate within an anomalous merged entity.

<a id="m-e10b584e0433"></a>
## RAW versus ENRICHED results

_Source context: TripWorld Phase 4: global retrieval foundation and OpenAI spike. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-e10b584e0433-0"></a>

The 12 intents each have English and Chinese queries. Six destinations, two variants,
and two eligibility settings produce **576 cases**, each reporting Top-5/10/20.
All full results, scores, categories, entity metadata, location flags, and overlap
diagnostics are in the ignored `data/tripworld/reports/phase4_spike.json`.
The following inspected examples use eligibility filtering and the English query
unless stated otherwise. Scores are cosine values, not calibrated quality scores.

<a id="b-e10b584e0433-1"></a>

| Observation | RAW | ENRICHED | Interpretation |
| --- | --- | --- | --- |
| Melbourne, quiet indoor | Time Out Fed Square first (0.290); State Library third (0.266) | RMIT Swanston Library first (0.323), La Trobe Reading Room second (0.310), State Library third (0.309) | Useful library prior; access and actual quietness remain unverified |
| Kuala Lumpur, gardens | TWG Tea at The Gardens first (0.371), Town Park second (0.350) | Town Park first (0.396), tea shop second (0.371), Taman Tasik third (0.355) | Better category alignment; name-based contamination persists |
| Kansas City, gardens | Green Lady Lounge second (0.276), between parks | Three parks first; lounge fourth (0.289) | Better park ordering despite a higher irrelevant lounge score |
| Santiago, gardens | Parque Balmaceda first (0.335), other parks mixed with plazas | Five park-category results at the top, Balmaceda first (0.375) | Helpful outdoor category expansion |
| Antalya, gardens | Botanical-garden-category entity first; park and unrelated venue mixed | University botanical garden enters fourth (0.338) | Useful category recall; public access is unknown |
| Tokyo, Chinese nightlife | BOOK AND BED TOKYO first (0.323) | A bar first (0.325), Craft Beer Moon Light second (0.310) | More nightlife-aligned ordering in the sparse sample |

<a id="b-e10b584e0433-2"></a>

Enrichment is promising for category/experience alignment, but is not uniformly better:

<a id="b-e10b584e0433-3"></a>

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

<a id="b-e10b584e0433-4"></a>

Average RAW/ENRICHED ID overlap is 78.61% at Top-5, 79.62% at Top-10, and 81.91% at
Top-20 across all paired cases. This measures ranking change, not accuracy. English/
Chinese Top-5 overlap after eligibility filtering is 57.78% RAW and 61.39% ENRICHED.
Both languages produce plausible museum/nightlife examples, but paraphrase rankings
are not invariant. No relevance labels, precision/recall score, or formal benchmark
claim is made.

<a id="m-ce28450ddce0"></a>
## Eligibility, duplicates, and Top-K

_Source context: TripWorld Phase 4: global retrieval foundation and OpenAI spike. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-ce28450ddce0-0"></a>

Counts below are retrieved slots across 144 unfiltered cases per variant, not unique POIs.

<a id="b-ce28450ddce0-1"></a>

| K | Slots | RAW ineligible | ENRICHED ineligible |
| --- | ---: | ---: | ---: |
| 5 | 720 | 41 (5.69%) | 38 (5.28%) |
| 10 | 1,440 | 87 (6.04%) | 97 (6.74%) |
| 20 | 2,880 | 187 (6.49%) | 232 (8.06%) |

<a id="b-ce28450ddce0-2"></a>

Ineligible examples include office-category Wisma Chuang and residential Warisan
Cityview. Excluding ineligible removes all such labeled slots by construction but
keeps unknown, including some irrelevant stores or services. At filtered Top-20,
unknown accounts for 1,013 RAW and 784 ENRICHED slots. This is not a measured residual
contamination rate: unknown is not synonymous with unsuitable.

<a id="b-ce28450ddce0-3"></a>

There were zero duplicate entity IDs and zero representative-coordinate radius
violations in every Top-K. Location-anomalous entities still appeared in three RAW
and two ENRICHED filtered Top-20 slots. Duplicate suppression covers source Google-ID
groups, not all real-world identity ambiguity.

<a id="b-ce28450ddce0-4"></a>

Increasing K widens the candidate pool and admits more weak/off-intent results.
No production K, similarity threshold, or score-to-Q_rel mapping is selected.
Do not universally exclude cafes, hotels, stations, libraries, markets, or nightlife;
their suitability depends on intent and later validation.

<a id="m-8ef0b16d306c"></a>
## Mapping gaps and next-stage recommendations

_Source context: TripWorld Phase 4: global retrieval foundation and OpenAI spike. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8ef0b16d306c-0"></a>

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

<a id="b-8ef0b16d306c-1"></a>

Recommended next stage, subject to approval:

<a id="b-8ef0b16d306c-2"></a>

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

<a id="m-d77defaa1963"></a>
## Reproduction and checks

_Source context: TripWorld Phase 4: global retrieval foundation and OpenAI spike. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-d77defaa1963-0"></a>

Implementation lives in `backend/app/tripworld/retrieval/`; the isolated entry point is
`scripts/tripworld_retrieval.py`. Configuration and queries are in
`data/tripworld/embedding_model.v1.json` and `retrieval_queries.v1.json`.

<a id="b-d77defaa1963-1"></a>

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

<a id="b-d77defaa1963-2"></a>

Only the OpenAI endpoint is used; no implicit Luna/Azure/base-URL fallback and no
implicit `.env` loading. The adapter sanitizes API errors. Transient connection,
408/409/429/5xx errors have bounded backoff; authentication/quota failures stop.
Each completed batch is atomically checkpointed and checked by input/vector hash.
The same input/configuration/batch partition reuses completed vectors. A lost response
before a durable checkpoint can be billed again: no API-level exactly-once guarantee
is claimed. Do not delete checkpoints or change batch partition mid-resume.
Changing operational configuration also changes checkpoint fingerprints. Concurrent
writers to the same artifact directory are not supported by this development CLI.

<a id="b-d77defaa1963-3"></a>

The tokenizer cache, raw/projected data, entity/vector artifacts, checkpoints, and
generated reports are gitignored. Only code, tiny fixtures, configuration/manifests,
and this report are intended for version control. The full backend regression suite
passed **644 tests**, including **39 TripWorld tests**; Ruff passed. Tests use fake
embedding providers/HTTP responses and do not require API credentials or downloads.
They cover deterministic grouping/rebuilds, geo boundaries, normalized exact ranking,
artifact corruption/version mismatch, retry and failure behavior, preflight budgets,
and interruption/resume. Existing Phase 1-3 work remains uncommitted and preserved.
No commit, push, database setup, global embedding, or V2 runtime work was performed.

<a id="m-0045d5920358"></a>
## TripWorld Phase 5: persistent retrieval layer

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-0045d5920358-0"></a>

Phase 4 and Phase 5 were explicitly accepted as complete. The user designated Phases
1-5 as the frozen technical baseline on 2026-09-18, except for concrete bug fixes.
Phase 5 implements an isolated global retrieval
layer; it does not modify V0/V1 runtime, Q+C+G+R+E, or itinerary generation. Phase 6
Google resolution and candidate integration remain unimplemented. This document
records completed full-corpus engineering validation on September 18, 2026. Phase 5
is implemented; this is not a complete V2 runtime milestone or complete V2 freeze.
The process record is in `thesis_notes/V2/README.md`; Phase 6 remains a design-only
proposal in `docs/tripworld_phase6_proposal.md`, awaiting approval.

<a id="m-a706feb88a66"></a>
## Reproducible local setup

_Source context: TripWorld Phase 5: persistent retrieval layer. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a706feb88a66-0"></a>

Use Docker Desktop in Linux-container mode. The separate `compose.tripworld.yaml`
project pins `pgvector/pgvector:0.8.2-pg17` by image SHA-256, with PostgreSQL 17.10
and pgvector 0.8.2 verified in the running container. It exposes port 55432 only
on 127.0.0.1, has a `pg_isready` healthcheck, and uses the persistent named volume
`reliable-tripworld_tripworld_pgdata`. It does not require native Windows PostgreSQL.

<a id="b-a706feb88a66-1"></a>

Create an ignored `.env.tripworld` from the TripWorld variables in `.env.example`.
Set a nonempty database password locally; no real credentials belong in Git.
Set `OPENAI_API_KEY` in the process environment before paid embedding/query operations.
The CLI loads an environment file only when `--env-file` is supplied and does not
override existing process variables. OpenAI uses its own API endpoint, not Luna/Azure.

<a id="b-a706feb88a66-2"></a>

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

<a id="b-a706feb88a66-3"></a>

`validate` reuses Phase 4's existing 24-query vector checkpoint, without API calls.
It requires the completed production vector set and the Phase 4 sample/query artifacts.
The retrieval service itself does not depend on the Phase 4 sample.

<a id="m-161c7c49d158"></a>
## Five-ID sanity check

_Source context: TripWorld Phase 5: persistent retrieval layer. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-161c7c49d158-0"></a>

Exactly five primary Google Places ID lookups used the existing `GooglePlacesProvider`
with field mask `id,displayName,location` and no retries. All succeeded; no fallback
lookups were made. The names and returned coordinates were inspected with no obvious
identity mismatch. This is technical validation of the lookup flow, not a validity-rate
estimate for TripWorld.

<a id="b-161c7c49d158-1"></a>

| TripWorld name | Google returned name | Latitude | Longitude |
| --- | --- | ---: | ---: |
| Aqua City Odaiba Shrine | Aqua City Odaiba Shrine | 35.6279735 | 139.7738151 |
| Taman Tasik Sri Rampai | Tasik Sri Rampai | 3.1942631 | 101.7285624 |
| Violeta Parra Museum | Violeta Parra Museum | -33.4387945 | -70.6353190 |
| Nabız Live | Nabız Live | 36.8489159 | 30.7536748 |
| State Library Victoria | State Library Victoria | -37.8097255 | 144.9654504 |

<a id="b-161c7c49d158-2"></a>

The exact entity/Google IDs and Unicode names are retained in the ignored
`data/tripworld/reports/phase5_google_sanity.json`. No per-entity global validation state
was added, no corpus refresh took place, and no reusable Google resolution bridge was built.

<a id="m-481da1e19814"></a>
## Schema, provenance, and ingestion

_Source context: TripWorld Phase 5: persistent retrieval layer. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-481da1e19814-0"></a>

`backend/app/tripworld/database/migrations/001_retrieval.sql` initializes the extension
and schema. The migration runner records filename/checksum and rejects edits to applied
migrations. Initialization is transactional and serialized with an advisory lock.
Subsequent changes belong in new numbered migration files.

<a id="b-481da1e19814-1"></a>

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

<a id="b-481da1e19814-2"></a>

RAW vectors are not imported. Old vectors with changed text cannot match updated
entities; unchanged text can reuse its vector even if non-text metadata changes.
Historical unreferenced vectors can remain as reusable cache; no destructive global
vector purge is part of normal ingestion.

<a id="b-481da1e19814-3"></a>

Entity ingestion validates the Parquet SHA-256, builder/text versions and each row's
provenance against its manifest. COPY loads a temporary staging table, validates counts
and duplicate IDs, then performs a transactional content/version-aware upsert and
removes stale entity rows from that full snapshot. No per-row INSERT loop is used.
The ingestion/build locks prevent a corpus replacement during an embedding build.

<a id="b-481da1e19814-4"></a>

The initial full COPY ingestion populated **647,057 rows in 100.57 seconds**.
An unchanged full-corpus rerun completed in **83.76 seconds**, with **zero changed
rows and zero removals**. Tests separately exercise changed-text invalidation and rollback.
Production source SHA-256 remains
`a0de2721b0b8c1581d78496bfe06da1c3c7dc46cab2a7454c171504732c808f7`.
The original TripWorld revision and approved Phase 1-4 artifacts were not regenerated.

<a id="m-6b99d17e55a2"></a>
## Explicit production policy and preflight

_Source context: TripWorld Phase 5: persistent retrieval layer. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6b99d17e55a2-0"></a>

Policy `tripworld-production-policy-v1` excludes ineligible entities, empty text,
invalid/missing coordinates, country conflicts, and coordinate spread **strictly
greater than 10 km**. Unknown remains available. Metadata for every excluded entity
stays in PostgreSQL. The 1-10 km spread flag remains visible on otherwise allowed
entities; the policy is conservative screening, not identity repair or Google validation.

<a id="b-6b99d17e55a2-1"></a>

| Exclusion | Overlapping reason count | Mutually exclusive first reason |
| --- | ---: | ---: |
| Ineligible | 63,789 | 63,789 |
| Empty text | 3 | 3 |
| Invalid coordinates | 9 | 6 |
| Country conflict | 449 | 397 |
| Spread over 10 km | 2,847 | 2,067 |

<a id="b-6b99d17e55a2-2"></a>

The first-reason priority is the order above. Total excluded is **66,262**;
**580,795 entities** remain, representing **577,011 distinct ENRICHED texts**.
Their texts contain 44,095,604 tokens per entity, or **43,805,323 unique-text tokens**.
Maximum input is 1,515 tokens; no truncation is needed.

<a id="b-6b99d17e55a2-3"></a>

At the [published standard model rate](https://developers.openai.com/api/docs/models/text-embedding-3-small)
of US$0.02/million input tokens, the conservative new-vector cost is **US$0.87611**
before existing-vector reuse. Three-attempt exposure is approximately **US$2.62832**.
The preflight requires standard cost <= US$2, retry exposure <= US$5, input <=8,191
tokens, and at least 25 GiB free workspace disk. It runs before paid generation.
Observed workspace free space was approximately 242 GiB, host C: approximately 337 GiB,
and the Docker VM filesystem reported approximately 945 GiB available.

<a id="b-6b99d17e55a2-4"></a>

Per-entity vector payload upper bound is 3,568,404,480 bytes (3.32 GiB). Physical text
deduplication reduces this slightly. The rough DB estimate is 4.73-8.69 GiB, excluding
WAL/backups/Docker overhead; checkpoints occupy additional local disk space. The Phase 4
serial-throughput extrapolation was 11,104 seconds (3.08 hours); actual global timings
are reported below rather than inferred from that sample.

<a id="m-62406f399665"></a>
## Embedding generation and recovery

_Source context: TripWorld Phase 5: persistent retrieval layer. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-62406f399665-0"></a>

The vector space is fixed: OpenAI `text-embedding-3-small`, default 1536 dimensions,
cosine, float32 and L2 normalization, with no prefixes/custom dimensions. ENRICHED is
the only production representation. OpenAI's alias is recorded as such, not presented
as an immutable model-weight revision.

<a id="b-62406f399665-1"></a>

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

<a id="b-62406f399665-2"></a>

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

<a id="b-62406f399665-3"></a>

The completed database contains **577,011 physical vectors**, covering all **580,795
production RetrievalEntities** through `entity_embeddings`. There are zero missing
entity vectors and zero invalid dimensions/norms. Text deduplication preserves one
logical retrieval slot per entity; it does not merge separate entities.

<a id="b-62406f399665-4"></a>

The saved-response audit records **8,577 successful production requests / 8,577
attempts**, **43,669,473 API tokens**, and an estimated **US$0.87338946**. This includes
production timing probes and recovered checkpoints, and excludes the 1,880 reused
Phase 4 vectors. No retries appear in those saved responses. Operator interruptions
and a Windows progress-report file-lock failure occurred during tuning; completed
vector batches were preserved. Progress-report writes now retry and cannot abort a
paid build merely because telemetry is temporarily locked. Another 448 pending
vectors were recovered from checkpoints during a later resume.

<a id="b-62406f399665-5"></a>

The first-to-last saved production response window was **4,065.77 seconds (67.76
minutes)**, from 06:50:15 to 07:58:01 UTC. It includes pauses and tuning but excludes
startup before the first saved response; it is not an exact uninterrupted job runtime.
The final uninterrupted segment took **2,752.63 seconds (45.88 minutes)**. Interrupted
requests whose responses were lost may have been billed and cannot be reconstructed;
the saved-response ledger is an observed cost estimate, not a complete billing invoice.

<a id="b-62406f399665-6"></a>

At completion, PostgreSQL measured **7,260,591,795 bytes (6.76 GiB)**. The entities
table and indexes occupied **1,615,937,536 bytes (1.50 GiB)**; the embeddings table,
TOAST and indexes occupied **5,635,112,960 bytes (5.25 GiB)**. Logical vector datum
size was **3,547,463,628 bytes (3.30 GiB)** including pgvector datum overhead. Docker,
WAL, backups and local checkpoints are additional. These are completion snapshots;
normal database maintenance and reruns can change physical allocation.

<a id="b-62406f399665-7"></a>

Generation reports and checkpoints stay under ignored `data/tripworld/reports/` and
`data/tripworld/artifacts/phase5/`. Secrets are never included. Request IDs and response
model/timestamp/usage data support auditing. API usage costs are estimates, not invoices.

<a id="m-36f1ae8f9733"></a>
## Retrieval service and indexes

_Source context: TripWorld Phase 5: persistent retrieval layer. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-36f1ae8f9733-0"></a>

`RetrievalService` separates query embedding from `PostgresSearch`. It accepts a
semantic intent, generic coordinates/radius, optional country and Top-K, and returns
ranked typed entity metadata, cosine similarity and distance. Query construction is
not the raw trip request and does not modify the V1 interpreter. Normal discovery
always applies the fixed policy; callers cannot silently include ineligible entities.
Search validates an existing embedding space without creating or updating it, and the
service rejects a missing/incompatible space before constructing a paid API provider.
Lexical lookup and geographic counts do not require populated vector storage.

<a id="b-36f1ae8f9733-1"></a>

The exact SQL pipeline is bounding box (including antimeridian splits), optional
country consistency, Haversine radius, structured policy, compatible vector join,
cosine ordering, and deterministic entity-ID tie-breaking. Missing country metadata
remains available. Locality equality is never the geographic filter. Top-K is a caller
parameter (1-1000), not a final V2 selection policy.

<a id="b-36f1ae8f9733-2"></a>

B-tree indexes cover entity identity, non-null Google ID uniqueness, latitude,
longitude, country and allowed text hashes; a GIN array index supports normalized
exact preferred-name/alias lookup. Vector storage has a composite space/text-hash
primary key. There is **no HNSW, IVFFlat, PostGIS, fuzzy lexical ranking or score fusion**.

<a id="b-36f1ae8f9733-3"></a>

```powershell
uv run python scripts/tripworld_database.py --env-file .env.tripworld query "quiet indoor places" --latitude -37.812659 --longitude 144.965733 --radius-km 15 --country AU --top-k 10
uv run python scripts/tripworld_database.py --env-file .env.tripworld query "State Library Lawn" --latitude -37.812659 --longitude 144.965733 --radius-km 15 --country AU --lexical
```

<a id="m-2ce25799e654"></a>
## Validation and next-stage boundary

_Source context: TripWorld Phase 5: persistent retrieval layer. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-2ce25799e654-0"></a>

Automated tests use mocked OpenAI responses and an optional separate `tripworld_test`
database. The test fixture refuses to reset the production database. Enable real DB
tests with `TRIPWORLD_TEST_DATABASE=1` and the local DB credentials; create the separate
test database first. Default tests skip these integration tests when not configured.
No normal test makes a live OpenAI call.

<a id="b-2ce25799e654-1"></a>

The final full backend regression suite, including real PostgreSQL integration,
passed **662 tests**. Ruff and `git diff --check` passed. Coverage includes migration
checksums, COPY rollback/idempotence, text changes, vector compatibility/reuse, resume,
policy versions, dateline/pole/radius handling, cosine ties, aliases, sanitized DB
errors, missing-space rejection before paid API calls, and read-only retrieval.

<a id="b-2ce25799e654-2"></a>

Full-corpus validation passed **144 cases** (24 English/Chinese queries across six
destinations), checking all 2,880 returned slots for entity-ID uniqueness within each
query, geographic correctness, and eligibility/anomaly policy. An independent NumPy
calculation over the complete Santiago 15 km candidate pool matched PostgreSQL's
Top-20 order. Queries used existing Phase 4 vectors with zero API calls. Two additional
end-to-end service smoke queries used the live OpenAI adapter: 2 requests, 16 tokens,
estimated US$0.00000032, accounted separately from the document build.

<a id="b-2ce25799e654-3"></a>

Among the 2,880 slots, 2,317 were eligible and 563 unknown; none were ineligible.
Eleven retained the 1-10 km coordinate-spread flag. Geography verifies the entity's
representative coordinates, not every merged source coordinate or current Google
location. Different IDs may still refer to the same real place; identity deduplication
at the later Google canonicalization stage remains necessary.

<a id="m-07e2002d23bf"></a>
## Exact-search measurements

_Source context: TripWorld Phase 5: persistent retrieval layer / Validation and next-stage boundary. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-07e2002d23bf-0"></a>

All measurements use the populated global database, Top-K 10, a single client,
two query intents (English culture and Chinese quiet-indoor), and five warm repeats
per intent. Each table p50/p95 pools those ten SQL execution samples. They exclude
query embedding, network round trips and future Google resolution. First-touch values
show both intents; caches were not flushed and overlapping scopes can warm later
measurements. These small-sample percentiles are diagnostics, not a concurrency SLA
or formal retrieval-quality benchmark. Sydney is not a benchmark destination.

<a id="b-07e2002d23bf-1"></a>

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

<a id="b-07e2002d23bf-2"></a>

Tokyo's 15 km first-touch EXPLAIN used bitmap latitude/longitude/country indexes,
produced 48,102 allowed bounding-box rows, reduced them to 46,020 radius-qualified
rows, and performed 46,020 embedding primary-key lookups before cosine sorting and
the final ten metadata lookups. Execution took 1,092.37 ms, with 257,098 shared block
hits and 197,070 reads. Vector access and ranking dominate this dense case; there is
no global 577k-vector scan or ANN approximation. Full JSON plans and client timings
are retained in the ignored validation report.

<a id="b-07e2002d23bf-3"></a>

**Decision: retain exact search for the initial interactive planner.** Medium/low
density scopes take milliseconds to a few hundred milliseconds, while Tokyo 30 km
has warm p95 around 1.50 seconds for SQL alone. This is workable for a small number
of retrieval intents in the current staged planner, but it does not establish a
sub-500 ms or high-concurrency service. If a later measured latency/concurrency budget
cannot tolerate dense-scope cost, separately evaluate filtered ANN against this exact
baseline, checking geographic/policy recall and sufficient results after filtering.
HNSW is not currently implemented or recommended solely due to global corpus size;
any implementation requires separate approval.

<a id="m-297319e8fd36"></a>
## Representative multilingual and lexical results

_Source context: TripWorld Phase 5: persistent retrieval layer / Validation and next-stage boundary. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-297319e8fd36-0"></a>

Both languages can retrieve category-relevant venues, but rankings differ and are
not guaranteed translations of one another. For the culture intent, top results
at the configured 15 km destination scope were:

<a id="b-297319e8fd36-1"></a>

| Destination | English culture Top-3 | Chinese culture Top-3 |
| --- | --- | --- |
| Tokyo | ESP MUSEUM; WHAT MUSEUM; Bunkamura THE MUSEUM | Bunka Gakuen Costume Museum; National Institutes for Cultural Heritage; Fujifilm Photo History Museum |
| Kuala Lumpur | The National Museum of Malaysia; Muzium Telekom; National Textiles Museum | Lost In Chinatown; BNM Museum and Art Gallery - Museum Cafè; Bank Negara Malaysia Museum and Art Gallery |
| Santiago | Museo de Arte Contemporáneo; Museo de Arte Contemporáneo (MAC); MUI | Museo de Arte Contemporáneo; La Moneda Cultural Center; National Museum of Fine Arts |
| Antalya | Antalya Archaeology Museum; Antalya Culture and Arts; Ataturk House & Museum | Antalya Culture and Arts; Kültür; Antalya Archaeology Museum |
| Melbourne | Immigration Museum; Melbourne Museum; National Gallery of Victoria | Immigration Museum; Melbourne Museum; Royal Exhibition Building |
| Kansas City | American Jazz Museum; Kemper Museum of Contemporary Art; The Nelson-Atkins Museum of Art | Negro Leagues Baseball Museum; National WWI Museum and Memorial; Hallmark Visitors Center |

<a id="b-297319e8fd36-2"></a>

The Chinese culture query is the `culture.zh` entry in
`data/tripworld/retrieval_queries.v1.json`; the English text is "museums and cultural
attractions". Cross-language results are useful discovery signals, not proof of
travel suitability: the Kuala Lumpur Chinese Top-3 includes a museum cafe, and
Tokyo includes a cultural institution. Sparse Melbourne/Kansas City coverage limits
recall even when SQL is fast. Broader production results need not match the small
Phase 4 sample; the NumPy comparison controls for the same full candidate pool.

<a id="b-297319e8fd36-3"></a>

Normalized exact lexical lookup maps **State Library Lawn** to **State Library
Victoria** and retrieves **Aqua City Odaiba Shrine** by preferred name, with no
embedding or Google API call. It is intentionally not fuzzy search or score fusion.

<a id="m-8f74edef815a"></a>
## Working-tree and evidence status

_Source context: TripWorld Phase 5: persistent retrieval layer / Validation and next-stage boundary. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-8f74edef815a-0"></a>

Phase 5 adds `compose.tripworld.yaml`, `backend/app/tripworld/database/`,
`scripts/tripworld_database.py`, database tests and this report. It extends the
existing OpenAI adapter/checkpoint support, dependency groups/lockfile, environment
example and project status. Existing Phase 1-4 uncommitted files are preserved.
Tracked modifications are `.env.example`, `.gitignore`, `PROJECT.md`, `pyproject.toml`
and `uv.lock`; TripWorld code/tests/scripts/configuration/docs remain untracked pending
an explicitly requested commit. No V0/V1 runtime or selection files changed. No commit,
push, Google bridge, candidate funnel, Q_rel mapping or itinerary change was made.

<a id="b-8f74edef815a-1"></a>

Raw data, generated Parquet/NumPy/checkpoint artifacts, validation reports and real
credentials remain ignored. Reproducible code/configuration, manifests, versions,
hashes, tiny fixtures and this aggregate report remain reviewable in the repository.
Local detailed evidence is under `data/tripworld/reports/`: `phase5_google_sanity.json`,
`phase5_ingestion.json`, `phase5_reingestion.json`, `phase5_preflight.json`,
`phase5_embedding_run.json`, `phase5_audit.json`, `phase5_validation.json`,
`phase5_lexical.json` and `phase5_service_smoke.json`.

<a id="b-8f74edef815a-2"></a>

Phase 6 recommendations (not implemented): resolve only the ranked candidates actually
needed. Try an existing Google ID first, fall back to name/location on failure; FSQ-only
candidates begin with name/location search. Discard unresolved candidates and continue
until the required usable pool or request budget is reached. Preserve discovery and
resolution provenance, deduplicate by canonical Google ID, reuse request-scoped cache,
and retain Google-first candidates without a TripWorld match. Do not prevalidate the
global corpus, and do not turn cosine similarity directly into Q_rel without a separate
integration design. Existing Q+C+G+R+E remains unchanged.

<a id="b-8f74edef815a-3"></a>

For that design, keep cosine score and retrieval rank as discovery provenance, then
compute the existing Q_rel from the resolved canonical POI using its current contract.
Any future score fusion needs an explicit definition and separate approval. Give
resolution a per-trip call/attempt budget (including failed lookups and fallbacks),
reuse the existing RequestCache for repeated IDs/searches, and stop on either a usable
pool target or budget exhaustion. Candidate replacement should continue down the RAG
ranking after a failed resolution without blocking Google-first discovery. Exact
budget, pool size and concurrency settings remain Phase 6 decisions.

<a id="m-41ab3c8cc35d"></a>
## Phase 6 implementation checkpoint - 2026-09-19 (no V2 live)

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-41ab3c8cc35d-0"></a>

V2 runtime integration is implemented: independent run_v2 and scripts/run_v2.py reuse
the current tools planner with bounded TripWorld discovery after Google/named identity
resolution and before shared factual admission. Source-neutral origins and compatible
Details caching connect RAG-only and mixed candidates to the same deterministic supply,
Reviews/Profile, primary itinerary_2 and post-itinerary Nearby. No source quota or new
selector, generation prompt or reference policy. V1 remains Google-only; V0 tool-free;
product default and frontend are unchanged. The former design-only status below is history.

<a id="b-41ab3c8cc35d-1"></a>

Approved correction: scan <=20 returned slots and merge known identities freely; only
entities needing NEW resolution consume the six-attempt cap. Incremental limits remain
one embedding batch, two Top-K-10 queries, eight Details, two fallback searches and a
30-second phase. Main C/R/K and Nearby budgets remain unchanged. No production corpus
rebuild, migration, vector regeneration or real model/Google call occurred.

<a id="b-41ab3c8cc35d-2"></a>

An external baseline, later deleted by user authorization, saved 306 whitelisted source/config/test/document files
and 11 migration deletions at D:/Workspace/Capstone/phase6_source_snapshots/20260919T113719Z.
Credentials, production data and ignored evidence archives were excluded.

<a id="b-41ab3c8cc35d-3"></a>

Validation: 91 focused tests passed. The single full backend invocation stopped during
collection with one new V2/V0 test-module naming collision, before tests ran. Renaming
the V2 test resolved the collision; 14 affected runner tests passed. Later admission/fate
diagnostics passed 29 affected tests. No second full run: full-backend regression acceptance
remains incomplete. Ruff/diff checks passed. One authorized local PostgreSQL read-only
async-adapter check passed using a saved query vector, with zero embedding calls.

<a id="b-41ab3c8cc35d-4"></a>

See docs/tripworld_phase6_proposal.md for actual file mapping, limits, exact evidence and
two proposed future V2 live requests. Before paid/live acceptance, recommend approval for
one fresh complete regression check. No V2 live, stage/commit/push, B2 cleanup or re-freeze.

<a id="m-35b7a552d4f7"></a>
## V2 — RAG

_Source context: Research Versions. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-f30b385cbc48-0"></a>

Current: Phase6 integration and quality_first_1 have accepted bounded development-live evidence.
The following retained planning narrative records the Phase1-5/Phase6-design-only checkpoint
before implementation; it is not current execution guidance. See current closeout above.

<a id="b-f30b385cbc48-1"></a>

V2 adds retrieval grounding to V1. The planned offline knowledge sources are TripWorld for relatively stable destination, POI, and travel-pattern knowledge, with TP-RAG as a possible China-specific supplement.

<a id="b-f30b385cbc48-2"></a>

RAG should help identify relevant places, areas, combinations, and typical visit patterns; it should not replace live verification. Dynamic facts such as current opening status, disruptions, weather, route duration, and ticket changes should come from current sources.

<a id="b-f30b385cbc48-3"></a>

TripWorld Phase 1-4 data preparation, deterministic global RetrievalEntity construction,
and the isolated OpenAI embedding spike have been accepted as complete. Phase 5 is
also explicitly accepted as complete; Phases 1-5 form the frozen technical baseline
as of 2026-09-18, except for concrete bug fixes. Phase 5 implemented and validated a
persistent PostgreSQL + pgvector retrieval layer using ENRICHED
text and OpenAI `text-embedding-3-small` at 1536 dimensions. See
`docs/tripworld_phase4.md` and `docs/tripworld_phase5.md` for implementation status and
validation evidence. This retrieval service remains separate from the V1/V2 candidate
funnel; no V1 selection or itinerary-generation behavior changes are authorized here.
The complete V2 planning version is not implemented or frozen. Phase 6 is design-only;
`docs/tripworld_phase6_proposal.md` requires separate approval before implementation.

<a id="b-f30b385cbc48-4"></a>

Future Google usage must be demand-driven: resolve only the ranked TripWorld candidates
needed for a trip, trying an existing Google Place ID first and name/location fallback
when needed. Drop unresolved candidates and continue within request budgets. Do not
prevalidate the global corpus. The Google resolution bridge and candidate merge belong
to a separately approved Phase 6.

## Current replacement and shared acceptance

The old QCGRE integration proposal below is superseded by the [current V2 design](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/v2_design.md). Its selection context is explained in [selector experiments](v1-selector-experiments.md#causal-chain). The [joint quality acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/development_record.md) is the sole full shared result; this file owns V2-specific retrieval and performance events. The inline-vector shadow-table proposal remains paused, not implemented or disproven.


## Current implementation checkpoint acceptance (2026-09-20)

V2 current implementation checkpoint accepted. The [joint acceptance record](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/development_record.md)
keeps Tokyo/Sydney results, later offline sorting, finite triage and checkpoint governance once.
Normal RAG and RAG-only downstream use are demonstrated; exact-search variance remains engineering
work. No storage migration, re-embedding, permanent freeze or V3 implementation follows implicitly.
The [reproducibility audit](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/v2_tripworld_retrieval.md)
separates a functional rebuild from restoring exact local vector values.

## Shared first-generation extension - 2026-09-20

The shared coverage/role/diagnostic/K20 extension is implemented and checked offline;
no fresh live result is claimed. Acquisition goals remain unchanged and no repair loop
exists. The single [development event](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/development_record.md)
owns sizing, first failures and subsequent targeted test results. Historical live and
full-suite records above retain their original configuration and outcome.

### Connection tolerance change

London connection establishment exhausted2 seconds before SQL/embedding. Approved change:
connect10 seconds only; SQL60, RAG360, explicit outer600 unchanged. Mocked adapter checks
verify the effective timeout, not actual connectivity improvement. No SQL/storage/vector
change or live retry was performed. Longer connection waiting does not solve exact-search
I/O variability. See the shared event for the original capture and precise limitation.


## Compatible transfer output update (2026-09-25)

The shared itinerary DTO now accepts optional `transfers` (missing defaults empty).
Current V3 binds and presents verified/unknown per-leg route estimates and separate
application reserves; V0-V2 do not fabricate transfers or acquire additional routes for
this field. Primary model DTO/prompt, K, existing version entry points and product default
are unchanged. The frontend can render this optional data when supplied; this does not
implement the deferred Product V3/API selection or the whole frontend backlog.
See [V3 design](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/v3_design.md) and the
[development verification record](v3-development.md#mixed-transport-and-joint-components-2026-09-25).
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
