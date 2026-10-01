# Historical RTPEval Ticket 02 snapshot

Imported 2026-10-01. Live task state, labels, dependencies and discussion are owned by
[GitHub Issue #14](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/14).
The original local ticket is preserved verbatim below. Its Status, dates and comments
are historical and must not be maintained as a second live tracker.
Repository contracts and acceptance records retain their detailed authority.

<!-- RTPEVAL-HISTORICAL-SOURCE:RTPEVAL-02 -->

---

# 02: Symmetric usage capture and resource report

Blocked by: None. User authorized closure, implementation and offline acceptance on 2026-09-29.

Status: resolved
Type: task

**What to build:** An independently invoked planner attempt can produce linked usage observations and a resource report with comparable outer timing across V0-V3.

**Readiness gate:** Closed by [usage capture contract](../usage-capture-contract.md). Implemented as opt-in producer instrumentation, not evaluator-owned planner execution. See [acceptance](../ticket-02-acceptance.md).

**Acceptance criteria:**

- [x] Use common monotonic outer timing through final result and cleanup; retain stage scope and overlapping timing semantics.
- [x] Capture actual model usage, provider sends, cache hits, retry events and missingness with event IDs; distinguish measured, reported, derived and estimated observations.
- [x] Link usage to selected run and result hash; absent collection may be declared unavailable, never zero.
- [x] Repair totals are subsets of underlying events; oracle usage has a separate ledger.
- [x] Verify mocked success, retries, failure, cache hit, missing tokens and cleanup; instrumentation must not change planning decisions or require a real run.


- [x] Provide researcher-facing per-request resource values, differences and ratios where defined, with compatible measurement scope and explicit missingness. Zero/missing baselines must not create misleading ratios. Descriptive batch summaries retain request-level records; formal inference follows the separate analysis plan.
- [x] Reports support later thesis/presentation discussion, not another non-blind human scoring round. Usage remains hidden from blinded raters and outside itinerary totals; no efficiency score or arbitrary PASS threshold is introduced.

## Authorization and verification boundary

Original publication did not authorize implementation. The user subsequently approved this ticket through implementation and offline acceptance; it is now resolved. Specification readiness does not mean dependencies are complete or execution is permitted. Executed checks are recorded in the acceptance document; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.

2026-09-29: User authorized specification closure, implementation and offline acceptance without additional routine approvals. No live runs or Git actions are authorized.

## Answer

Implemented isolated per-attempt usage capture, token callbacks, SDK usage capture, scoped HTTP hooks, separate cache observations and researcher comparisons. Initial broad regression found four hook-cleanup failures; fixed with capture-scoped registration and concurrent-client ownership. Final broad regression: 944 passed, 1 skipped; latest usage/evaluation subset: 51 passed, 1 skipped. No live services, benchmark execution or Git actions.


2026-09-30: Follow-up review findings corrected under explicit user approval. Related regression suite: 113 passed / one existing Windows symlink privilege skip; Ruff checks pass. See the acceptance follow-up for failure-before/fix-after evidence and updated input boundaries. Status remains resolved for the offline scope only.
