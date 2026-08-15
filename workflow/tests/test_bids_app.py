"""Tests for BIDS App discovery and layout."""

import tempfile
import unittest
from pathlib import Path

from workflow.bids_runner import discover_t1w_scans, derivative_subject_dir, T1wScan


class BidsDiscoveryTests(unittest.TestCase):
    def test_discover_session_t1w(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            anat = root / "sub-001" / "ses-1" / "anat"
            anat.mkdir(parents=True)
            t1w = anat / "sub-001_ses-1_T1w.nii.gz"
            t1w.write_bytes(b"")
            scans = discover_t1w_scans(root, participant_labels=["001"])
            self.assertEqual(len(scans), 1)
            self.assertEqual(scans[0].subject_label, "001")
            self.assertEqual(scans[0].session_label, "1")
            self.assertEqual(scans[0].t1w_path, t1w)

    def test_derivative_subject_dir(self) -> None:
        scan = T1wScan("001", "1", Path("/tmp/t1w.nii.gz"))
        out = derivative_subject_dir(Path("/out/autohs"), scan)
        self.assertEqual(out, Path("/out/autohs/sub-001/ses-1"))


if __name__ == "__main__":
    unittest.main()
