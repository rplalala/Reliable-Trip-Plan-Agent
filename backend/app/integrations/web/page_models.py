"""Bounded PageRetriever contracts; page text is not accepted evidence."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PageModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class PageFetchStatus(StrEnum):
    FETCHED = "fetched"
    BLOCKED = "blocked"
    INACCESSIBLE = "inaccessible"
    UNSUPPORTED = "unsupported"
    OVERSIZED = "oversized"
    TIMEOUT = "timeout"


class PageFetchRequest(PageModel):
    task_id: str
    observed_url: str
    observed_urls: tuple[str, ...] = Field(min_length=1)
    allowed_domains: tuple[str, ...] = Field(min_length=1)


class PageContentBlock(PageModel):
    """Primary-page body text with its source heading path, excluding link text."""

    text: str = Field(min_length=1)
    section_headings: tuple[str, ...] = ()


class PageFetchResult(PageModel):
    task_id: str
    observed_url: str
    status: PageFetchStatus
    final_url: str | None = None
    redirect_chain: tuple[str, ...] = ()
    authorized_domain: str | None = None
    text: str | None = None
    page_title: str | None = None
    content_blocks: tuple[PageContentBlock, ...] = ()
    body_sha256: str | None = None
    http_request_count: int = 0
    reason: str | None = None
