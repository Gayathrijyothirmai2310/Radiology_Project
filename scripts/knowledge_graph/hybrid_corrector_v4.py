import os
import json
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

BASE = os.path.expanduser("~/Radiology_Project")

CHEXAGENT_CSV = os.path.join(
    BASE,
    "outputs",
    "chexagent_reports_100.csv"
)

KG_ERROR_DIR = os.path.join(
    BASE,
    "knowledge_graph",
    "kg_errors"
)

RECOMMENDATION_DIR = os.path.join(
    BASE,
    "knowledge_graph",
    "recommendations"
)

OUTPUT_DIR = os.path.join(
    BASE,
    "knowledge_graph",
    "corrected_reports_v4"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==========================================================
# Load CheXagent Reports
# ==========================================================

print("=" * 60)
print("Knowledge Graph Guided Report Correction V4")
print("=" * 60)

df = pd.read_csv(CHEXAGENT_CSV)

print(f"Loaded {len(df)} CheXagent reports")

# Create a dictionary for quick lookup
report_lookup = {}

for _, row in df.iterrows():

    report_lookup[row["image_id"]] = {

        "findings": str(
            row["generated_findings"]
        ),

        "impression": str(
            row["generated_impression"]
        )
    }

print("CheXagent reports indexed successfully.")

# ==========================================================
# Helper Functions
# ==========================================================

def clean_text(text):
    """
    Remove extra spaces and blank lines.
    """

    if text is None:
        return ""

    text = str(text)

    text = text.replace("\r", "")

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text.strip()


def split_sentences(text):
    """
    Convert paragraph into sentence list.
    """

    text = clean_text(text)

    sentences = []

    for sentence in text.split("."):

        sentence = sentence.strip()

        if sentence:

            sentences.append(sentence + ".")

    return sentences


def remove_duplicates(sentences):
    """
    Remove repeated sentences while preserving order.
    """

    seen = set()

    output = []

    for sentence in sentences:

        key = sentence.lower().strip()

        if key not in seen:

            seen.add(key)

            output.append(sentence)

    return output
# ==========================================================
# Knowledge Graph Helper Functions
# ==========================================================

def load_kg_errors(image_id):
    """
    Load KG error JSON for one image.
    """

    json_file = os.path.join(
        KG_ERROR_DIR,
        image_id.replace(".png", ".json")
    )

    if not os.path.exists(json_file):
        return None

    with open(json_file) as f:
        return json.load(f)


def load_recommendations(image_id):
    """
    Load recommendation file if available.
    """

    txt_file = os.path.join(
        RECOMMENDATION_DIR,
        image_id.replace(".png", ".txt")
    )

    if not os.path.exists(txt_file):
        return ""

    with open(txt_file) as f:
        return f.read()


def build_correction_sentences(data):
    """
    Convert KG entities into readable clinical sentences.
    """

    findings = []

    if data is None:
        return findings

    entities = [
        x.lower()
        for x in data.get("missing_entities", [])
    ]

    # --------------------------------------------------
    # Rib fracture
    # --------------------------------------------------

    if "fracture" in entities:

        side = ""

        if "right" in entities:
            side = "right"

        elif "left" in entities:
            side = "left"

        rib = ""

        rib_numbers = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "sixth",
            "seventh",
            "eighth",
            "ninth",
            "tenth",
            "eleventh",
            "twelfth"
        ]

        for r in rib_numbers:

            if r in entities:
                rib = r
                break

        location = ""

        for loc in [
            "posterior",
            "anterior",
            "lateral"
        ]:

            if loc in entities:
                location = loc
                break

        modifier = ""

        if "minimally" in entities:
            modifier = "Minimally displaced "

        elif "mildly" in entities:
            modifier = "Mildly displaced "

        sentence = (
            f"{modifier}fracture of the "
            f"{side} {rib} {location} rib."
        )

        sentence = " ".join(sentence.split())

        findings.append(sentence)

    # --------------------------------------------------
    # Pneumothorax
    # --------------------------------------------------

    if "pneumothorax" in entities:

        findings.append(
            "No pneumothorax is identified."
        )

    # --------------------------------------------------
    # Pleural Effusion
    # --------------------------------------------------

    if "effusion" in entities:

        findings.append(
            "Pleural effusion is present."
        )

    # --------------------------------------------------
    # Opacity
    # --------------------------------------------------

    if "opacity" in entities:

        findings.append(
            "Pulmonary opacity is present."
        )

    # --------------------------------------------------
    # Atelectasis
    # --------------------------------------------------

    if "atelectasis" in entities:

        findings.append(
            "Bibasal atelectatic changes are present."
        )

    return remove_duplicates(findings)

