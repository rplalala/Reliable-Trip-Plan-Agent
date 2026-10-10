# Embedding timeout test diagnosis and repair

2026-10-02. Status: test-only repair Implemented and offline Validated after an initial
diagnosis-only checkpoint. Base: `3427784b87d5864aba25dcba8b48430ec4de9dac`.
The approved [proposal](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/41#issuecomment-5956258516)
changed only `test_httpx2_embedding_timeout_and_cancel_close_owned_client` in
`backend/tests/tripworld/test_runtime_retrieval.py`. RuntimeRetrieval, usage hooks,
production configuration, dependencies and V0–V3 behavior were unchanged.

## Confirmed failure and negative probes

The original timeout parameter started a **20-ms** deadline, then waited indefinitely
for mock-handler entry before observing its child embedding task. The deadline could
finish that task before the handler set the event, leaving an unconsumed TimeoutError
and a permanently waiting test.

Installed OpenAI 3.13.0 lazily constructs `client.embeddings` and gathers platform
metadata before reaching the mock transport. Independent resource-property measurements
were **641.578ms cold / 0.001ms warm**. An instrumented original test recorded deadline
start at 45.009ms and platform work beginning at 1327.075ms: **1282.066ms** of request
preparation before that await boundary in this probe. These are bounded local diagnostic
observations, not a performance benchmark or general SDK latency guarantee.

The elapsed 20ms deadline cancels the task at the subsequent await. The embedding task
finishes with TimeoutError before the handler sets its event. The test remains waiting
indefinitely and never reads that task's result; the bounded repro also reports an
unretrieved task exception. SDK cold initialization is the trigger, and the unbounded
handler-only handshake is the test defect. Runtime cancellation did occur; no Retrieval
or usage-hook defect was demonstrated. Synchronous initialization cannot be preempted
by an asyncio deadline, so this does not establish a strict wall-clock timeout guarantee.

The cancel parameter runs second in the same process and passes after SDK resources
are warm. That explains the observed cold-process/order sensitivity; it does not prove
every prior full-suite ordering will reproduce the problem.

| Probe | Observed result |
| --- | --- |
| Original unchanged test, two-second outer diagnostic watchdog | Twice: 1 failed / 1 passed / 14 deselected; timeout parameter stopped at entered.wait; embedding already had TimeoutError |
| Minimal real SDK + HTTPX2 mock, without Retrieval/DB/usage hooks | Handler never entered; embedding task was done with TimeoutError; reproduction failed within the one-second handshake bound |
| Minimal mock with diagnostic SDK deadline 1 second | Handler entered at 718.743ms; no network used |
| Original test with platform information prewarmed | Still 1 failed / 1 passed; warming only metadata is insufficient |
| Original test with a constant platform-function stub | Still 1 failed / 1 passed; request preparation preceding metadata also matters |
| Original test using Windows Selector event-loop policy | Same 1 failed / 1 passed; switching policy does not resolve it |
| SDK body transformation measured alone | 0.339ms cold / 0.044ms warm; this isolated transformation does not explain the measured large preparation delay |
| Timeout branch directly awaiting its task, still at 20ms | Terminates with an assertion failure rather than hanging: the expected HTTP attempt has not occurred |
| In-memory candidate with bounded waits and test-only 5-second deadline | First 2 passed / 14 deselected in 7.32s; after explicit child cleanup, 2 passed / 14 deselected in 6.85s |

The minimal real-SDK/MockTransport reproduction excluded Retrieval, DB and usage hooks.
Warm metadata, a constant platform stub and Selector loop policy did not fix the hang.
HTTPX 2 incompatibility was contradicted by successful entry at the longer deadline.
The confirmed defect was the unbounded test handshake, not a demonstrated production
retrieval/usage defect. All probes used synthetic credentials and MockTransport.

## Applied repair and distinct validation checkpoints

Timeout now awaits the embedding task directly; caller cancellation bounds handler-entry
waiting to three seconds. Final cleanup cancels/consumes the child, with a ten-second
scenario watchdog. The five-second **test-only** deadline permits measured cold setup
before testing in-flight timeout, retaining single-send, HTTP metadata, diagnostic and
owned-client-close assertions. It adds about five seconds to the timeout case. The outer
watchdog is outside `pytest.raises`, so its failure cannot pass as the intended timeout.

| Checkpoint | Observed result | Scope |
| --- | --- | --- |
| Actual original source, 12-second outer watchdog | **1 failed, 1 passed, 14 deselected**, 15.76 seconds | Bounded reproduction, no in-memory patch |
| Same loop after actual source repair | **2 passed, 14 deselected**, 8.24 seconds | No unconsumed child exception |
| Fresh timeout parameter | **1 passed**, 8.47 seconds | Direct pytest without warming/stubs |
| Fresh cancel parameter | **1 passed**, 5.39 seconds | Separate process |
| Retrieval module | **16 passed**, 9.96 seconds | Both repaired branches included |
| Full unfiltered offline backend | **2234 passed, 10 skipped**, 196.39 seconds; zero deselections | Nine database opt-ins disabled, one symlink privilege skip |
| Later route/schedule/retrieval closeout | **166 passed**, 34.26 seconds | Overlapping affected selection |

Standards/Spec reviews found no actionable issue or scope expansion; Ruff/compilation
and production-file diff checks passed. Earlier Ticket 07's **2232/10/2-deselected**
gate remained a separate historical result, not rewritten as the new full pass.
Repair commit: `b18daef4af2fecba36d7b84315c8946a772aeae8`; route closeout was separately
`2b66c9f889ca8964f97dbc67b2a601ebb56be64c`. The original diagnosis proposal preceded
approval/application; it is not a patch to reapply.

## Evidence and reproducibility limits

Local diagnosis/repair evidence is under
`thesis_notes/evaluation/debug/2026-10-02-embedding-timeout/`: `reproduce.py`,
`minimal.py`, `check_repair.py`, `repair-red.log`, `repair-green.log`, `repair-false.log`,
`repair-true.log`, `repair-module.log`, `repair-full-regression.log` and original probe logs.
No diagnostic instrumentation was added to source. The original two-second wrapper
intentionally reproduces RED and is too short for the repaired five-second fixture;
`check_repair.py` uses the actual repaired source and longer watchdog. Published source
permits direct pytest of the named function/module without that ignored archive.

Asyncio cannot preempt synchronous SDK initialization or arbitrary blocking cleanup.
These are cooperative async wait bounds, not strict wall-clock guarantees on every host.
Synthetic verification establishes test behavior, not live provider availability,
performance guarantees or formal evaluation results. No real model/network/database
supplement or full-suite pass was claimed during diagnosis alone.
