# Frontend MVP As-Built Milestone

## Status

- Completion date: 2026-09-11
- Implementation baseline: `e119f6a`
- Implementation, automated checks, and live Azure Foundry acceptance passed.

## Purpose and Scope

The Frontend MVP established the minimum complete planning path from a user-facing
React application to the real research planner:

```text
React Product UI
-> Product API
-> PlanningService
-> active research planner
-> Azure Foundry
-> structured itinerary
```

It also established a separate Developer / Research UI for testing natural-language
requirement extraction and inspecting the complete research response. This milestone
covers only the planning vertical slice; account, persistence, and later research-version
functionality are outside its scope.

## Product and Developer Architecture

One React + TypeScript application contains two separate route and layout trees:

- The Product UI is user-facing and version-agnostic.
- The Developer UI is intended for local development and research and is explicitly
  aware of research versions that actually exist.
- The Product API does not expose research or debug fields such as `system_version`,
  provider or stage details, or research version identifiers.
- The Product UI does not provide a raw JSON or debug panel.
- The Developer UI displays the complete `PlanningResult` and V0 debug errors.

The Developer UI has no authentication in this milestone. It must be protected or
disabled before any public production deployment.

## React Routes and Layouts

| Route | Layout | Responsibility |
| --- | --- | --- |
| `/` | `ProductLayout` | Product landing page |
| `/plan` | `ProductLayout` | Structured planning form and itinerary display |
| `/dev` | `DeveloperLayout` | Redirect to `/dev/planner` |
| `/dev/planner` | `DeveloperLayout` | Research workbench and raw JSON display |
| `*` | Standalone | Not Found page |

Product and Developer navigation, visual treatment, inputs, and output presentation are
kept separate.

## Product Planning Form

The Product form requires:

- `destination`
- `start_date`
- `end_date`
- `traveler_count`

Budget is optional. If supplied, both `budget.amount` and `budget.currency` are required.
The optional `additional_preferences` textarea is the only free-text Product input.

The Product form does not accept raw `request_text` and does not display a research
version or `reference_date`. The frontend derives `reference_date` from the browser-local
year, month, and day values rather than from a UTC ISO timestamp.

## Product API Contract

The Product endpoint is:

```text
POST /api/planning
```

Example request:

```json
{
  "destination": "Beijing",
  "start_date": "2026-10-01",
  "end_date": "2026-10-03",
  "traveler_count": 2,
  "budget": {
    "amount": "2000",
    "currency": "AUD"
  },
  "additional_preferences": "Local food and quiet mornings.",
  "reference_date": "2026-09-11"
}
```

`budget`, `additional_preferences`, and `reference_date` are optional. `reference_date`
is an internal transport value used for compatibility with the planner interface and is
not a user-facing Product form field.

A completed response contains:

```json
{
  "status": "completed",
  "requirements": {},
  "itinerary": {}
}
```

A defensive clarification response contains:

```json
{
  "status": "needs_clarification",
  "requirements": {}
}
```

`needs_clarification` covers the defensive case in which the canonical request contains
the structured fields but the active planner still cannot extract them reliably. The
Product UI uses a neutral message and does not imply that the user necessarily omitted an
already completed field.

An active-planner failure produces a Product-safe HTTP 502 response without exposing
internal provider or execution details.

## Developer API Contract

The Developer endpoint is:

```text
POST /api/dev/planning
```

Example request:

```json
{
  "version": "v0",
  "request_text": "Plan a trip to Beijing from 2026-10-01 to 2026-10-03 for 2 travelers.",
  "reference_date": "2026-09-11"
}
```

At Frontend MVP milestone completion, `v0` was the only accepted version. A successful
response is the complete research-facing `PlanningResult`:

```json
{
  "system_version": "v0",
  "requirements": {},
  "itinerary": {}
}
```

The Developer API preserves raw natural-language `request_text`, explicit
`reference_date`, explicit research-version selection, missing-requirement details, and
stage/provider failure details. The Developer UI renders successful and error responses as
raw JSON.

## PlanningService Boundary

`PlanningService` is the version-agnostic application boundary between the Product API and
the research planners. At Frontend MVP milestone completion, the Product active planner was
V0 and the path was:

```text
ProductPlanningRequest
-> deterministic canonical request builder
-> TravelRequest
-> programmatic run_v0(...)
-> PlanningResult
-> Product response mapping
```

The integration calls the programmatic V0 entry point that returns `PlanningResult`. It
does not invoke the CLI, capture stdout, or serialize and parse CLI JSON.

