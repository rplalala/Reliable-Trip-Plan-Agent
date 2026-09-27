# Offline comparison: extra correction versus short model-facing references

Date: 2026-09-27. Status: recommendation only; not approved for implementation.
Historical status above describes the comparison checkpoint. The user subsequently approved
option B; implementation and verification are recorded in short-reference-spec.md.
Scope: shared V1-V3 POI semantics. No production changes, live calls, quantity Repair
changes, commits or formal experiment were performed for this comparison.

## Evidence

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

## Option A: two corrections, at most three total attempts per batch

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

## Option B: batch-local short candidate and evidence references

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

### Offline representation measurement

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

## Recommendation and verification gates

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
