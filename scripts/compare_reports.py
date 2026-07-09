import os
import json
import re
import random
import warnings
import logging

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
# Load test dataset
# ==========================================================

jsonl_path = "/home/gayathr.jyothirmai/Radiology_Project/data/processed/test.jsonl"

with open(jsonl_path, "r") as f:
    samples = [json.loads(line) for line in f]

# ==========================================================
# Pick a random image every run
# ==========================================================

sample = random.choice(samples)

image_name = sample["image_name"]

image_path = os.path.join(
    "/home/gayathr.jyothirmai/Radiology_Project",
    sample["image_path"],
)

human_findings = sample["findings_text"]
human_impression = sample["impression_text"]

# ==========================================================
# Display selected image
# ==========================================================

print("\n")
print("=" * 90)
print("IMAGE INFORMATION")
print("=" * 90)

print(f"\nImage ID   : {image_name}")
print(f"Image Path : {image_path}")

# ==========================================================
# Load CheXagent
# ==========================================================

model_name = "StanfordAIMI/CheXagent-2-3b"

print("\nLoading CheXagent model...\n")

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    trust_remote_code=True,
)

model.eval()

print("Model Loaded Successfully!")

# ==========================================================
# Official Findings Pipeline
# ==========================================================

anatomies = [
    "Airway",
    "Breathing",
    "Cardiac",
    "Diaphragm",
    "Everything else (e.g., mediastinal contours, bones, soft tissues, tubes, valves, and pacemakers)"
]

prompts = [
    f'Please provide a detailed description of "{anatomy}" in the chest X-ray'
    for anatomy in anatomies
]

anatomies = ["View"] + anatomies
prompts = ["Determine the view of this CXR"] + prompts

findings = ""

print("\n")
print("=" * 90)
print("GENERATING FINDINGS")
print("=" * 90)

for anatomy, prompt in zip(anatomies, prompts):

    print(f"\nGenerating {anatomy}...")

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

    response = response.replace("**", "")

    response = re.sub(r"\[[^\]]+\]", "", response)

    response = re.sub(r"\s+", " ", response).strip()

    print(response)

    if anatomy != "View":
        findings += response + " "

findings = re.sub(r"\s+", " ", findings).strip()
# ==========================================================
# Clean Findings
# ==========================================================

findings = findings.replace("**", "")
findings = re.sub(r"\[[^\]]+\]", "", findings)
findings = re.sub(r"<\|.*?\|>", "", findings)
findings = re.sub(r"\([^)]*\)", "", findings)
findings = re.sub(r"\s+", " ", findings).strip()

print("\n")
print("=" * 90)
print("FINAL FINDINGS")
print("=" * 90)
print(findings)

# ==========================================================
# Generate Impression
# ==========================================================

print("\n")
print("=" * 90)
print("GENERATING IMPRESSION")
print("=" * 90)

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

impression = impression.replace("**", "")
impression = re.sub(r"\[[^\]]+\]", "", impression)
impression = re.sub(r"<\|.*?\|>", "", impression)
impression = re.sub(r"\([^)]*\)", "", impression)
impression = re.sub(r"\s+", " ", impression).strip()

# ==========================================================
# Number Human Impression
# ==========================================================

human_sentences = [
    s.strip()
    for s in human_impression.split(".")
    if s.strip()
]

human_numbered = ""

for i, sentence in enumerate(human_sentences, 1):
    human_numbered += f"{i}. {sentence}.\n"

# ==========================================================
# Number AI Impression
# ==========================================================

ai_sentences = [
    s.strip()
    for s in impression.split(".")
    if s.strip()
]

ai_numbered = ""

for i, sentence in enumerate(ai_sentences, 1):
    ai_numbered += f"{i}. {sentence}.\n"

# ==========================================================
# Print Final Comparison
# ==========================================================

print("\n")
print("=" * 90)
print("HUMAN GENERATED REPORT (Ground Truth)")
print("=" * 90)

print("\nIMAGE ID:")
print(image_name)

print("\nIMAGE PATH:")
print(image_path)

print("\nFINDINGS:\n")
print(human_findings)

print("\nIMPRESSION:\n")
print(human_numbered)

print("\n")
print("=" * 90)
print("CHEXAGENT GENERATED REPORT")
print("=" * 90)

print("\nIMAGE ID:")
print(image_name)

print("\nIMAGE PATH:")
print(image_path)

print("\nFINDINGS:\n")
print(findings)

print("\nIMPRESSION:\n")

if ai_numbered.strip():
    print(ai_numbered)
else:
    print("1. No impression generated.")

print("\n")
print("=" * 90)
print("END OF REPORT")
print("=" * 90)
