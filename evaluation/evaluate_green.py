import os
import pandas as pd

from green_score import GREEN

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_CSV = os.path.join(
    BASE_DIR,
    "outputs",
    "chexagent_reports_100.csv"
)

OUTPUT_CSV = os.path.join(
    BASE_DIR,
    "outputs",
    "chexagent_reports_green.csv"
)

SUMMARY_TXT = os.path.join(
    BASE_DIR,
    "evaluation",
    "green_summary.txt"
)

# ==========================================================
# Load reports
# ==========================================================

print("Loading reports...")

df = pd.read_csv(INPUT_CSV)

refs = (
    df["ground_truth_impression"]
    .fillna("")
    .astype(str)
    .tolist()
)

hyps = (
    df["generated_impression"]
    .fillna("")
    .astype(str)
    .tolist()
)

print(f"Loaded {len(df)} reports.")

# ==========================================================
# Load GREEN model
# ==========================================================

print("\nLoading GREEN model...")

green = GREEN(
    model_name="StanfordAIMI/GREEN-radllama2-7b",
    output_dir="."
)

print("GREEN model loaded.")

# ==========================================================
# Evaluate
# ==========================================================

print("\nRunning GREEN evaluation...")

mean_score, std_score, green_scores, summary, results_df = green(
    refs,
    hyps,
)

print("\n================ RESULTS_DF COLUMNS ================\n")
print(results_df.columns)

print("\n================ RESULTS_DF ================\n")
print(results_df)

print("\n================ SUMMARY ================\n")
print(summary)
# ==========================================================
# Save per-report scores
# ==========================================================

# ==========================================================
# Save per-report scores
# ==========================================================

df["GREEN_score"] = green_scores
df["Hallucination_score"] = 1 - df["GREEN_score"]

df.to_csv(OUTPUT_CSV, index=False)

# ==========================================================
# Summary
# ==========================================================

# ==========================================================
# Summary
# ==========================================================

summary_text = f"""
GREEN Evaluation Summary
========================

Number of Reports : {len(df)}

Average GREEN Score : {mean_score:.4f}

GREEN Score Standard Deviation : {std_score:.4f}
"""

with open(SUMMARY_TXT, "w") as f:
    f.write(summary_text)

# ==========================================================
# Print results
# ==========================================================

print(summary_text)

print(f"Per-report scores saved to:\n{OUTPUT_CSV}")

print(f"\nSummary saved to:\n{SUMMARY_TXT}")
