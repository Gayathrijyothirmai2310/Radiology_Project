# 🩻 Radiology Project

## AI-Assisted Chest X-Ray Report Generation and Evaluation using Vision-Language Models

This research project focuses on **AI-assisted chest X-ray report generation and comprehensive evaluation** using Large Vision-Language Models (LVLMs). The study investigates the gap between AI-generated radiology reports and expert-written reports through automated evaluation, hallucination analysis, clinical consistency checking, and future Knowledge Graph-based reasoning.

---

# 👥 Authors

Dharmavarapu Gayathri Jyothirmai

Anvesh Reddy Lankala

Under the guidance of

Dr. P. Krishna Reddy

---

# 📌 Project Overview

The objective of this project is to generate radiology reports from chest X-ray images using advanced Vision-Language Models and evaluate their accuracy, reliability, and clinical relevance compared with expert-written reports.

The current research workflow includes:

- Chest X-ray report generation using CheXagent

- Automated evaluation using traditional NLP metrics

- Semantic similarity evaluation

- Clinical finding comparison using CheXbert

- Hallucination detection using GREEN model

- Counterfactual analysis for reliability assessment

- Future Knowledge Graph-based clinical reasoning and evaluation

---

# 🏗️ Repository Structure

```
Radiology_Project/
│
├── scripts/                  # Python scripts for report generation and evaluation
├── notebooks/                # Jupyter notebooks for experiments
├── outputs/                  # AI-generated reports and predictions
├── evaluation/               # Evaluation metrics and analysis results
├── logs/                     # Execution and experiment logs
├── models/                   # Model references and configurations
├── data/                     # Dataset files (excluded from GitHub)
│
├── check_dataset.py          # Dataset verification script
├── push_dataset.py           # Dataset upload utility
└── README.md
```

---

# 📂 Dataset

This project uses a processed version of the **MIMIC-CXR dataset**.

Due to dataset size and storage limitations, the dataset files are not included in this GitHub repository.

## Original Processed Dataset

Dataset:

```
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project
```

## Annotated Dataset

An additional annotated dataset has been created for enhanced evaluation and future research.

Dataset:

```
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project_Annotated
```

The GitHub repository intentionally excludes datasets because of storage limitations.

---

# 🔬 Research Workflow

The current experimental pipeline consists of:

1. Dataset preparation and preprocessing

2. Chest X-ray report generation using CheXagent

3. Storage of AI-generated reports

4. Evaluation using BLEU score

5. Evaluation using ROUGE metrics

6. Semantic similarity evaluation using BERTScore

7. Clinical abnormality comparison using CheXbert

8. Hallucination detection analysis using GREEN model

9. Counterfactual analysis for model reliability

10. Knowledge Graph-based evaluation framework development (ongoing)

---

# 📈 Evaluation Metrics

The project evaluates generated reports using multiple complementary metrics:

| Metric | Purpose |
|--------|---------|
| BLEU | Measures n-gram similarity between generated and reference reports |
| ROUGE | Evaluates overlap of important clinical information |
| BERTScore | Measures semantic similarity using contextual embeddings |
| CheXbert | Compares clinical observations and abnormalities |
| GREEN | Evaluates hallucination and factual consistency |

Additional evaluation methods will be integrated as the research progresses.

---

# 📊 Results and Outputs

Generated reports are stored in:

```
outputs/
```

Evaluation results are stored in:

```
evaluation/
```

Experiment execution logs are stored in:

```
logs/
```

---

# ⚙️ Environment Setup

## Programming Language

```
Python 3.10
```

## Conda Environment

```
chexagent
```

## Hardware

GPU:

```
NVIDIA RTX 6000 Ada Generation
```

Platform:

```
Turing HPC Cluster
```

---

# 🚀 Running the Project

## Generate AI Reports

```bash
python scripts/compare_reports_official.py
```

## Evaluate BLEU and ROUGE

```bash
python scripts/evaluate_bleu_rouge.py
```

## Evaluate BERTScore

```bash
python scripts/evaluate_bertscore.py
```

## Evaluate CheXbert

```bash
python scripts/evaluate_chexbert.py
```

---

# 🧬 Research Direction

The goal of this research is to develop a clinically meaningful evaluation framework that goes beyond traditional text similarity metrics.

Future research directions include:

- Hallucination detection and reduction using GREEN model

- Counterfactual Contrastive Learning (CCL) for improving report reliability

- Temporal comparison of longitudinal radiology reports

- Knowledge Graph construction for clinical reasoning

- Automatic error detection in AI-generated reports

- Radiology report quality scoring dashboard

- Explainable AI-based evaluation methods

---

# 🔗 Repository Links

## Code Repository

```
https://github.com/Gayathrijyothirmai2310/Radiology_Project
```

## Dataset

```
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project
```

## Annotated Dataset

```
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project_Annotated
```

---

# 🌟 Future Vision

The long-term objective of this research is to develop a reliable and transparent evaluation framework for AI-generated radiology reports by integrating:

- Vision-Language Models

- Clinical Knowledge Representation

- Knowledge Graph Reasoning

- Hallucination Detection

- Counterfactual Learning

This framework aims to improve the reliability, interpretability, and clinical usefulness of AI-assisted radiology systems.

---

# 👩‍💻 Authors

Dharmavarapu Gayathri Jyothirmai

Anvesh Reddy Lankala

Under the guidance of

Dr. P. Krishna Reddy