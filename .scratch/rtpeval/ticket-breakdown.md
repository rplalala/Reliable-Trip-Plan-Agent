# Evaluation implementation ticket breakdown — approved

Publication: Approved; 12 local tickets published; implementation not authorized.
Date: 2026-09-28

The user approved the 12-item granularity and dependencies. Individual tickets are published below. No task is claimed or implemented; the parent specification status remains unchanged.

## Sources and boundaries

Use the current [specification](spec.md), [closeout audit](closeout-audit.md), [artifact contract](artifact-contract.md), [evidence/time contract](evidence-time-contract.md), [metrics](metrics-contract.md), [score profile](score-profile.md) and [glossary](../../docs/evaluation_glossary.md). PROJECT.md remains implementation context; recheck relevant code at implementation time.

Each item delivers a narrow verifiable path, including its own data contract, behavior, report/interaction and offline acceptance checks. No separate horizontal schema/test/UI tickets are created. No broad prefactor is currently justified. CLI/local artifacts suffice unless a specific slice needs HTML; no new API or infrastructure is implied.

Ticket status describes specification readiness, not authorization or dependency completion. needs-info items name a bounded technical gate; resolve code/provider facts directly and ask the user only for decisions affecting result meaning. Dependent tickets cannot start until their listed blockers complete. All code, fixtures, real service calls, formal cases, experiment analysis, commits and freeze remain outside this documentation task.

Usage collection is an upstream supporting capability and cannot become evaluator-owned planner execution. Formal benchmark composition, qualification and iteration decisions remain outside these tickets. The future Codex comparison keeps the existing adapter boundary only; no harness ticket is proposed.

## Approved slices

### 01. Batch intake and independent schedule projection

**Blocked by:** None (subject to specification closure and separate implementation approval)

**Specification status:** needs-info

**What to build:** Submit a curated four-version batch and obtain either an immutable evaluation inventory or actionable intake diagnostics, without running or requalifying planners.

**Readiness gate:** Exact independent activity-role and transport/Transfer correspondence rules must be completed before implementation; use current artifacts and schema, not V3 lineage.

**Acceptance criteria:**

- [ ] Validate file hashes, full-input linkage, reviewed RequirementSpec, selected versions/runs and major schema versions; reject path escapes and do not silently drop groups.
- [ ] Preserve original result artifacts and stable source references. Expose itinerary data to quality readers separately from mechanism metadata.
- [ ] Treat generic no-POI items as transition/free time; preserve named unresolved visits and protected time; diagnose multi-POI blocks without guessing a split.
- [ ] Produce a traceable schedule/transport projection, with duplicate representations reconciled and ambiguous associations explicit.
- [ ] Offline fixtures demonstrate valid intake, malformed linkage, unavailable usage envelopes and missing optional draft handling; no runner or provider is invoked.

### 02. Symmetric usage capture and resource report

**Blocked by:** None (subject to specification closure and separate implementation approval)

**Specification status:** needs-info

**What to build:** An independently invoked planner attempt can produce linked usage observations and a resource report with comparable outer timing across V0-V3.

**Readiness gate:** Map actual token/provider-send hooks, stage boundaries and final resource capture at the implementation checkpoint. This is upstream instrumentation, not planner execution owned by Evaluation.

**Acceptance criteria:**

- [ ] Use common monotonic outer timing through final result and cleanup; retain stage scope and overlapping timing semantics.
- [ ] Capture actual model usage, provider sends, cache hits, retry events and missingness with event IDs; distinguish measured, reported, derived and estimated observations.
- [ ] Link usage to selected run and result hash; absent collection may be declared unavailable, never zero.
- [ ] Repair totals are subsets of underlying events; oracle usage has a separate ledger.
- [ ] Verify mocked success, retries, failure, cache hit, missing tokens and cleanup; instrumentation must not change planning decisions or require a real run.

### 03. Identity resolution, adjudication and grounding report

**Blocked by:** 01

**Specification status:** needs-info

**What to build:** Convert submitted venue references into independently evidenced identities, review queues and a grounding/ID-consistency report.

**Readiness gate:** Specify conservative automatic acceptance, role review and preselected audit sampling using development fixtures before implementing or enabling automatic acceptance.

**Acceptance criteria:**

