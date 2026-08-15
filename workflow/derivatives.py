"""BIDS Derivatives layout and sidecar metadata for AutoHS outputs."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from workflow.bids_types import T1wScan


@dataclass(frozen=True)
class DerivativePaths:
    subject_dir: Path
    metrics_json: Path
    report_pdf: Path
    summary_txt: Path
    figures_dir: Path


def derivative_basename(scan: T1wScan) -> str:
    base = f"sub-{scan.subject_label}"
    if scan.session_label:
        base = f"{base}_ses-{scan.session_label}"
    return base


def derivative_paths(output_root: Path, scan: T1wScan) -> DerivativePaths:
    base = derivative_basename(scan)
    if scan.session_label:
        subject_dir = output_root / f"sub-{scan.subject_label}" / f"ses-{scan.session_label}"
    else:
        subject_dir = output_root / f"sub-{scan.subject_label}"

    return DerivativePaths(
        subject_dir=subject_dir,
        metrics_json=subject_dir / f"{base}_desc-autohs_metrics.json",
        report_pdf=subject_dir / "figures" / f"{base}_desc-autohs_report.pdf",
        summary_txt=subject_dir / f"{base}_desc-autohs_summary.txt",
        figures_dir=subject_dir / "figures",
    )


def bids_uri(bids_dir: Path, t1w_path: Path) -> str:
    rel = t1w_path.resolve().relative_to(bids_dir.resolve()).as_posix()
    return f"bids::{rel}"


def enrich_metrics_payload(
    payload: dict[str, Any],
    *,
    scan: T1wScan,
    bids_dir: Path,
    pipeline: str,
    version: str,
) -> dict[str, Any]:
    source_uri = bids_uri(bids_dir, scan.t1w_path)
    enriched = dict(payload)
    enriched["Sources"] = [{"URL": source_uri}]
    enriched["SpatialReference"] = {"URL": source_uri}
    enriched["GeneratedBy"] = [
        {
            "Name": "AutoHS",
            "Version": version,
            "Description": f"AutoHS hippocampal asymmetry workflow ({pipeline})",
        }
    ]
    enriched["BIDS"] = {
        "Subject": scan.subject_label,
        "Session": scan.session_label,
        "T1w": scan.t1w_path.name,
    }
    return enriched


def publish_bids_derivatives(
    work_output: Path,
    paths: DerivativePaths,
    *,
    scan: T1wScan,
    bids_dir: Path,
    pipeline: str,
    version: str,
) -> None:
    paths.subject_dir.mkdir(parents=True, exist_ok=True)
    paths.figures_dir.mkdir(parents=True, exist_ok=True)

    report_json = work_output / "report.json"
    if report_json.exists():
        payload = json.loads(report_json.read_text(encoding="utf-8"))
        enriched = enrich_metrics_payload(
            payload,
            scan=scan,
            bids_dir=bids_dir,
            pipeline=pipeline,
            version=version,
        )
        paths.metrics_json.write_text(json.dumps(enriched, indent=2), encoding="utf-8")
        # Backward-compatible alias for legacy consumers
        shutil.copy2(paths.metrics_json, paths.subject_dir / "report.json")

    pdf_src = work_output / "report.pdf"
    if pdf_src.exists():
        shutil.copy2(pdf_src, paths.report_pdf)

    summary_src = work_output / "summary.txt"
    if summary_src.exists():
        shutil.copy2(summary_src, paths.summary_txt)

    viz_src = work_output / "visualizations" / "coronal"
    if viz_src.exists():
        base = derivative_basename(scan)
        for idx, png in enumerate(sorted(viz_src.glob("*.png"))):
            dest = paths.figures_dir / f"{base}_desc-autohs_hippocampus-coronal{idx:02d}.png"
            shutil.copy2(png, dest)

    result_src = work_output / "ai_compute_result.json"
    if result_src.exists():
        sidecar = paths.subject_dir / f"{derivative_basename(scan)}_desc-autohs_provenance.json"
        payload = json.loads(result_src.read_text(encoding="utf-8"))
        payload["Sources"] = [{"URL": bids_uri(bids_dir, scan.t1w_path)}]
        payload["GeneratedBy"] = [
            {"Name": "AutoHS", "Version": version, "Description": "AI-compute step"}
        ]
        sidecar.write_text(json.dumps(payload, indent=2), encoding="utf-8")
