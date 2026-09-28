"""
Standalone CLI Inference Script for Plant Disease Prediction.
Usage:
    py predict.py --image "path/to/leaf.jpg"
"""

import os
import sys
import json
import argparse
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from src.model import get_model
from src.disease_info import get_disease_details


def run_prediction(image_path: str, model_path: str = "models/plant_disease_model.pth", class_map_path: str = "models/class_names.json"):
    if not os.path.exists(image_path):
        print(f"Error: Image '{image_path}' not found.")
        return

    if not os.path.exists(model_path) or not os.path.exists(class_map_path):
        print("Error: Trained model weights or class mapping not found in 'models/'. Please train the model first.")
        return

    # Load class labels
    with open(class_map_path, "r") as f:
        class_names = json.load(f)

    # Load Model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(model_path, map_location=device)
    arch = checkpoint.get("architecture", "mobilenet_v3_small")

    model = get_model(num_classes=len(class_names), architecture=arch, pretrained=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    # Preprocess image
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    image = Image.open(image_path).convert("RGB")
    tensor = preprocess(image).unsqueeze(0).to(device)

    # Inference
    with torch.no_grad():
        outputs = model(tensor)
        probs = F.softmax(outputs, dim=1)[0]

    top_prob, top_idx = torch.topk(probs, k=1)
    predicted_class = class_names[top_idx[0].item()]
    confidence = top_prob[0].item() * 100

    info = get_disease_details(predicted_class)

    print("\n" + "=" * 55)
    print("🌿 Plant Disease Diagnosis Result")
    print("=" * 55)
    print(f"Target Crop:       {info['crop']}")
    print(f"Condition:         {info['disease']}")
    print(f"Confidence:        {confidence:.2f}%")
    print(f"Pathogen:          {info['pathogen']}")
    print(f"Symptoms:          {info['symptoms']}")
    print("-" * 55)
    print(f"Prevention:        {info['prevention']}")
    print(f"Organic Remedy:    {info['organic_treatment']}")
    print(f"Chemical Spray:    {info['chemical_treatment']}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict Plant Disease from Leaf Image")
    parser.add_argument("--image", type=str, required=True, help="Path to input image file")
    parser.add_argument("--model", type=str, default="models/plant_disease_model.pth", help="Path to trained model checkpoint")
    args = parser.parse_args()

    run_prediction(args.image, model_path=args.model)
