# 03: Identity resolution, adjudication and grounding report

Blocked by: [01: Batch intake and independent schedule projection](01-batch-intake-projection.md)

Status: needs-info
Type: task

**What to build:** Convert submitted venue references into independently evidenced identities, review queues and a grounding/ID-consistency report.

**Readiness gate:** Specify conservative automatic acceptance, role review and preselected audit sampling using development fixtures before implementing or enabling automatic acceptance.

**Acceptance criteria:**

- [ ] Name-only and supplied-ID references receive independent association checks; provider rank and ID retrieval alone cannot prove a match.
- [ ] Ambiguity, ID/name conflict and high-impact requirement matches enter adjudication; unresolved decisions retain reasons.
- [ ] Preserve claimed-ID conflict even when a reviewed named venue supplies downstream identity; do not rewrite planner output.
- [ ] Persist versioned review decisions and replay them; audit selection cannot depend on favorable version results.
- [ ] Fixtures cover branches, wrong cities, aliases, malformed candidates, wrong IDs and unavailable evidence; changing V3 findings cannot change grounding.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
