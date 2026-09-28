"""
Plant disease knowledge base providing descriptions, symptoms, causes,
and actionable organic/chemical remedies for detected leaf conditions.
Tailored specifically for the 23-class PlantVillage dataset.
"""

DISEASE_DATABASE = {
    # ---------------- Apple ----------------
    "Apple___Apple_scab": {
        "crop": "Apple",
        "disease": "Apple Scab",
        "pathogen": "Fungus (Venturia inaequalis)",
        "symptoms": "Olive-green to black velvety spots on leaves, premature leaf drop, dark scabby lesions on fruit.",
        "prevention": "Rake and destroy fallen leaves in autumn. Prune trees to increase sunlight penetration and air circulation.",
        "organic_treatment": "Apply sulfur or copper-based fungicide sprays early in the growing season before bud burst.",
        "chemical_treatment": "Fungicides containing myclobutanil, captan, or mancozeb at the green tip stage."
    },
    "Apple___Black_rot": {
        "crop": "Apple",
        "disease": "Black Rot",
        "pathogen": "Fungus (Botryosphaeria obtusa)",
        "symptoms": "Frogeye leaf spots (brown with purple margins), cankers on limbs, and firm black rot on maturing fruit.",
        "prevention": "Prune out dead wood, twigs, and mummified fruit from trees during dormancy.",
        "organic_treatment": "Copper soap or sulfur sprays during early bloom stages.",
        "chemical_treatment": "Captan or thiophanate-methyl applications during petal fall and cover sprays."
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "disease": "Cedar Apple Rust",
        "pathogen": "Fungus (Gymnosporangium juniperi-virginianae)",
        "symptoms": "Bright yellow-orange or reddish spots on upper leaf surfaces. Orange tubular projections beneath leaves.",
        "prevention": "Remove nearby eastern red cedar or juniper trees if possible; choose rust-resistant apple varieties.",
        "organic_treatment": "Neem oil or sulfur sprays when tree leaves first begin to unfurl.",
        "chemical_treatment": "Myclobutanil, propiconazole, or mancozeb sprays applied from pink bud stage through petal fall."
    },
    "Apple___healthy": {
        "crop": "Apple",
        "disease": "Healthy Apple Leaf",
        "pathogen": "None",
        "symptoms": "Vibrant green leaves with no lesions, curling, or discoloration.",
        "prevention": "Maintain balanced fertilization, consistent drip watering, and regular tree pruning.",
        "organic_treatment": "Not needed. Continue standard preventive care.",
        "chemical_treatment": "Not needed."
    },

    # ---------------- Corn (Maize) ----------------
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn (Maize)",
        "disease": "Gray Leaf Spot",
        "pathogen": "Fungus (Cercospora zeae-maydis)",
        "symptoms": "Rectangular, tan-to-gray lesions restricted by the leaf veins, running parallel along the leaf blade.",
        "prevention": "Rotate crops with non-host species (such as soybeans). Practice deep tillage to bury infected residues.",
        "organic_treatment": "Bio-fungicides containing Bacillus amyloliquefaciens or Trichoderma.",
        "chemical_treatment": "Foliar fungicides such as azoxystrobin, pyraclostrobin, or propiconazole."
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)",
        "disease": "Common Rust",
        "pathogen": "Fungus (Puccinia sorghi)",
        "symptoms": "Small, powdery cinnamon-brown pustules scattered across both upper and lower leaf surfaces.",
        "prevention": "Plant resistant hybrid seeds; avoid excessive overhead irrigation.",
        "organic_treatment": "Neem oil or sulfur sprays during early detection in warm, humid weather.",
        "chemical_treatment": "Triazole or strobilurin-based fungicides if threshold exceeds 5% of leaf area."
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)",
        "disease": "Northern Corn Leaf Blight",
        "pathogen": "Fungus (Exserohilum turcicum)",
        "symptoms": "Large, elongated cigar-shaped grayish-green to tan lesions on lower leaves progressing upwards.",
        "prevention": "Select resistant hybrids; practice 1-2 year crop rotation away from corn.",
        "organic_treatment": "Copper octanoate sprays or bio-fungicide formulations.",
        "chemical_treatment": "Foliar fungicides like Pyraclostrobin + Metconazole applied prior to tasseling."
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)",
        "disease": "Healthy Corn Leaf",
        "pathogen": "None",
        "symptoms": "Uniform deep green foliage, robust stalk, no chlorosis or spotting.",
        "prevention": "Soil testing, optimal nitrogen and phosphorus levels, and adequate moisture.",
        "organic_treatment": "Not needed.",
        "chemical_treatment": "Not needed."
    },

    # ---------------- Pepper Bell ----------------
    "Pepper__bell___Bacterial_spot": {
        "crop": "Bell Pepper",
        "disease": "Bacterial Spot",
        "pathogen": "Bacterium (Xanthomonas campestris pv. vesicatoria)",
        "symptoms": "Water-soaked circular or irregular spots on leaves turning brown with yellow haloes; leaf drop.",
        "prevention": "Use certified pathogen-free seeds; sanitize seedbeds; avoid overhead sprinkler watering.",
        "organic_treatment": "Liquid copper fungicide mixed with potassium bicarbonate applied in early mornings.",
        "chemical_treatment": "Fixed copper bactericides combined with mancozeb for enhanced efficacy."
    },
    "Pepper__bell___healthy": {
        "crop": "Bell Pepper",
        "disease": "Healthy Bell Pepper Leaf",
        "pathogen": "None",
        "symptoms": "Glossy, deep green, smooth leaves with intact margins and vigorous growth.",
        "prevention": "Ensure well-draining warm soil, consistent moisture, and adequate calcium nutrition.",
        "organic_treatment": "Not needed.",
        "chemical_treatment": "Not needed."
    },

    # ---------------- Potato ----------------
    "Potato___Early_blight": {
        "crop": "Potato",
        "disease": "Early Blight",
        "pathogen": "Fungus (Alternaria solani)",
        "symptoms": "Concentric rings ('target board' pattern) inside dark brown spots on older lower leaves, leaf yellowing.",
        "prevention": "Avoid overhead watering; maintain soil fertility; rotate crops with non-solanaceous plants.",
        "organic_treatment": "Copper oxychloride or potassium bicarbonate sprays on lower leaves.",
        "chemical_treatment": "Chlorothalonil, mancozeb, or azoxystrobin fungicides applied every 7-10 days."
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "disease": "Late Blight",
        "pathogen": "Oomycete (Phytophthora infestans)",
        "symptoms": "Water-soaked dark lesions on leaf tips/margins, white mold on undersides during humid weather, rapid death.",
        "prevention": "Plant certified disease-free seed tubers; eliminate volunteer potato plants; avoid overhead sprinkling.",
        "organic_treatment": "Fixed copper fungicides applied preventively before disease spreads.",
        "chemical_treatment": "Fungicides containing metalaxyl, cymoxanil, or mandipropamid."
    },
    "Potato___healthy": {
        "crop": "Potato",
        "disease": "Healthy Potato Leaf",
        "pathogen": "None",
        "symptoms": "Healthy dark green composite leaves free from spots, curling, or wilting.",
        "prevention": "Proper hilling, adequate drip irrigation, and balanced potassium/nitrogen nutrition.",
        "organic_treatment": "Not needed.",
        "chemical_treatment": "Not needed."
    },

    # ---------------- Tomato ----------------
    "Tomato_Bacterial_spot": {
        "crop": "Tomato",
        "disease": "Bacterial Spot",
        "pathogen": "Bacterium (Xanthomonas spp.)",
        "symptoms": "Small, dark greasy spots with yellow halos on leaves; scabby dark specks on green fruits.",
        "prevention": "Use certified disease-free seeds; avoid overhead irrigation; clean garden tools thoroughly.",
        "organic_treatment": "Copper-based bactericides combined with mancozeb; spray early in the morning.",
        "chemical_treatment": "Streptomycin sulphate (where permitted) or fixed copper sprays."
    },
    "Tomato_Early_blight": {
        "crop": "Tomato",
        "disease": "Early Blight",
        "pathogen": "Fungus (Alternaria linariae / solani)",
        "symptoms": "Dark concentric bullseye lesions on lower leaves, surrounded by yellow tissue; lower leaves wither and drop.",
        "prevention": "Mulch around the base of plants to prevent soil splash; prune lower 12 inches of foliage.",
        "organic_treatment": "Neem oil, copper fungicide, or Bacillus subtilis sprays.",
        "chemical_treatment": "Chlorothalonil, mancozeb, or difenoconazole sprays applied at first symptom."
    },
    "Tomato_Late_blight": {
        "crop": "Tomato",
        "disease": "Late Blight",
        "pathogen": "Oomycete (Phytophthora infestans)",
        "symptoms": "Pale green/water-soaked irregular leaf spots turning dark brown with white fuzz beneath; rot on green fruits.",
        "prevention": "Ensure wide plant spacing for airflow; avoid overhead watering; remove infected plants immediately.",
        "organic_treatment": "Preventive copper sprays before cool, wet weather sets in.",
        "chemical_treatment": "Systemic fungicides like cymoxanil, fluopicolide, or metalaxyl-M."
    },
    "Tomato_Leaf_Mold": {
        "crop": "Tomato",
        "disease": "Leaf Mold",
        "pathogen": "Fungus (Passalora fulva)",
        "symptoms": "Pale green or yellowish spots on upper leaf surfaces; velvety olive-green to brown mold on the undersides.",
        "prevention": "Reduce humidity in greenhouses; space plants out; increase ventilation.",
        "organic_treatment": "Bio-fungicides like Bacillus subtilis; copper soap sprays.",
        "chemical_treatment": "Chlorothalonil, thiophanate-methyl, or azoxystrobin."
    },
    "Tomato_Septoria_leaf_spot": {
        "crop": "Tomato",
        "disease": "Septoria Leaf Spot",
        "pathogen": "Fungus (Septoria lycopersici)",
        "symptoms": "Numerous small circular brown spots with grayish-white centers and dark brown borders; starts on lower foliage.",
        "prevention": "Mulch base to stop soil splash; avoid handling plants when wet; practice 3-year crop rotation.",
        "organic_treatment": "Copper octanoate or sulfur sprays.",
        "chemical_treatment": "Chlorothalonil or mancozeb applied at 7-10 day intervals."
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "crop": "Tomato",
        "disease": "Two-Spotted Spider Mite Infestation",
        "pathogen": "Pest (Tetranychus urticae)",
        "symptoms": "Yellow stippling/speckling on leaf tops; fine silken webbing on leaf undersides and stem joints; leaves turn bronze.",
        "prevention": "Avoid drought stress; rinse dust off plants; maintain beneficial insect habitats.",
        "organic_treatment": "Insecticidal soap, neem oil, or horticultural oils; release predatory mites (Phytoseiulus persimilis).",
        "chemical_treatment": "Acaricides / miticides like abamectin, bifenazate, or spiromesifen."
    },
    "Tomato__Target_Spot": {
        "crop": "Tomato",
        "disease": "Target Spot",
        "pathogen": "Fungus (Corynespora cassiicola)",
        "symptoms": "Small circular brown spots with lighter centers; pinpoint lesions expand with concentric zones and yellow halos.",
        "prevention": "Improve airflow; avoid excessive nitrogen fertilizer; destroy diseased crop refuse.",
        "organic_treatment": "Copper-based fungicides applied preventively.",
        "chemical_treatment": "Fungicides containing boscalid, chlorothalonil, or pyraclostrobin."
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "crop": "Tomato",
        "disease": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "pathogen": "Virus (transmitted by Whiteflies - Bemisia tabaci)",
        "symptoms": "Severe upward leaf curling, yellowing of leaf margins, stunted plant growth, failure to set fruit.",
        "prevention": "Control whiteflies using yellow sticky cards, insect netting, and reflective mulches; plant TYLCV-resistant varieties.",
        "organic_treatment": "Insecticidal soaps and neem oil to suppress whitefly vectors.",
        "chemical_treatment": "Systemic insecticides (e.g. imidacloprid, acetamiprid) targeting vector populations."
    },
    "Tomato__Tomato_mosaic_virus": {
        "crop": "Tomato",
        "disease": "Tomato Mosaic Virus (ToMV)",
        "pathogen": "Tobamovirus (highly contagious via physical contact)",
        "symptoms": "Mottled light and dark green patterns on leaves, leaf distortion (shoestringing), internal browning of fruit.",
        "prevention": "Wash hands with milk or soap before handling; disinfect tools; do not smoke near tomato plants.",
        "organic_treatment": "No cure once infected; promptly pull and burn infected plants to protect remaining crops.",
        "chemical_treatment": "No chemical virucide exists."
    },
    "Tomato_healthy": {
        "crop": "Tomato",
        "disease": "Healthy Tomato Leaf",
        "pathogen": "None",
        "symptoms": "Crisp green serrated leaves with no spots, blotches, or yellowing.",
        "prevention": "Regular deep watering at base, well-draining soil, full sun, and balanced nutrients.",
        "organic_treatment": "Not needed.",
        "chemical_treatment": "Not needed."
    }
}


