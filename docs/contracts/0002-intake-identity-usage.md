# Intake, identity, snapshots and usage

Current implemented contract for Tickets 01-04, including the 2026-10-03 ordinary-output
revision. Source records are immutable; offline replay and independent review are separate
from live acquisition. [Evaluation architecture](../0006-independent-evaluation.md) owns
implemented/deferred scope. This file owns preparation wire and provenance; scorer rules
live in the related topic contracts.

<a id="rtpeval-intake-projection-contract"></a>
<a id="rtpeval-intake-projection-contract--batch-intake-and-independent-projection-contract"></a>
<a id="rtpeval-intake-projection-contract--scope-and-inspected-facts"></a>
<a id="rtpeval-intake-projection-contract--intake-result-and-parsing-boundary"></a>
<a id="rtpeval-intake-projection-contract--stable-source-identity-and-reader-separation"></a>
<a id="rtpeval-intake-projection-contract--time-occupancy-and-display-consequences"></a>
<a id="rtpeval-intake-projection-contract--reason-categories-and-future-acceptance-examples"></a>
<a id="rtpeval-intake-projection-contract--closure-and-remaining-ownership"></a>
<a id="rtpeval-intake-projection-contract--implemented-preparation-interface--2026-09-29"></a>
<a id="rtpeval-intake-projection-contract--follow-up-correction-boundary---2026-09-30"></a>
<a id="batch-intake-and-independent-projection-contract"></a>
<a id="intake-result-and-parsing-boundary"></a>
<a id="stable-source-identity-and-reader-separation"></a>

<a id="intake"></a>

## Intake and stable projection

Accept one explicitly selected batch. Emit material_diagnostics, inventory, projection_diagnostics and track_availability. A material error returns needs_material_correction for the submitted batch; do not silently evaluate a smaller cohort. Projection uncertainty does not revoke benchmark qualification. No producer runner, validator, requirement interpreter or workflow-completion check is invoked.

Fatal material errors: unreadable/ambiguous JSON (including duplicate object keys), missing mandatory input/result/RequirementSpec or required usage envelope, incorrect hashes or group/run/version linkage, unsupported artifact major version, path escaping the resolved batch root (including links/junctions), non-object itinerary, absent/non-array days or activities, non-object activity, missing/non-string required activity identifier/title, nonunique activity IDs or nonunique/unreadable declared day dates. These prevent stable interpretation; do not reconstruct them. A confirmed multi-POI visit block is an existing delivery-contract diagnostic, not a request to split it.

A declared unavailable usage envelope is valid and disables only resource measurements. Missing optional V3 draft/final-primary projections disable paired analysis; never reconstruct them from the selected final. A malformed optional projection records its own unavailable reason without replacing the selected final.

Use a versioned evaluation wire reader rather than running every product validator. itinerary_1 (including historically absent output_version) and itinerary_2 are explicitly recognized; original absence remains recorded. Missing historically optional roles become unknown in the derived view; missing optional transfer/reference arrays become empty with an absent-field marker. Preserve additional result fields without exposing them to quality readers. Unknown major versions require adapter support, not guessing.

Representable content issues remain diagnostic observations: date gaps, empty activities, unsorted records, overlap, output-versus-request date/destination discrepancy, unknown roles, invalid/missing time values, uncertain timezone, unknown place association and bad Transfer links. Do not silently repair, reject for low quality or use current live-request date limits. Retain source records even when dependent metrics cannot judge them. Original request hashes and producer-attested linkage establish which Input was run; a content discrepancy alone does not prove a wrong-file submission.

A source reference is (batch_id, group_id, run_id, artifact_sha256, JSON pointer). Derived record IDs use this tuple and projection-contract version, not canonical place ID. Preserve original array positions, declared day, original activity ID and raw values. Sorting makes a separate view; it never changes source pointers. Same activity IDs in draft/final or two runs do not imply correspondence.

Quality view exposes itinerary fields, reviewed requirements and later independent records only. Planner requirements, supply, RAG origins, validation findings, cost projections, route diagnostics and Repair records remain outside it. Preserve Transfer mode, endpoint/time/duration claims as claims; validation_state, unknowns, evidence_refs, mode_source and calculation_basis cannot decide quality. Mechanism readers access their own data channel. Human rendering must strip private source/version/provider identifiers while retaining meaningful itinerary text and uncertainty.

