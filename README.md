# 🩻 Radiology Project

## AI-Assisted Chest X-Ray Report Generation and Evaluation using Vision-Language Models

This research project focuses on **AI-assisted chest X-ray report generation and comprehensive evaluation** using Large Vision-Language Models (LVLMs). The project explores the gap between AI-generated radiology reports and expert-written reports through automated evaluation, hallucination analysis, and future Knowledge Graph-based reasoning.

---

## 👥 Authors

**Dharmavarapu Gayathri Jyothirmai**
**Anvesh Reddy Lankala**

Under the guidance of
**Dr. P. Krishna Reddy**

---

# 📌 Project Overview

The objective of this project is to generate radiology reports from chest X-ray images using advanced AI models and evaluate their clinical accuracy, similarity, and reliability compared with expert-written reports.

The current research workflow includes:

✅ Chest X-ray report generation using **CheXagent**
✅ Automated evaluation using traditional NLP metrics
✅ Semantic similarity evaluation
✅ Clinical label-based evaluation using CheXbert
✅ Hallucination detection analysis using GREEN model
✅ Counterfactual analysis
✅ Future Knowledge Graph-based evaluation and reasoning

---

# 🏗️ Repository Structure

```
Radiology_Project/
│
├── scripts/               # Python scripts for generation and evaluation
├── notebooks/             # Jupyter notebooks for experiments
├── outputs/               # Generated AI reports
├── evaluation/            # Evaluation results and metric scores
├── logs/                  # Execution logs
├── models/                # Model references/configurations
├── data/                  # Dataset files (not included in GitHub)
├── check_dataset.py
├── push_dataset.py
└── README.md
```

---

# 📂 Dataset

The project uses a processed version of the **MIMIC-CXR dataset**.

The datasets are hosted separately due to their size.

## Original Processed Dataset

📌 Dataset:

```
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project
```

## Annotated Dataset

An additional annotated dataset is introduced for enhanced evaluation and future research:

📌 Annotated Dataset:

```
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project_Annotated
```

The GitHub repository intentionally excludes datasets because of storage limitations.

---

# 🔬 Current Research Workflow

1. 📥 Prepare and preprocess chest X-ray dataset
2. 🤖 Generate reports using CheXagent
3. 💾 Store generated AI reports
4. 📊 Evaluate using BLEU
5. 📊 Evaluate using ROUGE
6. 🧠 Evaluate semantic similarity using BERTScore
7. 🩺 Compare clinical findings using CheXbert
8. ⚠️ Analyze hallucinations using GREEN model
9. 🔍 Perform counterfactual analysis
10. 🕸️ Develop Knowledge Graph based evaluation framework (ongoing)

---

# 📈 Evaluation Metrics

Current evaluation includes:

| Metric    | Purpose                                                            |
| --------- | ------------------------------------------------------------------ |
| BLEU      | Measures n-gram similarity between generated and reference reports |
| ROUGE     | Evaluates overlap of important report information                  |
| BERTScore | Measures semantic similarity using contextual embeddings           |
| CheXbert  | Compares clinical observations and abnormalities                   |
| GREEN     | Evaluates hallucinations and factual consistency                   |

Additional evaluation methods will be integrated during future development.

---

# 📊 Results

Generated reports are stored in:

```
outputs/
```

Evaluation results are stored in:

```
evaluation/
```

Execution logs are stored in:

```
logs/
```

---

# ⚙️ Environment

## Python

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

## Generate Reports

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

This project aims to move beyond simple text similarity evaluation and develop a clinically meaningful evaluation framework for AI-generated radiology reports.

Future research directions include:

* 🟢 Hallucination detection and reduction using GREEN model
* 🔄 Counterfactual Contrastive Learning (CCL) for improving report reliability
* 🕒 Temporal comparison of longitudinal radiology reports
* 🕸️ Knowledge Graph construction for clinical reasoning
* 🚨 Automatic error detection in generated reports
* 📊 Radiology report quality scoring dashboard
* 🔍 Explainable AI-based evaluation methods

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

The long-term goal of this research is to develop a robust evaluation framework for AI-generated radiology reports by combining:

🩻 Vision-Language Models
🧠 Clinical Knowledge Representation
🕸️ Knowledge Graph Reasoning
⚠️ Hallucination Detection
🔄 Counterfactual Learning

to improve the reliability, transparency, and clinical usefulness of AI-assisted radiology systems.

---

# 👩‍💻 Author

**Dharmavarapu Gayathri Jyothirmai**
**Anvesh Reddy Lankala**

Under the guidance of
**Dr. P. Krishna Reddy**
