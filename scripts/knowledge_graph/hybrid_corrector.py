import os
import json
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

BASE = os.path.expanduser("~/Radiology_Project")

REPORT_CSV = os.path.join(
    BASE,
    "outputs",
    "chexagent_reports_100.csv"
)

KG_ERRORS = os.path.join(
    BASE,
    "knowledge_graph",
    "kg_errors"
)

OUTPUT_DIR = os.path.join(
    BASE,
    "knowledge_graph",
    "corrected_reports"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# Load reports
# ==========================================================

df = pd.read_csv(REPORT_CSV)

print(f"\nLoaded {len(df)} reports.\n")

saved = 0

# ==========================================================
# Helper functions
# ==========================================================

def remove_hallucinations(text, hallucinations):
    """
    Remove hallucinated entity words from the report.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    for word in hallucinations:
        text = text.replace(word, "")
        text = text.replace(word.capitalize(), "")

    return " ".join(text.split())


def add_missing_findings(text, missing_entities):
    """
    Add clinically important missing entities.
    """

    important = {
        "fracture",
        "rib",
        "pneumothorax",
        "effusion",
        "opacity",
        "edema",
        "atelectasis",
        "consolidation",
        "cardiomegaly",
        "mass",
        "nodule",
        "pleural",
        "pneumonia",
        "collapse"
    }

    findings = []

    for entity in missing_entities:

        entity = entity.lower()

        if entity in important:
            findings.append(entity)

    findings = sorted(list(set(findings)))

    if findings:
        text += "\n\nPossible missing findings: "
        text += ", ".join(findings)
        text += "."

    return text


# ==========================================================
# Process reports
# ==========================================================

for _, row in df.iterrows():

    # Remove ".png"
    image_id = os.path.splitext(str(row["image_id"]))[0]

    report = row["generated_impression"]

    error_file = os.path.join(
        KG_ERRORS,
        image_id + ".json"
    )

    if not os.path.exists(error_file):
        print(f"Skipping {image_id} (KG file missing)")
        continue

    with open(error_file, "r") as f:
        errors = json.load(f)

    hallucinated = errors.get("hallucinated_entities", [])
    missing = errors.get("missing_entities", [])

    corrected = remove_hallucinations(
        report,
        hallucinated
    )

    corrected = add_missing_findings(
        corrected,
        missing
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        image_id + ".txt"
    )

    with open(output_file, "w") as f:
        f.write(corrected)

    saved += 1

# ==========================================================
# Done
# ==========================================================

print("\n" + "=" * 60)
print(f"Saved {saved} corrected reports.")
print(f"Folder : {OUTPUT_DIR}")
print("=" * 60)
