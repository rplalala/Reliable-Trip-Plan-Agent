# 07: Same-day route checks from frozen evidence

Blocked by: [04: Independent snapshot acquisition and offline replay](04-evidence-snapshot.md)

Status: needs-info
Type: task

**What to build:** Produce route coverage, feasibility, cap violations and observed transfer burden for actual same-day transitions.

**Readiness gate:** Close deterministic continuous-interval/departure selection around protected time and explicit transport correspondence; no departure search optimization or silent date shifting.

**Acceptance criteria:**

- [ ] Exclude inter-day legs and confirmed same-canonical transitions as N/A; different venues at one address are not automatically identical.
- [ ] Use stated mode and valid returned Google duration including traffic fallback; successful explicit no-route is FAIL, errors/incomplete evidence UNKNOWN.
- [ ] Apply WALK distance/time cap, TRANSIT/DRIVE caps, DRIVE 600-second reserve, and independent 300-second cap/schedule tolerances without adding them together.
- [ ] Preserve fractional precision, raw overruns/deficits and partial observed subtotals; do not invent duration for no-route or add provider waiting twice.
- [ ] Fixtures cover tolerance boundaries, missing duration/distance, status/condition combinations and blockers; all scoring is offline.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
