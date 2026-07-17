# 🩻 Radiology Project

## AI-Assisted Chest X-Ray Report Generation and Knowledge Graph-Guided Evaluation using Vision-Language Models

This research project focuses on **AI-assisted chest X-ray report generation and clinical evaluation using Vision-Language Models (VLMs)**.

The study investigates the reliability of AI-generated radiology reports by comparing them with expert-written reports using automated evaluation techniques, clinical consistency analysis, hallucination detection, and Knowledge Graph-based reasoning.

The primary objective of this research is to identify limitations in AI-generated radiology reports and develop a reliable evaluation framework that improves factual accuracy, reduces hallucinations, and enhances clinical interpretability.

---

# 👩‍💻 Student

**Gayathri Jyothirmai**

Under the guidance of

**Dr. P. Krishna Reddy**

---

# 📌 Project Overview

The objective of this project is to generate chest X-ray radiology reports using advanced Vision-Language Models and evaluate their accuracy, reliability, and clinical relevance compared with expert-written radiologist reports.

The current research workflow includes:

- Chest X-ray report generation using **CheXagent**
- Automated evaluation using NLP-based metrics
- Semantic similarity evaluation
- Clinical abnormality comparison using CheXbert
- Hallucination detection using GREEN model
- Knowledge Graph-based clinical reasoning
- Analysis of AI-generated report limitations

---

# 🏗️ Repository Structure

```
Radiology_Project/
│
├── scripts/                  # Python scripts for report generation and evaluation
├── notebooks/                # Jupyter notebooks for experiments
├── outputs/                  # AI-generated reports
├── evaluation/               # Evaluation metrics and analysis results
├── logs/                     # Experiment execution logs
├── models/                   # Model configurations and references
├── knowledge_graph/          # Knowledge Graph-based analysis modules
├── data/                     # Dataset files (excluded from GitHub)
│
├── check_dataset.py          # Dataset verification script
├── push_dataset.py           # Dataset upload utility
└── README.md
```

---

# 📂 Dataset

This project uses a processed version of the **MIMIC-CXR dataset** containing chest X-ray images and corresponding radiology reports.

Due to dataset size and storage limitations, dataset files are not included in this GitHub repository.

## Processed Dataset

Hugging Face Dataset:

```
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project
```

## Annotated Dataset

An additional annotated dataset was created for enhanced clinical evaluation and future Knowledge Graph-based research.

```
https://huggingface.co/datasets/Anvesh-Lankala/Radiology_Project_Annotated
```

The GitHub repository intentionally excludes datasets because of storage limitations.

---

# 🔬 Research Workflow

The experimental pipeline consists of the following stages:

## 1. Dataset Preparation

- Chest X-ray image preprocessing
- Radiology report extraction
- Dataset organization into evaluation splits

## 2. AI Report Generation

Chest X-ray reports are generated using:

**CheXagent-2-3B Vision-Language Model**

The model generates radiologist-style:

- Findings
- Impression

sections from chest X-ray images.

## 3. Automated Report Evaluation

Generated reports are evaluated using:

- BLEU score
- ROUGE metrics
- BERTScore semantic similarity
- CheXbert clinical finding comparison
- GREEN hallucination evaluation

## 4. Knowledge Graph-Based Evaluation

A Knowledge Graph framework is developed to:

- Represent clinical findings
- Identify inconsistent observations
- Detect possible hallucinated findings
- Improve report reliability
- Provide explainable clinical reasoning

---

# 📈 Evaluation Metrics

| Metric | Purpose |
|--------|---------|
| BLEU | Measures n-gram similarity between generated and reference reports |
| ROUGE | Evaluates overlap of important clinical information |
| BERTScore | Measures semantic similarity using contextual embeddings |
| CheXbert | Compares clinical abnormalities extracted from reports |
| GREEN | Evaluates hallucination and factual consistency |

---

# 📊 Results and Outputs

Generated CheXagent reports are stored in:

```
outputs/
```

Evaluation results are stored in:

```
evaluation/
```

Knowledge Graph analysis results are stored in:

```
knowledge_graph/
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

Computing Platform:

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

## Knowledge Graph Evaluation

```bash
python knowledge_graph/<evaluation_script>.py
```

---

# 🧬 Research Contributions

This research aims to develop an improved evaluation framework for AI-generated radiology reports by integrating:

- Vision-Language Models
- Clinical information extraction
- Hallucination detection
- Knowledge Graph reasoning
- Explainable AI evaluation

The framework focuses on identifying gaps between AI-generated reports and expert radiologist reports.

---

# 🔭 Future Research Directions

Future extensions include:

- Knowledge Graph-guided report refinement
- Temporal reasoning using longitudinal radiology information
- Automated clinical error detection
- Radiology report quality scoring dashboard
- Explainable AI-based evaluation
- Reduction of hallucinated findings in generated reports

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

The long-term goal of this research is to build a reliable and transparent evaluation framework for AI-assisted radiology reporting.

By combining:

- Vision-Language Models
- Clinical Knowledge Graphs
- Hallucination detection
- Clinical reasoning
- Explainable evaluation methods

this framework aims to improve the accuracy, reliability, and clinical usefulness of AI-generated radiology reports.

---

# 👩‍💻 Student

**Gayathri Jyothirmai**

Under the guidance of

**Dr. P. Krishna Reddy**
