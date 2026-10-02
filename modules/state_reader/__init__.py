import json
from pathlib import Path

CANONICAL_ROOT = Path("/mnt/project")
STATE_PATH = CANONICAL_ROOT / "state" / "current.json"
STATE_PATH_FALLBACK = CANONICAL_ROOT / "current.json"

class StateReaderError(Exception):
    pass

def read_state() -> dict:
    path = STATE_PATH if STATE_PATH.exists() else STATE_PATH_FALLBACK

    if not path.exists():
        raise StateReaderError(
            f"State file not found. Tried: {STATE_PATH}, {STATE_PATH_FALLBACK}"
        )

    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                text = parts[2].strip()
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise StateReaderError(f"State file is malformed JSON: {e}")

def get_status() -> str:
    return read_state().get("status", "UNKNOWN")

def get_verified_capabilities() -> list:
    return read_state().get("verified_capabilities", [])

def get_known_bugs() -> list:
    return read_state().get("known_bugs", [])

def get_active_objective() -> str | None:
    return read_state().get("active_objective")
