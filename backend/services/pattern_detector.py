def detect_patterns(entities):
    alerts = []

    if len(entities.get("phones", [])) > 0:
        alerts.append("Suspicious phone number detected")

    if len(entities.get("emails", [])) > 0:
        alerts.append("Contact email found")

    return alerts
