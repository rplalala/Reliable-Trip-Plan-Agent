<!-- RTPEVAL-MIGRATION:RTPEVAL draft-sha256:5c90553a89e1f08f370867ff4df4bad635027730dda8a7ba850d396e6c53007d -->

## Scope and current authority

Track the approved RTPEval 12-ticket implementation plan for submitted source-linked
four-version artifacts. PROJECT.md owns current project scope and authorization;
repository contracts own detailed meaning. GitHub Issues are the designated owner
of migrated task state/discussion under the approved tracker switch. Pinned document
links identify the reviewed pre-migration checkpoint; subsequent tracker updates
remain local until separately committed/pushed.

Original local ticket publication: 2026-09-28. Migration draft preparation: 2026-10-01.
Tickets 01-04 completed their approved offline scopes; 05 is specification-ready with
implementation approval pending; 06/08/09 have ready specifications subject to their
predecessors; 07/10/11/12 still need bounded technical closure. No new implementation,
live acquisition, formal case/experiment, freeze or Git action is granted by migration.

## Child issues

- [x] [Ticket 01: Batch intake and independent schedule projection](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/13) — resolved.
- [x] [Ticket 02: Symmetric usage capture and resource report](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/14) — resolved.
- [x] [Ticket 03: Identity resolution, adjudication and grounding report](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/15) — resolved.
- [x] [Ticket 04: Independent snapshot acquisition and offline replay](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/16) — resolved.
- [ ] [Ticket 05: Requirement and schedule metrics](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17) — ready-for-agent.
- [ ] [Ticket 06: Opening checks from frozen evidence](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18) — ready-for-agent.
- [ ] [Ticket 07: Same-day route checks from frozen evidence](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19) — needs-info.
- [ ] [Ticket 08: Multimetric report and auxiliary scores](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20) — ready-for-agent.
- [ ] [Ticket 09: Four-plan blinded ranking workflow](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21) — ready-for-agent.
- [ ] [Ticket 10: Independent V3 before/after report](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22) — needs-info.
- [ ] [Ticket 11: Controlled Repair replay and outcome report](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23) — needs-info.
- [ ] [Ticket 12: Mechanism and official-evidence audit reports](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24) — needs-info.

Dependency links retain completed predecessor history. Open blocker relationships
remain distinct from specification labels and explicit implementation authorization.
The parent remains open until its full approved implementation scope is completed.

## Design and implementation records

- [Reviewed project context at documentation checkpoint](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/PROJECT.md)
- [Approved 12-ticket plan](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/ticket-breakdown.md)
- [Module specification](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/.scratch/rtpeval/spec.md)
- [Evaluator design](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/evaluator_design.md)
- [Implemented package guide](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/backend/evaluation/README.md)

Keep contracts and acceptance records in the repository. References must identify the
reviewed published documentation commit, not an uncommitted working tree or local path.
Current Ticket 05 rule: a reviewed explicit named required visit without stated count or
repetition means exact one for the trip. Source-backed explicit repetition permits
at-least-one fixed-time matching while stated total/date quotas remain binding. Planner
choices and soft interests do not create hard visit obligations. Protected blockers do
not add non-overlap units. Transport occupancy uses V0 model transport activities and
V1-V3 application transfers; planner findings do not supply factual ground truth.

## Migration boundary

Published on 2026-10-01 from the approved local migration draft. Publication and
tracker activation were explicitly authorized. The migration verifies all 13 issue
identities, intended states/labels, 13 dependency edges and accessible contract links.
Future implementation, Git actions and live/research work need their own authorization.
The linked child Issues own live task state; repository contracts and acceptance
records retain detailed meaning. Source ticket files become historical snapshots.
Prior local comments retain their original dates as imported history rather than being
recreated as comments falsely attributed to original dates/authors.
