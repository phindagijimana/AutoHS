"""Shared BIDS data structures for AutoHS."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class T1wScan:
    subject_label: str
    session_label: Optional[str]
    t1w_path: Path
