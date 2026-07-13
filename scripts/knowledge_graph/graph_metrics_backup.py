

def calculate_f1(matches, predicted, truth):

    if predicted == 0:
        precision = 0
    else:
        precision = matches / predicted


    if truth == 0:
        recall = 0
    else:
        recall = matches / truth


    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)


    return {
        "precision": round(precision,4),
        "recall": round(recall,4),
        "f1": round(f1,4)
    }



def entity_metrics(
        generated_entities,
        groundtruth_entities):


    generated=set(generated_entities)
    truth=set(groundtruth_entities)


    matched=len(
        generated.intersection(truth)
    )


    return calculate_f1(
        matched,
        len(generated),
        len(truth)
    )



def relation_metrics(
        generated_relations,
        groundtruth_relations):


    generated=set(generated_relations)
    truth=set(groundtruth_relations)


    matched=len(
        generated.intersection(truth)
    )


    return calculate_f1(
        matched,
        len(generated),
        len(truth)
    )



def graph_score(entity_f1, relation_f1):

    return round(
        (entity_f1 + relation_f1)/2,
        4
    )
