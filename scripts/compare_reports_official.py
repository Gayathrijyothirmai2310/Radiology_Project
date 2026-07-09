import json
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ==========================================================
# Load first sample
# ==========================================================

jsonl_path = "/home/gayathr.jyothirmai/Radiology_Project/data/processed/test.jsonl"

with open(jsonl_path, "r") as f:
    sample = json.loads(f.readline())

image_name = sample["image_name"]

image_path = (
    "/home/gayathr.jyothirmai/Radiology_Project/"
    + sample["image_path"]
)

human_findings = sample["findings_text"]
human_impression = sample["impression_text"]

print("=" * 90)
print("IMAGE INFORMATION")
print("=" * 90)

print(f"\nImage ID   : {image_name}")
print(f"Image Path : {image_path}")

# ==========================================================
# Load Model
# ==========================================================

model_name = "StanfordAIMI/CheXagent-2-3b"

print("\nLoading CheXagent...\n")

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
# Generate Findings (Official Pipeline)
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

print("\nGenerating Findings...\n")

for anatomy, prompt in zip(anatomies, prompts):

    query = tokenizer.from_list_format([
        {"image": image_path},
        {"text": prompt},
    ])

    conversation = [
        {"from": "system", "value": "You are a helpful assistant."},
        {"from": "human", "value": query},
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

    if anatomy != "View":
        findings += response + " "

findings = re.sub(r"\s+", " ", findings).strip()

# ==========================================================
# Generate Impression
# ==========================================================

prompt = f"""
Write the Impression section for the following Findings.

Findings:
{findings}

Return only the Impression.
"""

query = tokenizer.from_list_format([
    {"text": prompt}
])

conversation = [
    {"from": "system", "value": "You are an expert radiologist."},
    {"from": "human", "value": query},
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
).strip()

impression = impression.replace("**", "")
impression = re.sub(r"\s+", " ", impression)

# ==========================================================
# Number Impression Sentences
# ==========================================================

sentences = [
    s.strip()
    for s in impression.split(".")
    if s.strip()
]

numbered_impression = ""

for i, sentence in enumerate(sentences, 1):
    numbered_impression += f"{i}. {sentence}.\n"

# ==========================================================
# Number Human Impression
# ==========================================================

human_sentences = [
    s.strip()
    for s in human_impression.split(".")
    if s.strip()
]

numbered_human = ""

for i, sentence in enumerate(human_sentences, 1):
    numbered_human += f"{i}. {sentence}.\n"

# ==========================================================
# Print Results
# ==========================================================

print("\n")
print("=" * 90)
print("HUMAN GENERATED REPORT (Ground Truth)")
print("=" * 90)

print("\nFINDINGS:\n")
print(human_findings)

print("\nIMPRESSION:\n")
print(numbered_human)

print("\n")
print("=" * 90)
print("CHEXAGENT GENERATED REPORT")
print("=" * 90)

print("\nFINDINGS:\n")
print(findings)

print("\nIMPRESSION:\n")
print(numbered_impression)
