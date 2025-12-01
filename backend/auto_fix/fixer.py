def auto_fix(creative, validation_output):
    fixed = creative.copy()

    # Fix missing alcohol warning
    for err in validation_output["errors"]:
        if "Alcohol warning" in err:
            fixed["warning_text"] = "Drink Responsibly. 18+ Only."

    # Fix small font
    if "Font size is too small." in validation_output["warnings"]:
        fixed["font_size"] = 16

    # Fix logo position
    if "Logo not in recommended" in str(validation_output["warnings"]):
        fixed["logo_position"] = "top-right"

    return fixed