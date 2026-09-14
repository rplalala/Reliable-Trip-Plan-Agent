"""Small async JSON transport boundary for external HTTP adapters."""

from typing import Protocol, runtime_checkable

import httpx


class ProviderHTTPError(RuntimeError):
    """Provider request failed or returned a non-JSON response."""


@runtime_checkable
class AsyncJSONTransport(Protocol):
    async def request_json(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, object] | None = None,
        json_body: object | None = None,
    ) -> object:
        """Send one request and return its decoded JSON payload."""

        ...


class HttpxJSONTransport:
    """HTTPX implementation with provider retries intentionally disabled."""

    def __init__(self, *, timeout_seconds: float = 20.0) -> None:
        self._timeout_seconds = timeout_seconds

    async def request_json(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, object] | None = None,
        json_body: object | None = None,
    ) -> object:
        try:
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json_body,
                )
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderHTTPError(f"Provider HTTP request failed: {type(exc).__name__}") from exc
