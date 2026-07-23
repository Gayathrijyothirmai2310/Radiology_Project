import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score


gt_file = "/home/gayathr.jyothirmai/Radiology_Project/evaluation/chexbert_gt_labels_v8/labeled_reports.csv"

gen_file = "/home/gayathr.jyothirmai/Radiology_Project/evaluation/chexbert_v8_labels/labeled_reports.csv"
output = "/home/gayathr.jyothirmai/Radiology_Project/evaluation/chexbert_summary.txt"


gt = pd.read_csv(gt_file)
gen = pd.read_csv(gen_file)


conditions = [
    c for c in gt.columns
    if c != "Report Impression"
]


y_true = gt[conditions].values
y_pred = gen[conditions].values


# CheXbert:
# 1 = positive
# 0 = negative
# -1 = uncertain
# NaN = blank

# Convert to binary:
# positive stays 1
# uncertain/negative/blank become 0

y_true = (y_true == 1).astype(int)
y_pred = (y_pred == 1).astype(int)


scores = {}


scores["micro_precision"] = precision_score(
    y_true.flatten(),
    y_pred.flatten(),
    average="micro",
    zero_division=0
)

scores["micro_recall"] = recall_score(
    y_true.flatten(),
    y_pred.flatten(),
    average="micro",
    zero_division=0
)

scores["micro_f1"] = f1_score(
    y_true.flatten(),
    y_pred.flatten(),
    average="micro",
    zero_division=0
)


scores["macro_f1"] = f1_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0
)


with open(output, "w") as f:
    for k,v in scores.items():
        f.write(f"{k}: {v:.4f}\n")


print("\nCheXbert Clinical Scores")
print("------------------------")

for k,v in scores.items():
    print(f"{k}: {v:.4f}")


print("\nSaved:")
print(output)
