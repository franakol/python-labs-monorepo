"""Weather Service implementation.

This module provides the WeatherService class that returns weather forecasts
for known cities with predefined data.
"""

import logging
from datetime import datetime

from weather_service.exceptions import CityNotFoundError, InvalidAPIKeyError
from weather_service.models import WeatherForecast

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for retrieving weather forecasts.

    This is a mock service that returns predefined weather data
    for a set of known cities. It demonstrates the TDD workflow
    where tests are written before implementation.

    Attributes:
        _weather_data: Dictionary of predefined weather data for known cities.

    Example:
        >>> service = WeatherService()
        >>> forecast = service.get_forecast("London")
        >>> print(f"Temperature: {forecast.temperature}°C")
        Temperature: 15.0°C
    """

    def __init__(self) -> None:
        """Initialize the WeatherService with predefined city data."""
        self._weather_data: dict[str, dict] = {
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

    def get_forecast(self, city: str, api_key: str | None = None) -> WeatherForecast:
        """Get weather forecast for a city.

        Args:
            city: The name of the city to get forecast for.
                  City lookup is case-insensitive.
            api_key: Optional API key. In this mock, 'invalid-key' raises error.

        Returns:
            WeatherForecast containing city weather data.

        Raises:
            CityNotFoundError: If the city is not found in the database.
            InvalidAPIKeyError: If the provided API key is invalid.

        Example:
            >>> service = WeatherService()
            >>> forecast = service.get_forecast("london")
            >>> forecast.city
            'London'
        """
        logger.info(f"Fetching weather forecast for {city}")

        # Validate API key (mock logic)
        if api_key == "invalid-key":
            raise InvalidAPIKeyError(f"Invalid API key: {api_key}")

        # Normalize city name (case-insensitive lookup)
        try:
            normalized_city = self._normalize_city_name(city)
        except ValueError:
            logger.error(f"Error fetching forecast for city: {city}")
            # Re-raise internal ValueError as CityNotFoundError
            raise CityNotFoundError(city) from None

        data = self._weather_data[normalized_city]

        return WeatherForecast(
            city=normalized_city,
            temperature=data["temperature"],
            conditions=data["conditions"],
            humidity=data["humidity"],
            wind_speed=data["wind_speed"],
            timestamp=datetime.now(),
        )

    def _normalize_city_name(self, city: str) -> str:
        """Normalize city name to match known cities.

        Args:
            city: The city name to normalize.

        Returns:
            The canonical city name.

        Raises:
            CityNotFoundError: If the city is not found.
        """
        if not city:
            logger.error(f"Error fetching forecast for city: {city}")
            raise CityNotFoundError("")

        city_lower = city.lower()
        for known_city in self._weather_data:
            if known_city.lower() == city_lower:
                return known_city

        logger.error(f"Error fetching forecast for city: {city}")
        raise CityNotFoundError(city)
