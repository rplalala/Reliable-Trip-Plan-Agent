# Tickets 01 and 02 follow-up review

Date: 2026-09-30.
Base: `364f91f05f01328266bfb00c5b75885242d93d7d`.
Scope: existing uncommitted Ticket 01/02 code, shared adapter changes, contracts and offline tests. Ticket 03 was excluded. User requested review only; implementation and tests were not edited.

## Standards

Zero actionable findings. No explicit repository standard violation or concrete maintenance issue was identified in this review. Shared adapter instrumentation remains opt-in; prompts, budgets and planner decisions were not changed by the reviewed diff. This does not override the Spec findings below.

## Spec

1. **P1 - Missing selected-run provenance/full-input validation.** `backend/evaluation/intake.py:288`. Artifact contract requires each selected run's provenance reference and complete input hash linkage. Intake validates RequirementSpec-to-input and usage-to-result, but never reads run provenance. A synthetic fixture with valid-hash provenance files declaring wrong input hash, wrong run and wrong version is still accepted; omitted provenance is also accepted. Group membership and completion attestation do not validate the provenance that is actually supplied. Require and validate the selected-run full-input association without rerunning planners. The implementation README's optional-provenance wording does not establish an approved relaxation of this requirement.
2. **P2 - Overlapping/equal-time visits lack required ambiguity diagnostics.** `backend/evaluation/projection.py:176-205`. Contract says equal/overlapping times remain conflicts/ambiguities. Two visits at 09:00-10:00 and 09:30-11:30 are accepted with `adjacency_status=ordered_candidates` and a negative gap (10:00 to 09:30); no overlap diagnostic is emitted. Equal-start visits are likewise ordered using tie-breakers without recording the ambiguity. Preserve sources/candidate pairs but expose the conflict instead of claiming unambiguous chronology.
3. **P2 - Unknown Repair tokens become zero.** `backend/evaluation/usage_report.py:71-80`. Contract requires missing token observations to remain unavailable. An actual offline `capture_attempt` with one Repair SDK call returning no usage produces null whole-run/observed token totals, but `repair_token_observed_subtotal=0`. No Repair token value was observed. Emit null when none of the Repair events have known usage, retaining partial subtotal semantics when some are observed.
4. **P2 - Missing event collections are reported as zero.** `backend/evaluation/usage_report.py:20-40`. With available/default-adapter coverage but absent model/provider/cache arrays, the report defaults them to empty lists and emits zero calls/tokens/sends/cache hits. The contract requires missing observations to remain unavailable. Validate required collections before calculating complete totals.
5. **P2 - Duplicate cache events are counted twice.** `backend/evaluation/usage_report.py:21-24,40`. Two cache-hit rows with the same event ID yield cache_hits=2 because only model/provider collections are checked for duplicate IDs. The contract explicitly rejects duplicate event IDs rather than double weighting. Include cache event identities in validation.

## Verification

- Root reran `.venv/Scripts/python.exe -m pytest backend/tests/evaluation backend/tests/observability/test_usage_capture.py -q -rs`: **91 passed, 1 skipped**. Includes existing Ticket 03 tests; counts are not exclusive Ticket 01/02 coverage.
- Standards reviewer independently reran the capture suite: **13 passed**; these overlap with the above count.
- Additional synthetic temporary-artifact probes exercised real `load_batch` for provenance and chronology; a fixture SDK call inside real `capture_attempt` reproduced Repair missingness. Direct report probes demonstrated missing-array zero and duplicate cache counting. Probe outputs were inspected in-session, with no persistent raw logs.
- No correction or corrective retest was performed. Existing tests passing does not cover these counterexamples. Earlier acceptance records remain historical and their no-remaining-findings conclusions are qualified by this review.
- No real provider/model/database call, formal benchmark/experiment, commit/push or planner behavior change occurred. Existing workspace changes were preserved.

Final counts: Standards 0; Spec 5 (one P1, four P2). Recommended next step: correct these boundaries with offline regression tests before dependent evaluation work.


## Correction disposition - 2026-09-30

The user authorized all five fixes; they are now implemented and validated offline. Twenty-two regression cases cover the failure-before/fix-after sequence. Final evaluation/capture suite: **113 passed, 1 skipped** (existing Windows symlink privilege limit); Ruff check, format check and git diff whitespace check passed.

Standards follow-up: zero actionable findings. Spec follow-up initially found that overlap uncertainty also blocked independently reviewed transport endpoint binding. A failing public-intake regression was added, then corrected by restricting the adjacency filter to automatic positional matching. Final Spec review reports zero remaining findings, with an independent targeted rerun of nine provenance/overlap tests (overlapping coverage, not additional totals).

See ticket-01-acceptance.md and ticket-02-acceptance.md for the detailed sequence. Original findings above describe the pre-correction implementation and are no longer outstanding. No planner/capture adapter behavior changes, real services, formal benchmark/experiment, commit/push or freeze occurred. New provenance wire and conservative chronology/missingness rules are documented in the active contracts and package guide.
