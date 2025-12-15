"""Tests for WeatherService logging."""

import logging

from pytest import LogCaptureFixture

from weather_service.service import WeatherService


def test_get_forecast_logs_request(caplog: LogCaptureFixture) -> None:
    """Test that valid request logs info message.

    RED Phase: Fails because logging is not implemented.
    """
    service = WeatherService()
    city = "London"

    with caplog.at_level(logging.INFO):
        service.get_forecast(city)

    assert f"Fetching weather forecast for {city}" in caplog.text


def test_get_forecast_logs_error(caplog: LogCaptureFixture) -> None:
    """Test that error logs error message.

    RED Phase: Fails because logging is not implemented.
    """
    service = WeatherService()
    city = "Atlantis"

    with caplog.at_level(logging.ERROR):
        try:
            service.get_forecast(city)
        except Exception:
            pass

    assert f"Error fetching forecast for city: {city}" in caplog.text
