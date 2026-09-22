"""Nearby Search wire contracts with no network transport."""

import asyncio

import pytest

from backend.app.integrations.google.places import PLACES_NEARBY_FIELD_MASK, GooglePlacesProvider
from backend.app.integrations.models import LatLng, PlaceNearbySearchRequest
from backend.tests.integrations.google.test_adapters import TRACER, FakeTransport


def request():
    return PlaceNearbySearchRequest(
        center=LatLng(latitude=0, longitude=0),
        radius_metres=800,
        max_result_count=10,
        included_types=("restaurant", "cafe", "park", "museum"),
        field_mask=PLACES_NEARBY_FIELD_MASK,
    )


def test_nearby_restricted_distance_wire_mask_and_attribution():
    transport = FakeTransport(
        [
            {
                "places": [
                    {
                        "id": "new",
                        "displayName": {"text": "Cafe"},
                        "location": {"latitude": 0.001, "longitude": 0},
                        "types": ["cafe"],
                        "formattedAddress": "Full address",
                        "primaryType": "cafe",
                        "attributions": [
                            {"provider": "Example", "providerUri": "https://example.test"}
                        ],
                    },
                    {
                        "id": "invalid",
                        "displayName": {"text": "Invalid"},
                        "location": {"latitude": 100, "longitude": 0},
                    },
                    {"displayName": {"text": "No identity"}},
                ]
            }
        ]
    )
    provider = GooglePlacesProvider(api_key="fake", transport=transport, tracer=TRACER)
    result = asyncio.run(provider.search_nearby(request()))
    assert len(transport.calls) == 1
    call = transport.calls[0]
    assert call["url"].endswith("/places:searchNearby")
    body = call["json_body"]
    assert body["rankPreference"] == "DISTANCE" and "locationBias" not in body
    assert body["locationRestriction"]["circle"]["radius"] == 800
    assert body["maxResultCount"] == 10
    assert body["includedTypes"] == ["restaurant", "cafe", "park", "museum"]
    assert body["includeFutureOpeningBusinesses"] is False
    assert set(call["headers"]["X-Goog-FieldMask"].split(",")) == {
        "places.id",
        "places.displayName",
        "places.location",
        "places.formattedAddress",
        "places.primaryType",
        "places.types",
        "places.businessStatus",
        "places.attributions",
    }
    assert len(result.candidates) == 1
    assert result.candidates[0].attributions[0]["provider"] == "Example"
    assert result.candidates[0].formatted_address == "Full address"


def test_nearby_adapter_never_retries():
    class Broken:
        calls = 0

        async def request_json(self, *args, **kwargs):
            self.calls += 1
            raise RuntimeError("offline provider error")

    transport = Broken()
    provider = GooglePlacesProvider(api_key="fake", transport=transport, tracer=TRACER)
    with pytest.raises(RuntimeError):
        asyncio.run(provider.search_nearby(request()))
    assert transport.calls == 1
