# Frontend and API design

React separates product routes / and /plan from /dev/planner. Vite proxies /api and /health to
FastAPI in development. Product POST /api/planning dispatches through PlanningService to V0;
developer POST /api/dev/planning is explicitly V0-only. Neither exposes V1/V2/config selection.

The product form has structured destination/dates/travelers/preferences, but budget remains
optional while backend total amount/currency is mandatory. Frontend response types omit some
clarification issues. Developer UI retains older free-text input against a structured backend.
These gaps are not completed migrations. ItineraryView separates primary and reference roles;
references are not scheduled or costed activities. Supplied-place wording is stale for Nearby.

[Shared requirements](shared_requirements.md) and [output](shared_itinerary_output.md) own contracts.
[Frontend milestone](frontend_milestone.md) preserves original API/builder behavior and tests;
current documents do not rewrite it as if later input changes existed at the original checkpoint.

## Date and attribution alignment (2026-09-22)

Product date controls load GET /api/planning/date-window from the backend, using its configured-zone
reference date. The14-date calendar window is separate from the10-day maximum inclusive trip.
End max=min(start+9, allowedEnd); backend validation remains authoritative across midnight.
The developer reference-date initial value also comes from the server, but remains an explicit
research override. No default-engine or broader request-form migration is included.
Itinerary presentation includes conditional Open-Meteo attribution and CC BY4.0 link. It does not
claim V0 fetched weather or that forecasts prove future conditions.
