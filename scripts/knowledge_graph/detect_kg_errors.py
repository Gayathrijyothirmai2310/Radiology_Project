import os
import json
import string

# ==============================
# Paths
# ==============================

BASE_DIR = os.path.expanduser("~/Radiology_Project")

GENERATED_DIR = os.path.join(BASE_DIR,
                             "knowledge_graph",
                             "generated_json")

GROUNDTRUTH_DIR = os.path.join(BASE_DIR,
                               "knowledge_graph",
                               "groundtruth_json")

OUTPUT_DIR = os.path.join(BASE_DIR,
                          "knowledge_graph",
                          "kg_errors")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================
# Helper Functions
# ==============================

def normalize(text):
    """
    Normalize entity tokens so that:
    Rib == rib == rib.
    """
    text = text.lower().strip()

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    return text


def load_entities(json_path):

    with open(json_path, "r") as f:
        data = json.load(f)

    report = list(data.values())[0]

    entities = report["entities"]

    entity_map = {}

    for entity_id, entity in entities.items():

        token = normalize(entity["tokens"])

        entity_map[entity_id] = {
            "token": token,
            "label": entity["label"],
            "relations": entity.get("relations", [])
        }

    return report["text"], entity_map


def build_entity_set(entity_map):

    entity_set = set()

    for entity in entity_map.values():
        entity_set.add(entity["token"])

    return entity_set


def build_relation_set(entity_map):

    relation_set = set()

    for source_id, entity in entity_map.items():

        source_token = entity["token"]

        for relation_type, target_id in entity["relations"]:

            if target_id not in entity_map:
                continue

            target_token = entity_map[target_id]["token"]

            relation_set.add(
                (
                    source_token,
                    relation_type,
                    target_token
                )
            )

    return relation_set


# ==============================
# Compare Graphs
# ==============================

generated_files = sorted(
    [
        f for f in os.listdir(GENERATED_DIR)
        if f.endswith(".json")
    ]
)

print(f"\nFound {len(generated_files)} generated graphs.\n")

processed = 0

for filename in generated_files:

    generated_path = os.path.join(GENERATED_DIR, filename)
    groundtruth_path = os.path.join(GROUNDTRUTH_DIR, filename)

    if not os.path.exists(groundtruth_path):
        print(f"Skipping {filename} (ground truth missing)")
        continue

    # --------------------------
    # Load graphs
    # --------------------------

    generated_text, generated_entities = load_entities(generated_path)
    groundtruth_text, groundtruth_entities = load_entities(groundtruth_path)

    generated_entity_set = build_entity_set(generated_entities)
    groundtruth_entity_set = build_entity_set(groundtruth_entities)

    generated_relation_set = build_relation_set(generated_entities)
    groundtruth_relation_set = build_relation_set(groundtruth_entities)

    # --------------------------
    # Entity comparison
    # --------------------------

    missing_entities = sorted(
        list(groundtruth_entity_set - generated_entity_set)
    )

    hallucinated_entities = sorted(
        list(generated_entity_set - groundtruth_entity_set)
    )

    common_entities = sorted(
        list(generated_entity_set & groundtruth_entity_set)
    )

    # --------------------------
    # Relation comparison
    # --------------------------

    missing_relations = sorted(
        [
            {
                "source": r[0],
                "relation": r[1],
                "target": r[2]
            }
            for r in (groundtruth_relation_set - generated_relation_set)
        ],
        key=lambda x: (x["source"], x["relation"], x["target"])
    )

    hallucinated_relations = sorted(
        [
            {
                "source": r[0],
                "relation": r[1],
                "target": r[2]
            }
            for r in (generated_relation_set - groundtruth_relation_set)
        ],
        key=lambda x: (x["source"], x["relation"], x["target"])
    )

    # --------------------------
    # Build output JSON
    # --------------------------

    result = {

        "image_id": filename.replace(".json", ""),

        "generated_text": generated_text,

        "ground_truth_text": groundtruth_text,

        "missing_entities": missing_entities,

        "hallucinated_entities": hallucinated_entities,

        "common_entities": common_entities,

        "missing_relations": missing_relations,

        "hallucinated_relations": hallucinated_relations,

        "summary": {

            "generated_entity_count":
                len(generated_entity_set),

            "groundtruth_entity_count":
                len(groundtruth_entity_set),

            "common_entity_count":
                len(common_entities),

            "missing_entity_count":
                len(missing_entities),

            "hallucinated_entity_count":
                len(hallucinated_entities),

            "generated_relation_count":
                len(generated_relation_set),

            "groundtruth_relation_count":
                len(groundtruth_relation_set),

            "missing_relation_count":
                len(missing_relations),

            "hallucinated_relation_count":
                len(hallucinated_relations)
        }
    }

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)

    processed += 1

print("=" * 60)
print(f"Processed : {processed}")
print(f"Saved to  : {OUTPUT_DIR}")
print("=" * 60)
