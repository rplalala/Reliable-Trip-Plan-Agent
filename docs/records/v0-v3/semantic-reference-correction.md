# Semantic Reference Correction

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="semantic-reference-correction-contract-live-revalidation-plan"></a>

<a id="semantic-reference-correction-contract-live-revalidation-plan--semantic-contract-correction-authorized-live-revalidation"></a>

## Semantic contract correction: authorized live revalidation

Prepared 2026-09-27 (Australia/Sydney). User authorized iteration to prepare and dispatch
directly to the existing smoke tests conversation, without another plan approval.
This authorization supersedes the implementation phase's no-live restriction only for
these three development cases. No code changes, commits, budget tuning or formal benchmark.

<a id="semantic-reference-correction-contract-live-revalidation-plan--execution"></a>

### Execution

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

<a id="semantic-reference-correction-contract-live-revalidation-plan--limits-and-stop-rules"></a>

### Limits and stop rules

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

<a id="semantic-reference-correction-contract-live-revalidation-plan--evidence-and-acceptance"></a>

### Evidence and acceptance

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

<a id="semantic-reference-correction-correction-options-comparison"></a>

<a id="semantic-reference-correction-correction-options-comparison--offline-comparison-extra-correction-versus-short-model-facing-references"></a>

## Offline comparison: extra correction versus short model-facing references

Date: 2026-09-27. Status: recommendation only; not approved for implementation.
Historical status above describes the comparison checkpoint. The user subsequently approved
option B; implementation and verification are recorded in short-reference-spec.md.
Scope: shared V1-V3 POI semantics. No production changes, live calls, quantity Repair
changes, commits or formal experiment were performed for this comparison.

<a id="semantic-reference-correction-correction-options-comparison--evidence"></a>

### Evidence

Source: logs/semantic_contract_revalidation_20260927/report.md and linked Sydney V1
semantic input/output/outcome captures, read locally. Current implementation is
backend/app/services/poi_semantics.py, schemas/poi_semantics.py and
llm/azure_foundry/client.py. The service allows two total attempts per batch and returns
only fully validated batches. The model DTO currently repeats unrestricted string
canonical IDs and source references at row and match levels.

Sydney V1 first returned one wrong ID (last character 4 became 5). Its second output
fixed identity coverage but introduced an extra `7f` in a supported match citation.
The affected row's first citation was correct. Thus this was newly introduced corruption,
not just a first-response citation hidden behind identity validation. It used two of six
calls and 49.918 seconds of 120; neither call reached the 45-second cap. The per-batch
attempt ceiling, not the request-wide budget, prevented a third call.

<a id="semantic-reference-correction-correction-options-comparison--option-a-two-corrections-at-most-three-total-attempts-per-batch"></a>

### Option A: two corrections, at most three total attempts per batch

Keep request-wide 6 calls, 120 seconds, 45 seconds/call and token ceilings unchanged.
Only the per-batch correction allowance increases from one to two. Raising only the
global limits would not bypass the current hard-coded two-attempt loop.

This is the smaller implementation: bounded attempt policy, prompt wording, correction
chain capture and boundary tests. It would enable a third call in the observed case,
subject to the actual remaining deadline; it does not establish that this call would pass.
The current correction payload is the original input plus diagnostic feedback, not an edit
of the previous output. A further call still regenerates all 32 rows and may introduce
another unrelated mistake. Preserve bounded prior diagnostics when designing the second
correction so the first failure class is not simply forgotten; never relax validation.

For planning only, observed 32-row calls took about 20-26 seconds and reported roughly
4.1-4.7k input and 4.4-6.4k output tokens. An extra similar call has that approximate marginal
cost, not a guaranteed duration or token count; timeout remains at most 45 seconds clipped
by remaining limits. A third call could bring this phase to roughly 70-76 seconds. This
leaves less budget for subsequent batches. Monetary cost is not calculated: actual billed
usage and deployment prices were not inspected. There is no measured success probability
for the third call and no justification yet to increase both global calls and time.