<a id="rtpeval-ticket-01-03-simplification"></a>
<a id="rtpeval-intake-projection-contract--independent-activity-classification"></a>
<a id="rtpeval-intake-projection-contract--order-and-candidate-transitions"></a>
<a id="rtpeval-intake-projection-contract--transport-correspondence-association-is-not-factual-agreement"></a>
<a id="rtpeval-intake-projection-contract--superseding-transport-source-decision---2026-09-30"></a>
<a id="rtpeval-intake-projection-contract--transport-responsibility-correction---2026-09-30"></a>
<a id="rtpeval-ticket-01-03-simplification--tickets-0103-structural-claims-and-ordinary-output-compatibility"></a>
<a id="rtpeval-ticket-01-03-simplification--authority-and-scope"></a>
<a id="rtpeval-ticket-01-03-simplification--observed-facts-and-limits"></a>
<a id="rtpeval-ticket-01-03-simplification--1-v0-occurrence-association"></a>
<a id="rtpeval-ticket-01-03-simplification--2-structural-role-and-place-claims"></a>
<a id="rtpeval-ticket-01-03-simplification--4-accepted-cost-boundary"></a>
<a id="rtpeval-ticket-01-03-simplification--5-acceptance-examples-for-later-implementation"></a>
<a id="rtpeval-ticket-01-03-simplification--documentation-validation"></a>
<a id="rtpeval-ticket-01-03-simplification--subsequent-implementation-approval-and-checkpoint"></a>
<a id="independent-activity-classification"></a>
<a id="order-and-candidate-transitions"></a>
<a id="transport-correspondence-association-is-not-factual-agreement"></a>
<a id="superseding-transport-source-decision---2026-09-30"></a>
<a id="transport-responsibility-correction---2026-09-30"></a>
<a id="tickets-0103-structural-claims-and-ordinary-output-compatibility"></a>
<a id="2-structural-role-and-place-claims"></a>

<a id="claims"></a>

## Structural claims and directed occurrence association

Emit `evaluation_role=primary_visit|transport|transition|unresolved`, role status, source
references, reasons and independent review linkage. An explicit `main_poi` with usable
`place_name` supplies the structural visit/place claim; an ordinary descriptive title does
not need to equal that name. Without usable place fields, retain the supported name-only/
review path rather than manufacturing a venue. Explicit competing structural/content claims
retain `competing_claim`, its field/text/source and parsed destination/origin as applicable.

Title regexes do not veto declared visit or transport roles. A structured `main_poi`
remains a primary visit even without a place field or with a placeholder-like title;
this does not establish its factual venue identity. A declared `free_time` is non-POI,
including `Coffee break` or a named lounge, regardless of title wording. Independent
occupancy/protection review still decides whether it is a time commitment. A locationless
declared transport remains transport even with a `Visit`/`Tour` title. Independently
reviewed roles retain precedence. Unknown roles without usable place claims remain
unresolved; daily counts still retain genuine role and date-attribution uncertainty.

Bounded title parsing may retain source-linked `competing_claim` metadata and feed the
separate identity review. It cannot establish semantic role contradictions or factual
identity. Transport endpoint parsing still applies to authoritative transport records;
this revision adds no general semantic model or new LLM invocation.

Generic locationless activities are transition-like; named unresolved POIs stay visits.
Nearby is unscheduled. Unknown/inconsistent roles retain review and applicability counts.
Neither candidate membership nor costs establish independent role/identity.

Preserve delivered day membership. For a day with comparable valid timestamps, order visit candidates by start, then end, then original pointer for display stability. Equal/overlapping times remain conflicts/ambiguities, not corrected chronology. Invalid or incomparable clocks cannot establish adjacency by arbitrary lexical sorting; emit an adjacency-unresolved record with involved sources.

Candidate legs connect consecutive primary visits within a day. Nearby, transition placeholders and transport records do not become POI endpoints. Protected intervals remain separate blockers. Possible intervening unresolved-role records prevent declaring a clean complete adjacency list for that span; preserve the candidate and uncertainty instead of skipping them. Canonical same-place N/A is decided later using independent identity, not equality of claimed IDs.

