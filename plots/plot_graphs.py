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

chexagent_raw = [0.0485, 0.3843, 0.1340, 0.2429, 0.8720, 0.8864, 0.8864, 0.8864, 0.2476, 0.2560]
v9_raw        = [0.0673, 0.4328, 0.1627, 0.2916, 0.8864, 0.9031, 0.8987, 0.9009, 0.2834, 0.7318]

# -----------------------------
# Normalize per metric (important!)
# -----------------------------
all_vals = np.array([chexagent_raw, v9_raw])
min_vals = all_vals.min(axis=0)
max_vals = all_vals.max(axis=0)

chexagent = (np.array(chexagent_raw) - min_vals) / (max_vals - min_vals + 1e-8)
v9        = (np.array(v9_raw)        - min_vals) / (max_vals - min_vals + 1e-8)

# -----------------------------
# Radar setup
# -----------------------------
N = len(metrics)
angles = np.linspace(0, 2*np.pi, N, endpoint=False)

# Close loop
angles = np.concatenate([angles, [angles[0]]])
chexagent = np.concatenate([chexagent, [chexagent[0]]])
v9        = np.concatenate([v9, [v9[0]]])

# -----------------------------
# Style (Seaborn-like)
# -----------------------------
plt.style.use("seaborn-v0_8-whitegrid")

fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)

# Colors (soft, publication-friendly)
color_chex = "#4C72B0"   # muted blue
color_v9   = "#DD8452"   # muted orange

# -----------------------------
# Plot
# -----------------------------
ax.plot(angles, chexagent, linewidth=2.5, color=color_chex, label="CheXagent")
ax.fill(angles, chexagent, color=color_chex, alpha=0.25)

ax.plot(angles, v9, linewidth=2.5, color=color_v9, label="V9")
ax.fill(angles, v9, color=color_v9, alpha=0.25)

# -----------------------------
# Labels
# -----------------------------
ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics, fontsize=10)

ax.set_yticks([0.2, 0.4, 0.6, 0.8])
ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8"], fontsize=9)
ax.set_ylim(0, 1)

# -----------------------------
# Clean aesthetics
# -----------------------------
ax.spines["polar"].set_visible(False)
ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

# Title
plt.title("Model Comparison Across Metrics (Normalized Radar)", 
          fontsize=14, pad=20, weight="semibold")

# Legend
legend = plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=True)
legend.get_frame().set_alpha(0.9)

plt.tight_layout()

# -----------------------------
# Save (publication ready)
# -----------------------------
plt.savefig("radar_comparison.png", dpi=300, bbox_inches="tight")
plt.savefig("radar_comparison.pdf", bbox_inches="tight")

plt.show()
