# Final quality report development

Ticket [08 / #20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20),
2026-10-02. Status: Implemented and offline Validated. The
[quality contract](../../contracts/0005-quality-human-review.md#scores) owns current
scores and report wire; this record concerns the original final-only report version 1.

<a id="rtpeval-ticket-08-acceptance"></a>

## Composition and accounting decisions

The approved [preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20#issuecomment-5955702362)
composed independent requirement/schedule, opening and route scorers without changing
individual scorer policies. The immutable report/CLI used exact rational P/N scores,
request-wide common masks, true N/A and unresolved-population null totals, with strict
source/identity/snapshot joins. Resource, human and mechanism tracks remained separate;
paired snapshots were rejected rather than scored as final-only.

A mixed FAIL/UNKNOWN regression exposed reversed aggregate state priority. Correction
makes established FAIL decisive while preserving separate counts and UNKNOWN evidence.
Fixture checks also clarified that journeys are distinct commitments, uncertain journey
occupancy can prevent confirmed non-overlap, and stale evidence must be relinked before
numeric comparisons. These were fixture/material corrections, not changes to scorers.

## Validation and review

| Checkpoint | Result | Meaning |
| --- | --- | --- |
| Dedicated report/CLI | **39 passed**, 9.01 seconds | Exact thirds, asymmetric masks/totals, partial decisive failures, null no-route duration, optional absence, immutable/repeatable CLI and findings-only numeric invariance after relinking |
| Initial full backend | **1 failed, 2272 passed, 10 skipped**, 182.44 seconds | Static evaluator import allowlist lacked the newly used standard-library `fractions` |
| Focused guard/report correction | **95 passed, 1 skipped**, 12.79 seconds | Only `fractions` added; no-planner/network prohibition retained |
| Final pre-review full backend | **2273 passed, 10 skipped**, 191.66 seconds; zero deselections | Nine database opt-ins and one host symlink case skipped |

Ruff, four-file formatting, compilation and CLI help passed. Test logs are local under
`thesis_notes/evaluation/ticket-08-validation/`; Python was 3.12.14 and the dedicated
fixtures were under `.scratch/ticket08-tests`. These gates overlap and are not additive.

Review base: `f1d6ecf77d653d9c09bf44d93798002885a1bd2e`.
Implementation/direct tests: `5625f81`. Independent Standards and Spec reviews had
no actionable findings; no code correction was needed. Spec checked common-mask
accounting, source joins, material-failure atomicity, retained partial magnitudes and
numeric invariance. Subsequent [tracker acceptance](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20#issuecomment-5956220975)
closed #20 and marked Ticket 08 complete in then-open parent #12.

## Limits

All checks were synthetic/offline with `TRIPWORLD_TEST_DATABASE=0`. No live/database
supplement or formal benchmark was performed. This checkpoint did not implement paired
V3 totals or a human renderer. Source/review hashes establish linkage, not authenticity;
verified compliance does not establish unconditional real-world usefulness. Later
[paired reporting](v3-pair-report.md) and [density scoring](2026-10-04-daily-density.md)
retain their own policy and validation history.
