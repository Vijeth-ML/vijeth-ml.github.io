"""Train an MLP and CNN on EMNIST Balanced with a validation split.

The test set is evaluated once per model after training. The original coursework
files are preserved in original/; this script is a cleaned reproducibility path.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchvision.datasets import EMNIST
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix


class MLP(nn.Module):
    def __init__(self, input_size: int = 28 * 28, hidden_size: int = 256,
                 num_classes: int = 47, hidden_layers: int = 2):
        super().__init__()
        layers: list[nn.Module] = [nn.Flatten(), nn.Linear(input_size, hidden_size), nn.ReLU()]
        for _ in range(hidden_layers - 1):
            layers.extend([nn.Linear(hidden_size, hidden_size), nn.ReLU()])
        layers.append(nn.Linear(hidden_size, num_classes))
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


class CNN(nn.Module):
    def __init__(self, num_classes: int = 47):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.AdaptiveAvgPool2d((4, 4)),
        )
        self.classifier = nn.Sequential(nn.Flatten(), nn.Linear(32 * 4 * 4, 128), nn.ReLU(), nn.Linear(128, num_classes))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module, device: torch.device) -> dict:
    model.eval()
    loss_sum = 0.0
    total = 0
    y_true: list[int] = []
    y_pred: list[int] = []
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            logits = model(images)
            loss_sum += criterion(logits, labels).item() * labels.size(0)
            preds = logits.argmax(dim=1)
            total += labels.size(0)
            y_true.extend(labels.cpu().tolist())
            y_pred.extend(preds.cpu().tolist())
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )
    return {
        "loss": loss_sum / max(total, 1),
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_precision": precision,
        "macro_recall": recall,
        "macro_f1": f1,
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=list(range(47))).tolist(),
        "n_examples": total,
    }


def train_one(name: str, model: nn.Module, train_loader: DataLoader, val_loader: DataLoader,
              test_loader: DataLoader, epochs: int, lr: float, weight_decay: float,
              device: torch.device) -> dict:
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    model.to(device)
    history = []
    best_val = -1.0
    best_state = None
    for epoch in range(1, epochs + 1):
        model.train()
        loss_sum = 0.0
        total = correct = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            loss_sum += loss.item() * labels.size(0)
            correct += (logits.argmax(1) == labels).sum().item()
            total += labels.size(0)
        val = evaluate(model, val_loader, criterion, device)
        row = {"epoch": epoch, "train_loss": loss_sum / max(total, 1),
               "train_accuracy": correct / max(total, 1),
               "validation_loss": val["loss"], "validation_accuracy": val["accuracy"]}
        history.append(row)
        print(f"{name} epoch {epoch:02d}/{epochs}: train_acc={row['train_accuracy']:.4f} val_acc={row['validation_accuracy']:.4f}")
        if val["accuracy"] > best_val:
            best_val = val["accuracy"]
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    # Hold the test set out of model selection; evaluate the selected checkpoint once.
    test = evaluate(model, test_loader, criterion, device)
    return {"model": name, "best_validation_accuracy": best_val, "history": history, "test": test}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--num-workers", type=int, default=0)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        parser.error("--epochs and --batch-size must be positive")

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    train_full = EMNIST(root=str(args.data_dir), split="balanced", train=True, download=True, transform=transform)
    test_set = EMNIST(root=str(args.data_dir), split="balanced", train=False, download=True, transform=transform)
    val_size = int(0.1 * len(train_full))
    train_size = len(train_full) - val_size
    train_set, val_set = random_split(train_full, [train_size, val_size], generator=torch.Generator().manual_seed(args.seed))
    common = {"batch_size": args.batch_size, "num_workers": args.num_workers, "pin_memory": device.type == "cuda"}
    train_loader = DataLoader(train_set, shuffle=True, **common)
    val_loader = DataLoader(val_set, shuffle=False, **common)
    test_loader = DataLoader(test_set, shuffle=False, **common)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "dataset": "EMNIST Balanced",
        "seed": args.seed,
        "train_examples": len(train_set),
        "validation_examples": len(val_set),
        "test_examples": len(test_set),
        "classes": len(train_full.classes),
        "device": str(device),
        "configuration": vars(args) | {"data_dir": str(args.data_dir), "output_dir": str(args.output_dir)},
        "models": [],
    }
    for name, model, decay in [
        ("MLP", MLP(), args.weight_decay),
        ("CNN", CNN(), 0.0),
    ]:
        result = train_one(name, model, train_loader, val_loader, test_loader,
                           args.epochs, args.lr, decay, device)
        torch.save(model.state_dict(), args.output_dir / f"{name.lower()}_best.pt")
        results["models"].append(result)
    out_path = args.output_dir / "results.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Saved metrics and confusion matrices to {out_path}")
    for result in results["models"]:
        test = result["test"]
        print(f"{result['model']} test accuracy={test['accuracy']:.4f}; macro-F1={test['macro_f1']:.4f}")


if __name__ == "__main__":
    main()
