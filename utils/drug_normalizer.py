import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "medicines.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    MEDICINES = json.load(f)

def normalize_drug(name: str):
    name = name.strip().lower()
    for key, data in MEDICINES.items():
        if name == key or name in [a.lower() for a in data["aliases"]]:
            return key
    return None
