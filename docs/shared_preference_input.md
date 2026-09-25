# Shared Preference Input Validation and Clarification Gate

Current status (2026-09-25): implemented + offline-validated, with bounded prompt12 taxonomy
and Case4 safety live evidence. Case5 was provider-preempted; latest UI mapping and prompt13
budget scope remain offline-only. This is shared V0-V3 correctness, not V3-exclusive value.
Product selection remains V0. See [closeout evidence](v3_closeout.md); historical records are unchanged.

## Contract and execution

`PlanningRequest` schema/date validation precedes the existing single preference interpretation
call. Empty/whitespace preferences retain the no-model path. `InterpretationDraft` adds
`preference_input_assessment`; current strict wire output requires it. The domain's nullable
compatibility field means historical/unassessed, never implicit VALID. Current request execution
rejects missing assessment as a `RequirementBoundaryError`; historical direct canonicalization
remains readable without fabricating an assessment. Synthetic test re-expression is explicitly
labeled and does not migrate historical files.

Current markers: `preference_prompt_13`, `preference_draft_9`, strict schema name `PreferenceDraftV9`,
and assessment `preference_input_2`. The downstream interpreted requirements version remains 3:
the gate does not replace canonical requirements or change their evidence semantics.

The two assessment dimensions are input disposition (`VALID`, `CLARIFICATION_REQUIRED`,
`REWRITE_REQUIRED`) and safety disposition (`CLEAR`, `SAFETY_BLOCK`). Application policy verifies
their consistency with typed issues before choosing safety, rewrite, clarification, then continue.
VALID only means no request-level preference issue currently requires user correction before
planning continues. It does not certify feasibility, supported requirements, place existence,
opening, access, tickets, prices, routes, budget adequacy, or successful final generation. Existing
canonicalization, hard-requirement/capability guards and downstream evidence checks still execute.

Eight bounded issue categories cover destination physical-visit conflict, structured-field
conflict, same-subject/scope hard contradiction, unsupported scope, material semantic ambiguity,
non-travel task-control instruction, contextual self-harm risk, and explicit serious harm to a
person. The last category is deliberately not an unrestricted OTHER_SAFETY catch-all. No regex,
keyword classifier, geography lookup, second judge, or additional model call has been added.

Each issue contains up to three exact quote/occurrence pairs, quote status, optional related field,
optional operational-conflict index, and bounded subject/condition scope. At most eight assessment
issues are accepted; unmatched legacy operational conflicts retain their existing six-entry bound.
Reason/action strings come from application templates. Current field values come only from
`PlanningRequest`, not model output. Contradiction requires two distinct located sources; this
proves grounding, not the semantic truth of the model's contradiction judgment.

## Grounding and failure ownership

New gate sources and linked operational conflicts require exact, case-sensitive original text
and the existing occurrence mapping. They never use fuzzy matching or the older source mapper's
casefold fallback. Fabricated quotes, wrong occurrences, invalid links, inconsistent dispositions,
malformed DTOs and missing current assessment are interpreter contract failures, not user issues.
The gate also checks supplied extracted requirement sources before returning a blocked decision.

`quote_status=unavailable` is allowed only for a structured-field issue linked to a matching,
independently exact-sourced `operational_conflicts` entry. UI shows reason/action and quote
unavailability, not an invented sentence. The typed result retains basis references. Other
unavailable-quote claims do not satisfy this contract. New ambiguities use typed issues; legacy
`extraction_issues` retain the prior generic clarification boundary, not invented source spans.

Three meanings remain distinct: user input issue, interpreter contract/dependency failure, and
real-world UNKNOWN. The last is not an input rejection condition. System/provider refusal is also
not reinterpreted as a model-authored safety assessment. Cancellation propagates normally.

Paris plus an explicit incompatible physical New York visit is a model classification case for
rewrite. New York-style jazz, similar experiences, past references and Versailles are not conflicts
merely because another city name appears. The interpreter is instructed not to act as a geography
or feasibility checker. Material unsupported cross-city product scope may need clarification.
Soft tensions, diverse travelers and ordinary flexible/relaxed preferences should continue.
These are prompt requirements; mocked tests do not prove real-model precision on these examples.

