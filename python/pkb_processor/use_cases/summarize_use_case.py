import json
import os
import sys
from datetime import datetime
from pathlib import Path

from pkb_processor.adapters.ai_client import summarize_note
from pkb_processor.adapters.storage import workspace_root, write_json
from pkb_processor.utils.env import load_env_file


def _load_latest_summaries_map() -> dict[str, str]:
    """
    Returns:
      note_path -> abstract
    """
    path = workspace_root() / "pkb" / "summaries" / "latest.json"
    if not path.exists():
        return {}

    try:
        prev = json.loads(path.read_text(encoding="utf-8"))
        result: dict[str, str] = {}
        for item in prev.get("summaries") or []:
            if item and item.get("note_path") and item.get("abstract"):
                result[item["note_path"]] = item["abstract"]
        return result
    except (OSError, json.JSONDecodeError):
        return {}


def run_summarize() -> None:
    load_env_file()
    ingest_path = workspace_root() / "pkb" / "state" / "ingest.json"
    if not ingest_path.exists():
        raise RuntimeError("missing ingest state; run ingest first")

    data = json.loads(ingest_path.read_text(encoding="utf-8"))
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        raise RuntimeError("missing env: OBSIDIAN_VAULT_PATH")

    existing_map = _load_latest_summaries_map()
    changed_notes = list(data.get("notes") or [])

    # A 方案：
    # - 如果本次没有变更：保留旧摘要文件，不覆盖成空。
    # - 如果本次有变更：只对变更条目调用 AI，然后与旧摘要合并再写回。
    if not changed_notes:
        if existing_map:
            print(
                f"[summarize] no changed notes; keep existing summaries ({len(existing_map)})",
                file=sys.stderr,
            )
            return

        # 首次运行且没有变更：若 ingest 里带了全量 hash，则尝试全量填充
        if data.get("hash_by_path"):
            for p in sorted(data["hash_by_path"].keys()):
                changed_notes.append({"path": p, "title": Path(p).stem})
            if changed_notes:
                print(
                    "[summarize] first run with no changed notes; filling all vault notes",
                    file=sys.stderr,
                )

    summaries_map = dict(existing_map)
    for note in changed_notes:
        content = ""
        try:
            with open(note["path"], "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            content = ""

        abstract = summarize_note(note["title"], content)
        summaries_map[note["path"]] = abstract

    summaries = [{"note_path": k, "abstract": v} for k, v in summaries_map.items()]

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