# ==========================================================
# Knowledge Graph Helper Functions
# ==========================================================

def load_kg_errors(image_id):
    """
    Load KG error JSON for one image.
    """

    json_file = os.path.join(
        KG_ERROR_DIR,
        image_id.replace(".png", ".json")
    )

    if not os.path.exists(json_file):
        return None

    with open(json_file) as f:
        return json.load(f)


def load_recommendations(image_id):
    """
    Load recommendation file if available.
    """

    txt_file = os.path.join(
        RECOMMENDATION_DIR,
        image_id.replace(".png", ".txt")
    )

    if not os.path.exists(txt_file):
        return ""

    with open(txt_file) as f:
        return f.read()


def build_correction_sentences(data):
    """
    Convert KG entities into readable clinical sentences.
    """

    findings = []

    if data is None:
        return findings

    entities = [
        x.lower()
        for x in data.get("missing_entities", [])
    ]

    # --------------------------------------------------
    # Rib fracture
    # --------------------------------------------------

    if "fracture" in entities:

        side = ""

        if "right" in entities:
            side = "right"

        elif "left" in entities:
            side = "left"

        rib = ""

        rib_numbers = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "sixth",
            "seventh",
            "eighth",
            "ninth",
            "tenth",
            "eleventh",
            "twelfth"
        ]

        for r in rib_numbers:

            if r in entities:
                rib = r
                break

        location = ""

        for loc in [
            "posterior",
            "anterior",
            "lateral"
        ]:

            if loc in entities:
                location = loc
                break

        modifier = ""

        if "minimally" in entities:
            modifier = "Minimally displaced "

        elif "mildly" in entities:
            modifier = "Mildly displaced "

        sentence = (
            f"{modifier}fracture of the "
            f"{side} {rib} {location} rib."
        )

        sentence = " ".join(sentence.split())

        findings.append(sentence)

    # --------------------------------------------------
    # Pneumothorax
    # --------------------------------------------------

    if "pneumothorax" in entities:

        findings.append(
            "No pneumothorax is identified."
        )

    # --------------------------------------------------
    # Pleural Effusion
    # --------------------------------------------------

    if "effusion" in entities:

        findings.append(
            "Pleural effusion is present."
        )

    # --------------------------------------------------
    # Opacity
    # --------------------------------------------------

    if "opacity" in entities:

        findings.append(
            "Pulmonary opacity is present."
        )

    # --------------------------------------------------
    # Atelectasis
    # --------------------------------------------------

    if "atelectasis" in entities:

        findings.append(
            "Bibasal atelectatic changes are present."
        )

    return remove_duplicates(findings)

# ==========================================================
# Findings Editor
# ==========================================================

def update_findings(original_findings,
                    kg_data,
                    correction_sentences):
    """
    Improve the CheXagent findings using the Knowledge Graph.
    """

    findings = split_sentences(original_findings)

    # ----------------------------------------------
    # Remove hallucinated statements
    # ----------------------------------------------

    hallucinated = []

    if kg_data is not None:

        hallucinated = [
            x.lower()
            for x in kg_data.get(
                "hallucinated_entities",
                []
            )
        ]

    cleaned = []

    for sentence in findings:

        lower = sentence.lower()

        remove = False

        for entity in hallucinated:

            if entity in lower:

                remove = True
                break

        if not remove:
            cleaned.append(sentence)

    # ----------------------------------------------
    # Add KG corrections
    # ----------------------------------------------

    for sentence in correction_sentences:

        exists = False

        for current in cleaned:

            if sentence.lower() in current.lower():

                exists = True
                break

        if not exists:

            cleaned.append(sentence)

    # ----------------------------------------------
    # Remove duplicates
    # ----------------------------------------------

    cleaned = remove_duplicates(cleaned)

    return "\n".join(cleaned)

