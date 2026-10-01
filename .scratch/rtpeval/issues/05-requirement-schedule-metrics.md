# Historical RTPEval Ticket 05 snapshot

Imported 2026-10-01. Live task state, labels, dependencies and discussion are owned by
[GitHub Issue #17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17).
The original local ticket is preserved verbatim below. Its Status, dates and comments
are historical and must not be maintained as a second live tracker.
Repository contracts and acceptance records retain their detailed authority.

<!-- RTPEVAL-HISTORICAL-SOURCE:RTPEVAL-05 -->

---

# 05: Requirement and schedule metrics

Blocked by: [01: Batch intake and independent schedule projection](01-batch-intake-projection.md); [03: Identity resolution, adjudication and grounding report](03-identity-adjudication.md)

Status: ready-for-agent
Type: task

**What to build:** Score reviewed obligations and schedule structure, and report date coverage, overlap, density and repetition from independent records.

**Readiness gate:** Closed by the [requirement/schedule contract](../requirement-schedule-contract.md) on 2026-10-01. One parent obligation is one check; protected intervals are blockers, not extra activity units. Implementation approval remains pending.

**Acceptance criteria:**

- [ ] Support minimum/exact/date obligations and exclusions; possible unresolved matches can prevent definitive absence/count conclusions.
- [ ] Nearby never satisfies primary-visit obligations; minimum revisits are not automatically repetition violations.
- [ ] Report positive overlap pairs and union overlap time separately, without duplicate transport occupancy.
- [ ] Report density, repeat counts and date coverage descriptively rather than turning every sparse/overfull day into FAIL.
- [ ] Fixtures exercise touching intervals, multiple overlaps, unresolved identity and protected intervals; never infer new requirements from planner interpretation.

## Authorization and verification boundary

The specification is ready after the approved closure and Q1/Q2 decisions on 2026-10-01. This ticket is not claimed and implementation is not authorized. Specification readiness does not mean dependencies are complete or execution is permitted. Acceptance checks are future work, not test results. Use offline fixtures/mocks only after implementation approval; live services, formal cases, experiments, commits and freezes require separate authorization. Resolve technical facts from current code/contracts; ask only about unresolved choices affecting result meaning.

## Comments

2026-09-28: The user approved the 12-ticket granularity and dependencies. Published without implementation. The approved breakdown index supplies shared specification and contract references.


## Accepted scope-review decisions - 2026-09-30

- Same-scope overlapping protected_time intervals form one occupancy blocker with all original obligation references retained. The protections do not conflict with each other merely by overlapping; each original obligation is still evaluated separately. Differing protection scopes must not be flattened into one restriction.
- Transport representation follows the user's explicit version boundary: V0 uses model transport activities; V1-V3 use application-owned transfers exclusively. Model transport activities in V1-V3 remain original source records but do not contribute transport occupancy or fallback. Independent route evidence remains required. This supersedes the earlier equal-authority Activity/Transfer conflict question.
- Before Ticket 05 scoring, correct Ticket 01 projection and its tests to apply the accepted transport-source rule. Current code still implements the earlier reconciliation rule. This is an identified prerequisite, not completed work.

Time-operator/wire closure and the concrete implementation scope remain pending. This update records accepted decisions only; it does not claim Ticket 05 implementation or tests.


2026-09-30 transport prerequisite update: version-specific source selection and generation boundaries are implemented in the uncommitted workspace. See the transport correction sections of the projection contract and PROJECT.md. Ticket 05 scoring, time-operator closure and protected-time blocker union remain unimplemented; this prerequisite does not authorize starting them.

Transport prerequisite acceptance: [correction record](../transport-correction-acceptance.md), final backend 1973 passed / 10 skipped. Ticket 05 remains needs-info; no scoring was implemented.

## Specification closure — 2026-10-01

The user authorized specification closure, then accepted Q1 (protected intervals do
not add non-overlap units) and Q2 (dated start/containment/minimum-or-exact duration,
the initial at-least-one selector, subsequently corrected to single-visit default
with explicit repetition required for at-least-one matching). Dependencies 01/03
are resolved, and the transport prerequisite has committed acceptance; the earlier
uncommitted/pending statements above are historical.

The [contract](../requirement-schedule-contract.md) defines typed payloads, conservative
identity/count bounds, one-parent weighting, explicit protection scopes, independent
time/occupancy review, descriptive repetition and unresolved-denominator reporting.
It identifies missing executable validation in intake, incomplete/alternative traffic
claims and fixed-time subject coverage as implementation seams. No scorer was built.

Implementation scope proposed: requirement validator/scorer, shared time and occupancy
helpers, fixed-time subject participation in existing identity preparation, an offline
JSON CLI, focused tests, package/acceptance documentation and Standards/Spec review.
Opening, route verdicts/departure selection, totals/masks and Repair deltas are separate
tickets. Existing workspace changes are preserved; no Git or live-run approval follows.

Additional future acceptance checks:

- [ ] Exact start/whole-window/minimum-or-exact duration use zero grace and one matching
  occurrence for the whole conjunction; unsupported quantifiers remain UNKNOWN.
- [ ] Protected unions retain original checks, scopes and correspondence provenance;
  blockers do not inflate non-overlap denominators.
- [ ] Time/role/association uncertainty never becomes empty occupancy, zero duration or
  a denominator silently reduced to only known units.

## User cardinality correction — 2026-10-01

Unstated named visit counts are exact one for the trip, including fixed-time-only
requirements. Only explicit repeat permission/count meaning enables at-least-one time
matching; explicit exact/minimum/date quotas are not relaxed. The updated contract
requires source-backed repeat permission and same-subject selector/count consistency.
This supersedes the initial Q2 default and the older default minimum-one authoring
rule. Future acceptance must verify second confirmed/potential occurrences and both
selectors. Status remains specification-ready; implementation approval is pending.
