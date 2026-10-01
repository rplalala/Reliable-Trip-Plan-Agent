<!-- Draft only. Resolve every migration token before approved publication. -->

## Current status at migration preparation

- Project ticket: RTPEval 07; GitHub issue number/URL pending.
- Parent: [RTPEval implementation]({{ISSUE_PARENT_URL}}).
- Local specification status: `needs-info`.
- Intended GitHub state: `open`.
- Dependency history: [Ticket 04]({{ISSUE_T04_URL}}).
- Implementation authorization: pending. Specification readiness and dependency completion do not grant approval.

Needs technical specification closure: deterministic continuous-interval/departure selection remains open. Ticket 04 is completed offline; that dependency completion does not close this gate or authorize implementation.

## Acceptance criteria

- [ ] Exclude inter-day legs and confirmed same-canonical transitions as N/A; different venues at one address are not automatically identical.
- [ ] Use stated mode and valid returned Google duration including traffic fallback; successful explicit no-route is FAIL, errors/incomplete evidence UNKNOWN.
- [ ] Apply WALK distance/time cap, TRANSIT/DRIVE caps, DRIVE 600-second reserve, and independent 300-second cap/schedule tolerances without adding them together.
- [ ] Preserve fractional precision, raw overruns/deficits and partial observed subtotals; do not invent duration for no-route or add provider waiting twice.
- [ ] Fixtures cover tolerance boundaries, missing duration/distance, status/condition combinations and blockers; all scoring is offline.

## Contract and evidence

- [route-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/route-contract.md)
- [activity-scope-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/activity-scope-contract.md)
- [evidence-time-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/evidence-time-contract.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/07-route-checks.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `8a2e4fd9fce9ec875d3234bcc26bb4f4eb5266d83cb8a1361b3b891bfc8b5a83`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T07 -->
# 07: Same-day route checks from frozen evidence

Blocked by: [04: Independent snapshot acquisition and offline replay]({{ISSUE_T04_URL}})

Status: needs-info
Type: task

**What to build:** Produce route coverage, feasibility, cap violations and observed transfer burden for actual same-day transitions.

**Readiness gate:** Close deterministic continuous-interval/departure selection around protected time and explicit transport correspondence; no departure search optimization or silent date shifting.

**Acceptance criteria:**

- [ ] Exclude inter-day legs and confirmed same-canonical transitions as N/A; different venues at one address are not automatically identical.
- [ ] Use stated mode and valid returned Google duration including traffic fallback; successful explicit no-route is FAIL, errors/incomplete evidence UNKNOWN.
- [ ] Apply WALK distance/time cap, TRANSIT/DRIVE caps, DRIVE 600-second reserve, and independent 300-second cap/schedule tolerances without adding them together.
- [ ] Preserve fractional precision, raw overruns/deficits and partial observed subtotals; do not invent duration for no-route or add provider waiting twice.
- [ ] Fixtures cover tolerance boundaries, missing duration/distance, status/condition combinations and blockers; all scoring is offline.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
<!-- END IMPORTED SOURCE T07 -->

</details>
