import os
import pandas as pd

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

from rouge_score import rouge_scorer

# ======================================================
# Paths
# ======================================================

PROJECT_ROOT = "/home/gayathr.jyothirmai/Radiology_Project"

INPUT_CSV = os.path.join(
    PROJECT_ROOT,
    "outputs",
    "chexagent_reports_100.csv",
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "evaluation",
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_CSV = os.path.join(
    OUTPUT_DIR,
    "bleu_rouge_scores.csv",
)

SUMMARY_FILE = os.path.join(
    OUTPUT_DIR,
    "bleu_rouge_summary.txt",
)

# ======================================================
# Read CSV
# ======================================================

df = pd.read_csv(INPUT_CSV)

# ======================================================
# Initialize
# ======================================================

smooth = SmoothingFunction().method1

rouge = rouge_scorer.RougeScorer(
    ["rouge1", "rouge2", "rougeL"],
    use_stemmer=True,
)

bleu_scores = []

rouge1_scores = []
rouge2_scores = []
rougeL_scores = []

# ======================================================
# Evaluate
# ======================================================

for index, row in df.iterrows():

    reference = str(row["ground_truth_findings"])
    prediction = str(row["generated_findings"])

    bleu = sentence_bleu(
        [reference.split()],
        prediction.split(),
        smoothing_function=smooth,
    )

    scores = rouge.score(reference, prediction)

    rouge1 = scores["rouge1"].fmeasure
    rouge2 = scores["rouge2"].fmeasure
    rougeL = scores["rougeL"].fmeasure

    bleu_scores.append(bleu)
    rouge1_scores.append(rouge1)
    rouge2_scores.append(rouge2)
    rougeL_scores.append(rougeL)

# ======================================================
# Save scores
# ======================================================

df["BLEU"] = bleu_scores
df["ROUGE-1"] = rouge1_scores
df["ROUGE-2"] = rouge2_scores
df["ROUGE-L"] = rougeL_scores

df.to_csv(OUTPUT_CSV, index=False)

# ======================================================
# Compute averages
# ======================================================

avg_bleu = sum(bleu_scores) / len(bleu_scores)
avg_r1 = sum(rouge1_scores) / len(rouge1_scores)
avg_r2 = sum(rouge2_scores) / len(rouge2_scores)
avg_rl = sum(rougeL_scores) / len(rougeL_scores)

# ======================================================
# Print
# ======================================================

print("\nEvaluation Complete\n")

print(f"Average BLEU     : {avg_bleu:.4f}")
print(f"Average ROUGE-1  : {avg_r1:.4f}")
print(f"Average ROUGE-2  : {avg_r2:.4f}")
print(f"Average ROUGE-L  : {avg_rl:.4f}")

# ======================================================
# Save summary
# ======================================================

with open(SUMMARY_FILE, "w") as f:

    f.write("BLEU / ROUGE Evaluation\n")
    f.write("========================\n\n")

    f.write(f"Images Evaluated : {len(df)}\n\n")

    f.write(f"Average BLEU     : {avg_bleu:.4f}\n")
    f.write(f"Average ROUGE-1  : {avg_r1:.4f}\n")
    f.write(f"Average ROUGE-2  : {avg_r2:.4f}\n")
    f.write(f"Average ROUGE-L  : {avg_rl:.4f}\n")

print("\nResults saved to:")

print(OUTPUT_CSV)
print(SUMMARY_FILE)
