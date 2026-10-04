# Daily density scoring development acceptance — 2026-10-04

Status: Implemented, offline validated and reviewed. This is an engineering
acceptance record, not a formal benchmark, version freeze or thesis conclusion.

## Current approved table — Issue #52

The current authority is the final table in
[Issue #52](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/52) and the
[density contract](../../contracts/0005-quality-human-review.md#daily-density).
`rtpeval_daily_density_2` supersedes the initial numeric policy recorded below.

| Primary POI count | Ordinary | Relaxed | Rich |
| --- | ---: | ---: | ---: |
| 0 | 100 | 100 | 100 |
| 1 | 40 | 20 | 60 |
| 2 | 0 | 0 | 0 |
| 3 | 10 | 40 | 0 |
| 4 | 50 | 70 | 30 |
| 5 | 80 | 90 | 70 |
| 6 or more | 100 | 100 | 100 |

The final-table follow-up started from clean revision
`e364111872cb05d0c9e5cc9a095274a5205f2a69`. Its public scoring and report seams
use this table only. Explicit-count policy, source-occurrence population, mean
deduction, original auxiliary score, wire shapes and uncertainty rules are retained.
The ordinary 2..3 count interval now has cost bounds 0..10 and UNKNOWN exact deduction.
Issue #52 is associated through current contracts, PROJECT.md, commit references and
this acceptance owner. Its GitHub specification is self-contained because local code
and updated documents have not been published.

### Final-table follow-up validation

The public ordinary three-visit test first failed with actual cost 0 versus expected
10. After that change passed, the relaxed three-visit test failed with actual cost 10
versus expected 40; updating its three/four/five costs then passed the 21 existing
density tests. Additional public tests verify four/five cross-pace ordering, exact
mixed 3/4/5-day means, the revised ordinary 2..3 UNKNOWN interval, and current profile
propagation to final and paired reports. The focused scoring/workflow suite passed
31 tests. In the synthetic three-visit report case, the original auxiliary score is
37.5 for each pace, while overall scores are ordinary 27.5, relaxed 0 and rich 37.5;
the identical V3 pair has zero adjusted delta. These are implementation fixtures.

Fresh offline outputs are retained separately in ignored
`artifacts/seoul-density-final/` (`replay.py`, `density-reviews.json`, `quality.json`,
`pair.json`, `acceptance.json`). Native CLIs replayed twice with socket/DNS access
prohibited and identical output bytes. Original Seoul source-file SHA-256 checks
passed. Scores remain V1 85, V2 90, V3 100 and V3 draft/final 95→100; V0 remains
unavailable. This one/two-visit population validates regression only, while synthetic
three/four/five-visit cases validate the changed deductions.

The full backend suite passed **2524 tests, 10 skipped** in 266.78 seconds, with
external connections blocked by existing fixtures. Ruff lint/format checks for all
three changed Python files and diff whitespace checks passed. The implementation and
direct tests were committed together as `20e7eff` (`fix: apply final approved density
penalties (#52)`) before code review. The final-table review uses fixed point
`e364111872cb05d0c9e5cc9a095274a5205f2a69`; documentation/acceptance changes remain
uncommitted during that review. Two parallel code-review agents reported **Standards:
0 findings; Spec: 0 findings** against the committed diff and current Issue #52 body.
No code correction was required. Current contracts, usage guidance, project status and
this acceptance record are committed as a final documentation group after review.
Issue #52 records the accepted local implementation; code publication still needs
separate authorization. The next section is superseded implementation history, not
another current table.

## Initial implementation history (superseded numeric policy)

Starting/review revision: `f09e4a1c0360ba2ef196bdfad03fd06d81f9af8b`.
Implementation commit: `95048bf` (`feat: score reviewed daily itinerary density`).
The starting tree was clean. The implementation and directly related tests were
committed before the two-axis review; core contract, package guide, PROJECT.md and
this acceptance record were uncommitted during review. Raw local evidence is ignored
and is not committed. No push, branch change, provider call or planner modification was
part of this task.

## User request and decision sequence

The original Seoul pilot produced equal 100-point V1-V3 five-dimensional auxiliary
scores despite different daily visit populations. Inspection established that the
existing `<2`, `2..5`, `>5` density categories were descriptive and contributed no
penalty, including zero or more than five visits.

The user requested penalties based on ordinary, relaxed and rich pace, explicit
daily-count precedence and progressively greater busyness costs. The initial proposed
ordinary/rich one-visit deductions were 20/30; the user requested stronger deductions,
retaining relaxed one-visit cost 20, making six or more visits cost 100 and adjusting
the rest of the curve. The initial, now superseded ordinary curve for counts 0..5 was
`100,40,0,0,50,80`; relaxed is `100,20,0,10,30,50`; rich is
`100,60,0,0,30,70`; every count >=6 costs 100. The
[current contract](../../contracts/0005-quality-human-review.md#daily-density) owns the
numeric policy and preparation schema.

The approved formula preserves the original five-dimensional score and subtracts the
equal-weight mean of requested-date deductions, clamping the result at zero. This
implementation adds `overall_total` and preserves `auxiliary_total`, with report schema
2 to distinguish historical output. V3 stages share one reviewed input policy and
export both original and adjusted deltas. Matching explicit daily counts are exempt;
confirmed mismatches receive a labelled 100-point daily count deduction. These are
daily-policy outcomes, not synthetic named-place requirement checks.

Independent pace/count interpretation is represented by quoted original-input review
with batch/revision/input linkage, reviewer/time/origin/rationale and dated overrides.
There is no planner interpretation or additional model call. Missing review of nonempty
preferences is unresolved; a no-preference request defaults to ordinary. Uncertain
counts retain nonmonotonic deduction bounds. UNKNOWN is not silently zero or an
assumed count. Source-distinct primary occurrences are retained; same-venue repetition
remains separately descriptive rather than silently changing the population.

## Implementation and validation sequence

Public test seams: density policy/scoring, final quality report, V3 pair report,
report CLIs and downstream independent mechanism preparation.

1. The initial density test failed because the module was absent. The scorer then
   passed the worked ordinary 1/4/5 example, including exact mean `170/3`.
2. Final and paired report tests failed on unsupported `density_reviews` arguments;
   integrating the scorer and adjusted totals made them pass. A synthetic same-score
   V3 one-to-two-visit repair changes the adjusted score by 20 points.
3. The quality CLI test failed on an unrecognized review flag. Both CLIs gained the
   flag, exact review-file hashing and canonical preparation hashing; the targeted
   report/CLI suite passed 81 tests at that checkpoint.
4. Downstream integration rejected the new pair schema. Mechanism preparation now
   accepts pair report versions 1 and 2 with the existing exact source/hash checks.
   An initial read-only test captured files before its argument helper wrote fixture
   preparation; moving capture after preparation corrected the test, without changing
   production replay. Both workflow tests then passed.
5. Windows denied access to the default pytest temporary/cache locations. Tests were
   rerun using unique ignored `artifacts/density-tests-*` base directories with the
   cache provider disabled. No unrelated file permissions or implementation changed.
6. The full backend suite passed **2516 tests, 10 skipped** in 299.62 seconds before
   the implementation commit. External connections are blocked by existing fixtures.
   Ruff lint passed for evaluator source/tests; format checks passed for all 11 changed
   Python files; `git diff --check` passed. A broader format check reported one
   pre-existing formatting difference in untouched `schedule_time.py`; it was preserved.

The tests cover every pace/count table row, explicit counts including rest and six-plus
days, date-specific overrides, mismatches, million-count bounds without range expansion,
nonmonotonic uncertainty, missing reviews, stale/foreign material, provenance, adjusted
score clamping, paired deltas and read-only replay. The test fixture's semantic review
is synthetic; the existing network safeguard prevents real provider use.

## Preserved Seoul evidence: offline replay observations

Local evidence identifiers (historical paths, not fresh-clone dependencies):
`artifacts/seoul-density/replay.py`, `density-reviews.json`, `quality.json`, `pair.json`
and `acceptance.json`. Input/result/evidence sources remain the original ignored
`artifacts/seoul/` files. The review quotes `Please keep the pace relaxed.` from
original Input, with `review_origin=agent`; the palace-once request is not a daily
total-count request.

The actual native report CLIs were replayed offline twice with frozen timestamps;
outputs were byte-identical. Socket connect, connection creation and DNS resolution
were prohibited. SHA-256 checks across every original Seoul file confirmed no mutation.
New output paths preserve the original pilot report, packet and completion audit.

| Projection | Known daily primary counts | Original auxiliary score | Mean deduction | Overall score |
| --- | --- | ---: | ---: | ---: |
| V0 final | 2,2,2,2 | unavailable | 0 | unavailable |
| V1 final | 2,1,1,1 | 100 | 15 | 85 |
| V2 final | 2,2,1,1 | 100 | 10 | 90 |
| V3 final | 2,2,2,2 | 100 | 0 | 100 |
| V3 draft | 2,2,2,1 | 100 | 5 | 95 |
| V3 final primary | 2,2,2,2 | 100 | 0 | 100 |

Observed paired adjusted delta is **+5**; original auxiliary delta remains zero.
V0 still has unresolved source/evidence applicability from the original pilot; no
density rule manufactures a usable total. This shows the requested scoring mechanism
on one existing request, not general version superiority or controlled Repair efficacy.

## Review and remaining boundaries

Two parallel code-review agents reviewed the committed implementation against the
starting revision and original user request. Standards reported zero findings; Spec
reported zero code findings and one pending-document inconsistency: a later contract
paragraph still named pair report wire 1. The final documentation now names wire 2 and
retains wire 1 as historical mechanism-input compatibility. No code correction commit
was required. Final documentation is committed separately after review, preserving the
original implementation commit. Final documentation diff checks passed; the reviewers
did not repeat the full test suite.

Independent semantic review is still necessary for free-text pace/count requests;
quote validation checks provenance, not the correctness of a reviewer's meaning.
Counts are source occurrences, not unique canonical venues. Other quality metrics,
human preference rankings, mechanism observations, unknown evidence and original live
costs remain separate. The numeric deductions are user-directed engineering policy;
no formal benchmark calibration or final research conclusion was performed.
