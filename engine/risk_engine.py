SEVERITY_POINTS = {"HIGH": 30, "MEDIUM": 15, "LOW": 5}

def calculate_score(alerts):
    score = max(0, 100 - sum(SEVERITY_POINTS.get(a["severity"], 0) for a in alerts))
    if any(a["severity"] == "HIGH" for a in alerts):
        level = "HIGH RISK"
    elif any(a["severity"] == "MEDIUM" for a in alerts):
        level = "REVIEW"
    else:
        level = "LOW RISK"
    return score, level
