"""Database storage pipeline stage.

This module provides the DatabaseStorer implementation that
persists processed results to a PostgreSQL database.
"""

import logging
from datetime import datetime
from typing import Any, Protocol

from pipeline.exceptions import StorageError
from pipeline.interfaces.stages import DatabaseStorerInterface
from pipeline.models import AnalyzedText, ProcessedResult

logger = logging.getLogger(__name__)


class DatabaseConnection(Protocol):
    """Protocol for database connections.

    Defines the interface expected from database connection objects.
    """

    def cursor(self) -> Any:
        """Create a cursor for executing queries."""
        ...

    def commit(self) -> None:
        """Commit the current transaction."""
        ...

    def rollback(self) -> None:
        """Rollback the current transaction."""
        ...


class DatabaseStorer(DatabaseStorerInterface):
    """Implementation of database storage stage.

    Persists processed results to a PostgreSQL database using
    the provided connection.
    """

    # SQL for inserting results
    _INSERT_SQL = """
        INSERT INTO processed_results (
            original_content, cleaned_content, sentiment, sentiment_score,
            trace_id, processed_at, source, metadata
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """

    def __init__(self, connection: DatabaseConnection) -> None:
        """Initialize the storer with a database connection.

        Args:
            connection: Database connection object (e.g., psycopg2 connection).
        """
        self._connection = connection

    @property
    def name(self) -> str:
        """Return the stage name."""
        return "DatabaseStorer"

    def process(self, data: AnalyzedText) -> ProcessedResult:
        """Store analyzed text in the database.

        Args:
            data: The analyzed text to store.

        Returns:
            ProcessedResult with database ID.

        Raises:
            StorageError: If storage fails.
        """
        logger.info(f"[{data.trace_id}] Starting database storage")

        # Validate input
        if data.content is None:
            logger.error(f"[{data.trace_id}] Content is None")
            raise StorageError("Content cannot be None", data=None)

        processed_at = datetime.now()

        try:
            # Create processed result
            result = ProcessedResult(
                original_content=data.content,  # In full pipeline, would come from earlier stage
                cleaned_content=data.content,
                sentiment=data.sentiment,
                sentiment_score=data.sentiment_score,
                trace_id=data.trace_id,
                processed_at=processed_at,
            )

            # Insert into database
            result_id = self._insert_result(result)
            result.id = result_id

            logger.info(f"[{data.trace_id}] Stored result with id={result_id}")

            return result

        except StorageError:
            raise
        except Exception as e:
            logger.error(f"[{data.trace_id}] Database error: {e}")
            self._connection.rollback()
            raise StorageError(f"Failed to store result: {e}", data=data)

    def _insert_result(self, result: ProcessedResult) -> int:
        """Insert a result into the database.

        Args:
            result: The result to insert.

        Returns:
            The generated database ID.
        """
        import json

        with self._connection.cursor() as cursor:
            cursor.execute(
                self._INSERT_SQL,
                (
                    result.original_content,
                    result.cleaned_content,
                    result.sentiment.value,
                    result.sentiment_score,
                    str(result.trace_id),
                    result.processed_at,
                    result.source,
                    json.dumps(result.metadata),
                ),
            )

            row = cursor.fetchone()
            result_id: int = row[0]

        self._connection.commit()

        return result_id
