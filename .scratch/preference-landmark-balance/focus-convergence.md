# Focus rule convergence

Date: 2026-09-28. Status: Implemented and offline Validated; not Frozen. Base `cc4d5a0`,
with existing uncommitted ticket 03, pilot tooling and historical documentation changes.
The user invoked implement after approving the converged rule discussion. No commit or
new live attempt is authorized by this task. The earlier three-case pilot stays unchanged.

## Accepted scope and implementation

Ordinary interests target one; exact sourced current-trip focus targets two; explicit
quantities/exclusions/category-only restrictions keep their existing semantics. Neither
enthusiasm nor focus infers many visits or a category ratio. Targets are not maxima:
same-category landmarks retain independent value after preference saturation.

ExperienceGoal and FoundryExperienceGoalDTO now expose only ordinary/exclusive trip scopes.
Candidate admission, Details continuation and final selection bypass general exploration
only for explicit exclusive scope. Shared soft eligibility includes whole-trip category
goals, preventing a model scope label from dropping target/provenance; broad style without
a category goal remains uncounted. Shared interpretation/generation prompts express the
same rule. Prompt18/wire12 and capture metadata identify the narrowed output contract.
Canonical envelope4 is retained; historical themed payloads are evidence, not valid new
inputs, and are never automatically migrated into focus claims.

## Validation sequence

The first interpreter regression used the exact Melbourne text with a controlled category
goal, whole-trip scope and exact focus quote. It failed because soft_coverage was null;
shared eligibility correction made it pass. Two DTO/domain tests then showed themed was
still accepted; narrowing both enums made them pass. Historical test fixtures were updated
to ordinary focus rather than themed. An integration fixture initially chose an unsupplied
synthetic POI and was corrected to an actually supplied option; no production relaxation.
The planning-entry regression checks candidate alternatives, independent landmarks and
final target2/matched1/remaining1, rather than counting supplied POIs as fulfillment.
The first related run after fixture fixes passed 48 tests.

A broader 110-test run had 109 passes and one capture-version wiring failure: the acceptance
tool still recorded prompt17. It was updated to18, and its nine-test file passed. Scoped
Ruff passed. Two independent review agents inspected Standards and Spec against the fixed
HEAD plus the working tree: zero remaining findings; Standards independently identified
the same tool metadata mismatch before its correction. No static typechecker is configured
for the backend. Frontend and version entry points are unchanged.

Final full backend regression: **1807 passed / 9 skipped in 75.57 seconds**. This includes
independent V0-V3, explicit counts/exclusions/exclusive behavior, API/presentation, capture
tooling and budgets. Scoped Ruff lint/format and `git diff --check` passed. There were no
live calls and no commits. Standards: zero remaining findings; Spec: zero findings.

## Boundaries and next step

Subsequent authorized validation: the unchanged Melbourne V3 input completed once and
passed the bounded focus acceptance; see [assessment](pilot/focus-revalidation-assessment.md).
The following boundaries describe the offline closeout and remain limits on general claims.

Mocked model/provider tests establish contract, selection and coverage behavior, not whether
a live model consistently chooses the intended focus source. Hard semantic handling, explicit
count mechanisms, Repair authority, budgets and provider calls are unchanged. In particular,
the prior Brisbane maximum-as-style limitation is not converted into a new count validator.
V0 remains LLM + prompt; V1-V3 share grounded rules and remain independently runnable.
After offline closeout, propose a separately bounded Melbourne V3 live verification; do not
reuse the exhausted/frozen three-case manifest or claim the old live failure now passed.
