# Reliable Trip Plan Agent

An LLM-based travel planning system focused on generating feasible and reliable itineraries.

The project will be developed as four independently runnable versions:

- V0: plain LLM planning
- V1: V0 plus external information and tools
- V2: V1 plus retrieval-augmented generation
- V3: V2 plus constraint validation, targeted repair, and re-validation

V0 is the implemented plain-LLM baseline. It uses a fixed two-stage LangGraph workflow:

```text
User request -> requirement extraction -> LLM generation -> structured itinerary
```

V0 uses only the configured model deployment's pretrained knowledge through a Microsoft
Foundry OpenAI-compatible endpoint. It does not use external tools, web search, RAG,
validation, repair, weather, routes, places APIs, or persistence.

V1-A is also independently implemented. It preserves the V0 requirement and result contracts,
then adds bounded Google Places, Weather Daily Forecast, and Route Matrix evidence before final
generation. V1-A has no Web Search, reviews, RAG, validation/repair loop, or database.

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

## Setup

Install the project and development dependencies:

```shell
uv sync
```

Copy `.env.example` to `.env`, then provide the Microsoft Foundry endpoint, deployment, and
API key. `LLM_MODEL` records the underlying model shared by all system versions, while
`AZURE_OPENAI_DEPLOYMENT` identifies the deployment sent in the API request's `model` field.
The two values may differ and neither is hard-coded in a graph or node. The Foundry endpoint
uses the OpenAI-compatible `/openai/v1` API and does not require an API version setting.

V1-A additionally requires `GOOGLE_MAPS_API_KEY`. `APP_TIME_ZONE` controls the explicit IANA
calendar time zone used by production date sources and defaults to `Australia/Sydney`.

## Run V0

Run the independently executable V0 entry point:

```shell
uv run python scripts/run_v0.py --request "Plan three days in Kyoto starting tomorrow."
```

Provide a fixed reference date when the request contains relative dates:

```shell
uv run python scripts/run_v0.py \
  --request "Plan three days in Kyoto starting next Monday." \
  --reference-date 2026-09-11
```

`--reference-date` is a trusted research and testing override. Normal Product requests use the
backend's configured-zone runtime date and cannot supply an alternative reference date.

Every planner version shares an inclusive ten-day planning window. For a reference date of
`2026-09-11`, requested and generated itinerary dates must stay between `2026-09-11` and
`2026-09-20`. A short trip outside that window is invalid even when its duration is less than
ten days.

The command prints a `PlanningResult` JSON object. If destination, start date, or end date is
missing after requirement extraction, V0 exits without generating an itinerary and reports the
unresolved fields.

## Run V1-A

Run the independent V1 entry point after enabling Places API (New), Weather API, and Routes API
for the configured Google Maps Platform key:

```shell
uv run python scripts/run_v1.py --request "Plan two days in Sydney starting tomorrow."
```

The trusted `--reference-date` research override is also supported. Normal V1 CLI runs create a
best-effort local trace under `logs/`; raw provider and LLM payloads remain disabled unless
`V1_TRACE_PAYLOAD_MODE=raw` is explicitly configured. The Product API continues to use V0.

## Development checks

Run the test suite:

```shell
uv run pytest
```

Run static lint checks:

```shell
uv run ruff check .
```

Run the development API:

```shell
uv run uvicorn backend.app.main:app --reload
```

The health endpoint is available at `GET /health`.

## Run the frontend

Install the frontend dependencies:

```shell
cd frontend
npm install
```

Start the Vite development server:

```shell
npm run dev
```

The frontend uses relative API URLs. During local development, Vite proxies `/api` and
`/health` to the FastAPI server at `http://127.0.0.1:8000`.

The product routes are `/` and `/plan`. Product planning calls `POST /api/planning` through a
version-agnostic service boundary. The service currently uses the programmatic V0 planner and
can later switch to V3 without exposing a research version to product clients. Product clients
submit explicit destination, date, and traveler fields, plus optional budget and preference
fields. The service deterministically builds the natural-language request consumed by V0.

The developer workbench is available at `/dev/planner` and calls `POST /api/dev/planning` with
an explicit implemented research version. It currently supports only V0 and intentionally
shows raw planning and debug responses. This local development functionality must be protected
or disabled before a public production deployment.

Run the frontend checks:

```shell
npm run test
npm run lint
npm run build
```

## Current structure

```text
backend/
├── app/
│   ├── api/
│   ├── evidence/
│   ├── integrations/
│   ├── llm/
│   ├── observability/
│   ├── policies/
│   ├── runtime/
│   ├── schemas/
│   ├── services/
│   └── versions/
│       ├── v0/
│       └── v1/
└── tests/
frontend/
└── src/
    ├── app/
    ├── features/
    ├── layouts/
    ├── routes/
    └── shared/
scripts/
├── run_v0.py
└── run_v1.py
```

Future version-specific code and entry points will be added only when each version is approved.
Shared result schemas remain limited to fields common to every version; evidence, retrieval,
validation, and repair data use version-specific contracts.
