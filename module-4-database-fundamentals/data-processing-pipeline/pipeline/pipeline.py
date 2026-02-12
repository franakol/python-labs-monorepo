"""Pipeline orchestrator for coordinating data processing stages.

This module provides the DataPipeline class that chains together
pipeline stages and manages the end-to-end data flow.
"""

import logging
from typing import Any

from pipeline.exceptions import PipelineError
from pipeline.interfaces.stages import PipelineStage
from pipeline.models import ProcessedResult, RawText

logger = logging.getLogger(__name__)


class DataPipeline:
    """Orchestrator for multi-stage data processing.

    Coordinates the execution of pipeline stages in sequence,
    passing data from one stage to the next.

    Attributes:
        _stages: List of pipeline stages to execute.
    """

    def __init__(self, stages: list[PipelineStage[Any, Any]]) -> None:
        """Initialize the pipeline with stages.

        Args:
            stages: Ordered list of stages to execute.
        """
        self._stages = stages
        stage_names = [s.name for s in stages]
        logger.info(f"Pipeline initialized with stages: {stage_names}")

    @property
    def stages(self) -> list[PipelineStage[Any, Any]]:
        """Return the list of pipeline stages."""
        return self._stages

    def run(self, input_data: RawText) -> ProcessedResult:
        """Execute the full pipeline on input data.

        Args:
            input_data: The raw text to process.

        Returns:
            ProcessedResult after all stages complete.

        Raises:
            PipelineError: If any stage fails.
        """
        trace_id = input_data.trace_id
        logger.info(f"[{trace_id}] Starting pipeline execution")
        logger.info(f"[{trace_id}] Input: {input_data.content[:50]}...")

        data: Any = input_data

        for stage in self._stages:
            stage_name = stage.name
            logger.info(f"[{trace_id}] Entering stage: {stage_name}")

            try:
                data = stage.process(data)
                logger.info(f"[{trace_id}] Completed stage: {stage_name}")
                logger.debug(f"[{trace_id}] Stage output type: {type(data).__name__}")

            except PipelineError:
                logger.error(f"[{trace_id}] Pipeline error in {stage_name}")
                raise

            except Exception as e:
                logger.error(f"[{trace_id}] Unexpected error in {stage_name}: {e}")
                raise PipelineError(f"Stage {stage_name} failed: {e}") from e

        logger.info(f"[{trace_id}] Pipeline execution complete")

        if not isinstance(data, ProcessedResult):
            raise PipelineError(
                f"Pipeline did not produce ProcessedResult, got {type(data).__name__}"
            )

        return data

    def add_stage(self, stage: PipelineStage[Any, Any]) -> None:
        """Add a stage to the end of the pipeline.

        Args:
            stage: The stage to add.
        """
        self._stages.append(stage)
        logger.info(f"Added stage: {stage.name}")

    def remove_stage(self, stage_name: str) -> bool:
        """Remove a stage by name.

        Args:
            stage_name: Name of the stage to remove.

        Returns:
            True if stage was removed, False if not found.
        """
        for i, stage in enumerate(self._stages):
            if stage.name == stage_name:
                self._stages.pop(i)
                logger.info(f"Removed stage: {stage_name}")
                return True
        return False
