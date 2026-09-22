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
## Approval-ready next scope and validation

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Bounded read-only diagnosis - 2026-09-20 (no paid calls; fixes pending approval). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-8ea3e07f972f-0"></a>

No numeric production timeout increase is recommended from these eight observations:
Tokyo sometimes exceeded even 15 seconds. Raising SQL to 15 for each of two sequential
queries would also consume the 30-second RAG phase before embedding/identity work. A 5- or
8-second bound cannot presently be described as reliable. Keep current production defaults
until a separately approved change has measured justification; retain Google fallback.

<a id="b-8ea3e07f972f-1"></a>

1. Approve a narrow observability repair only: distinct SQL-suboperation/phase timeout
   diagnostics, execute/fetch timings, structured SQLSTATE/cancellation information, and
   actual embedding-client HTTP hooks. Optional development capture of query vectors must
   retain query/space/hash association under ignored artifacts. No policy/budget change.
2. Approve a separate bounded performance follow-up, if desired: investigate the observed
   data-page/TOAST access and cardinality underestimate; at most one equivalent geographic
   CTE rewrite and four read-only <=15-second executions. Compare same vector/scope/policy,
   ordered IDs and scores (e.g. absolute tolerance 1e-6), including stable ties. Only promote
   a rewrite after equivalence and improvement are demonstrated; do not assume removing
   MATERIALIZED or the spill alone fixes random reads. No index/infrastructure changes.
3. Named-role extension is an independent optional approval. Without it or user identity
   clarification, preserve Melbourne's current stop; never delete REQUIRED to exercise RAG.
4. Run affected adapter/service/telemetry tests with fake transport and cancellation; keep
   V1 RAG-free and V0 external-free. No full suite was repeated for this diagnostic task.
5. After a repair and offline checks, separately approve at most one necessary fresh V2
   Tokyo live to verify real query capture, normal SQL/resolution/merge/fate and unchanged
   Nearby roles. Do not repeat both full trips automatically or guarantee RAG selection.

<a id="b-8ea3e07f972f-2"></a>

This task added only scripts/diagnose_tripworld_sql.py and its five offline tests, plus
existing documentation/archive updates. All five tests passed; Ruff and diff checks passed.
An initial Ruff line-length finding was corrected in the diagnostic script, not production.
Exactly eight local retrieval executions, zero external/paid calls; frozen production hashes
unchanged. No full-suite repetition, global settings, database writes, B2 cleanup, frontend
change, commit/push, freeze or V3. Original full-regression/live acceptance status is unchanged.

<a id="m-4a1077481a18"></a>
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
## Next bounded live requests (proposal only, not executed)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2 / Implementation checkpoint - 2026-09-19. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-5ebd49a38905-0"></a>

Subject to later approval and a fresh trusted-date check, propose exactly two fresh runs:

<a id="b-5ebd49a38905-2"></a>

```json
{
  "input_version": "planning_request_2",
  "destination": "Melbourne, Australia",
  "start_date": "2026-09-21",
  "end_date": "2026-09-23",
  "traveler_count": 3,
  "budget": {"amount": "1800", "currency": "AUD"},
  "additional_preferences": "I definitely want to visit Queen Victoria Market."
}
```

<a id="b-5ebd49a38905-3"></a>

Tokyo targets positive discovery; Melbourne targets named-only/system-default retrieval.
If interpretation or identity resolution differs, retain that outcome without forcing or
replacing it. Dates must be revalidated/frozen before execution if approval is later.
Historical profiling motivated dense/sparse destination choices; it is not a runtime count.
No comparison benchmark, extra scenario, paid call or live preparation was executed here.

<a id="b-5ebd49a38905-4"></a>

The reviewed A-K design follows, with the approved six-entity counting correction applied.
Statements proposing file extraction describe the design intent; the implementation mapping
above records the smaller actual shared-builder placement and reuse choices.

