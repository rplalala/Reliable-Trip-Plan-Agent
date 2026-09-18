# V0 As-Built Milestone

## Status

- Completion date: 2026-09-11
- Baseline commit: `34943c7` (`docs: document V0 setup and usage`)

## Research Definition and Scope

V0 is the plain-LLM research baseline. It uses the configured model's pretrained
knowledge in two structured LLM stages: requirement extraction followed by itinerary
generation.

```text
TravelRequest
-> Requirement Extraction
-> TravelRequirements
-> Itinerary Generation
-> Itinerary
-> PlanningResult(system_version="v0")
```

V0 provides an explicit, independently runnable baseline for later comparison with
V1, V2, and V3.

## Non-Scope

V0 does not include:

- External tools or web search
- Google Places, routes, weather, or other live information sources
- RAG
- Database persistence
- Memory or a LangGraph checkpointer
- Constraint validation
- Retry, regeneration, repair, or re-validation
- A V0-specific FastAPI planning endpoint
- Benchmark or formal experiment logic

## Final Graph Topology

The V0 LangGraph topology is fixed:

```text
START
-> extract_requirements
-> generate_itinerary
-> END
```

The minimal `V0State` contains `request`, `reference_date`, `requirements`, and
`itinerary`. A successful run makes exactly one LLM call in each node.

## Requirement Extraction

The `extract_requirements` node receives the original `TravelRequest` and a
`reference_date`. It:

- Extracts only requirements stated by the user or directly resolvable from the
  reference date
- Does not invent a destination, dates, traveler count, budget, activities,
  exclusions, or preferences
- Uses `null` for unknown scalar values
- Records missing or uncertain fields in `unresolved_fields`
- Normalizes explicitly stated currencies to ISO 4217 codes

If `destination`, `start_date`, or `end_date` is missing after extraction, V0 fails
before itinerary generation. An explicitly supplied reference date is used to resolve
relative dates; otherwise, the system's current local date is used.

## Itinerary Generation

The `generate_itinerary` node receives the original request, extracted
`TravelRequirements`, and reference date. It generates a structured itinerary using
only the model's pretrained general knowledge.

It does not claim that opening hours, availability, prices, routes, travel times,
weather, events, or disruptions were checked. For every activity start and end, the
Azure Foundry transport representation requires:

- `date`: exactly `YYYY-MM-DD`
- `time`: exactly `HH:MM:SS`
- `utc_offset`: exactly `+HH:MM` or `-HH:MM`

## Shared Domain Schemas

V0 uses the provider-independent shared domain schemas:

- `TravelRequest`
- `Money`
- `TravelRequirements`
- `Activity`
- `ItineraryDay`
- `Itinerary`
- `PlanningResult`
- `SystemVersion.V0`

Pydantic validation on these models is the final domain contract. The stable shared
`PlanningResult` contract contains only `system_version`, `requirements`, and
`itinerary`.

## Azure Foundry and StructuredLLMClient Architecture

LangGraph nodes depend only on the provider-independent `StructuredLLMClient`
protocol. They do not depend directly on Azure Foundry, LangChain's OpenAI client, or
provider-specific transport models.

```text
V0 node
-> StructuredLLMClient
-> AzureFoundryStructuredLLMClient
-> Provider-native JSON Schema structured output
-> Azure Foundry DTO
-> Deterministic mapper
-> Shared domain model
```

The Azure Foundry adapter uses `ChatOpenAI` with the OpenAI-compatible `/openai/v1`
endpoint, the Responses API, provider-native JSON Schema structured output with
`strict=True`, and `max_retries=0`.

`LLM_MODEL` records the underlying model used by the system.
`AZURE_OPENAI_DEPLOYMENT` identifies the Azure Foundry deployment passed in the API
request's `model` field. The implementation does not assume that these values are
always identical.

## Azure Foundry DTOs and Deterministic Mapping

Both structured-output stages use provider-specific transport DTOs:

- `FoundryMoneyDTO`
- `FoundryTravelRequirementsDTO`
- `FoundryDateTimeDTO`
- `FoundryActivityDTO`
- `FoundryItineraryDayDTO`
- `FoundryItineraryDTO`

The DTOs use strict validation and forbid additional fields. The mapping layer:

- Strictly validates ISO dates, times, and UTC offsets
- Constructs timezone-aware domain datetimes from complete transport components
- Converts transport DTOs into the existing shared domain models

It does not guess, fill, normalize, repair, or semantically correct values. Missing,
invalid, or ambiguous values fail immediately.

## Programmatic Runner and CLI

The programmatic entry point is:

```python
await run_v0(request, llm_client, reference_date=...)
```

The independent command-line entry point is:

```shell
uv run python scripts/run_v0.py \
  --request "Plan a 1-day trip to Kyoto on 2026-10-01 for one traveler." \
  --reference-date 2026-09-11
```

On success, the CLI writes a `PlanningResult` JSON object. It uses ASCII-safe JSON
escaping so Unicode output is safe on Windows GBK/cp936 consoles while preserving the
original Unicode values after JSON parsing.

## Error and Fail-Fast Behavior

