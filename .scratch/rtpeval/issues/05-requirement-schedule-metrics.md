# 05: Requirement and schedule metrics

Blocked by: [01: Batch intake and independent schedule projection](01-batch-intake-projection.md); [03: Identity resolution, adjudication and grounding report](03-identity-adjudication.md)

Status: needs-info
Type: task

**What to build:** Score reviewed obligations and schedule structure, and report date coverage, overlap, density and repetition from independent records.

**Readiness gate:** Finish supported time-operator boundaries and metric unit enumeration, including the non-overlap subscore; explicit counts must not be diluted by arbitrary extra subchecks.

**Acceptance criteria:**

- [ ] Support minimum/exact/date obligations and exclusions; possible unresolved matches can prevent definitive absence/count conclusions.
- [ ] Nearby never satisfies primary-visit obligations; minimum revisits are not automatically repetition violations.
- [ ] Report positive overlap pairs and union overlap time separately, without duplicate transport occupancy.
- [ ] Report density, repeat counts and date coverage descriptively rather than turning every sparse/overfull day into FAIL.
- [ ] Fixtures exercise touching intervals, multiple overlaps, unresolved identity and protected intervals; never infer new requirements from planner interpretation.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
