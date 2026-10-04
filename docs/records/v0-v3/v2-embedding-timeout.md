# Embedding Timeout

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="timeout-test-diagnosis-diagnosis"></a>

<a id="timeout-test-diagnosis-diagnosis--existing-embedding-timeout-test-diagnosis"></a>

## Existing embedding timeout test diagnosis

Date: 2026-10-02, Australia/Sydney. Original checkpoint: diagnosis only, repair proposed.
The user subsequently approved repair; actual source is now corrected and targeted tests
and reviews pass. See [repair acceptance](v2-embedding-timeout.md#timeout-test-diagnosis-repair-acceptance) for current verification.
Base HEAD: 3427784b87d5864aba25dcba8b48430ec4de9dac on feature/evaluation, with
the inherited uncommitted Ticket 07 implementation/docs. User scope: offline diagnosis.
No backend implementation or runtime budget, credential or dependency changed. The
subsequent repair changes only the approved test function; pending-approval/source-unchanged
statements below describe the original diagnostic checkpoint.

<a id="timeout-test-diagnosis-diagnosis--confirmed-failure-chain"></a>

### Confirmed failure chain

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

<a id="timeout-test-diagnosis-diagnosis--actual-reproduction-and-falsification"></a>

### Actual reproduction and falsification

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

<a id="timeout-test-diagnosis-diagnosis--proposed-bounded-repair"></a>

### Proposed bounded repair

[Concrete patch](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/41#issuecomment-5956258516) changes only the affected function in
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

<a id="timeout-test-diagnosis-diagnosis--evidence-preservation-and-limits"></a>

### Evidence preservation and limits

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

<a id="timeout-test-diagnosis-repair-acceptance"></a>

<a id="timeout-test-diagnosis-repair-acceptance--existing-embedding-timeout-test-repair-acceptance"></a>

## Existing embedding timeout test repair acceptance

Date: 2026-10-02, Australia/Sydney. Base HEAD:
3427784b87d5864aba25dcba8b48430ec4de9dac on feature/evaluation, plus inherited
uncommitted Ticket 07 implementation/docs and the approved diagnosis record.
Current status: test-only repair implemented and validated; targeted checks and both
review axes pass; unfiltered full offline backend regression passes. The separately
approved local closeout commits the test repair at b18daef; nothing has been pushed.

<a id="timeout-test-diagnosis-repair-acceptance--approved-and-implemented-scope"></a>

### Approved and implemented scope

The user approved the concrete [proposal](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/41#issuecomment-5956258516) after the
[diagnosis](v2-embedding-timeout.md#timeout-test-diagnosis-diagnosis). Only the affected function in
backend/tests/tripworld/test_runtime_retrieval.py changes executable repository content:

- Timeout branch directly observes its embedding task rather than first waiting for
  the mock handler event, which may never occur after a request-preparation timeout.
- Caller-cancel branch waits at most three seconds for handler entry before cancellation.
- Finally cancel and consume the child task; bound the entire scenario to ten seconds.
- Use a five-second synthetic test deadline, allowing observed SDK cold initialization
  before testing an in-flight timeout. Retain all single-send, HTTP metadata, diagnostic
  and owned-client-close assertions. This adds about five seconds to the timeout case.

RuntimeRetrieval, usage hooks and config/runtime.yaml have zero content diff from HEAD.
No V0-V3 behavior, production budget or dependency changed. No real provider/model/database,
native privilege check, formal experiment, Git action, freeze or Ticket 08 is included.
The repaired test's HTTP requests use only the existing HTTPX2 MockTransport and fake keys.

<a id="timeout-test-diagnosis-repair-acceptance--actual-red-correction-and-verification"></a>

### Actual red, correction and verification

The original diagnosis preserved repeated failures caused by an unbounded entered.wait
after the embedding task had already returned TimeoutError during SDK cold preparation.
To validate the actual repair with the same command before and after, a separate archived
feedback loop uses a twelve-second outer watchdog, long enough for the approved five-second
fixture deadline and ten-second scenario watchdog. It does not inject a candidate patch.

1. Actual original test, before source edit: **1 failed / 1 passed / 14 deselected in
   15.76s**. Failure is the bounded reproduction of the indefinite handshake; the
   embedding task already finished with TimeoutError, leaving an unconsumed exception.
2. Apply only the approved test-function patch. The same actual-source loop becomes
   GREEN: **2 passed / 14 deselected in 8.24s**, without the unconsumed task exception.
3. Separate fresh process, timeout parameter alone: **1 passed in 8.47s**. Separate
   fresh process, caller-cancel parameter alone: **1 passed in 5.39s**. These use direct
   pytest invocations, not the diagnostic wrapper or SDK warming/stubbing.
4. Entire runtime retrieval module: **16 passed in 9.96s**. Backend Ruff and changed-test
   compilation pass; production runtime/usage/config diff checks show no change.
5. Unfiltered full offline backend result: **2234 passed / 10 skipped in 196.39s**, with
   **zero deselections** and both repaired parameters included. No -k exclusion was used.
   Nine skips are opt-in real PostgreSQL checks disabled by TRIPWORLD_TEST_DATABASE=0;
   one is the host symlink-privilege case. No prior Ticket 06 native/database supplement
   is counted as this repair's validation. The earlier Ticket 07 2232/10/2-deselected
   gate remains a separate historical result rather than being rewritten as this run.

<a id="timeout-test-diagnosis-repair-acceptance--independent-code-review"></a>

### Independent code review

Fixed point: HEAD 3427784b; scoped working diff command:
`git diff 3427784b87d5864aba25dcba8b48430ec4de9dac -- backend/tests/tripworld/test_runtime_retrieval.py`.
No new commits. Both reviewers read the approved proposal/current diagnostic scope.

**Standards:** no documented breach or actionable smell. Changes stay in the approved
single function, use existing mocks, bound asynchronous waits and clean up owned tasks.
**Spec:** no missing requirement, implementation error or scope expansion. The outer
watchdog sits outside pytest.raises, so its TimeoutError is not accepted as the intended
embedding timeout. Original assertions and production configuration remain unchanged.
Both reviews were read-only; test results above are primary-agent observations.

<a id="timeout-test-diagnosis-repair-acceptance--evidence-limitations-and-cleanup"></a>

### Evidence, limitations and cleanup

Ignored archive: thesis_notes/evaluation/debug/2026-10-02-embedding-timeout/ contains
check_repair.py, repair-red.log, repair-green.log, repair-false.log, repair-true.log,
repair-module.log and repair-full-regression.log. The earlier diagnosis probes and notes
remain dated history; their two-second diagnostic wrapper is not the current repair loop.
The repair loop invokes only actual source, with no private SDK stub or warming probe.

Current local feedback command (requires the ignored archive):

```powershell
.venv/Scripts/python.exe thesis_notes/evaluation/debug/2026-10-02-embedding-timeout/check_repair.py
```

The earlier diagnosis-only reproduce.py uses a two-second wrapper and is historical;
it is deliberately too short for the repaired five-second fixture and must not be used
as a post-repair acceptance command. Direct pytest/module/full commands are the gates.

Asyncio timeouts cannot preempt synchronous SDK initialization or arbitrary blocking
cleanup; these are bounds on cooperative asynchronous waiting, not strict wall-clock
guarantees under every SDK/host failure. Synthetic tests establish implementation behavior,
not live provider availability or formal evaluation results. Prior Ticket 07 filtered and
pre-boundary unfiltered checkpoints remain historical; this new gate is reported separately.
Research archive updates are historical evidence, not project authority or fresh-checkout assets.

<a id="timeout-test-diagnosis-repair-acceptance--repair-validation-closeout-before-git-approval"></a>

### Repair validation closeout before Git approval

GitHub Issue #19 and parent Issue #12 received the approved repair supplement and were
read back successfully. Issue #19 remains closed/completed; parent #12 remains open.
The earlier filtered Ticket 07 checkpoint is preserved as history. No issue state,
assignment, label, later-ticket scope or Git publication was changed.

All six repair logs were checked before removing the five generated pytest roots:
timeout-test-repair-targets, timeout-test-repair-false, timeout-test-repair-true,
timeout-test-repair-module and timeout-test-repair-full under .scratch/.
The diagnosis/acceptance documents and archived evidence remain available.
Final diff checks found no whitespace errors, no production-file changes for this repair,
no diagnostic instrumentation in backend source, and no staged changes.
HEAD remains 3427784b87d5864aba25dcba8b48430ec4de9dac on feature/evaluation.
The working tree retains the uncommitted Ticket 07 implementation plus this approved
test/documentation repair; no commit was created. Documentation-only closeout did not
require repeating the successful code validation.

<a id="timeout-test-diagnosis-repair-acceptance--subsequent-approved-local-commit-closeout--2026-10-02"></a>

### Subsequent approved local commit closeout — 2026-10-02

The user explicitly approved Ticket 07 closeout in three logical groups. Route code/tests
are committed at 2b66c9f889ca8964f97dbc67b2a601ebb56be64c. The independent single-function
test repair is committed at b18daef4af2fecba36d7b84315c8946a772aeae8 with message
`test: bound embedding timeout and cancellation checks`. This record, the permanent
diagnosis and exact proposal belong to the third documentation group, not a source
repair or generated runtime artifact. Earlier no-Git statements retain their original
diagnosis/implementation/validation scope and are superseded only by this later approval.
The proposal is an already-applied historical patch, not an instruction to reapply it.

Before committing, the combined route/CLI, shared requirement/schedule and runtime
retrieval subset passed **166 tests in 34.26s**; backend Ruff and diff checks passed.
The earlier unfiltered 2234/10/zero-deselection gate is unchanged. No production code,
runtime limit, dependency, live/database/native supplement, push, freeze or Ticket 08
work was introduced. Ignored probes/logs remain local evidence and are not staged.
