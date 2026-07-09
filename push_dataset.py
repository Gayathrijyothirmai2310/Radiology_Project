import os
import pandas as pd
from datasets import Dataset, Image

# === UPDATE YOUR HUGGING FACE CREDENTIALS HERE ===
HF_USERNAME = "Anvesh-Lankala"  # e.g., "gayathr-j"
REPO_NAME = "Radiology_Project"   # What you want to call it on HF
# =================================================

CSV_FILE = "data/processed/mimic_cxr_processed.csv"
IMAGE_DIR = "data/processed/mimic_cxr_images"

print("🚀 Step 1: Loading metadata CSV...")
df = pd.read_csv(CSV_FILE)

print("🔗 Step 2: Mapping image paths to dataframe...")
# Since 'image_name' already has '.png' at the end, we just join the folder path to it!
def get_full_path(img_name):
    return os.path.join(IMAGE_DIR, str(img_name))

# Create the 'image' column Hugging Face needs
df["image"] = df["image_name"].apply(get_full_path)

print("🖼️ Step 3: Converting to Hugging Face Image Dataset...")
dataset = Dataset.from_pandas(df)

# Cast the string paths into actual Image objects
dataset = dataset.cast_column("image", Image())

print("\n📊 Dataset successfully prepared:")
print(dataset)

print(f"\n📤 Step 4: Uploading to Hugging Face Hub as '{HF_USERNAME}/{REPO_NAME}'...")
# This streams everything directly to your repository
dataset.push_to_hub(f"{HF_USERNAME}/{REPO_NAME}")

print("\n✅ Success! Your image dataset has been uploaded to the hub.")
