# V0 milestone checkpoints

Current shared/V3 engineering checkpoint (2026-09-25): see [closeout](v3_closeout.md)
for current configuration, shared ownership and artifact-verified evidence. Earlier dated
implementation/live statements below retain their original scope. V0 remains tool-free;
V1/V2 do not run Repair; the product default remains V0. Provider recovery UI is offline-only.


## Latest accepted boundary - 2026-09-20

V0 retains tool-free shared-input/output execution; the latest joint quality run did not rerun V0.

Status: implemented + bounded development-live-validated where covered, not production-ready, formal benchmark or automatic re-freeze. The latest joint V1/V2 event used explicit quality_first_1; these configuration limits do not extend the V0 CLI. This does not rewrite earlier frozen configurations. Exact implementation/config hashes, offline history, live inputs, failures, artifacts and limitations are maintained once in the [joint event](development_record.md#m-e07748f66be8). Reviews/Profile and ten-day K16 live were not covered; unknown Web reasoner usage stays unknown. No new validation is performed by this migration.

Dated records below preserve original scope, status and evidence; they are not current runtime instructions. Current design is maintained separately. Proposed or unexecuted steps remain unexecuted unless a later explicitly identified record establishes otherwise.

<a id="m-cad8591a7c35"></a>
## Authorized shared-foundation migration - 2026-09-19

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-cad8591a7c35-0"></a>

The historical freeze and results below are preserved. Current V0/V1 now share
PlanningRequest (planning_request_2), authoritative structured trip facts and optional
semantic-only preference interpretation. V0 remains plain LLM without external evidence;
V1 retains its external tools and deterministic candidate supply. Empty preferences skip
interpretation. This intentionally changes old free-text input behavior, not the research
mechanism distinction. No exact old-output parity, new live acceptance or re-freeze is
claimed. Shared-foundation offline validation: 769 passed, 9 skipped; Ruff/diff passed.
No live calls were made. Current contracts/validation: docs/v1_design.md and README. Do not combine old-input
V0 measurements with revised V1 as a tools-only comparison. Frontend alignment is outstanding.

<a id="m-13e4fb9a2522"></a>
## Status

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-13e4fb9a2522-0"></a>

- Completion date: 2026-09-11
- Baseline commit: `34943c7` (`docs: document V0 setup and usage`)

<a id="m-120ec257da76"></a>
## Testing Strategy and Milestone Status

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-120ec257da76-0"></a>

The V0 test suite covers:

<a id="b-120ec257da76-1"></a>

- The exact two-node graph topology and two intended LLM stages
- Missing-critical-requirement handling
- No-retry and no-repair behavior
- The shared `PlanningResult` contract and `SystemVersion.V0`
- Azure Foundry DTO schema compatibility and strict validation
- Deterministic DTO-to-domain mapping and preservation of domain validation
- Provider abstraction and deployment configuration
- Unit-test isolation from external network access
- CLI JSON output, exit codes, and cp936 Unicode round-trip behavior

<a id="b-120ec257da76-2"></a>

At the V0 milestone freeze:

<a id="b-120ec257da76-3"></a>

- `pytest`: 50 passed
- Ruff: passed
- `git diff --check`: passed

<a id="b-120ec257da76-4"></a>

Subsequent repository-wide regression runs have continued to pass all V0 tests.

<a id="m-670d804821bf"></a>
## Known Limitations

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-670d804821bf-0"></a>

- Travel facts come only from model pretraining and may be outdated or inaccurate.
- Opening hours, availability, prices, routes, travel times, weather, and disruptions
  are not verified.
- UTC offsets are supplied by the model and checked for format, not geographic or
  date-specific correctness.
- Itinerary feasibility and user constraints are not programmatically validated.
- Missing critical requirements are not resolved through an interactive clarification
  flow.
- Provider, DTO, mapping, or domain failures terminate the run without recovery.
- V0 has no persistence, memory, or repair mechanism.

<a id="m-7414be5440b3"></a>
## Frozen V0 Research Behavior

_Source context: V0 As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-7414be5440b3-0"></a>

V0 freezes research behavior, not the literal contents of its files. The following
research behavior must remain stable for V0/V1 comparison:

<a id="b-7414be5440b3-1"></a>

- The two-node graph and requirement-extraction-to-itinerary-generation order
- Exactly two LLM calls in a successful run
- Plain-LLM generation without external information
- The prompts' semantic behavior and planning objective, rather than their exact text
- Fail-fast handling of missing critical requirements
- Reference-date behavior
- Strict DTO validation and deterministic DTO-to-domain mapping
- No retry, regeneration, constraint-validation loop, or repair
- The shared `PlanningResult` contract and `SystemVersion.V0`
- The independent `scripts/run_v0.py` execution path

<a id="b-7414be5440b3-2"></a>

Necessary backward-compatible shared infrastructure changes are allowed only when
they do not change V0 research behavior and all V0 regression tests continue to pass.


## Compatible transfer output update (2026-09-25)

The shared itinerary DTO now accepts optional `transfers` (missing defaults empty).
Current V3 binds and presents verified/unknown per-leg route estimates and separate
application reserves; V0-V2 do not fabricate transfers or acquire additional routes for
this field. Primary model DTO/prompt, K, existing version entry points and product default
are unchanged. The frontend can render this optional data when supplied; this does not
implement the deferred Product V3/API selection or the whole frontend backlog.
See [V3 design](v3_design.md#shared-output-and-frontend) and the
[development verification record](v3_development.md#mixed-transport-and-joint-components-2026-09-25).
This is shared output compatibility, not evidence of a V3-only quality gain or a re-freeze.


### Post-milestone shared startup correction (2026-09-25)

A fresh standard V0 CLI process failed before --help due to eager services package exports
re-entering the partially initialized V0 graph. Lazy planning exports now preserve public imports
without that cycle. Fresh-process --help regressions cover V0-V3. This is shared correctness,
not a V3 mechanism benefit; previous milestones/live records are not rewritten. Shared prompt13
also distinguishes party trip-budget totals from expense scope; explicit provider filtering has
an independent public rewrite action. See shared_preference_input.md for boundaries and tests.
