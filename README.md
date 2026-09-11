# Reliable Trip Plan Agent

An LLM-based travel planning system focused on generating feasible and reliable itineraries.

The project will be developed as four independently runnable versions:

- V0: plain LLM planning
- V1: V0 plus external information and tools
- V2: V1 plus retrieval-augmented generation
- V3: V2 plus constraint validation, targeted repair, and re-validation

The repository is currently in Phase 0. It contains the backend foundation and shared data
contracts only. No planning version has been implemented yet.

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

## Setup

Install the project and development dependencies:

```shell
uv sync
```

Copy `.env.example` to `.env` when local environment values are needed. Phase 0 does not
require provider credentials.

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

## Current structure

```text
backend/
├── app/
│   ├── main.py
│   └── schemas/
└── tests/
```

Future version-specific code and entry points will be added only when each version is
implemented. Shared result schemas will remain limited to fields common to every version;
evidence, retrieval, validation, and repair data will use version-specific contracts.
