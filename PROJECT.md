# Capstone Project Context

## Title

**An LLM-Based Travel Planning System for Feasible and Reliable Itinerary Generation**

## Research Goal

This project studies how to make LLM-generated travel itineraries more feasible and reliable. A practical motivation is that travelers may not know a destination well enough to recognize hidden errors in a plausible-looking plan.

The system develops through four comparable research versions:

```text
V0  Plain LLM
V1  V0 + external information and tools
V2  V1 + RAG
V3  V2 + explicit feasibility validation, targeted repair, and re-validation
```

The versions should differ mainly by their intended added mechanism. Preserving that distinction is essential for later evaluation.

## Current Scope

The current stage is system design and development: architecture, backend and necessary frontend implementation, provider integration, evidence normalization, runtime configuration, observability, and implementation testing.

Formal benchmark design, cross-version evaluation, experiment analysis, thesis writing, and final research conclusions are deferred. Small pilot scenarios and live-provider runs may verify integrations and implementation behavior, but are not formal research results.

Introduce infrastructure only when the current version has a concrete need for it. V0 and V1 do not require an application database.

# Research Versions

## V0 — Plain LLM

```text
User request → Requirement extraction → LLM generation → Structured itinerary
```

V0 is the plain-LLM baseline. It does not acquire external planning evidence, use RAG, or perform general feasibility validation and repair.

V0 may still enforce shared project-level input and output contracts, including the trip-date policy below. For requests valid under those contracts, preserve its requirement extraction, model configuration, output schema, base planning objective, and general generation semantics where practical.

## V1 — External Information and Tools

V1 adds bounded, application-controlled external evidence to the otherwise comparable V0 planning flow:

```text
Requirement extraction
→ External information acquisition
→ Typed evidence normalization
→ Evidence-informed itinerary generation
```

V1 is **one research version** with two active implementation milestones:

| Milestone | Purpose | Status |
| --- | --- | --- |
| V1-A | Google-backed travel evidence and POI selection | Revised implementation live-validated and explicitly re-frozen on 2026-09-14 |
| V1-B | Official and current Web evidence for final selected POIs | Phase 1/2 and Phase 3 implemented and development-live-validated |

**Complete V1 is frozen as of 2026-09-15** following final offline checks and cross-country development live validation. The original V1-A 2026-09-12 freeze and revised V1-A 2026-09-14 re-freeze remain separate historical checkpoints.

V1-A discovers and selects POIs using Google Places evidence, alongside Google Weather and Routes. The revised selection flow is cheap candidate discovery, structured narrowing, selective Place Details plus rating, further narrowing, selective reviews, review-derived `ExperienceProfile`, and final POI selection. Rating and reviews inform selection; neither is required for every candidate. Do not use or display `userRatingCount`.

V1-A was originally frozen on 2026-09-12, then intentionally reopened for rating/review-aware POI selection and explicitly re-frozen on 2026-09-14. The original freeze remains a separate historical checkpoint. The former V1-C milestone is retired from the active architecture; Places review evidence now belongs to V1-A.

After the revised V1-A checkpoint, V1 migrated free-form user semantics into one V1 requirements LLM call returning unchanged `TravelRequirements` plus bounded `NamedPlaceIntent`, `RequestedPlaceInformation`, `ExperiencePreferenceIntent`, transport preference, and `PoiInterest`. Application code validates source spans and typed values, reconciles Place IDs, and deterministically executes selection, routing, and evidence acquisition. The active V1 graph does not use raw-text keyword/regex fallback to reinterpret these meanings. V0's requirements contract and execution path remain unchanged.

V1-B addresses decision-relevant official/current information gaps that structured providers cannot reliably answer, such as temporary closures, special opening hours, admission, tickets, and reservations. It does not broadly re-check every selected POI or facts already sufficiently answered by structured evidence.

V1-B supplements only final selected POIs with current first-party official evidence. Its integrated path projects stable selected Place IDs and structured facts, plans targeted Web tasks for explicit residual needs or concrete operational/date risks, acquires bounded Luna Web and optional official pages, then runs EvidenceReasoner, a deterministic Grounding / Provenance Gate, and a claim-scoped EvidenceResolver. Accepted/effective facts and explicit uncertainty reach the planner; raw search observations and rejected claims do not. Normal Web/Page budgets are 6/6. These are pre-planning evidence controls, not V3 itinerary-feasibility validation.

