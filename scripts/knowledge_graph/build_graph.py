import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

json_file = "KnowledgeGraph/json/image_6502.json"

with open(json_file, "r") as f:
    data = json.load(f)

report = data["0"]

entities = report["entities"]

G = nx.DiGraph()

# Add nodes
for entity_id, entity in entities.items():
    G.add_node(
        entity_id,
        token=entity["tokens"],
        label=entity["label"]
    )

# Add edges
for entity_id, entity in entities.items():
    for relation in entity["relations"]:
        relation_name = relation[0]
        target = relation[1]

        G.add_edge(
            entity_id,
            target,
            relation=relation_name
        )

print(f"Nodes : {G.number_of_nodes()}")
print(f"Edges : {G.number_of_edges()}")

# Draw graph
plt.figure(figsize=(8,6))

pos = nx.spring_layout(G, seed=42)

node_labels = {
    n: G.nodes[n]["token"]
    for n in G.nodes()
}

nx.draw_networkx_nodes(G, pos, node_size=1800)

nx.draw_networkx_labels(
    G,
    pos,
    labels=node_labels,
    font_size=9
)

nx.draw_networkx_edges(
    G,
    pos,
    arrows=True
)

edge_labels = nx.get_edge_attributes(G, "relation")

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=8
)

plt.axis("off")

Path("KnowledgeGraph/graphs").mkdir(exist_ok=True)
Path("KnowledgeGraph/visualizations").mkdir(exist_ok=True)

nx.write_graphml(
    G,
    "KnowledgeGraph/graphs/image_6502.graphml"
)

plt.savefig(
    "KnowledgeGraph/visualizations/image_6502.png",
    dpi=300,
    bbox_inches="tight"
)

print("Graph saved successfully!")
