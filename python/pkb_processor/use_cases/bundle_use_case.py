import json
from datetime import datetime

from pkb_processor.adapters.storage import workspace_root, write_json


def run_bundle() -> None:
    summary_path = workspace_root() / "pkb" / "summaries" / "latest.json"
    if not summary_path.exists():
        raise RuntimeError("missing summaries; run summarize first")

    summary_data = json.loads(summary_path.read_text(encoding="utf-8"))
    count = summary_data.get("count", 0)

    payload = {
        "bundle_id": datetime.utcnow().strftime("bundle-%Y%m%d%H%M%S"),
        "goal_snapshot": "learning",
        "summary_count": count,
        "notes": "This is a starter bundle payload for AI context feeding.",
    }
    write_json(str(workspace_root() / "pkb" / "context-bundles" / "latest.json"), payload)
    print(f"[bundle] context bundle built from {count} summaries")
