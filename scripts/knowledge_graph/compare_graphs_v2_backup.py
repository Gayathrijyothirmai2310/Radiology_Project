import os
import json
import pandas as pd
from tqdm import tqdm

from graph_metrics import (
    entity_metrics,
    relation_metrics,
    graph_score
)


from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


GENERATED_DIR = PROJECT_ROOT / "knowledge_graph" / "generated_json"
GROUNDTRUTH_DIR = PROJECT_ROOT / "knowledge_graph" / "groundtruth_json"

OUTPUT_DIR = PROJECT_ROOT / "knowledge_graph" / "comparison_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)



def load_radgraph(path):

    with open(path, "r") as f:
        data = json.load(f)

    report = list(data.values())[0]

    entities = report["entities"]

    nodes = {}
    relations = []


    for entity_id, entity in entities.items():

        token = (
            entity["tokens"]
            .lower()
            .strip()
        )

        nodes[entity_id] = token


    for entity_id, entity in entities.items():

        source = nodes[entity_id]

        for relation in entity["relations"]:

            relation_type = relation[0]
            target_id = relation[1]

            target = nodes.get(
                target_id,
                None
            )

            if target:

                relations.append(
                    (
                        source,
                        relation_type,
                        target
                    )
                )


    return (
        list(nodes.values()),
        relations
    )



summary=[]

files = sorted(
    [
        f for f in os.listdir(GENERATED_DIR)
        if f.endswith(".json")
    ]
)

for filename in tqdm(files):


    generated_path=os.path.join(
        GENERATED_DIR,
        filename
    )


    gt_path=os.path.join(
        GROUNDTRUTH_DIR,
        filename
    )


    if not os.path.exists(gt_path):
        continue


    generated_nodes, generated_relations = load_radgraph(
        generated_path
    )


    gt_nodes, gt_relations = load_radgraph(
        gt_path
    )


    entity_result = entity_metrics(
        generated_nodes,
        gt_nodes
    )


    relation_result = relation_metrics(
        generated_relations,
        gt_relations
    )


    score = graph_score(
        entity_result["f1"],
        relation_result["f1"]
    )


    result={

        "image_id":
        filename.replace(".json",""),

        "entity_metrics":
        entity_result,

        "relation_metrics":
        relation_result,

        "graph_score":
        score

    }


    with open(
        os.path.join(
            OUTPUT_DIR,
            filename
        ),
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )


    summary.append({

        "image_id":
        filename.replace(".json",""),

        "entity_f1":
        entity_result["f1"],

        "relation_f1":
        relation_result["f1"],

        "graph_score":
        score

    })



df=pd.DataFrame(summary)


df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "graph_metrics_summary.csv"
    ),
    index=False
)


print("\n")
print("="*60)
print("Knowledge Graph V2 Evaluation Finished")
print("="*60)

print(
    f"Cases evaluated : {len(df)}"
)

print(
    f"Average graph score : {df.graph_score.mean():.4f}"
)

print("="*60)
