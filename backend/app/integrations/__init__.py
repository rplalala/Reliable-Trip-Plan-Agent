"""External provider protocols and concrete adapters."""

from backend.app.integrations.protocols import PlacesProvider, RoutesProvider, WeatherProvider

__all__ = ["PlacesProvider", "RoutesProvider", "WeatherProvider"]
