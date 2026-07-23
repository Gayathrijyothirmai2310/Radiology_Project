import pandas as pd
from pathlib import Path

from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer


PROJECT_ROOT = Path.home() / "Radiology_Project"


V8_CSV = (
    PROJECT_ROOT /
    "evaluation" /
    "v8_reports.csv"
)


GROUND_TRUTH = (
    PROJECT_ROOT /
    "outputs" /
    "chexagent_reports_100.csv"
)


OUTPUT_DIR = (
    PROJECT_ROOT /
    "evaluation"
)


scores_file = OUTPUT_DIR / "v8_bleu_rouge_scores.csv"
summary_file = OUTPUT_DIR / "v8_bleu_rouge_summary.txt"



# ----------------------------
# Load Data
# ----------------------------

v8 = pd.read_csv(V8_CSV)

gt = pd.read_csv(GROUND_TRUTH)



merged = v8.merge(
    gt[
        [
            "image_id",
            "ground_truth_findings",
            "ground_truth_impression"
        ]
    ],
    on="image_id",
    how="inner"
)



print("Reports evaluated:", len(merged))



# ----------------------------
# Metrics
# ----------------------------

scorer = rouge_scorer.RougeScorer(
    [
        "rouge1",
        "rouge2",
        "rougeL"
    ],
    use_stemmer=True
)



results = []



for _, row in merged.iterrows():


    reference = str(
        row["ground_truth_findings"]
    )


    generated = str(
        row["generated_findings"]
    )


    reference_tokens = reference.split()

    generated_tokens = generated.split()



    try:

        bleu = sentence_bleu(
            [reference_tokens],
            generated_tokens
        )

    except:

        bleu = 0



    rouge = scorer.score(
        reference,
        generated
    )



    results.append(
        {
            "image_id": row["image_id"],

            "BLEU": bleu,

            "ROUGE-1":
            rouge["rouge1"].fmeasure,

            "ROUGE-2":
            rouge["rouge2"].fmeasure,

            "ROUGE-L":
            rouge["rougeL"].fmeasure
        }
    )



df = pd.DataFrame(results)



df.to_csv(
    scores_file,
    index=False
)



# ----------------------------
# Summary
# ----------------------------

summary = f"""
V8 Knowledge Graph Report Evaluation
====================================

Images Evaluated : {len(df)}

Average BLEU     : {df['BLEU'].mean():.4f}

Average ROUGE-1  : {df['ROUGE-1'].mean():.4f}

Average ROUGE-2  : {df['ROUGE-2'].mean():.4f}

Average ROUGE-L  : {df['ROUGE-L'].mean():.4f}

"""


with open(summary_file,"w") as f:

    f.write(summary)



print(summary)

print("Saved:")
print(scores_file)
print(summary_file)
