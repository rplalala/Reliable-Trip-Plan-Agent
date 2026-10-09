# Development guide

Current entry points, reconciled 2026-10-03. [PROJECT.md](../../PROJECT.md) owns status
and authorization; [architecture](../0001-system-architecture.md) and
[application contracts](../0007-application-operations.md) explain the code and APIs.
Commands below are references, not evidence of execution or approval for a live run.

<a id="b-4cf18c540a96-0"></a>
<a id="b-4cf18c540a96-1"></a>
<a id="b-4cf18c540a96-2"></a>
<a id="setup"></a>

<a id="current-local-api-and-input-assistance-2026-09-26"></a>
<a id="setup-and-ordinary-development"></a>

## Environment and local application

Use Python 3.12 and the existing uv environment. From the repository root:

```powershell
uv sync
uv sync --group retrieval
npm --prefix frontend ci
.\.venv\Scripts\python.exe scripts/run_api.py --host 127.0.0.1 --port 8000
```

`uv sync` also installs this repository editable, exposing `rtpeval` in `.venv`.
From the repository root, `uv run rtpeval --help` discovers validation and evaluation.
`uv run rtpeval validate MANIFEST` emits native intake JSON.
`uv run rtpeval evaluate execute MANIFEST --directory FRESH --options OPTIONS --prices PRICES`
prepares and executes the automatic
report; provider calls require their own execution authorization. Preparation and saved
evidence replay stay offline. See
[installed automatic evaluation](../../backend/evaluation/README.md#installed-automatic-evaluation)
for credentials, reviewed contexts, native budgets, one-use directories and the retained
prepared-directory/exact-digest route.
See [installed batch validation](../../backend/evaluation/README.md#installed-batch-validation)
for material requirements, exit meanings and the retained legacy commands.

Start the frontend in another terminal with `npm --prefix frontend run dev`.
Vite proxies `/api` and `/health` to `http://127.0.0.1:8000`.
The [API launcher](../../scripts/run_api.py) selects the Windows event loop needed by
async PostgreSQL access. Use it for local Windows API development. `GET /health`
checks the application process; it does not certify provider or corpus readiness.
Product routes are `/` and `/plan`; Developer is `/dev`.
Product runs V3 and Developer exposes independent V0-V3 from the shared structured form.

Populate local `.env` from [the non-secret example](../../.env.example).
Foundry endpoint/deployment/key and `GOOGLE_MAPS_API_KEY` serve planning;
`.env.tripworld` or process environment supplies `OPENAI_API_KEY` and
`TRIPWORLD_DB_HOST/PORT/NAME/USER/PASSWORD` for retrieval. Model and deployment names
are distinct settings. Never commit real credentials. Default local DB host/port are
127.0.0.1:55432. See [configuration](../../config/README.md) for exact current keys.

V2/V3 require the compatible TripWorld database and artifact/embedding sidecars.
The pinned vocabulary under `.cache/tokenizer` must also exist; the planner does not
download it. `python -m tools.data.prepare_tokenizer --help` describes explicit preparation.

<a id="b-61a2c7801de0-0"></a>
<a id="b-61a2c7801de0-2"></a>
<a id="b-61a2c7801de0-3"></a>
<a id="b-61a2c7801de0-4"></a>
<a id="b-61a2c7801de0-5"></a>
<a id="b-61a2c7801de0-6"></a>
<a id="b-61a2c7801de0-7"></a>
<a id="versions"></a>

<a id="reproducible-development-entry-points"></a>
<a id="weatherdate-execution-boundary-2026-09-22"></a>

## Independent version execution

Save one complete `planning_request_2` object as a local `request.json`, not a batch
manifest. [PlanningRequest](../../backend/app/schemas/request.py) owns the schema:
destination, start/end ISO dates, traveler count, mandatory total budget/currency and
optional additional preferences. Example shape (replace dates before a live run):

```json
{
  "input_version": "planning_request_2",
  "destination": "Tokyo, Japan",
  "start_date": "2026-10-05",
  "end_date": "2026-10-07",
  "traveler_count": 3,
  "budget": {"amount": "180000", "currency": "JPY"},
  "additional_preferences": "I definitely want to visit Meiji Jingu. I prefer small museums and local architecture."
}
```

The shared date policy admits today through today+13, inclusive duration at most ten
days, using Australia/Sydney reference time. Check `GET /api/planning/date-window`
for a fresh request. An offline fixture can pin `--reference-date`; a historical
override must not disguise stale dates in a live run.

```powershell
.\.venv\Scripts\python.exe scripts/run_v0.py --input-json request.json
.\.venv\Scripts\python.exe scripts/run_v1.py --input-json request.json --runtime-config config/runtime.yaml --development-timeout-seconds 600
.\.venv\Scripts\python.exe scripts/run_v2.py --input-json request.json --runtime-config config/runtime.yaml --development-timeout-seconds 600 --rag-env-file .env.tripworld
.\.venv\Scripts\python.exe scripts/run_v3.py --input-json request.json --runtime-config config/runtime.yaml --development-timeout-seconds 600 --rag-env-file .env.tripworld
```

V0 is tool-free and accepts neither runtime configuration nor development-timeout flags.
V1 adds normalized external evidence; V2 adds retrieval; V3 adds validation and targeted
repair. V3 requires an explicit positive development timeout no greater than 600 seconds.
These entry points can call paid services and require an approved live plan and budget.
The ordinary CLI does not recreate an acceptance capture, saved query vectors or a
missing observation. Opt-in library capture belongs to the caller.

Current tunable values come from [runtime.yaml](../../config/runtime.yaml) and its typed
loaders. For example, the main-generation input ceiling is 252000 tokens; old acceptance
budgets/hashes describe their own revisions. Use the configuration reference rather
than copying checkpoint hashes into a new run.

<a id="b-9276e33ca3cc-0"></a>
<a id="b-9276e33ca3cc-1"></a>
<a id="data"></a>

<a id="what-git-does-and-does-not-save"></a>
<a id="shared-runtime-contracts-and-offline-implementations"></a>
<a id="checkpoint-reconstruction-boundary"></a>
<a id="first-generation-checkpoint-configuration"></a>

## Retrieval restore and reproducibility

Use the [TripWorld release/restore instructions](../../README.md#tripworld-database-release)
to restore the saved database without repeating ingestion or embedding. The database,
compatible vectors, `retrieval_entities.parquet.manifest.json` and
`phase5_embedding_run.json` have different roles and must remain compatible.
Git contains source and static contracts, not the generated corpus or Docker volume.
Release availability does not make provider calls offline or recreate original live evidence.

The [retrieval design](../0004-retrieval-persistence%28v2v3%29.md) owns compatibility and
query behavior. [V2 development records](../records/v0-v3/v2-development.md) preserve
historical builds, failures and validation. Deleted source/config recovery snapshots are
unavailable; historical paths are not recovery instructions. The old broad `validate`
operation uses historical query artifacts and maintenance ANALYZE, so it is not a default
read-only clean-clone check. Do not rebuild vectors or destroy a volume to follow this guide.

<a id="b-5aacb36d6308-0"></a>
<a id="tools"></a>

<a id="script-inventory"></a>
<a id="current-tool-boundaries-after-repository-cleanup"></a>

## Code and tool navigation

| Entry | Responsibility |
| --- | --- |
| [Version runners](../0001-system-architecture.md#concrete-code-map) | Independent execution and shared graph seams |
| [API boundary](../0007-application-operations.md#http-contract-map) | Product/Developer request, result and stream contracts |
| [Evaluation package](../../backend/evaluation/README.md) | Offline intake, independent review, scoring and human package commands |
| [Evaluation development tools](../../backend/evaluation/tools/route_requests_cli.py) | V0 smoke request/budget preparation; not Product runtime or final quality scoring |
| [Data tools](../../tools/data/tripworld_database.py) | Explicit ingestion, embedding, integrity and query operations |
| [Source preparation](../../tools/data/prepare_tripworld.py) | Source projection/profiling and corpus preparation |
| [Retrieval tools](../../tools/data/tripworld_retrieval.py) | Entity construction and exact retrieval reference tools |
| [Runtime acceptance](../../tools/validation/runtime_acceptance.py) | Owned-resource/capture library, not an autonomous live launcher |
| [Short-reference smoke](../../tools/validation/short_reference_packet.py) | Freeze and preflight six development adapter cases; separately authorized one-shot execution |
| [Requirement acceptance](../../tools/validation/requirement_acceptance.py) | Explicit frozen matrices and execution |
| [Retrieval validation](../../tools/validation/retrieval_validation.py) | Explicit database validation |
| [Retrieval timing](../../tools/diagnostics/retrieval_performance.py) | Bounded SQL timing/plans |
| [Payload sizing](../../tools/diagnostics/itinerary_payload.py) | Offline synthetic serializer checks |
| [Candidate diagnostics](../../tools/diagnostics/candidate_supply.py) | Offline supplied-capture analysis |

Use module invocation, for example `python -m tools.data.tripworld_database --help`.
Runtime application code does not import `tools` or tests. Runtime identity/vector
compatibility lives in `backend/app/tripworld`; persistence/build/schema tooling lives
under `tools/data/tripworld`. Requirement fingerprints have one runtime definition in
[fingerprints.py](../../backend/app/runtime/fingerprints.py); development captures use
the optional port from [requirement_capture.py](../../tools/validation/requirement_capture.py).

Evaluation's development-only V0 route tool uses
`python -m backend.evaluation.tools.route_requests_cli`. This is separate from the
repository-level `tools/validation` helpers. Ordinary evaluator CLIs remain in
`backend.evaluation`; they are command entries into actual evaluator functionality.
Neither location makes smoke a required product execution step.

<a id="preference-smoke-provider-diagnostics"></a>

## Verification and evidence

For implementation changes, choose checks for affected seams. Standard commands:

```powershell
uv run pytest
uv run ruff check .
npm --prefix frontend run test
npm --prefix frontend run lint
npm --prefix frontend run build
npm --prefix frontend run build:blind-review
```

Shared schema/core changes need broader regression; milestones need the full relevant
suite. Prefer mocks/fixtures for provider ports. Tests, a milestone and a user-approved
freeze are separate gates. Actual failure/correction/retest evidence belongs in existing
[version records](../records/README.md) and Issues, with its revision and scope.
Preference-provider diagnostics describe observed responses only, never reconstructed
explanations of older failures or additional billable usage. Nothing here authorizes a
formal benchmark, new live calls, a dataset rebuild or publication.
