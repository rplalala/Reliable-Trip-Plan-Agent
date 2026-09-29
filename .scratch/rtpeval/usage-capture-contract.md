# Ticket 02 usage capture and resource reporting contract

Date: 2026-09-29.
Status: Technical closure under the user's authorization to implement Ticket 02 and run offline acceptance. Not formal experiment authorization.
Base revision: 364f91f; working tree also contains the uncommitted Ticket 01 implementation/specification closeout.

## Checked seams and ownership

V0 returns no symmetric usage trace. Shared V1-V3 budget summaries contain useful counters but do not guarantee billing or physical sends. Primary Foundry calls return usage through LangChain callbacks; requirements also retain last_call_metadata, which is not safe as a concurrent global collector. Semantic/nomination/Repair calls already have per-call callbacks. Official search/reasoning use direct Responses SDK calls. Retrieval embedding uses its own SDK client and existing request hooks. These require complementary observation seams, not summation of historical trace totals.

A benchmark-owned caller invokes capture_attempt around its existing selected-version invocation and owned-client cleanup. Evaluation intake/scoring never calls that function to run planners. Dependency construction included inside invoke is timed; construction performed beforehand is explicitly outside this scope. The caller must use the same invocation boundary for all versions. Existing PlannerRuntime.run includes owned cleanup; direct runners with caller-owned clients require the cleanup callable. CLI scripts and production APIs do not automatically enable capture.

Capture is opt-in and request-local. It neither changes prompts, retries, timeouts, budgets nor adopts planner judgments. Existing observed stage decorators provide inclusive stage spans; unobserved stages remain unattributed. Structured generation includes V0/shared structured calls; requirements use their own nested stage. Repair/repair_round ancestry marks a subset with round IDs. Stage times are not summed into outer latency.

## Events and meanings

- Model events: unique LangChain run IDs for chat callbacks; unique SDK invocation IDs for official reasoning/search and embedding. Provider-returned input/output/total tokens are preserved; total may be derived only from both known components. Missing usage is null, including failures. Embedding prompt/total usage is retained without inventing output tokens.
- Provider events: one event per actual HTTP transport entry on instrumented clients, including repeated sends. Counts do not prove successful delivery, paid requests, or billable matrix elements. Matrix requested elements are observed from request cardinality, never provider billing.
- Response hooks record HTTP status. An attempt with no response remains incomplete; outer failure/cancellation is recorded separately, without inventing a server status. Response latency measures time to response hook, not full parsing time.
- Cache events: get_or_create cache reuse is separate from lookup hits (which may merely inspect availability). Neither implies a saved API call; cache keys and request content are not persisted.
- Retry attempts are distinct transport events; no guessed retry cause or grouping is derived from identical URLs. Current default SDKs disable automatic retries. Internal provider web-search operations and model reasoning are not equated with application HTTP sends.

Only allowlisted numeric/identity/status metadata is retained. No prompts, user text, result contents, URLs, credentials, request bodies, response bodies or exception messages are stored in usage. Model/config names are metadata; errors retain type only. Existing trace callbacks are not replayed or added to event totals.

## Envelope and missingness

Envelope schema is rtpeval_usage_1 with group_id, run_id, version, namespace, exact result_sha256, timing, model_calls, provider_events, cache_events, stage_summaries, repair_summary, coverage, missing_fields and diagnostics. A caller-supplied serializer must return the exact bytes later saved as result; capture stops its clock before serialization and sink work. Failed attempts have no adopted result hash. Failure envelopes are retained by benchmark construction, not made into qualified batches.

namespace separates planner and oracle ledgers. Nested capture is rejected to avoid double counting. Concurrent attempts use isolated contexts. Exceptions/cancellation and cleanup are preserved; a cleanup error does not replace an existing primary error. Sink failure is reported on the supplied ledger's diagnostics and does not turn a successful planner result into failure. The producer must check that a valid usage artifact was actually saved before handoff.

Default adapter coverage is unverified: custom injected clients may bypass all hooks. A producer using the checked, instrumented default adapter paths may explicitly declare default_adapters. This is a recorded collection configuration, not inferred from zero observed calls. Unverified capture reports observed subtotals and unavailable whole-run counts/tokens, never false zero. It does not establish capture coverage for arbitrary new adapters.

## Researcher report

Each selected group/version retains elapsed scope/outcome, complete comparable totals where supported, observed token subtotal, missing-token call count, observed HTTP sends, cache reuse versus lookup counts and Repair event subsets. Resource reports are separate from quality scoring and human blind tasks. Duplicate selected versions or event IDs are rejected rather than silently double-weighted.

Within-request comparisons give absolute difference and candidate/baseline ratio only for compatible namespace/outcome and, for latency, the same selected-invocation-through-cleanup boundary. Zero baselines have a difference but no ratio; missing observations remain unavailable. Descriptive medians include available counts and separate namespace/outcome/scope cohorts; the request rows remain available. There is no efficiency score, PASS threshold, inferential test, cost conversion or claim that lower usage is better quality.

## Verification boundary

Offline tests must exercise real LangChain callback propagation, HTTP mock transports, repeat sends, matrix elements, duplicate notifications, missing tokens, cache distinctions, cleanup timing, failure/cancellation, concurrent isolation, sink failure, and comparison missingness. Shared-client/runtime regressions must remain green. Real provider/model/DB runs and benchmark creation remain excluded. See ticket-02-acceptance.md for executed results once available.


## Report validation follow-up - 2026-09-30

For available/partial collection, model_calls, provider_events and cache_events must each be explicit arrays. Missing/null collections are rejected, not inferred empty. An unavailable envelope may omit them; present collections must still be arrays. Duplicate event IDs are rejected within each of the three collections. Repair observed token subtotal is null when no referenced Repair event has numeric token usage; an observed zero stays zero, and a partial known subtotal does not become a complete total. Producer instrumentation and planner decisions are unchanged.
