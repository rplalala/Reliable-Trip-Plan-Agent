"""Shared environment-backed runtime settings."""

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_APP_TIME_ZONE = "Australia/Sydney"


class RuntimeSettings(BaseSettings):
    """Configuration shared by every independently runnable planner version."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_time_zone: str = Field(
        default=DEFAULT_APP_TIME_ZONE,
        min_length=1,
        validation_alias="APP_TIME_ZONE",
    )

    @field_validator("app_time_zone")
    @classmethod
    def validate_time_zone(cls, value: str) -> str:
        """Reject an unknown IANA time-zone identifier at configuration load time."""

        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Unknown IANA time zone: {value}") from exc
        return value
