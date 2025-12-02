def validate_creative_engine(creative, rules):
    errors = []
    warnings = []
    suggestions = []

    # Forbidden phrases
    for phrase in rules["rules"]["disallowed_phrases"]:
        if phrase.lower() in creative["text"].lower():
            errors.append(f"Forbidden phrase: {phrase}")
            suggestions.append("Remove restricted marketing claims.")

    # Logo validation
    if rules["rules"]["logo_required"] and not creative.get("brand_logo"):
        errors.append("Brand logo is missing.")
        suggestions.append("Upload your brand logo.")

    # Alcohol warning
    if creative.get("category") == "alcohol":
        if not creative.get("warning_text"):
            errors.append("Alcohol warning text missing.")
            suggestions.append("Add: 'Drink Responsibly. 18+ Only.'")

    # Logo position
    if creative.get("brand_logo"):
        if creative["logo_position"] not in rules["rules"]["allowed_logo_positions"]:
            warnings.append("Logo placed incorrectly.")

    # Font size
    if creative["font_size"] < rules["rules"]["min_font_size"]:
        warnings.append("Font size too small.")
        suggestions.append("Increase font size.")

    return {
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions
    }