import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

project = "NeuroInsight-AutoHS"
copyright = "2025, University of Rochester"
author = "Philbert Ndagijimana"
release = open(Path(__file__).resolve().parents[2] / "version").read().strip()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
