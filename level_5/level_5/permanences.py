"""Permanences for level_5.

Permanences are objects that persist throughout the pipeline lifecycle.
They store state, data, models, or any resources needed by multiple processes.
"""

from pathlib import Path
import shutil
from typing import Any

from torchvision import datasets, transforms

from tipi.abstractions import Permanence


class ConfigPermanence(Permanence):
    """Stores configuration parameters for the pipeline."""

    def __init__(self, config_path: Path | str):
        """Initialize configuration permanence.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = (
            Path(config_path) if isinstance(config_path, str) else config_path
        )
        self.settings: dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        # Simple example - could load from TOML, YAML, JSON, etc.
        self.settings = {
            "batch_size": 32,
            "learning_rate": 0.001,
            "epochs": 10,
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.settings.get(key, default)

    def cleanup(self) -> None:
        """Clean up resources."""
        self.settings.clear()


class DataPermanence(Permanence):
    """Stores data loaded during the pipeline."""

    def __init__(
        self,
        root: Path | str,
        data_set: str = "FashionMNIST",
        transform: Any = None,
        download: bool = True,
        prevent_deletion: bool = True,
    ):
        """Initialize data permanence.

        Args:
            root: Root directory for data files
            data_set: Name of the dataset to load
            transform: Transformations to apply to the data
            download: Whether to download the dataset if it doesn't exist
            prevent_deletion: Whether to prevent deletion of the downloaded dataset
        """
        self.root = Path(root) if isinstance(root, str) else root
        dataset_class = getattr(datasets, data_set, None)
        if dataset_class is None:
            raise ValueError(
                f"Dataset {data_set} is not available in torchvision.datasets."
            )

        if isinstance(transform, str):
            transform = getattr(transforms, transform, None)
        elif isinstance(transform, list):
            transform = transforms.Compose([
                getattr(transforms, t)() if isinstance(t, str) else t for t in transform
            ])
        if not transform:
            transform = transforms.ToTensor()  # Default transform

        self.training_data = dataset_class(
            root=self.root,
            train=True,
            download=download,
            transform=transform,
        )
        self.test_data = dataset_class(
            root=self.root,
            train=False,
            download=download,
            transform=transform,
        )

        self.prevent_deletion = prevent_deletion

    def cleanup(self) -> None:
        """Clean up resources."""
        if not self.prevent_deletion:
            shutil.rmtree(self.root, ignore_errors=True)
        self.training_data = None
        self.test_data = None
