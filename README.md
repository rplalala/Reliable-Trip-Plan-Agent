# Reliable Trip Plan Agent

An LLM-based travel-planning Capstone project investigating reliable itineraries through explicit
version boundaries. V0 uses plain LLM generation, V1 adds external travel information, and V2 adds
TripWorld retrieval for primary candidate discovery. V3 validation and targeted repair are not implemented.

## Current capability

V0/V1/V2 run independently. All accept planning_request_2 with mandatory destination, dates,
traveler count, total-trip budget and currency, plus optional additional_preferences. Nonempty
preferences receive one shared interpretation; empty preferences skip that call. The final
itinerary_2 separates timed primary activities from optional unplanned references.

V1/V2 acquire bounded evidence and use deterministic planning-candidate supply. V2 resolves RAG
candidates to Google-backed identity before canonical merge and shared admission. After successful
primary generation, V1/V2 may search around scheduled places and append up to three independent
Nearby references without changing the primary plan. V0 has no external travel acquisition.

V2 current implementation checkpoint accepted. Tokyo and Sydney bounded development smokes
covered normal RAG and the shared quality_first_1 pipeline.
This is not formal benchmark acceptance, complete correctness or automatic version re-freeze.
Product and developer APIs still run V0; quality_first_1 is now the default V1/V2 runtime policy. Frontend budget and
developer-input alignment remain incomplete. Tokyo Weather coverage limits (Sydney Weather succeeded), SQL variance and generation/evidence
quality limits remain visible, rather than being represented as verified capabilities.

## Quick start

Use Python3.12 and uv. Configure private local .env values from the non-secret .env.example.
Never commit credentials. The ordinary API setup is:

```shell
uv sync
uv run uvicorn backend.app.main:app --reload
```

The health endpoint is GET /health. From frontend/, npm install and npm run dev start the UI;
Vite proxies API traffic to the local backend. These instructions are not executed by documentation work.

Independent entry points are scripts/run_v0.py, scripts/run_v1.py and scripts/run_v2.py, each using
--input-json request.json. V1/V2 accept --runtime-config config/runtime.yaml and
--development-timeout-seconds 600. V2 additionally accepts --rag-env-file .env.tripworld and needs
existing compatible PostgreSQL data/vectors plus the retrieval dependency group. Preparing a request
requires a supported date window; no corpus rebuild is part of ordinary planning. V0 does not accept
those V1/V2 configuration flags. A --reference-date override is for trusted development use only.

## Repository responsibilities

backend/app contains version runners, shared contracts/policies and provider adapters; backend/tests
contains verification fixtures and tests. frontend contains product/developer UI. scripts contains only the V0/V1/V2 runners. tools/data contains offline corpus, embedding and
database preparation; tools/validation owns acceptance harnesses; tools/diagnostics owns current
retrieval, acquisition and payload analysis. Retired selector implementations and exclusive tests
have been removed. config holds the single runtime.yaml with the quality_first_1 policy. docs contains shared and version-specific design, milestones and development records.
PROJECT.md records current scope/status; docs/README.md indexes document responsibilities.
Ignored logs contain real run/call evidence; artifacts contains selected offline results and
.cache contains local tokenizer assets. Source/document/config recovery snapshots were deleted.
Thesis notes, datasets, query vectors and database volumes require independent saving;
a Git source commit does not back them up.
