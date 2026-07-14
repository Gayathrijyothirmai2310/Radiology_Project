import os
import json

# -----------------------------
# Paths
# -----------------------------
BASE = os.path.expanduser("~/Radiology_Project")

ERROR_DIR = os.path.join(BASE,
                         "knowledge_graph",
                         "kg_errors")

OUTPUT_DIR = os.path.join(BASE,
                          "knowledge_graph",
                          "recommendations")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Clinical recommendation rules
# -----------------------------

RULES = {

    "fracture":
        "Possible fracture detected. Review the affected bone carefully.",

    "pneumothorax":
        "Consider evaluating for pneumothorax.",

    "effusion":
        "Consider evaluating for pleural effusion.",

    "edema":
        "Review for pulmonary edema.",

    "opacity":
        "Review the reported pulmonary opacity.",

    "consolidation":
        "Consider evaluating for consolidation.",

    "atelectasis":
        "Review for possible atelectasis.",

    "nodule":
        "Consider evaluating for pulmonary nodule.",

    "mass":
        "Review for pulmonary mass.",

    "cardiomegaly":
        "Evaluate cardiac silhouette for cardiomegaly.",

    "rib":
        "Review the rib region carefully.",

    "pleural":
        "Review pleural findings.",

    "pneumonia":
        "Consider evaluating for pneumonia.",

    "device":
        "Verify the position of support devices.",

    "tube":
        "Verify tube placement.",

    "line":
        "Verify line placement."
}


def recommendation(entity):

    entity = entity.lower().strip()

    for key in RULES:

        if key in entity:
            return RULES[key]

    return f"Review finding: {entity}."


files = sorted(os.listdir(ERROR_DIR))

print(f"\nFound {len(files)} KG error files.\n")

count = 0

for file in files:

    if not file.endswith(".json"):
        continue

    with open(os.path.join(ERROR_DIR, file), "r") as f:
        data = json.load(f)

    image_id = data["image_id"]

    missing = sorted(set(data["missing_entities"]))
    hallucinated = sorted(set(data["hallucinated_entities"]))

    output = []

    output.append("Knowledge Graph Recommendations")
    output.append("=" * 40)
    output.append("")

    # -----------------------------
    # Missing Findings
    # -----------------------------

    if missing:

        output.append("Missing Findings")
        output.append("----------------")

        for m in missing:
            output.append(f"• {recommendation(m)}")

        output.append("")

    # -----------------------------
    # Unsupported Findings
    # -----------------------------

    if hallucinated:

        output.append("Unsupported Findings")
        output.append("--------------------")

        for h in hallucinated:
            output.append(
                f"• '{h}' is not supported by the reference graph."
            )

        output.append("")

    # -----------------------------
    # Final Recommendation
    # -----------------------------

    output.append("Clinical Recommendation")
    output.append("-----------------------")

    output.append(
        "Review the above findings before finalizing the report."
    )

    output.append(
        "Remove unsupported observations if they are clinically inappropriate."
    )

    output.append(
        "Consider incorporating clinically relevant missing findings."
    )

    with open(os.path.join(OUTPUT_DIR,
                           image_id + ".txt"), "w") as f:

        f.write("\n".join(output))

    count += 1

print("=" * 60)
print(f"Generated recommendations : {count}")
print(f"Saved to : {OUTPUT_DIR}")
print("=" * 60)