<a id="semantic-reference-correction-correction-options-comparison--option-b-batch-local-short-candidate-and-evidence-references"></a>

### Option B: batch-local short candidate and evidence references

Use an explicit model-facing DTO with short candidate references such as p01 and evidence
references such as e01. Keep descriptive candidate facts unchanged. Generate a bijective
mapping from supplied candidates and their supplied sources before calling the model.
Maintain that same mapping across correction attempts. Resolve exact known references
back into the existing canonical domain schema only after validating complete unique
candidate coverage and same-candidate evidence ownership. Then apply existing semantic,
requirement and exception checks before atomic cache/ledger admission.

Keep evidence references explicit: do not drop them or automatically turn every supported
claim into an evidence-backed claim. Unknown/duplicate/missing candidate references,
unknown source references and another candidate's valid source must still fail. Do not
infer identity by output order or fuzzy-match strings. Short-reference expansion is an
explicit predeclared wire contract, not guessing a correction for a malformed canonical ID.
Correctly formatted references still do not prove semantic support.

This is moderate bounded work: projection/resolution at the service boundary, dedicated
wire DTO/client response handling, prompt and fingerprint, input token accounting and
capture provenance. The current client immediately validates the canonical domain DTO,
so a wire/domain seam is required; this is not merely changing prompt examples. Keep
downstream canonical schemas, candidate policy, V0 and quantity Repair unchanged. Record
wire output, mapping identity/hash and resolved output/error in bounded opt-in captures.
Cache keys must include the projection/prompt version and canonical inputs. Existing
one-correction and global budgets remain unchanged. No dynamic-schema enums, partial
row repair or extra retry subsystem is required for the minimum option.

<a id="semantic-reference-correction-correction-options-comparison--offline-representation-measurement"></a>

#### Offline representation measurement

Used the repository's offline o200k engineering tokenizer on compact, sorted JSON.
Exact known canonical ID/source strings were replaced with pNN/eNN, including binding
values. All other content stayed unchanged; malformed strings remained unmodified.
This is a serialization counterfactual, not a model invocation or runnable implementation.
It excludes changed schema/prompt/framing/mapping-capture overhead and is not provider
billing, latency or quality measurement. A separate wire DTO may change the final totals.

| Captured output | Rows | Exact ID/source occurrences | Original input/output JSON tokens | Short input/output JSON tokens |
|---|---:|---:|---:|---:|
| Sydney V1 initial, failed | 32 | 89 | 2995 / 4169 | 1885 / 2594 |
| Sydney V1 correction, failed | 32 | 89 | 3140 / 4330 | 2011 / 2751 |
| Sydney V3 first batch, accepted | 32 | 81 | 2931 / 3994 | 1819 / 2560 |
| Sydney V3 second batch, accepted | 11 | 28 | 1283 / 1275 | 910 / 788 |
| Melbourne V1, accepted | 32 | 78 | 2942 / 3660 | 1828 / 2282 |

The accepted 32-row cases reduce output-content tokens by 35.9% and 37.7%, and input
content by about 38%. This establishes substantial repeated identifier text, not fewer
model mistakes. Short references can still be confused with another valid candidate.

<a id="semantic-reference-correction-correction-options-comparison--recommendation-and-verification-gates"></a>

### Recommendation and verification gates

Recommend B first for the next implementation scope. Repeated long-string corruption has
appeared in multiple captures, including a new error introduced by a full-batch correction.
B removes that copying burden on initial calls as well as corrections and reduces repeated
text without adding model calls. A is a reasonable lower-effort fallback when minimizing
implementation change is the priority; do not claim it is ineffective or rule out a later
bounded allowance increase. Do not implement both together: that adds scope and makes the
next smoke result harder to interpret. No live efficacy or success-rate estimate is available
for either option.

