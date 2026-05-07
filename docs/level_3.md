# Level 3

Level 3 intorduces the controller class, which helps us to describe how to apply device detection.

## Goal

We would like to create a controller object.
But this will only be temporary for level 3.
We later use the built-in controller object of tipi.

We could skip this step, because we already provide logic how to access provided logic,
But we thought it could be a good idea to show how the controller works under the hood.
This will help to understand and debug code later easier.

## Before / After

Currently the device is selected via:

```python
device = (
    torch.accelerator.current_accelerator().type
    if torch.accelerator.is_available()
    else "cpu"
)
```

After Applying the tasks below we will be able to analyze on startup the device of the system and
if torch version needs to be changed for the target system.
We also try to explain how to achieve different system support based on this approach

## Tasks

1. Create a copy of level 2 code
2. Create a controller module
3. Implement controller in script

### Create a Controller module

Create a new module called `controller.py` with following content:

```python
# level_3/controller.py
from tipi.abstractions import Permanence
from tipi.core.builder import ProcessWithParams
from tipi.core.controller import PipelineController
from tipi.core.permanences import Device

permanences: dict[str, Permanence] = {"Device": Device()}
process_specs: list[ProcessWithParams] = []

controller = PipelineController(permanences=permanences, process_specs=process_specs)

__all__ = ["controller"]
```

this allows us to utelize the `Device` permanence similiar to what later in the full integration happens.

### Implement controller in script

To implement the controller an access the device we just need to import it:

```python
from controller import controller
```

and replace the `device` creation:

```diff
+device = controller.get_permanence("Device").device
-device = (
-    torch.accelerator.current_accelerator().type
-    if torch.accelerator.is_available()
-    else "cpu"
)
```

## Result

On the first glance this seems to change nothing when we execute:

```bash
uv run python level_3/train.py
```

But this allows us to utelize the implemented accelerator utelities.
For example:

- automatic get the available device with the most available vram
- select automatically cpu if none is available
- provide support for multiple backends (cuda and xpu at the moment)
- additionals to come...

In the implementation of [level 5](level_5.md#todo) we will learn how to configure this finally in
the pipeline.

## Troubleshooting

If you had issues to recreate this level, please provide informations via [troubleshoot form](https://github.com/tensorimgpipeline/Tutorial/issues/new?template=LEVEL_TROUBLESHOOT.yml)