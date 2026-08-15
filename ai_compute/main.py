#!/usr/bin/env python3
"""AI-compute container entrypoint — AutoHS step 2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ai_compute.asymmetry import build_metrics
from ai_compute.extract import extract_volumes
from ai_compute.report import write_json_report, write_pdf_report, write_text_summary
from ai_compute.visualize import generate_overlays_if_possible


def find_aseg_mgz(freesurfer_dir: Path, subject_id: str) -> Path | None:
    candidates = [
        freesurfer_dir / subject_id / "mri" / "aseg.mgz",
        freesurfer_dir / subject_id / "mri" / "aseg.auto.mgz",
    ]
    for path in freesurfer_dir.rglob("aseg.mgz"):
        candidates.append(path)
    for path in freesurfer_dir.rglob("aseg.auto.mgz"):
        candidates.append(path)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def run(job_id: str, input_file: Path, freesurfer_dir: Path, output_dir: Path, subject_id: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    left, right, stats_path = extract_volumes(freesurfer_dir, subject_id)
    metrics = build_metrics(left, right)

    meta = {
        "input_file": str(input_file),
        "aseg_stats": str(stats_path),
        "step": "ai-compute",
        "container": "ai-compute",
    }

    aseg_mgz = find_aseg_mgz(freesurfer_dir, subject_id)
    overlays = generate_overlays_if_possible(input_file, aseg_mgz, output_dir)

    write_json_report(output_dir, job_id, metrics, meta)
    write_text_summary(output_dir, job_id, metrics)
    try:
        write_pdf_report(output_dir, job_id, metrics, meta)
    except ImportError:
        pass

    result = {
        "job_id": job_id,
        "status": "completed",
        "metrics": metrics,
        "outputs": {
            "report_json": str(output_dir / "report.json"),
            "report_pdf": str(output_dir / "report.pdf"),
            "summary_txt": str(output_dir / "summary.txt"),
            "overlay_count": len(overlays),
        },
    }
    (output_dir / "ai_compute_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="NeuroInsight-AutoHS AI-compute (AutoHS pipeline step 2)")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--freesurfer", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--subject-id", default=None)
    args = parser.parse_args()

    subject_id = args.subject_id or f"job_{args.job_id}"

    try:
        result = run(args.job_id, args.input, args.freesurfer, args.output, subject_id)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"job_id": args.job_id, "status": "failed", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
