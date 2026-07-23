import os
import json
import pandas as pd

# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = os.path.expanduser("~/Radiology_Project")

CHEXAGENT_CSV = os.path.join(
    PROJECT_ROOT,
    "outputs",
    "chexagent_reports_100.csv"
)

KG_FOLDER = os.path.join(
    PROJECT_ROOT,
    "knowledge_graph",
    "kg_errors"
)

CORRECTED_FOLDER = os.path.join(
    PROJECT_ROOT,
    "knowledge_graph",
    "corrected_reports_v7"
)

OUTPUT_FOLDER = os.path.join(
    PROJECT_ROOT,
    "knowledge_graph",
    "comparison_reports"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
