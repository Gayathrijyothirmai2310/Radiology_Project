# Radiology Project

AI-assisted chest X-ray report generation and evaluation using CheXagent, BLEU, ROUGE, BERTScore, CheXbert, and future Knowledge Graph based analysis.

---

## Project Overview

This project focuses on generating radiology reports from chest X-ray images using Large Vision-Language Models (LVLMs) and evaluating their quality against expert-written reports.

Current work includes:

- Report generation using CheXagent
- Automatic evaluation using BLEU
- ROUGE evaluation
- BERTScore evaluation
- CheXbert label comparison
- Counterfactual analysis
- Knowledge Graph based evaluation (Work in Progress)

---

## Repository Structure

```
Radiology_Project/
│
├── scripts/               # Python scripts
├── notebooks/             # Jupyter notebooks
├── outputs/               # Generated reports
├── evaluation/            # Evaluation results
├── logs/                  # Execution logs
├── models/                # Model references/configs
├── data/                  # (Not included in GitHub)
├── check_dataset.py
├── push_dataset.py
└── README.md
```

---

## Dataset

The dataset is hosted separately on Hugging Face.

Dataset:

https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project

The GitHub repository intentionally excludes the dataset because of its size.

---

## Current Workflow

1. Prepare dataset
2. Generate reports using CheXagent
3. Save generated reports
4. Evaluate using BLEU
5. Evaluate using ROUGE
6. Evaluate using BERTScore
7. Evaluate using CheXbert
8. Perform Knowledge Graph analysis (ongoing)

---

## Evaluation Metrics

Current evaluation includes:

- BLEU
- ROUGE
- BERTScore
- CheXbert

Additional metrics may be added during future development.

---

## Results

Generated reports are stored inside:

```
outputs/
```

Evaluation summaries are stored inside:

```
evaluation/
```

Execution logs are stored inside:

```
logs/
```

---

## Environment

Python 3.10

Conda Environment:

```
chexagent
```

GPU:

- NVIDIA RTX 6000 Ada

Platform:

- Turing HPC Cluster

---

## Running the Project

Generate reports

```bash
python scripts/compare_reports_official.py
```

Evaluate BLEU and ROUGE

```bash
python scripts/evaluate_bleu_rouge.py
```

Evaluate BERTScore

```bash
python scripts/evaluate_bertscore.py
```

---

## Repository

Code:
https://github.com/Gayathrijyothirmai2310/Radiology_Project

Dataset:
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project

---

## Future Work

- Improve report generation quality
- Reduce hallucinations
- Temporal report comparison
- Knowledge Graph construction
- Automatic error detection
- Report quality scoring dashboard

---

## Author

Gayathri Jyothirmai

Research Project