# V3 final engineering closeout — 2026-09-25

Status: V3 ENGINEERING CLOSED — FINAL ENGINEERING CHECKPOINT RECORDED. Benchmark Frozen: NO. Formal Evaluation: NOT STARTED.
Next stage: Evaluation Readiness Audit, not started or authorized by this checkpoint.

## Authorized post-checkpoint review corrections — 2026-09-25

Status: implemented + offline-validated; no new live evidence. The review used committed
checkpoint `c339b832799c6e186792f91b988da293ad767c71`. The authorized fixes were applied on
the current `feature/frontend` working tree while preserving its existing uncommitted work.
They do not retroactively change historical smoke outcomes or increase any runtime limit.

- Shared V1/V2/V3 transfer checking now uses the continuous interval containing the actual
  bound departure for WALK and basic DRIVE as well as time-dependent modes. A 20-minute
  transfer departing at 11:50 cannot borrow a 13:00-14:00 gap across fixed 12:00-13:00 rest.
  Explicitly binding departure to 13:00 can pass with the same route estimate. Missing
  timezone information remains UNKNOWN. This is shared correctness, not a V3-only benefit.
- V3 stage `comparison`, `main_visits_lost`, `coverage_regressions` and `spatial` now describe
  the original-to-adopted result, rather than inheriting the final attempted round. Round
  proposals, losses and rejection reasons remain in `rounds`. Net visit losses include
  removed or replaced original main visits; moving an unchanged identity is not visit loss.
  The existing comparison vocabulary is retained: `coverage_regressions` records count
  reductions, including an authorized overfull reduction from six visits to five, rather
  than exclusively new coverage violations. No acceptance rule was relaxed.
- `RepairBudget` obtains its implicit Repair policy from the supplied runtime snapshot.
  Explicit `policy` still takes precedence; missing Repair policy fails clearly. Independent
  stage callers no longer need to pass the same policy twice. Normal graph callers already
  supplied both values. This change does not claim to remove every legacy diagnostics
  configuration read elsewhere in the application.

Offline execution order:

1. New focused regressions: 6 passed, 1 failed. A global configuration-loader mock also
   blocked the fixture's existing diagnostics read. The mock was narrowed to budget
   construction; the real stage still checks injected policy execution.
2. Focused tests plus Repair, multi-round, B/C targets, mixed transport, shared initial
   routes, V3 wiring and API-evidence regressions: 261 passed.
3. Ruff initially reported two overlong lines in the new test file; formatting that file
   resolved them. The targeted Ruff check passed; the initial diff whitespace check passed.
4. An additional accepted-then-rejected deletion regression yielded 7 passed, 1 failed:
   its assertion incorrectly treated all count reductions as coverage violations. The
   assertion was corrected to preserve the existing allowed six-to-five comparison meaning.
5. Final focused regressions: 8 passed. Targeted Ruff passed. No model, HTTP, embedding,
   database or live calls were made; no full-repository regression was run.

Implementation: `route_options.py`, `repair_budget.py`, `repair_service.py`.
Regression coverage: `backend/tests/versions/v3/test_closeout_corrections.py`.
Historical artifacts, budgets, prompts, V0 behavior and the product default are unchanged.

## Authority and checkpoint identity

Current code and parsed runtime configuration establish implementation facts. Accepted user
contracts establish intended behavior; a discrepancy is not legalized by editing documentation.
This checkpoint covers the combined shared and V3 tree, not independently validated intermediate
commits. Exact final commit hashes are recorded in the completion report, avoiding self-reference.
Later correctness fixes require authorization, validation and a new distinguishable checkpoint.

## Delivered flow and ownership

V0-V3 remain independent runners. The product default remains V0. One shared preference
interpreter enforces typed assessment, source quotations and canonical requirements. Provider
rejection, malformed output and domain contract failure are distinct from user-input dispositions.
V0 does not acquire travel evidence. V1 adds tools; V2 adds request-owned TripWorld retrieval,
canonical resolution and merged supply. V3 reuses that primary flow through a post-primary hook.

Shared initial mixed transport prepares directed options and binds actual timed adjacencies after
one primary generation. Provider duration, application reserve and UNKNOWN remain separate.
V1/V2 report diagnostics without targeted Repair. These baseline changes, the CLI import-cycle
fix, shared output and Preference Gate are not V3-exclusive research contributions.

