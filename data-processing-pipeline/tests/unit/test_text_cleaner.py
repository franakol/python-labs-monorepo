"""Unit tests for TextCleaner stage.

Tests the text cleaning functionality in isolation following TDD approach.
These tests are written BEFORE the implementation (RED phase).
"""

import pytest

from pipeline.exceptions import CleaningError
from pipeline.implementations.text_cleaner import TextCleaner
from pipeline.models import CleanedText, RawText


class TestTextCleaner:
    """Tests for the TextCleaner implementation."""

    @pytest.fixture
    def cleaner(self) -> TextCleaner:
        """Create a TextCleaner instance for testing."""
        return TextCleaner()

    def test_cleaner_has_correct_name(self, cleaner: TextCleaner) -> None:
        """Test that cleaner has the expected stage name."""
        assert cleaner.name == "TextCleaner"

    def test_process_returns_cleaned_text(self, cleaner: TextCleaner) -> None:
        """Test that process returns a CleanedText object."""
        raw = RawText(content="Hello world")
        result = cleaner.process(raw)
        assert isinstance(result, CleanedText)

    def test_preserves_trace_id(self, cleaner: TextCleaner) -> None:
        """Test that the trace_id is carried through from input."""
        raw = RawText(content="Test content")
        result = cleaner.process(raw)
        assert result.trace_id == raw.trace_id

    def test_stores_original_content(self, cleaner: TextCleaner) -> None:
        """Test that original content is preserved in output."""
        raw = RawText(content="  Original  content  ")
        result = cleaner.process(raw)
        assert result.original_content == "  Original  content  "

    # Whitespace normalization tests
    def test_removes_leading_whitespace(self, cleaner: TextCleaner) -> None:
        """Test that leading whitespace is removed."""
        raw = RawText(content="   Hello")
        result = cleaner.process(raw)
        assert result.content == "Hello"

    def test_removes_trailing_whitespace(self, cleaner: TextCleaner) -> None:
        """Test that trailing whitespace is removed."""
        raw = RawText(content="Hello   ")
        result = cleaner.process(raw)
        assert result.content == "Hello"

    def test_normalizes_internal_whitespace(self, cleaner: TextCleaner) -> None:
        """Test that multiple internal spaces are collapsed to single space."""
        raw = RawText(content="Hello    world")
        result = cleaner.process(raw)
        assert result.content == "Hello world"

    def test_normalizes_tabs_and_newlines(self, cleaner: TextCleaner) -> None:
        """Test that tabs and newlines are converted to spaces."""
        raw = RawText(content="Hello\tworld\ntest")
        result = cleaner.process(raw)
        assert result.content == "Hello world test"

    # HTML stripping tests
    def test_removes_html_tags(self, cleaner: TextCleaner) -> None:
        """Test that HTML tags are removed."""
        raw = RawText(content="<p>Hello</p> <b>world</b>")
        result = cleaner.process(raw)
        assert result.content == "Hello world"

    def test_removes_nested_html_tags(self, cleaner: TextCleaner) -> None:
        """Test that nested HTML tags are removed."""
        raw = RawText(content="<div><span>Hello</span></div>")
        result = cleaner.process(raw)
        assert result.content == "Hello"

    def test_removes_html_with_attributes(self, cleaner: TextCleaner) -> None:
        """Test that HTML tags with attributes are removed."""
        raw = RawText(content='<a href="url">Link</a>')
        result = cleaner.process(raw)
        assert result.content == "Link"

    # Unicode normalization tests
    def test_normalizes_unicode_characters(self, cleaner: TextCleaner) -> None:
        """Test that unicode is normalized (NFKC form)."""
        raw = RawText(content="café")  # combining acute accent
        result = cleaner.process(raw)
        assert result.content == "café"

    def test_removes_zero_width_characters(self, cleaner: TextCleaner) -> None:
        """Test that zero-width characters are removed."""
        raw = RawText(content="Hello\u200bworld")  # zero-width space
        result = cleaner.process(raw)
        assert result.content == "Hello world" or result.content == "Helloworld"

    # Special cases
    def test_handles_empty_string(self, cleaner: TextCleaner) -> None:
        """Test that empty strings are handled."""
        raw = RawText(content="")
        result = cleaner.process(raw)
        assert result.content == ""

    def test_handles_whitespace_only(self, cleaner: TextCleaner) -> None:
        """Test that whitespace-only strings become empty."""
        raw = RawText(content="   \t\n   ")
        result = cleaner.process(raw)
        assert result.content == ""

    def test_records_cleaning_operations(self, cleaner: TextCleaner) -> None:
        """Test that cleaning operations are logged."""
        raw = RawText(content="  <p>Hello</p>  ")
        result = cleaner.process(raw)
        assert len(result.cleaning_operations) > 0
        assert any("whitespace" in op.lower() for op in result.cleaning_operations)
        assert any("html" in op.lower() for op in result.cleaning_operations)

    # Error handling tests
    def test_raises_cleaning_error_for_none_content(
        self, cleaner: TextCleaner
    ) -> None:
        """Test that CleaningError is raised for invalid input."""
        # Create a RawText with None content (simulated by patching)
        raw = RawText(content="valid")
        raw.content = None  # type: ignore[assignment]
        with pytest.raises(CleaningError):
            cleaner.process(raw)
