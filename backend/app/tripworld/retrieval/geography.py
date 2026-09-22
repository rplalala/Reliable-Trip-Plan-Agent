"""Destination-agnostic spherical filters, including poles and the antimeridian."""

import math

from pydantic import BaseModel, ConfigDict, Field

EARTH_RADIUS_KM = 6371.0088


class GeographicScope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    radius_km: float = Field(gt=0, le=math.pi * EARTH_RADIUS_KM)
    country: str | None = None


def valid_coordinates(latitude: object, longitude: object) -> bool:
    return (
        isinstance(latitude, (int, float))
        and isinstance(longitude, (int, float))
        and math.isfinite(latitude)
        and math.isfinite(longitude)
        and -90 <= latitude <= 90
        and -180 <= longitude <= 180
        and (latitude != 0 or longitude != 0)
    )


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * (
        math.sin(math.radians(lon2 - lon1) / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(min(1.0, max(0.0, a))))


def bounding_box(scope: GeographicScope) -> tuple[float, float, float]:
    """Return latitude limits and wrapped longitude half-width in degrees."""
    angle = scope.radius_km / EARTH_RADIUS_KM
    lat = math.radians(scope.latitude)
    lo, hi = max(-math.pi / 2, lat - angle), min(math.pi / 2, lat + angle)
    if lo <= -math.pi / 2 or hi >= math.pi / 2:
        width = 180.0
    else:
        width = math.degrees(math.asin(min(1.0, math.sin(angle) / math.cos(lat))))
    return math.degrees(lo), math.degrees(hi), width


def in_bounding_box(latitude: float, longitude: float, scope: GeographicScope) -> bool:
    lo, hi, width = bounding_box(scope)
    delta = abs((longitude - scope.longitude + 180) % 360 - 180)
    return lo - 1e-9 <= latitude <= hi + 1e-9 and delta <= width + 1e-9


def in_radius(latitude: float, longitude: float, scope: GeographicScope) -> bool:
    return in_bounding_box(latitude, longitude, scope) and (
        haversine_km(scope.latitude, scope.longitude, latitude, longitude) <= scope.radius_km + 1e-9
    )
