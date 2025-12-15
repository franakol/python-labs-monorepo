"""Abstract base class for weather providers.

This module defines the WeatherProvider interface that all concrete
weather providers must implement. This follows the Dependency Inversion
Principle (DIP) from SOLID.
"""

from abc import ABC, abstractmethod
from typing import Any


class WeatherProvider(ABC):
    """Abstract base class for weather data providers.

    All weather providers must implement the get_weather method
    to retrieve weather data for a given city.

    Example:
        >>> class MyProvider(WeatherProvider):
        ...     def get_weather(self, city: str) -> dict:
        ...         return {"temperature": 20.0, ...}
    """

    @abstractmethod
    def get_weather(self, city: str) -> dict[str, Any]:
        """Get weather data for a city.

        Args:
            city: The name of the city.

        Returns:
            Dictionary containing weather data with keys:
            - temperature: float
            - conditions: str
            - humidity: int
            - wind_speed: float

        Raises:
            CityNotFoundError: If the city is not found.
        """
        pass
