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

Also the epoch iteration needs to be deleted.
Lines 61 - 99.

We want to create a class `Trainer`, which provides those methods.

Instead we update the script by creating our class instance and
calling their methods (they don't exists yet) at the same place:

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
    train_loader=train_dataloader,
    test_loader=test_dataloader,
    optimizer=optimizer,
    epochs=5,
    loss_fn=loss_fn,
    device=device
)

trainer.run_epochs()
```

## Create the class

The class `Trainer` needs to provide now all the things which are needed in the
for loop methods it provides:

```python
class Trainer:
    def __init__(
        self,
        model: torch.nn.Module,
        train_loader: torch.utils.data.DataLoader[datasets.FashionMNIST],
        test_loader: torch.utils.data.DataLoader[datasets.FashionMNIST],
        optimizer: torch.optim.Optimizer,
        epochs: int,
        loss_fn: Any,
        device: torch.device | None = None,
    ) -> None:
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.optimizer = optimizer
        self.epochs = epochs
        self.loss_fn = loss_fn
        self.device = device

        # properties
        self.train_size = len(train_loader.dataset) # type: ignore
        self.test_size = len(test_loader.dataset) # type: ignore
        self.num_batches_test = len(test_loader)
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
    def train_epoch(self) -> None:
        for batch, (X, y) in enumerate(self.train_loader):
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

    def test_epoch(self) -> None:
        for X, y in self.test_loader:
            X, y = X.to(self.device), y.to(self.device)
            pred = self.model(X)
            self.test_loss += self.loss_fn(pred, y).item()
            self.correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    def run_epochs(self):
        for t in range(self.epochs):
            print(f"Epoch {t+1}\n-------------------------------")
            self.model.train()
            self.train_epoch()
            self.model.eval()
            self.reset()
            with torch.no_grad():
                self.test_epoch()
            self.test_loss /= self.num_batches_test
            self.correct /= self.test_size
            print(f"Test Error: \n Accuracy: {(100*self.correct):>0.1f}%, Avg loss: {self.test_loss:>8f} \n")
```

## Result

If everything works as expected, the result should look the same as in [level_0](level_1.md#expected-result)
