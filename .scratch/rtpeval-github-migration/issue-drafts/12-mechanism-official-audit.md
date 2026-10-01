<!-- Draft only. Resolve every migration token before approved publication. -->

## Current status at migration preparation

- Project ticket: RTPEval 12; GitHub issue number/URL pending.
- Parent: [RTPEval implementation]({{ISSUE_PARENT_URL}}).
- Local specification status: `needs-info`.
- Intended GitHub state: `open`.
- Dependency history: [Ticket 01]({{ISSUE_T01_URL}}).
- Implementation authorization: pending. Specification readiness and dependency completion do not grant approval.

Needs technical closure of mechanism denominators and accepted/exposed/rule-used evidence provenance. Predecessor Ticket 01 is completed offline; independent quality judgment remains separate.

## Acceptance criteria

- [ ] Mechanism metadata has a separate reader; it cannot change quality judgments or identity decisions.
- [ ] Distinguish trigger, acceptance, round progression and internal target status from independently measured resolution.
- [ ] Official audit includes Evidence-Gate-accepted facts exposed to the model or used by a rule; no claim of causal LLM use or random website cross-check.
- [ ] Attach existing linked usage where available; do not depend on completed usage collection or invent missing stage costs.
- [ ] Fixtures cover rejected/unexposed facts, exposed/rule-used facts, missing trace and duplicate round records; output includes provenance and audit availability, not fabricated official truth.

## Contract and evidence

- [spec](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/spec.md)
- [metrics-contract](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/{{DOCUMENTATION_COMMIT}}/.scratch/rtpeval/metrics-contract.md)

Detailed contracts remain versioned repository documents. Their URLs use the reviewed
publication commit; the migration draft is not evidence that these documents are online.
The original-input/project authority and task approval rules remain in PROJECT.md/AGENTS.md.
Historical test numbers below are recorded results, not tests rerun during migration.

## Migration provenance

Prepared 2026-10-01 (Australia/Sydney) from `.scratch/rtpeval/issues/12-mechanism-official-audit.md` at local code
checkpoint `473600254023f7d41648eed02215b6ab84e4ff03` plus the uncommitted documentation state.
Exact source-byte SHA-256: `b7f2fe7a04f40c45d8be0653ddbe2c0d38666458761c5b60b7e9f9baa97e5198`.
GitHub creation/import dates will be migration dates; original work dates remain in
the preserved record. Historical statements about pending work, missing authorization
or uncommitted code apply to their original checkpoints; the current summary above
and linked current contracts describe this migration snapshot.

<details>
<summary>Preserved local ticket and historical comments</summary>

<!-- BEGIN IMPORTED SOURCE T12 -->
# 12: Mechanism and official-evidence audit reports

Blocked by: [01: Batch intake and independent schedule projection]({{ISSUE_T01_URL}})

Status: needs-info
Type: task

**What to build:** Export traceable internal mechanism observations and an audit queue for qualifying official facts, isolated from independent quality scores.

**Readiness gate:** Map exact round/target/acceptance denominators and accepted/exposed/rule-used fact provenance at the implementation checkpoint; absent signals must remain unavailable.

**Acceptance criteria:**

- [ ] Mechanism metadata has a separate reader; it cannot change quality judgments or identity decisions.
- [ ] Distinguish trigger, acceptance, round progression and internal target status from independently measured resolution.
- [ ] Official audit includes Evidence-Gate-accepted facts exposed to the model or used by a rule; no claim of causal LLM use or random website cross-check.
- [ ] Attach existing linked usage where available; do not depend on completed usage collection or invent missing stage costs.
- [ ] Fixtures cover rejected/unexposed facts, exposed/rule-used facts, missing trace and duplicate round records; output includes provenance and audit availability, not fabricated official truth.

## Authorization and verification boundary

Publication records the approved breakdown only. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.
<!-- END IMPORTED SOURCE T12 -->

</details>
