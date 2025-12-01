def calculate_score(validation_result):
    score = 100
    reasons = []

    # Hard errors = -40
    for err in validation_result["errors"]:
        score -= 40
        reasons.append(f"Major issue: {err}")

    # Warnings = -10
    for warn in validation_result["warnings"]:
        score -= 10
        reasons.append(f"Minor issue: {warn}")

    # Risk level
    if score >= 80:
        risk = "Low"
    elif 50 <= score < 80:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "score": max(score, 0),
        "risk": risk,
        "reasons": reasons
    }