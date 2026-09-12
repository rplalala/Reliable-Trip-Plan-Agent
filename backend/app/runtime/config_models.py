"""Strict, immutable schema for the one project-wide runtime YAML file."""

from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt, field_validator, model_validator

from backend.app.observability.run_trace import TracePayloadMode
from backend.app.runtime.budget_limits import ToolBudgetKey, validate_budget_values


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
    search_calls: StrictInt
    detail_calls: StrictInt


class WeatherBudgetConfig(_ConfigModel):
    calls: StrictInt


class RoutesBudgetConfig(_ConfigModel):
    matrix_elements: StrictInt
    alternative_pairs: StrictInt
    alternative_matrix_calls: StrictInt


class WebBudgetConfig(_ConfigModel):
    search_queries: StrictInt
    page_fetches: StrictInt


class ExperienceBudgetConfig(_ConfigModel):
    review_enriched_places: StrictInt


class BudgetConfig(_ConfigModel):
    candidates: StrictInt
    places: PlacesBudgetConfig
    weather: WeatherBudgetConfig
    routes: RoutesBudgetConfig
    web: WebBudgetConfig
    experience: ExperienceBudgetConfig

    def as_key_limits(self) -> dict[ToolBudgetKey, int]:
        return {
            ToolBudgetKey.CANDIDATES: self.candidates,
            ToolBudgetKey.PLACE_SEARCH_CALLS: self.places.search_calls,
            ToolBudgetKey.PLACE_DETAIL_CALLS: self.places.detail_calls,
            ToolBudgetKey.REVIEW_ENRICHED_PLACES: self.experience.review_enriched_places,
            ToolBudgetKey.WEB_SEARCH_QUERIES: self.web.search_queries,
            ToolBudgetKey.PAGE_FETCHES: self.web.page_fetches,
            ToolBudgetKey.ROUTE_MATRIX_ELEMENTS: self.routes.matrix_elements,
            ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS: self.routes.alternative_pairs,
            ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS: self.routes.alternative_matrix_calls,
            ToolBudgetKey.WEATHER_CALLS: self.weather.calls,
        }

    @model_validator(mode="after")
    def within_hard_limits(self) -> "BudgetConfig":
        validate_budget_values(self.as_key_limits())
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
    schema_version: StrictInt
    app: AppConfig
    budget: BudgetConfig
    logging: LoggingConfig
    trace: TraceConfig

    @field_validator("schema_version")
    @classmethod
    def supported_schema(cls, value: int) -> int:
        if value != 1:
            raise ValueError("Unsupported runtime configuration schema version")
        return value
