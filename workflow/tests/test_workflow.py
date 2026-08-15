"""Tests for workflow pipeline loading and validation."""

import unittest
from pathlib import Path

from workflow.load_pipeline import PipelineLoader, PipelineValidationError


class WorkflowPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.loader = PipelineLoader()

    def test_load_pipeline(self) -> None:
        pipeline = self.loader.load()
        self.assertEqual(pipeline.data["name"], "neuroinsight")
        self.assertEqual(len(pipeline.steps), 18)
        self.assertEqual(len(pipeline.freesurfer_substeps), 17)

    def test_execution_order_count(self) -> None:
        self.loader.load()
        order = self.loader.get_execution_order()
        self.assertEqual(len(order), 18)
        self.assertEqual(order[0], "upload-validate")
        self.assertEqual(order[-1], "pdf-report")

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
        step = self.loader.get_step("calculate-asymmetry")
        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.data["progress"], 95)

    def test_freesurfer_subpipeline_loaded(self) -> None:
        pipeline = self.loader.load()
        self.assertIsNotNone(pipeline.freesurfer_subpipeline)
        assert pipeline.freesurfer_subpipeline is not None
        self.assertEqual(
            pipeline.freesurfer_subpipeline["parent_step"],
            "freesurfer-segmentation",
        )
        micro_order = pipeline.freesurfer_subpipeline["micro_execution_order"]
        self.assertEqual(len(micro_order), 17)

    def test_code_reference_files_exist(self) -> None:
        pipeline = self.loader.load()
        if not (Path(__file__).resolve().parent.parent.parent / "backend").exists():
            self.skipTest("Standalone workflow repo — code refs point to external NeuroInsight app")
        repo_root = Path(__file__).resolve().parent.parent.parent
        for step in list(pipeline.steps.values()) + list(pipeline.freesurfer_substeps.values()):
            ref = step.code_reference
            if ref and ref.get("file"):
                self.assertTrue(
                    (repo_root / ref["file"]).exists(),
                    f"Missing file for step {step.id}",
                )


if __name__ == "__main__":
    unittest.main()
