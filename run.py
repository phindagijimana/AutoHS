#!/usr/bin/env python3
"""AutoHS BIDS App entrypoint."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

__version__ = (ROOT / "version").read_text(encoding="utf-8").strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="autohs",
        description=(
            "AutoHS: Automated Hippocampal Sclerosis workflow for T1-weighted MRI. "
            "A BIDS App that performs hippocampal segmentation, asymmetry indexing, "
            "and clinical reporting."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "bids_dir",
        help="The root folder of a BIDS-valid dataset (sub-* folders at top level).",
    )
    parser.add_argument(
        "output_dir",
        help="Path where AutoHS derivatives and reports will be stored.",
    )
    parser.add_argument(
        "analysis_level",
        choices=["participant"],
        help='Processing stage to run. AutoHS currently supports only "participant".',
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"AutoHS {__version__}",
    )

    bids = parser.add_argument_group("Options for filtering BIDS queries")
    bids.add_argument(
        "--participant-label",
        "--participant_label",
        dest="participant_label",
        nargs="+",
        help="Participant label(s) without the sub- prefix (e.g. 01 02).",
    )
    bids.add_argument(
        "--session-label",
        "--session_label",
        dest="session_label",
        nargs="+",
        help="Session label(s) without the ses- prefix.",
    )
    bids.add_argument(
        "--skip-bids-validator",
        "--skip_bids_validator",
        dest="skip_bids_validator",
        action="store_true",
        help="Do not run bids-validator before processing.",
    )
    bids.add_argument(
        "--bids-filter-file",
        dest="bids_filter_file",
        help="PyBIDS filter file (JSON) to restrict T1w selection.",
    )

    perf = parser.add_argument_group("Options to handle performance")
    perf.add_argument(
        "-w",
        "--work-dir",
        dest="work_dir",
        help="Working directory for intermediate files. Defaults to <output_dir>/work.",
    )
    perf.add_argument(
        "--nthreads",
        "--n-threads",
        dest="n_threads",
        type=int,
        help="Number of CPU threads for segmentation.",
    )
    perf.add_argument(
        "--runtime",
        choices=["docker", "apptainer", "auto"],
        default="auto",
        help="Container runtime for segmentation (auto detects Docker or Apptainer).",
    )

    workflow = parser.add_argument_group("Workflow configuration")
    workflow.add_argument(
        "--fastsurfer",
        action="store_true",
        help="Use FastSurfer instead of FreeSurfer for step 1 (faster, CPU-friendly).",
    )
    workflow.add_argument(
        "--fs-license-file",
        dest="fs_license_file",
        help="Path to FreeSurfer license.txt (required unless --fastsurfer is set).",
    )
    workflow.add_argument(
        "--reports-only",
        action="store_true",
        help="Re-run AI-compute and reports from existing segmentation in the work directory.",
    )
    return parser


def maybe_validate_bids(bids_dir: Path, skip: bool) -> None:
    if skip or not shutil_which("bids-validator"):
        return
    result = subprocess.run(
        ["bids-validator", str(bids_dir)],
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def shutil_which(name: str) -> str | None:
    import shutil

    return shutil.which(name)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.reports_only and args.fastsurfer:
        parser.error("--reports-only cannot be combined with --fastsurfer.")

    bids_dir = Path(args.bids_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    work_dir = Path(args.work_dir).resolve() if args.work_dir else output_dir / "work"
    runtime = None if args.runtime == "auto" else args.runtime

    if not bids_dir.exists():
        parser.error(f"BIDS directory not found: {bids_dir}")

    maybe_validate_bids(bids_dir, args.skip_bids_validator)

    from workflow.bids_runner import BidsRunner

    runner = BidsRunner(ROOT)
    published = runner.run_participant(
        bids_dir=bids_dir,
        output_dir=output_dir,
        work_dir=work_dir,
        participant_labels=args.participant_label,
        session_labels=args.session_label,
        bids_filter_file=Path(args.bids_filter_file) if args.bids_filter_file else None,
        fastsurfer=args.fastsurfer,
        fs_license_file=Path(args.fs_license_file) if args.fs_license_file else None,
        runtime=runtime,
        n_threads=args.n_threads,
        reports_only=args.reports_only,
    )

    print(f"AutoHS completed {len(published)} scan(s).")
    print(f"Derivatives: {output_dir / 'autohs'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
