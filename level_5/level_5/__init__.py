"""level_5 - A TensorImgPipeline project.

This module registers permanences and processes for the level_5 pipeline.
"""

from tipi.abstractions import Permanence, PipelineProcess

from level_5.permanences import (
    ConfigPermanence,
    DataPermanence,
)
from level_5.processes import (
    LoadDataProcess,
    ProcessDataProcess,
)

# Register permanences that will be available throughout the pipeline
permanences_to_register: set[type[Permanence]] = {
    ConfigPermanence,
    DataPermanence,
}

# Register processes that define the pipeline steps
processes_to_register: set[type[PipelineProcess]] = {
    LoadDataProcess,
    ProcessDataProcess,
}

__all__ = [
    "permanences_to_register",
    "processes_to_register",
]