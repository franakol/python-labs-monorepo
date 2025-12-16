"""Data models for the processing pipeline.

These dataclasses represent data at different stages of the pipeline,
providing type safety and clear documentation of data flow.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class Sentiment(Enum):
    """Sentiment classification categories."""

    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"


@dataclass
class RawText:
    """Input data for the pipeline.

    Attributes:
        content: The raw text content to process.
        source: Optional identifier for where the text came from.
        trace_id: Unique ID for tracing this data through the pipeline.
        metadata: Additional metadata about the text.
        created_at: Timestamp when the data was created.
    """

    content: str
    source: str | None = None
    trace_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CleanedText:
    """Text after cleaning stage.

    Attributes:
        content: The cleaned text content.
        original_content: The original text before cleaning.
        trace_id: Unique ID carried from the input.
        cleaning_operations: List of operations performed during cleaning.
    """

    content: str
    original_content: str
    trace_id: UUID
    cleaning_operations: list[str] = field(default_factory=list)


@dataclass
class AnalyzedText:
    """Text after sentiment analysis stage.

    Attributes:
        content: The text content that was analyzed.
        sentiment: The classified sentiment category.
        sentiment_score: Numerical score from -1.0 (negative) to 1.0 (positive).
        trace_id: Unique ID carried from previous stages.
        confidence: Confidence level of the analysis (0.0 to 1.0).
    """

    content: str
    sentiment: Sentiment
    sentiment_score: float
    trace_id: UUID
    confidence: float = 1.0


@dataclass
class ProcessedResult:
    """Final result ready for storage.

    Attributes:
        id: Unique identifier for the result.
        original_content: The original input text.
        cleaned_content: The text after cleaning.
        sentiment: The classified sentiment.
        sentiment_score: Numerical sentiment score.
        trace_id: Unique ID for full pipeline tracing.
        processed_at: Timestamp when processing completed.
        source: Optional source identifier.
        metadata: Additional metadata.
    """

    original_content: str
    cleaned_content: str
    sentiment: Sentiment
    sentiment_score: float
    trace_id: UUID
    processed_at: datetime = field(default_factory=datetime.now)
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    id: int | None = None
