"""In-memory request-scoped cache used by V1 acquisition services."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar, cast

from backend.app.integrations.dispatch import ProviderNotSentError, send_observer

ValueT = TypeVar("ValueT")
_MISSING = object()


class RequestCache:
    """Deduplicate provider work inside one run without persistent storage."""

    def __init__(self) -> None:
        self.attempts: dict[tuple[object, ...], str] = {}
        self._values: dict[tuple[object, ...], object] = {}

    async def get_or_create(
        self,
        key: tuple[object, ...],
        factory: Callable[[], Awaitable[ValueT]],
    ) -> tuple[ValueT, bool]:
        """Return a cached value or create it once; report whether it was a hit."""

        cached = self._values.get(key, _MISSING)
        if cached is not _MISSING:
            return cast(ValueT, cached), True

        value = await factory()
        self._values[key] = value
        return value, False

    def __len__(self) -> int:
        return len(self._values)

    def lookup(self, key: tuple[object, ...]) -> tuple[object | None, bool]:
        """Inspect request-local state without reserving or creating work."""
        value = self._values.get(key, _MISSING)
        return (None, False) if value is _MISSING else (value, True)

    def terminal_attempt(self, key):
        return self.attempts.get(key, "not_attempted").startswith("sent_")

    async def dispatch(self, key, factory, *, on_send=None, observed=False):
        """Record a provider dispatch after preflight/reservation, never before it."""
        if self.terminal_attempt(key):
            raise RuntimeError("Request already dispatched; retries are disabled")
        self.attempts[key] = "reserved_not_sent"

        def sent():
            if self.terminal_attempt(key):
                raise RuntimeError("Hidden provider retry is not allowed")
            if on_send is not None:
                on_send()
            self.attempts[key] = "sent_incomplete"

        token = send_observer.set(sent if observed else None)
        try:
            if not observed:
                sent()
            result = await factory()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if not self.terminal_attempt(key):
                raise ProviderNotSentError(type(exc).__name__) from exc
            self.attempts[key] = "sent_failed"
            raise
        finally:
            send_observer.reset(token)
        if not self.terminal_attempt(key):
            raise ProviderNotSentError("Transport returned without sending")
        self.attempts[key] = "sent_succeeded"
        return result
