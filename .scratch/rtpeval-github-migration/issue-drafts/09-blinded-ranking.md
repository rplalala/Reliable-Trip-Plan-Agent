<!-- Draft only. Resolve every migration token before approved publication. -->

## Current status at migration preparation

- Project ticket: RTPEval 09; GitHub issue number/URL pending.
- Parent: [RTPEval implementation]({{ISSUE_PARENT_URL}}).
- Local specification status: `ready-for-agent`.
- Intended GitHub state: `open`.
- Dependency history: [Ticket 01]({{ISSUE_T01_URL}}).
- Implementation authorization: pending. Specification readiness and dependency completion do not grant approval.

Specification-ready; predecessor Ticket 01 is completed offline. Implementation approval is pending. This slice can be scheduled independently of automatic scoring once authorized; no real rater session is approved.

## Acceptance criteria

- [ ] Render original Input and uniform A/B/C/D plans; preserve meaningful uncertainty and hide versions, provenance, internal findings, scores and private mapping.
- [ ] Freeze balanced randomized assignments; sample/task count comes from supplied configuration, not module quotas.
- [ ] Support ties, unjudgeable/N/A and drafts separately for preference, pace and usefulness; every ranked label appears exactly once.
- [ ] Provide save/resume and explicit JSON export/import with revision validation and researcher-only mapping.
- [ ] Derive six correlated pair outcomes; hidden duplicates contribute consistency observations only. Verify metadata leakage and visually inspect renderer examples; no real rater session is authorized.

## Contract and evidence

- [artifact-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/artifact-contract.md)
- [intake-projection-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/intake-projection-contract.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/09-blinded-ranking.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `b227b2770031ce63273a9efa79a13fc060e8153af94a070e2316c0cedcc905c1`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T09 -->
# 09: Four-plan blinded ranking workflow

Blocked by: [01: Batch intake and independent schedule projection]({{ISSUE_T01_URL}})

Status: ready-for-agent
Type: task

**What to build:** Generate a local anonymous HTML review package, save/import rankings and export researcher-side paired outcomes.

**Readiness gate:** Does not wait for automatic scores, Google acquisition or usage collection. Uses the shared source-preserving projection.

**Acceptance criteria:**

- [ ] Render original Input and uniform A/B/C/D plans; preserve meaningful uncertainty and hide versions, provenance, internal findings, scores and private mapping.
- [ ] Freeze balanced randomized assignments; sample/task count comes from supplied configuration, not module quotas.
- [ ] Support ties, unjudgeable/N/A and drafts separately for preference, pace and usefulness; every ranked label appears exactly once.
- [ ] Provide save/resume and explicit JSON export/import with revision validation and researcher-only mapping.
- [ ] Derive six correlated pair outcomes; hidden duplicates contribute consistency observations only. Verify metadata leakage and visually inspect renderer examples; no real rater session is authorized.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
<!-- END IMPORTED SOURCE T09 -->

</details>
