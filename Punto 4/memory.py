# memory.py
import json
import os
from datetime import datetime, timezone

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")


def load_memory() -> dict:
    try:
        if not os.path.exists(MEMORY_FILE):
            return {}
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def get_client_memory(client_id: str) -> dict | None:
    memory = load_memory()
    return memory.get(client_id, None)


def save_client_memory(client_id: str, bank: str, state: str, account_type: str):
    try:
        memory = load_memory()
        memory[client_id] = {
            "bank":           bank,
            "state":          state,
            "account_type":   account_type,
            "last_funded_at": datetime.now(timezone.utc).isoformat()
        }
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)
    except Exception:
        # In cloud environments the filesystem may be read-only
        # Memory will persist only within the current session
        pass
