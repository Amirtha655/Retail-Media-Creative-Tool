import json
import os

def load_rules():
    path = os.path.join("rules", "tesco.json")
    with open(path, "r") as f:
        return json.load(f)