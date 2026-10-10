# Daily density scoring decisions and validation

2026-10-04, [Issue #52](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/52).
Status: Implemented, offline Validated and reviewed. The
[density contract](../../contracts/0005-quality-human-review.md#daily-density) owns
current deductions and review wire. This is engineering policy validation, not formal
benchmark calibration or a research conclusion.

## Why density became scored

The Seoul pilot gave V1–V3 equal five-dimensional auxiliary scores despite different
visit populations. The existing `<2`, `2..5`, `>5` categories were descriptive, including
zero and six-plus visits. The approved change retained `auxiliary_total` and introduced
`overall_total = max(0, auxiliary_total - mean_daily_penalty)`, weighting each requested
date equally. Final/paired wire version 2 distinguishes it from old reports.

Independent source-linked pace/count review supports ordinary, relaxed and rich profiles,
dated exceptions and explicit-count precedence. It does not copy planner interpretation
or invent hard quotas from subjective pacing. Nonmonotonic uncertainty remains bounded;
unavailable feasibility evidence cannot become an available score through a deduction.

## Numeric policy revisions

The initial proposed ordinary/rich one-visit deductions of 20/30 were strengthened before
implementation. The first implemented curves for counts 0..5 were ordinary
`100,40,0,0,50,80`, relaxed `100,20,0,10,30,50`, rich `100,60,0,0,30,70`;
all counts >=6 deducted 100. These are superseded historical values.

The final follow-up changed ordinary count 3 from 0 to 10 and relaxed counts 3/4/5
from 10/30/50 to 40/70/90; all other entries remained unchanged. The ordinary 2..3
uncertain population therefore has 0..10 bounds and an UNKNOWN exact deduction.
Explicit-count rules, source populations, mean subtraction, original auxiliary score
and wire shapes remained unchanged. The full active table is maintained in the contract.

## Preserved Seoul replay observations

The source input/results/evidence under `artifacts/seoul/` were retained unchanged.
Agent review quoted `Please keep the pace relaxed.`; the palace-once obligation was
not a daily total-count request. Native report CLIs ran offline twice with fixed times,
socket/DNS prohibited and byte-identical outputs. Original file SHA-256 checks passed.

| Projection | Daily primary counts | Auxiliary | Mean deduction | Overall |
| --- | --- | ---: | ---: | ---: |
| V0 final | 2,2,2,2 | unavailable | 0 | unavailable |
| V1 final | 2,1,1,1 | 100 | 15 | 85 |
| V2 final | 2,2,1,1 | 100 | 10 | 90 |
| V3 final | 2,2,2,2 | 100 | 0 | 100 |
| V3 draft | 2,2,2,1 | 100 | 5 | 95 |
| V3 final primary | 2,2,2,2 | 100 | 0 | 100 |

The paired overall delta is **+5**, auxiliary delta zero. V0 remains unavailable under
the pilot's original applicability uncertainty. Final-table replay preserved these
one/two-visit results; only synthetic 3/4/5 cases exercise the revised deductions.
Local evidence: `artifacts/seoul-density/` and `artifacts/seoul-density-final/`, containing
`replay.py`, `density-reviews.json`, `quality.json`, `pair.json`, `acceptance.json`.
These are historical identifiers, not fresh-clone dependencies.

## Validation checkpoints

Tests cover table rows, rest/six-plus explicit counts, dated overrides, mismatches,
large-count uncertainty without range expansion, missing/stale reviews, exact means,
clamping, paired deltas, read-only CLIs and downstream mechanism compatibility with
pair wire 1/2. The initial integration corrected downstream rejection of pair version 2.

| Revision | Observed gate | Scope |
| --- | --- | --- |
| Initial policy, `95048bf`; base `f09e4a1c0360ba2ef196bdfad03fd06d81f9af8b` | **2516 passed, 10 skipped**, 299.62 seconds | Backend; earlier report/CLI subset **81 passed** |
| Final table, `20e7eff`; base `e364111872cb05d0c9e5cc9a095274a5205f2a69` | **2524 passed, 10 skipped**, 266.78 seconds | Backend; density tests **21 passed**, focused scoring/workflow **31 passed** |

A synthetic three-visit report retains auxiliary 37.5, with overall ordinary 27.5,
relaxed 0 and rich 37.5; an identical V3 pair has zero delta. The changed ordinary and
relaxed tests failed with old values before correction. Gates overlap, not add together.
Ruff/format/diff checks passed for changed files; an untouched `schedule_time.py`
formatting difference was preserved. Both review axes found no code findings. Initial
review also identified a stale pair-wire-1 documentation sentence, corrected to wire 2
with historical compatibility retained.

## Publication and limits

[PR #54](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/54) delivered the
five-commit scope through `300ee039b3e2a2116a0b21f93eb09c9da2ade126` against
`4aa76a956f55822d39c2b61f2d3105e8b1b33932`, excluding later Issue #53 work.
[Independent release review](https://github.com/rplalala/Reliable-Trip-Plan-Agent/pull/54#issuecomment-5979830137)
had zero findings on both axes. Merge `69197cdc5a99c96ab94e15fa8b9313b11b1127c9`
closed #52. Existing exact-code validation was reused; hosted CI had no checks and
mypy/pyright were not configured.

Quote validation proves source linkage, not semantic correctness of pace/count review.
Counts are source occurrences, not unique venues. Human preference, mechanisms, unknown
facts and original live costs remain separate. One-request replay establishes no
version superiority or controlled Repair efficacy; original pilot artifacts were not
rewritten by this scoring change.
