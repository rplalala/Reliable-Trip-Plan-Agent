# Existing embedding timeout test repair acceptance

Date: 2026-10-02, Australia/Sydney. Base HEAD:
3427784b87d5864aba25dcba8b48430ec4de9dac on feature/evaluation, plus inherited
uncommitted Ticket 07 implementation/docs and the approved diagnosis record.
Current status: test-only repair implemented and validated; targeted checks and both
review axes pass; unfiltered full offline backend regression passes. The separately
approved local closeout commits the test repair at b18daef; nothing has been pushed.

## Approved and implemented scope

The user approved the concrete [proposal](fix-proposal.patch) after the
[diagnosis](diagnosis.md). Only the affected function in
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

## Actual red, correction and verification

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

## Independent code review

Fixed point: HEAD 3427784b; scoped working diff command:
`git diff 3427784b87d5864aba25dcba8b48430ec4de9dac -- backend/tests/tripworld/test_runtime_retrieval.py`.
No new commits. Both reviewers read the approved proposal/current diagnostic scope.

**Standards:** no documented breach or actionable smell. Changes stay in the approved
single function, use existing mocks, bound asynchronous waits and clean up owned tasks.
**Spec:** no missing requirement, implementation error or scope expansion. The outer
watchdog sits outside pytest.raises, so its TimeoutError is not accepted as the intended
embedding timeout. Original assertions and production configuration remain unchanged.
Both reviews were read-only; test results above are primary-agent observations.

## Evidence, limitations and cleanup

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

## Repair validation closeout before Git approval

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

## Subsequent approved local commit closeout — 2026-10-02

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
