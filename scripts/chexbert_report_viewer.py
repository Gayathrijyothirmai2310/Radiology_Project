import pandas as pd


gt_file = "/home/gayathr.jyothirmai/Radiology_Project/evaluation/chexbert_gt_labels/labeled_reports.csv"

ai_file = "/home/gayathr.jyothirmai/Radiology_Project/evaluation/chexbert_generated_labels/labeled_reports.csv"


gt = pd.read_csv(gt_file)
ai = pd.read_csv(ai_file)


conditions = [
    c for c in gt.columns
    if c != "Report Impression"
]


def convert_label(x):

    if pd.isna(x):
        return 0

    if x == 1:
        return 1

    return 0



# choose report number here
index = 0


print("\n")
print("="*65)
print("CHEXBERT CLINICAL VECTOR COMPARISON")
print("="*65)

print("\nHUMAN REPORT:")
print(gt.iloc[index]["Report Impression"])

print("\nAI GENERATED REPORT:")
print(ai.iloc[index]["Report Impression"])


print("\n")
print("-"*65)

print(
    f"{'PATHOLOGY CATEGORY':25s}"
    f"{'HUMAN':10s}"
    f"{'AI':10s}"
    f"STATUS"
)

print("-"*65)


for i,condition in enumerate(conditions):

    human = convert_label(gt.iloc[index][condition])
    model = convert_label(ai.iloc[index][condition])


    if human == model:

        if human == 1:
            status="Match (Positive)"
        else:
            status="Match (Normal)"

    else:

        if human == 0 and model == 1:
            status="FALSE POSITIVE"

        elif human == 1 and model == 0:
            status="FALSE NEGATIVE"

        else:
            status="Mismatch"


    print(
        f"{i+1}. {condition:22s}"
        f"{human:<10}"
        f"{model:<10}"
        f"{status}"
    )


print("="*65)
