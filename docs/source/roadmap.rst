Roadmap
=======

AutoHS targets the same **production bar** as mature BIDS Apps such as QSIPrep.
Status as of **v0.1.10**:

Stage 1 — Publish
-----------------

* Read the Docs — **live** at `<https://autohs.readthedocs.io/en/latest/>`_
* Docker Hub ``autohs/autohs`` — **workflow done**; add ``DOCKERHUB_*`` secrets to publish
* CI: tests + documentation build on every PR — **done**
* Root ``LICENSE`` (MIT) — **done**

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
* BIDS website listing — **deferred** (see :doc:`bids_apps_hub`)
* Zenodo — **GitHub integration enabled**; add concept DOI to ``CITATION.cff`` after first archived release

Documentation depth (QSIPrep parity)
------------------------------------

* Theory, installation, usage, outputs, preprocessing — **done**
* Sample data, citation, methods boilerplate — **done**
* FAQ, troubleshooting, contributing — **done**
* README focused on BIDS App; run examples centralized in quickstart — **done**

Run ``./scripts/setup_ecosystem.sh`` for remaining one-time maintainer steps (Docker Hub secrets, Zenodo DOI).
