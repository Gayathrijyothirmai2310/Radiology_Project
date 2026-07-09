import pandas as pd
import os


input_file = "outputs/chexagent_reports_100.csv"

output_dir = "evaluation/chexbert_inputs"

os.makedirs(output_dir, exist_ok=True)


df = pd.read_csv(input_file)


# Ground truth
gt = pd.DataFrame()

gt["Report Impression"] = df["ground_truth_impression"].fillna("")


gt.to_csv(
    f"{output_dir}/ground_truth.csv",
    index=False
)


# CheXagent generated
gen = pd.DataFrame()

gen["Report Impression"] = df["generated_impression"].fillna("")


gen.to_csv(
    f"{output_dir}/chexagent_generated.csv",
    index=False
)


print("Created:")
print(f"{output_dir}/ground_truth.csv")
print(f"{output_dir}/chexagent_generated.csv")
