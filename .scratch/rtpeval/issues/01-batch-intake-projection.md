# 01: Batch intake and independent schedule projection

Blocked by: None. Ticket 01 implementation was separately approved and completed.

Status: resolved
Type: task

**What to build:** Submit a curated four-version batch and obtain either an immutable evaluation inventory or actionable intake diagnostics, without running or requalifying planners.

**Readiness gate:** Specification closed on 2026-09-29 in the [intake/projection contract](../intake-projection-contract.md). Independent source linkage, role review, transport association/deduplication and uncertainty paths are defined. Implementation and offline acceptance were subsequently approved and completed; see the acceptance record.

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

Implemented independent batch intake and source-preserving projection, with immutable output and a local CLI. See [Ticket 01 acceptance](../ticket-01-acceptance.md). Validation: 38 passed, 1 skipped (native Windows symlink creation unavailable); Ruff and CLI help passed. No shared planning algorithms changed; no provider/model/database calls, formal benchmark cases or commits. The skip remains an explicit platform limitation.


2026-09-30: Follow-up review findings corrected under explicit user approval. Related regression suite: 113 passed / one existing Windows symlink privilege skip; Ruff checks pass. See the acceptance follow-up for failure-before/fix-after evidence and updated input boundaries. Status remains resolved for the offline scope only.
