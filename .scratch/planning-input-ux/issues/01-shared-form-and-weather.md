# Shared currency/date controls and compact weather

Status: resolved
Type: task
Approval: Approved by user on 2026-09-26; implemented without live calls or commit.
Blocked by: None.
Spec: [Planning input UX](../spec.md)

## Scope

Implement spec sections 2-4 in the shared Product/Dev components. Introduce the single currency
list/select with AUD default, controlled ISO date input plus English calendar (including Dev
reference date), and compact daily weather strip. Preserve date-window ownership, existing
planning request payloads, onEdit invalidation and all V0-V3 behavior. No external calls.

Expected files: PlanningForm.tsx, ItineraryView.tsx, datePolicy.ts, DeveloperPlannerPage.tsx,
styles/global.css, new CurrencySelect/TripDateInput components and currency data under the
planning feature; their direct tests. Update form consumers/tests for the intentional control
changes, without weakening request/status assertions. Avoid unrelated styling or UI redesign.

## Interfaces and budget

CurrencySelect is controlled by code value/onChange/disabled; unknown codes cannot be entered
through the UI. TripDateInput accepts value/onChange/label/min/max/disabled; incomplete edits
remain editable but cannot submit. Weather reads the existing ProductWeather shape. No backend
schema change, provider/model call or new endpoint. A new UI dependency requires a documented
accessibility and maintenance choice, not automatic installation in this planning task.

## TDD slices

1. Currency defaults to AUD and selecting another listed code changes only currency; search,
   keyboard selection and required budget validation work. Both page request payloads stay valid.
2. Strict dates reject February 30, partial text and out-of-window ranges before ISO arithmetic;
   leap day, DST/timezone boundaries, inclusive ten-day limit and Dev reference override work.
3. Calendar keyboard navigation, Escape/focus return and disabled states work. Date labels and
   visible values remain ISO/English with Chinese browser locale; lang-only workarounds do not pass.
4. Weather has one desktop strip, retained source credit/units, honest missing-data behavior
   and narrow-screen wrapping; itinerary content/order and completion warning remain unchanged.

## Acceptance

Shared component/page tests, full frontend tests and TypeScript/Vite build pass. Offline browser
inspection at desktop and 375 px width shows no overflow, no Chinese date segments and readable
keyboard focus. Product and Dev submit unchanged ISO fields and selected currency. Calendar
date policy remains backend-authoritative. No backend/runtime budget/default changes.

## Comments

- 2026-09-26: Proposed first slice; no implementation or tests executed in the planning task.
- 2026-09-26: Implemented the shared currency select/search, strict ISO text dates with an
  English keyboard-accessible calendar in Product and Dev, and compact daily weather with
  retained attribution. Existing planning request fields and V0-V3 dispatch are unchanged.
  Red tests first covered date validity, currency selection, calendar navigation and weather
  layout. Full frontend suite passed (70 tests); TypeScript/Vite build and ESLint passed.
  Offline browser inspection at desktop and 375 px covered Product and Dev; neither had
  horizontal overflow. Browser activity called only the local date-window API, not planning,
  model or provider endpoints. Tasks 02 and 03 remain pending user approval.
