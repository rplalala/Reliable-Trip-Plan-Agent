# V3 final engineering checkpoint — 2026-09-25

Status: V3 ENGINEERING CLOSED. Benchmark Frozen: NO; Formal Evaluation: NOT STARTED
at this checkpoint. It established combined shared/V3 engineering behavior, not every
intermediate commit or universally correct trips. Later current behavior belongs to
[validation/repair](../../0005-validation-repair(v3).md) and
[application operations](../../0007-application-operations.md).

<a id="shared-milestone-notice-2026-09-25"></a>

## Shared milestone notice - 2026-09-25

At this checkpoint V0 remained tool-free, V1/V2 did not run Repair and Product
defaulted to V0. Provider recovery UI had only offline validation. These statements
were shared with V0/V1/V2 and frontend milestone records; later product defaults
are documented in [current application operations](../../0007-application-operations.md).

## Mechanism boundaries and shared corrections

V3 reused primary tools/RAG planning, preserved draft/original reports and validated
before Nearby. Hard conflicts and minimum one-visit coverage preceded optional reviews.
Target-specific permissions, application-owned identity/evidence and dependency-aware
transactional components controlled adoption; same-validator rechecks and business
comparison preserved the latest adopted state after rejection. Nearby remained references.
Shared initial mixed transport, Preference Gate, output and startup fixes were baseline
changes, not V3-exclusive research contributions. V0 stayed tool-free; V1/V2 had no Repair.

Closeout restored normalized route-evidence recording lost in shared mixed-route
preparation, migrated stale tests to approved limits/Gate/full_day contracts and added
two missing mocked prompt 13 budget cases: accommodation-only and flights-only exclusions.
Prompts, configuration and limits were unchanged. Mocked cases do not establish real-model
classification reliability or new serializer sizing.

The subsequent offline review at `c339b832799c6e186792f91b988da293ad767c71`
identified three corrections without changing historical live observations:

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

Regressions cover injected Repair policy, continuous windows and accepted-then-rejected
net comparison. The affected selection passed **261 tests** and the final focused set
**8 tests**; Ruff/diff checks passed. No full repository run or live service was performed for those later corrections.

## Frozen configuration at this checkpoint

The checkpoint used `config/runtime.yaml` schema 6, parsed once per request. Its normalized
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
Checkpoint preference markers: prompt 13, draft 9, strict `PreferenceDraftV9`, assessment 2;
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

## Validation of the combined closeout tree

Network-deny execution guards blocked outbound sockets/psycopg, with only event-loop
internal socketpair exempted; frontend used a fetch/connection-deny preload.
`TRIPWORLD_TEST_DATABASE=0`, fake providers and MockTransport remained active.
The chronological checkpoints below are not summed:

| Checkpoint | Observed result | Explanation |
| --- | --- | --- |
| Initial backend | **1442 passed, 21 failed, 9 skipped**, 1472 collected, 76.65 seconds, exit 1 | Eight stale quality-limit assertions, seven shared-input/outcome assumptions, five absent `full_day` fixture fields and one real missing normalized route-evidence artifact; no stopped-database cause |
| Affected correction selection | **273 passed**, 23.27 seconds | Trace, shared planning/quality/protection/routes/recovery and V3 B/multiround/Repair |
| Final combined backend | **1463 passed, 9 skipped**, 1472 collected, 73.46 seconds, exit 0 | No failure/error/xfail/xpass; disabled optional PostgreSQL tests |
| Frontend | **33 passed / 6 files**, 15.42 seconds | Lint, TypeScript and Vite build also passed |
| Fresh startup | All V0–V3 `--help` processes and six shared service exports succeeded | Startup compatibility, not live execution |

Final Ruff/diff checks passed; no later full run is claimed.
Configuration/content manifests and normalized hashes are local under
`logs/v3_final_engineering_closeout_20260925/`; raw historical logs and unrelated `.gitignore`,
thesis notes and unconfirmed evaluator work were excluded. Intermediate commits were
not independently certified checkpoints.

## Remaining evidence and research limits

Public access, admission, reservations and costs may stay UNKNOWN; verified whole-trip
expense accounting is unsupported. Legal primary visits may be unsuitable and different
IDs may represent experiential duplication. One visit/day is not two; completed targets
prove neither complete feasibility nor superiority over V2. Model/provider classification
can vary and the provider can preempt a non-travel classification.

The checkpoint closed approved engineering scope with no unresolved blocking divergence,
while preserving those limitations. Evaluation Readiness Audit was the proposed next
stage, not an execution started by closeout. Subsequent work requires a distinguishable
approved checkpoint; later changes do not retroactively validate earlier outputs.
