# Benchmark responsibility decisions and deferred proposals

Historical checkpoint: 2026-09-28. Status: Accepted responsibility boundary; detailed
benchmark design deferred. These decisions/proposals are not a frozen benchmark or a
present execution plan. Current [batch terminology](../../0006-independent-evaluation.md#batch-and-benchmark-terminology)
and [material contract](../../contracts/0001-evaluation-artifacts.md#rtpeval-spec)
own the implemented handoff; later producer completion and external requirement-review
interfaces are in the [intake contract](../../contracts/0002-intake-identity-usage.md#producer-material-handoff).

## Construction versus independent evaluation

The accepted division made construction responsible for inputs, complete V0–V3 workflows,
selected results, usage/provenance, attempt/exclusion records and iteration recommendations.
Only the user could select iteration or an identified evaluation batch. Candidate admission
was distinct from final selection; Evaluation did not monitor candidates, generate planners,
select replacements or independently requalify producer workflows.

Ordinary generic no-POI placeholders ceased to disqualify groups: their evaluation role
was transition/free-time, without inventing venues or erasing user-protected time. Named
unresolved POIs remained possible visits. Multi-POI blocks sharing one visit interval
still violated the delivery contract; Evaluation could not invent a split.

All four workflows had to complete. Resource-truncated pending Repair was ineligible,
but a numeric cap alone did not establish truncation. Normal no-candidate/no-opportunity/
rejected-repair stops could qualify. Sparse days, repetition, residual conflicts and
UNKNOWN alone were not workflow failures. Exact completion/stop mapping and construction
tooling remained later design work at this checkpoint.

## Source material, review and development exposure

The proposed handoff had four separate result files and four separately associated usage
files, a versioned manifest, exact input/source/configuration hashes and reviewed requirements.
Unavailable usage remained missing resource evidence, not quality failure; Repair/stage
subsets were not added twice and evaluator acquisition had its own ledger. Symmetric
capture, common timing and retry/cache semantics were then unimplemented preparation gaps.
Optional V3 drafts/mechanisms/official claims supported separate tracks without making
absence a new eligibility gate.

At this checkpoint, RequirementSpec allowed assistant drafting from original Input with
explicit user review. Explicit obligations, soft preferences and unsupported/unresolved
clauses were distinct; output inspection could not author obligations or pacing quotas.
Later separately operated agent author/reviewer handoff is a subsequent accepted interface,
not a reinterpretation of this historical human-review requirement.

If failures informed tuning, construction had to retain attempts, reasons, checkpoint
changes and exposure, distinguishing observations from hypotheses. A later success did
not erase failure; candidates were not automatically held-out. Matched checkpoints and
final sampling could not silently mix old and new outputs.

## Provisional study composition

The following remained OPEN, not executable quotas or evaluator gates:

| Topic | Historical proposal and unresolved decision |
| --- | --- |
| City exposure | Tokyo, Sydney, London, Melbourne and Berlin were development/regression cities. Categories distinguished mention, fixture, smoke, debugging, tuning and held-out eligibility; a fixture name alone was not targeted itinerary tuning. Held-out cities remained OPEN. |
| City selection | Consider exposure, basic Places/Routes operability, reasonable TripWorld coverage, geography/timezones and urban diversity. Do not select using V3 scores, require cross-city travel silently or choose only richest RAG coverage. |
| Request composition | Six cities × six types = **36 unique requests**: Basic, Soft Preference, REQUIRED, REQUIRED + EXCLUDED, Pace/Spatial, Complex. Basic retained mandatory budget; Complex did not necessarily mean long. |
| Length strata | **12** requests of 2–3 days, **18** of 4–5 days, **6** of 7–10 days, crossed with type rather than confounded. |
| Optional repeats | One run/version gives **144** runs; second runs on 12 preselected requests give **192**. Cost, latency, usage, failure and variation from approved development work would inform the choice; repeats did not become independent requests or extra main weight. Live repeats mix external variation unless inputs are controlled. |
| Failures/replenishment | The complete-workflow cohort was not unconditional performance. Attempt/exclusion/resource counts stayed external; replacement/retry/stopping rules remained OPEN before execution, with excluded individual versions outside main scores. |

Analysis tags could cover named dates/counts/revisits, OPTIONAL/EXCLUDED, exterior/entry
intent, protected time, transport preference, pacing, whole-party/subgroup preferences,
long trips and constrained budgets. Tags did not activate special scoring rules.
Contradictory, ambiguous, unsupported or demonstrably unsatisfiable requests needed
explicit boundary-case semantics, not normal success assumptions or a complete planner
infeasibility solver.

Controlled Repair remained a separate V3-only study basis of **24 targets and 8 controls**,
not a four-version cohort or pooled E2E score. Case construction/execution and the final
analysis/sampling plan required separate authorization and specification.
