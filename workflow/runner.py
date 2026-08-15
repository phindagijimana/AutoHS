"""Execute the runnable two-step AutoHS workflow."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from workflow.queue import JobQueue
from workflow.resources import assess_resources

logger = logging.getLogger(__name__)

FREESURFER_IMAGE = os.getenv("FREESURFER_IMAGE", "freesurfer/freesurfer:7.4.1")
FASTSURFER_IMAGE = os.getenv("FASTSURFER_IMAGE", "deepmi/fastsurfer:latest")
AI_COMPUTE_IMAGE = os.getenv("AI_COMPUTE_IMAGE", "autohs/ai-compute:latest")
MAX_RUNNING = int(os.getenv("AUTOHS_MAX_RUNNING", "1"))


class WorkflowRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.data_dir = repo_root / "data"
        self.jobs_dir = self.data_dir / "jobs"
        self.queue = JobQueue(self.data_dir / "autohs.db")

    def submit(self, input_path: Path, *, fastsurfer: bool = False) -> str:
        input_path = input_path.resolve()
        if not input_path.exists():
            raise FileNotFoundError(input_path)
        name = input_path.name.lower()
        if not (name.endswith(".nii") or name.endswith(".nii.gz")):
            raise ValueError("Input must be .nii or .nii.gz")

        segmentation = "fastsurfer" if fastsurfer else "freesurfer"
        job = self.queue.create_job(
            input_path,
            self.jobs_dir / "pending",
            segmentation=segmentation,
        )
        work_dir = self.jobs_dir / job.id
        work_dir.mkdir(parents=True, exist_ok=True)
        input_dir = work_dir / "input"
        input_dir.mkdir(exist_ok=True)
        dest = input_dir / input_path.name
        shutil.copy2(input_path, dest)
        self.queue.update_job(job.id, work_dir=str(work_dir), input_path=str(dest))
        logger.info("Submitted job %s", job.id)
        return job.id

    def run_pending_if_resources_available(self) -> Optional[str]:
        if self.queue.count_by_status("running") >= MAX_RUNNING:
            return None

        pending = self.queue.oldest_pending()
        if not pending:
            return None

        status = assess_resources(
            self.data_dir,
            running_jobs=self.queue.count_by_status("running"),
            max_running=MAX_RUNNING,
            freesurfer_image=FREESURFER_IMAGE,
            fastsurfer_image=FASTSURFER_IMAGE,
            ai_compute_image=AI_COMPUTE_IMAGE,
            segmentation=pending.segmentation,
        )
        if not status.ok:
            logger.info("Resources not ready: %s", "; ".join(status.reasons))
            return None

        self.run_job(pending.id)
        return pending.id

    def run_job(self, job_id: str) -> None:
        job = self.queue.get_job(job_id)
        work_dir = Path(job.work_dir or self.jobs_dir / job_id)
        input_file = Path(job.input_path)
        subject_id = f"job_{job_id}"
        use_fastsurfer = job.segmentation == "fastsurfer"
        step_name = "fastsurfer-processing" if use_fastsurfer else "freesurfer-processing"

        self.queue.update_job(
            job_id,
            status="running",
            step=step_name,
            progress=5,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        try:
            seg_dir = (
                self._run_fastsurfer(job_id, input_file, work_dir, subject_id)
                if use_fastsurfer
                else self._run_freesurfer(job_id, input_file, work_dir, subject_id)
            )
            self.queue.update_job(job_id, step="ai-compute", progress=60)
            result_dir = self._run_ai_compute(job_id, input_file, seg_dir, work_dir, subject_id)
            self.queue.update_job(
                job_id,
                status="completed",
                step="done",
                progress=100,
                result_path=str(result_dir),
                completed_at=datetime.now(timezone.utc).isoformat(),
            )
        except Exception as exc:
            logger.exception("Job %s failed", job_id)
            self.queue.update_job(
                job_id,
                status="failed",
                error_message=str(exc),
                step="failed",
                completed_at=datetime.now(timezone.utc).isoformat(),
            )
            raise

    def _run_freesurfer(
        self, job_id: str, input_file: Path, work_dir: Path, subject_id: str
    ) -> Path:
        freesurfer_dir = work_dir / "freesurfer"
        freesurfer_dir.mkdir(parents=True, exist_ok=True)
        subject_dir = freesurfer_dir / subject_id
        if subject_dir.exists():
            shutil.rmtree(subject_dir)

        license_path = self._find_license()
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

        logger.info("Starting FreeSurfer container for job %s", job_id)
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            tail = (result.stderr or result.stdout or "")[-2000:]
            raise RuntimeError(f"FreeSurfer step failed (exit {result.returncode}): {tail}")

        stats_file = subject_dir / "stats" / "aseg.stats"
        if not stats_file.exists():
            raise FileNotFoundError(f"FreeSurfer finished but missing {stats_file}")

        return freesurfer_dir

    def _run_fastsurfer(
        self, job_id: str, input_file: Path, work_dir: Path, subject_id: str
    ) -> Path:
        freesurfer_dir = work_dir / "freesurfer"
        freesurfer_dir.mkdir(parents=True, exist_ok=True)
        subject_dir = freesurfer_dir / subject_id
        if subject_dir.exists():
            shutil.rmtree(subject_dir)

        import os as _os

        cpu_count = _os.cpu_count() or 4
        num_threads = max(1, cpu_count - 2)
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

        logger.info("Starting FastSurfer container for job %s", job_id)
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            tail = (result.stderr or result.stdout or "")[-2000:]
            raise RuntimeError(f"FastSurfer step failed (exit {result.returncode}): {tail}")

        stats_file = self._find_segmentation_stats(subject_dir)
        if not stats_file:
            raise FileNotFoundError(
                f"FastSurfer finished but missing hippocampal stats under {subject_dir}"
            )

        return freesurfer_dir

    @staticmethod
    def _find_segmentation_stats(subject_dir: Path) -> Path | None:
        from ai_compute.extract import find_aseg_stats

        return find_aseg_stats(subject_dir.parent, subject_dir.name)

    def _run_ai_compute(
        self,
        job_id: str,
        input_file: Path,
        freesurfer_dir: Path,
        work_dir: Path,
        subject_id: str,
    ) -> Path:
        output_dir = work_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
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
            AI_COMPUTE_IMAGE,
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

        logger.info("Starting AI-compute container for job %s", job_id)
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            tail = (result.stderr or result.stdout or "")[-2000:]
            raise RuntimeError(f"AI-compute step failed (exit {result.returncode}): {tail}")

        result_file = output_dir / "ai_compute_result.json"
        if not result_file.exists():
            raise FileNotFoundError("AI-compute finished but ai_compute_result.json missing")

        return output_dir

    def _find_license(self) -> Path:
        candidates = [
            self.repo_root / "license.txt",
            Path(os.getenv("FREESURFER_LICENSE", "")),
            Path.home() / "license.txt",
        ]
        for candidate in candidates:
            if candidate and candidate.exists():
                return candidate.resolve()
        raise FileNotFoundError(
            "FreeSurfer license.txt not found. Place license.txt in repo root or set FREESURFER_LICENSE."
        )
