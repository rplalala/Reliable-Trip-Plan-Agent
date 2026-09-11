"""Deterministic conversion from provider DTOs to planner evidence."""

from collections.abc import Mapping
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation

from backend.app.evidence.models import (
    EvidenceAvailability,
    OpeningHoursEvidence,
    PlaceCandidate,
    PlaceEvidence,
    RouteElementEvidence,
    RouteEvidence,
    WeatherDayEvidence,
    WeatherEvidence,
)
from backend.app.integrations.models import (
    PlaceCandidateDTO,
    PlaceDetailsDTO,
    RouteMatrixDTO,
    RouteMatrixRequest,
    WeatherForecastDTO,
    WeatherRequest,
)


def _parse_datetime(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


def _retrieved_at(value: str) -> datetime:
    return _parse_datetime(value) or datetime.now(UTC)


def normalize_place_candidate(
    dto: PlaceCandidateDTO,
    *,
    source_query: str,
    category: str,
) -> PlaceCandidate:
    """Attach deterministic query provenance to a minimal Places candidate."""

    return PlaceCandidate(
        place_id=dto.place_id,
        name=dto.display_name,
        formatted_address=dto.formatted_address,
        latitude=dto.location.latitude,
        longitude=dto.location.longitude,
        primary_type=dto.primary_type,
        business_status=dto.business_status,
        source_query=source_query,
        category=category,
        provider_rank=dto.provider_rank,
    )


def _opening_hours(details: PlaceDetailsDTO) -> OpeningHoursEvidence | None:
    source = details.current_opening_hours
    applicability = "provider_current_window"
    if source is None:
        source = details.regular_opening_hours
        applicability = "regular_weekly_pattern"
    if source is None:
        return None

    descriptions = source.get("weekdayDescriptions", [])
    return OpeningHoursEvidence(
        applicability=applicability,
        weekday_descriptions=(
            [item for item in descriptions if isinstance(item, str)]
            if isinstance(descriptions, list)
            else []
        ),
        open_now=source.get("openNow") if isinstance(source.get("openNow"), bool) else None,
        next_open_time=_parse_datetime(source.get("nextOpenTime")),
        next_close_time=_parse_datetime(source.get("nextCloseTime")),
    )


def _money_text(value: object) -> str | None:
    if not isinstance(value, Mapping):
        return None
    currency = value.get("currencyCode")
    units = value.get("units", 0)
    nanos = value.get("nanos", 0)
    if not isinstance(currency, str):
        return None
    try:
        amount = Decimal(str(units)) + (Decimal(str(nanos)) / Decimal("1000000000"))
    except InvalidOperation:
        return None
    return f"{currency} {amount:.2f}"


def _price_range_text(value: dict[str, object] | None) -> str | None:
    if value is None:
        return None
    low = _money_text(value.get("startPrice"))
    high = _money_text(value.get("endPrice"))
    if low is not None and high is not None:
        return f"{low} - {high}"
    return low or high


def normalize_place_details(
    details: PlaceDetailsDTO,
    *,
    candidate: PlaceCandidate,
) -> PlaceEvidence:
    """Keep only planning-relevant Place Details fields."""

    return PlaceEvidence(
        place_id=details.place_id,
        name=details.display_name,
        formatted_address=details.formatted_address or candidate.formatted_address,
        latitude=details.location.latitude,
        longitude=details.location.longitude,
        primary_type=details.primary_type or candidate.primary_type,
        business_status=details.business_status or candidate.business_status,
        timezone_id=details.time_zone,
        opening_hours=_opening_hours(details),
        rating=details.rating,
        user_rating_count=details.user_rating_count,
        price_level=details.price_level,
        price_range=_price_range_text(details.price_range),
        accessibility_options=details.accessibility_options,
        website_uri=details.website_uri,
        availability=EvidenceAvailability.AVAILABLE,
        retrieved_at=_retrieved_at(details.retrieved_at),
        source_ref=f"google_places:{details.place_id}",
    )


def unavailable_place_details(candidate: PlaceCandidate, reason: str) -> PlaceEvidence:
    """Preserve candidate facts when rich details fail."""

    return PlaceEvidence(
        place_id=candidate.place_id,
        name=candidate.name,
        formatted_address=candidate.formatted_address,
        latitude=candidate.latitude,
        longitude=candidate.longitude,
        primary_type=candidate.primary_type,
        business_status=candidate.business_status,
        availability=EvidenceAvailability.PARTIAL,
        unavailable_reason=reason,
        retrieved_at=datetime.now(UTC),
        source_ref=f"google_places:{candidate.place_id}",
    )


def _display_date(value: object) -> date | None:
    if not isinstance(value, Mapping):
        return None
    try:
        return date(int(value["year"]), int(value["month"]), int(value["day"]))
    except (KeyError, TypeError, ValueError):
        return None


def _nested_mapping(value: object, *keys: str) -> Mapping[str, object] | None:
    current = value
    for key in keys:
        if not isinstance(current, Mapping):
            return None
        current = current.get(key)
    return current if isinstance(current, Mapping) else None


def _number(value: object) -> float | None:
    if isinstance(value, int | float) and not isinstance(value, bool):
        return float(value)
    return None


def _temperature(day: Mapping[str, object], field: str) -> float | None:
    value = day.get(field)
    if not isinstance(value, Mapping):
        return None
    degrees = _number(value.get("degrees"))
    return degrees if degrees is not None else _number(value.get("value"))


def _condition(day: Mapping[str, object]) -> str | None:
    weather = _nested_mapping(day, "daytimeForecast", "weatherCondition")
    if weather is None:
        weather = _nested_mapping(day, "nighttimeForecast", "weatherCondition")
    if weather is None:
        return None
    condition_type = weather.get("type")
    if isinstance(condition_type, str):
        return condition_type
    description = weather.get("description")
    if isinstance(description, Mapping) and isinstance(description.get("text"), str):
        return str(description["text"])
    return None


def _precipitation(day: Mapping[str, object]) -> int | None:
    values: list[int] = []
    for period in ("daytimeForecast", "nighttimeForecast"):
        probability = _nested_mapping(day, period, "precipitation", "probability")
        if probability is not None and isinstance(probability.get("percent"), int):
            values.append(int(probability["percent"]))
    return max(values) if values else None


def _wind(day: Mapping[str, object]) -> float | None:
    values: list[float] = []
    for period in ("daytimeForecast", "nighttimeForecast"):
        speed = _nested_mapping(day, period, "wind", "speed")
        if speed is not None:
            value = _number(speed.get("value"))
            if value is not None:
                values.append(value)
    return max(values) if values else None


def normalize_weather(
    dto: WeatherForecastDTO,
    *,
    request: WeatherRequest,
    destination: str,
) -> WeatherEvidence:
    """Filter provider days strictly to the requested inclusive date range."""

    normalized_days: list[WeatherDayEvidence] = []
    for raw_day in dto.forecast_days:
        display_date = _display_date(raw_day.get("displayDate"))
        if display_date is None:
            continue
        if not request.requested_start <= display_date <= request.requested_end:
            continue
        normalized_days.append(
            WeatherDayEvidence(
                date=display_date,
                condition=_condition(raw_day),
                min_temperature_c=_temperature(raw_day, "minTemperature"),
                max_temperature_c=_temperature(raw_day, "maxTemperature"),
                precipitation_probability_percent=_precipitation(raw_day),
                max_wind_speed_kph=_wind(raw_day),
            )
        )
    normalized_days.sort(key=lambda item: item.date)
    expected_count = (request.requested_end - request.requested_start).days + 1
    if not normalized_days:
        availability = EvidenceAvailability.UNAVAILABLE
    elif len(normalized_days) < expected_count:
        availability = EvidenceAvailability.PARTIAL
    else:
        availability = EvidenceAvailability.AVAILABLE
    return WeatherEvidence(
        destination=destination,
        latitude=request.location.latitude,
        longitude=request.location.longitude,
        availability=availability,
        days=normalized_days,
        unavailable_reason=(
            "Provider returned no forecast days inside the requested trip range"
            if not normalized_days
            else None
        ),
        retrieved_at=_retrieved_at(dto.retrieved_at),
        source_ref="google_weather:daily_forecast",
    )


def unavailable_weather(request: WeatherRequest, destination: str, reason: str) -> WeatherEvidence:
    return WeatherEvidence(
        destination=destination,
        latitude=request.location.latitude,
        longitude=request.location.longitude,
        availability=EvidenceAvailability.UNAVAILABLE,
        unavailable_reason=reason,
        retrieved_at=datetime.now(UTC),
        source_ref="google_weather:daily_forecast",
    )


def _status_text(value: object) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        code = value.get("code")
        message = value.get("message")
        if code is None and message is None:
            return "OK"
        return ": ".join(str(item) for item in (code, message) if item is not None)
    return None


def _duration_seconds(value: object) -> int | None:
    if not isinstance(value, str) or not value.endswith("s"):
        return None
    try:
        return max(0, round(float(value[:-1])))
    except ValueError:
        return None


def normalize_routes(
    dto: RouteMatrixDTO,
    *,
    request: RouteMatrixRequest,
    mode_reason: str,
) -> RouteEvidence:
    """Map matrix indexes back to stable Place IDs and retain failures explicitly."""

    elements: list[RouteElementEvidence] = []
    for raw in dto.elements:
        origin_index = raw.get("originIndex")
        destination_index = raw.get("destinationIndex")
        if not isinstance(origin_index, int) or not isinstance(destination_index, int):
            continue
        if not 0 <= origin_index < len(request.origins):
            continue
        if not 0 <= destination_index < len(request.destinations):
            continue
        condition = raw.get("condition") if isinstance(raw.get("condition"), str) else None
        exists = condition == "ROUTE_EXISTS"
        elements.append(
            RouteElementEvidence(
                origin_place_id=request.origins[origin_index].place_id,
                destination_place_id=request.destinations[destination_index].place_id,
                status=_status_text(raw.get("status")),
                condition=condition,
                distance_meters=(
                    int(raw["distanceMeters"])
                    if isinstance(raw.get("distanceMeters"), int)
                    else None
                ),
                duration_seconds=_duration_seconds(raw.get("duration")),
                availability=(
                    EvidenceAvailability.AVAILABLE
                    if exists
                    else EvidenceAvailability.UNAVAILABLE
                ),
            )
        )
    available_count = sum(
        item.availability is EvidenceAvailability.AVAILABLE for item in elements
    )
    if not elements or available_count == 0:
        availability = EvidenceAvailability.UNAVAILABLE
    elif available_count < len(elements):
        availability = EvidenceAvailability.PARTIAL
    else:
        availability = EvidenceAvailability.AVAILABLE
    return RouteEvidence(
        travel_mode=request.travel_mode,
        mode_reason=mode_reason,
        routing_preference=request.routing_preference,
        availability=availability,
        elements=elements,
        unavailable_reason=("No route matrix elements were available" if not elements else None),
        retrieved_at=_retrieved_at(dto.retrieved_at),
        source_ref="google_routes:compute_route_matrix",
    )


def unavailable_routes(
    request: RouteMatrixRequest,
    *,
    mode_reason: str,
    reason: str,
) -> RouteEvidence:
    return RouteEvidence(
        travel_mode=request.travel_mode,
        mode_reason=mode_reason,
        routing_preference=request.routing_preference,
        availability=EvidenceAvailability.UNAVAILABLE,
        unavailable_reason=reason,
        retrieved_at=datetime.now(UTC),
        source_ref="google_routes:compute_route_matrix",
    )
