# 03: Identity resolution, adjudication and grounding report

Blocked by: [01: Batch intake and independent schedule projection](01-batch-intake-projection.md)

Status: resolved
Type: task

**What to build:** Convert submitted venue references into independently evidenced identities, review queues and a grounding/ID-consistency report.

**Readiness gate:** Specify conservative automatic acceptance, role review and preselected audit sampling using development fixtures before implementing or enabling automatic acceptance.

**Acceptance criteria:**

- [x] Name-only and supplied-ID references receive independent association checks; provider rank and ID retrieval alone cannot prove a match.
- [x] Ambiguity, ID/name conflict and high-impact requirement matches enter adjudication; unresolved decisions retain reasons.
- [x] Preserve claimed-ID conflict even when a reviewed named venue supplies downstream identity; do not rewrite planner output.
- [x] Persist versioned review decisions and replay them; audit selection cannot depend on favorable version results.
- [x] Fixtures cover branches, wrong cities, aliases, malformed candidates, wrong IDs and unavailable evidence; changing V3 findings cannot change grounding.

## Publication boundary (historical)

At publication, the approved breakdown did not authorize implementation. The current offline implementation and acceptance are recorded below. Live services, formal cases, experiments, commits and freezes remain separately controlled.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.

2026-09-29: Ticket 01 was resolved and the user requested Ticket 03 offline implementation after a scope review. Work was claimed. The user then accepted separate strict supplied-ID details and no-ID name-search paths, high-impact review, and predeclared audit sampling. No live acquisition or formal evaluation was authorized.

## Answer

Implemented the [offline identity contract](../identity-implementation-contract.md), [replay module](../../../backend/evaluation/identity.py), [CLI](../../../backend/evaluation/identity_cli.py) and [synthetic acceptance tests](../../../backend/tests/evaluation/test_identity.py). [Acceptance](../ticket-03-acceptance.md) records 58 passed, one platform-dependent skip, Ruff/CLI checks, review corrections and remaining evidence-acquisition limits. Ticket 04 remains responsible for independent live snapshot collection under separate authorization.


2026-09-30 follow-up: four review defects were reproduced, corrected and covered by 20 additional offline regression cases after user authorization. Latest acceptance is 78 passed / one Windows symlink privilege skip, with Ruff/format checks passing and zero actionable Standards/Spec follow-up findings. Status remains resolved for the offline scope only; see the acceptance follow-up for exact conservative address/title rules and limits.
