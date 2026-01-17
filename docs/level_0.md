# Level 0

Here is the start.
You have just left the [Quickstart](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) Tutorial of Pytorch.

Before we can start with the transition, we need to prepare some steps to follow this tutorial.

## Preparation

First we need to install [uv](https://docs.astral.sh/uv/getting-started/installation/).
Aftwards we create in the current workspace the uv project:

```bash
uv init
```

Next we need to prepare the sources for pytorch to work properly in this scenario.
For this scenario a GPU is not necessary, so we need to declare the sources accordingly inside `pyproject.toml`:

```toml
[tool.uv]
required-environments = [
    "sys_platform == 'linux' and platform_machine == 'x86_64'"
]

[tool.uv.sources]
torch = [
  { index = "pytorch-cpu" },
]
torchvision = [
  { index = "pytorch-cpu" },
]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
```

Now we are able to install CPU version of `torch` and `torchvision`.

```bash
uv add torch torchvision
```

This should bring us to the point of the Pytorch Tutorial.

We should be able to execute:

```bash
uv run python level_0/train.py
```

## Expected Output

```text
Downloading http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz
...
Shape of X [N, C, H, W]: torch.Size([64, 1, 28, 28])
Shape of y: torch.Size([64]) torch.int64
Using cpu device
NeuralNetwork(
  (flatten): Flatten(...)
  ...
)
Epoch 1
-------------------------------
loss: 2.306702  [   64/60000]
loss: 2.295077  [ 6464/60000]
...
Test Error:
 Accuracy: 34.2%, Avg loss: 2.234821

...
Epoch 5
-------------------------------
...
Done!
Saved PyTorch Model State to model.pth
Predicted: "Ankle boot", Actual: "Ankle boot"
```

## What's next?

This script works, but notice a few pain points:

- **No progress indication** — You have no idea how long each epoch takes
- **No experiment tracking** — Loss values scroll by and are lost
- **Hardcoded device** — Works, but could be cleaner
- **Monolithic script** — Hard to reuse or test individual parts

In [Level 1](level_1.md), we'll refactor the script so we get managable for-loops.
