import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path.home() / "Radiology_Project"

V8_DIR = (
    PROJECT_ROOT /
    "knowledge_graph" /
    "corrected_reports_v8"
)

OUTPUT = (
    PROJECT_ROOT /
    "evaluation" /
    "v8_reports.csv"
)

records = []

for file in sorted(V8_DIR.glob("*.txt")):

    image_id = file.stem + ".png"

    with open(file, "r") as f:
        text = f.read()

    if "IMPRESSION:" in text:
        findings = text.split("IMPRESSION:")[0]
        impression = text.split("IMPRESSION:")[1]
    else:
        findings = text
        impression = ""

    findings = (
        findings
        .replace("FINDINGS:", "")
        .strip()
    )

    impression = impression.strip()

    records.append(
        {
            "image_id": image_id,
            "generated_findings": findings,
            "generated_impression": impression
        }
    )

df = pd.DataFrame(records)

df.to_csv(
    OUTPUT,
    index=False
)

print("=" * 50)
print("V8 CSV CREATED")
print("=" * 50)
print("Location:", OUTPUT)
print("Reports:", len(df))
