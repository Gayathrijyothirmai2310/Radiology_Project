import os
import json
import pandas as pd
from tqdm import tqdm

GENERATED_DIR = "KnowledgeGraph/generated_json"
GROUNDTRUTH_DIR = "KnowledgeGraph/groundtruth_json"

OUTPUT_JSON_DIR = "KnowledgeGraph/comparison_json"
OUTPUT_REPORT_DIR = "KnowledgeGraph/comparison_reports"

os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)
os.makedirs(OUTPUT_REPORT_DIR, exist_ok=True)


def load_entities(path):
    with open(path, "r") as f:
        data = json.load(f)

    report = list(data.values())[0]
    entities = report["entities"]

    entity_list = []

    for _, entity in entities.items():
        entity_list.append({
            "token": entity["tokens"].lower().strip(),
            "label": entity["label"],
            "relations": entity["relations"]
        })

    return entity_list


summary = []

files = sorted(os.listdir(GENERATED_DIR))

for filename in tqdm(files):

    generated_file = os.path.join(GENERATED_DIR, filename)
    gt_file = os.path.join(GROUNDTRUTH_DIR, filename)

    if not os.path.exists(gt_file):
        continue

    generated_entities = load_entities(generated_file)
    gt_entities = load_entities(gt_file)

    generated_tokens = set(x["token"] for x in generated_entities)
    gt_tokens = set(x["token"] for x in gt_entities)

    common = sorted(list(generated_tokens & gt_tokens))
    missing = sorted(list(gt_tokens - generated_tokens))
    extra = sorted(list(generated_tokens - gt_tokens))

    similarity = 0.0

    if len(gt_tokens) > 0:
        similarity = len(common) / len(gt_tokens)

    comparison = {
        "image_id": filename.replace(".json", ""),
        "generated_entity_count": len(generated_tokens),
        "groundtruth_entity_count": len(gt_tokens),
        "common_entities": common,
        "missing_entities": missing,
        "hallucinated_entities": extra,
        "entity_similarity": round(similarity, 4)
    }

    with open(
        os.path.join(OUTPUT_JSON_DIR, filename),
        "w"
    ) as f:
        json.dump(comparison, f, indent=4)

    summary.append({
        "image_id": filename.replace(".json", ""),
        "generated_entities": len(generated_tokens),
        "groundtruth_entities": len(gt_tokens),
        "matched": len(common),
        "missing": len(missing),
        "hallucinated": len(extra),
        "entity_similarity": round(similarity, 4)
    })

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    os.path.join(
        OUTPUT_REPORT_DIR,
        "graph_comparison_summary.csv"
    ),
    index=False
)

print()
print("=" * 60)
print("Finished comparing all Knowledge Graphs.")
print(f"Cases compared : {len(summary_df)}")
print(f"Average similarity : {summary_df['entity_similarity'].mean():.4f}")
print("=" * 60)
