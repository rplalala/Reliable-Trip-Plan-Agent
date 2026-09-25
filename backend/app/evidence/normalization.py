"""Deterministic conversion from provider DTOs to planner evidence."""

from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime, timedelta
from decimal import ROUND_CEILING, Decimal, InvalidOperation
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from backend.app.evidence.models import (
    EvidenceAvailability,
    OpeningHoursEvidence,
    PlaceCandidate,
    PlaceEvidence,
    RouteElementEvidence,
    RouteElementEvidenceType,
    RouteEvidence,
    RouteEvidencePurpose,
    WeatherDayEvidence,
    WeatherEvidence,
)
from backend.app.integrations.models import (
    PlaceCandidateDTO,
    PlaceDetailsDTO,
    RouteMatrixDTO,
    RouteMatrixRequest,
    RouteWaypoint,
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


def _source_dates(source: Mapping[str, object]) -> list[date]:
    dates: set[date] = set()
    for raw_period in source.get("periods", []) if isinstance(source.get("periods"), list) else []:
        if isinstance(raw_period, Mapping):
            for endpoint in ("open", "close"):
                point = raw_period.get(endpoint)
                if isinstance(point, Mapping) and (parsed := _display_date(point.get("date"))):
                    dates.add(parsed)
    raw_special_days = source.get("specialDays", [])
    for special in raw_special_days if isinstance(raw_special_days, list) else []:
        if isinstance(special, Mapping) and (parsed := _display_date(special.get("date"))):
            dates.add(parsed)
    return sorted(dates)


def _current_window(details: PlaceDetailsDTO) -> tuple[date, date] | None:
    if details.time_zone is None:
        return None
    try:
        zone = ZoneInfo(details.time_zone)
        requested_at = _parse_datetime(details.requested_at or details.retrieved_at)
    except ZoneInfoNotFoundError:
        return None
    if requested_at is None:
        return None
    local_date = requested_at.astimezone(zone).date()
    return local_date, local_date + timedelta(days=6)


def _opening_hours(
    source: dict[str, object] | None,
    *,
    applicability: str,
    valid_window: tuple[date, date] | None = None,
) -> OpeningHoursEvidence | None:
    if source is None:
        return None

    descriptions = source.get("weekdayDescriptions", [])
    return OpeningHoursEvidence(
        periods_state=(
            "missing"
            if "periods" not in source
            else "present"
            if isinstance(source["periods"], list)
            and all(isinstance(p, dict) for p in source["periods"])
            else "invalid"
        ),
        periods=source.get("periods")
        if isinstance(source.get("periods"), list)
        and all(isinstance(p, dict) for p in source["periods"])
        else None,
        special_days=[
            d
            for row in (
                source.get("specialDays", []) if isinstance(source.get("specialDays"), list) else []
            )
            if isinstance(row, dict) and (d := _display_date(row.get("date")))
        ],
        applicability=applicability,
        valid_from=valid_window[0] if valid_window else None,
        valid_through=valid_window[1] if valid_window else None,
        source_dated_days=_source_dates(source),
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

    current_hours = _opening_hours(
        details.current_opening_hours,
        applicability="provider_current_window",
        valid_window=_current_window(details),
    )
    regular_hours = _opening_hours(
        details.regular_opening_hours,
        applicability="regular_weekly_pattern",
    )
    return PlaceEvidence(
        place_id=details.place_id,
        name=details.display_name,
        formatted_address=details.formatted_address or candidate.formatted_address,
        latitude=details.location.latitude,
        longitude=details.location.longitude,
        primary_type=details.primary_type or candidate.primary_type,
        business_status=details.business_status or candidate.business_status,
        timezone_id=details.time_zone,
        requested_at=_parse_datetime(details.requested_at or details.retrieved_at),
        opening_hours=current_hours or regular_hours,
        current_opening_hours=current_hours,
        regular_opening_hours=regular_hours,
        rating=details.rating,
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


def normalize_weather(
    dto: WeatherForecastDTO,
    *,
    request: WeatherRequest,
    destination: str,
) -> WeatherEvidence:
    """Filter provider days strictly to the requested inclusive date range."""

    by_date = {
        day.date: WeatherDayEvidence(**day.model_dump())
        for day in dto.forecast_days
        if request.requested_start <= day.date <= request.requested_end
    }
    normalized_days = sorted(by_date.values(), key=lambda day: day.date)
    from datetime import timedelta

    requested_dates = [
        request.requested_start + timedelta(days=offset)
        for offset in range((request.requested_end - request.requested_start).days + 1)
    ]
    fields = tuple(WeatherDayEvidence.model_fields.keys() - {"date"})
    useful = [day for day in normalized_days if any(getattr(day, f) is not None for f in fields)]
    missing_dates = [d for d in requested_dates if d not in {day.date for day in useful}]
    incomplete = any(any(getattr(day, f) is None for f in fields) for day in normalized_days)
    availability = (
        EvidenceAvailability.UNAVAILABLE
        if not useful
        else EvidenceAvailability.PARTIAL
        if missing_dates or incomplete
        else EvidenceAvailability.AVAILABLE
    )
    return WeatherEvidence(
        destination=destination,
        latitude=request.location.latitude,
        longitude=request.location.longitude,
        availability=availability,
        days=normalized_days,
        missing_dates=missing_dates,
        unavailable_reason="Some requested weather data is unavailable"
        if availability != EvidenceAvailability.AVAILABLE
        else None,
        retrieved_at=_retrieved_at(dto.retrieved_at),
        source_ref=dto.source_ref,
        timezone=dto.timezone,
        attribution=dto.attribution,
    )


def unavailable_weather(request: WeatherRequest, destination: str, reason: str) -> WeatherEvidence:
    from datetime import timedelta

    return WeatherEvidence(
        destination=destination,
        latitude=request.location.latitude,
        longitude=request.location.longitude,
        availability=EvidenceAvailability.UNAVAILABLE,
        missing_dates=[
            request.requested_start + timedelta(days=i)
            for i in range((request.requested_end - request.requested_start).days + 1)
        ],
        unavailable_reason=reason,
        retrieved_at=datetime.now(UTC),
        source_ref=f"{request.provider}:daily_forecast",
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
        seconds = Decimal(value[:-1])
        if not seconds.is_finite() or seconds < 0:
            return None
        return int(seconds.to_integral_value(rounding=ROUND_CEILING))
    except (ValueError, InvalidOperation):
        return None


def normalize_routes(
    dto: RouteMatrixDTO,
    *,
    request: RouteMatrixRequest,
    mode_reason: str,
    purpose: RouteEvidencePurpose = RouteEvidencePurpose.BASELINE,
) -> RouteEvidence:
    """Map matrix indexes back to stable Place IDs and retain failures explicitly."""

    elements: list[RouteElementEvidence] = []
    for raw in dto.elements:
        origin_index = raw.get("originIndex")
        destination_index = raw.get("destinationIndex")
        if (
            not isinstance(origin_index, int)
            or isinstance(origin_index, bool)
            or not isinstance(destination_index, int)
            or isinstance(destination_index, bool)
        ):
            continue
        if not 0 <= origin_index < len(request.origins):
            continue
        if not 0 <= destination_index < len(request.destinations):
            continue
        condition = raw.get("condition") if isinstance(raw.get("condition"), str) else None
        status = raw.get("status")
        status_state = (
            "missing"
            if "status" not in raw
            else "success"
            if isinstance(status, Mapping)
            and type(status.get("code", 0)) is int
            and status.get("code", 0) == 0
            else "error"
            if isinstance(status, Mapping) and type(status.get("code")) is int
            else "invalid"
        )
        duration = _duration_seconds(raw.get("duration"))
        exists = condition == "ROUTE_EXISTS" and status_state == "success" and duration is not None
        elements.append(
            RouteElementEvidence(
                origin_place_id=request.origins[origin_index].place_id,
                destination_place_id=request.destinations[destination_index].place_id,
                status=_status_text(raw.get("status")),
                condition=condition,
                status_state=status_state,
                unavailable_reason=None
                if exists
                else f"provider_status_{status_state}"
                if status_state != "success"
                else "invalid_or_missing_duration"
                if duration is None
                else condition or "missing_condition",
                requested_at=_parse_datetime(dto.requested_at),
                retrieved_at=_retrieved_at(dto.retrieved_at),
                origin_index=origin_index,
                destination_index=destination_index,
                static_duration_seconds=_duration_seconds(raw.get("staticDuration")),
                fallback_info=raw.get("fallbackInfo")
                if isinstance(raw.get("fallbackInfo"), dict)
                else None,
                distance_meters=(
                    int(raw["distanceMeters"])
                    if isinstance(raw.get("distanceMeters"), int)
                    and not isinstance(raw.get("distanceMeters"), bool)
                    and raw["distanceMeters"] >= 0
                    else None
                ),
                duration_seconds=duration,
                availability=(
                    EvidenceAvailability.AVAILABLE if exists else EvidenceAvailability.UNAVAILABLE
                ),
            )
        )
    available_count = sum(item.availability is EvidenceAvailability.AVAILABLE for item in elements)
    if not elements or available_count == 0:
        availability = EvidenceAvailability.UNAVAILABLE
    elif available_count < len(elements):
        availability = EvidenceAvailability.PARTIAL
    else:
        availability = EvidenceAvailability.AVAILABLE
    return RouteEvidence(
        travel_mode=request.travel_mode,
        requested_at=_parse_datetime(dto.requested_at),
        mode_reason=mode_reason,
        purpose=purpose,
        routing_preference=request.routing_preference,
        representative_departure_time=request.departure_time,
        availability=availability,
        elements=elements,
        unavailable_reason=("No route matrix elements were available" if not elements else None),
        retrieved_at=_retrieved_at(dto.retrieved_at),
        source_ref="google_routes:compute_route_matrix",
    )


def merge_baseline_route_chunks(
    waypoints: Sequence[RouteWaypoint],
    chunks: Sequence[tuple[RouteMatrixRequest, RouteEvidence]],
    *,
    travel_mode: str,
    mode_reason: str,
    routing_preference: str | None,
    departure_time: datetime | None,
    fallback_reason: str | None = None,
) -> RouteEvidence:
    """Merge local-index results into one stable, complete directed Place-ID grid."""

    place_ids = tuple(item.place_id for item in waypoints)
    if len(set(place_ids)) != len(place_ids):
        raise ValueError("Baseline Route Matrix requires unique selected Place IDs")
    merged: dict[tuple[str, str], RouteElementEvidence] = {}
    assigned_origins: set[str] = set()
    for request, evidence in chunks:
        if tuple(item.place_id for item in request.destinations) != place_ids:
            raise ValueError("Baseline chunk destinations must match selected POI order")
        if request.travel_mode != travel_mode:
            raise ValueError("Baseline chunk mode must match the selected transport mode")
        raw_pairs: dict[tuple[str, str], list[RouteElementEvidence]] = {}
        for item in evidence.elements:
            raw_pairs.setdefault((item.origin_place_id, item.destination_place_id), []).append(item)
        for origin in request.origins:
            if origin.place_id in assigned_origins:
                raise ValueError("A baseline origin appears in more than one chunk")
            assigned_origins.add(origin.place_id)
            for destination in request.destinations:
                pair = (origin.place_id, destination.place_id)
                rows = raw_pairs.get(pair, [])
                if len(rows) == 1:
                    element = rows[0]
                    if element.availability is EvidenceAvailability.UNAVAILABLE:
                        element = element.model_copy(
                            update={
                                "unavailable_reason": (
                                    element.condition
                                    or element.status
                                    or "provider_route_unavailable"
                                )
                            }
                        )
                else:
                    reason = (
                        "duplicate_provider_indices"
                        if len(rows) > 1
                        else evidence.unavailable_reason or "missing_provider_element"
                    )
                    element = RouteElementEvidence(
                        origin_place_id=origin.place_id,
                        destination_place_id=destination.place_id,
                        evidence_type=RouteElementEvidenceType.NOT_OBSERVED,
                        availability=EvidenceAvailability.UNAVAILABLE,
                        unavailable_reason=reason,
                    )
                merged[pair] = element
    elements = [
        merged.get((origin, destination))
        or RouteElementEvidence(
            origin_place_id=origin,
            destination_place_id=destination,
            evidence_type=RouteElementEvidenceType.NOT_OBSERVED,
            availability=EvidenceAvailability.UNAVAILABLE,
            unavailable_reason=fallback_reason or "baseline_chunk_not_attempted",
        )
        for origin in place_ids
        for destination in place_ids
    ]
    available_count = sum(item.availability is EvidenceAvailability.AVAILABLE for item in elements)
    availability = (
        EvidenceAvailability.AVAILABLE
        if available_count == len(elements) and elements
        else EvidenceAvailability.PARTIAL
        if available_count
        else EvidenceAvailability.UNAVAILABLE
    )
    return RouteEvidence(
        travel_mode=travel_mode,
        mode_reason=mode_reason,
        purpose=RouteEvidencePurpose.BASELINE,
        routing_preference=routing_preference,
        representative_departure_time=departure_time,
        availability=availability,
        elements=elements,
        unavailable_reason=(
            fallback_reason or "No baseline route elements were available"
            if availability is EvidenceAvailability.UNAVAILABLE
            else "Some baseline route elements were unavailable"
            if availability is EvidenceAvailability.PARTIAL
            else None
        ),
        retrieved_at=max(
            (evidence.retrieved_at for _, evidence in chunks), default=datetime.now(UTC)
        ),
        source_ref="google_routes:compute_route_matrix",
    )


def unavailable_routes(
    request: RouteMatrixRequest,
    *,
    mode_reason: str,
    reason: str,
    purpose: RouteEvidencePurpose = RouteEvidencePurpose.BASELINE,
) -> RouteEvidence:
    return RouteEvidence(
        travel_mode=request.travel_mode,
        mode_reason=mode_reason,
        purpose=purpose,
        routing_preference=request.routing_preference,
        representative_departure_time=request.departure_time,
        availability=EvidenceAvailability.UNAVAILABLE,
        unavailable_reason=reason,
        retrieved_at=datetime.now(UTC),
        source_ref="google_routes:compute_route_matrix",
    )
