# Authorized short-reference live revalidation

Date: 2026-09-27, Australia/Sydney. User explicitly approved the three-case live
revalidation after prompt-5 implementation, 1721 passing backend tests (9 skipped),
and independent Standards/Spec reviews. This is development acceptance, not a benchmark.

## Execution scope

Inherit the inputs, order, network policy, budgets, stop rules, capture limits and reporting
requirements of contract-live-revalidation-plan.md, with the replacements below. That
document's prompt-4 result is historical and its output directory must not be reused.
No production/tool changes, budget tuning, quantity Repair implementation, commits or push.

- Current prompt: poi_semantics_prompt_5; wire version: poi_semantics_wire_1.
- Three cases: Sydney V1, Sydney V3, Melbourne V1, sequential independent processes,
  one attempt each, no automatic rerun or extra network probes.
- Original input files: logs/live_smoke_20260926/{sydney,melbourne}/input.json.
  Preserve original bytes, dates, two travelers, AUD 3000 and preferences.
- New evidence root: logs/semantic_short_reference_revalidation_20260927/.
- Reuse the previously validated launcher unchanged, copied into the new root. Iteration
  runs prepare once offline; smoke tests must not prepare again or reset started cases.
- Current real Sydney date is September 27. Launcher must independently use the real date
  at each start and stop if September 29 or later. Never backdate or silently shift dates.
- Request authorized network execution from the first launch. Resolve permission needs
  in smoke tests, not by relaying them between conversations. A pre-launch permission
  failure is not a live attempt; do not run a restricted-network fallback first.

Run from the repository root after offline preparation:

```powershell
.venv\Scripts\python.exe -m logs.semantic_short_reference_revalidation_20260927.run_one sydney_v1
.venv\Scripts\python.exe -m logs.semantic_short_reference_revalidation_20260927.run_one sydney_v3
.venv\Scripts\python.exe -m logs.semantic_short_reference_revalidation_20260927.run_one melbourne_v1
```

Per case retain 600-second application / 660-second outer limit; semantic 6 calls/request,
120 total seconds, 45 seconds/call, 32000 input and 8192 output tokens. At most two calls
per semantic batch across all correctable classes. All other runtime defaults and provider
limits remain unchanged, including existing V3 runtime Repair behavior if reached.
Stop the batch for credential/date failures, missing capture, exposed secrets, exceeded
budgets, unexpected providers or changed input/runtime policy. Ordinary terminal case
failures may be reported before proceeding to the next case. No bypass or code fixes.

## Additional acceptance evidence for the new wire contract

Preserve normalized requirement and semantic captures, plus V3 Repair capture if reached,
all manifest/hash/usage/provider-count and downstream-result evidence from the prior plan.
For each semantic call, inspect these offline after execution:

1. Input/output uses candidate_ref pNN and evidence refs eNN, with expected wire/prompt
   version. Canonical mapping is in input-capture reference_mapping, not the model's input.
2. Candidate coverage is unique and complete; every used evidence ref belongs to the same
   candidate. Accepted outcome assessments restore the exact original canonical IDs and
   sources from the mapping; output order is not an identity guarantee.
3. Mapping hash and the mapping itself stay equal between an original call and correction.
   Record original/correction linkage, failure classes, presend stops and all actual usage.
4. Distinguish first-call pass, corrected pass, correction failed/unavailable and later
   downstream failure. A first-call pass can validate live wire integration without proving
   correction efficacy. Never force an error to exercise correction.
5. Report missing provenance or inability to verify mapping as evidence limitations, not a
   clean pass. Do not mistake correct references for verified semantic claims or operating
   facts. Date coverage, route UNKNOWN, RAG partial, cost uncertainty and quantity observations
   remain separate from wire-contract acceptance; no general reliability claim.

Write report.md in English plus a concise Chinese handoff containing actual process,
results, suspected Spec deviations and items needing diagnosis/verification, with exact
evidence paths. Smoke tests only executes/reports. Iteration owns diagnosis, implementation
and acceptance judgment. User-authorized coordination includes returning the handoff to
iteration thread 01a0d8d3-b759-7920-957b-a0b144352afe. Keep secrets and raw envelopes private.
