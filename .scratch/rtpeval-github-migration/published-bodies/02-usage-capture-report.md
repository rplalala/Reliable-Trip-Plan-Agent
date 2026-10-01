<!-- RTPEVAL-MIGRATION:RTPEVAL-02 draft-sha256:ebf7b91ffd854a9137da43473a44ad1f54b6429d109bccd5cf6fb0ca63567dbe -->

## Current status at migration preparation

- Project ticket: RTPEval 02. Published GitHub Issue: [#14](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/14).
- Parent: [RTPEval implementation](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12).
- Local specification status: `resolved`.
- Intended GitHub state: `closed`; closure reason: completed.
- Dependency history: None.
- Historical offline implementation and acceptance completed; new extensions/live execution remain separately authorized.

Completed under the approved offline scope: opt-in attempt capture and linked researcher resource reporting. Missing usage is explicit; instrumentation does not run planners on behalf of the evaluator or add resource measurements to quality scores.

## Acceptance criteria

- [x] Use common monotonic outer timing through final result and cleanup; retain stage scope and overlapping timing semantics.
- [x] Capture actual model usage, provider sends, cache hits, retry events and missingness with event IDs; distinguish measured, reported, derived and estimated observations.
- [x] Link usage to selected run and result hash; absent collection may be declared unavailable, never zero.
- [x] Repair totals are subsets of underlying events; oracle usage has a separate ledger.
- [x] Verify mocked success, retries, failure, cache hit, missing tokens and cleanup; instrumentation must not change planning decisions or require a real run.


- [x] Provide researcher-facing per-request resource values, differences and ratios where defined, with compatible measurement scope and explicit missingness. Zero/missing baselines must not create misleading ratios. Descriptive batch summaries retain request-level records; formal inference follows the separate analysis plan.
- [x] Reports support later thesis/presentation discussion, not another non-blind human scoring round. Usage remains hidden from blinded raters and outside itinerary totals; no efficiency score or arbitrary PASS threshold is introduced.

## Contract and evidence

- [usage-capture-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/usage-capture-contract.md)
- [ticket-02-acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/ticket-02-acceptance.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/02-usage-capture-report.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `586cc09bdf55305df34756a9a7c21f3dff8d8ed35074a7d55c53c81f2612fdda`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T02 -->
# 02: Symmetric usage capture and resource report

Blocked by: None. User authorized closure, implementation and offline acceptance on 2026-09-29.

Status: resolved
Type: task

**What to build:** An independently invoked planner attempt can produce linked usage observations and a resource report with comparable outer timing across V0-V3.

**Readiness gate:** Closed by [usage capture contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/usage-capture-contract.md). Implemented as opt-in producer instrumentation, not evaluator-owned planner execution. See [acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/ticket-02-acceptance.md).

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
<!-- END IMPORTED SOURCE T02 -->

</details>
