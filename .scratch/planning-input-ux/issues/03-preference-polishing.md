# Gate-aware preference polishing with preservation review

Status: resolved
Type: task
Approval: Approved by the delegated scope agent under the user's 2026-09-26 instruction; implemented without live calls or commit.
Blocked by: Real-model Gate-success testing requires separate authorization.
Spec: [Planning input UX](../spec.md)

## Scope and interfaces

Implement POST /api/input-assistance/preferences/polish using a dedicated service, strict
schemas and bounded external-model adapter. Reuse existing model configuration/client ownership
patterns, not the planner runner or interpretation Gate as an optimization loop. Share any
input-assistance router/config introduced by 02 rather than creating a competing endpoint.
Expected files: assistance API/schemas, services/preference_polishing.py, dedicated prompt/adapter,
input_assistance config, frontend planning API/types, PreferencePolisher.tsx and PlanningForm.tsx.

Input/output/error contracts and budget are defined in the spec. Keep original text and
read-only structured context, revision checking, preview/Apply/Dismiss/Undo. Applying a
suggestion invalidates prior planning results using the existing onEdit contract. Normal
planning still runs the unmodified Gate. No changes to shared requirement semantics/prompts.

## Call budget

<=4,000 source characters / 1,500 tokens, with no truncation. One draft plus at most one
preservation-review call, no retries, no automatic Gate call or resubmission. <=8,000 total
input tokens per call, <=2,000 draft output and <=1,000 reviewer output; 20 s/call within
40 s total. Three manual attempts/form, one in-flight/process, 20 operations/day/process.
Count attempts that already started; missing configuration or invalid input makes no call.
Input exceeding assistance limits remains available for normal planning under its existing
larger limit. Cancellation, failure and uncertain fidelity never replace the original.

## TDD examples and slices

1. Model boundary and API: two calls at most, structured output validation, bounded token
   envelopes/timeouts, no SDK retry, injected late/cancelled response and input budget rejection.
2. Preservation controls with controlled model fixtures:
   - mountain climbing + zoo + rich trip retains those wishes, without indoor substitution,
     mandatory strengthening, invented quotas or a luxury-spending interpretation;
   - exactly two British Museum visits on different dates preserves identity/count/date scope;
   - do not visit zoos retains negation; at least twice does not become exactly twice;
   - wheelchair step-free access and must/optional conditions retain their strength;
   - exclude flights/hotels from budget preserves expense scope without changing the amount;
   - preference destination/budget conflicting with form context returns needs_input;
   - unsupported mandatory conditions stay mandatory; unclear decisive references ask for input;
   - irrelevant or adversarial instructions cannot alter form fields or generate a Gate-pass claim.
3. Reviewer rejection/uncertainty and explicit number/date/currency mismatch suppress Apply.
   A model safety/provider block produces a sanitized blocked result, never a bypass rewrite.
4. UI: original and candidate side by side, explicit Apply/Undo, unchanged/needs_input views,
   edit-during-request and context changes invalidate results, duplicate clicks are prevented,
   failures preserve text, applying never starts planning automatically.
5. Controlled real Gate/service boundary regression: compatible examples remain compatible;
   genuine conflicting/unsupported hard requests are not silently converted into valid requests.
   Tests with mocked models verify behavior, not actual model equivalence or pass-rate gains.

## Acceptance

Service/API and shared Product/Dev page regressions pass, including 01/02 behavior. Offline
browser verifies suggestion, uncertainty, error and stale-result states without live calls.
No promise of guaranteed equivalence or Gate success appears in UI/docs. No planning/Repair
budget is consumed or changed. Record the prompt identity and implementation test examples.
Any claim that real-model Gate success improved requires separately authorized, small
development-time testing; no formal benchmark or automatic repeated optimization is included.

## Comments

- 2026-09-26: User explicitly prioritized better Gate acceptance while preserving meaning.
  The proposed preservation-review call is an additional safeguard requiring spec approval;
  preview and the normal Gate remain necessary because model review is fallible.
- 2026-09-26: Implemented explicit draft/review service, bounded model adapter, strict API and
  shared Product/Dev preview with Apply/Dismiss/Undo and stale-response guards. First backend and
  UI tests were red for missing modules; implementation made them green. The full backend suite
  first exposed missing runtime-config documentation and token-budget trace redaction handling;
  both were corrected. Standards review found client-cleanup failure handling, and Spec review
  found date/currency-token and malformed-model error mapping gaps; regression tests were red
  before fixes, green after fixes, and both review axes rechecked. Prompt identities are
  preference_polish_1 and preference_preservation_review_1. Fake-model tests cover mountain,
  zoo and rich-trip wording; exact named revisit, negation, accessibility, budget scope,
  structured conflict, provider block and uncertain review. No actual model-fidelity or
  Gate-success improvement is claimed.
