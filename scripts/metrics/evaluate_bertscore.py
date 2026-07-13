import os
import pandas as pd
from bert_score import score

# ===========================================
# Paths
# ===========================================

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
    "bertscore_scores.csv",
)

SUMMARY_FILE = os.path.join(
    OUTPUT_DIR,
    "bertscore_summary.txt",
)

# ===========================================
# Read CSV
# ===========================================

df = pd.read_csv(INPUT_CSV)

references = df["ground_truth_findings"].fillna("").astype(str).tolist()
predictions = df["generated_findings"].fillna("").astype(str).tolist()

print("Computing BERTScore...")

P, R, F1 = score(
    predictions,
    references,
    lang="en",
    verbose=True,
)

df["BERTScore_Precision"] = P.tolist()
df["BERTScore_Recall"] = R.tolist()
df["BERTScore_F1"] = F1.tolist()

df.to_csv(OUTPUT_CSV, index=False)

avg_p = float(P.mean())
avg_r = float(R.mean())
avg_f1 = float(F1.mean())

print("\nBERTScore Results")
print(f"Precision : {avg_p:.4f}")
print(f"Recall    : {avg_r:.4f}")
print(f"F1        : {avg_f1:.4f}")

with open(SUMMARY_FILE, "w") as f:
    f.write("BERTScore Evaluation\n")
    f.write("====================\n\n")
    f.write(f"Images Evaluated : {len(df)}\n\n")
    f.write(f"Precision : {avg_p:.4f}\n")
    f.write(f"Recall    : {avg_r:.4f}\n")
    f.write(f"F1        : {avg_f1:.4f}\n")

print("\nSaved:")
print(OUTPUT_CSV)
print(SUMMARY_FILE)