## Stop, API, UI and privacy

The gate runs in shared `interpret_preferences`/canonicalization before travel acquisition. Real
V0-V3 runner tests cover rewrite, clarification, safety, contract failure, timeout and cancellation:
one interpreter attempt, zero travel provider calls, no retrieval factory initialization, and no
primary or Repair call. V3's lazy owner still closes without creating a runtime. Existing borrowed
client ownership remains unchanged; construction of local objects is not an external connection.

Ordinary issues reuse `ClarificationRequired` through `PreferenceInputBlocked` and the product
`needs_clarification` response, with typed disposition and issue rows inside `issues`. Safety has
a separate `safety_blocked` product response containing only application support text, no sensitive
quote echo. It does not infer current location from destination. Contract errors use the product
system-failure response. The developer API now also returns HTTP 502 for contract failures, rather
than grouping them with HTTP 422 user clarification. V0 CLI now uses exit 1 for contract failure,
matching the existing tools runner; user clarification remains exit 2.

The form remains populated. Ordinary feedback displays original quotes as React text, current
related field values, reason and action; unavailable quotes are marked. Editing clears old issues,
safety output, errors and itinerary. Submission clears old results, prevents repeated submission
while pending, and uses the new response. Safety has separate presentation.

Normal new gate telemetry includes only issue types, quote statuses, dispositions and hashes.
It does not add preference/quote text. Existing explicitly enabled development capture can retain
bounded typed provenance and remains subject to existing redaction/private-storage policy. No new
full provider payload logging was enabled. Earlier run-level logging behavior is unchanged.

## Shared correctness fixes

Importing `RequirementBoundaryError` directly exposed a pre-existing eager LLM package/provider
circular import. The package's provider export is now lazy; its public import remains available.
This and the developer API/V0 CLI failure ownership corrections are shared fixes, not V3 benefits.

## Actual offline validation sequence

1. Initial targeted backend run stopped during collection on the circular import; no tests ran.
2. After the lazy export correction: 127 passed, one historical wire re-expression test failed
   because current assessment was absent. Added explicitly synthetic assessment in that test only.
3. Targeted gate/shared interpretation/strict DTO/API checks: 137 passed.
4. Affected V0/V1/V2/V3, provider DTO and API regression: 224 passed. Frontend's parallel first
   invocation did not start because the sandbox denied Vite cache writes. Local authorized rerun:
   16 passed, one new test failed because its text selector matched both textarea and blockquote.
5. Narrowed the selector; frontend 17 passed. Added exact wire failure and lazy-owner cleanup
   coverage; targeted backend 96 passed. Offline sizing ran without any provider calls.
6. Ruff initially reported 16 import-order/line-length findings; corrected only relevant files.
7. Added developer API/CLI system-failure, provenance and telemetry checks: backend 251 passed.
   Targeted Ruff, frontend lint and TypeScript/Vite production build passed.
8. Restricted operational-conflict links to structured issues and tested the inverse case:
   final gate/strict DTO subset 68 passed; final changed-page subset 15 passed. Final targeted
   Ruff and `git diff --check` passed. No full-repository regression was run.

These overlapping test counts are execution records, not additive unique test totals. Fixtures
exercise application decisions, not actual LLM understanding. No live, Google, embedding or DB
connections, benchmark, new capacity policy, commit or push was performed.

## Serializer sizing and unchanged limits

Reproduce offline with `.venv/Scripts/python.exe -m tools.diagnostics.preference_payload`.
Uses the actual system/user prompts, strict wire schema, domain/transport DTO and offline o200k
tokenizer. Existing preference guard: 8,000 tokens and 24,000 characters, both enforced before
the interpreter. This is NOT the primary/Repair 252k policy. There is no dedicated combined
interpreter engineering ceiling or framing reserve in current configuration, nor a new per-call
output cap in this change. Provider/model defaults were not changed.

