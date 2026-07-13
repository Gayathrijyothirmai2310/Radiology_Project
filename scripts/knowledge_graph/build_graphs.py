import json
import networkx as nx
import matplotlib.pyplot as plt

from pathlib import Path

JSON_DIR = Path("KnowledgeGraph/json")
GRAPH_DIR = Path("KnowledgeGraph/graphs")
VIS_DIR = Path("KnowledgeGraph/visualizations")

GRAPH_DIR.mkdir(exist_ok=True)
VIS_DIR.mkdir(exist_ok=True)

json_files = sorted(JSON_DIR.glob("*.json"))

print(f"Found {len(json_files)} JSON files.\n")

for json_file in json_files:

    with open(json_file, "r") as f:
        data = json.load(f)

    report = data["0"]

    entities = report["entities"]

    G = nx.DiGraph()

    # ------------------------
    # Add Nodes
    # ------------------------

    for entity_id, entity in entities.items():

        G.add_node(
            entity_id,
            token=entity["tokens"],
            label=entity["label"]
        )

    # ------------------------
    # Add Edges
    # ------------------------

    for entity_id, entity in entities.items():

        for relation in entity["relations"]:

            relation_name = relation[0]
            target = relation[1]

            G.add_edge(
                entity_id,
                target,
                relation=relation_name
            )

    graph_file = GRAPH_DIR / f"{json_file.stem}.graphml"

    nx.write_graphml(G, graph_file)

    plt.figure(figsize=(8,6))

    pos = nx.spring_layout(G, seed=42)

    node_labels = {
        n: G.nodes[n]["token"]
        for n in G.nodes()
    }

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=1800
    )

    nx.draw_networkx_labels(
        G,
        pos,
        labels=node_labels,
        font_size=8
    )

    nx.draw_networkx_edges(
        G,
        pos,
        arrows=True
    )

    edge_labels = nx.get_edge_attributes(
        G,
        "relation"
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=7
    )

    plt.axis("off")

    image_file = VIS_DIR / f"{json_file.stem}.png"

    plt.savefig(
        image_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Processed {json_file.stem}")

print("\nDone!")
print(f"Graphs saved to: {GRAPH_DIR}")
print(f"Images saved to: {VIS_DIR}")
