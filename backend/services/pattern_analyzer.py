from collections import defaultdict

def detect_crime_patterns(records):
    """
    Detects same crime happening in multiple states
    and extracts common strategy indicators
    """

    patterns = defaultdict(list)

    for r in records:
        crime = r.get("crime")
        if not crime:
            continue

        patterns[crime].append(r)

    results = []

    for crime, recs in patterns.items():
        if len(recs) < 2:
            continue  # needs at least 2 cases

        states = list(set(r.get("state") for r in recs if r.get("state")))
        phones = list(set(r.get("phone") for r in recs if r.get("phone")))
        vehicles = list(set(r.get("vehicle") for r in recs if r.get("vehicle")))
        ips = list(set(r.get("ip") for r in recs if r.get("ip")))

        if len(states) > 1:
            results.append({
                "crime": crime,
                "states": states,
                "phone": phones[0] if phones else None,
                "vehicle": vehicles[0] if vehicles else None,
                "ip": ips[0] if ips else None,
            })

    return results
