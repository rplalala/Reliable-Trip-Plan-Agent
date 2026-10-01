<!-- RTPEVAL-MIGRATION:RTPEVAL-11 draft-sha256:404e3cf38bbf8fa72c9676c06797c6cfcd095ba62b6c3fd8f1ce6f6fe252f87a -->

## Current status at migration preparation

- Project ticket: RTPEval 11. Published GitHub Issue: [#23](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23).
- Parent: [RTPEval implementation](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12).
- Local specification status: `needs-info`.
- Intended GitHub state: `open`.
- Dependency history: [Ticket 10](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22).
- Implementation authorization: pending. Specification readiness and dependency completion do not grant approval.

Needs specification closure and is blocked by unfinished Ticket 10. Controlled replay capability/control invariants remain open; publishing this issue does not generate formal cases or authorize experiments.

## Acceptance criteria

- [ ] Use real validator, target selection, scope, candidate preparation, acceptance and re-validation; never inject targets/scopes to bypass measured behavior.
- [ ] Freeze provider responses, candidate pool and capability configuration in offline replay; fail on unexpected live provider/model/DB access.
- [ ] Distinguish confirmed conflicts/product-policy violations from review opportunities using explicit fixture metadata; do not universally call sparse/duplicate/overfull a defect.
- [ ] Retain target-detection misses in denominators and report no-change/control regressions independently of patch acceptance.
- [ ] Support the accepted 24-target/8-control design without generating those formal cases here; use synthetic implementation fixtures only after coding approval.

## Contract and evidence

- [spec](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/spec.md)
- [metrics-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/metrics-contract.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/11-controlled-repair.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `7776a0459a2d0e0f95bc1dbce50e37076cb516fe3b7a0367d1610c897701bcd3`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T11 -->
# 11: Controlled Repair replay and outcome report

Blocked by: [10: Independent V3 before/after report](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22)

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
<!-- END IMPORTED SOURCE T11 -->

</details>
