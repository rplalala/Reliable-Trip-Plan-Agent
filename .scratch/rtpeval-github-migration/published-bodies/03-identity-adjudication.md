<!-- RTPEVAL-MIGRATION:RTPEVAL-03 draft-sha256:cd126c1ba90b5bd362b1e81df5c29b098382ed0181ccee47eb34b5422248357f -->

## Current status at migration preparation

- Project ticket: RTPEval 03. Published GitHub Issue: [#15](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/15).
- Parent: [RTPEval implementation](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12).
- Local specification status: `resolved`.
- Intended GitHub state: `closed`; closure reason: completed.
- Dependency history: [Ticket 01](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/13).
- Historical offline implementation and acceptance completed; new extensions/live execution remain separately authorized.

Completed under the approved offline scope: independent supplied-ID/name-only association, factual adjudication, predeclared automatic-result audit and grounding/ID-consistency reports. Follow-up regression is recorded below; live Google evidence completeness is not claimed. The planned Ticket 05 fixed-time subject extension remains future work.

## Acceptance criteria

- [x] Name-only and supplied-ID references receive independent association checks; provider rank and ID retrieval alone cannot prove a match.
- [x] Ambiguity, ID/name conflict and high-impact requirement matches enter adjudication; unresolved decisions retain reasons.
- [x] Preserve claimed-ID conflict even when a reviewed named venue supplies downstream identity; do not rewrite planner output.
- [x] Persist versioned review decisions and replay them; audit selection cannot depend on favorable version results.
- [x] Fixtures cover branches, wrong cities, aliases, malformed candidates, wrong IDs and unavailable evidence; changing V3 findings cannot change grounding.

## Contract and evidence

- [identity-implementation-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/identity-implementation-contract.md)
- [ticket-03-acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/ticket-03-acceptance.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/03-identity-adjudication.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `07f777812bd1e8c27023fbf728f022503587490512d2f9cf0898fbdd005fc416`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T03 -->
# 03: Identity resolution, adjudication and grounding report

Blocked by: [01: Batch intake and independent schedule projection](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/13)

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

Implemented the [offline identity contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/identity-implementation-contract.md), [replay module](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/backend/evaluation/identity.py), [CLI](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/backend/evaluation/identity_cli.py) and [synthetic acceptance tests](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/backend/tests/evaluation/test_identity.py). [Acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/ticket-03-acceptance.md) records 58 passed, one platform-dependent skip, Ruff/CLI checks, review corrections and remaining evidence-acquisition limits. Ticket 04 remains responsible for independent live snapshot collection under separate authorization.


2026-09-30 follow-up: four review defects were reproduced, corrected and covered by 20 additional offline regression cases after user authorization. Latest acceptance is 78 passed / one Windows symlink privilege skip, with Ruff/format checks passing and zero actionable Standards/Spec follow-up findings. Status remains resolved for the offline scope only; see the acceptance follow-up for exact conservative address/title rules and limits.
<!-- END IMPORTED SOURCE T03 -->

</details>
