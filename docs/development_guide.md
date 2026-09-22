# Development guide

> Repository cleanup (2026-09-20): source/document/config recovery snapshots, including
> `D:/Workspace/Capstone/phase6_source_snapshots`, have been permanently deleted by user approval.
> Snapshot paths in dated entries describe historical actions, not available recovery locations.
> Retired selector implementations are no longer executable. Historical methods/results remain.

Static instructions, not authorization to run paid scenarios or mutate data.

## Reproducible development entry points

<a id="b-61a2c7801de0-0"></a>

Run from the repository root with the existing Python3.12 environment and retrieval dependency
group installed. These commands are documentation only; they were NOT executed in this closeout.
The V2 database, completed corpus and compatible saved vectors must already exist. No rebuild
is implied. The pinned offline tokenizer vocabulary in .cache/tokenizer must be available;
its preparation utility is explicit and is not run by the planner. Local .env supplies Foundry
endpoint/deployment/key and GOOGLE_MAPS_API_KEY; .env.tripworld (or process environment) supplies
OPENAI_API_KEY and TRIPWORLD_DB_HOST/PORT/NAME/USER/PASSWORD. Never commit either secret file.
The default DB host/port are127.0.0.1:55432; non-secret defaults appear in .env.example.

Save this complete input as request.json locally (not a manifest wrapper):

<a id="b-61a2c7801de0-2"></a>

```json
{
  "input_version": "planning_request_2",
  "destination": "Tokyo, Japan",
  "start_date": "2026-09-21",
  "end_date": "2026-09-23",
  "traveler_count": 3,
  "budget": {"amount": "180000", "currency": "JPY"},
  "additional_preferences": "I definitely want to visit Meiji Jingu. I prefer small museums and places with distinctive local architecture."
}
```

<a id="b-61a2c7801de0-3"></a>

```powershell
.\.venv\Scripts\python.exe scripts/run_v0.py --input-json request.json --reference-date 2026-09-20
.\.venv\Scripts\python.exe scripts/run_v1.py --input-json request.json --reference-date 2026-09-20 --runtime-config config/runtime.yaml --development-timeout-seconds 600
.\.venv\Scripts\python.exe scripts/run_v2.py --input-json request.json --reference-date 2026-09-20 --runtime-config config/runtime.yaml --development-timeout-seconds 600 --rag-env-file .env.tripworld
```

<a id="b-61a2c7801de0-4"></a>

These are frozen development dates, not permission to repeat the scenarios. For a later fresh
request, use the actual supported date window before dispatch; do not disguise stale dates
with a historical reference-date override. V0 does not accept the quality/runtime/development
flags and remains tool-free. Functions are backend.app.versions.v0.runner.run_v0,
backend.app.versions.v1.runner.run_v1 and backend.app.versions.v2.runner.run_v2.
All share planning_request_2 and final itinerary_2. V1/V2 model DTO is primary-only; Nearby is
post-itinerary. V0's one generation may return model-knowledge references without tools.

<a id="b-61a2c7801de0-5"></a>

quality_first_1 is loaded from the sole config/runtime.yaml by default. --runtime-config remains
an optional explicit file-selection facility, not a requirement to activate this policy.
The former quality YAML was consolidated without changing its values. The historical60/180 JSON
and its unused production loader were removed; historical tests construct those values explicitly.
The V2 runner still rejects a conflicting rag_config under quality_first_1. No --profile or
--rag-config CLI flag exists. This default-policy change has offline checks, not a new live run.
Selected values: input160000 incl.framing2048,output16384 incl.reasoning,SQL60s,RAG360s,
ordinary Details120s.600s is applied only by an explicit CLI/Python development timeout argument;
the config ceiling alone does not wrap every product request in600s.
Effective-config SHA-256 from acceptance manifest:
`aec5fb5d2b07dffb486b0d8211ae4b339bf6006af980a2cd1ede47f85746d722`.
Historical pre-coverage YAML file-byte SHA-256:
`416320cf286241cd1f00f84cc73e62ec388e03a7f41188456c0bb6fd652b84a0`.
These are different hash domains; CLI trace hashes may also include effective budget metadata.

<a id="b-61a2c7801de0-6"></a>

The standard CLI is a runnable entry point, not the complete acceptance-capture command.
Existing AcceptanceSession was used with the actual runners; run_matrix currently supports
shared/V0/V1 cases, not V2. V2 vector capture is opt-in through RuntimeRetrieval(capture_directory=...)
in the development caller. No CLI --capture-vectors or quality V2 matrix dispatcher exists.
Keep saved acceptance manifests/captures; a runner command does not reconstruct missing evidence.

