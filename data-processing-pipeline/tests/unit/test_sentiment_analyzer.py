"""Unit tests for SentimentAnalyzer stage.

Tests the sentiment analysis functionality in isolation following TDD approach.
These tests are written BEFORE the implementation (RED phase).
"""

import pytest

from pipeline.exceptions import AnalysisError
from pipeline.implementations.sentiment_analyzer import SentimentAnalyzer
from pipeline.models import AnalyzedText, CleanedText, Sentiment
from uuid import uuid4


class TestSentimentAnalyzer:
    """Tests for the SentimentAnalyzer implementation."""

    @pytest.fixture
    def analyzer(self) -> SentimentAnalyzer:
        """Create a SentimentAnalyzer instance for testing."""
        return SentimentAnalyzer()

    @pytest.fixture
    def sample_cleaned_text(self) -> CleanedText:
        """Create a sample CleanedText for testing."""
        return CleanedText(
            content="This is sample text",
            original_content="This is sample text",
            trace_id=uuid4(),
            cleaning_operations=["whitespace_normalization"],
        )

    def test_analyzer_has_correct_name(self, analyzer: SentimentAnalyzer) -> None:
        """Test that analyzer has the expected stage name."""
        assert analyzer.name == "SentimentAnalyzer"

    def test_process_returns_analyzed_text(
        self, analyzer: SentimentAnalyzer, sample_cleaned_text: CleanedText
    ) -> None:
        """Test that process returns an AnalyzedText object."""
        result = analyzer.process(sample_cleaned_text)
        assert isinstance(result, AnalyzedText)

    def test_preserves_trace_id(
        self, analyzer: SentimentAnalyzer, sample_cleaned_text: CleanedText
    ) -> None:
        """Test that the trace_id is carried through from input."""
        result = analyzer.process(sample_cleaned_text)
        assert result.trace_id == sample_cleaned_text.trace_id

    def test_preserves_content(
        self, analyzer: SentimentAnalyzer, sample_cleaned_text: CleanedText
    ) -> None:
        """Test that content is preserved in output."""
        result = analyzer.process(sample_cleaned_text)
        assert result.content == sample_cleaned_text.content

    # Sentiment score tests
    def test_sentiment_score_in_valid_range(
        self, analyzer: SentimentAnalyzer, sample_cleaned_text: CleanedText
    ) -> None:
        """Test that sentiment score is between -1.0 and 1.0."""
        result = analyzer.process(sample_cleaned_text)
        assert -1.0 <= result.sentiment_score <= 1.0

    def test_positive_text_has_positive_score(
        self, analyzer: SentimentAnalyzer
    ) -> None:
        """Test that positive text gets a positive sentiment score."""
        positive_text = CleanedText(
            content="This is wonderful amazing fantastic excellent great",
            original_content="This is wonderful amazing fantastic excellent great",
            trace_id=uuid4(),
        )
        result = analyzer.process(positive_text)
        assert result.sentiment_score > 0
        assert result.sentiment == Sentiment.POSITIVE

    def test_negative_text_has_negative_score(
        self, analyzer: SentimentAnalyzer
    ) -> None:
        """Test that negative text gets a negative sentiment score."""
        negative_text = CleanedText(
            content="This is terrible awful horrible bad worst",
            original_content="This is terrible awful horrible bad worst",
            trace_id=uuid4(),
        )
        result = analyzer.process(negative_text)
        assert result.sentiment_score < 0
        assert result.sentiment == Sentiment.NEGATIVE

    def test_neutral_text_has_neutral_score(
        self, analyzer: SentimentAnalyzer
    ) -> None:
        """Test that neutral text gets a near-zero sentiment score."""
        neutral_text = CleanedText(
            content="The meeting is scheduled for tomorrow",
            original_content="The meeting is scheduled for tomorrow",
            trace_id=uuid4(),
        )
        result = analyzer.process(neutral_text)
        assert result.sentiment == Sentiment.NEUTRAL

    # Sentiment classification tests
    def test_positive_classification(self, analyzer: SentimentAnalyzer) -> None:
        """Test positive sentiment classification."""
        text = CleanedText(
            content="I love this product it is absolutely wonderful",
            original_content="I love this product it is absolutely wonderful",
            trace_id=uuid4(),
        )
        result = analyzer.process(text)
        assert result.sentiment == Sentiment.POSITIVE

    def test_negative_classification(self, analyzer: SentimentAnalyzer) -> None:
        """Test negative sentiment classification."""
        text = CleanedText(
            content="I hate this terrible service it is awful",
            original_content="I hate this terrible service it is awful",
            trace_id=uuid4(),
        )
        result = analyzer.process(text)
        assert result.sentiment == Sentiment.NEGATIVE

    def test_neutral_classification(self, analyzer: SentimentAnalyzer) -> None:
        """Test neutral sentiment classification."""
        text = CleanedText(
            content="The document contains information",
            original_content="The document contains information",
            trace_id=uuid4(),
        )
        result = analyzer.process(text)
        assert result.sentiment == Sentiment.NEUTRAL

    # Edge cases
    def test_empty_text_is_neutral(self, analyzer: SentimentAnalyzer) -> None:
        """Test that empty text is classified as neutral."""
        empty_text = CleanedText(
            content="",
            original_content="",
            trace_id=uuid4(),
        )
        result = analyzer.process(empty_text)
        assert result.sentiment == Sentiment.NEUTRAL
        assert result.sentiment_score == 0.0

    def test_mixed_sentiment_text(self, analyzer: SentimentAnalyzer) -> None:
        """Test text with mixed positive and negative words."""
        mixed_text = CleanedText(
            content="The good news is wonderful but the bad news is terrible",
            original_content="The good news is wonderful but the bad news is terrible",
            trace_id=uuid4(),
        )
        result = analyzer.process(mixed_text)
        # Score should be somewhere in between
        assert -1.0 <= result.sentiment_score <= 1.0

    def test_confidence_in_valid_range(
        self, analyzer: SentimentAnalyzer, sample_cleaned_text: CleanedText
    ) -> None:
        """Test that confidence score is between 0.0 and 1.0."""
        result = analyzer.process(sample_cleaned_text)
        assert 0.0 <= result.confidence <= 1.0

    # Error handling
    def test_raises_analysis_error_for_none_content(
        self, analyzer: SentimentAnalyzer
    ) -> None:
        """Test that AnalysisError is raised for invalid input."""
        invalid_text = CleanedText(
            content="valid",
            original_content="valid",
            trace_id=uuid4(),
        )
        invalid_text.content = None  # type: ignore[assignment]
        with pytest.raises(AnalysisError):
            analyzer.process(invalid_text)