V3 preserves draft and original report, then validates before Nearby. Hard conflicts and minimum
one-primary-visit coverage precede optional quantity/repetition/overfull reviews. Minimum coverage
is not the default two-visit review goal. Active target worksheets localize acquisition, operation
authorization and projection; deferred targets do not silently request resources. A provides elastic
free-time authorization, atomic consumption and real-place adjacency. B provides demand-based
REQUIRED protection, adjacent moves and scoped compensation. C provides evidence-supported
opening/transfer conflict repair. Public access and unbound semantics are not invented facts.

Candidate context, target-specific options, identity/source ledger and actual input stay separate.
UNKNOWN may be selected without becoming verified. Preparation reference counts do not prove
schedulability. Presentation history rotates opportunities; evidence-backed conflicts have narrow
scope. No-progress causes material-opportunity reassessment, not an identical automatic retry.
Fingerprints omit incidental round/audit changes. The latest adopted draft is the next input.

One patch may contain multiple targets. Dependency-aware components are applied transactionally;
illegal/dependent edits cannot be silently salvaged as independent. Same-validator revalidation and
business comparison determine adoption. Evidence-only changes are not arrangement improvement.
Fair reassessment applies new evidence to both sides. Rejected components/rounds retain the latest
adopted state and unresolved compensation. Final identities, dates, costs and diagnostics use the
adopted primary and application-managed whitelist. One final Nearby stage only adds references.
Request deadlines, cache/attempt/failure history and cancellation span phases; owned resources close.

## Current effective limits

The authority is `config/runtime.yaml` schema 6, parsed once per request. Current normalized
snapshot SHA-256: `a4a9c9d7f388dbf78f172651d4c8b46b609bf044490b0cffe96f01beeea50ba2`.

- Ordinary initial Details 60; initial RAG Details 30 and resolution 30; K maximum 20.
- Baseline Routes 7 requests / 400 elements / 64 per matrix. Shared mixed additions: 32 pairs,
  32 requests, 64 elements; post-primary reservation 16 pairs / 16 requests / 32 elements within
  those totals. Route-work 120 seconds, post-primary reserve 30, provider timeout 20.
- Primary and each Repair input 252000 engineering tokens; each output 16384; framing reserve2048.
- Repair: 5 rounds / 5 calls total, stage360 seconds, round120, model70, preparation45,
  recheck reserve20, minimum model start30, round reference60, finalize reserve1.
- Repair union32 identities, activity120, candidate/feedback text ceilings12000 characters each.
- Repair stage totals: Google6 (ordinary5 + fallback1), canonical30, Details30, embedding1,
  RAG retrieval1 Top-K10, Routes24 requests (8 reserved post-proposal) / 32 elements.
  These never multiply by rounds/targets. Cache hits are not sends; failures retain attempt history.
- Quantity/repetition/overfull reviews default false. Daily review range2-5; product minimum1.
  Adjacent move1 day, blank-day09:00-18:00, two alternatives per gap, two exploration positions.
- WALK route3 km, TRANSIT45 minutes, DRIVE30 minutes plus10 reserve; discovery radii2/5 km;
  automatic leg45 minutes. Repair detour floor1 km / ratio0.5, no-route fallback1 km /45 minutes,
  cumulative added daily travel90 minutes. Travel minutes are not execution seconds.
- Nearby3 requests,10 seconds stage,4 seconds/request,0 retries,maximum3 references.
- Whole-request600 seconds only with explicit development activation; YAML alone does not grant it.

No limits or runtime policies changed during closeout. See `config/README.md` for full key semantics.
Current preference markers: prompt13, draft9, strict `PreferenceDraftV9`, assessment2;
`interpreted_requirements_3` and `itinerary_2` remain the downstream contracts.

## Artifact-verified development evidence

These are bounded historical observations at their own manifests/source hashes, not live validation
of every byte in the final checkpoint. Full `result-complete.json` and round artifacts were used;
a truncated `v3-finalized-complete.json` preview was not treated as a complete research record.

