import os
from typing import Any


def mysql_enabled() -> bool:
    return os.getenv("MYSQL_ENABLED", "false").lower() == "true"


def _connect():
    import pymysql

    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "pkb"),
        charset="utf8mb4",
        autocommit=False,
    )


def init_schema() -> None:
    if not mysql_enabled():
        return

    conn = _connect()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pkb_summaries (
              id BIGINT PRIMARY KEY AUTO_INCREMENT,
              note_path TEXT NOT NULL,
              abstract_text LONGTEXT NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              UNIQUE KEY uniq_note_path (note_path(255))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_summaries(items: list[dict[str, Any]]) -> None:
    if not mysql_enabled() or not items:
        return

    conn = _connect()
    try:
        cur = conn.cursor()
        cur.executemany(
            """
            INSERT INTO pkb_summaries (note_path, abstract_text)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE abstract_text = VALUES(abstract_text)
            """,
            [(item["note_path"], item["abstract"]) for item in items],
        )
        conn.commit()
    finally:
        conn.close()