Verbatim passages shared with another maintained section: [1](development_guide.md#b-61a2c7801de0-2). The migration ledger recorded these occurrences at migration time; it was later deleted with the authorized recovery-material cleanup and is no longer available.

<a id="m-654a63012104"></a>
## Historical Phase6 baseline A. Actual baseline and integration seams

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-654a63012104-0"></a>

Keep planning_request_2, required structured trip facts and currency, optional preferences,
one shared interpretation when nonempty and none when empty, application-owned IDs and
provenance, deterministic supply, selective Reviews/Profile, REQUIRED/OPTIONAL inputs,
itinerary_2 and post-itinerary Nearby. Do not restore QCGRE, B1/B2 evaluation or subset
enumeration. Do not change embedding model, selector, planner objective or reference policy.

<a id="b-654a63012104-1"></a>

Actual execution is:

<a id="b-654a63012104-2"></a>

```text
versions/v1/graph.py: acquire_candidate_funnel
  -> PlanningCandidateSupplyPipeline.run (inherited from SemanticPOIPipeline)
  -> assessments / capacities / Google query construction
  -> search_candidate_observations -> merge_search_observations
  -> resolve_named_place_intents -> REQUIRED/EXCLUDED checks
  -> factual eligibility -> admission_order -> c_raw admission
  -> Details until r_pool -> selective Reviews/Profile
  -> PlanningCandidateSupplyPipeline.select -> select_planning_supply
  -> project_selected_places -> Weather / Routes / Official Web
  -> primary-only generation / identity and date checks
  -> discover_reference_recommendations -> END
```

<a id="b-654a63012104-3"></a>

The inherited class contains retained historical evaluator code, but the active subclass
overrides initialization and selection. Do not accidentally activate the base select method.

<a id="b-654a63012104-4"></a>

Insert a V2-only extension AFTER Google merge and operational named-place resolution,
BEFORE factual eligibility/admission_order. Preserve Google observations, resolve bounded
RAG hits, canonical-union the results, then use the same enrichment/supply. The shared
pipeline extension defaults to absent in V1. REQUIRED/EXCLUDED resolution must precede
discretionary RAG spending and retain its existing clarification behavior.

<a id="b-654a63012104-5"></a>

V2 orchestration owns the query plan, retrieval, resolution budgets, cancellation and
diagnostics. Introduce independent run_v2 and scripts/run_v2.py with actual SystemVersion.V2.
Extract a small shared graph builder with explicit pipeline factory/version injection;
keep build_v1_graph a Google-only wrapper with its existing node order. V2 supplies the
extension, not a run_v1-then-append wrapper. V0 remains independent and tool-free; product
default and frontend are unchanged. No V1/V0 initialization requires a RAG client or DB.

<a id="b-654a63012104-6"></a>

Capacities remain K=min(16,2*days+2), R=max(10,K+2), C=max(20,2*R), review cap
min(6,ceil(K/3)), subject to current budgets and REQUIRED expansion. Three days normally
means C=20, R=10, K=8, reviews<=3. No RAG quota or extra supply slots; zero RAG admission
is a possible outcome. This changes discovery, not deterministic selection policy.

<a id="m-5ca12ee1b977"></a>
## Historical Phase6 baseline B. Google-only contracts and minimal extensions

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-5ca12ee1b977-0"></a>

| Current seam | Proposed extension |
| --- | --- |
| evidence/models.py PlaceCandidate.provider_rank | Nullable when no real Google search rank exists; never zero as a fabricated rank. source_query/category remain discovery metadata. |
| selection_models.py PlaceSelectionInput.query_hits | Permit empty only with validated TripWorld origin; require a real origin overall. |
| QueryIntentHit | Keep strict original Google response position/count unchanged. |
| poi_funnel.py merge_search_observations | Preserve Google merge; add separate canonical-union helper, avoiding min() on empty Google hits. |
| selection_normalization.py | Carry origins through Details normalization; project direct-ID current Details into cheap candidate fields. |
| semantic_poi_pipeline.py associations | Unique requirement refs from all real discovery origins, not just Google hits. |
| planning_supply_pipeline.py SupplyCandidate.intent_ids | Unique original discovery intent IDs from all sources. |
| planning_supply.py | Algorithm and source-neutral supply contract unchanged. |
| planning_supply_result.py / traces | Version-aware RAG diagnostics alongside planning_supply_1; itinerary_2 unchanged. |

<a id="b-5ca12ee1b977-1"></a>

A TripWorld origin retains entity ID, query ID, original intent/requirement refs, user-query
versus system-default origin, retrieval rank/cosine/distance, corpus/artifact/text/space/policy
identity and resolution evidence reference. Cosine never becomes Google rank. A real fallback
search rank belongs to the resolution ledger, not a newly invented user preference.

<a id="b-5ca12ee1b977-2"></a>

Merge by actual Google canonical ID. Keep the existing Google candidate projection for
mixed-source IDs and union origins/date observations with existing conflict handling.
RAG-only current name/coordinates/status come from Google. Deduplicate entity and canonical
hits and requirement associations; repeated queries cannot earn multiple rewards or fetches.
Canonical IDs do not solve physical venue/subvenue duplication.

<a id="m-fafa5592b38a"></a>
## Historical Phase6 baseline C. Existing TripWorld foundation and runtime adapter

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-fafa5592b38a-0"></a>

Read-only manifest inspection: dataset revision 421bc1dc63068bb398055b1ce987265fe22415db,
source SHA-256 bd94d73c8443a18b5c7d31c0bd0b855cd141763b63841ee90646be1d73f9345e;
retrieval_entities.parquet.manifest.json records 647,057 entities (526,682 Google-backed,
120,375 FSQ-only), builder tripworld-retrieval-entity-v1. Accepted Phase 5 records report
580,795 production entities covered by 577,011 physical vectors. These are saved results,
not a new live database audit.

<a id="b-fafa5592b38a-1"></a>

Reuse tripworld-production-policy-v1: exclude ineligible, empty text, invalid coordinates,
country conflicts and coordinate spread >10 km; unknown remains eligible for discovery.
Reuse ENRICHED, text-embedding-3-small, 1536 dimensions, normalized cosine and SPACE_ID.
Existing database/search.py uses bounding-box plus exact Haversine radius, policy filtering,
compatible vectors and cosine descending/entity-ID ties. No ANN, migration or rebuild.

<a id="b-fafa5592b38a-2"></a>

Existing database/service.py is synchronous and writes resumable query checkpoints.
connection.py has a 10-second connection timeout and 15-minute statement timeout;
EmbeddingConfig defaults to three application attempts and 60-second requests (SDK retry=0).
Do not use those offline defaults unchanged in runtime or change offline build behavior.

<a id="b-fafa5592b38a-3"></a>

Add a V2 async runtime adapter reusing the SQL builder and vector/space validation, with
read-only DB transactions, bounded connection/statements, cancellable HTTP and owned resource
cleanup. Do not claim wait_for(to_thread(sync_retrieval)) cancels its background work.
Check compatible space/policy and expected completed build/artifact identity before embedding;
mismatch means degradation, not automatic repair. No full vector scan per request.
Runtime query embeddings are bounded new inputs; corpus vectors are never regenerated.
Query caching is request-local, not the offline checkpoint directory.

<a id="m-f57630f15dd9"></a>
## Historical Phase6 baseline D. Query plan and the latest empty-intent observation

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f57630f15dd9-0"></a>

The accepted live result at logs/nearby_reference_acceptance_20260919_095712/result.json
contains discovery_intents=[] in BOTH raw interpreter responses and in V1's canonical
contract. Distinctive/local and mother's less-walking meanings were itinerary_style.
The mapper consolidates/validates returned intents; it did not delete a query here.
The prompt permits no queries and normally keeps set/conditional preferences downstream.
Actual Google searches were destination, Opera House, default top attractions and local food.
This is a permitted extraction outcome, not a failed search dispatch. Whether local feel
should have produced a query remains an interpretation-quality limitation.

<a id="b-f57630f15dd9-1"></a>

Proposed rag_query_plan_1:

<a id="b-f57630f15dd9-2"></a>

1. Reuse DiscoveryIntent.query_text with at least one linked favor requirement. Order by
   strongest linked requirement using the current strength ordering, then intent_id.
   Select at most TWO distinct texts, <=200 code points each. Merge exact normalized
   duplicate texts and union origin refs. Trace omitted intents; no semantic reinterpretation.
2. If a usable intent exists, use only selected intents; do not fill unused slots with defaults.
3. Otherwise issue ONE versioned system query, "top attractions", from GENERIC_SEARCH_TERMS.
   It has no user requirement/subject refs and earns no subject-preference coverage.
4. This covers empty preferences, nonempty/no-intent, named-only and itinerary/set-only
   preferences. Named targets still use Google operational resolution. Avoid-only meanings
   do not become positive discovery queries. Keep normalized semantics available downstream.
5. Embed only query text, not dates, money, travelers, IDs or the whole request. No second
   interpretation model, raw preference keyword/regex rules or inferred walking radius.

<a id="b-f57630f15dd9-3"></a>

Top-K=10/query, <=20 slots. Round-robin ordered query streams, each cosine descending then
entity ID; deduplicate entity IDs and union origins across at most 20 positions. Consider at most SIX entities
that need NEW resolution; already-known canonical IDs do not consume this attempt cap.
No cross-query cosine score comparison, adaptive K, second pass or guaranteed RAG quota.

<a id="b-f57630f15dd9-4"></a>

Use a 15 km exact radius around resolved destination coordinates, not locality equality.
DestinationContext has no trustworthy country code; initial country=None rather than parsing
a displayed destination string. A future already-verified typed country can constrain the
same filter; no extra acquisition for it. Recheck current Google positions within 15 km for
RAG-only candidates. This is an engineering coverage boundary, not city limits or walking
tolerance. Existing Google discovery geography is unchanged; border/large-city limits remain.

<a id="m-079a102cbe2f"></a>
## Historical Phase6 baseline E. Google resolution and stage-aligned evidence

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-079a102cbe2f-0"></a>

- A stored Google ID already in current Google observations only adds TripWorld provenance;
  its normal Details stage provides current enrichment, without an extra validation call.
- Otherwise obtain/reuse the same PLACES_DETAILS_FIELD_MASK and language as main enrichment.
  One current response serves identity and later enrichment. Reject malformed/mismatched IDs
  and invalid coordinates; there is no separate validation API followed by duplicate Details.
- Missing/failed ID permits ONE name/location fallback per entity, at most TWO searches/trip.
  Use preferred corpus name plus available locality, bias around corpus coordinates,
  page_size=3 and the existing candidate-search mask. Bias is not strict geographic filtering.
- Require actual fallback coordinates within 1 km of corpus coordinates AND the 15 km
  destination scope, plus exact Unicode/case/spacing-normalized name equality to a recorded
  corpus name/alias. Exactly one qualifying canonical ID is required. Ambiguous/no match
  skips; no fuzzy guess, alias LLM or iterative alias searches. Fetch/reuse its Details and
  recheck identity/geography. Direct-ID displacements >1 km are recorded and use this same
  bounded fallback instead of silently accepting a questionable corpus association.
- Filter resolved exclusions. Ordinary RAG failure skips/continues within budget. Existing
  unresolved REQUIRED/EXCLUDED clarification cannot be silently bypassed by corpus guesses.
  A bad RAG association must not invalidate an otherwise valid Google candidate.

<a id="b-079a102cbe2f-1"></a>

The 1 km identity tolerance is proposed and deliberately conservative; it may miss real
relocations or aliases. It is not a user preference threshold or proof of identity by itself.

<a id="b-079a102cbe2f-2"></a>

Keep full early Details in cache/ledger. Admission sees only cheap current candidate fields
and origins, not early rating, price, opening-hours richness or Profile. After the normal
admission order/c_raw cut, the same Details loop promotes compatible cached responses into
structured evidence/rating. Date/status checks, R_pool, review allocation and supply policy
remain the same. Early paid data discarded by admission is a known cost, not a reason to
give it privileged admission. An existing Google candidate's pending Details should not be
prefetched merely because RAG also returned it.

<a id="b-079a102cbe2f-3"></a>

TripWorld categories/enrichment remain retrieval priors and static discovery provenance,
never Google current facts, official claims, ExperienceProfile or verified satisfaction.
Reviews/Profile remain their existing evidence chain. Supply/itinerary evidence references
retain Google evidence plus separate actual TripWorld discovery origins.

<a id="m-c32f17d52a20"></a>
## Historical Phase6 baseline F. Approved incremental budget, caching and degradation

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-c32f17d52a20-0"></a>

| Item | Approved per-request bound |
| --- | --- |
| Query texts/vectors | <=2, <=200 code points and <=512 tokens each, <=1024 tokens total; reject overflow, do not truncate meaning |
| Embedding HTTP sends | <=1 batch of missing queries, retry=0, <=8 s |
| Retrieval SQL | <=2, Top-K=10 each, <=3 s statement timeout each |
| DB connect | <=2 s; compatibility work also inside total phase limit |
| New-resolution entities attempted | <=6; known Google/request-resolved IDs are free provenance unions; scan <=20 positions |
| Incremental Details sends | <=8 total shared between direct-ID and fallback results |
| Incremental fallback searches | <=2, <=3 results each, one per entity, no pagination |
| Incremental Google call | <=4 s and remaining phase time, retry=0 |
| Whole RAG phase | <=30 s including connection, compatibility, embedding, retrieval and resolution; sequential initially |
| Main supply/acquisition | Unchanged C/R/K; candidates<=36, final<=16, main Details<=18, candidate searches<=12, Reviews/Profile<=6 |
| Nearby | Unchanged: <=3 sends, 10 results, 800 m, 300 m reuse, 10 s, <=4 s/request, no retry, 0-3 references |

<a id="b-c32f17d52a20-1"></a>

Worst-case Google ceilings become 18+8=26 Details, 12+2=14 candidate/fallback searches,
plus existing destination search<=1 and separate Nearby. Details retains its rating-inclusive
mask: this is NOT zero incremental Google cost. No new generation/Profile/Web/Routes budget.
These are ceilings, not estimated usage or bills; the phase deadline may stop work earlier.

<a id="b-c32f17d52a20-2"></a>

Use a separate V2 budget ledger, not larger main ToolBudgetLimits (which affect capacities)
or borrowing main/Nearby allowances. Reserve before sends; failed sends consume attempts.
Cache hits cost no new send and preserve original phase ownership. Shared Details key stays
(operation, place_id, exact field_mask, language). Existing acquisition caches _ProviderResult
failures as values: preserve negative memoization so main enrichment does not retry the same
failed request. RequestCache itself does not cache raised exceptions; record RAG failure keys.
Sequential execution avoids adding a concurrency/single-flight subsystem.

<a id="b-c32f17d52a20-3"></a>

Embedding cache includes exact text and SPACE_ID. Retrieval adds scope, K, corpus and policy.
Fallback keys include complete effective request parameters, not name only. Origins are
unioned despite cached results. Report attempts/sends/cache hits/resolution failures separately.

<a id="b-c32f17d52a20-4"></a>

Before each operation check remaining monotonic time. Cancel and await I/O cleanup; no detached
worker may write results after return. User cancellation propagates. DB/embedding/compatibility
failure stops remaining RAG work; individual resolution failure continues within remaining
limits. Keep already obtained Google observations and validated partial RAG successes. Never
restart the V1 planner, interpretation or paid acquisition. Trace complete/empty/partial/
unavailable/deadline-limited/budget-limited/no-geographic-scope separately.

<a id="b-c32f17d52a20-5"></a>

Google-only continuation is a normal degraded V2 path. If the original main pipeline itself
has no usable candidates or an unresolved REQUIRED identity, preserve its failure semantics.

<a id="m-31c71e22e815"></a>
## Historical Phase6 baseline G. File impact and version boundaries

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-31c71e22e815-0"></a>

Proposed new files (not present implementations):

<a id="b-31c71e22e815-1"></a>

- backend/app/versions/v2/{__init__,graph,runner,state,config}.py and scripts/run_v2.py;
  state/config may simply reuse common types where no new contract is needed.
- backend/app/services/tripworld_discovery.py: bounded orchestration and resolution.
- backend/app/tripworld/retrieval/runtime.py: cancellable embedding/read-only DB adapter.
- backend/app/policies/tripworld_query_plan.py and schemas/tripworld_discovery.py.
- A small versions/shared/ graph builder only as required for explicit V1/V2 injection.

<a id="b-31c71e22e815-2"></a>

Extend evidence/{models,selection_models,selection_normalization}.py, policies/poi_funnel.py,
services/{semantic_poi_pipeline,planning_supply_pipeline,evidence_acquisition}.py for origin
projection, canonical union, optional hook and explicit budget ownership with shared cache.
Extend runtime/config_models.py and config/runtime.yaml with separately versioned V2 settings;
preserve V0/V1 defaults. Adapt versions/v1/graph.py minimally for the shared builder without
changing its flow; retain independent V1 runner behavior. Extend planning_supply_result.py,
observability/run_trace.py and acceptance_session.py only for explicit V2 diagnostics/dispatch.
Developer dispatch may need an explicit V2 registration; product default/frontend do not.

<a id="b-31c71e22e815-3"></a>

Reuse corpus/manifests/storage, policy, space constants, SQL builder and geography utilities.
Keep interpreter/prompts, deterministic supply algorithm, Review/Profile, primary generation
DTO/prompts, itinerary_2 and reference discovery policy unchanged. Main/reference/anchor
ledgers remain separate; Nearby anchors are actual scheduled canonical IDs with Google
coordinates, regardless of their discovery origin. No B2 cleanup or V3 mechanisms.

<a id="m-07ae647fd61a"></a>
## Historical Phase6 baseline H. Offline test matrix

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-07ae647fd61a-0"></a>

| Test group | Required result |
| --- | --- |
| Google/RAG same ID; multi-query repeated hits | One identity, real origins unioned, no fake rank/duplicate reward or fetch |
| RAG-only stored ID | Current Google resolution, reusable Details, entry into ordinary supply possible |
| Missing/invalid ID fallback | One bounded search, unique exact alias and both geography checks; ambiguity skips |
| Resolution failures | Later candidates considered within limits; partial successes retained |
| Cache / early Details | Same key reused, failure not retried, incompatible mask not reused; rating hidden until normal stage |
| REQUIRED/EXCLUDED | Original operational semantics retained; ordinary RAG errors cannot silently drop a required identity |
| Priors vs facts | Corpus text cannot populate current Google facts/Profile or verified claims |
| Empty/no-intent/named-only/set-only/avoid-only | Explicit default with no user refs, no extra interpreter or raw NLP |
| Query ordering/duplicates/overflow | Deterministic plan/round-robin, bounded vectors/hits/entities, no adaptive K |
| DB/embedding/compatibility errors | Existing Google work reused; no planner restart or repeated paid calls |
| Deadline/timeout/cancel | No later scheduling, no background mutation, cleanup awaited, cancellation propagates |
| V1/V0 differential fixtures | V1 no RAG and identical calls/capacities/supply without extension; V0 no external calls |
| Main/Nearby integration | RAG before supply, final scheduled anchors only, unchanged reference budget and main itinerary |
| Provenance mapping | RAG-only nullable rank accepted only with real origin; origins survive enrichment/output traces |

<a id="b-07ae647fd61a-1"></a>

Use fake embeddings, fake async DB and MockTransport, no live services in normal tests.
Reuse SQL/geographic fixtures and add adapter parameter/cancellation coverage. After authorized
shared-contract/graph changes: affected tests, one full backend run, Ruff and diff checks;
preserve original failures and affected reruns. This design task runs none of them. Historical
reference results remain 829 passed / 9 skipped / 8 failed, then 53 affected tests passed.

<a id="m-3013e0fa9830"></a>
## Historical Phase6 baseline I. Future small V2 live plan (not authorized now)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-3013e0fa9830-0"></a>

After implementation/offline approval, propose at most TWO fresh V2 runs: Tokyo and Melbourne.
Saved Phase 5 15-km post-policy coverage is 46,020 versus 284 entities: dense versus sparse.
Runtime geocoding centers may differ; these are destination-selection evidence, not promised
runtime counts. No Phase 5 matrix rerun, V1/V2 superiority benchmark or replacement samples.

<a id="b-3013e0fa9830-1"></a>

Freeze complete legal three-day structured requests, travelers, total budget/currency and one
named REQUIRED place each. Tokyo uses a positive discovery preference; Melbourne uses named-only
preferences to exercise the no-discovery/default case. Exact requests/named places/dates require
later live-plan approval before calls. Do not force an intent if the interpreter returns none.
Empty-preference interpretation-skipping remains offline-covered; no extra third scenario.

<a id="b-3013e0fa9830-2"></a>

Record actual run_v2, input/config/prompt/schema/corpus hashes, query origins and refs, embedding
and SQL work, unique hits/Google overlap, resolved/new IDs, admitted/enriched/supplied/scheduled
RAG-only and mixed-source IDs separately, skips, cache and failures/degradation, incremental
Google sends, usage and phase latency. Nearby references do not prove RAG main integration.
Zero new/scheduled RAG candidates is an observation, not permission to retune or rerun.

<a id="m-a561f50b5622"></a>
## Historical Phase6 baseline J. Minimum recoverable baseline before implementation

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-a561f50b5622-0"></a>

Inspection found 79 modified tracked files, 11 tracked deletions, 53 untracked status entries
(some are directories), and an empty index. Existing implementation changes are not Phase 6.
This task updates documentation only and does not reset, stage or commit that work.

<a id="b-a561f50b5622-1"></a>

Before implementation, separately approve a coherent checkpoint of shared input/interpreter,
deterministic acquisition/supply, DTO/mapping, V0/V1 graph/runner, itinerary_2/Nearby,
runtime config/locks, acceptance harness, tests/fixtures and current docs. Save migration
deletions together with replacements. A tracked diff alone misses untracked executable files.

<a id="b-a561f50b5622-2"></a>

Untracked history includes semantic_evaluator.py, semantic_evaluation/projection/set_selection
policies/schemas, test_b2_* modules, scripts/analyze_b2_decision.py, b2_development_fixtures.py,
measure_b2_contract.py, measure_b2_policy.py and docs/b2_implementation.md. These lack a committed
file baseline. Preserve them in a separately scoped historical commit group or secure local
snapshot. semantic_poi_pipeline.py is also untracked but contains ACTIVE inherited acquisition:
it is not disposable B2 history. No experiment cleanup is proposed.

<a id="b-a561f50b5622-3"></a>

Save pre-existing frontend changes separately; they do not block backend design. Ignored
thesis_notes and raw captures/logs are separate local evidence, retained as-is; an optional
separately authorized external backup/inventory is preferable to force-adding them. Never
commit credentials, raw provider payloads, datasets, vectors or DB files. Actual commit/save
scope requires separate approval; this proposal performs neither operation.

<a id="m-91685180c47b"></a>
## Historical Phase6 baseline K. Approved implementation choices (live approval remains separate)

_Source context: Phase 6 Proposal: TripWorld Main-Candidate Discovery for V2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-91685180c47b-0"></a>

Approve the V2-only pre-admission hook and source-neutral origins; unchanged supply policy
and capacities; <=2 queries, Top-K 10, <=6 new-resolution entities; one explicit top-attractions default;
15 km scope without inferred country; conservative unique alias + 1 km fallback;
<=8 incremental Details and <=2 fallback searches; one embedding batch; 30-second phase
with 8/3/2/4-second embedding/SQL/connect/Google limits, zero retries; independent budget
ownership, equal stage visibility and Google-only degradation; baseline preservation first.

<a id="b-91685180c47b-1"></a>

Risks: sparse coverage, conservative identity misses, corpus displacement/subvenues, no source
quota and ID-sorted admission limiting retrieval-rank influence, early paid Details later
discarded, broad defaults and shared-hook regression. Defaults are proposed engineering limits,
not tuned optimums. Existing exact retrieval remains the chosen infrastructure. Nearby does
not solve low activity count/date coverage. No selector or main-density redesign is included.

<a id="b-91685180c47b-2"></a>

The original design-only work stopped before implementation. The later approved implementation
and its exact validation limits are recorded above. No live, corpus rebuild, cleanup, staging,
commit/push or re-freeze is authorized by implementation completion.

<a id="b-91685180c47b-3"></a>

---

<a id="m-28011df8675a"></a>
## Historical proposal (preserved, superseded; not executable guidance)

_Source context: original document introduction/navigation. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-28011df8675a-0"></a>

The following text retains the older 2026-09-18 proposal and intermediate B2-era header.
Its Q_rel, review-sensitivity, candidate contracts and approval questions are historical.
Only the current proposal above is the Phase 6 implementation approval target.

<a id="m-188b69f89bcc"></a>
## Historical Phase 6 Proposal: TripWorld Candidate Discovery

_Source context: original document introduction/navigation. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-188b69f89bcc-0"></a>

Status: **Superseded selection adaptation; runtime integration still paused.**
The historical Q_rel adaptation below was not implemented. B2 now supplies the shared
source-neutral selection boundary; a future V2 plan must be revised and separately approved.
See [POI selection evolution](development_record.md) for the decision history and
[Current POI selection](development_record.md) for B2. TripWorld Phases 1-5 remain accepted.
V1 is reopened, not re-frozen. The dated repository observations and proposed APIs below
refer to the 2026-09-18 baseline, not current executable interfaces.

<a id="m-8a1faf887e3a"></a>
## 1. What exists and where integration belongs

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-8a1faf887e3a-0"></a>

`backend/app/versions/v1/graph.py` executes one typed requirement interpretation,
date validation, destination resolution, `acquire_candidate_funnel`, review-aware
selection, Weather, Routes, Official Web, itinerary generation and final date checks.
`V1EvidenceAcquisitionService.run_candidate_funnel()` in
`backend/app/services/evidence_acquisition.py` currently owns:

<a id="b-8a1faf887e3a-1"></a>

```text
build_place_search_intents
 -> search_candidate_observations
 -> merge_search_observations
 -> named-place resolution / exclusions
 -> select_pois(capacity=c_raw, require_details=False)
 -> select_pois(capacity=r_pool, require_details=False)
 -> current Details/rating for contenders
 -> select_pois(capacity=k_final, require_details=True)
 -> review-aware refinement in a later graph node
```

<a id="b-8a1faf887e3a-2"></a>

The exact proposed integration seam is **after ordinary Google observations exist,
before the merged pool is narrowed to C_raw** (currently immediately before the
`merged = merge_search_observations(observations)` statement). The implementation
would live in a **V2-owned funnel**, not a new branch inside V1's method. Named-place
resolution must first be computed from the existing Google observations/intents and
protected through union; RAG must not silently reinterpret unresolved explicit names.

<a id="b-8a1faf887e3a-3"></a>

```text
Same typed requirements and resolved destination
 -> existing explicit-name / Google interest discovery
 -> bounded TripWorld semantic discovery in parallel conceptually, ordered operationally
 -> on-demand current Google acquisition for needed RAG hits
 -> canonical union, preserving source histories and named-place constraints
 -> C_raw -> R_pool -> Details reuse/acquisition -> review-sensitive final selection
 -> existing selected-POI evidence and itinerary behavior
```

<a id="b-8a1faf887e3a-4"></a>

Do not append RAG POIs after final selection. Do not call the entire V1 planner again
on RAG failure: that repeats interpretation and potentially paid calls. Continue with
the already available Google-only observations, typed semantics, cache and budgets.

<a id="b-8a1faf887e3a-5"></a>

There is currently no `backend/app/versions/v2/` graph/runner or `scripts/run_v2.py`.
The shared `SystemVersion` already lists V2, but that enum does not implement it.
The product `PlanningService` currently delegates to V0; Phase 6 must not silently
switch the product API/frontend to V2. A separate V2 runner is the initial entry point.

<a id="m-9d739b3c59a2"></a>
## 2. Existing contracts and concrete incompatibilities

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-9d739b3c59a2-0"></a>

| Current component | Reuse / constraint |
| --- | --- |
| `TripIntentExtractionResult` in `schemas/trip_intent.py` | Reuse the single V1 LLM extraction and source-span validation unchanged |
| `PoiInterest`, `ExperiencePreferenceIntent`, `NamedPlaceIntent` | Semantic query inputs; no second parser or raw-text regex interpretation |
| `PlaceSearchIntent` / `SearchIntentKind` | Reuse stable intent identity/importance where applicable |
| `DestinationContext` in `evidence/models.py` | Already contains coordinates; has no country or radius |
| `RetrievalService` / `GeographicScope` | Existing ENRICHED query embedding, fixed production policy and exact retrieval |
| `GooglePlacesProvider`, request/response DTOs, normalization | Current identity/information acquisition; preserve fixed masks and reviews separation |
| `RequestCache`, `ToolBudget` | Reuse request-local semantics with explicit V2 additions described below |
| `QueryIntentHit` | Keep unchanged: it explicitly means one unfiltered Google search position |
| `PlaceSelectionInput` | Requires at least one Google hit; cannot represent RAG-only candidates as-is |
| `PlaceCandidate` | Requires nonnegative `provider_rank`, even for downstream evidence; needs an explicit compatibility solution |
| `merge_search_observations` | Chooses a canonical row using minimum Google rank; not a multi-source canonical merger |
| `select_pois` / review sensitivity | Hardwired to Google hits for Q, C and stable ties; cannot be reused blindly with fake hits |

<a id="b-9d739b3c59a2-1"></a>

The main issue is wider than changing `q_rel()`: Google-only assumptions also occur
in `c_cov`, `best_rank`, required-place ordering, the canonical merge, and
`find_review_sensitive_candidates()` (`min(hit.provider_rank ...)`). Review
counterfactuals call the same selector repeatedly. A new relevance rule must be used
consistently at C_raw, R_pool, no-review final, review sensitivity and final selection.

<a id="m-9a9516c998d7"></a>
## 3. Query construction from existing semantics

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-9a9516c998d7-0"></a>

Propose a small V2 `RagQueryPlan` with:

<a id="b-9a9516c998d7-1"></a>

```text
query_id / query_builder_version / semantic_text
originating_intent_ids / intent_kind / source_spans
purpose: poi_interest | experience_discovery | generic_fallback
geographic_scope: latitude, longitude, radius_km, country?
fetch_k / max_fetch_k / deterministic_query_order
```

<a id="b-9a9516c998d7-2"></a>

`DiscoveryIntent` today holds only semantic text; the new plan surrounds it with
provenance and bounds. It does not change the frozen corpus/embedding space.

<a id="b-9a9516c998d7-3"></a>

Use the validated `PoiInterest.surface` and its importance to create one query per
distinct non-named interest, up to a configured maximum. Reuse the corresponding
Google `PlaceSearchIntent.intent_id` where the same interest exists; otherwise use
a stable source-independent ID derived from the normalized interest and importance.
Repeated RAG queries must not invent additional coverage rewards for the same interest.
Deduplicate exact normalized texts and execute in deterministic priority order.

<a id="b-9a9516c998d7-4"></a>

Use a finite mapping of existing experience enums to positive discovery phrases, not
a new parser: e.g. AVOID_CROWDS -> quieter/less crowded places; PREFER_FAMILY_FRIENDLY
-> family-oriented attractions. PREFER_ACCESSIBLE may guide discovery but cannot
assert accessibility. Walking and visit-duration needs lack reliable corpus fields;
retain them for existing experience/routes handling, with no claimed hard retrieval
filter. Query wording is a heuristic to approve and version, not factual inference.

<a id="b-9a9516c998d7-5"></a>

Prefer a small list of separate interest queries and at most bounded supplementary
experience queries over one very long concatenated request or every Cartesian
interest/preference combination. Experience-only queries carry provenance but do not
create new C_cov interest IDs. Where interests exist, they may be included as text
context, but do not turn every compound query into proof of matching every interest.
If no usable typed interests exist, reuse a bounded generic fallback concept and
fallback importance. Named-place queries remain exclusively in the existing explicit
path. Requested admission/hours questions belong to downstream official evidence,
not additional RAG queries. Do not embed dates, budgets, IDs or the raw full request.

<a id="b-9a9516c998d7-6"></a>

Coordinates come from the existing `resolve_destination()` result. Radius is a
validated V2 runtime policy, not an inferred locality equality or a hardcoded Sydney
scope. Optional country stays null initially: current `DestinationContext` has no
country, and parsing a formatted address would invent an unreliable contract. A
future structured country extension needs a separate reviewed provider mapping.
No automatic unbounded radius expansion; any bounded retry scope must be explicit.

<a id="b-9a9516c998d7-7"></a>

`RetrievalService` is currently synchronous, writes query checkpoints, uses build-sized
timeouts/configuration and expects a live DB connection. A V2 wrapper must provide
request deadlines, short DB statement/connection limits and bounded query tokens/
retries without changing offline Phase 5 behavior. Use a bounded worker-owned
connection and adapter timeout; an async timeout alone does not stop an underlying
thread/API request. Avoid sharing one psycopg connection across concurrent tasks.
For planning, prefer request-scoped query-vector reuse; keep existing disk checkpoints
for the standalone CLI rather than silently persisting every user's semantic query.
No new infrastructure, vector index, embedding model or corpus regeneration is needed.

<a id="m-0222a361af56"></a>
## 4. Ranked-stream resolution and deterministic stopping

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-0222a361af56-0"></a>

Each query yields an ordered stream. Within a stream order is cosine descending,
then entity ID (as in Phase 5). Across queries use deterministic importance-prioritized
round-robin, preserving within-stream order; raw cosine from different queries is
not a globally calibrated score. Keep every originating hit even when entity/Google
identity deduplication means acquisition occurs only once.

<a id="b-0222a361af56-1"></a>

Proposed state machine:

<a id="b-0222a361af56-2"></a>

```text
for hit in stable merged stream:
    attach any already-known discovery provenance
    if usable target reached: stop new acquisitions
    if entity/canonical ID already processed: reuse outcome; do not spend again
    if existing Google ID: obtain/reuse current Details
    else, or after failed ID acquisition: bounded name/location search
    uniquely reconcile fallback -> obtain/reuse current Details
    validate canonical ID, current coordinates and existing POI eligibility
    if unresolved/unusable: record reason; continue to next hit
    union by returned canonical Google ID
    count only a distinct usable RAG contribution toward target
```

<a id="b-0222a361af56-3"></a>

Keep all local already-retrieved provenance even when acquisition stops early. Define
the target as **new distinct usable canonical candidates beyond the Google pool**;
an overlap adds discovery provenance but does not satisfy a target intended to improve
recall. Record both total RAG-resolved identities and net new identities. Overlap can
still cost a Details call if current information was not acquired already. Stop on
usable target, API/fallback budget, deadline, configured stream cap or exhaustion.

<a id="b-0222a361af56-4"></a>

`usable` means current Google identity/coordinates and the existing structured
eligibility checks succeed; missing rating alone is allowed. Permanently closed,
invalid-coordinate, excluded or definitely-after-trip opening entities do not count.
V1 treats temporary closure/unknown status as risks, not unconditional exclusion;
preserve that behavior and allow existing evidence handling to address it.

<a id="b-0222a361af56-5"></a>

Recommend configuration expressed in relation to existing effective capacities:
`usable_rag_target <= c_raw` and bounded by acquisition headroom; initial fetch K can
be `min(max_fetch_k, ceil(oversampling_factor * target_for_query))`. Numeric defaults
remain unapproved. Start with one acquisition at a time for deterministic spend and
stopping. Concurrency >1 requires ordered reservations, bounded in-flight work and
deterministic result commitment; it must not resolve the entire retrieved set eagerly.

<a id="b-0222a361af56-6"></a>

Phase 5 exposes Top-K, not pagination. If a configured incremental fetch is approved,
reuse the same query vector with larger K through `PostgresSearch`, skip previously
seen IDs and stop at max K. Do not re-embed unchanged text or promise an unlimited
server cursor. Freeze the corpus/version for a run or abort RAG if its identity changes.

<a id="m-ce32492f60df"></a>
## 5. ID-first, fallback and FSQ-only acquisition

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ce32492f60df-0"></a>

For an ID-backed hit use `PlaceDetailsRequest` with **the existing full
`PLACES_DETAILS_FIELD_MASK` and matching language**. This is the actual current-info
acquisition, not a small validation call followed by another identical Details call.
Reviews remain separate and selective. Store the normalized Details/rating result
and use returned Google ID/name/location as canonical metadata. Preserve the historical
TripWorld ID and any returned-ID redirect as resolution provenance.

<a id="b-ce32492f60df-1"></a>

A 200 response is not sufficient if identity/coordinates are unusable. Recheck the
Google coordinates against destination scope and plausibility relative to the source
entity. Do not reject ordinary renamed places solely on different spelling when an
ID succeeds; reject unresolved geographic contradictions. Matching thresholds and
handling of valid moved businesses require explicit configuration/approval.

<a id="b-ce32492f60df-2"></a>

For a failed/stale ID or FSQ-only entity, Text Search uses a bounded preferred-name
plus locality/destination query and source-coordinate bias, reusing the existing
request DTO and mask. Existing Google bias is a fixed **50 km circle** and is not a
hard radius filter. The resolver must apply its own Haversine checks to the results.
Use exact normalized preferred-name/known-alias evidence plus geographic consistency
for an initial conservative unique match. Do not accept the first search result
unconditionally, invent an LLM identity judge or resolve ambiguity by provider rank.
If multiple plausible matches remain, reject/replace. Exact matching sacrifices recall;
more permissive fuzzy matching needs separate justification and tests.

<a id="b-ce32492f60df-3"></a>

A selected fallback search result must obtain the full current Details mask before
RAG-only admission. Search success alone is not the full current-info contract. Search
rank for a name/location resolution query is **identity evidence**, not relevance to
the originating interest; never feed it into Q_rel. The existing provider does not
expose detailed HTTP status categories in its service outcome; initially treat a
sanitized acquisition failure as fallback-eligible under the bounded budget. A future
error-code extension could distinguish quota/auth outages from stale IDs, but is not
necessary to pretend those distinctions already exist. No global Google validation.

<a id="m-ed77e27483cc"></a>
## 6. RequestCache and paid-call reuse

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ed77e27483cc-0"></a>

Actual current keys in `V1EvidenceAcquisitionService` are:

<a id="b-ed77e27483cc-1"></a>

```text
Details: ("place_details", place_id, field_mask, language_code)
Search:  ("places_search", casefold(text_query), page_size, field_mask,
          include_future_opening_businesses, (lat, lon) or None, language_code)
Reviews: ("place_reviews", place_id, field_mask, language_code)
```

<a id="b-ed77e27483cc-2"></a>

`_cached_provider_call_with_status()` checks cache before its factory consumes budget.
It caches `_ProviderResult` for successes **and provider failures**; budget rejection
is outside the provider catch and is not a successful cached result. `RequestCache`
itself does not cache raised exceptions and has no in-flight single-flight protection.

<a id="b-ed77e27483cc-3"></a>

Propose a small public acquisition gateway delegating to existing cache/key logic,
with explicit charging context and typed acquisition outcome. Keep current private
methods as unchanged-default wrappers for V1. Both V2 Google discovery and RAG
resolution must share one gateway/cache instance. Do not directly inject a raw DTO
under a key whose existing value type is `_ProviderResult`, or create a second cache
namespace for the same successful Details request. Canonical redirects additionally
reuse the already obtained outcome by returned ID within the gateway, with provenance;
they must not require a second paid Details request just to populate that alias.

<a id="b-ed77e27483cc-4"></a>

Match exact masks/language so later contender enrichment hits the cache. A minimal
sanity-check mask cannot satisfy full Details, and reviews cannot satisfy Details.
Failed IDs/attempted fallback keys are reused within the request; revisiting the same
failed hit must not spend again. For initial concurrency=1 existing cache semantics
are sufficient. Add V2-local keyed locks/single-flight only if concurrency is approved;
do not silently alter V1 scheduling or assume the current cache already guarantees it.

<a id="b-ed77e27483cc-5"></a>

Early successful RAG Details remain in the cache/evidence sidecar. During C_raw/R_pool
scoring, project rating/details to the same stage-appropriate visibility as Google
search observations. Otherwise RAG would receive R_rating before Google gets it.
Only the selected contender stage exposes Details/rating symmetrically. Candidates
outside R_pool do not bypass its limit merely because their Details were preloaded.

<a id="m-925549dd822f"></a>
## 7. ToolBudget: protect the baseline, expose incremental cost

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-925549dd822f-0"></a>

Current normal limits are candidate searches **12**, Details **18**, candidates **36**,
final POIs **16**, and reviews/Profile **6**; hard search/Details ceilings are **12/20**.
Capacities are trip-dependent: `k_final=min(16,2*days+2)`, `r_pool=max(10,k_final+2)`,
`c_raw=max(20,2*r_pool)`, reduced by operating limits. R_pool is currently limited by
configured Details capacity, not by already-spent calls. Pre-resolving RAG from that
same unreserved budget can starve ordinary enrichment and break graceful degradation.

<a id="b-925549dd822f-1"></a>

Existing PLACE_DETAIL_CALLS and CANDIDATE_SEARCH_CALLS describe the operation correctly,
but have no allocation ownership, reservation or RAG/fallback dimension. Recommend:

<a id="b-925549dd822f-2"></a>

- Retain operation totals for every actual Google request, including failures.
- Add narrow V2 allocation counters for RAG resolution calls and fallback searches,
  plus query count/token/deadline bounds; do not repurpose review or destination counters.
- Reserve the baseline discovery and Google-only R_pool Details entitlement before
  permitting incremental RAG cache misses. Run explicit/ordinary Google searches first.
- Cache hits cost zero API units. A failed direct ID costs one Details unit; fallback
  search costs a search unit; a subsequent Details miss costs another Details unit.
  Every real HTTP attempt counts; the current Google transport has retries disabled.
- Use atomic reservation/checking across operation totals and RAG sublimits before
  calling the provider. No charge refunds for failed paid attempts. Blocked budget
  checks are logged separately and do not increment HTTP-attempt counts.

<a id="b-925549dd822f-3"></a>

**Budget decision requiring approval:** keeping the existing 12/20 hard ceilings can
leave little or no incremental capacity (especially fallback searches and long trips).
The design must then clip RAG target to available reserved headroom, including zero.
To permit a useful positive target consistently, approve explicit **V2-only total
ceilings** and normal limits in centralized configuration while preserving V1's exact
12/20 ceilings and normal values. A new RAG bucket must not secretly bypass a claimed
global limit; the effective V2 total is baseline allocation plus approved incremental
allocation and must be shown in trace/cost reports. This proposal recommends that
explicit V2 envelope, but does not freeze its numerical values or modify any limits.

<a id="b-925549dd822f-4"></a>

Candidate counters count distinct admitted C_raw IDs, not every raw SQL hit or every
failed resolution. FINAL_POIS is charged once, after review-aware selection. Review,
Weather, Routes and Web budgets are preserved. RAG outage must not spend their budgets.
No unbounded second pass or budget refund is used to conceal replacement costs.

<a id="m-9e3ef4c58416"></a>
## 8. Canonical merge and two kinds of provenance

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-9e3ef4c58416-0"></a>

Use returned current **Google Place ID** as the canonical key. Source RetrievalEntity
IDs/FSQ IDs remain provenance. Union genuine Google interest hits and RAG discovery
hits separately; deduplicate repeated hit records by stable source/query/entity IDs.
Keep current Details once per canonical ID, preserve opening-date conflicts and
explicit exclusions, and never overwrite current Google facts with historical data.

<a id="b-9e3ef4c58416-1"></a>

| Case | discovery_sources | metadata_sources |
| --- | --- | --- |
| Google discovery plus optional local metadata | GOOGLE_PLACES | GOOGLE_PLACES, TRIPWORLD |
| RAG discovery then Google identity/current-info acquisition | TRIPWORLD_RAG | TRIPWORLD, GOOGLE_PLACES |
| Independent Google and RAG discovery | GOOGLE_PLACES, TRIPWORLD_RAG | GOOGLE_PLACES, TRIPWORLD |
| Explicit named-place path | USER_EXPLICIT (plus genuinely independent channels only) | GOOGLE_PLACES, optionally TRIPWORLD |

<a id="b-9e3ef4c58416-2"></a>

Google calls performed solely to resolve a RAG hit do not create GOOGLE_PLACES
discovery provenance. Likewise local metadata enrichment is not RAG discovery.
Store Google operation role (discovery vs resolution), original intent, raw search
position/count, RAG rank/cosine, corpus/space/hash versions, resolution path/attempts,
cache outcomes and stop reason. Actual run trace can later support source attribution;
this phase does not implement a formal V1-vs-V2 evaluation.

<a id="b-9e3ef4c58416-3"></a>

Google-first optional enrichment uses a batched indexed lookup on
`tripworld.entities.google_place_id`, which already has a unique nonnull index.
No extra Google request or embedding is needed. Missing rows/DB failures leave the
Google candidate untouched. Even locally excluded/anomalous metadata must not veto a
valid Google-first candidate: the TripWorld production policy governs its discovery
channel, not Google's independent path. Keep flags informational and priors out of
current facts/Profile. Lookup results also are not independent semantic interest hits.

<a id="b-9e3ef4c58416-4"></a>

Keep original Google observations immutable alongside the canonical union. If no
usable RAG contribution survives, run the original Google-only normalization and
selection projection, including its search-coordinate behavior. Do not let a failed
RAG attempt's cached Details silently change that baseline projection; this makes
the promised outage-equivalence test precise.

<a id="m-c5d2d5ab1fc4"></a>
## 9. Q_rel alternatives and recommendation

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-c5d2d5ab1fc4-0"></a>

Current `policies/poi_selection.py` computes, for each real Google hit:

<a id="b-c5d2d5ab1fc4-1"></a>

```text
w = 1.0 explicit_requirement, 0.8 normal_preference, 0.4 fallback
q(hit) = 30*w                                  if raw_count == 1
         30*w*(raw_count-1-zero_based_rank)/(raw_count-1) otherwise
Q_rel = max(q(hit)), default 0
```

<a id="b-c5d2d5ab1fc4-2"></a>

`actual_result_count` is the **raw response length**, even when invalid DTO rows are
filtered. It is not post-dedupe count or usable Google resolution count. Example:
Google normal-preference rank 0 of 20 contributes 24; rank 19 contributes 0. A lone
name-fallback result would wrongly contribute 24 if misrepresented as interest search.
RAG is 1-based Top-K rank with a truncated caller-chosen K, cosine has no shared
calibration, and resolution failures must not rerank the survivors to increase Q.

<a id="b-c5d2d5ab1fc4-3"></a>

| Alternative | V1 compatibility / determinism | Interpretability and source comparability | Complexity / experimental implication |
| --- | --- | --- | --- |
| A. Conservative Google-evidence Q; RAG-only Q=0 | Exact V1 Q formula retained for genuine Google hits; deterministic | Zero means no Google ranking evidence, not semantic irrelevance; makes no rank equivalence claim | Smallest new scoring policy; biases against RAG-only places and may underestimate its potential contribution |
| B. Explicit source-aware ordinal RAG relevance, e.g. bounded rank decay combined by max | V1 unchanged if opt-in only; deterministic with fixed query policy | Transparent new heuristic, but RAG score scale and Google scale still uncalibrated; not a relabeling of rank | More parameters, multi-query effects and ablations needed later; changing fetch K must not inflate scores |
| C. V2-wide common rank fusion such as weighted reciprocal rank | V1 binary can stay unchanged; V2 Google-only ranking can change | Common ordinal rule is explicit, but assumes comparable source weights rather than proving relevance equivalence | Changes selection even beyond added discovery, confounding future mechanism comparisons |
| D. Obtain new Google interest-query evidence for each RAG candidate | Can use a real Google hit if actually returned, never an invented rank | Restores provider evidence but cannot force Google to rank a desired candidate | Extra quota, possible exclusion of exactly the long-tail candidates RAG should add |
| E. Learned/calibrated or LLM relevance | V1 can remain separate, but new model/evaluation dependence | Calibration needs labels; LLM adds uncertain scoring behavior | Outside this phase and project scope; reject for initial integration |

<a id="b-c5d2d5ab1fc4-4"></a>

**Recommend A as an explicit, conservative Phase 6 starting policy**, subject to user
approval. Preserve all genuine Google hits and compute Q from them. For RAG-only
candidates set Q=0 with `relevance_evidence=google_rank_unavailable`; cosine/rank
control discovery resolution order and remain trace metadata, not a final score.
An overlapping candidate keeps its existing Google Q unchanged. No source-count bonus.
Do not claim this makes sources equally competitive: a RAG-only venue can lose to a
Google top hit solely because only the latter has Q evidence. If that tradeoff is
unacceptable, choose B explicitly before implementation; do not silently compensate
with a hidden quota, cosine threshold or positive constant.

<a id="b-c5d2d5ab1fc4-5"></a>

C_cov retains the formula `max(25*intent_weight for uncovered interest IDs)`, default
zero. Introduce a source-independent **InterestCoverageHit** separate from Google
QueryIntentHit. A RAG result from a POI-interest query contributes that same normalized
interest ID/importance after successful canonical resolution; this is discovery
association, not verified factual suitability. Identical interests from two channels
count once. Pure experience queries do not add coverage IDs or manufacture E evidence.
Coverage for interest queries remains a retrieval heuristic just as provider hits
were, so this extension must be explicit in later comparisons.

<a id="b-c5d2d5ab1fc4-6"></a>

Stable V2 ties: descending total, then the best genuine Google rank if present,
then canonical Google ID; missing Google rank sorts after finite ranks. This retains
the existing ordering for Google-only inputs and leaves RAG-only ties deterministic
without mixing rank spaces. RAG rank remains acquisition priority only under A.
Required named places keep priority and existing relative ordering. Review-sensitive
ties must use the same key, not `min()` over an empty Google-hit list.

<a id="m-6497f9f374a5"></a>
## 10. Selection contracts, reuse and unchanged C/G/R/E

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-6497f9f374a5-0"></a>

Propose `V2PlaceSelectionInput` with canonical candidate, a possibly empty list of
real `google_query_hits`, separate coverage hits, RAG hits/provenance, and the existing
structured evidence/rating/opening-date/coordinate state fields. Retain V1's strict
nonempty `PlaceSelectionInput.query_hits` invariant. Do not loosen QueryIntentHit or
populate it with synthetic rows.

<a id="b-6497f9f374a5-1"></a>

One narrowly scoped shared extension is needed for downstream `PlaceCandidate`:
allow `provider_rank: int | None` with null representing **no Google discovery rank**,
while V1 normalization still always supplies the same integer. Preserve V1's serialized
values and output path. V2 source query/category come from real originating semantic
intent; provenance lives in a V2 sidecar rather than unbounded fields in itinerary DTOs.
Audit every consumer before implementation: legacy `shortlist()` sorts provider_rank
and must never receive V2/null-rank inputs. This schema extension and its compatibility
tests require approval; an alternative separate canonical candidate type would require
more downstream projection/generalization, not justify a fabricated rank=0.

<a id="b-6497f9f374a5-2"></a>

Use V2-owned selection/merge orchestration and a source-aware selector policy. Reuse
unchanged pure eligibility, distance, rating and E scoring via a narrow structural
candidate view/protocol where needed; do not pass arbitrary duck-typed dictionaries.
Factor only the common pure greedy loop if practical, with V1's existing Q/coverage/
tie functions as unchanged defaults and V2's policy explicit. Differential tests must
prove the default V1 path exactly equivalent, including conflicts and review sensitivity.
Do not create a giant shared graph full of version conditionals.

<a id="b-6497f9f374a5-3"></a>

Review selection must use that same V2 selector in its counterfactual tests. Reuse
the existing Reviews acquisition, preprocessing, bounded Profile prompt/validation
and `score_experience` semantics. A narrowly injected selection/coverage/tie policy
with V1 defaults is preferable to copying the entire review pipeline. V2 funnel and
review input interfaces should expose the existing capacities, must/excluded IDs,
conflicts and evidence while adding the new provenance. The exact type seam is a
reviewable refactor prerequisite, not an assertion the present classes already support it.

<a id="b-6497f9f374a5-4"></a>

- **C_cov:** same 25*weight uncovered-interest formula; source-independent association
  extension documented above. No additional reward for multiple retrieval variants.
- **G_geo:** same initial 5, within 3 km 10, within 10 km 5, otherwise 0; use canonical
  Google coordinates. Current V1 normalization retains its search candidate even
  after Details; V2 must explicitly project current Details coordinates into its
  canonical candidate before final scoring/routes, leaving V1 untouched. Before
  Details, Google search coordinates are still current provider observations.
- **R_rating:** unchanged bounded Google-rating function, missing=0, no historical
  TripWorld rating. Keep stage visibility symmetric despite early RAG Details.
- **E_exp:** unchanged review-supported Profile -> deterministic score, no category
  priors or RAG similarity accepted as Profile evidence. Unknown remains unknown.

<a id="b-6497f9f374a5-5"></a>

The shared total stays Q+C+G+R+E. Candidate membership and hence review sensitivity,
coverage and geography can change in V2; unchanged formulas do not imply unchanged
selected sets. Current V1's general feasibility limitations are not repaired here.

<a id="m-b5f3eb38927a"></a>
## 11. Graceful degradation and consistency

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-b5f3eb38927a-0"></a>

| Condition | Required behavior |
| --- | --- |
| Zero RAG hits | Continue Google observations; record empty retrieval |
| OpenAI query embedding error/timeout | End affected RAG work within deadline; no second requirements call; use Google path |
| PostgreSQL outage/configuration/version mismatch | Mark RAG unavailable; no corpus mutation/rebuild at runtime; use Google path |
| Historical Google ID fails | Attempt configured bounded name/location fallback; preserve failure provenance |
| Fallback ambiguous/fails | Reject this hit, continue stream; no fabricated identity |
| FSQ-only cannot resolve | Same rejection/replacement rule |
| Google RAG allocation exhausted | Stop new misses; retain successful candidates and baseline budget entitlement |
| All RAG hits fail | Google-only staged selection with existing cache/results; no repeat discovery or interpretation |
| RAG hit overlaps Google | Merge provenance/intent association, reuse cached current info, one canonical candidate |
| Optional Google-first metadata lookup fails | Continue unchanged Google candidate |
| RAG produces excluded/invalid current POI | Do not admit; continue under the same budget |

<a id="b-b5f3eb38927a-1"></a>

Do not swallow baseline errors: if Google itself has no viable candidates, preserve
the existing clear failure behavior; RAG cannot guarantee generation without successful
current resolution. With identical successful Google responses and no usable RAG
contribution, the Google-only selection result should match V1. A service outage must
not alter Q, candidate capacities, named-place requirements or planner prompt semantics.
Returned output identifies V2 even if its RAG channel degraded; trace states the fallback.

<a id="m-f46bf9da99e4"></a>
## 12. Proposed implementation files and scope

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-f46bf9da99e4-0"></a>

Nothing in this list is created as executable Phase 6 code by this design task.

<a id="b-f46bf9da99e4-1"></a>

| Proposed area | Responsibility |
| --- | --- |
| `backend/app/versions/v2/{graph,state,runner,config}.py`, `scripts/run_v2.py` | Separate version orchestration, same typed extraction/date/output semantics |
| `backend/app/tripworld/integration/{models,queries,retrieval,resolution,merge}.py` | Typed query/provenance contracts, bounded synchronous-service adapter, ranked resolver, canonical union |
| `backend/app/services/v2_candidate_funnel.py` | Source union before C_raw and cache-aware staged enrichment |
| `backend/app/policies/v2_selection.py` | Approved Q policy, coverage projection, stable ties |
| Small public facade in `services/evidence_acquisition.py` | Existing identical request keys/outcomes plus explicit V2 acquisition charging, V1 defaults preserved |
| Historical scoring/review-policy seam (retired, never implemented for V2) | Superseded by B2; a future source-neutral integration design requires separate approval |
| `evidence/models.py` and minimal read-only selection input protocol | Nullable absent Google rank and shared evidence view, without fake provider hits |
| `runtime/{budget_limits,budget,config_models,config_loader}.py`, `config/runtime.yaml` | Explicit V2 allocations/ceilings/settings with backward-compatible V1 defaults; no hidden constants |
| V2-focused tests under `backend/tests/versions/v2/`, `backend/tests/tripworld/` | Fake-provider integration, policy and degradation checks |

<a id="b-f46bf9da99e4-2"></a>

Existing Phase 5 migrations/corpus/vector-space files remain unchanged. Batch local
Google-ID metadata lookup can live in the integration repository adapter and use the
existing index. No HNSW, IVFFlat, extra DB service, corpus refresh, reranker, new LLM
parser, frontend rollout or V3 validation/repair is in scope.

<a id="b-f46bf9da99e4-3"></a>

V2 settings should be one versioned optional section of the centralized runtime
configuration, validated only as appropriate, with old V1 values unchanged. Do not
make V1 startup require OpenAI embedding credentials or PostgreSQL. A V2 run with
unavailable RAG dependencies should log that channel's failure and use its Google
path; malformed policy values should still fail configuration validation.

<a id="m-a8444d50f7f1"></a>
## 13. Focused implementation test plan (future, no live paid calls)

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-a8444d50f7f1-0"></a>

Use fake Google/OpenAI providers, fixed request date, a tiny entity fixture and isolated
test DB where SQL integration is necessary. Assert calls, keys, scores and trace
provenance as well as final IDs:

<a id="b-a8444d50f7f1-1"></a>

1. TripWorld-only discovery resolves to a canonical Google POI; real Google hits remain
   empty, Q=0 under A, legitimate interest coverage present.
2. Google-only discovery reproduces V1 score vectors, ties, conflicts and final IDs.
3. Independent dual discovery produces one canonical candidate with two discovery
   sources; repeated RAG hits do not duplicate acquisition, score bonuses or capacity.
4. Google-first local metadata enrichment adds TRIPWORLD metadata only; missing or
   ineligible local records never reject or relabel Google discovery.
5. ID Details success is reused by contender enrichment with exactly one paid call.
6. Stale ID -> unique name/location fallback -> Details; count all three misses.
7. Failed/ambiguous fallback -> next ranked hit, including FSQ-only success/failure.
8. Name equality at distant coordinates and nearby homonyms are rejected; returned-ID
   redirects preserve alias provenance and avoid a second Details call.
9. Usable target stops acquisition; overlaps do not falsely satisfy net-new target;
   exhausted lists, configured max K, call/fallback budgets and deadlines all terminate.
10. Cache hits spend zero; failed outcomes are reused; mask/language mismatch is a
    distinct request; no DTO/result-type cache collision or duplicated in-flight call.
11. RAG budget use cannot consume reserved baseline Details/search/review capacity;
    current hard-limit clipping and any approved V2 total envelope are enforced.
12. USER_EXPLICIT required/optional/excluded identities remain authoritative across
    union, and RAG does not promote an unresolved name to a silently resolved must-visit.
13. OpenAI/DB outage, zero hits and all-resolution-failed cases reproduce Google-only
selection with one interpreter invocation, no repeated paid discovery, same dates.
14. Changing category priors cannot populate ExperienceProfile/E_exp; only actual
    review-derived validated evidence changes E. Review counterfactuals use V2 Q/ties.
15. Current Google coordinates drive G/routes; TripWorld coordinates remain provenance;
    early RAG rating cannot influence pre-Details narrowing asymmetrically.
16. Q alternatives have explicit unit expectations: no fake rank/count, no cosine Q,
    no fallback-name-query Q, no post-filter rank renormalization, shared-interest C
    counted once, optional missing Google rank never crashes a legacy consumer.
17. Stable output under shuffled input order, duplicate query hits and (if enabled)
    variable completion timing; no source-order-dependent canonical metadata choice.
18. V0/V1 full regression remains green; V1 startup works with RAG dependencies absent;
    V2 entry point works independently; product default does not switch accidentally.

<a id="b-a8444d50f7f1-2"></a>

Run focused tests during implementation, then full backend regression and Ruff.
No live smoke, formal relevance benchmark or V1/V2 outcome comparison is authorized
by this design-only task. A later user-approved small integration smoke may confirm
provider wiring after offline checks.

<a id="m-673bafc7ad97"></a>
## 14. Decisions requested before implementation

_Source context: Historical Phase 6 Proposal: TripWorld Candidate Discovery. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-673bafc7ad97-0"></a>

1. Approve conservative Q option A (genuine Google Q, RAG-only zero) or choose explicit
   source-aware option B for a separate parameterized relevance proposal.
2. Approve V2-only query/provenance/coverage contracts, nullable absent Google rank,
   and the minimal shared acquisition/selection/review seams with strict V1 parity.
3. Choose incremental V2 Google spend envelope versus strict existing-ceiling headroom;
   then set usable target, oversampling/max K, query cap and fallback cap together.
4. Approve conservative unique name/alias plus geographic matching; choose radius,
   identity-distance tolerance and timeout values through small development fixtures,
   without freezing arbitrary constants here.
5. Start sequentially; any later concurrency increase requires single-flight and
   deterministic budget reservations. Preserve exact pgvector retrieval for now.

<a id="b-673bafc7ad97-1"></a>

Main risks: Q=0 under-rewards RAG-only candidates; name matching can miss aliases;
historical identity merges mix contexts; paid resolution may dominate latency/cost;
too little reserved headroom disables useful retrieval; coverage remains uneven;
shared-policy seams can accidentally change V1 if not differentially tested.
The boundary is explicit: this document is a proposal, not approval to implement it.

<a id="m-cb0e66f7464f"></a>
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
[Phase 6 proposal](v2_development.md). Artifacts: logs/phase6_acceptance_20260920.
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
## Phase 6 proposal revision - 2026-09-19 (Proposed at that checkpoint)

_Source context: POI Selection Evolution: QCGRE, B1, B2. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-0a2db7988bbf-0"></a>

The user accepted post-itinerary Nearby discovery as implemented + bounded
development-live-validated, with no V1 re-freeze or further reference expansion. Historical
same-pool reference results remain superseded history, not evidence of the new mechanism.

<a id="b-0a2db7988bbf-1"></a>

The existing tripworld_phase6_proposal.md was revised in place around the actual
deterministic planning-candidate-supply pipeline, retaining the obsolete Q_rel/B2 proposal
as historical text. V2 is proposed to add bounded TripWorld discovery after Google/named
resolution and before admission, resolve current Google identity/Details on demand, union
real origins and reuse existing supply/generation/Nearby. No runtime integration occurred.

<a id="b-0a2db7988bbf-2"></a>

Raw and normalized interpreter results from the accepted nearby live run both have empty
DiscoveryIntent lists; distinctive/local and less-walking preferences were itinerary_style.
No search-dispatch loss was found. The proposed policy uses returned positive discovery
intents or one explicit system default, without another parser or changes to interpretation.

<a id="b-0a2db7988bbf-3"></a>

Proposed limits awaiting approval: two query texts, one embedding batch, Top-K 10 each,
six entities considered for resolution, eight incremental Details sends, two fallback
searches, 15 km scope, conservative 1 km exact-alias fallback and a 30-second phase.
Existing supply/review/Nearby capacities are unchanged. Early Details remain hidden from
admission and are reused in normal enrichment. Failures keep already acquired Google work.

<a id="b-0a2db7988bbf-4"></a>

Corpus manifests and accepted Phase 5 records were read without a database connection or
rebuild. Tokyo/Melbourne are proposed future development examples because saved 15 km
post-policy coverage differs (46,020 versus 284); this is not a formal benchmark design.
A recoverable baseline should preserve untracked active contracts and retained B2 history;
ignored captures/thesis notes remain separate archives, not automatically Git content.

<a id="b-0a2db7988bbf-5"></a>

This design task updates only PROJECT.md, the existing Phase 6 proposal and this evolution
record. No executable changes, tests, provider/model calls, DB operations, embedding rebuild,
cleanup, frontend work, stage/commit/push or re-freeze. Historical full-suite results remain
829 passed, 9 skipped, 8 failed, followed by 53 passing affected tests. Stop for approval.

<a id="m-ff970e716b21"></a>
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
## Phase 6 planning resumed - 2026-09-19 (design only)

_Source context: Capstone Project Context. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-35b7a552d4f7-0"></a>

The user accepted post-itinerary Nearby references as **implemented + bounded
development-live-validated**. Feature expansion ends here; this is not a complete
correctness proof or V1 re-freeze. Historical quality limits and test/live results remain.

<a id="b-35b7a552d4f7-1"></a>

Current main planning uses planning_request_2, shared optional preference interpretation,
application-owned identities, deterministic planning_supply_1, selective Reviews/Profile,
REQUIRED/OPTIONAL inputs, itinerary_2 primary generation and post-itinerary Nearby.
TripWorld Phases 1-5 remain accepted: ENRICHED text-embedding-3-small / 1536, saved vectors,
PostgreSQL + pgvector and geographically filtered exact retrieval. V1 does not call RAG;
V0 remains tool-free; no executable V2 runner exists yet.

<a id="b-35b7a552d4f7-2"></a>

The existing docs/tripworld_phase6_proposal.md now proposes V2-only RAG discovery before
shared admission/enrichment/supply, bounded on-demand Google resolution, canonical merge
with real multi-source origins, independent incremental budgets and Google-only degradation.
It supersedes obsolete Q_rel/B2 integration assumptions while retaining the old proposal as
history. Query planning reuses DiscoveryIntent or an explicit system default when absent,
without another interpreter. Runtime integration and numeric parameters await approval.
No executable changes, tests/live, DB/embedding rebuild, cleanup, frontend work or baseline
commit is included in this design task. A recoverable source/test/document checkpoint is
recommended before authorized implementation; ignored evidence archives remain separate.

<a id="m-f30b385cbc48"></a>
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

The old QCGRE integration proposal below is superseded by the [current V2 design](v2_design.md). Its selection context is explained in [selector experiments](v1_selector_experiments.md#causal-chain). The [joint quality acceptance](development_record.md#m-e07748f66be8) is the sole full shared result; this file owns V2-specific retrieval and performance events. The inline-vector shadow-table proposal remains paused, not implemented or disproven.


## Current implementation checkpoint acceptance (2026-09-20)

V2 current implementation checkpoint accepted. The [joint acceptance record](development_record.md#v2-current-checkpoint-acceptance)
keeps Tokyo/Sydney results, later offline sorting, finite triage and checkpoint governance once.
Normal RAG and RAG-only downstream use are demonstrated; exact-search variance remains engineering
work. No storage migration, re-embedding, permanent freeze or V3 implementation follows implicitly.
The [reproducibility audit](v2_tripworld_retrieval.md#clean-environment-reproducibility-audit-2026-09-20)
separates a functional rebuild from restoring exact local vector values.

## Shared first-generation extension - 2026-09-20

The shared coverage/role/diagnostic/K20 extension is implemented and checked offline;
no fresh live result is claimed. Acquisition goals remain unchanged and no repair loop
exists. The single [development event](development_record.md#first-generation-coverage-20260920)
owns sizing, first failures and subsequent targeted test results. Historical live and
full-suite records above retain their original configuration and outcome.

### Connection tolerance change

London connection establishment exhausted2 seconds before SQL/embedding. Approved change:
connect10 seconds only; SQL60, RAG360, explicit outer600 unchanged. Mocked adapter checks
verify the effective timeout, not actual connectivity improvement. No SQL/storage/vector
change or live retry was performed. Longer connection waiting does not solve exact-search
I/O variability. See the shared event for the original capture and precise limitation.
