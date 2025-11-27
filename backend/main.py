from fastapi import FastAPI
from pydantic import BaseModel
from services.rule_loader import load_rules
from services.template_loader import load_templates

app = FastAPI()

# Model for validation request
class CreativeInput(BaseModel):
    template: str
    rule: str
    headline: str
    price: str = None
    cta: str = None
    used_colors: list = []

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

    # 1. Check headline length
    max_chars = templates["headline"]["max_characters"]
    if len(input.headline) > max_chars:
        errors.append(f"Headline too long. Maximum {max_chars} characters allowed.")

    # 2. Check forbidden words
    if "disallowed_words" in rules:
        for word in rules["disallowed_words"]:
            if word.lower() in input.headline.lower():
                errors.append(f"Forbidden word used: {word}")

    # 3. Check alcohol discount
    if "max_discount_percentage" in rules and input.price:
        try:
            percent = int(input.price.replace("%", "").replace("OFF", ""))
            if percent > rules["max_discount_percentage"]:
                errors.append(f"Discount exceeds allowed limit: {rules['max_discount_percentage']}%")
        except:
            pass

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
