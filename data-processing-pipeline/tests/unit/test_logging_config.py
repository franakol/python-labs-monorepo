"""Unit tests for the logging configuration module."""

import logging

from pipeline.logging_config import PipelineFormatter, get_logger, setup_logging


class TestLoggingConfig:
    """Tests for logging configuration."""

    def test_setup_logging_creates_handler(self) -> None:
        """Test that setup_logging configures the pipeline logger."""
        setup_logging(level=logging.DEBUG)

        logger = logging.getLogger("pipeline")
        assert len(logger.handlers) > 0
        assert logger.level == logging.DEBUG

    def test_setup_logging_with_custom_format(self) -> None:
        """Test setup_logging with custom format string."""
        custom_format = "%(levelname)s - %(message)s"
        setup_logging(format_string=custom_format)

        logger = logging.getLogger("pipeline")
        assert len(logger.handlers) > 0

    def test_get_logger_returns_pipeline_child(self) -> None:
        """Test that get_logger returns a child of pipeline logger."""
        logger = get_logger("test_component")
        assert logger.name == "pipeline.test_component"

    def test_pipeline_formatter_format(self) -> None:
        """Test that PipelineFormatter formats records correctly."""
        formatter = PipelineFormatter("%(pipeline_name)s | %(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)

        assert "data-processing-pipeline" in result
        assert "Test message" in result
