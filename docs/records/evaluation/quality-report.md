# Quality Report

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="rtpeval-ticket-08-acceptance"></a>

<a id="rtpeval-ticket-08-acceptance--ticket-08-offline-quality-report-acceptance"></a>

## Ticket 08 offline quality report acceptance

Date: 2026-10-02, Australia/Sydney. Review fixed point:
`f1d6ecf77d653d9c09bf44d93798002885a1bd2e`, branch `feature/evaluation`.
Status: implementation, offline validation, dual review and tracker synchronization
complete; local closeout recorded without push or version freeze.

<a id="rtpeval-ticket-08-acceptance--authority-and-approved-scope"></a>

### Authority and approved scope

The user approved the concrete [preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20#issuecomment-5955702362) implementation and
local commits under the new [AGENTS](../../../AGENTS.md) commit-before-review workflow,
explicitly without push. [PROJECT](../../../PROJECT.md) owns current scope. GitHub
[Issue #20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20) owns task state;
[parent #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12) remains open.
The six inherited preflight documentation changes are directly related to this task.
No planner/scorer policy, provider integration, dependency, database/native supplement,
formal benchmark/inference, paired V3 total, later ticket or version freeze is included.

<a id="rtpeval-ticket-08-acceptance--implemented-behavior"></a>

### Implemented behavior

- `build_quality_report` composes the existing requirement/schedule, opening and route
  scorers with `paired=False`, validated identity records and one frozen evidence snapshot.
  The immutable result and local CLI export `rtpeval_quality_report_1`.
- Ordered requirements/grounding/non_overlap/opening/routes dimensions use known
  P/F/U counts, verified P/N, coverage, UNKNOWN and confirmed-violation rates. Exact
  count fractions are retained; unrounded `Fraction` values determine 0-100 scores and
  auxiliary means. Conditional compliance is diagnostic, never the score input.
- Parent obligations, logical commitments, visits and combined route legs retain one
  weight. Raw checks, partial-evidence outcomes, exact duration/magnitude/basis records,
  descriptive coverage/density/repetition and observed transfer burden remain visible.
- One mask and equal rational weights apply to each request's four final versions.
  All-four established zero applicability excludes jointly. Included single-version
  no-check N/A keeps null raw rates and contributes zero. Unresolved populations retain
  partial counts but null affected scores/contributions/totals, without redistribution.
  Empty masks yield null totals and an upstream reconciliation diagnostic.
- Identity summaries cannot supply metric counts. Grounding is derived from validated
  primary-visit occurrences; unresolved identity is UNKNOWN, not a fabricated FAIL.
  Declaration/content conflicts keep the existing role-review correction boundary.
- Key/hash joins require exactly the selected final run in every component. Invalid,
  stale or corrupt material yields empty groups; no smaller cohort is exported. Valid
  paired snapshots are explicitly unsupported scope. Missing provider observations
  within a valid snapshot retain their original UNKNOWN states.
- Source artifact bytes, canonical prepared/replay digests, independent evidence/review/
  audit/reference hashes, snapshot/plan and component-rule provenance are preserved.
  CLI exact preparation-file hashes are separate and covered by the content hash;
  only `generated_at` and `content_hash` are excluded. An explicit aware timestamp
  reproduces JSON. CLI uses UTC by default, emits null rather than nonfinite values,
  returns 0 for complete replay even with failures/unavailable totals, otherwise 2.
- Resource/human/mechanism analyses remain `not_integrated`; usage-envelope and optional
  V3 projection availability are metadata, not quality penalties or paired deltas.
  Multiple requests retain separate masks/totals with no pooled comparison or ranking.

<a id="rtpeval-ticket-08-acceptance--actual-development-sequence"></a>

### Actual development sequence

1. The first public report test failed at collection because `quality_report.py` did not
   exist. Minimal implementation then exposed a wrongly adapted `measures` key; it was
   corrected to the producer's actual `schedule_measures` field.
2. Initial fixture expectations were reconciled with existing occupancy: a logical
   journey is a distinct commitment, and unknown journey occupancy can prevent confirmed
   conflict-free visits. The scorer was preserved; expectations were corrected.
3. The first CLI test likewise failed on the missing CLI module, then passed after its
   implementation. It rejects socket construction, compares source bytes before/after,
   repeats exact JSON and checks exact-file/content hashing.
4. Additional public-boundary tests identified contradictory synthetic exact quotas and
   stale identity-summary/snapshot linkage. Fixtures now use compatible minimum quotas
   and reacquire/relink evidence before comparing numeric results. Raw snapshot bytes
   are reused through injected synthetic transport; route summaries are not raw payloads.
   Actual producer burden/repetition field names replaced incorrect test assumptions.
5. A real mixed FAIL/UNKNOWN regression exposed aggregation's reversed state priority.
   Confirmed FAIL now overrides outcome uncertainty for an established denominator;
   counts and UNKNOWN remain distinct. No existing scorer behavior was changed.
6. Dedicated report/CLI validation: **39 passed in 9.01s**, repository Python 3.12.14,
   no cacheprovider, local `.scratch/ticket08-tests`. This includes exact thirds, unknown
   populations, asymmetric totals, empty/common masks, partial decisive opening failures,
   null-duration no-route failures, multiple requests, optional resource absence and
   findings-only changes after proper relinking. Stale reuse still fails.
7. Initial Ruff found import/formatting/UTC-alias issues and long lines; all were corrected.
   Final backend Ruff, four-file formatting check, compilation and CLI help passed.
8. The first full offline backend gate returned **1 failed, 2272 passed, 10 skipped
   in 182.44s**. `test_no_planner_import_or_network_on_intake` has a package-wide
   explicit import allowlist that lacked the newly used standard-library `fractions`.
   Add only that module to the allowlist, preserving planner/network prohibitions.
   This is a direct test compatibility update for the approved exact-rational seam,
   not a new dependency or an unrelated production change. Retest results follow below.
9. Focused intake/report/CLI retest: **95 passed, 1 skipped in 12.79s**. The skip is
   the existing host symlink-privilege case. Backend Ruff passed; the related existing
   test diff is exactly one standard-library allowlist addition.
10. Full unfiltered offline backend retest: **2273 passed, 10 skipped in 191.66s**,
    **zero deselections**. This is the final pre-review executable gate. Nine database
    opt-ins and one host symlink case skipped; no supplement was run. Logs are preserved
    in the ignored research archive `thesis_notes/evaluation/ticket-08-validation/`.

All evidence is synthetic development verification, not a formal benchmark or actual
provider availability study. `TRIPWORLD_TEST_DATABASE=0`; no live/native supplement
is inferred from previous Ticket 06 approvals.

<a id="rtpeval-ticket-08-acceptance--review-commits-and-tracker-boundary"></a>

### Review, commits and tracker boundary

Implementation/direct tests were committed before the Standards/Spec review:
`5625f81` — `feat: compose offline final quality reports and verified scores` (five files,
including the directly related fractions allowlist entry). Corrections must remain
separate commits; no amend/squash or push.

<a id="rtpeval-ticket-08-acceptance--standards"></a>

#### Standards

**0 documented-standard violations; 0 actionable code smells.** The committed diff
follows offline-only composition, English content, immutable results, no new dependency/
planner change, and the approved public preparation interface. Cross-component data
access is the explicit aggregate responsibility rather than a reason for added abstractions.
The fractions allowlist addition preserves the no-network/planner import guard.

<a id="rtpeval-ticket-08-acceptance--spec"></a>

#### Spec

**0 findings.** The reviewer verified five-dimensional P/F/U/exact arithmetic, common
masks, true N/A zero contributions, unresolved denominators/null totals, final-only
scope, optional-track boundaries, strict source/identity/snapshot linkage, empty groups
for material failure, retained partial FAIL/completeness/magnitudes, CLI file-byte hashing
and findings-only numeric invariance after proper replay.

Both axes inspected `git diff f1d6ecf77d653d9c09bf44d93798002885a1bd2e...5625f81`
and the complete task commit list in independent parallel review agents, as required
by the code-review skill. Neither modified files or repeated the full gate. There are
no review findings to correct, so no artificial fix commit is created. Final documentation
is a separate coherent commit. Backend Ruff/compile/format/CLI and English/local-link
checks passed: **195 local targets across nine English documents**. Final document
scope also includes the verified tracker synchronization record.

An attempted GitHub Issue progress update was rejected by automatic approval review:
the reviewer did not recognize local implementation approval as authority to publish
local commit/path/status/test information externally. That first attempt did not mutate
an Issue. The follow-up verified the exact origin remote against the configured tracker
and the approved preflight's related tracker-record scope. A reduced acceptance summary
omitted newly published local hashes, internal paths and detailed test counts. The same
GitHub connector then passed automatic approval; no alternate channel or workaround was
used. Issue #20 is closed with reason completed, its five live acceptance items checked;
parent #12 marks Ticket 08 complete and stays open. Both full bodies were read back with
exact equality to their submitted updates. Labels/assignments/dependencies/imported
history remain unchanged. [Tracker record](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20#issuecomment-5956220975) preserves the
actual publication content/boundary. Local detailed records/commits remain unpublished.

<a id="rtpeval-ticket-08-acceptance--local-git-closeout"></a>

#### Local Git closeout

Implementation/direct tests: 5625f81, five files, before review. Final documentation:
`docs: record quality report validation and local closeout`, nine coherent current
contract/preflight/acceptance/tracker-record/project/package/index files, including the
six inherited preflight documents. No review correction commits were needed. No ignored
archives, credentials, raw provider/model payloads, runtime logs or generated pytest
artifacts are staged. Full gate output is preserved in the ignored research archive
before cleaning the task's generated pytest roots/logs. The final documentation commit
identity and clean Git status are reported in the chat; this document cannot self-reference
its own eventual commit hash. All task commits remain local/unpublished, without push.

<a id="rtpeval-ticket-08-acceptance--limits-and-next-boundary"></a>

### Limits and next boundary

No paired V3 totals, human ranking UI, resource comparison, mechanism audit, formal
cross-request analysis, real provider/model/database call or version freeze. V0-V3
entry points and planner behavior are unchanged. Ticket 09 requires separate approval.
Independent semantic/source/evidence reviews remain trust boundaries; numerical
verified success does not prove unconditional real-world itinerary usefulness.
