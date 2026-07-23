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
    "corrected_reports_v6"
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

def parse_chexagent_report(text):

    findings=[]


    if pd.isna(text):

        return findings



    for sentence in str(text).split("."):

        sentence = sentence.strip()


        if sentence:

            findings.append(
                sentence+"."
            )


    return findings



# ============================================================
# Remove Hallucinations
# ============================================================

def remove_hallucinated_sentences(
        findings,
        hallucinated_entities
):


    cleaned=[]



    for sentence in findings:


        remove=False


        for entity in hallucinated_entities:


            if entity.lower() in sentence.lower():

                remove=True

                break



        if not remove:

            cleaned.append(sentence)



    return cleaned



# ============================================================
# KG Reconstruction
# ============================================================

def reconstruct_findings_from_kg(
        missing_entities,
        missing_relations
):


    entities=set(
        x.lower()
        for x in missing_entities
    )


    findings=[]



    # Rib fractures

    if (
        "fracture" in entities
        and
        "rib" in entities
    ):


        if (
            "sixth" in entities
            and
            "posterior" in entities
        ):

            findings.append(
                "Minimally displaced fracture of the right sixth posterior rib."
            )



        if (
            "fifth" in entities
            and
            "lateral" in entities
        ):

            findings.append(
                "Possible fracture of the right fifth lateral rib."
            )



    # Pneumothorax

    if "pneumothorax" in entities:

        findings.append(
            "No pneumothorax."
        )



    # Effusion

    if "effusion" in entities:

        findings.append(
            "Pleural effusion is present."
        )



    # Opacity

    if (
        "opacity" in entities
        or
        "opacities" in entities
    ):

        findings.append(
            "Pulmonary opacity is present."
        )


    return findings



# ============================================================
# Merge
# ============================================================

def merge_reports(
        chexagent,
        kg_findings
):


    merged=[]

    seen=set()



    for sentence in chexagent + kg_findings:


        key=(
            sentence.lower()
            .replace(
                "there is",
                ""
            )
            .replace(
                " ",
                ""
            )
        )



        if key not in seen:

            merged.append(sentence)

            seen.add(key)



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


    impression=[]



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

            impression.append(sentence)



    return impression



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
        "Knowledge Graph Guided Report Correction V6"
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
        "V6 PIPELINE COMPLETED"
    )



if __name__=="__main__":

    main()
