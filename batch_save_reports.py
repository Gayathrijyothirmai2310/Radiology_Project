import os
from report_output import generate_report  # 🔥 import function

# ✅ Correct image folder
image_folder = "data/processed/mimic_cxr_images"

# ✅ Output folder
output_folder = "reports"
os.makedirs(output_folder, exist_ok=True)

# 🔁 Loop through images
for image_name in os.listdir(image_folder):

    if image_name.endswith(".png"):

        image_path = os.path.join(image_folder, image_name)
        image_id = image_name.replace(".png", "")

        # 🔥 Generate report dynamically
        report = generate_report(image_name, image_path)

        # ✅ Save
        output_path = os.path.join(output_folder, f"{image_id}.txt")

        with open(output_path, "w") as f:
            f.write(report)

        print(f"✅ Saved: {output_path}")

print("\n🎉 DONE: All reports generated!")
