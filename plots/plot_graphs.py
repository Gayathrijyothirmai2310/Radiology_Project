import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Data
# -----------------------------
metrics = [
    "BLEU", "ROUGE-1", "ROUGE-2", "ROUGE-L",
    "BERTScore", "Micro Precision", "Micro Recall",
    "Micro F1", "Macro F1", "GREEN"
]

chexagent = np.array([0.0485, 0.3843, 0.1340, 0.2429, 0.8720, 0.8864, 0.8864, 0.8864, 0.2476, 0.2560])
v9        = np.array([0.0673, 0.4328, 0.1627, 0.2916, 0.8864, 0.9031, 0.8987, 0.9009, 0.2834, 0.7318])

# -----------------------------
# Sort by V9 (descending)
# -----------------------------
sorted_idx = np.argsort(v9)[::-1]

metrics_sorted = [metrics[i] for i in sorted_idx]
chex_sorted = chexagent[sorted_idx]
v9_sorted   = v9[sorted_idx]

# -----------------------------
# Positions
# -----------------------------
x = np.arange(len(metrics_sorted))
width = 0.35

# -----------------------------
# Style
# -----------------------------
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))

color_chex = "#4C72B0"
color_v9   = "#DD8452"

# -----------------------------
# Plot
# -----------------------------
bars1 = ax.bar(x - width/2, chex_sorted, width, label="CheXagent", color=color_chex)
bars2 = ax.bar(x + width/2, v9_sorted, width, label="V9", color=color_v9)

# -----------------------------
# Labels
# -----------------------------
ax.set_xlabel("Metrics", fontsize=11)
ax.set_ylabel("Score", fontsize=11)
ax.set_title("Model Comparison (Sorted by V9 Performance)", fontsize=14, weight="semibold")

ax.set_xticks(x)
ax.set_xticklabels(metrics_sorted, rotation=30, ha="right")

ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Clean look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# -----------------------------
# Value labels
# -----------------------------
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2,
                height + 0.01,
                f"{height:.2f}",
                ha='center', va='bottom', fontsize=8)

add_labels(bars1)
add_labels(bars2)

plt.tight_layout()

# -----------------------------
# Save
# -----------------------------
plt.savefig("sorted_comparison.png", dpi=300, bbox_inches="tight")
plt.savefig("sorted_comparison.pdf", bbox_inches="tight")

plt.show()