| Fixture | Preference tokens | System | User | Strict wire | Serialized sum |
| --- | ---: | ---: | ---: | ---: | ---: |
| Normal | 8 | 3408 | 110 | 3432 | 6950 |
| Several ordinary requirements | 25 | 3408 | 127 | 3432 | 6967 |
| Multiple issues, three quotes, two-source contradiction | 13 | 3408 | 115 | 3432 | 6955 |
| At preference token limit | 8000 | 3408 | 8101 | 3432 | 14941 |
| At character limit (24000) | 3000 | 3408 | 3102 | 3432 | 9942 |

The sum excludes unknown provider framing and is not actual billed usage. Synthetic minimal
response is 86 tokens; two-issue response is 201 tokens, not a maximum output guarantee. The
8,002-token and 24,001-character examples are rejected as `preference_input_overflow`, with zero
provider calls. Schema growth alone provides no evidence for increasing budgets. Real-model
classification, strict endpoint acceptance and possible truncation still require separately
authorized development live validation.


### Minimum daily coverage update (2026-09-25)

Shared output now reports the one-primary-visit minimum independently of 2-5 review
quantity guidance. V0-V2 remain diagnostic-only; V3 prioritizes confirmed minimum gaps
below hard protections and above optional reviews. Explicit source-linked full-day time
protections support exemptions; uncertain applicability remains unknown. Product output
includes coverage status without research metadata or source quotations. The primary
prompt, default engine and budgets are unchanged. See [shared minimum coverage](shared_minimum_daily_coverage.md)
for counting, compatibility, exemption and partial-result boundaries, and the V3 development
checkpoint for offline and live evidence. This does not retroactively validate historical runs.


## Contract alignment checkpoint (2026-09-25)

Historical Step1 run `9f50dee0-4cc1-4f18-8eec-800a90597730` remains BLOCKED:
the destination issue carried operational_conflict_index=0. Its core classification and
wire parse succeeded, but the unchanged domain ownership invariant rejected it. Only
case1 ran; nine cases were not attempted; downstream travel work was zero. Original
artifacts are unchanged. A source-hashed fixture preserves the exact structured text.

The prompt now explicitly reserves operational_conflict_index for structured_request_conflict
and shows the full Paris/Bronx Zoo shape with a null index and no duplicate operational row.
The strict issue array uses two small anyOf branches: structured issues allow integer/null,
other issues structurally require null and located quote status. No invalid output is cleaned.
Domain validation independently retains the ownership rule. Request values remain application-owned.

Conditional-field audit:
- index ownership: wire branch and domain; range/list bounds remain domain/application checks;
- quote_status/unavailable: non-structured branch forbids unavailable; domain requires a linked
  structured issue with empty source_refs; application verifies linked exact sources;
- source_refs: no separate related_source_quote field exists; contradiction uses two distinct
  sources. Domain checks count/status; application checks exact text, case, occurrence and spans;
- related_field: structured wire branch requires a RequestField; destination-specific equality
  remains domain-enforced; linked field equality and authoritative value lookup are application-owned;
- located linked issues now require each source span to overlap the linked conflict's sources,
  preventing unrelated sentences/occurrences sharing a field from being consumed. This is source
  association, not a new semantic truth classifier;
- safety_disposition and input_disposition consistency remain application checks derived from
  issue types. Sensitive UI suppression and independent safety exit are unchanged;
- scope length and overall issue/source limits remain domain checks. Extra fields are forbidden.
Thus wire ownership is structural, but not every provenance or cross-field rule is wire-guaranteed.

Versions: preference_prompt_10 -> 11; preference_draft_8 -> 9 (wire name PreferenceDraftV9);
preference_input_1 -> 2 for strengthened linked-source association. Interpreted requirements
contract remains unchanged; no taxonomy, budget, retry or travel behavior expansion.

Offline execution order: 134 targeted tests passed on first run; 44 affected API/version and
canonicalization regressions passed. Initial Ruff found six long test lines; formatting fixed
those and final targeted Ruff passed. git diff --check passed (existing CRLF notices only).
No frontend production change or frontend checks in this phase. No real calls in Phase A.
Phase B is separately gated on this offline checkpoint and freezes ten expectations before calls.


### New Step1 smoke: harness blocker, zero model sends

