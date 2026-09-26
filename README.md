# Reliable Trip Plan Agent

An LLM-based travel-planning Capstone project with four independently runnable versions: V0
uses plain model generation, V1 adds external travel information, V2 adds TripWorld retrieval,
and V3 adds validation, targeted repair and re-validation. [PROJECT.md](PROJECT.md) records
the current engineering state and evidence boundaries.

## Current application

The Product page at `/plan` runs V3. The Developer page at `/dev` offers independent V0–V3
runs from a shared input snapshot. Both forms require a destination, dates, traveler count
and whole-trip budget, with optional preferences. The Product API can return the latest
itinerary with an incomplete policy status; completion is shown separately from the itinerary.

Shared input assistance includes a selectable currency, locale-independent date input and
GeoDB city suggestions. Selecting a suggestion fills the city/region/country label; manual
destination entry remains available. FastAPI calls the public free GeoDB service over HTTPS
and normalizes its response. The browser does not call GeoDB directly.

The optional **Polish preferences** action makes at most one model call. A schema-valid rewrite
is displayed beside the original for the user to Apply or Dismiss; an applied rewrite can be
undone. The prompt asks the model to preserve meaning, but the application does not perform
a second preservation review or suppress a rewrite based on local semantic comparisons.
The normal planning Gate still runs when the user submits the form. Daily weather is shown
compactly alongside the itinerary.

## Local development

Use Python 3.12, the repository's virtual environment, and private local credentials based on
`.env.example`. On Windows, start FastAPI with the project's event-loop-compatible launcher:

```powershell
.\.venv\Scripts\python.exe scripts/run_api.py --host 127.0.0.1 --port 8000
```

In a separate terminal, start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

The backend health endpoint is `GET /health`; Vite proxies `/api` and `/health` to the
backend. The version entry points are `scripts/run_v0.py`, `scripts/run_v1.py`,
`scripts/run_v2.py` and `scripts/run_v3.py`. V2/V3 retrieval requires an existing compatible
PostgreSQL/pgvector database and its configured local environment. See the
[development guide](docs/development_guide.md) for version-specific commands and dependencies.

## TripWorld database release

The project owner's [TripWorld database release folder](https://drive.google.com/drive/folders/14VjxQU7jR8PGuiMWes5uaPLIOdrMNaQ0?usp=sharing)
contains the processed entities, retrieval text and saved vectors. Download the complete
release while preserving its directory structure, then verify the files against
`SHA256SUMS.txt`. The release `README.md` gives the import steps and validation results.

Restore `tripworld.pgcustom` into an empty PostgreSQL database with pgvector available.
The tested versions are PostgreSQL 17.10 and pgvector 0.8.2. For the current retrieval
runtime, copy the two packaged sidecars into these repository paths:

```text
data/tripworld/artifacts/retrieval_entities.parquet.manifest.json
data/tripworld/reports/phase5_embedding_run.json
```

Importing the release avoids downloading the TripWorld source data and regenerating the
stored embeddings. Online planning still needs the configured model and travel providers.
Keep the database dump outside Git.

## Documentation and evidence

[docs/README.md](docs/README.md) indexes current design and dated development records.
The [planning input UX specification](.scratch/planning-input-ux/spec.md) owns the assistance
contract and limits. Local `logs/` and `artifacts/` contain development evidence, including
potential provider/model data, and are not part of a source commit. This project has not run
a formal V0–V3 benchmark or reached a new version freeze through the recent input UX work.
