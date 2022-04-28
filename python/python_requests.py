
def create_drugbank_query(symptom):
    return f"\"description : *{symptom}*\""

def create_drugbank_query_side_effect(symptom):
    return f"\"toxicity : *{symptom}*\""

def create_hpo_query(symptom):
    return f"\"symptom : *{symptom}* OR synonym : *{symptom}* OR is_a : *{symptom}*\""