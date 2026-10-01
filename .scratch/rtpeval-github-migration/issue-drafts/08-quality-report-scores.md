<!-- Draft only. Resolve every migration token before approved publication. -->

## Current status at migration preparation

- Project ticket: RTPEval 08; GitHub issue number/URL pending.
- Parent: [RTPEval implementation]({{ISSUE_PARENT_URL}}).
- Local specification status: `ready-for-agent`.
- Intended GitHub state: `open`.
- Dependency history: [Ticket 05]({{ISSUE_T05_URL}}); [Ticket 06]({{ISSUE_T06_URL}}); [Ticket 07]({{ISSUE_T07_URL}}).
- Implementation authorization: pending. Specification readiness and dependency completion do not grant approval.

Specification-ready but blocked by unfinished Tickets 05, 06 and 07. The accepted common-mask five-dimension arithmetic must preserve UNKNOWN, denominator availability and separate descriptive/resource/human tracks. Implementation approval is pending.

## Acceptance criteria

- [ ] Compute verified score P/(P+F+U), coverage (P+F)/N and companion counts without turning UNKNOWN into FAIL.
- [ ] Apply one group-wide dimension mask; common N/A is omitted, individual no-check N/A contributes zero while raw rates remain N/A.
- [ ] Keep quality metrics, usage and human judgments separate; preserve mask/counts and do not claim a universal usefulness score.
- [ ] Export input/snapshot/rule hashes and availability; an empty mask returns a diagnostic, not an invented total.
- [ ] Fixture batch-to-report tests verify exact arithmetic, repeatability, no network, and invariance under changes to V3 internal findings; inferential analysis is outside this ticket.

## Contract and evidence

- [metrics-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/metrics-contract.md)
- [score-profile](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/score-profile.md)
- [artifact-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/artifact-contract.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/08-quality-report-scores.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `8f5ce91fbd133057aa3252cfd3009f8a379a72f2307b7f2be46dd7c333815adc`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T08 -->
# 08: Multimetric report and auxiliary scores

Blocked by: [05: Requirement and schedule metrics]({{ISSUE_T05_URL}}); [06: Opening checks from frozen evidence]({{ISSUE_T06_URL}}); [07: Same-day route checks from frozen evidence]({{ISSUE_T07_URL}})

Status: ready-for-agent
Type: task

**What to build:** Export a reproducible four-version request-level quality report with the accepted five subscores and auxiliary total.

**Readiness gate:** No dependency on usage, human judgments or mechanism reports; missing optional tracks remain explicitly pending/unavailable.

**Acceptance criteria:**

- [ ] Compute verified score P/(P+F+U), coverage (P+F)/N and companion counts without turning UNKNOWN into FAIL.
- [ ] Apply one group-wide dimension mask; common N/A is omitted, individual no-check N/A contributes zero while raw rates remain N/A.
- [ ] Keep quality metrics, usage and human judgments separate; preserve mask/counts and do not claim a universal usefulness score.
- [ ] Export input/snapshot/rule hashes and availability; an empty mask returns a diagnostic, not an invented total.
- [ ] Fixture batch-to-report tests verify exact arithmetic, repeatability, no network, and invariance under changes to V3 internal findings; inferential analysis is outside this ticket.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
<!-- END IMPORTED SOURCE T08 -->

</details>
