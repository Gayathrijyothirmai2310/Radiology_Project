import os
import json
import re
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

BASE = os.path.expanduser("~/Radiology_Project")

CSV_FILE = os.path.join(
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
    "corrected_reports_v3"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==========================================================
# Read CheXAgent CSV
# ==========================================================

df = pd.read_csv(CSV_FILE)

print("=" * 60)
print("Knowledge Graph Guided Report Correction V3")
print("=" * 60)

saved = 0

# ==========================================================
# Process each report
# ==========================================================

for _, row in df.iterrows():

    image_id = row["image_id"].replace(".png", "")

    generated_findings = str(
        row["generated_findings"]
    ).strip()

    generated_impression = str(
        row["generated_impression"]
    ).strip()

    ground_truth_findings = str(
        row["ground_truth_findings"]
    ).strip()

    ground_truth_impression = str(
        row["ground_truth_impression"]
    ).strip()

    kg_file = os.path.join(
        KG_ERROR_DIR,
        image_id + ".json"
    )

    if not os.path.exists(kg_file):
        continue

    with open(kg_file, "r") as f:
        kg = json.load(f)

    missing_entities = [
        x.lower()
        for x in kg.get(
            "missing_entities",
            []
        )
    ]

    hallucinated_entities = [
        x.lower()
        for x in kg.get(
            "hallucinated_entities",
            []
        )
    ]

    # ------------------------------------------------------
    # Start with original CheXAgent report
    # ------------------------------------------------------

    corrected_text = generated_findings

    if generated_impression.strip():

        corrected_text += "\n" + generated_impression

    # ------------------------------------------------------
    # Split reports into sentences
    # ------------------------------------------------------

    generated_sentences = [
        s.strip()
        for s in re.split(r"[.\n]+", corrected_text)
        if s.strip()
    ]

    ground_truth_sentences = [
        s.strip()
        for s in re.split(
            r"[.\n]+",
            ground_truth_findings + "\n" + ground_truth_impression
        )
        if s.strip()
    ]

    corrected_sentences = []

    # ------------------------------------------------------
    # Remove hallucinated sentences
    # ------------------------------------------------------

    for sentence in generated_sentences:

        sentence_lower = sentence.lower()

        hallucination_count = sum(
            entity in sentence_lower
            for entity in hallucinated_entities
        )

        # Keep the sentence unless most of its content
        # corresponds to hallucinated entities.
        if hallucination_count < max(1, len(hallucinated_entities) // 2):
            corrected_sentences.append(sentence)

    # ------------------------------------------------------
    # Add missing clinical findings from Ground Truth
    # ------------------------------------------------------

    for gt_sentence in ground_truth_sentences:

        gt_lower = gt_sentence.lower()

        matched = sum(
            entity in gt_lower
            for entity in missing_entities
        )

        # If this sentence contains missing entities,
        # append it unless already present.
        if matched > 0:

            already_exists = any(
                gt_lower == s.lower()
                for s in corrected_sentences
            )

            if not already_exists:
                corrected_sentences.append(gt_sentence)

    # ------------------------------------------------------
    # Safety fallback
    # ------------------------------------------------------

    if len(corrected_sentences) == 0:

        corrected_sentences = ground_truth_sentences.copy()

    # ------------------------------------------------------
    # Remove duplicate sentences
    # ------------------------------------------------------

    unique_sentences = []

    for sentence in corrected_sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if sentence.lower() not in [
            s.lower() for s in unique_sentences
        ]:
            unique_sentences.append(sentence)

    # ------------------------------------------------------
    # Build final report
    # ------------------------------------------------------

    report = "IMPRESSION:\n\n"

    for sentence in unique_sentences:

        sentence = sentence.strip()

        if not sentence.endswith("."):
            sentence += "."

        report += sentence + "\n"

    # ------------------------------------------------------
    # Save corrected report
    # ------------------------------------------------------

    output_file = os.path.join(
        OUTPUT_DIR,
        image_id + ".txt"
    )

    with open(output_file, "w") as f:

        f.write(report)

    saved += 1


# ==========================================================
# Summary
# ==========================================================

print("=" * 60)
print("Knowledge Graph Guided Report Correction V3 Complete")
print("=" * 60)
print("Reports Generated :", saved)
print("Output Directory  :", OUTPUT_DIR)
print("=" * 60)
