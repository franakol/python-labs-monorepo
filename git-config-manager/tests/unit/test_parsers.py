"""Unit tests for ConfigParser implementations.

Tests follow TDD - written first for JSON and YAML parsers.
"""

import pytest

from gitconfig.core.parsers import JsonParser, YamlParser
from gitconfig.exceptions import ParseError
from gitconfig.models import ConfigFormat


class TestJsonParser:
    """Tests for the JSON parser implementation."""

    def test_format_is_json(self) -> None:
        """Test that format property returns JSON."""
        parser = JsonParser()
        assert parser.format == ConfigFormat.JSON

    def test_file_extension_is_json(self) -> None:
        """Test that file_extension returns 'json'."""
        parser = JsonParser()
        assert parser.file_extension == "json"

    def test_parse_valid_json(self) -> None:
        """Test parsing valid JSON content."""
        parser = JsonParser()
        content = '{"name": "test", "value": 123}'

        result = parser.parse(content)

        assert result == {"name": "test", "value": 123}

    def test_parse_nested_json(self) -> None:
        """Test parsing nested JSON content."""
        parser = JsonParser()
        content = '{"database": {"host": "localhost", "port": 5432}}'

        result = parser.parse(content)

        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 5432

    def test_parse_json_with_arrays(self) -> None:
        """Test parsing JSON with arrays."""
        parser = JsonParser()
        content = '{"items": [1, 2, 3], "names": ["a", "b"]}'

        result = parser.parse(content)

        assert result["items"] == [1, 2, 3]
        assert result["names"] == ["a", "b"]

    def test_parse_invalid_json_raises_error(self) -> None:
        """Test that invalid JSON raises ParseError."""
        parser = JsonParser()
        content = '{"name": "unclosed string}'

        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "json" in str(exc_info.value).lower()

    def test_serialize_dict_to_json(self) -> None:
        """Test serializing a dict to JSON string."""
        parser = JsonParser()
        data = {"name": "test", "value": 123}

        result = parser.serialize(data)

        assert '"name"' in result
        assert '"test"' in result
        assert "123" in result

    def test_serialize_produces_valid_json(self) -> None:
        """Test that serialized output can be parsed back."""
        parser = JsonParser()
        data = {"nested": {"key": "value"}, "list": [1, 2, 3]}

        serialized = parser.serialize(data)
        parsed = parser.parse(serialized)

        assert parsed == data

    def test_validate_valid_json_returns_true(self) -> None:
        """Test that validate returns True for valid JSON."""
        parser = JsonParser()
        content = '{"key": "value"}'

        assert parser.validate(content) is True

    def test_validate_invalid_json_returns_false(self) -> None:
        """Test that validate returns False for invalid JSON."""
        parser = JsonParser()
        content = "{invalid json"

        assert parser.validate(content) is False


class TestYamlParser:
    """Tests for the YAML parser implementation."""

    def test_format_is_yaml(self) -> None:
        """Test that format property returns YAML."""
        parser = YamlParser()
        assert parser.format == ConfigFormat.YAML

    def test_file_extension_is_yaml(self) -> None:
        """Test that file_extension returns 'yaml'."""
        parser = YamlParser()
        assert parser.file_extension == "yaml"

    def test_parse_valid_yaml(self) -> None:
        """Test parsing valid YAML content."""
        parser = YamlParser()
        content = """
name: test
value: 123
"""
        result = parser.parse(content)

        assert result == {"name": "test", "value": 123}

    def test_parse_nested_yaml(self) -> None:
        """Test parsing nested YAML content."""
        parser = YamlParser()
        content = """
database:
  host: localhost
  port: 5432
"""
        result = parser.parse(content)

        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 5432

    def test_parse_yaml_with_lists(self) -> None:
        """Test parsing YAML with lists."""
        parser = YamlParser()
        content = """
items:
  - 1
  - 2
  - 3
names:
  - a
  - b
"""
        result = parser.parse(content)

        assert result["items"] == [1, 2, 3]
        assert result["names"] == ["a", "b"]

    def test_parse_invalid_yaml_raises_error(self) -> None:
        """Test that invalid YAML raises ParseError."""
        parser = YamlParser()
        content = """
invalid:
  - item1
    broken: indentation
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "yaml" in str(exc_info.value).lower()

    def test_serialize_dict_to_yaml(self) -> None:
        """Test serializing a dict to YAML string."""
        parser = YamlParser()
        data = {"name": "test", "value": 123}

        result = parser.serialize(data)

        assert "name:" in result
        assert "test" in result

    def test_serialize_produces_valid_yaml(self) -> None:
        """Test that serialized output can be parsed back."""
        parser = YamlParser()
        data = {"nested": {"key": "value"}, "items": [1, 2, 3]}

        serialized = parser.serialize(data)
        parsed = parser.parse(serialized)

        assert parsed == data

    def test_validate_valid_yaml_returns_true(self) -> None:
        """Test that validate returns True for valid YAML."""
        parser = YamlParser()
        content = "key: value\n"

        assert parser.validate(content) is True

    def test_validate_invalid_yaml_returns_false(self) -> None:
        """Test that validate returns False for invalid YAML."""
        parser = YamlParser()
        content = "key: [unclosed"

        assert parser.validate(content) is False
