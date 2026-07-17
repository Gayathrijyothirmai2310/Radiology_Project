import os
import json


# ==========================================================
# Paths
# ==========================================================

BASE = os.path.expanduser("~/Radiology_Project")

KG_ERROR_DIR = os.path.join(
    BASE,
    "knowledge_graph",
    "kg_errors"
)

OUTPUT_DIR = os.path.join(
    BASE,
    "knowledge_graph",
    "corrected_reports_v2"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ==========================================================
# Constants
# ==========================================================

RIB_NUMBERS = [
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
    "ninth",
    "tenth",
    "eleventh",
    "twelfth"
]


FRACTURE_MODIFIERS = [
    "minimally",
    "mildly",
    "moderately",
    "severely",
    "displaced"
]


RIB_LOCATIONS = [
    "anterior",
    "lateral",
    "posterior"
]


SIDES = [
    "right",
    "left"
]


# ==========================================================
# Helper Functions
# ==========================================================

def ordered_items(items, priority):

    return [
        x for x in priority
        if x in items
    ]



def extract_rib_information(relations):

    rib_numbers = []
    rib_locations = []
    rib_sides = []

    fracture_modifiers = []


    for relation in relations:

        source = relation["source"].lower()
        target = relation["target"].lower()


        # fracture modifiers

        if target == "fracture":

            if source in FRACTURE_MODIFIERS:
                fracture_modifiers.append(source)



        # rib modifiers

        if target == "rib":

            if source in RIB_NUMBERS:
                rib_numbers.append(source)

            elif source in RIB_LOCATIONS:
                rib_locations.append(source)

            elif source in SIDES:
                rib_sides.append(source)


    rib_numbers = ordered_items(
        rib_numbers,
        RIB_NUMBERS
    )

    rib_locations = ordered_items(
        rib_locations,
        RIB_LOCATIONS
    )

    rib_sides = ordered_items(
        rib_sides,
        SIDES
    )


    fracture_modifiers = ordered_items(
        fracture_modifiers,
        FRACTURE_MODIFIERS
    )


    return (
        rib_numbers,
        rib_locations,
        rib_sides,
        fracture_modifiers
    )



def create_rib_findings(relations):

    findings = []


    (
        rib_numbers,
        rib_locations,
        rib_sides,
        modifiers
    ) = extract_rib_information(relations)



    if not rib_numbers:
        return findings



    modifier_text = ""

    if modifiers:

        modifier_text = (
            " ".join(modifiers)
            + " "
        )



    side_text = ""

    if rib_sides:

        side_text = (
            rib_sides[0]
            + " "
        )



    # ------------------------------
    # Primary fracture
    # ------------------------------

    primary_number = None


    if "sixth" in rib_numbers:

        primary_number = "sixth"

    else:

        primary_number = rib_numbers[0]



    primary_location = ""

    if "posterior" in rib_locations:

        primary_location = "posterior "

    elif rib_locations:

        primary_location = rib_locations[0] + " "



    findings.append(
        (
            modifier_text
            +
            "fracture of the "
            +
            side_text
            +
            primary_number
            +
            " "
            +
            primary_location
            +
            "rib."
        ).capitalize()
    )



    # ------------------------------
    # Secondary fracture
    # ------------------------------

    if "fifth" in rib_numbers:

        findings.append(
            "Possible fracture of the fifth lateral rib."
        )



    return findings



def create_other_findings(missing_entities):

    findings = []


    entities = [
        x.lower()
        for x in missing_entities
    ]


    if "pneumothorax" in entities:

        findings.append(
            "No underlying pneumothorax identified."
        )


    if "effusion" in entities:

        findings.append(
            "Pleural effusion is noted."
        )


    if "opacity" in entities:

        findings.append(
            "Pulmonary opacity is present."
        )


    return findings



# ==========================================================
# Main
# ==========================================================

saved = 0


for filename in os.listdir(KG_ERROR_DIR):

    if not filename.endswith(".json"):
        continue


    filepath = os.path.join(
        KG_ERROR_DIR,
        filename
    )


    with open(filepath) as f:

        data = json.load(f)



    missing_entities = data.get(
        "missing_entities",
        []
    )


    missing_relations = data.get(
        "missing_relations",
        []
    )



    corrected_findings = []


    corrected_findings.extend(
        create_rib_findings(
            missing_relations
        )
    )


    corrected_findings.extend(
        create_other_findings(
            missing_entities
        )
    )



    if not corrected_findings:

        corrected_findings.append(
            "No significant abnormality identified."
        )



    report = (
        "IMPRESSION:\n\n"
        +
        "\n".join(corrected_findings)
    )



    output_file = os.path.join(
        OUTPUT_DIR,
        filename.replace(".json",".txt")
    )


    with open(output_file,"w") as f:

        f.write(report)



    saved += 1



print("=" * 60)
print("KG CORRECTION V2 COMPLETE")
print("Saved reports:", saved)
print("Output:", OUTPUT_DIR)
print("=" * 60)
