"""Fast architecture smoke tests; these do not train or download EMNIST."""
import torch
from src.train_compare import CNN, MLP


def test_models_return_47_class_logits():
    batch = torch.randn(4, 1, 28, 28)
    assert CNN()(batch).shape == (4, 47)
    assert MLP()(batch).shape == (4, 47)
