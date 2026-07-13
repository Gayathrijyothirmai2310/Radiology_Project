import re



# -------------------------------------------------
# Medical Entity Normalization
# -------------------------------------------------

def normalize_entity(entity):

    entity = entity.lower().strip()


    # remove punctuation
    entity = re.sub(
        r"[^a-z0-9\s]",
        "",
        entity
    )


    # common radiology synonyms
    replacements = {

        "ptx": "pneumothorax",

        "pleural fluid": "pleural effusion",

        "fluid in pleural space": "pleural effusion",

        "opacity": "opacity",

        "opacities": "opacity",

        "fractured rib": "rib fracture",

        "fracture of rib": "rib fracture",

        "ribs fracture": "rib fracture",

        "atelectatic": "atelectasis",

        "collapsed lung": "atelectasis",

        "enlarged heart": "cardiomegaly",

        "heart enlargement": "cardiomegaly"

    }


    if entity in replacements:
        entity = replacements[entity]


    # remove common modifiers
    remove_words = [
        "mild",
        "small",
        "large",
        "acute",
        "chronic",
        "possible",
        "minimal",
        "slight",
        "stable"
    ]


    words = entity.split()


    words = [
        w for w in words
        if w not in remove_words
    ]


    entity = " ".join(words)


    return entity





# -------------------------------------------------
# F1 calculation
# -------------------------------------------------

def calculate_f1(matches, predicted, truth):


    precision = (
        matches / predicted
        if predicted > 0
        else 0
    )


    recall = (
        matches / truth
        if truth > 0
        else 0
    )


    if precision + recall == 0:
        f1 = 0

    else:
        f1 = (
            2 *
            precision *
            recall /
            (precision + recall)
        )


    return {

        "precision": round(precision,4),

        "recall": round(recall,4),

        "f1": round(f1,4)

    }





# -------------------------------------------------
# Entity Metrics
# -------------------------------------------------

def entity_metrics(
        generated_entities,
        groundtruth_entities):


    generated=set(
        normalize_entity(x)
        for x in generated_entities
    )


    truth=set(
        normalize_entity(x)
        for x in groundtruth_entities
    )


    matched=len(
        generated.intersection(truth)
    )


    return calculate_f1(
        matched,
        len(generated),
        len(truth)
    )





# -------------------------------------------------
# Relation Metrics
# -------------------------------------------------

def relation_metrics(
        generated_relations,
        groundtruth_relations):


    generated=set(
        (
            normalize_entity(x[0]),
            x[1],
            normalize_entity(x[2])
        )
        for x in generated_relations
    )


    truth=set(
        (
            normalize_entity(x[0]),
            x[1],
            normalize_entity(x[2])
        )
        for x in groundtruth_relations
    )


    matched=len(
        generated.intersection(truth)
    )


    return calculate_f1(
        matched,
        len(generated),
        len(truth)
    )





# -------------------------------------------------
# Overall Graph Score
# -------------------------------------------------

def graph_score(
        entity_f1,
        relation_f1):


    return round(
        (entity_f1 + relation_f1) / 2,
        4
    )
