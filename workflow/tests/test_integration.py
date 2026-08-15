"""End-to-end BIDS App integration tests (mocked segmentation)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from workflow.bids_runner import BidsRunner, discover_t1w_scans
from workflow.derivatives import derivative_paths
from workflow.tests.helpers import fake_fastsurfer, fake_freesurfer, install_fake_segmentation

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MINIMAL_BIDS = FIXTURES / "minimal_bids"
REPO_ROOT = Path(__file__).resolve().parents[2]


class BidsAppIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        if not (MINIMAL_BIDS / "sub-001" / "ses-1" / "anat" / "sub-001_ses-1_T1w.nii.gz").exists():
            self.skipTest("minimal BIDS fixture missing")

    @patch("workflow.bids_runner.run_fastsurfer", side_effect=fake_fastsurfer)
    def test_fastsurfer_pipeline_end_to_end(self, _mock_fastsurfer) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output_dir = root / "out"
            work_dir = root / "work"

            runner = BidsRunner(REPO_ROOT)
            published = runner.run_participant(
                bids_dir=MINIMAL_BIDS,
                output_dir=output_dir,
                work_dir=work_dir,
                participant_labels=["001"],
                fastsurfer=True,
                runtime="apptainer",
            )

            self.assertEqual(len(published), 1)
            derivative_root = output_dir / "autohs"
            scan_paths = derivative_paths(derivative_root, discover_t1w_scans(MINIMAL_BIDS)[0])

            self.assertTrue(scan_paths.metrics_json.exists())
            metrics = json.loads(scan_paths.metrics_json.read_text(encoding="utf-8"))
            self.assertIn("Sources", metrics)
            self.assertAlmostEqual(metrics["metrics"]["asymmetry_index"], round(300 / 6700, 4))
            self.assertTrue(scan_paths.summary_txt.exists())
            self.assertTrue((derivative_root / "dataset_description.json").exists())
            self.assertTrue((derivative_root / "autohs_run.json").exists())

            run_log = json.loads((derivative_root / "autohs_run.json").read_text(encoding="utf-8"))
            self.assertEqual(run_log["pipeline"], "fastsurfer")
            self.assertFalse(run_log["reports_only"])

    @patch("workflow.bids_runner.run_freesurfer", side_effect=fake_freesurfer)
    def test_freesurfer_pipeline_end_to_end(self, _mock_freesurfer) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output_dir = root / "out"
            work_dir = root / "work"
            license_path = root / "license.txt"
            license_path.write_text("fixture\n", encoding="utf-8")

            runner = BidsRunner(REPO_ROOT)
            published = runner.run_participant(
                bids_dir=MINIMAL_BIDS,
                output_dir=output_dir,
                work_dir=work_dir,
                participant_labels=["001"],
                fs_license_file=license_path,
                runtime="apptainer",
            )

            self.assertEqual(len(published), 1)
            metrics_path = published[0] / "sub-001_ses-1_desc-autohs_metrics.json"
            self.assertTrue(metrics_path.exists())

    def test_reports_only_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output_dir = root / "out"
            work_dir = root / "work"
            scan_work = work_dir / "sub-001_ses-1"
            t1w_name = "sub-001_ses-1_T1w.nii.gz"
            (scan_work / "input").mkdir(parents=True)
            shutil.copy2(MINIMAL_BIDS / "sub-001" / "ses-1" / "anat" / t1w_name, scan_work / "input" / t1w_name)
            install_fake_segmentation(scan_work, subject_id="job_0011", pipeline="fastsurfer")

            runner = BidsRunner(REPO_ROOT)
            published = runner.run_participant(
                bids_dir=MINIMAL_BIDS,
                output_dir=output_dir,
                work_dir=work_dir,
                participant_labels=["001"],
                reports_only=True,
            )

            self.assertEqual(len(published), 1)
            run_log = json.loads(
                (output_dir / "autohs" / "autohs_run.json").read_text(encoding="utf-8")
            )
            self.assertTrue(run_log["reports_only"])
            self.assertEqual(run_log["pipeline"], "reports-only")

    def test_bids_filter_file_selects_session(self) -> None:
        scans = discover_t1w_scans(
            MINIMAL_BIDS,
            participant_labels=["001"],
            bids_filter_file=FIXTURES / "bids_filter_session1.json",
        )
        self.assertEqual(len(scans), 1)
        self.assertEqual(scans[0].session_label, "1")

        empty = discover_t1w_scans(
            MINIMAL_BIDS,
            participant_labels=["001"],
            bids_filter_file=FIXTURES / "bids_filter_no_match.json",
        )
        self.assertEqual(empty, [])


class BidsAppCliIntegrationTests(unittest.TestCase):
    def test_run_py_version(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "run.py"), "--version"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("AutoHS", result.stdout)


if __name__ == "__main__":
    unittest.main()
