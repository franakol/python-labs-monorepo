"""Tests for WeatherService - TDD Red Phase.

These tests are written BEFORE the implementation exists.
They should FAIL initially to demonstrate the TDD workflow.
"""

import pytest

from weather_service.models import WeatherForecast
from weather_service.service import WeatherService


class TestWeatherServiceGetForecast:
    """Test cases for WeatherService.get_forecast() method."""

    def test_get_forecast_returns_weather_forecast_for_valid_city(self) -> None:
        """Test that get_forecast returns a WeatherForecast for a known city.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        service = WeatherService()
        city = "London"

        # Act
        result = service.get_forecast(city)

        # Assert
        assert isinstance(result, WeatherForecast)
        assert result.city == "London"

    def test_get_forecast_returns_temperature_for_valid_city(self) -> None:
        """Test that forecast includes temperature data.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        service = WeatherService()
        city = "London"

        # Act
        result = service.get_forecast(city)

        # Assert
        assert result.temperature is not None
        assert isinstance(result.temperature, float)

    def test_get_forecast_returns_conditions_for_valid_city(self) -> None:
        """Test that forecast includes weather conditions.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        service = WeatherService()
        city = "Paris"

        # Act
        result = service.get_forecast(city)

        # Assert
        assert result.conditions is not None
        assert isinstance(result.conditions, str)

    def test_get_forecast_returns_humidity_for_valid_city(self) -> None:
        """Test that forecast includes humidity data.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        service = WeatherService()
        city = "Tokyo"

        # Act
        result = service.get_forecast(city)

        # Assert
        assert result.humidity is not None
        assert 0 <= result.humidity <= 100

    @pytest.mark.parametrize(
        "city,expected_temp",
        [
            ("London", 15.0),
            ("Paris", 18.0),
            ("Tokyo", 22.0),
            ("New York", 20.0),
            ("Sydney", 25.0),
        ],
    )
    def test_get_forecast_returns_predefined_data_for_known_cities(
        self, city: str, expected_temp: float
    ) -> None:
        """Test that known cities return consistent predefined data.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        service = WeatherService()

        # Act
        result = service.get_forecast(city)

        # Assert
        assert result.city == city
        assert result.temperature == expected_temp

    def test_get_forecast_returns_wind_speed_for_valid_city(self) -> None:
        """Test that forecast includes wind speed data.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        service = WeatherService()
        city = "London"

        # Act
        result = service.get_forecast(city)

        # Assert
        assert result.wind_speed is not None
        assert isinstance(result.wind_speed, float)
        assert result.wind_speed >= 0

    def test_get_forecast_returns_timestamp(self) -> None:
        """Test that forecast includes a timestamp.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        from datetime import datetime

        service = WeatherService()
        city = "Paris"

        # Act
        result = service.get_forecast(city)

        # Assert
        assert result.timestamp is not None
        assert isinstance(result.timestamp, datetime)

    def test_get_forecast_is_case_insensitive(self) -> None:
        """Test that city lookup is case insensitive.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        service = WeatherService()

        # Act
        result_lower = service.get_forecast("london")
        result_upper = service.get_forecast("LONDON")
        result_mixed = service.get_forecast("LoNdOn")

        # Assert - all should return London data
        assert result_lower.city == "London"
        assert result_upper.city == "London"
        assert result_mixed.city == "London"
        assert result_lower.temperature == result_upper.temperature

    def test_get_forecast_returns_consistent_data(self) -> None:
        """Test that repeated calls return the same data.

        RED Phase: This test will fail because WeatherService doesn't exist yet.
        """
        # Arrange
        service = WeatherService()
        city = "Tokyo"

        # Act
        result1 = service.get_forecast(city)
        result2 = service.get_forecast(city)

        # Assert
        assert result1.temperature == result2.temperature
        assert result1.conditions == result2.conditions
        assert result1.humidity == result2.humidity
