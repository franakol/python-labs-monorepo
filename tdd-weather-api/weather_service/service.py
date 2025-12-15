"""Weather Service implementation.

This module provides the WeatherService class that returns weather forecasts
using a pluggable provider pattern (Dependency Inversion Principle).
"""

import logging
from datetime import datetime

from weather_service.exceptions import InvalidAPIKeyError
from weather_service.models import WeatherForecast
from weather_service.providers.base import WeatherProvider
from weather_service.providers.mock_provider import MockWeatherProvider

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for retrieving weather forecasts.

    This service uses dependency injection to allow different weather
    providers to be plugged in. By default, it uses MockWeatherProvider.

    Attributes:
        _provider: The weather provider used to fetch data.

    Example:
        >>> service = WeatherService()
        >>> forecast = service.get_forecast("London")
        >>> print(f"Temperature: {forecast.temperature}°C")
        Temperature: 15.0°C

        # With custom provider:
        >>> custom_provider = MyCustomProvider()
        >>> service = WeatherService(provider=custom_provider)
    """

    def __init__(self, provider: WeatherProvider | None = None) -> None:
        """Initialize the WeatherService with a weather provider.

        Args:
            provider: Optional weather provider. Defaults to MockWeatherProvider.
        """
        self._provider: WeatherProvider = provider or MockWeatherProvider()

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

        # Get weather data from provider
        data = self._provider.get_weather(city)

        # Normalize city name for display
        normalized_city = city.title()
        if " " in city:
            # Handle multi-word cities like "New York"
            normalized_city = " ".join(word.title() for word in city.split())

        return WeatherForecast(
            city=normalized_city,
            temperature=data["temperature"],
            conditions=data["conditions"],
            humidity=data["humidity"],
            wind_speed=data["wind_speed"],
            timestamp=datetime.now(),
        )
