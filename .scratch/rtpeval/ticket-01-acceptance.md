# Ticket 01 offline acceptance

Date: 2026-09-29.
Base revision: 364f91f05f01328266bfb00c5b75885242d93d7d.
Working tree: earlier specification-closure edits plus new independent evaluation package/tests; uncommitted. The user approved Ticket 01 implementation and offline acceptance only.
Status: Implemented and validated offline within stated limitations. Not benchmark/version frozen.

## Delivered behavior

- Immutable, source-linked batch inventory from a user-curated manifest and separate per-version files.
- Fatal integrity/linkage/wire errors return needs_material_correction with no partial cohort. Date/content uncertainty remains diagnostic; no live planning-date validation or workflow requalification.
- Independent activity roles, review replay and within-day candidate adjacency. No canonical ID truth claim.
- Structured Transfer and text-based transport claims coexist; confirmed duplicates share occupancy, segments are retained, contradictions remain alternatives, and missing arrivals are not synthesized.
- Allowlisted quality data excludes planner requirements, RAG origin, route verdicts and V3 findings. Optional V3 projections and unavailable usage are explicitly tracked.
- Read-only local CLI and Python API; package guide documents envelope vocabulary and review preparation.

## Verification sequence

1. Initial test collection failed due to an unclosed bracket in the new test file; corrected before execution. Ruff reported formatting/line-length issues and two zip strictness findings; formatting and explicit strict=False resolved them. An intermediate edit used the Windows default GBK reader and failed on UTF-8 source; explicit UTF-8 resolved that tooling issue.
2. Initial behavior suite passed 20 tests. Review added structural, numeric, source-quote, stale-review, day-boundary, role uncertainty and filesystem-boundary cases.
3. Code review found that a general negation filter would mistake 'not live verified' for mode negation. Restricted negation to mode statements, added regression coverage, and restricted automatic positional binding for rich endpoint prose.
4. Final evaluation suite: **38 passed, 1 skipped**. The skipped real symlink test requires host privileges unavailable here. Literal traversal and a simulated resolved-link escape test pass; native link/junction behavior is not claimed validated by that simulation.
5. Ruff check and format check pass; CLI --help succeeds. Document/link and diff checks are run at closeout. No shared application code changed, so the unrelated planner suite was not rerun.

Tests use synthetic local temporary artifacts, with network guards. An import-boundary check restricts this package to standard-library and relative imports. Finding-mutation testing compares semantic projections while permitting correct artifact-hash/source-ID changes. This is not a formal experiment or proof of future provider coverage.

## Remaining limits

- Rich/ambiguous natural-language roles/endpoints require independent review; no model-based classifier is implemented.
- Timezone resolution, canonical resolution, oracle acquisition, metric scoring, usage collection, renderer and Repair reporting belong to subsequent tickets.
- Intake checks RequirementSpec structure/provenance and basic referential integrity; full obligation operator semantics belong to Ticket 05.
- No actual benchmark package, live API/model/database call, native junction test, thesis analysis, Git commit or version freeze occurred.

## References

- [Implementation guide](../../backend/evaluation/README.md)
- [Ticket](issues/01-batch-intake-projection.md)
- [Contract](intake-projection-contract.md)
- [Tests](../../backend/tests/evaluation/test_intake.py)


## Authorized follow-up corrections - 2026-09-30

The later review found full-input provenance and overlapping-visit gaps in the earlier implementation. The user authorized correction; previous acceptance remains historical. Selected runs now require `rtpeval_provenance_1` with exact group/run/version/full-input/result association, using the existing file hash/path/schema reader. Its hash is retained in inventory. Overlapping/equal-start visits retain source records and candidate legs but produce explicit diagnostics and unresolved affected adjacency.

TDD sequence: all six missing/mismatched provenance cases initially failed, then passed after validation and explicit fixture sidecars were added. Existing evaluation suite then passed 84 tests with one skip. Both overlapping-time cases initially failed, then passed after projection correction. No planner validation or chronology repair was added. Final combined evaluation/capture suite: **113 passed, 1 skipped**; the skip remains native Windows symlink privileges. Ruff check/format check pass. Final review disposition is recorded in ticket-01-02-review.md. No live calls, benchmark/experiment, commit/push or freeze. Legacy synthetic/material deliveries missing provenance need an explicit producer sidecar; this is not an automatic attestation of actual execution.

Follow-up Spec review caught an interaction: the new unresolved adjacency also excluded explicitly reviewed transport endpoints. A public intake regression first failed with no associated claim; filtering was moved to automatic positional matching only. The regression then passed, preserving unique reviewed association alongside unresolved chronology. The final 113-test pass above includes this correction.
