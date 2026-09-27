# Semantic contract correction: authorized live revalidation

Prepared 2026-09-27 (Australia/Sydney). User authorized iteration to prepare and dispatch
directly to the existing smoke tests conversation, without another plan approval.
This authorization supersedes the implementation phase's no-live restriction only for
these three development cases. No code changes, commits, budget tuning or formal benchmark.

## Execution

Use the current uncommitted working tree (prompt poi_semantics_prompt_4), based on
339e7e4a4a9eac133f2bdff69217b8b35c6990b4. Offline implementation validation passed
1712 backend tests (9 skipped), followed by 72 focused tests; both review axes passed.

Run Sydney V1, Sydney V3, Melbourne V1 sequentially in separate processes, once each.
Original inputs remain under logs/live_smoke_20260926/{sydney,melbourne}/input.json:
two travelers, AUD 3000, landmarks/waterfront/local-food relaxed-pace preference;
Sydney 2026-09-28 through 2026-10-02, Melbourne through 2026-10-05.
The launcher uses the real Australia/Sydney date. Stop before calls on September 29
or later; never backdate or silently change inputs. Do not rerun old evidence directories.

Iteration copied the already validated launcher without code changes into a fresh ignored
directory and executed its offline prepare command. Do not run prepare again. From repo root:

```powershell
.venv\Scripts\python.exe -m logs.semantic_contract_revalidation_20260927.run_one sydney_v1
.venv\Scripts\python.exe -m logs.semantic_contract_revalidation_20260927.run_one sydney_v3
.venv\Scripts\python.exe -m logs.semantic_contract_revalidation_20260927.run_one melbourne_v1
```

Run with authorized network access from the outset, requesting execution permissions in
the smoke tests conversation if required. Never relay permission requests between chats.
No automatic rerun or extra network probe is included. A permission rejection before
launch is not a model attempt; resolve it there before executing. A started failed case
must retain its evidence and must not be reset or retried under this plan.

## Limits and stop rules

Inherit all ceilings and provider limits from live-acceptance-plan.md and the prepared
runtime copy: 600-second application/660-second outer ceiling per case; semantic 6 calls,
120 seconds total, 45 seconds/call, 32000 input/8192 output tokens. Original plus correction
is at most two calls per batch across identity, citation and exception classes, within the
same request allowance. Existing generation, provider, RAG and V3 Repair limits/policies
stay unchanged. No quantity Repair implementation or policy tuning is authorized; report
downstream runtime behavior if reached. This is three bounded cases, not a dollar cap.

Inspect evidence between cases. An ordinary terminal case failure may be reported and
followed by the next case. Stop the entire batch for invalid dates, credential failure,
capture loss, secret exposure, unexpected provider use, exceeded budgets or changed input/
runtime policy. Do not bypass semantic validation or repair code/tooling in smoke tests.
Report tooling blockers to iteration. Do not print credentials, endpoint URLs or raw payloads.

## Evidence and acceptance

Save all new evidence beneath logs/semantic_contract_revalidation_20260927/, including
manifest.json, per-case request/runtime/result/execution, trace, requirement and semantic
input/output/outcome captures, and V3 Repair capture if reached. Existing normalized capture
caps/redaction apply (semantic 1 MiB/stage, 4 MiB/case); raw envelopes stay disabled.
Record actual input/runtime hashes, dirty revision, prompt version, call links, elapsed
time, usage and actual provider counters. A missing expected capture is not a clean pass.

For each batch distinguish first-call pass, corrected pass, correction failed/unavailable,
and out-of-scope terminal failure. A corrected pass requires one linked correction with
bounded feedback, the identical candidate/requirement/binding input, full validation and
no invalid cache/ledger admission. Report exact first and second failure classes when
available. No third call is allowed for a different error class. First-call pass shows
continuation but does not demonstrate correction efficacy. Never fabricate a failure to
force the correction branch. Semantic success followed by downstream failure is not full
itinerary acceptance. Report date coverage, generation reachability and all downstream
Spec deviations separately; no broad reliability or version-freeze conclusion.

Write an English report.md and a concise Chinese handoff containing process, per-case
outcomes, observed Spec deviations, items needing diagnosis/verification, evidence paths
and unavailable evidence. Smoke tests owns execution/reporting only; iteration owns
diagnosis, proposals, implementation and acceptance judgment. User-authorized coordination
includes sending that report to iteration thread 01a0d8d3-b759-7920-957b-a0b144352afe.