V0 transport supports complete `from NAME to NAME` clauses, optionally prefixed by `walk`,
`walking`, `drive`, `driving`, `transit`, `public transit`, `transfer` or `travel`.
Only complete supported title/notes declarations supply endpoint pairs. All recognized
pairs must agree; unrelated prose and generic estimate notes neither supply a pair nor
block association. A bare supported mode title (or `Transport`/`Transfer`) without any
recognized endpoint declaration can associate through exactly one containing gap.
An unsupported non-bare title remains unbound without independent endpoint review.
Match complete NFC/casefold/whitespace-normalized scheduled labels,
resolved chronology and exactly one same-day occurrence gap containing the whole transport
interval. Repeated labels are acceptable if only one occurrence pair survives. Contradictory,
reversed, unsupported, overlapping or ambiguous claims retain review; no nearest/favorable
pair or positional override is chosen. Independent reviewed endpoints can associate despite
a separate time conflict; the review does not clear that conflict.

V0 mode comes from independent mode review or a bounded explicit title declaration.
Supported bare labels include walk/walking/on foot, public transit/public transport,
bus/train/metro/subway/tram, and drive/driving/by car. Recognized directed movement
clauses may supply the leading mode label. The first semicolon-separated title clause
must declare a supported mode; later recognized mode declarations must agree. Missing,
unsupported or conflicting mode declarations remain UNKNOWN. Notes are not mode fields;
incidental conditional/transport keywords and narrative negations are not interpreted.
Original prose is preserved for independent review rather than treated as semantic proof.

