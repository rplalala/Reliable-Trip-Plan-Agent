# Ticket 03 offline implementation and acceptance

Date: 2026-09-29.
Base revision: 364f91f05f01328266bfb00c5b75885242d93d7d.
Working tree: Tickets 01/02 and prior specification changes remain uncommitted; Ticket 03 adds only independent evaluation files, one Ticket 01 import-boundary test allowlist entry, and related documentation. No commit or push.
Status: Implemented and validated offline within the limits below. Not a formal benchmark, live evidence run or version freeze.

## Delivered behavior

- Read accepted Ticket 01 visit/role/source projections and independently reviewed named requirement subjects without importing planner judgments.
- Apply the user-approved strict supplied-ID details and no-ID name-search association paths, with explicit city/address and observable competition checks. Provider rank and mere ID retrieval do not establish a match.
- Queue aliases, branches, wrong-city/malformed/missing evidence, ID/name conflicts and potential REQUIRED/EXCLUDED matches for factual adjudication. Keep unresolved reasons and avoid calling missing candidates hallucinations.
- Require a versioned, predeclared audit seed/count. Select strict automatic proposals deterministically by a semantic key; sampled references remain pending until reviewed. The queue hides version labels.
- Replay consecutive versioned review decisions bound to source/evidence hashes. A reviewed named venue can resolve for downstream identity while a wrong supplied ID remains an explicit conflict.
- Report each final and available V3 optional projection's applicable/resolved/unresolved visit counts, grounding fraction, claimed-ID consistency and unresolved-role count. No obligation/opening/route/auxiliary total is produced.
- Expose a Python API and read-only local CLI for offline replay. Input evidence/reviews remain separate files; result artifacts are never rewritten.

## Verification sequence

1. Initial identity suite found two test-fixture mistakes: the altered V1 result had not been saved back to the synthetic batch, making the supposed supplied ID absent. The fixture writer was corrected; no production identity rule changed for that failure.
2. Initial Ruff findings were import-fixture naming and formatting issues. The test fixture was shared through the existing pytest module plugin, and code was formatted.
3. The first combined evaluation suite found one failure in Ticket 01's standard-library import allowlist after Ticket 03 introduced `unicodedata`. The allowlist was updated; its network/import boundary was not relaxed.
4. Review tightened branch handling: supplied-ID details with only name/city and no specific output location now require an independent full-page name-search competition check. Added a direct details/branch fixture and retained the specific-address path.
5. Final offline evaluation suite: **58 passed, 1 skipped**. The skip is the existing Ticket 01 native Windows symlink creation test; host privileges prevent creating that link. Its traversal/resolved-path alternatives remain tested. Ruff check and format check pass on the evaluation package/tests; identity CLI help and fixture-driven no-network replay pass. `git diff --check` reports no whitespace errors.

The tests use synthetic files and observations only. They include name-only and supplied-ID acceptance, alias, branch, wrong city, malformed response, provider failure, wrong ID/right name, closed business, distinct colocated IDs, high-impact subjects, review revision/stale hash, audit determinism, V3-finding mutation and network blocking. The V3-only internal-finding file change alters source hashes as expected but leaves semantic audit keys and grounding summaries unchanged.

## Review and limitations

Local Standards/Spec review checked source isolation, same V0-V3 policy, strict association, separate claimed-ID conflict, UNKNOWN propagation, pending audit behavior, review replay and no planner/network imports. No remaining finding required a code change after the final suite.

The evidence envelope is a Ticket 04 handoff; no acquisition client, provider budget, retry policy, cache or raw Google snapshot was implemented. Declaring an independent source in a fixture is not proof of real acquisition. A full-page response cannot prove global name uniqueness because the current adapter has no pagination/alias guarantee. Strict rules can leave real places unresolved. The module can replay a persisted reviewer JSON file but does not provide a reviewer UI or verify human factual accuracy. Benchmark preparation must prove the audit plan was frozen before result inspection. Formal cases, live services, scoring downstream of identity and V0-V3 behavior changes are outside this acceptance.

## References

- [Implementation contract](identity-implementation-contract.md)
- [Ticket](issues/03-identity-adjudication.md)
- [Package guide](../../backend/evaluation/README.md)
- [Implementation](../../backend/evaluation/identity.py)
- [Offline tests](../../backend/tests/evaluation/test_identity.py)


## Follow-up corrections and revalidation — 2026-09-30

Status: The four findings in [follow-up review](ticket-03-review.md) are corrected and validated offline. This supersedes the review's corrections-pending state while preserving both earlier records. Base remains `364f91f05f01328266bfb00c5b75885242d93d7d`; all work is uncommitted.

- Generic country/admin/postcode matches no longer activate the details-only branch shortcut. Only a matching recognized numbered street component can do so; unsupported forms need competition search or review.
- Search/details candidates with matching IDs but contradictory normalized names or full formatted addresses enter review.
- Separate title claims must equal the name or `Visit <name>` to pass automatically. Other prose enters adjudication rather than being interpreted as consistent. Original title now participates in the semantic audit key.
- Dictionary/list claimed IDs no longer raise during high-impact matching. The affected reference remains unresolved while unrelated valid records are reported normally.

Validation sequence used the public intake/resolver path, one defect at a time. Generic-location regressions initially failed in all three cases, then passed after correction (including the existing specific-street positive case). Search/details regressions initially failed in all three cases, then passed. Title tests initially had eight failures and four valid-title passes across V0-V3, then all twelve passed. Dictionary/list ID tests initially both raised TypeError, then both passed and retained six resolved unaffected visits with one audit-pending visit. These are 20 additional synthetic test cases, not a benchmark.

The combined suite passed **78 tests with 1 skip** before final formatting. Initial Ruff check reported eight long lines in the added tests; formatting corrected them. Final rerun: **78 passed, 1 skipped**, Ruff check and format check passed; `git diff --check` had no whitespace errors (only existing CRLF normalization warnings). The skip remains the Windows symlink privilege case. The evaluation suite includes offline CLI replay with network access blocked. Standards and Spec follow-up reviews each found zero actionable issues in these corrections.

Only evaluator code/tests and related records changed in this correction pass. Existing Ticket 01/02 work and V0-V3 planner paths remain intact. No real Google/model/database calls, formal cases/experiments, commit/push or freeze occurred. Conservative English street/title recognition and strict full-address equality can increase adjudication workload; they do not establish worldwide semantic parsing or live evidence coverage. Ticket 04 still requires separately authorized scope.
