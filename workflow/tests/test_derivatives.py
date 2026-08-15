"""Tests for BIDS derivatives publishing."""

import json
import tempfile
import unittest
from pathlib import Path

from workflow.bids_types import T1wScan
from workflow.derivatives import derivative_paths, publish_bids_derivatives


class DerivativesPublishTests(unittest.TestCase):
    def test_publish_bids_derivatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bids_dir = root / "bids"
            t1w = bids_dir / "sub-001" / "ses-1" / "anat" / "sub-001_ses-1_T1w.nii.gz"
            t1w.parent.mkdir(parents=True)
            t1w.write_bytes(b"")

            work_output = root / "work" / "output"
            work_output.mkdir(parents=True)
            (work_output / "report.json").write_text(
                json.dumps(
                    {
                        "job_id": "001",
                        "metrics": {
                            "left_hippocampus_mm3": 5000.0,
                            "right_hippocampus_mm3": 5200.0,
                            "asymmetry_index": -0.02,
                            "laterality": "Symmetric",
                            "hs_classification": "Balanced (No HS)",
                        },
                    }
                ),
                encoding="utf-8",
            )
            (work_output / "summary.txt").write_text("summary", encoding="utf-8")

            output_root = root / "out" / "autohs"
            scan = T1wScan("001", "1", t1w)
            paths = derivative_paths(output_root, scan)
            publish_bids_derivatives(
                work_output,
                paths,
                scan=scan,
                bids_dir=bids_dir,
                pipeline="fastsurfer",
                version="0.1.0",
            )

            self.assertTrue(paths.metrics_json.exists())
            payload = json.loads(paths.metrics_json.read_text(encoding="utf-8"))
            self.assertIn("Sources", payload)
            self.assertEqual(payload["metrics"]["asymmetry_index"], -0.02)
            self.assertTrue(paths.summary_txt.exists())
            self.assertTrue((paths.subject_dir / "report.json").exists())


if __name__ == "__main__":
    unittest.main()
