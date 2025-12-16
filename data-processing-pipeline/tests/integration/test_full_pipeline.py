"""Integration tests for the full data processing pipeline.

Uses testcontainers-python to spin up a real PostgreSQL container
for end-to-end testing of the complete pipeline flow.
"""

import psycopg2
import pytest

from pipeline.implementations.database_storer import DatabaseStorer
from pipeline.implementations.sentiment_analyzer import SentimentAnalyzer
from pipeline.implementations.text_cleaner import TextCleaner
from pipeline.models import ProcessedResult, RawText, Sentiment
from pipeline.pipeline import DataPipeline

# Try to import testcontainers, skip tests if not available
try:
    from testcontainers.postgres import PostgresContainer

    TESTCONTAINERS_AVAILABLE = True
except ImportError:
    TESTCONTAINERS_AVAILABLE = False


# SQL for creating the results table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS processed_results (
    id SERIAL PRIMARY KEY,
    original_content TEXT NOT NULL,
    cleaned_content TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    sentiment_score FLOAT NOT NULL,
    trace_id VARCHAR(36) NOT NULL,
    processed_at TIMESTAMP NOT NULL,
    source VARCHAR(255),
    metadata JSONB DEFAULT '{}'
);
"""


@pytest.mark.integration
@pytest.mark.skipif(
    not TESTCONTAINERS_AVAILABLE,
    reason="testcontainers not installed or Docker not running"
)
class TestFullPipelineIntegration:
    """Integration tests for the complete data processing pipeline."""

    @pytest.fixture(scope="class")
    def postgres_container(self):
        """Start a PostgreSQL container for the test class."""
        with PostgresContainer("postgres:15-alpine") as postgres:
            yield postgres

    @pytest.fixture
    def db_connection(self, postgres_container):
        """Create a database connection and set up the schema."""
        connection = psycopg2.connect(
            host=postgres_container.get_container_host_ip(),
            port=postgres_container.get_exposed_port(5432),
            user=postgres_container.username,
            password=postgres_container.password,
            database=postgres_container.dbname,
        )

        # Create the results table
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
        connection.commit()

        yield connection

        connection.close()

    @pytest.fixture
    def full_pipeline(self, db_connection) -> DataPipeline:
        """Create a complete pipeline with all stages."""
        stages = [
            TextCleaner(),
            SentimentAnalyzer(),
            DatabaseStorer(connection=db_connection),
        ]
        return DataPipeline(stages)

    def test_pipeline_processes_positive_text(
        self, full_pipeline: DataPipeline, db_connection
    ) -> None:
        """Test processing positive text through the full pipeline."""
        raw_input = RawText(
            content="  <p>This product is absolutely wonderful and amazing!</p>  ",
            source="test",
        )

        result = full_pipeline.run(raw_input)

        # Verify the result
        assert isinstance(result, ProcessedResult)
        assert result.sentiment == Sentiment.POSITIVE
        assert result.sentiment_score > 0
        assert result.id is not None

        # Verify it was stored in the database
        with db_connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM processed_results WHERE id = %s",
                (result.id,)
            )
            row = cursor.fetchone()
            assert row is not None
            assert row[3] == "positive"  # sentiment column

    def test_pipeline_processes_negative_text(
        self, full_pipeline: DataPipeline, db_connection
    ) -> None:
        """Test processing negative text through the full pipeline."""
        raw_input = RawText(
            content="This is terrible and horrible, the worst experience ever.",
            source="test",
        )

        result = full_pipeline.run(raw_input)

        assert result.sentiment == Sentiment.NEGATIVE
        assert result.sentiment_score < 0
        assert result.id is not None

    def test_pipeline_processes_neutral_text(
        self, full_pipeline: DataPipeline, db_connection
    ) -> None:
        """Test processing neutral text through the full pipeline."""
        raw_input = RawText(
            content="The meeting is scheduled for tomorrow at 3pm.",
            source="test",
        )

        result = full_pipeline.run(raw_input)

        assert result.sentiment == Sentiment.NEUTRAL
        assert result.id is not None

    def test_pipeline_cleans_html_tags(
        self, full_pipeline: DataPipeline, db_connection
    ) -> None:
        """Test that HTML tags are cleaned before analysis."""
        raw_input = RawText(
            content='<div class="main"><p>Simple text</p></div>',
            source="test",
        )

        result = full_pipeline.run(raw_input)

        # Cleaned content should not have HTML tags
        assert "<div" not in result.cleaned_content
        assert "<p>" not in result.cleaned_content
        assert "Simple text" in result.cleaned_content

    def test_pipeline_preserves_trace_id(
        self, full_pipeline: DataPipeline, db_connection
    ) -> None:
        """Test that trace_id is preserved through all stages."""
        raw_input = RawText(
            content="Test content for tracing",
            source="test",
        )

        result = full_pipeline.run(raw_input)

        assert result.trace_id == raw_input.trace_id

    def test_multiple_items_processed(
        self, full_pipeline: DataPipeline, db_connection
    ) -> None:
        """Test processing multiple items through the pipeline."""
        inputs = [
            RawText(content="Great product!", source="test1"),
            RawText(content="Terrible service.", source="test2"),
            RawText(content="Normal day.", source="test3"),
        ]

        results = [full_pipeline.run(inp) for inp in inputs]

        # All should have IDs
        assert all(r.id is not None for r in results)

        # Count in database
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM processed_results")
            count = cursor.fetchone()[0]
            assert count >= 3
