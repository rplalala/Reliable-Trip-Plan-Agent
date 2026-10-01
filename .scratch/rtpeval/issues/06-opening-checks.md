# Historical RTPEval Ticket 06 snapshot

Imported 2026-10-01. Live task state, labels, dependencies and discussion are owned by
[GitHub Issue #18](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18).
The original local ticket is preserved verbatim below. Its Status, dates and comments
are historical and must not be maintained as a second live tracker.
Repository contracts and acceptance records retain their detailed authority.

<!-- RTPEVAL-HISTORICAL-SOURCE:RTPEVAL-06 -->

---

# 06: Opening checks from frozen evidence

Blocked by: [04: Independent snapshot acquisition and offline replay](04-evidence-snapshot.md)

Status: ready-for-agent
Type: task

**What to build:** Produce opening verdicts and supporting coverage/conflict measurements for applicable visits using offline snapshot evidence.

**Readiness gate:** No additional semantic blocker beyond upstream identity, snapshot and time contracts; independent parser fixtures remain part of implementation acceptance.

**Acceptance criteria:**

- [ ] Apply independent local-time interpretation, multiple/overnight periods and documented always-open encoding.
- [ ] Distinguish current/date-specific, regular fallback, known unresolved special date, closed, missing and invalid evidence.
- [ ] Require full containment with zero grace; end exactly at closing passes.
- [ ] Partial evidence may support a labelled conflict lower bound but cannot invent full outside minutes or complete coverage.
- [ ] Offline boundary/DST/truncation fixtures and an internal-finding mutation test establish evidence-driven results.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
