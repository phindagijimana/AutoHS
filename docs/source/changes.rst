Changes
=======

Release history for AutoHS. See also ``CHANGELOG.md`` in the repository root.

0.1.7 (2026-08-16)
------------------

* Mock AI-compute in integration tests; invoke CI test modules explicitly

0.1.6 (2026-08-16)
------------------

* Harden BIDS discovery and CI environment (``PYTHONPATH``, PyBIDS error handling)

0.1.5 (2026-08-16)
------------------

* Run native AI-compute in-process (fixes CI subprocess failures)
* Fix unclosed ``version`` file handles during derivative publishing

0.1.4 (2026-08-16)
------------------

* Fall back to filesystem T1w discovery when PyBIDS finds no scans (unless a
  ``--bids-filter-file`` is provided)

0.1.3 (2026-08-15)
------------------

* Pass ``PYTHONPATH`` to native AI-compute subprocess (fixes CI integration tests)

0.1.2 (2026-08-15)
------------------

CI and release workflow fixes.

* Native AI-compute uses the active ``python`` interpreter in GitHub Actions
* Apptainer release workflow installs from the official PPA

0.1.1 (2026-08-15)
------------------

Production-ready BIDS App release (Stages 2–5 of the QSIPrep-level roadmap).

* BIDS Derivatives layout (``desc-autohs`` outputs)
* ``--bids-filter-file`` and ``--reports-only``
* Integration tests on a minimal BIDS fixture
* ``CITATION.cff``, changelog, Apptainer release workflow
* BIDS website registration template

0.1.0 (2026-08-15)
------------------

Initial public BIDS App release.

* BIDS App CLI with FreeSurfer / FastSurfer backends
* BIDS Derivatives layout (``desc-autohs`` outputs)
* ``--bids-filter-file`` and ``--reports-only``
* Read the Docs, CI, Docker Hub publish workflow
* Apptainer ``.sif`` GitHub release artifacts
* Integration tests on a minimal BIDS fixture
