"""Tests for WeatherProvider abstraction and dependency injection.

TDD Red Phase: These tests require an abstract WeatherProvider interface
that doesn't exist yet. Tests will fail until we implement the interface.
"""

from abc import ABC
from unittest.mock import Mock

from weather_service.providers.base import WeatherProvider
from weather_service.service import WeatherService


class TestWeatherProviderInterface:
    """Tests for the abstract WeatherProvider interface."""

    def test_weather_provider_is_abstract(self) -> None:
        """Test that WeatherProvider cannot be instantiated directly.

        RED Phase: Fails because WeatherProvider doesn't exist.
        """
        assert issubclass(WeatherProvider, ABC)

    def test_weather_provider_has_get_weather_method(self) -> None:
        """Test that WeatherProvider defines get_weather abstract method.

        RED Phase: Fails because WeatherProvider doesn't exist.
        """
        assert hasattr(WeatherProvider, "get_weather")


class TestWeatherServiceDependencyInjection:
    """Tests for WeatherService dependency injection."""

    def test_weather_service_accepts_provider(self) -> None:
        """Test that WeatherService can accept a custom provider.

        RED Phase: Fails because WeatherService doesn't accept provider param.
        """
        mock_provider = Mock(spec=WeatherProvider)
        service = WeatherService(provider=mock_provider)
        assert service._provider is mock_provider

    def test_weather_service_uses_injected_provider(self) -> None:
        """Test that WeatherService uses the injected provider.

        RED Phase: Fails because WeatherService doesn't use provider.
        """
        mock_provider = Mock(spec=WeatherProvider)
        mock_provider.get_weather.return_value = {
            "temperature": 99.0,
            "conditions": "Test",
            "humidity": 50,
            "wind_speed": 5.0,
        }

        service = WeatherService(provider=mock_provider)
        forecast = service.get_forecast("TestCity")

        mock_provider.get_weather.assert_called_once_with("TestCity")
        assert forecast.temperature == 99.0
        assert forecast.conditions == "Test"

    def test_weather_service_defaults_to_mock_provider(self) -> None:
        """Test that WeatherService defaults to MockWeatherProvider.

        RED Phase: Fails because MockWeatherProvider doesn't exist.
        """
        from weather_service.providers.mock_provider import MockWeatherProvider

        service = WeatherService()
        assert isinstance(service._provider, MockWeatherProvider)
