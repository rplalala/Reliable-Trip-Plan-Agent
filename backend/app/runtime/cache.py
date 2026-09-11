"""In-memory request-scoped cache used by V1 acquisition services."""

from collections.abc import Awaitable, Callable
from typing import TypeVar, cast

ValueT = TypeVar("ValueT")
_MISSING = object()


class RequestCache:
    """Deduplicate provider work inside one run without persistent storage."""

    def __init__(self) -> None:
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
