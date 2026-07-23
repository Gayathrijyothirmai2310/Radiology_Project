import os
import json
from collections import Counter

kg_dir = "knowledge_graph/kg_errors"

totals = Counter()

num_images = 0

for file in os.listdir(kg_dir):
    if not file.endswith(".json"):
        continue

    with open(os.path.join(kg_dir, file), "r") as f:
        data = json.load(f)

    s = data["summary"]

    totals["Generated Entities"] += s["generated_entity_count"]
    totals["Ground Truth Entities"] += s["groundtruth_entity_count"]

    totals["Missing Findings"] += s["missing_entity_count"]
    totals["Hallucinated Findings"] += s["hallucinated_entity_count"]

    totals["Missing Relations"] += s["missing_relation_count"]
    totals["Hallucinated Relations"] += s["hallucinated_relation_count"]

    num_images += 1

print("="*50)
print("Knowledge Graph Error Summary")
print("="*50)
print(f"Images Evaluated : {num_images}\n")

for k, v in totals.items():
    print(f"{k:25s}: {v}")

print("\nAverage per Report")
print("-"*50)

print(f"Missing Findings      : {totals['Missing Findings']/num_images:.2f}")
print(f"Hallucinations        : {totals['Hallucinated Findings']/num_images:.2f}")
print(f"Missing Relations     : {totals['Missing Relations']/num_images:.2f}")
print(f"Hallucinated Relations: {totals['Hallucinated Relations']/num_images:.2f}")