Run `9c8eb048-1e8c-47bd-b17f-9578a7c7c6f8` in
`logs/shared_preference_gate_alignment_10case_20260925/` stopped with
`execution_or_capture_failure:UnboundLocalError` before case1. The new capture block was
inserted into the NOT_ATTEMPTED branch at the wrong indentation and read `before` before
assignment. This is a recording-harness defect, not model/domain feedback. Syntax-only
preparation did not catch it. No repair/rerun occurred under this authorization.

All10 cases NOT_ATTEMPTED; zero interpretation calls, HTTP sends, travel/primary/Repair work.
No actual usage, quote, classification or strict-provider acceptance result exists. Current
configured deployment gpt-6-luna; both SDK clients report closed; elapsed0.781s, recorded exit1.
All source and historical hashes unchanged. Phase A is implemented + offline-validated;
Phase B remains BLOCKED. The old failure remains historical evidence; neither run can be
relabelled bounded live-smoke validated. New harness repair/live requires further authorization.

### Recording harness repair: offline checkpoint (2026-09-25)

The separately authorized harness correction is implemented and offline-validated. Historical
run directories, including their defective run.py, remain unchanged. Gate prompt11, wire9,
input2, domain invariants, model defaults and travel budgets were not modified by this repair.
Step1 real-model acceptance is still BLOCKED; no new real call or live directory was created.

The historical defect had two control-flow effects: capture read `before` before initialization,
and an incorrectly indented unconditional `continue` made normal invocation unreachable. Merely
initializing the variable would not have repaired the harness.

`tools/validation/preference_gate_smoke.py` now provides a reusable interpreter-only state machine:

- read-only preflight checks frozen source/history hashes, deployment, future dates, case IDs and
  expectations; an existing output directory is rejected before client construction;
- each case is registered before its one permitted interpretation call, with independent response,
  HTTP and usage records; NOT_ATTEMPTED cases never inspect response state;
- the existing adapter and real shared interpreter retain contract/provenance authority. Wire
  re-parsing is audit-only; it never replaces domain output or repairs an illegal combination;
- missing assessment, expected-outcome mismatch, contract/provider/capture failure and cancellation
  stop further cases. Already attempted work remains attempted even if its artifact write fails;
- the first failure reason survives later capture/cleanup errors, which are recorded separately;
- cumulative callback usage is retained in finally, including after failure. Per-response and model
  metadata usage corroborate it and are not added again. Missing usage is not estimated;
- application-grounded provenance and actual outcomes remain visible. Only response text/usage are
  captured, not internal reasoning blocks or full provider payloads; known credentials are redacted;
- the owned adapter is closed, cancellation is re-raised, and source/history integrity is checked.
  Closure claims describe observable adapter completion, not invented transport state.

`tools/validation/run_preference_gate_smoke.ps1` propagates the Python exit code. It does not end
with a successful file-write command that masks failure. The module requires `--execute-live`, a
frozen manifest and its SHA-256, and a new output path; this flag is not a substitute for explicit
user authorization. Run from the repository root. Future authorized command shape:

```powershell
& ./tools/validation/run_preference_gate_smoke.ps1 `
  -Manifest <new-frozen-manifest.json> -ManifestSha256 <sha256> `
  -Output <new-independent-log-directory> -ExecuteLive
```

This checkpoint does not prepare that live manifest or authorize execution. The historical manifest
must not be reused with stale source hashes. The harness currently accepts a single frozen expected
outcome per case and rejects nonempty allowed_alternatives rather than silently ignoring them.
It uses no travel runner, so it cannot initiate Google/RAG/Weather/Routes/primary/Repair work.

Offline execution order:

1. Initial new harness suite: 17 passed, 1 failed. The cancellation fixture returned an unawaited
   coroutine from a synchronous MockTransport handler, yielding a transport error rather than cancel.
2. Changing that handler to throw directly still produced 17 passed, 1 failed: the injected transport
   cancellation surfaced as a dependency AttributeError. This was not evidence of a successful
   cancellation test. The harness boundary test was changed to inject CancelledError at the model
   boundary, verifying real interpreter-to-harness propagation, saved state and adapter cleanup.
