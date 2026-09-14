"""Google Places API (New) adapter with fixed cost-aware field masks."""

from collections.abc import Mapping
from datetime import UTC, datetime
from urllib.parse import quote

from backend.app.integrations.google.common import (
    ProviderResponseError,
    require_mapping,
    trace_exchange,
)
from backend.app.integrations.http import AsyncJSONTransport
from backend.app.integrations.models import (
    LatLng,
    PlaceCandidateDTO,
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceOpeningDateDTO,
    PlaceReviewDTO,
    PlaceReviewsDTO,
    PlaceReviewsRequest,
    PlaceSearchRequest,
    PlaceSearchResponse,
)
from backend.app.observability.run_trace import RunTracer

PLACES_DESTINATION_FIELDS = (
    "places.id",
    "places.displayName",
    "places.location",
    "places.formattedAddress",
    "places.primaryType",
    "places.businessStatus",
)
PLACES_DESTINATION_FIELD_MASK = ",".join(PLACES_DESTINATION_FIELDS)

PLACES_CANDIDATE_FIELDS = (*PLACES_DESTINATION_FIELDS, "places.openingDate")
PLACES_CANDIDATE_FIELD_MASK = ",".join(PLACES_CANDIDATE_FIELDS)

PLACES_DETAILS_FIELDS = (
    "id",
    "displayName",
    "location",
    "formattedAddress",
    "primaryType",
    "businessStatus",
    "openingDate",
    "timeZone",
    "currentOpeningHours",
    "regularOpeningHours",
    "rating",
    "websiteUri",
    "priceLevel",
    "priceRange",
    "accessibilityOptions",
)
PLACES_DETAILS_FIELD_MASK = ",".join(PLACES_DETAILS_FIELDS)

PLACES_REVIEWS_FIELDS = (
    "id",
    "reviews.name",
    "reviews.text",
    "reviews.publishTime",
    "reviews.googleMapsUri",
)
PLACES_REVIEWS_FIELD_MASK = ",".join(PLACES_REVIEWS_FIELDS)


def _localized_text(value: object) -> str | None:
    if not isinstance(value, Mapping):
        return None
    text = value.get("text")
    return text if isinstance(text, str) and text.strip() else None


