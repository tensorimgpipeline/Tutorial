# Level 1

With a working tutorial from `pytorch` combined with `uv` we are now able to begin the refactoring.
The goal of the refactoring is to achieve a smooth transition to a final integration with the tool [tipi](https://pypi.org/project/TensorImgPipeline/).

This level provides the Instruction, to modify the `train.py` script, so that the integration of provided utility of the `tipi` package could be used.

## Refactor

Copy the level_0 to level_1 directory (it is also possible to use a version control system to switch between levels.
We decided against this, since we want a clean final state of each level.).

### Remove the current train iterator functions

From `level_1/train.py` remove the two functions:

- `def train`
- `def test`

Also, the epoch iteration needs to be deleted.
Lines 61-99.

We want to create a class `Trainer`, which provides those methods.

Instead, we update the script by creating our class instance and
calling their methods (they don't exist yet) at the same place:

At the top of the script below the other imports:

```python
from . import trainer as trainer_lib
```

> This creates some trouble with type checkers, in a real
> refactoring all this should be executed in a package.

Now at line 63 we can create:

```python
trainer = trainer_lib.Trainer(
    model=model,
    optimizer=optimizer,
    loss_fn=loss_fn,
    device=device
)

trainer.run_epochs(range(epochs), train_dataloader, test_dataloader)
```

## Create the class

The class `Trainer` needs to provide now all the things which are needed in the
for loop methods it provides:

```python
class Trainer:
    def __init__(
        self,
        model: torch.nn.Module,
        optimizer: torch.optim.Optimizer,
        loss_fn: Any,
        device: torch.device | None = None,
    ) -> None:
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.device = device

        # properties
        self.test_loss: float
        self.correct: float
```

To work correctly in the test and with a to give it more usability we provide a reset method:

```python
    def reset(self):
        self.test_loss = 0.0
        self.correct = 0.0

```

> In this scenario we call it directly in the epoch loop, but we could also run it directly in
> the `__init__` method.

The real refactoring is now happening the three loop methods of the `Trainer` class.
The recipe follows this concept:

```
Identify the Loop -> Identify calls ouside Loop -> Move Loop into function
-> Move outside loop into higher hierachy function
```

For Example the `torch.no_grad`, `model.train`, `model.eval` or other calls move into the `epoch`
method.

Here are the three methods:

```python
    def train_epoch(self, dataloader: torch.utils.data.DataLoader[datasets.FashionMNIST]) -> None:
        for batch, (X, y) in enumerate(dataloader):
            X, y = X.to(self.device), y.to(self.device)

            # Compute prediction error
            pred = self.model(X)
            loss = self.loss_fn(pred, y)

            # Backpropagation
            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()

            if batch % 100 == 0:
                loss, current = loss.item(), (batch + 1) * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{self.train_size:>5d}]")

    def test_epoch(self, dataloader: torch.utils.data.DataLoader[datasets.FashionMNIST]) -> None:
        for X, y in dataloader:
            X, y = X.to(self.device), y.to(self.device)
            pred = self.model(X)
            self.test_loss += self.loss_fn(pred, y).item()
            self.correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    def run_epochs(
        self,
        epochs: range,
        train_loader: torch.utils.data.DataLoader[datasets.FashionMNIST],
        test_loader: torch.utils.data.DataLoader[datasets.FashionMNIST],
    ):
        self.train_size = len(train_loader.dataset)  # type: ignore
        self.test_size = len(test_loader.dataset)  # type: ignore
        self.num_batches_test = len(test_loader)
        for t in epochs:
            print(f"Epoch {t+1}\n-------------------------------")
            self.model.train()
            self.train_epoch(train_loader)
            self.model.eval()
            self.reset()
            with torch.no_grad():
                self.test_epoch(test_loader)
            self.test_loss /= self.num_batches_test
            self.correct /= self.test_size
            print(f"Test Error: \n Accuracy: {(100*self.correct):>0.1f}%, Avg loss: {self.test_loss:>8f} \n")
```

## Result

If everything works as expected, the result should look the same as in [level_0](level_1.md#expected-result)

## What's next?

We are now prepared to use the first functionality of tipi: decorator progress bars.

In [Level 2](level_2.md), we'll add progress bars via decorator so you can see training progress in real-time.