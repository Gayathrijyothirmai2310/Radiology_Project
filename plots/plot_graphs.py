import os
import matplotlib.pyplot as plt
import numpy as np

metrics = [
    "BLEU", "ROUGE-1", "ROUGE-2", "ROUGE-L",
    "BERTScore F1",
    "CheXbert Micro Precision",
    "CheXbert Micro Recall",
    "CheXbert Micro F1",
    "CheXbert Macro F1",
    "GREEN"
]

chexagent = [0.0485, 0.3843, 0.1340, 0.2429, 0.8720, 0.8864, 0.8864, 0.8864, 0.2476, 0.2560]
v9        = [0.0673, 0.4328, 0.1627, 0.2916, 0.8864, 0.9031, 0.8987, 0.9009, 0.2834, 0.7318]

os.makedirs("plots", exist_ok=True)

x = np.arange(len(metrics))
width = 0.35

plt.figure(figsize=(14, 7))


plt.bar(x - width/2, chexagent, width, label="CheXagent", color='blue')
plt.bar(x + width/2, v9, width, label="V9", color='orange')

plt.xticks(x, metrics, rotation=30, ha='right')
plt.ylabel("Score")
plt.title("Comparison of Evaluation Metrics")

plt.legend()
plt.grid(axis='y')

plt.tight_layout()
plt.savefig("plots/comparison_all_metrics.png")

print("Saved at plots/comparison_all_metrics.png")
