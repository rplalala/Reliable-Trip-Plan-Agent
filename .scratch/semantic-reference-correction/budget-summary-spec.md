# Independent compact budget summary

Approved 2026-09-27 by acceptance of the V3 offline audit recommendation. Implement with
TDD and independent review; no live, commits, API budget changes or quantity Repair changes.

Write budget.json alongside run.json whenever file tracing finalizes. It is independent of
the aggregate payload truncation limit and has its own 64 KiB bound. Keep run identity,
configuration hash, final status, final primary tool counters/limits, and separate semantic,
RAG, Repair, Nearby and primary-generation numeric observations and configured limits.
Include per-call reported usage where already observed; explicitly mark unavailable usage
as missing rather than zero. Requirements and primary-generation billed usage are not
newly instrumented by this task and must remain missing when not available.

Reuse existing runtime events and final budget.summary(), without issuing requests or
changing planning decisions. Cumulative snapshots replace earlier snapshots; call/round
identities deduplicate repeated events. Do not combine separate primary/RAG/Repair pools.
Keep raw provider content, user text, itinerary, model labels and credentials out of this
numeric allowlisted artifact. At most 32 call/round records per tracked stage; any dropped
records explicitly mark collection incomplete. An exceptional size overflow produces an
explicit incomplete marker, not a seemingly complete truncated JSON. Budget write failure
must not prevent ordinary final trace writing or change the planning result. Atomic rename
prevents treating a partial pending write as the final budget artifact.

Approved test seams are the public FileRunTracer event/finish artifact boundary and actual
V3 graph with mocked external services. Verify forced aggregate truncation, repeated-event
deduplication, separate pools, missing usage, allowlisting, capacity limits, failed runs and
write failures. Complete full backend regression and Standards/Spec review before reporting.
This records application budgets, not a provider invoice or proof of uninstrumented sends.

## Offline completion checkpoint

The truncation test first failed because no budget.json existed, then passed with an
independent numeric summary. A deduplication/stage test failed before event collection was
added. A simulated budget-file write failure then exposed coupling to ordinary finish
(run.json remained running); separate best-effort atomic summary writing fixed it.
Public-boundary tests also cover filtering private fields, the record cap and the actual
mocked-external-service V3 graph with deliberately truncated run.json.

Full backend regression passed 1726 tests with 9 skipped (78.61 seconds). Independent
Standards review found no actionable issues. Spec review found one P2 omission: rag_cancelled
and resolution_attempts were not collected. A new test reproduced the missing counter;
the fix passed 63 trace/RAG/V3 wiring tests (7.96 seconds). Scoped lint/format checks pass.
Independent Spec re-review closed the P2; both review axes have zero remaining findings.
No API budget, planning policy, quantity Repair algorithm, live call or commit changed.
This artifact is written when the existing tracer finish boundary is invoked; cancellation
paths that never call finish are not newly finalized by this change. Requirements and main
generation usage remain missing until a separately scoped producer exposes those metrics.
