# 01: Batch intake and independent schedule projection

Blocked by: None. Specification closure and separate implementation approval are still required.

Status: needs-info
Type: task

**What to build:** Submit a curated four-version batch and obtain either an immutable evaluation inventory or actionable intake diagnostics, without running or requalifying planners.

**Readiness gate:** Exact independent activity-role and transport/Transfer correspondence rules must be completed before implementation; use current artifacts and schema, not V3 lineage.

**Acceptance criteria:**

- [ ] Validate file hashes, full-input linkage, reviewed RequirementSpec, selected versions/runs and major schema versions; reject path escapes and do not silently drop groups.
- [ ] Preserve original result artifacts and stable source references. Expose itinerary data to quality readers separately from mechanism metadata.
- [ ] Treat generic no-POI items as transition/free time; preserve named unresolved visits and protected time; diagnose multi-POI blocks without guessing a split.
- [ ] Produce a traceable schedule/transport projection, with duplicate representations reconciled and ambiguous associations explicit.
- [ ] Offline fixtures demonstrate valid intake, malformed linkage, unavailable usage envelopes and missing optional draft handling; no runner or provider is invoked.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.

2026-09-28 pause checkpoint: The user requested documentation updates before a break. This ticket remains needs-info, unclaimed and not implemented. The next intended activity is specification closure, not execution. Code-resolvable facts should be checked directly; only unresolved result-meaning choices require user questions.