- [ ] Name-only and supplied-ID references receive independent association checks; provider rank and ID retrieval alone cannot prove a match.
- [ ] Ambiguity, ID/name conflict and high-impact requirement matches enter adjudication; unresolved decisions retain reasons.
- [ ] Preserve claimed-ID conflict even when a reviewed named venue supplies downstream identity; do not rewrite planner output.
- [ ] Persist versioned review decisions and replay them; audit selection cannot depend on favorable version results.
- [ ] Fixtures cover branches, wrong cities, aliases, malformed candidates, wrong IDs and unavailable evidence; changing V3 findings cannot change grounding.

### 04. Independent snapshot acquisition and offline replay

**Blocked by:** 03

**Specification status:** needs-info

**What to build:** Acquire or replay a shared, versioned evidence snapshot for the batch venue union and each required directed route context.

**Readiness gate:** Specify bounded acquisition settings, retry/completeness behavior and persistence constraints; no live acquisition is authorized by ticket drafting or offline implementation.

**Acceptance criteria:**

- [ ] Include available V3 drafts when paired scoring is requested; union collection does not merge visit occurrences.
- [ ] Use evaluation-owned cache/evidence; preserve raw provider provenance, request context, retrieval times, failures and hashes.
- [ ] Route keys distinguish endpoints, direction, mode and departure context; do not substitute planner baseline evidence or reverse-leg estimates.
- [ ] Frozen snapshot replay performs no network calls; partial provider failures remain recorded rather than silently shrinking denominators.
- [ ] Mock acquisition demonstrates deduplication, missing matrix elements, retry accounting, corruption detection and deterministic replay.

### 05. Requirement and schedule metrics

**Blocked by:** 01, 03

**Specification status:** needs-info

**What to build:** Score reviewed obligations and schedule structure, and report date coverage, overlap, density and repetition from independent records.

**Readiness gate:** Finish supported time-operator boundaries and metric unit enumeration, including the non-overlap subscore; explicit counts must not be diluted by arbitrary extra subchecks.

**Acceptance criteria:**

- [ ] Support minimum/exact/date obligations and exclusions; possible unresolved matches can prevent definitive absence/count conclusions.
- [ ] Nearby never satisfies primary-visit obligations; minimum revisits are not automatically repetition violations.
- [ ] Report positive overlap pairs and union overlap time separately, without duplicate transport occupancy.
- [ ] Report density, repeat counts and date coverage descriptively rather than turning every sparse/overfull day into FAIL.
- [ ] Fixtures exercise touching intervals, multiple overlaps, unresolved identity and protected intervals; never infer new requirements from planner interpretation.

### 06. Opening checks from frozen evidence

**Blocked by:** 04

**Specification status:** ready-for-agent

**What to build:** Produce opening verdicts and supporting coverage/conflict measurements for applicable visits using offline snapshot evidence.

**Readiness gate:** No additional semantic blocker beyond upstream identity, snapshot and time contracts; independent parser fixtures remain part of implementation acceptance.

**Acceptance criteria:**

- [ ] Apply independent local-time interpretation, multiple/overnight periods and documented always-open encoding.
- [ ] Distinguish current/date-specific, regular fallback, known unresolved special date, closed, missing and invalid evidence.
- [ ] Require full containment with zero grace; end exactly at closing passes.
- [ ] Partial evidence may support a labelled conflict lower bound but cannot invent full outside minutes or complete coverage.
- [ ] Offline boundary/DST/truncation fixtures and an internal-finding mutation test establish evidence-driven results.

### 07. Same-day route checks from frozen evidence

**Blocked by:** 04

**Specification status:** needs-info

**What to build:** Produce route coverage, feasibility, cap violations and observed transfer burden for actual same-day transitions.

**Readiness gate:** Close deterministic continuous-interval/departure selection around protected time and explicit transport correspondence; no departure search optimization or silent date shifting.

**Acceptance criteria:**

