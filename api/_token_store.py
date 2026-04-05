import json
import os
from typing import Any, Dict, Optional

# NOTE: This is MVP-only. /tmp is ephemeral and can be cleared on cold start.
_TOKEN_PATH = "/tmp/polar_token.json"
_CACHE: Dict[str, Any] = {}


def load_token() -> Dict[str, Any]:
    global _CACHE
    if _CACHE:
        return _CACHE
    try:
        with open(_TOKEN_PATH, "r", encoding="utf-8") as f:
            _CACHE = json.load(f)
            return _CACHE
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def save_token(data: Dict[str, Any]) -> None:
    global _CACHE
    _CACHE = data
    try:
        with open(_TOKEN_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        # ignore for MVP
        pass


def clear_token() -> None:
    global _CACHE
    _CACHE = {}
    try:
        os.remove(_TOKEN_PATH)
    except Exception:
        pass
