Privacy and public data
=======================

AutoHS is a public open-source BIDS App. This page summarizes what is (and is not)
published in the repository and documentation.

What we publish
---------------

* **Software source code** and BIDS App CLI
* **Documentation** at `<https://autohs.readthedocs.io/en/latest/>`_
* **Public sample data pointers** — IDEAS ``sub-1`` and ``sub-2`` (OpenNeuro ds005602, CC0).
  NIfTI files are downloaded via ``scripts/download_ideas_sample.sh`` and are not stored in git.
* **Synthetic test fixtures** — empty placeholder NIfTI for CI (``workflow/tests/fixtures/``)
* **Software author names** in ``CITATION.cff`` (standard for citable tools)

What we do not publish
----------------------

* FreeSurfer ``license.txt`` (gitignored; use ``license.txt.example``)
* Local job outputs under ``data/jobs/`` (gitignored)
* Non-public research cohorts or institutional datasets
* Patient identifiers, demographics, or clinical records

Sample dataset policy
---------------------

The IDEAS sample uses de-identified public scans. When adding examples or tests, use only:

* Public datasets (IDEAS, OpenNeuro, etc.) with proper citation, or
* Synthetic / empty fixtures for CI

HPC configuration
-----------------

Apptainer image paths (``FREESURFER_SIF``, ``FASTSURFER_SIF``) must be set in your
environment. The repository does **not** ship site-specific filesystem paths.

Reporting issues
----------------

If you believe sensitive information was committed by mistake, open a private security
issue with the maintainer or request history cleanup on GitHub.
