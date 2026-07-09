import os
import json
import re
import warnings
import logging
import csv

# ==========================================================
# Hide warnings
# ==========================================================

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

warnings.filterwarnings("ignore")

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

# ==========================================================
# Configuration
# ==========================================================

PROJECT_ROOT = "/home/gayathr.jyothirmai/Radiology_Project"

JSONL_PATH = os.path.join(
    PROJECT_ROOT,
    "data/processed/test.jsonl",
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "outputs",
)

OUTPUT_CSV = os.path.join(
    OUTPUT_DIR,
    "chexagent_reports_100.csv",
)

NUM_IMAGES = 100

MODEL_NAME = "StanfordAIMI/CheXagent-2-3b"

# ==========================================================
# Create output directory
# ==========================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# Read dataset
# ==========================================================

with open(JSONL_PATH, "r") as f:
    samples = [json.loads(line) for line in f]

samples = samples[:NUM_IMAGES]

print("=" * 90)
print("CHEXAGENT BATCH REPORT GENERATION")
print("=" * 90)

print(f"\nTotal test images selected : {len(samples)}")

# ==========================================================
# Load model (ONLY ONCE)
# ==========================================================

print("\nLoading CheXagent model...\n")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True,
)

model.eval()

print("Model Loaded Successfully!")

# ==========================================================
# Official Findings Prompts
# ==========================================================

ANATOMIES = [
    "Airway",
    "Breathing",
    "Cardiac",
    "Diaphragm",
    "Everything else (e.g., mediastinal contours, bones, soft tissues, tubes, valves, and pacemakers)"
]

PROMPTS = [
    f'Please provide a detailed description of "{anatomy}" in the chest X-ray'
    for anatomy in ANATOMIES
]

ANATOMIES = ["View"] + ANATOMIES
PROMPTS = ["Determine the view of this CXR"] + PROMPTS

# ==========================================================
# Helper
# ==========================================================

def clean_text(text):

    text = text.replace("**", "")

    text = re.sub(r"\[[^\]]+\]", "", text)

    text = re.sub(r"<\|.*?\|>", "", text)

    text = re.sub(r"\([^)]*\)", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

# ==========================================================
# Generate Findings
# ==========================================================

def generate_findings(image_path):

    findings = ""

    for anatomy, prompt in zip(ANATOMIES, PROMPTS):

        query = tokenizer.from_list_format([
            {"image": image_path},
            {"text": prompt},
        ])

        conversation = [
            {
                "from": "system",
                "value": "You are a helpful assistant."
            },
            {
                "from": "human",
                "value": query
            },
        ]

        input_ids = tokenizer.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            return_tensors="pt",
        )

        output = model.generate(
            input_ids.to(model.device),
            do_sample=False,
            num_beams=1,
            temperature=1,
            top_p=1.0,
            use_cache=True,
            max_new_tokens=256,
            pad_token_id=tokenizer.eos_token_id,
        )

        response = tokenizer.decode(
            output[0][input_ids.shape[1]:],
            skip_special_tokens=True,
        ).strip()

        response = clean_text(response)

        if anatomy != "View":
            findings += response + " "

    findings = clean_text(findings)

    return findings


# ==========================================================
# Generate Impression
# ==========================================================

def generate_impression(findings):

    prompt = f"""
Write a professional radiology IMPRESSION section based only on the
following FINDINGS.

FINDINGS:
{findings}

Return only the Impression paragraph.
"""

    query = tokenizer.from_list_format([
        {"text": prompt}
    ])

    conversation = [
        {
            "from": "system",
            "value": "You are an expert radiologist."
        },
        {
            "from": "human",
            "value": query
        }
    ]

    input_ids = tokenizer.apply_chat_template(
        conversation,
        add_generation_prompt=True,
        return_tensors="pt",
    )

    output = model.generate(
        input_ids.to(model.device),
        do_sample=False,
        num_beams=1,
        temperature=1,
        top_p=1.0,
        use_cache=True,
        max_new_tokens=256,
        pad_token_id=tokenizer.eos_token_id,
    )

    impression = tokenizer.decode(
        output[0][input_ids.shape[1]:],
        skip_special_tokens=True,
    )

    impression = clean_text(impression)

    return impression

# ==========================================================
# Process Dataset
# ==========================================================

results = []

print("\n")
print("=" * 90)
print("STARTING BATCH GENERATION")
print("=" * 90)

for idx, sample in enumerate(samples, start=1):

    image_name = sample["image_name"]

    image_path = os.path.join(
        PROJECT_ROOT,
        sample["image_path"],
    )

    human_findings = sample["findings_text"]
    human_impression = sample["impression_text"]

    print("\n" + "-" * 90)
    print(f"Processing Image {idx}/{len(samples)}")
    print(f"Image : {image_name}")

    try:

        findings = generate_findings(image_path)

        impression = generate_impression(findings)

        results.append({

            "image_id": image_name,

            "image_path": image_path,

            "ground_truth_findings": human_findings,

            "generated_findings": findings,

            "ground_truth_impression": human_impression,

            "generated_impression": impression

        })

        print("✓ Completed")

    except Exception as e:

        print(f"✗ Error : {e}")

        results.append({

            "image_id": image_name,

            "image_path": image_path,

            "ground_truth_findings": human_findings,

            "generated_findings": "",

            "ground_truth_impression": human_impression,

            "generated_impression": "",

            "error": str(e)

        })

# ==========================================================
# Save CSV
# ==========================================================

print("\n")
print("=" * 90)
print("SAVING RESULTS")
print("=" * 90)

fieldnames = [
    "image_id",
    "image_path",
    "ground_truth_findings",
    "generated_findings",
    "ground_truth_impression",
    "generated_impression",
    "error",
]

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.DictWriter(
        csvfile,
        fieldnames=fieldnames,
        extrasaction="ignore",
    )

    writer.writeheader()

    for row in results:
        writer.writerow(row)

print(f"\nCSV saved successfully!")

print(f"\nLocation:")
print(OUTPUT_CSV)

print(f"\nTotal Images Processed : {len(results)}")

print("\n")
print("=" * 90)
print("BATCH REPORT GENERATION COMPLETED")
print("=" * 90)
