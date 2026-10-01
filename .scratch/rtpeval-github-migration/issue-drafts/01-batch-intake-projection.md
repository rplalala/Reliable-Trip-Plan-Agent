<!-- Draft only. Resolve every migration token before approved publication. -->

## Current status at migration preparation

- Project ticket: RTPEval 01; GitHub issue number/URL pending.
- Parent: [RTPEval implementation]({{ISSUE_PARENT_URL}}).
- Local specification status: `resolved`.
- Intended GitHub state: `closed`; closure reason: completed.
- Dependency history: None.
- Historical offline implementation and acceptance completed; new extensions/live execution remain separately authorized.

Completed under the approved offline scope: immutable batch intake, original-input/result provenance and independent role/schedule projection. Version-specific transport source selection is also implemented: V0 activities; V1-V3 transfers. Independent factual feasibility and later metric scoring are separate.

## Acceptance criteria

- [x] Validate file hashes, full-input linkage, reviewed RequirementSpec, selected versions/runs and major schema versions; reject path escapes and do not silently drop groups.
- [x] Preserve original result artifacts and stable source references. Expose itinerary data to quality readers separately from mechanism metadata.
- [x] Treat generic no-POI items as transition/free time; preserve named unresolved visits and protected time; diagnose multi-POI blocks without guessing a split.
- [x] Produce a traceable schedule/transport projection, with duplicate representations reconciled and ambiguous associations explicit.
- [x] Offline fixtures demonstrate valid intake, malformed linkage, unavailable usage envelopes and missing optional draft handling; no runner or provider is invoked.

## Contract and evidence

- [intake-projection-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/intake-projection-contract.md)
- [ticket-01-acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/ticket-01-acceptance.md)
- [transport-correction-acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/transport-correction-acceptance.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/01-batch-intake-projection.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `7fdea086a6805e4d401357843f6b2f00f09117a6dd1dc36a6a8b4209587dedfc`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T01 -->
# 01: Batch intake and independent schedule projection

Blocked by: None. Ticket 01 implementation was separately approved and completed.

Status: resolved
Type: task

**What to build:** Submit a curated four-version batch and obtain either an immutable evaluation inventory or actionable intake diagnostics, without running or requalifying planners.

**Readiness gate:** Specification closed on 2026-09-29 in the [intake/projection contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/intake-projection-contract.md). Independent source linkage, role review, transport association/deduplication and uncertainty paths are defined. Implementation and offline acceptance were subsequently approved and completed; see the acceptance record.

**Acceptance criteria:**

- [x] Validate file hashes, full-input linkage, reviewed RequirementSpec, selected versions/runs and major schema versions; reject path escapes and do not silently drop groups.
- [x] Preserve original result artifacts and stable source references. Expose itinerary data to quality readers separately from mechanism metadata.
- [x] Treat generic no-POI items as transition/free time; preserve named unresolved visits and protected time; diagnose multi-POI blocks without guessing a split.
- [x] Produce a traceable schedule/transport projection, with duplicate representations reconciled and ambiguous associations explicit.
- [x] Offline fixtures demonstrate valid intake, malformed linkage, unavailable usage envelopes and missing optional draft handling; no runner or provider is invoked.

## Authorization and verification boundary

The original publication did not authorize implementation. On 2026-09-29 the user separately approved Ticket 01 implementation and offline acceptance; this ticket is now resolved. Specification readiness does not mean dependencies are complete or execution is permitted. The acceptance record reports executed offline checks; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.

2026-09-28 pause checkpoint: The user requested documentation updates before a break. This ticket remains needs-info, unclaimed and not implemented. The next intended activity is specification closure, not execution. Code-resolvable facts should be checked directly; only unresolved result-meaning choices require user questions.

2026-09-29: The user authorized specification closure only. Current schemas/prompts/policies were inspected at 364f91f. The detailed contract closes this ticket's technical information gap without changing quality formulas. Status is now ready-for-agent for specification readiness; no implementation is claimed or tested, and unchecked acceptance criteria remain future work.

2026-09-29: User authorized Ticket 01 implementation and offline acceptance. Claimed for this scope only; later tickets, live calls and Git actions remain unauthorized.

## Answer

Implemented independent batch intake and source-preserving projection, with immutable output and a local CLI. See [Ticket 01 acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/ticket-01-acceptance.md). Validation: 38 passed, 1 skipped (native Windows symlink creation unavailable); Ruff and CLI help passed. No shared planning algorithms changed; no provider/model/database calls, formal benchmark cases or commits. The skip remains an explicit platform limitation.


2026-09-30: Follow-up review findings corrected under explicit user approval. Related regression suite: 113 passed / one existing Windows symlink privilege skip; Ruff checks pass. See the acceptance follow-up for failure-before/fix-after evidence and updated input boundaries. Status remains resolved for the offline scope only.
<!-- END IMPORTED SOURCE T01 -->

</details>
