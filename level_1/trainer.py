# tutorial/level_1/trainer.py
from __future__ import annotations
from typing import Any

import torch
from torchvision import datasets


class Trainer:
    """Minimal trainer that holds state for training/testing loops.

    Designed so train_epoch() and test_epoch() are simple methods you can
    call from main (one-liners). Later you can subclass this to become a
    PipelineProcess / permanence.
    """

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

        self.test_loss: float
        self.correct: float

    def reset(self):
        self.test_loss = 0.0
        self.correct = 0.0

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

