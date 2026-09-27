# Offline diagnosis of non-reference semantic failures

Date: 2026-09-27. Historical status at diagnosis: complete; proposed changes not yet approved
or implemented. The subsequent user-approved minimum extension is now implemented and
offline validated; see `spec.md`. Replay commands below reproduce the pre-extension diagnosis
and its old terminal/call-count assertions; they are not current-code acceptance commands.
Base revision: `339e7e4a4a9eac133f2bdff69217b8b35c6990b4`, with prior uncommitted citation
correction, acceptance tooling, documentation and AGENTS edits. No production edit, live
request or commit occurred in this diagnosis.

## Evidence and repeatable loop

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

## Findings

### Sydney V1: ordinary preference promoted to an unauthorized exception

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

### Sydney V3 and Melbourne V1: one-character identity corruption

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

### Why all three terminate

Only SemanticReferenceError enters the existing same-batch correction loop. Identity-set
and unauthorized-exception errors use the terminal base error. The current behavior matches
the previously approved citation-only scope; these runs expose additional contract failure
classes, not evidence that the implemented citation correction regressed or was exercised.

## Options and recommendation

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

## Proposed TDD acceptance points

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
