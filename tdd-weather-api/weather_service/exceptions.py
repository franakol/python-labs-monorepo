"""Custom exceptions for the Weather Service."""


class WeatherServiceError(Exception):
    """Base exception for all weather service errors."""

    pass


class CityNotFoundError(WeatherServiceError):
    """Raised when a city is not found in the weather data."""

    def __init__(self, city: str) -> None:
        self.message = f"City not found: {city}"
        super().__init__(self.message)


class InvalidAPIKeyError(WeatherServiceError):
    """Raised when an invalid API key is provided."""

    pass
