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
