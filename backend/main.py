from fastapi import FastAPI
from pydantic import BaseModel
from services.rule_loader import load_rules
from services.template_loader import load_templates

# Day 3 imports
from validators.validate_engine import validate_creative_engine
from crs.score_engine import calculate_score
from auto_fix.fixer import auto_fix_layout

app = FastAPI()

# -----------------------------
# Day 2 Model (KEEP AS IS)
# -----------------------------
class CreativeInput(BaseModel):
    template: str
    rule: str
    headline: str
    price: str = None
    cta: str = None
    used_colors: list = []

# -----------------------------
# Day 2 Endpoints (KEEP AS IS)
# -----------------------------
@app.get("/")
def home():
    return {"message": "Backend is running successfully"}

@app.get("/rules")
def get_rules():
    return load_rules()

@app.get("/templates")
def get_templates():
    return load_templates()

@app.post("/validate_creative")
def validate_creative(input: CreativeInput):
    rules = load_rules()[input.rule]
    templates = load_templates()[input.template]
    errors = []

    # 1. Headline length validation
    max_chars = templates["headline"]["max_characters"]
    if len(input.headline) > max_chars:
        errors.append(f"Headline too long. Maximum {max_chars} characters allowed.")

    # 2. Forbidden words
    if "disallowed_words" in rules:
        for word in rules["disallowed_words"]:
            if word.lower() in input.headline.lower():
                errors.append(f"Forbidden word used: {word}")

    # 3. Alcohol discount rule
    if "max_discount_percentage" in rules and input.price:
        try:
            percent = int(input.price.replace("%", "").replace("OFF", ""))
            if percent > rules["max_discount_percentage"]:
                errors.append(
                    f"Discount exceeds allowed limit of {rules['max_discount_percentage']}%"
                )
        except:
            pass

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

# -------------------------------------------------------
#                     DAY 3 FEATURES
# -------------------------------------------------------

# NEW Model for Layout Validation
class LayoutInput(BaseModel):
    category: str              # alcohol / lep / general
    text: str = ""             # headline or main text
    font_size: int = 14
    brand_logo: bool = False
    logo_position: str = "top-left"
    warning_text: str = None
    # You can add more layout items as needed


@app.post("/validate")
def validate_layout(layout: LayoutInput):
    rules = load_rules()
    return validate_creative_engine(layout.dict(), rules["Tesco"])


@app.post("/crs")
def creative_risk_score(layout: LayoutInput):
    rules = load_rules()
    validation_output = validate_creative_engine(layout.dict(), rules["Tesco"])
    return calculate_score(validation_output)


@app.post("/auto-fix")
def auto_fix_creative(layout: LayoutInput):
    rules = load_rules()
    validation_output = validate_creative_engine(layout.dict(), rules["Tesco"])
    fixed_layout = auto_fix_layout(layout.dict(), validation_output)
    return fixed_layout