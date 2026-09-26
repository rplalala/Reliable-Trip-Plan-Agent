"""Application-owned admission and call limits for destination assistance."""

from datetime import UTC, datetime
from threading import Lock
from time import monotonic

from backend.app.integrations.geodb.client import DestinationSuggestion, GeoDBClient
from backend.app.runtime.config_models import DestinationAssistanceConfig


class DestinationRateLimited(RuntimeError):
    """The local per-process request allowance was reached."""


class DestinationSuggestionService:
    def __init__(
        self,
        client: GeoDBClient,
        config: DestinationAssistanceConfig | None = None,
        *,
        now=monotonic,
        utc_now=lambda: datetime.now(UTC),
    ) -> None:
        self._client = client
        self._config = config or DestinationAssistanceConfig()
        self._now = now
        self._utc_now = utc_now
        self._lock = Lock()
        self._last_send = float("-inf")
        self._day = None
        self._count = 0

    def accepts(self, prefix: str) -> bool:
        return self._config.min_chars <= len(prefix) <= self._config.max_chars

    async def suggest(self, prefix: str) -> list[DestinationSuggestion]:
        with self._lock:
            day = self._utc_now().date()
            if day != self._day:
                self._day, self._count = day, 0
            current = self._now()
            if (
                self._count >= self._config.daily_attempts_per_process
                or current < self._last_send + self._config.minimum_interval_seconds
            ):
                raise DestinationRateLimited()
            self._count += 1
            self._last_send = current
        return await self._client.search(
            prefix,
            limit=self._config.result_limit,
            timeout_seconds=self._config.timeout_seconds,
        )
