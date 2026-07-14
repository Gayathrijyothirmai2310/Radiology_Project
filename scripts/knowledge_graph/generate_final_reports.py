import os
import json
import pandas as pd

# =====================================================
# Paths
# =====================================================

PROJECT = os.path.expanduser("~/Radiology_Project")

REPORT_CSV = os.path.join(
    PROJECT,
    "outputs",
    "chexagent_reports_100.csv"
)

KG_ERRORS = os.path.join(
    PROJECT,
    "knowledge_graph",
    "kg_errors"
)

RECOMMENDATIONS = os.path.join(
    PROJECT,
    "knowledge_graph",
    "recommendations"
)

OUTPUT_FOLDER = os.path.join(
    PROJECT,
    "knowledge_graph",
    "final_reports"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =====================================================
# Load reports
# =====================================================

reports = pd.read_csv(REPORT_CSV)

print()
print("=" * 60)
print(f"Loaded {len(reports)} reports.")
print("=" * 60)
print()

# =====================================================
# Process each report
# =====================================================

for _, row in reports.iterrows():

    image_id = row["image_id"].replace(".png", "")

    generated_report = str(row["generated_impression"])

    ground_truth = str(row["ground_truth_impression"])

    kg_error_file = os.path.join(
        KG_ERRORS,
        image_id + ".json"
    )

    recommendation_file = os.path.join(
        RECOMMENDATIONS,
        image_id + ".txt"
    )

    if not os.path.exists(kg_error_file):
        continue

    with open(kg_error_file) as f:
        kg = json.load(f)

    recommendation = ""

    if os.path.exists(recommendation_file):

        with open(recommendation_file) as f:
            recommendation = f.read()
    missing = kg["missing_entities"]
    hallucinated = kg["hallucinated_entities"]

    final_report = ""

    final_report += "Original Report\n"
    final_report += "---------------\n"
    final_report += generated_report.strip()

    final_report += "\n\n"

    final_report += "Knowledge Graph Review\n"
    final_report += "----------------------\n"

    if len(missing) == 0 and len(hallucinated) == 0:

        final_report += (
            "No discrepancies were detected between the generated "
            "report and the reference knowledge graph.\n"
        )

    else:

        final_report += (
            "The knowledge graph comparison identified findings "
            "that may require review before finalizing the report.\n\n"
        )

        if len(missing):

            final_report += "Possible missing findings:\n"

            for item in sorted(missing):
                final_report += f"- {item}\n"

            final_report += "\n"

        if len(hallucinated):

            final_report += "Potential unsupported findings:\n"

            for item in sorted(hallucinated):
                final_report += f"- {item}\n"

            final_report += "\n"

    final_report += (
        "Recommendation:\n"
        "Review the above findings against the chest X-ray before "
        "finalizing the report.\n"
    )

    outfile = os.path.join(
        OUTPUT_FOLDER,
        image_id + ".txt"
    )

    with open(outfile, "w") as f:
        f.write(final_report)

print()
print("=" * 60)
print("Finished generating final KG-guided reports.")
print("Saved to:")
print(OUTPUT_FOLDER)
print("=" * 60)
