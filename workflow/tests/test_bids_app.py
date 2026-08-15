"""Tests for BIDS App discovery and derivatives layout."""

import json
import tempfile
import unittest
from pathlib import Path

from workflow.bids_runner import discover_t1w_scans, derivative_subject_dir
from workflow.bids_types import T1wScan
from workflow.derivatives import bids_uri, derivative_basename, derivative_paths, enrich_metrics_payload


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

    def test_derivative_filenames(self) -> None:
        scan = T1wScan("001", "1", Path("/bids/sub-001/ses-1/anat/sub-001_ses-1_T1w.nii.gz"))
        paths = derivative_paths(Path("/out/autohs"), scan)
        self.assertEqual(
            paths.metrics_json.name,
            "sub-001_ses-1_desc-autohs_metrics.json",
        )
        self.assertEqual(
            paths.report_pdf.name,
            "sub-001_ses-1_desc-autohs_report.pdf",
        )

    def test_bids_uri_and_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bids_dir = Path(tmp)
            t1w = bids_dir / "sub-001" / "ses-1" / "anat" / "sub-001_ses-1_T1w.nii.gz"
            t1w.parent.mkdir(parents=True)
            t1w.write_bytes(b"")
            scan = T1wScan("001", "1", t1w)
            uri = bids_uri(bids_dir, t1w)
            self.assertEqual(uri, "bids::sub-001/ses-1/anat/sub-001_ses-1_T1w.nii.gz")
            enriched = enrich_metrics_payload(
                {"job_id": "001", "metrics": {"asymmetry_index": 0.1}},
                scan=scan,
                bids_dir=bids_dir,
                pipeline="fastsurfer",
                version="0.1.0",
            )
            self.assertEqual(enriched["Sources"][0]["URL"], uri)
            self.assertEqual(enriched["SpatialReference"]["URL"], uri)
            self.assertEqual(enriched["GeneratedBy"][0]["Name"], "AutoHS")


if __name__ == "__main__":
    unittest.main()
