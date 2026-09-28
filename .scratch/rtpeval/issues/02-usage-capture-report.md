# 02: Symmetric usage capture and resource report

Blocked by: None. Specification closure and separate implementation approval are still required.

Status: needs-info
Type: task

**What to build:** An independently invoked planner attempt can produce linked usage observations and a resource report with comparable outer timing across V0-V3.

**Readiness gate:** Map actual token/provider-send hooks, stage boundaries and final resource capture at the implementation checkpoint. This is upstream instrumentation, not planner execution owned by Evaluation.

**Acceptance criteria:**

- [ ] Use common monotonic outer timing through final result and cleanup; retain stage scope and overlapping timing semantics.
- [ ] Capture actual model usage, provider sends, cache hits, retry events and missingness with event IDs; distinguish measured, reported, derived and estimated observations.
- [ ] Link usage to selected run and result hash; absent collection may be declared unavailable, never zero.
- [ ] Repair totals are subsets of underlying events; oracle usage has a separate ledger.
- [ ] Verify mocked success, retries, failure, cache hit, missing tokens and cleanup; instrumentation must not change planning decisions or require a real run.


- [ ] Provide researcher-facing per-request resource values, differences and ratios where defined, with compatible measurement scope and explicit missingness. Zero/missing baselines must not create misleading ratios. Descriptive batch summaries retain request-level records; formal inference follows the separate analysis plan.
- [ ] Reports support later thesis/presentation discussion, not another non-blind human scoring round. Usage remains hidden from blinded raters and outside itinerary totals; no efficiency score or arbitrary PASS threshold is introduced.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
