# 10: Independent V3 before/after report

Blocked by: [08: Multimetric report and auxiliary scores](08-quality-report-scores.md)

Status: needs-info
Type: task

**What to build:** Score available draft/final pairs against one frozen snapshot and trace independent changes with visit-loss and regression context.

**Readiness gate:** Define activity correspondence, many-to-many edits and independent conflict/obligation tracking without using internal target IDs.

**Acceptance criteria:**

- [ ] Require both outputs; missing pair is unavailable, identical valid outputs can yield zero change.
- [ ] Track date, canonical identity, requirement obligation and source correspondence; target disappearance does not prove resolution.
- [ ] Report new conflicts, removed visits, coverage and denominator changes alongside score deltas.
- [ ] Keep pre-repair draft labelled as V3 draft, never an independent V2 run.
- [ ] Fixtures verify unchanged outputs, removed/replaced visits, unresolved mapping and newly introduced conflicts.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
