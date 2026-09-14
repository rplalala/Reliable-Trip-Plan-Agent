"""Strict, immutable schema for the one project-wide runtime YAML file."""

from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    field_validator,
    model_validator,
)

from backend.app.observability.run_trace import TracePayloadMode
from backend.app.runtime.budget_limits import (
    ToolBudgetKey,
    validate_baseline_per_request_elements,
    validate_budget_values,
)


class _ConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class AppConfig(_ConfigModel):
    time_zone: str

    @field_validator("time_zone")
    @classmethod
    def valid_time_zone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Unknown IANA time zone: {value}") from exc
        return value


class PlacesBudgetConfig(_ConfigModel):
    destination_search_calls: StrictInt
    candidate_search_calls: StrictInt
    detail_calls: StrictInt
    review_detail_calls: StrictInt


class WeatherBudgetConfig(_ConfigModel):
    calls: StrictInt


class RoutesBudgetConfig(_ConfigModel):
    # Legacy single-matrix limit remains in use by the current V1 graph.
    matrix_elements: StrictInt
    baseline_elements_per_request: StrictInt
    baseline_elements_per_run: StrictInt
    baseline_calls: StrictInt
    alternative_pairs: StrictInt
    alternative_matrix_calls: StrictInt


class WebBudgetConfig(_ConfigModel):
    evidence_tasks: StrictInt
    page_fetches: StrictInt


class AuthorityDomainOverride(_ConfigModel):
    place_id: str = Field(min_length=1)
    information_needs: list[str] = Field(min_length=1)
    domains: list[str] = Field(min_length=1)

    @field_validator("information_needs")
    @classmethod
    def supported_information_needs(cls, values: list[str]) -> list[str]:
        allowed = {
            "current_operational_status",
            "date_specific_operational_exception",
            "special_date_hours",
            "admission_ticket",
            "reservation_requirement",
        }
        if any(value not in allowed for value in values) or len(set(values)) != len(values):
            raise ValueError("Unknown or duplicate official information need")
        return values

    @field_validator("domains")
    @classmethod
    def valid_domains(cls, values: list[str]) -> list[str]:
        from backend.app.policies.official_web import canonicalize_allowed_domains

        if len(canonicalize_allowed_domains(values)) != len(values):
            raise ValueError("Duplicate authorized domain")
        return values


class PageRetrievalConfig(_ConfigModel):
    max_targets_per_need: Literal[2]
    max_redirects: Literal[2]
    timeout_seconds: Literal[10]
    max_response_bytes: Literal[262144]
    max_text_chars: StrictInt = Field(ge=1, le=20000)


class ClaimExtractionConfig(_ConfigModel):
    max_native_sources: StrictInt = Field(ge=1, le=3)
    max_native_snippet_chars: StrictInt = Field(ge=1, le=1200)
    max_candidates_per_call: StrictInt = Field(ge=1, le=3)
    max_calls_per_need: Literal[3]
    max_extraction_output_units: StrictInt = Field(ge=1, le=1200)


class WebEvidenceConfig(_ConfigModel):
    reasoning_effort: Literal["low", "medium"]
    max_tool_calls: StrictInt = Field(ge=1, le=3)
    search_context_size: Literal["low", "medium", "high"]
    timeout_seconds: StrictInt = Field(ge=1, le=60)
    authority_domain_overrides: list[AuthorityDomainOverride]
    page_retrieval: PageRetrievalConfig
    claim_extraction: ClaimExtractionConfig


class ExperienceBudgetConfig(_ConfigModel):
    review_enriched_places: StrictInt
    profile_llm_calls: StrictInt


class BudgetConfig(_ConfigModel):
    candidates: StrictInt
    final_pois: StrictInt
    places: PlacesBudgetConfig
    weather: WeatherBudgetConfig
    routes: RoutesBudgetConfig
    web: WebBudgetConfig
    experience: ExperienceBudgetConfig

    def as_key_limits(self) -> dict[ToolBudgetKey, int]:
        return {
            ToolBudgetKey.CANDIDATES: self.candidates,
            ToolBudgetKey.DESTINATION_SEARCH_CALLS: self.places.destination_search_calls,
            ToolBudgetKey.CANDIDATE_SEARCH_CALLS: self.places.candidate_search_calls,
            ToolBudgetKey.PLACE_DETAIL_CALLS: self.places.detail_calls,
            ToolBudgetKey.REVIEW_DETAIL_CALLS: self.places.review_detail_calls,
            ToolBudgetKey.REVIEW_ENRICHED_PLACES: self.experience.review_enriched_places,
            ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS: self.experience.profile_llm_calls,
            ToolBudgetKey.FINAL_POIS: self.final_pois,
            ToolBudgetKey.WEB_EVIDENCE_TASKS: self.web.evidence_tasks,
            ToolBudgetKey.PAGE_FETCHES: self.web.page_fetches,
            ToolBudgetKey.ROUTE_MATRIX_ELEMENTS: self.routes.matrix_elements,
            ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS: self.routes.baseline_elements_per_run,
            ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS: self.routes.baseline_calls,
            ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS: self.routes.alternative_pairs,
            ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS: self.routes.alternative_matrix_calls,
            ToolBudgetKey.WEATHER_CALLS: self.weather.calls,
        }

    @model_validator(mode="after")
    def within_hard_limits(self) -> "BudgetConfig":
        validate_budget_values(self.as_key_limits())
        validate_baseline_per_request_elements(self.routes.baseline_elements_per_request)
        if self.routes.baseline_elements_per_request > self.routes.baseline_elements_per_run:
            raise ValueError(
                "baseline_elements_per_request cannot exceed baseline_elements_per_run"
            )
        if self.places.review_detail_calls < self.experience.review_enriched_places:
            raise ValueError("review_detail_calls must cover review_enriched_places")
        if self.experience.profile_llm_calls < self.experience.review_enriched_places:
            raise ValueError("profile_llm_calls must cover review_enriched_places")
        return self


class LoggingConfig(_ConfigModel):
    level: str
    console: StrictBool

    @field_validator("level")
    @classmethod
    def valid_level(cls, value: str) -> str:
        if value not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("logging.level must be a standard uppercase logging level")
        return value


class TraceConfig(_ConfigModel):
    enabled: StrictBool
    directory: Path
    payload_level: TracePayloadMode
    capture_llm: StrictBool
    capture_tools: StrictBool
    capture_evidence: StrictBool
    raw_provider_payloads: StrictBool
    max_payload_bytes: StrictInt

    @field_validator("max_payload_bytes")
    @classmethod
    def positive_payload_limit(cls, value: int) -> int:
        if value < 1:
            raise ValueError("trace.max_payload_bytes must be positive")
        return value


class RuntimeConfig(_ConfigModel):
    schema_version: Literal[5]
    app: AppConfig
    budget: BudgetConfig
    web_evidence: WebEvidenceConfig
    logging: LoggingConfig
    trace: TraceConfig

    @field_validator("schema_version")
    @classmethod
    def supported_schema(cls, value: int) -> int:
        if value != 5:
            raise ValueError("Unsupported runtime configuration schema version")
        return value
