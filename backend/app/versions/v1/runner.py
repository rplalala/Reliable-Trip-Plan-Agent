"""Public runner and command-line behavior for V1."""

import argparse
import asyncio
import json
import sys
from collections.abc import Sequence
from datetime import UTC, date, datetime
from uuid import uuid4

from backend.app.integrations.azure_foundry.evidence_reasoner import AzureFoundryEvidenceReasoner
from backend.app.integrations.azure_foundry.web_search import AzureFoundryWebEvidenceProvider
from backend.app.integrations.google import (
    GooglePlacesProvider,
    GoogleRoutesProvider,
    GoogleWeatherProvider,
)
from backend.app.integrations.http import HttpxJSONTransport
from backend.app.integrations.protocols import PlacesProvider, RoutesProvider, WeatherProvider
from backend.app.integrations.web.extraction_protocols import OfficialEvidenceReasoner
from backend.app.integrations.web.http_page_retriever import SafeHTMLPageRetriever
from backend.app.integrations.web.protocols import PageRetriever, WebEvidenceProvider
from backend.app.llm.client import StructuredLLMClient
from backend.app.observability.run_trace import (
    NullRunTracer,
    RunTraceContext,
    RunTracer,
    create_run_tracer,
)
from backend.app.policies.trip_dates import (
    DateProvider,
    SystemDateProvider,
    TripDatePolicyError,
    create_trip_date_window,
)
from backend.app.runtime.budget import ToolBudget, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.runtime.config_loader import (
    load_runtime_config,
    resolve_trace_directory,
    runtime_config_snapshot,
)
from backend.app.runtime.config_models import WebEvidenceConfig
from backend.app.runtime.logging_config import configure_logging
from backend.app.runtime.settings import RuntimeSettings
from backend.app.schemas.planning import PlanningResult, SystemVersion
from backend.app.schemas.request import TravelRequest
from backend.app.services.evidence_acquisition import (
    NoViableCandidatesError,
    V1EvidenceAcquisitionService,
)
from backend.app.services.official_web_grounding import OfficialWebGroundingService
from backend.app.services.official_web_integration import OfficialWebIntegrationService
from backend.app.services.web_evidence_acquisition import WebEvidenceAcquisitionService
from backend.app.versions.v0.graph import MissingRequiredFieldsError
from backend.app.versions.v0.runner import create_foundry_client, parse_reference_date
from backend.app.versions.v1.config import V1Settings
from backend.app.versions.v1.graph import V1StageError, build_v1_graph


