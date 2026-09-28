# 🌿 Plant Disease Detection & Advisory System

An end-to-end Deep Learning system built with PyTorch and Streamlit that identifies plant leaf diseases from photos and delivers actionable treatment and prevention advice.

---

## 📁 Project Architecture

```
plant-disease-detection/
├── app.py                      # Streamlit interactive web interface
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── models/                     # Saved model checkpoints & metrics
│   ├── plant_disease_model.pth # Best trained model weights
│   ├── class_names.json        # Class label mapping
│   └── training_metrics.png    # Training loss & accuracy curves
└── src/
    ├── __init__.py
    ├── dataset.py              # Data loading, train-val split & augmentations
    ├── model.py                # MobileNetV3 / ResNet18 / Custom CNN architectures
    ├── train.py                # Training pipeline with learning rate scheduling
    └── disease_info.py         # Knowledge base of symptoms & remedies
```

---

## 🚀 Quick Start Guide

### 1. Training the Model
To train the CNN on your dataset:
```bash
py src/train.py --data_dir "PATH_TO_YOUR_DATASET" --epochs 10 --batch_size 32
```

Optional training arguments:
- `--arch`: `mobilenet_v3_small` (default, fast & high accuracy), `resnet18`, or `custom_cnn`
- `--epochs`: Number of passes through the dataset (e.g. 10 or 15)
- `--batch_size`: Batch size (e.g. 16, 32, or 64)
- `--lr`: Learning rate (default `0.001`)

### 2. Running the Web Application
Once trained (or while testing):
```bash
py -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌟 Key Features
- **Accurate CNN Diagnosis**: Utilizes transfer learning with MobileNetV3 or custom CNN for high classification accuracy.
- **Data Augmentation**: Flips, rotations, color jitter, and random scaling to prevent overfitting on varied lighting/angles.
- **Actionable Treatment Plans**:
  - Pathogen identification (fungal, bacterial, viral, or pest)
  - Cultural prevention methods
  - Eco-friendly organic remedies (neem oil, copper fungicides, biocontrol)
  - Approved chemical treatments for emergency outbreaks
- **Interactive UI**: Drag-and-drop leaf upload, probability scores, top-3 candidates, and searchable plant disease library.