Minimum TDD for B: exact wire/canonical roundtrip; out-of-order valid rows; missing,
duplicate and unknown references; known cross-candidate evidence rejected; supported
match without evidence rejected; semantic/named exception permissions unchanged; mapping
stable within corrections and isolated across batches; cache/projection fingerprints;
full input sizing and existing call/time/deadline limits; capture linkage/redaction/caps;
client mocked-transport integration; unchanged canonical downstream V1-V3/V0 regressions.

After approval and implementation, iteration owns offline tests/review and prepares any
new authorized smoke; smoke tests executes only. First-call success is not correction
efficacy; unresolved/incorrect semantic judgments must remain visible. If repeated failures
persist despite shorter references, use the new captures to compare a second correction
against other changes and measured remaining request budget. Do not backdate expired
travel inputs. No additional live execution is authorized by this comparison.

<a id="semantic-reference-correction-non-reference-diagnosis"></a>

<a id="semantic-reference-correction-non-reference-diagnosis--offline-diagnosis-of-non-reference-semantic-failures"></a>

## Offline diagnosis of non-reference semantic failures

Date: 2026-09-27. Historical status at diagnosis: complete; proposed changes not yet approved
or implemented. The subsequent user-approved minimum extension is now implemented and
offline validated; see `spec.md`. Replay commands below reproduce the pre-extension diagnosis
and its old terminal/call-count assertions; they are not current-code acceptance commands.
Base revision: `339e7e4a4a9eac133f2bdff69217b8b35c6990b4`, with prior uncommitted citation
correction, acceptance tooling, documentation and AGENTS edits. No production edit, live
request or commit occurred in this diagnosis.

<a id="semantic-reference-correction-non-reference-diagnosis--evidence-and-repeatable-loop"></a>

### Evidence and repeatable loop

Source: `logs/semantic_reference_network_revalidation_20260927/<case>/attempt_1/semantics/`.
Input/output pairs were joined by call_id. These normalized captures are access-restricted;
local elevated reads were needed, not network access. No endpoints or credentials were read
from stderr or printed. Source input/response contents were not rewritten.

From the repository root:

```powershell
.venv\Scripts\python.exe -m logs.semantic_reference_network_revalidation_20260927.diagnosis.replay
.venv\Scripts\python.exe -m logs.semantic_reference_network_revalidation_20260927.diagnosis.probes
```

The first command injects saved responses at the external model boundary and calls the real
POISemanticsService.assess. It asserts the exact historical errors, one call and zero cached
rows. Repeated runs produced the same failures. The second minimizes each failure to one
candidate and tests counterfactual output edits, saving diagnosis/replay_results.json.
These are diagnostic probes, not automatic repair logic or claims of model compliance.

<a id="semantic-reference-correction-non-reference-diagnosis--findings"></a>

### Findings

<a id="semantic-reference-correction-non-reference-diagnosis--sydney-v1-ordinary-preference-promoted-to-an-unauthorized-exception"></a>

#### Sydney V1: ordinary preference promoted to an unauthorized exception

All 32 identities match. Ten food-service rows have role exception_only and claim semantic_3.
Their reasons explicitly say the local-food preference permits an exception-only option.
Input semantic_3 is a continuing ordinary preference with explicit_primary_exception=false,
polarity=favor. named_requirements and application_named_bindings are empty. Thus all ten
exception claims lack authorization under the current rule, not just the first rejected row.
One captured row plus its input reproduces Unauthorized primary exception.

Current spec (shared_poi_semantics_plan.md sections on roles and contract) reserves main-role
exceptions for application-authorized bounded experiences or matching REQUIRED named places.
ExperienceGoal rejects continuing+explicit_primary_exception. The validator correctly rejects
the output. This does not prohibit an ordinary food activity from appearing elsewhere in a
trip; it prevents upgrading that preference into a main sightseeing exception.

