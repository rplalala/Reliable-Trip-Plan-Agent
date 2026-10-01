# Existing embedding timeout test diagnosis

Date: 2026-10-02, Australia/Sydney. Original checkpoint: diagnosis only, repair proposed.
The user subsequently approved repair; actual source is now corrected and targeted tests
and reviews pass. See [repair acceptance](repair-acceptance.md) for current verification.
Base HEAD: 3427784b87d5864aba25dcba8b48430ec4de9dac on feature/evaluation, with
the inherited uncommitted Ticket 07 implementation/docs. User scope: offline diagnosis.
No backend implementation or runtime budget, credential or dependency changed. The
subsequent repair changes only the approved test function; pending-approval/source-unchanged
statements below describe the original diagnostic checkpoint.

## Confirmed failure chain

The affected test is
`backend/tests/tripworld/test_runtime_retrieval.py::test_httpx2_embedding_timeout_and_cancel_close_owned_client`.
Its timeout parameter begins a 20ms Retrieval deadline, then unconditionally waits for
the HTTPX2 mock handler's `entered` event before observing the embedding task.

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

## Actual reproduction and falsification

First bounded invocation needed a repository-local basetemp parent; two setup errors
preceded reproduction and are not counted as hang evidence. After that correction:

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

Ranked hypotheses were presented before probes. SDK cold request preparation was confirmed;
the narrower platform-only explanation was refined after negative probes. HTTPX2 transport
incompatibility was contradicted by successful handler entry and passing candidate checks.
Windows event-loop policy did not explain the failure. No real HTTP/model/database call
was made: all requests used the existing MockTransport and synthetic credentials.

## Proposed bounded repair

[Concrete patch](fix-proposal.patch) changes only the affected function in
`backend/tests/tripworld/test_runtime_retrieval.py`:

1. Timeout branch observes the embedding task directly, without waiting for handler entry.
2. Cancellation branch bounds handler-entry waiting to 3 seconds.
3. Finally cancel/consume any unfinished child task; bound the entire scenario to 10 seconds.
4. Increase this test's synthetic embedding deadline from 0.02 to 5 seconds so the
   intended in-flight HTTP timeout remains testable despite observed cold setup. Existing
   no-retry, attempt/diagnostic and owned-client-close assertions are retained.

The larger limit applies only to the fixture, not config/runtime.yaml or V2/V3 production.
It adds approximately five seconds to this timeout test, with no provider cost. A limit
of one second was observed to permit one minimal request but is below another measured
1.28-second setup; five seconds gives headroom without complex fake-deadline machinery.
Bounds and assertions still fail visibly if setup exceeds the allowance; no hang is masked
as PASS. This is a tested candidate, not an applied repair. Scope approval is required.

After approval: apply the single-test-function patch; rerun both parameters in fresh
processes and all 16 runtime retrieval tests, review the test diff, and rerun the complete
offline backend suite without Ticket 07's two deselections. Database opt-ins remain disabled;
no native privilege supplement, live call, Git action, freeze or Ticket 08 is included.

## Evidence preservation and limits

Historical debug harnesses are retained under
`thesis_notes/evaluation/debug/2026-10-02-embedding-timeout/`, deliberately ignored and
not fresh-checkout dependencies. `reproduce.py` bounds the original unchanged tests and
supports isolated probes/in-memory candidate; `minimal.py` removes application concerns.
Both are clearly diagnostic, and DEBUG-timeout-diag instrumentation was never added to
backend source. The archive record preserves the exact scope, observed results and
the distinction between a proposed repair and implementation. No full-suite run or final
repair acceptance is claimed for this diagnosis-only task.

Local reproduction commands from the repository root (ignored archive must be present):

```powershell
.venv/Scripts/python.exe thesis_notes/evaluation/debug/2026-10-02-embedding-timeout/reproduce.py
.venv/Scripts/python.exe thesis_notes/evaluation/debug/2026-10-02-embedding-timeout/reproduce.py --candidate
```

The first intentionally returns RED when the original test hangs; the second runs only
the in-memory patch and leaves the actual test source untouched. Preserve distinct
diagnostic versus repair acceptance status when using these commands.

Final checks: the archived original-repro command again returned 1 failed / 1 passed /
14 deselected in 5.87s; its log is preserved beside the harness. The first proposal patch
check failed because normalized LF context did not match the Windows checkout; preserving
the existing line endings corrected it, and `git apply --check` now passes. The patch
was not applied. Git content checks confirm runtime.py, usage.py and the affected test
remain unchanged. Generated diagnostic fixtures were removed; no debug instrumentation
was added to backend source and no bounded probe remains running.
