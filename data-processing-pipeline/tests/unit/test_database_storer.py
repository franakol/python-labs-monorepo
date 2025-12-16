"""Unit tests for DatabaseStorer stage.

Tests the database storage functionality using mocks for the database connection.
These tests are written BEFORE the implementation (TDD RED phase).
"""

from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from pipeline.exceptions import StorageError
from pipeline.implementations.database_storer import DatabaseStorer
from pipeline.models import AnalyzedText, ProcessedResult, Sentiment


class TestDatabaseStorer:
    """Tests for the DatabaseStorer implementation."""

    @pytest.fixture
    def mock_connection(self) -> MagicMock:
        """Create a mock database connection."""
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value.__enter__ = MagicMock(return_value=cursor)
        conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        cursor.fetchone.return_value = (1,)  # Return an ID
        return conn

    @pytest.fixture
    def storer(self, mock_connection: MagicMock) -> DatabaseStorer:
        """Create a DatabaseStorer instance with mock connection."""
        return DatabaseStorer(connection=mock_connection)

    @pytest.fixture
    def sample_analyzed_text(self) -> AnalyzedText:
        """Create a sample AnalyzedText for testing."""
        return AnalyzedText(
            content="This is a positive message",
            sentiment=Sentiment.POSITIVE,
            sentiment_score=0.8,
            trace_id=uuid4(),
            confidence=0.9,
        )

    def test_storer_has_correct_name(self, storer: DatabaseStorer) -> None:
        """Test that storer has the expected stage name."""
        assert storer.name == "DatabaseStorer"

    def test_process_returns_processed_result(
        self, storer: DatabaseStorer, sample_analyzed_text: AnalyzedText
    ) -> None:
        """Test that process returns a ProcessedResult object."""
        result = storer.process(sample_analyzed_text)
        assert isinstance(result, ProcessedResult)

    def test_preserves_trace_id(
        self, storer: DatabaseStorer, sample_analyzed_text: AnalyzedText
    ) -> None:
        """Test that the trace_id is carried through from input."""
        result = storer.process(sample_analyzed_text)
        assert result.trace_id == sample_analyzed_text.trace_id

    def test_preserves_content(
        self, storer: DatabaseStorer, sample_analyzed_text: AnalyzedText
    ) -> None:
        """Test that content is preserved in output."""
        result = storer.process(sample_analyzed_text)
        assert result.cleaned_content == sample_analyzed_text.content

    def test_preserves_sentiment(
        self, storer: DatabaseStorer, sample_analyzed_text: AnalyzedText
    ) -> None:
        """Test that sentiment data is preserved."""
        result = storer.process(sample_analyzed_text)
        assert result.sentiment == sample_analyzed_text.sentiment
        assert result.sentiment_score == sample_analyzed_text.sentiment_score

    def test_result_has_processed_at_timestamp(
        self, storer: DatabaseStorer, sample_analyzed_text: AnalyzedText
    ) -> None:
        """Test that result has a processed_at timestamp."""
        result = storer.process(sample_analyzed_text)
        assert isinstance(result.processed_at, datetime)

    def test_result_has_database_id(
        self, storer: DatabaseStorer, sample_analyzed_text: AnalyzedText
    ) -> None:
        """Test that result has an ID after storage."""
        result = storer.process(sample_analyzed_text)
        assert result.id is not None

    # Database interaction tests
    def test_executes_insert_query(
        self,
        storer: DatabaseStorer,
        mock_connection: MagicMock,
        sample_analyzed_text: AnalyzedText,
    ) -> None:
        """Test that an INSERT query is executed."""
        storer.process(sample_analyzed_text)

        cursor = mock_connection.cursor.return_value.__enter__.return_value
        cursor.execute.assert_called_once()

        # Check that the call contains INSERT
        call_args = cursor.execute.call_args
        assert "INSERT" in call_args[0][0].upper()

    def test_commits_transaction(
        self,
        storer: DatabaseStorer,
        mock_connection: MagicMock,
        sample_analyzed_text: AnalyzedText,
    ) -> None:
        """Test that the transaction is committed."""
        storer.process(sample_analyzed_text)
        mock_connection.commit.assert_called_once()

    # Error handling tests
    def test_raises_storage_error_on_db_error(
        self, mock_connection: MagicMock
    ) -> None:
        """Test that StorageError is raised on database errors."""
        mock_connection.cursor.return_value.__enter__.return_value.execute.side_effect = (
            Exception("DB Error")
        )
        storer = DatabaseStorer(connection=mock_connection)

        analyzed = AnalyzedText(
            content="test",
            sentiment=Sentiment.NEUTRAL,
            sentiment_score=0.0,
            trace_id=uuid4(),
        )

        with pytest.raises(StorageError):
            storer.process(analyzed)

    def test_raises_storage_error_for_none_content(
        self, storer: DatabaseStorer
    ) -> None:
        """Test that StorageError is raised for invalid input."""
        invalid_text = AnalyzedText(
            content="valid",
            sentiment=Sentiment.NEUTRAL,
            sentiment_score=0.0,
            trace_id=uuid4(),
        )
        invalid_text.content = None  # type: ignore[assignment]

        with pytest.raises(StorageError):
            storer.process(invalid_text)

    def test_rollback_on_error(
        self, mock_connection: MagicMock
    ) -> None:
        """Test that rollback is called on database errors."""
        mock_connection.cursor.return_value.__enter__.return_value.execute.side_effect = (
            Exception("DB Error")
        )
        storer = DatabaseStorer(connection=mock_connection)

        analyzed = AnalyzedText(
            content="test",
            sentiment=Sentiment.NEUTRAL,
            sentiment_score=0.0,
            trace_id=uuid4(),
        )

        with pytest.raises(StorageError):
            storer.process(analyzed)

        mock_connection.rollback.assert_called_once()
