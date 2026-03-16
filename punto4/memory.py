# memory.py
# Handles persistent client memory between sessions (local JSON)

import json
import os
from datetime import datetime, timezone

MEMORY_FILE = "memory.json"


def load_memory() -> dict:
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def get_client_memory(client_id: str) -> dict | None:
    memory = load_memory()
    return memory.get(client_id, None)


def save_client_memory(client_id: str, bank: str, state: str, account_type: str):
    memory = load_memory()
    memory[client_id] = {
        "bank":          bank,
        "state":         state,
        "account_type":  account_type,
        "last_funded_at": datetime.now(timezone.utc).isoformat()
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
