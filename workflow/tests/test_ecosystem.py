"""Tests for Stage 5 ecosystem metadata files."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


class EcosystemMetadataTests(unittest.TestCase):
    def test_citation_cff(self) -> None:
        path = REPO_ROOT / "CITATION.cff"
        self.assertTrue(path.exists(), "CITATION.cff is required for releases")
        content = path.read_text(encoding="utf-8")
        self.assertIn("cff-version:", content)
        self.assertIn("title: AutoHS", content)
        self.assertIn("preferred-citation:", content)

    def test_changelog(self) -> None:
        path = REPO_ROOT / "CHANGELOG.md"
        self.assertTrue(path.exists())
        content = path.read_text(encoding="utf-8")
        self.assertIn("[0.1.0]", content)

    def test_bids_registry_snippet(self) -> None:
        path = REPO_ROOT / "registry" / "bids-website-apps.yml"
        self.assertTrue(path.exists())
        content = path.read_text(encoding="utf-8")
        self.assertIn("phindagijimana/AutoHS", content)
        self.assertIn("autohs/autohs", content)

    def test_license(self) -> None:
        path = REPO_ROOT / "LICENSE"
        self.assertTrue(path.exists(), "MIT LICENSE is required at repository root")
        content = path.read_text(encoding="utf-8")
        self.assertIn("MIT License", content)


if __name__ == "__main__":
    unittest.main()
