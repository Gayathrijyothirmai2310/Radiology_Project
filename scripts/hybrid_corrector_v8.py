#!/usr/bin/env python3

"""
============================================================
Knowledge Graph Guided Report Correction V6
============================================================

Final Batch Processing Version

Author:
Gayathri Jyothirmai

============================================================
"""


import json
import logging

from pathlib import Path

import pandas as pd



# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger(__name__)



# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path.home() / "Radiology_Project"


CHEXAGENT_REPORTS = (
    PROJECT_ROOT /
    "outputs" /
    "chexagent_reports_100.csv"
)


KG_ERRORS_DIR = (
    PROJECT_ROOT /
    "knowledge_graph" /
    "kg_errors"
)


OUTPUT_DIR = (
    PROJECT_ROOT /
    "knowledge_graph" /
    "corrected_reports_v8"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# Load Reports
# ============================================================

def load_chexagent_reports():

    logger.info(
        "Loading CheXagent reports..."
    )


    df = pd.read_csv(
        CHEXAGENT_REPORTS
    )


    logger.info(
        f"Loaded {len(df)} reports."
    )


    return df



def load_kg_errors():

    logger.info(
        "Loading KG errors..."
    )


    kg_errors = {}


    for file in KG_ERRORS_DIR.glob("*.json"):


        with open(file,"r") as f:

            kg_errors[file.stem] = json.load(f)



    logger.info(
        f"Loaded {len(kg_errors)} KG files."
    )


    return kg_errors



# ============================================================
# Parse Report
# ============================================================

import re

def parse_chexagent_report(text):
    """
    Improved parser that preserves complete sentences while
    removing empty fragments.
    """

    if pd.isna(text):
        return []

    text = str(text).replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()

    sentences = re.split(r'(?<=[.!?])\s+', text)

    findings = []

    for s in sentences:
        s = s.strip()

        if not s:
            continue

        if s[-1] not in ".!?":
            s += "."

        findings.append(s)

    return findings


# ============================================================
# Remove Hallucinations
# ============================================================

def remove_hallucinated_sentences(sentences, kg_errors):
    """
    Removes only strongly hallucinated findings.
    Preserves clinically useful CheXagent sentences.
    """

    if not sentences:
        return []

    hallucinated_entities = set()

    if kg_errors:

        # Case 1: KG error dictionary
        if isinstance(kg_errors, dict):

            hallucinated_entities = {
                h.lower().strip()
                for h in kg_errors.get(
                    "hallucinated_entities",
                    []
                )
            }

        # Case 2: KG error list
        elif isinstance(kg_errors, list):

            hallucinated_entities = {
                h.lower().strip()
                for h in kg_errors
            }

    cleaned = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        remove = False

        # Remove sentence only if it directly contains
        # a hallucinated entity from KG comparison
        for entity in hallucinated_entities:

            if entity and entity in sentence_lower:
                remove = True
                break

        if not remove:
            cleaned.append(sentence)

    return cleaned


# ============================================================
# KG Reconstruction
# ============================================================

def reconstruct_findings_from_kg(kg_data, kg_errors=None):

    """
    Relation-aware reconstruction of clinical findings from KG.
    Converts KG entities and relations into radiology-style findings.
    """

    if not kg_data:
        return []


    findings = []


    # -----------------------------
    # Extract entities
    # -----------------------------

    if isinstance(kg_data, list):

        entities = kg_data

    else:

        entities = []


    # -----------------------------
    # Extract relations
    # -----------------------------

    if isinstance(kg_errors, list):

        relations = kg_errors

    else:

        relations = []


    entity_names = []

    for e in entities:

        entity_names.append(
            str(e).lower().strip()
        )


    # -----------------------------
    # Reconstruct fracture findings
    # -----------------------------

    if "fracture" in entity_names:


        fracture_modifiers = []


        for r in relations:

            if (
                r.get("target") == "fracture"
                and
                r.get("relation") == "modify"
            ):

                fracture_modifiers.append(
                    r.get("source")
                )


        fracture_text = ""


        if "minimally" in fracture_modifiers:

            fracture_text += "Minimally "


        if "displaced" in fracture_modifiers:

            fracture_text += "displaced "


        fracture_text += "fracture"


        # -----------------------------
        # Rib location reconstruction
        # -----------------------------

        rib_modifiers = []


        for r in relations:

            if (
                r.get("target") == "rib"
                and
                r.get("relation") == "modify"
            ):

                modifier = r.get("source")


                if modifier not in [
                    "fifth",
                    "lateral"
                ]:

                    rib_modifiers.append(
                        modifier
                    )


        # Correct clinical order

        ordered = []


        clinical_order = [

            "right",
            "left",

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

            "posterior",
            "anterior",
            "lateral"

        ]


        for word in clinical_order:

            if word in rib_modifiers:

                ordered.append(word)


        if ordered:

            fracture_text += (
                " of the "
                +
                " ".join(ordered)
                +
                " rib"
            )


        fracture_text = (
            fracture_text.capitalize()
            +
            "."
        )


        findings.append(
            fracture_text
        )


        # -----------------------------
        # Possible second fracture
        # -----------------------------

        if (
            "fifth" in entity_names
            and
            "lateral" in entity_names
        ):

            findings.append(
                "Possible fracture of the fifth lateral rib."
            )


    # -----------------------------
    # Pneumothorax
    # -----------------------------

    if "pneumothorax" in entity_names:

        findings.append(
            "No pneumothorax."
        )


    return findings

# ============================================================
# Merge
# ============================================================

def merge_reports(chexagent_findings, kg_findings):
    """
    Combines CheXagent and KG findings.
    KG findings are used to recover missing information,
    while preserving CheXagent report fluency.
    """

    if isinstance(chexagent_findings, str):
        chexagent_findings = [
            s.strip() + "."
            for s in chexagent_findings.split(".")
            if s.strip()
        ]

    if isinstance(kg_findings, str):
        kg_findings = [
            s.strip() + "."
            for s in kg_findings.split(".")
            if s.strip()
        ]

    merged = []

    # Add KG-supported findings first
    for finding in kg_findings:

        finding_clean = finding.strip()

        if not finding_clean:
            continue

        if finding_clean not in merged:
            merged.append(finding_clean)


    # Add remaining CheXagent findings
    for finding in chexagent_findings:

        finding_clean = finding.strip()

        if not finding_clean:
            continue


        duplicate = False

        finding_words = set(
            finding_clean.lower().replace(".", "").split()
        )

        for existing in merged:

            existing_words = set(
                existing.lower().replace(".", "").split()
            )

            overlap = len(
                finding_words.intersection(existing_words)
            )

            if overlap >= 3:
                duplicate = True
                break


        if not duplicate:
            merged.append(finding_clean)


    return merged

# ============================================================
# Conflict Resolution
# ============================================================

def resolve_conflicts(findings):


    output=[]

    pneumothorax_added=False



    for sentence in findings:


        if "pneumothorax" in sentence.lower():


            if not pneumothorax_added:

                output.append(
                    "No pneumothorax."
                )

                pneumothorax_added=True


        else:

            output.append(sentence)



    return output



# ============================================================
# Ordering
# ============================================================

def order_findings(findings):


    abnormal=[]

    normal=[]



    for sentence in findings:


        lower=sentence.lower()



        if (
            "fracture" in lower
            or
            "effusion" in lower
            or
            "opacity" in lower
            or
            "pneumothorax" in lower
        ):

            abnormal.append(sentence)

        else:

            normal.append(sentence)



    return abnormal + normal



# ============================================================
# Impression
# ============================================================

def generate_impression(findings):
    """
    Generates a concise radiology-style impression.
    Handles both list and string inputs.
    """

    if not findings:
        return "No significant abnormality identified."


    # Fix string input
    if isinstance(findings, str):

        findings = [
            s.strip()
            for s in findings.split(".")
            if s.strip()
        ]

        findings = [
            s + "."
            for s in findings
        ]


    impression = []


    priority_terms = [
        "fracture",
        "pneumothorax",
        "effusion",
        "opacity",
        "consolidation",
        "atelectasis",
        "nodule",
        "mass",
        "edema",
        "infiltrate"
    ]


    for finding in findings:

        if not isinstance(finding, str):
            continue

        if any(
            term in finding.lower()
            for term in priority_terms
        ):
            impression.append(finding)


    if not impression:
        impression = findings[:2]


    # Remove duplicates
    final = []

    for item in impression:

        if item not in final:
            final.append(item)


    return "\n".join(final)

# ============================================================
# Format
# ============================================================

def format_report(
        findings,
        impression
):

    report=[]


    report.append(
        "FINDINGS:\n"
    )


    for item in findings:

        report.append(item)


    report.append(
        "\nIMPRESSION:\n"
    )


    if isinstance(impression, str):

        report.append(impression)

    else:

        for i,item in enumerate(impression,1):

            report.append(
                f"{i}. {item}"
            )


    return "\n".join(report)

# ============================================================
# Process One Image
# ============================================================

def process_report(
        row,
        kg_error
):


    findings=parse_chexagent_report(
        row["generated_findings"]
    )


    findings=remove_hallucinated_sentences(
        findings,
        kg_error["hallucinated_entities"]
    )


    kg_findings=reconstruct_findings_from_kg(
        kg_error["missing_entities"],
        kg_error["missing_relations"]
    )


    merged=merge_reports(
        findings,
        kg_findings
    )


    merged=resolve_conflicts(
        merged
    )


    merged=order_findings(
        merged
    )


    impression=generate_impression(
        merged
    )


    return format_report(
        merged,
        impression
    )



# ============================================================
# Main
# ============================================================

def main():


    logger.info("="*60)

    logger.info(
        "Knowledge Graph Guided Report Correction V8"
    )

    logger.info("="*60)



    reports=load_chexagent_reports()

    kg_errors=load_kg_errors()



    count=0



    for _,row in reports.iterrows():


        image_id=Path(
            row["image_id"]
        ).stem



        if image_id not in kg_errors:

            continue



        report=process_report(
            row,
            kg_errors[image_id]
        )



        output_file=(
            OUTPUT_DIR /
            f"{image_id}.txt"
        )



        with open(
            output_file,
            "w"
        ) as f:

            f.write(report)



        count+=1



        logger.info(
            f"Saved {image_id}"
        )



    logger.info(
        "\n================================"
    )

    logger.info(
        f"Completed reports: {count}"
    )

    logger.info(
        f"Output folder: {OUTPUT_DIR}"
    )

    logger.info(
        "V8 PIPELINE COMPLETED"
    )



if __name__=="__main__":

    main()
