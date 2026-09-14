"""Web acquisition abstraction used by V1 services."""

from typing import Protocol, runtime_checkable

from backend.app.integrations.web.models import WebEvidenceSearchRequest, WebSearchObservation
from backend.app.integrations.web.page_models import PageFetchRequest, PageFetchResult


@runtime_checkable
class WebEvidenceProvider(Protocol):
    @property
    def cache_identity(self) -> str:
        """Identify the provider deployment in semantic request-cache keys."""

        ...

    async def search(self, request: WebEvidenceSearchRequest) -> WebSearchObservation:
        """Run one application-bounded Web Evidence search task."""

        ...


@runtime_checkable
class PageRetriever(Protocol):
    async def fetch(self, request: PageFetchRequest) -> PageFetchResult:
        """Attempt one observed evidence URL under bounded access controls."""

        ...
