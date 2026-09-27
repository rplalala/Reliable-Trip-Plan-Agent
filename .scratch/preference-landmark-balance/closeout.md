# Preference and landmark balance closeout

Date: 2026-09-28. Status: user-approved feature closeout; not a version freeze.
The user authorized logical local commits without another approval. No push, merge,
new live attempt, formal evaluation or unrelated implementation is authorized.

## Delivered behavior

Tickets 01-03 and the subsequent focus correction are complete. Ordinary positive POI
interests have a soft target of one; exact sourced current-trip focus has two. User-authored
quantities, exclusions and explicit category-only restrictions retain their existing meaning.
There is no inferred themed scope, large category count or ratio. One/two are fulfillment
targets, not maxima. Candidate opportunities retain a replacement beyond the target and
stop extra preference priority when saturated; independent landmark value survives.
Only distinct supported scheduled POIs count as grounded coverage. V0 stays LLM + prompt;
V1-V3 retain independent execution and their existing tools/RAG/validation boundaries.

## Evidence and historical sequence

Ticket03 regression passed 1793 / 9 skipped. The first three-case V3 pilot completed but
Melbourne failed focus interpretation: goal/whole_trip/themed with no target2. The user then
chose unified one/two rules. Failing offline regressions preceded the correction; historical
fixtures and an unsupplied synthetic POI fixture were corrected, and stale capture-version
metadata was fixed. The resulting full suite passed 1807 / 9 skipped. Standards and Spec
reviews have no remaining findings. Follow-up launcher/capture checks passed 11 after a
test process stub was corrected to preserve Git inspection. No provider probes were used.

One separately authorized unchanged-input Melbourne V3 attempt then passed bounded focus
acceptance in 99.781 seconds: museums 2/2, architecture 2/1, gardens 1/1. Eight qualified
nominees reached supply and six reached the eight-visit final itinerary (3/3/2). Captures
were complete and recorded budgets stayed within limits. Initial equaled final; Repair
was not exercised and 11 UNKNOWN findings remain. No automatic retries occurred.
See [first pilot](pilot/assessment.md), [correction](focus-convergence.md),
[revalidation](pilot/focus-revalidation-assessment.md) and [offline evidence](verification.md).

## Commit grouping

Pre-commit checks also found mixed line endings in the pilot launcher; formatter-only
normalization passed and its 11 tests passed again. The first combined regression stalled
near the existing HTTP embedding timeout/cancellation tests and was interrupted before
any commit. That file then passed all 16 tests independently. Inspection found a 20 ms
mock embedding deadline followed by an unbounded handler-entry wait: a scheduling race
is a hypothesis, not a reproduced production defect. No retrieval code/test was changed.
A full rerun with a 30-second diagnostic stack-dump threshold was used to resolve the gate.
It passed **1808 tests / 9 skipped in 77.43 seconds**. Ruff lint/format and staged diff
checks passed. The interrupted run is not counted as a successful regression.

1. Production preference/landmark policy, strict interpretation, prompt/capture identity,
   and directly related tests. Ticket03 and its accepted focus correction remain one
   coherent capability rather than committing an intermediate known failure.
2. Bounded development pilot/revalidation launchers, their tests and fixed synthetic-user
   scenario inputs. Runtime captures, manifests, logs and credentials remain untracked.
3. Current design/spec/status documentation and the bounded validation/closeout records.

Unrelated pre-existing food/sparse-day, historical semantic-closeout and handoff additions
are preserved unstaged. Ignored thesis records are maintained locally, not force-added.

Executed implementation/tool commits:

- `4084a2f feat: balance soft preferences with landmark opportunities`
- `274ab27 test: add bounded landmark pilot and focus revalidation tools`

The documentation commit containing this record completes the approved grouping. Runtime
manifests retain their original pre-commit revision/hashes; commits and line-ending cleanup
do not retroactively alter recorded execution identity or authorize reusing old manifests.

## Limits and next step

The user accepted closing this feature. This does not certify universal model reliability,
fees, opening/access, whole-trip affordability, Repair efficacy or cross-version superiority.
Historical themed payloads are retained as evidence but fail the narrowed current schema.
Brisbane's maximum-three wording is still a style preference rather than a new executable
count validator. The Melbourne third day is relatively light and the self-guided-tour POI's
visit object deserves future scrutiny; neither prompted another mechanism or live retry.
No additional work starts automatically after the checkpoint. A new issue and scope may
address a selected remaining limitation later.
