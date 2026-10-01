<!-- RTPEVAL-MIGRATION:RTPEVAL-10 draft-sha256:e931a01a7127dde3f8c5d7b8b682493043446c3e9ef118afb627689423ebcc8f -->

## Current status at migration preparation

- Project ticket: RTPEval 10. Published GitHub Issue: [#22](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22).
- Parent: [RTPEval implementation](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12).
- Local specification status: `needs-info`.
- Intended GitHub state: `open`.
- Dependency history: [Ticket 08](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20).
- Implementation authorization: pending. Specification readiness and dependency completion do not grant approval.

Needs specification closure and is blocked by unfinished Ticket 08. Activity correspondence, denominator changes and independent obligation/conflict tracking must be defined before implementation.

## Acceptance criteria

- [ ] Require both outputs; missing pair is unavailable, identical valid outputs can yield zero change.
- [ ] Track date, canonical identity, requirement obligation and source correspondence; target disappearance does not prove resolution.
- [ ] Report new conflicts, removed visits, coverage and denominator changes alongside score deltas.
- [ ] Keep pre-repair draft labelled as V3 draft, never an independent V2 run.
- [ ] Fixtures verify unchanged outputs, removed/replaced visits, unresolved mapping and newly introduced conflicts.

## Contract and evidence

- [metrics-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/metrics-contract.md)
- [spec](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/spec.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/10-v3-pre-post.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `f50c22e05bb3d6886b0a3d41a394d3d70a8240c7ee81ff0ad658017ecf05d815`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T10 -->
# 10: Independent V3 before/after report

Blocked by: [08: Multimetric report and auxiliary scores](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20)

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
<!-- END IMPORTED SOURCE T10 -->

</details>
