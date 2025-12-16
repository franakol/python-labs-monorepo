"""Abstract interfaces for pipeline stages.

Defines the contracts that all pipeline stage implementations must follow,
enabling dependency injection and testability.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

# Type variables for input and output types
InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class PipelineStage(ABC, Generic[InputT, OutputT]):
    """Abstract base class for all pipeline stages.

    Each stage in the pipeline transforms data from one type to another.
    Implementations must define the process method.

    Type Parameters:
        InputT: The type of data this stage accepts.
        OutputT: The type of data this stage produces.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this pipeline stage.

        Returns:
            A human-readable name for logging and debugging.
        """
        pass

    @abstractmethod
    def process(self, data: InputT) -> OutputT:
        """Process input data and return transformed output.

        Args:
            data: The input data to process.

        Returns:
            The transformed data.

        Raises:
            PipelineError: If processing fails.
        """
        pass


class TextCleanerInterface(PipelineStage[Any, Any], ABC):
    """Interface for text cleaning stages.

    Implementations clean and normalize raw text for further processing.
    """

    @property
    def name(self) -> str:
        """Return the stage name."""
        return "TextCleaner"


class SentimentAnalyzerInterface(PipelineStage[Any, Any], ABC):
    """Interface for sentiment analysis stages.

    Implementations analyze text and assign sentiment scores.
    """

    @property
    def name(self) -> str:
        """Return the stage name."""
        return "SentimentAnalyzer"


class DatabaseStorerInterface(PipelineStage[Any, Any], ABC):
    """Interface for database storage stages.

    Implementations persist processed results to a database.
    """

    @property
    def name(self) -> str:
        """Return the stage name."""
        return "DatabaseStorer"
