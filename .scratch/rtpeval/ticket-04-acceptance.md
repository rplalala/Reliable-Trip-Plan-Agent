# Ticket 04 offline snapshot acceptance

Date: 2026-09-30. Base revision: `1eb441f` on `feature/evaluation`.
Working tree: Ticket 04 implementation/tests/contracts and documentation are uncommitted. Previously committed Tickets 01-03 are preserved; the only existing-test change adds asyncio to the standard-library import allowlist.
Status: Implemented and validated for the approved injected-transport/offline scope. Not live-ready Google integration, formal evaluation, benchmark freeze or version freeze.

## Delivered

- Two-stage request planning: independent Search/Details observations feed Ticket 03; source-checked adopted identities feed canonical details union and explicit route-context plans.
- Deduplicate identical request descriptors while retaining every original reference and candidate leg. Optional available V3 draft/final_primary is included when paired is requested; missing optional projections, unresolved identities and missing route contexts remain explicit.
- Route requests preserve direction, identities, coordinates/evidence hashes, mode, departure basis and routing options. Only necessary one-cell matrices are requested; Ticket 07 still owns departure/applicability choices.
- Acquisition uses an injected async transport, explicit send/attempt/time bounds, safe transport-failure categories and bounded retry. Raw response bytes, hashes, request/retrieval times and every failed attempt remain stored. The oracle ledger is separate from planner usage.
- Fresh directories only; manifest published last. Replay checks request coverage, plan/hash linkage, safe paths, response hashes, derived summaries, ledger and UTC time order. It does not acquire data or recompute scoring verdicts.
- Offline CLI prepares plans, replays snapshots and exports identity evidence. No live acquisition command/client, credential loading or database dependency is installed.

## Actual validation sequence

1. Implemented public seams one slice at a time. Initial plan/acquisition/bridge/union/CLI tests failed because the respective interfaces did not yet exist, then passed after each slice. Route-context test initially failed at the deliberately unsupported context boundary, then passed after explicit context validation/keying was implemented.
2. Retry regressions first failed for the absent typed-failure path; HTTP, timeout and transport retry/budget cases then passed. Permanent HTTP failures and malformed successful responses do not retry.
3. The first network guard also blocked Windows asyncio's local socket pair. The fixture was corrected to allow loopback socket construction while rejecting external socket connections. This was a test-harness issue, not a provider connection.
4. Corruption tests passed raw hash/path/coverage/summary cases but initially failed ledger and missing-attempt cases. Replay now recomputes ledger totals and validates unrequested-record states; all passed.
5. Parameter allowlisting regression initially failed because an extra authorization field could reach persistence. Operation-specific input fields and reference/operation linkage are now checked before directory creation/transport invocation. No credential value was real.
6. Initial combined evaluation run: 1 failed, 126 passed, 1 skipped. The failure was the existing import allowlist lacking asyncio. Added only that standard-library module, retaining the no-planner/no-network-client boundary.
7. Standards and Spec reviews both found the same P2: missing acquisition timestamps were accepted at replay and broke the identity bridge later. Four timestamp regressions (missing, naive, reversed, outside collection interval) failed first, then passed after UTC/time-order validation. Final reviewers report zero remaining actionable findings on their respective axes.
8. Further targeted coverage checks supplied-ID/name-only handoff, malformed optional location, stale identity source hashes, reverse legs, context distinctions, optional drafts, matrix precision/missing/duplicate elements and CLI error reporting. Final snapshot suite: **35 passed**.
9. Ruff initially found import ordering, line length and ambiguous short variables. Corrected imports/names and formatted files; final Ruff check/format check and compileall pass. No separate static typechecker is configured in pyproject.toml.
10. Final full backend suite: **1957 passed, 10 skipped in 83.84 seconds**. Nine database integration tests remain opt-in and were skipped; one native Windows symlink test lacks privileges. The interim evaluation/capture suite of 145 passed / one skip and reviewer targeted runs overlap this final result and must not be added as independent evidence. CLI help and git diff whitespace checks pass.

## Limits and next step

Evidence is synthetic and temporary. No actual Google/model/database call, formal case, benchmark, experiment, commit/push or freeze occurred. The transport contract is executable but does not serialize live Google requests; provider applicability and storage/retention settings require a separately authorized operational integration. Request timeout/send limits are development engineering defaults, not an approved live budget.

The declared independent coordinate/source context must be prepared and reviewed externally; hashes and source links establish consistency with supplied material, not factual authenticity. Planner-to-oracle lag is null because no reliable planner timestamps were supplied. Snapshot integrity is verified against its manifest and optional trusted plan; callers requiring external tamper evidence must retain a trusted manifest hash. A programming error or cancellation leaves an unpublished directory, not an automatically resumed snapshot. API/CLI successful replay does not imply complete evidence or a quality PASS.

Recommended next step: inspect Ticket 05's supported obligation/time-operator boundaries, or separately scope a live transport integration if explicitly desired. Ticket 06 can consume frozen raw opening evidence once its implementation is authorized. No dependent ticket starts automatically.
