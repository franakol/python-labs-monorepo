"""Sentiment analysis pipeline stage.

This module provides the SentimentAnalyzer implementation that
analyzes text sentiment using a keyword-based approach (simulated).
"""

import logging
from collections.abc import Set

from pipeline.exceptions import AnalysisError
from pipeline.interfaces.stages import SentimentAnalyzerInterface
from pipeline.models import AnalyzedText, CleanedText, Sentiment

logger = logging.getLogger(__name__)


class SentimentAnalyzer(SentimentAnalyzerInterface):
    """Implementation of sentiment analysis stage.

    Uses a simple keyword-based approach to determine sentiment.
    This is a simulated implementation for demonstration purposes.
    """

    # Positive words for sentiment detection
    _POSITIVE_WORDS: Set[str] = frozenset(
        [
            "good",
            "great",
            "excellent",
            "wonderful",
            "amazing",
            "fantastic",
            "love",
            "best",
            "happy",
            "positive",
            "beautiful",
            "brilliant",
            "outstanding",
            "perfect",
            "awesome",
            "delightful",
            "pleasant",
            "superb",
            "marvelous",
            "terrific",
        ]
    )

    # Negative words for sentiment detection
    _NEGATIVE_WORDS: Set[str] = frozenset(
        [
            "bad",
            "terrible",
            "awful",
            "horrible",
            "worst",
            "hate",
            "poor",
            "negative",
            "disappointing",
            "sad",
            "ugly",
            "dreadful",
            "disgusting",
            "pathetic",
            "miserable",
            "annoying",
            "frustrating",
            "useless",
            "boring",
            "mediocre",
        ]
    )

    # Thresholds for classification
    _POSITIVE_THRESHOLD = 0.1
    _NEGATIVE_THRESHOLD = -0.1

    @property
    def name(self) -> str:
        """Return the stage name."""
        return "SentimentAnalyzer"

    def process(self, data: CleanedText) -> AnalyzedText:
        """Analyze sentiment of cleaned text.

        Args:
            data: The cleaned text to analyze.

        Returns:
            AnalyzedText with sentiment score and classification.

        Raises:
            AnalysisError: If the input content is invalid.
        """
        logger.info(f"[{data.trace_id}] Starting sentiment analysis")

        # Validate input
        if data.content is None:
            logger.error(f"[{data.trace_id}] Content is None")
            raise AnalysisError("Content cannot be None", text=None)

        # Handle empty content
        if not data.content.strip():
            logger.info(f"[{data.trace_id}] Empty content, returning neutral")
            return AnalyzedText(
                content=data.content,
                sentiment=Sentiment.NEUTRAL,
                sentiment_score=0.0,
                trace_id=data.trace_id,
                confidence=1.0,
            )

        # Calculate sentiment score
        score, confidence = self._calculate_sentiment(data.content)

        # Classify sentiment
        sentiment = self._classify_sentiment(score)

        logger.info(
            f"[{data.trace_id}] Sentiment analysis complete: "
            f"score={score:.3f}, sentiment={sentiment.value}, confidence={confidence:.3f}"
        )

        return AnalyzedText(
            content=data.content,
            sentiment=sentiment,
            sentiment_score=score,
            trace_id=data.trace_id,
            confidence=confidence,
        )

    def _calculate_sentiment(self, text: str) -> tuple[float, float]:
        """Calculate sentiment score from text.

        Uses keyword counting to determine sentiment.

        Args:
            text: The text to analyze.

        Returns:
            Tuple of (sentiment_score, confidence).
            Score is between -1.0 and 1.0.
            Confidence is between 0.0 and 1.0.
        """
        words = text.lower().split()

        if not words:
            return 0.0, 1.0

        positive_count = sum(1 for word in words if word in self._POSITIVE_WORDS)
        negative_count = sum(1 for word in words if word in self._NEGATIVE_WORDS)

        total_sentiment_words = positive_count + negative_count

        # Calculate raw score
        if total_sentiment_words == 0:
            # No sentiment words found, neutral
            return 0.0, 0.5  # Lower confidence when no keywords found

        # Score based on ratio of positive to negative
        raw_score = (positive_count - negative_count) / total_sentiment_words

        # Confidence based on how many sentiment words were found
        # More words = higher confidence
        confidence = min(1.0, total_sentiment_words / 5)

        logger.debug(
            f"Sentiment calculation: +{positive_count}/-{negative_count}, "
            f"score={raw_score:.3f}, confidence={confidence:.3f}"
        )

        return raw_score, confidence

    def _classify_sentiment(self, score: float) -> Sentiment:
        """Classify sentiment based on score.

        Args:
            score: The sentiment score (-1.0 to 1.0).

        Returns:
            Sentiment classification enum.
        """
        if score > self._POSITIVE_THRESHOLD:
            return Sentiment.POSITIVE
        elif score < self._NEGATIVE_THRESHOLD:
            return Sentiment.NEGATIVE
        else:
            return Sentiment.NEUTRAL
