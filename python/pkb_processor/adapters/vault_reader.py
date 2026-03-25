from pathlib import Path

from pkb_processor.domain.models import Note


def read_notes(vault_path: str) -> list[Note]:
    base = Path(vault_path)
    if not base.exists():
        raise FileNotFoundError(f"vault path not found: {vault_path}")

    notes: list[Note] = []
    for md in base.rglob("*.md"):
        content = md.read_text(encoding="utf-8", errors="ignore")
        title = md.stem
        notes.append(Note(path=str(md), title=title, content=content))
    return notes