V1-V3 associate Transfers through directed consecutive same-day activity IDs. Wrong/dangling/
nonadjacent/cross-day IDs remain unbound; place-ID disagreement stays a separate claim.
Authority is V0 Activity and V1-V3 Transfer. `transport_source`, `transport_applicable`,
`ignored_transport` and diagnostics preserve ignored representations without occupancy or
fallback. Missing transfers remain missing. Same-source duplicate claims share source sets,
segments remain segments, and conflicts stay alternatives rather than summed or shortened.
Association status and agreement are separate. No claimed arrival is synthesized from duration.
Display-only inferred arrival follows [human review](0005-quality-human-review.md#human).

`policy_version=structural_claims_directed_occurrences_4`; immutable source-reference
`projection_version=rtpeval_projection_1`. Internal-finding-only source changes can preserve
semantic projections while still changing exact artifact hashes and source identities.
Replay derived identity/evidence/report preparations when classification changes; preserve
original source artifacts and historical reports. The density table remains
`rtpeval_daily_density_2`.

<a id="rtpeval-identity-contract"></a>
<a id="rtpeval-identity-implementation-contract"></a>
<a id="rtpeval-identity-contract--independent-identity-resolution-contract--draft"></a>
<a id="rtpeval-identity-contract--purpose-and-boundary"></a>
<a id="rtpeval-identity-contract--code-facts"></a>
<a id="rtpeval-identity-contract--inputs-and-preserved-records"></a>
<a id="rtpeval-identity-contract--common-resolution-process"></a>
<a id="rtpeval-identity-contract--downstream-behavior"></a>
<a id="rtpeval-identity-contract--accepted-idname-conflict-handling"></a>
<a id="rtpeval-identity-contract--simple-examples"></a>
<a id="rtpeval-identity-contract--future-verification"></a>
<a id="rtpeval-identity-contract--ticket-03-specialization--2026-09-29"></a>
<a id="rtpeval-identity-implementation-contract--ticket-03-offline-identity-implementation-contract"></a>
<a id="rtpeval-identity-implementation-contract--scope-and-source-boundary"></a>
<a id="rtpeval-identity-implementation-contract--offline-wire-inputs"></a>
<a id="rtpeval-identity-implementation-contract--strict-automatic-acceptance"></a>
<a id="rtpeval-identity-implementation-contract--review-outcome-and-reporting"></a>
<a id="rtpeval-identity-implementation-contract--verification-and-limits"></a>
<a id="rtpeval-identity-implementation-contract--ticket-05-subject-scope-extension--specification-only-2026-10-01"></a>
<a id="rtpeval-ticket-01-03-simplification--3-independent-structured-address-evidence"></a>
<a id="accepted-idname-conflict-handling"></a>
<a id="offline-wire-inputs"></a>
<a id="strict-automatic-acceptance"></a>
<a id="3-independent-structured-address-evidence"></a>

<a id="identity"></a>

## Independent identity and adjudication

Ticket 03 reads accepted projection references, reviewed REQUIRED/EXCLUDED/fixed-time
subjects, independent observations, a predeclared audit and optional decisions. It uses
neither planner evidence nor provider rank as confidence. Each established primary visit is
a grounding unit even without an ID; unresolved roles retain a separate population count.
Requirement subjects and high-impact possible obligation matches require independent review.
A visit is high-impact when its normalized name matches a subject or independent candidate/
claimed IDs can overlap. If a same-group subject has no usable independent candidates, all
primary visits in that group need review rather than assuming they cannot match.
Nearby/transport are outside main grounding. Resolution and claimed-ID consistency differ:
a reviewed intended venue A can resolve while its incorrect supplied ID B remains conflicting.
Unresolved identity is not proof of fabrication, and resolved identity is not opening/route PASS.

`rtpeval_identity_evidence_1` has `batch_id`, `batch_revision` and `records`. A record is keyed by Ticket 01 `reference_id`, has a unique `observation_id`, declares `source_kind=independent_google_places`, and may carry `details` and/or `search`. Missing records mean unavailable evidence. An available details observation retains `requested_place_id`, `retrieved_at` and `place`; search retains `query`, `requested_page_size`, `actual_result_count`, `retrieved_at` and raw-order `candidates`. Candidates carry Google ID, display name and formatted address; rank, business status and additional provider fields may be retained but rank never acts as confidence. Failed/unavailable/malformed observations retain their status. Invalid envelope linkage, duplicate references or impossible count structure are rejected rather than producing a partial report. A declared independent source is provenance metadata, not proof that an external service was contacted.

`rtpeval_identity_audit_1` has the same batch/revision plus a nonempty seed and positive `sample_count`. The plan is a required, separately frozen input. Among strict automatic proposals, choose the lowest hash of seed, batch/revision and a semantic audit key, then select up to the declared count. The key includes group/version/projection/source pointer and visible place claim, but excludes the result file hash and V3 internal findings. Selected proposals require review before entering resolved grounding counts. An absent plan or zero sample count is rejected. The module verifies deterministic replay and records plan hashes; benchmark preparation must establish that the plan was fixed before result inspection.

`rtpeval_identity_reviews_1` has batch/revision and per-reference decisions. Each decision supplies the current observation hash, consecutive positive revision, reviewer reference, review time, rationale, and `confirm`, `reject` or `unresolved`. A confirmation names an ID present in independent observation candidates. Stale evidence, duplicate/missing review revisions and unsupported candidate IDs are rejected. The report retains the entire history and uses the latest decision. A rejection leaves identity unresolved; it does not automatically prove a fictional place. A new artifact source reference or evidence observation needs new reviewed linkage.

### Automatic association and typed addresses

Structured place claims and independent evidence determine association. Title-derived
`competing_claim` metadata is diagnostic and cannot veto automatic proposals, including
`Visit Museum A in the morning` or `Museum A and its gardens`. Required review/audit
gates and independently evidenced name/ID/address/destination conflicts still apply.

Names use NFC, casefold and whitespace normalization only. Aliases, translations, competing
branches and approximate names remain review cases. Supplied-ID details must return the
requested ID and corroborate the structural name/destination/location; lookup success alone
is insufficient. Without the supported independently matching numbered-street shortcut,
full-page independent name search must show the same sole raw/usable candidate. A supplied
search remains contradiction evidence even when the shortcut applies. Name-only search
uses the submitted name, page size 20 and exactly one raw/usable candidate. The bounded
observation does not prove global uniqueness. Generic country/admin/postcode agreement
cannot activate the shortcut. The legacy numbered English street recognizer accepts only
`street/st`, `road/rd`, `avenue/ave`, `lane/ln`, `drive/dr`, `boulevard/blvd`,
`way` and `court/ct` (optional terminal period). Other forms need typed support or review.

Independent candidates retain original formatted address and optional typed
`address_components` (`longText`, optional `shortText`, `types`). The snapshot bridge copies
raw `addressComponents`, never synthesizing it. Typed locality supports city association;
explicit destination qualifiers must agree. Country/state/postcode/street occurrences of
the same word do not substitute for locality. Street-number/route components support street
locations and provider short forms; generic locality agreement is not a numbered-street match.

For equal ID/compatible name, differing formatted strings can agree through complete typed
street-number/route/locality/country evidence; optional admin/postal components must agree on
both sides. Missing/conflicting components do not prove equivalence. With components absent,
exact legacy comma/semicolon address-component matching remains available. With typed locality
available, unsupported location tokens cannot borrow favorable formatted prose. Malformed
components remain diagnostic. No substring city test, geocoding, alias inference, extra request,
LLM call or old-snapshot backfill is added. Planner field masks/budgets are unchanged.

`association_policy_version=structural_claims_typed_addresses_3` is required downstream.
`subject_scope_version=required_excluded_fixed_time_1` and `reference_set_digest` bind the
recomputed reference population. Old derived reports require offline replay and new affected
plans; fixed-time subjects may change high-impact review even with unchanged source hashes.
Missing observation remains UNKNOWN; missing/stale preparation linkage requires replay.

Reports retain independent decision path, candidate/observation/rule/audit hashes, latest
review and complete history, resolved/unresolved states and consistent/conflicting/unverifiable/
absent claimed-ID association. High-impact/audit queues hide source versions. Reviewed rejection
is unresolved, not automatically fictional; an empty queue does not imply every venue grounded.

<a id="rtpeval-snapshot-contract"></a>
<a id="rtpeval-snapshot-contract--ticket-04-snapshot-implementation-contract"></a>
<a id="rtpeval-snapshot-contract--public-seams"></a>
<a id="rtpeval-snapshot-contract--acquisition-and-persistence"></a>
<a id="rtpeval-snapshot-contract--ticket-03-bridge-and-response-interpretation"></a>
<a id="rtpeval-snapshot-contract--validation-and-limits"></a>
<a id="rtpeval-snapshot-contract--concrete-route-context-wire"></a>
<a id="acquisition-and-persistence"></a>
<a id="ticket-03-bridge-and-response-interpretation"></a>
<a id="concrete-route-context-wire"></a>

<a id="snapshots"></a>

## Request planning, injected acquisition and immutable replay

`build_identity_plan(intake, paired=False)` selects all final primary visits and relevant requirement subjects, plus available V3 optional projections when paired is requested. It creates independent name-search requests (page size 20, original destination/location retained) and supplied-ID details requests. Search is collected for supplied IDs too; rank never establishes identity. Missing names/malformed IDs remain explicit blocked reference entries. Original occurrences are never deduplicated, only identical request descriptors.

`build_evidence_plan(intake, identity_report, route_contexts, paired=False)` validates report/source linkage and deduplicates details requests for resolved canonical identities. Unresolved references remain explicit. Every candidate leg is inventoried; missing route contexts remain pending rather than disappearing. Explicit contexts identify actual source reference endpoints and include mode, aware departure or explicit time-independent basis, routing options, and independently prepared endpoint coordinates with evidence hashes. Endpoint canonical IDs must match the adopted identities. This records supplied independent context; it does not certify the factual truth of externally prepared coordinates. Ticket 07 owns context selection and applicability; Ticket 04 never optimizes or shifts dates.

Requests have canonical-JSON SHA-256 keys over operation and complete parameters. Route keys preserve direction, identities, coordinates/provenance, mode, departure context and routing options. Only necessary one-origin/one-destination matrix requests are emitted; there is no Cartesian union matrix. Requested matrix elements count each actual send, including retries.

`acquire_snapshot(plan, directory, transport, policy)` requires a fresh directory and an explicitly supplied async transport. It provides operation/parameters, not credentials or URLs; no built-in network client or live CLI is enabled. The transport returns status_code and exact response bytes. A transport failure is represented by a typed safe code; exception messages and credential headers are not persisted.

Policy requires an explicit positive max_sends, max_attempts (default 2), timeout_seconds (default 20), retry_delay_seconds (default 1). Sequential acquisition uses deterministic sorted request keys. Only transport failures/timeouts, HTTP 429 and HTTP 5xx are retried within both bounds. All attempts, errors, UTC request/retrieval times and raw response hashes are preserved. Malformed JSON and missing matrix elements are not silently retried or converted to no-route. Budget exhaustion records every remaining request as unavailable. Retry success does not erase earlier attempts.

The snapshot is an evaluation-owned immutable collection interval, not a simultaneous observation. Deduplication is per plan/snapshot; reruns require a new directory and snapshot. A versioned manifest is published last using exclusive creation. Interrupted directories without a manifest are not replayable. There is no planner cache access, cross-snapshot stale reuse, retention promise, or automatic resume.

`load_snapshot(directory, expected_plan=None)` validates schema, keys, raw response hashes, safe relative paths and required request coverage; it replays without transport access. It returns raw observations plus normalized summaries with original values intact. Failure/partial records remain in coverage; corrupt artifacts fail replay rather than shrinking it. Replay is deterministic and uses stored timestamps. Provider response bytes remain separate from derived JSON summaries.

`identity_evidence(snapshot)` creates the existing identity envelope with source-linked per-reference records, requested IDs/query/page size and actual raw search count. Malformed search candidates remain represented so Ticket 03 can block acceptance. Raw response files and hashes remain auditable via observation references. Details retain timezone/current/regular hours and coordinates in snapshot raw data for later tickets; no opening verdict is computed.

The accepted [snapshot-coordinate bridge](0004-opening-routes.md#accepted-snapshot-coordinate-extension-2026-10-03)
reads linked raw identity-snapshot coordinates after canonical identity adoption. The identity
wire remains unchanged; coordinate extraction preserves separate provenance and uncertainty.
This removes duplicate preparation when existing evidence suffices, without live acquisition.

Matrix summaries require a unique expected (0,0) element and preserve raw duration strings, status, condition and fallback. Missing/duplicate/unexpected indices are explicit incomplete evidence, not no-route or a substitute estimate. This slice does not compute Routes/opening/requirement verdicts or parse durations into rounded planner DTOs.

Oracle acquisition has a separate snapshot ledger (namespace=oracle), actual transport invocations, retries, requested matrix elements and within-snapshot request deduplication. It is not added to planner usage and makes no billing/delivery claim. Exact planner-to-oracle lag is unavailable without independently supplied planner timestamps; absence is explicit rather than invented.

`route_contexts` is an array; CLI input wraps it in `{"contexts": [...]}`. Each entry has `leg_id` from the evidence plan's leg inventory, `source_kind=independent_evaluation_context`, `mode` (WALK/TRANSIT/DRIVE), `departure`, `time_basis` (explicit_departure/time_independent), `origin`, `destination`, and `routing_options`. An explicit departure is offset-aware and preserved verbatim. Time-independent queries require null departure. Both endpoints contain exactly `place_id`, finite latitude/longitude, and a 64-character lowercase `evidence_sha256`. Options are restricted to routing_preference, avoid_tolls, avoid_highways, avoid_ferries, language_code and region_code. The transport integration owns provider support validation; an unsupported context returns a recorded failure, never a silently altered date/mode. Required context metadata and allowed parameter fields are validated before dispatch.

Replay validates UTC collection/attempt timestamps and their ordering as well as raw hashes, summaries, request coverage and derived ledger totals. A corrupt timestamp cannot reach the identity bridge as apparently valid evidence. Supplied identity reports must match intake source hashes and all original identity source records. These hashes provide integrity/linkage against the supplied plan and raw files, not cryptographic proof of an external acquisition. The caller must retain a trusted plan/manifest artifact hash when stronger external provenance verification is required.

The identity bridge additionally retains raw typed address components under the current
association policy. It does not normalize them into manufactured evidence. Query/response
applicability belongs to [opening/routes](0004-opening-routes.md). A built-in operational Google
client, credential handling, storage/retention policy and live allowance are not provided.

<a id="rtpeval-usage-capture-contract"></a>
<a id="rtpeval-usage-capture-contract--ticket-02-usage-capture-and-resource-reporting-contract"></a>
<a id="rtpeval-usage-capture-contract--checked-seams-and-ownership"></a>
<a id="rtpeval-usage-capture-contract--events-and-meanings"></a>
<a id="rtpeval-usage-capture-contract--envelope-and-missingness"></a>
<a id="rtpeval-usage-capture-contract--researcher-report"></a>
<a id="rtpeval-usage-capture-contract--verification-boundary"></a>
<a id="rtpeval-usage-capture-contract--report-validation-follow-up---2026-09-30"></a>
<a id="intake-identity-usage"></a>
<a id="ticket-02-usage-capture-and-resource-reporting-contract"></a>
<a id="events-and-meanings"></a>
<a id="envelope-and-missingness"></a>
<a id="researcher-report"></a>

<a id="usage"></a>

## Opt-in usage capture and resource reporting

V0 returns no symmetric usage trace. Shared V1-V3 budget summaries contain useful counters but do not guarantee billing or physical sends. Primary Foundry calls return usage through LangChain callbacks; requirements also retain last_call_metadata, which is not safe as a concurrent global collector. Semantic/nomination/Repair calls already have per-call callbacks. Official search/reasoning use direct Responses SDK calls. Retrieval embedding uses its own SDK client and existing request hooks. These require complementary observation seams, not summation of historical trace totals.

A benchmark-owned caller invokes capture_attempt around its existing selected-version invocation and owned-client cleanup. Evaluation intake/scoring never calls that function to run planners. Dependency construction included inside invoke is timed; construction performed beforehand is explicitly outside this scope. The caller must use the same invocation boundary for all versions. Existing PlannerRuntime.run includes owned cleanup; direct runners with caller-owned clients require the cleanup callable. CLI scripts and production APIs do not automatically enable capture.

Capture is opt-in and request-local. It neither changes prompts, retries, timeouts, budgets nor adopts planner judgments. Existing observed stage decorators provide inclusive stage spans; unobserved stages remain unattributed. Structured generation includes V0/shared structured calls; requirements use their own nested stage. Repair/repair_round ancestry marks a subset with round IDs. Stage times are not summed into outer latency.

- Model events: unique LangChain run IDs for chat callbacks; unique SDK invocation IDs for official reasoning/search and embedding. Provider-returned input/output/total tokens are preserved; total may be derived only from both known components. Missing usage is null, including failures. Embedding prompt/total usage is retained without inventing output tokens.
- Provider events: one event per actual HTTP transport entry on instrumented clients, including repeated sends. Counts do not prove successful delivery, paid requests, or billable matrix elements. Matrix requested elements are observed from request cardinality, never provider billing.
- Response hooks record HTTP status. An attempt with no response remains incomplete; outer failure/cancellation is recorded separately, without inventing a server status. Response latency measures time to response hook, not full parsing time.
- Cache events: get_or_create cache reuse is separate from lookup hits (which may merely inspect availability). Neither implies a saved API call; cache keys and request content are not persisted.
- Retry attempts are distinct transport events; no guessed retry cause or grouping is derived from identical URLs. Current default SDKs disable automatic retries. Internal provider web-search operations and model reasoning are not equated with application HTTP sends.

Only allowlisted numeric/identity/status metadata is retained. No prompts, user text, result contents, URLs, credentials, request bodies, response bodies or exception messages are stored in usage. Model/config names are metadata; errors retain type only. Existing trace callbacks are not replayed or added to event totals.

Envelope schema is rtpeval_usage_1 with group_id, run_id, version, namespace, exact result_sha256, timing, model_calls, provider_events, cache_events, stage_summaries, repair_summary, coverage, missing_fields and diagnostics. A caller-supplied serializer must return the exact bytes later saved as result; capture stops its clock before serialization and sink work. Failed attempts have no adopted result hash. Failure envelopes are retained by benchmark construction, not made into qualified batches.

namespace separates planner and oracle ledgers. Nested capture is rejected to avoid double counting. Concurrent attempts use isolated contexts. Exceptions/cancellation and cleanup are preserved; a cleanup error does not replace an existing primary error. Sink failure is reported on the supplied ledger's diagnostics and does not turn a successful planner result into failure. The producer must check that a valid usage artifact was actually saved before handoff.

Default adapter coverage is unverified: custom injected clients may bypass all hooks. A producer using the checked, instrumented default adapter paths may explicitly declare default_adapters. This is a recorded collection configuration, not inferred from zero observed calls. Unverified capture reports observed subtotals and unavailable whole-run counts/tokens, never false zero. It does not establish capture coverage for arbitrary new adapters.

Available/partial collection requires explicit `model_calls`, `provider_events` and
`cache_events` arrays; empty differs from absent/null. Unavailable envelopes can omit them,
but present collections must be arrays. Each collection rejects duplicate event IDs.
Repair token subtotal is null when no referenced event has observed token usage; measured
zero remains zero, and a partial subtotal does not become a complete total.

Each selected group/version retains elapsed scope/outcome, complete comparable totals where supported, observed token subtotal, missing-token call count, observed HTTP sends, cache reuse versus lookup counts and Repair event subsets. Resource reports are separate from quality scoring and human blind tasks. Duplicate selected versions or event IDs are rejected rather than silently double-weighted.

Within-request comparisons give absolute difference and candidate/baseline ratio only for compatible namespace/outcome and, for latency, the same selected-invocation-through-cleanup boundary. Zero baselines have a difference but no ratio; missing observations remain unavailable. Descriptive medians include available counts and separate namespace/outcome/scope cohorts; the request rows remain available. There is no efficiency score, PASS threshold, inferential test, cost conversion or claim that lower usage is better quality.

<a id="independent-identity-resolution-contract--draft"></a>
<a id="purpose-and-boundary"></a>
<a id="code-facts"></a>
<a id="inputs-and-preserved-records"></a>
<a id="common-resolution-process"></a>
<a id="downstream-behavior"></a>
<a id="simple-examples"></a>
<a id="future-verification"></a>
<a id="ticket-03-specialization--2026-09-29"></a>
<a id="ticket-03-offline-identity-implementation-contract"></a>
<a id="scope-and-source-boundary"></a>
<a id="review-outcome-and-reporting"></a>
<a id="verification-and-limits"></a>
<a id="ticket-05-subject-scope-extension--specification-only-2026-10-01"></a>
<a id="scope-and-inspected-facts"></a>
<a id="time-occupancy-and-display-consequences"></a>
<a id="reason-categories-and-future-acceptance-examples"></a>
<a id="closure-and-remaining-ownership"></a>
<a id="implemented-preparation-interface--2026-09-29"></a>
<a id="follow-up-correction-boundary---2026-09-30"></a>
<a id="ticket-04-snapshot-implementation-contract"></a>
<a id="public-seams"></a>
<a id="validation-and-limits"></a>
<a id="authority-and-scope"></a>
<a id="observed-facts-and-limits"></a>
<a id="1-v0-occurrence-association"></a>
<a id="4-accepted-cost-boundary"></a>
<a id="5-acceptance-examples-for-later-implementation"></a>
<a id="documentation-validation"></a>
<a id="subsequent-implementation-approval-and-checkpoint"></a>
<a id="checked-seams-and-ownership"></a>
<a id="verification-boundary"></a>
<a id="report-validation-follow-up---2026-09-30"></a>

<a id="history"></a>

## Code, commands and acceptance

Implementation owners: [intake](../../backend/evaluation/intake.py),
[projection](../../backend/evaluation/projection.py), [identity](../../backend/evaluation/identity.py),
[snapshot](../../backend/evaluation/snapshot.py) and [usage](../../backend/app/observability/usage.py).
[Package commands](../../backend/evaluation/README.md) describe invocation and exits.
[Intake/identity/usage records](../records/evaluation/intake-identity-usage.md) preserve executed
checks, earlier conservative rules, corrections and the ordinary-output acceptance.
Original plans remain in [parent #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12)
and Tickets [01](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/13),
[02](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/14),
[03](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/15),
[04](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/16).
Earlier title-equivalence/equal-transport-authority restrictions are not current rules.