| Mechanism | Observed artifact and limit |
| --- | --- |
| Shared initial mixed transport | `logs/v1_tokyo_3day_shared_mixed_20260926/`: final WALK1092/662 seconds and DRIVE924 seconds, with separate DRIVE reserve; V1 has no Repair. |
| Five-round feedback | `logs/v3_honolulu_9day_shared_mixed_20260927/`, run8b7db82f-9c52-4cdc-b802-2c273406ee66: R2/R4 empty, subsequent distinct material fingerprints and 10/2 incoming rotated identities; R5 rejected, adopted itinerary unchanged fromR3. Historical cap16 route requests, not today's24. |
| Joint minimum coverage | `logs/v3_honolulu_9day_minimum_coverage_20260927/`, runf9bd621d-0eb5-47d7-8af8-03825d57524b: R1 three separate additions for zero-primary dates; visits10->18, missing minimum dates3->0, five rounds, one ordinary quantity review remains. |
| Same-round partial component adoption | Same minimum-coverage run, R2: component1 accepted; component2 rejected with `Insufficient unoccupied transfer window`. Confirmed from component records, not inferred from ACCEPTED_PARTIAL. |
| Adopted TRANSIT | Same final-primary: day1-homa -> day1-waikiki1845 seconds and day4-queen-emma -> day4-inspiration-museum686 seconds, `time_applicable` PASS. Limited adopted observations, not comprehensive TRANSIT/future reliability. |
| Later rejection preserves adoption | Same R5 empty patch rejected; adopted itinerary equals R4. Nearby saved diagnostics:3 sends,3 references; primary invariant recorded. |
| Gate taxonomy | `logs/shared_preference_taxonomy_prompt12_20260925/`, rund9a30d0a-da89-4c2e-8b55-032ae4fde4d7: ten preregistered cases passed. Prompt12 only; not classifier stability or prompt13 live evidence. |
| Safety/provider separation | `logs/shared_preference_case45_diagnostics_20260925/`, run035259d6-a204-44e4-a2d2-60af512ef106: Case4 structured SAFETY_BLOCK with grounded quote; Case5 HTTP400 content_filter/invalid_request_error -> provider_request_rejected, no Gate classification. No downstream travel calls. |

Old first Gate run9f50dee0-4cc1-4f18-8eec-800a90597730 remains historical contract failure.
Current content-filter UI mapping and prompt13 budget-scope behavior have offline evidence only.
Absence of a positive optional-ambiguity example in the taxonomy set is not extra live coverage.
Review-off/exemptions, all C operation combinations, cancellation/provider-failure/component
dependency combinations remain offline-only or not naturally observed live as individually noted.
No broad all-branch live claim is made.

## Closeout changes and limitations

Only two missing prompt13 offline input cases were added: accommodation-only and flights-only
expense exclusions. Existing combined exclusions and true amount/currency/per-person conflicts
remain tested through wire/domain/interpreter paths. Mocked DTOs prove path preservation, not
real-model classification reliability. Closeout also restored the normalized route-evidence payload lost when shared mixed-route
preparation replaced the old acquisition method. This is a shared V1/V2/V3 observability
regression fix, not new Repair capability. Stale tests were migrated to approved current limits,
Gate outcomes and the full_day wire field; four long test lines were wrapped. No prompt,
configuration or budget changed. Documentation aligns current status while preserving earlier dated checkpoints.

Public access, admission, reservations and costs may remain UNKNOWN. Full expense-scope and
verified whole-trip accounting are unsupported. Model/provider classification is not universally
stable; a provider can preempt a non-travel-control classification. Suitability of a legal primary
visit and different-ID experiential duplication remain limitations. One visit/day is not two,
and completed targets do not establish complete trip feasibility or superiority over V2.
Nearby cannot fill primary coverage. RTPEval research OPEN/DEFER items, including provider-blocked
outcome taxonomy, are unchanged; the unconfirmed evaluator document is excluded from this commit.

## Validation and Git preservation

Final combined-tree validation passed; chronology is recorded below. Execution-only guards under ignored
closeout logs deny socket connections including loopback services (internal socketpair exempted),
and psycopg connections; DB opt-in is disabled. Existing fake providers/MockTransport remain active.
Tests do not count as new serializer sizing; historical measured payloads retain their own scope.
The intended file manifest/ownership and working-tree/content hashes are retained in local logs.
Original `.gitignore`, thesis notes, historical logs and unconfirmed evaluator work are excluded.
Git's existing line-ending normalization is distinguished from substantive content changes.

## Final validation chronology

