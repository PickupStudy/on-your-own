import json
import os
import sys
from datetime import datetime
from pathlib import Path

from pkb_processor.adapters.ai_client import summarize_note
from pkb_processor.adapters.storage import workspace_root, write_json
from pkb_processor.utils.env import load_env_file


def _summaries_latest_empty() -> bool:
    path = workspace_root() / "pkb" / "summaries" / "latest.json"
    if not path.exists():
        return True
    try:
        prev = json.loads(path.read_text(encoding="utf-8"))
        return prev.get("count", 0) == 0 or not prev.get("summaries")
    except (OSError, json.JSONDecodeError):
        return True


def run_summarize() -> None:
    load_env_file()
    ingest_path = workspace_root() / "pkb" / "state" / "ingest.json"
    if not ingest_path.exists():
        raise RuntimeError("missing ingest state; run ingest first")

    data = json.loads(ingest_path.read_text(encoding="utf-8"))
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        raise RuntimeError("missing env: OBSIDIAN_VAULT_PATH")

    notes = list(data.get("notes") or [])
    if not notes and data.get("hash_by_path") and _summaries_latest_empty():
        for p in sorted(data["hash_by_path"].keys()):
            notes.append({"path": p, "title": Path(p).stem})
        if notes:
            print(
                "[summarize] no changed notes; filling all vault notes (latest summaries empty)",
                file=sys.stderr,
            )

    summaries = []
    for note in notes:
        content = ""
        try:
            with open(note["path"], "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            content = ""

        abstract = summarize_note(note["title"], content)
        summaries.append(
            {
                "note_path": note["path"],
                "abstract": abstract,
            }
        )

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(summaries),
        "summaries": summaries,
    }
    write_json(str(workspace_root() / "pkb" / "summaries" / "latest.json"), payload)
    # 延迟导入；MySQL 失败时不阻断本地 JSON 产物
    try:
        from pkb_processor.adapters.mysql_store import init_schema, save_summaries

        init_schema()
        save_summaries(summaries)
    except Exception as exc:
        print(f"[summarize] mysql skipped (file output still saved): {exc}", file=sys.stderr)

    print(f"[summarize] generated summaries: {len(summaries)}")
