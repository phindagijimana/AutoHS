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

Stage 2 — BIDS derivatives compliance
-------------------------------------

* BIDS Derivatives filenames (``desc-autohs`` entities)
* JSON sidecars with pipeline provenance
* ``Sources`` / ``SpatialReference`` metadata where applicable

Stage 3 — Feature completeness
------------------------------

* ``--bids-filter-file`` (PyBIDS filters JSON for T1w selection)
* ``--reports-only`` (re-run AI-compute from existing segmentation in ``-w``)

Stage 4 — Integration testing
-----------------------------

* CI job on a minimal BIDS fixture dataset (``workflow/tests/fixtures/``)
* End-to-end smoke test with mocked FastSurfer/FreeSurfer segmentation

Stage 5 — Ecosystem
-------------------

* ``CITATION.cff`` and ``CHANGELOG.md`` for releases
* Apptainer ``.sif`` artifacts on GitHub releases (``.github/workflows/apptainer-release.yml``)
* BIDS website registration template (``registry/bids-website-apps.yml``) — see :doc:`bids_apps_hub`

**Maintainer action:** open a PR to `bids-standard/bids-website` ``apps.yml`` using the registry snippet.
