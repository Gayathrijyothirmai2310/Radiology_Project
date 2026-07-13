import os
import json
import pandas as pd
from tqdm import tqdm
from radgraph import RadGraph

# -------------------------------------------------
# Paths
# -------------------------------------------------

CSV_PATH = "outputs/chexagent_reports_100.csv"
OUTPUT_DIR = "KnowledgeGraph/json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------
# Load CSV
# -------------------------------------------------

df = pd.read_csv(CSV_PATH)

print(f"Loaded {len(df)} reports.")

# -------------------------------------------------
# Load RadGraph
# -------------------------------------------------

print("Loading RadGraph...")
model = RadGraph()
print("RadGraph loaded successfully.\n")

# -------------------------------------------------
# Process reports
# -------------------------------------------------

for idx, row in tqdm(df.iterrows(), total=len(df)):

    image_id = row["image_id"]
    report = row["generated_impression"]

    if pd.isna(report):
        continue

    try:
        result = model(report)

        save_path = os.path.join(
            OUTPUT_DIR,
            image_id.replace(".png", ".json")
        )

        with open(save_path, "w") as f:
            json.dump(result, f, indent=4)

    except Exception as e:

        print(f"Error processing {image_id}")
        print(e)

print("\nFinished extracting entities.")