Prompt 3 says an explicit sourced experience request can authorize an exception, but does not
spell out the authoritative flag/polarity condition or the REQUIRED identity-binding branch.
The model's rationale is consistent with interpreting explicit mention of food as permission.
That is a supported prompt-alignment explanation, not proof of the model's internal reasoning.
The permission flag was actually supplied: serializer roundtrip equality rules out losing it
in the current input serializer. No evidence establishes that changing the prompt alone will
reliably prevent the error.

Removing exception claims alone permits the batch but leaves exception_only rows ineligible;
changing those same ten rows to non_main also permits the batch. This locates the invalid
claim. Neither counterfactual justifies silently stripping fields in production or endorses
all semantic judgments in the response.

<a id="semantic-reference-correction-non-reference-diagnosis--sydney-v3-and-melbourne-v1-one-character-identity-corruption"></a>

#### Sydney V3 and Melbourne V1: one-character identity corruption

Each response has 32 unique rows, but one input ID is missing and one unexpected ID is present.
Sydney: ChIJk8CcRwivEmsROPWHqq2Qlv0 becomes ChIJk8CcRwivEmsROPWHqq2Qlv2 (El Camino Cantina).
Melbourne: ChIJczgQh8lC1moR9r9gP44FRvY becomes ChIJczgQh8lC1moR9r9gP44FRvN (Chinatown).
The same changed ID appears in row and match citations. This is observable output corruption,
not evidence that Google supplied different IDs. Names/context remain consistent with the
missing input. A single candidate/row reproduces each identity-set failure.

Fixing only place_id reveals Invalid semantic evidence references and triggers the existing
citation-only correction (the deterministic fake model repeats the bad references and fails).
Changing that one ID and its citations together permits the original 32-row batch. Input
serialization roundtrips exactly for all three cases. The captured schema-valid output already
contains the corruption; no current service-side remapping defect was found.

The structured output schema accepts arbitrary strings for IDs and references. strict JSON
schema controls structure, not membership in the submitted batch. Exact identity-set and
citation membership are therefore application checks. Long opaque IDs repeated at several
locations create a copying burden; its contribution to real-model error frequency is not
quantified by these three observations.

<a id="semantic-reference-correction-non-reference-diagnosis--why-all-three-terminate"></a>

#### Why all three terminate

Only SemanticReferenceError enters the existing same-batch correction loop. Identity-set
and unauthorized-exception errors use the terminal base error. The current behavior matches
the previously approved citation-only scope; these runs expose additional contract failure
classes, not evidence that the implemented citation correction regressed or was exercised.

<a id="semantic-reference-correction-non-reference-diagnosis--options-and-recommendation"></a>

### Options and recommendation

1. Recommended minimum: keep strict validation and extend the existing single correction
   allowance to identity-set and exception-authorization/ownership contract errors. This is
   one correction per batch across all supported error classes, never one per error class.
   Provide bounded structured feedback: missing/unexpected/duplicate IDs, affected row and
   requirement IDs, and the actual allowed exception conditions. Reassess the whole same
   batch; keep full validation before atomic cache/ledger admission. Do not fuzzy-match IDs,
   overwrite citations, remove rejected claims or silently accept only good rows.
2. Make the exception instructions explicit: only favor+explicit_primary_exception=true or
   REQUIRED named requirement with the exact application binding can authorize an exception;
   a supported match remains necessary and the role must be exception_only. Ordinary food
   preferences with false authorization do not grant exceptions. Keep canonical IDs and
   reference values exact. Update prompt/cache fingerprints and capture metadata.
3. Alternative prevention: batch-local short handles or dynamic schema enums can reduce the
   long-ID copying surface. They add adapter/mapping/schema/cache and provenance boundaries;
   enums still do not guarantee unique complete coverage or exception authorization. This is
   a larger design option if bounded correction remains unreliable or costly, not included
   in the minimum implementation. Do not infer IDs by response order.
