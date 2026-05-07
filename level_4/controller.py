from tipi.abstractions import Permanence
from tipi.core.builder import ProcessWithParams
from tipi.core.controller import PipelineController
from tipi.core.permanences import Device
from tipi.core.permanences import BasicLogger as Logger

permanences: dict[str, Permanence] = {"Device": Device(), "Logger": Logger()}
process_specs: list[ProcessWithParams] = []

controller = PipelineController(permanences=permanences, process_specs=process_specs)

__all__ = ["controller"]
