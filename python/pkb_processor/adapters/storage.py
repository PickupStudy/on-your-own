import json
from pathlib import Path
from typing import Any


def write_json(path: str, payload: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def workspace_root() -> Path:
    return Path.cwd().resolve().parent
