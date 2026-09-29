# 04: Independent snapshot acquisition and offline replay

Blocked by: [03: Identity resolution, adjudication and grounding report](03-identity-adjudication.md)

Status: needs-info
Type: task

**What to build:** Acquire or replay a shared, versioned evidence snapshot for the batch venue union and each required directed route context.

**Readiness gate:** Specify bounded acquisition settings, retry/completeness behavior and persistence constraints; no live acquisition is authorized by ticket drafting or offline implementation.

**Acceptance criteria:**

- [ ] Include available V3 drafts when paired scoring is requested; union collection does not merge visit occurrences.
- [ ] Use evaluation-owned cache/evidence; preserve raw provider provenance, request context, retrieval times, failures and hashes.
- [ ] Route keys distinguish endpoints, direction, mode and departure context; do not substitute planner baseline evidence or reverse-leg estimates.
- [ ] Frozen snapshot replay performs no network calls; partial provider failures remain recorded rather than silently shrinking denominators.
- [ ] Mock acquisition demonstrates deduplication, missing matrix elements, retry accounting, corruption detection and deterministic replay.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
