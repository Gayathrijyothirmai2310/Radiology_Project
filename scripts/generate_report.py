import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# -----------------------------
# Model
# -----------------------------
model_name = "StanfordAIMI/CheXagent-2-3b"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    trust_remote_code=True
)
model.eval()

# -----------------------------
# Image Path
# -----------------------------
image_path = "/home/gayathr.jyothirmai/Radiology_Project/data/processed/mimic_cxr_images/image_0000.png"

# -----------------------------
# Prompt
# -----------------------------
prompt = "Generate a detailed radiology report for this chest X-ray."

query = tokenizer.from_list_format([
    {"image": image_path},
    {"text": prompt},
])

conversation = [
    {
        "from": "system",
        "value": "You are a helpful radiology assistant."
    },
    {
        "from": "human",
        "value": query
    }
]

input_ids = tokenizer.apply_chat_template(
    conversation,
    add_generation_prompt=True,
    return_tensors="pt"
)

print("Generating report...")

output = model.generate(
    input_ids.to(model.device),
    max_new_tokens=512,
    do_sample=False
)

report = tokenizer.decode(
    output[0][input_ids.shape[1]:-1],
    skip_special_tokens=True
)

print("\n==========================")
print("Generated Report")
print("==========================")
print(report)
