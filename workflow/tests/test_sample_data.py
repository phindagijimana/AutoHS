"""Tests for the IDEAS sample BIDS dataset."""

from __future__ import annotations

import unittest
from pathlib import Path

from workflow.bids_runner import discover_t1w_scans

IDEAS_BIDS = Path(__file__).resolve().parents[2] / "sample_data" / "ideas_bids"
T1W_SUB1 = IDEAS_BIDS / "sub-1" / "anat" / "sub-1_T1w.nii.gz"


class IdeasSampleDataTests(unittest.TestCase):
    def test_ideas_sample_metadata_present(self) -> None:
        self.assertTrue((IDEAS_BIDS / "dataset_description.json").exists())
        self.assertTrue((IDEAS_BIDS / "SOURCES.json").exists())
        self.assertTrue((IDEAS_BIDS / "README.md").exists())

    def test_discover_ideas_t1w_when_downloaded(self) -> None:
        if not T1W_SUB1.exists():
            self.skipTest("Run ./scripts/download_ideas_sample.sh to fetch IDEAS NIfTI files")

        scans = discover_t1w_scans(IDEAS_BIDS, participant_labels=["1", "2"])
        labels = sorted({scan.subject_label for scan in scans})
        self.assertEqual(labels, ["1", "2"])
        self.assertEqual(len(scans), 2)


if __name__ == "__main__":
    unittest.main()
