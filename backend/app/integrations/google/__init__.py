"""Google Maps Platform adapters used by V1-A."""

from backend.app.integrations.google.places import (
    PLACES_CANDIDATE_FIELD_MASK,
    PLACES_DESTINATION_FIELD_MASK,
    PLACES_DETAILS_FIELD_MASK,
    PLACES_REVIEWS_FIELD_MASK,
    GooglePlacesProvider,
)
from backend.app.integrations.google.routes import (
    ROUTE_MATRIX_FIELD_MASK,
    GoogleRoutesProvider,
)
from backend.app.integrations.google.weather import GoogleWeatherProvider

__all__ = [
    "GooglePlacesProvider",
    "GoogleRoutesProvider",
    "GoogleWeatherProvider",
    "PLACES_CANDIDATE_FIELD_MASK",
    "PLACES_DESTINATION_FIELD_MASK",
    "PLACES_DETAILS_FIELD_MASK",
    "PLACES_REVIEWS_FIELD_MASK",
    "ROUTE_MATRIX_FIELD_MASK",
]
