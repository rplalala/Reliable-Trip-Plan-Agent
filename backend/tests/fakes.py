"""Shared deterministic test doubles."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FixedDateProvider:
    """Return one fixed reference date for every test run."""

    value: date

    def today(self) -> date:
        return self.value
