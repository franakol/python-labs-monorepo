"""Tests for WeatherService error handling.

TDD Red Phase: These tests require custom exceptions that don't exist yet.
"""

import pytest

from weather_service.exceptions import CityNotFoundError, InvalidAPIKeyError
from weather_service.service import WeatherService


class TestWeatherServiceErrors:
    """Test cases for error conditions."""

    def test_get_forecast_raises_error_for_unknown_city(self) -> None:
        """Test that unknown city raises CityNotFoundError.

        RED Phase: Fails because CityNotFoundError doesn't exist.
        """
        # Arrange
        service = WeatherService()
        unknown_city = "Atlantis"

        # Act & Assert
        with pytest.raises(CityNotFoundError) as exc_info:
            service.get_forecast(unknown_city)

        assert str(exc_info.value) == f"City not found: {unknown_city}"

    def test_get_forecast_raises_error_for_empty_city(self) -> None:
        """Test that empty city raises CityNotFoundError.

        RED Phase: Fails because CityNotFoundError doesn't exist.
        """
        # Arrange
        service = WeatherService()

        # Act & Assert
        with pytest.raises(CityNotFoundError):
            service.get_forecast("")

    def test_get_forecast_raises_error_for_invalid_api_key(self) -> None:
        """Test that invalid API key raises InvalidAPIKeyError.

        RED Phase: Fails because service doesn't check API key yet.
        """
        # Arrange
        service = WeatherService()
        invalid_key = "invalid-key"

        # Act & Assert
        # The lab says: "Write failing tests for invalid inputs (e.g., unknown city, invalid API key)"
        # We need to add API key support to get_forecast
        with pytest.raises(InvalidAPIKeyError):
            service.get_forecast("London", api_key=invalid_key)
