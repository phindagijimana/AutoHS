"""Resource checks before starting AutoHS jobs."""

from __future__ import annotations

import shutil
import subprocess
import os
from dataclasses import dataclass
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None  # type: ignore


@dataclass
class ResourceStatus:
    ok: bool
    reasons: list[str]


def check_docker() -> tuple[bool, str]:
    if not shutil.which("docker"):
        return False, "docker CLI not found"
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return False, f"docker info failed: {exc}"
    if result.returncode != 0:
        return False, "docker daemon not available"
    return True, "docker ok"


def check_disk(path: Path, min_gb: float = 50.0) -> tuple[bool, str]:
    usage = shutil.disk_usage(path)
    free_gb = usage.free / (1024**3)
    if free_gb < min_gb:
        return False, f"insufficient disk: {free_gb:.1f} GB free (< {min_gb} GB)"
    return True, f"disk ok ({free_gb:.1f} GB free)"


def check_memory(min_gb: float = 8.0) -> tuple[bool, str]:
    if psutil is None:
        return True, "psutil not installed — skipping memory check"
    available_gb = psutil.virtual_memory().available / (1024**3)
    if available_gb < min_gb:
        return False, f"insufficient RAM: {available_gb:.1f} GB available (< {min_gb} GB)"
    return True, f"memory ok ({available_gb:.1f} GB available)"


def check_image(image: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", image],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return False, str(exc)
    if result.returncode != 0:
        return False, f"image not found: {image}"
    return True, f"image ok: {image}"


def assess_resources(
    data_dir: Path,
    running_jobs: int,
    max_running: int = 1,
    freesurfer_image: str = "freesurfer/freesurfer:7.4.1",
    ai_compute_image: str = "autohs/ai-compute:latest",
) -> ResourceStatus:
    reasons: list[str] = []
    ok = True

    if running_jobs >= max_running:
        ok = False
        reasons.append(f"queue full: {running_jobs}/{max_running} running")

    min_disk = float(os.getenv("AUTOHS_MIN_DISK_GB", "10"))
    min_mem = float(os.getenv("AUTOHS_MIN_MEMORY_GB", "8"))
    for check in (
        check_docker(),
        check_disk(data_dir, min_gb=min_disk),
        check_memory(min_gb=min_mem),
        check_image(freesurfer_image),
        check_image(ai_compute_image),
    ):
        passed, message = check
        reasons.append(message)
        if not passed:
            ok = False

    return ResourceStatus(ok=ok, reasons=reasons)
