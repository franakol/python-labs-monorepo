"""Text cleaning pipeline stage.

This module provides the TextCleaner implementation that normalizes
and cleans raw text for further processing.
"""

import html
import logging
import re
import unicodedata

from pipeline.exceptions import CleaningError
from pipeline.interfaces.stages import TextCleanerInterface
from pipeline.models import CleanedText, RawText

logger = logging.getLogger(__name__)


class TextCleaner(TextCleanerInterface):
    """Implementation of text cleaning stage.

    Cleans and normalizes raw text by:
    - Removing leading/trailing whitespace
    - Normalizing internal whitespace
    - Removing HTML tags
    - Normalizing unicode characters
    """

    # Regex pattern for HTML tags
    _HTML_TAG_PATTERN = re.compile(r"<[^>]+>")

    # Regex pattern for multiple whitespace
    _WHITESPACE_PATTERN = re.compile(r"\s+")

    # Zero-width characters to remove
    _ZERO_WIDTH_CHARS = frozenset(
        [
            "\u200b",  # zero-width space
            "\u200c",  # zero-width non-joiner
            "\u200d",  # zero-width joiner
            "\ufeff",  # byte order mark
        ]
    )

    @property
    def name(self) -> str:
        """Return the stage name."""
        return "TextCleaner"

    def process(self, data: RawText) -> CleanedText:
        """Process raw text and return cleaned text.

        Args:
            data: The raw text input to clean.

        Returns:
            CleanedText with normalized content.

        Raises:
            CleaningError: If the input content is invalid.
        """
        logger.info(f"[{data.trace_id}] Starting text cleaning")

        # Validate input
        if data.content is None:
            logger.error(f"[{data.trace_id}] Content is None")
            raise CleaningError("Content cannot be None", original_text=None)

        operations: list[str] = []
        content = data.content
        original = content

        # Step 1: Normalize unicode (NFKC form)
        content = self._normalize_unicode(content)
        operations.append("unicode_normalization")
        logger.debug(f"[{data.trace_id}] After unicode normalization: {content[:50]}...")

        # Step 2: Remove zero-width characters
        content = self._remove_zero_width_chars(content)
        operations.append("zero_width_removal")

        # Step 3: Remove HTML tags
        content = self._strip_html(content)
        operations.append("html_stripping")
        logger.debug(f"[{data.trace_id}] After HTML stripping: {content[:50]}...")

        # Step 4: Normalize whitespace
        content = self._normalize_whitespace(content)
        operations.append("whitespace_normalization")
        logger.debug(f"[{data.trace_id}] After whitespace normalization: {content[:50]}...")

        logger.info(f"[{data.trace_id}] Cleaning complete. Operations: {operations}")

        return CleanedText(
            content=content,
            original_content=original,
            trace_id=data.trace_id,
            cleaning_operations=operations,
        )

    def _normalize_unicode(self, text: str) -> str:
        """Normalize unicode to NFKC form.

        Args:
            text: The text to normalize.

        Returns:
            Unicode-normalized text.
        """
        return unicodedata.normalize("NFKC", text)

    def _remove_zero_width_chars(self, text: str) -> str:
        """Remove zero-width unicode characters.

        Args:
            text: The text to clean.

        Returns:
            Text with zero-width characters removed.
        """
        for char in self._ZERO_WIDTH_CHARS:
            text = text.replace(char, "")
        return text

    def _strip_html(self, text: str) -> str:
        """Remove HTML tags from text.

        Args:
            text: The text containing HTML.

        Returns:
            Text with HTML tags stripped.
        """
        # Remove HTML tags
        text = self._HTML_TAG_PATTERN.sub("", text)
        # Unescape HTML entities
        text = html.unescape(text)
        return text

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text.

        - Convert tabs and newlines to spaces
        - Collapse multiple spaces to single space
        - Strip leading/trailing whitespace

        Args:
            text: The text to normalize.

        Returns:
            Whitespace-normalized text.
        """
        # Replace all whitespace with single space
        text = self._WHITESPACE_PATTERN.sub(" ", text)
        # Strip leading/trailing
        text = text.strip()
        return text
