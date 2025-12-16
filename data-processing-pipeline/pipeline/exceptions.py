"""Custom exceptions for the data processing pipeline.

Each pipeline stage has its own exception type to enable precise error handling
and debugging of multi-stage data flows.
"""


class PipelineError(Exception):
    """Base exception for all pipeline errors.

    All custom exceptions in the pipeline inherit from this class,
    allowing callers to catch any pipeline-related error.
    """

    pass


class CleaningError(PipelineError):
    """Raised when text cleaning fails.

    Attributes:
        message: Description of the cleaning failure.
        original_text: The text that failed to be cleaned.
    """

    def __init__(self, message: str, original_text: str | None = None) -> None:
        """Initialize the cleaning error.

        Args:
            message: Description of what went wrong during cleaning.
            original_text: The text that could not be cleaned.
        """
        self.message = message
        self.original_text = original_text
        super().__init__(f"Cleaning error: {message}")


class AnalysisError(PipelineError):
    """Raised when sentiment analysis fails.

    Attributes:
        message: Description of the analysis failure.
        text: The text that failed analysis.
    """

    def __init__(self, message: str, text: str | None = None) -> None:
        """Initialize the analysis error.

        Args:
            message: Description of what went wrong during analysis.
            text: The text that could not be analyzed.
        """
        self.message = message
        self.text = text
        super().__init__(f"Analysis error: {message}")


class StorageError(PipelineError):
    """Raised when database storage fails.

    Attributes:
        message: Description of the storage failure.
        data: The data that failed to be stored.
    """

    def __init__(self, message: str, data: object | None = None) -> None:
        """Initialize the storage error.

        Args:
            message: Description of what went wrong during storage.
            data: The data that could not be stored.
        """
        self.message = message
        self.data = data
        super().__init__(f"Storage error: {message}")