3. New harness suite: 18 passed; targeted Ruff passed.
4. Added the original ten frozen inputs/expectations with explicitly synthetic model responses,
   missing/illegal output, quote/occurrence, safety/clarification, redaction and CLI checks. New
   harness plus shared Gate/alignment and SDK requirement-boundary regressions: 137 passed.
5. Ruff check passed; format-check identified the two new Python files, which were formatted.
6. Added explicit PowerShell subprocess exit propagation, guaranteed to fail manifest hash validation
   before settings/client loading. Final harness suite: 22 passed. No real provider was called.

The test fixture records the historical manifest SHA-256 and copies only frozen cases/expectations;
it does not claim synthetic responses were returned by the historical model. Tests use the actual
strict SDK parser and shared interpreter with MockTransport; the cancellation boundary uses a mock
model. V0-V3 entry points are forbidden in the harness tests, and the existing shared Gate suite
exercises blocked downstream paths. No frontend code or primary/Repair serializer changed, so no
frontend build, sizing, or full-repository regression was run.

Limitations: a new authorized real-model run is still needed to verify the deployed provider's
current wire contract and the ten semantic cases. Model-boundary cancellation is covered; this
checkpoint does not claim live in-flight SDK/network cancellation validation. Storage failure can
leave an incomplete artifact; the in-memory summary/exit status records failure where possible and
never authorizes a retry. Neither historical failed run has been converted into a passing run.

### Taxonomy boundary alignment: Cases 2-3 (2026-09-25, offline only)

The completed, separately authorized smoke batches preserved the following observations: Case1
passed the corrected index/wire/domain path; Cases6-10 matched their frozen expectations. Case2
returned semantic_ambiguity/CLARIFICATION_REQUIRED rather than contradiction/rewrite, while grounding
both original sentences correctly. Case3 returned destination_scope_conflict/REWRITE_REQUIRED rather
than unsupported scope/clarification. Both were structurally legal and application-blocked outcomes,
not domain failures. Case4's unstructured provider refusal and Case5's HTTP400 remain independent
open items; this change does not diagnose or fix them.

The shared prompt is now preference_prompt_12. Wire preference_draft_9, input preference_input_2
and interpreted_requirements_3 are unchanged. Strict schema descriptions, enum sets, domain
invariants, application/API mapping, frontend and budgets are unchanged. Schema already expresses
the required shapes/ownership; a description-only wire revision was not necessary. The client
capture and acceptance-tool prompt markers were updated so recorded versions match the actual prompt.

The four existing categories now have distinct semantic instructions:

- internal_requirement_contradiction: individually clear, non-negotiable requirements on the same
  subject, time, scope and conditions cannot jointly hold. Not knowing which requirement the user
  would give up is not uncertainty about what the requirements mean. Never soften one clear hard
  requirement into a high/soft preference simply to avoid the contradiction.
- semantic_ambiguity: decisive subject/reference, scope, time/condition or strength is missing, so
  the requirement itself cannot reliably be understood. Ordinary flexibility is not ambiguity.
- destination_scope_conflict: physical visit intent directly conflicts with or replaces the
  authoritative destination (Paris/Bronx Zoo or Tokyo instead); rewrite is required.
- unsupported_request_scope: the user retains the destination but requests an additional segment
  the current single-destination product cannot represent (Paris plus a London day); clarify the
  product scope, without claiming objective geographic impossibility.

Earlier instructions broadly routed structured contradictions to operational_conflicts, conflicting
named/multiple-destination intentions to extraction_issues, and conflicting modes to clarification.
The combined unsupported-scope/ambiguity description also obscured their distinction. These were
locally aligned with the Gate decision sequence, rather than appending case-specific answers alone.
Destination intent/extension issues do not also create an operational conflict that would override
clarification. Typed issues are not duplicated in extraction_issues. Other structured-field conflicts
retain existing operational links and source validation.

The prompt retains valid walking/metro trade-offs, different travelers' soft preferences, Versailles
under the current scope policy and style/analogy references. The phrase "Use walking or metro
depending on what works for me." alone remains normal flexibility. A separate synthetic ambiguity
fixture refers to a mandatory restriction supposedly stated earlier when none was provided. No
keyword/regex city, also/instead, only/must or model-reason reclassification was added. Application
still executes a structurally legal model taxonomy even when the frozen semantic expectation differs.

