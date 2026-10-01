# Historical RTPEval Ticket 12 snapshot

Imported 2026-10-01. Live task state, labels, dependencies and discussion are owned by
[GitHub Issue #24](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24).
The original local ticket is preserved verbatim below. Its Status, dates and comments
are historical and must not be maintained as a second live tracker.
Repository contracts and acceptance records retain their detailed authority.

<!-- RTPEVAL-HISTORICAL-SOURCE:RTPEVAL-12 -->

---

# 12: Mechanism and official-evidence audit reports

Blocked by: [01: Batch intake and independent schedule projection](01-batch-intake-projection.md)

Status: needs-info
Type: task

**What to build:** Export traceable internal mechanism observations and an audit queue for qualifying official facts, isolated from independent quality scores.

**Readiness gate:** Map exact round/target/acceptance denominators and accepted/exposed/rule-used fact provenance at the implementation checkpoint; absent signals must remain unavailable.

**Acceptance criteria:**

- [ ] Mechanism metadata has a separate reader; it cannot change quality judgments or identity decisions.
- [ ] Distinguish trigger, acceptance, round progression and internal target status from independently measured resolution.
- [ ] Official audit includes Evidence-Gate-accepted facts exposed to the model or used by a rule; no claim of causal LLM use or random website cross-check.
- [ ] Attach existing linked usage where available; do not depend on completed usage collection or invent missing stage costs.
- [ ] Fixtures cover rejected/unexposed facts, exposed/rule-used facts, missing trace and duplicate round records; output includes provenance and audit availability, not fabricated official truth.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
