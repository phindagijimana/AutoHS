# Changelog

All notable changes to AutoHS are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.8] - 2026-08-16

### Added

- IDEAS sample dataset (`sample_data/ideas_bids/`) with download script and citations
- Expanded `CITATION.cff` and docs for IDEAS, FreeSurfer, FastSurfer, and BIDS references
- Maintainer helper `scripts/setup_ecosystem.sh` (Read the Docs, Docker Hub, Zenodo checklist)
- FAQ, troubleshooting, and methods boilerplate documentation pages
- `--md-only-boilerplate` and `--not-stop-on-first-crash` CLI flags
- Docker image smoke test job in CI

### Fixed

- Removed invalid Zenodo placeholder DOI from `CITATION.cff` (pending first Zenodo release)

## [0.1.7] - 2026-08-16

### Fixed

- Mock AI-compute in integration tests for reliable GitHub Actions runs
- Invoke test modules explicitly in CI

## [0.1.6] - 2026-08-16

### Fixed

- Harden BIDS discovery when PyBIDS is unavailable or raises during indexing
- Normalize subject/session labels to strings; set ``PYTHONPATH`` in CI

## [0.1.5] - 2026-08-16

### Fixed

- Run native AI-compute in-process to avoid subprocess import/warning failures in CI
- Read ``version`` file without leaking unclosed file handles

## [0.1.4] - 2026-08-16

### Fixed

- Fall back to filesystem T1w discovery when PyBIDS returns no scans (unless
  ``--bids-filter-file`` is set)

## [0.1.3] - 2026-08-15

### Fixed

- Pass ``PYTHONPATH`` to the native AI-compute subprocess so CI can import ``ai_compute``

## [0.1.2] - 2026-08-15

### Fixed

- Use the active ``python`` interpreter for native AI-compute in CI (GitHub Actions)
- Install Apptainer from the official PPA in the release workflow

## [0.1.1] - 2026-08-15

### Added

- BIDS Derivatives layout with `desc-autohs` filenames and provenance sidecars
- `--bids-filter-file` and `--reports-only` BIDS App modes
- Integration tests on a minimal BIDS fixture dataset
- `CITATION.cff`, `CHANGELOG.md`, and BIDS website registry snippet
- Apptainer `.sif` GitHub release workflow

## [0.1.0] - 2026-08-15

### Added

- BIDS App entrypoint (`run.py` / `run`) with QSIPrep-style CLI groups
- FreeSurfer and FastSurfer segmentation backends (`--fastsurfer`)
- BIDS Derivatives outputs with `desc-autohs` filenames and provenance sidecars
- `--bids-filter-file` and `--reports-only` participant modes
- Legacy queue workflow (`./AutoHS submit`) with Slurm/Apptainer HPC scripts
- Sphinx documentation (Read the Docs) and CI (tests + docs build)
- Docker publish workflow for `autohs/autohs` on semver tags
- Apptainer `.sif` release workflow attached to GitHub releases
- Minimal BIDS integration test fixture and end-to-end CI smoke tests
- `CITATION.cff` for software and publication metadata

[0.1.7]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.7
[0.1.6]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.6
[0.1.5]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.5
[0.1.4]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.4
[0.1.3]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.3
[0.1.2]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.2
[0.1.1]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.1
[0.1.0]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.0
