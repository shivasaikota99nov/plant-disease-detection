"""
Neural Network Architectures for Plant Disease Detection:
1. Custom CNN from scratch (for learning / demonstration of CNN fundamentals)
2. Transfer Learning models (MobileNetV3, ResNet18) for production-grade accuracy
"""

import torch
import torch.nn as nn
from torchvision import models


class CustomCNN(nn.Module):
    """
    Custom 4-block Convolutional Neural Network built from scratch.
    Ideal for academic demonstration and understanding CNN feature extraction.
    """
    def __init__(self, num_classes: int):
        super(CustomCNN, self).__init__()
        
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 224 -> 112

            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 112 -> 56

            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 56 -> 28

            # Block 4
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 28 -> 14
        )
        
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


def get_model(num_classes: int, architecture: str = "mobilenet_v3_small", pretrained: bool = True) -> nn.Module:
    """
    Model factory to create a plant disease detection network.
    Supported architectures:
      - 'mobilenet_v3_small' (Fast, lightweight, high accuracy, recommended)
      - 'resnet18' (Standard deep residual network)
      - 'custom_cnn' (From scratch 4-stage convolutional network)
    """
    arch = architecture.lower()

    if arch == "custom_cnn":
        return CustomCNN(num_classes=num_classes)

    elif arch == "resnet18":
        weights = models.ResNet18_Weights.DEFAULT if pretrained else None
        model = models.resnet18(weights=weights)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes)
        )
        return model

    elif arch == "mobilenet_v3_small":
        weights = models.MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
        model = models.mobilenet_v3_small(weights=weights)
        in_features = model.classifier[0].in_features
        model.classifier = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.Hardswish(inplace=True),
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(256, num_classes)
        )
        return model

    else:
        raise ValueError(f"Unknown architecture: {architecture}. Choose from 'mobilenet_v3_small', 'resnet18', or 'custom_cnn'.")
