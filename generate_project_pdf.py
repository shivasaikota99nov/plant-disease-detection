"""
Script to generate a professional, beautifully styled Project Guide & Viva Prep PDF
for the Plant Disease Detection and Advisory System.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Adds page numbers and header/footer to each page."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))

        # Header (pages after page 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Plant Disease Detection System — Project & Viva Guide")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "Confidential — For Internal Project Presentation & Viva Prep")
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)

        self.restoreState()


def create_pdf(output_filename="Plant_Disease_Detection_Project_Guide.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1b5e20"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#444444"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2e7d32"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1565c0"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=6
    )

    quote_style = ParagraphStyle(
        'Quote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1b5e20"),
        leftIndent=12,
        rightIndent=12,
        spaceAfter=8
    )

    q_style = ParagraphStyle(
        'VivaQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#b71c1c"),
        spaceBefore=8,
        spaceAfter=2,
        keepWithNext=True
    )

    a_style = ParagraphStyle(
        'VivaA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#263238"),
        leftIndent=8,
        spaceAfter=8
    )

    elements = []

    # ---------------- TITLE & HEADER ----------------
    elements.append(Paragraph("🌿 Plant Disease Detection & Advisory System", title_style))
    elements.append(Paragraph("<b>Complete Project Architecture, File Guide & Viva Preparation Notes</b><br/>Written in Simple Vocabulary for Group Study & Professor Presentation", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2e7d32"), spaceAfter=14))

    # ---------------- 1. EXECUTIVE SUMMARY ----------------
    elements.append(Paragraph("1. Project Overview (In Simple Words)", h1_style))
    elements.append(Paragraph(
        "<b>What is this project?</b><br/>"
        "This project is an AI-powered system that helps farmers and gardeners quickly identify plant diseases from leaf photos. "
        "A user simply takes a picture of a diseased leaf and uploads it to our web interface. "
        "The system diagnoses the exact disease, shows how confident it is, and immediately gives practical organic and chemical treatment advice.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Key Achievements:</b><br/>"
        "• Trained on <b>23 plant categories</b> (Apple, Tomato, Potato, Corn, Bell Pepper) covering healthy leaves and various diseases.<br/>"
        "• Achieved <b>84.42% validation accuracy</b> using MobileNetV3 deep learning architecture.<br/>"
        "• Built an interactive <b>Streamlit web application</b> with built-in demo sample images for quick live demonstrations.",
        body_style
    ))

    # Architecture Table
    arch_data = [
        [Paragraph("<b>Layer</b>", body_style), Paragraph("<b>Files Involved</b>", body_style), Paragraph("<b>Function in Simple Terms</b>", body_style)],
        [Paragraph("<b>1. Data Layer</b>", body_style), Paragraph("src/dataset.py", body_style), Paragraph("Loads images, creates an 80/20 train-test split, and applies data augmentation (rotations/flips).", body_style)],
        [Paragraph("<b>2. Model & Brain</b>", body_style), Paragraph("src/model.py<br/>src/train.py", body_style), Paragraph("Defines the Convolutional Neural Network (CNN) and trains it to recognize disease patterns.", body_style)],
        [Paragraph("<b>3. User Interface</b>", body_style), Paragraph("app.py<br/>src/disease_info.py", body_style), Paragraph("Interactive website where users upload photos, see predictions, and read remedy instructions.", body_style)],
        [Paragraph("<b>4. Utilities</b>", body_style), Paragraph("predict.py<br/>run_app.bat", body_style), Paragraph("Tools to run tests from command line and launch the web app with a double-click.", body_style)]
    ]
    t_arch = Table(arch_data, colWidths=[90, 100, 314])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e8f5e9")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#1b5e20")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_arch)
    elements.append(Spacer(1, 14))

    # ---------------- 2. FILE BY FILE EXPLANATION ----------------
    elements.append(Paragraph("2. File-by-File Breakdown: Use and Explanation", h1_style))
    elements.append(Paragraph("Here is what every file in the project does, and exactly what to say when your professor asks about it.", body_style))

    # File 1: app.py
    elements.append(Paragraph("📄 1. app.py — The Web User Interface", h2_style))
    elements.append(Paragraph(
        "• <b>What it is:</b> The main web dashboard built with Python's <b>Streamlit</b> framework.<br/>"
        "• <b>What it does:</b> It gives the user a clean website where they can drag and drop a leaf image or pick from pre-loaded sample leaves. "
        "It sends the image to our trained model, gets the disease prediction and probability score, and displays the causes, symptoms, and organic/chemical treatments.<br/>"
        "• <b>What to say to your professor:</b>", body_style
    ))
    elements.append(Paragraph("🗣️ <i>'Sir, app.py is our presentation and deployment layer. It runs a lightweight Streamlit web server that accepts leaf photos, executes PyTorch inference in real time, and renders clear diagnosis and remedies.'</i>", quote_style))

    # File 2: src/model.py
    elements.append(Paragraph("📄 2. src/model.py — Neural Network Architectures", h2_style))
    elements.append(Paragraph(
        "• <b>What it is:</b> The blueprint of the deep learning model.<br/>"
        "• <b>What it does:</b> It contains the code for <b>MobileNetV3-Small</b> (Transfer Learning), a <b>Custom 4-block CNN built from scratch</b>, and <b>ResNet18</b>. "
        "We chose MobileNetV3 because it is lightweight and designed to run fast on normal computers and mobile devices while still giving high accuracy.<br/>"
        "• <b>What to say to your professor:</b>", body_style
    ))
    elements.append(Paragraph("🗣️ <i>'In model.py, we implemented MobileNetV3 using Transfer Learning. It uses depthwise separable convolutions which drastically reduces the number of parameters, making it fast and accurate.'</i>", quote_style))

    # File 3: src/dataset.py
    elements.append(Paragraph("📄 3. src/dataset.py — Data Pipeline & Augmentation", h2_style))
    elements.append(Paragraph(
        "• <b>What it is:</b> The data loading and preprocessing module.<br/>"
        "• <b>What it does:</b> It scans the dataset folder, automatically splits data into <b>80% training</b> and <b>20% validation</b>, "
        "and applies <b>Data Augmentation</b> (random rotation, horizontal flip, vertical flip, brightness and contrast adjustments). "
        "This teaches the model to recognize leaves even when photos are taken from odd angles or under different lighting.<br/>"
        "• <b>What to say to your professor:</b>", body_style
    ))
    elements.append(Paragraph("🗣️ <i>'This file builds our PyTorch DataLoader pipeline. We implemented data augmentation and normalized images with ImageNet statistics to ensure the model generalizes well and does not overfit.'</i>", quote_style))

    # File 4: src/train.py
    elements.append(Paragraph("📄 4. src/train.py — Training & Optimization Pipeline", h2_style))
    elements.append(Paragraph(
        "• <b>What it is:</b> The script that actually trains the AI model.<br/>"
        "• <b>What it does:</b> It passes images through the network, calculates error using <b>Cross-Entropy Loss</b>, and updates weights using the <b>AdamW optimizer</b>. "
        "It includes a Learning Rate Scheduler that slows down learning when improvements stall, saves the best model checkpoint to <code>models/plant_disease_model.pth</code>, and plots the loss/accuracy curves.<br/>"
        "• <b>What to say to your professor:</b>", body_style
    ))
    elements.append(Paragraph("🗣️ <i>'train.py manages the training loop and backpropagation. It tracks validation loss epoch by epoch and automatically saves only the best performing checkpoint.'</i>", quote_style))

    elements.append(PageBreak())

    # File 5: src/disease_info.py
    elements.append(Paragraph("📄 5. src/disease_info.py — Agricultural Knowledge Base", h2_style))
    elements.append(Paragraph(
        "• <b>What it is:</b> A dictionary and database containing expert remedy information for all 23 plant classes.<br/>"
        "• <b>What it does:</b> Normal image classifiers only output a raw label like 'Tomato_Early_blight'. "
        "This file translates that label into helpful advice: the name of the fungus, visual symptoms, preventive farming steps, organic eco-friendly sprays (like Neem oil), and chemical fungicides.<br/>"
        "• <b>What to say to your professor:</b>", body_style
    ))
    elements.append(Paragraph("🗣️ <i>'This module converts our deep learning output into an actionable farmer advisory system, bridging raw computer vision with practical agricultural science.'</i>", quote_style))

    # File 6: predict.py
    elements.append(Paragraph("📄 6. predict.py — Quick Command-Line Testing Tool", h2_style))
    elements.append(Paragraph(
        "• <b>What it is:</b> A standalone script to test single leaf images in the terminal without opening a browser.<br/>"
        "• <b>What it does:</b> You run <code>py predict.py --image path/to/leaf.jpg</code>, and it immediately outputs the prediction, confidence percentage, and remedies in the terminal.<br/>"
        "• <b>What to say to your professor:</b>", body_style
    ))
    elements.append(Paragraph("🗣️ <i>'predict.py is our headless command-line inference script. It is useful for automated testing, batch processing, or integrating with external mobile APIs.'</i>", quote_style))

    # File 7 & 8: Models folder & bat
    elements.append(Paragraph("📄 7. run_app.bat & requirements.txt", h2_style))
    elements.append(Paragraph(
        "• <b>run_app.bat:</b> A Windows batch script that allows anyone to double-click and launch the web app instantly.<br/>"
        "• <b>requirements.txt:</b> Lists exact Python packages (torch, torchvision, streamlit, pillow, matplotlib) so anyone can install and run the project.",
        body_style
    ))

    elements.append(Paragraph("📁 8. The models/ Folder Files", h2_style))
    elements.append(Paragraph(
        "• <b>plant_disease_model.pth:</b> The saved 'brain' of the model. It contains millions of learned numbers (weights and biases). That is why VS Code shows it as a binary file—it is meant to be loaded by PyTorch, not read as text.<br/>"
        "• <b>class_names.json:</b> A list that matches class numbers (0 to 22) with real plant names.<br/>"
        "• <b>training_metrics.png:</b> The saved graph showing training/validation loss dropping and accuracy rising across epochs.",
        body_style
    ))
    elements.append(Spacer(1, 10))

    # ---------------- 3. VIVA QUESTIONS & ANSWERS ----------------
    elements.append(Paragraph("3. Top 12 Viva Questions & Answers (Simple & Direct)", h1_style))
    elements.append(Paragraph("Study these questions with your group members. Professors frequently ask these exact concepts:", body_style))

    viva_qa = [
        (
            "Q1: What is the main aim/objective of your project?",
            "The main objective is to detect plant leaf diseases early and accurately using deep learning, and to provide farmers with immediate organic and chemical remedy recommendations through an easy-to-use web interface."
        ),
        (
            "Q2: Why did you use a Convolutional Neural Network (CNN) instead of traditional Machine Learning (like Random Forest or SVM)?",
            "Traditional machine learning requires manual feature extraction (measuring shapes, color histograms, texture manually), which fails when lighting or leaf orientation changes. CNNs automatically learn visual features (edges, spots, patterns) directly from raw image pixels layer by layer."
        ),
        (
            "Q3: What is Transfer Learning, and why did you use MobileNetV3?",
            "Transfer learning means taking a model already trained on millions of images (ImageNet) and fine-tuning it on our plant dataset. Instead of learning basic shapes from scratch, it already understands image fundamentals. We chose MobileNetV3 because it is lightweight, fast, and designed to run efficiently on standard computers without needing an expensive GPU."
        ),
        (
            "Q4: What is the difference between Training Accuracy and Validation Accuracy?",
            "Training accuracy measures how well the model predicts images it has already seen during practice. Validation accuracy measures how well the model performs on new, unseen test images. A high validation accuracy (like our 84.42%) proves that the model genuinely learned rather than just memorizing."
        ),
        (
            "Q5: How did you prevent Overfitting in your model?",
            "We used three main techniques: (1) Data Augmentation (random flips, rotations, and color jitter) so the model sees different variations of leaves; (2) A Dropout layer (0.3) in the classifier head to randomly turn off neurons and prevent over-reliance; and (3) A Validation split with checkpointing to save only the model with the highest validation score."
        ),
        (
            "Q6: Why is the file 'plant_disease_model.pth' not readable in VS Code?",
            "A .pth file is a serialized binary checkpoint containing millions of floating-point neural network weights and mathematical matrices. It is not plain text or Python code. It is loaded directly into computer memory by PyTorch using torch.load()."
        ),
        (
            "Q7: What Loss Function and Optimizer did you use, and why?",
            "We used Cross-Entropy Loss because it is the standard and most effective loss function for multi-class classification problems. For optimization, we used AdamW (Adam with decoupled weight decay), which dynamically adjusts learning rates for each parameter while preventing weights from growing too large."
        ),
        (
            "Q8: What is the purpose of Data Augmentation in src/dataset.py?",
            "In real life, farmers take photos under different sunlight, angles, and distances. Data augmentation artificially creates these conditions during training by randomly zooming, rotating, and flipping the leaves so the model performs reliably in real-world conditions."
        ),
        (
            "Q9: What dataset did you use and how many classes are there?",
            "We used the PlantVillage dataset containing over 35,000 images across 23 distinct classes. It covers major crops like Tomato, Potato, Apple, Corn, and Bell Pepper, including both healthy leaves and multiple fungal, bacterial, and viral diseases."
        ),
        (
            "Q10: What are the inputs and outputs of your model?",
            "• Input: An RGB leaf photo resized and normalized to (3, 224, 224) pixels.<br/>"
            "• Output: A probability distribution across 23 classes calculated using the Softmax activation function. The class with the highest probability is selected as the diagnosis."
        ),
        (
            "Q11: Why is your project organized into multiple files instead of one big file?",
            "Following software engineering best practices, we separated concerns into distinct modules: data loading, model architecture, training logic, advisory data, and UI. This makes the code readable, reusable, easier to debug, and simple to maintain."
        ),
        (
            "Q12: What are the future enhancements for this project?",
            "1. Deploying as a native Android/iOS mobile app with offline inference.<br/>"
            "2. Adding multi-language support (e.g. Hindi, Telugu, Tamil, Spanish) for local farmers.<br/>"
            "3. Integrating severe weather alerts and pest risk prediction based on GPS location."
        )
    ]

    for q, a in viva_qa:
        elements.append(Paragraph(q, q_style))
        elements.append(Paragraph(f"<b>Answer:</b> {a}", a_style))

    elements.append(Spacer(1, 10))

    # ---------------- 4. DEMO GUIDE ----------------
    elements.append(Paragraph("4. How to Present Your Demo in 2 Minutes", h1_style))
    elements.append(Paragraph(
        "Follow these exact steps when presenting your screen to the evaluators:<br/>"
        "<b>Step 1:</b> Double-click <code>run_app.bat</code> or run <code>py -m streamlit run app.py</code> in VS Code terminal.<br/>"
        "<b>Step 2:</b> Open the browser at <code>http://localhost:8501</code>.<br/>"
        "<b>Step 3:</b> Under 'Quick Demo', select <b>Tomato Early Blight</b> or <b>Apple Scab</b> from the sample dropdown.<br/>"
        "<b>Step 4:</b> Show the confidence score (e.g. <b>99.46%</b>) and open the accordions to show the <b>Organic Remedies</b> (Neem oil, Bacillus subtilis) and <b>Chemical Sprays</b>.<br/>"
        "<b>Step 5:</b> Switch to the <b>'Model Metrics & Curves'</b> tab to show the training accuracy graph, proving your model was trained and evaluated properly.",
        body_style
    ))

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"--> Successfully generated PDF: {output_filename}")


if __name__ == "__main__":
    output_pdf = r"C:\Users\shiva\.gemini\antigravity\scratch\plant-disease-detection\Plant_Disease_Detection_Project_Guide.pdf"
    create_pdf(output_pdf)
