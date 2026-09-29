# Ticket 02 implementation and offline acceptance

Date: 2026-09-29.
Base revision: 364f91f05f01328266bfb00c5b75885242d93d7d.
Working-tree context: uncommitted Ticket 01 code/specification and Ticket 02 observation hooks, report, tests and documentation. No commit was created.
Status: Implemented and validated offline. Not benchmark frozen or formally evaluated.

## Scope and implementation

The user authorized closure through implementation/testing without repeated approvals, except unresolved consequential decisions. No such new scoring decision was needed. The [contract](usage-capture-contract.md) fixes the invocation/cleanup clock, provider-reported versus derived/missing usage, actual dispatch-attempt versus billing distinction, cache reuse versus lookup, Repair subsets and research-report semantics.

- [Capture guide](../../backend/app/observability/USAGE.md): benchmark-owned opt-in invocation with caller-owned sink and exact-byte serializer.
- [Neutral event ledger](../../backend/app/observability/usage.py): request-local model/provider/cache/stage observations; scoped HTTP hook installation/removal supports concurrent shared clients.
- [Attempt capture](../../backend/app/observability/usage_capture.py): LangChain callbacks, failure/cancellation/cleanup preservation, result linkage and explicit coverage declarations.
- [Resource report](../../backend/evaluation/usage_report.py): selected four-version groups, per-request differences/ratios and descriptive medians with availability counts. Single-attempt summaries remain usable by the upstream attempt ledger.

Shared adapters expose observation seams for Foundry structured/semantic/nomination/Repair, direct official search/reasoning, retrieval embedding, JSON/page HTTP, cache and existing stage wrappers. Prompts, models, budgets, retries and planning decisions were not changed. V3 final resource cleanup occurs inside the producer's selected invocation; the returned result is not rewritten. The quality scorer/reader does not run planners.

## Actual verification sequence

1. Initial capture suite: 10 tests passed. Targeted existing paths plus evaluation: 139 passed, one pre-existing Ticket 01 native symlink test skipped.
2. Initial broad relevant regression: 4 failed, 937 passed, 1 skipped. All four failures were existing requirement-harness assertions that client HTTP hooks must be empty after cleanup. No failing assertion established a changed itinerary result.
3. Corrected ownership: inactive capture installs no hooks; active capture attaches lazily and removes only its own callbacks. Shared clients retain hooks until all concurrent capture owners finish. Added concurrency/cleanup regression coverage rather than weakening existing tests.
4. Focused cleanup/requirement-harness retest: 37 passed. Further usage tests cover explicit retry after SDK failure and coexistence with existing usage callbacks. Final capture suite: 13 passed.
5. Repeated broad relevant regression: **944 passed, 1 skipped** across observability/runtime, Foundry, integrations, retrieval runtime, planner runtime, V0-V3 and evaluation. Duration about 103 seconds. During this run, a resource-report-only guard was tightened for four-version membership/unavailable envelopes; the latest targeted usage/evaluation rerun passed **51 tests, 1 skipped**, covering that final change.
6. Ruff passed on all changed Python paths; usage-report CLI help succeeded. Final whitespace and document-link checks are recorded at closeout. Test counts overlap and must not be added as independent evidence.

The skipped test is the Ticket 01 native Windows symlink creation check: host privileges do not allow creating it. Literal traversal and simulated resolved-link escape coverage pass. No real provider/model/database calls or formal benchmark executions were performed; mocks and synthetic local artifacts exercise actual callback and transport seams.

## Review findings and corrections

Local Standards/Spec review checked observation-only integration, callback noninterference, scoped cleanup, failure and cancellation propagation, distinct source/missingness labels, no prompt/URL/credential retention, and request-level comparisons. HTTP hooks are not physical-delivery or billing proof. Cleanup failure does not replace a primary failure/cancellation; usage sink failure leaves the planner result intact and appears on the supplied ledger diagnostics.

No-record does not imply zero: unverified adapters yield observed subtotals and unavailable complete counts. Failed model calls without returned usage prevent a complete token total. Zero baselines give no ratio. Namespace/outcome/timing mismatch blocks the applicable comparison. Comparison groups require four usage envelopes; availability inside envelopes can still be partial/unavailable. No efficiency score or quality-score contribution is introduced.

## Remaining limits and next boundary

- Capture must be explicitly enabled by benchmark producer invocation. Existing ordinary CLI runs do not automatically save usage. A producer must confirm artifact persistence and matching result bytes.
- default_adapters is a declared, checked integration configuration; arbitrary injected/new clients are not inferred covered. No live completeness claim was established here.
- Unobserved stages remain unattributed. Internal provider web-search actions and model reasoning are not reconstructed from HTTP counts. A request with no response retains incomplete outcome, not a guessed status.
- Stage latency is inclusive/non-additive. Cache lookups do not prove reused results or saved API requests. Observed route-matrix cardinality is not billable usage.
- Resource reporting is for researcher analysis and future thesis/presentation discussion, separate from blind human review and quality totals. No actual thesis analysis was performed.
- Ticket 03 identity closure remains a separate next task. No formal cases, shared checkpoint freeze, commit or push occurred.


## Authorized follow-up corrections - 2026-09-30

The user authorized the three report-boundary corrections identified in the follow-up review. Available/partial usage requires explicit event arrays; unavailable envelopes may omit them. Repair tokens with no observed values now stay null, while observed zero and partial known subtotals are preserved. Cache duplicate event IDs are rejected like model/provider duplicates. Capture hooks and planner paths were not changed.

TDD sequence: six missing/null array cases failed before correction, then passed along with unavailable-envelope compatibility. Repair subtotal tests initially had one failure and two passes, then all three passed. Duplicate-event tests initially had one cache failure and two existing model/provider passes, then all three passed. Final combined evaluation/capture suite: **113 passed, 1 skipped** (the existing native Windows symlink privilege case). Ruff check/format check pass. These counts overlap Ticket 01 validation and include Ticket 03; do not add them as independent evidence. No need to rerun unrelated planner suites because this correction pass only changed evaluator readers/reporting and fixtures. Final review disposition is in ticket-01-02-review.md. No live service, formal benchmark/experiment, commit/push or freeze.