- Missing critical requirements fail after the extraction call and produce CLI exit
  code `2`.
- Extraction provider or schema failures are reported for the
  `extract_requirements` stage.
- Itinerary provider, DTO, mapping, or domain failures are reported for the
  `generate_itinerary` stage.
- Stage and unexpected execution failures produce CLI exit code `1`.
- V0 performs no automatic retry, regeneration, normalization, or repair.
- The Azure Foundry provider client is configured with `max_retries=0`.

## Independent Execution

V0 is defined under `backend/app/versions/v0/` and remains independently runnable
through `scripts/run_v0.py`. Later versions must use their own explicit graphs and
entry points rather than dynamically modifying the V0 graph. Changes to shared code
must not silently change V0 research behavior.

## Testing Strategy and Milestone Status

The V0 test suite covers:

- The exact two-node graph topology and two intended LLM stages
- Missing-critical-requirement handling
- No-retry and no-repair behavior
- The shared `PlanningResult` contract and `SystemVersion.V0`
- Azure Foundry DTO schema compatibility and strict validation
- Deterministic DTO-to-domain mapping and preservation of domain validation
- Provider abstraction and deployment configuration
- Unit-test isolation from external network access
- CLI JSON output, exit codes, and cp936 Unicode round-trip behavior

At the V0 milestone freeze:

- `pytest`: 50 passed
- Ruff: passed
- `git diff --check`: passed

Subsequent repository-wide regression runs have continued to pass all V0 tests.

## Live Azure Foundry Smoke Tests

Development smoke testing confirmed successful Azure Foundry endpoint,
authentication, and deployment connectivity. Synthetic Kyoto, Sydney, and Paris
requests completed the full V0 path, including requirement extraction, DTO conversion,
domain validation, and `PlanningResult` generation.

The final Paris CLI smoke test exited with code `0`, produced valid JSON, and preserved
Unicode content through JSON serialization and parsing. These smoke tests verified the
implementation only; they were not benchmark runs.

## Known Limitations

- Travel facts come only from model pretraining and may be outdated or inaccurate.
- Opening hours, availability, prices, routes, travel times, weather, and disruptions
  are not verified.
- UTC offsets are supplied by the model and checked for format, not geographic or
  date-specific correctness.
- Itinerary feasibility and user constraints are not programmatically validated.
- Missing critical requirements are not resolved through an interactive clarification
  flow.
- Provider, DTO, mapping, or domain failures terminate the run without recovery.
- V0 has no persistence, memory, or repair mechanism.

## Frozen V0 Research Behavior

V0 freezes research behavior, not the literal contents of its files. The following
research behavior must remain stable for V0/V1 comparison:

- The two-node graph and requirement-extraction-to-itinerary-generation order
- Exactly two LLM calls in a successful run
- Plain-LLM generation without external information
- The prompts' semantic behavior and planning objective, rather than their exact text
- Fail-fast handling of missing critical requirements
- Reference-date behavior
- Strict DTO validation and deterministic DTO-to-domain mapping
- No retry, regeneration, constraint-validation loop, or repair
- The shared `PlanningResult` contract and `SystemVersion.V0`
- The independent `scripts/run_v0.py` execution path

Necessary backward-compatible shared infrastructure changes are allowed only when
they do not change V0 research behavior and all V0 regression tests continue to pass.

## Post-Milestone Shared Date-Policy Update

This section records a later approved Stage 0 shared-infrastructure change. The
ten-day date rule described here was not part of the original V0 milestone and must
not be interpreted as original milestone behavior.

The V0 planner architecture remains unchanged:

```text
START
-> extract_requirements
-> generate_itinerary
-> END
```

For requests that satisfy the shared date contract, V0 still makes exactly two LLM
calls and retains the same prompts, Microsoft Foundry model/provider behavior, final
itinerary schema, base planning objective, and plain-LLM generation semantics.

Stage 0 added the project-wide invariant:

```text
reference_date <= start_date <= end_date <= reference_date + 9 days

Final itinerary dates
subset of Requested trip dates
subset of [reference_date, reference_date + 9 days]
```

The final-date check covers the itinerary's top-level start and end dates, every
itinerary-day date, and every activity start/end calendar date. A violation fails
deterministically. V0 does not repair, regenerate, retry, or alter the invalid dates.

This invariant is a shared V0/V1/future V2/V3 input/output contract, not external
evidence, V1 functionality, or V3-style validation and repair.

The Product planning path now obtains one trusted backend host-local reference date
at run start. Product clients cannot submit `reference_date`. The independently
runnable V0 CLI, Developer API, and programmatic test interface retain explicit fixed
reference dates as trusted research/testing functionality. The fixed date is captured
once per run so a midnight boundary cannot change the allowed window mid-run.

Stage 0 regression results after this post-milestone update were:

- Backend test suite: 91 passed
- V0 version-specific tests: 16 passed
- Ruff: passed
- Frontend tests: 21 passed
- Frontend ESLint and production build: passed
- `git diff --check`: passed

This update changes only the accepted date contract for V0. It is not a redesign of
the V0 research baseline.
