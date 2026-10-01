<!-- RTPEVAL-MIGRATION:RTPEVAL-06 draft-sha256:616252aa5ba228c3b7aea08fa974f8ccc9248a0663e10ce3568a45887374033f -->

## Current status at migration preparation

- Project ticket: RTPEval 06. Published GitHub Issue: [#18](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18).
- Parent: [RTPEval implementation](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12).
- Local specification status: `ready-for-agent`.
- Intended GitHub state: `open`.
- Dependency history: [Ticket 04](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/16).
- Implementation authorization: pending. Specification readiness and dependency completion do not grant approval.

Specification-ready; predecessor Ticket 04 is completed offline. Implementation approval is still pending. Opening judgments require independent time/evidence parsing and zero grace, with partial/exception evidence retained honestly.

## Acceptance criteria

- [ ] Apply independent local-time interpretation, multiple/overnight periods and documented always-open encoding.
- [ ] Distinguish current/date-specific, regular fallback, known unresolved special date, closed, missing and invalid evidence.
- [ ] Require full containment with zero grace; end exactly at closing passes.
- [ ] Partial evidence may support a labelled conflict lower bound but cannot invent full outside minutes or complete coverage.
- [ ] Offline boundary/DST/truncation fixtures and an internal-finding mutation test establish evidence-driven results.

## Contract and evidence

- [opening-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/opening-contract.md)
- [evidence-time-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/evidence-time-contract.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/06-opening-checks.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `818de3297383a3a960e1c353ac5af16e96654a1a034cd83da40893ad0f384a7d`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T06 -->
# 06: Opening checks from frozen evidence

Blocked by: [04: Independent snapshot acquisition and offline replay](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/16)

Status: ready-for-agent
Type: task

**What to build:** Produce opening verdicts and supporting coverage/conflict measurements for applicable visits using offline snapshot evidence.

**Readiness gate:** No additional semantic blocker beyond upstream identity, snapshot and time contracts; independent parser fixtures remain part of implementation acceptance.

**Acceptance criteria:**

- [ ] Apply independent local-time interpretation, multiple/overnight periods and documented always-open encoding.
- [ ] Distinguish current/date-specific, regular fallback, known unresolved special date, closed, missing and invalid evidence.
- [ ] Require full containment with zero grace; end exactly at closing passes.
- [ ] Partial evidence may support a labelled conflict lower bound but cannot invent full outside minutes or complete coverage.
- [ ] Offline boundary/DST/truncation fixtures and an internal-finding mutation test establish evidence-driven results.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
<!-- END IMPORTED SOURCE T06 -->

</details>
