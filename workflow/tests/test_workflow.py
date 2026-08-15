"""Tests for workflow pipeline loading and validation."""

import unittest
from pathlib import Path

from workflow.load_pipeline import PipelineLoader, PipelineValidationError


class WorkflowPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.loader = PipelineLoader()

    def test_load_pipeline(self) -> None:
        pipeline = self.loader.load()
        self.assertEqual(pipeline.data["name"], "autohs")
        self.assertEqual(len(pipeline.steps), 2)
        self.assertEqual(len(pipeline.freesurfer_substeps), 17)

    def test_execution_order_count(self) -> None:
        self.loader.load()
        order = self.loader.get_execution_order()
        self.assertEqual(len(order), 2)
        self.assertEqual(order[0], "freesurfer-processing")
        self.assertEqual(order[1], "ai-compute")

    def test_validate_passes(self) -> None:
        self.loader.load()
        errors = self.loader.validate(raise_on_error=False)
        self.assertEqual(errors, [])

    def test_validate_raises_on_missing_step(self) -> None:
        pipeline = self.loader.load()
        pipeline.data["execution_order"].append({"step": "nonexistent-step"})
        self.loader._pipeline = pipeline

        with self.assertRaises(PipelineValidationError) as ctx:
            self.loader.validate()

        self.assertTrue(any("nonexistent-step" in error for error in ctx.exception.errors))

    def test_get_step(self) -> None:
        self.loader.load()
        step = self.loader.get_step("ai-compute")
        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.id, "ai-compute")

    def test_freesurfer_subpipeline_loaded(self) -> None:
        pipeline = self.loader.load()
        self.assertIsNotNone(pipeline.freesurfer_subpipeline)
        assert pipeline.freesurfer_subpipeline is not None
        self.assertEqual(
            pipeline.freesurfer_subpipeline["parent_step"],
            "freesurfer-processing",
        )


class AIComputeTests(unittest.TestCase):
    def test_asymmetry_formula(self) -> None:
        from ai_compute.asymmetry import calculate_asymmetry_index

        self.assertEqual(calculate_asymmetry_index(1000, 900), round(100 / 1900, 4))

    def test_laterality_thresholds(self) -> None:
        from ai_compute.asymmetry import classify_laterality

        self.assertEqual(classify_laterality(0.06), "Left > Right")
        self.assertEqual(classify_laterality(-0.06), "Right > Left")
        self.assertEqual(classify_laterality(0.02), "Symmetric")

    def test_hs_thresholds(self) -> None:
        from ai_compute.asymmetry import classify_hs_laterality

        self.assertIn("Right HS suspected", classify_hs_laterality(0.05))
        self.assertIn("Left HS suspected", classify_hs_laterality(-0.08))
        self.assertIn("Balanced", classify_hs_laterality(0.0))

    def test_parse_aseg_stats(self) -> None:
        from ai_compute.extract import parse_aseg_stats
        import tempfile

        content = "# comment\n1  17  100  3500.0  Left-Hippocampus\n2  53  90  3200.0  Right-Hippocampus\n"
        with tempfile.NamedTemporaryFile("w", suffix=".stats", delete=False) as tmp:
            tmp.write(content)
            path = Path(tmp.name)
        volumes = parse_aseg_stats(path)
        self.assertEqual(volumes["left"], 3500.0)
        self.assertEqual(volumes["right"], 3200.0)
        path.unlink()

    def test_find_aseg_dkt_stats(self) -> None:
        from ai_compute.extract import find_aseg_stats
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stats_dir = root / "job_test" / "stats"
            stats_dir.mkdir(parents=True)
            stats_file = stats_dir / "aseg+DKT.stats"
            stats_file.write_text(
                "1  17  100  3500.0  Left-Hippocampus\n2  53  90  3200.0  Right-Hippocampus\n",
                encoding="utf-8",
            )
            found = find_aseg_stats(root, "job_test")
            self.assertEqual(found, stats_file)


class WorkflowRunnerTests(unittest.TestCase):
    def test_submit_fastsurfer_flag(self) -> None:
        import tempfile
        from workflow.runner import WorkflowRunner

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            nii = root / "scan.nii.gz"
            nii.write_bytes(b"")
            runner = WorkflowRunner(root)
            job_id = runner.submit(nii, fastsurfer=True)
            job = runner.queue.get_job(job_id)
            self.assertEqual(job.segmentation, "fastsurfer")


if __name__ == "__main__":
    unittest.main()
