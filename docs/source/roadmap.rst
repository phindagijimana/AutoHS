Roadmap
=======

AutoHS targets the same **production bar** as mature BIDS Apps such as QSIPrep.
Status as of **v0.1.8**:

Stage 1 — Publish
-----------------

* Read the Docs configuration (``.readthedocs.yaml``) — **live** at `<https://autohs.readthedocs.io/en/latest/>`_
* Docker Hub image ``autohs/autohs`` via GitHub Actions — **workflow done**; add
  ``DOCKERHUB_*`` secrets (see :doc:`maintainers`)
* CI: tests + documentation build on every PR — **done**

Stage 2 — BIDS derivatives compliance
-------------------------------------

* BIDS Derivatives filenames (``desc-autohs`` entities) — **done**
* JSON sidecars with pipeline provenance — **done**
* ``Sources`` / ``SpatialReference`` metadata — **done**

Stage 3 — Feature completeness
------------------------------

* ``--bids-filter-file`` — **done**
* ``--reports-only`` — **done**
* ``--md-only-boilerplate`` — **done**
* ``--not-stop-on-first-crash`` — **done**

Stage 4 — Integration testing
-----------------------------

* CI on minimal BIDS fixture — **done**
* End-to-end tests with mocked segmentation — **done**
* Docker image smoke test in CI — **done**

Stage 5 — Ecosystem
-------------------

* ``CITATION.cff`` and ``CHANGELOG.md`` — **done**
* Apptainer ``.sif`` on GitHub Releases — **done**
* IDEAS sample dataset + citations — **done**
* BIDS website PR — **submitted** (see :doc:`bids_apps_hub`)
* Zenodo DOI — **pending** first GitHub release with Zenodo integration

Documentation depth (QSIPrep parity)
------------------------------------

* Installation, usage, outputs, preprocessing — **done**
* Sample data, citation, methods boilerplate — **done**
* FAQ and troubleshooting — **done**
* Live Read the Docs site — **done** (`autohs.readthedocs.io`)

Run ``./scripts/setup_ecosystem.sh`` for the remaining one-time maintainer steps.
