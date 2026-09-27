# Application-owned semantic identities

Approved 2026-09-27: implement option B from correction-options-comparison.md using TDD,
offline validation and independent Standards/Spec review. No live, commits, quantity Repair
changes or budget increases. Existing request-wide limits and one correction per batch stay.

## Contract

- The model-facing input/output uses batch-local candidate_ref pNN and source_ref/evidence
  refs eNN. The application owns the exact bijective mapping to canonical place IDs and
  sources. Keep candidate descriptive facts and requirement semantics unchanged.
- Use a separate wire DTO; keep downstream canonical schemas and V0 behavior unchanged.
  Do not resolve rows by response position. Reject missing, duplicate or unknown candidate
  references, unknown evidence and known evidence belonging to another candidate.
- Keep evidence selection explicit. A supported match without evidence is invalid; assigning
  a valid source does not prove semantic support. No automatic evidence filling, fuzzy ID
  repair, silent claim removal or partial invalid-batch admission.
- Keep the same mapping through correction. Named bindings must retain exact ownership,
  including when their canonical candidate is outside the batch. Short refs reused by later
  batches must not leak authorization or cached results between canonical candidates.
- Validate the complete wire result, resolve exact identities, then validate canonical
  domain semantics before atomically caching. Preserve strict exception authorization,
  role ownership, requirement checks and negative/unresolved judgments.
- Cache keys include canonical inputs and projection/prompt version. Token accounting uses
  actual wire input plus the actual wire schema/prompt/framing and corrective feedback.
- Preserve opt-in bounded capture, known-secret redaction and linked attempts. Record wire
  input/output, canonical mapping/hash/version and accepted resolved output or error. Keep
  canonical maps in local captures, not in the prompt sent to the model.

## Verification seams

Approved service assess/prepare and mocked external SDK/HTTP boundaries. Cover reordered
roundtrip, invalid ownership/coverage, supported evidence, named/semantic exception rules,
correction stability, batch isolation/cache invalidation, global budgets/deadlines/input
sizing, capture linkage/caps and shared V1-V3 integration with V0 regression. Run full
backend regression and independent code review. No offline test proves model accuracy.

## Implementation checkpoint

The first service-boundary test failed because canonical-long-A appeared in the model input.
After adding the projection and wire DTO it passed with reversed model row order and exact
canonical source restoration. Existing reference/exception/SDK tests were migrated to wire
values while keeping canonical public-result assertions. Migration exposed two fixture
assumptions: Candidate Details classification depended on model-visible canonical IDs, and
the input-ceiling test counted canonical rather than transmitted input. These tests now use
supplied display names and actual projected input, respectively. Neither fix relaxes the
production contract.

The first full backend run found 9 failures (1712 passed, 9 skipped): eight SDK harness
cases still constructed old place_id wire fixtures, and one offline replay case computed
the old cache key. Updated the mock transport field and centralized semantic_cache_key
for both service and FrozenSemantics replay. No quantity Repair algorithm was changed.
The affected SDK/replay suites then passed 41 tests. The final full backend run passed
1721 tests with 9 skipped in 72.41 seconds. Scoped Ruff and formatting checks passed across
13 changed Python files. No separate static typechecker is configured in pyproject.toml.

Independent Standards and Spec reviews found zero actionable issues, including a second
review of the SDK/replay compatibility fixes. All tests were offline; wire mapping tests
establish exact application behavior, not model semantic accuracy or live reliability.
No live calls, commits, quantity Repair policy changes or version freezes occurred.

## Subsequent authorized live checkpoint

The user separately approved three cases under short-reference-live-plan.md. Sydney V1,
Sydney V3 and Melbourne V1 all exited 0 and returned 5/5, 5/5 and 8/8 days. Four semantic
batches were first-call accepted; capture audits confirmed mapping hashes, unique complete
wire coverage, source ownership and exact canonical restoration. Iteration accepts the
wire integration for these cases. No correction was exercised; neither correction efficacy
nor a measured general reliability improvement is established.

Sydney V3 completed one authorized coverage Repair, while other UNKNOWN findings remain.
All 38 activity costs were null; V1 daily target gaps and food-preference questions require
separate Spec triage. Exact V3 aggregate API counters remain unaudited because run.json was
truncated: original_bytes=4908309 versus configured max_payload_bytes=1000000, not the JSON
wrapper's file length. Existing events and dedicated captures may support offline recovery.
The next recommended task is that offline audit, not more live attempts or quantity Repair.
See logs/semantic_short_reference_revalidation_20260927/report.md. No new code or commit.
