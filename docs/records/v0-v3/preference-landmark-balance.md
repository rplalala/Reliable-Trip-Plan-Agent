# Preference Landmark Balance

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="preference-landmark-balance-closeout"></a>

<a id="preference-landmark-balance-closeout--preference-and-landmark-balance-closeout"></a>

## Preference and landmark balance closeout

Date: 2026-09-28. Status: user-approved feature closeout; not a version freeze.
The user authorized logical local commits without another approval. No push, merge,
new live attempt, formal evaluation or unrelated implementation is authorized.

<a id="preference-landmark-balance-closeout--delivered-behavior"></a>

### Delivered behavior

Tickets 01-03 and the subsequent focus correction are complete. Ordinary positive POI
interests have a soft target of one; exact sourced current-trip focus has two. User-authored
quantities, exclusions and explicit category-only restrictions retain their existing meaning.
There is no inferred themed scope, large category count or ratio. One/two are fulfillment
targets, not maxima. Candidate opportunities retain a replacement beyond the target and
stop extra preference priority when saturated; independent landmark value survives.
Only distinct supported scheduled POIs count as grounded coverage. V0 stays LLM + prompt;
V1-V3 retain independent execution and their existing tools/RAG/validation boundaries.

<a id="preference-landmark-balance-closeout--evidence-and-historical-sequence"></a>

### Evidence and historical sequence

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
See [first pilot](v3-preference-landmark-pilot.md#preference-landmark-balance-pilot-assessment), [correction](preference-landmark-balance.md#preference-landmark-balance-focus-convergence),
[revalidation](v3-preference-landmark-pilot.md#preference-landmark-balance-pilot-focus-revalidation-assessment) and [offline evidence](preference-landmark-balance.md#preference-landmark-balance-verification).

<a id="preference-landmark-balance-closeout--commit-grouping"></a>

### Commit grouping

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

<a id="preference-landmark-balance-closeout--limits-and-next-step"></a>

### Limits and next step

The user accepted closing this feature. This does not certify universal model reliability,
fees, opening/access, whole-trip affordability, Repair efficacy or cross-version superiority.
Historical themed payloads are retained as evidence but fail the narrowed current schema.
Brisbane's maximum-three wording is still a style preference rather than a new executable
count validator. The Melbourne third day is relatively light and the self-guided-tour POI's
visit object deserves future scrutiny; neither prompted another mechanism or live retry.
No additional work starts automatically after the checkpoint. A new issue and scope may
address a selected remaining limitation later.

<a id="preference-landmark-balance-focus-convergence"></a>

<a id="preference-landmark-balance-focus-convergence--focus-rule-convergence"></a>

## Focus rule convergence

Date: 2026-09-28. Status: Implemented and offline Validated; not Frozen. Base `cc4d5a0`,
with existing uncommitted ticket 03, pilot tooling and historical documentation changes.
The user invoked implement after approving the converged rule discussion. No commit or
new live attempt is authorized by this task. The earlier three-case pilot stays unchanged.

<a id="preference-landmark-balance-focus-convergence--accepted-scope-and-implementation"></a>

### Accepted scope and implementation

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

<a id="preference-landmark-balance-focus-convergence--validation-sequence"></a>

### Validation sequence

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

<a id="preference-landmark-balance-focus-convergence--boundaries-and-next-step"></a>

### Boundaries and next step

Subsequent authorized validation: the unchanged Melbourne V3 input completed once and
passed the bounded focus acceptance; see [assessment](v3-preference-landmark-pilot.md#preference-landmark-balance-pilot-focus-revalidation-assessment).
The following boundaries describe the offline closeout and remain limits on general claims.

Mocked model/provider tests establish contract, selection and coverage behavior, not whether
a live model consistently chooses the intended focus source. Hard semantic handling, explicit
count mechanisms, Repair authority, budgets and provider calls are unchanged. In particular,
the prior Brisbane maximum-as-style limitation is not converted into a new count validator.
V0 remains LLM + prompt; V1-V3 share grounded rules and remain independently runnable.
After offline closeout, propose a separately bounded Melbourne V3 live verification; do not
reuse the exhausted/frozen three-case manifest or claim the old live failure now passed.

<a id="preference-landmark-balance-verification"></a>

<a id="preference-landmark-balance-verification--offline-acceptance-evidence-map"></a>

## Offline acceptance evidence map

Date: 2026-09-28. Base: `cc4d5a0`, with uncommitted ticket 03 changes.
This maps all parent-spec observable scenarios across the three implementation tickets.
Tests use controlled collaborators; they do not establish live quality or formal superiority.

| Parent scenario | Evidence under backend/tests | Observable coverage |
| --- | --- | --- |
| 1 | services/test_soft_preference_coverage.py | Ordinary/focus/emotional/ambiguous wording, exact provenance |
| 2 | services/test_landmark_discovery.py; policies/test_planning_supply.py; versions/v3/test_semantic_repair.py | Exclusion/exclusive admission, explicit quantities and maxima retain existing semantics |
| 3 | services/test_soft_preference_coverage.py; services/test_balanced_landmarks.py | Supported overlapping interests; distinct scheduled IDs; unsupported/repeated/reference exclusions |
| 4 | services/test_balanced_landmarks.py | Three same-category landmarks survive; multi-ref intent cannot bypass saturation |
| 5 | services/test_balanced_landmarks.py | Closed landmark excluded, replacements supplied; candidate supply not final fulfillment |
| 6 | services/test_balanced_landmarks.py; services/test_soft_preference_coverage.py | Eight interests/one day yields truthful gaps; broad goals retain non-count semantics |
| 7 | services/test_landmark_discovery.py; services/test_balanced_landmarks.py | General search with many interests; dense 63-candidate pools in three synthetic destinations |
| 8 | services/test_landmark_nomination.py; services/test_landmark_discovery.py | Destination-only nomination, no REQUIRED promotion, existing qualification |
| 9 | services/test_landmark_nomination.py; services/test_landmark_discovery.py | Exact reuse, ambiguity, alias rejection, later RAG identity changes |
| 10 | services/test_landmark_discovery.py | Named first, four within twelve, cache, exhausted and returned allocations |
| 11 | services/test_landmark_nomination.py; llm/azure_foundry/test_landmark_nomination_adapter.py | One send, strict DTO/token/deadline/timeout boundaries |
| 12 | services/test_landmark_nomination.py; services/test_landmark_discovery.py | Auxiliary fallback, cancellation, cleanup and unrelated hard errors |
| 13 | services/test_landmark_discovery.py; services/test_balanced_landmarks.py; services/test_quality_first.py | Roles, closed Details, unchanged resource/capacity checks |
| 14 | Shared FIRST_GENERATION_POLICY used by version runner tests | Variety, soft rank, dates/routes/time, explicit separate visits and no inferred site merge; prompt behavior is not live efficacy |
| 15 | services/test_landmark_nomination.py; services/test_soft_preference_coverage.py; versions/v0-v3 suites | Independent runners, V0 no nomination, V1/V2 no Repair, V3 no new soft-gap authority |
| 16 | observability/test_budget_summary.py; services/test_soft_preference_coverage.py; API/presentation suites | Missing usage retained; source-backed soft targets separate from counts |

Ticket 03 dedicated entry fixtures are in services/test_balanced_landmarks.py. Existing
quantity, identity, V3 and presentation regressions remain part of the full backend gate.
A fake generated itinerary cannot prove that a live model follows guidance. No live pilot,
formal experiment, version freeze, parent-site graph or new budget is claimed.
