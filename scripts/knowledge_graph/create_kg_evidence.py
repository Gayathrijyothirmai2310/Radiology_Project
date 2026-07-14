import os
import json
import pandas as pd

PROJECT = os.path.expanduser("~/Radiology_Project")

REPORTS = os.path.join(
    PROJECT,
    "outputs",
    "chexagent_reports_100.csv"
)

ERROR_FOLDER = os.path.join(
    PROJECT,
    "knowledge_graph",
    "kg_errors"
)

RECOMMEND_FOLDER = os.path.join(
    PROJECT,
    "knowledge_graph",
    "recommendations"
)

OUTPUT = os.path.join(
    PROJECT,
    "knowledge_graph",
    "kg_evidence_summary.csv"
)

reports = pd.read_csv(REPORTS)

rows = []

for _, row in reports.iterrows():

    image = row["image_id"].replace(".png","")

    error_file = os.path.join(ERROR_FOLDER, image + ".json")
    recommendation_file = os.path.join(RECOMMEND_FOLDER, image + ".txt")

    if not os.path.exists(error_file):
        continue

    with open(error_file) as f:
        err = json.load(f)

    recommendation = ""

    if os.path.exists(recommendation_file):
        with open(recommendation_file) as f:
            recommendation = f.read()

    summary = err["summary"]

    rows.append({

        "image_id":image,

        "generated_report":
            row["generated_impression"],

        "ground_truth":
            row["ground_truth_impression"],

        "missing_entities":
            ", ".join(err["missing_entities"]),

        "hallucinated_entities":
            ", ".join(err["hallucinated_entities"]),

        "missing_relations":
            summary["missing_relation_count"],

        "hallucinated_relations":
            summary["hallucinated_relation_count"],

        "recommendation":
            recommendation.replace("\n"," ")

    })

df = pd.DataFrame(rows)

df.to_csv(OUTPUT,index=False)

print()
print("="*60)
print("Saved KG Evidence Summary")
print(OUTPUT)
print("="*60)
