"""Shared helpers for workflow integration tests."""

from __future__ import annotations

from pathlib import Path

ASEG_STATS = (
    "# AutoHS test fixture\n"
    "1  17  100  3500.0  Left-Hippocampus\n"
    "2  53  90  3200.0  Right-Hippocampus\n"
)


def install_fake_segmentation(
    work_dir: Path,
    *,
    subject_id: str,
    pipeline: str = "fastsurfer",
) -> Path:
    """Create minimal FreeSurfer/FastSurfer-like stats for AI-compute."""
    seg_dir = work_dir / "freesurfer"
    stats_dir = seg_dir / subject_id / "stats"
    stats_dir.mkdir(parents=True, exist_ok=True)
    stats_name = "aseg+DKT.stats" if pipeline == "fastsurfer" else "aseg.stats"
    (stats_dir / stats_name).write_text(ASEG_STATS, encoding="utf-8")
    return seg_dir


def fake_fastsurfer(**kwargs) -> Path:
    work_dir = kwargs["work_dir"]
    subject_id = kwargs["subject_id"]
    return install_fake_segmentation(work_dir, subject_id=subject_id, pipeline="fastsurfer")


def fake_freesurfer(**kwargs) -> Path:
    work_dir = kwargs["work_dir"]
    subject_id = kwargs["subject_id"]
    return install_fake_segmentation(work_dir, subject_id=subject_id, pipeline="freesurfer")