4. Budget-only change: all three used only 1/6 calls, about 20-26/120 seconds and fewer than
   8192 output tokens, with no recorded timeout/truncation. Raising limits alone cannot enter
   a correction branch excluded by error type. Keep defaults for the proposed minimum. If
   later captures show correction blocked by time/calls, compare a measured increase with
   smaller batches/shorter output or further mechanisms using actual marginal cost/latency.
   Smaller batches may increase total calls; raising limits remains a valid future option.

Likely files: services/poi_semantics.py, services/poi_semantics_prompts.py,
schemas/poi_semantics.py, focused service/SDK capture tests and current design/config docs.
Shared V1-V3 behavior changes; V0, acquisition capacities and quantity Repair stay unchanged.
Proposed budget: unchanged 6 calls/request, 120 seconds total, 45 seconds/call, 32000 input,
8192 output. Feedback counts toward input sizing. Transport, cancellation, timeouts and
unrelated malformed-schema errors keep existing behavior; no generic unbounded retry.

<a id="semantic-reference-correction-non-reference-diagnosis--proposed-tdd-acceptance-points"></a>

### Proposed TDD acceptance points

- Through assess/prepare, saved or minimized identity failure then a complete valid response
  succeeds on exactly two calls, preserving correct canonical mapping and cache reuse.
- Identity plus citation corruption is corrected together; merely fixing the ID must still
  fail citation validation. Missing/extra/duplicate cases have bounded actionable feedback.
- Ordinary continuing food preference cannot authorize exception_only eligibility. A model
  correction to valid non_main can continue; repeated unauthorized claims remain terminal.
- Positive controls: explicitly authorized bounded experiences and exactly bound REQUIRED
  named places remain eligible only with supported matches; OPTIONAL/wrong bindings cannot.
- Cross-class sequence (identity then citation, or authorization then identity) stops at two
  calls with zero invalid-batch cache entries; no third attempt per new error class.
- Shared call, input, total and both absolute-deadline limits apply to correction. Cancellation,
  failed provider call, exhausted allowance and accepted earlier batches preserve contracts.
- Actual SDK/capture tests verify linked original/correction input-output-outcome, redaction,
  size caps and failed/unavailable correction records. Changing prompt invalidates cache keys.
- Candidate Details continuation sees only validated rows. Ordinary non_main/unresolved output
  must not trigger correction. Verify shared V1-V3 integration and independent V0 regression.

Offline counterfactual acceptance is not live efficacy. New live acceptance belongs to the
smoke tests conversation after implementation, offline tests/review and user authorization.
Original travel dates expire for new runs on 2026-09-29; do not backdate future attempts.

<a id="semantic-reference-correction-v3-budget-audit"></a>

<a id="semantic-reference-correction-v3-budget-audit--v3-offline-budget-audit-after-short-reference-smoke"></a>

## V3 offline budget audit after short-reference smoke

Date: 2026-09-27. Source run: 1eba61e8-ad9b-48cc-9998-6e5d8392b0af.
Status: recorded call/count and selected token/time budgets reconstructed; no recorded
overrun. This is application evidence auditing, not a complete provider billing audit.
No production changes, live requests, commits or quantity Repair changes.

<a id="semantic-reference-correction-v3-budget-audit--method-and-reproducibility"></a>

### Method and reproducibility

Run `.venv/Scripts/python.exe tools/validation/packets/semantic-reference-correction/audit_v3_budget.py`
from the repository root. It reads the saved result, runtime, execution and events only,
and writes `logs/semantic_short_reference_revalidation_20260927/v3-budget-audit.json`.
The initial reconstruction completed successfully: 45 range checks passed. Event sequences
are continuous from 1 through 212, with no malformed JSON lines. The script preserves
SHA-256 fingerprints of its four source files and a source location for each budget row.
The sequence check supports continuity, not proof of uninstrumented network behavior.

