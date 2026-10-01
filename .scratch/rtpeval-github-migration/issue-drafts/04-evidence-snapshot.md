<!-- Draft only. Resolve every migration token before approved publication. -->

## Current status at migration preparation

- Project ticket: RTPEval 04; GitHub issue number/URL pending.
- Parent: [RTPEval implementation]({{ISSUE_PARENT_URL}}).
- Local specification status: `resolved`.
- Intended GitHub state: `closed`; closure reason: completed.
- Dependency history: [Ticket 03]({{ISSUE_T03_URL}}).
- Historical offline implementation and acceptance completed; new extensions/live execution remain separately authorized.

Completed under the approved injected-transport/offline scope: independent snapshot planning, bounded persistence and integrity-checked replay. This completion does not supply a built-in operational Google client or authorize live acquisition.

## Acceptance criteria

- [x] Include available V3 drafts when paired scoring is requested; union collection does not merge visit occurrences.
- [x] Use evaluation-owned cache/evidence; preserve raw provider provenance, request context, retrieval times, failures and hashes.
- [x] Route keys distinguish endpoints, direction, mode and departure context; do not substitute planner baseline evidence or reverse-leg estimates.
- [x] Frozen snapshot replay performs no network calls; partial provider failures remain recorded rather than silently shrinking denominators.
- [x] Mock acquisition demonstrates deduplication, missing matrix elements, retry accounting, corruption detection and deterministic replay.

## Contract and evidence

- [snapshot-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/snapshot-contract.md)
- [ticket-04-acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/ticket-04-acceptance.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/04-evidence-snapshot.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `c8547fd5a1ed360bd07be40bf3de62ce8989aeb06445c4cd1043bc6787537532`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T04 -->
# 04: Independent snapshot acquisition and offline replay

Blocked by: [03: Identity resolution, adjudication and grounding report]({{ISSUE_T03_URL}})

Status: resolved
Type: task

**What to build:** Acquire or replay a shared, versioned evidence snapshot for the batch venue union and each required directed route context.

**Readiness gate:** Closed by [snapshot contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/snapshot-contract.md) under explicit offline implementation approval; live acquisition remains unauthorized.

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

Implemented [snapshot planning/acquisition/replay](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/backend/evaluation/snapshot.py), [offline CLI](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/backend/evaluation/snapshot_cli.py), and [35 synthetic tests](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/backend/tests/evaluation/test_snapshot.py). See [contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/snapshot-contract.md) and [acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/ticket-04-acceptance.md). Final full backend validation: 1957 passed, 10 skipped; Ruff/format/compile checks pass. Timestamp integrity findings were corrected; Standards and Spec final reviews each have zero outstanding findings. This resolves only the approved injected-transport/offline scope; live Google serialization/acquisition, operational retention approval and formal evaluation are not claimed.
<!-- END IMPORTED SOURCE T04 -->

</details>
