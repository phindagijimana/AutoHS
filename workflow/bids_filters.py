"""PyBIDS filter file loading for AutoHS BIDS App queries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_bids_filter_file(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"BIDS filter file must contain a JSON object: {path}")
    return payload


def t1w_query_filters(bids_filter_file: Path | None) -> tuple[dict[str, Any], bool]:
    """Return PyBIDS kwargs and regex_search flag for the T1w query."""
    if bids_filter_file is None:
        return {}, False

    filters = load_bids_filter_file(bids_filter_file)
    t1w = filters.get("t1w", {})
    if not isinstance(t1w, dict):
        raise ValueError("BIDS filter file 't1w' entry must be a JSON object.")

    query = dict(t1w)
    regex_search = query.pop("regex_search", False)
    if isinstance(regex_search, str):
        regex_search = regex_search.lower() in ("true", "1", "yes")
    return query, bool(regex_search)
