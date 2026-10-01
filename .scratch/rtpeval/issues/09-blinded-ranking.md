# Historical RTPEval Ticket 09 snapshot

Imported 2026-10-01. Live task state, labels, dependencies and discussion are owned by
[GitHub Issue #21](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21).
The original local ticket is preserved verbatim below. Its Status, dates and comments
are historical and must not be maintained as a second live tracker.
Repository contracts and acceptance records retain their detailed authority.

<!-- RTPEVAL-HISTORICAL-SOURCE:RTPEVAL-09 -->

---

# 09: Four-plan blinded ranking workflow

Blocked by: [01: Batch intake and independent schedule projection](01-batch-intake-projection.md)

Status: ready-for-agent
Type: task

**What to build:** Generate a local anonymous HTML review package, save/import rankings and export researcher-side paired outcomes.

**Readiness gate:** Does not wait for automatic scores, Google acquisition or usage collection. Uses the shared source-preserving projection.

**Acceptance criteria:**

- [ ] Render original Input and uniform A/B/C/D plans; preserve meaningful uncertainty and hide versions, provenance, internal findings, scores and private mapping.
- [ ] Freeze balanced randomized assignments; sample/task count comes from supplied configuration, not module quotas.
- [ ] Support ties, unjudgeable/N/A and drafts separately for preference, pace and usefulness; every ranked label appears exactly once.
- [ ] Provide save/resume and explicit JSON export/import with revision validation and researcher-only mapping.
- [ ] Derive six correlated pair outcomes; hidden duplicates contribute consistency observations only. Verify metadata leakage and visually inspect renderer examples; no real rater session is authorized.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