Ordinary send events cross-check the selection-stage tool snapshot and cumulative route
snapshots. RAG sends cross-check the final discovery counters. Repair's 12 successful sent
acquisition records cross-check its counters and round event. Nearby and semantic counts
cross-check their individual call records. Cumulative snapshots and nested round copies
are not added together. Repair routes and RAG Details have separate pools from primary
route/Details budgets; they must not be charged to the primary limits for this audit.

<a id="semantic-reference-correction-v3-budget-audit--recovered-budget-values"></a>

### Recovered budget values

| Pool / metric | Recorded use / limit |
|---|---:|
| Primary destination / candidate searches | 1/1; 3/12 |
| Primary Details / weather | 32/60; 1/2 |
| Primary admitted candidates / final POIs at selection | 64/64; 16/20 |
| Primary review Details / experience model calls at selection | 0/8; 0/8 |
| Primary baseline routes / elements | 4/7; 256/400 |
| Primary alternative route calls / unique pairs / elements | 16/32; 11/32; 16/64 |
| Official web tasks / page fetches | 0/8; 0/8 |
| RAG retrieval queries / returned positions | 2/4; 40/80 |
| RAG Details / fallback | 26/30; 4/4 |
| RAG elapsed | 15.400/360 seconds |
| Semantic calls / elapsed | 2/6; 27.412/120 seconds |
| Semantic per-call elapsed | 15.533 and 11.879, each below 45 seconds |
| Semantic engineering input | 5210 and 4493, each below 32000 |
| Semantic reported output | 3270 and 2229, each below 8192 |
| Primary generation engineering input | 65807/252000 |
| Repair rounds / model calls | 1/5; 1/5 |
| Repair routes / elements | 12/24; 12/32 |
| Repair preparation routes | 12/16 (8 of 24 reserved for post-proposal) |
| Repair new Google / fallback / embedding / retrieval / canonical / Details | all 0, within their separate limits |
| Repair engineering input / reported output | 31970/252000; 1166/16384 |
| Nearby requests / elapsed | 3/3; 1.563/10 seconds |
| Application elapsed | 114.860/600 seconds |

One primary RAG embedding send matches one saved HTTP attempt, with 7 reported tokens;
this was one batched embedding operation for two retrieval queries, not two model calls.
Reported semantic input usage (3023 and 2306) differs from engineering input counts because
the latter include conservative prompt/schema/framing accounting. Do not mix those units.

<a id="semantic-reference-correction-v3-budget-audit--reached-limits-are-not-overruns"></a>

### Reached limits are not overruns

RAG fallback reached 4/4 and recorded two fallback_budget stops. Nearby used 3/3. Primary
pre-generation alternative routes used 16 calls: the other 16 of the 32-call pool were
reserved for post-generation. The final cumulative route-work snapshot contains 96
alternative_route_matrix_calls stop reasons. These are denied work opportunities, not
96 additional sends or proof that all 32 calls were consumed. Post-generation did not
increase the primary route count; Repair's 12 calls are separately recorded and budgeted.
Thus there are real coverage limits worth considering separately, but no recorded excess.

<a id="semantic-reference-correction-v3-budget-audit--remaining-evidence-boundaries"></a>

### Remaining evidence boundaries

The monolithic run.json has original_bytes=4908309 versus max_payload_bytes=1000000;
the 1090256-byte file contains a truncated preview wrapper, not a complete summary.
The event stream is usable; v3_finalized itself is intentionally summarized/truncated,
but its corresponding final result and individual Repair artifacts remain available.

Requirement captures preserve draft/outcome, not usage; dedicated main-generation token
usage is not present in the surviving evidence examined. Therefore complete requirement/
main-model billed token totals, every individual provider latency and a monetary total
cannot be reconstructed here. Engineering input checks and configured output/time caps
are not substitutes for missing actual usage. No claim of complete billed-token or
packet-level auditing is made. The 38 activities' null monetary costs are a separate
travel-budget issue, unrelated to this API resource-budget audit.

<a id="semantic-reference-correction-v3-budget-audit--recommendation"></a>

### Recommendation