Rating remains a quantitative Places signal. `ExperienceProfile` represents retrieved-review evidence for deterministic POI selection; unsupported signals remain unknown. The LLM does not select the final POI set, and reviews/Profile are not passed to the itinerary prompt. Neither rating nor reviews may override an official date-specific closure. Any future frontend rating/review display must use actually acquired evidence for itinerary POIs; frontend work is not implemented.

V1 may instruct the generator to use supplied evidence carefully—for example, not to plan a clearly non-walkable transfer as an ordinary walk or invent unsupported transit details. This is still **evidence-informed generation**, not general post-generation feasibility validation. An itinerary may therefore violate supplied evidence even when that evidence was acquired correctly.

V1 retains point-valued shared `Money` and optional activity `estimated_cost`. At its Foundry mapping boundary, V1 preserves valid points, converts a clear finite same-currency two-endpoint numeric range to a Decimal midpoint, and sets unsupported optional costs to `null`. This uses no LLM repair call and does not turn a derived activity estimate into accepted official admission evidence or alter V0.

V1 does not implement RAG, a free-form agentic tool loop, general violation detection, targeted repair, or re-validation.

## V2 — RAG

V2 adds retrieval grounding to V1. The planned offline knowledge sources are TripWorld for relatively stable destination, POI, and travel-pattern knowledge, with TP-RAG as a possible China-specific supplement.

RAG should help identify relevant places, areas, combinations, and typical visit patterns; it should not replace live verification. Dynamic facts such as current opening status, disruptions, weather, route duration, and ticket changes should come from current sources.

TripWorld Phase 1-4 data preparation, deterministic global RetrievalEntity construction,
and the isolated OpenAI embedding spike have been accepted as complete. Phase 5 is
also explicitly accepted as complete; Phases 1-5 form the frozen technical baseline
as of 2026-09-18, except for concrete bug fixes. Phase 5 implemented and validated a
persistent PostgreSQL + pgvector retrieval layer using ENRICHED
text and OpenAI `text-embedding-3-small` at 1536 dimensions. See
`docs/tripworld_phase4.md` and `docs/tripworld_phase5.md` for implementation status and
validation evidence. This retrieval service remains separate from the V1/V2 candidate
funnel; no V1 selection or itinerary-generation behavior changes are authorized here.
The complete V2 planning version is not implemented or frozen. Phase 6 is design-only;
`docs/tripworld_phase6_proposal.md` requires separate approval before implementation.

Future Google usage must be demand-driven: resolve only the ranked TripWorld candidates
needed for a trip, trying an existing Google Place ID first and name/location fallback
when needed. Drop unresolved candidates and continue within request budgets. Do not
prevalidate the global corpus. The Google resolution bridge and candidate merge belong
to a separately approved Phase 6.

## V3 — Validation, Targeted Repair, and Re-validation

V3 adds explicit feasibility checking after evidence-informed generation:

```text
Draft itinerary
→ Feasibility validation
→ Violation detection
→ Targeted repair when needed
→ Re-validation
```

Candidate checks include budget, opening hours, transfer time, weather suitability, activity density, required or excluded activities, and operationalized user preferences.

Validation should be deterministic where practical. Repair should focus on affected itinerary components and preserve already-valid content rather than defaulting to full regeneration.

Shared date input/output checks in V0–V3 are project-wide contracts. They are **not** the general feasibility-validation mechanism studied in V3.

# Shared Trip-Date Policy

Every version uses the same supported planning window. Fix the runtime reference date once at run start:

```text
reference_date <= start_date <= end_date <= reference_date + 9 days
```

The final itinerary may contain dates only within the requested trip range:

```text
Final itinerary dates
⊆ Requested trip dates
⊆ [reference_date, reference_date + 9 days]
```

The backend enforces this contract deterministically, including for direct API calls. Frontend date restrictions provide user guidance but are not the authority. Tests may inject a fixed date; production requests must not use arbitrary caller-supplied reference dates to bypass the real runtime window.

# Engineering Architecture

Use a modular monolith:

```text
React + TypeScript frontend
          ↓ HTTP / JSON
FastAPI backend
          ├─ Version-specific planning graphs and entry points
          ├─ Application services and evidence acquisition
          ├─ Typed schemas, policies, and evidence normalization
          ├─ LLM and external-provider integrations
          ├─ Runtime configuration and Run Trace
          └─ RAG, validation, repair, and persistence only when needed
```

