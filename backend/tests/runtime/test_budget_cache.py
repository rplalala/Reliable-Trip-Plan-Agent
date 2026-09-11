"""Tests for request-level budget and in-memory deduplication."""

import asyncio

import pytest

from backend.app.runtime.budget import (
    ToolBudget,
    ToolBudgetExceededError,
    ToolBudgetKey,
    ToolBudgetLimits,
)
from backend.app.runtime.cache import RequestCache


def test_tool_budget_rejects_work_before_exceeding_hard_limit() -> None:
    budget = ToolBudget(ToolBudgetLimits(max_place_search_calls=1))
    budget.consume(ToolBudgetKey.PLACE_SEARCH_CALLS)

    with pytest.raises(ToolBudgetExceededError):
        budget.consume(ToolBudgetKey.PLACE_SEARCH_CALLS)

    assert budget.summary()["place_search_calls"] == {"used": 1, "limit": 1}


def test_request_cache_deduplicates_success_and_unavailable_values() -> None:
    cache = RequestCache()
    calls = 0

    async def load():
        nonlocal calls
        calls += 1
        return {"availability": "unavailable"}

    async def scenario():
        first = await cache.get_or_create(("weather", "sydney"), load)
        second = await cache.get_or_create(("weather", "sydney"), load)
        return first, second

    (first, first_hit), (second, second_hit) = asyncio.run(scenario())

    assert first == second == {"availability": "unavailable"}
    assert first_hit is False
    assert second_hit is True
    assert calls == 1