The initial V3 aggregate provider-count gap is now closed at the recorded application
counter level. No further live attempt is needed to establish those recorded counts.
Recommend a small independent, bounded final budget/usage summary (e.g. budget.json),
containing effective limits, per-pool final counters and per-stage reported usage/missing
status, written before any large-payload truncation. Reuse existing counters and call IDs;
do not serialize the full itinerary or payload history into it. An offline test should
force run.json truncation while keeping that summary complete and avoiding double counts.
This is a proposal only, not implemented by this audit.

Raising max_payload_bytes above 4,908,309 would preserve this specific run and is a valid
low-effort temporary option, but duplicates a multi-megabyte result and moves the cutoff;
future growth may lose the same end-of-run fields. A separate compact summary is preferable
for recurring budget audits. Do not change API budgets or quantity Repair based on this
trace-storage issue. Any implementation or limit change needs its own approved scope.

<a id="model-reference-audit-2026-10-05"></a>

## Cross-chain model identity reference audit, 2026-10-05

Status: Implemented; offline validation and review recorded below. This event follows
the user's approved request to audit V0-V3, evaluation and other current model boundaries
for supplied long IDs that models must reproduce, and insert reversible short references.
The starting revision was `08b2cc477b779d3b168aa593a64ba4e07a166676`. The work began from
a clean `feature/evaluation` checkout; the changes below were initially uncommitted.
The preceding V0 identity pilot is separate historical evidence under
[#63](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/63); this audit did not
extend its live authorization or adopt its proposals. The current rule is maintained in
[system architecture](../../0001-system-architecture.md#model-identity-references).
At the user's subsequent request, [Issue #64](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/64)
was created on 2026-10-05 for this cross-chain work after local implementation/review.
It records the original commits, checked implementation acceptance and pending Git
delivery, with related Issues #63 and #28. The original commits were not rewritten.

### Audit and implementation

| Current model boundary | Observation and resulting change |
| --- | --- |
| V0 primary | No supplied external place ID to reproduce. Model-created activity/transport identities retain their existing contract. No external tools added. |
| Shared requirement interpretation | Source quotations and existing short local requirement references; no long-ID round trip found. Unchanged. |
| V1-V3 primary | Full canonical place IDs previously appeared in evidence and returned `source_place_id`. Shared aliases now cover evidence, compact directed routes, identity-based conflicts, official projections and candidate supply. |
| Review profiling | Canonical place ID previously returned alongside already-short `review_N` references. Only the place identity now uses an alias. |
| POI semantic classification | Existing `pNN`/`eNN` projection already protects canonical places and evidence. Unchanged. |
| Landmark nomination | Names and descriptions, with application identity resolution afterwards. No supplied long-ID round trip found. Unchanged. |
| V3 Repair | Full place/activity/target IDs previously had to be copied. Aliases now cover their structured permissions, feedback, route endpoints, temporal fragments, lineage keys/values and compensation permissions. Original patch authorization/adoption remains canonical. |
| Official evidence reasoning | Canonical place IDs and hashed source keys previously returned in assessments. Place, source and task fields now use aliases; original URLs, exact spans and source alignment remain required. |
| Product introductions | Supplied activity IDs previously returned in decoration output. Activity aliases are restored before existing result ownership checks. |
| Preference polishing, native web search, embeddings | No supplied long IDs that the model must repeat; provider-generated citation IDs and vectors are separate. Unchanged. |
| Native evaluator | No operational identity-assistance LLM caller. Added an offline proposal packet using reference/place aliases; no model client, live acquisition, human adjudication or native adoption was added. Controlled Repair continues using its isolated frozen ports. |

The shared data-only mapping utility has no SDK, planner or evaluator-policy dependency.
Aliases derive from complete identities in each request and have distinct namespaces;
they neither truncate hashes nor infer identity from prose. Response enums preserve
nullability, and exact restoration precedes existing domain validation. Evaluator packets
add exact decision coverage and per-reference candidate ownership checks. Primary and
Repair input sizing now includes the transmitted alias payload, instruction and enum
schema under unchanged ceilings. No retries or additional model/API sends were introduced.

### Validation sequence

Regression tests first reproduced canonical-ID leakage or failure to restore short
references at primary, Repair, introduction and official-reasoning boundaries. Helper
tests cover immutable input text, reversible keyed tables, identical ID prefixes,
separate per-call mappings, nullability and unknown/canonical-echo rejection.

An initial focused run passed 224 checks. An affected run passed 481 with one failure:
an old Repair SDK fixture supplied non-JSON `input` and expected the DTO class directly.
The fixture was corrected to the existing canonical JSON input contract and now checks
the constrained activity enum and unchanged per-call output-token options. Further
regressions exposed unmapped lineage, fragment/related activity and removable-place
references; those fields were added. Subsequent focused validation passed 654 checks.
User-supplied prompt markers are now excluded from application-owned JSON parsing.

The first full run had 2,682 passes, 10 skips and two failures. The evaluator import
guard rejected the new helper's imports; the mapping was moved to a neutral backend
module and the JSON-only identity packet stopped importing planner code. The guard and
related checks then passed 19 tests without weakening the guard. A frozen requirement
acceptance test observed a source-file change during that run and rejected its boundary
hash; with source stable it passed separately. The final adapter suite passed 9 tests,
including a real SDK over MockTransport: one short-reference request, constrained
response schema and canonical domain restoration, without live network access.

With code stable, the final full backend suite passed **2,686 tests, 10 skipped in
249.85 seconds**. Ruff and `git diff --check` passed. These were offline implementation
checks, including fixtures and MockTransport, not a new live pilot or formal benchmark.

Implementation was committed before review, as required by AGENTS.md:

- `a8b13d1`: `feat: use short model references across planning adapters` (shared utility,
  provider projections, budget accounting and directly related regressions).
- `e9567f6`: `feat: prepare evaluator identity proposals with short references` (independent
  offline proposal packet and its coverage/ownership tests).

Parallel code review examined both commits against the recorded starting revision and
the approved user request. Standards reported zero documented violations or actionable
baseline smells; Spec reported zero missing requirements, scope extensions or incorrect
implementations. No post-review code correction was required. The final documentation
group updates PROJECT.md, the architecture contract, this event and its record index.
Publication was not performed; `main` and `origin/main` remained at
`1e2aaa9ef53a650207e371986a9dc6229187d11a`.

### Preserved V0 evidence and limits

Local evidence identifiers, not published dependencies:
`artifacts/short-id-20261005/{focused-01.log,affected-01.log,focused-final.log,full-backend.log,full-backend-final.log}`
and `v0-identity-{short-input,reference-map,offline-replay}.json` in that directory.
The old `artifacts/v0-identity-prototype-20261005` packet remained untouched: all 61
authorized file hashes were verified unchanged. The new offline packet represents nine
references and twelve distinct candidates. Its mapping hash is
`4a7d36cc0e0ccf64138f1faf36a194b99fe606c8999538966b3cc16fbe66a36b`.

The program re-encoded the existing proposals and restored them identically. This was
not a new model response. Consistently serialized offline input estimates changed from
5,017 to 4,522 tokens; these are engineering estimates, not the old provider's reported
4,213 input tokens, measured new usage, a billing reduction or evidence of better model
accuracy. No live calls were made. Native identity adoption remains zero and the four
V0 routes remain UNKNOWN. The original V0 itinerary was neither rerun nor optimized.

Short references prevent long-ID copying errors at the protected boundaries. They do
not establish candidate truth, eliminate semantic mistakes or validate transport.
The evaluator packet still requires a separately prepared and authorized execution to
measure model behavior with short IDs. V0-V3 retain independent entry points and version
mechanisms; this shared transport correction does not freeze a version or constitute
a formal benchmark. Publication and further live execution remain separate actions.
