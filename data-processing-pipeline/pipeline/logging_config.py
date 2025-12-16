"""Logging configuration for the data processing pipeline.

Provides structured logging with JSON format and trace ID support
for observability across pipeline stages.
"""

import logging
import sys
from typing import Any


class PipelineFormatter(logging.Formatter):
    """Custom formatter for structured pipeline logs.

    Formats logs with consistent structure including trace IDs
    when available in the log message.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record.

        Args:
            record: The log record to format.

        Returns:
            Formatted log string.
        """
        # Add pipeline-specific fields
        record.pipeline_name = "data-processing-pipeline"

        return super().format(record)


def setup_logging(
    level: int = logging.INFO,
    format_string: str | None = None,
) -> None:
    """Configure logging for the pipeline.

    Sets up a console handler with structured formatting.

    Args:
        level: The logging level (default: INFO).
        format_string: Custom format string (optional).
    """
    if format_string is None:
        format_string = (
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )

    # Create formatter
    formatter = PipelineFormatter(format_string)

    # Configure root logger for pipeline
    logger = logging.getLogger("pipeline")
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Prevent propagation to root logger
    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a pipeline component.

    Args:
        name: The component name (e.g., 'text_cleaner').

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(f"pipeline.{name}")
