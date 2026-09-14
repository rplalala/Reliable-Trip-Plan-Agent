"""Application-visible Web Search requests and observations."""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class WebModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class WebEvidenceSearchRequest(WebModel):
    task_id: str = Field(min_length=1)
    place_id: str = Field(min_length=1)
    place_name: str = Field(min_length=1)
    information_need: str = Field(min_length=1)
    requested_facets: tuple[str, ...] = ()
    requested_subject_scope: str = "whole_venue"
    requested_scope_text: str | None = None
    applicable_start_date: date
    applicable_end_date: date
    allowed_domains: tuple[str, ...] = Field(min_length=1)
    task_instruction: str = Field(min_length=1)
    template_version: str = Field(min_length=1)


class WebActionType(StrEnum):
    SEARCH = "search"
    OPEN_PAGE = "open_page"
    FIND_IN_PAGE = "find_in_page"
    OTHER = "other"


class WebActionObservation(WebModel):
    action_type: WebActionType
    status: str
    queries: tuple[str, ...] = ()
    target_url: str | None = None
    source_urls: tuple[str, ...] = ()


class WebSearchHit(WebModel):
    url: str
    source_domain: str
    title: str | None = None
    snippet: str | None = None
    action_index: int
    result_index: int
    allowed_domain: bool


class WebCitationObservation(WebModel):
    url: str
    title: str | None = None
    start_index: int | None = None
    end_index: int | None = None


class WebUsageObservation(WebModel):
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    reasoning_tokens: int | None = None


class WebSearchObservation(WebModel):
    response_id: str | None = None
    provider_status: str | None = None
    actions: tuple[WebActionObservation, ...] = ()
    hits: tuple[WebSearchHit, ...] = ()
    citations: tuple[WebCitationObservation, ...] = ()
    usage: WebUsageObservation | None = None
    latency_ms: int | None = None
    partial: bool = False
