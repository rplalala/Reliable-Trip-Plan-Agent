# Historical RTPEval Ticket 08 snapshot

Imported 2026-10-01. Live task state, labels, dependencies and discussion are owned by
[GitHub Issue #20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20).
The original local ticket is preserved verbatim below. Its Status, dates and comments
are historical and must not be maintained as a second live tracker.
Repository contracts and acceptance records retain their detailed authority.

<!-- RTPEVAL-HISTORICAL-SOURCE:RTPEVAL-08 -->

---

# 08: Multimetric report and auxiliary scores

Blocked by: [05: Requirement and schedule metrics](05-requirement-schedule-metrics.md); [06: Opening checks from frozen evidence](06-opening-checks.md); [07: Same-day route checks from frozen evidence](07-route-checks.md)

Status: ready-for-agent
Type: task

**What to build:** Export a reproducible four-version request-level quality report with the accepted five subscores and auxiliary total.

**Readiness gate:** No dependency on usage, human judgments or mechanism reports; missing optional tracks remain explicitly pending/unavailable.

**Acceptance criteria:**

- [ ] Compute verified score P/(P+F+U), coverage (P+F)/N and companion counts without turning UNKNOWN into FAIL.
- [ ] Apply one group-wide dimension mask; common N/A is omitted, individual no-check N/A contributes zero while raw rates remain N/A.
- [ ] Keep quality metrics, usage and human judgments separate; preserve mask/counts and do not claim a universal usefulness score.
- [ ] Export input/snapshot/rule hashes and availability; an empty mask returns a diagnostic, not an invented total.
- [ ] Fixture batch-to-report tests verify exact arithmetic, repeatability, no network, and invariance under changes to V3 internal findings; inferential analysis is outside this ticket.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
