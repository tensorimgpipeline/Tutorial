# Level 2

With the updated code from [level 1](level_1.md) we are able to proceed and to include our first tipi tool.

## Goal

We now want to apply in a first simple step the `progress_task` decorator of tipi.
The good thing: We are doing it now, but don't rework this later, since the decorator already implements 
smooth into the tipi structure.
In a second step we like to remove all the leftover print statements and include them into the status 
of the `ProgressBar`.

## Before / After

The script still includes a lot print statements.

After we implemented the below tasks all print statements are presented via `ProgressBar` and status.

## Tasks

1. Apply Progress Decorator
2. Apply simple Update
3. Replace print statements via status

### Apply the Progress Decorator

First, we need to import the `progress_task` decorator into our `trainer.py` module:

```python
from tipi.decorators import progress_task
```

This allows us to provide our iterating methods with the decorator:

```python
...

    @progress_task()
    def train_epoch(self, dataloader: torch.utils.data.DataLoader[datasets.FashionMNIST]) -> None:
...

    @progress_task()
    def test_epoch(self, dataloader: torch.utils.data.DataLoader[datasets.FashionMNIST]) -> None:
...

    @progress_task()
    def run_epochs(
...
```

With this few changes we are already able to execute the `train.py` again:

```bash
uv run python level_2/train.py
```

This time the expected output should not change at all.
This is intentional, since we want to replace `print` statements with `yield`.

Since the functions do not yield anything right now, the progress bar is not initialized.
As soon as the function is converted into a `Generator`, the decorator will interact
with provided `Update`

### Apply simple Update

As a first simple step we would like to get the progress bars working.
Since the decorators are already in place we need to add two things per loop:

1. The Return Type of the functions from `-> None` to `-> Generator[Update, None, None]`[^1]
2. Somewhere inside the loops (best at the end) a `yield Update()`

Additional we need import `collections.abc.Generator` and `tipi.decorators.Update`

We now are able to execute again:

```bash
uv run python levle_2/train.py
```

We expect to see now something like this:

```bash
loss: 1.072322  [57664/60000]
Train Epoch ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ (938/938) •  • 0:00:00
Test Epoch ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ (157/157) •  • 0:00:00
Test Error: 
 Accuracy: 64.8%, Avg loss: 1.086084 

Run Epochs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ (5/5) •  • 0:00:00
Done!
Saved PyTorch Model State to model.pth
Predicted: "Ankle boot", Actual: "Ankle boot"
```

We still heavy the print statments but also already the progress bar.
With this state the name of the function is used as the title of the progress bar.

### Replace print statements via status

To replace the print statements we have to options:

1. Add the statement as the first argument (`message`) to the `Update` class.
2. Add another `yield Update("my message", advance=0)`

Setting the advance to 0 updates only the status message of the current progress bar.

For our example does this mean:

We apply option 1 for `run_epochs` and `test_epoch` and option 2
for `train_epoch`.

## Result

After completing the tasks, we should have now a working progress bar. 
The output is now much cleaner, but still has room for improvement.
The good thing: Those improvements are already in place and work as soon as the later integrate the pipeline.

## Troubleshooting

If you had issues to recreate this level, please provide informations via [troubleshoot form](https://github.com/tensorimgpipeline/Tutorial/issues/new?template=LEVEL_TROUBLESHOOT.yml)

### AI autocomplete

Since our functions are now `Generator` objects, some ai code completions think other functions like
`run_epochs` need to process them, and provide completions like `yield from train_epoch`.

Those completions are not necessary, since we already process the generators via the decorator.

### Return Value

The generator type annotaion provides three fields `Generator[<yield-type>, <send-type>, <return-type>]`.

So, if we would like to use the decorator and create usual return pattern, we could achieve it like this:

```python
@progress_task()
def iteration() -> Generator[Update, None, int]:
    for i in range(5):
        yield Update(f"Iteration: {i}")
    return i
```