`DeveloperPlanningService` is a separate version-aware boundary that preserves direct V0
execution and the complete research response. The V0 graph, prompts, runner behavior,
DTO/mapping, and CLI entry point were not modified for this milestone.

## Deterministic Canonical Request Builder

`build_canonical_request_text()` is a deterministic pure function that uses only validated
values explicitly supplied in the Product request.

For the example Product request above, the exact output is:

```text
Plan a trip to Beijing from 2026-10-01 to 2026-10-03 for 2 travelers with a total budget of 2000 AUD. Additional preferences: Local food and quiet mornings.
```

The builder does not infer missing information, convert currencies, rewrite preferences,
add activities or purposes, alter dates or traveler counts, or perform semantic
normalization. The Product UI does not display the generated canonical text.

## Product Validation

Frontend validation requires:

- All required structured fields
- An integer `traveler_count` of at least one
- An `end_date` on or after `start_date`
- Both amount and currency when either budget field is supplied
- A non-negative budget amount
- A three-letter uppercase currency code
- No duplicate submission while planning is in progress

Backend Pydantic validation independently enforces the structured contract, date range,
traveler count, budget constraints, and forbidden extra fields. Product requests containing
research fields such as `version` or raw `request_text` are rejected.

Invalid Product requests return HTTP 422 before `PlanningService`, V0, or Azure Foundry is
invoked. Schema and domain validation are therefore present in this milestone. What is not
yet implemented is external-evidence-based feasibility and constraint validation of the
generated itinerary.

## Separation from Research Versions

The Product frontend depends only on the stable Product contract and neither imports nor
submits `system_version`. At Frontend MVP milestone completion, the Developer frontend
explicitly exposed only the implemented V0 research version; it contained no V1, V2, or V3
placeholders, disabled panels, or fake implementations.

This separation allows the Product active planner to change behind `PlanningService`
without making research-version selection part of the normal Product experience.

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

A temporary sandbox network restriction observed during the first live run was an execution
environment limitation, not a code defect.

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

## Expected Direction After V3

After V3 is implemented and independently verified, the Product active planner is expected
to move from V0 to V3 behind `PlanningService`. The core Product API should remain
version-agnostic, and existing Product clients should remain backward compatible. V3 may add
justified user-facing information through backward-compatible optional fields.

The Developer UI should add V1, V2, and V3 only as those versions are actually implemented.
Formal comparison functionality remains subject to separate approval and design.

## Post-Milestone Stage 0 Date-UX Update

This section records a later approved Stage 0 shared-contract update. The behavior
below was not part of the original Frontend MVP milestone. In particular, the earlier
Product request example and description of Product `reference_date` document the
historical milestone contract and are superseded by this section for current behavior.

The Product date inputs now permit only the inclusive browser-local window from today
through today plus nine days:

```text
start min = today
start max = today + 9 days
end min   = selected start, or today before a start is selected
end max   = today + 9 days
```

The Product form independently checks the same window and `end_date >= start_date`
before enabling submission. Browser-local year, month, and day fields are used for
formatting and calendar-day arithmetic. The implementation does not derive date-input
values by slicing a UTC `toISOString()` result.

Product API requests no longer include `reference_date`. The backend captures the
trusted runtime-local reference date and authoritatively validates the requested range,
so bypassing or omitting frontend constraints cannot bypass the shared ten-day policy.
Product requests that attempt to submit `reference_date` are rejected as containing an
unsupported extra field.

This Stage 0 update does not change:

- The Product layout or overall Product interaction design
- The Product response contract
- The deterministic canonical request builder for valid structured inputs
- V0 being the active Product planner at this stage
- Developer UI behavior, except that its explicit date remains a trusted research input
- The separation between Product and Developer routes and contracts

Stage 0 frontend verification completed with 21 tests, passing ESLint, and a passing
production build. Backend validation remains the authoritative security and domain
boundary; the frontend restriction is a user-experience aid.

## Future Product UI Evidence Display

This is future work, not part of the Frontend MVP or the current Product UI. For a POI
that appears in the final itinerary, a future Product UI may display its actual
acquired Google Places `rating`. If that POI also has retrieved review evidence and
an `ExperienceProfile` summary, the UI may display one concise review-derived
summary. The summary must come from the retrieved reviews and `ExperienceProfile`,
not from the planner's or an LLM's general knowledge. Do not fabricate ratings or
review summaries for POIs without the corresponding acquired evidence. Do not
display `userRatingCount`.
