# Level 4

Level 4 introduces our loggers.
Our loggers do not log just values or messages, also graphs.
For many this is not a new information, but we try to create a generalized interface.
So switch from one logging service to another doesn't create a lot of headaches.

## Goal

We would like to replace the leftover print statements with debug logging.
Most of it displays already information that classifies as debug.
Since in ML routines informations rarly classifies as info, our logger does not provide a info method.
Instead we would like to use `log_metrics` and `log_figure` methods of loggers.

## Before / After

Currently we use normal print statements to display information:

```python
print(f"Using {device} device")
```

We would like to replace them with our logger methods, like `debug`:

```python
logger.debug(f"Using {device} device")
```

Additional we place methods to create plots of our data:

```python
logger.log_figure()
```

## Tasks

1. Provide `BasicLogger` via `controller`
2. Replace print statements
3. Implement metric and figure logging
4. Replace `BasicLogger` with `TensorBoardLogger`

### Provide `BasicLOgger` via `controller`

To provide the `BasicLogger` we just need to import it into the controller module
and extend the permanences dict:

```python
from tipi.core.permanences import BasicLogger as Logger

permanences: dict[str, Permanence] = {
    "Device": Device(),
    "Logger": Logger(log_level="DEBUG", log_dir="level_4/logs/basic"),
}
```

We need to set the `log_level` for now to `DEBUG`, so we are able to actually see our print statements.
By default the log_dir is defined as `logs/basic`, but we change it so we do not interfer with the other levels.

### Update the `Trainer`

Since our trainer also provides print statments, aswell as logging metrics we need to add our pattern system to the trainer:

```python
from tipi.core.permanences.loggers.base import BaseLoggerManager
from tipi.core.permanences.loggers.patterns import batch_loss, test_loss, test_accuracy
```

We add as `logger: BaseLoggerManager` parameter to the `__init__` of the `Trainer` and make it 
available with `self.logger = logger`

Now we are able to use the patterns to log metrics at the needed positions:

```python
#  class based metics log    Pattern Helper Method
#                   |                  |     Log Value
#                   |                  |         |
#                   v                  v         v
    self.logger.log_metrics(metrics=batch_loss(loss))
```

### Replace print statements

In the script `train.py` we just read the logger from controller,
somewhere above the first print statement:

```python
logger = controller.get_permanence("Logger")
```

If we now execute:

```bash
uv run python level_4/train.py
```

only our progress bar should be displayed.
The logs should be found at `logs/basic/basic_logger.log`.

### Implement metric and figure logging

In comparison to Tensorboard and WandB or others, our `BasicLogger` does not provide a while training plot method.
Instead the plots are generated manually via `log_metric_figure`.
In this tutorial we apply this at the end.

We import the necessary patterns:

```python
from tipi.core.permanences.loggers.basic import BasicLogger
from tipi.core.permanences.loggers.patterns import LOSS_CURVE, ACCURACY_CURVE
```

and call the `log_metric_figure` with given pattern:

```python
if isinstance(logger, BasicLogger):
    logger.log_metric_figure(figure_pattern=LOSS_CURVE)
    logger.log_metric_figure(figure_pattern=ACCURACY_CURVE)
```

The Check is implemented, so we do not run into issues with our next step.

### Replace `BasicLogger` with `TensorBoardLogger`

Replacing the Logger is quite simple, since we only need to switch the Logger class in our controller:

```diff
-from tipi.core.permanences.loggers.basic import BasicLogger as Logger
+from tipi.core.permanences.loggers.tensorboard import TensorBoardLogger as Logger
+from tipi.core.permanences.loggers.patterns import LOSS_CURVE, ACCURACY_CURVE
```

We need the `CURVE` patterns so the logger is able to create the custom scalar layout from it.

So the only extension to our controller:

```python
    "Logger": Logger(
        log_level="DEBUG",
        log_dir="level_4/logs/basic",
        patterns=[LOSS_CURVE, ACCURACY_CURVE],
    )
```

### Bonus: Confusion Matrix

All Loggers provide an implementation of `log_figure`, which allows to log custom figures.
To provide an example how this is working, we provided the `build_confusion_matrix_figure`.
We need to create our own pattern for the dataset by adding the `pattern.py` module.
This pattern ensures the building process of the figure will be aligned to our dataset.

We import the pattern on top of our `train.py` script:

```python
from pattern import FashionMNISTConfusionPattern
```

Since our test run was a bit cheap until now we update it and use the `log_figure`:

```diff
+y_preds = []
+y_trues = []
+
x, y = test_data[0][0], test_data[0][1]
with torch.no_grad():
-     x = x.to(device)
-    pred = model(x)
-    predicted, actual = classes[pred[0].argmax(0)], classes[y]
+    for X, y in test_dataloader:
+        X = X.to(device)
+        y = y.to(device)
+
+        logits = model(X)
+        preds = logits.argmax(dim=1)
+
+        y_preds.extend(preds.detach().cpu().tolist())
+        y_trues.extend(y.detach().cpu().tolist())
+
+    predicted, actual = (
+        classes[y_preds[0]],
+        classes[y_trues[0]],
+    )
    logger.debug(f'Predicted: "{predicted}", Actual: "{actual}"')

if isinstance(logger, BasicLogger):
    logger.log_metric_figure(figure_pattern=LOSS_CURVE)
    logger.log_metric_figure(figure_pattern=ACCURACY_CURVE)

+fig = logger.build_confusion_matrix_figure(
+    figure_pattern=FashionMNISTConfusionPattern, y_true=y_trues, y_pred=y_preds
+)
+
+logger.log_figure(name="ConfusionMatrix", figure=fig)
```

Since the TensorBoardLogger is active the figure will be logged to the image tab of TensorBoard.

> This Bonus example will not be included in level_5.

## Result

With all those changes in place and exectution with `BasicLogger` and `TensorBoardLogger` at least once, 
we should now have the following files in our directory:

```
level_4/logs/basic/
├── accuracy_50.png
├── basic_logger.log
├── events.out.tfevents.1783596576....
├── loss_50.png
├── metrics.jsonl
└── tensorboard_logger.log
```

## Troubleshooting

If you had issues to recreate this level, please provide informations via [troubleshoot form](https://github.com/tensorimgpipeline/Tutorial/issues/new?template=LEVEL_TROUBLESHOOT.yml)

