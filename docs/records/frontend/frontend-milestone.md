# Frontend milestone checkpoints

Frontend retains its original milestone scope below. The [shared 2026-09-25 notice](../v0-v3/v3-closeout.md#shared-milestone-notice-2026-09-25)
records the historical Product default, version isolation and recovery-UI limitations.

This record preserves the original V0-backed frontend milestone and later date/output
changes. Current [application operations](../../0007-application-operations.md) are
maintained separately; later Product V3 acceptance has its own [record](product-v3-acceptance.md).

## Status

- Completion date: 2026-09-11
- Implementation baseline: `e119f6a`
- Implementation, automated checks, and live Azure Foundry acceptance passed.

## Automated Tests and Milestone Results

Backend coverage includes Product and Developer HTTP contracts, structured validation,
canonical exact-output and determinism, programmatic V0 integration, defensive
clarification mapping, Product-safe failures, Developer debug behavior, and existing V0
regressions.

Frontend coverage includes the route trees, browser-local reference date, version-agnostic
Product payloads, form validation, completed itinerary rendering, neutral clarification
messaging, Product-safe failures, duplicate-submission prevention, and Developer V0/raw
response behavior.

At Frontend MVP milestone completion:

- `uv run pytest`: 73 passed
- `uv run ruff check .`: passed
- `npm run test`: 16 passed
- `npm run lint`: passed
- `npm run build`: passed
- `git diff --check`: passed

## Live Azure Foundry Product E2E

The final Product acceptance used Beijing, 2026-10-01 through 2026-10-03, two travelers, a
total budget of 2000 AUD, and the preference `Local food and quiet mornings.`

The React submission succeeded, `POST /api/planning` returned HTTP 200 with
`status="completed"`, the expected canonical request was built, and the real
`PlanningService -> V0 -> Azure Foundry` path completed. The itinerary rendered correctly
in `/plan`. The Product API did not expose research/debug fields such as `system_version`,
provider or stage details, or research version identifiers, and the Product UI did not
provide a raw JSON/debug panel.

## Developer E2E

The final `/dev/planner` acceptance confirmed that V0 was the only selectable version, raw
`request_text` remained functional, and `reference_date` remained visible. The real V0 and
Azure Foundry execution succeeded, and the complete `PlanningResult` was displayed as raw
JSON. Product form changes did not alter Developer behavior.

## Validation and No-LLM Acceptance

An invalid Product date range was blocked by frontend validation where applicable. The same
invalid request sent directly to the Product API returned HTTP 422. `PlanningService`, V0,
and Azure Foundry were not invoked.

## Known Limitations

- At Frontend MVP milestone completion, Product planning used the V0 plain-LLM baseline and
  relied on model pretraining rather than live external evidence.
- Schema and domain validation exist, but external-evidence-based feasibility and constraint
  validation are not implemented.
- Opening hours, prices, routes, weather, availability, and live events are not verified.
- There is no programmatic itinerary repair or re-validation.
- The defensive clarification outcome has no interactive resolution flow.
- Product failures require the user to review the input and submit again.
- The unauthenticated Developer UI is not suitable for public deployment.
- Itinerary presentation is functional but has not received full UI polish.
- There is no persistence, user-account lifecycle, or saved-trip lifecycle.

## Explicitly Deferred Functionality

The following functionality is outside this milestone:

- Auth
- Profile
- PostgreSQL
- Saved Trips
- UI polish
- V1, V2, and V3 Developer panels
- Research-version comparison

## Post-Milestone Stage 0 Date-UX Update

This section records a later approved Stage 0 shared-contract update. The behavior
below was not part of the original Frontend MVP milestone. In particular, the earlier
Product request example and description of Product `reference_date` document the
historical milestone contract and are superseded at that Stage 0 checkpoint. The active date policy is in
[requirements/evidence](../../0002-requirements-evidence.md).

Stage 0 limited browser-local dates to today through today+9, checked ordered dates
before enabling submission, and avoided deriving calendar dates by slicing UTC ISO
strings. Product stopped sending `reference_date`; the backend captured its trusted
runtime-local reference and rejected extra reference-date fields. Developer retained
its trusted research-date input. Product layout/response and active V0 planning
remained unchanged. This historical +9 window is not the later +13 policy.

Stage 0 frontend verification completed with 21 tests, passing ESLint, and a passing
production build. Backend validation remains the authoritative security and domain
boundary; the frontend restriction is a user-experience aid.

## Compatible transfer output update (2026-09-25)

Frontend participated in the 2026-09-25 optional-transfer compatibility update;
its existing execution path and Product-selection scope were preserved. [Shared DTO/presentation boundary and verification](../v0-v3/v1-development.md#compatible-transfer-output-update-2026-09-25).
