import re

def extract_entities(text):
    entities = {
        "phones": [],
        "emails": [],
        "states": [],
        "crimes": [],
        "vehicles": [],
        "ips": []
    }

    # Phone numbers
    entities["phones"] = re.findall(r"\b\d{10}\b", text)

    # Emails
    entities["emails"] = re.findall(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        text
    )

    # Vehicle numbers (Indian format)
    entities["vehicles"] = re.findall(
        r"\b[A-Z]{2}\s?\d{2}\s?[A-Z]{1,2}\s?\d{4}\b",
        text.upper()
    )

    # IP addresses
    entities["ips"] = re.findall(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        text
    )

    # States
    for state in ["Rajasthan", "Maharashtra", "Delhi", "Gujarat"]:
        if state.lower() in text.lower():
            entities["states"].append(state)

    # Crimes
    for crime in ["Theft", "Robbery", "Cyber Fraud", "Fraud"]:
        if crime.lower() in text.lower():
            entities["crimes"].append(crime)

    return entities
