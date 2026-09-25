"""Shared deterministic test doubles."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FixedDateProvider:
    """Return one fixed reference date for every test run."""

    value: date

    def today(self) -> date:
        return self.value


class V0TestRuntime:
    """Explicit offline adapter for tests of the unchanged V0 interpretation boundary."""

    def __init__(self, client, expected_version="v0"):
        self.client = client
        self.expected_version = expected_version

    async def run(self, version, request, *, reference_date, tracer=None):
        from backend.app.versions.v0.runner import run_v0

        # Product gate tests reuse the shared boundary without pretending to exercise V3 tools.
        assert version == self.expected_version
        return await run_v0(request, self.client, reference_date=reference_date)