<a id="b-61a2c7801de0-7"></a>

Product POST /api/planning still dispatches V0. Developer POST /api/dev/planning currently has
version Literal['v0'] and plan_v0 only. Neither API exposes V1/V2/config selection. Independent
V1/V2 CLI/Python execution works; product-facing version selection is an outstanding task.
Frontend already has structured destination/date/traveler/preference inputs and reference display,
but ProductPlanningInput.budget and the form still permit omitted budget, contrary to mandatory
backend total budget/currency. Clarification issues are also absent from its response type.
Its reference wording still says 'supplied place information', although Nearby can be outside
primary supply. This closeout documents these gaps without changing frontend or default engine.

## Setup and ordinary development

<a id="b-4cf18c540a96-0"></a>

Python 3.12 and uv are used. `uv sync` installs the ordinary project/development environment;
`uv sync --group retrieval` includes the optional retrieval dependencies. The local `.env` comes
from the non-secret `.env.example`; never put credentials in manifests or Git. The configured
Foundry model name and deployment identifier have separate meanings.

<a id="b-4cf18c540a96-1"></a>

For API development use `uv run uvicorn backend.app.main:app --reload`; health is `GET /health`.
The frontend uses `npm install` then `npm run dev` from `frontend/`, with Vite proxying `/api`
and `/health` to `http://127.0.0.1:8000`. Product routes are `/` and `/plan`; `/dev/planner`
still has a legacy free-text UI despite the structured backend developer request.

<a id="b-4cf18c540a96-2"></a>

Relevant tests are run for implementation changes, not repeatedly to save documentation.
The ordinary commands are `uv run pytest` and `uv run ruff check .`; frontend checks are
`npm run test`, `npm run lint`, `npm run build`. These are references, not checks executed
by this documentation consolidation.

## Script inventory

<a id="b-5aacb36d6308-0"></a>

Paths below are relative to the repository root. Historical selector tools are retired.

| Entry | Purpose | Execution boundary |
| --- | --- | --- |
| `scripts/run_v0.py`, `run_v1.py`, `run_v2.py` | Independent planners | Live requires explicit authorization |
| `tools/data/prepare_tripworld.py` | Source projection, profiling and corpus | Offline except explicit download |
| `tools/data/tripworld_database.py` | Ingestion, vector build, integrity, independent query | Subcommands may write DB or call embedding |
| `tools/data/tripworld_retrieval.py` | Entity construction and current exact retrieval reference tools | Explicit build/query work |
| `tools/data/prepare_tokenizer.py` | Pinned public vocabulary preparation | Explicit download only |
| `tools/validation/runtime_acceptance.py` | Owned resources and layered capture | Library, not an autonomous live launcher |
| `tools/validation/requirement_acceptance.py` | Frozen requirement matrices | Explicit freeze/execute |
| `tools/validation/retrieval_validation.py` | Database/retrieval validation | Explicit database work |
| `tools/diagnostics/retrieval_performance.py` | Bounded SQL timing/plans | Read-only DB queries require authorization |
| `tools/diagnostics/retrieval_service.py` | Standalone retrieval comparison adapter | Explicit query embedding and SQL |
| `tools/diagnostics/itinerary_payload.py` | Real serializer plus synthetic K12/K20 sizing | Offline |
| `tools/diagnostics/candidate_supply.py` | Saved-capture Details/gate and capacity analysis | Offline, explicit input paths |

`services/candidate_acquisition.py` owns current shared acquisition. The supply service delegates
to it; neither imports an evaluator or subset enumerator. Experiment-only implementations, fixtures
and tests were deleted; current identity, budget, provenance, Profile and cancellation assertions remain.

## What Git does and does not save

<a id="b-9276e33ca3cc-0"></a>

| Material | Current location | Preservation boundary |
| --- | --- | --- |
| Source, tests, configuration, scripts, documentation | Repository paths | Saved by the approved seven-commit repository checkpoint |
| Static dataset/model/category/query contracts | `data/tripworld/*.json` | Versioned reproducibility metadata |
| Raw/projected/entity data, vectors and generated manifests | Ignored `data/tripworld/` subdirectories | Independent local backup needed |
| SQL database | Docker volume `reliable-tripworld_tripworld_pgdata` | Requires separate backup; no backup health check performed here |
| Acceptance captures, manifests, actual vectors | `logs/quality_first_1_live_20260920/recovery/` | Ignored, may contain private provider/user data; preserve privately |
| Earlier failures and payload sizing | `logs/quality_first_1_live_20260920/` | Preserve failed and successful runs separately |
| Recovery source/doc/config snapshots | Deleted by user approval | No longer available; no replacement copies |
| Thesis/development archive | Ignored `thesis_notes/` | Separate archive, not current requirements or automatic Git backup |
| Real credentials | `.env`, `.env.tripworld`, process environment | Never commit or print |

