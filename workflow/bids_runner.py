"""BIDS App driver for AutoHS."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from workflow.segmentation import run_ai_compute, run_fastsurfer, run_freesurfer

try:
    from bids import BIDSLayout
except ImportError:
    BIDSLayout = None  # type: ignore


@dataclass
class T1wScan:
    subject_label: str
    session_label: Optional[str]
    t1w_path: Path


def discover_t1w_scans(
    bids_dir: Path,
    participant_labels: Optional[list[str]] = None,
    session_labels: Optional[list[str]] = None,
) -> list[T1wScan]:
    bids_dir = bids_dir.resolve()
    scans: list[T1wScan] = []

    if BIDSLayout is not None:
        layout = BIDSLayout(str(bids_dir), validate=False)
        subjects = participant_labels or layout.get_subjects()
        for subject in subjects:
            sessions = session_labels or layout.get_sessions(subject=subject) or [None]
            for session in sessions:
                files = layout.get(
                    subject=subject,
                    session=session,
                    suffix="T1w",
                    extension=[".nii", ".nii.gz"],
                    return_type="file",
                )
                for path in files:
                    scans.append(
                        T1wScan(
                            subject_label=subject,
                            session_label=session,
                            t1w_path=Path(path),
                        )
                    )
        if scans:
            return scans

    for subject_dir in sorted(bids_dir.glob("sub-*")):
        subject = subject_dir.name.replace("sub-", "", 1)
        if participant_labels and subject not in participant_labels:
            continue
        session_dirs = sorted(subject_dir.glob("ses-*")) or [subject_dir]
        for session_dir in session_dirs:
            session = None
            search_root = session_dir
            if session_dir.name.startswith("ses-"):
                session = session_dir.name.replace("ses-", "", 1)
                if session_labels and session not in session_labels:
                    continue
            anat_dir = search_root / "anat"
            if not anat_dir.exists():
                continue
            for t1w in sorted(anat_dir.glob("*_T1w.nii*")):
                scans.append(
                    T1wScan(
                        subject_label=subject,
                        session_label=session,
                        t1w_path=t1w.resolve(),
                    )
                )
    return scans


def write_derivatives_description(output_root: Path, pipeline_name: str = "autohs") -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    description = {
        "Name": "AutoHS",
        "BIDSVersion": "1.9.0",
        "DatasetType": "derivative",
        "GeneratedBy": [
            {
                "Name": pipeline_name,
                "Version": open(Path(__file__).resolve().parents[1] / "version").read().strip(),
                "Description": (
                    "Automated hippocampal sclerosis workflow: segmentation, "
                    "hippocampal volumes, asymmetry index, and clinical report."
                ),
            }
        ],
        "HowToAcknowledge": (
            "Ndagijimana P, Brennan D, Shinohara R, Gugger J. MRI derived hippocampal "
            "asymmetry identifies hippocampal sclerosis in epilepsy surgical specimens. "
            "Brain Communications. Accepted (in press)."
        ),
    }
    (output_root / "dataset_description.json").write_text(
        json.dumps(description, indent=2),
        encoding="utf-8",
    )


def derivative_subject_dir(
    output_root: Path,
    scan: T1wScan,
) -> Path:
    subject = f"sub-{scan.subject_label}"
    if scan.session_label:
        return output_root / subject / f"ses-{scan.session_label}"
    return output_root / subject


def publish_derivatives(work_output: Path, derivative_dir: Path) -> None:
    derivative_dir.mkdir(parents=True, exist_ok=True)
    for name in ("report.json", "report.pdf", "summary.txt", "ai_compute_result.json"):
        src = work_output / name
        if src.exists():
            shutil.copy2(src, derivative_dir / name)
    viz_src = work_output / "visualizations"
    if viz_src.exists():
        viz_dst = derivative_dir / "visualizations"
        if viz_dst.exists():
            shutil.rmtree(viz_dst)
        shutil.copytree(viz_src, viz_dst)


class BidsRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def _find_license(self, fs_license_file: Optional[Path]) -> Path:
        candidates = [
            fs_license_file,
            self.repo_root / "license.txt",
            Path.home() / ".freesurfer" / "license.txt",
        ]
        for candidate in candidates:
            if candidate and Path(candidate).exists():
                return Path(candidate).resolve()
        raise FileNotFoundError(
            "FreeSurfer license not found. Pass --fs-license-file or set FREESURFER_LICENSE."
        )

    def run_participant(
        self,
        *,
        bids_dir: Path,
        output_dir: Path,
        work_dir: Path,
        participant_labels: Optional[list[str]] = None,
        session_labels: Optional[list[str]] = None,
        fastsurfer: bool = False,
        fs_license_file: Optional[Path] = None,
        runtime: Optional[str] = None,
        n_threads: Optional[int] = None,
    ) -> list[Path]:
        bids_dir = bids_dir.resolve()
        output_root = output_dir / "autohs"
        work_dir = work_dir.resolve()
        work_dir.mkdir(parents=True, exist_ok=True)
        write_derivatives_description(output_root)

        scans = discover_t1w_scans(bids_dir, participant_labels, session_labels)
        if not scans:
            raise FileNotFoundError(f"No T1w scans found under {bids_dir}")

        license_path = None if fastsurfer else self._find_license(fs_license_file)
        published: list[Path] = []

        for scan in scans:
            job_id = scan.subject_label
            if scan.session_label:
                job_id = f"{scan.subject_label}_{scan.session_label}"
            subject_id = f"sub-{scan.subject_label}"
            if scan.session_label:
                subject_id = f"{subject_id}_ses-{scan.session_label}"

            scan_work = work_dir / subject_id
            scan_work.mkdir(parents=True, exist_ok=True)
            input_copy = scan_work / "input" / scan.t1w_path.name
            input_copy.parent.mkdir(parents=True, exist_ok=True)
            if not input_copy.exists():
                shutil.copy2(scan.t1w_path, input_copy)

            seg_subject_id = f"job_{job_id.replace('-', '')}"
            if fastsurfer:
                seg_dir = run_fastsurfer(
                    input_file=input_copy,
                    work_dir=scan_work,
                    subject_id=seg_subject_id,
                    runtime=runtime,
                    job_id=job_id,
                    n_threads=n_threads,
                )
            else:
                seg_dir = run_freesurfer(
                    input_file=input_copy,
                    work_dir=scan_work,
                    subject_id=seg_subject_id,
                    license_path=license_path,  # type: ignore[arg-type]
                    runtime=runtime,
                    job_id=job_id,
                )

            work_output = run_ai_compute(
                repo_root=self.repo_root,
                job_id=job_id,
                input_file=input_copy,
                freesurfer_dir=seg_dir,
                output_dir=scan_work / "output",
                subject_id=seg_subject_id,
                runtime=runtime,
            )

            derivative_dir = derivative_subject_dir(output_root, scan)
            publish_derivatives(work_output, derivative_dir)
            published.append(derivative_dir)

        log = {
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "pipeline": "fastsurfer" if fastsurfer else "freesurfer",
            "scans_processed": len(published),
            "derivative_root": str(output_root),
        }
        (output_root / "autohs_run.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
        return published
