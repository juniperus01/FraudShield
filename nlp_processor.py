import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    """Extract customer name, account number, bank branch, and credit score using NLP."""
    doc = nlp(text)
    entities = {
        "customer_name": "",
        "account_no": "",
        "bank_branch": "",
        "credit_score": 0
    }
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["customer_name"] = ent.text
        elif ent.label_ == "ORG":
            entities["bank_branch"] = ent.text
        elif ent.label_ == "CARDINAL":
            if len(ent.text) > 5:  # Assume large numbers are account numbers
                entities["account_no"] = ent.text
            else:  # Assume small numbers are credit scores
                entities["credit_score"] = int(ent.text) if ent.text.isdigit() else 0
    
    print(entities)

    return entities
