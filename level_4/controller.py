from tipi.abstractions import Permanence
from tipi.core.builder import ProcessWithParams
from tipi.core.controller import PipelineController
from tipi.core.permanences import Device
from tipi.core.permanences.loggers.tensorboard import TensorBoardLogger as Logger
from tipi.core.permanences.loggers.patterns import LOSS_CURVE, ACCURACY_CURVE

permanences: dict[str, Permanence] = {
    "Device": Device(),
    "Logger": Logger(
        log_level="DEBUG",
        log_dir="level_4/logs/basic",
        patterns=[LOSS_CURVE, ACCURACY_CURVE],
    ),
}
process_specs: list[ProcessWithParams] = []

controller = PipelineController(permanences=permanences, process_specs=process_specs)

__all__ = ["controller"]