# ==========================================================
# Impression Editor
# ==========================================================

def update_impression(original_impression,
                      kg_data,
                      correction_sentences):
    """
    Improve the CheXagent impression using the Knowledge Graph.
    """

    impression = split_sentences(original_impression)

    hallucinated = []

    if kg_data is not None:

        hallucinated = [
            x.lower()
            for x in kg_data.get(
                "hallucinated_entities",
                []
            )
        ]

    cleaned = []

    # ----------------------------------------------
    # Remove hallucinated impression sentences
    # ----------------------------------------------

    for sentence in impression:

        lower = sentence.lower()

        remove = False

        for entity in hallucinated:

            if entity in lower:

                remove = True
                break

        if not remove:

            cleaned.append(sentence)

    # ----------------------------------------------
    # Add important KG corrections
    # ----------------------------------------------

    important_keywords = [

        "fracture",
        "pneumothorax",
        "effusion",
        "opacity",
        "atelectasis",
        "consolidation",
        "mass",
        "nodule",
        "edema"

    ]

    for sentence in correction_sentences:

        lower = sentence.lower()

        if any(word in lower for word in important_keywords):

            exists = False

            for current in cleaned:

                if sentence.lower() == current.lower():

                    exists = True
                    break

            if not exists:

                cleaned.append(sentence)

    cleaned = remove_duplicates(cleaned)

    # ----------------------------------------------
    # Default impression if empty
    # ----------------------------------------------

    if len(cleaned) == 0:

        cleaned.append(
            "No acute abnormality identified."
        )

    return "\n".join(cleaned)

# ==========================================================
# Generate Corrected Reports
# ==========================================================

saved = 0

for image_id in sorted(report_lookup.keys()):

    print(f"Processing {image_id}")

    # ----------------------------------------------
    # Original CheXagent report
    # ----------------------------------------------

    original_findings = report_lookup[image_id]["findings"]
    original_impression = report_lookup[image_id]["impression"]

    # ----------------------------------------------
    # KG information
    # ----------------------------------------------

    kg_data = load_kg_errors(image_id)

    recommendation = load_recommendations(image_id)

    correction_sentences = build_correction_sentences(
        kg_data
    )

    # ----------------------------------------------
    # Improve report
    # ----------------------------------------------

    final_findings = update_findings(
        original_findings,
        kg_data,
        correction_sentences
    )

    final_impression = update_impression(
        original_impression,
        kg_data,
        correction_sentences
    )

    # ----------------------------------------------
    # Build final report
    # ----------------------------------------------

    report = []

    report.append("FINDINGS:\n")

    report.append(final_findings)

    report.append("\n")

    report.append("IMPRESSION:\n")

    report.append(final_impression)

    # Optional: include KG recommendation
    if recommendation.strip():

        report.append("\n")
        report.append("=" * 60)
        report.append("KNOWLEDGE GRAPH RECOMMENDATION")
        report.append("=" * 60)
        report.append(recommendation)

    report_text = "\n".join(report)

    # ----------------------------------------------
    # Save report
    # ----------------------------------------------

    output_file = os.path.join(
        OUTPUT_DIR,
        image_id.replace(".png", ".txt")
    )

    with open(output_file, "w") as f:

        f.write(report_text)

    saved += 1

# ==========================================================
# Summary
# ==========================================================

print("=" * 60)
print("Knowledge Graph Guided Report Correction V4 Complete")
print("=" * 60)
print("Reports Generated :", saved)
print("Output Directory  :", OUTPUT_DIR)
print("=" * 60)
