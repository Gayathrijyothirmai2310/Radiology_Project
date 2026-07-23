import pandas as pd
import os

# Original reports (contains ground truth)
original = pd.read_csv("outputs/chexagent_reports_100.csv")

# V8 generated reports
v8 = pd.read_csv("evaluation/v8_reports.csv")

# Merge using image_id
df = original.merge(
    v8[["image_id", "generated_impression"]],
    on="image_id",
    suffixes=("_old", "")
)

output_dir = "evaluation/chexbert_inputs"
os.makedirs(output_dir, exist_ok=True)

# Ground truth
gt = pd.DataFrame()
gt["Report Impression"] = df["ground_truth_impression"].fillna("")

gt.to_csv(
    f"{output_dir}/ground_truth.csv",
    index=False
)

# V8 generated
gen = pd.DataFrame()
gen["Report Impression"] = df["generated_impression"].fillna("")

gen.to_csv(
    f"{output_dir}/v8_generated.csv",
    index=False
)

print("=" * 50)
print("CheXbert inputs created")
print("=" * 50)
print(f"Ground Truth : {output_dir}/ground_truth.csv")
print(f"V8 Reports   : {output_dir}/v8_generated.csv")
