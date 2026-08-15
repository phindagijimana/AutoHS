"""Extract hippocampal volumes from FreeSurfer outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


def parse_aseg_stats(stats_file: Path) -> dict[str, float]:
    volumes: dict[str, float] = {}
    if not stats_file.exists():
        return volumes

    with stats_file.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "Left-Hippocampus" in line:
                parts = line.split()
                if len(parts) >= 4:
                    volumes["left"] = float(parts[3])
            elif "Right-Hippocampus" in line:
                parts = line.split()
                if len(parts) >= 4:
                    volumes["right"] = float(parts[3])
    return volumes


def find_aseg_stats(freesurfer_dir: Path, subject_id: str) -> Optional[Path]:
    candidates = [
        freesurfer_dir / subject_id / "stats" / "aseg.stats",
        freesurfer_dir / f"freesurfer_docker_{subject_id}" / "stats" / "aseg.stats",
        freesurfer_dir / subject_id / "mri" / "stats" / "aseg.stats",
    ]
    for path in freesurfer_dir.rglob("aseg.stats"):
        candidates.append(path)

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate
    return None


def extract_volumes(freesurfer_dir: Path, subject_id: str) -> tuple[float, float, Path]:
    stats_path = find_aseg_stats(freesurfer_dir, subject_id)
    if not stats_path:
        raise FileNotFoundError(
            f"No aseg.stats found under {freesurfer_dir} for subject {subject_id}"
        )

    volumes = parse_aseg_stats(stats_path)
    left = volumes.get("left")
    right = volumes.get("right")
    if left is None or right is None:
        raise ValueError(f"Missing hippocampal volumes in {stats_path}")

    return left, right, stats_path
