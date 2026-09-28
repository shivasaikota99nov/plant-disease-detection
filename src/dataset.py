"""
Dataset preparation, augmentation, and data loaders for plant disease training.
Handles both pre-split datasets and single combined folders with automatic train-val splitting
and balanced class subsampling for fast CPU training.
"""

import os
from typing import Tuple, List, Optional
import torch
from torch.utils.data import DataLoader, Dataset, Subset, random_split
from torchvision import datasets, transforms


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def get_transforms(image_size: int = 224) -> Tuple[transforms.Compose, transforms.Compose]:
    train_transform = transforms.Compose([
        transforms.Resize((image_size + 32, image_size + 32)),
        transforms.RandomResizedCrop(image_size, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(degrees=20),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

    val_transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

    return train_transform, val_transform


class TransformDataset(Dataset):
    def __init__(self, subset, transform):
        self.subset = subset
        self.transform = transform

    def __len__(self):
        return len(self.subset)

    def __getitem__(self, idx):
        img, label = self.subset[idx]
        return self.transform(img), label


def load_plant_data(
    data_dir: str,
    batch_size: int = 32,
    val_split: float = 0.2,
    max_samples_per_class: Optional[int] = None,
    num_workers: int = 0
) -> Tuple[DataLoader, DataLoader, List[str]]:
    """
    Loads dataset from directory.
    - If max_samples_per_class is set, takes up to that many samples per class for fast, balanced training.
    - Automatically splits into train and validation sets with proper augmentations.
    """
    train_transform, val_transform = get_transforms(image_size=224)

    # Clean path resolution
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' does not exist.")

    # Check for nested Dataset directory
    nested_dir = os.path.join(data_dir, "Dataset")
    if os.path.isdir(nested_dir) and not any(os.path.isdir(os.path.join(data_dir, sub)) for sub in ["train", "Apple___Apple_scab"]):
        data_dir = nested_dir

    print(f"--> Reading images from: {data_dir}")
    full_dataset = datasets.ImageFolder(data_dir)
    class_names = full_dataset.classes

    # Subsample if max_samples_per_class is requested
    if max_samples_per_class and max_samples_per_class > 0:
        print(f"--> Balancing dataset to max {max_samples_per_class} images per class (CPU optimized)...")
        class_indices = {i: [] for i in range(len(class_names))}
        for idx, (_, target) in enumerate(full_dataset.samples):
            if len(class_indices[target]) < max_samples_per_class:
                class_indices[target].append(idx)

        selected_indices = []
        for idxs in class_indices.values():
            selected_indices.extend(idxs)

        dataset_to_split = Subset(full_dataset, selected_indices)
        total_samples = len(selected_indices)
    else:
        dataset_to_split = full_dataset
        total_samples = len(full_dataset)

    val_size = max(int(total_samples * val_split), 1)
    train_size = total_samples - val_size

    generator = torch.Generator().manual_seed(42)
    train_subset, val_subset = random_split(dataset_to_split, [train_size, val_size], generator=generator)

    train_dataset = TransformDataset(train_subset, train_transform)
    val_dataset = TransformDataset(val_subset, val_transform)

    print(f"--> Dataset ready: {train_size} training samples, {val_size} validation samples across {len(class_names)} classes.")

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers
    )

    return train_loader, val_loader, class_names