async def run_v1(
    request: TravelRequest,
    llm_client: StructuredLLMClient,
    places_provider: PlacesProvider,
    weather_provider: WeatherProvider,
    routes_provider: RoutesProvider,
    *,
    reference_date: date | None = None,
    date_provider: DateProvider | None = None,
    budget_limits: ToolBudgetLimits | None = None,
    tracer: RunTracer | None = None,
    llm_config_identity: str | None = None,
    web_provider: WebEvidenceProvider | None = None,
    page_retriever: PageRetriever | None = None,
    official_reasoner: OfficialEvidenceReasoner | None = None,
    web_evidence_config: WebEvidenceConfig | None = None,
) -> PlanningResult:
    """Run V1 with one fixed date, shared budget, cache, tracer, and explicit graph."""

    if reference_date is not None and date_provider is not None:
        raise ValueError("reference_date and date_provider cannot both be supplied")

    effective_reference_date = reference_date or (date_provider or SystemDateProvider()).today()
    date_window = create_trip_date_window(effective_reference_date)
    effective_tracer = tracer or NullRunTracer(uuid4())
    budget = ToolBudget(budget_limits)
    cache = RequestCache()
    evidence_service = V1EvidenceAcquisitionService(
        places_provider=places_provider,
        weather_provider=weather_provider,
        routes_provider=routes_provider,
        budget=budget,
        cache=cache,
        tracer=effective_tracer,
    )
    web_dependencies = (web_provider, page_retriever, official_reasoner)
    if any(item is not None for item in web_dependencies) and not all(
        item is not None for item in web_dependencies
    ):
        raise ValueError(
            "Official-Web provider, page retriever, and reasoner must be supplied together"
        )
    official_web_service = None
    if web_provider is not None and page_retriever is not None and official_reasoner is not None:
        web_config = web_evidence_config or load_runtime_config().web_evidence
        official_web_service = OfficialWebIntegrationService(
            acquisition=WebEvidenceAcquisitionService(
                provider=web_provider,
                budget=budget,
                cache=cache,
                tracer=effective_tracer,
                config=web_config,
            ),
            grounding=OfficialWebGroundingService(
                page_retriever=page_retriever,
                reasoner=official_reasoner,
                budget=budget,
                tracer=effective_tracer,
                config=web_config,
            ),
            budget=budget,
            tracer=effective_tracer,
        )
    graph = build_v1_graph(
        llm_client,
        evidence_service,
        effective_tracer,
        llm_config_identity=(
            llm_config_identity or f"{type(llm_client).__module__}.{type(llm_client).__qualname__}"
        ),
        official_web_service=official_web_service,
    )
    effective_tracer.event(
        "run_started",
        {
            "run_id": effective_tracer.run_id,
            "system_version": SystemVersion.V1.value,
            "request": request,
            "runtime_reference_date": effective_reference_date,
            "allowed_date_window": {
                "start": date_window.allowed_start,
                "end": date_window.allowed_end,
            },
        },
    )
    try:
        final_state = await graph.ainvoke(
            {"request": request, "reference_date": effective_reference_date}
        )
        requirements = final_state.get("requirements")
        itinerary = final_state.get("itinerary")
        if requirements is None or itinerary is None:
            raise RuntimeError("V1 graph completed without a planning result")
        result = PlanningResult(
            system_version=SystemVersion.V1,
            requirements=requirements,
            itinerary=itinerary,
        )
    except Exception as exc:
        effective_tracer.event(
            "run_failed",
            {"error": type(exc).__name__},
        )
        effective_tracer.finish(
            status="failed",
            requirements=None,
            tool_usage=budget.summary(),
            outcome=None,
            error={"error": type(exc).__name__},
        )
        raise

    effective_tracer.event("run_completed")
    effective_tracer.finish(
        status="completed",
        requirements=result.requirements,
        tool_usage=budget.summary(),
        outcome=result,
    )
    return result


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the independent V1 command-line parser."""

    parser = argparse.ArgumentParser(description="Run the V1-A evidence-informed travel planner.")
    parser.add_argument("--request", required=True, help="Natural-language travel request.")
    parser.add_argument(
        "--reference-date",
        type=parse_reference_date,
        help="Trusted research reference date in YYYY-MM-DD format.",
    )
    return parser


def serialize_planning_result(result: PlanningResult) -> str:
    """Serialize CLI JSON using ASCII escapes for encoding-independent output."""

    return result.model_dump_json(indent=2, ensure_ascii=True)


def _create_google_providers(
    settings: V1Settings,
    tracer: RunTracer,
) -> tuple[PlacesProvider, WeatherProvider, RoutesProvider]:
    api_key = settings.google_maps_api_key.get_secret_value()
    transport = HttpxJSONTransport()
    return (
        GooglePlacesProvider(api_key=api_key, transport=transport, tracer=tracer),
        GoogleWeatherProvider(api_key=api_key, transport=transport, tracer=tracer),
        GoogleRoutesProvider(api_key=api_key, transport=transport, tracer=tracer),
    )


def _create_official_web_providers(
    settings: V1Settings,
    config: WebEvidenceConfig,
) -> tuple[WebEvidenceProvider, PageRetriever, OfficialEvidenceReasoner]:
    endpoint = str(settings.azure_openai_endpoint)
    deployment = settings.azure_openai_deployment
    api_key = settings.azure_openai_api_key.get_secret_value()
    return (
        AzureFoundryWebEvidenceProvider(
            endpoint=endpoint, deployment=deployment, api_key=api_key, config=config
        ),
        SafeHTMLPageRetriever(config.page_retrieval),
        AzureFoundryEvidenceReasoner(
            endpoint=endpoint, deployment=deployment, api_key=api_key, config=config
        ),
    )


def main(
    argv: Sequence[str] | None = None,
    *,
    llm_client: StructuredLLMClient | None = None,
    places_provider: PlacesProvider | None = None,
    weather_provider: WeatherProvider | None = None,
    routes_provider: RoutesProvider | None = None,
    tracer: RunTracer | None = None,
    budget_limits: ToolBudgetLimits | None = None,
    date_provider: DateProvider | None = None,
    web_provider: WebEvidenceProvider | None = None,
    page_retriever: PageRetriever | None = None,
    official_reasoner: OfficialEvidenceReasoner | None = None,
) -> int:
    """Execute the V1 CLI and return a process exit code."""

    args = build_argument_parser().parse_args(argv)
    all_clients_injected = all(
        item is not None
        for item in (llm_client, places_provider, weather_provider, routes_provider)
    )
    settings: V1Settings | None = None
    try:
        runtime_config = load_runtime_config()
        configure_logging(runtime_config.logging)
        if all_clients_injected:
            runtime_settings = RuntimeSettings()
        else:
            settings = V1Settings()
            runtime_settings = settings
        budget_limits = budget_limits or (
            settings.tool_budget_limits() if settings is not None else ToolBudgetLimits()
        )

        if args.reference_date is not None and date_provider is not None:
            raise ValueError("reference_date and date_provider cannot both be supplied")
        effective_reference_date = (
            args.reference_date
            or (date_provider or SystemDateProvider(runtime_settings.app_time_zone)).today()
        )
        run_id = uuid4()
        started_at = datetime.now(UTC)
        config_snapshot, config_hash = runtime_config_snapshot(
            runtime_config,
            effective_budget={
                **{key.value: value for key, value in budget_limits.as_key_limits().items()},
                "baseline_route_matrix_elements_per_request": (
                    budget_limits.max_baseline_route_matrix_elements_per_request
                ),
            },
        )
        context = RunTraceContext(
            run_id=run_id,
            system_version=SystemVersion.V1.value,
            reference_date=effective_reference_date,
            date_window=create_trip_date_window(effective_reference_date),
            request=TravelRequest(request_text=args.request),
            started_at=started_at,
            runtime_config=config_snapshot,
            runtime_config_sha256=config_hash,
        )
        if tracer is None:
            if settings is None:
                effective_tracer: RunTracer = NullRunTracer(run_id)
            else:
                effective_tracer = create_run_tracer(
                    context,
                    enabled=runtime_config.trace.enabled,
                    root=resolve_trace_directory(runtime_config.trace.directory),
                    payload_mode=runtime_config.trace.payload_level,
                    max_payload_bytes=runtime_config.trace.max_payload_bytes,
                    capture_llm=runtime_config.trace.capture_llm,
                    capture_tools=runtime_config.trace.capture_tools,
                    capture_evidence=runtime_config.trace.capture_evidence,
                    raw_provider_payloads=runtime_config.trace.raw_provider_payloads,
                )
        else:
            effective_tracer = tracer

        if settings is not None:
            default_places, default_weather, default_routes = _create_google_providers(
                settings, effective_tracer
            )
            llm_client = llm_client or create_foundry_client(settings)
            places_provider = places_provider or default_places
            weather_provider = weather_provider or default_weather
            routes_provider = routes_provider or default_routes
            default_web, default_pages, default_reasoner = _create_official_web_providers(
                settings, runtime_config.web_evidence
            )
            web_provider = web_provider or default_web
            page_retriever = page_retriever or default_pages
            official_reasoner = official_reasoner or default_reasoner

        if (
            llm_client is None
            or places_provider is None
            or weather_provider is None
            or routes_provider is None
        ):
            raise RuntimeError("V1 providers were not configured")

        result = asyncio.run(
            run_v1(
                TravelRequest(request_text=args.request),
                llm_client,
                places_provider,
                weather_provider,
                routes_provider,
                reference_date=effective_reference_date,
                budget_limits=budget_limits,
                tracer=effective_tracer,
                llm_config_identity=(
                    settings.azure_openai_deployment if settings is not None else None
                ),
                web_provider=web_provider,
                page_retriever=page_retriever,
                official_reasoner=official_reasoner,
                web_evidence_config=runtime_config.web_evidence,
            )
        )
    except MissingRequiredFieldsError as exc:
        error = {
            "error": "missing_required_fields",
            "unresolved_fields": list(exc.unresolved_fields),
        }
        print(json.dumps(error), file=sys.stderr)
        return 2
    except TripDatePolicyError as exc:
        print(json.dumps(exc.as_detail()), file=sys.stderr)
        return 2
    except NoViableCandidatesError as exc:
        print(
            json.dumps({"error": "no_viable_candidates", "message": str(exc)}),
            file=sys.stderr,
        )
        return 2
    except V1StageError as exc:
        cause = exc.__cause__
        error = {
            "error": "v1_stage_failed",
            "stage": exc.stage,
            "message": str(cause) if cause is not None else str(exc),
        }
        print(json.dumps(error), file=sys.stderr)
        return 1
    except Exception as exc:
        error = {"error": "v1_execution_failed", "message": str(exc)}
        print(json.dumps(error), file=sys.stderr)
        return 1

    print(serialize_planning_result(result))
    return 0
