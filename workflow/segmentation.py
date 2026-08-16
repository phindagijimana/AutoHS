"""Segmentation backends for AutoHS (Docker or Apptainer)."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

FREESURFER_IMAGE = os.getenv("FREESURFER_IMAGE", "freesurfer/freesurfer:7.4.1")
FASTSURFER_IMAGE = os.getenv("FASTSURFER_IMAGE", "deepmi/fastsurfer:latest")
FREESURFER_SIF = os.getenv(
    "FREESURFER_SIF",
    "/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/others/containers/freesurfer_7.4.1.sif",
)
FASTSURFER_SIF = os.getenv(
    "FASTSURFER_SIF",
    "/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/others/containers/fastsurfer_latest.sif",
)


def _run_cmd(cmd: list[str], label: str, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False, env=env)
    if result.returncode != 0:
        tail = (result.stderr or result.stdout or "")[-2000:]
        raise RuntimeError(f"{label} failed (exit {result.returncode}): {tail}")


def detect_runtime(preferred: str | None = None) -> str:
    if preferred in {"docker", "apptainer"}:
        return preferred
    env = os.getenv("AUTOHS_RUNTIME", "").lower()
    if env in {"docker", "apptainer"}:
        return env
    if shutil.which("docker"):
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode == 0:
                return "docker"
        except (subprocess.TimeoutExpired, OSError):
            pass
    if shutil.which("apptainer") or shutil.which("singularity"):
        return "apptainer"
    raise RuntimeError("Neither Docker nor Apptainer/Singularity is available")


def run_freesurfer(
    *,
    input_file: Path,
    work_dir: Path,
    subject_id: str,
    license_path: Path,
    runtime: str | None = None,
    job_id: str = "autohs",
) -> Path:
    freesurfer_dir = work_dir / "freesurfer"
    freesurfer_dir.mkdir(parents=True, exist_ok=True)
    subject_dir = freesurfer_dir / subject_id
    if subject_dir.exists():
        shutil.rmtree(subject_dir)

    runtime = detect_runtime(runtime)
    input_file = input_file.resolve()
    license_path = license_path.resolve()

    if runtime == "docker":
        container_name = f"autohs-freesurfer-{job_id}"
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True, check=False)
        cmd = [
            "docker",
            "run",
            "--rm",
            "--name",
            container_name,
            "--user",
            "root",
            "-v",
            f"{freesurfer_dir.resolve()}:/subjects",
            "-v",
            f"{input_file.parent.resolve()}:/input:ro",
            "-v",
            f"{license_path}:/usr/local/freesurfer/license.txt:ro",
            "-e",
            "FS_LICENSE=/usr/local/freesurfer/license.txt",
            "-e",
            "SUBJECTS_DIR=/subjects",
            FREESURFER_IMAGE,
            "/bin/bash",
            "-c",
            (
                f"source /usr/local/freesurfer/FreeSurferEnv.sh && "
                f"recon-all -i /input/{input_file.name} -s {subject_id} "
                f"-autorecon1 -autorecon2-volonly && "
                f"mri_segstats --seg /subjects/{subject_id}/mri/aseg.auto.mgz "
                f"--excludeid 0 --sum /subjects/{subject_id}/stats/aseg.stats "
                f"--i /subjects/{subject_id}/mri/brain.mgz"
            ),
        ]
        _run_cmd(cmd, "FreeSurfer (Docker)")
    else:
        sif = Path(FREESURFER_SIF)
        if not sif.exists():
            raise FileNotFoundError(f"FreeSurfer SIF not found: {sif}")
        apptainer = "apptainer" if shutil.which("apptainer") else "singularity"
        cmd = [
            apptainer,
            "exec",
            "--bind",
            f"{freesurfer_dir.resolve()}:/subjects",
            "--bind",
            f"{input_file.parent.resolve()}:/input:ro",
            "--bind",
            f"{license_path}:/usr/local/freesurfer/license.txt:ro",
            "--env",
            "FS_LICENSE=/usr/local/freesurfer/license.txt",
            "--env",
            "SUBJECTS_DIR=/subjects",
            str(sif),
            "/bin/bash",
            "-c",
            (
                f"export FS_FREESURFERENV_NO_OUTPUT=1; "
                f"source /usr/local/freesurfer/FreeSurferEnv.sh; "
                f"recon-all -i /input/{input_file.name} -s {subject_id} "
                f"-autorecon1 -autorecon2-volonly; "
                f"mri_segstats --seg /subjects/{subject_id}/mri/aseg.auto.mgz "
                f"--excludeid 0 --sum /subjects/{subject_id}/stats/aseg.stats "
                f"--i /subjects/{subject_id}/mri/brain.mgz"
            ),
        ]
        _run_cmd(cmd, "FreeSurfer (Apptainer)")

    stats_file = subject_dir / "stats" / "aseg.stats"
    if not stats_file.exists():
        raise FileNotFoundError(f"FreeSurfer finished but missing {stats_file}")
    return freesurfer_dir


def run_fastsurfer(
    *,
    input_file: Path,
    work_dir: Path,
    subject_id: str,
    runtime: str | None = None,
    job_id: str = "autohs",
    n_threads: int | None = None,
) -> Path:
    freesurfer_dir = work_dir / "freesurfer"
    freesurfer_dir.mkdir(parents=True, exist_ok=True)
    subject_dir = freesurfer_dir / subject_id
    if subject_dir.exists():
        shutil.rmtree(subject_dir)

    runtime = detect_runtime(runtime)
    input_file = input_file.resolve()
    cpu_count = os.cpu_count() or 4
    num_threads = n_threads or max(1, int(os.getenv("AUTOHS_THREADS", max(1, cpu_count - 2))))

    if runtime == "docker":
        container_name = f"autohs-fastsurfer-{job_id}"
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True, check=False)
        cmd = [
            "docker",
            "run",
            "--rm",
            "--name",
            container_name,
            "-v",
            f"{input_file.parent.resolve()}:/input:ro",
            "-v",
            f"{freesurfer_dir.resolve()}:/output",
            FASTSURFER_IMAGE,
            "--t1",
            f"/input/{input_file.name}",
            "--sid",
            subject_id,
            "--sd",
            "/output",
            "--seg_only",
            "--device",
            "cpu",
            "--batch",
            "1",
            "--threads",
            str(num_threads),
            "--viewagg_device",
            "cpu",
        ]
        _run_cmd(cmd, "FastSurfer (Docker)")
    else:
        sif = Path(FASTSURFER_SIF)
        if not sif.exists():
            raise FileNotFoundError(f"FastSurfer SIF not found: {sif}")
        apptainer = "apptainer" if shutil.which("apptainer") else "singularity"
        cmd = [
            apptainer,
            "exec",
            "--bind",
            f"{input_file.parent.resolve()}:/input:ro",
            "--bind",
            f"{freesurfer_dir.resolve()}:/output",
            "--env",
            "TQDM_DISABLE=1",
            "--cleanenv",
            str(sif),
            "/fastsurfer/run_fastsurfer.sh",
            "--t1",
            f"/input/{input_file.name}",
            "--sid",
            subject_id,
            "--sd",
            "/output",
            "--seg_only",
            "--device",
            "cpu",
            "--batch",
            "1",
            "--threads",
            str(num_threads),
            "--viewagg_device",
            "cpu",
        ]
        _run_cmd(cmd, "FastSurfer (Apptainer)")

    from ai_compute.extract import find_aseg_stats

    if not find_aseg_stats(freesurfer_dir, subject_id):
        raise FileNotFoundError(
            f"FastSurfer finished but missing hippocampal stats under {subject_dir}"
        )
    return freesurfer_dir


def run_ai_compute(
    *,
    repo_root: Path,
    job_id: str,
    input_file: Path,
    freesurfer_dir: Path,
    output_dir: Path,
    subject_id: str,
    runtime: str | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    runtime = detect_runtime(runtime)

    if runtime == "docker":
        ai_image = os.getenv("AI_COMPUTE_IMAGE", "autohs/ai-compute:latest")
        container_name = f"autohs-ai-compute-{job_id}"
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True, check=False)
        cmd = [
            "docker",
            "run",
            "--rm",
            "--name",
            container_name,
            "-v",
            f"{input_file.parent.resolve()}:/data/input:ro",
            "-v",
            f"{freesurfer_dir.resolve()}:/data/freesurfer:ro",
            "-v",
            f"{output_dir.resolve()}:/data/output",
            ai_image,
            "--job-id",
            job_id,
            "--input",
            f"/data/input/{input_file.name}",
            "--freesurfer",
            "/data/freesurfer",
            "--output",
            "/data/output",
            "--subject-id",
            subject_id,
        ]
        _run_cmd(cmd, "AI-compute (Docker)")
    else:
        if str(repo_root.resolve()) not in sys.path:
            sys.path.insert(0, str(repo_root.resolve()))
        from ai_compute.main import run as run_ai_compute_step

        run_ai_compute_step(
            job_id,
            input_file.resolve(),
            freesurfer_dir.resolve(),
            output_dir.resolve(),
            subject_id,
        )

    result_file = output_dir / "ai_compute_result.json"
    if not result_file.exists():
        raise FileNotFoundError("AI-compute finished but ai_compute_result.json missing")
    return output_dir
