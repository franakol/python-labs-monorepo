"""Unit tests for the Pipeline orchestrator.

Tests the pipeline coordination and stage chaining using mocked stages.
"""

from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from pipeline.exceptions import PipelineError
from pipeline.interfaces.stages import PipelineStage
from pipeline.models import ProcessedResult, RawText, Sentiment
from pipeline.pipeline import DataPipeline


class MockStage(PipelineStage[Any, Any]):
    """Mock pipeline stage for testing."""

    def __init__(self, name: str, output: Any) -> None:
        self._name = name
        self._output = output
        self.process_called = False
        self.process_input: Any = None

    @property
    def name(self) -> str:
        return self._name

    def process(self, data: Any) -> Any:
        self.process_called = True
        self.process_input = data
        return self._output


class TestDataPipeline:
    """Tests for the DataPipeline orchestrator."""

    @pytest.fixture
    def sample_raw_text(self) -> RawText:
        """Create sample input for testing."""
        return RawText(
            content="Test input content",
            source="test",
            trace_id=uuid4(),
        )

    @pytest.fixture
    def sample_processed_result(self) -> ProcessedResult:
        """Create sample final output."""
        return ProcessedResult(
            original_content="Test",
            cleaned_content="test",
            sentiment=Sentiment.NEUTRAL,
            sentiment_score=0.0,
            trace_id=uuid4(),
            id=1,
        )

    def test_pipeline_stores_stages(self) -> None:
        """Test that pipeline stores provided stages."""
        stages = [
            MockStage("stage1", "output1"),
            MockStage("stage2", "output2"),
        ]
        pipeline = DataPipeline(stages)
        assert len(pipeline.stages) == 2

    def test_run_executes_stages_in_order(
        self, sample_raw_text: RawText, sample_processed_result: ProcessedResult
    ) -> None:
        """Test that stages are executed in order."""
        stage1 = MockStage("stage1", "after_stage1")
        stage2 = MockStage("stage2", "after_stage2")
        stage3 = MockStage("stage3", sample_processed_result)

        pipeline = DataPipeline([stage1, stage2, stage3])
        pipeline.run(sample_raw_text)

        assert stage1.process_called
        assert stage2.process_called
        assert stage3.process_called

        # Check data flows through stages
        assert stage2.process_input == "after_stage1"
        assert stage3.process_input == "after_stage2"

    def test_run_returns_processed_result(
        self, sample_raw_text: RawText, sample_processed_result: ProcessedResult
    ) -> None:
        """Test that run returns the final ProcessedResult."""
        stage = MockStage("final", sample_processed_result)
        pipeline = DataPipeline([stage])

        result = pipeline.run(sample_raw_text)

        assert result is sample_processed_result

    def test_run_raises_on_stage_error(self, sample_raw_text: RawText) -> None:
        """Test that PipelineError is raised when a stage fails."""
        failing_stage = MockStage("failing", None)
        failing_stage.process = MagicMock(side_effect=Exception("Stage failed"))

        pipeline = DataPipeline([failing_stage])

        with pytest.raises(PipelineError):
            pipeline.run(sample_raw_text)

    def test_run_raises_if_not_processed_result(
        self, sample_raw_text: RawText
    ) -> None:
        """Test that error is raised if final output is not ProcessedResult."""
        stage = MockStage("wrong_output", "not a ProcessedResult")
        pipeline = DataPipeline([stage])

        with pytest.raises(PipelineError):
            pipeline.run(sample_raw_text)

    def test_add_stage(self) -> None:
        """Test adding a stage to the pipeline."""
        pipeline = DataPipeline([])
        stage = MockStage("new_stage", "output")

        pipeline.add_stage(stage)

        assert len(pipeline.stages) == 1
        assert pipeline.stages[0].name == "new_stage"

    def test_remove_stage(self) -> None:
        """Test removing a stage from the pipeline."""
        stage1 = MockStage("stage1", "output1")
        stage2 = MockStage("stage2", "output2")
        pipeline = DataPipeline([stage1, stage2])

        result = pipeline.remove_stage("stage1")

        assert result is True
        assert len(pipeline.stages) == 1
        assert pipeline.stages[0].name == "stage2"

    def test_remove_nonexistent_stage(self) -> None:
        """Test removing a stage that doesn't exist."""
        pipeline = DataPipeline([])

        result = pipeline.remove_stage("nonexistent")

        assert result is False

    def test_empty_pipeline_raises_error(self, sample_raw_text: RawText) -> None:
        """Test that empty pipeline raises error on run."""
        pipeline = DataPipeline([])

        with pytest.raises(PipelineError):
            pipeline.run(sample_raw_text)
