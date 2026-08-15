Roadmap
=======

AutoHS is being brought to the same **production bar** as mature BIDS Apps such as
QSIPrep. Work proceeds in ordered stages.

Stage 1 — Publish
-----------------

* Read the Docs configuration (``.readthedocs.yaml``)
* Docker Hub image ``autohs/autohs`` via GitHub Actions
* CI: tests + documentation build on every PR

Connect Read the Docs and Docker Hub secrets (see :doc:`maintainers`).

Stage 2 — BIDS derivatives compliance (current)
-----------------------------------------------

* BIDS Derivatives filenames (``desc-autohs`` entities)
* JSON sidecars with pipeline provenance
* ``sources`` / ``SpatialReference`` metadata where applicable

Stage 3 — Feature completeness
------------------------------

* Implement ``--bids-filter-file`` (PyBIDS filters JSON)
* Implement ``--reports-only`` (re-run AI-compute from existing segmentation)

Stage 4 — Integration testing
-------------------------------

* CI job on a minimal public BIDS dataset
* End-to-end smoke test (FastSurfer + report generation)

Stage 5 — Ecosystem
-------------------

* Register on the `BIDS Apps hub <https://github.com/bids-apps>`_
* Release Apptainer ``.sif`` artifacts alongside Docker tags
* Versioned changelog and citation file (``CITATION.cff``)
