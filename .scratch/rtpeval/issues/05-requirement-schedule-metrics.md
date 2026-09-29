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


## Accepted scope-review decisions - 2026-09-30

- Same-scope overlapping protected_time intervals form one occupancy blocker with all original obligation references retained. The protections do not conflict with each other merely by overlapping; each original obligation is still evaluated separately. Differing protection scopes must not be flattened into one restriction.
- Transport representation follows the user's explicit version boundary: V0 uses model transport activities; V1-V3 use application-owned transfers exclusively. Model transport activities in V1-V3 remain original source records but do not contribute transport occupancy or fallback. Independent route evidence remains required. This supersedes the earlier equal-authority Activity/Transfer conflict question.
- Before Ticket 05 scoring, correct Ticket 01 projection and its tests to apply the accepted transport-source rule. Current code still implements the earlier reconciliation rule. This is an identified prerequisite, not completed work.

Time-operator/wire closure and the concrete implementation scope remain pending. This update records accepted decisions only; it does not claim Ticket 05 implementation or tests.


2026-09-30 transport prerequisite update: version-specific source selection and generation boundaries are implemented in the uncommitted workspace. See the transport correction sections of the projection contract and PROJECT.md. Ticket 05 scoring, time-operator closure and protected-time blocker union remain unimplemented; this prerequisite does not authorize starting them.

Transport prerequisite acceptance: [correction record](../transport-correction-acceptance.md), final backend 1973 passed / 10 skipped. Ticket 05 remains needs-info; no scoring was implemented.
