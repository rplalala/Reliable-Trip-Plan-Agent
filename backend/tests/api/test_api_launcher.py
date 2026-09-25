"""Launcher loop selection without starting a listener or contacting providers."""

import asyncio
import sys

from scripts.run_api import create_api_loop


def test_api_loop_runs_coroutines_and_supports_windows_selector():
    async def inspect_loop():
        loop = asyncio.get_running_loop()
        if sys.platform == "win32":
            assert isinstance(loop, asyncio.SelectorEventLoop)
        return True

    assert asyncio.run(inspect_loop(), loop_factory=create_api_loop)
