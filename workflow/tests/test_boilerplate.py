"""Tests for methods boilerplate generation."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


class MethodsBoilerplateTests(unittest.TestCase):
    def test_boilerplate_module_freesurfer(self) -> None:
        from workflow.boilerplate import methods_boilerplate

        text = methods_boilerplate(version="0.1.8", fastsurfer=False)
        self.assertIn("FreeSurfer", text)
        self.assertIn("0.1.8", text)
        self.assertIn("Ndagijimana", text)

    def test_boilerplate_module_fastsurfer(self) -> None:
        from workflow.boilerplate import methods_boilerplate

        text = methods_boilerplate(version="0.1.8", fastsurfer=True)
        self.assertIn("FastSurfer", text)
        self.assertNotIn("FreeSurfer 7.4.1", text)

    def test_run_py_md_only_boilerplate(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "run.py"), "--md-only-boilerplate"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("AutoHS", result.stdout)
        self.assertIn("FreeSurfer", result.stdout)


if __name__ == "__main__":
    unittest.main()