<a id="b-9276e33ca3cc-1"></a>

The pinned PostgreSQL/pgvector setup is recorded in [Phase 5](v2_development.md).
Its creation/embedding commands describe historical setup, not mandatory steps before each run.
Do not destroy the volume or rebuild vectors to follow this guide.

## Current tool boundaries after repository cleanup

The planner entry points remain `python scripts/run_v0.py`, `python scripts/run_v1.py`,
and `python scripts/run_v2.py`. Current data tools are under `tools/data`, validation
harnesses under `tools/validation`, and diagnostics under `tools/diagnostics`.
Use module invocation from the repository root, for example:

```powershell
python -m tools.data.prepare_tripworld --help
python -m tools.data.tripworld_database --help
python -m tools.data.tripworld_retrieval --help
python -m tools.validation.requirement_acceptance --help
python -m tools.diagnostics.retrieval_performance --help
python -m tools.diagnostics.itinerary_payload --help
python -m tools.diagnostics.candidate_supply --help
```

Help does not authorize a live execution. AcceptanceSession is imported from
`tools.validation.runtime_acceptance`. Runtime code must not import tools or tests.
`logs` retains actual run/call evidence; offline results belong to ignored `artifacts`,
and the primary-generation tokenizer vocabulary belongs to `.cache/tokenizer`.
Console logging, metadata payload level, raw-provider-payload defaults, redaction and
usage semantics are unchanged. Inaccessible historical capture subtrees are retained.

### Shared runtime contracts and offline implementations

The main runtime/tool migration was followed by a narrow mixed-module split. Shared identity
helpers remain in `backend/app/tripworld/artifacts.py`; artifact persistence and build reuse
live in `tools/data/tripworld/artifact_persistence.py`. The immutable manifest stays in app,
while raw Parquet schema validation lives in `tools/data/tripworld/source_schema.py`.

Vector space identity and compatibility remain in `backend/app/tripworld/database/vectors.py`.
Offline batch configuration, batch result/provider contracts and the corpus production configuration
live in `tools/data/tripworld/embedding_config.py`. Runtime and offline tools use the same
`backend/app/tripworld/retrieval/embedding.py` vector validator.

The requirement digest has one definition in `backend/app/runtime/fingerprints.py`.
`DevelopmentRequirementCapture` lives in `tools/validation/requirement_capture.py`; the runtime
client accepts its existing optional capture interface without importing that implementation.
Runtime tracing, retrieval timing/error diagnostics and opt-in query-vector capture remain in app.
No retired-path forwarding modules are provided. Import-only relocation does not authorize live work.


## Checkpoint reconstruction boundary

The [TripWorld clean-environment audit](v2_tripworld_retrieval.md#clean-environment-reproducibility-audit-2026-09-20)
contains actual relocated commands, inputs/outputs, environment, expected counts and the distinction
between rebuilding a functional corpus and restoring identical vectors. In particular the old broad
`validate` command depends on local historical query artifacts and performs maintenance ANALYZE;
it is not the default clean-clone read-only verification step. Instructions do not authorize execution.

## First-generation checkpoint configuration

Current YAML byte SHA-256: `e2d749fedb3f68698c5de7f88f1b6f0fb750fbc9edb00bfbd8c3133567a7cb40`.
Current effective RuntimeConfig SHA-256: `862d694487bdd1313ec1fc62856abca2cb5d0d56c0beb75a6dc771be7630eb36`.
Earlier acceptance hashes above are historical. Current shared final supply ceiling20,
baseline Routes400 elements/seven calls, connection10 seconds. SQL60/RAG360/ordinary
Details120 and input160000/output16384 remain unchanged; outer600 stays an explicit
development invocation. Existing CLI flags and default engine are unchanged.

## Weather/date execution boundary (2026-09-22)

The current single runtime.yaml retains existing budgets and Australia/Sydney reference time zone.
The shared policy now admits today..today+13, with inclusive duration at most10. No CLI override
flag is required for this rule. V1/V2 instantiate OpenMeteoWeatherProvider through the shared tool
factory; Places/Routes still require the existing Google key, Weather does not. No second-provider
fallback exists. V0 has no Weather calls. API/form date limits come from /api/planning/date-window.
Existing CLI/AcceptanceSession use the same shared validation; use the true reference date for live.
A separately approved new test should freeze dates before calls; old dated captures are historical.
