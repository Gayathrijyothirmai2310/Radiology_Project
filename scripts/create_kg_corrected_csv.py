from pathlib import Path
import pandas as pd

PROJECT = Path.home() / "Radiology_Project"

original_csv = PROJECT / "outputs" / "chexagent_reports_100.csv"

corrected_dir = PROJECT / "knowledge_graph" / "corrected_reports_v2"

output_csv = PROJECT / "outputs" / "kg_corrected_reports.csv"

df = pd.read_csv(original_csv)

generated_findings = []
generated_impression = []

for _, row in df.iterrows():

    image_id = row["image_id"]

    report_file = corrected_dir / f"{Path(image_id).stem}.txt"

    if report_file.exists():

        text = report_file.read_text(encoding="utf-8")

        text = text.replace("IMPRESSION:", "").strip()

    else:

        text = ""

    generated_findings.append(text)

    generated_impression.append(text)

df["generated_findings"] = generated_findings

df["generated_impression"] = generated_impression

df.to_csv(output_csv, index=False)

print("Saved:", output_csv)
print("Cases:", len(df))
