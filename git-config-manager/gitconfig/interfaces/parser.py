"""Abstract interface for configuration file parsing.

This module defines the contract for parsing and serializing
configuration files in various formats (JSON, YAML, etc.).
"""

from abc import ABC, abstractmethod
from typing import Any

from gitconfig.models import ConfigFormat


class ConfigParserInterface(ABC):
    """Abstract interface for configuration file parsing.

    Implementations handle reading and writing configuration data
    in specific formats like JSON or YAML.
    """

    @property
    @abstractmethod
    def format(self) -> ConfigFormat:
        """Return the configuration format this parser handles."""
        ...

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Return the file extension for this format (without dot)."""
        ...

    @abstractmethod
    def parse(self, content: str) -> dict[str, Any]:
        """Parse configuration content into a dictionary.

        Args:
            content: Raw string content to parse.

        Returns:
            Parsed configuration as a dictionary.

        Raises:
            ParseError: If the content cannot be parsed.
        """
        ...

    @abstractmethod
    def serialize(self, data: dict[str, Any]) -> str:
        """Serialize a dictionary to configuration format.

        Args:
            data: Dictionary to serialize.

        Returns:
            Serialized content as a string.

        Raises:
            ParseError: If the data cannot be serialized.
        """
        ...

    @abstractmethod
    def validate(self, content: str) -> bool:
        """Validate that content is valid for this format.

        Args:
            content: Raw string content to validate.

        Returns:
            True if the content is valid, False otherwise.
        """
        ...
