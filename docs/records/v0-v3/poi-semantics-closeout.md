# POI semantics and quantity-review acceptance

September 2026. Status: approved engineering closeout, not a version freeze or benchmark.
Current rules belong to [requirements/evidence](../../0002-requirements-evidence.md) and
[validation/repair](../../0005-validation-repair(v3).md). This record separates semantic
interpretation, captured pilot results, Product propagation and the later review-policy change.
The original [implementation record](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/a6aff13a00af35467b9c88ec2906d10a96095f04/docs/shared_poi_semantics_plan.md)
retains the earlier source history.

## Semantic meaning and completion corrections

The delivery distinguished ordinary interests, source-grounded category goals, exact/
minimum counts, distinct dates and primary-role exceptions. Named revisits used
`VisitRequirement` without a duplicate unsupported-hard semantic obligation. Request-owned
candidate assessment added role/goal/provenance support; four Spec corrections unified
canonical counting across labels, enforced category count/date goals, propagated named
completion and prioritized explicit goals within existing supply capacity.

The first live batch stopped on transport dependency failure. A separately authorized
batch completed A (**8 distinct visits**) and B (**exact two museums on different dates,
at least two parks**), then stopped C at unsupported-hard interpretation. After named-
visit routing correction, C completed British Museum exactly twice on different dates,
with complete policy status and no duplicate hard semantic obligation.

D initially stopped at rich-trip ambiguity. Prompt 16 retained ordinary rich wishes as
soft meaning. Its next attempt passed interpretation but failed semantic evidence-reference
validation; semantic prompt 2 required exact same-candidate references, with bounded
capture and prompt-aware cache identity. The dual-capture retest completed **14 distinct
visits** and **four quantity gaps**. Repair had not run because quantity review was off,
not because rounds were exhausted. This was accepted semantics, not complete trip quality.

## Product completion and review-policy changes — 2026-09-26

The Product route rebuilt only three legacy fields, losing policy-completion/reason values
in JSON and SSE. Correction converts the complete allowlisted Product result, excludes
runtime diagnostics and displays adopted incomplete itineraries with an unmet-requirements
message. Request `completed` remains distinct from policy completion. Four API regressions
failed before correction; complete/incomplete/unassessed JSON/SSE and page checks passed
without changing the strict frontend transport parser.

Quantity was still disabled during that API checkpoint; the captured D override did not
change production. The later approved policy enabled default V3 quantity review for
Product/Dev and removed the obsolete `repetition_review_enabled` schema/target/report key.
Overfull stayed false; explicit disabling remained possible. Confirmed unauthorized
repeat correction, lawful count/date revisits and UNKNOWN protections were retained.
The complete comparison pool was already wired into Repair; no new selection policy,
London/date rule, budget or local-operation authority was introduced. Shared interpretation
applies to V0–V3, candidate judgments to evidence-bearing versions, Repair to V3.
Custom YAML had to remove the obsolete key; cached backend configuration required restart.
Old typed snapshots retain their historical code for replay.

## Latest D quantity pilot

Run `8ebe8b6a-6a62-4e98-806b-b2efbc21807f`, London October 1-8, one traveler, AUD3000,
unchanged mountain/zoo/rich-trip input. One authorized run, exit0, 183.844 seconds.
The newly generated itinerary had three gaps (October 3/7/8), distinct from the prior D
sample's four dates. Two Repair rounds added three visits, from15 to18 distinct canonical
IDs. Final daily counts: **3/3/2/2/2/2/2/2**. Original activities remained unchanged.

Two additions came from the comparison pool and one from unused selected supply. Repair
reused37 qualified candidates, with no new search, Details, embedding, retrieval or semantic
calls. Usage was2/5 Repair model calls,18/24 route sends and18/32 elements; request-wide
semantic usage stayed2/6 calls and36.478/120 seconds. The existing limits/defaults were not
changed. Two requirement records, six semantic records and a1,395,829-byte Repair snapshot
were captured; typed offline replay and14 acceptance checks passed. Final findings include
22 PASS and26 UNKNOWN, with no confirmed violation or unresolved quantity-review target.

Evidence is local and ignored: `artifacts/poi_semantics_acceptance/20260926_D_quantity_review/`.
Its `report.md`, `checks.json`, `execution.json` and `offline_replay.json` provide the bounded
observations. Raw captures are not proposed for Git. This development pilot is not a benchmark
or a controlled comparison with the earlier D generation.

## Bounded validation checkpoints

| Checkpoint | Observed result | Scope and causal qualification |
| --- | --- | --- |
| Initial Spec fixes | **1590 passed, 9 skipped, 1 failed**, then **1591 passed, 9 skipped** | Old fixture violated confirmed-repeat priority; corrected fixture retained its loss assertion |
| Named C routing | **1602 passed, 9 skipped** | Before separate C live revalidation |
| Prompt 16 ambiguity | **1611 passed, 9 skipped** | Nine controlled interpretation regressions; before D reference failure |
| Semantic/capture corrections | **1625 passed, 9 skipped** | Partial-write capacity and telemetry-stability corrections |
| Quantity capture/replay | **1640 passed, 9 skipped**, 75.77 seconds; focused V3 **421 passed** | Includes 15 added package tests; typed replay no provider/model calls |
| Product propagation | **1646 passed, 9 skipped**, 80.96 seconds; frontend **59 passed / 8 files** | JSON/SSE and incomplete-state fixes; TypeScript/Vite/scoped Ruff passed |
| Default review policy | **1648 passed, 9 skipped**, 72.84 seconds | Migration regressions retain repeat/legal/UNKNOWN safeguards; frontend unchanged, prior gate reused |

An interrupted default-policy run stalled near retrieval timeout/cancellation tests;
isolated retrieval **16 passed** and the fresh full gate passed with no timeout report.
No retrieval code changed. Checkpoints overlap and are not additive. Backend Ruff and
changed-file compilation passed; earlier frontend **56/8** was superseded by the 59-test
correction gate, not new evidence of deployed/live Product behavior.

## Offline integration and source provenance

The approved integration exercised real Product/Dev routing, Vite proxy, FastAPI SSE,
services, RequestPlannerRuntime and independent version runners; only external collaborators
were synthetic. Product displayed the default-on quantity addition and incomplete warning;
Dev completed all four flows with quantity=true, overfull=false, no obsolete repetition
field and an `ACCEPTED_PARTIAL` fixture. All business cases passed first submission;
setup corrections were not retried business requests. Temporary processes were stopped.
Local evidence: `artifacts/offline_integration_20260926/`.

The exported candidate tree initially lacked local virtualenv/tokenizer assets, yielding
**30 failed, 1578 passed, 9 skipped**. With those unchanged dependencies supplied, backend
passed **1608, 9 skipped**, 72.92 seconds; the separate tooling group passed **40**, 6.47
seconds. Implementation hashes matched the 1648-pass workspace. These subset gates do
not sum into another full run. Reviewed revisions were `0652222`, `014c726`, `29647ef`,
`9c910b2`, `40b0b26`; all 105 inventoried files were committed at that closeout.

## Decisions and limitations

Penguin Beach is an internal exhibit and London Zoo its parent, not identical names.
Visiting the exhibit then other areas can be reasonable. The user declined further work;
that relationship alone established no defect or open blocker. P3 pending-reason heuristic
remained deferred. UNKNOWN access/hours/suitability/cost remained UNKNOWN; indoor climbing
was labelled a related alternative, not actual mountain climbing. Quantity success does
not establish richness, feasibility, stable interpretation or a controlled comparison
with the earlier regenerated D output.
