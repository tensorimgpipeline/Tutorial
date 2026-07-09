from tipi.core.permanences.loggers.patterns import ConfusionMatrixFigurePattern

fashion_mnist_classes = (
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
)

fashion_mnist_class_values = tuple(range(len(fashion_mnist_classes)))

FashionMNISTConfusionPattern = ConfusionMatrixFigurePattern(
    name="FashionMNISTConfusionMatrix",
    title="FashionMNIST Confusion Matrix",
    class_values=fashion_mnist_class_values,
    class_labels=fashion_mnist_classes,
    annotation_format="d",
)
