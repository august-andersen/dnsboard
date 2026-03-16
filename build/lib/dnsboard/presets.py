import json
import sys
from pathlib import Path


def get_presets_path() -> Path:
    return Path.home() / ".dnsboard" / "presets.json"


def load_presets() -> dict[str, list[str]]:
    path = get_presets_path()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            return data
        return {}
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Could not read presets: {e}", file=sys.stderr)
        return {}


def save_preset(name: str, domains: list[str]) -> None:
    path = get_presets_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    presets = load_presets()
    presets[name] = domains
    path.write_text(json.dumps(presets, indent=2))


def delete_preset(name: str) -> bool:
    presets = load_presets()
    if name not in presets:
        return False
    del presets[name]
    path = get_presets_path()
    path.write_text(json.dumps(presets, indent=2))
    return True