- [ ] Exclude inter-day legs and confirmed same-canonical transitions as N/A; different venues at one address are not automatically identical.
- [ ] Use stated mode and valid returned Google duration including traffic fallback; successful explicit no-route is FAIL, errors/incomplete evidence UNKNOWN.
- [ ] Apply WALK distance/time cap, TRANSIT/DRIVE caps, DRIVE 600-second reserve, and independent 300-second cap/schedule tolerances without adding them together.
- [ ] Preserve fractional precision, raw overruns/deficits and partial observed subtotals; do not invent duration for no-route or add provider waiting twice.
- [ ] Fixtures cover tolerance boundaries, missing duration/distance, status/condition combinations and blockers; all scoring is offline.

### 08. Multimetric report and auxiliary scores

**Blocked by:** 05, 06, 07

**Specification status:** ready-for-agent

**What to build:** Export a reproducible four-version request-level quality report with the accepted five subscores and auxiliary total.

**Readiness gate:** No dependency on usage, human judgments or mechanism reports; missing optional tracks remain explicitly pending/unavailable.

**Acceptance criteria:**

- [ ] Compute verified score P/(P+F+U), coverage (P+F)/N and companion counts without turning UNKNOWN into FAIL.
- [ ] Apply one group-wide dimension mask; common N/A is omitted, individual no-check N/A contributes zero while raw rates remain N/A.
- [ ] Keep quality metrics, usage and human judgments separate; preserve mask/counts and do not claim a universal usefulness score.
- [ ] Export input/snapshot/rule hashes and availability; an empty mask returns a diagnostic, not an invented total.
- [ ] Fixture batch-to-report tests verify exact arithmetic, repeatability, no network, and invariance under changes to V3 internal findings; inferential analysis is outside this ticket.

### 09. Four-plan blinded ranking workflow

**Blocked by:** 01

**Specification status:** ready-for-agent

**What to build:** Generate a local anonymous HTML review package, save/import rankings and export researcher-side paired outcomes.

**Readiness gate:** Does not wait for automatic scores, Google acquisition or usage collection. Uses the shared source-preserving projection.

**Acceptance criteria:**

- [ ] Render original Input and uniform A/B/C/D plans; preserve meaningful uncertainty and hide versions, provenance, internal findings, scores and private mapping.
- [ ] Freeze balanced randomized assignments; sample/task count comes from supplied configuration, not module quotas.
- [ ] Support ties, unjudgeable/N/A and drafts separately for preference, pace and usefulness; every ranked label appears exactly once.
- [ ] Provide save/resume and explicit JSON export/import with revision validation and researcher-only mapping.
- [ ] Derive six correlated pair outcomes; hidden duplicates contribute consistency observations only. Verify metadata leakage and visually inspect renderer examples; no real rater session is authorized.

### 10. Independent V3 before/after report

**Blocked by:** 08

**Specification status:** needs-info

**What to build:** Score available draft/final pairs against one frozen snapshot and trace independent changes with visit-loss and regression context.

**Readiness gate:** Define activity correspondence, many-to-many edits and independent conflict/obligation tracking without using internal target IDs.

**Acceptance criteria:**

- [ ] Require both outputs; missing pair is unavailable, identical valid outputs can yield zero change.
- [ ] Track date, canonical identity, requirement obligation and source correspondence; target disappearance does not prove resolution.
- [ ] Report new conflicts, removed visits, coverage and denominator changes alongside score deltas.
- [ ] Keep pre-repair draft labelled as V3 draft, never an independent V2 run.
- [ ] Fixtures verify unchanged outputs, removed/replaced visits, unresolved mapping and newly introduced conflicts.

### 11. Controlled Repair replay and outcome report

**Blocked by:** 10

**Specification status:** needs-info

**What to build:** Replay separately supplied controlled fixtures through the real V3 Repair path and report independent target/control outcomes.

**Readiness gate:** Define target/control invariants, regression units, replay seams and frozen capability inputs. Formal case construction and real executions remain separately authorized benchmark work.

**Acceptance criteria:**

- [ ] Use real validator, target selection, scope, candidate preparation, acceptance and re-validation; never inject targets/scopes to bypass measured behavior.
- [ ] Freeze provider responses, candidate pool and capability configuration in offline replay; fail on unexpected live provider/model/DB access.
- [ ] Distinguish confirmed conflicts/product-policy violations from review opportunities using explicit fixture metadata; do not universally call sparse/duplicate/overfull a defect.
- [ ] Retain target-detection misses in denominators and report no-change/control regressions independently of patch acceptance.
- [ ] Support the accepted 24-target/8-control design without generating those formal cases here; use synthetic implementation fixtures only after coding approval.

