import json
import os

def load_rules():
    # Path to the rules folder
    folder = os.path.join(os.path.dirname(__file__), "..", "..", "rules")
    folder = os.path.abspath(folder)

    rules = {}

    # Load all JSON files inside /rules
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file)) as f:
                rules[file] = json.load(f)

    return rules