def _lat_lng(value: object, *, context: str) -> LatLng:
    mapping = require_mapping(value, context=context)
    try:
        return LatLng(
            latitude=float(mapping["latitude"]),
            longitude=float(mapping["longitude"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ProviderResponseError(f"{context} has no valid coordinate") from exc


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def _time_zone_id(value: object) -> str | None:
    """Extract the IANA ID from the Places API TimeZone object."""

    if isinstance(value, Mapping):
        return _optional_string(value.get("id"))
    return _optional_string(value)


def _opening_date(value: object) -> PlaceOpeningDateDTO | None:
    if not isinstance(value, Mapping):
        return None
    parts: dict[str, int] = {}
    for name in ("year", "month", "day"):
        part = value.get(name)
        if isinstance(part, int) and not isinstance(part, bool) and part > 0:
            parts[name] = part
    return PlaceOpeningDateDTO(**parts) if parts else None


def _aware_datetime(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


class GooglePlacesProvider:
    """Map Google Places JSON into small provider DTOs."""

    def __init__(
        self,
        *,
        api_key: str,
        transport: AsyncJSONTransport,
        tracer: RunTracer,
        base_url: str = "https://places.googleapis.com/v1",
    ) -> None:
        self._api_key = api_key
        self._transport = transport
        self._tracer = tracer
        self._base_url = base_url.rstrip("/")

    async def search_text(self, request: PlaceSearchRequest) -> PlaceSearchResponse:
        body: dict[str, object] = {
            "textQuery": request.text_query,
            "pageSize": request.page_size,
            "languageCode": request.language_code,
        }
        if request.include_future_opening_businesses:
            body["includeFutureOpeningBusinesses"] = True
        if request.location_bias is not None:
            body["locationBias"] = {
                "circle": {
                    "center": request.location_bias.model_dump(),
                    "radius": 50_000.0,
                }
            }
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self._api_key,
            "X-Goog-FieldMask": request.field_mask,
        }
        response = await self._transport.request_json(
            "POST",
            f"{self._base_url}/places:searchText",
            headers=headers,
            json_body=body,
        )
        trace_exchange(
            self._tracer,
            name="google_places_search_text",
            request={"headers": headers, "body": body},
            response=response,
        )
        payload = require_mapping(response, context="Places Text Search response")
        raw_places = payload.get("places", [])
        if not isinstance(raw_places, list):
            raise ProviderResponseError("Places Text Search places must be an array")

        candidates: list[PlaceCandidateDTO] = []
        for rank, raw_place in enumerate(raw_places):
            if not isinstance(raw_place, Mapping):
                continue
            place_id = _optional_string(raw_place.get("id"))
            display_name = _localized_text(raw_place.get("displayName"))
            if place_id is None or display_name is None:
                continue
            try:
                location = _lat_lng(raw_place.get("location"), context="Place location")
            except ProviderResponseError:
                continue
            candidates.append(
                PlaceCandidateDTO(
                    place_id=place_id,
                    display_name=display_name,
                    location=location,
                    formatted_address=_optional_string(raw_place.get("formattedAddress")),
                    primary_type=_optional_string(raw_place.get("primaryType")),
                    business_status=_optional_string(raw_place.get("businessStatus")),
                    opening_date=_opening_date(raw_place.get("openingDate")),
                    provider_rank=rank,
                )
            )
        return PlaceSearchResponse(
            candidates=candidates,
            actual_result_count=len(raw_places),
            retrieved_at=datetime.now(UTC).isoformat(),
        )

    async def get_place_details(self, request: PlaceDetailsRequest) -> PlaceDetailsDTO:
        requested_at = datetime.now(UTC).isoformat()
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self._api_key,
            "X-Goog-FieldMask": request.field_mask,
        }
        params = {"languageCode": request.language_code}
        response = await self._transport.request_json(
            "GET",
            f"{self._base_url}/places/{quote(request.place_id, safe='')}",
            headers=headers,
            params=params,
        )
        trace_exchange(
            self._tracer,
            name="google_places_details",
            request={"headers": headers, "params": params, "place_id": request.place_id},
            response=response,
        )
        place = require_mapping(response, context="Place Details response")
        place_id = _optional_string(place.get("id"))
        display_name = _localized_text(place.get("displayName"))
        if place_id is None or display_name is None:
            raise ProviderResponseError("Place Details response lacks id or displayName")
        return PlaceDetailsDTO(
            place_id=place_id,
            display_name=display_name,
            location=_lat_lng(place.get("location"), context="Place Details location"),
            formatted_address=_optional_string(place.get("formattedAddress")),
            primary_type=_optional_string(place.get("primaryType")),
            business_status=_optional_string(place.get("businessStatus")),
            opening_date=_opening_date(place.get("openingDate")),
            time_zone=_time_zone_id(place.get("timeZone")),
            current_opening_hours=(
                dict(place["currentOpeningHours"])
                if isinstance(place.get("currentOpeningHours"), Mapping)
                else None
            ),
            regular_opening_hours=(
                dict(place["regularOpeningHours"])
                if isinstance(place.get("regularOpeningHours"), Mapping)
                else None
            ),
            rating=(
                float(place["rating"])
                if isinstance(place.get("rating"), int | float)
                and not isinstance(place.get("rating"), bool)
                and 0 <= place["rating"] <= 5
                else None
            ),
            website_uri=_optional_string(place.get("websiteUri")),
            price_level=_optional_string(place.get("priceLevel")),
            price_range=(
                dict(place["priceRange"]) if isinstance(place.get("priceRange"), Mapping) else None
            ),
            accessibility_options=(
                {
                    str(key): value
                    for key, value in place["accessibilityOptions"].items()
                    if isinstance(value, bool)
                }
                if isinstance(place.get("accessibilityOptions"), Mapping)
                else None
            ),
            requested_at=requested_at,
            retrieved_at=datetime.now(UTC).isoformat(),
        )

    async def get_place_reviews(self, request: PlaceReviewsRequest) -> PlaceReviewsDTO:
        """Fetch only review evidence for one Place ID."""

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self._api_key,
            "X-Goog-FieldMask": request.field_mask,
        }
        params = {"languageCode": request.language_code}
        response = await self._transport.request_json(
            "GET",
            f"{self._base_url}/places/{quote(request.place_id, safe='')}",
            headers=headers,
            params=params,
        )
        trace_exchange(
            self._tracer,
            name="google_places_reviews",
            request={"headers": headers, "params": params, "place_id": request.place_id},
            response={
                "place_id": request.place_id,
                "review_count": (
                    len(response.get("reviews", []))
                    if isinstance(response, Mapping) and isinstance(response.get("reviews"), list)
                    else None
                ),
            },
        )
        place = require_mapping(response, context="Place Reviews response")
        returned_id = _optional_string(place.get("id"))
        if returned_id is not None and returned_id != request.place_id:
            raise ProviderResponseError("Place Reviews response ID does not match request")
        raw_reviews = place.get("reviews", [])
        if not isinstance(raw_reviews, list):
            raise ProviderResponseError("Place Reviews reviews must be an array")
        if any(not isinstance(item, Mapping) for item in raw_reviews):
            raise ProviderResponseError("Place Reviews contains an invalid review")
        reviews = [
            PlaceReviewDTO(
                resource_name=_optional_string(item.get("name")),
                text=_localized_text(item.get("text")),
                publish_time=_aware_datetime(item.get("publishTime")),
                google_maps_uri=_optional_string(item.get("googleMapsUri")),
            )
            for item in raw_reviews
        ]
        return PlaceReviewsDTO(
            place_id=request.place_id,
            reviews=reviews,
            retrieved_at=datetime.now(UTC).isoformat(),
        )
