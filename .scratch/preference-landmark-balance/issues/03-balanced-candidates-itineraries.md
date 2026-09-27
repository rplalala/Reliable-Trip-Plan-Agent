# 03: Balance preference coverage and landmarks through final itinerary generation

**What to build:** Travelers receive candidate opportunities and final itineraries
that accommodate soft interests while retaining representative local landmarks,
alternatives and varied experiences. Preference saturation does not impose category
caps or remove independent landmark value. Deliver the integrated behavior across
the four independent versions with verified resource and authority boundaries.

**Parent:** [Preference coverage and local landmark balance](../spec.md).

**Blocked by:** None. Prerequisite tickets 01 and 02 are implemented and offline validated.

Status: resolved
Type: task

## Acceptance criteria

- [x] The shared grounded selection/generation flow consumes ticket 01's soft-target
  semantics and ticket 02's resolved model-origin landmark metadata. Landmark
  opportunity survives bounded merging and final supply selection rather than being
  recorded only as an unused discovery result.
- [x] Repeated discovery associations with the same ordinary preference do not keep
  monopolizing candidate opportunity. Candidate balancing retains meaningful
  alternatives rather than selecting exactly one/two matching POIs and discarding
  replacements needed for dates, routes or admission.
- [x] Candidate opportunity and final coverage remain distinct: selected candidates
  never count as fulfilled until actually scheduled. Final coverage retains the
  source-backed ordinary/focus distinction and supported multi-interest matches.
- [x] After a final soft target is met, its extra preference priority is saturated.
  Additional same-category landmarks remain eligible because classic value and
  support for other uncovered preferences are independent dimensions.
- [x] A landmark may also be preference-matching; general landmark opportunity is
  not defined solely as candidates unmatched to every preference. A third museum
  can still be selected for its independent value after museum coverage is met.
- [x] Explicit user counts, maxima, named visits, exclusions and exclusive scopes
  preserve precedence. Landmark rank remains soft and cannot override confirmed
  infeasibility, reliable identity/admission checks or an explicit restriction.
- [x] Generation instructions combine representative destination coverage with
  dates, routing, available time and experience variety. No fixed category ratio,
  geographic quota, extra generation call or forced filling of every hour is added.
- [x] Constrained trips may leave some soft preferences uncovered and disclose the
  gaps without fabricating satisfaction, converting them to CONFIRMED findings or
  activating a new V3 Repair mechanism.
- [x] Nomination/generation guidance discourages repetitive site fragments while
  preserving explicit separate-visit requests. Suspected overlap alone does not
  justify hard deletion, canonical identity merging or a parent-site inference.
- [x] Nomination/identity failure still permits qualified fallback planning, with
  truthful missing-landmark and soft-coverage diagnostics. Integrated prioritization
  does not bypass the one-call, token/time or twelve-search/four-supplement bounds.
- [x] Existing candidate, Details, final-supply, RAG, semantic, route and Repair
  limits remain intact; nomination is not rerun to fill gaps and no second primary
  generation is introduced.
- [x] V0 uses only the accepted prompt principles in its existing flow; grounded
  canonical ranking and coverage enforcement do not leak into V0. V1/V2 remain
  without Repair, and V3 retains its existing authority and UNKNOWN handling.
- [x] End-to-end fixtures cover preference-dense requests, overlapping interests,
  same-category landmarks after saturation, a third eligible landmark, unavailable
  preference candidates with alternatives, restrictive requests, constrained time,
  fallback, and short/long trip capacity. Use several synthetic destinations rather
  than a hard-coded Paris fixture as the sole acceptance criterion.
- [x] Tests inspect observable supplied/generation context, final progress/output
  and actual collaborator usage; they do not manufacture a live quality guarantee
  from fake LLM responses or treat rank as evidence of operating facts.
- [x] All four independent execution paths pass the relevant full backend suite.
  Affected API/presentation and bounded observability checks, applicable lint/format
  checks, Standards/Spec review and necessary corrections are complete.
- [x] Current project/design/configuration documentation is synchronized with actual
  implemented behavior; dated development records preserve failures, corrections,
  retests and remaining limits. Specification readiness is not described as live
  validation, version freezing or demonstrated cross-version superiority.

## Verification and delivery

Use the approved existing planning entry points with injected collaborators and the
nomination adapter checks delivered by ticket 02. Each preceding ticket must already
be independently verified; this ticket exercises their combined externally visible
policy rather than postponing all testing until integration.

Before closeout, account for every required observable scenario in the parent spec
across the three completed tickets. Record which evidence is offline only. Any
subsequent live pilot requires a separately prepared plan with cases, attempts,
network/retry rules, capture locations, acceptance criteria and approved budgets;
the established smoke-test conversation executes it. No live attempt is required or
authorized to close this offline implementation ticket.

## Boundaries

No formal benchmark, Paris-specific tuning, parent-site graph, non-main dining
feature, new V0 mechanism, V1/V2 Repair, or soft-goal expansion of V3 Repair authority.
No unapproved budget increase, Git action or version freeze. Preserve earlier
uncommitted work and historical smoke/validation artifacts.

## Comments

- 2026-09-28 closeout: user accepted the feature after focus-rule correction and bounded
  Melbourne V3 revalidation. Implementation saved in4084a2f; pilot tooling in274ab27.
  Final combined regression1808 passed/9 skipped. See [closeout](../closeout.md) for the
  interrupted-test/rerun sequence, live limits and local commit grouping. No version freeze.

- 2026-09-27: The user approved this integration slice as blocked by both 01 and 02.
  Tests, review and related documentation are included in each ticket; this slice
  owns combined behavior and final cross-version regression.

- 2026-09-28: Implemented against `cc4d5a0`; uncommitted. Full backend 1793 passed /
  9 skipped; scoped Ruff/diff checks and Standards/Spec re-review passed. Multi-ref intent
  saturation failure was reproduced and corrected before final regression. Scenario
  coverage across tickets 01-03 is in [verification](../verification.md). No live quality,
  latency, cost or superiority claim; no version freeze or new Repair authority.
