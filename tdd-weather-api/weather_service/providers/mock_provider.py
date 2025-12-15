"""Mock weather provider implementation.

This module provides a MockWeatherProvider that returns predefined
weather data for testing and development purposes.
"""

import logging
from typing import Any

from weather_service.exceptions import CityNotFoundError
from weather_service.providers.base import WeatherProvider

logger = logging.getLogger(__name__)


class MockWeatherProvider(WeatherProvider):
    """Mock weather provider with predefined city data.

    This provider returns hardcoded weather data for a set of known cities.
    Used for testing and as the default provider.

    Attributes:
        _weather_data: Dictionary mapping city names to weather data.
    """

    def __init__(self) -> None:
        """Initialize with predefined weather data for known cities."""
        self._weather_data: dict[str, dict[str, Any]] = {
            "London": {
                "temperature": 15.0,
                "conditions": "Cloudy",
                "humidity": 75,
                "wind_speed": 12.5,
            },
            "Paris": {
                "temperature": 18.0,
                "conditions": "Sunny",
                "humidity": 60,
                "wind_speed": 8.0,
            },
            "Tokyo": {
                "temperature": 22.0,
                "conditions": "Partly Cloudy",
                "humidity": 65,
                "wind_speed": 10.0,
            },
            "New York": {
                "temperature": 20.0,
                "conditions": "Clear",
                "humidity": 55,
                "wind_speed": 15.0,
            },
            "Sydney": {
                "temperature": 25.0,
                "conditions": "Sunny",
                "humidity": 50,
                "wind_speed": 18.0,
            },
        }

    def get_weather(self, city: str) -> dict[str, Any]:
        """Get weather data for a city.

        Args:
            city: The name of the city (case-insensitive).

        Returns:
            Dictionary containing weather data.

        Raises:
            CityNotFoundError: If the city is not found.
        """
        if not city:
            logger.error(f"Error fetching forecast for city: {city}")
            raise CityNotFoundError("")

        normalized = self._normalize_city_name(city)
        if normalized is None:
            logger.error(f"Error fetching forecast for city: {city}")
            raise CityNotFoundError(city)

        return self._weather_data[normalized]

    def _normalize_city_name(self, city: str) -> str | None:
        """Normalize city name to match known cities.

        Args:
            city: The city name to normalize.

        Returns:
            The canonical city name, or None if not found.
        """
        city_lower = city.lower()
        for known_city in self._weather_data:
            if known_city.lower() == city_lower:
                return known_city
        return None
