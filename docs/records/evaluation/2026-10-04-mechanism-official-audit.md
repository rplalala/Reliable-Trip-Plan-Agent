# Ticket 12 mechanism and official-evidence audit — 2026-10-04

Status: Implemented, offline validated and fixed-base dual-axis review completed.
Source contract: [mechanism/audit](../../contracts/0001-evaluation-artifacts.md#mechanism-official-audit)
and [executable wire](../../contracts/0001-evaluation-artifacts.md#mechanism-audit-executable-wire).
Tracker: [Ticket 12 / #24](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24).

The user approved the complete concrete scope before implementation. Starting fixed point
was `21986f542cd5ec72ec519709c5882477c80c7413`, with a clean tracked worktree/index.
Implementation and direct tests were committed before review:
`8e945fd45b1b0e26ec55a71e748e13f8ccf8660d`
(`feat: add mechanism reports and opt-in official evidence audit`). No branch switch,
push, Issue mutation, PR, merge, live run, formal audit or version freeze was authorized.

## Delivered behavior

Preparation reuses the four-version batch or saved genuine V3-only Ticket 11 sources.
Exact result bytes and original input/run identity are verified; optional channels retain
local material diagnostics. Repair trigger is nonempty original authorized scope. Original
versus related targets, attempts, rounds, components and internal progress have separate
units. Cumulative parent summaries and matching trace copies are not added to child counts.
Missing metadata/denominators remain null, with observed cells and coverage retained.

Default-off caller-owned capture observes Gate-accepted claim catalogs, exact primary/Repair
structured projections, actual default-adapter submission, and actual V3 opening-rule
selections. Recording adds no prompt/schema/provider/budget changes. Injected unobserved
clients remain partial. Returns, failed calls and cancellations retain their original
behavior. Capacity and secret-bearing observations produce partial diagnostics; sink
failure logs its error type without replacing planning.

Audit units bind exact accepted source/claim revisions and all qualifying occurrences.
Preparation-only, rejected/search-only and accepted-unused claims do not qualify.
Independent human reviews bind exact queue/unit hashes and preserve reviewer, time,
rationale, supporting sources and unavailable verdicts. Observed qualifying units and
review/verifiable coverage remain visible when the complete population is unknown.
Independent Ticket 10/11 outcomes and usage remain separate attachments; internal Repair
acceptance is not an independently verified resolution or truth score.

## Validation sequence

1. Public capture, report, audit and CLI slices first failed with absent implementation
   modules, then passed after implementation. Subsequent boundary checks cover real runner/
   adapter prompts and call counts, result/adoption parity, usage-off rule selection,
   budget aborts, failure/cancellation, exact hashes, duplicate/conflicting identities,
   related targets, pending components and review missingness.
2. One real-graph fixture failed because empty preference input correctly skipped
   interpretation while the fixture queued an extra response. The explicit intended
   request corrected the fixture. Budget abort uses actual `input_tokens` and the named
   resource error. Retest passed. A rule-selection fixture initially used the historical
   `official:` alias; using actual Gate `official_web:` identity corrected the fixture.
3. Focused evaluator/observability/official integration/multiround/V3 validation/default
   adapter regression: **978 passed, 1 skipped**. Later dedicated Ticket 12 gate:
   **40 passed**. Full backend gate: **2477 passed, 10 skipped** in 318.11 seconds.
   Skips are existing environment/opt-in cases, not missing newly required acceptance tests.
4. Ruff and compile checks passed. Format initially found mixed line endings in three
   hook files; the formatter corrected them and all fourteen intended Python files passed.
   No configured/installed mypy or pyright was available; no type-check result is claimed.

These are synthetic/offline development checks. They do not establish provider receipt,
model attention, causal influence, real capture overhead, a formal truth rate, corpus
coverage or version ranking. Official rule observation is scoped to actual V3 operating/
opening selections, not verified admission or whole-trip affordability. Existing trace
fragments cannot establish complete historical denominators.

## Dual-axis review and corrections

The code-review skill used two independent read-only agents on
`21986f5...8e945fd`, reviewing the committed implementation against repository standards
and the originating fixed-point accepted contract. Standards: **0 findings**.
Spec: **2 P2 findings**, both report integrity/missingness errors:

- Matching trace rounds only compared status, accepting contradictory continuation,
  cumulative counters or usage. The fix compares these shared source fields while preserving
  valid saved-result mechanism counts and marking only the trace channel invalid.
- Truncated capture counted a catalog claim without its lost qualifying occurrence as
  accepted-unused. The fix leaves confirmed unused/population counts unavailable for
  partial capture and retains explicitly named observed counts/catalog remainder.

Four regression cases first failed (three trace cells and one real bounded-capture
producer/consumer flow), then passed after correction. The combined affected report/audit
test selection passed **29 tests**. The evaluator-wide correction gate passed
**640 tests, 1 skipped**, in 100.09 seconds. Fix commit:
`877dc89` (`fix: preserve trace integrity and partial audit uncertainty`). The earlier
full backend gate is not being described as validation of this later report-only correction.
No runtime hooks, planner budgets, prompts or score wires changed in the correction.

Committed correction recheck completed on both axes: Standards **0 new findings**;
Spec **both findings closed, no new concrete findings**. The Spec reviewer independently
reran the four new regression cases and all passed. Final contract/package/PROJECT and
record-index updates preserve the distinction between the full implementation gate and
the later evaluator-wide correction gate. No further implementation issue is outstanding
within this approved scope. Real capture overhead, live/formal execution, publication,
tracker synchronization and any version freeze remain outside this acceptance.