### 12. Mechanism and official-evidence audit reports

**Blocked by:** 01

**Specification status:** needs-info

**What to build:** Export traceable internal mechanism observations and an audit queue for qualifying official facts, isolated from independent quality scores.

**Readiness gate:** Map exact round/target/acceptance denominators and accepted/exposed/rule-used fact provenance at the implementation checkpoint; absent signals must remain unavailable.

**Acceptance criteria:**

- [ ] Mechanism metadata has a separate reader; it cannot change quality judgments or identity decisions.
- [ ] Distinguish trigger, acceptance, round progression and internal target status from independently measured resolution.
- [ ] Official audit includes Evidence-Gate-accepted facts exposed to the model or used by a rule; no claim of causal LLM use or random website cross-check.
- [ ] Attach existing linked usage where available; do not depend on completed usage collection or invent missing stage costs.
- [ ] Fixtures cover rejected/unexposed facts, exposed/rule-used facts, missing trace and duplicate round records; output includes provenance and audit availability, not fabricated official truth.

## Published tickets

| Ticket | Blocked by | Status |
| --- | --- | --- |
| [01: Batch intake and independent schedule projection](issues/01-batch-intake-projection.md) | None | needs-info |
| [02: Symmetric usage capture and resource report](issues/02-usage-capture-report.md) | None | needs-info |
| [03: Identity resolution, adjudication and grounding report](issues/03-identity-adjudication.md) | 01 | needs-info |
| [04: Independent snapshot acquisition and offline replay](issues/04-evidence-snapshot.md) | 03 | needs-info |
| [05: Requirement and schedule metrics](issues/05-requirement-schedule-metrics.md) | 01, 03 | needs-info |
| [06: Opening checks from frozen evidence](issues/06-opening-checks.md) | 04 | ready-for-agent |
| [07: Same-day route checks from frozen evidence](issues/07-route-checks.md) | 04 | needs-info |
| [08: Multimetric report and auxiliary scores](issues/08-quality-report-scores.md) | 05, 06, 07 | ready-for-agent |
| [09: Four-plan blinded ranking workflow](issues/09-blinded-ranking.md) | 01 | ready-for-agent |
| [10: Independent V3 before/after report](issues/10-v3-pre-post.md) | 08 | needs-info |
| [11: Controlled Repair replay and outcome report](issues/11-controlled-repair.md) | 10 | needs-info |
| [12: Mechanism and official-evidence audit reports](issues/12-mechanism-official-audit.md) | 01 | needs-info |

Nine tickets retain needs-info; 06, 08 and 09 are specification-ready but still blocked by dependencies. No implementation is authorized. Subsequent specification closure should start with 01's role/transport correspondence; 02's usage hook mapping is an independent supporting task. Human ranking does not wait for Google or scoring. Quality reporting does not wait for usage, Controlled Repair or mechanism reports.

## Approval and clarification record

2026-09-28: The user approved all 12 items and blocking edges. Published individual tickets without changing the parent specification or starting code, fixtures or experiments. Usage reporting includes researcher-facing descriptive comparisons for later thesis/presentation discussion; it is neither a new non-blind rating task nor part of the itinerary quality total. Actual analysis and thesis writing remain outside this task.

## Specification closure and resume boundary — 2026-09-28

The user approved the 12-ticket granularity/dependencies and requested a documentation checkpoint before taking a break. Ticket 01 closure has not started; no ticket is claimed. Resume with its specification closure only after the user resumes work, not with implementation.

needs-info denotes a bounded missing technical definition, not necessarily a question awaiting the user. Before implementing each ticket, inspect current relevant code, resolve factual gaps, document the contract and acceptance criteria, and ask the user only about unresolved choices affecting result meaning. Settle cross-cutting rules before dependent implementations. Waiting for another ticket is expressed by Blocked by; specification readiness does not remove that dependency or grant implementation authorization.

The next intended work is Ticket 01's independent activity-role classification, transport/Transfer correspondence and source linkage. Do not decide those details during this pause checkpoint. Usage capture remains a supporting prerequisite for usable resource comparisons, not a prerequisite for itinerary quality scoring or blinded review.
