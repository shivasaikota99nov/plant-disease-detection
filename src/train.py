"""
Training script for the Plant Disease Detection CNN.
Saves model weights, class index mappings, and accuracy/loss curves.
"""

import os
import sys
import json
import time
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# Ensure local src imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.model import get_model
from src.dataset import load_plant_data


def train_model(
    data_dir: str,
    output_dir: str = "models",
    architecture: str = "mobilenet_v3_small",
    epochs: int = 8,
    batch_size: int = 32,
    lr: float = 0.001,
    max_samples_per_class: int = 80
):
    os.makedirs(output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"--> Using compute device: {device}")

    # 1. Load Data
    print(f"--> Loading dataset from '{data_dir}'...")
    train_loader, val_loader, class_names = load_plant_data(
        data_dir=data_dir,
        batch_size=batch_size,
        max_samples_per_class=max_samples_per_class
    )
    num_classes = len(class_names)
    print(f"--> Detected {num_classes} plant classes.")

    # Save class names mapping
    class_map_path = os.path.join(output_dir, "class_names.json")
    with open(class_map_path, "w") as f:
        json.dump(class_names, f, indent=2)
    print(f"--> Saved class mapping to {class_map_path}")

    # 2. Build Model
    print(f"--> Building '{architecture}' model for {num_classes} classes...")
    model = get_model(num_classes=num_classes, architecture=architecture, pretrained=True)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)

    history = {
        "train_loss": [], "val_loss": [],
        "train_acc": [], "val_acc": []
    }
    best_val_acc = 0.0
    best_model_path = os.path.join(output_dir, "plant_disease_model.pth")

    print("\n" + "=" * 55)
    print(f"Starting Training: {epochs} Epochs | Batch Size {batch_size}")
    print("=" * 55)

    start_time = time.time()

    for epoch in range(1, epochs + 1):
        epoch_start = time.time()

        # Training Phase
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total_train += targets.size(0)
            correct_train += predicted.eq(targets).sum().item()

        epoch_train_loss = running_loss / total_train if total_train > 0 else 0.0
        epoch_train_acc = 100.0 * correct_train / total_train if total_train > 0 else 0.0

        # Validation Phase
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)

                outputs = model(inputs)
                loss = criterion(outputs, targets)

                val_loss += loss.item() * inputs.size(0)
                _, predicted = outputs.max(1)
                total_val += targets.size(0)
                correct_val += predicted.eq(targets).sum().item()

        epoch_val_loss = val_loss / total_val if total_val > 0 else 0.0
        epoch_val_acc = (100.0 * correct_val / total_val) if total_val > 0 else 0.0

        scheduler.step(epoch_val_loss)
        epoch_duration = time.time() - epoch_start

        # Record history
        history["train_loss"].append(epoch_train_loss)
        history["val_loss"].append(epoch_val_loss)
        history["train_acc"].append(epoch_train_acc)
        history["val_acc"].append(epoch_val_acc)

        print(
            f"Epoch [{epoch:02d}/{epochs:02d}] ({epoch_duration:.1f}s) | "
            f"Train Loss: {epoch_train_loss:.4f} - Train Acc: {epoch_train_acc:.2f}% | "
            f"Val Loss: {epoch_val_loss:.4f} - Val Acc: {epoch_val_acc:.2f}%"
        )

        # Checkpoint if best validation accuracy
        if epoch_val_acc >= best_val_acc:
            best_val_acc = epoch_val_acc
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "accuracy": best_val_acc,
                "architecture": architecture,
                "num_classes": num_classes,
                "class_names": class_names
            }, best_model_path)
            print(f"  --> Saved new best model checkpoint to '{best_model_path}' ({best_val_acc:.2f}%)")

    total_training_time = time.time() - start_time
    print("\n" + "=" * 55)
    print(f"Training Complete in {total_training_time/60:.2f} mins. Best Val Accuracy: {best_val_acc:.2f}%")
    print("=" * 55)

    # 3. Save Training History Plot
    plot_training_metrics(history, output_dir)
    return best_model_path


def plot_training_metrics(history: dict, output_dir: str):
    epochs_range = range(1, len(history["train_loss"]) + 1)
    plt.figure(figsize=(12, 5))

    # Loss
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, history["train_loss"], label="Train Loss", marker="o", color="#e74c3c")
    plt.plot(epochs_range, history["val_loss"], label="Val Loss", marker="s", color="#3498db")
    plt.title("Model Loss Across Epochs")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    # Accuracy
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, history["train_acc"], label="Train Accuracy", marker="o", color="#2ecc71")
    plt.plot(epochs_range, history["val_acc"], label="Val Accuracy", marker="s", color="#f39c12")
    plt.title("Model Accuracy Across Epochs (%)")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plot_path = os.path.join(output_dir, "training_metrics.png")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"--> Saved training curves chart to '{plot_path}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CNN on Plant Disease Dataset")
    parser.add_argument("--data_dir", type=str, default="dataset/Dataset", help="Path to plant disease dataset folder")
    parser.add_argument("--output_dir", type=str, default="models", help="Directory to save weights & metrics")
    parser.add_argument("--arch", type=str, default="mobilenet_v3_small", choices=["mobilenet_v3_small", "resnet18", "custom_cnn"])
    parser.add_argument("--epochs", type=int, default=6, help="Number of epochs to train")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--max_samples_per_class", type=int, default=80, help="Max images per class (0 for all)")
    args = parser.parse_args()

    train_model(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        architecture=args.arch,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        max_samples_per_class=args.max_samples_per_class
    )
