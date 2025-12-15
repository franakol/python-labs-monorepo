"""Data models for the Weather Service.

These dataclasses define the request and response structures
for the weather API with strict type hints.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WeatherForecast:
    """Weather forecast response model.

    Attributes:
        city: The city name for the forecast.
        temperature: Temperature in Celsius.
        conditions: Weather conditions description (e.g., 'Sunny', 'Cloudy').
        humidity: Relative humidity percentage (0-100).
        wind_speed: Wind speed in km/h.
        timestamp: When the forecast was generated.
    """

    city: str
    temperature: float
    conditions: str
    humidity: int
    wind_speed: float | None = None
    timestamp: datetime | None = None


@dataclass(frozen=True)
class WeatherRequest:
    """Weather forecast request model.

    Attributes:
        city: The city name to get forecast for.
        api_key: Optional API key for authentication.
    """

    city: str
    api_key: str | None = None
