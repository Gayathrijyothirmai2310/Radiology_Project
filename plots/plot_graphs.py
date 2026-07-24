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

chexagent = [0.0485, 0.3843, 0.1340, 0.2429, 0.8720, 0.8864, 0.8864, 0.8864, 0.2476, 0.2560]
v9        = [0.0673, 0.4328, 0.1627, 0.2916, 0.8864, 0.9031, 0.8987, 0.9009, 0.2834, 0.7318]

# -----------------------------
# Positions
# -----------------------------
x = np.arange(len(metrics))
width = 0.35

# -----------------------------
# Style (clean & publication-like)
# -----------------------------
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))

# Colors (consistent, single color per model)
color_chex = "#4C72B0"
color_v9   = "#DD8452"

# -----------------------------
# Plot bars
# -----------------------------
bars1 = ax.bar(x - width/2, chexagent, width, label="CheXagent", color=color_chex)
bars2 = ax.bar(x + width/2, v9, width, label="V9", color=color_v9)

# -----------------------------
# Labels & formatting
# -----------------------------
ax.set_xlabel("Metrics", fontsize=11)
ax.set_ylabel("Score", fontsize=11)
ax.set_title("Model Comparison Across Evaluation Metrics", fontsize=14, weight="semibold")

ax.set_xticks(x)
ax.set_xticklabels(metrics, rotation=30, ha="right")

ax.legend(frameon=True)
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Remove top/right borders for clean look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# -----------------------------
# Optional: add value labels
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
# Save (publication quality)
# -----------------------------
plt.savefig("vertical_comparison.png", dpi=300, bbox_inches="tight")
plt.savefig("vertical_comparison.pdf", bbox_inches="tight")

plt.show()
