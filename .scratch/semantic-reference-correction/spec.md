# Bounded semantic reference correction

Approved: 2026-09-27. Implementation baseline: `339e7e4a4a9eac133f2bdff69217b8b35c6990b4`.

## Scope

For shared V1-V3 POI semantic assessment, allow at most one corrective model call per
batch after invalid or missing evidence citations. Supply the same canonical candidates,
requirements and named bindings with bounded diagnostic feedback. Revalidate the entire
response, including identity, requirement, exception and evidence rules, before caching.
Ordinary non_main/unresolved judgments and non-reference failures do not trigger correction.
V0 and quantity Repair remain unchanged. No live calls or commits are authorized.

Both attempts consume the existing request-owned semantic call/time budgets. Defaults stay
6 calls/request, 45 seconds/call, 120 seconds total, 32000 input and 8192 output tokens.
Correction input is sized including feedback. Absolute deadlines remain effective. If
correction cannot be sent, or fails, retain a terminal failure, not an unverified fallback.
Already accepted batches remain recorded; invalid batches never enter the cache/ledger.

## Evidence and validation

Record bounded allowed/offending refs for row and match failures. Link correction calls to
the rejected call; preserve input/output/outcome capture through the existing opt-in writer,
redaction and size caps. Record pre-send correction stops. Capture failure must not alter
acceptance. Cancellation propagates without retry.

Test through assess/prepare and the real SDK/capture boundary with synthetic responses.
Cover correction and cache reuse, double failure, shared budgets/deadlines/input sizing,
cancellation/provider errors, and accepted earlier batches. Run backend regression tests
and independent Standards/Spec review before completion. Live efficacy is unvalidated.

## Historical evidence

`logs/live_smoke_20260926/report.md` describes eight one-attempt development runs.
Melbourne V1 recorded an extra underscore in a match citation. Sydney V1/V3 failed row
citation validation, but rejected full outputs were not retained. Tests reconstruct the
observed failure class; they do not replay complete missing provider responses.

## Completion checkpoint

Implemented and offline validated on 2026-09-27; no live execution or commit.
TDD first reproduced terminal row-reference failure, then passed after bounded correction.
A budget-stop evidence test failed because the stop was not captured; implementation added
capture/tracing. The real writer then exposed a missing call_id; a distinct linked stop ID
fixed it. The focused suite passed 48 tests at that point. Additional service boundaries
and SDK correction-success coverage passed 53 tests in the final targeted run.
Full backend checkpoint: 1689 passed, 9 skipped, before the final two test additions;
production code was unchanged afterward. Ruff and diff checks passed.
Standards and Spec review found no remaining issues after separating deadline, total-time
and input-limit test triggers; service-owned and caller-owned deadlines are both covered.
These tests use synthetic provider responses and one reconstructed observed match typo,
not complete replay of the unavailable historical rejected outputs.

## Approved contract-correction expansion — 2026-09-27

The user approved the minimum option in `non-reference-diagnosis.md`, using TDD and
independent code review. This supersedes the citation-only exclusion above specifically
for identity-set mismatch (missing, unexpected or duplicate IDs), unauthorized exception
claims and exception-role ownership errors. All supported classes share ONE corrective
call per batch, not one per error class. Return the complete same batch and revalidate
all rules before atomic cache/ledger admission. Never remap IDs, drop rejected claims or
silently accept only valid rows. Unrelated malformed schemas and provider failures remain
terminal; ordinary valid non_main/unresolved judgments do not trigger correction.

Feedback must be bounded and actionable, containing identity differences or affected
exception requirements and actual permission conditions. Explicit exception authorization
requires favor plus explicit_primary_exception=true, or a REQUIRED named requirement
bound to the exact place. A supported evidence-backed match and exception_only role
remain necessary. Clarify these rules in the prompt and update its fingerprint.

Budgets remain 6 calls/request, 45 seconds/call, 120 seconds total, 32000 input and 8192
output tokens. Correction still consumes those shared limits, includes feedback in input
sizing, respects both deadlines and uses linked opt-in input/output/outcome capture.
V1-V3 share this change; V0 and quantity Repair are unchanged. No live runs or commits.
Offline synthetic/minimized acceptance does not establish real-model correction efficacy.

### Expansion validation checkpoint

TDD reproduced three identity-set failures before adding the shared correction entry; all
three then passed. A separate ordinary-food exception test failed before exception errors
became correctable, then passed without granting main eligibility. Tests also cover strict
positive/negative authorization, role correction, cross-class terminal second failures,
unchanged candidate inputs, bounded feedback, cache reuse, shared call-budget exhaustion
and linked real-SDK mocked-transport capture for citation, identity and exception failures.

Full backend regression: 1712 passed, 9 skipped (91.98 seconds). A subsequent test-only
addition covered unresolved or absent matches despite named permission; the final focused
service/capture suite passed 72 tests (4.76 seconds). Production code did not change after
the full suite. Independent Standards and Spec reviews found zero actionable issues; the
Spec review's optional supported-match coverage suggestion was implemented and passed.
No live calls, quantity Repair changes, commits or version freezes occurred.
