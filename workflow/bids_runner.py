"""BIDS App driver for AutoHS."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from workflow.bids_filters import t1w_query_filters
from workflow.bids_types import T1wScan
from workflow.segmentation import run_ai_compute, run_fastsurfer, run_freesurfer

try:
    from bids import BIDSLayout
except ImportError:
    BIDSLayout = None  # type: ignore


def _repo_version() -> str:
    return (Path(__file__).resolve().parents[1] / "version").read_text(encoding="utf-8").strip()


def scan_job_id(scan: T1wScan) -> str:
    if scan.session_label:
        return f"{scan.subject_label}_{scan.session_label}"
    return scan.subject_label


def scan_work_subject_id(scan: T1wScan) -> str:
    subject_id = f"sub-{scan.subject_label}"
    if scan.session_label:
        subject_id = f"{subject_id}_ses-{scan.session_label}"
    return subject_id


def segmentation_subject_id(job_id: str) -> str:
    return f"job_{job_id.replace('-', '')}"


def resolve_existing_work(scan_work: Path, job_id: str) -> tuple[Path, Path, str]:
    """Locate input T1w and existing segmentation for --reports-only."""
    input_dir = scan_work / "input"
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Missing work input directory: {input_dir}")

    input_files = sorted(input_dir.glob("*.nii*"))
    if not input_files:
        raise FileNotFoundError(f"No T1w input found under {input_dir}")

    seg_dir = scan_work / "freesurfer"
    if not seg_dir.is_dir():
        raise FileNotFoundError(
            f"Missing segmentation output for reports-only mode: {seg_dir}"
        )

    seg_subject_id = segmentation_subject_id(job_id)
    if not (seg_dir / seg_subject_id).is_dir():
        candidates = [path for path in seg_dir.iterdir() if path.is_dir()]
        if len(candidates) == 1:
            seg_subject_id = candidates[0].name
        else:
            raise FileNotFoundError(
                f"Could not locate segmentation subject directory under {seg_dir}"
            )

    return input_files[0], seg_dir, seg_subject_id


def discover_t1w_scans(
    bids_dir: Path,
    participant_labels: Optional[list[str]] = None,
    session_labels: Optional[list[str]] = None,
    bids_filter_file: Optional[Path] = None,
) -> list[T1wScan]:
    bids_dir = bids_dir.resolve()
    scans: list[T1wScan] = []
    t1w_filters, regex_search = t1w_query_filters(
        bids_filter_file.resolve() if bids_filter_file else None
    )

    if BIDSLayout is not None:
        layout = BIDSLayout(str(bids_dir), validate=False)
        subjects = participant_labels or layout.get_subjects()
        for subject in subjects:
            sessions = session_labels or layout.get_sessions(subject=subject) or [None]
            for session in sessions:
                query = dict(t1w_filters)
                if "session" in query:
                    filter_session = query["session"]
                    if session is not None and filter_session != session:
                        continue
                else:
                    query["session"] = session
                files = layout.get(
                    subject=subject,
                    suffix="T1w",
                    extension=[".nii", ".nii.gz"],
                    return_type="file",
                    regex_search=regex_search,
                    **query,
                )
                for path in files:
                    resolved_session = session
                    if resolved_session is None and "session" in query:
                        resolved_session = query["session"]
                    scans.append(
                        T1wScan(
                            subject_label=subject,
                            session_label=resolved_session,
                            t1w_path=Path(path),
                        )
                    )
        if scans or bids_filter_file is not None:
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
                "Version": _repo_version(),
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
    from workflow.derivatives import derivative_paths

    return derivative_paths(output_root, scan).subject_dir


def publish_derivatives(
    work_output: Path,
    output_root: Path,
    *,
    scan: T1wScan,
    bids_dir: Path,
    pipeline: str = "freesurfer",
    version: Optional[str] = None,
) -> Path:
    from workflow.derivatives import derivative_paths, publish_bids_derivatives

    if version is None:
        version = _repo_version()
    paths = derivative_paths(output_root, scan)
    publish_bids_derivatives(
        work_output,
        paths,
        scan=scan,
        bids_dir=bids_dir,
        pipeline=pipeline,
        version=version,
    )
    return paths.subject_dir


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
        bids_filter_file: Optional[Path] = None,
        fastsurfer: bool = False,
        fs_license_file: Optional[Path] = None,
        runtime: Optional[str] = None,
        n_threads: Optional[int] = None,
        reports_only: bool = False,
    ) -> list[Path]:
        bids_dir = bids_dir.resolve()
        output_root = output_dir / "autohs"
        work_dir = work_dir.resolve()
        work_dir.mkdir(parents=True, exist_ok=True)
        write_derivatives_description(output_root)

        scans = discover_t1w_scans(
            bids_dir,
            participant_labels,
            session_labels,
            bids_filter_file=bids_filter_file,
        )
        if not scans:
            raise FileNotFoundError(f"No T1w scans found under {bids_dir}")

        if reports_only and fastsurfer:
            raise ValueError("--reports-only cannot be combined with --fastsurfer.")

        license_path = None
        if not reports_only and not fastsurfer:
            license_path = self._find_license(fs_license_file)

        pipeline = "reports-only"
        if not reports_only:
            pipeline = "fastsurfer" if fastsurfer else "freesurfer"

        published: list[Path] = []

        for scan in scans:
            job_id = scan_job_id(scan)
            subject_id = scan_work_subject_id(scan)

            scan_work = work_dir / subject_id
            scan_work.mkdir(parents=True, exist_ok=True)

            if reports_only:
                input_copy, seg_dir, seg_subject_id = resolve_existing_work(scan_work, job_id)
            else:
                input_copy = scan_work / "input" / scan.t1w_path.name
                input_copy.parent.mkdir(parents=True, exist_ok=True)
                if not input_copy.exists():
                    shutil.copy2(scan.t1w_path, input_copy)

                seg_subject_id = segmentation_subject_id(job_id)
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

            derivative_dir = publish_derivatives(
                work_output,
                output_root,
                scan=scan,
                bids_dir=bids_dir,
                pipeline=pipeline,
            )
            published.append(derivative_dir)

        log = {
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "pipeline": pipeline,
            "reports_only": reports_only,
            "scans_processed": len(published),
            "derivative_root": str(output_root),
        }
        (output_root / "autohs_run.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
        return published
