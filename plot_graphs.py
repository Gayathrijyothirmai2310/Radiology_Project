import matplotlib.pyplot as plt
import os

os.makedirs("plots", exist_ok=True)

metrics = {
    "BLEU": (0.0485, 0.0673),
    "ROUGE-1": (0.3843, 0.4328),
    "ROUGE-2": (0.1340, 0.1627),
    "ROUGE-L": (0.2429, 0.2916),
    "BERTScore": (0.8720, 0.8864),
    "GREEN": (0.2560, 0.7318),

    "CheXbert_Micro_Precision": (0.8864, 0.9031),
    "CheXbert_Micro_Recall": (0.8864, 0.8987),
    "CheXbert_Micro_F1": (0.8864, 0.9009),
    "CheXbert_Macro_F1": (0.2476, 0.2834)
}

for metric, (before, after) in metrics.items():
    plt.figure()

    plt.plot(["CheXagent", "V9"], [before, after], marker='o')

    plt.title(f"{metric} Comparison")
    plt.ylabel("Score")

    plt.savefig(f"plots/{metric}_line.png")

    plt.close()
