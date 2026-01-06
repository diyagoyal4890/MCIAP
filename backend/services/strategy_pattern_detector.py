from collections import defaultdict

def detect_same_strategy_across_locations(records):
    patterns = defaultdict(lambda: defaultdict(list))
    alerts = []

    for r in records:
        strategy = r.get("strategy")
        state = r.get("state")
        file = r.get("file")

        if not strategy:
            continue

        if state:
            patterns[strategy][state].append(file)
        else:
            patterns[strategy]["UNKNOWN"].append(file)

    for strategy, states in patterns.items():
        valid_states = {k: v for k, v in states.items() if k != "UNKNOWN"}

        if len(valid_states) > 1:
            alerts.append({
                "type": "cross_state",
                "strategy": strategy,
                "states": valid_states
            })

        if "UNKNOWN" in states:
            alerts.append({
                "type": "missing_state",
                "strategy": strategy,
                "files": states["UNKNOWN"]
            })

    return alerts