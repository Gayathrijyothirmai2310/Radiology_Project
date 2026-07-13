import os
import json
import pandas as pd
from tqdm import tqdm
from radgraph import RadGraph

CSV_PATH = "outputs/chexagent_reports_100.csv"
OUTPUT_DIR = "KnowledgeGraph/groundtruth_json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)

print(f"Loaded {len(df)} reports.")

print("Loading RadGraph...")
model = RadGraph()
print("RadGraph loaded successfully.")

for _, row in tqdm(df.iterrows(), total=len(df)):

    image_id = row["image_id"].replace(".png", "")

    report = str(row["ground_truth_impression"])

    if report.strip() == "" or report == "nan":
        continue

    result = model(report)

    save_path = os.path.join(
        OUTPUT_DIR,
        image_id + ".json"
    )

    with open(save_path, "w") as f:
        json.dump(result, f, indent=4)

print("\nFinished extracting Ground Truth entities.")