Historical fixtures historical_contradiction_taxonomy.json and historical_scope_taxonomy.json
preserve exact structured text, parsed outcomes, frozen expectations and original artifact SHA-256.
They remain mismatch fixtures: tests explicitly prove they are NOT automatically corrected.
Synthetic positive/negative tests separately exercise the real strict SDK/parser over MockTransport,
domain DTO and shared application interpreter. They establish contract handling, not improved real
model classification accuracy. Existing Gate regressions cover quote case/occurrence, fabricated
sources, related conflict links, index ownership, authoritative structured values, normal VALID
continuation and blocked V0-V3 paths with zero downstream work.

Execution order: first targeted taxonomy/Gate/alignment/request-wide run passed99 tests. Initial
Ruff found six long lines in the edited prompt/new test; line wrapping and test formatting fixed
them, and targeted Ruff passed. Affected SDK requirement-boundary/harness regression passed64 tests.
Final taxonomy retest passed16 tests after formatting; git diff --check passed. Both historical
artifact hashes and the actual wire-schema hash match their saved live sources.
No real model, provider, embedding, database or travel call occurred. No frontend change/build,
full V3 rerun or payload sizing was needed for this bounded prompt-only policy revision.

The previous live classifications and expected outcomes remain unchanged. Case2/3 policy is now
implemented + offline-validated, but semantic stability of prompt12 awaits separately approved real
model testing. Case4 structured Safety/refusal mapping and Case5 provider HTTP400 cause remain open.
This checkpoint makes no new live-smoke validation claim and does not authorize a new run.


## 2026-09-25: Case 4/5 provider diagnostics alignment

Status: implemented + offline-validated; no new live evidence. This is shared V0-V3
observability/failure attribution, not a taxonomy or Safety accuracy change. Prompt12,
wire9, Gate/domain contracts, deployment, token limits and zero retries are unchanged.

Historical Case4 remains HTTP200 ordinary refusal text with provider_incomplete, without
sufficient captured response status/reason to identify the provider cause. It did not produce
a validated structured SAFETY_BLOCK. Historical Case5 remains HTTP400 with insufficient
provider diagnostics; its earlier configuration_failure label does not establish a configuration,
schema, content-policy or prompt-injection root cause. Historical artifacts are unchanged.

The adapter now retains provider_diagnostics_1 internally on last_call_metadata and boundary
exceptions. The allowlist includes HTTP status when exposed by the exception, provider code/type,
bounded message, provider request/response IDs, response status, incomplete reason, structured
refusal presence, text presence, real token totals, availability, missing fields and truncation.
Missing values remain null. Internal hashed request_id is distinct from provider_request_id.
A successful-response HTTP status not exposed by the adapter is not invented: the harness keeps
its independently observed HTTP status. Capture is explicitly partial, not a complete raw envelope.

Only explicit machine-readable request/schema/parameter/deployment codes establish HTTP400
configuration/request-contract attribution. Generic invalid_request_error type alone is insufficient.
Unexplained or nonconfiguration 400 responses are provider_request_rejected; 401/403 are request
rejections; 429/5xx and connection failures retain dependency/transport failure attribution and
available HTTP facts. SDK exception class is not recorded as a provider error code.

Structured refusal remains provider_refusal. Incomplete responses and completed non-JSON prose
remain provider_incomplete; prose is not semantically classified as refusal or Safety. Damaged
JSON and invalid DTOs retain contract failure. Neither refusal path creates SAFETY_BLOCK, rewrite,
clarification or valid input. Only the existing structured domain path can classify preferences.

Error messages are limited to1024 characters; other textual fields to256. Known credential values
and escaped forms, existing secret redaction, and auth/key/cookie-like text are removed before
truncation. Raw headers, unrestricted error bodies, reasoning content and additional sensitive user
text are not added. Already buffered error envelopes up to16KiB may be inspected for top-level
usage discarded by SDK unwrapping; no read sends network requests. Larger/unavailable envelopes
leave usage unavailable. Normal callback usage remains authoritative; diagnostics are not added
to callback totals. Provider diagnostic details are deliberately absent from as_dict/public APIs.

