import os
import json
import pandas as pd
from tqdm import tqdm
from pathlib import Path

from graph_metrics import (
    entity_metrics,
    relation_metrics,
    graph_score,
    normalize_entity
)

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATED_DIR = PROJECT_ROOT / "knowledge_graph" / "generated_json"
GROUNDTRUTH_DIR = PROJECT_ROOT / "knowledge_graph" / "groundtruth_json"

OUTPUT_DIR = PROJECT_ROOT / "knowledge_graph" / "comparison_results"
OUTPUT_DIR.mkdir(exist_ok=True)

# -------------------------------------------------
# Load RadGraph JSON
# -------------------------------------------------

def load_radgraph(path):

    with open(path, "r") as f:
        data = json.load(f)

    report = list(data.values())[0]
    entities = report["entities"]

    nodes = {}
    relations = []

    # Nodes
    for entity_id, entity in entities.items():

        nodes[entity_id] = (
            entity["tokens"]
            .lower()
            .strip()
        )

    # Relations
    for entity_id, entity in entities.items():

        source = nodes[entity_id]

        for relation in entity["relations"]:

            relation_type = relation[0]
            target_id = relation[1]

            if target_id in nodes:

                target = nodes[target_id]

                relations.append(
                    (
                        source,
                        relation_type,
                        target
                    )
                )

    return list(nodes.values()), relations

# -------------------------------------------------
# Wrong Relation Detection
# -------------------------------------------------

def find_wrong_relations(
        generated,
        truth):

    wrong = []

    generated_dict = {}
    truth_dict = {}

    for source, relation, target in generated:

        generated_dict[
            (
                normalize_entity(source),
                relation
            )
        ] = normalize_entity(target)

    for source, relation, target in truth:

        truth_dict[
            (
                normalize_entity(source),
                relation
            )
        ] = normalize_entity(target)

    for key in generated_dict:

        if key in truth_dict:

            if generated_dict[key] != truth_dict[key]:

                wrong.append({

                    "finding": key[0],

                    "relation": key[1],

                    "expected_target":
                    truth_dict[key],

                    "generated_target":
                    generated_dict[key]

                })

    return wrong


# -------------------------------------------------
# Evaluation
# -------------------------------------------------

summary = []

files = sorted([
    f
    for f in os.listdir(GENERATED_DIR)
    if f.endswith(".json")
])

for filename in tqdm(files):

    generated_file = GENERATED_DIR / filename
    truth_file = GROUNDTRUTH_DIR / filename

    if not truth_file.exists():
        continue

    generated_nodes, generated_relations = load_radgraph(
        generated_file
    )

    truth_nodes, truth_relations = load_radgraph(
        truth_file
    )

    entity_result = entity_metrics(
        generated_nodes,
        truth_nodes
    )

    relation_result = relation_metrics(
        generated_relations,
        truth_relations
    )

    score = graph_score(
        entity_result["f1"],
        relation_result["f1"]
    )

    generated_norm = set(
        normalize_entity(x)
        for x in generated_nodes
    )

    truth_norm = set(
        normalize_entity(x)
        for x in truth_nodes
    )

    hallucinated = sorted(
        list(
            generated_norm -
            truth_norm
        )
    )

    missing = sorted(
        list(
            truth_norm -
            generated_norm
        )
    )

    wrong_relations = find_wrong_relations(
        generated_relations,
        truth_relations
    )

    result = {

        "image_id":
        filename.replace(".json", ""),

        "entity_metrics":
        entity_result,

        "relation_metrics":
        relation_result,

        "graph_score":
        score,

        "hallucinated_nodes":
        hallucinated,

        "missing_nodes":
        missing,

        "wrong_relations":
        wrong_relations
    }

    with open(
        OUTPUT_DIR / filename,
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )

    summary.append({

        "image_id":
        filename.replace(".json", ""),

        "entity_precision":
        entity_result["precision"],

        "entity_recall":
        entity_result["recall"],

        "entity_f1":
        entity_result["f1"],

        "relation_precision":
        relation_result["precision"],

        "relation_recall":
        relation_result["recall"],

        "relation_f1":
        relation_result["f1"],

        "graph_score":
        score,

        "hallucinated_count":
        len(hallucinated),

        "missing_count":
        len(missing),

        "wrong_relation_count":
        len(wrong_relations)

    })


# -------------------------------------------------
# Save Summary
# -------------------------------------------------

df = pd.DataFrame(summary)

df.to_csv(
    OUTPUT_DIR / "graph_metrics_summary_v2.csv",
    index=False
)

# -------------------------------------------------
# Print Results
# -------------------------------------------------

print()
print("=" * 70)
print("Knowledge Graph V2.1 Evaluation Finished")
print("=" * 70)

print(
    f"Cases evaluated : {len(df)}"
)

print(
    f"Average Entity F1 : {df.entity_f1.mean():.4f}"
)

print(
    f"Average Relation F1 : {df.relation_f1.mean():.4f}"
)

print(
    f"Average Graph Score : {df.graph_score.mean():.4f}"
)

print(
    f"Average Hallucinations : {df.hallucinated_count.mean():.2f}"
)

print(
    f"Average Missing Nodes : {df.missing_count.mean():.2f}"
)

print(
    f"Average Wrong Relations : {df.wrong_relation_count.mean():.2f}"
)

print("=" * 70)