def get_disease_details(class_name: str) -> dict:
    """
    Returns disease information matching a class name.
    If exact name is not in database, normalizes naming formats or provides general recommendations.
    """
    # Direct match
    if class_name in DISEASE_DATABASE:
        return DISEASE_DATABASE[class_name]

    # Try fuzzy key match (handling differences in double/triple underscores)
    normalized_query = class_name.replace("___", "_").replace("__", "_").lower()
    for key, val in DISEASE_DATABASE.items():
        if key.replace("___", "_").replace("__", "_").lower() == normalized_query:
            return val

    # Dynamic fallback parser
    cleaned_name = class_name.replace("___", " - ").replace("__", " - ").replace("_", " ").strip()
    is_healthy = "healthy" in class_name.lower()

    if is_healthy:
        return {
            "crop": cleaned_name.split(" - ")[0] if " - " in cleaned_name else "Plant",
            "disease": "Healthy Plant Leaf",
            "pathogen": "None",
            "symptoms": "No visible signs of pathogen infection, pest damage, or nutrient stress.",
            "prevention": "Continue standard routine care: monitor soil moisture, inspect foliage weekly, and maintain good airflow.",
            "organic_treatment": "No treatment required.",
            "chemical_treatment": "No treatment required."
        }
    else:
        parts = cleaned_name.split(" - ")
        crop = parts[0] if len(parts) > 1 else "Plant"
        disease = parts[1] if len(parts) > 1 else cleaned_name

        return {
            "crop": crop,
            "disease": disease,
            "pathogen": "Suspected Fungal / Bacterial / Viral pathogen",
            "symptoms": f"Visible leaf lesions or discoloration typical of {disease}.",
            "prevention": "Prune visibly diseased leaves, avoid watering from above the foliage, and sanitize gardening tools.",
            "organic_treatment": "Isolate the plant and apply broad-spectrum organic copper fungicide or neem oil spray.",
            "chemical_treatment": "Consult a local agricultural extension specialist for approved regional treatment sprays."
        }
