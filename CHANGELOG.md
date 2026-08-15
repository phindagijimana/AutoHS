# Changelog

All notable changes to AutoHS are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/phindagijimana/AutoHS/releases/tag/v0.1.0
