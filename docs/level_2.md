# Level 2

With the updated code from [level 1](level_1.md) we are able to proceed and to include our first tipi tool.

We now want to apply in a first simple step the `progress_task` decorator of tipi.
The good thing: We are doing it now, but don't rework this later, since the decorator already implements 
smooth into the tipi structure.

## Apply the Progress Decorator

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

This time the expected output should look like this:

```bash
-------------------------------
loss: 2.298546  [   64/60000]
loss: 2.289133  [ 6464/60000]
loss: 2.275903  [12864/60000]
loss: 2.271281  [19264/60000]
loss: 2.222085  [25664/60000]
loss: 2.212286  [32064/60000]
loss: 2.212423  [38464/60000]
Train Epoch ━━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━━  69% 0:00:02
Run Epochs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
```

We still heavy the print statments but also already the progress bar.
With this state the name of the function is used as the title of the progress bar.