def validate_creative(creative, rules):
    errors = []
    warnings = []
    suggestions = []

    # 1. Forbidden phrases check
    for phrase in rules["rules"]["disallowed_phrases"]:
        if phrase.lower() in creative["text"].lower():
            errors.append(f"Forbidden phrase found: {phrase}")
            suggestions.append("Remove restricted marketing claims.")

    # 2. Required logo check
    if rules["rules"]["logo_required"] and "brand_logo" not in creative:
        errors.append("Brand logo is missing.")
        suggestions.append("Upload a brand logo.")

    # 3. Alcohol creative checks
    if creative.get("category") == "alcohol":
        alcohol_rules = rules["rules"]["alcohol_warning_required"]
        if alcohol_rules and "warning_text" not in creative:
            errors.append("Alcohol warning text is missing.")
            suggestions.append("Add: 'Drink Responsibly. 18+ Only.'")

    # 4. Minimum font size
    if creative["font_size"] < rules["rules"]["min_font_size"]:
        warnings.append("Font size is too small.")
        suggestions.append("Increase text size to improve readability.")

    # 5. Logo position check
    if "brand_logo" in creative:
        if creative["logo_position"] not in rules["rules"]["allowed_logo_positions"]:
            warnings.append("Logo not in recommended position.")
            suggestions.append(f"Recommended positions: {rules['rules']['allowed_logo_positions']}")

    return {
        "status": "fail" if errors else "pass",
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions
    }