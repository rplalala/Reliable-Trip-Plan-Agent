# Requirement and schedule evaluation development

Ticket [05 / #17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17),
2026-10-02. Status: Implemented and offline Validated. Baseline:
`fc9996803b05b9b444583f0985274bee75c4ed0f`. Current obligation, time and occupancy
rules belong to the [requirement/schedule contract](../../contracts/0003-requirement-schedule.md).

<a id="rtpeval-ticket-05-acceptance"></a>

## Obligation meaning and completeness

The delivery introduced source-linked requirement/schedule reports and an offline CLI.
Named counts originally used adopted canonical identity; later physical-association
matching has a separate [correction record](intake-identity-usage.md#requirement-physical-association-correction-2026-10-09).

Exact/minimum/date/distinct-date counts and single/multiple fixed-time selectors retain
all conditions within one obligation. Unsupported or unclear meaning remains visible.
Development defects included invalid executable fields escaping correction, empty
unclassified content becoming N/A, and unknown unresolved kinds becoming invented
weighted units. Corrections preserve unresolved completeness and avoid counting linked
annotations/soft preferences twice. Contradictory quotas, dated capacity and incompatible
time/exclusion conditions produce whole-batch material correction.

Spec review found that `start_at + duration` without a window skipped local-day capacity
validation. The correction covers duration-only/day boundaries using independent zones.
A direct-helper identity/role finding was withdrawn because public preflight made it
unreachable; it is not retained as a real product defect.

## Occupancy and uncertainty

The implementation separates V0 Activities from V1–V3 Transfers, logical commitments,
segmented/alternative journeys and protected boundaries. Triple-overlap tests distinguish
pair sums from conflict union; 23/25-hour DST protection days are not forced to 24 hours.
Contradictory protection-placeholder links require material correction.

A second Spec finding showed unbound claims discarding available independent times for
conflict exclusion. Correction retains known disjoint candidate time without establishing
endpoint association. Missing clocks preserve consistent structural counts; unsupported
time remains UNKNOWN. Occupancy review cannot select transport alternatives or adjudicate
endpoints. Whole-request instants may remain known when daily attribution is unavailable.

## Validation and provenance

Public tests cover repeated sources/potential matches, same-visit time conjunctions,
precise boundaries, missing zones, duplicates/segments, mode-only uncertainty, missing
claims and source-linked fixed generic/protection correspondence. CLI checks prohibit
socket construction, repeat exact JSON and verify unchanged source bytes. Relinked
planner findings and Nearby entries do not change independent numeric results.

| Checkpoint | Observed result | Scope |
| --- | --- | --- |
| Initial evaluator regression | **1 failed, 231 passed, 1 skipped** | Import allowlist lacked standard-library `zoneinfo` |
| Guard correction | **232 passed, 1 skipped** | Added only `zoneinfo`; planner/external-client boundary retained |
| Spec correction recheck | **74 passed** | Capacity and independent candidate-time corrections |
| Final offline backend | **2063 passed, 10 skipped**, 121.06 seconds | `TRIPWORLD_TEST_DATABASE=0`; nine database opt-ins and one Windows symlink case skipped |
| Later local closeout | **234 passed, 1 skipped**, 13.04 seconds | Evaluator; separate identity check **41 passed**, 2.07 seconds |

Standards' duplicated canonical-digest finding was resolved through shared
`records.canonical_digest`. Final Standards/Spec had no unresolved actionable findings.
Ruff, formatting, compilation, CLI help, 190 local document targets and diff checks passed.
No static type checker was configured or installed. Checkpoints overlap, not add together.
Review preceded commits because that original task prohibited them; subsequent approval
allowed one capability commit and [Issue closeout](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17#issuecomment-5935469356).

## Limits

Evidence is synthetic supplied material, not Google/model/database observations or a
formal experiment. Hashes establish consistency, not factual authenticity. Installed
IANA data is part of reproducibility; precision beyond six fractional digits and
unsupported overnight/vague/ordinal/all-occurrence semantics remain unresolved.
Requirement/non-overlap PASS certifies neither opening/access nor route feasibility.
This stage supplied no five-dimension total, blind package or Repair comparison.