Planning, orchestration, evidence acquisition, RAG, validation, and repair belong in the backend. The frontend collects requirements, calls the APIs, and presents results; it should not own research-critical planning logic.

Keep V0, V1, V2, and V3 independently runnable through explicit version-specific graphs and entry points, such as `scripts/run_v0.py` through `scripts/run_v3.py`. Do not implement all versions as one large graph controlled mainly by version conditionals. Do not create future-version modules before they are required.

## Provider and Evidence Boundaries

LangGraph nodes should call internal services, not third-party APIs directly:

```text
Graph node → Acquisition service → Provider integration → External API
```

Provider integrations own authentication, API requests, provider DTOs, response mapping, and provider-specific errors. The evidence layer deterministically converts provider-facing models into typed internal planning evidence. Raw provider payloads should not be passed through the graph or directly into planner prompts.

Use evidence types suited to their purpose rather than requiring one universal `Evidence` schema. Preserve source identity, retrieval time, availability, uncertainty, and provenance where relevant. Distinguish provider-observed information from derived estimates.

Evidence authority depends on the claim. Official notices are usually strongest for official operational changes; structured route and weather providers are appropriate for their respective measurements; visitor accounts can support subjective experience. Do not silently promote uncertain or subjective evidence into confirmed factual claims.

## Bounded Tool Use

External acquisition is deterministic and application-controlled where practical. Use a request-level ToolBudget for candidate search, enrichment, weather, routes, web queries, and other provider work. Avoid hidden fan-out and unconstrained LLM-selected tool loops.

Request-scoped caching may deduplicate identical operations within a run. Do not introduce persistent evidence caching solely for V1.

# Runtime Configuration and Observability

`config/runtime.yaml` is the global source for non-secret runtime policy, including normal ToolBudget limits, application time zone, logging, and Run Trace settings. One centralized code-level definition sets project-wide ToolBudget hard safety ceilings:

```text
Global hard limit → runtime.yaml limit → per-run usage
```

Changing a normal limit within its hard boundary should require only a YAML change. Policies should not introduce hidden secondary ToolBudget caps. Invalid, missing, malformed, or out-of-range runtime configuration must fail fast rather than silently fall back.

Keep secrets and genuine deployment-specific values outside committed runtime policy, typically in `.env`. Never commit credentials, raw provider or LLM payloads, or runtime logs.

Each development run should have a `run_id` and lightweight Run Trace sufficient to inspect its configuration, progression, evidence provenance, tool usage, failures, and outcome. Record a sanitized effective runtime configuration and stable hash for reproducibility. Payload capture should be configurable, and credentials must be redacted from traces and runtime logs.

Trace and logging **write failures** should be best-effort and should not change planning semantics. This does not apply to configuration validation failures, which must fail fast.

# Database Direction

Do not introduce PostgreSQL, pgvector, or another persistence system merely because it is in the preferred stack. V0 and V1 can use per-run state, request-scoped cache/deduplication, and file-based Run Trace without an application database.

Introduce persistence or vector storage only when a concrete capability—potentially V2 retrieval or later saved application data—requires it. Run Trace is observability, not an application evidence database.

# Version Preservation and Development Rules

Keep versions comparable by preserving, where practical, the shared input contract, requirement-extraction behavior, LLM model/configuration, output schema, and base planning objective. Later versions may reuse shared schemas, policies, services, and integrations, but must not silently redefine earlier research behavior.

Implementation completion and freeze are separate. Passing tests or a live smoke run does not freeze a milestone; freeze requires explicit user approval and accurate documentation. Detailed V1 architecture and milestone history belong in `docs/v1_design.md` and `docs/v1_milestone.md`, not this project-level document.

Development principles:

- Add only the mechanism required by the current approved stage.
- Preserve independently runnable and comparable V0–V3 paths.
- Keep external evidence acquisition separate from general feasibility validation.
- Use typed normalized evidence with explicit uncertainty and provenance.
- Keep tool use bounded, observable, reproducible, and application-controlled.
- Keep secrets separate from committed runtime policy.
- Prefer focused tests with fake providers; use live runs for integration verification, not formal evaluation.
- Avoid premature databases, microservices, future-version modules, and unnecessary frontend complexity.
- Document meaningful post-freeze changes without rewriting historical milestones.
- Do not begin formal research evaluation or thesis work until explicitly requested.
