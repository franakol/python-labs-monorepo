"""Configuration file parsers.

This module provides concrete implementations of ConfigParserInterface
for JSON and YAML configuration file formats.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml

from gitconfig.exceptions import ParseError
from gitconfig.interfaces.parser import ConfigParserInterface
from gitconfig.models import ConfigFormat

logger = logging.getLogger(__name__)


class JsonParser(ConfigParserInterface):
    """JSON configuration file parser.

    Handles parsing and serializing JSON configuration files.
    """

    @property
    def format(self) -> ConfigFormat:
        """Return the configuration format this parser handles."""
        return ConfigFormat.JSON

    @property
    def file_extension(self) -> str:
        """Return the file extension for this format (without dot)."""
        return "json"

    def parse(self, content: str) -> dict[str, Any]:
        """Parse JSON content into a dictionary.

        Args:
            content: Raw JSON string content to parse.

        Returns:
            Parsed configuration as a dictionary.

        Raises:
            ParseError: If the content cannot be parsed as JSON.
        """
        try:
            result = json.loads(content)
            if not isinstance(result, dict):
                raise ParseError(
                    Path("<string>"),
                    "json",
                    "Expected JSON object at root level",
                )
            return result
        except json.JSONDecodeError as e:
            raise ParseError(Path("<string>"), "json", str(e)) from e

    def serialize(self, data: dict[str, Any]) -> str:
        """Serialize a dictionary to JSON format.

        Args:
            data: Dictionary to serialize.

        Returns:
            Serialized JSON content as a string.
        """
        return json.dumps(data, indent=2, sort_keys=True)

    def validate(self, content: str) -> bool:
        """Validate that content is valid JSON.

        Args:
            content: Raw string content to validate.

        Returns:
            True if the content is valid JSON, False otherwise.
        """
        try:
            json.loads(content)
            return True
        except json.JSONDecodeError:
            return False


class YamlParser(ConfigParserInterface):
    """YAML configuration file parser.

    Handles parsing and serializing YAML configuration files.
    Uses safe_load/safe_dump to prevent arbitrary code execution.
    """

    @property
    def format(self) -> ConfigFormat:
        """Return the configuration format this parser handles."""
        return ConfigFormat.YAML

    @property
    def file_extension(self) -> str:
        """Return the file extension for this format (without dot)."""
        return "yaml"

    def parse(self, content: str) -> dict[str, Any]:
        """Parse YAML content into a dictionary.

        Args:
            content: Raw YAML string content to parse.

        Returns:
            Parsed configuration as a dictionary.

        Raises:
            ParseError: If the content cannot be parsed as YAML.
        """
        try:
            result = yaml.safe_load(content)
            if result is None:
                return {}
            if not isinstance(result, dict):
                raise ParseError(
                    Path("<string>"),
                    "yaml",
                    "Expected YAML mapping at root level",
                )
            return result
        except yaml.YAMLError as e:
            raise ParseError(Path("<string>"), "yaml", str(e)) from e

    def serialize(self, data: dict[str, Any]) -> str:
        """Serialize a dictionary to YAML format.

        Args:
            data: Dictionary to serialize.

        Returns:
            Serialized YAML content as a string.
        """
        return yaml.safe_dump(data, default_flow_style=False, sort_keys=True)

    def validate(self, content: str) -> bool:
        """Validate that content is valid YAML.

        Args:
            content: Raw string content to validate.

        Returns:
            True if the content is valid YAML, False otherwise.
        """
        try:
            yaml.safe_load(content)
            return True
        except yaml.YAMLError:
            return False
