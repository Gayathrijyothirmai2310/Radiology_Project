import os
import json
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = os.path.expanduser("~/Radiology_Project")

REPORT_CSV = os.path.join(
    PROJECT_ROOT,
    "outputs",
    "chexagent_reports_100.csv"
)

KG_ERRORS = os.path.join(
    PROJECT_ROOT,
    "knowledge_graph",
    "kg_errors"
)

OUTPUT_FOLDER = os.path.join(
    PROJECT_ROOT,
    "knowledge_graph",
    "hybrid_reports"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================================
# Load reports
# ==========================================================

reports = pd.read_csv(REPORT_CSV)

print("\n============================================================")
print(f"Loaded {len(reports)} reports.")
print("============================================================\n")


# ==========================================================
# Helper Functions
# ==========================================================

def normalize(text):
    """
    Normalize entity names.
    """
    if text is None:
        return ""

    return (
        str(text)
        .replace("_", " ")
        .replace("-", " ")
        .strip()
        .lower()
    )


def pretty_entity(entity):
    """
    Convert entity into readable text.
    """

    entity = normalize(entity)

    mapping = {
        "fracture":
            "Possible fracture may require further review.",

        "pneumothorax":
            "Evaluate for possible pneumothorax.",

        "rib":
            "Review the ribs for possible abnormality.",

        "opacity":
            "Assess for pulmonary opacity.",

        "pleural effusion":
            "Assess for pleural effusion.",

        "atelectasis":
            "Evaluate for possible atelectasis.",

        "consolidation":
            "Assess for pulmonary consolidation.",

        "effusion":
            "Review for pleural effusion.",

        "edema":
            "Evaluate for pulmonary edema.",

        "aspiration":
            "Consider aspiration if clinically appropriate.",

        "tube":
            "Review support device positioning.",

        "ett":
            "Review endotracheal tube position.",

        "chest":
            "Review the chest region carefully."
    }

    if entity in mapping:
        return mapping[entity]

    return entity.capitalize()


def clean_generated_report(report):
    """
    Remove useless reports like 'No.'
    """

    report = str(report).strip()

    bad_reports = {
        "",
        ".",
        "no",
        "no.",
        "none",
        "none.",
        "normal",
        "normal."
    }

    if report.lower() in bad_reports:

        return (
            "The initial AI-generated report was incomplete "
            "and did not contain sufficient clinical information."
        )

    return report

# ==========================================================
# Process every report
# ==========================================================

for _, row in reports.iterrows():

    image_id = str(row["image_id"]).replace(".png", "")

    print(image_id)

    original_report = clean_generated_report(
        row["generated_impression"]
    )

    kg_file = os.path.join(
        KG_ERRORS,
        image_id + ".json"
    )

    # ------------------------------------------------------
    # Skip if KG file is missing
    # ------------------------------------------------------

    if not os.path.exists(kg_file):

        print(f"Missing KG file: {image_id}")
        continue

    with open(kg_file, "r") as f:
        kg = json.load(f)

    # ------------------------------------------------------
    # Read Knowledge Graph errors
    # ------------------------------------------------------

    missing = sorted(
        list(
            set(
                normalize(x)
                for x in kg.get("missing_entities", [])
                if str(x).strip()
            )
        )
    )

    hallucinated = sorted(
        list(
            set(
                normalize(x)
                for x in kg.get("hallucinated_entities", [])
                if str(x).strip()
            )
        )
    )

    missing_relations = kg.get(
        "missing_relations",
        []
    )

    hallucinated_relations = kg.get(
        "hallucinated_relations",
        []
    )

    # ------------------------------------------------------
    # Build report
    # ------------------------------------------------------

    report_lines = []

    report_lines.append("CHEXAGENT REPORT")
    report_lines.append("=" * 60)
    report_lines.append("")
    report_lines.append(original_report)
    report_lines.append("")
    report_lines.append("KNOWLEDGE GRAPH REVIEW")
    report_lines.append("=" * 60)
    report_lines.append("")

    # ======================================================
    # Missing Findings
    # ======================================================

    if len(missing) > 0:

        report_lines.append("Potential Missing Findings")
        report_lines.append("-" * 35)

        for entity in missing:
            report_lines.append(f"• {pretty_entity(entity)}")

        report_lines.append("")

    # ======================================================
    # Unsupported Findings
    # ======================================================

    if len(hallucinated) > 0:

        report_lines.append("Potential Unsupported Findings")
        report_lines.append("-" * 35)

        for entity in hallucinated:
            report_lines.append(f"• {entity}")

        report_lines.append("")

    # ======================================================
    # Relation Summary
    # ======================================================

    report_lines.append("Knowledge Graph Summary")
    report_lines.append("-" * 35)

    report_lines.append(
        f"Missing findings detected      : {len(missing)}"
    )

    report_lines.append(
        f"Unsupported findings detected : {len(hallucinated)}"
    )

    report_lines.append(
        f"Missing relations detected    : {len(missing_relations)}"
    )

    report_lines.append(
        f"Unsupported relations detected: {len(hallucinated_relations)}"
    )

    report_lines.append("")

    # ======================================================
    # Recommendation
    # ======================================================

    report_lines.append("Clinical Recommendation")
    report_lines.append("-" * 35)

    if len(missing) == 0 and len(hallucinated) == 0:

        report_lines.append(
            "The AI-generated report is fully consistent with the Knowledge Graph."
        )

    else:

        if len(missing) > 0:
            report_lines.append(
                "• Review the potentially missing findings before finalizing the report."
            )

        if len(hallucinated) > 0:
            report_lines.append(
                "• Verify unsupported findings against the chest X-ray."
            )

        report_lines.append(
            "• The Knowledge Graph provides decision support only and should be interpreted together with image review."
        )

    report_lines.append("")
    report_lines.append("=" * 60)
    report_lines.append("End of Knowledge Graph Review")

    # ======================================================
    # Save report
    # ======================================================

    output_file = os.path.join(
        OUTPUT_FOLDER,
        image_id + ".txt"
    )

    with open(output_file, "w") as f:
        f.write("\n".join(report_lines))

print("\n============================================================")
print("Finished generating hybrid reports.")
print(f"Saved to: {OUTPUT_FOLDER}")
print("============================================================")
