"""SQLite job queue for runnable AutoHS."""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


@dataclass
class Job:
    id: str
    input_path: str
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    work_dir: Optional[str] = None
    result_path: Optional[str] = None
    step: Optional[str] = None
    progress: int = 0


class JobQueue:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    input_path TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    error_message TEXT,
                    work_dir TEXT,
                    result_path TEXT,
                    step TEXT,
                    progress INTEGER DEFAULT 0
                )
                """
            )
            conn.commit()

    def create_job(self, input_path: Path, work_dir: Path) -> Job:
        job_id = uuid.uuid4().hex[:8]
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO jobs (id, input_path, status, created_at, work_dir, step, progress)
                VALUES (?, ?, 'pending', ?, ?, 'queued', 0)
                """,
                (job_id, str(input_path.resolve()), now, str(work_dir.resolve())),
            )
            conn.commit()
        return self.get_job(job_id)

    def get_job(self, job_id: str) -> Job:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if not row:
            raise KeyError(f"Job not found: {job_id}")
        return Job(**dict(row))

    def list_jobs(self, limit: int = 20) -> list[Job]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [Job(**dict(row)) for row in rows]

    def count_by_status(self, status: str) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS c FROM jobs WHERE status = ?", (status,)
            ).fetchone()
        return int(row["c"])

    def update_job(self, job_id: str, **fields: Any) -> None:
        if not fields:
            return
        columns = ", ".join(f"{key} = ?" for key in fields)
        values = list(fields.values()) + [job_id]
        with self._connect() as conn:
            conn.execute(f"UPDATE jobs SET {columns} WHERE id = ?", values)
            conn.commit()

    def oldest_pending(self) -> Optional[Job]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM jobs WHERE status = 'pending' ORDER BY created_at ASC LIMIT 1"
            ).fetchone()
        return Job(**dict(row)) if row else None
