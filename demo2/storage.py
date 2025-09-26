import json
from pathlib import Path
from typing import Dict, Any

DATA_FILE = Path("data.json")

def load_items() -> Dict[int, Any]:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r") as f:
        return {int(k): v for k, v in json.load(f).items()}

def save_items(items: Dict[int, Any]):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)
