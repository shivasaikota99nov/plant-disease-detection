"""
Streamlit Web Application: AI Plant Disease Detection System
Provides leaf disease diagnosis, confidence metrics, and targeted treatment recommendations.
"""

import os
import json
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import streamlit as st

# Local project imports
from src.model import get_model
from src.disease_info import get_disease_details, DISEASE_DATABASE

# Page Configuration
st.set_page_config(
    page_title="PlantGuard AI - Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #2e7d32;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f1f8e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .alert-card {
        background-color: #ffebee;
        border-left: 5px solid #e53935;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .healthy-card {
        background-color: #e8f5e9;
        border-left: 5px solid #2e7d32;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .stProgress > div > div > div > div {
        background-color: #4caf50;
    }
</style>
""", unsafe_allow_html=True)


MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "plant_disease_model.pth")
CLASS_MAP_PATH = os.path.join(MODEL_DIR, "class_names.json")
METRICS_PATH = os.path.join(MODEL_DIR, "training_metrics.png")


@st.cache_resource
def load_trained_model():
    """Loads model weights and class labels from the models directory."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(CLASS_MAP_PATH):
        return None, None, None

    with open(CLASS_MAP_PATH, "r") as f:
        class_names = json.load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(MODEL_PATH, map_location=device)
    
    arch = checkpoint.get("architecture", "mobilenet_v3_small")
    num_classes = len(class_names)

    model = get_model(num_classes=num_classes, architecture=arch, pretrained=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    return model, class_names, checkpoint


def predict_image(image: Image.Image, model, class_names, top_k=3):
    """Preprocesses input image and returns top-k predictions."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    img_tensor = preprocess(image.convert("RGB")).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)[0]

    top_probs, top_indices = torch.topk(probs, k=min(top_k, len(class_names)))
    
    results = []
    for prob, idx in zip(top_probs, top_indices):
        results.append({
            "class_name": class_names[idx.item()],
            "confidence": float(prob.item() * 100)
        })
    return results


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?auto=format&fit=crop&w=600&q=80", use_container_width=True)
    st.markdown("### 🌿 PlantGuard AI")
    st.markdown("An intelligent computer vision system for real-time crop disease diagnosis.")
    
    st.divider()

    model, class_names, checkpoint = load_trained_model()
    if model is not None:
        st.success(" Model Status: **Online & Loaded**")
        st.write(f"**Architecture:** `{checkpoint.get('architecture', 'MobileNetV3')}`")
        st.write(f"**Trained Classes:** `{len(class_names)}`")
        if "accuracy" in checkpoint:
            st.write(f"**Validation Accuracy:** `{checkpoint['accuracy']:.2f}%`")
    else:
        st.warning(" Model Status: **No Trained Weights Found**")
        st.info("Train a model using the `Train New Model` tab or run `python src/train.py --data_dir <path>`")

    st.divider()
    st.markdown("#### Hardware & Runtime")
    st.write(f"Device: `{'CUDA GPU' if torch.cuda.is_available() else 'CPU'}`")


# ---------------- MAIN HEADER ----------------
st.markdown("<div class='main-header'>🌿 Plant Disease Detection & Advisory System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Upload a photo of a crop or plant leaf to diagnose diseases and view organic & chemical treatments.</div>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs([" Leaf Diagnosis", " Model Metrics & Curves", " Disease Knowledge Base"])

# ---------------- TAB 1: DIAGNOSIS ----------------
with tab1:
    col_upload, col_result = st.columns([1, 1.2], gap="large")

    with col_upload:
        st.markdown("### 1. Upload or Select Leaf Photo")

        # Sample images option
        sample_dir = os.path.join(os.path.dirname(__file__), "sample_leaves")
        sample_options = ["None (Upload my own image)"]
        if os.path.exists(sample_dir):
            sample_options += [f for f in os.listdir(sample_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        selected_sample = st.selectbox("Quick Demo: Pick a pre-loaded sample leaf", sample_options)

        uploaded_file = st.file_uploader(
            "Or upload your own leaf photo (JPG, JPEG, PNG)...",
            type=["jpg", "jpeg", "png"]
        )

        image = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Leaf Image", use_container_width=True)
        elif selected_sample != "None (Upload my own image)":
            sample_path = os.path.join(sample_dir, selected_sample)
            image = Image.open(sample_path)
            clean_sample_name = selected_sample.replace('_sample.jpg', '').replace('___', ' - ').replace('_', ' ')
            st.image(image, caption=f"Sample: {clean_sample_name}", use_container_width=True)
        else:
            st.info("💡 Tip: For best accuracy, capture the leaf under even lighting with the diseased area clearly visible.")

    with col_result:
        st.markdown("### 2. Diagnosis Results")
        if image is None:
            st.write("Awaiting image selection or upload...")
        elif model is None:
            st.error("No trained model found! Please train the model first with your dataset.")
        else:
            with st.spinner("Analyzing leaf with Convolutional Neural Network..."):
                predictions = predict_image(image, model, class_names, top_k=3)
                top_pred = predictions[0]
                disease_info = get_disease_details(top_pred["class_name"])
                is_healthy = "healthy" in top_pred["class_name"].lower()

            # Result Header Card
            card_class = "healthy-card" if is_healthy else "alert-card"
            st.markdown(
                f"""
                <div class="{card_class}">
                    <h3 style="margin: 0; color: inherit;">{'✅ Healthy Plant' if is_healthy else '⚠️ Disease Detected'}</h3>
                    <h4 style="margin: 0.3rem 0; font-weight: 600;">{disease_info['disease']}</h4>
                    <p style="margin: 0;">Target Crop: <b>{disease_info['crop']}</b> | Confidence: <b>{top_pred['confidence']:.2f}%</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Confidence bar
            st.progress(min(1.0, top_pred["confidence"] / 100.0))

            # Actionable Information Accordions
            with st.expander("🔬 Symptoms & Pathogen Details", expanded=True):
                st.write(f"**Pathogen:** {disease_info.get('pathogen', 'N/A')}")
                st.write(f"**Symptoms:** {disease_info.get('symptoms', 'N/A')}")

            with st.expander("🛡️ Prevention & Cultural Practices", expanded=True):
                st.write(disease_info.get("prevention", "Ensure good sanitation and proper spacing."))

            with st.expander("🌱 Organic Remedies (Eco-Friendly)", expanded=True):
                st.write(disease_info.get("organic_treatment", "Apply neem oil or biological fungicides."))

            with st.expander("💊 Chemical Treatment (If Outbreak Persists)"):
                st.write(disease_info.get("chemical_treatment", "Consult local extension services."))

            # Alternative Predictions
            if len(predictions) > 1:
                st.markdown("#### Top Predictions Comparison")
                for pred in predictions:
                    c_name = pred['class_name'].replace('___', ' - ').replace('_', ' ')
                    st.write(f"- **{c_name}**: `{pred['confidence']:.2f}%`")


# ---------------- TAB 2: METRICS ----------------
with tab2:
    st.markdown("### Model Architecture & Training Curves")
    if os.path.exists(METRICS_PATH):
        st.image(METRICS_PATH, caption="Loss and Accuracy Curves across Training Epochs", use_container_width=True)
    else:
        st.info("Training history chart will appear here once you train a model.")

    if class_names:
        st.markdown(f"#### Recognized Classes ({len(class_names)} Categories)")
        cols = st.columns(3)
        for i, c_name in enumerate(class_names):
            clean = c_name.replace("___", " : ").replace("_", " ")
            cols[i % 3].write(f"• `{clean}`")


# ---------------- TAB 3: KNOWLEDGE BASE ----------------
with tab3:
    st.markdown("### Plant Disease Reference Library")
    search = st.text_input("🔍 Search disease, crop, or symptom...", "")
    
    filtered = {
        k: v for k, v in DISEASE_DATABASE.items()
        if search.lower() in k.lower() or search.lower() in v["disease"].lower() or search.lower() in v["crop"].lower()
    }

    for key, info in filtered.items():
        with st.expander(f"🌿 {info['crop']} - {info['disease']}"):
            st.write(f"**Pathogen:** {info['pathogen']}")
            st.write(f"**Symptoms:** {info['symptoms']}")
            st.write(f"**Prevention:** {info['prevention']}")
            st.write(f"**Organic Treatment:** {info['organic_treatment']}")
            st.write(f"**Chemical Treatment:** {info['chemical_treatment']}")
