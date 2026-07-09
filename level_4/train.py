import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

from trainer import Trainer
from controller import controller

from tipi.core.permanences.loggers.basic import BasicLogger
from tipi.core.permanences.loggers.patterns import LOSS_CURVE, ACCURACY_CURVE

# Download training data from open datasets.
training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

# Download test data from open datasets.
test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

batch_size = 64

logger = controller.get_permanence("Logger")

# Create data loaders.
train_dataloader = DataLoader(training_data, batch_size=batch_size)
test_dataloader = DataLoader(test_data, batch_size=batch_size)

for X, y in test_dataloader:
    logger.debug(f"Shape of X [N, C, H, W]: {X.shape}")
    logger.debug(f"Shape of y: {y.shape} {y.dtype}")
    break


device = controller.get_permanence("Device").device
logger.debug(f"Using {device} device")


# Define model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


model = NeuralNetwork().to(device)
logger.debug(model)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

epochs = 5

trainer = Trainer(
    model,
    optimizer=optimizer,
    loss_fn=loss_fn,
    device=torch.device(device),
    logger=logger,
)

trainer.run_epochs(range(epochs), train_dataloader, test_dataloader)
logger.debug("Done!")

torch.save(model.state_dict(), "model.pth")
logger.debug("Saved PyTorch Model State to model.pth")

model = NeuralNetwork().to(device)
model.load_state_dict(torch.load("model.pth", weights_only=True))

classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

model.eval()
x, y = test_data[0][0], test_data[0][1]
with torch.no_grad():
    x = x.to(device)
    pred = model(x)
    predicted, actual = classes[pred[0].argmax(0)], classes[y]
    logger.debug(f'Predicted: "{predicted}", Actual: "{actual}"')

if isinstance(logger, BasicLogger):
    logger.log_metric_figure(figure_pattern=LOSS_CURVE)
    logger.log_metric_figure(figure_pattern=ACCURACY_CURVE)
