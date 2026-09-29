# 04: Independent snapshot acquisition and offline replay

Blocked by: [03: Identity resolution, adjudication and grounding report](03-identity-adjudication.md)

Status: resolved
Type: task

**What to build:** Acquire or replay a shared, versioned evidence snapshot for the batch venue union and each required directed route context.

**Readiness gate:** Closed by [snapshot contract](../snapshot-contract.md) under explicit offline implementation approval; live acquisition remains unauthorized.

**Acceptance criteria:**

- [x] Include available V3 drafts when paired scoring is requested; union collection does not merge visit occurrences.
- [x] Use evaluation-owned cache/evidence; preserve raw provider provenance, request context, retrieval times, failures and hashes.
- [x] Route keys distinguish endpoints, direction, mode and departure context; do not substitute planner baseline evidence or reverse-leg estimates.
- [x] Frozen snapshot replay performs no network calls; partial provider failures remain recorded rather than silently shrinking denominators.
- [x] Mock acquisition demonstrates deduplication, missing matrix elements, retry accounting, corruption detection and deterministic replay.

## Authorization and verification boundary

The original publication authorized the breakdown only. The user subsequently approved this ticket through offline implementation and validation; see the acceptance record. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.


2026-09-30: User approved offline contract closure and implementation with injected fake transport, versioned snapshot persistence and replay. No live provider/model/database acquisition or Git action authorized.


## Answer

Implemented [snapshot planning/acquisition/replay](../../../backend/evaluation/snapshot.py), [offline CLI](../../../backend/evaluation/snapshot_cli.py), and [35 synthetic tests](../../../backend/tests/evaluation/test_snapshot.py). See [contract](../snapshot-contract.md) and [acceptance](../ticket-04-acceptance.md). Final full backend validation: 1957 passed, 10 skipped; Ruff/format/compile checks pass. Timestamp integrity findings were corrected; Standards and Spec final reviews each have zero outstanding findings. This resolves only the approved injected-transport/offline scope; live Google serialization/acquisition, operational retention approval and formal evaluation are not claimed.
