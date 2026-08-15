"""Tests for BIDS filter file parsing and reports-only work resolution."""

import json
import tempfile
import unittest
from pathlib import Path

from workflow.bids_filters import load_bids_filter_file, t1w_query_filters
from workflow.bids_runner import resolve_existing_work, scan_job_id, scan_work_subject_id
from workflow.bids_types import T1wScan


class BidsFilterTests(unittest.TestCase):
    def test_t1w_query_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "filters.json"
            path.write_text(
                json.dumps({"t1w": {"session": "1", "run": "2", "regex_search": "true"}}),
                encoding="utf-8",
            )
            filters, regex = t1w_query_filters(path)
            self.assertEqual(filters, {"session": "1", "run": "2"})
            self.assertTrue(regex)

    def test_invalid_filter_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "filters.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_bids_filter_file(path)


class ReportsOnlyWorkTests(unittest.TestCase):
    def test_resolve_existing_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scan_work = Path(tmp)
            (scan_work / "input").mkdir()
            (scan_work / "input" / "sub-001_ses-1_T1w.nii.gz").write_bytes(b"")
            seg_root = scan_work / "freesurfer" / "job_0011"
            seg_root.mkdir(parents=True)
            (seg_root / "stats").mkdir()

            scan = T1wScan("001", "1", Path("/tmp/t1w.nii.gz"))
            job_id = scan_job_id(scan)
            self.assertEqual(job_id, "001_1")
            self.assertEqual(scan_work_subject_id(scan), "sub-001_ses-1")

            input_copy, seg_dir, seg_subject_id = resolve_existing_work(scan_work, job_id)
            self.assertEqual(input_copy.name, "sub-001_ses-1_T1w.nii.gz")
            self.assertEqual(seg_dir, scan_work / "freesurfer")
            self.assertEqual(seg_subject_id, "job_0011")


if __name__ == "__main__":
    unittest.main()
