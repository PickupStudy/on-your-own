import os
from hashlib import sha256
from datetime import datetime

from pkb_processor.adapters.storage import workspace_root, write_json
from pkb_processor.adapters.vault_reader import read_notes
from pkb_processor.utils.env import load_env_file


def run_ingest() -> None:
    load_env_file()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        raise RuntimeError("missing env: OBSIDIAN_VAULT_PATH")

    notes = read_notes(vault_path)
    state_path = workspace_root() / "pkb" / "state" / "ingest.json"
    previous_map: dict[str, str] = {}
    if state_path.exists():
        import json

        old_state = json.loads(state_path.read_text(encoding="utf-8"))
        previous_map = old_state.get("hash_by_path", {})

    changed = []
    hash_by_path = {}
    for note in notes:
        digest = sha256(note.content.encode("utf-8", errors="ignore")).hexdigest()
        hash_by_path[note.path] = digest
        if previous_map.get(note.path) != digest:
            changed.append({"path": note.path, "title": note.title})

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(notes),
        "changed_count": len(changed),
        "notes": changed,
        "hash_by_path": hash_by_path,
    }
    write_json(str(state_path), payload)
    print(f"[ingest] scanned notes: {len(notes)}, changed: {len(changed)}")
