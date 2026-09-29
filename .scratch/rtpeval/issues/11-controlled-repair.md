# 11: Controlled Repair replay and outcome report

Blocked by: [10: Independent V3 before/after report](10-v3-pre-post.md)

Status: needs-info
Type: task

**What to build:** Replay separately supplied controlled fixtures through the real V3 Repair path and report independent target/control outcomes.

**Readiness gate:** Define target/control invariants, regression units, replay seams and frozen capability inputs. Formal case construction and real executions remain separately authorized benchmark work.

**Acceptance criteria:**

- [ ] Use real validator, target selection, scope, candidate preparation, acceptance and re-validation; never inject targets/scopes to bypass measured behavior.
- [ ] Freeze provider responses, candidate pool and capability configuration in offline replay; fail on unexpected live provider/model/DB access.
- [ ] Distinguish confirmed conflicts/product-policy violations from review opportunities using explicit fixture metadata; do not universally call sparse/duplicate/overfull a defect.
- [ ] Retain target-detection misses in denominators and report no-change/control regressions independently of patch acceptance.
- [ ] Support the accepted 24-target/8-control design without generating those formal cases here; use synthetic implementation fixtures only after coding approval.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