All commands used local installed dependencies. Python ran with the execution-only
`logs/v3_final_engineering_closeout_20260925/guard` on PYTHONPATH. The guard denies outbound
socket connections (including local services) and psycopg connections, except the internal
Windows socketpair used by event loops. `TRIPWORLD_TEST_DATABASE=0`; fake providers and
MockTransport remained in use. Frontend used NODE_OPTIONS with a connection/fetch-deny preload.
No live external service calls were possible/allowed during closeout validation.

1. First complete backend: `python -B -X utf8 .../run_offline.py` invokes
   `pytest backend/tests -q --junitxml=.../backend.xml`. Collected1472:1442 passed,
   21 failed,9 skipped,76.65 seconds,exit1. Failures:8 stale quality-limit assertions,
   7 shared-input fixture/outcome assumptions,5 missing full_day wire fields,1 missing
   normalized route-evidence artifact. No failure was caused by a stopped database.
2. First `python -B -m ruff check backend scripts tools`:4 existing long test lines.
3. Frontend `npm --prefix frontend test`:6 files/33 tests passed,15.42 seconds,exit0.
4. `npm --prefix frontend run lint`:exit0; `npm --prefix frontend run build`:TypeScript
   and Vite passed,exit0. Vite build1.01 seconds; this is not the combined command duration.
5. Migrated stale fixtures/assertions to approved current contracts/limits, wrapped the four
   lines and restored shared normalized route recording. No scheduling/policy thresholds changed.
6. Targeted pytest: observability/test_run_trace; services/test_quality_first,
   test_shared_planning_input,test_time_protection,test_initial_mixed_routes,
   test_preference_recovery; versions/v3/test_b_targets,test_multiround,test_repair:
   273 passed,23.27 seconds,exit0. Ruff then passed. Scopes overlap; counts are not summed.
7. Final complete backend on corrected combined tree:1472 collected,1463 passed,
   0 failed/errors,9 skipped,0 xfail/xpass,73.46 seconds,exit0. Nine skips are explicitly
   disabled optional PostgreSQL tests; no DB connection was attempted.
8. Separate fresh processes: `python -B scripts/run_v0.py --help`, V1, V2 and V3 variants,
   all exit0 (3.53/3.67/3.93/3.88 seconds). All six public shared service exports import,exit0.
9. Final Ruff and `git diff --check`:passed. Post-validation edits only record factual
   documentation; no further functional rerun is required for those addenda.

The only newly added behavioral cases are separate accommodation-only and flights-only budget
exclusions; combined exclusion and real monetary/currency/per-person conflicts already existed.
All pass through current mocked wire/domain/interpreter paths. This is not prompt13 real-model
acceptance. No new serializer sizing or live request was performed during closeout.

## Checkpoint preservation

Files are grouped into shared planning/transport/output/configuration, V3 repair/validation,
shared Preference Gate/provider/runtime correctness, and documentation. Direct tests accompany
implementation; mixed dependency files stay together rather than being cosmetically refactored.
The complete per-file ownership matrix and tested normalized-content hashes are stored in ignored
closeout records. Final Git blobs are compared against that frozen manifest under the repository's
existing CRLF/LF normalization. Intermediate commits are not independently certified states.
`.gitignore` user edits, unconfirmed `docs/evaluator_design.md`, logs and thesis notes remain out.

This closes the approved engineering scope, not every possible semantic capability. No unresolved
blocking divergence was found after the recorded correction/regressions. Known limitations above
remain explicit. Benchmark Frozen: NO. Formal Evaluation: NOT STARTED. Evaluation Readiness Audit
is the next proposed stage and has not begun. Future correctness changes require a new authorized
checkpoint; the exact final HEAD is supplied by the completion report, not this same commit.

### Staging-time static correction

The cached diff check additionally found one trailing space in the previously untracked
`test_preference_smoke_harness.py` (not covered by the unstaged tracked-file diff check).
The Gate commit was paused. Only that whitespace was removed; its focused offline suite then
passed22 tests in8.00 seconds,exit0, under the same network-deny guard. No test logic changed.
The final checkpoint therefore combines the complete1463-pass run with this affected-file retest.
The manifest was re-locked after this correction; the earlier lock is preserved in local records.
All intended files were subsequently scanned for trailing whitespace, with none remaining.
