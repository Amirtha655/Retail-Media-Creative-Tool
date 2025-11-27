import json
import os

def load_templates():
    # Path to the templates folder
    folder = os.path.join(os.path.dirname(__file__), "..", "..", "templates")
    folder = os.path.abspath(folder)

    templates = {}

    # Load all JSON files inside /templates
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file)) as f:
                templates[file] = json.load(f)

    return templates
