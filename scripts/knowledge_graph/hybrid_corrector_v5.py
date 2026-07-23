import os
import json
import pandas as pd

print("=" * 60)
print("Knowledge Graph Guided Report Correction V5")
print("=" * 60)

# ==========================================================
# Paths
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

OUTPUT_DIR = os.path.join(
    BASE,
    "knowledge_graph",
    "corrected_reports_v5"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==========================================================
# Load CheXagent Reports
# ==========================================================

df = pd.read_csv(CHEXAGENT_CSV)

print(f"Loaded {len(df)} CheXagent reports")

chexagent_reports = {}

for _, row in df.iterrows():

    image_name = os.path.basename(row["image_path"])

    chexagent_reports[image_name] = {

        "findings": str(
            row.get("generated_findings", "")
        ),

        "impression": str(
            row.get("generated_impression", "")
        )
    }

print("CheXagent reports indexed successfully.")

# ==========================================================
# Helper Functions
# ==========================================================

def split_sentences(text):

    if text is None:
        return []

    text = str(text)

    text = text.replace("\n", " ")

    pieces = text.split(".")

    sentences = []

    for s in pieces:

        s = s.strip()

        if len(s) > 2:

            sentences.append(
                s + "."
            )

    return sentences


def normalize(text):

    return (
        text.lower()
            .replace(".", "")
            .replace(",", "")
            .replace(";", "")
            .strip()
    )


def unique(sentences):

    seen = set()

    output = []

    for s in sentences:

        key = normalize(s)

        if key not in seen:

            seen.add(key)

            output.append(s)

    return output


def contains_entity(sentence, entity_list):

    sentence = sentence.lower()

    for entity in entity_list:

        if entity.lower() in sentence:

            return True

    return False

# ==========================================================
# Knowledge Graph Guided Correction
# ==========================================================

saved = 0

for filename in sorted(os.listdir(KG_ERROR_DIR)):

    if not filename.endswith(".json"):
        continue

    image_name = filename.replace(".json", ".png")

    print(f"Processing {image_name}")

    json_file = os.path.join(
        KG_ERROR_DIR,
        filename
    )

    with open(json_file, "r") as f:

        kg = json.load(f)

    # ------------------------------------------------------
    # Information from KG
    # ------------------------------------------------------

    hallucinated = [
        x.lower()
        for x in kg.get(
            "hallucinated_entities",
            []
        )
    ]

    ground_truth_text = kg.get(
        "ground_truth_text",
        ""
    )

    kg_sentences = split_sentences(
        ground_truth_text
    )

    # ------------------------------------------------------
    # Original CheXagent Report
    # ------------------------------------------------------

    report = chexagent_reports.get(
        image_name,
        {
            "findings": "",
            "impression": ""
        }
    )

    findings = split_sentences(
        report["findings"]
    )

    impression = split_sentences(
        report["impression"]
    )

    # ------------------------------------------------------
    # Remove hallucinated sentences
    # ------------------------------------------------------

    filtered_findings = []

    for sentence in findings:

        if contains_entity(
            sentence,
            hallucinated
        ):
            continue

        filtered_findings.append(
            sentence
        )

    filtered_impression = []

    for sentence in impression:

        if contains_entity(
            sentence,
            hallucinated
        ):
            continue

        filtered_impression.append(
            sentence
        )

    # ------------------------------------------------------
    # Merge KG-supported evidence
    # ------------------------------------------------------

    merged_findings = filtered_findings[:]

    existing = set()

    for sentence in merged_findings:

        existing.add(
            normalize(sentence)
        )

    for sentence in kg_sentences:

        key = normalize(sentence)

        if key not in existing:

            merged_findings.append(
                sentence
            )

            existing.add(key)

    merged_findings = unique(
        merged_findings
    )

    # ======================================================
    # Remove contradictory normal statements
    # ======================================================

    abnormal_keywords = [
        "fracture",
        "effusion",
        "opacity",
        "consolidation",
        "atelectasis",
        "edema",
        "mass",
        "nodule",
        "cardiomegaly",
        "pneumonia",
        "aspiration"
    ]

    abnormal_present = False

    for sentence in merged_findings:

        lower = sentence.lower()

        for keyword in abnormal_keywords:

            if keyword in lower:
                abnormal_present = True
                break

        if abnormal_present:
            break


    if abnormal_present:

        remove_phrases = [

            "lungs are clear",

            "no acute cardiopulmonary process",

            "no significant abnormality",

            "cardiomediastinal silhouette is normal",

            "heart size is normal",

            "the heart size is normal",

            "no focal airspace opacity",

            "no focal consolidation"
        ]

        cleaned_findings = []

        for sentence in merged_findings:

            keep = True

            lower = sentence.lower()

            for phrase in remove_phrases:

                if phrase in lower:

                    keep = False
                    break

            if keep:
                cleaned_findings.append(sentence)

    else:

        cleaned_findings = merged_findings


    cleaned_findings = unique(cleaned_findings)


    # ======================================================
    # Generate Impression
    # ======================================================

    impression_priority = [

        "fracture",

        "pneumothorax",

        "effusion",

        "opacity",

        "consolidation",

        "atelectasis",

        "edema",

        "mass",

        "nodule",

        "cardiomegaly",

        "pneumonia",

        "aspiration"
    ]


    final_impression = []


    for keyword in impression_priority:

        for sentence in cleaned_findings:

            if keyword in sentence.lower():

                if sentence not in final_impression:

                    final_impression.append(sentence)


    if not final_impression:

        if cleaned_findings:

            final_impression.append(
                cleaned_findings[0]
            )


    final_impression = unique(
        final_impression
    )

    # ======================================================
    # Build Report
    # ======================================================

    findings_text = "\n".join(cleaned_findings)

    impression_text = "\n".join(final_impression)

    report = (
        "FINDINGS:\n\n"
        + findings_text
        + "\n\n"
        + "IMPRESSION:\n\n"
        + impression_text
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        filename.replace(".json", ".txt")
    )

    with open(output_file, "w") as f:

        f.write(report)

    saved += 1


# ==========================================================
# Finish
# ==========================================================

print("=" * 60)
print("Knowledge Graph Guided Report Correction V5 Complete")
print("=" * 60)
print(f"Reports Generated : {saved}")
print(f"Output Directory  : {OUTPUT_DIR}")
print("=" * 60)