Smoke harness copies adapter diagnostics without semantic reinterpretation. It retains the first
stop reason and records secondary capture/cleanup errors. Adapter capture exceptions, including
canonicalization capture, cannot replace the interpreter result/failure. Existing zero-retry and
one-call-per-case controls remain in effect. No new live harness invocation is authorized here.

Actual validation sequence:
1. New diagnostics + boundary + harness:76 passed,2 failed. One new test supplied text where the
   manifest fixture required a DTO. The old malformed-response test used ordinary prose; it now
   uses broken JSON, preserving contract-failure coverage separately from prose/incomplete tests.
2. Corrected suites plus shared Gate/API/V0-V3 blocked paths:146 passed.
3. Ruff:9 long-line errors; wrapping/formatting corrections followed.
4. Additional diagnostics run:15 passed,1 failed. Real SDK unwrapped the error body and omitted
   top-level usage. Added bounded inspection of the already buffered response; retest:16 passed.
5. Affected four-suite regression:148 passed. Ruff then found one remaining long string, corrected
   by wrapping only. Final targeted Ruff and git diff --check passed.

Tests use real SDK parsing/adapter/boundary/interpreter with MockTransport, including refusal,
incomplete with/without reason,400 code distinctions,429/503, connection errors, usage and redaction.
Actual V0-V3 runner tests inject adapter failures and forbid travel providers/RAG initialization/
Repair; model calls remain one and V3 resources close. Product API tests retain502 system failure
without internal provider details. Valid structured Safety and normal VALID remain unchanged.
No frontend code changed, so no frontend build; no full V3 suite, live, sizing or formal evaluation.

Open: only a separately approved real-model Case4/5 smoke can establish current provider behavior.
The missing historical metadata cannot be recovered or reclassified by this offline correction.


## 2026-09-25: Provider-filter recovery, CLI imports and budget scope

Implemented + offline-validated; no new live validation. An exact normalized provider error code
content_filter, with provider_request_rejected ownership, now enables an application-authored
message explaining provider filtering and asking the user to rewrite travel preferences. This is
not a domain REWRITE_REQUIRED or SAFETY_BLOCK. Product HTTP response status is provider_blocked;
it exposes only message/action, not raw provider diagnostics, request IDs or sensitive input.
Shared CLI/developer boundary output retains its provider failure category with the same safe
action. Unknown400, other codes and unrelated failures retain system/dependency behavior. No
keyword classification, automatic retry, second model, budget or deployment change was introduced.

The standard V0 --help previously failed in a fresh process: v0.graph imported the preference
leaf service, services.__init__ eagerly imported planning, and planning requested V0StageError
from the partially initialized graph. Planning package exports now load lazily while preserving
existing public imports. Fresh-process --help tests cover all four standard version scripts.
Earlier interpreter smoke success did not establish the standard CLI startup path was healthy.

Shared prompt advances from preference_prompt_12 to preference_prompt_13; wire9, input2 and domain
schema remain unchanged. Total-trip amount means the party total across dates, not mandatory
inclusion of all expense categories. Excluding flights/accommodation/prepaid costs is preserved
as a sourced semantic requirement and does not alone create budget.amount/currency conflict.
Explicit amount, currency and per-person reinterpretation conflicts remain blocked. The application
does not override model classifications. Cost-scope enforcement is not newly implemented; a hard
requirement whose execution is unsupported can still need clarification under existing policy.
Synthetic tests prove contract/mapping behavior, not real-model reduction of false positives.

Execution sequence: initial standard V0 --help reproduced ImportError before calls; after the
lazy export change it exited0. Initial five-suite backend run passed121 tests. Frontend test startup
failed with Vite temporary-directory EPERM (no tests ran); the same offline command with permitted
filesystem access passed16 tests. Initial Ruff found5 formatting/import errors; import fix and line
wrapping/formatting resolved them. Frontend TypeScript/production build passed. Affected boundary,
smoke harness and recovery suites passed76 tests. Final targeted Ruff, frontend ESLint and
 git diff --check passed. No live, formal evaluation, commit or historical artifact change.
