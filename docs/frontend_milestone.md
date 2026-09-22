# Frontend milestone checkpoints

Dated records below preserve original scope, status and evidence; they are not current runtime instructions. Current design is maintained separately. Proposed or unexecuted steps remain unexecuted unless a later explicitly identified record establishes otherwise.

<a id="m-f3db512f7a23"></a>
## Frontend MVP As-Built Milestone

_Source context: original document introduction/navigation. Preserved checkpoint wording; apply its recorded date and status._



<a id="m-9038cac8cf8c"></a>
## Status

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-9038cac8cf8c-0"></a>

- Completion date: 2026-09-11
- Implementation baseline: `e119f6a`
- Implementation, automated checks, and live Azure Foundry acceptance passed.

<a id="m-0d0e286f46ee"></a>
## Automated Tests and Milestone Results

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-0d0e286f46ee-0"></a>

Backend coverage includes Product and Developer HTTP contracts, structured validation,
canonical exact-output and determinism, programmatic V0 integration, defensive
clarification mapping, Product-safe failures, Developer debug behavior, and existing V0
regressions.

<a id="b-0d0e286f46ee-1"></a>

Frontend coverage includes the route trees, browser-local reference date, version-agnostic
Product payloads, form validation, completed itinerary rendering, neutral clarification
messaging, Product-safe failures, duplicate-submission prevention, and Developer V0/raw
response behavior.

<a id="b-0d0e286f46ee-2"></a>

At Frontend MVP milestone completion:

<a id="b-0d0e286f46ee-3"></a>

- `uv run pytest`: 73 passed
- `uv run ruff check .`: passed
- `npm run test`: 16 passed
- `npm run lint`: passed
- `npm run build`: passed
- `git diff --check`: passed

<a id="m-d014b09b773b"></a>
## Live Azure Foundry Product E2E

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-d014b09b773b-0"></a>

The final Product acceptance used Beijing, 2026-10-01 through 2026-10-03, two travelers, a
total budget of 2000 AUD, and the preference `Local food and quiet mornings.`

<a id="b-d014b09b773b-1"></a>

The React submission succeeded, `POST /api/planning` returned HTTP 200 with
`status="completed"`, the expected canonical request was built, and the real
`PlanningService -> V0 -> Azure Foundry` path completed. The itinerary rendered correctly
in `/plan`. The Product API did not expose research/debug fields such as `system_version`,
provider or stage details, or research version identifiers, and the Product UI did not
provide a raw JSON/debug panel.

<a id="b-d014b09b773b-2"></a>

A temporary sandbox network restriction observed during the first live run was an execution
environment limitation, not a code defect.

<a id="m-0f7ef3a35cb0"></a>
## Developer E2E

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-0f7ef3a35cb0-0"></a>

The final `/dev/planner` acceptance confirmed that V0 was the only selectable version, raw
`request_text` remained functional, and `reference_date` remained visible. The real V0 and
Azure Foundry execution succeeded, and the complete `PlanningResult` was displayed as raw
JSON. Product form changes did not alter Developer behavior.

<a id="m-a841a9aab9e8"></a>
## Validation and No-LLM Acceptance

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-a841a9aab9e8-0"></a>

An invalid Product date range was blocked by frontend validation where applicable. The same
invalid request sent directly to the Product API returned HTTP 422. `PlanningService`, V0,
and Azure Foundry were not invoked.

<a id="m-6faafc5f80da"></a>
## Known Limitations

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6faafc5f80da-0"></a>

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

<a id="m-6eb7b2061eb3"></a>
## Explicitly Deferred Functionality

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-6eb7b2061eb3-0"></a>

The following functionality is outside this milestone:

<a id="b-6eb7b2061eb3-1"></a>

- Auth
- Profile
- PostgreSQL
- Saved Trips
- UI polish
- V1, V2, and V3 Developer panels
- Research-version comparison

<a id="m-5290bde95512"></a>
## Post-Milestone Stage 0 Date-UX Update

_Source context: Frontend MVP As-Built Milestone. Preserved checkpoint wording; apply its recorded date and status._

<a id="b-5290bde95512-0"></a>

This section records a later approved Stage 0 shared-contract update. The behavior
below was not part of the original Frontend MVP milestone. In particular, the earlier
Product request example and description of Product `reference_date` document the
historical milestone contract and are superseded by this section for current behavior.

<a id="b-5290bde95512-1"></a>

The Product date inputs now permit only the inclusive browser-local window from today
through today plus nine days:

<a id="b-5290bde95512-2"></a>

```text
start min = today
start max = today + 9 days
end min   = selected start, or today before a start is selected
end max   = today + 9 days
```

<a id="b-5290bde95512-3"></a>

The Product form independently checks the same window and `end_date >= start_date`
before enabling submission. Browser-local year, month, and day fields are used for
formatting and calendar-day arithmetic. The implementation does not derive date-input
values by slicing a UTC `toISOString()` result.

<a id="b-5290bde95512-4"></a>

Product API requests no longer include `reference_date`. The backend captures the
trusted runtime-local reference date and authoritatively validates the requested range,
so bypassing or omitting frontend constraints cannot bypass the shared ten-day policy.
Product requests that attempt to submit `reference_date` are rejected as containing an
unsupported extra field.

<a id="b-5290bde95512-5"></a>

This Stage 0 update does not change:

<a id="b-5290bde95512-6"></a>

- The Product layout or overall Product interaction design
- The Product response contract
- The deterministic canonical request builder for valid structured inputs
- V0 being the active Product planner at this stage
- Developer UI behavior, except that its explicit date remains a trusted research input
- The separation between Product and Developer routes and contracts

<a id="b-5290bde95512-7"></a>

Stage 0 frontend verification completed with 21 tests, passing ESLint, and a passing
production build. Backend validation remains the authoritative security and domain
boundary; the frontend restriction is a user-experience aid.
