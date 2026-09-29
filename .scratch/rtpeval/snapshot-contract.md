# Ticket 04 snapshot implementation contract

Date: 2026-09-30. Status: Implemented offline; final validation is recorded in ticket-04-acceptance.md.
Base: 1eb441f on feature/evaluation. No live acquisition or benchmark freeze.

## Public seams

`build_identity_plan(intake, paired=False)` selects all final primary visits and relevant requirement subjects, plus available V3 optional projections when paired is requested. It creates independent name-search requests (page size 20, original destination/location retained) and supplied-ID details requests. Search is collected for supplied IDs too; rank never establishes identity. Missing names/malformed IDs remain explicit blocked reference entries. Original occurrences are never deduplicated, only identical request descriptors.

`build_evidence_plan(intake, identity_report, route_contexts, paired=False)` validates report/source linkage and deduplicates details requests for resolved canonical identities. Unresolved references remain explicit. Every candidate leg is inventoried; missing route contexts remain pending rather than disappearing. Explicit contexts identify actual source reference endpoints and include mode, aware departure or explicit time-independent basis, routing options, and independently prepared endpoint coordinates with evidence hashes. Endpoint canonical IDs must match the adopted identities. This records supplied independent context; it does not certify the factual truth of externally prepared coordinates. Ticket 07 owns context selection and applicability; Ticket 04 never optimizes or shifts dates.

Requests have canonical-JSON SHA-256 keys over operation and complete parameters. Route keys preserve direction, identities, coordinates/provenance, mode, departure context and routing options. Only necessary one-origin/one-destination matrix requests are emitted; there is no Cartesian union matrix. Requested matrix elements count each actual send, including retries.

## Acquisition and persistence

`acquire_snapshot(plan, directory, transport, policy)` requires a fresh directory and an explicitly supplied async transport. It provides operation/parameters, not credentials or URLs; no built-in network client or live CLI is enabled. The transport returns status_code and exact response bytes. A transport failure is represented by a typed safe code; exception messages and credential headers are not persisted.

Policy requires an explicit positive max_sends, max_attempts (default 2), timeout_seconds (default 20), retry_delay_seconds (default 1). Sequential acquisition uses deterministic sorted request keys. Only transport failures/timeouts, HTTP 429 and HTTP 5xx are retried within both bounds. All attempts, errors, UTC request/retrieval times and raw response hashes are preserved. Malformed JSON and missing matrix elements are not silently retried or converted to no-route. Budget exhaustion records every remaining request as unavailable. Retry success does not erase earlier attempts.

The snapshot is an evaluation-owned immutable collection interval, not a simultaneous observation. Deduplication is per plan/snapshot; reruns require a new directory and snapshot. A versioned manifest is published last using exclusive creation. Interrupted directories without a manifest are not replayable. There is no planner cache access, cross-snapshot stale reuse, retention promise, or automatic resume.

`load_snapshot(directory, expected_plan=None)` validates schema, keys, raw response hashes, safe relative paths and required request coverage; it replays without transport access. It returns raw observations plus normalized summaries with original values intact. Failure/partial records remain in coverage; corrupt artifacts fail replay rather than shrinking it. Replay is deterministic and uses stored timestamps. Provider response bytes remain separate from derived JSON summaries.

## Ticket 03 bridge and response interpretation

`identity_evidence(snapshot)` creates the existing identity envelope with source-linked per-reference records, requested IDs/query/page size and actual raw search count. Malformed search candidates remain represented so Ticket 03 can block acceptance. Raw response files and hashes remain auditable via observation references. Details retain timezone/current/regular hours and coordinates in snapshot raw data for later tickets; no opening verdict is computed.

Matrix summaries require a unique expected (0,0) element and preserve raw duration strings, status, condition and fallback. Missing/duplicate/unexpected indices are explicit incomplete evidence, not no-route or a substitute estimate. This slice does not compute Routes/opening/requirement verdicts or parse durations into rounded planner DTOs.

Oracle acquisition has a separate snapshot ledger (namespace=oracle), actual transport invocations, retries, requested matrix elements and within-snapshot request deduplication. It is not added to planner usage and makes no billing/delivery claim. Exact planner-to-oracle lag is unavailable without independently supplied planner timestamps; absence is explicit rather than invented.

## Validation and limits

Offline tests use temporary synthetic batches, fake transport and network guards. Cover two-stage handoff, optional projections, retained occurrences, directed contexts, partial failures, missing matrix elements, bounded retries/budget, corruption/path escape, immutable output and deterministic replay. Operational provider request serialization, current API applicability/retention settings and real live budgets require a separate authorized integration; the injectable acquisition interface must not be presented as a ready-to-run Google client.


## Concrete route context wire

`route_contexts` is an array; CLI input wraps it in `{"contexts": [...]}`. Each entry has `leg_id` from the evidence plan's leg inventory, `source_kind=independent_evaluation_context`, `mode` (WALK/TRANSIT/DRIVE), `departure`, `time_basis` (explicit_departure/time_independent), `origin`, `destination`, and `routing_options`. An explicit departure is offset-aware and preserved verbatim. Time-independent queries require null departure. Both endpoints contain exactly `place_id`, finite latitude/longitude, and a 64-character lowercase `evidence_sha256`. Options are restricted to routing_preference, avoid_tolls, avoid_highways, avoid_ferries, language_code and region_code. The transport integration owns provider support validation; an unsupported context returns a recorded failure, never a silently altered date/mode. Required context metadata and allowed parameter fields are validated before dispatch.

Replay validates UTC collection/attempt timestamps and their ordering as well as raw hashes, summaries, request coverage and derived ledger totals. A corrupt timestamp cannot reach the identity bridge as apparently valid evidence. Supplied identity reports must match intake source hashes and all original identity source records. These hashes provide integrity/linkage against the supplied plan and raw files, not cryptographic proof of an external acquisition. The caller must retain a trusted plan/manifest artifact hash when stronger external provenance verification is required.
